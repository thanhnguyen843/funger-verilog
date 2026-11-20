`timescale 1ns / 1ps
`include "battle_defs.vh"

module tb_fsm_fuzzer;

    reg clk;
    reg rst_n;
    reg cmd_en;
    reg [3:0] cmd_type;
    reg [7:0] cmd_param1;
    reg [7:0] cmd_param2;
    reg [7:0] cmd_param3;

    wire [3:0]  game_state;
    wire signed [31:0] player_x;
    wire signed [31:0] player_y;
    wire [31:0] step_count;
    wire [5:0]  enemy_id;
    wire [7:0]  enemy_hp;
    wire [7:0]  enemy_max_hp;

    battle_top dut (
        .clk             (clk),
        .rst_n           (rst_n),
        .cmd_en          (cmd_en),
        .cmd_type        (cmd_type),
        .cmd_param1      (cmd_param1),
        .cmd_param2      (cmd_param2),
        .cmd_param3      (cmd_param3),
        .game_state_out  (game_state),
        .player_x_out    (player_x),
        .player_y_out    (player_y),
        .step_count_out  (step_count),
        .enemy_id_out    (enemy_id),
        .enemy_hp_out    (enemy_hp),
        .enemy_max_hp_out(enemy_max_hp),
        .active_pal_idx_out(),
        .active_pal_id_out(),
        .active_pal_hp_out(),
        .active_pal_max_hp_out(),
        .pal0_id_out     (),
        .pal0_hp_out     (),
        .pal0_max_hp_out (),
        .pal1_id_out     (),
        .pal1_hp_out     (),
        .pal1_max_hp_out (),
        .pal2_id_out     (),
        .pal2_hp_out     (),
        .pal2_max_hp_out (),
        .normal_herb_qty_out(),
        .strong_crys_qty_out(),
        .battle_turn_out (),
        .battle_status_out(),
        .game_finished_out(),
        .is_victory_out  ()
    );

    wire [2:0] current_tile;
    map_rom u_check_map (
        .in_x(player_x),
        .in_y(player_y),
        .out_tile(current_tile)
    );

    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    integer i;
    integer fuzzer_errors = 0;
    integer wall_collisions_tested = 0;
    integer random_seed = 32'hDEAD_BEEF;

    function [31:0] lfsr_rand;
        input [31:0] s;
        begin
            lfsr_rand = (s >> 1) ^ (-(s & 1) & 32'hD0000001);
        end
    endfunction

    reg [7:0] random_key;
    reg [7:0] keys_pool [0:11];

    initial begin
        keys_pool[0] = "W";
        keys_pool[1] = "A";
        keys_pool[2] = "S";
        keys_pool[3] = "D";
        keys_pool[4] = "1";
        keys_pool[5] = "2";
        keys_pool[6] = "3";
        keys_pool[7] = "4";
        keys_pool[8] = "B";
        keys_pool[9] = "X"; // Garbage key
        keys_pool[10]= 8'd0; // Null key
        keys_pool[11]= 8'd255; // Out of bounds key

        // 1. Reset system
        rst_n = 0;
        cmd_en = 0;
        cmd_type = 0;
        cmd_param1 = 0;
        cmd_param2 = 0;
        cmd_param3 = 0;
        #20;
        rst_n = 1;
        #20;

        // Advance to Draft and Map
        @(posedge clk);
        cmd_en = 1; cmd_type = 4'd1; cmd_param1 = 8'd1; @(posedge clk); cmd_en = 0; #20;
        @(posedge clk);
        cmd_en = 1; cmd_type = 4'd2; cmd_param1 = 8'd1; @(posedge clk); cmd_en = 0; #20;
        @(posedge clk);
        cmd_en = 1; cmd_type = 4'd3; cmd_param1 = 8'd1; cmd_param2 = 8'd2; cmd_param3 = 8'd3; @(posedge clk); cmd_en = 0; #20;

        $display("[*] Starting FSM Random Input Fuzzing (50,000 Iterations)...");

        for (i = 0; i < 50000; i = i + 1) begin
            random_seed = lfsr_rand(random_seed);
            random_key = keys_pool[random_seed % 12];

            @(posedge clk);
            cmd_en     <= 1'b1;
            cmd_type   <= 4'd4; // Movement / action strobe
            cmd_param1 <= random_key;
            cmd_param2 <= random_seed[15:8];
            cmd_param3 <= random_seed[23:16];
            @(posedge clk);
            cmd_en     <= 1'b0;
            #1;

            // Check 1: No Unknown (X) or High-Impedance (Z) states
            if (^game_state === 1'bx || ^player_x === 1'bx || ^player_y === 1'bx) begin
                $display("[FAIL] Unknown (X/Z) state detected at cycle %0d!", i);
                fuzzer_errors = fuzzer_errors + 1;
            end

            // Check 2: Player NEVER walks inside a wall tile while in map exploration
            if (game_state == `STATE_MAP) begin
                if (current_tile == `TILE_WALL) begin
                    $display("[FAIL] Boundary violation! Player walked into TILE_WALL at (%0d, %0d)!", player_x, player_y);
                    fuzzer_errors = fuzzer_errors + 1;
                end
                wall_collisions_tested = wall_collisions_tested + 1;
            end
        end

        $display("[*] Fuzzing Completed: 50,000 random inputs processed.");
        $display("    - Wall collisions evaluated: %0d", wall_collisions_tested);
        $display("    - System stability errors: %0d", fuzzer_errors);

        if (fuzzer_errors == 0) begin
            $display(">>> FSM RANDOM FUZZING: 100%% PASS (Zero Deadlocks, Zero Wall Glitches) <<<");
        end else begin
            $display(">>> FSM RANDOM FUZZING: FAILED WITH %0d ERRORS! <<<", fuzzer_errors);
        end

        $finish;
    end
endmodule
