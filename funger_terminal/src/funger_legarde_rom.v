// ============================================================================
// Module: funger_legarde_rom.v
// Fear & Hunger 1 Character Sprite Model: Le'garde
// Grid: 26x26 Pixels | 7 Colors + Index 0: Transparent
// ============================================================================

`timescale 1ns / 1ps

module funger_legarde_rom #(
    parameter WIDTH  = 26,
    parameter HEIGHT = 26
) (
    input  wire       flip_h,         // 1: Quay mat sang trai (Facing Left), 0: Nguyen ban
    input  wire [5:0] row,
    input  wire [5:0] col,
    output reg  [2:0] pixel_val,
    output wire       is_transparent,
    output reg  [7:0] r,
    output reg  [7:0] g,
    output reg  [7:0] b
);

    // Dieu khien huong quay mat: flip_h = 0: Quay mat sang phai (Facing Right), flip_h = 1: Nguyen ban (Facing Left)
    wire [5:0] eff_col = flip_h ? col : (WIDTH - 1 - col);

    // ------------------------------------------------------------------------
    // 1. Hình dạng (spr_row): Ma trận điểm ảnh
    // ------------------------------------------------------------------------
    reg [77:0] row_pixels;

    always @(*) begin
        if (eff_col < WIDTH)
            pixel_val = row_pixels[(WIDTH - 1 - eff_col)*3 +: 3];
        else
            pixel_val = 3'd0;
    end

    always @(*) begin
        case (row)
            6'd0: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd1,3'd1,3'd1,3'd1,3'd1,3'd1,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0};
            6'd1: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd4,3'd4,3'd4,3'd4,3'd4,3'd4,3'd2,3'd1,3'd0,3'd0,3'd0,3'd0,3'd0};
            6'd2: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd7,3'd7,3'd4,3'd4,3'd7,3'd4,3'd4,3'd3,3'd1,3'd0,3'd0,3'd0,3'd0};
            6'd3: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd4,3'd4,3'd4,3'd7,3'd4,3'd4,3'd4,3'd4,3'd4,3'd1,3'd0,3'd0,3'd0,3'd0};
            6'd4: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd4,3'd4,3'd7,3'd7,3'd7,3'd4,3'd4,3'd4,3'd4,3'd4,3'd1,3'd0,3'd0,3'd0};
            6'd5: row_pixels = {3'd1,3'd1,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd4,3'd4,3'd1,3'd7,3'd7,3'd1,3'd3,3'd4,3'd4,3'd4,3'd1,3'd0,3'd0,3'd0};
            6'd6: row_pixels = {3'd1,3'd3,3'd1,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd4,3'd2,3'd3,3'd7,3'd7,3'd3,3'd5,3'd4,3'd4,3'd4,3'd1,3'd0,3'd0,3'd0};
            6'd7: row_pixels = {3'd1,3'd3,3'd2,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd4,3'd1,3'd5,3'd7,3'd7,3'd5,3'd5,3'd4,3'd4,3'd3,3'd1,3'd0,3'd0,3'd0};
            6'd8: row_pixels = {3'd0,3'd1,3'd6,3'd1,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd4,3'd1,3'd6,3'd7,3'd7,3'd7,3'd4,3'd4,3'd4,3'd1,3'd0,3'd0,3'd0,3'd0};
            6'd9: row_pixels = {3'd0,3'd0,3'd1,3'd6,3'd1,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd6,3'd4,3'd1,3'd3,3'd5,3'd4,3'd4,3'd4,3'd5,3'd6,3'd1,3'd0,3'd0,3'd0};
            6'd10: row_pixels = {3'd0,3'd0,3'd0,3'd1,3'd5,3'd2,3'd1,3'd0,3'd0,3'd0,3'd1,3'd6,3'd5,3'd4,3'd3,3'd5,3'd5,3'd4,3'd4,3'd5,3'd6,3'd5,3'd6,3'd1,3'd0,3'd0};
            6'd11: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd1,3'd3,3'd5,3'd1,3'd1,3'd1,3'd5,3'd3,3'd4,3'd6,3'd5,3'd6,3'd6,3'd6,3'd4,3'd4,3'd5,3'd6,3'd5,3'd1,3'd0,3'd0};
            6'd12: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd2,3'd5,3'd1,3'd2,3'd3,3'd2,3'd1,3'd5,3'd6,3'd6,3'd6,3'd5,3'd3,3'd2,3'd1,3'd1,3'd3,3'd1,3'd1,3'd0};
            6'd13: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd1,3'd1,3'd2,3'd2,3'd1,3'd1,3'd1,3'd1,3'd3,3'd3,3'd3,3'd3,3'd1,3'd1,3'd1,3'd0,3'd1,3'd5,3'd1,3'd0};
            6'd14: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd1,3'd1,3'd0,3'd0,3'd1,3'd5,3'd6,3'd6,3'd6,3'd5,3'd3,3'd2,3'd1,3'd0,3'd0,3'd1,3'd2,3'd1};
            6'd15: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd6,3'd3,3'd5,3'd5,3'd5,3'd3,3'd6,3'd6,3'd5,3'd1,3'd0,3'd1,3'd2,3'd1};
            6'd16: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd6,3'd3,3'd6,3'd6,3'd6,3'd3,3'd6,3'd6,3'd5,3'd1,3'd0,3'd0,3'd1,3'd1};
            6'd17: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd5,3'd2,3'd5,3'd6,3'd5,3'd2,3'd5,3'd6,3'd6,3'd1,3'd0,3'd0,3'd0,3'd0};
            6'd18: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd3,3'd2,3'd3,3'd3,3'd3,3'd2,3'd3,3'd5,3'd5,3'd2,3'd0,3'd0,3'd0,3'd0};
            6'd19: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd2,3'd2,3'd1,3'd1,3'd2,3'd2,3'd2,3'd2,3'd6,3'd1,3'd0,3'd0,3'd0};
            6'd20: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd6,3'd2,3'd1,3'd0,3'd1,3'd2,3'd3,3'd6,3'd5,3'd1,3'd0,3'd0,3'd0};
            6'd21: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd5,3'd6,3'd1,3'd0,3'd0,3'd1,3'd2,3'd5,3'd6,3'd5,3'd1,3'd0,3'd0};
            6'd22: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd6,3'd1,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd5,3'd5,3'd1,3'd0,3'd0};
            6'd23: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd5,3'd1,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd6,3'd5,3'd1,3'd0};
            6'd24: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd1,3'd1,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd6,3'd1,3'd0};
            6'd25: row_pixels = {3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd0,3'd1,3'd1,3'd1,3'd0};
            default: row_pixels = 78'd0;
        endcase
    end

    // ------------------------------------------------------------------------
    // 2. Bảng màu (spr_col): Index 0 = Transparent, Index 1..N = RGB
    // ------------------------------------------------------------------------
    assign is_transparent = (pixel_val == 3'd0);

    always @(*) begin
        case (pixel_val)
            3'd0: begin r = 8'd0; g = 8'd0; b = 8'd0; end // Transparent
            3'd1: begin r = 8'd2; g = 8'd1; b = 8'd1; end
            3'd2: begin r = 8'd62; g = 8'd52; b = 8'd51; end
            3'd3: begin r = 8'd125; g = 8'd104; b = 8'd99; end
            3'd4: begin r = 8'd177; g = 8'd126; b = 8'd78; end
            3'd5: begin r = 8'd167; g = 8'd147; b = 8'd144; end
            3'd6: begin r = 8'd199; g = 8'd187; b = 8'd185; end
            3'd7: begin r = 8'd229; g = 8'd196; b = 8'd161; end
            default: begin r = 8'd0; g = 8'd0; b = 8'd0; end
        endcase
    end

endmodule
