// ============================================================================
// Pokemon Lite: Terror & Starvation - Top Level Module (battle_top.v)
// Tích hợp toàn bộ các khối phần cứng RTL:
//   - monster_rom (25 loài quái với chỉ số thực)
//   - sprite_rom  (25 models quái, 2 models items, narrator, title, game over)
//   - map_rom     (mê cung 60x80)
//   - collision_unit (va chạm tường & Defeated Tile Memory)
//   - rng_unit    (32-bit LFSR PRNG với weighted spawn 65% / 28% / 7%)
//   - damage_alu  (ma trận sát thương với DEF & 6.25% Crit)
//   - inventory_ram (đội hình Pals và vật phẩm sinh tồn)
//   - terminal_ui (đồ họa console ANSI với Combat Log)
// ============================================================================

`timescale 1ns / 1ps
`include "battle_defs.vh"

module battle_top (
    input  wire        clk,
    input  wire        rst_n,

    // Giao tiếp điều khiển từ Testbench / CPU
    input  wire        cmd_en,
    input  wire [3:0]  cmd_type,
    input  wire [7:0]  cmd_param1,
    input  wire [7:0]  cmd_param2,
    input  wire [7:0]  cmd_param3,

    // Xuất trạng thái hệ thống
    output wire [3:0]  game_state_out,
    output wire signed [31:0] player_x_out,
    output wire signed [31:0] player_y_out,
    output wire [31:0] step_count_out,

    output wire [5:0]  enemy_id_out,
    output wire [7:0]  enemy_hp_out,
    output wire [7:0]  enemy_max_hp_out,

    output wire [1:0]  active_pal_idx_out,
    output wire [4:0]  active_pal_id_out,
    output wire [7:0]  active_pal_hp_out,
    output wire [7:0]  active_pal_max_hp_out,

    output wire [4:0]  pal0_id_out,
    output wire [7:0]  pal0_hp_out,
    output wire [7:0]  pal0_max_hp_out,

    output wire [4:0]  pal1_id_out,
    output wire [7:0]  pal1_hp_out,
    output wire [7:0]  pal1_max_hp_out,

    output wire [4:0]  pal2_id_out,
    output wire [7:0]  pal2_hp_out,
    output wire [7:0]  pal2_max_hp_out,

    output wire [7:0]  normal_herb_qty_out,
    output wire [7:0]  strong_crys_qty_out,

    // Widen battle_turn from 4-bit to 8-bit
    output wire [7:0]  battle_turn_out,
    output wire [1:0]  battle_status_out,
    output wire        game_finished_out,
    output wire        is_victory_out,

    // Combat Log Outputs
    output wire [7:0]  last_dmg_dealt_out,
    output wire [7:0]  last_dmg_taken_out,
    output wire [2:0]  last_event_flag_out
);

    // ========================================================================
    // 1. THANH GHI TRẠNG THÁI NỘI BỘ
    // ========================================================================
    reg [3:0] state_reg;

    reg signed [31:0] player_x;
    reg signed [31:0] player_y;
    reg [31:0]        step_count;

    // 5 ứng viên Draft ngẫu nhiên
    reg [4:0] draft_candidates [0:4];

    // Trạng thái quái đối thủ
    reg [5:0] enemy_id_reg;
    reg [7:0] enemy_hp_reg;
    reg [7:0] enemy_max_hp_reg;
    reg [7:0] enemy_atk_reg;
    reg [7:0] enemy_def_reg;

    // Trạng thái trận đấu (8-bit turn counter)
    reg [7:0] battle_turn;
    reg [1:0] combat_status;
    reg       is_victory_flag;
    reg       is_game_over_flag;

    // Combat Log registers:
    // 0: Start, 1: Attack, 2: Defend, 3: Heal, 4: Flee failed, 5: Switch Pal
    reg [7:0] last_dmg_dealt;
    reg [7:0] last_dmg_taken;
    reg [2:0] last_event_flag;

    // Defeated Tile Memory (Circular Buffer of 16 coordinates)
    reg [3:0]   cleared_head;
    reg [15:0]  cleared_valid;
    reg [127:0] cleared_coords_x;
    reg [127:0] cleared_coords_y;

    // Tín hiệu điều khiển RAM
    reg       ram_draft_load;
    reg [4:0] ram_draft_p0_id;
    reg [4:0] ram_draft_p1_id;
    reg [4:0] ram_draft_p2_id;
    reg [7:0] ram_draft_p0_max;
    reg [7:0] ram_draft_p1_max;
    reg [7:0] ram_draft_p2_max;

    reg       ram_hp_update;
    reg [1:0] ram_target_idx;
    reg [7:0] ram_new_hp;
    reg       ram_item_consume;
    reg [3:0] ram_consume_type;
    reg [1:0] ram_active_idx_req;

    reg       ram_item_receive;
    reg [3:0] ram_recv_type;
    reg [7:0] ram_recv_qty;

    // ========================================================================
    // 2. KẾT NỐI CÁC MODULE CON
    // ========================================================================

    // Module Bộ nhớ Túi đồ & Đội hình
    wire [1:0] inv_active_idx;
    wire [3:0] inv_c0_id, inv_c1_id, inv_c2_id;
    wire [4:0] inv_p0_id = {1'b0, inv_c0_id};
    wire [4:0] inv_p1_id = {1'b0, inv_c1_id};
    wire [4:0] inv_p2_id = {1'b0, inv_c2_id};
    wire [7:0] inv_p0_hp, inv_p1_hp, inv_p2_hp;
    wire [7:0] inv_p0_max, inv_p1_max, inv_p2_max;
    wire [7:0] inv_normal_qty, inv_strong_qty;
    wire       inv_all_fainted;

    inventory_ram u_inv (
        .clk              (clk),
        .rst_n            (rst_n),
        .active_idx_in    (ram_active_idx_req),
        .active_idx_out   (inv_active_idx),
        .char0_id         (inv_c0_id),
        .char1_id         (inv_c1_id),
        .char2_id         (inv_c2_id),
        .char3_id         (),
        .char0_hp         (inv_p0_hp),
        .char1_hp         (inv_p1_hp),
        .char2_hp         (inv_p2_hp),
        .char3_hp         (),
        .char0_max_hp     (inv_p0_max),
        .char1_max_hp     (inv_p1_max),
        .char2_max_hp     (inv_p2_max),
        .char3_max_hp     (),
        .poppy_qty        (inv_normal_qty),
        .marijuana_qty    (inv_strong_qty),
        .key_qty          (),
        .draft_load_en    (ram_draft_load),
        .draft_c0_id      (ram_draft_p0_id[3:0]),
        .draft_c1_id      (ram_draft_p1_id[3:0]),
        .draft_c2_id      (ram_draft_p2_id[3:0]),
        .draft_c3_id      (4'd4),
        .draft_c0_max     (ram_draft_p0_max),
        .draft_c1_max     (ram_draft_p1_max),
        .draft_c2_max     (ram_draft_p2_max),
        .draft_c3_max     (8'd100),
        .hp_update_en     (ram_hp_update),
        .target_char_idx  (ram_target_idx),
        .new_hp_val       (ram_new_hp),
        .item_consume_en  (ram_item_consume),
        .consume_item_type(ram_consume_type),
        .item_receive_en  (ram_item_receive),
        .receive_item_type(ram_recv_type),
        .receive_amount   (ram_recv_qty),
        .team_all_fainted (inv_all_fainted)
    );

    // Module PRNG LFSR 32-bit (Weighted Spawns)
    wire [31:0] rng_val;
    wire        rng_flee_bit;
    wire [5:0]  rng_monster_roll;

    rng_unit u_rng (
        .clk            (clk),
        .rst_n          (rst_n),
        .step_en        (cmd_en),
        .seed_val       (32'h1984_ACE1),
        .lfsr_val       (rng_val),
        .rand_bit_50    (rng_flee_bit),
        .rand_monster_id(rng_monster_roll)
    );

    // Module CSDL quái vật thật từ monster_rom
    wire [5:0] rom_query_id = rng_monster_roll;
    wire [7:0] rom_hp, rom_atk, rom_def, rom_weight;
    wire       rom_is_default_elite;

    monster_rom u_mon_rom (
        .monster_id      (rom_query_id),
        .is_elite        (1'b0),
        .base_hp         (rom_hp),
        .base_atk        (rom_atk),
        .base_def        (rom_def),
        .spawn_weight    (rom_weight),
        .is_default_elite(rom_is_default_elite)
    );

    // Pal đang tham chiến hiện tại
    wire [4:0] cur_pal_id  = (inv_active_idx == 2'd0) ? inv_p0_id  : ((inv_active_idx == 2'd1) ? inv_p1_id  : inv_p2_id);
    wire [7:0] cur_pal_hp  = (inv_active_idx == 2'd0) ? inv_p0_hp  : ((inv_active_idx == 2'd1) ? inv_p1_hp  : inv_p2_hp);
    wire [7:0] cur_pal_max = (inv_active_idx == 2'd0) ? inv_p0_max : ((inv_active_idx == 2'd1) ? inv_p1_max : inv_p2_max);

    // Truy vấn chỉ số quái Pal đang chiến đấu
    reg [7:0] cur_pal_atk;
    reg [7:0] cur_pal_def;
    always @(*) begin
        case (cur_pal_id)
            5'd1:  begin cur_pal_atk = 8'd20; cur_pal_def = 8'd15; end
            5'd2:  begin cur_pal_atk = 8'd22; cur_pal_def = 8'd10; end
            5'd3:  begin cur_pal_atk = 8'd16; cur_pal_def = 8'd12; end
            5'd4:  begin cur_pal_atk = 8'd18; cur_pal_def = 8'd12; end
            5'd5:  begin cur_pal_atk = 8'd25; cur_pal_def = 8'd8;  end
            5'd6:  begin cur_pal_atk = 8'd18; cur_pal_def = 8'd22; end
            5'd7:  begin cur_pal_atk = 8'd24; cur_pal_def = 8'd8;  end
            5'd8:  begin cur_pal_atk = 8'd21; cur_pal_def = 8'd14; end
            5'd9:  begin cur_pal_atk = 8'd15; cur_pal_def = 8'd20; end
            5'd10: begin cur_pal_atk = 8'd20; cur_pal_def = 8'd14; end
            5'd11: begin cur_pal_atk = 8'd18; cur_pal_def = 8'd25; end
            5'd12: begin cur_pal_atk = 8'd22; cur_pal_def = 8'd11; end
            5'd13: begin cur_pal_atk = 8'd28; cur_pal_def = 8'd18; end
            5'd14: begin cur_pal_atk = 8'd19; cur_pal_def = 8'd16; end
            5'd15: begin cur_pal_atk = 8'd17; cur_pal_def = 8'd24; end
            5'd16: begin cur_pal_atk = 8'd19; cur_pal_def = 8'd17; end
            5'd17: begin cur_pal_atk = 8'd26; cur_pal_def = 8'd12; end
            5'd18: begin cur_pal_atk = 8'd20; cur_pal_def = 8'd16; end
            5'd19: begin cur_pal_atk = 8'd23; cur_pal_def = 8'd9;  end
            5'd20: begin cur_pal_atk = 8'd25; cur_pal_def = 8'd11; end
            5'd21: begin cur_pal_atk = 8'd19; cur_pal_def = 8'd26; end
            5'd22: begin cur_pal_atk = 8'd17; cur_pal_def = 8'd18; end
            5'd23: begin cur_pal_atk = 8'd24; cur_pal_def = 8'd19; end
            5'd24: begin cur_pal_atk = 8'd27; cur_pal_def = 8'd22; end
            5'd25: begin cur_pal_atk = 8'd30; cur_pal_def = 8'd25; end
            default: begin cur_pal_atk = 8'd20; cur_pal_def = 8'd10; end
        endcase
    end

    // Module Kiểm tra Va chạm Mê cung & Defeated Tile Memory
    wire signed [31:0] move_dx = (cmd_type == 4'd4 && (cmd_param1 == "a" || cmd_param1 == "A" || cmd_param1 == 8'd4)) ? -32'sd1 :
                                 ((cmd_type == 4'd4 && (cmd_param1 == "d" || cmd_param1 == "D" || cmd_param1 == 8'd6)) ?  32'sd1 : 32'sd0);
    wire signed [31:0] move_dy = (cmd_type == 4'd4 && (cmd_param1 == "w" || cmd_param1 == "W" || cmd_param1 == 8'd8)) ? -32'sd1 :
                                 ((cmd_type == 4'd4 && (cmd_param1 == "s" || cmd_param1 == "S" || cmd_param1 == 8'd2)) ?  32'sd1 : 32'sd0);
    wire signed [31:0] col_next_x, col_next_y;
    wire col_blocked, col_monster, col_chest, col_exit;
    wire [2:0] col_tile;

    collision_unit u_col (
        .curr_x          (player_x),
        .curr_y          (player_y),
        .dir_dx          (move_dx),
        .dir_dy          (move_dy),
        .cleared_valid   (cleared_valid),
        .cleared_coords_x(cleared_coords_x),
        .cleared_coords_y(cleared_coords_y),
        .cleared_mask    (720'd0),
        .next_x          (col_next_x),
        .next_y          (col_next_y),
        .is_blocked      (col_blocked),
        .is_monster      (col_monster),
        .is_chest        (col_chest),
        .is_gate         (col_exit),
        .dest_tile       (col_tile)
    );

    // Module Damage ALU với Phòng Thủ (DEF) và Chí Mạng (Crit 6.25%)
    wire [1:0] alu_p1_act = (state_reg == `STATE_BATTLE_LOOP && cmd_type == 4'd1) ? `ACTION_ATTACK :
                            ((state_reg == `STATE_BATTLE_LOOP && cmd_type == 4'd2) ? `ACTION_DEFEND :
                            ((state_reg == `STATE_BATTLE_LOOP && (cmd_type == 4'd3 || cmd_type == 4'd4)) ? `ACTION_ITEM_OR_FLEE : `ACTION_NONE));

    // Dynamic Enemy AI based on HP threshold and RNG
    reg [1:0] alu_p2_act;
    always @(*) begin
        if (enemy_hp_reg < (enemy_max_hp_reg >> 2)) begin
            // Critical HP (< 25%): 50% desperate guard, 50% all-out assault
            alu_p2_act = rng_val[1] ? `ACTION_DEFEND : `ACTION_ATTACK;
        end else begin
            // Normal HP: Alternate with pseudo-random seed variation
            alu_p2_act = (battle_turn[0] ^ rng_val[2]) ? `ACTION_ATTACK : `ACTION_DEFEND;
        end
    end

    wire       alu_flee_fail = (state_reg == `STATE_BATTLE_LOOP && cmd_type == 4'd4 && rng_flee_bit == 1'b0);
    wire [7:0] alu_dmg_to_p1, alu_dmg_to_p2, alu_flee_pen;

    damage_alu u_alu (
        .p1_action      (alu_p1_act),
        .p2_action      (alu_p2_act),
        .p1_base_atk    (cur_pal_atk),
        .p2_base_atk    (enemy_atk_reg),
        .p1_def         (cur_pal_def),
        .p2_def         (enemy_def_reg),
        .rng_bits       (rng_val[3:0]),
        .p1_curr_hp     (cur_pal_hp),
        .is_flee_failed (alu_flee_fail),
        .limb_target    (3'd0),
        .is_lethal_mode (1'b0),
        .enemy_disarmed (1'b0),
        .p1_damage      (alu_dmg_to_p1),
        .p2_damage      (alu_dmg_to_p2),
        .p1_flee_penalty(alu_flee_pen)
    );

    // Wires tính toán hồi phục máu & hồi sinh khi HP = 0
    wire [1:0] heal_target_idx = (cmd_param2 <= 8'd2) ? cmd_param2[1:0] : inv_active_idx;
    wire [7:0] heal_target_hp  = (heal_target_idx == 2'd0) ? inv_p0_hp :
                                 ((heal_target_idx == 2'd1) ? inv_p1_hp : inv_p2_hp);
    wire [7:0] heal_target_max = (heal_target_idx == 2'd0) ? inv_p0_max :
                                 ((heal_target_idx == 2'd1) ? inv_p1_max : inv_p2_max);

    // Normal Herb: +20 HP (nếu ngất thì hồi sinh lên 20 HP)
    wire [7:0] heal_calc_normal = (heal_target_hp + 8'd20 > heal_target_max) ?
                                  heal_target_max : (heal_target_hp + 8'd20);
    // Strong Crystal: +50 HP (nếu ngất thì hồi sinh lên 50 HP)
    wire [7:0] heal_calc_strong = (heal_target_hp + 8'd50 > heal_target_max) ?
                                  heal_target_max : (heal_target_hp + 8'd50);

    // Tính toán hồi máu khi mở túi ngoài map (dùng cmd_param1 làm target)
    wire [1:0] map_target_idx  = (cmd_param1 <= 8'd2) ? cmd_param1[1:0] : inv_active_idx;
    wire [7:0] map_target_hp   = (map_target_idx == 2'd0) ? inv_p0_hp :
                                 ((map_target_idx == 2'd1) ? inv_p1_hp : inv_p2_hp);
    wire [7:0] map_target_max  = (map_target_idx == 2'd0) ? inv_p0_max :
                                 ((map_target_idx == 2'd1) ? inv_p1_max : inv_p2_max);
    wire [7:0] map_heal_normal = (map_target_hp + 8'd20 > map_target_max) ?
                                 map_target_max : (map_target_hp + 8'd20);
    wire [7:0] map_heal_strong = (map_target_hp + 8'd50 > map_target_max) ?
                                 map_target_max : (map_target_hp + 8'd50);

    // ========================================================================
    // 3. FSM ĐIỀU KHIỂN HỆ THỐNG
    // ========================================================================
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state_reg         <= `STATE_TITLE;
            player_x          <= 32'd2;
            player_y          <= 32'd2;
            step_count        <= 32'd0;

            enemy_id_reg      <= 5'd1;
            enemy_hp_reg      <= 8'd100;
            enemy_max_hp_reg  <= 8'd100;
            enemy_atk_reg     <= 8'd20;
            enemy_def_reg     <= 8'd10;

            battle_turn       <= 8'd1;
            combat_status     <= `STATUS_ONGOING;
            is_victory_flag   <= 1'b0;
            is_game_over_flag <= 1'b0;

            last_dmg_dealt    <= 8'd0;
            last_dmg_taken    <= 8'd0;
            last_event_flag   <= 3'd0;

            cleared_head      <= 4'd0;
            cleared_valid     <= 16'd0;
            cleared_coords_x  <= 128'd0;
            cleared_coords_y  <= 128'd0;

            ram_draft_load    <= 1'b0;
            ram_draft_p0_id   <= 5'd1;
            ram_draft_p1_id   <= 5'd2;
            ram_draft_p2_id   <= 5'd6;
            ram_draft_p0_max  <= 8'd120;
            ram_draft_p1_max  <= 8'd95;
            ram_draft_p2_max  <= 8'd110;

            ram_hp_update     <= 1'b0;
            ram_target_idx    <= 2'd0;
            ram_new_hp        <= 8'd0;
            ram_item_consume  <= 1'b0;
            ram_consume_type  <= `ITEM_NORMAL;
            ram_active_idx_req<= 2'd0;

            ram_item_receive  <= 1'b0;
            ram_recv_type     <= 3'd0;
            ram_recv_qty      <= 8'd0;

            // 5 ứng viên Draft mẫu
            draft_candidates[0] <= 5'd1;  // Ursa-Apex
            draft_candidates[1] <= 5'd2;  // Hornowl
            draft_candidates[2] <= 5'd6;  // Megascarab
            draft_candidates[3] <= 5'd10; // Joecool
            draft_candidates[4] <= 5'd11; // Mechagolem
        end else begin
            // Mặc định hạ các xung điều khiển
            ram_draft_load   <= 1'b0;
            ram_hp_update    <= 1'b0;
            ram_item_consume <= 1'b0;
            ram_item_receive <= 1'b0;

            if (cmd_en) begin
                case (state_reg)
                    // Giai đoạn 1: Màn hình Bắt đầu (Title Screen)
                    `STATE_TITLE: begin
                        if (cmd_type == 4'd1) begin
                            state_reg <= `STATE_NARRATOR; // Bắt đầu game
                        end else if (cmd_type == 4'd2) begin
                            state_reg         <= `STATE_GAME_OVER; // Thoát game
                            is_game_over_flag <= 1'b1;
                        end
                    end

                    // Giai đoạn 2: Cốt truyện / Người Dẫn Chuyện (Narrator Lore)
                    `STATE_NARRATOR: begin
                        if (cmd_type == 4'd1) begin
                            state_reg <= `STATE_DRAFT; // Chuyển sang chọn bạn đồng hành
                        end
                    end

                    // Giai đoạn 3: Bốc thăm 3 Bạn đồng hành (Companion Draft)
                    `STATE_DRAFT: begin
                        ram_draft_p0_id <= draft_candidates[(cmd_param1 > 0 && cmd_param1 <= 5) ? (cmd_param1 - 1) : 0];
                        ram_draft_p1_id <= draft_candidates[(cmd_param2 > 0 && cmd_param2 <= 5) ? (cmd_param2 - 1) : 1];
                        ram_draft_p2_id <= draft_candidates[(cmd_param3 > 0 && cmd_param3 <= 5) ? (cmd_param3 - 1) : 2];

                        ram_draft_p0_max <= 8'd100;
                        ram_draft_p1_max <= 8'd100;
                        ram_draft_p2_max <= 8'd100;
                        ram_draft_load   <= 1'b1;

                        player_x  <= 32'd2;
                        player_y  <= 32'd2;
                        state_reg <= `STATE_MAP;
                    end

                    // Giai đoạn 4: Khám phá Mê cung 60x80
                    `STATE_MAP: begin
                        if (cmd_type == 4'd4) begin
                            if (!col_blocked) begin
                                player_x   <= col_next_x;
                                player_y   <= col_next_y;
                                step_count <= step_count + 1'b1;

                                if (col_exit) begin
                                    state_reg       <= `STATE_VICTORY;
                                    is_victory_flag <= 1'b1;
                                end else if (col_chest) begin
                                    // Tiếp tế hòm đồ: Nhận 1 Survival Herb và đánh dấu cleared
                                    ram_item_receive <= 1'b1;
                                    ram_recv_type    <= `ITEM_POPPY;
                                    ram_recv_qty     <= 8'd1;
                                    cleared_coords_x[cleared_head*8 +: 8] <= col_next_x[7:0];
                                    cleared_coords_y[cleared_head*8 +: 8] <= col_next_y[7:0];
                                    cleared_valid[cleared_head]           <= 1'b1;
                                    cleared_head                          <= (cleared_head + 1'b1) & 4'd15;
                                end else if (col_monster) begin
                                    // Đồng bộ chỉ số quái vật thật từ monster_rom
                                    enemy_id_reg     <= rng_monster_roll;
                                    enemy_hp_reg     <= rom_hp;
                                    enemy_max_hp_reg <= rom_hp;
                                    enemy_atk_reg    <= rom_atk;
                                    enemy_def_reg    <= rom_def;
                                    battle_turn      <= 8'd1;
                                    combat_status    <= `STATUS_ONGOING;
                                    last_dmg_dealt   <= 8'd0;
                                    last_dmg_taken   <= 8'd0;
                                    last_event_flag  <= 3'd0;
                                    state_reg        <= `STATE_BATTLE_LOOP;
                                end
                            end
                        end else if (cmd_type == 4'd5) begin
                            // Mở túi đồ trên map
                            state_reg <= `STATE_MAP_BAG;
                        end else if (cmd_type == 4'd0) begin
                            // Thoát game
                            state_reg         <= `STATE_GAME_OVER;
                            is_game_over_flag <= 1'b1;
                        end
                    end

                    // Giai đoạn 4.1: Mở Túi Đồ Ngoài Map
                    `STATE_MAP_BAG: begin
                        if (cmd_type == 4'd1) begin
                            // Dùng Normal Herb (+20 HP)
                            if (inv_normal_qty > 0 && cmd_param1 <= 8'd2) begin
                                ram_target_idx   <= map_target_idx;
                                ram_new_hp       <= map_heal_normal;
                                ram_hp_update    <= 1'b1;
                                ram_consume_type <= `ITEM_NORMAL;
                                ram_item_consume <= 1'b1;
                            end
                        end else if (cmd_type == 4'd2) begin
                            // Dùng Strong Crystal (+50 HP)
                            if (inv_strong_qty > 0 && cmd_param1 <= 8'd2) begin
                                ram_target_idx   <= map_target_idx;
                                ram_new_hp       <= map_heal_strong;
                                ram_hp_update    <= 1'b1;
                                ram_consume_type <= `ITEM_STRONG;
                                ram_item_consume <= 1'b1;
                            end
                        end else if (cmd_type == 4'd0) begin
                            // Đóng túi quay lại map
                            state_reg <= `STATE_MAP;
                        end
                    end

                    // Giai đoạn 5: Vòng Lặp Trận Đấu (Tactical Turn-Based Combat)
                    `STATE_BATTLE_LOOP: begin
                        case (cmd_type)
                            4'd1: begin // [1] Tấn công (Attack)
                                if (cur_pal_hp > 8'd0) begin
                                    if (enemy_hp_reg > alu_dmg_to_p2) begin
                                        enemy_hp_reg <= enemy_hp_reg - alu_dmg_to_p2;
                                        if (cur_pal_hp > alu_dmg_to_p1) begin
                                            ram_target_idx <= inv_active_idx;
                                            ram_new_hp     <= cur_pal_hp - alu_dmg_to_p1;
                                            ram_hp_update  <= 1'b1;
                                        end else begin
                                            ram_target_idx <= inv_active_idx;
                                            ram_new_hp     <= 8'd0;
                                            ram_hp_update  <= 1'b1;
                                        end
                                    end else begin
                                        enemy_hp_reg <= 8'd0;
                                        // Thắng trận tức thì trong chu kỳ hạ gục quái vật (Fix B2)
                                        cleared_coords_x[cleared_head*8 +: 8] <= player_x[7:0];
                                        cleared_coords_y[cleared_head*8 +: 8] <= player_y[7:0];
                                        cleared_valid[cleared_head]           <= 1'b1;
                                        cleared_head                          <= (cleared_head + 1'b1) & 4'd15;
                                        state_reg                             <= `STATE_MAP;
                                    end

                                    last_dmg_dealt  <= alu_dmg_to_p2;
                                    last_dmg_taken  <= alu_dmg_to_p1;
                                    last_event_flag <= 3'd1;
                                    battle_turn     <= battle_turn + 1'b1;
                                end else if (!inv_all_fainted) begin
                                    // Pal đã gục không thể tấn công, tự động đổi sang Pal còn sống (Fix B3)
                                    if (inv_p0_hp > 0)      ram_active_idx_req <= 2'd0;
                                    else if (inv_p1_hp > 0) ram_active_idx_req <= 2'd1;
                                    else if (inv_p2_hp > 0) ram_active_idx_req <= 2'd2;
                                end
                            end

                            4'd2: begin // [2] Phòng thủ (Defend)
                                if (cur_pal_hp > alu_dmg_to_p1) begin
                                    ram_target_idx <= inv_active_idx;
                                    ram_new_hp     <= cur_pal_hp - alu_dmg_to_p1;
                                    ram_hp_update  <= 1'b1;
                                end else begin
                                    ram_target_idx <= inv_active_idx;
                                    ram_new_hp     <= 8'd0;
                                    ram_hp_update  <= 1'b1;
                                end

                                last_dmg_dealt  <= 8'd0;
                                last_dmg_taken  <= alu_dmg_to_p1;
                                last_event_flag <= 3'd2;
                                battle_turn     <= battle_turn + 1'b1;
                            end

                            4'd3: begin // [3] Hồi Máu / Hồi Sinh bằng Túi Đồ
                                if (cmd_param1 == 8'd1 && inv_normal_qty > 0) begin
                                    ram_target_idx   <= heal_target_idx;
                                    ram_new_hp       <= heal_calc_normal;
                                    ram_hp_update    <= 1'b1;
                                    ram_consume_type <= `ITEM_NORMAL;
                                    ram_item_consume <= 1'b1;
                                    last_dmg_dealt   <= 8'd0;
                                    last_dmg_taken   <= alu_dmg_to_p1;
                                    last_event_flag  <= 3'd3;
                                    battle_turn      <= battle_turn + 1'b1;
                                end else if (cmd_param1 == 8'd2 && inv_strong_qty > 0) begin
                                    ram_target_idx   <= heal_target_idx;
                                    ram_new_hp       <= heal_calc_strong;
                                    ram_hp_update    <= 1'b1;
                                    ram_consume_type <= `ITEM_STRONG;
                                    ram_item_consume <= 1'b1;
                                    last_dmg_dealt   <= 8'd0;
                                    last_dmg_taken   <= alu_dmg_to_p1;
                                    last_event_flag  <= 3'd3;
                                    battle_turn      <= battle_turn + 1'b1;
                                end
                            end

                            4'd4: begin // [4] Bỏ Chạy (50%)
                                if (rng_flee_bit == 1'b1) begin
                                    // Bỏ chạy thành công -> thoát về map ngay
                                    state_reg <= `STATE_MAP;
                                end else begin
                                    // Bỏ chạy thất bại -> mất 30% HP hiện tại và chịu đòn địch
                                    if (cur_pal_hp > (alu_dmg_to_p1 + alu_flee_pen)) begin
                                        ram_target_idx <= inv_active_idx;
                                        ram_new_hp     <= cur_pal_hp - (alu_dmg_to_p1 + alu_flee_pen);
                                        ram_hp_update  <= 1'b1;
                                    end else begin
                                        ram_target_idx <= inv_active_idx;
                                        ram_new_hp     <= 8'd0;
                                        ram_hp_update  <= 1'b1;
                                    end

                                    last_dmg_dealt  <= 8'd0;
                                    last_dmg_taken  <= alu_dmg_to_p1 + alu_flee_pen;
                                    last_event_flag <= 3'd4;
                                    battle_turn     <= battle_turn + 1'b1;
                                end
                            end

                            4'd5: begin // [5] Đổi Quái Giữa Trận (Switch Pal Mid-Battle)
                                if (cmd_param1 <= 8'd2) begin
                                    ram_active_idx_req <= cmd_param1[1:0];
                                    last_dmg_dealt     <= 8'd0;
                                    last_dmg_taken     <= 8'd0;
                                    last_event_flag    <= 3'd5;
                                    battle_turn        <= battle_turn + 1'b1;
                                end
                            end
                        endcase

                        // Kiểm tra kết quả trận đấu sau hành động
                        if (enemy_hp_reg == 8'd0) begin
                            // Thắng trận! Lưu tọa độ vào Defeated Tile Memory
                            cleared_coords_x[cleared_head*8 +: 8] <= player_x[7:0];
                            cleared_coords_y[cleared_head*8 +: 8] <= player_y[7:0];
                            cleared_valid[cleared_head]           <= 1'b1;
                            cleared_head                          <= (cleared_head + 1'b1) & 4'd15;
                            state_reg                             <= `STATE_MAP;
                        end else if (inv_all_fainted && inv_normal_qty == 0 && inv_strong_qty == 0) begin
                            // Cả 3 Pals đều gục VÀ hết sạch thuốc -> Game Over
                            state_reg         <= `STATE_GAME_OVER;
                            is_game_over_flag <= 1'b1;
                        end else if (cur_pal_hp == 8'd0 && !inv_all_fainted) begin
                            // Tự động chuyển sang Pal còn sống đầu tiên
                            if (inv_p0_hp > 0)      ram_active_idx_req <= 2'd0;
                            else if (inv_p1_hp > 0) ram_active_idx_req <= 2'd1;
                            else if (inv_p2_hp > 0) ram_active_idx_req <= 2'd2;
                        end
                    end
                endcase
            end
        end
    end

    // Gán tín hiệu ngõ ra cho các cổng giao tiếp
    assign game_state_out        = state_reg;
    assign player_x_out          = player_x;
    assign player_y_out          = player_y;
    assign step_count_out        = step_count;

    assign enemy_id_out          = enemy_id_reg;
    assign enemy_hp_out          = enemy_hp_reg;
    assign enemy_max_hp_out      = enemy_max_hp_reg;

    assign active_pal_idx_out    = inv_active_idx;
    assign active_pal_id_out     = cur_pal_id;
    assign active_pal_hp_out     = cur_pal_hp;
    assign active_pal_max_hp_out = cur_pal_max;

    assign pal0_id_out           = inv_p0_id;
    assign pal0_hp_out           = inv_p0_hp;
    assign pal0_max_hp_out       = inv_p0_max;

    assign pal1_id_out           = inv_p1_id;
    assign pal1_hp_out           = inv_p1_hp;
    assign pal1_max_hp_out       = inv_p1_max;

    assign pal2_id_out           = inv_p2_id;
    assign pal2_hp_out           = inv_p2_hp;
    assign pal2_max_hp_out       = inv_p2_max;

    assign normal_herb_qty_out   = inv_normal_qty;
    assign strong_crys_qty_out   = inv_strong_qty;

    assign battle_turn_out       = battle_turn;
    assign battle_status_out     = combat_status;
    assign game_finished_out     = is_game_over_flag || is_victory_flag;
    assign is_victory_out        = is_victory_flag;

    assign last_dmg_dealt_out    = last_dmg_dealt;
    assign last_dmg_taken_out    = last_dmg_taken;
    assign last_event_flag_out   = last_event_flag;

endmodule
