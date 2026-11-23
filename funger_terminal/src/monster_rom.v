// ============================================================================
// Module: monster_rom.v
// Unified Database for:
//   - 20 Retro Monsters (IDs 1 to 20, from monster.v)
//   - 16 Fantasy Creatures (IDs 21 to 36, from fantasy_creatures.v)
//   - ID 23: Mimic (Deceitful Chest Horror - Spawn Weight 0, Never Elite)
//   - Selected Elites with low spawn probability (Weight 1-2) & +20% Stats
// ============================================================================

`timescale 1ns / 1ps
`include "battle_defs.vh"

module monster_rom (
    input  wire [5:0]  monster_id,   // 1 to 36
    input  wire        is_elite,     // 1: Elite Monster (+20% stats)
    output reg  [7:0]  base_hp,
    output reg  [7:0]  base_atk,
    output reg  [7:0]  base_def,
    output reg  [7:0]  spawn_weight,
    output reg         is_default_elite,
    output reg  [1:0]  archetype
);

    reg [7:0] raw_hp;
    reg [7:0] raw_atk;
    reg [7:0] raw_def;

    always @(*) begin
        is_default_elite = 1'b0;
        case (monster_id)
            6'd1, 6'd2, 6'd26:  archetype = `ARCHETYPE_SPECTRAL;
            6'd4, 6'd19, 6'd22: archetype = `ARCHETYPE_ARMORED;
            6'd7, 6'd20, 6'd28: archetype = `ARCHETYPE_TERROR;
            default:            archetype = `ARCHETYPE_NORMAL;
        endcase

        case (monster_id)
            // --- Part 1: Retro Monsters (1 to 20) ---
            6'd1:  begin raw_hp = 8'd85;  raw_atk = 8'd21; raw_def = 8'd12; spawn_weight = 8'd8; end // Mage Ghost
            6'd2:  begin raw_hp = 8'd80;  raw_atk = 8'd19; raw_def = 8'd10; spawn_weight = 8'd9; end // Classic Ghost
            6'd3:  begin raw_hp = 8'd110; raw_atk = 8'd16; raw_def = 8'd18; spawn_weight = 8'd8; end // Maw Slime
            6'd4:  begin raw_hp = 8'd150; raw_atk = 8'd24; raw_def = 8'd22; spawn_weight = 8'd2; is_default_elite = 1'b1; end // Brachio Titan [ELITE]
            6'd5:  begin raw_hp = 8'd100; raw_atk = 8'd20; raw_def = 8'd16; spawn_weight = 8'd7; end // Antler Totem
            6'd6:  begin raw_hp = 8'd115; raw_atk = 8'd22; raw_def = 8'd14; spawn_weight = 8'd6; end // Kraken Octopus
            6'd7:  begin raw_hp = 8'd90;  raw_atk = 8'd25; raw_def = 8'd10; spawn_weight = 8'd7; end // Beholder Eye
            6'd8:  begin raw_hp = 8'd95;  raw_atk = 8'd24; raw_def = 8'd14; spawn_weight = 8'd8; end // Shadow Swordsman
            6'd9:  begin raw_hp = 8'd120; raw_atk = 8'd14; raw_def = 8'd24; spawn_weight = 8'd7; end // Giant Snail
            6'd10: begin raw_hp = 8'd90;  raw_atk = 8'd23; raw_def = 8'd12; spawn_weight = 8'd8; end // Grave Spider
            6'd11: begin raw_hp = 8'd85;  raw_atk = 8'd20; raw_def = 8'd14; spawn_weight = 8'd8; end // Dungeon Ant
            6'd12: begin raw_hp = 8'd105; raw_atk = 8'd18; raw_def = 8'd16; spawn_weight = 8'd7; end // Battle Llama
            6'd13: begin raw_hp = 8'd85;  raw_atk = 8'd24; raw_def = 8'd8;  spawn_weight = 8'd8; end // Shadow Hound
            6'd14: begin raw_hp = 8'd95;  raw_atk = 8'd19; raw_def = 8'd14; spawn_weight = 8'd8; end // Forest Stag
            6'd15: begin raw_hp = 8'd80;  raw_atk = 8'd18; raw_def = 8'd12; spawn_weight = 8'd9; end // Cave Gnome
            6'd16: begin raw_hp = 8'd100; raw_atk = 8'd21; raw_def = 8'd18; spawn_weight = 8'd7; end // Mini Knight
            6'd17: begin raw_hp = 8'd105; raw_atk = 8'd23; raw_def = 8'd12; spawn_weight = 8'd6; end // Little Drake
            6'd18: begin raw_hp = 8'd95;  raw_atk = 8'd15; raw_def = 8'd20; spawn_weight = 8'd8; end // Shadow Slug
            6'd19: begin raw_hp = 8'd140; raw_atk = 8'd22; raw_def = 8'd24; spawn_weight = 8'd2; is_default_elite = 1'b1; end // Dark Construct [ELITE]
            6'd20: begin raw_hp = 8'd160; raw_atk = 8'd28; raw_def = 8'd20; spawn_weight = 8'd1; is_default_elite = 1'b1; end // Abyssal Overlord [ELITE]

            // --- Part 2: Fantasy Creatures (21 to 36) ---
            6'd21: begin raw_hp = 8'd115; raw_atk = 8'd24; raw_def = 8'd14; spawn_weight = 8'd6; end // Wyvern
            6'd22: begin raw_hp = 8'd110; raw_atk = 8'd20; raw_def = 8'd20; spawn_weight = 8'd6; end // Gargoyle
            6'd23: begin raw_hp = 8'd95;  raw_atk = 8'd22; raw_def = 8'd12; spawn_weight = 8'd0; end // Mimic (CHEST ONLY, NOT ELITE)
            6'd24: begin raw_hp = 8'd145; raw_atk = 8'd26; raw_def = 8'd16; spawn_weight = 8'd2; is_default_elite = 1'b1; end // Hydra [ELITE]
            6'd25: begin raw_hp = 8'd85;  raw_atk = 8'd23; raw_def = 8'd10; spawn_weight = 8'd8; end // Imp Demon
            6'd26: begin raw_hp = 8'd95;  raw_atk = 8'd22; raw_def = 8'd12; spawn_weight = 8'd7; end // Spectral Beast
            6'd27: begin raw_hp = 8'd130; raw_atk = 8'd18; raw_def = 8'd22; spawn_weight = 8'd5; end // Treant
            6'd28: begin raw_hp = 8'd100; raw_atk = 8'd25; raw_def = 8'd12; spawn_weight = 8'd5; end // Beholder
            6'd29: begin raw_hp = 8'd155; raw_atk = 8'd22; raw_def = 8'd25; spawn_weight = 8'd2; is_default_elite = 1'b1; end // Stone Golem [ELITE]
            6'd30: begin raw_hp = 8'd135; raw_atk = 8'd27; raw_def = 8'd18; spawn_weight = 8'd2; is_default_elite = 1'b1; end // Sun Chimera [ELITE]
            6'd31: begin raw_hp = 8'd100; raw_atk = 8'd21; raw_def = 8'd15; spawn_weight = 8'd6; end // Siren Naga
            6'd32: begin raw_hp = 8'd110; raw_atk = 8'd20; raw_def = 8'd18; spawn_weight = 8'd5; end // Unicorn
            6'd33: begin raw_hp = 8'd150; raw_atk = 8'd25; raw_def = 8'd20; spawn_weight = 8'd2; is_default_elite = 1'b1; end // Ouroboros [ELITE]
            6'd34: begin raw_hp = 8'd115; raw_atk = 8'd24; raw_def = 8'd15; spawn_weight = 8'd5; end // Anubis Warrior
            6'd35: begin raw_hp = 8'd125; raw_atk = 8'd29; raw_def = 8'd14; spawn_weight = 8'd2; is_default_elite = 1'b1; end // Phoenix [ELITE]
            6'd36: begin raw_hp = 8'd170; raw_atk = 8'd30; raw_def = 8'd22; spawn_weight = 8'd1; is_default_elite = 1'b1; end // Cthulhu Abomination [ELITE]
            default: begin
                raw_hp = 8'd100; raw_atk = 8'd20; raw_def = 8'd12; spawn_weight = 8'd5;
            end
        endcase

        // Boost stats by +20% if Elite (Mimic is never elite) via 16-bit shift-scale (~51/256 = 19.92%)
        if (is_elite && monster_id != 6'd23) begin
            base_hp  = raw_hp  + (({8'd0, raw_hp}  * 8'd51) >> 8);
            base_atk = raw_atk + (({8'd0, raw_atk} * 8'd51) >> 8);
            base_def = raw_def + (({8'd0, raw_def} * 8'd51) >> 8);
        end else begin
            base_hp  = raw_hp;
            base_atk = raw_atk;
            base_def = raw_def;
        end
    end

    // Task to lookup monster details
    task get_monster;
        input  [5:0]   mid;
        input          elite;
        output [7:0]   hp;
        output [7:0]   atk;
        output [7:0]   def;
        output [7:0]   weight;
        output         is_el;
        reg [7:0] rh, ra, rd;
        begin
            is_el = 1'b0;
            case (mid)
                6'd1:  begin rh = 8'd85;  ra = 8'd21; rd = 8'd12; weight = 8'd8; end
                6'd2:  begin rh = 8'd80;  ra = 8'd19; rd = 8'd10; weight = 8'd9; end
                6'd3:  begin rh = 8'd110; ra = 8'd16; rd = 8'd18; weight = 8'd8; end
                6'd4:  begin rh = 8'd150; ra = 8'd24; rd = 8'd22; weight = 8'd2; is_el = 1'b1; end
                6'd5:  begin rh = 8'd100; ra = 8'd20; rd = 8'd16; weight = 8'd7; end
                6'd6:  begin rh = 8'd115; ra = 8'd22; rd = 8'd14; weight = 8'd6; end
                6'd7:  begin rh = 8'd90;  ra = 8'd25; rd = 8'd10; weight = 8'd7; end
                6'd8:  begin rh = 8'd95;  ra = 8'd24; rd = 8'd14; weight = 8'd8; end
                6'd9:  begin rh = 8'd120; ra = 8'd14; rd = 8'd24; weight = 8'd7; end
                6'd10: begin rh = 8'd90;  ra = 8'd23; rd = 8'd12; weight = 8'd8; end
                6'd11: begin rh = 8'd85;  ra = 8'd20; rd = 8'd14; weight = 8'd8; end
                6'd12: begin rh = 8'd105; ra = 8'd18; rd = 8'd16; weight = 8'd7; end
                6'd13: begin rh = 8'd85;  ra = 8'd24; rd = 8'd8;  weight = 8'd8; end
                6'd14: begin rh = 8'd95;  ra = 8'd19; rd = 8'd14; weight = 8'd8; end
                6'd15: begin rh = 8'd80;  ra = 8'd18; rd = 8'd12; weight = 8'd9; end
                6'd16: begin rh = 8'd100; ra = 8'd21; rd = 8'd18; weight = 8'd7; end
                6'd17: begin rh = 8'd105; ra = 8'd23; rd = 8'd12; weight = 8'd6; end
                6'd18: begin rh = 8'd95;  ra = 8'd15; rd = 8'd20; weight = 8'd8; end
                6'd19: begin rh = 8'd140; ra = 8'd22; rd = 8'd24; weight = 8'd2; is_el = 1'b1; end
                6'd20: begin rh = 8'd160; ra = 8'd28; rd = 8'd20; weight = 8'd1; is_el = 1'b1; end

                6'd21: begin rh = 8'd115; ra = 8'd24; rd = 8'd14; weight = 8'd6; end
                6'd22: begin rh = 8'd110; ra = 8'd20; rd = 8'd20; weight = 8'd6; end
                6'd23: begin rh = 8'd95;  ra = 8'd22; rd = 8'd12; weight = 8'd0; end // Mimic
                6'd24: begin rh = 8'd145; ra = 8'd26; rd = 8'd16; weight = 8'd2; is_el = 1'b1; end
                6'd25: begin rh = 8'd85;  ra = 8'd23; rd = 8'd10; weight = 8'd8; end
                6'd26: begin rh = 8'd95;  ra = 8'd22; rd = 8'd12; weight = 8'd7; end
                6'd27: begin rh = 8'd130; ra = 8'd18; rd = 8'd22; weight = 8'd5; end
                6'd28: begin rh = 8'd100; ra = 8'd25; rd = 8'd12; weight = 8'd5; end
                6'd29: begin rh = 8'd155; ra = 8'd22; rd = 8'd25; weight = 8'd2; is_el = 1'b1; end
                6'd30: begin rh = 8'd135; ra = 8'd27; rd = 8'd18; weight = 8'd2; is_el = 1'b1; end
                6'd31: begin rh = 8'd100; ra = 8'd21; rd = 8'd15; weight = 8'd6; end
                6'd32: begin rh = 8'd110; ra = 8'd20; rd = 8'd18; weight = 8'd5; end
                6'd33: begin rh = 8'd150; ra = 8'd25; rd = 8'd20; weight = 8'd2; is_el = 1'b1; end
                6'd34: begin rh = 8'd115; ra = 8'd24; rd = 8'd15; weight = 8'd5; end
                6'd35: begin rh = 8'd125; ra = 8'd29; rd = 8'd14; weight = 8'd2; is_el = 1'b1; end
                6'd36: begin rh = 8'd170; ra = 8'd30; rd = 8'd22; weight = 8'd1; is_el = 1'b1; end
                default: begin
                    rh = 8'd100; ra = 8'd20; rd = 8'd12; weight = 8'd5;
                end
            endcase

            if ((elite || is_el) && mid != 6'd23) begin
                hp  = rh + (({8'd0, rh} * 8'd51) >> 8);
                atk = ra + (({8'd0, ra} * 8'd51) >> 8);
                def = rd + (({8'd0, rd} * 8'd51) >> 8);
                is_el = 1'b1;
            end else begin
                hp  = rh;
                atk = ra;
                def = rd;
            end
        end
    endtask

    // Task to print monster name in English (padded to exactly 32 chars for column alignment)
    task print_monster_name;
        input [5:0] id;
        begin
            case (id)
                6'd1:  $write("Mage Ghost                      ");
                6'd2:  $write("Classic Ghost                   ");
                6'd3:  $write("Maw Slime                       ");
                6'd4:  $write("Brachio Titan                   ");
                6'd5:  $write("Antler Totem                    ");
                6'd6:  $write("Kraken Octopus                  ");
                6'd7:  $write("Beholder Eye                    ");
                6'd8:  $write("Shadow Swordsman                ");
                6'd9:  $write("Giant Snail                     ");
                6'd10: $write("Grave Spider                    ");
                6'd11: $write("Dungeon Ant                     ");
                6'd12: $write("Battle Llama                    ");
                6'd13: $write("Shadow Hound                    ");
                6'd14: $write("Forest Stag                     ");
                6'd15: $write("Cave Gnome                      ");
                6'd16: $write("Mini Knight                     ");
                6'd17: $write("Little Drake                    ");
                6'd18: $write("Shadow Slug                     ");
                6'd19: $write("Dark Construct                  ");
                6'd20: $write("Abyssal Overlord                ");

                6'd21: $write("Wyvern                          ");
                6'd22: $write("Gargoyle                        ");
                6'd23: $write("Mimic (Chest Horror)            ");
                6'd24: $write("Hydra                           ");
                6'd25: $write("Imp Demon                       ");
                6'd26: $write("Spectral Beast                  ");
                6'd27: $write("Treant                          ");
                6'd28: $write("Beholder                        ");
                6'd29: $write("Stone Golem                     ");
                6'd30: $write("Sun Chimera                     ");
                6'd31: $write("Siren Naga                      ");
                6'd32: $write("Unicorn                         ");
                6'd33: $write("Ouroboros                       ");
                6'd34: $write("Anubis Warrior                  ");
                6'd35: $write("Phoenix                         ");
                6'd36: $write("Cthulhu Abomination             ");
                default: $write("Unknown Entity                  ");
            endcase
        end
    endtask

    // Task to print monster type in English (padded to exactly 18 chars for column alignment)
    task print_monster_type;
        input [5:0] id;
        begin
            case (id)
                6'd1:  $write("Ghost / Occult    ");
                6'd2:  $write("Spectral Undead   ");
                6'd3:  $write("Abyss Slime       ");
                6'd4:  $write("Colossal Beast    ");
                6'd5:  $write("Forest Totem      ");
                6'd6:  $write("Abyssal Cephalopod");
                6'd7:  $write("Aberration Eye    ");
                6'd8:  $write("Dark Blade        ");
                6'd9:  $write("Armored Shell     ");
                6'd10: $write("Venom Arachnid    ");
                6'd11: $write("Swarm Insect      ");
                6'd12: $write("Mystic Quadruped  ");
                6'd13: $write("Shadow Beast      ");
                6'd14: $write("Woodland Spirit   ");
                6'd15: $write("Subterranean Dwarf");
                6'd16: $write("Steel Armored     ");
                6'd17: $write("Draconic Hatchling");
                6'd18: $write("Ooze Slug         ");
                6'd19: $write("Ancient Golem     ");
                6'd20: $write("Eldritch Tyrant   ");

                6'd21: $write("Draconic Wyvern   ");
                6'd22: $write("Stone Gargoyle    ");
                6'd23: $write("Mimic Deceiver    ");
                6'd24: $write("Multihead Serpent ");
                6'd25: $write("Hell Fiend        ");
                6'd26: $write("Spectral Phantom  ");
                6'd27: $write("Ancient Arboreal  ");
                6'd28: $write("Evil Eye Fiend    ");
                6'd29: $write("Granite Colossus  ");
                6'd30: $write("Solar Chimera     ");
                6'd31: $write("Serpentine Siren  ");
                6'd32: $write("Sacred Unicorn    ");
                6'd33: $write("Cosmic Serpent    ");
                6'd34: $write("Guardian Jackal   ");
                6'd35: $write("Immortal Phoenix  ");
                6'd36: $write("Elder God Cosmic  ");
                default: $write("Unknown Origin    ");
            endcase
        end
    endtask

endmodule
