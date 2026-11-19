// ============================================================================
// Interactive Gameplay Testbench: tb_play.v
// Fear & Hunger: Terminal Labyrinth - Deluxe Overhaul Edition
// RTL Hardware Simulation with Full Fear & Hunger Features:
//   1. Dynamic Moving Cursor Menu Navigation ([W/S] or [Up/Down], [E/Space/Enter], [1-6])
//   2. Targetable Body Parts (Head, Torso, Arms, Legs, Decapitation, Crawling, Disarm)
//   3. Coin Flip of Death (Lethal Clashes, Suspense, Parrying vs Devastation)
//   4. Mind & Hunger Survival Gauges & Items (Moldy Bread, Dried Meat, Ale, Herbs)
//   5. Hexen & Class Skills for Explorers (Steal, Fast Stance, Hurting, Black Orb, Devour)
//   6. Screen Shake & Visual Slash FX
// ============================================================================

`timescale 1ns / 1ps
`include "battle_defs.vh"

module tb_play;

    reg clk;
    reg rst_n;

    always #5 clk = ~clk;

    // Submodules
    terminal_ui   ui();
    character_rom char_db();
    monster_rom   mon_db();
    map_rom       map_db();

    // Explorer Squad (4 Explorers)
    reg [255:0] team_name [0:3];
    reg [255:0] team_class [0:3];
    reg [7:0]   team_hp   [0:3];
    reg [7:0]   team_max  [0:3];
    reg [7:0]   team_atk  [0:3];
    reg [7:0]   team_def  [0:3];
    reg [7:0]   team_mind [0:3];
    reg [7:0]   team_hunger [0:3];
    reg [3:0]   team_char_id [0:3];
    reg [1:0]   active_member, old_member;

    // Survival Bag & Resources
    reg [7:0]   bag_poppy;
    reg [7:0]   bag_marijuana;
    reg [7:0]   bag_bread;
    reg [7:0]   bag_meat;
    reg [7:0]   bag_ale;
    reg [7:0]   bag_keys;

    // Player & Map Position
    reg signed [31:0] player_x;
    reg signed [31:0] player_y;
    reg [31:0]        step_count;
    reg [719:0]       cleared_mask;
    reg [36:0]        encountered_mask;
    integer           monsters_defeated_count;

    // Interaction variables
    integer scan_ret;
    integer int_choice;
    integer c1, c2, c3, c4;
    reg [127:0] str_input;
    reg [7:0]   cmd_char;
    reg [511:0] map_alert_msg;
    reg signed [31:0] target_x, target_y;
    integer     target_idx;
    reg [2:0]   target_tile;

    // Combat state: General
    reg [5:0]   cur_enemy_id;
    reg [7:0]   cur_enemy_hp, cur_enemy_max;
    reg [7:0]   cur_enemy_atk, cur_enemy_def, cur_enemy_weight;
    reg         cur_enemy_is_elite;
    reg         dummy_el;
    reg [3:0]   combat_turn;
    reg         in_combat;
    reg         combat_fled;
    integer     calc_dmg;
    integer     r_roll;
    reg         is_hard_mode;
    reg [7:0]   heal_poppy_val;
    reg [7:0]   heal_marijuana_val;

    // Combat state: Body Parts / Limbs
    reg [7:0]   enemy_head_hp, enemy_head_max;
    reg [7:0]   enemy_torso_hp, enemy_torso_max;
    reg [7:0]   enemy_arm_r_hp, enemy_arm_r_max;
    reg [7:0]   enemy_arm_l_hp, enemy_arm_l_max;
    reg [7:0]   enemy_leg_r_hp, enemy_leg_r_max;
    reg [7:0]   enemy_leg_l_hp, enemy_leg_l_max;
    reg         enemy_is_crawling;
    reg         enemy_is_disarmed;
    reg [511:0] combat_log_msg;
    reg [511:0] player_action_log;

    // Moving Cursors & Menus
    reg         title_cursor;
    reg         title_confirmed;
    reg         diff_cursor;
    reg         diff_confirmed;
    reg [1:0]   squad_cursor;
    reg         squad_confirmed;

    reg [2:0]   action_cursor;
    reg [2:0]   limb_cursor;
    reg         coin_cursor;
    reg [1:0]   skill_cursor;
    reg [2:0]   bag_cursor;

    // Menu loop helpers
    reg         action_confirmed;
    reg [2:0]   action_selected;
    reg         sub_confirmed;
    reg         sub_cancelled;
    reg [2:0]   limb_selected;
    reg         coin_selected;
    reg [1:0]   skill_selected;

    // Game lifecycle
    reg game_running;
    reg game_victory;
    reg game_over;

    // Helper function to check if whole team fainted
    function is_team_dead;
        input integer dummy;
        begin
            is_team_dead = (team_hp[0] == 0 && team_hp[1] == 0 && team_hp[2] == 0 && team_hp[3] == 0);
        end
    endfunction

    // Helper task to switch to next alive member with Boxed Alert
    task switch_to_alive_member;
        integer k;
        reg [1:0] old_idx;
        begin
            if (team_hp[active_member] == 0) begin
                old_idx = active_member;
                for (k = 3; k >= 0; k = k - 1) begin
                    if (team_hp[k] > 0) active_member = k[1:0];
                end
                if (active_member != old_idx) begin
                    ui.notify_hero_fallen(team_name[old_idx], team_name[active_member]);
                end
            end
        end
    endtask

    // Helper task to initialize enemy limbs based on enemy stats
    task init_enemy_limbs;
        input [7:0] total_hp;
        begin
            // Head: 25% of HP (Decapitation = Instant Kill)
            enemy_head_max  = (total_hp * 8'd25) / 8'd100;
            if (enemy_head_max < 8'd15) enemy_head_max = 8'd15;
            enemy_head_hp   = enemy_head_max;

            // Torso: 75% of HP (Core Vitals)
            enemy_torso_max = (total_hp * 8'd75) / 8'd100;
            if (enemy_torso_max < 8'd40) enemy_torso_max = 8'd40;
            enemy_torso_hp  = enemy_torso_max;

            // Right Arm (Weapon Arm): 35% of HP
            enemy_arm_r_max = (total_hp * 8'd35) / 8'd100;
            if (enemy_arm_r_max < 8'd20) enemy_arm_r_max = 8'd20;
            enemy_arm_r_hp  = enemy_arm_r_max;

            // Left Arm (Shield/Claw): 30% of HP
            enemy_arm_l_max = (total_hp * 8'd30) / 8'd100;
            if (enemy_arm_l_max < 8'd18) enemy_arm_l_max = 8'd18;
            enemy_arm_l_hp  = enemy_arm_l_max;

            // Right Leg: 30% of HP
            enemy_leg_r_max = (total_hp * 8'd30) / 8'd100;
            if (enemy_leg_r_max < 8'd18) enemy_leg_r_max = 8'd18;
            enemy_leg_r_hp  = enemy_leg_r_max;

            // Left Leg: 30% of HP
            enemy_leg_l_max = (total_hp * 8'd30) / 8'd100;
            if (enemy_leg_l_max < 8'd18) enemy_leg_l_max = 8'd18;
            enemy_leg_l_hp  = enemy_leg_l_max;

            enemy_is_crawling = 1'b0;
            enemy_is_disarmed = 1'b0;
        end
    endtask

    // ========================================================================
    // MAIN GAME EXECUTION
    // ========================================================================
    initial begin
        clk   = 0;
        rst_n = 0;
        #20 rst_n = 1;

        bag_poppy        = 8'd10;
        bag_marijuana    = 8'd3;
        bag_bread        = 8'd5;
        bag_meat         = 8'd3;
        bag_ale          = 8'd4;
        bag_keys         = 8'd0;
        player_x         = 2;
        player_y         = 2;
        step_count       = 0;
        cleared_mask     = 720'd0;
        encountered_mask = 37'd0;
        monsters_defeated_count = 0;
        active_member    = 2'd0;
        game_running     = 1'b1;
        game_victory     = 1'b0;
        game_over        = 1'b0;
        map_alert_msg    = 0;

        title_cursor    = 1'b0;
        title_confirmed = 1'b0;
        diff_cursor     = 1'b0;
        diff_confirmed  = 1'b0;
        squad_cursor    = 2'd0;
        squad_confirmed = 1'b0;

        action_cursor    = 3'd0;
        limb_cursor      = 3'd0;
        coin_cursor      = 1'b0;
        skill_cursor     = 2'd0;
        bag_cursor       = 3'd0;

        // 1. Title Screen (Direct Numeric Input: [1] Start | [0] Quit)
        ui.render_title_screen(1'b0);
        $write("  >> Enter command [1: Start Expedition | 0: Abandon Hope]: ");
        $fflush();
        scan_ret = $fscanf(32'h80000000, "%s", str_input);
        cmd_char = str_input[7:0];
        if (cmd_char == "0" || cmd_char == "q" || cmd_char == "Q") begin
            $display("\n  >> Expedition abandoned before entering the darkness.");
            $finish;
        end

        // 1.5 Difficulty Selection Screen (Direct Numeric Input: [1] Normal | [2] Hardcore)
        ui.render_difficulty_select_screen(1'b0);
        $write("  >> Select Difficulty [1: Fear & Hunger (Normal) | 2: Terror & Starvation (Hard)]: ");
        $fflush();
        scan_ret = $fscanf(32'h80000000, "%s", str_input);
        cmd_char = str_input[7:0];

        if (cmd_char == "2" || cmd_char == "h" || cmd_char == "H") begin
            is_hard_mode       = 1'b1;
            heal_poppy_val     = 8'd30;
            heal_marijuana_val = 8'd70;
            $display("\n\033[1;31m  >> [TERROR & STARVATION ACTIVATED] The dark catacombs will show no mercy.\033[0m\n");
        end else begin
            is_hard_mode       = 1'b0;
            heal_poppy_val     = 8'd50;
            heal_marijuana_val = 8'd120;
            $display("\n\033[1;32m  >> [FEAR & HUNGER ACTIVATED] Ready your party for the harrowing descent.\033[0m\n");
        end

        // 2. Draft 4 Characters Screen (Direct Numeric Input: 1-4)
        ui.render_character_select_screen(is_hard_mode, 2'd0);
        $write("  >> Select Squad Preset [1: Balanced | 2: Occult | 3: Mercenaries | 4: Custom]: ");
        $fflush();
        scan_ret = $fscanf(32'h80000000, "%s", str_input);
        cmd_char = str_input[7:0];

        if (cmd_char == "2") begin
            // Occult Sorcery: Enki, Nas'hrah, The Girl, Cahara
            c1 = 3; c2 = 8; c3 = 7; c4 = 1;
        end else if (cmd_char == "3") begin
            // Iron Mercenaries: Ragnvaldr, Le'garde, D'arce, Cahara
            c1 = 4; c2 = 5; c3 = 2; c4 = 1;
        end else if (cmd_char == "4") begin
            // Custom Squad: Choose any 4 Explorer IDs
            $write("     Enter ID for Explorer 1 (1-8): "); $fflush(); scan_ret = $fscanf(32'h80000000, "%s", str_input); c1 = str_input[7:0] - "0";
            $write("     Enter ID for Explorer 2 (1-8): "); $fflush(); scan_ret = $fscanf(32'h80000000, "%s", str_input); c2 = str_input[7:0] - "0";
            $write("     Enter ID for Explorer 3 (1-8): "); $fflush(); scan_ret = $fscanf(32'h80000000, "%s", str_input); c3 = str_input[7:0] - "0";
            $write("     Enter ID for Explorer 4 (1-8): "); $fflush(); scan_ret = $fscanf(32'h80000000, "%s", str_input); c4 = str_input[7:0] - "0";
        end else begin
            // Balanced Vanguard (Default): Cahara, D'arce, Enki, Ragnvaldr
            c1 = 1; c2 = 2; c3 = 3; c4 = 4;
        end

        if (c1 < 1 || c1 > 8) c1 = 1;
        if (c2 < 1 || c2 > 8) c2 = 2;
        if (c3 < 1 || c3 > 8) c3 = 3;
        if (c4 < 1 || c4 > 8) c4 = 4;

        team_char_id[0] = c1[3:0];
        team_char_id[1] = c2[3:0];
        team_char_id[2] = c3[3:0];
        team_char_id[3] = c4[3:0];

        char_db.get_character(team_char_id[0], is_hard_mode, team_hp[0], team_atk[0], team_def[0], team_name[0], team_class[0]);
        team_max[0] = team_hp[0]; team_mind[0] = 8'd100; team_hunger[0] = 8'd0;

        char_db.get_character(team_char_id[1], is_hard_mode, team_hp[1], team_atk[1], team_def[1], team_name[1], team_class[1]);
        team_max[1] = team_hp[1]; team_mind[1] = 8'd100; team_hunger[1] = 8'd0;

        char_db.get_character(team_char_id[2], is_hard_mode, team_hp[2], team_atk[2], team_def[2], team_name[2], team_class[2]);
        team_max[2] = team_hp[2]; team_mind[2] = 8'd100; team_hunger[2] = 8'd0;

        char_db.get_character(team_char_id[3], is_hard_mode, team_hp[3], team_atk[3], team_def[3], team_name[3], team_class[3]);
        team_max[3] = team_hp[3]; team_mind[3] = 8'd100; team_hunger[3] = 8'd0;

        $display("\n\033[1;32m  >> Squad successfully recruited into the Labyrinth of Shadows!\033[0m");
        ui.render_squad_screen(
            team_char_id[0], team_char_id[1], team_char_id[2], team_char_id[3],
            team_name[0], team_name[1], team_name[2], team_name[3],
            team_class[0], team_class[1], team_class[2], team_class[3],
            team_hp[0], team_max[0], team_hp[1], team_max[1],
            team_hp[2], team_max[2], team_hp[3], team_max[3],
            team_atk[0], team_def[0], team_atk[1], team_def[1],
            team_atk[2], team_def[2], team_atk[3], team_def[3],
            active_member[1:0]
        );
        $write("  \033[1;33m>> Press [C] or Enter to descend into the dungeon: \033[0m");
        $fflush();
        scan_ret = $fscanf(32'h80000000, "%s", str_input);

        // ====================================================================
        // 3. MAIN LABYRINTH EXPLORATION LOOP
        // ====================================================================
        while (game_running && !game_victory && !game_over) begin
            // Render Map Screen with Survival HUD
            ui.render_map_screen(
                is_hard_mode,
                player_x, player_y, step_count,
                bag_poppy, bag_marijuana, bag_keys,
                team_name[0], team_name[1], team_name[2], team_name[3],
                team_hp[0], team_max[0], team_hp[1], team_max[1],
                team_hp[2], team_max[2], team_hp[3], team_max[3],
                cleared_mask
            );

            // Display Survival Status Gauges (Mind & Hunger) for Active Member
            $display("  \033[1;37mFRONTLINE:\033[0m \033[1;33m%-12s\033[0m | \033[38;2;80;180;255m[MIND] %3d/100\033[0m | \033[38;2;255;160;40m[HUNGER] %3d/100\033[0m | \033[38;2;255;105;180m[HP] %3d/%3d\033[0m\033[K",
                     team_name[active_member], team_mind[active_member], team_hunger[active_member], team_hp[active_member], team_max[active_member]);
            $display("\033[1;32m==================================================================================\033[0m\033[K");

            if (map_alert_msg != 0) begin
                $display("  \033[1;33m>> [NOTICE]: %0s\033[0m\033[K", map_alert_msg);
                map_alert_msg = 0;
            end

            $write("  >> Move [W/A/S/D or Arrow Keys] | Pouch [I] | Party Roster [P] | Quit [Q]: \033[K\033[J");
            $fflush();
            scan_ret = $fscanf(32'h80000000, "%s", str_input);
            if (scan_ret <= 0) begin
                game_running = 1'b0;
                cmd_char = "q";
            end else begin
                cmd_char = str_input[7:0];
            end

            if (cmd_char == "q" || cmd_char == "Q") begin
                game_running = 1'b0;
                $display("\n  >> Surrendered to the oppressive terror and darkness.");
            end else if (cmd_char == "p" || cmd_char == "P") begin
                ui.render_squad_screen(
                    team_char_id[0], team_char_id[1], team_char_id[2], team_char_id[3],
                    team_name[0], team_name[1], team_name[2], team_name[3],
                    team_class[0], team_class[1], team_class[2], team_class[3],
                    team_hp[0], team_max[0], team_hp[1], team_max[1],
                    team_hp[2], team_max[2], team_hp[3], team_max[3],
                    team_atk[0], team_def[0], team_atk[1], team_def[1],
                    team_atk[2], team_def[2], team_atk[3], team_def[3],
                    active_member[1:0]
                );
                $write("  \033[1;33m>> Press [C] or Enter to return to exploration: \033[0m\033[K");
                $fflush();
                scan_ret = $fscanf(32'h80000000, "%s", str_input);
                $write("\033[2J\033[H");
            end else if (cmd_char == "i" || cmd_char == "I") begin
                // Open Survival Pouch outside combat with Moving Cursor
                sub_confirmed = 1'b0;
                sub_cancelled = 1'b0;
                while (!sub_confirmed && !sub_cancelled) begin
                    ui.render_survival_bag_interactive(
                        bag_cursor, is_hard_mode,
                        bag_poppy, bag_marijuana, bag_bread, bag_meat, bag_ale, bag_keys
                    );
                    $write("  >> Select item [W/S: Move Cursor | E/Enter/Space: Use | 1-5: Quick Select | C: Close Bag]: ");
                    $fflush();
                    scan_ret = $fscanf(32'h80000000, "%s", str_input);
                    cmd_char = str_input[7:0];
                    if (cmd_char == "w" || cmd_char == "W" || cmd_char == "k") begin
                        if (bag_cursor == 3'd0) bag_cursor = 3'd4;
                        else bag_cursor = bag_cursor - 3'd1;
                    end else if (cmd_char == "s" || cmd_char == "S" || cmd_char == "j") begin
                        if (bag_cursor == 3'd4) bag_cursor = 3'd0;
                        else bag_cursor = bag_cursor + 3'd1;
                    end else if (cmd_char == "e" || cmd_char == "E" || cmd_char == "x" || cmd_char == "X" || cmd_char == " ") begin
                        sub_confirmed = 1'b1;
                    end else if (cmd_char >= "1" && cmd_char <= "5") begin
                        bag_cursor = (cmd_char - "0") - 1;
                        sub_confirmed = 1'b1;
                    end else if (cmd_char == "c" || cmd_char == "C" || cmd_char == "q") begin
                        sub_cancelled = 1'b1;
                    end
                end

                if (sub_confirmed) begin
                    if (bag_cursor == 3'd0 && bag_poppy > 0) begin
                        bag_poppy = bag_poppy - 1;
                        team_hp[active_member] = team_hp[active_member] + heal_poppy_val;
                        if (team_hp[active_member] > team_max[active_member]) team_hp[active_member] = team_max[active_member];
                        ui.notify_consume_item("Poppy Flower", team_name[active_member], heal_poppy_val, team_hp[active_member], team_max[active_member]);
                    end else if (bag_cursor == 3'd1 && bag_marijuana > 0) begin
                        bag_marijuana = bag_marijuana - 1;
                        team_hp[active_member] = team_hp[active_member] + heal_marijuana_val;
                        if (team_hp[active_member] > team_max[active_member]) team_hp[active_member] = team_max[active_member];
                        team_mind[active_member] = team_mind[active_member] + 8'd20;
                        if (team_mind[active_member] > 8'd100) team_mind[active_member] = 8'd100;
                        ui.notify_consume_item("Marijuana Herb", team_name[active_member], heal_marijuana_val, team_hp[active_member], team_max[active_member]);
                    end else if (bag_cursor == 3'd2 && bag_bread > 0) begin
                        bag_bread = bag_bread - 1;
                        if (team_hunger[active_member] > 8'd40) team_hunger[active_member] = team_hunger[active_member] - 8'd40;
                        else team_hunger[active_member] = 8'd0;
                        $display("\n\033[1;32m  >> [EAT MOLDY BREAD]: Hunger of %s reduced by 40! (Current Hunger: %0d/100)\033[0m\n", team_name[active_member], team_hunger[active_member]);
                    end else if (bag_cursor == 3'd3 && bag_meat > 0) begin
                        bag_meat = bag_meat - 1;
                        if (team_hunger[active_member] > 8'd60) team_hunger[active_member] = team_hunger[active_member] - 8'd60;
                        else team_hunger[active_member] = 8'd0;
                        team_hp[active_member] = team_hp[active_member] + 8'd15;
                        if (team_hp[active_member] > team_max[active_member]) team_hp[active_member] = team_max[active_member];
                        $display("\n\033[1;32m  >> [EAT DRIED MEAT]: Hunger reduced by 60, restored 15 HP! (Hunger: %0d/100, HP: %0d/%0d)\033[0m\n", team_name[active_member], team_hunger[active_member], team_hp[active_member], team_max[active_member]);
                    end else if (bag_cursor == 3'd4 && bag_ale > 0) begin
                        bag_ale = bag_ale - 1;
                        team_mind[active_member] = team_mind[active_member] + 8'd35;
                        if (team_mind[active_member] > 8'd100) team_mind[active_member] = 8'd100;
                        $display("\n\033[1;36m  >> [DRINK ALE FLASK]: Warm spirits cleanse terror! Mind restored +35! (Mind: %0d/100)\033[0m\n", team_name[active_member], team_mind[active_member]);
                    end else begin
                        $display("\n\033[1;31m  >> Supplies depleted for this item!\033[0m\n");
                    end
                end
                $write("\033[2J\033[H");
            end else begin
                // Navigation Input (WASD or Arrow Keys)
                target_x = player_x;
                target_y = player_y;
                if (cmd_char == "w" || cmd_char == "W") target_y = player_y - 1;
                else if (cmd_char == "s" || cmd_char == "S") target_y = player_y + 1;
                else if (cmd_char == "a" || cmd_char == "A") target_x = player_x - 1;
                else if (cmd_char == "d" || cmd_char == "D") target_x = player_x + 1;

                target_tile = map_db.get_tile(target_x, target_y);
                target_idx  = target_x + (target_y * `MAP_WIDTH);

                if (target_tile == `TILE_WALL) begin
                    map_alert_msg = "Solid damp stone wall obstructs your path.";
                end else if (target_tile == `TILE_GATE) begin
                    if (bag_keys >= 3) begin
                        ui.notify_gate_status(bag_keys);
                        game_victory = 1'b1;
                    end else begin
                        ui.notify_gate_status(bag_keys);
                    end
                end else if (target_tile == `TILE_CHEST && !cleared_mask[target_idx]) begin
                    // Move onto Chest Tile
                    player_x   = target_x;
                    player_y   = target_y;
                    step_count = step_count + 1;

                    r_roll = ($random % 100);
                    if (r_roll < 0) r_roll = -r_roll;

                    if (r_roll < 20) begin
                        // 20% Mimic Trap Encounter
                        cur_enemy_id = 6'd23; // Mimic ID
                        mon_db.get_monster(cur_enemy_id, 1'b0, cur_enemy_hp, cur_enemy_atk, cur_enemy_def, cur_enemy_weight, dummy_el);
                        cur_enemy_max = cur_enemy_hp;
                        init_enemy_limbs(cur_enemy_hp);

                        $display("\n\033[41;1;37m  >>> [MIMIC TRAP TRIGGERED!] The ancient chest sprouts razor teeth and lunges forward! <<<  \033[0m\a");
                        in_combat   = 1'b1;
                        combat_turn = 4'd1;
                        combat_fled = 1'b0;
                        combat_log_msg = "MIMIC TRAP TRIGGERED! The chest sprouts razor teeth and lunges forward!";
                    end else begin
                        // 80% Safe Bounty Chest
                        r_roll = ($random % 100);
                        if (r_roll < 0) r_roll = -r_roll;
                        if (r_roll < 35) begin
                            bag_keys = bag_keys + 1;
                            ui.render_chest_open_screen(1'b0, "Dungeon Key (Ancient Runic Key)", 8'd1);
                            ui.notify_receive_item("Ancient Vault", "Dungeon Key", 8'd1);
                        end else if (r_roll < 60) begin
                            bag_bread = bag_bread + 2;
                            bag_meat  = bag_meat + 1;
                            ui.render_chest_open_screen(1'b0, "Rations & Salted Meat", 8'd3);
                            ui.notify_receive_item("Ancient Vault", "Moldy Bread x2 & Dried Meat x1", 8'd3);
                        end else if (r_roll < 80) begin
                            bag_marijuana = bag_marijuana + 1;
                            bag_ale       = bag_ale + 1;
                            ui.render_chest_open_screen(1'b0, "Marijuana Herb & Ale Flask", 8'd2);
                            ui.notify_receive_item("Ancient Vault", "Marijuana Herb x1 & Ale Flask x1", 8'd2);
                        end else begin
                            bag_poppy = bag_poppy + 1;
                            ui.render_chest_open_screen(1'b0, "White Poppy Flower", 8'd1);
                            ui.notify_receive_item("Ancient Vault", "Poppy Flower", 8'd1);
                        end
                        cleared_mask[target_idx] = 1'b1;
                        $write("\n  \033[1;33m>> Press [C] or Enter to collect bounty and continue: \033[0m\033[K");
                        $fflush();
                        scan_ret = $fscanf(32'h80000000, "%s", str_input);
                        $write("\033[2J\033[H");
                    end
                end else if (target_tile == `TILE_MONSTER && !cleared_mask[target_idx]) begin
                    // Move onto Monster Tile
                    player_x   = target_x;
                    player_y   = target_y;
                    step_count = step_count + 1;
                    $write("\033[2J\033[H");

                    // Select non-repeating monster
                    cur_enemy_id = 6'd1;
                    for (int_choice = 1; int_choice <= 36; int_choice = int_choice + 1) begin
                        if (!encountered_mask[int_choice] && int_choice != 23) begin
                            cur_enemy_id = int_choice[5:0];
                        end
                    end

                    // Check elite
                    r_roll = ($random % 100);
                    if (r_roll < 0) r_roll = -r_roll;
                    cur_enemy_is_elite = (r_roll < 25) ? 1'b1 : 1'b0;

                    mon_db.get_monster(cur_enemy_id, cur_enemy_is_elite, cur_enemy_hp, cur_enemy_atk, cur_enemy_def, cur_enemy_weight, dummy_el);
                    cur_enemy_max = cur_enemy_hp;
                    init_enemy_limbs(cur_enemy_hp);
                    encountered_mask[cur_enemy_id] = 1'b1;

                    in_combat   = 1'b1;
                    combat_turn = 4'd1;
                    combat_fled = 1'b0;
                    combat_log_msg = "Encounter started! Choose an action hotkey from the deck below.";
                    $display("\n\033[1;35m  >> [ENCOUNTER]: An ominous shadow descends upon you from the dark!\033[0m\a");
                end else begin
                    // Regular pathway walk
                    player_x   = target_x;
                    player_y   = target_y;
                    step_count = step_count + 1;

                    // Survival ticks: Hunger +1 every 5 steps, Mind -1 every 8 steps
                    if (step_count % 5 == 0) begin
                        if (team_hunger[active_member] < 8'd100)
                            team_hunger[active_member] = team_hunger[active_member] + 8'd1;
                    end
                    if (step_count % 8 == 0) begin
                        if (team_mind[active_member] > 8'd0)
                            team_mind[active_member] = team_mind[active_member] - 8'd1;
                    end

                    // Starvation penalty
                    if (team_hunger[active_member] >= 8'd100) begin
                        if (team_hp[active_member] > 8'd5) team_hp[active_member] = team_hp[active_member] - 8'd5;
                        else team_hp[active_member] = 8'd1;
                        $display("\033[1;31m  >> [STARVATION]: Agonizing stomach cramps! Lost 5 HP due to starvation!\033[0m");
                    end
                end
            end

            // ================================================================
            // 4. UNIFIED TACTICAL COMBAT ENGINE (BODY PARTS & COIN FLIP)
            // ================================================================
            while (in_combat && !is_team_dead(0)) begin
                switch_to_alive_member();

                // ------------------------------------------------------------
                // 1. RENDER 50/50 DIAGONAL SCREEN (Enemy Top-Right, Hero Bottom-Left)
                // ------------------------------------------------------------
                ui.render_battle_screen_diagonal(
                    is_hard_mode,
                    combat_turn,
                    // Hero Data
                    team_char_id[active_member],
                    team_name[active_member],
                    team_hp[active_member],
                    team_max[active_member],
                    team_mind[active_member],
                    team_hunger[active_member],
                    team_atk[active_member],
                    team_def[active_member],
                    bag_poppy,
                    bag_marijuana,
                    bag_bread,
                    bag_ale,
                    // Squad
                    team_char_id[0], team_char_id[1], team_char_id[2], team_char_id[3],
                    team_hp[0], team_hp[1], team_hp[2], team_hp[3],
                    // Foe Data
                    cur_enemy_id,
                    cur_enemy_is_elite,
                    cur_enemy_hp,
                    cur_enemy_max,
                    enemy_head_hp, enemy_head_max,
                    enemy_torso_hp, enemy_torso_max,
                    enemy_arm_r_hp, enemy_arm_r_max,
                    enemy_arm_l_hp, enemy_arm_l_max,
                    enemy_leg_r_hp, enemy_leg_l_max,
                    enemy_is_crawling,
                    enemy_is_disarmed,
                    // Event Log
                    combat_log_msg
                );

                // ------------------------------------------------------------
                // 2. DIRECT ACTION DECK INPUT (Instant 1 Key + Enter)
                // ------------------------------------------------------------
                $write("  >> Direct Action [Type Hotkey + Enter]: ");
                $fflush();
                scan_ret = $fscanf(32'h80000000, "%s", str_input);
                if (scan_ret <= 0) begin
                    in_combat = 1'b0;
                    game_running = 1'b0;
                    cmd_char = "f";
                end else begin
                    cmd_char = str_input[7:0];
                end

                calc_dmg = (team_atk[active_member] > cur_enemy_def) ? (team_atk[active_member] - cur_enemy_def + 6) : 8;
                action_confirmed = 1'b1;
                action_selected = 3'd0;

                // [H]: TARGET HEAD (25% Decapitation Instakill, 100% if Crawling)
                if (cmd_char == "h" || cmd_char == "H") begin
                    action_selected = 3'd1;
                    r_roll = ($random % 100); if (r_roll < 0) r_roll = -r_roll;
                    if (enemy_is_crawling || r_roll < 25) begin
                        ui.render_slash_fx();
                        if (enemy_head_hp > calc_dmg) enemy_head_hp = enemy_head_hp - calc_dmg;
                        else enemy_head_hp = 8'd0;

                        if (enemy_head_hp == 0) begin
                            cur_enemy_hp = 8'd0;
                            player_action_log = "[DECAPITATION INSTAKILL]: Severed foe's head completely! Enemy dead!";
                        end else begin
                            if (cur_enemy_hp > calc_dmg) cur_enemy_hp = cur_enemy_hp - calc_dmg;
                            else cur_enemy_hp = 8'd0;
                            $sformat(player_action_log, "Lethal strike on HEAD for %0d DMG! (Head HP: %0d/%0d)", calc_dmg, enemy_head_hp, enemy_head_max);
                        end
                    end else begin
                        player_action_log = "[MISSED]: Foe dodged away from your strike to the head!";
                    end
                end
                // [T]: TARGET TORSO (95% Core Vitals)
                else if (cmd_char == "t" || cmd_char == "T") begin
                    action_selected = 3'd1;
                    r_roll = ($random % 100); if (r_roll < 0) r_roll = -r_roll;
                    if (r_roll < 95) begin
                        ui.render_slash_fx();
                        if (enemy_torso_hp > calc_dmg) enemy_torso_hp = enemy_torso_hp - calc_dmg;
                        else enemy_torso_hp = 8'd0;

                        if (cur_enemy_hp > calc_dmg) cur_enemy_hp = cur_enemy_hp - calc_dmg;
                        else cur_enemy_hp = 8'd0;

                        if (enemy_torso_hp == 0) begin
                            cur_enemy_hp = 8'd0;
                            player_action_log = "[VITALS PUNCTURED]: Pierced torso core! Enemy slain!";
                        end else begin
                            $sformat(player_action_log, "Thrust pierced TORSO for %0d DMG! (Torso HP: %0d/%0d)", calc_dmg, enemy_torso_hp, enemy_torso_max);
                        end
                    end else begin
                        player_action_log = "[MISSED]: Thrust to torso glanced off stone armor!";
                    end
                end
                // [R]: TARGET RIGHT ARM (80% Disarm Weapon)
                else if (cmd_char == "r" || cmd_char == "R") begin
                    action_selected = 3'd1;
                    r_roll = ($random % 100); if (r_roll < 0) r_roll = -r_roll;
                    if (r_roll < 80) begin
                        ui.render_slash_fx();
                        if (enemy_arm_r_hp > calc_dmg) enemy_arm_r_hp = enemy_arm_r_hp - calc_dmg;
                        else enemy_arm_r_hp = 8'd0;

                        if (cur_enemy_hp > calc_dmg) cur_enemy_hp = cur_enemy_hp - calc_dmg;
                        else cur_enemy_hp = 8'd0;

                        if (enemy_arm_r_hp == 0 && !enemy_is_disarmed) begin
                            enemy_is_disarmed = 1'b1;
                            player_action_log = "[DISARMED !]: Weapon arm severed! Enemy attack cut by 60%!";
                        end else begin
                            $sformat(player_action_log, "Slashed RIGHT ARM for %0d DMG! (Arm HP: %0d/%0d)", calc_dmg, enemy_arm_r_hp, enemy_arm_r_max);
                        end
                    end else begin
                        player_action_log = "[MISSED]: Strike to the right arm was deflected!";
                    end
                end
                // [L]: TARGET LEFT ARM (80% Break Guard)
                else if (cmd_char == "l" || cmd_char == "L") begin
                    action_selected = 3'd1;
                    r_roll = ($random % 100); if (r_roll < 0) r_roll = -r_roll;
                    if (r_roll < 80) begin
                        ui.render_slash_fx();
                        if (enemy_arm_l_hp > calc_dmg) enemy_arm_l_hp = enemy_arm_l_hp - calc_dmg;
                        else enemy_arm_l_hp = 8'd0;

                        if (cur_enemy_hp > calc_dmg) cur_enemy_hp = cur_enemy_hp - calc_dmg;
                        else cur_enemy_hp = 8'd0;

                        if (enemy_arm_l_hp == 0) begin
                            player_action_log = "[OFFHAND CRUSHED]: Left arm destroyed! Guard permanently broken!";
                        end else begin
                            $sformat(player_action_log, "Slashed LEFT ARM for %0d DMG! (Arm HP: %0d/%0d)", calc_dmg, enemy_arm_l_hp, enemy_arm_l_max);
                        end
                    end else begin
                        player_action_log = "[MISSED]: Strike to the left arm missed!";
                    end
                end
                // [K]: TARGET LEGS (85% Force Crawl)
                else if (cmd_char == "k" || cmd_char == "K") begin
                    action_selected = 3'd1;
                    r_roll = ($random % 100); if (r_roll < 0) r_roll = -r_roll;
                    if (r_roll < 85) begin
                        ui.render_slash_fx();
                        if (enemy_leg_r_hp > calc_dmg) enemy_leg_r_hp = enemy_leg_r_hp - calc_dmg;
                        else enemy_leg_r_hp = 8'd0;

                        if (cur_enemy_hp > calc_dmg) cur_enemy_hp = cur_enemy_hp - calc_dmg;
                        else cur_enemy_hp = 8'd0;

                        if (enemy_leg_r_hp == 0 && !enemy_is_crawling) begin
                            enemy_is_crawling = 1'b1;
                            player_action_log = "[CRAWLING !]: Legs severed! Foe falls! Head hit chance is 100%!";
                        end else begin
                            $sformat(player_action_log, "Slashed LEGS for %0d DMG! (Legs HP: %0d/%0d)", calc_dmg, enemy_leg_r_hp, enemy_leg_l_max);
                        end
                    end else begin
                        player_action_log = "[MISSED]: Foe leapt back to evade leg strike!";
                    end
                end
                // [1]: SKILL 1
                else if (cmd_char == "1") begin
                    action_selected = 3'd2;
                    case (team_char_id[active_member])
                        4'd1: begin // Cahara Steal
                            bag_bread = bag_bread + 1;
                            if (cur_enemy_hp > 8'd14) cur_enemy_hp = cur_enemy_hp - 8'd14; else cur_enemy_hp = 0;
                            player_action_log = "[STEAL]: Cahara inflicts 14 DMG & steals Moldy Bread!";
                        end
                        4'd2: begin // D'arce Fast Stance
                            calc_dmg = team_atk[active_member] * 2;
                            if (cur_enemy_hp > calc_dmg) cur_enemy_hp = cur_enemy_hp - calc_dmg; else cur_enemy_hp = 0;
                            ui.render_slash_fx();
                            $sformat(player_action_log, "[FAST STANCE]: D'arce double slashes for %0d DMG!", calc_dmg);
                        end
                        4'd3: begin // Enki Black Orb
                            if (cur_enemy_hp > 8'd48) cur_enemy_hp = cur_enemy_hp - 8'd48; else cur_enemy_hp = 0;
                            player_action_log = "[BLACK ORB]: Enki hurls dark abyssal magic for 48 DMG!";
                        end
                        4'd4: begin // Ragnvaldr War Cry
                            team_atk[active_member] = team_atk[active_member] + 8'd12;
                            player_action_log = "[WAR CRY]: Ragnvaldr roars in berserk fury! ATK +12!";
                        end
                        4'd5: begin // Le'garde Leg Sweep
                            enemy_is_crawling = 1'b1;
                            if (cur_enemy_hp > 8'd22) cur_enemy_hp = cur_enemy_hp - 8'd22; else cur_enemy_hp = 0;
                            player_action_log = "[LEG SWEEP]: Le'garde strikes for 22 DMG and forces CRAWL!";
                        end
                        4'd6: begin // Moonless Primal Bite
                            if (cur_enemy_hp > 8'd34) cur_enemy_hp = cur_enemy_hp - 8'd34; else cur_enemy_hp = 0;
                            player_action_log = "[PRIMAL BITE]: Moonless tears flesh for 34 DMG!";
                        end
                        4'd7: begin // The Girl Mischief
                            player_action_log = "[MISCHIEF]: The Girl throws pebbles, confusing the beast!";
                        end
                        4'd8: begin // Nas'hrah Combustion
                            if (cur_enemy_hp > 8'd60) cur_enemy_hp = cur_enemy_hp - 8'd60; else cur_enemy_hp = 0;
                            player_action_log = "[COMBUSTION]: Nas'hrah ignites the foe for 60 DMG!";
                        end
                        default: begin
                            if (cur_enemy_hp > 8'd20) cur_enemy_hp = cur_enemy_hp - 8'd20; else cur_enemy_hp = 0;
                            player_action_log = "[STRIKE]: Inflicted 20 DMG with martial discipline!";
                        end
                    endcase
                end
                // [2]: SKILL 2
                else if (cmd_char == "2") begin
                    action_selected = 3'd2;
                    case (team_char_id[active_member])
                        4'd1: begin // Cahara En Garde
                            player_action_log = "[EN GARDE]: Cahara enters parry stance! Incoming DMG cut 50%!";
                        end
                        4'd2: begin // D'arce Loving Whispers
                            team_hp[active_member] = team_hp[active_member] + 8'd45;
                            if (team_hp[active_member] > team_max[active_member]) team_hp[active_member] = team_max[active_member];
                            player_action_log = "[LOVING WHISPERS]: Sylvian holy prayer restored +45 HP!";
                        end
                        4'd3: begin // Enki Blood Sacrifice
                            team_mind[active_member] = team_mind[active_member] + 8'd25;
                            if (team_mind[active_member] > 8'd100) team_mind[active_member] = 8'd100;
                            player_action_log = "[BLOOD SACRIFICE]: Forbidden runes restore +25 Mind!";
                        end
                        4'd4: begin // Ragnvaldr Devour
                            if (team_hunger[active_member] > 8'd30) team_hunger[active_member] = team_hunger[active_member] - 8'd30; else team_hunger[active_member] = 0;
                            if (cur_enemy_hp > 8'd20) cur_enemy_hp = cur_enemy_hp - 8'd20; else cur_enemy_hp = 0;
                            player_action_log = "[DEVOUR]: Ragnvaldr bites foe for 20 DMG! Hunger -30!";
                        end
                        4'd5: begin // Le'garde Tactician
                            team_def[active_member] = team_def[active_member] + 8'd15;
                            player_action_log = "[TACTICIAN]: Le'garde commands defense! DEF +15!";
                        end
                        4'd6: begin // Moonless Howl
                            if (cur_enemy_atk > 8'd10) cur_enemy_atk = cur_enemy_atk - 8'd10; else cur_enemy_atk = 8'd5;
                            player_action_log = "[HOWL]: Moonless howls! Enemy ATK reduced!";
                        end
                        4'd7: begin // The Girl Loving Hug
                            team_mind[active_member] = team_mind[active_member] + 8'd40;
                            if (team_mind[active_member] > 8'd100) team_mind[active_member] = 8'd100;
                            player_action_log = "[LOVING HUG]: The Girl hugs you warmly! Restored +40 Mind!";
                        end
                        4'd8: begin // Nas'hrah Hellfire
                            if (cur_enemy_hp > 8'd85) cur_enemy_hp = cur_enemy_hp - 8'd85; else cur_enemy_hp = 0;
                            player_action_log = "[HELLFIRE]: Nas'hrah casts apocalyptic flames for 85 DMG!";
                        end
                        default: begin
                            team_mind[active_member] = team_mind[active_member] + 8'd20;
                            if (team_mind[active_member] > 8'd100) team_mind[active_member] = 8'd100;
                            player_action_log = "[FOCUS MIND]: Calmed trembling hands, +20 Mind!";
                        end
                    endcase
                end
                // [P]: USE POPPY FLOWER
                else if (cmd_char == "p" || cmd_char == "P") begin
                    action_selected = 3'd3;
                    if (bag_poppy > 0) begin
                        bag_poppy = bag_poppy - 1;
                        team_hp[active_member] = team_hp[active_member] + heal_poppy_val;
                        if (team_hp[active_member] > team_max[active_member]) team_hp[active_member] = team_max[active_member];
                        $sformat(player_action_log, "Applied Poppy Flower! Restored +%0d HP to %s!", heal_poppy_val, team_name[active_member]);
                    end else begin
                        player_action_log = "[EMPTY]: No Poppy Flowers left in pouch!";
                    end
                end
                // [M]: USE MARIJUANA HERB
                else if (cmd_char == "m" || cmd_char == "M") begin
                    action_selected = 3'd3;
                    if (bag_marijuana > 0) begin
                        bag_marijuana = bag_marijuana - 1;
                        team_hp[active_member] = team_hp[active_member] + heal_marijuana_val;
                        if (team_hp[active_member] > team_max[active_member]) team_hp[active_member] = team_max[active_member];
                        $sformat(player_action_log, "Smoked Marijuana Herb! Restored +%0d HP to %s!", heal_marijuana_val, team_name[active_member]);
                    end else begin
                        player_action_log = "[EMPTY]: No Marijuana Herbs left in pouch!";
                    end
                end
                // [B]: EAT MOLDY BREAD
                else if (cmd_char == "b" || cmd_char == "B") begin
                    action_selected = 3'd3;
                    if (bag_bread > 0) begin
                        bag_bread = bag_bread - 1;
                        if (team_hunger[active_member] > 8'd40) team_hunger[active_member] = team_hunger[active_member] - 8'd40;
                        else team_hunger[active_member] = 0;
                        player_action_log = "Swallowed Moldy Bread mid-combat! Hunger reduced by 40!";
                    end else begin
                        player_action_log = "[EMPTY]: No Bread left in pouch!";
                    end
                end
                // [A]: DRINK ALE FLASK
                else if (cmd_char == "a" || cmd_char == "A") begin
                    action_selected = 3'd3;
                    if (bag_ale > 0) begin
                        bag_ale = bag_ale - 1;
                        team_mind[active_member] = team_mind[active_member] + 8'd35;
                        if (team_mind[active_member] > 8'd100) team_mind[active_member] = 8'd100;
                        player_action_log = "Drank spirits from Ale Flask! Cleansed terror, +35 Mind!";
                    end else begin
                        player_action_log = "[EMPTY]: No Ale left in pouch!";
                    end
                end
                // [G]: DEFENSIVE GUARD
                else if (cmd_char == "g" || cmd_char == "G") begin
                    action_selected = 3'd4;
                    $sformat(player_action_log, "%s raised weapon in solid guard! Incoming damage cut 70%%!", team_name[active_member]);
                end
                // [S]: TAG SWITCH FRONTLINE
                else if (cmd_char == "s" || cmd_char == "S") begin
                    action_selected = 3'd5;
                    old_member = active_member;
                    active_member = (active_member + 1) % 4;
                    while (team_hp[active_member] == 0 && active_member != old_member) begin
                        active_member = (active_member + 1) % 4;
                    end
                    $sformat(player_action_log, "[TAG SWITCH]: %s retreats! %s takes the frontline!", team_name[old_member], team_name[active_member]);
                end
                // [F]: FLEE
                else if (cmd_char == "f" || cmd_char == "F") begin
                    action_selected = 3'd6;
                    r_roll = ($random % 100); if (r_roll < 0) r_roll = -r_roll;
                    if (r_roll < 50) begin
                        player_action_log = "[ESCAPED]: Retreated safely into dark corridors!";
                        in_combat = 1'b0;
                        combat_fled = 1'b1;
                        $display("\n\033[1;32m  >> [RETREAT SUCCESSFUL]: You broke away from the clash and escaped into the dark!\033[0m");
                        $write("  \033[1;33m>> Press [C] or Enter to continue back to exploration: \033[0m\033[K");
                        $fflush();
                        scan_ret = $fscanf(32'h80000000, "%s", str_input);
                        $write("\033[2J\033[H");
                    end else begin
                        player_action_log = "[FAILED TO FLEE]: Beast blocked your escape route!";
                    end
                end
                // INVALID INPUT
                else begin
                    action_confirmed = 1'b0;
                    combat_log_msg = "Invalid hotkey! Enter H/T/R/L/K/1/2/P/M/B/A/G/S/F.";
                end

                // ------------------------------------------------------------
                // 3. ENEMY RETALIATION TURN
                // ------------------------------------------------------------
                if (action_confirmed && in_combat && cur_enemy_hp > 0 && !combat_fled) begin
                    r_roll = ($random % 100); if (r_roll < 0) r_roll = -r_roll;

                    // 30% chance lethal skill triggers Coin Flip
                    if (r_roll < 30 && !enemy_is_disarmed) begin
                        sub_confirmed = 1'b0;
                        while (!sub_confirmed) begin
                            ui.render_coin_flip_prompt(coin_cursor, "LABYRINTH BEAST", "LETHAL CLEAVE");
                            $write("  >> Call Coin of Fate [W/S: Flip Face | 1: Heads | 2: Tails | Enter]: ");
                            $fflush();
                            scan_ret = $fscanf(32'h80000000, "%s", str_input);
                            cmd_char = str_input[7:0];

                            if (cmd_char == "w" || cmd_char == "W" || cmd_char == "s" || cmd_char == "S") begin
                                coin_cursor = ~coin_cursor;
                            end else if (cmd_char == "1") begin
                                coin_selected = `COIN_HEADS;
                                sub_confirmed = 1'b1;
                            end else if (cmd_char == "2") begin
                                coin_selected = `COIN_TAILS;
                                sub_confirmed = 1'b1;
                            end else begin
                                coin_selected = coin_cursor;
                                sub_confirmed = 1'b1;
                            end
                        end

                        r_roll = ($random % 2); if (r_roll < 0) r_roll = -r_roll;
                        ui.render_coin_animation(coin_selected, r_roll[0]);

                        if (coin_selected == r_roll[0]) begin
                            if (cur_enemy_hp > 8'd20) cur_enemy_hp = cur_enemy_hp - 8'd20; else cur_enemy_hp = 0;
                            ui.notify_coin_result(1'b1, team_name[active_member], 8'd20, team_hp[active_member], team_max[active_member], team_mind[active_member]);
                            $sformat(combat_log_msg, "%s | [COIN SUCCESS]: Parried lethal cleave and countered for 20 DMG!", player_action_log);
                        end else begin
                            ui.render_screen_shake();
                            calc_dmg = cur_enemy_atk + 8'd25;
                            if (team_hp[active_member] > calc_dmg) team_hp[active_member] = team_hp[active_member] - calc_dmg;
                            else team_hp[active_member] = 8'd0;
                            if (team_mind[active_member] > 8'd20) team_mind[active_member] = team_mind[active_member] - 8'd20;
                            else team_mind[active_member] = 8'd0;
                            ui.notify_coin_result(1'b0, team_name[active_member], calc_dmg, team_hp[active_member], team_max[active_member], team_mind[active_member]);
                            $sformat(combat_log_msg, "%s | [COIN FAILED]: Lethal cleave struck! Took %0d DMG, -20 Mind!", player_action_log, calc_dmg);
                        end
                    end else begin
                        // Regular enemy retaliation
                        if (enemy_is_disarmed) begin
                            calc_dmg = 8'd4;
                        end else if (action_selected == 3'd4) begin
                            calc_dmg = (cur_enemy_atk > team_def[active_member]) ? ((cur_enemy_atk - team_def[active_member]) * 3 / 10) : 3;
                            if (calc_dmg < 2) calc_dmg = 2;
                        end else begin
                            calc_dmg = (cur_enemy_atk > team_def[active_member]) ? (cur_enemy_atk - team_def[active_member] + 4) : 6;
                        end

                        if (team_hp[active_member] > calc_dmg) team_hp[active_member] = team_hp[active_member] - calc_dmg;
                        else team_hp[active_member] = 8'd0;

                        $sformat(combat_log_msg, "%s | Foe retaliated, striking for %0d DMG!", player_action_log, calc_dmg);
                    end
                end else if (action_confirmed) begin
                    combat_log_msg = player_action_log;
                end

                // Turn upkeep
                if (in_combat && !combat_fled && action_confirmed) begin
                    combat_turn = combat_turn + 1;
                    if (team_hunger[active_member] < 8'd100) team_hunger[active_member] = team_hunger[active_member] + 8'd1;
                    if (team_mind[active_member] > 8'd1) team_mind[active_member] = team_mind[active_member] - 8'd1;
                end

                // Check Combat Resolution
                if (cur_enemy_hp == 0) begin
                    $display("\n\033[1;32m+====================================================================================================+\033[0m");
                    $display("\033[1;32m|  \033[42;1;37m >>> GLORIOUS VICTORY: THE FOE HAS BEEN SLAIN! SPOILS SCATTERED ACROSS THE FLOOR! <<< \033[0m\033[1;32m         |\033[0m");
                    $display("\033[1;32m+====================================================================================================+\033[0m\a");
                    in_combat = 1'b0;
                    cleared_mask[target_idx] = 1'b1;
                    monsters_defeated_count = monsters_defeated_count + 1;

                    r_roll = ($random % 100);
                    if (r_roll < 0) r_roll = -r_roll;

                    if (cur_enemy_is_elite || cur_enemy_id == 6'd23) begin
                        if (r_roll < 60) begin
                            bag_keys = bag_keys + 1;
                            ui.notify_receive_item("Elite Adversary Remains (60% Drop)", "Dungeon Key", 8'd1);
                        end
                        bag_meat = bag_meat + 1;
                        bag_ale  = bag_ale + 1;
                        ui.notify_receive_item("Elite Adversary Bounty", "Dried Meat x1 & Ale Flask x1", 8'd2);
                    end else begin
                        if (r_roll < 25) begin
                            bag_keys = bag_keys + 1;
                            ui.notify_receive_item("Monster Remains (25% Drop)", "Dungeon Key", 8'd1);
                        end else if (r_roll < 60) begin
                            bag_bread = bag_bread + 1;
                            ui.notify_receive_item("Monster Bounty", "Moldy Bread", 8'd1);
                        end else begin
                            bag_poppy = bag_poppy + 1;
                            ui.notify_receive_item("Monster Bounty", "Poppy Flower", 8'd1);
                        end
                    end

                    // Pity safety net for keys
                    if (bag_keys < 3) begin
                        if (((10 - monsters_defeated_count) <= (3 - bag_keys)) ||
                            (monsters_defeated_count >= 3 && bag_keys == 0) ||
                            (monsters_defeated_count >= 6 && bag_keys <= 1) ||
                            (monsters_defeated_count >= 8 && bag_keys <= 2)) begin
                            bag_keys = bag_keys + 1;
                            ui.notify_receive_item("Labyrinth Guarantee (Pity Safety Net)", "Dungeon Key", 8'd1);
                        end
                    end

                    $write("  \033[1;33m>> Press [C] or Enter to collect spoils and return to labyrinth: \033[0m\033[K");
                    $fflush();
                    scan_ret = $fscanf(32'h80000000, "%s", str_input);
                    $write("\033[2J\033[H");
                end else if (is_team_dead(0)) begin
                    game_over = 1'b1;
                    in_combat = 1'b0;
                end
            end
        end

        // End of Game Screens
        if (game_victory) begin
            ui.render_victory_screen();
        end else if (game_over) begin
            ui.render_game_over_screen();
        end

        $finish;
    end

endmodule
