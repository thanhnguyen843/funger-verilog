// ============================================================================
// Funger Hardware Engine: Sanity & Hunger Coprocessor (sanity_meter_unit.v)
// Inspired by: Environmental Entropy Unit (project3_chrono_tactics)
// Pure Synthesizable RTL Coprocessor managing:
//   - Environmental Horror: Mind decay and Labyrinth Hunger accumulation
//   - Dual Difficulty Profiles:
//       * Fear & Hunger (Normal): Forgiving ticks (16 steps/hunger, 32 steps/mind)
//       * Terror & Starvation (Hard): Brutal pressure (4 steps/hunger, 8 steps/mind)
//   - Panic State Detection: Drops ATK when Mind falls below 20
//   - Starvation Penalty Generation: Signals HP loss when Hunger reaches 90+
// ============================================================================

`timescale 1ns / 1ps
`include "battle_defs.vh"

module sanity_meter_unit (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        is_hard_mode,

    // Environmental event pulses (1-cycle strobes)
    input  wire        step_pulse,
    input  wire        encounter_pulse,
    input  wire        panic_strike_pulse,

    // Restoration Strobes (Items / Skills)
    input  wire        mind_restore_en,
    input  wire [7:0]  mind_restore_val,
    input  wire        hunger_restore_en,
    input  wire [7:0]  hunger_restore_val,

    // Status Outputs
    output wire [7:0]  mind_level,
    output wire [7:0]  hunger_level,
    output wire        is_panic,
    output wire        is_starving,
    output wire [6:0]  atk_penalty_pct,
    output reg         starve_dmg_pulse
);

    reg [7:0] r_mind;
    reg [7:0] r_hunger;
    reg [4:0] r_step_counter;

    reg [7:0] step_mind_decay;
    reg [7:0] event_mind_loss;
    reg [7:0] total_mind_loss;
    reg [8:0] next_mind_calc;

    reg [7:0] step_hunger_gain;
    reg [8:0] next_hunger_calc;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            r_mind           <= 8'd100;
            r_hunger         <= 8'd0;
            r_step_counter   <= 5'd0;
            starve_dmg_pulse <= 1'b0;
        end else begin
            starve_dmg_pulse <= 1'b0;

            // Step counter update
            if (step_pulse) begin
                r_step_counter <= r_step_counter + 5'd1;

                // Starvation health drain trigger
                if (r_hunger >= 8'd90) begin
                    if (is_hard_mode) begin
                        if (r_step_counter[1:0] == 2'b00)
                            starve_dmg_pulse <= 1'b1;
                    end else begin
                        if (r_step_counter[3:0] == 4'b0000)
                            starve_dmg_pulse <= 1'b1;
                    end
                end
            end

            // 1. Unified Mind Arbitration (Zero Clobbering / CDC Safe)
            if (step_pulse) begin
                if (is_hard_mode && r_step_counter[2:0] == 3'b111)
                    step_mind_decay = 8'd1;
                else if (!is_hard_mode && r_step_counter == 5'b11111)
                    step_mind_decay = 8'd1;
                else
                    step_mind_decay = 8'd0;
            end else begin
                step_mind_decay = 8'd0;
            end

            if (panic_strike_pulse)
                event_mind_loss = (is_hard_mode) ? 8'd25 : 8'd10;
            else if (encounter_pulse)
                event_mind_loss = (is_hard_mode) ? 8'd12 : 8'd4;
            else
                event_mind_loss = 8'd0;

            total_mind_loss = step_mind_decay + event_mind_loss;

            if (mind_restore_en) begin
                if ({1'b0, r_mind} + {1'b0, mind_restore_val} > 9'd100)
                    next_mind_calc = 9'd100;
                else
                    next_mind_calc = {1'b0, r_mind} + {1'b0, mind_restore_val};

                if (next_mind_calc > {1'b0, total_mind_loss})
                    r_mind <= next_mind_calc[7:0] - total_mind_loss;
                else
                    r_mind <= 8'd0;
            end else begin
                if (r_mind > total_mind_loss)
                    r_mind <= r_mind - total_mind_loss;
                else
                    r_mind <= 8'd0;
            end

            // 2. Unified Hunger Arbitration (Zero Clobbering / CDC Safe)
            if (step_pulse) begin
                if (is_hard_mode && r_step_counter[1:0] == 2'b11)
                    step_hunger_gain = 8'd1;
                else if (!is_hard_mode && r_step_counter[3:0] == 4'b1111)
                    step_hunger_gain = 8'd1;
                else
                    step_hunger_gain = 8'd0;
            end else begin
                step_hunger_gain = 8'd0;
            end

            next_hunger_calc = {1'b0, r_hunger} + {1'b0, step_hunger_gain};
            if (next_hunger_calc > 9'd100)
                next_hunger_calc = 9'd100;

            if (hunger_restore_en) begin
                if (next_hunger_calc > {1'b0, hunger_restore_val})
                    r_hunger <= next_hunger_calc[7:0] - hunger_restore_val;
                else
                    r_hunger <= 8'd0;
            end else begin
                r_hunger <= next_hunger_calc[7:0];
            end
        end
    end

    // Continuous Read Assignments
    assign mind_level       = r_mind;
    assign hunger_level     = r_hunger;
    assign is_panic         = (r_mind <= 8'd20);
    assign is_starving      = (r_hunger >= 8'd90);
    assign atk_penalty_pct  = (is_panic) ? ((is_hard_mode) ? 7'd25 : 7'd10) : 7'd0;

endmodule
