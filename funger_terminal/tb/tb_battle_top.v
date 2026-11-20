// ============================================================================
// Pokemon Lite: Terror & Starvation - Interactive Testbench (tb_battle_top.v)
// 100% English Interactive Console CLI Gameplay:
//   - Title Banner -> Narrator Lore -> Comprehensive Companion Draft Roster
//   - 60x80 Labyrinth exploration: Green walls, Amber player, Red monster nodes
//   - Survival Pouch (I) with ASCII models for Herbs & Crystals
//   - Tactical turn-based combat with Combat Log, DEF mitigation, 6.25% Crit
// ============================================================================

`timescale 1ns / 1ps
`include "battle_defs.vh"

module tb_battle_top;

    reg        clk;
    reg        rst_n;
    reg        cmd_en;
    reg [3:0]  cmd_type;
    reg [7:0]  cmd_param1;
    reg [7:0]  cmd_param2;
    reg [7:0]  cmd_param3;

    wire [3:0]  game_state;
    wire signed [31:0] player_x;
    wire signed [31:0] player_y;
    wire [31:0] step_count;

    wire [5:0]  enemy_id;
    wire [7:0]  enemy_hp;
    wire [7:0]  enemy_max_hp;

    wire [1:0]  active_pal_idx;
    wire [4:0]  active_pal_id;
    wire [7:0]  active_pal_hp;
    wire [7:0]  active_pal_max_hp;

    wire [4:0]  pal0_id;
    wire [7:0]  pal0_hp;
    wire [7:0]  pal0_max_hp;

    wire [4:0]  pal1_id;
    wire [7:0]  pal1_hp;
    wire [7:0]  pal1_max_hp;

    wire [4:0]  pal2_id;
    wire [7:0]  pal2_hp;
    wire [7:0]  pal2_max_hp;

    wire [7:0]  normal_herb_qty;
    wire [7:0]  strong_crys_qty;

    // 8-bit turn counter
    wire [7:0]  battle_turn;
    wire [1:0]  battle_status;
    wire        game_finished;
    wire        is_victory;

    // Combat Log signals
    wire [7:0]  last_dmg_dealt;
    wire [7:0]  last_dmg_taken;
    wire [2:0]  last_event_flag;

    // Instantiate Top RTL Module
    battle_top dut (
        .clk                 (clk),
        .rst_n               (rst_n),
        .cmd_en              (cmd_en),
        .cmd_type            (cmd_type),
        .cmd_param1          (cmd_param1),
        .cmd_param2          (cmd_param2),
        .cmd_param3          (cmd_param3),
        .game_state_out      (game_state),
        .player_x_out        (player_x),
        .player_y_out        (player_y),
        .step_count_out      (step_count),
        .enemy_id_out        (enemy_id),
        .enemy_hp_out        (enemy_hp),
        .enemy_max_hp_out    (enemy_max_hp),
        .active_pal_idx_out  (active_pal_idx),
        .active_pal_id_out   (active_pal_id),
        .active_pal_hp_out   (active_pal_hp),
        .active_pal_max_hp_out(active_pal_max_hp),
        .pal0_id_out         (pal0_id),
        .pal0_hp_out         (pal0_hp),
        .pal0_max_hp_out     (pal0_max_hp),
        .pal1_id_out         (pal1_id),
        .pal1_hp_out         (pal1_hp),
        .pal1_max_hp_out     (pal1_max_hp),
        .pal2_id_out         (pal2_id),
        .pal2_hp_out         (pal2_hp),
        .pal2_max_hp_out     (pal2_max_hp),
        .normal_herb_qty_out (normal_herb_qty),
        .strong_crys_qty_out (strong_crys_qty),
        .battle_turn_out     (battle_turn),
        .battle_status_out   (battle_status),
        .game_finished_out   (game_finished),
        .is_victory_out      (is_victory),
        .last_dmg_dealt_out  (last_dmg_dealt),
        .last_dmg_taken_out  (last_dmg_taken),
        .last_event_flag_out (last_event_flag)
    );

    // Terminal UI Engine & Monster Database
    terminal_ui ui();
    monster_rom mon_db(.monster_id(6'd1), .is_elite(1'b0), .base_hp(), .base_atk(), .base_def(), .spawn_weight(), .is_default_elite());

    // Clock generator 100MHz
    initial begin
        clk = 1'b0;
        forever #5 clk = ~clk;
    end

    // Task to pulse command strobes
    task send_cmd;
        input [3:0] c_type;
        input [7:0] p1;
        input [7:0] p2;
        input [7:0] p3;
        begin
            @(posedge clk);
            cmd_en     <= 1'b1;
            cmd_type   <= c_type;
            cmd_param1 <= p1;
            cmd_param2 <= p2;
            cmd_param3 <= p3;
            @(posedge clk);
            cmd_en     <= 1'b0;
            @(posedge clk);
        end
    endtask

    integer scan_ret;
    integer int_choice;
    reg [7:0] char_choice;
    reg [79:0] dummy_str;

    // Master interactive control routine
    initial begin
        cmd_en     = 1'b0;
        cmd_type   = 4'd0;
        cmd_param1 = 8'd0;
        cmd_param2 = 8'd0;
        cmd_param3 = 8'd0;

        // System Reset
        rst_n = 1'b0;
        #30;
        rst_n = 1'b1;
        #20;

        // ====================================================================
        // PHASE 1: TITLE SCREEN
        // ====================================================================
        ui.render_title_screen(1'b0);
        scan_ret = $fscanf(32'h80000000, "%d", int_choice);
        if (scan_ret <= 0 || int_choice == 2 || int_choice == 0) begin
            send_cmd(4'd2, 8'd0, 8'd0, 8'd0); // Quit
            ui.render_game_over_screen();
            $finish;
        end else begin
            send_cmd(4'd1, 8'd0, 8'd0, 8'd0); // Start
        end

        // ====================================================================
        // PHASE 2: PROLOGUE NARRATOR LORE
        // ====================================================================
        ui.render_narrator_screen();
        scan_ret = $fscanf(32'h80000000, "%s", dummy_str);
        send_cmd(4'd1, 8'd0, 8'd0, 8'd0); // Advance to draft

        // ====================================================================
        // PHASE 3: COMPANION DRAFT (LISTS CANDIDATE DOSSIERS IN ENGLISH)
        // ====================================================================
        ui.render_draft_screen(
            5'd1, 8'd120, 8'd20, 8'd15, // Ursa-Apex
            5'd2, 8'd95,  8'd22, 8'd10, // Hornowl
            5'd6, 8'd110, 8'd18, 8'd22, // Megascarab
            5'd10,8'd100, 8'd20, 8'd14, // Joecool
            5'd11,8'd130, 8'd18, 8'd25  // Mechagolem
        );

        // Pick Pal #1
        $write("  >> Enter Pal #1 slot choice (1 to 5): ");
        scan_ret = $fscanf(32'h80000000, "%d", int_choice);
        cmd_param1 = (int_choice >= 1 && int_choice <= 5) ? int_choice : 8'd1;

        // Pick Pal #2 (Prevent Duplicate - Item 6)
        cmd_param2 = 8'd0;
        while (cmd_param2 == 8'd0 || cmd_param2 == cmd_param1) begin
            $write("  >> Enter Pal #2 slot choice (1 to 5, unique): ");
            scan_ret = $fscanf(32'h80000000, "%d", int_choice);
            if (int_choice >= 1 && int_choice <= 5 && int_choice != cmd_param1) begin
                cmd_param2 = int_choice;
            end else if (scan_ret <= 0) begin
                cmd_param2 = (cmd_param1 == 8'd1) ? 8'd2 : 8'd1;
            end else begin
                $display("  \033[1;31m[!] Duplicate choice! Select a different companion.\033[0m");
            end
        end

        // Pick Pal #3 (Prevent Duplicate - Item 6)
        cmd_param3 = 8'd0;
        while (cmd_param3 == 8'd0 || cmd_param3 == cmd_param1 || cmd_param3 == cmd_param2) begin
            $write("  >> Enter Pal #3 slot choice (1 to 5, unique): ");
            scan_ret = $fscanf(32'h80000000, "%d", int_choice);
            if (int_choice >= 1 && int_choice <= 5 && int_choice != cmd_param1 && int_choice != cmd_param2) begin
                cmd_param3 = int_choice;
            end else if (scan_ret <= 0) begin
                if (cmd_param1 != 8'd3 && cmd_param2 != 8'd3) cmd_param3 = 8'd3;
                else if (cmd_param1 != 8'd4 && cmd_param2 != 8'd4) cmd_param3 = 8'd4;
                else cmd_param3 = 8'd5;
            end else begin
                $display("  \033[1;31m[!] Duplicate choice! Select a different companion.\033[0m");
            end
        end

        send_cmd(4'd3, cmd_param1, cmd_param2, cmd_param3);

        // ====================================================================
        // PHASE 4 & 5: EXPLORATION & COMBAT LOOP
        // ====================================================================
        while (!game_finished) begin
            if (game_state == `STATE_MAP) begin
                ui.render_pal_map_screen(
                    player_x, player_y, step_count,
                    normal_herb_qty, strong_crys_qty,
                    pal0_id, pal0_hp, pal0_max_hp,
                    pal1_id, pal1_hp, pal1_max_hp,
                    pal2_id, pal2_hp, pal2_max_hp
                );

                scan_ret = $fscanf(32'h80000000, "%s", dummy_str);
                char_choice = dummy_str[7:0];

                if (char_choice == "w" || char_choice == "W" || char_choice == "8") begin
                    send_cmd(4'd4, "w", 8'd0, 8'd0); // Up
                end else if (char_choice == "s" || char_choice == "S" || char_choice == "2") begin
                    send_cmd(4'd4, "s", 8'd0, 8'd0); // Down
                end else if (char_choice == "a" || char_choice == "A" || char_choice == "4") begin
                    send_cmd(4'd4, "a", 8'd0, 8'd0); // Left
                end else if (char_choice == "d" || char_choice == "D" || char_choice == "6") begin
                    send_cmd(4'd4, "d", 8'd0, 8'd0); // Right
                end else if (char_choice == "h" || char_choice == "H") begin
                    // Quick Heal Hotkey (Item 7): Heals companion with greatest HP deficit
                    if (normal_herb_qty > 0) begin
                        if ((pal0_max_hp - pal0_hp >= pal1_max_hp - pal1_hp) && (pal0_max_hp - pal0_hp >= pal2_max_hp - pal2_hp) && pal0_hp < pal0_max_hp) begin
                            send_cmd(4'd5, 8'd0, 8'd0, 8'd0);
                            #10;
                            send_cmd(4'd1, 8'd0, 8'd0, 8'd0); // Heal Pal 0
                            #10;
                            send_cmd(4'd0, 8'd0, 8'd0, 8'd0); // Return to map
                            $display("  \033[1;32m>> [QUICK HEAL]: Administered Normal Herb to Pal #1!\033[0m");
                        end else if ((pal1_max_hp - pal1_hp >= pal2_max_hp - pal2_hp) && pal1_hp < pal1_max_hp) begin
                            send_cmd(4'd5, 8'd0, 8'd0, 8'd0);
                            #10;
                            send_cmd(4'd1, 8'd1, 8'd0, 8'd0); // Heal Pal 1
                            #10;
                            send_cmd(4'd0, 8'd0, 8'd0, 8'd0); // Return to map
                            $display("  \033[1;32m>> [QUICK HEAL]: Administered Normal Herb to Pal #2!\033[0m");
                        end else if (pal2_hp < pal2_max_hp) begin
                            send_cmd(4'd5, 8'd0, 8'd0, 8'd0);
                            #10;
                            send_cmd(4'd1, 8'd2, 8'd0, 8'd0); // Heal Pal 2
                            #10;
                            send_cmd(4'd0, 8'd0, 8'd0, 8'd0); // Return to map
                            $display("  \033[1;32m>> [QUICK HEAL]: Administered Normal Herb to Pal #3!\033[0m");
                        end else begin
                            $display("  \033[1;32m>> [HEALTHY]: All squad companions are already at full HP!\033[0m");
                        end
                    end else begin
                        $display("  \033[1;31m>> [EMPTY]: No Normal Herbs remaining in survival pouch!\033[0m");
                    end
                end else if (char_choice == "i" || char_choice == "I") begin
                    send_cmd(4'd5, 8'd0, 8'd0, 8'd0); // Open Bag
                end else if (char_choice == "q" || char_choice == "Q" || char_choice == "0") begin
                    // Quit confirmation prompt (Item 7)
                    $write("  \033[1;33m>> Are you sure you want to abandon hope and quit? (Y/N): \033[0m");
                    scan_ret = $fscanf(32'h80000000, "%s", dummy_str);
                    if (dummy_str[7:0] == "y" || dummy_str[7:0] == "Y") begin
                        send_cmd(4'd0, 8'd0, 8'd0, 8'd0); // Quit
                    end else begin
                        $display("  >> Resumed expedition.");
                    end
                end
            end else if (game_state == `STATE_MAP_BAG) begin
                // Open pouch on map
                ui.render_pal_bag_screen(
                    `ITEM_NONE, normal_herb_qty, strong_crys_qty,
                    pal0_id, pal0_hp, pal0_max_hp,
                    pal1_id, pal1_hp, pal1_max_hp,
                    pal2_id, pal2_hp, pal2_max_hp
                );
                scan_ret = $fscanf(32'h80000000, "%d", int_choice);
                if (int_choice == 1 || int_choice == 2) begin
                    cmd_param1 = int_choice; // Store 1 (Herb) or 2 (Crystal)
                    ui.render_pal_bag_screen(
                        (cmd_param1 == 1) ? `ITEM_NORMAL : `ITEM_STRONG,
                        normal_herb_qty, strong_crys_qty,
                        pal0_id, pal0_hp, pal0_max_hp,
                        pal1_id, pal1_hp, pal1_max_hp,
                        pal2_id, pal2_hp, pal2_max_hp
                    );
                    $write("  >> Select Pal to administer item (1, 2, 3 or 0 to Cancel): ");
                    scan_ret = $fscanf(32'h80000000, "%d", int_choice);
                    if (int_choice >= 1 && int_choice <= 3) begin
                        send_cmd(cmd_param1, int_choice - 1, 8'd0, 8'd0);
                        $display("  >> [HEAL SUCCESS] Medicine administered to companion!");
                        #10;
                        send_cmd(4'd0, 8'd0, 8'd0, 8'd0); // Auto-close bag back to map after use
                    end else begin
                        send_cmd(4'd0, 8'd0, 8'd0, 8'd0); // Back
                    end
                end else begin
                    send_cmd(4'd0, 8'd0, 8'd0, 8'd0); // Close pouch
                end
            end else if (game_state == `STATE_BATTLE_LOOP) begin
                // Battle encounter with Combat Log (Item 4)
                ui.render_battle_screen_pal(
                    enemy_id, enemy_hp, enemy_max_hp,
                    active_pal_id, active_pal_hp, active_pal_max_hp,
                    battle_turn,
                    last_dmg_dealt, last_dmg_taken, last_event_flag
                );

                scan_ret = $fscanf(32'h80000000, "%d", int_choice);
                if (int_choice == 1) begin
                    // [1] Attack
                    send_cmd(4'd1, 8'd0, 8'd0, 8'd0);
                end else if (int_choice == 2) begin
                    // [2] Defend
                    send_cmd(4'd2, 8'd0, 8'd0, 8'd0);
                end else if (int_choice == 3) begin
                    // [3] Field Medicine (Select Item -> Select Pal)
                    ui.render_combat_heal_menu(
                        normal_herb_qty, strong_crys_qty,
                        active_pal_id, active_pal_hp, active_pal_max_hp
                    );
                    scan_ret = $fscanf(32'h80000000, "%d", int_choice);
                    if (int_choice == 1 || int_choice == 2) begin
                        cmd_param1 = int_choice; // 1: Herb (+20 HP), 2: Crystal (+50 HP)
                        ui.render_target_pal_menu(
                            cmd_param1[1:0],
                            pal0_id, pal0_hp, pal0_max_hp,
                            pal1_id, pal1_hp, pal1_max_hp,
                            pal2_id, pal2_hp, pal2_max_hp
                        );
                        scan_ret = $fscanf(32'h80000000, "%d", int_choice);
                        if (int_choice >= 1 && int_choice <= 3) begin
                            send_cmd(4'd3, cmd_param1, int_choice - 1, 8'd0);
                            $display("  >> [HEAL SUCCESS] Administered medicine to Pal #%0d!", int_choice);
                        end
                    end
                end else if (int_choice == 4) begin
                    // [4] Mid-Battle Switch Pal
                    ui.render_combat_switch_menu(
                        active_pal_idx,
                        pal0_id, pal0_hp, pal0_max_hp,
                        pal1_id, pal1_hp, pal1_max_hp,
                        pal2_id, pal2_hp, pal2_max_hp
                    );
                    scan_ret = $fscanf(32'h80000000, "%d", int_choice);
                    if (int_choice >= 1 && int_choice <= 3) begin
                        send_cmd(4'd5, int_choice - 1, 8'd0, 8'd0); // Switch Pal!
                    end
                end else if (int_choice == 5) begin
                    // [5] Flee (50%)
                    send_cmd(4'd4, 8'd0, 8'd0, 8'd0);
                end
            end
            #10;
        end

        // Final resolution
        if (is_victory) begin
            ui.render_victory_screen();
        end else begin
            ui.render_game_over_screen();
        end

        $display("\n[SIMULATION FINISHED] Simulation terminated cleanly.");
        $finish;
    end

endmodule
