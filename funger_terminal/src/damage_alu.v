// ============================================================================
// Pokemon Lite: Terror & Starvation - Damage ALU (damage_alu.v)
// Computes combat clash with DEF reduction, 6.25% Crit, and flee failure penalty
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
    output reg  [7:0] p1_damage,
    output reg  [7:0] p2_damage,
    output reg  [7:0] p1_flee_penalty
);

    reg [7:0] raw_dmg_1to2;
    reg [7:0] raw_dmg_2to1;
    reg [7:0] eff_dmg_1to2;
    reg [7:0] eff_dmg_2to1;

    always @(*) begin
        // 1. Calculate Base Damage with Defense Mitigations: max(2, ATK - (DEF >> 1))
        if (p1_base_atk > (p2_def >> 1)) begin
            raw_dmg_1to2 = p1_base_atk - (p2_def >> 1);
            if (raw_dmg_1to2 < 8'd2) raw_dmg_1to2 = 8'd2;
        end else begin
            raw_dmg_1to2 = 8'd2;
        end

        if (p2_base_atk > (p1_def >> 1)) begin
            raw_dmg_2to1 = p2_base_atk - (p1_def >> 1);
            if (raw_dmg_2to1 < 8'd2) raw_dmg_2to1 = 8'd2;
        end else begin
            raw_dmg_2to1 = 8'd2;
        end

        // 2. Critical Hit Multiplier (6.25% chance when rng_bits == 4'b1111: 1.5x damage)
        if (rng_bits == 4'b1111) begin
            eff_dmg_1to2 = raw_dmg_1to2 + (raw_dmg_1to2 >> 1);
        end else begin
            eff_dmg_1to2 = raw_dmg_1to2;
        end

        // Enemy crit check (when inverted rng_bits == 4'b1111)
        if (rng_bits == 4'b0000) begin
            eff_dmg_2to1 = raw_dmg_2to1 + (raw_dmg_2to1 >> 1);
        end else begin
            eff_dmg_2to1 = raw_dmg_2to1;
        end

        // 3. Compute 30% current HP penalty if player fails to flee
        if (is_flee_failed) begin
            p1_flee_penalty = (p1_curr_hp * 8'd3) / 8'd10;
            if (p1_flee_penalty == 8'd0 && p1_curr_hp > 8'd0)
                p1_flee_penalty = 8'd1; // Minimum 1 HP penalty
        end else begin
            p1_flee_penalty = 8'd0;
        end

        // 4. Action clash evaluation
        case ({p1_action, p2_action})
            {`ACTION_ATTACK, `ACTION_ATTACK}: begin
                // Mutual assault: both sustain opposing attack power
                p1_damage = eff_dmg_2to1;
                p2_damage = eff_dmg_1to2;
            end

            {`ACTION_ATTACK, `ACTION_DEFEND}: begin
                // Opponent guards: damage reduced by 75%
                p1_damage = 8'd0;
                p2_damage = (eff_dmg_1to2 * 8'd25) / 8'd100;
                if (p2_damage == 8'd0 && eff_dmg_1to2 > 8'd0) p2_damage = 8'd1;
            end

            {`ACTION_DEFEND, `ACTION_ATTACK}: begin
                // Player guards: incoming damage reduced by 75%
                p1_damage = (eff_dmg_2to1 * 8'd25) / 8'd100;
                if (p1_damage == 8'd0 && eff_dmg_2to1 > 8'd0) p1_damage = 8'd1;
                p2_damage = 8'd0;
            end

            {`ACTION_DEFEND, `ACTION_DEFEND}: begin
                // Mutual guard: no damage inflicted
                p1_damage = 8'd0;
                p2_damage = 8'd0;
            end

            {`ACTION_ITEM_OR_FLEE, `ACTION_ATTACK}: begin
                // Player consumes turn (using bag or failed flee): free enemy strike
                p1_damage = eff_dmg_2to1 + p1_flee_penalty;
                p2_damage = 8'd0;
            end

            {`ACTION_ITEM_OR_FLEE, `ACTION_DEFEND}: begin
                // Player consumes turn while enemy guards
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
