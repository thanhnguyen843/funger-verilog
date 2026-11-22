// ============================================================================
// Module: monster_state_model.v
// Tri-State Monster Visual Model Architecture for Fear & Hunger Hardware RTL
// Standard: ISO/IEC/IEEE 29148:2018 Hardware-Software Co-Design
//
// Supports all 36 monsters across 3 physiological battle states:
//   - 2'b00 (0): NORMAL   - Full intact original sprite, healthy stance
//   - 2'b01 (1): INJURED  - Severed weapon arm, broken legs, blood lacerations
//   - 2'b10 (2): DEAD     - Decapitated neck, blood spray, fallen carcass/pool
//
// Hardware Principles:
//   - 0 non-power-of-2 divisions/modulos (100% compliant with TS. Nguyễn Đình Hãn)
//   - Fully synthesizable LUT/multiplexer logic with minimal gate overhead
// ============================================================================

`timescale 1ns / 1ps

module monster_state_model (
    input  wire [5:0] monster_id,     // 1 to 36
    input  wire [1:0] state,          // 2'b00: NORMAL, 2'b01: INJURED, 2'b10: DEAD
    input  wire [4:0] row,            // Tọa độ hàng: 0..25
    input  wire [4:0] col,            // Tọa độ cột:  0..24
    output reg        pixel_val,      // 1: Có điểm ảnh, 0: Trong suốt
    output wire       is_transparent, // 1 nếu là nền ngoài
    output reg  [4:0] width,          // Chiều rộng pixel
    output reg  [4:0] height,         // Chiều cao pixel
    output reg  [7:0] r,
    output reg  [7:0] g,
    output reg  [7:0] b
);

    assign is_transparent = !pixel_val;

    // ------------------------------------------------------------------------
    // Sub-module Instances: Retro Monsters (1..20) & Fantasy Creatures (21..36)
    // ------------------------------------------------------------------------
    wire [4:0] base_m_id = (monster_id >= 6'd1 && monster_id <= 6'd20) ? (monster_id[4:0] - 5'd1) : 5'd0;
    wire [3:0] base_fc_id = (monster_id >= 6'd21) ? (monster_id[3:0] - 4'd5) : 4'd0;

    wire       m_px, m_trans;
    wire [4:0] m_w, m_h;
    wire [7:0] m_r, m_g, m_b;

    monster u_base_mon (
        .monster_id(base_m_id),
        .row(row),
        .col(col),
        .pixel_val(m_px),
        .is_transparent(m_trans),
        .width(m_w),
        .height(m_h),
        .r(m_r),
        .g(m_g),
        .b(m_b)
    );

    wire       fc_px, fc_trans;
    wire [7:0] fc_r, fc_g, fc_b;

    fantasy_creatures u_base_fc (
        .creature_id(base_fc_id),
        .row(row[3:0]),
        .col(col[3:0]),
        .pixel_val(fc_px),
        .is_transparent(fc_trans),
        .r(fc_r),
        .g(fc_g),
        .b(fc_b)
    );

    // Multiplex base sprite output
    reg       raw_px;
    reg [4:0] raw_w, raw_h;
    reg [7:0] raw_r, raw_g, raw_b;

    always @(*) begin
        if (monster_id <= 6'd20) begin
            raw_px = m_px;
            raw_w  = m_w;
            raw_h  = m_h;
            raw_r  = m_r;
            raw_g  = m_g;
            raw_b  = m_b;
        end else begin
            raw_px = (row < 5'd16 && col < 5'd16) ? fc_px : 1'b0;
            raw_w  = 5'd16;
            raw_h  = 5'd16;
            raw_r  = fc_r;
            raw_g  = fc_g;
            raw_b  = fc_b;
        end
    end

    // ------------------------------------------------------------------------
    // Tri-State Transformation Logic
    // ------------------------------------------------------------------------
    always @(*) begin
        width  = raw_w;
        height = raw_h;

        case (state)
            // ================================================================
            // STATE 0: NORMAL (Mặc định lành lặn)
            // ================================================================
            2'b00: begin
                pixel_val = raw_px;
                r         = raw_r;
                g         = raw_g;
                b         = raw_b;
            end

            // ================================================================
            // STATE 1: INJURED (Bị chấn thương, chặt chi, rách thịt)
            // ================================================================
            2'b01: begin
                // Tước vũ khí / Chặt tay phải (cắt bỏ phần rìa phải từ giữa thân)
                if (col >= (raw_w - 5'd4) && row >= 5'd4 && row <= 5'd13) begin
                    pixel_val = 1'b0;
                    r = 8'd0; g = 8'd0; b = 8'd0;
                end
                // Bẻ gãy chân (cắt bỏ phần đáy để tạo tư thế khụy xuống sàn)
                else if (row >= (raw_h - 5'd3)) begin
                    // Chỉ giữ lại một vài vệt máu rải rác dưới sàn
                    if ((col == 5'd3 || col == 5'd7 || col == (raw_w - 5'd4)) && raw_px) begin
                        pixel_val = 1'b1;
                        r = 8'd220; g = 8'd20; b = 8'd30; // Máu tươi sàn đá
                    end else begin
                        pixel_val = 1'b0;
                        r = 8'd0; g = 8'd0; b = 8'd0;
                    end
                end
                // Vết thương cào rách chảy máu trên ngực/thân
                else if (raw_px && (row == 5'd7 || row == 5'd10) && (col[1:0] == 2'b01)) begin
                    pixel_val = 1'b1;
                    r = 8'd240; g = 8'd30; b = 8'd40; // Laceration wound (Blood red)
                end
                // Điểm cụt khớp tay vừa bị chặt (đầu khớp rỉ máu)
                else if (raw_px && col == (raw_w - 5'd5) && row >= 5'd6 && row <= 5'd8) begin
                    pixel_val = 1'b1;
                    r = 8'd255; g = 8'd10; b = 8'd20; // Amputation stump
                end
                // Thân thể còn lại: Ám màu đỏ thương tích nhẹ
                else if (raw_px) begin
                    pixel_val = 1'b1;
                    r = 8'd240;
                    g = 8'd160;
                    b = 8'd160;
                end else begin
                    pixel_val = 1'b0;
                    r = 8'd0; g = 8'd0; b = 8'd0;
                end
            end

            // ================================================================
            // STATE 2: DEAD (Tử trận, trảm thủ, sụp đổ vũng máu)
            // ================================================================
            2'b10: begin
                // Trảm đầu: Xóa toàn bộ phần đầu phía trên
                if (row < 5'd5) begin
                    // Vài giọt máu bắn tung tóe lên không trung khi bay đầu
                    if ((row == 5'd1 && col == 5'd6) || (row == 5'd2 && col == 5'd4) || (row == 5'd3 && col == 5'd9)) begin
                        pixel_val = 1'b1;
                        r = 8'd255; g = 8'd0; b = 8'd0; // Blood droplet
                    end else begin
                        pixel_val = 1'b0;
                        r = 8'd0; g = 8'd0; b = 8'd0;
                    end
                end
                // Vết chém đứt cổ: Phun máu đỏ rực ngang cổ
                else if (row == 5'd5 && col >= 5'd3 && col <= (raw_w - 5'd3)) begin
                    pixel_val = 1'b1;
                    r = 8'd255; g = 8'd20; b = 8'd30; // Severed neck blood fountain
                end
                // Vũng máu loang rộng dưới đáy sàn
                else if (row >= (raw_h - 5'd3)) begin
                    // Vũng máu trải dài ra 2 bên mép
                    if (col >= 5'd1 && col < (raw_w - 5'd1)) begin
                        pixel_val = 1'b1;
                        r = 8'd150; g = 8'd15; b = 8'd25; // Dark pooling blood
                    end else begin
                        pixel_val = 1'b0;
                        r = 8'd0; g = 8'd0; b = 8'd0;
                    end
                end
                // Thân xác tử thi: Co quắp, sẫm màu hoại tử xám tro
                else if (raw_px) begin
                    // Chỉ giữ lại một nửa độ cao thân xác (gục ngã)
                    if (row >= 5'd8) begin
                        pixel_val = 1'b1;
                        r = 8'd110; g = 8'd70; b = 8'd70; // Corpse ash-red
                    end else begin
                        pixel_val = 1'b0;
                        r = 8'd0; g = 8'd0; b = 8'd0;
                    end
                end else begin
                    pixel_val = 1'b0;
                    r = 8'd0; g = 8'd0; b = 8'd0;
                end
            end

            default: begin
                pixel_val = raw_px;
                r         = raw_r;
                g         = raw_g;
                b         = raw_b;
            end
        endcase
    end

endmodule
