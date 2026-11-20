// ============================================================================
// Module 1: FSM Controller (battle_fsm.v)
// Specification:
//   Manages system states using a 3-bit state vector:
//     - STATE_INIT   (3'b000): Resets HP to 100, sets turn counter to 1
//     - STATE_INPUT  (3'b001): Captures player action and resolves AI action
//     - STATE_CALC   (3'b010): Triggers ALU, updates HP registers
//     - STATE_RENDER (3'b011): Outputs ASCII scene to terminal
//     - STATE_CHECK  (3'b100): Evaluates win/loss condition
//     - STATE_END    (3'b101): Halts simulation on terminal state
// ============================================================================

`timescale 1ns / 1ps
`include "battle_defs.vh"

module battle_fsm (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       step_en,         // Pulse or enable to advance state
    input  wire       battle_finished, // 1 if HP reaches 0 or all demo turns completed
    output reg  [2:0] state,
    output reg  [2:0] next_state,
    output wire       init_done        // High once initial render has completed
);

    reg init_rendered;

    // Next-state combinational logic
    always @(*) begin
        case (state)
            `STATE_INIT: begin
                // Move to initial render if not rendered yet, otherwise directly to INPUT
                if (!init_rendered)
                    next_state = `STATE_RENDER;
                else
                    next_state = `STATE_INPUT;
            end

            `STATE_INPUT: begin
                next_state = `STATE_CALC;
            end

            `STATE_CALC: begin
                next_state = `STATE_RENDER;
            end

            `STATE_RENDER: begin
                if (!init_rendered)
                    next_state = `STATE_INPUT;
                else
                    next_state = `STATE_CHECK;
            end

            `STATE_CHECK: begin
                if (battle_finished)
                    next_state = `STATE_END;
                else
                    next_state = `STATE_INPUT;
            end

            `STATE_END: begin
                next_state = `STATE_END; // Remain halted
            end

            default: begin
                next_state = `STATE_INIT;
            end
        endcase
    end

    // Sequential state register
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state         <= `STATE_INIT;
            init_rendered <= 1'b0;
        end else if (step_en) begin
            state <= next_state;
            if (state == `STATE_RENDER) begin
                init_rendered <= 1'b1;
            end
        end
    end

    assign init_done = init_rendered;

endmodule
