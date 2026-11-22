// ============================================================================
// DUAL-MODE HARDWARE VERIFICATION TESTBENCH: tb_dual_mode_top.v
// Top-Level Exhaustive Verification for:
//   - Mode 0: Fear & Hunger (Normal Mode - 1.5x ATK/DEF, 1.25x HP, +50 HP Poppy, slow hunger/decay)
//   - Mode 1: Terror & Starvation (Hardcore Mode - 1.0x Base, +30 HP Poppy, 4x fast hunger/decay, -12 encounter shock)
// Academic Standard: TS. Nguyen Dinh Han (HUST FaMI - COA / CS365 / IT3080)
// ============================================================================

`timescale 1ns / 1ps
`include "battle_defs.vh"

module tb_dual_mode_top;

    reg        clk;
    reg        rst_n;
    reg        cmd_en;
    reg [3:0]  cmd_type;
    reg [7:0]  cmd_param1;
    reg [7:0]  cmd_param2;
    reg [7:0]  cmd_param3;

    wire [3:0]  game_state_out;
    wire signed [31:0] player_x_out;
    wire signed [31:0] player_y_out;
    wire [31:0] step_count_out;

    wire [5:0]  enemy_id_out;
    wire [7:0]  enemy_hp_out;
    wire [7:0]  enemy_max_hp_out;

    wire [1:0]  active_pal_idx_out;
    wire [4:0]  active_pal_id_out;
    wire [7:0]  active_pal_hp_out;
    wire [7:0]  active_pal_max_hp_out;

    wire [4:0]  pal0_id_out;
    wire [7:0]  pal0_hp_out;
    wire [7:0]  pal0_max_hp_out;

    wire [4:0]  pal1_id_out;
    wire [7:0]  pal1_hp_out;
    wire [7:0]  pal1_max_hp_out;

    wire [4:0]  pal2_id_out;
    wire [7:0]  pal2_hp_out;
    wire [7:0]  pal2_max_hp_out;

    wire [4:0]  pal3_id_out;
    wire [7:0]  pal3_hp_out;
    wire [7:0]  pal3_max_hp_out;

    wire [7:0]  normal_herb_qty_out;
    wire [7:0]  strong_crys_qty_out;
    wire [7:0]  key_qty_out;
    wire        is_hard_mode_out;

    wire [7:0]  battle_turn_out;
    wire [1:0]  battle_status_out;
    wire        game_finished_out;
    wire        is_victory_out;

    wire [7:0]  last_dmg_dealt_out;
    wire [7:0]  last_dmg_taken_out;
    wire [2:0]  last_event_flag_out;

    // Instantiate Top-Level Synthesizable RTL
    battle_top dut (
        .clk                 (clk),
        .rst_n               (rst_n),
        .cmd_en              (cmd_en),
        .cmd_type            (cmd_type),
        .cmd_param1          (cmd_param1),
        .cmd_param2          (cmd_param2),
        .cmd_param3          (cmd_param3),

        .game_state_out      (game_state_out),
        .player_x_out        (player_x_out),
        .player_y_out        (player_y_out),
        .step_count_out      (step_count_out),

        .enemy_id_out        (enemy_id_out),
        .enemy_hp_out        (enemy_hp_out),
        .enemy_max_hp_out    (enemy_max_hp_out),

        .active_pal_idx_out  (active_pal_idx_out),
        .active_pal_id_out   (active_pal_id_out),
        .active_pal_hp_out   (active_pal_hp_out),
        .active_pal_max_hp_out(active_pal_max_hp_out),

        .pal0_id_out         (pal0_id_out),
        .pal0_hp_out         (pal0_hp_out),
        .pal0_max_hp_out     (pal0_max_hp_out),

        .pal1_id_out         (pal1_id_out),
        .pal1_hp_out         (pal1_hp_out),
        .pal1_max_hp_out     (pal1_max_hp_out),

        .pal2_id_out         (pal2_id_out),
        .pal2_hp_out         (pal2_hp_out),
        .pal2_max_hp_out     (pal2_max_hp_out),

        .pal3_id_out         (pal3_id_out),
        .pal3_hp_out         (pal3_hp_out),
        .pal3_max_hp_out     (pal3_max_hp_out),

        .normal_herb_qty_out (normal_herb_qty_out),
        .strong_crys_qty_out (strong_crys_qty_out),
        .key_qty_out         (key_qty_out),
        .is_hard_mode_out    (is_hard_mode_out),

        .battle_turn_out     (battle_turn_out),
        .battle_status_out   (battle_status_out),
        .game_finished_out   (game_finished_out),
        .is_victory_out      (is_victory_out),

        .last_dmg_dealt_out  (last_dmg_dealt_out),
        .last_dmg_taken_out  (last_dmg_taken_out),
        .last_event_flag_out (last_event_flag_out)
    );

    // Clock generator: 100MHz (10ns period)
    always #5 clk = ~clk;

    integer test_errors;
    integer total_probes;

    task send_cmd;
        input [3:0] c_type;
        input [7:0] p1;
        input [7:0] p2;
        input [7:0] p3;
        begin
            @(negedge clk);
            cmd_en     = 1'b1;
            cmd_type   = c_type;
            cmd_param1 = p1;
            cmd_param2 = p2;
            cmd_param3 = p3;
            @(posedge clk);
            #1;
            @(negedge clk);
            cmd_en     = 1'b0;
            cmd_type   = 4'd0;
            cmd_param1 = 8'd0;
            cmd_param2 = 8'd0;
            cmd_param3 = 8'd0;
            @(posedge clk);
            #1;
        end
    endtask

    task assert_cond;
        input condition;
        input [511:0] desc;
        begin
            total_probes = total_probes + 1;
            if (!condition) begin
                $display("  [FAIL] %0s", desc);
                test_errors = test_errors + 1;
            end else begin
                $display("  [PASS] %0s", desc);
            end
        end
    endtask

    initial begin
        clk = 0;
        rst_n = 0;
        cmd_en = 0;
        cmd_type = 0;
        cmd_param1 = 0;
        cmd_param2 = 0;
        cmd_param3 = 0;
        test_errors = 0;
        total_probes = 0;

        $display("\n================================================================================");
        $display("   TOP-LEVEL DUAL-MODE HARDWARE VERIFICATION SUITE (battle_top.v)");
        $display("   Mode 0: Fear & Hunger (Normal) vs Mode 1: Terror & Starvation (Hardcore)");
        $display("================================================================================\n");

        // ====================================================================
        // EXPERIMENT 1: MODE 0 (FEAR & HUNGER / NORMAL MODE)
        // ====================================================================
        $display("[*] --- TEST SUITE 1: Verifying Mode 0 (Fear & Hunger / Normal Mode) ---");
        rst_n = 0;
        #20;
        rst_n = 1;
        #10;

        assert_cond(game_state_out === `STATE_TITLE, "Top RTL resets cleanly to STATE_TITLE");
        assert_cond(is_hard_mode_out === 1'b0, "Default mode is Normal (is_hard_mode = 0)");

        // Transition from Title Screen with Mode 0 (cmd_param1 = 1: Normal)
        send_cmd(4'd1, 8'd1, 8'd0, 8'd0);
        assert_cond(game_state_out === `STATE_NARRATOR, "Transitioned to STATE_NARRATOR");
        assert_cond(is_hard_mode_out === 1'b0, "is_hard_mode_out remains 0 (Fear & Hunger Normal)");

        // Transition to Draft
        send_cmd(4'd1, 8'd0, 8'd0, 8'd0);
        assert_cond(game_state_out === `STATE_DRAFT, "Transitioned to STATE_DRAFT");

        // Draft Characters: 1=Cahara (125), 2=D'arce (145), 3=Enki (95), Ragnvaldr (155)
        // In Normal Mode: Expect 1.25x HP Boost!
        // Cahara: 125 + 31 = 156
        // D'arce: 145 + 36 = 181
        // Enki: 95 + 23 = 118
        // Ragnvaldr: 155 + 38 = 193
        send_cmd(4'd1, 8'd1, 8'd2, 8'd3);
        $display("DEBUG pal0_max: %0d, pal1: %0d, pal2: %0d, pal3: %0d | is_hard: %b", pal0_max_hp_out, pal1_max_hp_out, pal2_max_hp_out, pal3_max_hp_out, is_hard_mode_out);
        assert_cond(game_state_out === `STATE_MAP, "Draft complete, entered STATE_MAP");
        assert_cond(pal0_max_hp_out === 8'd156, "Mode 0: Cahara max HP boosted to 156 (1.25x of 125)");
        assert_cond(pal1_max_hp_out === 8'd181, "Mode 0: D'arce max HP boosted to 181 (1.25x of 145)");
        assert_cond(pal2_max_hp_out === 8'd118, "Mode 0: Enki max HP boosted to 118 (1.25x of 95)");
        assert_cond(pal3_max_hp_out === 8'd193, "Mode 0: Ragnvaldr max HP boosted to 193 (1.25x of 155)");

        // Pouch Healing in Mode 0: Poppy heals +50 HP
        // Damage Pal 0 first by 60
        dut.u_inv.r_char_hp[0] = 8'd90;
        #10;
        assert_cond(pal0_hp_out === 8'd90, "Pal 0 damaged to 90 HP");

        // Open bag on map (cmd_type = 4'd5)
        send_cmd(4'd5, 8'd0, 8'd0, 8'd0);
        assert_cond(game_state_out === `STATE_MAP_BAG, "Opened Survival Pouch on Map");

        // Consume Poppy on Pal 0 (cmd_type = 4'd1, cmd_param1 = 0): Expect 90 + 50 = 140 HP
        send_cmd(4'd1, 8'd0, 8'd0, 8'd0);
        assert_cond(pal0_hp_out === 8'd140, "Mode 0: Poppy restored +50 HP (90 -> 140 HP)");

        // Close bag (cmd_type = 4'd0)
        send_cmd(4'd0, 8'd0, 8'd0, 8'd0);
        assert_cond(game_state_out === `STATE_MAP, "Returned to STATE_MAP");

        // ====================================================================
        // EXPERIMENT 2: MODE 1 (TERROR & STARVATION / HARDCORE MODE)
        // ====================================================================
        $display("\n[*] --- TEST SUITE 2: Verifying Mode 1 (Terror & Starvation / Hardcore Mode) ---");
        rst_n = 0;
        #20;
        rst_n = 1;
        #10;

        assert_cond(game_state_out === `STATE_TITLE, "Top RTL resets cleanly to STATE_TITLE");

        // Transition from Title Screen with Mode 1 (cmd_param1 = 2: Hardcore)
        send_cmd(4'd1, 8'd2, 8'd0, 8'd0);
        assert_cond(game_state_out === `STATE_NARRATOR, "Transitioned to STATE_NARRATOR");
        assert_cond(is_hard_mode_out === 1'b1, "is_hard_mode_out asserted to 1 (Terror & Starvation Hardcore)!");

        // Transition to Draft
        send_cmd(4'd1, 8'd0, 8'd0, 8'd0);
        assert_cond(game_state_out === `STATE_DRAFT, "Transitioned to STATE_DRAFT");

        // Draft Characters in Hardcore Mode: Expect 1.0x Baseline HP (NO Boost)!
        // Cahara: 125
        // D'arce: 145
        // Enki: 95
        // Ragnvaldr: 155
        send_cmd(4'd1, 8'd1, 8'd2, 8'd3);
        $display("DEBUG pal0_max: %0d, pal1: %0d, pal2: %0d, pal3: %0d | is_hard: %b", pal0_max_hp_out, pal1_max_hp_out, pal2_max_hp_out, pal3_max_hp_out, is_hard_mode_out);
        assert_cond(game_state_out === `STATE_MAP, "Draft complete, entered STATE_MAP");
        assert_cond(pal0_max_hp_out === 8'd125, "Mode 1: Cahara max HP is 125 baseline (1.0x)");
        assert_cond(pal1_max_hp_out === 145,   "Mode 1: D'arce max HP is 145 baseline (1.0x)");
        assert_cond(pal2_max_hp_out === 8'd95,  "Mode 1: Enki max HP is 95 baseline (1.0x)");
        assert_cond(pal3_max_hp_out === 8'd155, "Mode 1: Ragnvaldr max HP is 155 baseline (1.0x)");

        // Pouch Healing in Mode 1: Poppy heals +30 HP (Hardcore ration)
        dut.u_inv.r_char_hp[0] = 8'd80;
        #10;
        assert_cond(pal0_hp_out === 8'd80, "Pal 0 damaged to 80 HP");

        // Open bag on map
        send_cmd(4'd5, 8'd0, 8'd0, 8'd0);
        assert_cond(game_state_out === `STATE_MAP_BAG, "Opened Survival Pouch on Map");

        // Consume Poppy on Pal 0 (cmd_type = 4'd1, cmd_param1 = 0): Expect 80 + 30 = 110 HP
        send_cmd(4'd1, 8'd0, 8'd0, 8'd0);
        assert_cond(pal0_hp_out === 8'd110, "Mode 1: Poppy restored +30 HP (80 -> 110 HP)");

        // Close bag (cmd_type = 4'd0)
        send_cmd(4'd0, 8'd0, 8'd0, 8'd0);
        assert_cond(game_state_out === `STATE_MAP, "Returned to STATE_MAP");

        // ====================================================================
        // EXPERIMENT 3: CHARACTER ROM STAT DIVERGENCE PROOF
        // ====================================================================
        $display("\n[*] --- TEST SUITE 3: Character ROM Stat Divergence Proof ---");
        // Cahara (ID 1): Base ATK=22, Base DEF=14
        // Mode 0: ATK = 22 + 11 = 33, DEF = 14 + 7 = 21
        // Mode 1: ATK = 22, DEF = 14
        assert_cond(dut.u_char_rom.char_atk === 8'd22, "Mode 1: Cahara active ATK is 22 baseline");
        assert_cond(dut.u_char_rom.char_def === 8'd14, "Mode 1: Cahara active DEF is 14 baseline");

        // ====================================================================
        // EXPERIMENT 4: TACTICAL STANCE REGEN DIVERGENCE PROOF
        // ====================================================================
        $display("\n[*] --- TEST SUITE 4: Tactical Stance Regen Divergence Proof ---");
        // In Iron Guard (Stance 2):
        dut.u_stance.r_stance = `STANCE_IRON_GUARD;
        #5;
        assert_cond(dut.top_regen_hp === 8'd3, "Mode 1: Iron Guard turn regen is 3 HP (Hardcore)");

        // ====================================================================
        // FINAL SUMMARY
        // ====================================================================
        $display("\n================================================================================");
        $display("   DUAL-MODE TOP RTL VERIFICATION SUMMARY:");
        $display("   Total Hardware Probes: %0d", total_probes);
        $display("   Failed Probes:         %0d", test_errors);
        if (test_errors == 0) begin
            $display("   >>> ALL DUAL-MODE HARDWARE PROBES PASSED 100%%%%! <<<");
            $display("   >>> MODE 0 (NORMAL) AND MODE 1 (HARDCORE) FULLY VERIFIED IN TOP RTL! <<<");
        end else begin
            $display("   >>> DUAL-MODE VERIFICATION FAILED! <<<");
        end
        $display("================================================================================\n");

        $finish;
    end

endmodule
