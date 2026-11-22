// ============================================================================
// Funger Hardware Engine: Tactical Stance Coprocessor (tactical_stance_unit.v)
// Inspired by: Dynamic Power Grid Routing (project2_stellar_void)
// Pure Synthesizable RTL Coprocessor computing:
//   - Stance 0 (Balanced): Standard baseline ATK & DEF
//   - Stance 1 (Berserk): +25% ATK boost (ATK + (ATK >> 2)), -25% DEF penalty
//   - Stance 2 (Iron Guard): +50% DEF boost (DEF + (DEF >> 1)), Turn HP regen
//   - Stance 3 (Agile): +25% Evasion, +25% Flee probability (75% / 90% Flee)
// ============================================================================

`timescale 1ns / 1ps
`include "battle_defs.vh"

module tactical_stance_unit (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        stance_cmd_en,
    input  wire [1:0]  stance_select,
    input  wire [7:0]  base_atk,
    input  wire [7:0]  base_def,
    input  wire        is_hard_mode,

    output reg  [1:0]  curr_stance,
    output reg  [7:0]  eff_atk,
    output reg  [7:0]  eff_def,
    output reg  [6:0]  evasion_pct,
    output reg  [6:0]  flee_success_pct,
    output reg  [7:0]  turn_regen_hp
);

    reg [1:0] r_stance;

    // Stance Register Update (Synchronous with Active-Low Reset)
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            r_stance <= `STANCE_BALANCED;
        end else if (stance_cmd_en) begin
            r_stance <= stance_select;
        end
    end

    // Combinational Stance Modifier Netlist (Pure Bit-Shifts, Zero Division)
    always @(*) begin
        curr_stance = r_stance;

        case (r_stance)
            `STANCE_BERSERK: begin
                // Berserk: +25% ATK (with saturation clamping), -25% DEF
                if ({1'b0, base_atk} + {3'b0, base_atk[7:2]} > 9'd255)
                    eff_atk = 8'd255;
                else
                    eff_atk = base_atk + (base_atk >> 2);

                if (base_def > (base_def >> 2))
                    eff_def = base_def - (base_def >> 2);
                else
                    eff_def = 8'd1;

                evasion_pct      = 7'd5;
                flee_success_pct = 7'd40;
                turn_regen_hp    = 8'd0;
            end

            `STANCE_IRON_GUARD: begin
                // Iron Guard: +50% DEF (with saturation clamping), -12.5% ATK, Regenerates HP each turn
                if (base_atk > (base_atk >> 3))
                    eff_atk = base_atk - (base_atk >> 3);
                else
                    eff_atk = 8'd1;

                if ({1'b0, base_def} + {2'b0, base_def[7:1]} > 9'd255)
                    eff_def = 8'd255;
                else
                    eff_def = base_def + (base_def >> 1);

                evasion_pct      = 7'd15;
                flee_success_pct = 7'd50;
                turn_regen_hp    = (is_hard_mode) ? 8'd3 : 8'd6;
            end

            `STANCE_AGILE: begin
                // Agile: Standard ATK & DEF, +25% Evasion, High Flee Success (75% Hard, 90% Normal)
                eff_atk          = base_atk;
                eff_def          = base_def;
                evasion_pct      = 7'd35;
                flee_success_pct = (is_hard_mode) ? 7'd75 : 7'd90;
                turn_regen_hp    = 8'd0;
            end

            default: begin // `STANCE_BALANCED`
                // Balanced: 1.0x Baseline
                eff_atk          = base_atk;
                eff_def          = base_def;
                evasion_pct      = 7'd10;
                flee_success_pct = (is_hard_mode) ? 7'd50 : 7'd65;
                turn_regen_hp    = 8'd0;
            end
        endcase

        // Minimum floor of 1 for attack and defense to prevent zero-stat lockup
        if (eff_atk == 8'd0) eff_atk = 8'd1;
        if (eff_def == 8'd0) eff_def = 8'd1;
    end

endmodule
