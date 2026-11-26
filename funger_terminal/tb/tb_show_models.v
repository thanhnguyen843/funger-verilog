// ============================================================================
// Testbench: tb_show_models.v
// Complete Model & Bestiary Encyclopedia Viewer for Fear & Hunger: Terminal
// Displays all 8 Playable Heroes, 20 Retro Monsters, 16 Fantasy Horrors,
// and Vault Relics with TrueColor Pixel Art Sprites & Full Combat Stats.
// ============================================================================

`timescale 1ns / 1ps

module tb_show_models;

    // Databases & Submodules
    character_rom u_char_rom(.char_id(4'd1), .is_hard_mode(1'b0), .char_hp(), .char_atk(), .char_def(), .char_name(), .char_class());
    monster_rom   u_mon_rom(.monster_id(6'd1), .is_elite(1'b0), .base_hp(), .base_atk(), .base_def(), .spawn_weight(), .is_default_elite());
    sprite_router u_router();

    // Chest Sprite ROM instances
    reg  [5:0]  c_r_t, c_c_t, c_r_b, c_c_b;
    wire [23:0] c_rgb_t, c_rgb_b;
    wire        c_trans_t, c_trans_b;
    chest_sprite_rom u_chest_t (.row(c_r_t), .col(c_c_t), .color_rgb(c_rgb_t), .is_transparent(c_trans_t));
    chest_sprite_rom u_chest_b (.row(c_r_b), .col(c_c_b), .color_rgb(c_rgb_b), .is_transparent(c_trans_b));

    // Key Sprite ROM instances
    reg  [5:0]  k_r_t, k_c_t, k_r_b, k_c_b;
    wire [23:0] k_rgb_t, k_rgb_b;
    wire        k_trans_t, k_trans_b;
    key_sprite_rom u_key_t (.row(k_r_t), .col(k_c_t), .color_rgb(k_rgb_t), .is_transparent(k_trans_t));
    key_sprite_rom u_key_b (.row(k_r_b), .col(k_c_b), .color_rgb(k_rgb_b), .is_transparent(k_trans_b));

    // Healing Items ROM instances (mapped to 20x20 hardware sprite_rom)
    reg  [5:0]  hb_r_t, hb_c_t, hb_r_b, hb_c_b;
    wire        hb_pix_t, hb_pix_b;
    sprite_rom u_herb_t   (.sprite_id(3'd5), .x(hb_c_t[4:0]), .y(hb_r_t[4:0]), .pixel_out(hb_pix_t));
    sprite_rom u_herb_b   (.sprite_id(3'd5), .x(hb_c_b[4:0]), .y(hb_r_b[4:0]), .pixel_out(hb_pix_b));

    reg  [5:0]  fl_r_t, fl_c_t, fl_r_b, fl_c_b;
    wire        fl_pix_t, fl_pix_b;
    sprite_rom u_flower_t (.sprite_id(3'd3), .x(fl_c_t[4:0]), .y(fl_r_t[4:0]), .pixel_out(fl_pix_t));
    sprite_rom u_flower_b (.sprite_id(3'd3), .x(fl_c_b[4:0]), .y(fl_r_b[4:0]), .pixel_out(fl_pix_b));

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
    // Pink health bar printer
    // ------------------------------------------------------------------------
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
            for (j = 0; j < filled; j = j + 1) begin
                $write("\033[48;2;255;105;180m \033[0m");
            end
            for (j = filled; j < bar_len; j = j + 1) begin
                $write("\033[48;2;50;50;50m \033[0m");
            end
            $write("\033[1;37m]\033[0m");
        end
    endtask

    // ------------------------------------------------------------------------
    // Helper task to get Monster Lore & Behavior
    // ------------------------------------------------------------------------
    task get_monster_lore;
        input  [5:0]   mid;
        output [300:0] line1;
        output [300:0] line2;
        begin
            case (mid)
                6'd1:  begin line1 = "Ethereal spirit wielding ancient occult sorcery."; line2 = "Channels astral bolts that bypass physical defenses."; end
                6'd2:  begin line1 = "Restless spectral phantom roaming forgotten crypts."; line2 = "Phases through obstacles; inflicts chilly terror."; end
                6'd3:  begin line1 = "Caustic gelatinous ooze with an insatiable hunger."; line2 = "High defensive resilience; dissolves steel equipment."; end
                6'd4:  begin line1 = "[ELITE] Enormous prehistoric titan of brutal force."; line2 = "Devastating stomp attacks; crushes reckless explorers."; end
                6'd5:  begin line1 = "Ritual wooden totem possessed by hostile forest animas."; line2 = "Channels earthy warding spells and heavy bludgeoning."; end
                6'd6:  begin line1 = "Aquatic tentacled horror from flooded lower depths."; line2 = "Constricts targets with multiple suckered limbs."; end
                6'd7:  begin line1 = "Levitating all-seeing ocular horror from the void."; line2 = "Projects psychic beams that weaken mind and resolve."; end
                6'd8:  begin line1 = "Cursed phantom blade master bound to endless patrol."; line2 = "Delivers lightning-fast decapitation sword techniques."; end
                6'd9:  begin line1 = "Heavily armored molluscan colossus with stone shell."; line2 = "Near-impenetrable natural defense; slow but persistent."; end
                6'd10: begin line1 = "Eight-legged subterranean hunter lurking in darkness."; line2 = "Spins paralytic web strands and injects virulent venom."; end
                6'd11: begin line1 = "Subterranean colonial burrower with chitinous armor."; line2 = "Swarming mandibles capable of crushing solid stone."; end
                6'd12: begin line1 = "Battle-hardened pack beast trained for dark skirmishes."; line2 = "Aggressive spitting and heavy hooved kicks."; end
                6'd13: begin line1 = "Nightmarish canine moving silently through shadows."; line2 = "High agility striker that ambushes vulnerable targets."; end
                6'd14: begin line1 = "Necrotic woodland deity wandering subterranean ruins."; line2 = "Charges with razor antlers; retains unearthly agility."; end
                6'd15: begin line1 = "Vindictive underground dweller hurling poisoned rocks."; line2 = "Nimble and erratic; difficult to land clean strikes on."; end
                6'd16: begin line1 = "Miniature clockwork automaton in polished vintage brass."; line2 = "Relentless mechanical precision and reinforced plating."; end
                6'd17: begin line1 = "Juvenile dragon whelp harboring searing dragonfire."; line2 = "Breathes caustic embers that ignite combustible items."; end
                6'd18: begin line1 = "Toxic necrotic slug leaving thick corrosive slime."; line2 = "Absorbs physical impacts; retaliates with venom acid."; end
                6'd19: begin line1 = "[ELITE] Colossal ancient construct powered by soul core."; line2 = "Supreme plate armor; pulverizes invaders with iron fists."; end
                6'd20: begin line1 = "[ELITE] Sovereign terror of the deepest void abyss."; line2 = "Highest attack power among retro foes; commands death."; end

                6'd21: begin line1 = "Winged draconic predator descending from cave ceilings."; line2 = "Swoops with razor talons; commands aerial initiative."; end
                6'd22: begin line1 = "Stone sentinel animated by cathedral necromancy."; line2 = "Rock-solid natural carapace; resistant to slashing damage."; end
                6'd23: begin line1 = "[CHEST TRAP] Predatory horror disguised as ancient chest."; line2 = "20% ambush when opening chests; NEVER spawns in 'M' tiles."; end
                6'd24: begin line1 = "[ELITE] Multi-headed serpent that regenerates vital flesh."; line2 = "Multiple biting heads strike sequentially with venom."; end
                6'd25: begin line1 = "Mischievous infernal demon conjuring brimstone bursts."; line2 = "Flits across battlefields while hurling searing hexes."; end
                6'd26: begin line1 = "Apparition predator flickering between void and flesh."; line2 = "Difficult to predict; phases past standard parries."; end
                6'd27: begin line1 = "Sentient subterranean tree giant rooted in damp catacombs."; line2 = "Massive endurance and crushing root lash attacks."; end
                6'd28: begin line1 = "Floating aberration with multiple occult eyestalks."; line2 = "Unleashes concentrated arcane lasers from each eye."; end
                6'd29: begin line1 = "[ELITE] Living monolith sculpted from enchanted granite."; line2 = "Highest physical defense in the labyrinth; unstoppable."; end
                6'd30: begin line1 = "[ELITE] Radiant hybrid beast breathing intense solar fire."; line2 = "Blinds opponents with solar flares; ferocious claws."; end
                6'd31: begin line1 = "Serpentine naga enchantress from sunken temple vaults."; line2 = "Strikes with coiled tail and piercing tridents."; end
                6'd32: begin line1 = "Fallen celestial steed corrupted by subterranean curse."; line2 = "Pierces armor with its spiral horn of celestial energy."; end
                6'd33: begin line1 = "[ELITE] Cosmic serpent devouring its own tail in cyclic fury."; line2 = "Possesses profound vitality and relentless bite power."; end
                6'd34: begin line1 = "Jackal-headed death guardian wielding an obsidian scythe."; line2 = "Judges souls with precise lethal sweeping strikes."; end
                6'd35: begin line1 = "[ELITE] Immortal firebird engulfed in eternal flames."; line2 = "Massive attack power; burns away enemy defensive guards."; end
                6'd36: begin line1 = "[ELITE] Apex Eldritch God whose presence shatters reality."; line2 = "Highest stats in the game (HP: 204 | ATK: 36 | DEF: 26)."; end
                default: begin line1 = "Uncharted entity roaming the subterranean depths."; line2 = "Dangerous and unpredictable behavior."; end
            endcase
        end
    endtask

    // ------------------------------------------------------------------------
    // Render 1 Playable Hero Card
    // ------------------------------------------------------------------------
    task display_hero_card;
        input [3:0] cid;
        integer lp, c;
        integer pw, ph;
        reg [7:0]   hp, atk, def;
        reg [7:0]   atk_ts, def_ts;
        reg [255:0] name, role;
        reg         pt, pb;
        reg [23:0]  pt_rgb, pb_rgb;
        integer     avg_stat;
        begin
            u_char_rom.get_character(cid, 1'b0, hp, atk, def, name, role);
            u_char_rom.get_character(cid, 1'b1, hp, atk_ts, def_ts, name, role);
            u_router.get_funger_dim(cid, pw, ph);
            avg_stat = (hp + atk + def) / 3;

            // Render 14 half-block lines (= 28 pixel rows)
            for (lp = 0; lp < 14; lp = lp + 1) begin
                // Left: Sprite Canvas (28 characters wide)
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

                // Right: Detailed Stat & Profile Box
                case (lp)
                    0:  $write("\033[1;36m+========================================================================+\033[0m");
                    1:  begin
                            $write("\033[1;36m| \033[1;33mHERO #%0d : %-20s\033[0m \033[1;37m[%2dx%2d TrueColor 24-bit Sprite]\033[0m \033[1;36m|\033[0m", cid, name, pw, ph);
                        end
                    2:  begin
                            $write("\033[1;36m| Archetype : \033[1;32m%-58s\033[1;36m |\033[0m", role);
                        end
                    3:  $write("\033[1;36m+------------------------------------------------------------------------+\033[0m");
                    4:  begin
                            $write("\033[1;36m| \033[1;35mBase Vitality : \033[1;37m%3d HP\033[0m  ", hp);
                            print_pink_health_bar(hp, 8'd150, 16);
                            $write("   \033[90m(Tank Tier: %s)\033[1;36m |\033[0m", hp >= 120 ? "Heavy" : (hp >= 100 ? "Solid" : "Light"));
                        end
                    5:  begin
                            $write("\033[1;36m| \033[1;32mF&H Normal : %2d ATK / %2d DEF\033[0m | \033[1;31mT&S Hardcore : %2d ATK / %2d DEF\033[0m       \033[1;36m|\033[0m", atk, def, atk_ts, def_ts);
                        end
                    6:  $write("\033[1;36m+------------------------------------------------------------------------+\033[0m");
                    7:  begin
                            case (cid)
                                4'd1: $write("\033[1;36m| \033[1;37mSkill : Agile dual-wielding swordsman with quick reflexive parries.    \033[1;36m|\033[0m");
                                4'd2: $write("\033[1;36m| \033[1;37mSkill : Heavy plate armor absorbs brutal blows; high defense guardian. \033[1;36m|\033[0m");
                                4'd3: $write("\033[1;36m| \033[1;37mSkill : Ancient occult curses tear enemy souls; fragile glass cannon.  \033[1;36m|\033[0m");
                                4'd4: $write("\033[1;36m| \033[1;37mSkill : Colossal stamina & berserker axes; highest raw HP in party.   \033[1;36m|\033[0m");
                                4'd5: $write("\033[1;36m| \033[1;37mSkill : Flawless military swordsmanship; well-rounded master tactician. \033[1;36m|\033[0m");
                                4'd6: $write("\033[1;36m| \033[1;37mSkill : Swift cave predator with vicious critical bite strikes.        \033[1;36m|\033[0m");
                                4'd7: $write("\033[1;36m| \033[1;37mSkill : Enigmatic child ward; supreme natural evasion and defense.     \033[1;36m|\033[0m");
                                4'd8: $write("\033[1;36m| \033[1;37mSkill : Decapitated burning doom wizard; game-highest ATK power (51).   \033[1;36m|\033[0m");
                                default: $write("\033[1;36m| \033[1;37mStandard expedition wanderer exploring the dark catacombs.             \033[1;36m|\033[0m");
                            endcase
                        end
                    8:  begin
                            case (cid)
                                4'd1: $write("\033[1;36m| \033[90mLore  : Mercenary driven by survival instinct to escape the dungeon.   \033[1;36m|\033[0m");
                                4'd2: $write("\033[1;36m| \033[90mLore  : Pious Holy Knight of Rondon searching for her captured captain.\033[1;36m|\033[0m");
                                4'd3: $write("\033[1;36m| \033[90mLore  : Dark Priest pursuing forbidden necromancy and forgotten runes. \033[1;36m|\033[0m");
                                4'd4: $write("\033[1;36m| \033[90mLore  : Northern Outlander seeking vengeance for his slaughtered clan. \033[1;36m|\033[0m");
                                4'd5: $write("\033[1;36m| \033[90mLore  : Prophesied leader of the Midnight Sun seeking divine ascent.   \033[1;36m|\033[0m");
                                4'd6: $write("\033[1;36m| \033[90mLore  : Direhound native to the subterranean ruins; fiercely loyal.    \033[1;36m|\033[0m");
                                4'd7: $write("\033[1;36m| \033[90mLore  : Silent innocent soul sheltered in the damp catacombs.          \033[1;36m|\033[0m");
                                4'd8: $write("\033[1;36m| \033[90mLore  : Ancient arch-mage of pure malice; speaks with burning wrath.   \033[1;36m|\033[0m");
                                default: $write("\033[1;36m| \033[90mLore  : An explorer seeking the ancient relic vault.                   \033[1;36m|\033[0m");
                            endcase
                        end
                    9:  $write("\033[1;36m+========================================================================+\033[0m");
                    default: $write("                                                                          ");
                endcase
                $write("\n");
            end
            $display("\033[1;30m--------------------------------------------------------------------------------------------------------\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // Render 1 Monster / Creature Card
    // ------------------------------------------------------------------------
    task display_monster_card;
        input [5:0] mid;
        integer lp, c;
        integer mw, mh;
        reg [7:0]   nhp, natk, ndef, weight;
        reg [7:0]   ehp, eatk, edef;
        reg         def_elite, dummy_el;
        reg         pt, pb;
        reg [23:0]  pt_rgb, pb_rgb;
        reg [300:0] lore1, lore2;
        begin
            u_mon_rom.get_monster(mid, 1'b0, nhp, natk, ndef, weight, def_elite);
            u_mon_rom.get_monster(mid, 1'b1, ehp, eatk, edef, weight, dummy_el);
            u_router.get_monster_dim(mid, mw, mh);
            get_monster_lore(mid, lore1, lore2);

            // 13 half-block lines (= 26 pixel rows)
            for (lp = 0; lp < 13; lp = lp + 1) begin
                // Left: Monster Sprite Canvas (28 chars wide)
                for (c = 0; c < 28; c = c + 1) begin
                    if (c < mw && lp * 2 < mh) begin
                        u_router.sample_monster_pixel(mid, lp*2, lp*2+1, c, pt, pt_rgb, pb, pb_rgb);
                        print_hb_pixel(pt, pt_rgb[23:16], pt_rgb[15:8], pt_rgb[7:0],
                                       pb, pb_rgb[23:16], pb_rgb[15:8], pb_rgb[7:0]);
                    end else begin
                        $write(" ");
                    end
                end

                // Middle Divider
                $write(" \033[1;30m|\033[0m ");

                // Right: Detailed Monster Information
                case (lp)
                    0:  begin
                            if (mid == 6'd23)
                                $write("\033[1;31m+========================================================================+\033[0m");
                            else if (def_elite)
                                $write("\033[1;35m+========================================================================+\033[0m");
                            else
                                $write("\033[1;34m+========================================================================+\033[0m");
                        end
                    1:  begin
                            if (mid == 6'd23)
                                $write("\033[1;31m| \033[41;1;37m[CHEST TRAP]\033[0m \033[1;33m#%02d MIMIC (Chest Horror)\033[0m \033[1;37m[%2dx%2d 1-Bit Phosphor Art]\033[0m \033[1;31m|\033[0m", mid, mw, mh);
                            else if (def_elite)
                                $write("\033[1;35m| \033[45;1;37m[ELITE APEX]\033[0m \033[1;33m#%02d ", mid);
                            else
                                $write("\033[1;34m| \033[42;1;30m[STANDARD]\033[0m   \033[1;33m#%02d ", mid);

                            if (mid != 6'd23) begin
                                u_mon_rom.print_monster_name(mid);
                                $write("\033[0m \033[1;37m[%2dx%2d 1-Bit Phosphor Art]\033[0m", mw, mh);
                                if (def_elite) $write(" \033[1;35m|\033[0m");
                                else           $write(" \033[1;34m|\033[0m");
                            end
                        end
                    2:  begin
                            if (mid == 6'd23)
                                $write("\033[1;31m| Classification : \033[1;31mChest Ambush (20%% chance on 'C', 0%% in 'M' corridor) |\033[0m");
                            else if (def_elite)
                                $write("\033[1;35m| Classification : \033[1;35mRare Elite Adversary (Spawn Weight: %0d / 138)             |\033[0m", weight);
                            else
                                $write("\033[1;34m| Classification : \033[1;32mCommon Labyrinth Foe (Spawn Weight: %0d / 138)             |\033[0m", weight);
                        end
                    3:  begin
                            if (mid == 6'd23) $write("\033[1;31m+------------------------------------------------------------------------+\033[0m");
                            else if (def_elite) $write("\033[1;35m+------------------------------------------------------------------------+\033[0m");
                            else $write("\033[1;34m+------------------------------------------------------------------------+\033[0m");
                        end
                    4:  begin
                            $write("| \033[1;37mStandard Form :\033[0m HP:%3d | ATK:%2d | DEF:%2d  ", nhp, natk, ndef);
                            print_pink_health_bar(nhp, 8'd204, 14);
                            $write("          |");
                        end
                    5:  begin
                            if (mid == 6'd23)
                                $write("| \033[90mElite Variant : N/A (Mimics never spawn as Elite monsters)             \033[0m|");
                            else
                                $write("| \033[1;35mElite Variant : HP:%3d | ATK:%2d | DEF:%2d (+20%% Stats Boost)              \033[0m|", ehp, eatk, edef);
                        end
                    6:  begin
                            if (mid == 6'd23)
                                $write("| \033[1;33mLoot Drops    : 20%% Key Drop  |  Poppy / Medicinal Chest Bounty        \033[0m|");
                            else if (def_elite)
                                $write("| \033[1;33mLoot Drops    : 50%% Dungeon Key Drop  |  20%% Healing Poppy Flower      \033[0m|");
                            else
                                $write("| \033[1;37mLoot Drops    : 20%% Dungeon Key Drop  |  No other items dropped        \033[0m|");
                        end
                    7:  begin
                            if (mid == 6'd23) $write("\033[1;31m+------------------------------------------------------------------------+\033[0m");
                            else if (def_elite) $write("\033[1;35m+------------------------------------------------------------------------+\033[0m");
                            else $write("\033[1;34m+------------------------------------------------------------------------+\033[0m");
                        end
                    8:  $write("| \033[1;37m%-70s\033[0m |", lore1);
                    9:  $write("| \033[90m%-70s\033[0m |", lore2);
                    10: begin
                            if (mid == 6'd23)
                                $write("\033[1;31m+========================================================================+\033[0m");
                            else if (def_elite)
                                $write("\033[1;35m+========================================================================+\033[0m");
                            else
                                $write("\033[1;34m+========================================================================+\033[0m");
                        end
                    default: $write("                                                                          ");
                endcase
                $write("\n");
            end
            $display("\033[1;30m--------------------------------------------------------------------------------------------------------\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // Render Section 4: Vault Relics & Interactive Items
    // ------------------------------------------------------------------------
    task display_relics_section;
        integer lp, c;
        begin
            $display("\n\033[1;33m========================================================================================================\033[0m");
            $display("\033[1;33m   SECTION 4: INTERACTIVE RELICS & SURVIVAL INVENTORY SUPPLIES                                          \033[0m");
            $display("\033[1;33m========================================================================================================\033[0m\n");

            // --- 1. Ancient Treasure Chest (20x23 Pixels) ---
            $display("\033[1;33m>>> [RELIC 1] ANCIENT ORNATE CHEST (20x23 Pixels, TrueColor 24-bit)\033[0m");
            for (lp = 0; lp < 12; lp = lp + 1) begin
                c_r_t = lp * 2;
                c_r_b = lp * 2 + 1;
                for (c = 0; c < 28; c = c + 1) begin
                    if (c < 20 && lp * 2 < 23) begin
                        c_c_t = c; c_c_b = c; #1;
                        print_hb_pixel(c_trans_t, c_rgb_t[23:16], c_rgb_t[15:8], c_rgb_t[7:0],
                                       c_trans_b, c_rgb_b[23:16], c_rgb_b[15:8], c_rgb_b[7:0]);
                    end else begin
                        $write(" ");
                    end
                end
                $write(" \033[1;30m|\033[0m ");
                case (lp)
                    0: $write("\033[1;33m+========================================================================+\033[0m");
                    1: $write("\033[1;33m| MODEL: Ancient Gilded Vault Chest (Opened Variant)                     |\033[0m");
                    2: $write("\033[1;33m| Map Tile      : Brown Block with 'C' [\\033[48;2;139;69;19m C \\033[0m]              |\033[0m");
                    3: $write("\033[1;33m+------------------------------------------------------------------------+\033[0m");
                    4: $write("\033[1;37m| Interaction   : Full-Screen Chest Inspection upon entry                |\033[0m");
                    5: $write("\033[1;37m| 80%% Loot      : Uncovers Poppy (+50 HP), Medicinal (+120 HP), or Key   |\033[0m");
                    6: $write("\033[1;31m| 20%% Ambush    : Triggers instant combat with the vicious Mimic horror  |\033[0m");
                    7: $write("\033[1;33m+========================================================================+\033[0m");
                    default: $write("                                                                          ");
                endcase
                $write("\n");
            end
            $display("\033[1;30m--------------------------------------------------------------------------------------------------------\033[0m\n");

            // --- 2. Dungeon Key (11x22 Pixels) ---
            $display("\033[1;36m>>> [RELIC 2] DUNGEON RUNIC KEY (11x22 Pixels, TrueColor 24-bit)\033[0m");
            for (lp = 0; lp < 12; lp = lp + 1) begin
                k_r_t = lp * 2;
                k_r_b = lp * 2 + 1;
                for (c = 0; c < 28; c = c + 1) begin
                    if (c < 11 && lp * 2 < 22) begin
                        k_c_t = c; k_c_b = c; #1;
                        print_hb_pixel(k_trans_t, k_rgb_t[23:16], k_rgb_t[15:8], k_rgb_t[7:0],
                                       k_trans_b, k_rgb_b[23:16], k_rgb_b[15:8], k_rgb_b[7:0]);
                    end else begin
                        $write(" ");
                    end
                end
                $write(" \033[1;30m|\033[0m ");
                case (lp)
                    0: $write("\033[1;36m+========================================================================+\033[0m");
                    1: $write("\033[1;36m| MODEL: Labyrinth Runic Deadbolt Key                                    |\033[0m");
                    2: $write("\033[1;36m| Acquisition   : Defeat monsters (20%% normal / 50%% elite) or chests     |\033[0m");
                    3: $write("\033[1;36m+------------------------------------------------------------------------+\033[0m");
                    4: $write("\033[1;37m| Purpose       : Collect 3 Keys to unlock the Cyan Exit Portal 'G'      |\033[0m");
                    5: $write("\033[1;37m| Gate Position : Embedded permanently on the rightmost labyrinth wall   |\033[0m");
                    6: $write("\033[1;32m| Victory Cond. : Reaching Gate 'G' with 3 keys grants ultimate victory! |\033[0m");
                    7: $write("\033[1;36m+========================================================================+\033[0m");
                    default: $write("                                                                          ");
                endcase
                $write("\n");
            end
            $display("\033[1;30m--------------------------------------------------------------------------------------------------------\033[0m\n");

            // --- 3. Poppy Flower (20x20 Pixels) ---
            $display("\033[38;2;242;34;84m>>> [SUPPLY 1] CRIMSON POPPY FLOWER (20x20 Pixels, TrueColor 24-bit)\033[0m");
            for (lp = 0; lp < 10; lp = lp + 1) begin
                fl_r_t = lp * 2;
                fl_r_b = lp * 2 + 1;
                for (c = 0; c < 28; c = c + 1) begin
                    if (c < 20 && lp * 2 < 20) begin
                        fl_c_t = c; fl_c_b = c; #1;
                        print_hb_pixel(!fl_pix_t, 8'd242, 8'd34, 8'd84,
                                       !fl_pix_b, 8'd242, 8'd34, 8'd84);
                    end else begin
                        $write(" ");
                    end
                end
                $write(" \033[1;30m|\033[0m ");
                case (lp)
                    0: $write("\033[38;2;242;34;84m+========================================================================+\033[0m");
                    1: $write("\033[38;2;242;34;84m| ITEM: Crimson Poppy (Restorative Herb Flower)             |\033[0m");
                    2: $write("\033[1;37m| Starting Stock: 10x Poppy in Survival Pouch                            |\033[0m");
                    3: $write("\033[1;32m| Healing Effect: Restores +50 HP to any chosen party member             |\033[0m");
                    4: $write("\033[1;33m| Tactical Note : Using in combat consumes 1 turn (Enemy retaliates!)    |\033[0m");
                    5: $write("\033[38;2;242;34;84m+========================================================================+\033[0m");
                    default: $write("                                                                          ");
                endcase
                $write("\n");
            end
            $display("\033[1;30m--------------------------------------------------------------------------------------------------------\033[0m\n");

            // --- 4. Medicinal Herb (20x20 Pixels) ---
            $display("\033[38;2;105;225;101m>>> [SUPPLY 2] RESTORATIVE MEDICINAL HERB (20x20 Pixels, TrueColor 24-bit)\033[0m");
            for (lp = 0; lp < 10; lp = lp + 1) begin
                hb_r_t = lp * 2;
                hb_r_b = lp * 2 + 1;
                for (c = 0; c < 28; c = c + 1) begin
                    if (c < 20 && lp * 2 < 20) begin
                        hb_c_t = c; hb_c_b = c; #1;
                        print_hb_pixel(!hb_pix_t, 8'd105, 8'd225, 8'd101,
                                       !hb_pix_b, 8'd105, 8'd225, 8'd101);
                    end else begin
                        $write(" ");
                    end
                end
                $write(" \033[1;30m|\033[0m ");
                case (lp)
                    0: $write("\033[38;2;105;225;101m+========================================================================+\033[0m");
                    1: $write("\033[38;2;105;225;101m| ITEM: Restorative Medicinal (High-Grade Tonic Herb)     |\033[0m");
                    2: $write("\033[1;37m| Starting Stock: 3x Medicinal in Survival Pouch                         |\033[0m");
                    3: $write("\033[1;32m| Healing Effect: Restores +120 HP to any chosen party member            |\033[0m");
                    4: $write("\033[1;33m| Tactical Note : Powerful medicine for reviving critically injured allies|\033[0m");
                    5: $write("\033[38;2;105;225;101m+========================================================================+\033[0m");
                    default: $write("                                                                          ");
                endcase
                $write("\n");
            end
            $display("\033[1;30m--------------------------------------------------------------------------------------------------------\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // Print Summary Statistical Table
    // ------------------------------------------------------------------------
    task display_summary_table;
        integer i;
        reg [7:0]   hp, atk, def, w;
        reg [7:0]   atk_ts, def_ts;
        reg [255:0] nm, cl;
        reg         is_el;
        begin
            $display("\033[1;37m========================================================================================================\033[0m");
            $display("\033[1;37m   MASTER STATISTICAL OVERVIEW : 8 HEROES + 36 MONSTERS (44 TOTAL MODELS)                               \033[0m");
            $display("\033[1;37m========================================================================================================\033[0m");
            $display(" ID  | Type      | Name                     | HP  | F&H ATK/DEF | T&S ATK/DEF | Notes");
            $display("-----+-----------+--------------------------+-----+-------------+-------------+-----------------------------");

            // 8 Characters
            for (i = 1; i <= 8; i = i + 1) begin
                u_char_rom.get_character(i[3:0], 1'b0, hp, atk, def, nm, cl);
                u_char_rom.get_character(i[3:0], 1'b1, hp, atk_ts, def_ts, nm, cl);
                $display(" H%0d | Hero      | %-24s | %3d |   %2d / %2d   |   %2d / %2d   | Dual Mode Hero (F&H vs T&S)", i, nm, hp, atk, def, atk_ts, def_ts);
            end
            $display("-----+-----------+--------------------------+-----+-------------+-------------+-----------------------------");

            // 36 Monsters
            for (i = 1; i <= 36; i = i + 1) begin
                u_mon_rom.get_monster(i[5:0], 1'b0, hp, atk, def, w, is_el);
                $write(" M%02d| ", i);
                if (i == 23) $write("Mimic     | ");
                else if (is_el) $write("Elite Mon | ");
                else $write("Normal Mon| ");

                case (i)
                    1:  $write("%-24s", "Mage Ghost");
                    2:  $write("%-24s", "Classic Ghost");
                    3:  $write("%-24s", "Maw Slime");
                    4:  $write("%-24s", "Brachio Titan");
                    5:  $write("%-24s", "Antler Totem");
                    6:  $write("%-24s", "Kraken Octopus");
                    7:  $write("%-24s", "Beholder Eye");
                    8:  $write("%-24s", "Shadow Swordsman");
                    9:  $write("%-24s", "Giant Snail");
                    10: $write("%-24s", "Grave Spider");
                    11: $write("%-24s", "Dungeon Ant");
                    12: $write("%-24s", "Battle Llama");
                    13: $write("%-24s", "Shadow Hound");
                    14: $write("%-24s", "Forest Stag");
                    15: $write("%-24s", "Cave Gnome");
                    16: $write("%-24s", "Mini Knight");
                    17: $write("%-24s", "Little Drake");
                    18: $write("%-24s", "Shadow Slug");
                    19: $write("%-24s", "Dark Construct");
                    20: $write("%-24s", "Abyssal Overlord");
                    21: $write("%-24s", "Wyvern");
                    22: $write("%-24s", "Gargoyle");
                    23: $write("%-24s", "Mimic (Chest Horror)");
                    24: $write("%-24s", "Hydra");
                    25: $write("%-24s", "Imp Demon");
                    26: $write("%-24s", "Spectral Beast");
                    27: $write("%-24s", "Treant");
                    28: $write("%-24s", "Beholder");
                    29: $write("%-24s", "Stone Golem");
                    30: $write("%-24s", "Sun Chimera");
                    31: $write("%-24s", "Siren Naga");
                    32: $write("%-24s", "Unicorn");
                    33: $write("%-24s", "Ouroboros");
                    34: $write("%-24s", "Anubis Warrior");
                    35: $write("%-24s", "Phoenix");
                    36: $write("%-24s", "Cthulhu Abomination");
                    default: $write("%-24s", "Unknown Entity");
                endcase

                $write(" | %3d |  %2d |  %2d |      %02d      | ", hp, atk, def, w);
                if (i == 23) $display("Chest Trap (20%% on 'C', 0 in 'M')");
                else if (is_el) $display("Default Elite (+20%% stats, 50%% Key)");
                else $display("Standard Labyrinth Foe (20%% Key)");
            end
            $display("-----+-----------+--------------------------+-----+-----+-----+--------------+-----------------------------");
            $display("\033[1;32m[TOTAL]: 44 Pixel Art Models Rendered (8 Heroes + 36 Monsters + Chest + Key + 2 Herbs)\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // Main Showcase Flow
    // ------------------------------------------------------------------------
    integer i;

    initial begin
        $display("\033[2J\033[H");
        $display("\033[1;31m========================================================================================================\033[0m");
        $display("\033[1;31m        FEAR & HUNGER: TERMINAL LABYRINTH - COMPLETE MODEL & STATISTICAL ENCYCLOPEDIA                   \033[0m");
        $display("\033[1;31m========================================================================================================\033[0m");
        $display("\033[1;33m  Visualizing all 44 Models (8 Playable Explorers + 36 Dungeon Monsters) & Vault Relics in High-Def ANSI \033[0m");
        $display("\033[1;31m========================================================================================================\033[0m\n");

        // --- SECTION 1: 8 FEAR & HUNGER HEROES ---
        $display("\033[1;36m========================================================================================================\033[0m");
        $display("\033[1;36m   SECTION 1: 8 PLAYABLE EXPEDITION HEROES (TrueColor 24-bit Pixel Art Sprites, Facing Right)           \033[0m");
        $display("\033[1;36m========================================================================================================\033[0m\n");
        for (i = 1; i <= 8; i = i + 1) begin
            display_hero_card(i[3:0]);
        end

        // --- SECTION 2: 20 RETRO MONSTERS ---
        $display("\033[1;35m========================================================================================================\033[0m");
        $display("\033[1;35m   SECTION 2: 20 RETRO LABYRINTH MONSTERS (IDs 1 to 20, Monochrome Retro Pixel Art)                     \033[0m");
        $display("\033[1;35m========================================================================================================\033[0m\n");
        for (i = 1; i <= 20; i = i + 1) begin
            display_monster_card(i[5:0]);
        end

        // --- SECTION 3: 16 FANTASY CREATURES & MIMIC ---
        $display("\033[1;32m========================================================================================================\033[0m");
        $display("\033[1;32m   SECTION 3: 16 CLASSIC FANTASY HORRORS & THE MIMIC (IDs 21 to 36, 16x16 Pixel Art)                    \033[0m");
        $display("\033[1;32m========================================================================================================\033[0m\n");
        for (i = 21; i <= 36; i = i + 1) begin
            display_monster_card(i[5:0]);
        end

        // --- SECTION 4: VAULT RELICS & SUPPLIES ---
        display_relics_section();

        // --- SECTION 5: MASTER SUMMARY TABLE ---
        display_summary_table();

        $display("\033[1;32m========================================================================================================\033[0m");
        $display("\033[1;32m   [END OF ENCYCLOPEDIA] ALL MODELS & CHARACTER/MONSTER STATS DISPLAYED SUCCESSFULLY.                   \033[0m");
        $display("\033[1;32m========================================================================================================\033[0m\n");

        $finish;
    end

endmodule
