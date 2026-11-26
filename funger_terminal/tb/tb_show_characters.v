// ============================================================================
// Testbench: tb_show_characters.v
// Dedicated Character Encyclopedia & TrueColor Pixel Art Viewer
// Displays all 8 Playable Heroes with 24-bit ANSI Half-Block Sprites,
// Combat Stats for both Modes (Fear & Hunger vs Terror & Starvation),
// Unique Skills, Tactical Roles, and Master Summary Table.
// ============================================================================

`timescale 1ns / 1ps

module tb_show_characters;

    // Submodules
    character_rom u_char_rom(.char_id(4'd1), .is_hard_mode(1'b0), .char_hp(), .char_atk(), .char_def(), .char_name(), .char_class());
    sprite_router u_router();

    // ------------------------------------------------------------------------
    // Half-block ANSI pixel printer
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
    // Health bar printer
    // ------------------------------------------------------------------------
    task print_health_bar;
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
            for (j = 0; j < filled; j = j + 1) begin
                $write("\033[38;2;255;65;85m\342\226\210\033[0m");
            end
            for (j = filled; j < bar_len; j = j + 1) begin
                $write("\033[38;2;70;70;70m\342\226\221\033[0m");
            end
            $write("\033[1;37m]\033[0m");
        end
    endtask

    // ------------------------------------------------------------------------
    // Render 1 Playable Hero Card
    // ------------------------------------------------------------------------
    task display_hero_card;
        input [3:0] cid;
        integer lp, c;
        integer pw, ph;
        reg [7:0]   hp, atk_norm, def_norm;
        reg [7:0]   hp_hard, atk_hard, def_hard;
        reg [255:0] name, role;
        reg         pt, pb;
        reg [23:0]  pt_rgb, pb_rgb;
        begin
            u_char_rom.get_character(cid, 1'b0, hp, atk_norm, def_norm, name, role);
            u_char_rom.get_character(cid, 1'b1, hp_hard, atk_hard, def_hard, name, role);
            u_router.get_funger_dim(cid, pw, ph);

            // Render 14 half-block lines (= 28 pixel rows)
            for (lp = 0; lp < 14; lp = lp + 1) begin
                // Left Column: Sprite Canvas (28 characters wide)
                for (c = 0; c < 28; c = c + 1) begin
                    if (c < pw && lp * 2 < ph) begin
                        u_router.sample_funger_pixel(cid, lp*2, lp*2+1, c, 1'b0, pt, pt_rgb, pb, pb_rgb);
                        print_hb_pixel(pt, pt_rgb[23:16], pt_rgb[15:8], pt_rgb[7:0],
                                       pb, pb_rgb[23:16], pb_rgb[15:8], pb_rgb[7:0]);
                    end else begin
                        $write(" ");
                    end
                end

                // Middle Divider
                $write(" \033[1;30m|\033[0m ");

                // Right Column: Detailed Stat & Profile Box
                case (lp)
                    0:  $write("\033[1;36m+==============================================================================+\033[0m");
                    1:  begin
                            $write("\033[1;36m| \033[1;33mEXPEDITION HERO #%0d : %-20s\033[0m \033[1;37m[%2dx%2d TrueColor 24-bit Pixel Art]\033[0m \033[1;36m|\033[0m", cid, name, pw, ph);
                        end
                    2:  begin
                            $write("\033[1;36m| Archetype : \033[1;32m%-64s\033[1;36m |\033[0m", role);
                        end
                    3:  $write("\033[1;36m+------------------------------------------------------------------------------+\033[0m");
                    4:  begin
                            $write("\033[1;36m| \033[1;35mBase Vitality : \033[1;37m%3d HP\033[0m  ", hp_hard);
                            print_health_bar(hp_hard, 8'd160, 16);
                            $write("   \033[90m(Tank Tier: %s)\033[1;36m         |\033[0m", hp_hard >= 140 ? "Heavy Heavy" : (hp_hard >= 115 ? "Solid Tier " : "Glass Light"));
                        end
                    5:  begin
                            $write("\033[1;36m| \033[1;32mNormal (F&H) : %3d HP | %2d ATK | %2d DEF\033[0m  \033[90m(+25%% HP, +50%% ATK/DEF Boost)\033[1;36m   |\033[0m", hp, atk_norm, def_norm);
                        end
                    6:  begin
                            $write("\033[1;36m| \033[1;31mHard   (T&S) : %3d HP | %2d ATK | %2d DEF\033[0m  \033[90m(Classic 1.0x Baseline Stats)   \033[1;36m|\033[0m", hp_hard, atk_hard, def_hard);
                        end
                    7:  $write("\033[1;36m+------------------------------------------------------------------------------+\033[0m");
                    8:  begin
                            case (cid)
                                4'd1: $write("\033[1;36m| \033[1;37mCombat Skill  : Swift Dual Wielding - High agility strike & fast parry.      \033[1;36m|\033[0m");
                                4'd2: $write("\033[1;36m| \033[1;37mCombat Skill  : Holy Shield Guard - 75%% physical DEF mitigation barrier.      \033[1;36m|\033[0m");
                                4'd3: $write("\033[1;36m| \033[1;37mCombat Skill  : Black Orb & Necromancy - Soul tearing occult sorcery.         \033[1;36m|\033[0m");
                                4'd4: $write("\033[1;36m| \033[1;37mCombat Skill  : Berserk War Cry - Devastating axe cleaves; highest HP pool.   \033[1;36m|\033[0m");
                                4'd5: $write("\033[1;36m| \033[1;37mCombat Skill  : Leg Sweep - Forces Crawling (pins enemy for 100%% Head Hit).  \033[1;36m|\033[0m");
                                4'd6: $write("\033[1;36m| \033[1;37mCombat Skill  : Primal Direhound Bite - High critical strike decapitation.   \033[1;36m|\033[0m");
                                4'd7: $write("\033[1;36m| \033[1;37mCombat Skill  : Innocent Ward - Supreme natural evasion (35%% base dodge rate).\033[1;36m|\033[0m");
                                4'd8: $write("\033[1;36m| \033[1;37mCombat Skill  : Flaming Skull of Doom - Game-highest ATK power (54 ATK max!). \033[1;36m|\033[0m");
                                default: $write("\033[1;36m| \033[1;37mCombat Skill  : Standard Expedition Exploration & Labyrinth Survival.        \033[1;36m|\033[0m");
                            endcase
                        end
                    9:  begin
                            case (cid)
                                4'd1: $write("\033[1;36m| \033[90mOrigin & Lore : Mercenary driven by survival instinct to escape the dungeon. \033[1;36m|\033[0m");
                                4'd2: $write("\033[1;36m| \033[90mOrigin & Lore : Pious Holy Knight of Rondon searching for her captain.      \033[1;36m|\033[0m");
                                4'd3: $write("\033[1;36m| \033[90mOrigin & Lore : Dark Priest pursuing forbidden alchemy and necromancy runes. \033[1;36m|\033[0m");
                                4'd4: $write("\033[1;36m| \033[90mOrigin & Lore : Northern Outlander seeking vengeance for his slaughtered clan.\033[1;36m|\033[0m");
                                4'd5: $write("\033[1;36m| \033[90mOrigin & Lore : Prophesied Commander of Midnight Sun seeking divine ascension.\033[1;36m|\033[0m");
                                4'd6: $write("\033[1;36m| \033[90mOrigin & Lore : Direhound native to subterranean ruins; loyal cave predator. \033[1;36m|\033[0m");
                                4'd7: $write("\033[1;36m| \033[90mOrigin & Lore : Silent innocent child sheltered in the damp dungeon crypts.  \033[1;36m|\033[0m");
                                4'd8: $write("\033[1;36m| \033[90mOrigin & Lore : Severed head of ancient arch-mage; speaks with burning wrath. \033[1;36m|\033[0m");
                                default: $write("\033[1;36m| \033[90mOrigin & Lore : An explorer braving the ancient labyrinth vault.             \033[1;36m|\033[0m");
                            endcase
                        end
                    10: begin
                            case (cid)
                                4'd1: $write("\033[1;36m| \033[1;33mRole in Squad : Scout-Walker (ideal lead explorer to absorb hunger drain).   \033[1;36m|\033[0m");
                                4'd2: $write("\033[1;36m| \033[1;33mRole in Squad : Primary Tank (Iron Guard Stance user, absorbs boss hits).     \033[1;36m|\033[0m");
                                4'd3: $write("\033[1;36m| \033[1;33mRole in Squad : Occult Backline Nuker (destroys elite torso & limbs quickly).  \033[1;36m|\033[0m");
                                4'd4: $write("\033[1;36m| \033[1;33mRole in Squad : Frontline Bruiser (highest health reserve, executes bosses). \033[1;36m|\033[0m");
                                4'd5: $write("\033[1;36m| \033[1;33mRole in Squad : Tactical Enabler (Leg Sweep guarantees 100%% decapitations).   \033[1;36m|\033[0m");
                                4'd6: $write("\033[1;36m| \033[1;33mRole in Squad : Flanker Beast (high critical strikes against fleeing foes).    \033[1;36m|\033[0m");
                                4'd7: $write("\033[1;36m| \033[1;33mRole in Squad : Evasive Dodge Tank (absorbs enemy attacks with zero damage).   \033[1;36m|\033[0m");
                                4'd8: $write("\033[1;36m| \033[1;33mRole in Squad : Pure Demolition (one-shots most dungeon foes in turn 1).      \033[1;36m|\033[0m");
                                default: $write("\033[1;36m| \033[1;33mRole in Squad : Squad Member.                                                \033[1;36m|\033[0m");
                            endcase
                        end
                    11: $write("\033[1;36m+==============================================================================+\033[0m");
                    default: $write("                                                                                ");
                endcase
                $write("\n");
            end
            $display("\033[1;30m----------------------------------------------------------------------------------------------------------------\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // Master Summary Table
    // ------------------------------------------------------------------------
    task display_summary_table;
        integer i;
        reg [7:0]   hp, atk_n, def_n;
        reg [7:0]   hp_h, atk_h, def_h;
        reg [255:0] nm, cl;
        begin
            $display("\033[1;37m+==============================================================================================================+\033[0m");
            $display("\033[1;37m|       FEAR & HUNGER: HARDWARE ENGINE - MASTER COMPARATIVE CHARACTER MATRIX (8 PLAYABLE HEROES)               |\033[0m");
            $display("\033[1;37m+=====+======================+=========================+=========+=============+=============+===================+\033[0m");
            $display("\033[1;37m| ID  | Hero Name            | Class Archetype         | Base HP | Normal(F&H) | Hard(T&S)   | Tactical Special  |\033[0m");
            $display("\033[1;37m|     |                      |                         |         | ATK  /  DEF | ATK  /  DEF |                   |\033[0m");
            $display("\033[1;37m+-----+----------------------+-------------------------+---------+-------------+-------------+-------------------+\033[0m");

            for (i = 1; i <= 8; i = i + 1) begin
                u_char_rom.get_character(i[3:0], 1'b0, hp, atk_n, def_n, nm, cl);
                u_char_rom.get_character(i[3:0], 1'b1, hp_h, atk_h, def_h, nm, cl);

                $write("| #%0d  | \033[1;33m%-20s\033[0m | %-23s |   %3d   |   \033[1;32m%2d / %2d\033[0m   |   \033[1;31m%2d / %2d\033[0m   | ",
                       i, nm, cl, hp_h, atk_n, def_n, atk_h, def_h);

                case (i)
                    1: $display("Scout / Quick Parry |");
                    2: $display("Holy Tank (75%% Cut) |");
                    3: $display("Black Orb Sorcery   |");
                    4: $display("Colossal Berserk HP |");
                    5: $display("Leg Sweep (100%% Hit)|");
                    6: $display("Direhound Crit Bite |");
                    7: $display("35%% Natural Evasion |");
                    8: $display("Max ATK (54 Power)  |");
                    default: $display("Explorer            |");
                endcase
            end
            $display("\033[1;37m+-----+----------------------+-------------------------+---------+-------------+-------------+-------------------+\033[0m");
            $display("\033[1;32m[HARDWARE PROFILE]: Synthesizable ROM, 24-bit RGB TrueColor stream, 0 hardware division operators.\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // Main Simulation Process
    // ------------------------------------------------------------------------
    integer i;

    initial begin
        $display("\033[2J\033[H");
        $display("\033[1;31m================================================================================================================\033[0m");
        $display("\033[1;31m              FEAR & HUNGER: TERMINAL LABYRINTH - PLAYABLE CHARACTER ENCYCLOPEDIA               \033[0m");
        $display("\033[1;31m================================================================================================================\033[0m");
        $display("\033[1;33m  Visualizing all 8 Playable Heroes with TrueColor 24-bit Sprites, Dual-Mode Scaling & Tactical Stats          \033[0m");
        $display("\033[1;31m================================================================================================================\033[0m\n");

        for (i = 1; i <= 8; i = i + 1) begin
            display_hero_card(i[3:0]);
        end

        display_summary_table();

        $display("\033[1;32m>>> ALL 8 CHARACTER MODELS & DUAL-MODE PROFILES RENDERED SUCCESSFULLY! <<<\033[0m\n");
        $finish;
    end

endmodule
