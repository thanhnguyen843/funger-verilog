// ============================================================================
// Module: chest_sprite_rom.v
// Model for Opened Treasure Chest from image (20x23 Pixels)
// Supports TrueColor 24-bit RGB and Transparency
// ============================================================================

`timescale 1ns / 1ps

module chest_sprite_rom (
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
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h543a29; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h553a25; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h553a25; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h553a25; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h543924; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h563a25; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h553924; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h553924; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h543823; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h543823; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h543924; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd1: begin
                case (col)
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h543b25; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hed8f2b; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hfcc73d; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hfbc839; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hfac93e; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hf19226; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hf38e22; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'hf18a23; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'hf28729; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'he97c1f; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'hdd6e26; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h4c3621; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h51351f; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h523621; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd2: begin
                case (col)
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h553a27; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hec8b24; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hf5a228; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hfac237; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hffdc69; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hfddc69; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hfcbe35; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hfac239; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'hffc640; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'hf09628; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'hcd5c18; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h4e311f; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'hed832f; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'hcd5b1d; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'hd15f20; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h503522; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd3: begin
                case (col)
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'h513a28; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'hffd660; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hfbd862; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hffd660; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hffd75e; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hfcd055; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hfcce54; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hfacd4e; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hfdcc4b; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'hffce4e; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'hfec945; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h4a361e; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'hef8730; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'hbe4b1e; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'hbf4d1b; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h9c3c14; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'hc44c18; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h4e361e; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd4: begin
                case (col)
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'h503b2a; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h543a29; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h553a27; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h543926; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h543926; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h543926; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h533a26; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h523925; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h533825; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h513824; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h513824; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h513623; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'hd05824; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'he3732b; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'ha73f1c; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'hb24719; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h832f13; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'hd05f25; end
                    6'd19: begin is_transparent = 1'b0; color_rgb = 24'h4d3626; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd5: begin
                case (col)
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h553a27; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h553a27; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h533825; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'ha92e1c; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'ha8311b; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'ha9301b; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'haa321a; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'had331b; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'hb3351c; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'hb0341a; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h523321; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h50341f; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'hcc5922; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'hd15f21; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h95351c; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h873116; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'hcd5f24; end
                    6'd19: begin is_transparent = 1'b0; color_rgb = 24'h4e3727; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd6: begin
                case (col)
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h543924; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h9e2d1d; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h9a2d19; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hc23b1e; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hc3391c; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hc73a1c; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hc93f1a; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'hca411d; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'hc73e1c; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'hbe381d; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h513021; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h4d321f; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'hce581b; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'hcc551b; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h8b3116; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'hba4f21; end
                    6'd19: begin is_transparent = 1'b0; color_rgb = 24'h4d3626; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd7: begin
                case (col)
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h533928; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h972c1a; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h852a17; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hbb351a; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hc53b1e; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hde4f25; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'he35025; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'he04e25; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'hc73c1d; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'hbe381b; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h4c311e; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h4c3120; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'hbe4c18; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'hbb4c1e; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h9f3e1b; end
                    6'd19: begin is_transparent = 1'b0; color_rgb = 24'h4d3626; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd8: begin
                case (col)
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h533729; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h982d19; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h912c18; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hd54723; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hde4b20; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'hf05c2c; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'hf15d2d; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'hd0421c; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'hd0411f; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'hac3018; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h453420; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h4b321e; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'hc65624; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h9e3e18; end
                    6'd19: begin is_transparent = 1'b0; color_rgb = 24'h4d3626; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd9: begin
                case (col)
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h523827; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h992e1a; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'had331e; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'he95924; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'hec5b2c; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'hee5e2a; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'hed5c2d; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'hec5c27; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'hbd3d16; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'ha22c1e; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h532e1c; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h4f3421; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h4f3421; end
                    6'd19: begin is_transparent = 1'b0; color_rgb = 24'h4c3629; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd10: begin
                case (col)
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h523925; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h513824; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h513824; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h513824; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h523925; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h503723; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h513623; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h4f3622; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h4f3421; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h4f3421; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h4f3421; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h503522; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd11: begin
                case (col)
                    6'd0: begin is_transparent = 1'b0; color_rgb = 24'h513d25; end
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'h513a28; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h553a27; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h543a29; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h543b27; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h533928; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h543926; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h533a26; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h533928; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h513b26; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h533827; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h533624; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h523724; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h523523; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h513422; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h513520; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h4e351f; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h503522; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h523621; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd12: begin
                case (col)
                    6'd0: begin is_transparent = 1'b0; color_rgb = 24'h583924; end
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'hfed966; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'hfed55f; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hfed45e; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hfed15a; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hfdd059; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hfdd059; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hfcc94a; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hfbc541; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hf8c643; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'hffe375; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'hcc5c2a; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'hb84d1f; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'hb84d1f; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'hbb4f1e; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'hc45623; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'hc75924; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'hd06227; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h4e3823; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd13: begin
                case (col)
                    6'd0: begin is_transparent = 1'b0; color_rgb = 24'h553924; end
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'hfdbf3a; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'hf59622; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hf9a729; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hb2bdc3; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hb9babc; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hbabbbd; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h68626e; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'he27018; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hde7217; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'hffc94b; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'he1711d; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h7c2a12; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h7d2d16; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h7d2d12; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h7d2d12; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h803017; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'hb94f1f; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h4d3722; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd14: begin
                case (col)
                    6'd0: begin is_transparent = 1'b0; color_rgb = 24'h533a24; end
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'hffd25c; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'hb2480e; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hcd6120; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hbebabb; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h645c59; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hbfbfbf; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h696363; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hac4b16; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hb9500f; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'hffda53; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'hde7323; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h842e0b; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h9f3e1b; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h9b3d1b; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h993a1a; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h9d3f1d; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'he06f2d; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h4f3524; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd15: begin
                case (col)
                    6'd0: begin is_transparent = 1'b0; color_rgb = 24'h533a24; end
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'hfdc345; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'haf450b; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hf0882f; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hbfb7c4; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h665e5c; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h999798; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h6a6665; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'he27636; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hde7021; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'hffd355; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'hda7024; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h842e0d; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'hac4b21; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'hab481e; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h803017; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h802f14; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'he1702c; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h4d3626; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd16: begin
                case (col)
                    6'd0: begin is_transparent = 1'b0; color_rgb = 24'h53372b; end
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'hfbbc39; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'hd56116; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hf0862e; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h837d7f; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h8d8e93; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h8f8e94; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h7c5f64; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hf88c43; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hdd6d21; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'hffbb41; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'hdc681f; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h832d0c; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'he97626; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'he67529; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'he7752c; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h8b351c; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'hdf6e2a; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h4d3626; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd17: begin
                case (col)
                    6'd0: begin is_transparent = 1'b0; color_rgb = 24'h54362b; end
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'hfcc23d; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'hd66217; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hed832d; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'heb7e2b; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hcf6221; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hce6021; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hc95c21; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hde6c23; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hd5651d; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'hffcb4e; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'hde6a21; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h873012; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'ha03f1c; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h9d3f1d; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h993c1b; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h9b3e1d; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'hde6f2a; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h4c3525; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd18: begin
                case (col)
                    6'd0: begin is_transparent = 1'b0; color_rgb = 24'h553a27; end
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'hf7b733; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'he77c1e; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hf9a73b; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hfaa437; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hfe9e37; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hfc9c35; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hffa24a; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hd7651f; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hbc511b; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'hffc543; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'hdf6b1e; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h842d11; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'hac4b20; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'ha8451c; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h802e16; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h803015; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'haa441e; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h4c3820; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd19: begin
                case (col)
                    6'd0: begin is_transparent = 1'b0; color_rgb = 24'h563725; end
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'hfab430; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'hc55315; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hd66924; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'he97f2b; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'he87b28; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'he87b28; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'he6762a; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'he07024; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hc1571d; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'hffc03b; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'hdb6619; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'ha53f19; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'hd66320; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'hd05c1f; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'hcc5920; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h883217; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'hc05423; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h4f3622; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd20: begin
                case (col)
                    6'd0: begin is_transparent = 1'b0; color_rgb = 24'h55382a; end
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'hf8b02a; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'had420e; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hb54c1c; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hb54c1c; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hb44b1b; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hb34a1a; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hb54b19; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hb44a18; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hb54918; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'hffa32a; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'hca5a12; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h862f11; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h913818; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h8e3817; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h8c3517; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h832f13; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'hcc5e23; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h4f3620; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd21: begin
                case (col)
                    6'd0: begin is_transparent = 1'b0; color_rgb = 24'h553621; end
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'hea9022; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'hf7b52d; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'hf7b32a; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hf7b32c; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hf5af29; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hf5af29; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hf6b02a; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hf9b129; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hf7af29; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'he57f1b; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'hac4314; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'hc75821; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'hcf5f20; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'hcd5f20; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'hcd5c22; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'hc95b20; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'ha03d1d; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h513520; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd22: begin
                case (col)
                    6'd0: begin is_transparent = 1'b0; color_rgb = 24'h523827; end
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'h533825; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h533825; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h533825; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h533825; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h533825; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h533825; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h523724; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h523724; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h513623; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h513623; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h513623; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h523722; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h513623; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h513623; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h503522; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h523621; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h523621; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h503522; end
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
