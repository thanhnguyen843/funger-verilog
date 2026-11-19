// ============================================================================
// Module: character_rom.v
// Complete Database for 8 Selectable Explorers (Pick 4 of 8)
// Supports Dual Difficulty Profiles:
//   - Mode 0: Fear & Hunger (1.5x ATK & DEF Boost, Poppy +50 HP, Weed +120 HP)
//   - Mode 1: Terror & Starvation (1.0x Baseline Classic, Poppy +30 HP, Weed +70 HP)
// ============================================================================

`timescale 1ns / 1ps

module character_rom;

    task get_character;
        input  [3:0]   char_id;
        input          is_hard_mode; // 0: Fear & Hunger (1.5x Boost), 1: Terror & Starvation (1.0x Base)
        output [7:0]   char_hp;
        output [7:0]   char_atk;
        output [7:0]   char_def;
        output [255:0] char_name;
        output [255:0] char_class;
        reg    [7:0]   base_atk, base_def;
        begin
            case (char_id)
                4'd1: begin // Cahara
                    char_name  = "Cahara";
                    char_class = "Mercenary (Balanced / Swift Rogue)";
                    char_hp    = 8'd110;
                    base_atk   = 8'd22;
                    base_def   = 8'd14;
                end
                4'd2: begin // D'arce
                    char_name  = "D'arce";
                    char_class = "Holy Knight (Guardian / Heavy Armor)";
                    char_hp    = 8'd130;
                    base_atk   = 8'd18;
                    base_def   = 8'd18;
                end
                4'd3: begin // Enki
                    char_name  = "Enki";
                    char_class = "Dark Priest (Occult Mage / Glass Cannon)";
                    char_hp    = 8'd85;
                    base_atk   = 8'd30;
                    base_def   = 8'd16;
                end
                4'd4: begin // Ragnvaldr
                    char_name  = "Ragnvaldr";
                    char_class = "Outlander (Berserker / Massive HP Tank)";
                    char_hp    = 8'd140;
                    base_atk   = 8'd24;
                    base_def   = 8'd10;
                end
                4'd5: begin // Le'garde
                    char_name  = "Le'garde";
                    char_class = "Commander (Tactician / All-Rounder)";
                    char_hp    = 8'd115;
                    base_atk   = 8'd22;
                    base_def   = 8'd14;
                end
                4'd6: begin // Moonless
                    char_name  = "Moonless";
                    char_class = "Cave Direhound (Swift Beast / High Crit)";
                    char_hp    = 8'd100;
                    base_atk   = 8'd26;
                    base_def   = 8'd14;
                end
                4'd7: begin // The Girl
                    char_name  = "The Girl";
                    char_class = "Innocent Ward (Nimble / High Evasion)";
                    char_hp    = 8'd90;
                    base_atk   = 8'd18;
                    base_def   = 8'd24;
                end
                4'd8: begin // Nas'hrah
                    char_name  = "Nas'hrah";
                    char_class = "Doom Wizard (Arch-Mage / Max Destruction)";
                    char_hp    = 8'd80;
                    base_atk   = 8'd34;
                    base_def   = 8'd12;
                end
                default: begin
                    char_name  = "Explorer";
                    char_class = "Novice Wanderer";
                    char_hp    = 8'd100;
                    base_atk   = 8'd20;
                    base_def   = 8'd12;
                end
            endcase

            if (is_hard_mode) begin
                // Mode 2: Terror & Starvation (Classic 1.0x baseline stats)
                char_atk = base_atk;
                char_def = base_def;
            end else begin
                // Mode 1: Fear & Hunger (Empowered 1.5x stats)
                char_atk = base_atk + (base_atk / 8'd2);
                char_def = base_def + (base_def / 8'd2);
            end
        end
    endtask

endmodule
