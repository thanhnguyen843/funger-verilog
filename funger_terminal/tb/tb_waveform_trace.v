// ============================================================================
// Module: tb_waveform_trace.v
// Dedicated Waveform Generation Testbench for GTKWave Showcase
// Dumps full-depth signals to sim/funger_architecture.vcd
// Demonstrating FSM control states, combinational ALU, and LFSR stepping
// ============================================================================

`timescale 1ns / 1ps
`include "battle_defs.vh"

module tb_waveform_trace;

    reg clk;
    reg rst_n;

    // FSM Emulation Signals
    reg [3:0] fsm_state;
    reg [2:0] battle_sub_state;
    reg [1:0] difficulty_mode;
    reg [1:0] active_pal_idx;

    // ALU Signals
    reg  [1:0] p1_action;
    reg  [1:0] p2_action;
    reg  [7:0] p1_atk;
    reg  [7:0] p2_atk;
    reg  [7:0] p1_def;
    reg  [7:0] p2_def;
    reg  [3:0] rng_bits;
    reg  [7:0] p1_hp;
    reg        flee_failed;
    reg  [2:0] limb;
    reg        lethal;
    reg        disarmed;

    wire [7:0] p1_dmg;
    wire [7:0] p2_dmg;
    wire [7:0] flee_pen;

    damage_alu u_alu (
        .p1_action      (p1_action),
        .p2_action      (p2_action),
        .p1_base_atk    (p1_atk),
        .p2_base_atk    (p2_atk),
        .p1_def         (p1_def),
        .p2_def         (p2_def),
        .rng_bits       (rng_bits),
        .p1_curr_hp     (p1_hp),
        .is_flee_failed (flee_failed),
        .limb_target    (limb),
        .is_lethal_mode (lethal),
        .enemy_disarmed (disarmed),
        .p1_damage      (p1_dmg),
        .p2_damage      (p2_dmg),
        .p1_flee_penalty(flee_pen)
    );

    // LFSR RNG Unit
    reg        rng_step;
    reg [31:0] rng_seed_data;
    wire[31:0] rng_state;
    wire       rand_bit_50;
    wire[6:0]  rand_pct;
    wire[5:0]  rand_monster_id;

    rng_unit u_rng (
        .clk             (clk),
        .rst_n           (rst_n),
        .step_en         (rng_step),
        .seed_val        (rng_seed_data),
        .lfsr_val        (rng_state),
        .rand_bit_50     (rand_bit_50),
        .rand_pct        (rand_pct),
        .rand_monster_id (rand_monster_id)
    );

    // Clock Generation: 50 MHz (Period = 20 ns)
    always #10 clk = ~clk;

    initial begin
        $dumpfile("sim/funger_architecture.vcd");
        $dumpvars(0, tb_waveform_trace);

        // System Initialization
        clk = 0;
        rst_n = 0;
        fsm_state = `STATE_TITLE;
        battle_sub_state = `B_STATE_MENU;
        difficulty_mode = 0;
        active_pal_idx = 0;
        p1_action = `ACTION_ATTACK;
        p2_action = `ACTION_ATTACK;
        p1_atk = 8'd33;
        p2_atk = 8'd25;
        p1_def = 8'd21;
        p2_def = 8'd12;
        rng_bits = 4'd0;
        p1_hp = 8'd156;
        flee_failed = 0;
        limb = `LIMB_TORSO;
        lethal = 0;
        disarmed = 0;
        rng_step = 0;
        rng_seed_data = 32'hA5A5_5A5A;

        #30;
        rst_n = 1;

        // Trace Event 1: Stepping Galois LFSR
        #20;
        rng_step = 1;
        #40;
        rng_step = 0;

        // Trace Event 2: State Transition TITLE -> DRAFT
        #20;
        fsm_state = `STATE_TITLE;
        #40;
        fsm_state = `STATE_DRAFT;
        difficulty_mode = 2'd0; // Fear & Hunger Mode (1.5x)

        // Trace Event 3: Enter Labyrinth Map & Step RNG
        #40;
        fsm_state = `STATE_MAP;
        rng_step = 1;
        #20;
        rng_step = 0;

        // Trace Event 4: Combat Engagement (Head Strike vs Attack)
        #40;
        fsm_state = `STATE_BATTLE_LOAD;
        #20;
        fsm_state = `STATE_BATTLE_LOOP;
        battle_sub_state = `B_STATE_MOVE_SEL;
        limb = `LIMB_HEAD; // 1.5x multiplier
        p1_action = `ACTION_ATTACK;
        p2_action = `ACTION_ATTACK;
        #20;
        battle_sub_state = `B_STATE_CALC;
        #20;
        battle_sub_state = `B_STATE_RESOLVE;

        // Trace Event 5: Enemy Guard (Damage Shift Right >> 2)
        #40;
        battle_sub_state = `B_STATE_MOVE_SEL;
        p2_action = `ACTION_DEFEND;
        #20;
        battle_sub_state = `B_STATE_CALC;
        #20;
        battle_sub_state = `B_STATE_RESOLVE;

        // Trace Event 6: Player Disarming Enemy (Both arms severed)
        #40;
        battle_sub_state = `B_STATE_MOVE_SEL;
        p2_action = `ACTION_ATTACK;
        disarmed = 1; // Enemy damage reduced to (atk >> 2)
        #20;
        battle_sub_state = `B_STATE_CALC;
        #20;
        battle_sub_state = `B_STATE_RESOLVE;

        // Trace Event 7: Failed Flee Attempt Penalty Calculation (30% HP)
        #40;
        battle_sub_state = `B_STATE_BAG_SEL;
        p1_action = `ACTION_ITEM_OR_FLEE;
        flee_failed = 1;
        #20;
        battle_sub_state = `B_STATE_CALC;
        #20;
        battle_sub_state = `B_STATE_RESOLVE;

        // Trace Event 8: Victory & Portal Gate Exit
        #60;
        fsm_state = `STATE_VICTORY;
        #60;

        $display("\033[1;32m[*] GTKWave Architecture Trace generated at: sim/funger_architecture.vcd\033[0m");
        $finish;
    end

endmodule
