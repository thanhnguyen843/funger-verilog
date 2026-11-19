// ============================================================================
// Module: key_sprite_rom.v
// Model for Dungeon Key (Chìa khóa hầm ngục) from image (11x22 Pixels)
// Supports TrueColor 24-bit RGB and Transparency
// ============================================================================

`timescale 1ns / 1ps

module key_sprite_rom (
    input  wire [5:0]  row,
    input  wire [5:0]  col,
    output reg  [23:0] color_rgb,
    output reg         is_transparent
);
    always @(*) begin
        is_transparent = 1'b1;
        color_rgb      = 24'h000000;
        case (row)
            6'd0: begin
                case (col)
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd1: begin
                case (col)
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hf9ea4f; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd2: begin
                case (col)
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'hffac16; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hf17d02; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hf17d02; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hf17d02; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hf17d02; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hf9ea4f; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd3: begin
                case (col)
                    6'd0: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'hfdae14; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hf07e02; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hf07e03; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hf07d02; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hfae952; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd4: begin
                case (col)
                    6'd0: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'hf17d04; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hf17d02; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hfaea4f; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd5: begin
                case (col)
                    6'd0: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'hf17d04; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hf17d02; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hf9ea4f; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd6: begin
                case (col)
                    6'd0: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'hf9ea4f; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hf17d02; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hf17d02; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd7: begin
                case (col)
                    6'd0: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'hf17d02; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hf9ea4f; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hf17e01; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hfeac18; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd8: begin
                case (col)
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'hf07e03; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hf9ea4f; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hf17d02; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hf17d02; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hfeac18; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd9: begin
                case (col)
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hf17d04; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd10: begin
                case (col)
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h000100; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h000002; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hf17d04; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hf27d04; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h000002; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd11: begin
                case (col)
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hf17d02; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd12: begin
                case (col)
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hf17d04; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hf9ea4f; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd13: begin
                case (col)
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hf17d04; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hf9ea4f; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd14: begin
                case (col)
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hf17d04; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hf9ea4f; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd15: begin
                case (col)
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hf9ea4f; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hf17d04; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hf9ea4f; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd16: begin
                case (col)
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hf17d02; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hf17d02; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hf17d02; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hfeac18; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd17: begin
                case (col)
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h010000; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h010000; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hf17d03; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hf17d04; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd18: begin
                case (col)
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hf17d04; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd19: begin
                case (col)
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'hffac16; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hf17d04; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hfead16; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd20: begin
                case (col)
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'hf17d03; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hf07e02; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hf07e02; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hf17d04; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hffac17; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd21: begin
                case (col)
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h000000; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            default: begin
                is_transparent = 1'b1;
                color_rgb      = 24'h000000;
            end
        endcase
    end
endmodule
