// ============================================================================
// Pokemon Lite: Terror & Starvation - Terminal UI (terminal_ui.v)
// 100% ENGLISH HIGH-CONTRAST RETRO ANSI GRAPHICS:
//   1. Redesigned Map:
//      - Walls: Green colored blocks with no text (\033[42m  \033[0m)
//      - Pathways: Path with grid dots (\033[90m .\033[0m)
//      - Player: High-visibility 'O' (\033[1;33;40m O\033[0m)
//      - Monsters: Purple 'M' blocks (\033[45;1;37m M\033[0m)
//      - Chests: Brown 'C' blocks (\033[48;2;139;69;19;1;37m C\033[0m)
//      - Gates: Cyan 'G' blocks EMBEDDED ON RIGHTMOST WALL (\033[46;1;30m G\033[0m)
//   2. Full-Screen Chest Opening Scene (like Battle Screen):
//      - Renders 20x23 TrueColor Opened Chest Sprite Model
//      - 20% Mimic Trap vs 80% Safe Loot with Boxed Notification
//   3. Compact Key Model & Item Models in Inventory
//   4. All notifications cleanly boxed with high-contrast backgrounds
// ============================================================================

`timescale 1ns / 1ps
`include "battle_defs.vh"

module terminal_ui;

    map_rom       u_map(.in_x(32'sd0), .in_y(32'sd0), .out_tile());
    monster_rom   u_mon_db(.monster_id(6'd1), .is_elite(1'b0), .base_hp(), .base_atk(), .base_def(), .spawn_weight(), .is_default_elite());
    character_rom u_char_db();

    // Sprite models for Chest and Key
    reg  [5:0] c_row_t, c_col_t, c_row_b, c_col_b;
    wire [23:0] c_rgb_t, c_rgb_b;
    wire        c_trans_t, c_trans_b;

    chest_sprite_rom u_chest_t (
        .row(c_row_t), .col(c_col_t), .color_rgb(c_rgb_t), .is_transparent(c_trans_t)
    );
    chest_sprite_rom u_chest_b (
        .row(c_row_b), .col(c_col_b), .color_rgb(c_rgb_b), .is_transparent(c_trans_b)
    );

    reg  [5:0] k_row_t, k_col_t, k_row_b, k_col_b;
    wire [23:0] k_rgb_t, k_rgb_b;
    wire        k_trans_t, k_trans_b;

    key_sprite_rom u_key_t (
        .row(k_row_t), .col(k_col_t), .color_rgb(k_rgb_t), .is_transparent(k_trans_t)
    );
    key_sprite_rom u_key_b (
        .row(k_row_b), .col(k_col_b), .color_rgb(k_rgb_b), .is_transparent(k_trans_b)
    );

    // ------------------------------------------------------------------------
    // ------------------------------------------------------------------------
    // Half-block pixel printer helper (High-Resolution 24-bit TrueColor)
    // ------------------------------------------------------------------------
    task print_hb_pixel;
        input        tt;
        input [7:0]  rt, gt, bt;
        input        tb;
        input [7:0]  rb, gb, bb;
        begin
            if (!tt && !tb) begin
                $write("\033[38;2;%0d;%0d;%0dm\033[48;2;%0d;%0d;%0dm\342\226\200\033[0m", rt, gt, bt, rb, gb, bb);
            end else if (!tt && tb) begin
                $write("\033[0m\033[38;2;%0d;%0d;%0dm\342\226\200\033[0m", rt, gt, bt);
            end else if (tt && !tb) begin
                $write("\033[0m\033[38;2;%0d;%0d;%0dm\342\226\204\033[0m", rb, gb, bb);
            end else begin
                $write(" ");
            end
        end
    endtask

    // ------------------------------------------------------------------------
    // 1. Title Screen (Based on new title.txt rendered in 3D-ASCII)
    // ------------------------------------------------------------------------
    task render_title_screen;
        input title_cursor;
        begin
            $write("\033[2J\033[H");
            $display("\033[1;31m====================================================================================================\033[0m");
            $display("\033[1;31m          ________  ___  ___      ________       ________      _______       ________               \033[0m");
            $display("\033[1;31m         |\\  _____\\|\\  \\|\\  \\    |\\   ___  \\    |\\   ____\\    |\\  ___ \\     |\\   __  \\              \033[0m");
            $display("\033[1;31m         \\ \\  \\__/ \\ \\  \\\\\\  \\   \\ \\  \\\\ \\  \\   \\ \\  \\___|    \\ \\   __/|    \\ \\  \\|\\  \\             \033[0m");
            $display("\033[1;31m          \\ \\   __\\ \\ \\  \\\\\\  \\   \\ \\  \\\\ \\  \\   \\ \\  \\  ___   \\ \\  \\_|/__   \\ \\   _  _\\            \033[0m");
            $display("\033[1;31m           \\ \\  \\_|  \\ \\  \\\\\\  \\   \\ \\  \\\\ \\  \\   \\ \\  \\|\\  \\   \\ \\  \\_|\\ \\   \\ \\  \\\\  \\|           \033[0m");
            $display("\033[1;31m            \\ \\__\\    \\ \\_______\\   \\ \\__\\\\ \\__\\   \\ \\_______\\   \\ \\_______\\   \\ \\__\\\\ _\\           \033[0m");
            $display("\033[1;31m             \\|__|     \\|_______|    \\|__| \\|__|    \\|_______|    \\|_______|    \\|__|\\|__|          \033[0m");
            $display("\033[1;33m                        [   T  E  R  M  I  N  A  L     E  D  I  T  I  O  N   ]                      \033[0m");
            $display("\033[1;31m====================================================================================================\033[0m");
            $display("\033[1;33m   [OBJECTIVE]: Collect 3 Dungeon Keys to open the Cyan Exit Gate 'G' on right wall!                \033[0m");
            $display("\033[1;36m   [CHESTS]: Open brown chests 'C' for loot (Poppy/Marijuana/Key) or face Mimic Horror!           \033[0m");
            $display("\033[1;31m====================================================================================================\033[0m");
            $display("   \033[1;32m[1] START EXPEDITION\033[0m    |    \033[1;31m[0] ABANDON HOPE (QUIT)\033[0m");
            $display("\033[1;31m====================================================================================================\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // 1.5 Difficulty Select Screen (Fear & Hunger vs Terror & Starvation)
    // ------------------------------------------------------------------------
    task render_difficulty_select_screen;
        input diff_cursor;
        begin
            $write("\033[2J\033[H");
            $display("\033[1;35m====================================================================================================\033[0m");
            $display("\033[1;35m                   SELECT EXPEDITION DIFFICULTY - CHOOSE YOUR PATH INTO DARKNESS                    \033[0m");
            $display("\033[1;35m====================================================================================================\033[0m\n");

            $display("  \033[1;32m[1] FEAR & HUNGER (Normal Mode - Standard Expeditions)\033[0m");
            $display("      - Explorer Combat Stats  : \033[1;32m1.5x ATK & DEF Boost\033[0m (Empowered to clash with horrors)");
            $display("      - Poppy Flower Healing   : \033[1;32m+50 HP\033[0m per application");
            $display("      - Marijuana Herb Healing : \033[1;32m+120 HP\033[0m potent medicinal cure");
            $display("      - Recommended for tacticians seeking fair odds against the subterranean horrors.\n");

            $display("  \033[1;31m[2] TERROR & STARVATION (Hard Mode - Classic Fear & Hunger Experience)\033[0m");
            $display("      - Explorer Combat Stats  : \033[1;31m1.0x Baseline Stats\033[0m (Raw, grim, lethal confrontations)");
            $display("      - Poppy Flower Healing   : \033[1;31m+30 HP\033[0m scarce emergency recovery");
            $display("      - Marijuana Herb Healing : \033[1;31m+70 HP\033[0m rationed herbal relief");
            $display("      - For hardcore survivors prepared to face despair, starvation, and sudden death.\n");

            $display("\033[1;35m====================================================================================================\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // 2. Character Select Screen (Pick 4 of 8 - Name and Stats Only)
    // ------------------------------------------------------------------------
    task render_character_select_screen;
        input       is_hard_mode;
        input [1:0] squad_cursor;
        integer i;
        reg [7:0]   hp, atk, def;
        reg [255:0] name, cl;
        begin
            $write("\033[2J\033[H");
            $display("\033[1;36m==================================================================================\033[0m");
            $display("\033[1;36m       CHOOSE YOUR SQUAD: SELECT 4 FROM 8 AVAILABLE EXPLORERS (STATS & NAMES)     \033[0m");
            if (is_hard_mode)
                $display("\033[1;31m       MODE: [TERROR & STARVATION] (Classic 1.0x Stats - Ruthless Hardcore)        \033[0m");
            else
                $display("\033[1;32m       MODE: [FEAR & HUNGER] (Empowered 1.5x ATK/DEF Boost - Standard Survival)   \033[0m");
            $display("\033[1;36m==================================================================================\033[0m");
            $display(" ID | EXPLORER NAME  | ROLE / COMBAT ARCHETYPE     |  HP   | ATTACK (ATK) | DEFENSE (DEF)");
            $display("----+----------------+-----------------------------+-------+--------------+--------------");

            for (i = 1; i <= 8; i = i + 1) begin
                u_char_db.get_character(i[3:0], is_hard_mode, hp, atk, def, name, cl);
                $display(" [%0d] | %-14s | %-27s | %3d HP |    %2d ATK    |    %2d DEF ",
                         i, name, cl, hp, atk, def);
            end

            $display("----+----------------+-----------------------------+-------+--------------+--------------");
            $display("\033[1;33m [SQUAD RECRUITMENT PRESETS - PRESS 1, 2, 3 OR 4]:\033[0m");
            $display("  \033[1;33m[1] Balanced Vanguard  : Cahara, D'arce, Enki, Ragnvaldr\033[0m");
            $display("  \033[1;35m[2] Occult Sorcery     : Enki, Nas'hrah, The Girl, Cahara\033[0m");
            $display("  \033[1;31m[3] Iron Mercenaries   : Ragnvaldr, Le'garde, D'arce, Cahara\033[0m");
            $display("  \033[1;36m[4] Custom Expedition  : Pick any 4 Explorers by ID (1-8)\033[0m");
            $display("----------------------------------------------------------------------------------\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // 2.5 Narrator Prologue Screen
    // ------------------------------------------------------------------------
    task render_narrator_screen;
        begin
            $write("\033[2J\033[H");
            $display("\033[1;35m====================================================================================================\033[0m");
            $display("\033[1;35m                                    PROLOGUE: DUNGEONS OF TERROR                                    \033[0m");
            $display("\033[1;35m====================================================================================================\033[0m\n");
            $display("  The oppressive dark air hangs heavy with the stench of decay and ancient dread.");
            $display("  Deep within the subterranean labyrinth, forbidden entities roam the winding halls.");
            $display("  You and your companions have descended into the abyss in search of escape.\n");
            $display("  Only 3 Dungeon Keys can unlock the ancient Exit Gate on the eastern perimeter.");
            $display("  Arm yourself, manage your herbs, and beware the horrors lurking in every shadow.\n");
            $display("\033[1;35m====================================================================================================\033[0m");
            $write("  \033[1;33m>> Press [1] or Enter to assemble your expedition squad: \033[0m");
        end
    endtask

    // ------------------------------------------------------------------------
    // 2.6 Companion Draft Screen (Fixed 32-char Name & 18-char Type Alignment)
    // ------------------------------------------------------------------------
    task render_draft_screen;
        input [4:0] c1_id; input [7:0] c1_hp, c1_atk, c1_def;
        input [4:0] c2_id; input [7:0] c2_hp, c2_atk, c2_def;
        input [4:0] c3_id; input [7:0] c3_hp, c3_atk, c3_def;
        input [4:0] c4_id; input [7:0] c4_hp, c4_atk, c4_def;
        input [4:0] c5_id; input [7:0] c5_hp, c5_atk, c5_def;
        begin
            $write("\033[2J\033[H");
            $display("\033[1;36m====================================================================================================\033[0m");
            $display("\033[1;36m                        COMPANION DRAFT: CHOOSE 3 DISTINCT SQUAD COMPANIONS                         \033[0m");
            $display("\033[1;36m====================================================================================================\033[0m");
            $display(" SLOT | COMPANION NAME                 | ELEMENT / TYPE     |   MAX HP   |  ATTACK  |  DEFENSE  ");
            $display("------+--------------------------------+--------------------+------------+----------+-----------");

            $write("  [1] | "); u_mon_db.print_monster_name({1'b0, c1_id});
            $write(" | "); u_mon_db.print_monster_type({1'b0, c1_id});
            $display(" |   %3d HP   |  %2d ATK  |  %2d DEF   ", c1_hp, c1_atk, c1_def);

            $write("  [2] | "); u_mon_db.print_monster_name({1'b0, c2_id});
            $write(" | "); u_mon_db.print_monster_type({1'b0, c2_id});
            $display(" |   %3d HP   |  %2d ATK  |  %2d DEF   ", c2_hp, c2_atk, c2_def);

            $write("  [3] | "); u_mon_db.print_monster_name({1'b0, c3_id});
            $write(" | "); u_mon_db.print_monster_type({1'b0, c3_id});
            $display(" |   %3d HP   |  %2d ATK  |  %2d DEF   ", c3_hp, c3_atk, c3_def);

            $write("  [4] | "); u_mon_db.print_monster_name({1'b0, c4_id});
            $write(" | "); u_mon_db.print_monster_type({1'b0, c4_id});
            $display(" |   %3d HP   |  %2d ATK  |  %2d DEF   ", c4_hp, c4_atk, c4_def);

            $write("  [5] | "); u_mon_db.print_monster_name({1'b0, c5_id});
            $write(" | "); u_mon_db.print_monster_type({1'b0, c5_id});
            $display(" |   %3d HP   |  %2d ATK  |  %2d DEF   ", c5_hp, c5_atk, c5_def);

            $display("------+--------------------------------+--------------------+------------+----------+-----------");
            $display("\033[1;33m [INSTRUCTION]: Select 3 different companion IDs (1-5) to join your expedition vanguard.\033[0m");
            $display("\033[1;36m====================================================================================================\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // 2.7 Tactical Pal Map Screen (3-Pal Engine with Fog of War & Compass)
    // ------------------------------------------------------------------------
    task render_pal_map_screen;
        input signed [31:0] px, py;
        input [31:0]        step_count;
        input [7:0]         herb_qty, crys_qty;
        input [4:0]         p0_id; input [7:0] p0_hp, p0_max;
        input [4:0]         p1_id; input [7:0] p1_hp, p1_max;
        input [4:0]         p2_id; input [7:0] p2_hp, p2_max;
        integer x, y, tile_dist;
        reg [2:0] raw_t;
        integer dx_gate, dy_gate;
        begin
            $write("\033[2J\033[H"); // Clean screen reset: No ghost text from previous combat screens
            $display("\033[1;32m==================================================================================\033[0m\033[K");
            $display("\033[1;32m  LABYRINTH [TERROR & STARVATION] | POS:[%2d,%2d] | STEPS:%-3d\033[0m\033[K",
                     px, py, step_count);
            $display("\033[1;32m==================================================================================\033[0m\033[K");

            for (y = 0; y < `MAP_HEIGHT; y = y + 1) begin
                $write("  ");
                for (x = 0; x < `MAP_WIDTH; x = x + 1) begin
                    tile_dist = (x > px ? x - px : px - x) + (y > py ? y - py : py - y);
                    if (x == px && y == py) begin
                        $write("\033[1;33;40m O\033[0m");
                    end else if (tile_dist > 7) begin
                        // Fog of War: Distant cells dimmed to dark dot
                        $write("\033[90m .\033[0m");
                    end else begin
                        raw_t = u_map.get_tile(x, y);
                        case (raw_t)
                            `TILE_WALL:    $write("\033[42m  \033[0m");
                            `TILE_PATH:    $write("\033[90m .\033[0m");
                            `TILE_MONSTER: $write("\033[45;1;37m M\033[0m");
                            `TILE_CHEST:   $write("\033[48;2;139;69;19;1;37m C\033[0m");
                            `TILE_GATE:    $write("\033[46;1;30m G\033[0m");
                            default:       $write("\033[90m .\033[0m");
                        endcase
                    end
                end
                $write("\033[K\n");
            end

            $display("\033[1;37m----------------------------------------------------------------------------------\033[0m\033[K");
            $display(" LEGEND: \033[42m  \033[0m Wall | \033[90m .\033[0m Path/Fog | \033[1;33m O\033[0m Player | \033[45;1;37m M\033[0m Foe | \033[48;2;139;69;19;1;37m C\033[0m Chest | \033[46;1;30m G\033[0m Gate\033[K");
            $display("\033[1;37m----------------------------------------------------------------------------------\033[0m\033[K");
            $display(" SQUAD: Pal #1: %3d/%3d HP | Pal #2: %3d/%3d HP | Pal #3: %3d/%3d HP\033[K",
                     p0_hp, p0_max, p1_hp, p1_max, p2_hp, p2_max);
            $display(" POUCH: \033[38;2;242;34;84m[+] Normal Herb x%-2d\033[0m | \033[38;2;105;225;101m[*] Strong Crystal x%-2d\033[0m\033[K",
                     herb_qty, crys_qty);
            $display(" CONTROLS: [W/A/S/D]: Move | [I]: Pouch | [H]: Quick Heal | [Q]: Quit\033[K");
            $display("\033[1;32m==================================================================================\033[0m\033[K\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // 2.8 Combat Tactical Sub-Menus (Heal, Target, Switch)
    // ------------------------------------------------------------------------
    task render_pal_bag_screen;
        input [3:0]   active_item;
        input [7:0]   normal_herb_qty, strong_crys_qty;
        input [4:0]   p0_id; input [7:0] p0_hp, p0_max;
        input [4:0]   p1_id; input [7:0] p1_hp, p1_max;
        input [4:0]   p2_id; input [7:0] p2_hp, p2_max;
        begin
            $write("\033[2J\033[H");
            $display("\033[1;35m====================================================================================================\033[0m");
            $display("                    SURVIVAL MEDICINE POUCH [TERROR & STARVATION]                                   ");
            $display("\033[1;35m====================================================================================================\033[0m\n");
            $display("   [1] Normal Herb x%-2d    : Restores +20 HP to targeted companion (usable on Map & Combat)", normal_herb_qty);
            $display("   [2] Strong Crystal x%-2d : Restores +50 HP to targeted companion (usable on Map & Combat)", strong_crys_qty);
            $display("   [0] Close Pouch (Return to Labyrinth Exploration)\n");
            $display("----------------------------------------------------------------------------------------------------");
            $display("   SQUAD STATUS:");
            $write("   [1] "); u_mon_db.print_monster_name({1'b0, p0_id}); $display(" | HP: %3d/%3d", p0_hp, p0_max);
            $write("   [2] "); u_mon_db.print_monster_name({1'b0, p1_id}); $display(" | HP: %3d/%3d", p1_hp, p1_max);
            $write("   [3] "); u_mon_db.print_monster_name({1'b0, p2_id}); $display(" | HP: %3d/%3d", p2_hp, p2_max);
            $display("\033[1;35m====================================================================================================\033[0m\n");
        end
    endtask

    task render_combat_heal_menu;
        input [7:0] normal_qty, strong_qty;
        input [4:0] pal_id;
        input [7:0] pal_hp, pal_max;
        begin
            $display("\n\033[1;33m==================================================================================\033[0m");
            $display("  \033[1;37mFIELD MEDICINE:\033[0m [1] Normal Herb x%-2d (+20 HP)  |  [2] Strong Crystal x%-2d (+50 HP)",
                     normal_qty, strong_qty);
            $display("  Active Companion HP: %3d/%3d", pal_hp, pal_max);
            $display("\033[1;33m==================================================================================\033[0m");
            $write("  >> Select medicine [1, 2, or 0 to Cancel]: ");
        end
    endtask

    task render_target_pal_menu;
        input [1:0] item_type;
        input [4:0] p0_id; input [7:0] p0_hp, p0_max;
        input [4:0] p1_id; input [7:0] p1_hp, p1_max;
        input [4:0] p2_id; input [7:0] p2_hp, p2_max;
        begin
            $display("\n\033[1;36m==================================================================================\033[0m");
            $display("  \033[1;37mSELECT TARGET COMPANION TO ADMINISTER:\033[0m");
            $write("   [1] "); u_mon_db.print_monster_name({1'b0, p0_id});
            $display(" | HP: %3d/%3d", p0_hp, p0_max);
            $write("   [2] "); u_mon_db.print_monster_name({1'b0, p1_id});
            $display(" | HP: %3d/%3d", p1_hp, p1_max);
            $write("   [3] "); u_mon_db.print_monster_name({1'b0, p2_id});
            $display(" | HP: %3d/%3d", p2_hp, p2_max);
            $display("\033[1;36m==================================================================================\033[0m");
            $write("  >> Choose companion [1, 2, 3 or 0 to cancel]: ");
        end
    endtask

    task render_combat_switch_menu;
        input [1:0] active_idx;
        input [4:0] p0_id; input [7:0] p0_hp, p0_max;
        input [4:0] p1_id; input [7:0] p1_hp, p1_max;
        input [4:0] p2_id; input [7:0] p2_hp, p2_max;
        begin
            $display("\n\033[1;35m==================================================================================\033[0m");
            $display("  \033[1;37mTACTICAL COMPANION ROSTER (ACTIVE: #%0d):\033[0m", active_idx + 1);
            $write("   [1] "); u_mon_db.print_monster_name({1'b0, p0_id});
            $display(" | HP: %3d/%3d %s", p0_hp, p0_max, (active_idx == 2'd0) ? "<ACTIVE>" : "");
            $write("   [2] "); u_mon_db.print_monster_name({1'b0, p1_id});
            $display(" | HP: %3d/%3d %s", p1_hp, p1_max, (active_idx == 2'd1) ? "<ACTIVE>" : "");
            $write("   [3] "); u_mon_db.print_monster_name({1'b0, p2_id});
            $display(" | HP: %3d/%3d %s", p2_hp, p2_max, (active_idx == 2'd2) ? "<ACTIVE>" : "");
            $display("\033[1;35m==================================================================================\033[0m");
            $write("  >> Select Companion to tag in [1, 2, 3]: ");
        end
    endtask

    // ------------------------------------------------------------------------
    // 2.9 Tactical Pal Battle Screen with Combat Log & Monster Type
    // ------------------------------------------------------------------------
    task render_battle_screen_pal;
        input [4:0] enemy_id;
        input [7:0] enemy_hp, enemy_max;
        input [4:0] active_pal_id;
        input [7:0] active_pal_hp, active_pal_max;
        input [7:0] battle_turn;
        input [7:0] last_dmg_dealt;
        input [7:0] last_dmg_taken;
        input [2:0] last_event_flag;
        begin
            $write("\033[H"); // Anti-flicker
            $display("\033[1;31m====================================================================================================\033[0m\033[K");
            $display("  \033[1;37mTACTICAL TURN-BASED CLASH [TURN %0d]\033[0m  |  \033[1;33mTERROR & STARVATION LABYRINTH\033[0m\033[K", battle_turn);
            $display("\033[1;31m====================================================================================================\033[0m\033[K");

            $write("  \033[1;31m[OPPONENT]:\033[0m \033[1;35m");
            u_mon_db.print_monster_name({1'b0, enemy_id});
            $write("\033[0m | TYPE: \033[1;36m[");
            u_mon_db.print_monster_type({1'b0, enemy_id});
            $display("]\033[0m\033[K");
            $display("  HP: \033[1;31m%3d/%3d\033[0m\033[K\n", enemy_hp, enemy_max);

            $write("  \033[1;32m[ACTIVE PAL]:\033[0m \033[1;33m");
            u_mon_db.print_monster_name({1'b0, active_pal_id});
            $display("\033[0m | HP: \033[1;32m%3d/%3d\033[0m\033[K", active_pal_hp, active_pal_max);
            $display("----------------------------------------------------------------------------------------------------\033[K");

            // Combat Log Display (Item 4)
            case (last_event_flag)
                3'd1: $display("  \033[1;33m>> [COMBAT LOG]: You struck foe for %0d DMG! Enemy countered for %0d DMG!\033[0m\033[K", last_dmg_dealt, last_dmg_taken);
                3'd2: $display("  \033[1;36m>> [COMBAT LOG]: You guarded! Reduced incoming damage to %0d DMG.\033[0m\033[K", last_dmg_taken);
                3'd3: $display("  \033[1;32m>> [COMBAT LOG]: Medicine applied! Foe attacked for %0d DMG during turn!\033[0m\033[K", last_dmg_taken);
                3'd4: $display("  \033[1;31m>> [COMBAT LOG]: Flee failed! Suffered %0d penalty DMG from enemy!\033[0m\033[K", last_dmg_taken);
                3'd5: $display("  \033[1;35m>> [COMBAT LOG]: Companion tagged into frontline combat!\033[0m\033[K");
                default: $display("  \033[90m>> [COMBAT LOG]: Wild creature engaged in tactical combat!\033[0m\033[K");
            endcase

            $display("----------------------------------------------------------------------------------------------------\033[K");
            $display("  ACTIONS: [1] ATTACK  |  [2] DEFEND  |  [3] MEDICINE POUCH  |  [4] SWITCH PAL  |  [5] FLEE\033[K");
            $display("\033[1;31m====================================================================================================\033[0m\033[K");
            $write("  >> Enter action (1-5): ");
        end
    endtask

    // ------------------------------------------------------------------------
    // 3. Redesigned Map Screen (Green Wall Blocks, Grid Dots, 'O', 'M', 'C', 'G')
    // ------------------------------------------------------------------------
    task render_map_screen;
        input               is_hard_mode;
        input signed [31:0] px, py;
        input [31:0]        step_count;
        input [7:0]         poppy_qty, marijuana_qty, key_qty;
        input [255:0]       c0_name, c1_name, c2_name, c3_name;
        input [7:0]         c0_hp, c0_max, c1_hp, c1_max, c2_hp, c2_max, c3_hp, c3_max;
        input [719:0]       cleared_mask;
        integer x, y;
        reg [2:0] raw_t;
        integer cell_idx;
        reg is_cleared;
        integer tile_dist;
        integer dx_gate, dy_gate;
        begin
            $write("\033[2J\033[H"); // Clean screen reset: No ghost text from previous combat screens
            $display("\033[1;32m==================================================================================\033[0m\033[K");
            if (is_hard_mode)
                $display("\033[1;31m  LABYRINTH [TERROR & STARVATION] | POS:[%2d,%2d] | STEPS:%-3d | KEYS:\033[1;33m%0d/3\033[1;31m\033[0m\033[K",
                         px, py, step_count, key_qty);
            else
                $display("\033[1;32m  LABYRINTH [FEAR & HUNGER]       | POS:[%2d,%2d] | STEPS:%-3d | KEYS:\033[1;33m%0d/3\033[1;32m\033[0m\033[K",
                         px, py, step_count, key_qty);
            $display("\033[1;32m==================================================================================\033[0m\033[K");

            for (y = 0; y < `MAP_HEIGHT; y = y + 1) begin
                $write("  ");
                for (x = 0; x < `MAP_WIDTH; x = x + 1) begin
                    cell_idx   = y * `MAP_WIDTH + x;
                    is_cleared = cleared_mask[cell_idx];
                    tile_dist = (x > px ? x - px : px - x) + (y > py ? y - py : py - y);

                    if (x == px && y == py) begin
                        // Player representation: Vibrant Yellow 'O'
                        $write("\033[1;33;40m O\033[0m");
                    end else if (tile_dist > 7) begin
                        // Fog of War: Distant cells dimmed to dark gray dot
                        $write("\033[90m .\033[0m");
                    end else begin
                        raw_t = u_map.get_tile(x, y);

                        // If tile was defeated or opened, render as regular path
                        if (is_cleared && (raw_t == `TILE_MONSTER || raw_t == `TILE_CHEST)) begin
                            raw_t = `TILE_PATH;
                        end

                        case (raw_t)
                            `TILE_WALL: begin
                                // Wall: Green colored blocks with NO text
                                $write("\033[42m  \033[0m");
                            end
                            `TILE_PATH: begin
                                // Pathway: No background color, subtle grid dot ' .'
                                $write("\033[90m .\033[0m");
                            end
                            `TILE_MONSTER: begin
                                // Monster: Purple block with 'M'
                                $write("\033[45;1;37m M\033[0m");
                            end
                            `TILE_CHEST: begin
                                // Chest: Brown block with 'C'
                                $write("\033[48;2;139;69;19;1;37m C\033[0m");
                            end
                            `TILE_GATE: begin
                                // Gate: Cyan block with 'G' EMBEDDED ON RIGHT WALL
                                $write("\033[46;1;30m G\033[0m");
                            end
                            default: begin
                                $write("\033[90m .\033[0m");
                            end
                        endcase
                    end
                end
                $write("\033[K\n");
            end

            $display("\033[1;37m----------------------------------------------------------------------------------\033[0m\033[K");
            $display(" LEGEND: \033[42m  \033[0m Green Wall | \033[90m .\033[0m Path Grid | \033[1;33m O\033[0m Player | \033[45;1;37m M\033[0m Foe | \033[48;2;139;69;19;1;37m C\033[0m Chest | \033[46;1;30m G\033[0m Exit Gate\033[K");
            $display("\033[1;37m----------------------------------------------------------------------------------\033[0m\033[K");
            $display(" SQUAD: 1.%-7s %3d/%3d | 2.%-7s %3d/%3d | 3.%-7s %3d/%3d | 4.%-7s %3d/%3d\033[K",
                     c0_name, c0_hp, c0_max,
                     c1_name, c1_hp, c1_max,
                     c2_name, c2_hp, c2_max,
                     c3_name, c3_hp, c3_max);
            $display(" POUCH: \033[38;2;242;34;84m[+] Poppy: %-2d (+%0d HP)\033[0m | \033[38;2;105;225;101m[*] Marijuana: %-2d (+%0d HP)\033[0m | \033[1;33m[K] Keys: %0d/3\033[0m\033[K",
                     poppy_qty, is_hard_mode ? 30 : 50, marijuana_qty, is_hard_mode ? 70 : 120, key_qty);
            $display(" CONTROLS: [W/A/S/D]: Move  |  [I]: Inventory & Heal  |  [P]: Party Roster  |  [Q]: Quit\033[K");
            $display("\033[1;32m==================================================================================\033[0m\033[K");
        end
    endtask

    // ------------------------------------------------------------------------
    // 4. Inventory Screen with Compact Key Model & Mini Pixel Icons
    // ------------------------------------------------------------------------
    task render_party_health_status;
        input [255:0] c0_name, c1_name, c2_name, c3_name;
        input [7:0]   c0_hp, c0_max, c1_hp, c1_max, c2_hp, c2_max, c3_hp, c3_max;
        begin
            $display("\033[1;36m+----------------------------------------------------------------------------------------------+\033[0m");
            $display("\033[1;36m|                              EXPEDITION SQUAD VITALITY STATUS                                |\033[0m");
            $display("\033[1;36m+----------------------------------------------------------------------------------------------+\033[0m");
            $write("  [1] %-14s : ", c0_name);
            print_pink_health_bar(c0_hp, c0_max, 16);
            $display("   %3d / %3d HP", c0_hp, c0_max);

            $write("  [2] %-14s : ", c1_name);
            print_pink_health_bar(c1_hp, c1_max, 16);
            $display("   %3d / %3d HP", c1_hp, c1_max);

            $write("  [3] %-14s : ", c2_name);
            print_pink_health_bar(c2_hp, c2_max, 16);
            $display("   %3d / %3d HP", c2_hp, c2_max);

            $write("  [4] %-14s : ", c3_name);
            print_pink_health_bar(c3_hp, c3_max, 16);
            $display("   %3d / %3d HP", c3_hp, c3_max);
            $display("\033[1;36m+----------------------------------------------------------------------------------------------+\033[0m\n");
        end
    endtask

    task render_bag_screen;
        input         is_hard_mode;
        input [7:0]   poppy_qty, marijuana_qty, key_qty;
        input [255:0] c0_name, c1_name, c2_name, c3_name;
        input [7:0]   c0_hp, c0_max, c1_hp, c1_max, c2_hp, c2_max, c3_hp, c3_max;
        begin
            $write("\033[2J\033[H");
            $display("\033[1;35m================================================================================================\033[0m");
            if (is_hard_mode)
                $display("\033[1;35m             EXPLORER SURVIVAL POUCH & INVENTORY  \033[1;31m[TERROR & STARVATION]\033[1;35m                         \033[0m");
            else
                $display("\033[1;35m             EXPLORER SURVIVAL POUCH & INVENTORY  \033[1;32m[FEAR & HUNGER]\033[1;35m                               \033[0m");
            $display("\033[1;35m================================================================================================\033[0m\n");

            $display("\033[1;37m MEDICAL & MISSION SUPPLIES IN POUCH:\033[0m");
            $display("+----------------------------------------------------------------------------------------------+");
            $display("|  MINI ICON    :  ITEM NAME & QUANTITY       |  EFFECT & OPERATIONAL USAGE                    |");
            $display("+----------------------------------------------------------------------------------------------+");

            // 1. Poppy Flower
            $display("|  \033[38;2;242;34;84m[+] P-Flower\033[0m   :  [1] \033[1;31mPoppy Flower x%-2d\033[0m     |  Restores \033[1;32m+%2d HP\033[0m to targeted companion         |",
                     poppy_qty, is_hard_mode ? 30 : 50);
            $display("|  \033[38;2;87;168;123m    (Flower)\033[0m  :                            |  Usable on Map & during Battles (Costs 1 Turn) |");
            $display("+----------------------------------------------------------------------------------------------+");

            // 2. Marijuana Herb
            $display("|  \033[38;2;105;225;101m[*] M-Herb  \033[0m   :  [2] \033[1;32mMarijuana Herb x%-2d\033[0m   |  Restores \033[1;32m+%3d HP\033[0m massive healing power        |",
                     marijuana_qty, is_hard_mode ? 70 : 120);
            $display("|  \033[38;2;42;162;114m    (Herb)  \033[0m  :                            |  Usable on Map & during Battles (Costs 1 Turn) |");
            $display("+----------------------------------------------------------------------------------------------+");

            // 3. Compact Key Model
            $display("|  \033[38;2;255;190;0m[K] Key     \033[0m   :  [3] \033[1;33mDungeon Key x%-2d/3\033[0m    |  Required to unlock Exit Gate 'G'              |", key_qty);
            $display("|  \033[38;2;220;140;0m    (Gold)  \033[0m  :                            |  Strictly reserved for Gate unlocking          |");
            $display("+----------------------------------------------------------------------------------------------+\n");

            render_party_health_status(c0_name, c1_name, c2_name, c3_name, c0_hp, c0_max, c1_hp, c1_max, c2_hp, c2_max, c3_hp, c3_max);
            $display("   [0] CLOSE INVENTORY (RETURN TO EXPEDITION)");
            $display("\033[1;35m================================================================================================\033[0m\n");
        end
    endtask

    // Helper task to get 18-char role description for compact UI cards
    task get_short_role;
        input  [3:0]   cid;
        output [143:0] s_role;
        begin
            case (cid)
                4'd1: s_role = "Mercenary (Rogue) ";
                4'd2: s_role = "Holy Knight (Tank)";
                4'd3: s_role = "Dark Priest (Mage)";
                4'd4: s_role = "Berserker (Tank)  ";
                4'd5: s_role = "Commander (Tact)  ";
                4'd6: s_role = "Cave Beast (Crit) ";
                4'd7: s_role = "Innocent Ward     ";
                4'd8: s_role = "Doom Wizard (Mage)";
                default: s_role = "Adventurer        ";
            endcase
        end
    endtask

    // ------------------------------------------------------------------------
    // 4B. Squad Lineup & Pixel Art Models Showcase Screen
    // ------------------------------------------------------------------------
    task render_squad_screen;
        input [3:0]   c0_id, c1_id, c2_id, c3_id;
        input [255:0] c0_name, c1_name, c2_name, c3_name;
        input [255:0] c0_class, c1_class, c2_class, c3_class;
        input [7:0]   c0_hp, c0_max, c1_hp, c1_max, c2_hp, c2_max, c3_hp, c3_max;
        input [7:0]   c0_atk, c0_def, c1_atk, c1_def, c2_atk, c2_def, c3_atk, c3_def;
        input [1:0]   active_idx;
        integer pair, lp, c;
        integer pw_l, ph_l, pw_r, ph_r;
        reg [3:0]   cur_id_l, cur_id_r;
        reg [255:0] cur_name_l, cur_name_r;
        reg [143:0] cur_srole_l, cur_srole_r;
        reg [7:0]   cur_hp_l, cur_max_l, cur_atk_l, cur_def_l;
        reg [7:0]   cur_hp_r, cur_max_r, cur_atk_r, cur_def_r;
        reg         is_act_l, is_act_r;
        reg         pt_l_trans, pb_l_trans, pt_r_trans, pb_r_trans;
        reg [23:0]  pt_l_rgb, pb_l_rgb, pt_r_rgb, pb_r_rgb;
        begin
            $write("\033[2J\033[H");
            $display("\033[1;36m====================================================================================================\033[0m");
            $display("\033[1;36m                     EXPEDITION SQUAD LINEUP: 4 CHOSEN EXPLORERS & MODELS                           \033[0m");
            $display("\033[1;36m====================================================================================================\033[0m\n");

            for (pair = 0; pair < 2; pair = pair + 1) begin
                if (pair == 0) begin
                    cur_id_l = c0_id; cur_name_l = c0_name;
                    cur_hp_l = c0_hp; cur_max_l = c0_max; cur_atk_l = c0_atk; cur_def_l = c0_def;
                    is_act_l = (active_idx == 2'd0);
                    get_short_role(c0_id, cur_srole_l);

                    cur_id_r = c1_id; cur_name_r = c1_name;
                    cur_hp_r = c1_hp; cur_max_r = c1_max; cur_atk_r = c1_atk; cur_def_r = c1_def;
                    is_act_r = (active_idx == 2'd1);
                    get_short_role(c1_id, cur_srole_r);
                end else begin
                    cur_id_l = c2_id; cur_name_l = c2_name;
                    cur_hp_l = c2_hp; cur_max_l = c2_max; cur_atk_l = c2_atk; cur_def_l = c2_def;
                    is_act_l = (active_idx == 2'd2);
                    get_short_role(c2_id, cur_srole_l);

                    cur_id_r = c3_id; cur_name_r = c3_name;
                    cur_hp_r = c3_hp; cur_max_r = c3_max; cur_atk_r = c3_atk; cur_def_r = c3_def;
                    is_act_r = (active_idx == 2'd3);
                    get_short_role(c3_id, cur_srole_r);
                end

                // Header line for the pair of character cards (46 chars + 4 gap + 46 chars)
                if (pair == 0) $write(" \033[1;33m[1] %-14s\033[0m", cur_name_l);
                else           $write(" \033[1;33m[3] %-14s\033[0m", cur_name_l);

                if (cur_hp_l == 0) $write(" \033[41;1;37m[UNCONSCIOUS]\033[0m             ");
                else if (is_act_l) $write(" \033[42;1;37m[* ACTIVE FRONTLINE]\033[0m      ");
                else               $write(" \033[44;1;37m[STANDBY COMPANION]\033[0m       ");

                $write("    ");

                if (pair == 0) $write(" \033[1;33m[2] %-14s\033[0m", cur_name_r);
                else           $write(" \033[1;33m[4] %-14s\033[0m", cur_name_r);

                if (cur_hp_r == 0) $display(" \033[41;1;37m[UNCONSCIOUS]\033[0m             ");
                else if (is_act_r) $display(" \033[42;1;37m[* ACTIVE FRONTLINE]\033[0m      ");
                else               $display(" \033[44;1;37m[STANDBY COMPANION]\033[0m       ");

                $display(" ----------------------------------------------    ----------------------------------------------");

                u_router.get_funger_dim(cur_id_l, pw_l, ph_l);
                u_router.get_funger_dim(cur_id_r, pw_r, ph_r);

                // 11 half-block lines = 22 pixel rows
                for (lp = 0; lp < 11; lp = lp + 1) begin
                    // Left character sprite (26 columns)
                    for (c = 0; c < 26; c = c + 1) begin
                        if (c < pw_l && lp * 2 < ph_l) begin
                            u_router.sample_funger_pixel(cur_id_l, lp*2, lp*2+1, c, 1'b0, pt_l_trans, pt_l_rgb, pb_l_trans, pb_l_rgb);
                            print_hb_pixel(pt_l_trans, pt_l_rgb[23:16], pt_l_rgb[15:8], pt_l_rgb[7:0],
                                           pb_l_trans, pb_l_rgb[23:16], pb_l_rgb[15:8], pb_l_rgb[7:0]);
                        end else begin
                            $write(" ");
                        end
                    end
                    $write("  ");

                    // Left character stats slice (18 columns)
                    if (lp == 1) begin
                        $write("\033[1;37mHP:  %3d / %3d\033[0m   ", cur_hp_l, cur_max_l);
                    end else if (lp == 2) begin
                        print_pink_health_bar(cur_hp_l, cur_max_l, 14);
                        $write("  ");
                    end else if (lp == 4) begin
                        $write("\033[1;33mATK:%2d\033[0m  \033[1;36mDEF:%2d\033[0m  ", cur_atk_l, cur_def_l);
                    end else if (lp == 6) begin
                        $write("\033[1;37m%-18s\033[0m", cur_srole_l);
                    end else if (lp == 8) begin
                        if (cur_hp_l == 0) $write("\033[1;31m[Unconscious]     \033[0m");
                        else if (is_act_l) $write("\033[1;32m[Frontline Battler]\033[0m");
                        else               $write("\033[90m[Reserve Standby] \033[0m");
                    end else begin
                        $write("                  ");
                    end

                    // Separation gap between left and right cards (4 columns)
                    $write("    ");

                    // Right character sprite (26 columns)
                    for (c = 0; c < 26; c = c + 1) begin
                        if (c < pw_r && lp * 2 < ph_r) begin
                            u_router.sample_funger_pixel(cur_id_r, lp*2, lp*2+1, c, 1'b0, pt_r_trans, pt_r_rgb, pb_r_trans, pb_r_rgb);
                            print_hb_pixel(pt_r_trans, pt_r_rgb[23:16], pt_r_rgb[15:8], pt_r_rgb[7:0],
                                           pb_r_trans, pb_r_rgb[23:16], pb_r_rgb[15:8], pb_r_rgb[7:0]);
                        end else begin
                            $write(" ");
                        end
                    end
                    $write("  ");

                    // Right character stats slice (18 columns)
                    if (lp == 1) begin
                        $write("\033[1;37mHP:  %3d / %3d\033[0m   ", cur_hp_r, cur_max_r);
                    end else if (lp == 2) begin
                        print_pink_health_bar(cur_hp_r, cur_max_r, 14);
                        $write("  ");
                    end else if (lp == 4) begin
                        $write("\033[1;33mATK:%2d\033[0m  \033[1;36mDEF:%2d\033[0m  ", cur_atk_r, cur_def_r);
                    end else if (lp == 6) begin
                        $write("\033[1;37m%-18s\033[0m", cur_srole_r);
                    end else if (lp == 8) begin
                        if (cur_hp_r == 0) $write("\033[1;31m[Unconscious]     \033[0m");
                        else if (is_act_r) $write("\033[1;32m[Frontline Battler]\033[0m");
                        else               $write("\033[90m[Reserve Standby] \033[0m");
                    end else begin
                        $write("                  ");
                    end

                    $write("\n");
                end

                $display(" ----------------------------------------------    ----------------------------------------------\n");
            end

            $display("\033[1;36m====================================================================================================\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // 5. Full-Screen Chest Opening Scene (Like Battle Screen)
    // ------------------------------------------------------------------------
    task render_chest_open_screen;
        input         is_mimic;
        input [255:0] loot_name;
        input [7:0]   loot_qty;
        integer lp, c;
        begin
            $write("\033[2J\033[H");
            $display("\033[1;33m==================================================================================\033[0m");
            $display("\033[1;33m               ANCIENT LABYRINTH TREASURE VAULT OPENED !                          \033[0m");
            $display("\033[1;33m==================================================================================\033[0m\n");

            // Render Chest Sprite Model (20x23 pixels -> 12 terminal lines)
            for (lp = 0; lp < 12; lp = lp + 1) begin
                c_row_t = lp * 2;
                c_row_b = lp * 2 + 1;
                $write("     ");

                for (c = 0; c < 20; c = c + 1) begin
                    c_col_t = c;
                    c_col_b = c;
                    #1;
                    print_hb_pixel(
                        c_trans_t, c_rgb_t[23:16], c_rgb_t[15:8], c_rgb_t[7:0],
                        c_trans_b, c_rgb_b[23:16], c_rgb_b[15:8], c_rgb_b[7:0]
                    );
                end

                // Accompanying description box alongside the chest sprite
                if (lp == 2) begin
                    if (is_mimic)
                        $write("    \033[41;1;37m+--------------------------------------------------------+\033[0m");
                    else
                        $write("    \033[44;1;37m+--------------------------------------------------------+\033[0m");
                end else if (lp == 3) begin
                    if (is_mimic)
                        $write("    \033[41;1;37m|  [!] CRITICAL DANGER: IT'S A MIMIC HORROR!             |\033[0m");
                    else
                        $write("    \033[44;1;37m|  [*] VAULT STATUS: CHEST UNLOCKED SECURELY!            |\033[0m");
                end else if (lp == 4) begin
                    if (is_mimic)
                        $write("    \033[41;1;37m|  The chest sprouts fangs and lunges forward!           |\033[0m");
                    else
                        $write("    \033[44;1;37m|  Inside the velvet lining, you discover rare bounty!   |\033[0m");
                end else if (lp == 5) begin
                    if (is_mimic)
                        $write("    \033[41;1;37m|  Mimic is a standard creature (NEVER Elite).           |\033[0m");
                    else
                        $write("    \033[44;1;37m|  >> ACQUIRED: %0dx %-38s|\033[0m", loot_qty, loot_name);
                end else if (lp == 6) begin
                    if (is_mimic)
                        $write("    \033[41;1;37m|  ENGAGING COMBAT! Draw your steel!                    |\033[0m");
                    else
                        $write("    \033[44;1;37m|  Supplies stored in Pouch. Tile is now cleared!        |\033[0m");
                end else if (lp == 7) begin
                    if (is_mimic)
                        $write("    \033[41;1;37m+--------------------------------------------------------+\033[0m");
                    else
                        $write("    \033[44;1;37m+--------------------------------------------------------+\033[0m");
                end

                $write("\n");
            end

            $display("\n\033[1;33m==================================================================================\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // 6. Boxed Notifications with High-Contrast Backgrounds
    // ------------------------------------------------------------------------
    // A. Item Acquired Notification (Standardized 102-Column Box)
    // ------------------------------------------------------------------------
    task notify_receive_item;
        input [255:0] source_str;
        input [255:0] item_name;
        input [7:0]   amount;
        begin
            $display("\033[1;36m+====================================================================================================+\033[0m");
            $display("\033[1;36m| \033[44;1;37m [BOUNTY ACQUIRED] \033[0m \033[1;37mSOURCE: %-73s \033[1;36m|\033[0m", source_str);
            $display("\033[1;36m| \033[1;33m>> You received: %0dx %-77s \033[1;36m|\033[0m", amount, item_name);
            $display("\033[1;36m+====================================================================================================+\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // B. Item Consumed Notification (Standardized 102-Column Box)
    // ------------------------------------------------------------------------
    task notify_consume_item;
        input [255:0] item_name;
        input [255:0] char_name;
        input [7:0]   heal_hp;
        input [7:0]   curr_hp;
        input [7:0]   max_hp;
        begin
            $display("\033[1;32m+====================================================================================================+\033[0m");
            $display("\033[1;32m| \033[48;2;0;90;110;1;37m [SUPPLY ADMINISTERED] \033[0m \033[1;37mApplied %-14s to %-47s \033[1;32m|\033[0m", item_name, char_name);
            $display("\033[1;32m| \033[1;33m>> %-14s recovers +%0d HP! (Current Vitality: %3d / %3d)                                   \033[1;32m|\033[0m",
                     char_name, heal_hp, curr_hp, max_hp);
            $display("\033[1;32m+====================================================================================================+\033[0m\n");
        end
    endtask

    // C. Gate Access Notice (Blocked vs Unlocked)
    task notify_gate_status;
        input [7:0] key_count;
        begin
            if (key_count < 8'd3) begin
                $display("\033[1;33m+================================================================================+\033[0m");
                $display("\033[1;33m| \033[1;31m[GATE SEALED]\033[0m \033[1;37mThe iron exit portal is locked with 3 massive runic deadbolts!   \033[1;33m|\033[0m");
                $display("\033[1;33m| \033[1;36m>> Required: 3 Dungeon Keys\033[0m  |  \033[1;33mCurrently Holding: %0d/3 Dungeon Keys             \033[1;33m|\033[0m", key_count);
                $display("\033[1;33m| \033[90mDefeat elite monsters or uncover ancient chests to locate the remaining keys!  \033[1;33m|\033[0m");
                $display("\033[1;33m+================================================================================+\033[0m\n");
            end else begin
                $display("\033[1;32m+================================================================================+\033[0m");
                $display("\033[1;32m| \033[1;33m[GATE UNLOCKED]\033[0m \033[1;37mALL 3 KEYS INSERTED! THE RUNIC PORTAL GRINDS OPEN!             \033[1;32m|\033[0m");
                $display("\033[1;32m| \033[1;32m>>> VICTORY ESCAPE:\033[0m \033[1;37mYou and your companions have survived the terror!          \033[1;32m|\033[0m");
                $display("\033[1;32m+================================================================================+\033[0m\n");
            end
        end
    endtask

    // ------------------------------------------------------------------------
    // High-Contrast Boxed Alert for Coin Flip & Combat Calamities
    // ------------------------------------------------------------------------
    task notify_coin_result;
        input         is_success;
        input [255:0] hero_name;
        input [7:0]   dmg_val;
        input [7:0]   curr_hp;
        input [7:0]   max_hp;
        input [7:0]   curr_mind;
        begin
            if (!is_success) begin
                $display("\n\033[1;31m+====================================================================================================+\033[0m");
                $display("\033[1;31m| \033[41;1;37m [!] COIN OF FATE FAILED - LETHAL BLOW STRUCK ! \033[0m\033[1;31m                                                   |\033[0m");
                $display("\033[1;31m| \033[1;37m>> %-12s failed to deflect the cleave! Took \033[1;31m-%0d DMG\033[1;37m and lost \033[1;36m-20 Mind\033[1;37m to terror!          \033[1;31m|\033[0m", hero_name, dmg_val);
                $display("\033[1;31m| \033[1;33m>> Vitality Status: %-12s has %3d / %3d HP | Mind: %3d/100                                        \033[1;31m|\033[0m", hero_name, curr_hp, max_hp, curr_mind);
                $display("\033[1;31m+====================================================================================================+\033[0m\n");
            end else begin
                $display("\n\033[1;32m+====================================================================================================+\033[0m");
                $display("\033[1;32m| \033[42;1;37m [*] COIN OF FATE SUCCESS - FLAWLESS COUNTER PARRY ! \033[0m\033[1;32m                                              |\033[0m");
                $display("\033[1;32m| \033[1;37m>> %-12s perfectly parried the lethal execution and countered for \033[1;32m+%0d pure DMG\033[1;37m!          \033[1;32m|\033[0m", hero_name, dmg_val);
                $display("\033[1;32m| \033[1;33m>> The adversary reels in shock and agonizing agony from your riposte!                             \033[1;32m|\033[0m");
                $display("\033[1;32m+====================================================================================================+\033[0m\n");
            end
        end
    endtask

    task notify_hero_fallen;
        input [255:0] hero_name;
        input [255:0] next_name;
        begin
            $display("\n\033[1;31m+====================================================================================================+\033[0m");
            $display("\033[1;31m| \033[41;1;37m [!] CRITICAL CASUALTY: FRONTLINE EXPLORER COLLAPSED ! \033[0m\033[1;31m                                            |\033[0m");
            $display("\033[1;31m| \033[1;37m>> %-12s has fallen unconscious to devastating wounds!                                     \033[1;31m|\033[0m", hero_name);
            $display("\033[1;33m| >> Reserve companion %-12s steps forward to defend the party frontline!                 \033[1;31m|\033[0m", next_name);
            $display("\033[1;31m+====================================================================================================+\033[0m\n");
        end
    endtask

    sprite_router u_router();

    // Task to render hot pink health bar (solid background blocks)
    task print_pink_health_bar;
        input [7:0] curr;
        input [7:0] max_v;
        input integer bar_len;
        integer filled, j;
        begin
            if (max_v > 0)
                filled = (curr * bar_len) / max_v;
            else
                filled = 0;
            if (filled > bar_len) filled = bar_len;
            if (filled == 0 && curr > 0) filled = 1;

            $write("\033[1;37m[\033[0m");
            // Pink filled blocks (space with pink background)
            for (j = 0; j < filled; j = j + 1) begin
                $write("\033[48;2;255;105;180m \033[0m");
            end
            // Empty dark blocks (space with dark gray background)
            for (j = filled; j < bar_len; j = j + 1) begin
                $write("\033[48;2;55;55;55m \033[0m");
            end
            $write("\033[1;37m]\033[0m");
        end
    endtask

    // Task to render cyan mind bar (solid background blocks)
    task print_cyan_mind_bar;
        input [7:0] curr;
        input integer bar_len;
        integer filled, j;
        begin
            filled = (curr * bar_len) / 100;
            if (filled > bar_len) filled = bar_len;
            if (filled == 0 && curr > 0) filled = 1;
            $write("\033[1;37m[\033[0m");
            for (j = 0; j < filled; j = j + 1) begin
                $write("\033[48;2;80;180;255m \033[0m");
            end
            for (j = filled; j < bar_len; j = j + 1) begin
                $write("\033[48;2;55;55;55m \033[0m");
            end
            $write("\033[1;37m]\033[0m");
        end
    endtask

    // Task to render amber hunger bar (solid background blocks)
    task print_amber_hunger_bar;
        input [7:0] curr;
        input integer bar_len;
        integer filled, j;
        begin
            filled = (curr * bar_len) / 100;
            if (filled > bar_len) filled = bar_len;
            if (filled == 0 && curr > 0) filled = 1;
            $write("\033[1;37m[\033[0m");
            for (j = 0; j < filled; j = j + 1) begin
                $write("\033[48;2;255;160;40m \033[0m");
            end
            for (j = filled; j < bar_len; j = j + 1) begin
                $write("\033[48;2;55;55;55m \033[0m");
            end
            $write("\033[1;37m]\033[0m");
        end
    endtask

    // Task to render custom mini bar with solid background blocks
    task print_mini_bar;
        input [7:0] curr;
        input [7:0] max_v;
        input integer bar_len;
        input [7:0] r, g, b;
        integer filled, j;
        begin
            if (max_v > 0)
                filled = (curr * bar_len) / max_v;
            else
                filled = 0;
            if (filled > bar_len) filled = bar_len;
            if (filled == 0 && curr > 0) filled = 1;

            $write("\033[1;37m[\033[0m");
            for (j = 0; j < filled; j = j + 1) begin
                $write("\033[48;2;%0d;%0d;%0dm \033[0m", r, g, b);
            end
            for (j = filled; j < bar_len; j = j + 1) begin
                $write("\033[48;2;45;45;45m \033[0m");
            end
            $write("\033[1;37m]\033[0m");
        end
    endtask

    task get_character_role;
        input  [3:0]   cid;
        output [167:0] role_str;
        begin
            case (cid)
                4'd1: role_str = "Mercenary (Rogue)";
                4'd2: role_str = "Holy Knight (Paladin)";
                4'd3: role_str = "Dark Priest (Mage)";
                4'd4: role_str = "Outlander (Berserker)";
                4'd5: role_str = "Midnight Sun (Leader)";
                4'd6: role_str = "Cave Wolf (Beast)";
                4'd7: role_str = "Innocent Ward";
                4'd8: role_str = "Doom Wizard (Lich)";
                default: role_str = "Dungeon Explorer";
            endcase
        end
    endtask

    task get_skill_names;
        input  [3:0]   cid;
        output [127:0] sk1;
        output [127:0] sk2;
        begin
            case (cid)
                4'd1: begin sk1 = "Steal"; sk2 = "En Garde"; end
                4'd2: begin sk1 = "Fast Stance"; sk2 = "Loving Whispers"; end
                4'd3: begin sk1 = "Black Orb"; sk2 = "Blood Sacr"; end
                4'd4: begin sk1 = "War Cry"; sk2 = "Devour"; end
                4'd5: begin sk1 = "Leg Sweep"; sk2 = "Tactician"; end
                4'd6: begin sk1 = "Primal Bite"; sk2 = "Howl"; end
                4'd7: begin sk1 = "Mischief"; sk2 = "Loving Hug"; end
                4'd8: begin sk1 = "Combustion"; sk2 = "Hellfire"; end
                default: begin sk1 = "Power Slash"; sk2 = "Focus Mind"; end
            endcase
        end
    endtask

    task print_short_name;
        input [3:0] cid;
        begin
            case (cid)
                4'd1: $write("Cahara");
                4'd2: $write("D'arce");
                4'd3: $write("Enki");
                4'd4: $write("Ragnvaldr");
                4'd5: $write("Le'garde");
                4'd6: $write("Moonless");
                4'd7: $write("The Girl");
                4'd8: $write("Nas'hrah");
                default: $write("Hero");
            endcase
        end
    endtask

    // ------------------------------------------------------------------------
    // Visual & Audio Polish Tasks (Screen Shake, Slash Visual FX)
    // ------------------------------------------------------------------------
    task render_slash_fx;
        begin
            $display("\033[1;31m   >>> ////// LETHAL EXECUTION: BRUTAL SLASH TEARS THROUGH FLESH ////// <<<\033[0m\a");
        end
    endtask

    task render_screen_shake;
        begin
            $write("\033[2C\033[1;31m[ VIOLENT IMPACT SHAKES YOUR BODY ! ]\033[0m\r\a");
        end
    endtask

    // ------------------------------------------------------------------------
    // Interactive Dynamic Cursor Selection Menus (Fear & Hunger Style)
    // ------------------------------------------------------------------------
    task render_action_menu;
        input [2:0] cursor_pos;
        input       is_hard_mode;
        input [7:0] poppy_qty, marijuana_qty;
        begin
            $display("\033[1;36m+====================================================================================================+\033[0m");
            $display("\033[1;36m|                                  TACTICAL ACTION COMMAND MENU                                      |\033[0m");
            $display("\033[1;36m+====================================================================================================+\033[0m");
            
            if (cursor_pos == 3'd0)
                $display("  \033[1;30;43m > [1] ATTACK (TARGET LIMBS)   \033[0m : \033[1;33mTarget enemy Head, Torso, Arms, or Legs!          \033[1;33m< [SELECT]\033[0m");
            else
                $display("    [1] ATTACK (TARGET LIMBS)   : Target enemy Head, Torso, Arms, or Legs!");

            if (cursor_pos == 3'd1)
                $display("  \033[1;30;43m > [2] SKILLS (HEXEN SKILLS)    \033[0m : \033[1;33mUnleash unique explorer class spells & abilities! \033[1;33m< [SELECT]\033[0m");
            else
                $display("    [2] SKILLS (HEXEN SKILLS)    : Unleash unique explorer class spells & abilities!");

            if (cursor_pos == 3'd2)
                $display("  \033[1;30;43m > [3] SUPPLIES (SURVIVAL BAG)  \033[0m : \033[1;33mAdminister herbs, food, or spirits (Costs 1 Turn!)\033[1;33m< [SELECT]\033[0m");
            else
                $display("    [3] SUPPLIES (SURVIVAL BAG)  : Administer herbs, food, or spirits (Costs 1 Turn!)");

            if (cursor_pos == 3'd3)
                $display("  \033[1;30;43m > [4] DEFEND (BRACE / GUARD)   \033[0m : \033[1;33mRaise guard to mitigate incoming assault by 70%%!  \033[1;33m< [SELECT]\033[0m");
            else
                $display("    [4] DEFEND (BRACE / GUARD)   : Raise guard to mitigate incoming assault by 70%%!");

            if (cursor_pos == 3'd4)
                $display("  \033[1;30;43m > [5] TAG SWITCH (FRONTLINE)   \033[0m : \033[1;33mSwap another conscious companion to frontline     \033[1;33m< [SELECT]\033[0m");
            else
                $display("    [5] TAG SWITCH (FRONTLINE)   : Swap another conscious companion to frontline");

            if (cursor_pos == 3'd5)
                $display("  \033[1;30;43m > [6] FLEE (DESPERATE RETREAT) \033[0m : \033[1;33mAttempt a retreat into dark corridors (50%% chance)\033[1;33m< [SELECT]\033[0m");
            else
                $display("    [6] FLEE (DESPERATE RETREAT) : Attempt a retreat into dark corridors (50%% chance)");

            $display("\033[1;36m+====================================================================================================+\033[0m");
            $display("\033[90m  Keys: [W/S] or [Up/Down]: Move Cursor | [E/Space/Enter]: Confirm Action | [1-6]: Quick Select\033[0m\n");
        end
    endtask

    // Task to render Limb Targeting Menu
    task render_limb_menu_interactive;
        input [2:0]   cursor_pos;
        input [7:0]   h_hp, h_max;
        input [7:0]   t_hp, t_max;
        input [7:0]   ar_hp, ar_max;
        input [7:0]   al_hp, al_max;
        input [7:0]   lr_hp, lr_max;
        input [7:0]   ll_hp, ll_max;
        input         is_crawling;
        input         is_disarmed;
        begin
            $display("\033[1;31m+====================================================================================================+\033[0m");
            $display("\033[1;31m|                        TARGET ENEMY BODY PARTS (TACTICAL SEVERING)                                 |\033[0m");
            $display("\033[1;31m+====================================================================================================+\033[0m");
            
            // Option 0: HEAD
            if (h_hp == 0) begin
                $display("    [1] HEAD             : \033[1;31m[SEVERED / DECAPITATED]\033[0m");
            end else if (cursor_pos == 3'd0) begin
                $write("  \033[1;30;43m > [1] HEAD             \033[0m : ");
                print_pink_health_bar(h_hp, h_max, 10);
                if (is_crawling)
                    $display(" \033[1;33m[Hit: 100%% - FOE CRAWLING! SEVER HEAD FOR INSTANT KILL!]\033[0m");
                else
                    $display(" \033[1;31m[Hit:  25%% - DECAPITATION = INSTANT KILL!]\033[0m");
            end else begin
                $write("    [1] HEAD             : ");
                print_pink_health_bar(h_hp, h_max, 10);
                if (is_crawling)
                    $display(" \033[1;33m[Hit: 100%% - FOE CRAWLING! SEVER HEAD FOR INSTANT KILL!]\033[0m");
                else
                    $display(" \033[90m[Hit:  25%% - DECAPITATION = INSTANT KILL!]\033[0m");
            end

            // Option 1: TORSO
            if (t_hp == 0) begin
                $display("    [2] TORSO            : \033[1;31m[PUNCTURED / DESTROYED]\033[0m");
            end else if (cursor_pos == 3'd1) begin
                $write("  \033[1;30;43m > [2] TORSO            \033[0m : ");
                print_pink_health_bar(t_hp, t_max, 10);
                $display(" \033[1;32m[Hit:  95%% - CORE VITALS (HEART & TORSO)]\033[0m");
            end else begin
                $write("    [2] TORSO            : ");
                print_pink_health_bar(t_hp, t_max, 10);
                $display(" \033[90m[Hit:  95%% - CORE VITALS]\033[0m");
            end

            // Option 2: RIGHT ARM (Weapon Arm)
            if (ar_hp == 0) begin
                $display("    [3] RIGHT ARM        : \033[1;31m[SEVERED / DISARMED]\033[0m");
            end else if (cursor_pos == 3'd2) begin
                $write("  \033[1;30;43m > [3] RIGHT ARM        \033[0m : ");
                print_pink_health_bar(ar_hp, ar_max, 10);
                $display(" \033[1;33m[Hit:  80%% - WEAPON ARM! SEVER TO DISARM HEAVY STRIKES!]\033[0m");
            end else begin
                $write("    [3] RIGHT ARM        : ");
                print_pink_health_bar(ar_hp, ar_max, 10);
                $display(" \033[90m[Hit:  80%% - WEAPON ARM]\033[0m");
            end

            // Option 3: LEFT ARM (Shield / Offhand)
            if (al_hp == 0) begin
                $display("    [4] LEFT ARM         : \033[1;31m[SEVERED / BROKEN GUARD]\033[0m");
            end else if (cursor_pos == 3'd3) begin
                $write("  \033[1;30;43m > [4] LEFT ARM         \033[0m : ");
                print_pink_health_bar(al_hp, al_max, 10);
                $display(" \033[1;33m[Hit:  80%% - OFFHAND / SHIELD ARM! SEVER TO CRUSH GUARD!]\033[0m");
            end else begin
                $write("    [4] LEFT ARM         : ");
                print_pink_health_bar(al_hp, al_max, 10);
                $display(" \033[90m[Hit:  80%% - OFFHAND ARM]\033[0m");
            end

            // Option 4: RIGHT LEG
            if (lr_hp == 0) begin
                $display("    [5] RIGHT LEG        : \033[1;31m[SEVERED / MUTILATED]\033[0m");
            end else if (cursor_pos == 3'd4) begin
                $write("  \033[1;30;43m > [5] RIGHT LEG        \033[0m : ");
                print_pink_health_bar(lr_hp, lr_max, 10);
                $display(" \033[1;36m[Hit:  85%% - RIGHT LEG! CRIPPLES EVASION!]\033[0m");
            end else begin
                $write("    [5] RIGHT LEG        : ");
                print_pink_health_bar(lr_hp, lr_max, 10);
                $display(" \033[90m[Hit:  85%% - RIGHT LEG]\033[0m");
            end

            // Option 5: LEFT LEG
            if (ll_hp == 0) begin
                $display("    [6] LEFT LEG         : \033[1;31m[SEVERED / MUTILATED]\033[0m");
            end else if (cursor_pos == 3'd5) begin
                $write("  \033[1;30;43m > [6] LEFT LEG         \033[0m : ");
                print_pink_health_bar(ll_hp, ll_max, 10);
                $display(" \033[1;36m[Hit:  85%% - LEFT LEG! SEVER BOTH LEGS TO FORCE CRAWL!]\033[0m");
            end else begin
                $write("    [6] LEFT LEG         : ");
                print_pink_health_bar(ll_hp, ll_max, 10);
                $display(" \033[90m[Hit:  85%% - LEFT LEG]\033[0m");
            end

            $display("\033[1;31m+====================================================================================================+\033[0m");
            $display("\033[90m  Keys: [W/S] or [Up/Down]: Move Cursor | [E/Space/Enter]: Sever Target Limb | [1-6]: Quick Select | [C]: Cancel\033[0m\n");
        end
    endtask

    // Task to render Coin Flip of Fate prompt
    task render_coin_flip_prompt;
        input         cursor_pos; // 0: Heads, 1: Tails
        input [255:0] enemy_name;
        input [255:0] attack_name;
        begin
            $display("\n\033[41;1;37m+====================================================================================================+\033[0m");
            $display("\033[41;1;37m|  !!! LETHAL THREAT DETECTED: %-18s PREPARES [%-20s] !!!     |\033[0m", enemy_name, attack_name);
            $display("\033[41;1;37m|  COIN FLIP OF FATE: PARRY COMPLETELY OR SUFFER CATASTROPHIC MUTILATION !                           |\033[0m");
            $display("\033[41;1;37m+====================================================================================================+\033[0m");
            $display("\033[1;33m  BET YOUR LIFE UPON THE COIN: \033[0m");
            if (cursor_pos == 1'b0) begin
                $display("  \033[1;30;43m > [1] HEADS (SYLVIAN'S GRACE) \033[0m : \033[1;32mBlessing of love and preservation\033[0m \033[1;33m< [SELECTED]\033[0m");
                $display("    [2] TAILS (GRO-GOROTH'S WRATH): Might of ancient slaughter and destruction");
            end else begin
                $display("    [1] HEADS (SYLVIAN'S GRACE) : Blessing of love and preservation");
                $display("  \033[1;30;43m > [2] TAILS (GRO-GOROTH'S WRATH): \033[1;31mMight of ancient slaughter and destruction\033[0m \033[1;33m< [SELECTED]\033[0m");
            end
            $display("\033[90m  Keys: [W/S] or [Up/Down]: Toggle Coin Face | [E/Space/Enter]: Flip Coin | [1/2]: Quick Select\033[0m\n");
        end
    endtask

    // Task to render Coin Animation
    task render_coin_animation;
        input user_choice;
        input flip_result;
        begin
            $display("\n  \033[1;33m>> THE COIN SPINS INTO THE DARK AIR... \033[0m");
            $display("     [ (O) | ]");
            $display("     [ (O) / ]");
            $display("     [ (O) - ]");
            $display("     [ (O) \\ ]\a");

            if (flip_result == 1'b0)
                $display("  \033[1;33m>> COIN LANDED ON: [ HEADS (SYLVIAN) ] !\033[0m");
            else
                $display("  \033[1;33m>> COIN LANDED ON: [ TAILS (GRO-GOROTH) ] !\033[0m");

            if (user_choice == flip_result) begin
                $display("\033[1;32m+====================================================================================================+\033[0m");
                $display("\033[1;32m|  >>> [SUBLIME PARRY!]: YOU CALLED THE COIN! DEFLECTED LETHAL BLOW AND COUNTER-STRUCK! <<<          |\033[0m");
                $display("\033[1;32m+====================================================================================================+\033[0m\a\n");
            end else begin
                $display("\033[1;31m+====================================================================================================+\033[0m");
                $display("\033[1;31m|  >>> [COIN FLIP FAILED!]: THE LETHAL BLOW SHATTERS FLESH AND BONE WITH CRITICAL CARNAGE! <<<       |\033[0m");
                $display("\033[1;31m+====================================================================================================+\033[0m\a\n");
            end
        end
    endtask

    // Task to render Skill Menu
    task render_skill_menu_interactive;
        input [1:0]   cursor_pos;
        input [3:0]   char_id;
        input [7:0]   char_mind;
        begin
            $display("\033[1;35m+====================================================================================================+\033[0m");
            $display("\033[1;35m|                            ANCIENT OCCULT SPELLS & HEXEN SKILLS                                    |\033[0m");
            $display("\033[1;35m+====================================================================================================+\033[0m");
            case (char_id)
                4'd1: begin // Cahara
                    if (cursor_pos == 2'd0)
                        $display("  \033[1;30;43m > [1] STEAL                 \033[0m : \033[1;33mPilfer items from foe's bag + Swift strike for 14 dmg (Mind: 0)\033[0m");
                    else
                        $display("    [1] STEAL                 : Pilfer items from foe's bag + Swift strike for 14 dmg (Mind: 0)");
                    if (cursor_pos == 2'd1)
                        $display("  \033[1;30;43m > [2] EN GARDE             \033[0m : \033[1;33mReactive parry stance, grants +30%% evasion this turn (Mind: 5)\033[0m");
                    else
                        $display("    [2] EN GARDE             : Reactive parry stance, grants +30%% evasion this turn (Mind: 5)");
                end
                4'd2: begin // D'arce
                    if (cursor_pos == 2'd0)
                        $display("  \033[1;30;43m > [1] FAST STANCE           \033[0m : \033[1;33mUnleash 2 rapid weapon strikes in 1 single turn! (Mind: 10)\033[0m");
                    else
                        $display("    [1] FAST STANCE           : Unleash 2 rapid weapon strikes in 1 single turn! (Mind: 10)");
                    if (cursor_pos == 2'd1)
                        $display("  \033[1;30;43m > [2] LOVING WHISPERS       \033[0m : \033[1;32mSylvian sacred prayer restores +45 HP to yourself (Mind: 15)\033[0m");
                    else
                        $display("    [2] LOVING WHISPERS       : Sylvian sacred prayer restores +45 HP to yourself (Mind: 15)");
                end
                4'd3: begin // Enki
                    if (cursor_pos == 2'd0)
                        $display("  \033[1;30;43m > [1] HURTING               \033[0m : \033[1;35mDark occult spell rips apart 1 enemy limb for 45 pure dmg (Mind: 15)\033[0m");
                    else
                        $display("    [1] HURTING               : Dark occult spell rips apart 1 enemy limb for 45 pure dmg (Mind: 15)");
                    if (cursor_pos == 2'd1)
                        $display("  \033[1;30;43m > [2] BLACK ORB             \033[0m : \033[1;35mCast 3 dark matter orbs inflicting 60 total damage (Mind: 25)\033[0m");
                    else
                        $display("    [2] BLACK ORB             : Cast 3 dark matter orbs inflicting 60 total damage (Mind: 25)");
                end
                4'd4: begin // Ragnvaldr
                    if (cursor_pos == 2'd0)
                        $display("  \033[1;30;43m > [1] DEVOUR                \033[0m : \033[1;31mSavage cannibalistic bite deals 35 dmg, -40 Hunger, +20 HP (Mind: 0)\033[0m");
                    else
                        $display("    [1] DEVOUR                : Savage cannibalistic bite deals 35 dmg, -40 Hunger, +20 HP (Mind: 0)");
                    if (cursor_pos == 2'd1)
                        $display("  \033[1;30;43m > [2] WAR CRY               \033[0m : \033[1;31mBloodcurdling roar reducing enemy DEF by 50%% (Mind: 10)\033[0m");
                    else
                        $display("    [2] WAR CRY               : Bloodcurdling roar reducing enemy DEF by 50%% (Mind: 10)");
                end
                4'd8: begin // Nas'hrah
                    if (cursor_pos == 2'd0)
                        $display("  \033[1;30;43m > [1] COMBUSTION            \033[0m : \033[1;31mCataclysmic hellfire incinerates ALL enemy limbs for 50 dmg! (Mind: 20)\033[0m");
                    else
                        $display("    [1] COMBUSTION            : Cataclysmic hellfire incinerates ALL enemy limbs for 50 dmg! (Mind: 20)");
                    if (cursor_pos == 2'd1)
                        $display("  \033[1;30;43m > [2] DOOM LAUGHTER         \033[0m : \033[1;33mMocking godly laughter cleanses squad terror, restoring 30 Mind (Mind: 0)\033[0m");
                    else
                        $display("    [2] DOOM LAUGHTER         : Mocking godly laughter cleanses squad terror, restoring 30 Mind (Mind: 0)");
                end
                default: begin
                    if (cursor_pos == 2'd0)
                        $display("  \033[1;30;43m > [1] ALL-OUT STRIKE        \033[0m : \033[1;33mReckless assault dealing 30 dmg at the cost of 10 HP (Mind: 5)\033[0m");
                    else
                        $display("    [1] ALL-OUT STRIKE        : Reckless assault dealing 30 dmg at the cost of 10 HP (Mind: 5)");
                    if (cursor_pos == 2'd1)
                        $display("  \033[1;30;43m > [2] GROIN TACKLE          \033[0m : \033[1;33mLow blow stuns the beast, causing it to forfeit next turn (Mind: 10)\033[0m");
                    else
                        $display("    [2] GROIN TACKLE          : Low blow stuns the beast, causing it to forfeit next turn (Mind: 10)");
                end
            endcase
            $display("\033[1;35m+====================================================================================================+\033[0m");
            $display("\033[90m  Keys: [W/S] or [Up/Down]: Move Cursor | [E/Space/Enter]: Cast Skill | [1/2]: Quick Select | [C]: Cancel\033[0m\n");
        end
    endtask

    // Task to render Survival Bag Menu
    task render_survival_bag_interactive;
        input [2:0] cursor_pos;
        input       is_hard_mode;
        input [7:0] bag_poppy;
        input [7:0] bag_marijuana;
        input [7:0] bag_bread;
        input [7:0] bag_meat;
        input [7:0] bag_ale;
        input [7:0] bag_keys;
        begin
            $display("\033[1;32m+====================================================================================================+\033[0m");
            $display("\033[1;32m|                                  SURVIVAL POUCH & PROVISIONS                                       |\033[0m");
            $display("\033[1;32m+====================================================================================================+\033[0m");
            
            // Item 0: Poppy
            if (cursor_pos == 3'd0)
                $display("  \033[1;30;43m > [1] POPPY FLOWER          \033[0m : Qty: %-2d | Restores +%0d HP             \033[1;33m< [SELECT]\033[0m", bag_poppy, is_hard_mode ? 30 : 50);
            else
                $display("    [1] POPPY FLOWER          : Qty: %-2d | Restores +%0d HP", bag_poppy, is_hard_mode ? 30 : 50);

            // Item 1: Marijuana
            if (cursor_pos == 3'd1)
                $display("  \033[1;30;43m > [2] MARIJUANA HERB        \033[0m : Qty: %-2d | Restores +%0d HP, +20 Mind   \033[1;33m< [SELECT]\033[0m", bag_marijuana, is_hard_mode ? 70 : 120);
            else
                $display("    [2] MARIJUANA HERB        : Qty: %-2d | Restores +%0d HP, +20 Mind", bag_marijuana, is_hard_mode ? 70 : 120);

            // Item 2: Moldy Bread
            if (cursor_pos == 3'd2)
                $display("  \033[1;30;43m > [3] MOLDY BREAD           \033[0m : Qty: %-2d | Relieves -40 Hunger          \033[1;33m< [SELECT]\033[0m", bag_bread);
            else
                $display("    [3] MOLDY BREAD           : Qty: %-2d | Relieves -40 Hunger", bag_bread);

            // Item 3: Dried Meat
            if (cursor_pos == 3'd3)
                $display("  \033[1;30;43m > [4] DRIED MEAT            \033[0m : Qty: %-2d | Relieves -60 Hunger, +15 HP  \033[1;33m< [SELECT]\033[0m", bag_meat);
            else
                $display("    [4] DRIED MEAT            : Qty: %-2d | Relieves -60 Hunger, +15 HP", bag_meat);

            // Item 4: Ale Flask
            if (cursor_pos == 3'd4)
                $display("  \033[1;30;43m > [5] ALE FLASK             \033[0m : Qty: %-2d | Cleanses Fear, +35 Mind      \033[1;33m< [SELECT]\033[0m", bag_ale);
            else
                $display("    [5] ALE FLASK             : Qty: %-2d | Cleanses Fear, +35 Mind", bag_ale);

            $display("\033[1;32m+====================================================================================================+\033[0m");
            $display("  \033[1;33mDUNGEON KEYS IN POSSESSION: %0d/3 KEYS\033[0m", bag_keys);
            $display("\033[90m  Keys: [W/S] or [Up/Down]: Move Cursor | [E/Space/Enter]: Use Item | [1-5]: Quick Select | [C]: Close Bag\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // 7. Tactical Battle Screen with Separated Sprites & Pink Health Bars
    // ------------------------------------------------------------------------
    task render_battle_screen;
        input         is_hard_mode;
        input [3:0]   char_id;
        input [5:0]   enemy_id;
        input         is_elite;
        input [7:0]   enemy_hp, enemy_max;
        input [255:0] act_name;
        input [7:0]   act_hp, act_max;
        input [3:0]   turn_no;
        input [7:0]   poppy_qty, marijuana_qty;
        integer lp, c;
        integer pw, ph, mw, mh, max_lines;
        reg        pt_trans, pb_trans, mt_trans, mb_trans;
        reg [23:0] pt_rgb, pb_rgb, mt_rgb, mb_rgb;
        begin
            $write("\033[2J\033[H");
            $display("\033[1;31m====================================================================================================\033[0m");
            if (enemy_id == 6'd23) begin
                $display("\033[41;1;37m                   !!! MIMIC ENCOUNTER: DECEITFUL CHEST HORROR ATTACKS! !!!                           \033[0m");
            end else if (is_elite) begin
                $display("\033[45;1;37m                   !!! ELITE ADVERSARY (+20%% STATS / 50%% KEY DROP / 20%% POPPY) !!!                 \033[0m");
            end else begin
                $display("\033[1;31m                   TACTICAL COMBAT: LABYRINTH CREATURE (20%% KEY DROP CHANCE)                        \033[0m");
            end
            $display("\033[1;31m====================================================================================================\033[0m\n");

            // Render side-by-side pixel art sprites: Player on Left vs Monster on Right (FAR APART)
            u_router.get_funger_dim(char_id, pw, ph);
            u_router.get_monster_dim(enemy_id, mw, mh);
            max_lines = ((ph > mh ? ph : mh) + 1) / 2;
            if (max_lines > 12) max_lines = 12;

            for (lp = 0; lp < max_lines; lp = lp + 1) begin
                $write("    ");
                // Left: Player Explorer (Faces Right by default)
                for (c = 0; c < 24; c = c + 1) begin
                    if (c < pw && lp * 2 < ph) begin
                        u_router.sample_funger_pixel(char_id, lp*2, lp*2+1, c, 1'b0, pt_trans, pt_rgb, pb_trans, pb_rgb);
                        print_hb_pixel(pt_trans, pt_rgb[23:16], pt_rgb[15:8], pt_rgb[7:0],
                                       pb_trans, pb_rgb[23:16], pb_rgb[15:8], pb_rgb[7:0]);
                    end else begin
                        $write(" ");
                    end
                end

                // Wide separation gap between combatants (34 spaces apart)
                $write("                                  ");

                // Right: Monster / Fantasy Creature Foe
                for (c = 0; c < 22; c = c + 1) begin
                    if (c < mw && lp * 2 < mh) begin
                        u_router.sample_monster_pixel(enemy_id, lp*2, lp*2+1, c, mt_trans, mt_rgb, mb_trans, mb_rgb);
                        print_hb_pixel(mt_trans, mt_rgb[23:16], mt_rgb[15:8], mt_rgb[7:0],
                                       mb_trans, mb_rgb[23:16], mb_rgb[15:8], mb_rgb[7:0]);
                    end else begin
                        $write(" ");
                    end
                end
                $write("\n");
            end
            $write("\n");

            // Combat Info: ONLY NAMES and PINK HEALTH BARS (no numbers, no extra clutter)
            // Row 1: Character and Enemy Names
            $write("    \033[1;33m%-24s\033[0m", act_name);
            $write("                                  ");
            $write("\033[1;35m");
            if (is_elite) $write("[ELITE] ");
            u_mon_db.print_monster_name(enemy_id);
            $display("\033[0m");

            // Row 2: Pink Health Bars
            $write("    ");
            print_pink_health_bar(act_hp, act_max, 16);
            $write("                                ");
            print_pink_health_bar(enemy_hp, enemy_max, 16);
            $display("\n");

            // Boxed Tactical Command Panel with full action descriptions
            $display("\033[1;36m+====================================================================================================+\033[0m");
            $display("\033[1;36m|                                  TACTICAL COMBAT COMMAND MENU                                      |\033[0m");
            $display("\033[1;36m+====================================================================================================+\033[0m");
            $display("\033[1;37m|  [1] ATTACK   : Strike foe with your active weapon to inflict physical damage (based on ATK vs DEF)|\033[0m");
            $display("\033[1;37m|  [2] DEFEND   : Raise guard to brace for enemy assault (Mitigates incoming damage by 70%%)           |\033[0m");
            $display("\033[1;37m|  [3] MEDICINE : Administer supplies from Survival Pouch (Poppy: +%2d HP | Marijuana: +%3d HP)       |\033[0m",
                     is_hard_mode ? 30 : 50, is_hard_mode ? 70 : 120);
            $display("\033[1;33m|                 >> NOTE: Using medicine consumes 1 Combat Turn! Enemy attacks in retaliation!      |\033[0m");
            $display("\033[1;37m|  [4] SWITCH   : Tag in another conscious squad member to lead combat (Consumes 1 Turn)              |\033[0m");
            $display("\033[1;37m|  [5] FLEE     : Attempt a desperate retreat back into corridors (50%% escape success probability)   |\033[0m");
            $display("\033[1;36m+====================================================================================================+\033[0m");
            $display("\033[1;37m  SURVIVAL SUPPLIES IN POUCH: \033[38;2;242;34;84m[+] Poppy: %0d (+%0d HP)\033[0m | \033[38;2;105;225;101m[*] Marijuana: %0d (+%0d HP)\033[0m",
                     poppy_qty, is_hard_mode ? 30 : 50, marijuana_qty, is_hard_mode ? 70 : 120);
            $display("\033[1;36m======================================================================================================\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // 7B. Diagonal 50/50 Battle Screen (Enemy Top-Right, Hero Bottom-Left)
    // ------------------------------------------------------------------------
    task render_battle_screen_diagonal;
        input         is_hard_mode;
        input [3:0]   turn_no;
        // Hero data
        input [3:0]   char_id;
        input [255:0] hero_name;
        input [7:0]   hero_hp, hero_max;
        input [7:0]   hero_mind, hero_hunger;
        input [7:0]   hero_atk, hero_def;
        input [7:0]   poppy_qty, marijuana_qty, bread_qty, ale_qty;
        // Squad Lineup
        input [3:0]   s1_id, s2_id, s3_id, s4_id;
        input [7:0]   s1_hp, s2_hp, s3_hp, s4_hp;
        // Enemy data
        input [5:0]   enemy_id;
        input         is_elite;
        input [7:0]   enemy_hp, enemy_max;
        input [7:0]   head_hp, head_max;
        input [7:0]   torso_hp, torso_max;
        input [7:0]   arm_r_hp, arm_r_max;
        input [7:0]   arm_l_hp, arm_l_max;
        input [7:0]   leg_r_hp, leg_r_max;
        input         is_crawling, is_disarmed;
        // Event log
        input [511:0] last_action_msg;
        integer lp, c;
        integer pw, ph, mw, mh;
        reg        pt_trans, pb_trans, mt_trans, mb_trans;
        reg [23:0] pt_rgb, pb_rgb, mt_rgb, mb_rgb;
        reg [167:0] hero_role;
        reg [127:0] sk1_name, sk2_name;
        begin
            get_character_role(char_id, hero_role);
            get_skill_names(char_id, sk1_name, sk2_name);
            u_router.get_funger_dim(char_id, pw, ph);
            u_router.get_monster_dim(enemy_id, mw, mh);

            $write("\033[2J\033[H");
            $display("\033[1;31m====================================================================================================\033[0m");
            $write("  \033[1;37mTACTICAL COMBAT [TURN %0d]\033[0m  |  \033[1;33mFEAR & HUNGER LABYRINTH\033[0m", turn_no);
            if (enemy_id == 6'd23)
                $display("  |  \033[41;1;37m[!] MIMIC HORROR ENCOUNTER [!]\033[0m");
            else if (is_elite)
                $display("  |  \033[45;1;37m[!] ELITE DUNGEON ADVERSARY (+20%% STATS) [!]\033[0m");
            else
                $display("  |  \033[1;31m[!] FOE ENGAGED [!]\033[0m");
            $display("\033[1;31m====================================================================================================\033[0m");

            // ----------------------------------------------------------------
            // TOP 50%: ENEMY ADVERSARY ZONE (Enemy Stats Left, Monster Right)
            // ----------------------------------------------------------------
            for (lp = 0; lp < 11; lp = lp + 1) begin
                // Left Column: Enemy Information & Targetable Limbs
                case (lp)
                    0: begin
                        $write("  \033[1;31m[FOE]:\033[0m \033[1;35m");
                        if (is_elite) $write("[ELITE] ");
                        u_mon_db.print_monster_name(enemy_id);
                        $write("\033[0m ");
                        print_mini_bar(enemy_hp, enemy_max, 10, 240, 50, 70);
                        $write(" \033[1;37m%3d/%3d HP\033[0m", enemy_hp, enemy_max);
                    end
                    1: begin
                        $write("  \033[90mCONDITION: \033[0m");
                        if (is_crawling) $write("\033[41;1;37m[CRAWLING]\033[0m ");
                        if (is_disarmed) $write("\033[43;1;30m[DISARMED]\033[0m ");
                        if (!is_crawling && !is_disarmed) $write("\033[1;32m[LETHAL / INTACT]\033[0m");
                    end
                    2: $write("  \033[1;30m------------------------------------------------\033[0m");
                    3: begin
                        $write("  \033[1;31m[H] HEAD \033[0m : ");
                        if (head_hp == 0) $write("\033[1;31m[SEVERED / DECAPITATED]            \033[0m");
                        else begin
                            print_mini_bar(head_hp, head_max, 8, 255, 60, 60);
                            $write(" %2d/%2d \033[90m(25%% Instakill)\033[0m", head_hp, head_max);
                        end
                    end
                    4: begin
                        $write("  \033[1;33m[T] TORSO\033[0m : ");
                        if (torso_hp == 0) $write("\033[1;31m[PUNCTURED / COLLAPSED]            \033[0m");
                        else begin
                            print_mini_bar(torso_hp, torso_max, 8, 255, 180, 50);
                            $write(" %2d/%2d \033[90m(95%% Vital Core)\033[0m", torso_hp, torso_max);
                        end
                    end
                    5: begin
                        $write("  \033[1;36m[R] R-ARM\033[0m : ");
                        if (arm_r_hp == 0) $write("\033[1;31m[SEVERED / DISARMED]               \033[0m");
                        else begin
                            print_mini_bar(arm_r_hp, arm_r_max, 8, 80, 200, 255);
                            $write(" %2d/%2d \033[90m(Disarms ATK)   \033[0m", arm_r_hp, arm_r_max);
                        end
                    end
                    6: begin
                        $write("  \033[1;36m[L] L-ARM\033[0m : ");
                        if (arm_l_hp == 0) $write("\033[1;31m[SEVERED / GUARD BROKEN]           \033[0m");
                        else begin
                            print_mini_bar(arm_l_hp, arm_l_max, 8, 80, 200, 255);
                            $write(" %2d/%2d \033[90m(Breaks Guard)  \033[0m", arm_l_hp, arm_l_max);
                        end
                    end
                    7: begin
                        $write("  \033[1;32m[K] LEGS \033[0m : ");
                        if (leg_r_hp == 0) $write("\033[1;31m[SEVERED / FORCED CRAWLING]        \033[0m");
                        else begin
                            print_mini_bar(leg_r_hp, leg_r_max, 8, 100, 230, 100);
                            $write(" %2d/%2d \033[90m(Forces Crawl)  \033[0m", leg_r_hp, leg_r_max);
                        end
                    end
                    8: $write("  \033[1;30m------------------------------------------------\033[0m");
                    9: $write("  \033[90m[TIP]: Severing both legs pins foe for 100%% head hit!\033[0m");
                    default: $write("                                                  ");
                endcase

                // Move cursor to column 56 for Monster Sprite rendering
                $write("\033[56G");
                for (c = 0; c < 22; c = c + 1) begin
                    if (c < mw && lp * 2 < mh) begin
                        u_router.sample_monster_pixel(enemy_id, lp*2, lp*2+1, c, mt_trans, mt_rgb, mb_trans, mb_rgb);
                        print_hb_pixel(mt_trans, mt_rgb[23:16], mt_rgb[15:8], mt_rgb[7:0],
                                       mb_trans, mb_rgb[23:16], mb_rgb[15:8], mb_rgb[7:0]);
                    end else begin
                        $write(" ");
                    end
                end
                $write("\n");
            end

            $display("\033[1;30m====================================================================================================\033[0m");

            // ----------------------------------------------------------------
            // BOTTOM 50%: HERO SQUAD ZONE (Hero Sprite Left, Hero Stats Right)
            // ----------------------------------------------------------------
            for (lp = 0; lp < 11; lp = lp + 1) begin
                $write("  ");
                // Left Column: Player Explorer Sprite Model
                for (c = 0; c < 24; c = c + 1) begin
                    if (c < pw && lp * 2 < ph) begin
                        u_router.sample_funger_pixel(char_id, lp*2, lp*2+1, c, 1'b0, pt_trans, pt_rgb, pb_trans, pb_rgb);
                        print_hb_pixel(pt_trans, pt_rgb[23:16], pt_rgb[15:8], pt_rgb[7:0],
                                       pb_trans, pb_rgb[23:16], pb_rgb[15:8], pb_rgb[7:0]);
                    end else begin
                        $write(" ");
                    end
                end

                // Move cursor to column 32 for Hero Stats & Squad Status
                $write("\033[32G");
                case (lp)
                    0: begin
                        $write("\033[1;32m[HERO]:\033[0m \033[1;33m");
                        print_short_name(char_id);
                        $write("\033[0m   ");
                        print_mini_bar(hero_hp, hero_max, 10, 255, 105, 180);
                        $write(" \033[1;37m%3d/%3d HP\033[0m", hero_hp, hero_max);
                    end
                    1: begin
                        $write("\033[38;2;80;180;255m[MIND]  :\033[0m ");
                        print_mini_bar(hero_mind, 8'd100, 8, 80, 180, 255);
                        $write(" %3d/100 | \033[38;2;255;160;40m[HUNGER]:\033[0m ", hero_mind);
                        print_mini_bar(hero_hunger, 8'd100, 8, 255, 160, 40);
                        $write(" %3d/100", hero_hunger);
                    end
                    2: begin
                        $write("\033[1;33mATK: %2d\033[0m  \033[1;36mDEF: %2d\033[0m  |  \033[1;37mCLASS:\033[0m \033[1;34m%s\033[0m",
                               hero_atk, hero_def, hero_role);
                    end
                    3: $write("\033[1;30m------------------------------------------------------------------\033[0m");
                    4: begin
                        $write("POUCH: \033[38;2;242;34;84m[P] Poppy: %-2d (+50HP)\033[0m   |  \033[38;2;105;225;101m[M] Weed: %-2d (+120HP)\033[0m",
                               poppy_qty, marijuana_qty);
                    end
                    5: begin
                        $write("       \033[38;2;230;180;50m[B] Bread: %-2d (-40Hng)\033[0m  |  \033[38;2;180;100;255m[A] Ale:  %-2d (+35Mnd)\033[0m",
                               bread_qty, ale_qty);
                    end
                    6: begin
                        $write("SQUAD: 1.");
                        print_short_name(s1_id);
                        $write("(%0d) 2.", s1_hp);
                        print_short_name(s2_id);
                        $write("(%0d) 3.", s2_hp);
                        print_short_name(s3_id);
                        $write("(%0d) 4.", s3_hp);
                        print_short_name(s4_id);
                        $write("(%0d)", s4_hp);
                    end
                    7: $write("\033[1;30m------------------------------------------------------------------\033[0m");
                    8: $write("\033[90m[STATUS]: Ready for orders. Type hotkey below and press Enter.\033[0m");
                    default: $write("                                                                  ");
                endcase
                $write("\n");
            end

            // ----------------------------------------------------------------
            // LAST ACTION EVENT TICKER (HIGH-CONTRAST BOXED NOTIFICATION)
            // ----------------------------------------------------------------
            $display("\033[1;33m+====================================================================================================+\033[0m");
            $display("\033[1;33m| \033[43;1;30m [EVENT & ACTION REPORT] \033[0m \033[1;37m%-72s\033[1;33m |\033[0m", last_action_msg);
            $display("\033[1;33m+====================================================================================================+\033[0m");

            // ----------------------------------------------------------------
            // DIRECT ACTION DECK (INSTANT 1-KEY COMMANDS)
            // ----------------------------------------------------------------
            $display("\033[1;37m  TARGET LIMB : \033[1;31m[H]\033[0m Head (Instakill)  \033[1;33m[T]\033[0m Torso  \033[1;36m[R]\033[0m R-Arm (Disarm)  \033[1;36m[L]\033[0m L-Arm  \033[1;32m[K]\033[0m Legs");
            $display("\033[1;37m  HEXEN SKILL : \033[1;35m[1]\033[0m %-16s  \033[1;35m[2]\033[0m %-16s", sk1_name, sk2_name);
            $display("\033[1;37m  USE POUCH   : \033[1;31m[P]\033[0m Poppy (+HP)  \033[1;32m[M]\033[0m Weed (+HP)  \033[1;33m[B]\033[0m Bread (-Hng)  \033[1;34m[A]\033[0m Ale (+Mnd)");
            $display("\033[1;37m  TACTICS     : \033[1;36m[G]\033[0m Guard (-70%% DMG)  \033[1;33m[S]\033[0m Switch Hero  \033[1;31m[F]\033[0m Flee (50%%)");
            $display("\033[1;36m====================================================================================================\033[0m");
        end
    endtask

    // ------------------------------------------------------------------------
    // 8. Game Over Screen (Based on new game over.txt)
    // ------------------------------------------------------------------------
    task render_game_over_screen;
        begin
            $write("\033[2J\033[H");
            $display("\033[1;31m====================================================================================================\033[0m");
            $display("\033[1;31m   ________  ________  _____ ______   _______           ________  ___      ___ _______   ________     \033[0m");
            $display("\033[1;31m  |\\   ____\\|\\   __  \\|\\   _ \\  _   \\|\\  ___ \\         |\\   __  \\|\\  \\    /  /|\\  ___ \\ |\\   __  \\    \033[0m");
            $display("\033[1;31m  \\ \\  \\___|\\ \\  \\|\\  \\ \\  \\\\\\__\\ \\  \\ \\   __/|        \\ \\  \\|\\  \\ \\  \\  /  / | \\   __/|\\ \\  \\|\\  \\   \033[0m");
            $display("\033[1;31m   \\ \\  \\  __\\ \\   __  \\ \\  \\\\|__| \\  \\ \\  \\_|/__       \\ \\  \\\\\\  \\ \\  \\/  / / \\ \\  \\_|/_\\ \\   _  _\\  \033[0m");
            $display("\033[1;31m    \\ \\  \\|\\  \\ \\  \\ \\  \\ \\  \\    \\ \\  \\ \\  \\_|\\ \\       \\ \\  \\\\\\  \\ \\    / /   \\ \\  \\_|\\ \\ \\  \\\\  \\| \033[0m");
            $display("\033[1;31m     \\ \\_______\\ \\__\\ \\__\\ \\__\\    \\ \\__\\ \\_______\\       \\ \\_______\\ \\__/ /     \\ \\_______\\ \\__\\\\ _\\ \033[0m");
            $display("\033[1;31m      \\|_______|\\|__|\\|__|\\|__|     \\|__|\\|_______|        \\|_______|\\|__|/       \\|_______|\\|__|\\|__|\033[0m");
            $display("\033[1;31m====================================================================================================\033[0m");
            $display("\033[1;37m+====================================================================================================+\033[0m");
            $display("\033[1;37m|  YOUR ENTIRE SQUAD HAS FALLEN TO THE LABYRINTH HORRORS... YOUR BONES ROT IN THE DARKNESS.         |\033[0m");
            $display("\033[1;37m+====================================================================================================+\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // 9. Victory Screen (Grand Escape Banner)
    // ------------------------------------------------------------------------
    task render_victory_screen;
        begin
            $write("\033[2J\033[H");
            $display("\033[1;33m====================================================================================================\033[0m");
            $display("\033[1;33m   ___      ___ ___  ________  _________  ________  ________      ___    ___ \033[0m");
            $display("\033[1;33m  |\\  \\    /  /|\\  \\|\\   ____\\|\\___   ___\\\\   __  \\|\\   __  \\    |\\  \\  /  /|\033[0m");
            $display("\033[1;33m  \\ \\  \\  /  / | \\  \\ \\  \\___|\\|___ \\  \\_\\ \\  \\|\\  \\ \\  \\|\\  \\   \\ \\  \\/  / /\033[0m");
            $display("\033[1;33m   \\ \\  \\/  / / \\ \\  \\ \\  \\        \\ \\  \\ \\ \\  \\\\\\  \\ \\   _  _\\   \\ \\    / / \033[0m");
            $display("\033[1;33m    \\ \\    / /   \\ \\  \\ \\  \\____    \\ \\  \\ \\ \\  \\\\\\  \\ \\  \\\\  \\|   \\/  /  /  \033[0m");
            $display("\033[1;33m     \\ \\__/ /     \\ \\__\\ \\_______\\   \\ \\__\\ \\ \\_______\\ \\__\\\\ _\\   __/  / /   \033[0m");
            $display("\033[1;33m      \\|__|/       \\|__|\\|_______|    \\|__|  \\|_______|\\|__|\\|__| |\\___/ /    \033[0m");
            $display("\033[1;33m                                                                  \\|___|/     \033[0m");
            $display("\033[1;32m                      [ E S C A P E   A C H I E V E D   -   V I C T O R Y ]                       \033[0m");
            $display("\033[1;33m====================================================================================================\033[0m");
            $display("\033[1;36m+====================================================================================================+\033[0m");
            $display("\033[1;36m|  \033[1;33mALL 3 RUNIC KEYS INSERTED!\033[1;37m THE RUNIC GATES GRIND OPEN AS GOLDEN LIGHT FLOODS THE DARKNESS!        \033[1;36m|\033[0m");
            $display("\033[1;36m|  \033[1;32mYou and your surviving companions have triumphed over the horrors and conquered the Labyrinth!   \033[1;36m|\033[0m");
            $display("\033[1;36m+====================================================================================================+\033[0m\n");
        end
    endtask

endmodule
