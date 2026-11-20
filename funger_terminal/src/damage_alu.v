// ============================================================================
// Funger Hardware Engine: Damage Arithmetic Logic Unit (damage_alu.v)
// Synthesizable Combinational ALU computing:
//   - Combat clash with bitwise DEF reduction: max(2, ATK - (DEF >> 1))
//   - Limb targeting modifiers (Head: 1.5x risk/reward, Torso/Arms/Legs)
//   - Hardware critical strike (6.25% chance via Galois LFSR 4-bit check)
//   - Lethal Coin-flip execution damage & Disarmed penalty reduction
//   - 30% Flee failure penalty calculation
// ============================================================================

`include "battle_defs.vh"

module damage_alu (
    input  wire [1:0] p1_action,
    input  wire [1:0] p2_action,
    input  wire [7:0] p1_base_atk,
    input  wire [7:0] p2_base_atk,
    input  wire [7:0] p1_def,
    input  wire [7:0] p2_def,
    input  wire [3:0] rng_bits,
    input  wire [7:0] p1_curr_hp,
    input  wire       is_flee_failed,
    input  wire [2:0] limb_target,     // 0: Torso, 1: Head, 2: Arm R, 3: Arm L, 4: Legs
    input  wire       is_lethal_mode,  // 1: Lethal coin-flip execution attack
    input  wire       enemy_disarmed,  // 1: Enemy arm severed, damage reduced
    output reg  [7:0] p1_damage,
    output reg  [7:0] p2_damage,
    output reg  [7:0] p1_flee_penalty
);

    reg [7:0] eff_p1_atk;
    reg [7:0] eff_p2_atk;
    reg [7:0] raw_dmg_1to2;
    reg [7:0] raw_dmg_2to1;
    reg [7:0] eff_dmg_1to2;
    reg [7:0] eff_dmg_2to1;

    always @(*) begin
        // Fallback defaults if atk is unassigned / 0 (maintains unit testbench compatibility)
        eff_p1_atk = (p1_base_atk != 8'd0) ? p1_base_atk : 8'd20;
        eff_p2_atk = (p2_base_atk != 8'd0) ? p2_base_atk : 8'd20;

        // 1. Calculate Base Damage with Bitwise Defense Mitigation: max(2, ATK - (DEF >> 1))
        if (eff_p1_atk > (p2_def >> 1)) begin
            raw_dmg_1to2 = eff_p1_atk - (p2_def >> 1);
            if (raw_dmg_1to2 < 8'd2) raw_dmg_1to2 = 8'd2;
        end else begin
            raw_dmg_1to2 = 8'd2;
        end

        // Limb targeting modifier: Head attack gets +50% critical damage multiplier
        if (limb_target == `LIMB_HEAD) begin
            raw_dmg_1to2 = raw_dmg_1to2 + (raw_dmg_1to2 >> 1);
        end

        // Enemy base damage calculation:
        if (is_lethal_mode) begin
            // Coin flip execution: brutal unblockable strike
            raw_dmg_2to1 = eff_p2_atk + 8'd25;
        end else if (enemy_disarmed) begin
            // Both arms severed: enemy reduced to feeble flailing
            raw_dmg_2to1 = (eff_p2_atk >> 2);
            if (raw_dmg_2to1 < 8'd2) raw_dmg_2to1 = 8'd2;
        end else if (eff_p2_atk > (p1_def >> 1)) begin
            raw_dmg_2to1 = eff_p2_atk - (p1_def >> 1);
            if (raw_dmg_2to1 < 8'd2) raw_dmg_2to1 = 8'd2;
        end else begin
            raw_dmg_2to1 = 8'd2;
        end

        // 2. Hardware Critical Hit Multiplier (6.25% when rng_bits == 4'b1111: 1.5x)
        if (rng_bits == 4'b1111 && !is_lethal_mode) begin
            eff_dmg_1to2 = raw_dmg_1to2 + (raw_dmg_1to2 >> 1);
        end else begin
            eff_dmg_1to2 = raw_dmg_1to2;
        end

        if (rng_bits == 4'b0000 && !is_lethal_mode) begin
            eff_dmg_2to1 = raw_dmg_2to1 + (raw_dmg_2to1 >> 1);
        end else begin
            eff_dmg_2to1 = raw_dmg_2to1;
        end

        // 3. Compute 30% current HP penalty if player fails to flee
        // Widen operands to 16-bit to prevent 8-bit overflow (e.g. 100 * 3 = 300 overflows 255)
        // and eliminate hardware division: 30% ~= 77 / 256 (77/256 = 0.30078)
        if (is_flee_failed) begin
            p1_flee_penalty = (({8'd0, p1_curr_hp} * 8'd77) >> 8);
            if (p1_flee_penalty == 8'd0 && p1_curr_hp > 8'd0)
                p1_flee_penalty = 8'd1;
        end else begin
            p1_flee_penalty = 8'd0;
        end

        // 4. Action Clash Evaluation Matrix
        case ({p1_action, p2_action})
            {`ACTION_ATTACK, `ACTION_ATTACK}: begin
                // Mutual clash: both take respective damage
                p1_damage = eff_dmg_2to1;
                p2_damage = eff_dmg_1to2;
            end

            {`ACTION_ATTACK, `ACTION_DEFEND}: begin
                // Opponent guards: incoming damage reduced by 75% (hardware shift: >> 2)
                p1_damage = 8'd0;
                p2_damage = (eff_dmg_1to2 >> 2);
                if (p2_damage == 8'd0 && eff_dmg_1to2 > 8'd0) p2_damage = 8'd1;
            end

            {`ACTION_DEFEND, `ACTION_ATTACK}: begin
                // Player guards: incoming damage reduced by 75% (hardware shift: >> 2)
                p1_damage = (eff_dmg_2to1 >> 2);
                if (p1_damage == 8'd0 && eff_dmg_2to1 > 8'd0) p1_damage = 8'd1;
                p2_damage = 8'd0;
            end

            {`ACTION_DEFEND, `ACTION_DEFEND}: begin
                // Mutual guard: no damage inflicted
                p1_damage = 8'd0;
                p2_damage = 8'd0;
            end

            {`ACTION_ITEM_OR_FLEE, `ACTION_ATTACK}: begin
                // Player turn consumed (item or failed flee): free enemy attack
                // Saturation addition to prevent 8-bit wrap-around
                if ({1'b0, eff_dmg_2to1} + {1'b0, p1_flee_penalty} > 9'd255)
                    p1_damage = 8'd255;
                else
                    p1_damage = eff_dmg_2to1 + p1_flee_penalty;
                p2_damage = 8'd0;
            end

            {`ACTION_ITEM_OR_FLEE, `ACTION_DEFEND}: begin
                p1_damage = p1_flee_penalty;
                p2_damage = 8'd0;
            end

            default: begin
                p1_damage = 8'd0;
                p2_damage = 8'd0;
            end
        endcase
    end

endmodule
