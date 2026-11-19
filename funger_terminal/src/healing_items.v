// ============================================================================
// Module: healing_items.v
// Kiến trúc phần cứng lưu trữ ROM và hiển thị 2 Vật phẩm Hồi máu (Healing Items):
//   Item 0: Green Herb (Thảo dược xanh) - 20x20 Pixels
//   Item 1: Red Flower (Bông hoa đỏ chữa lành) - 14x14 Pixels
// Đặc tính kỹ thuật:
//   - Độ phân giải màu TrueColor 24-bit RGB (R[23:16], G[15:8], B[7:0])
//   - Tích hợp cờ Trong suốt (is_transparent = 1) loại bỏ nền trắng
//   - Hỗ trợ tín hiệu điều khiển lật ngang phần cứng (flip_h)
// ============================================================================

`timescale 1ns / 1ps

// ----------------------------------------------------------------------------
// Module con 1: ROM Thảo dược xanh (Green Herb 20x20)
// ----------------------------------------------------------------------------
module healing_herb_rom (
    input  wire [5:0]  row,
    input  wire [5:0]  col,
    input  wire        flip_h,
    output reg  [23:0] color_rgb,
    output reg         is_transparent
);
    localparam WIDTH = 6'd20;
    wire [5:0] eff_col = flip_h ? (WIDTH - 1'b1 - col) : col;

    always @(*) begin
        is_transparent = 1'b1;
        color_rgb      = 24'h000000;
        case (row)
            6'd0: begin
                case (eff_col)
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h2a3143; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd1: begin
                case (eff_col)
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h6ae065; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd2: begin
                case (eff_col)
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h29a370; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd3: begin
                case (eff_col)
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h29a370; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd4: begin
                case (eff_col)
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h2aa274; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h2a3143; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd5: begin
                case (eff_col)
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h2a3143; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h2aa374; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h293343; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h2aa275; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h2a3143; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h69e263; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h2aa374; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h2a3144; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd6: begin
                case (eff_col)
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h2a3143; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h66e365; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h293144; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h2aa274; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h293144; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h69e166; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h24bd6b; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h2a3144; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd7: begin
                case (eff_col)
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h293241; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h21b174; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h22be6d; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h69e263; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h273343; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h2aa274; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h28a374; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h21b174; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h2a3144; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd8: begin
                case (eff_col)
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h273343; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h22be6d; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h69e166; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h273341; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h2aa274; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h69e263; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h22be6d; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h28a374; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h273343; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd9: begin
                case (eff_col)
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h21b174; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h22bf6b; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h24bd6b; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h2a3144; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h2aa274; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h21bf6b; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h21b174; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd10: begin
                case (eff_col)
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h20b273; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h2aa275; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h273244; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h29a370; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h67e263; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h2aa274; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h21b174; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h2a3143; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd11: begin
                case (eff_col)
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h20b274; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h2aa275; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h22b074; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h2a3143; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd12: begin
                case (eff_col)
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h2aa272; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h2aa275; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h22be6b; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd19: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd13: begin
                case (eff_col)
                    6'd1: begin is_transparent = 1'b0; color_rgb = 24'h293143; end
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h1eb276; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h29a372; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h2aa272; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h69e265; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h2a3146; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h24bd6b; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h22be6b; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h302f3f; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h69e263; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h28a372; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h29a372; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h1eb373; end
                    6'd19: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd14: begin
                case (eff_col)
                    6'd2: begin is_transparent = 1'b0; color_rgb = 24'h293241; end
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h21b174; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h22b074; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h21b174; end
                    6'd18: begin is_transparent = 1'b0; color_rgb = 24'h2a3144; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd15: begin
                case (eff_col)
                    6'd3: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h20b274; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h22be6d; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h2aa274; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h22be6b; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h2aa274; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h24bd6d; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h293244; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h24bd6b; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h21b176; end
                    6'd16: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd17: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd16: begin
                case (eff_col)
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h293143; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h293144; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h69e166; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h273343; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h22be6f; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h273343; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h29a374; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h2a3143; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h273343; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd17: begin
                case (eff_col)
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h2a3143; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h2aa274; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h273343; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h6ae065; end
                    6'd11: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd12: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h29a372; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd15: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd18: begin
                case (eff_col)
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h2a3143; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h2a3144; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h69e165; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h2a3143; end
                    6'd13: begin is_transparent = 1'b0; color_rgb = 24'h2a3143; end
                    6'd14: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd19: begin
                case (eff_col)
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h293243; end
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

// ----------------------------------------------------------------------------
// Module con 2: ROM Bông hoa đỏ (Red Flower 14x14)
// ----------------------------------------------------------------------------
module healing_flower_rom (
    input  wire [5:0]  row,
    input  wire [5:0]  col,
    input  wire        flip_h,
    output reg  [23:0] color_rgb,
    output reg         is_transparent
);
    localparam WIDTH = 6'd14;
    wire [5:0] eff_col = flip_h ? (WIDTH - 1'b1 - col) : col;

    always @(*) begin
        is_transparent = 1'b1;
        color_rgb      = 24'h000000;
        case (row)
            6'd3: begin
                case (eff_col)
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hd41b47; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hd41a49; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd4: begin
                case (eff_col)
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hd41a49; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h7f0c29; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hb4133a; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hd21b49; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hf22254; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd5: begin
                case (eff_col)
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hd11c49; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hd41b49; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h620a20; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h7b0f29; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hb1153a; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'hb3143d; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd6: begin
                case (eff_col)
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'hf62054; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hf22254; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'hd21b49; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'hb4133c; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'hb4143a; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd7: begin
                case (eff_col)
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'hd21b4b; end
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h438a60; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h357552; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd8: begin
                case (eff_col)
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h56a97b; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd9: begin
                case (eff_col)
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h57a87b; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd10: begin
                case (eff_col)
                    6'd4: begin is_transparent = 1'b0; color_rgb = 24'h438a60; end
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h5aa77d; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h56a97b; end
                    6'd9: begin is_transparent = 1'b0; color_rgb = 24'h5ba77b; end
                    6'd10: begin is_transparent = 1'b0; color_rgb = 24'h59a77b; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd11: begin
                case (eff_col)
                    6'd5: begin is_transparent = 1'b0; color_rgb = 24'h428a62; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h408b60; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h438a60; end
                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end
                endcase
            end
            6'd12: begin
                case (eff_col)
                    6'd6: begin is_transparent = 1'b0; color_rgb = 24'h438a62; end
                    6'd7: begin is_transparent = 1'b0; color_rgb = 24'h347652; end
                    6'd8: begin is_transparent = 1'b0; color_rgb = 24'h438a62; end
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

// ----------------------------------------------------------------------------
// Module chính: healing_items (Bộ chọn và điều khiển hiển thị vật phẩm hồi máu)
// ----------------------------------------------------------------------------
module healing_items (
    input  wire        item_id,        // 0: Green Herb (20x20), 1: Red Flower (14x14)
    input  wire [5:0]  row,            // Tọa độ hàng pixel
    input  wire [5:0]  col,            // Tọa độ cột pixel
    input  wire        flip_h,         // 1: Quay mặt / Lật ngang, 0: Bình thường
    output reg  [5:0]  width,          // Chiều rộng pixel
    output reg  [5:0]  height,         // Chiều cao pixel
    output reg  [23:0] color_rgb,      // Màu 24-bit RGB
    output reg         is_transparent  // 1: Nền trong suốt, 0: Có màu
);

    wire [23:0] herb_rgb, flower_rgb;
    wire        herb_trans, flower_trans;

    healing_herb_rom u_herb (
        .row(row),
        .col(col),
        .flip_h(flip_h),
        .color_rgb(herb_rgb),
        .is_transparent(herb_trans)
    );

    healing_flower_rom u_flower (
        .row(row),
        .col(col),
        .flip_h(flip_h),
        .color_rgb(flower_rgb),
        .is_transparent(flower_trans)
    );

    always @(*) begin
        case (item_id)
            1'b0: begin // Green Herb
                width          = 6'd20;
                height         = 6'd20;
                color_rgb      = herb_rgb;
                is_transparent = herb_trans;
            end
            1'b1: begin // Red Flower
                width          = 6'd14;
                height         = 6'd14;
                color_rgb      = flower_rgb;
                is_transparent = flower_trans;
            end
            default: begin
                width          = 6'd0;
                height         = 6'd0;
                color_rgb      = 24'h000000;
                is_transparent = 1'b1;
            end
        endcase
    end

endmodule
