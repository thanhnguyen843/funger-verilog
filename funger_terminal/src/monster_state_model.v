// ============================================================================
// Module: monster_state_model.v
// Tri-State Postural Morphology & Technical Amber Model Architecture
// Standard: ISO/IEC/IEEE 29148:2018 Hardware-Software Co-Design
//
// Designed for Academic Defense (Zero Gore, Zero Blood, Pure Architecture):
//   - 2'b00 (0): NORMAL   - Phosphor White (#FFFFFF), upright wielding posture
//   - 2'b01 (1): INJURED  - Technical Amber (#FFAA28), disarmed & crouched/crawling
//   - 2'b10 (2): DEAD     - Deactivated Ash Gray (#6E7378), decapitated & neutralized
//
// Hardware Principles:
//   - 0 non-power-of-2 divisions/modulos (100% compliant with TS. Nguyễn Đình Hãn)
//   - Row-shift logic (row - 4) for posture collapse + Bitwise arm coordinate masking
//   - 0 extra BRAM blocks used
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
    // Postural Row-Shift Mapping:
    // In INJURED state (2'b01), the monster crouches/crawls 4 rows lower.
    // ------------------------------------------------------------------------
    reg [4:0] query_row;
    always @(*) begin
        if (state == 2'b01) begin
            // Shift body down by 4 rows (crouch / crawling posture)
            if (row >= 5'd4)
                query_row = row - 5'd4;
            else
                query_row = 5'd31; // Above crouched body -> empty
        end else begin
            query_row = row;
        end
    end

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
        .row(query_row),
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
        .row(query_row[3:0]),
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

    always @(*) begin
        if (monster_id <= 6'd20) begin
            raw_px = (query_row < m_h) ? m_px : 1'b0;
            raw_w  = m_w;
            raw_h  = m_h;
        end else begin
            raw_px = (query_row < 5'd16 && col < 5'd16) ? fc_px : 1'b0;
            raw_w  = 5'd16;
            raw_h  = 5'd16;
        end
    end

    // ------------------------------------------------------------------------
    // Tri-State Posture & Amber Palette Transformation
    // ------------------------------------------------------------------------
    always @(*) begin
        width  = raw_w;
        height = raw_h;

        case (state)
            // ================================================================
            // STATE 0: NORMAL (Bright Phosphor White, Standing, Weapon In Hand)
            // ================================================================
            2'b00: begin
                pixel_val = raw_px;
                r         = 8'd255;
                g         = 8'd255;
                b         = 8'd255; // Clean Pure White (#FFFFFF)
            end

            // ================================================================
            // STATE 1: INJURED (Technical Amber, Disarmed, Crouched/Crawling)
            // ================================================================
            2'b01: begin
                if (query_row == 5'd31) begin
                    // Upper clearance above the crouched monster
                    pixel_val = 1'b0;
                    r = 8'd0; g = 8'd0; b = 8'd0;
                end
                // Chặt tay / Tước kiếm: Xóa cột cẳng tay và vũ khí bên phải
                else if (col >= (raw_w - 5'd4) && query_row >= 5'd4 && query_row <= 5'd13) begin
                    pixel_val = 1'b0;
                    r = 8'd0; g = 8'd0; b = 8'd0;
                end
                // Bẻ gãy chân: Cắt bỏ các hàng bàn chân cũ để ép sát sàn đá
                else if (query_row >= (raw_h - 5'd3)) begin
                    pixel_val = 1'b0;
                    r = 8'd0; g = 8'd0; b = 8'd0;
                end
                // Phần thân còn lại: Hiển thị nguyên vẹn với sắc Vàng Hổ Phách Cảnh Báo
                else if (raw_px) begin
                    pixel_val = 1'b1;
                    r         = 8'd255;
                    g         = 8'd180;
                    b         = 8'd40;  // Technical Warning Amber (#FFAA28)
                end else begin
                    pixel_val = 1'b0;
                    r = 8'd0; g = 8'd0; b = 8'd0;
                end
            end

            // ================================================================
            // STATE 2: DEAD (Deactivated Ash Gray, Decapitated, Neutralized)
            // ================================================================
            2'b10: begin
                // Trảm đầu: Xóa toàn bộ phần đầu phía trên
                if (row < 5'd6) begin
                    pixel_val = 1'b0;
                    r = 8'd0; g = 8'd0; b = 8'd0;
                end
                // Thân xác tử trận: Sụp đổ sát sàn, chuyển sang màu Xám Tro Tàn
                else if (raw_px && row >= 5'd8) begin
                    pixel_val = 1'b1;
                    r         = 8'd110;
                    g         = 8'd115;
                    b         = 8'd120; // Deactivated Ash Gray (#6E7378)
                end else begin
                    pixel_val = 1'b0;
                    r = 8'd0; g = 8'd0; b = 8'd0;
                end
            end

            default: begin
                pixel_val = raw_px;
                r         = 8'd255;
                g         = 8'd255;
                b         = 8'd255;
            end
        endcase
    end

endmodule
