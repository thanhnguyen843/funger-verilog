// ============================================================================
// Pokemon Lite: Terror & Starvation - Inventory & Team RAM (inventory_ram.v)
// Manages:
//   - 4-Character Squad (Cahara, D'arce, Enki, Ragnvaldr, etc.)
//   - Initial Supplies: 10 Poppy, 3 Marijuana, 0 Dungeon Keys
//   - Healing amounts: Poppy (+30 HP), Marijuana (+70 HP)
//   - Item Reception: Loot from chests & monster drops (Key, Poppy, Marijuana)
//   - Item Consumption: Out-of-combat (Map) & In-combat (Turn action)
// ============================================================================

`include "battle_defs.vh"

module inventory_ram (
    input  wire        clk,
    input  wire        rst_n,

    // Active battler index (0 to 3)
    input  wire [1:0]  active_idx_in,
    output wire [1:0]  active_idx_out,

    // 4 Squad Character IDs (1 to 8)
    output wire [3:0]  char0_id,
    output wire [3:0]  char1_id,
    output wire [3:0]  char2_id,
    output wire [3:0]  char3_id,

    // 4 Squad Dynamic Current HP
    output wire [7:0]  char0_hp,
    output wire [7:0]  char1_hp,
    output wire [7:0]  char2_hp,
    output wire [7:0]  char3_hp,

    // 4 Squad Maximum HP Limits
    output wire [7:0]  char0_max_hp,
    output wire [7:0]  char1_max_hp,
    output wire [7:0]  char2_max_hp,
    output wire [7:0]  char3_max_hp,

    // Inventory Quantities
    output wire [7:0]  poppy_qty,
    output wire [7:0]  marijuana_qty,
    output wire [7:0]  key_qty,

    // Control Strobes: Load 4 Chosen Characters
    input  wire        draft_load_en,
    input  wire [3:0]  draft_c0_id, draft_c1_id, draft_c2_id, draft_c3_id,
    input  wire [7:0]  draft_c0_max, draft_c1_max, draft_c2_max, draft_c3_max,

    // Control Strobe: Update HP (Damage or Heal)
    input  wire        hp_update_en,
    input  wire [1:0]  target_char_idx,
    input  wire [7:0]  new_hp_val,

    // Control Strobe: Consume Item
    input  wire        item_consume_en,
    input  wire [2:0]  consume_item_type, // ITEM_POPPY, ITEM_MARIJUANA

    // Control Strobe: Receive Item (From Chest or Monster Drop)
    input  wire        item_receive_en,
    input  wire [2:0]  receive_item_type, // ITEM_POPPY, ITEM_MARIJUANA, ITEM_KEY
    input  wire [7:0]  receive_amount,

    output wire        team_all_fainted
);

    reg [1:0]  r_active_idx;

    reg [3:0]  r_char_id  [0:3];
    reg [7:0]  r_char_hp  [0:3];
    reg [7:0]  r_char_max [0:3];

    reg [7:0]  r_poppy_qty;
    reg [7:0]  r_marijuana_qty;
    reg [7:0]  r_key_qty;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            r_active_idx <= 2'd0;

            r_char_id[0] <= 4'd1; r_char_hp[0] <= 8'd110; r_char_max[0] <= 8'd110; // Cahara
            r_char_id[1] <= 4'd2; r_char_hp[1] <= 8'd130; r_char_max[1] <= 8'd130; // D'arce
            r_char_id[2] <= 4'd3; r_char_hp[2] <= 8'd85;  r_char_max[2] <= 8'd85;  // Enki
            r_char_id[3] <= 4'd4; r_char_hp[3] <= 8'd140; r_char_max[3] <= 8'd140; // Ragnvaldr

            // Bắt đầu game: Luôn luôn có 10 Poppy và 3 Marijuana, 0 Chìa khóa
            r_poppy_qty     <= 8'd10;
            r_marijuana_qty <= 8'd3;
            r_key_qty       <= 8'd0;
        end else begin
            // 1. Tải đội hình 4 nhân vật từ màn hình chọn
            if (draft_load_en) begin
                r_char_id[0]  <= draft_c0_id;
                r_char_id[1]  <= draft_c1_id;
                r_char_id[2]  <= draft_c2_id;
                r_char_id[3]  <= draft_c3_id;

                r_char_max[0] <= draft_c0_max;
                r_char_max[1] <= draft_c1_max;
                r_char_max[2] <= draft_c2_max;
                r_char_max[3] <= draft_c3_max;

                r_char_hp[0]  <= draft_c0_max;
                r_char_hp[1]  <= draft_c1_max;
                r_char_hp[2]  <= draft_c2_max;
                r_char_hp[3]  <= draft_c3_max;

                r_active_idx  <= 2'd0;
            end

            // 2. Cập nhật HP nhân vật
            if (hp_update_en) begin
                r_char_hp[target_char_idx] <= new_hp_val;
            end

            // 3. Tiêu hao vật phẩm hồi máu
            if (item_consume_en) begin
                if (consume_item_type == `ITEM_POPPY && r_poppy_qty > 8'd0)
                    r_poppy_qty <= r_poppy_qty - 8'd1;
                else if (consume_item_type == `ITEM_MARIJUANA && r_marijuana_qty > 8'd0)
                    r_marijuana_qty <= r_marijuana_qty - 8'd1;
            end

            // 4. Nhận vật phẩm (Rương mở hoặc Quái rớt)
            if (item_receive_en) begin
                if (receive_item_type == `ITEM_POPPY)
                    r_poppy_qty <= r_poppy_qty + receive_amount;
                else if (receive_item_type == `ITEM_MARIJUANA)
                    r_marijuana_qty <= r_marijuana_qty + receive_amount;
                else if (receive_item_type == `ITEM_KEY)
                    r_key_qty <= r_key_qty + receive_amount;
            end

            // 5. Đổi nhân vật chiến đấu active
            r_active_idx <= active_idx_in;
        end
    end

    // Gán tín hiệu ngõ ra
    assign active_idx_out = r_active_idx;

    assign char0_id       = r_char_id[0];
    assign char1_id       = r_char_id[1];
    assign char2_id       = r_char_id[2];
    assign char3_id       = r_char_id[3];

    assign char0_hp       = r_char_hp[0];
    assign char1_hp       = r_char_hp[1];
    assign char2_hp       = r_char_hp[2];
    assign char3_hp       = r_char_hp[3];

    assign char0_max_hp   = r_char_max[0];
    assign char1_max_hp   = r_char_max[1];
    assign char2_max_hp   = r_char_max[2];
    assign char3_max_hp   = r_char_max[3];

    assign poppy_qty      = r_poppy_qty;
    assign marijuana_qty  = r_marijuana_qty;
    assign key_qty        = r_key_qty;

    // Kiểm tra toàn đội ngã gục
    assign team_all_fainted = (r_char_hp[0] == 8'd0) && (r_char_hp[1] == 8'd0) &&
                              (r_char_hp[2] == 8'd0) && (r_char_hp[3] == 8'd0);

endmodule
