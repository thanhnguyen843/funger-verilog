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

    output wire [4:0]  pal3_id_out,
    output wire [7:0]  pal3_hp_out,
    output wire [7:0]  pal3_max_hp_out,

    output wire [7:0]  normal_herb_qty_out,
    output wire [7:0]  strong_crys_qty_out,
    output wire [7:0]  key_qty_out,

    // Difficulty & Mode Flag (0: Fear & Hunger / Normal, 1: Terror & Starvation / Hardcore)
    output wire        is_hard_mode_out,

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
    reg       is_hard_mode_reg;
    assign is_hard_mode_out = is_hard_mode_reg;

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
    reg [7:0] defeated_monsters_count;
    reg [1:0] combat_status;
    reg       is_victory_flag;
    reg       is_game_over_flag;

    // Combat Log registers:
    // 0: Start, 1: Attack, 2: Defend, 3: Heal, 4: Flee failed, 5: Switch Pal
    reg [7:0] last_dmg_dealt;
    reg [7:0] last_dmg_taken;
    reg [2:0] last_event_flag;

    // Defeated Tile Memory (720-bit Full Mask + Circular Buffer of 16 coordinates)
    reg [719:0] cleared_mask;
    reg [3:0]   cleared_head;
    reg [15:0]  cleared_valid;
    reg [127:0] cleared_coords_x;
    reg [127:0] cleared_coords_y;

    // Tín hiệu điều khiển RAM
    reg       ram_draft_load;
    reg [4:0] ram_draft_p0_id;
    reg [4:0] ram_draft_p1_id;
    reg [4:0] ram_draft_p2_id;
    reg [4:0] ram_draft_p3_id;
    reg [7:0] ram_draft_p0_max;
    reg [7:0] ram_draft_p1_max;
    reg [7:0] ram_draft_p2_max;
    reg [7:0] ram_draft_p3_max;

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
    wire [3:0] inv_c0_id, inv_c1_id, inv_c2_id, inv_c3_id;
    wire [4:0] inv_p0_id = {1'b0, inv_c0_id};
    wire [4:0] inv_p1_id = {1'b0, inv_c1_id};
    wire [4:0] inv_p2_id = {1'b0, inv_c2_id};
    wire [4:0] inv_p3_id = {1'b0, inv_c3_id};
    wire [7:0] inv_p0_hp, inv_p1_hp, inv_p2_hp, inv_p3_hp;
    wire [7:0] inv_p0_max, inv_p1_max, inv_p2_max, inv_p3_max;
    wire [7:0] inv_normal_qty, inv_strong_qty, inv_key_qty;
    wire       inv_all_fainted;

    inventory_ram u_inv (
        .clk              (clk),
        .rst_n            (rst_n),
        .active_idx_in    (ram_active_idx_req),
        .active_idx_out   (inv_active_idx),
        .char0_id         (inv_c0_id),
        .char1_id         (inv_c1_id),
        .char2_id         (inv_c2_id),
        .char3_id         (inv_c3_id),
        .char0_hp         (inv_p0_hp),
        .char1_hp         (inv_p1_hp),
        .char2_hp         (inv_p2_hp),
        .char3_hp         (inv_p3_hp),
        .char0_max_hp     (inv_p0_max),
        .char1_max_hp     (inv_p1_max),
        .char2_max_hp     (inv_p2_max),
        .char3_max_hp     (inv_p3_max),
        .poppy_qty        (inv_normal_qty),
        .marijuana_qty    (inv_strong_qty),
        .key_qty          (inv_key_qty),
        .draft_load_en    (ram_draft_load),
        .draft_c0_id      (ram_draft_p0_id[3:0]),
        .draft_c1_id      (ram_draft_p1_id[3:0]),
        .draft_c2_id      (ram_draft_p2_id[3:0]),
        .draft_c3_id      (ram_draft_p3_id[3:0]),
        .draft_c0_max     (ram_draft_p0_max),
        .draft_c1_max     (ram_draft_p1_max),
        .draft_c2_max     (ram_draft_p2_max),
        .draft_c3_max     (ram_draft_p3_max),
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
        .is_elite        (is_hard_mode_reg ? (rom_is_default_elite || rng_val[7:6] == 2'b11) : rom_is_default_elite),
        .base_hp         (rom_hp),
        .base_atk        (rom_atk),
        .base_def        (rom_def),
        .spawn_weight    (rom_weight),
        .is_default_elite(rom_is_default_elite)
    );

    // Pal đang tham chiến hiện tại (4 nhân vật)
    wire [4:0] cur_pal_id  = (inv_active_idx == 2'd0) ? inv_p0_id  : ((inv_active_idx == 2'd1) ? inv_p1_id  : ((inv_active_idx == 2'd2) ? inv_p2_id : inv_p3_id));
    wire [7:0] cur_pal_hp  = (inv_active_idx == 2'd0) ? inv_p0_hp  : ((inv_active_idx == 2'd1) ? inv_p1_hp  : ((inv_active_idx == 2'd2) ? inv_p2_hp : inv_p3_hp));
    wire [7:0] cur_pal_max = (inv_active_idx == 2'd0) ? inv_p0_max : ((inv_active_idx == 2'd1) ? inv_p1_max : ((inv_active_idx == 2'd2) ? inv_p2_max : inv_p3_max));

    // Truy vấn chỉ số thật từ character_rom (Đồng bộ CSDL nhân vật)
    wire [7:0] rom_char_hp, rom_char_atk, rom_char_def;
    character_rom u_char_rom (
        .char_id     (cur_pal_id[3:0]),
        .is_hard_mode(is_hard_mode_reg),
        .char_hp     (rom_char_hp),
        .char_atk    (rom_char_atk),
        .char_def    (rom_char_def),
        .char_name   (),
        .char_class  ()
    );

    wire [7:0] cur_pal_atk = (cur_pal_id >= 5'd1 && cur_pal_id <= 5'd8) ? rom_char_atk : 8'd20;
    wire [7:0] cur_pal_def = (cur_pal_id >= 5'd1 && cur_pal_id <= 5'd8) ? rom_char_def : 8'd10;

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
        .cleared_mask    (cleared_mask),
        .next_x          (col_next_x),
        .next_y          (col_next_y),
        .is_blocked      (col_blocked),
        .is_monster      (col_monster),
        .is_chest        (col_chest),
        .is_gate         (col_exit),
        .dest_tile       (col_tile)
    );

    // Module Đồng xử lý Tư thế Chiến thuật (Tactical Stance Coprocessor)
    wire [1:0] top_curr_stance;
    wire [7:0] top_eff_atk, top_eff_def;
    wire [6:0] top_evasion_pct, top_flee_pct;
    wire [7:0] top_regen_hp;

    tactical_stance_unit u_stance (
        .clk              (clk),
        .rst_n            (rst_n),
        .stance_cmd_en    (state_reg == `STATE_BATTLE_LOOP && cmd_type == 4'd2),
        .stance_select    (cmd_param1[1:0]),
        .base_atk         (cur_pal_atk),
        .base_def         (cur_pal_def),
        .is_hard_mode     (is_hard_mode_reg),
        .curr_stance      (top_curr_stance),
        .eff_atk          (top_eff_atk),
        .eff_def          (top_eff_def),
        .evasion_pct      (top_evasion_pct),
        .flee_success_pct (top_flee_pct),
        .turn_regen_hp    (top_regen_hp)
    );

    // Module Đồng xử lý Tâm trí & Khắc nghiệt Môi trường (Sanity & Hunger Coprocessor)
    wire [7:0] top_mind_level, top_hunger_level;
    wire       top_is_panic, top_is_starving;
    wire [6:0] top_atk_penalty;
    wire       top_starve_pulse;

    sanity_meter_unit u_sanity (
        .clk                (clk),
        .rst_n              (rst_n),
        .is_hard_mode       (is_hard_mode_reg),
        .step_pulse         (state_reg == `STATE_MAP && cmd_type == 4'd4 && !col_blocked),
        .encounter_pulse    (state_reg == `STATE_MAP && col_monster),
        .panic_strike_pulse (1'b0),
        .mind_restore_en    (1'b0),
        .mind_restore_val   (8'd0),
        .hunger_restore_en  (1'b0),
        .hunger_restore_val (8'd0),
        .mind_level         (top_mind_level),
        .hunger_level       (top_hunger_level),
        .is_panic           (top_is_panic),
        .is_starving        (top_is_starving),
        .atk_penalty_pct    (top_atk_penalty),
        .starve_dmg_pulse   (top_starve_pulse)
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

    // Áp dụng Phạt hoảng loạn từ Sanity Coprocessor (giảm 12.5% công qua dịch bit >> 3, 0 phép chia)
    wire [7:0] pal_atk_after_sanity = top_is_panic ? (top_eff_atk - (top_eff_atk >> 3)) : top_eff_atk;

    // Giải mã bộ phận cơ thể (Limb targeting: 1=Head, 2=Torso, 3=ArmR, 4=ArmL, 5=Legs)
    wire [2:0] alu_limb_sel = (state_reg == `STATE_BATTLE_LOOP && cmd_type == 4'd1) ?
                              ((cmd_param1 == 8'd1) ? `LIMB_HEAD :
                               ((cmd_param1 == 8'd2) ? `LIMB_TORSO :
                                ((cmd_param1 == 8'd3) ? `LIMB_ARM_R :
                                 ((cmd_param1 == 8'd4) ? `LIMB_ARM_L :
                                  ((cmd_param1 == 8'd5) ? `LIMB_LEGS : cmd_param1[2:0]))))) : `LIMB_TORSO;

    damage_alu u_alu (
        .p1_action      (alu_p1_act),
        .p2_action      (alu_p2_act),
        .p1_base_atk    (pal_atk_after_sanity),
        .p2_base_atk    (enemy_atk_reg),
        .p1_def         (top_eff_def),
        .p2_def         (enemy_def_reg),
        .rng_bits       (rng_val[3:0]),
        .p1_curr_hp     (cur_pal_hp),
        .is_flee_failed (alu_flee_fail),
        .limb_target    (alu_limb_sel),
        .is_lethal_mode (1'b0),
        .enemy_disarmed (1'b0),
        .p1_damage      (alu_dmg_to_p1),
        .p2_damage      (alu_dmg_to_p2),
        .p1_flee_penalty(alu_flee_pen)
    );

    // Wires tính toán hồi phục máu & hồi sinh khi HP = 0 (Hỗ trợ đủ 4 nhân vật squad 0-3)
    wire [1:0] heal_target_idx = (cmd_param2 <= 8'd3) ? cmd_param2[1:0] : inv_active_idx;
    wire [7:0] heal_target_hp  = (heal_target_idx == 2'd0) ? inv_p0_hp :
                                 ((heal_target_idx == 2'd1) ? inv_p1_hp :
                                  ((heal_target_idx == 2'd2) ? inv_p2_hp : inv_p3_hp));
    wire [7:0] heal_target_max = (heal_target_idx == 2'd0) ? inv_p0_max :
                                 ((heal_target_idx == 2'd1) ? inv_p1_max :
                                  ((heal_target_idx == 2'd2) ? inv_p2_max : inv_p3_max));

    // Poppy Flower (+50 HP Normal, +30 HP Hardcore), Marijuana Herb (+120 HP Normal, +70 HP Hardcore)
    wire [7:0] poppy_heal_val = is_hard_mode_reg ? 8'd30 : 8'd50;
    wire [7:0] weed_heal_val  = is_hard_mode_reg ? 8'd70 : 8'd120;

    // Normal Herb: Poppy Flower (nếu ngất thì hồi sinh lên giá trị hồi phục)
    wire [7:0] heal_calc_normal = (heal_target_hp + poppy_heal_val > heal_target_max) ?
                                  heal_target_max : (heal_target_hp + poppy_heal_val);
    // Strong Crystal: Marijuana Herb (nếu ngất thì hồi sinh lên giá trị hồi phục)
    wire [7:0] heal_calc_strong = (heal_target_hp + weed_heal_val > heal_target_max) ?
                                  heal_target_max : (heal_target_hp + weed_heal_val);

    // Tính toán hồi máu khi mở túi ngoài map (dùng cmd_param1 làm target, hỗ trợ đủ 4 nhân vật)
    wire [1:0] map_target_idx  = (cmd_param1 <= 8'd3) ? cmd_param1[1:0] : inv_active_idx;
    wire [7:0] map_target_hp   = (map_target_idx == 2'd0) ? inv_p0_hp :
                                 ((map_target_idx == 2'd1) ? inv_p1_hp :
                                  ((map_target_idx == 2'd2) ? inv_p2_hp : inv_p3_hp));
    wire [7:0] map_target_max  = (map_target_idx == 2'd0) ? inv_p0_max :
                                 ((map_target_idx == 2'd1) ? inv_p1_max :
                                  ((map_target_idx == 2'd2) ? inv_p2_max : inv_p3_max));
    wire [7:0] map_heal_normal = (map_target_hp + poppy_heal_val > map_target_max) ?
                                 map_target_max : (map_target_hp + poppy_heal_val);
    wire [7:0] map_heal_strong = (map_target_hp + weed_heal_val > map_target_max) ?
                                 map_target_max : (map_target_hp + weed_heal_val);

    // Chỉ số máu gốc (Base HP) của 4 nhân vật trước khi nhân hệ số chế độ chơi
    wire [7:0] raw_draft_p0_max = ((cmd_param1 == 8'd2) ? 8'd145 : ((cmd_param1 == 8'd3) ? 8'd95 : ((cmd_param1 == 8'd4) ? 8'd155 : ((cmd_param1 == 8'd5) ? 8'd130 : 8'd125))));
    wire [7:0] raw_draft_p1_max = ((cmd_param2 == 8'd1) ? 8'd125 : ((cmd_param2 == 8'd3) ? 8'd95 : ((cmd_param2 == 8'd4) ? 8'd155 : ((cmd_param2 == 8'd5) ? 8'd130 : 8'd145))));
    wire [7:0] raw_draft_p2_max = ((cmd_param3 == 8'd1) ? 8'd125 : ((cmd_param3 == 8'd2) ? 8'd145 : ((cmd_param3 == 8'd4) ? 8'd155 : ((cmd_param3 == 8'd5) ? 8'd130 : 8'd95))));
    wire [7:0] raw_draft_p3_max = 8'd155; // Ragnvaldr

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
            defeated_monsters_count <= 8'd0;
            combat_status     <= `STATUS_ONGOING;
            is_victory_flag   <= 1'b0;
            is_game_over_flag <= 1'b0;
            is_hard_mode_reg  <= 1'b0;

            last_dmg_dealt    <= 8'd0;
            last_dmg_taken    <= 8'd0;
            last_event_flag   <= 3'd0;

            cleared_mask      <= 720'd0;
            cleared_head      <= 4'd0;
            cleared_valid     <= 16'd0;
            cleared_coords_x  <= 128'd0;
            cleared_coords_y  <= 128'd0;

            ram_draft_load    <= 1'b0;
            ram_draft_p0_id   <= 5'd1;
            ram_draft_p1_id   <= 5'd2;
            ram_draft_p2_id   <= 5'd3;
            ram_draft_p3_id   <= 5'd4;
            ram_draft_p0_max  <= 8'd125;
            ram_draft_p1_max  <= 8'd145;
            ram_draft_p2_max  <= 8'd95;
            ram_draft_p3_max  <= 8'd155;

            ram_hp_update     <= 1'b0;
            ram_target_idx    <= 2'd0;
            ram_new_hp        <= 8'd0;
            ram_item_consume  <= 1'b0;
            ram_consume_type  <= `ITEM_NORMAL;
            ram_active_idx_req<= 2'd0;

            ram_item_receive  <= 1'b0;
            ram_recv_type     <= 3'd0;
            ram_recv_qty      <= 8'd0;

            // 5 ứng viên Draft Fear & Hunger
            draft_candidates[0] <= 5'd1;  // Cahara
            draft_candidates[1] <= 5'd2;  // D'arce
            draft_candidates[2] <= 5'd3;  // Enki
            draft_candidates[3] <= 5'd4;  // Ragnvaldr
            draft_candidates[4] <= 5'd5;  // Le'garde
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
                            // cmd_param1 lựa chọn độ khó: 2/'2'/'h'/'H' = Terror & Starvation (Hardcore); else = Fear & Hunger (Normal)
                            if (cmd_param1 == 8'd2 || cmd_param1 == "2" || cmd_param1 == "h" || cmd_param1 == "H") begin
                                is_hard_mode_reg <= 1'b1;
                            end else begin
                                is_hard_mode_reg <= 1'b0;
                            end
                            state_reg <= `STATE_NARRATOR; // Bắt đầu game
                        end else if (cmd_type == 4'd2) begin
                            state_reg         <= `STATE_GAME_OVER; // Thoát game
                            is_game_over_flag <= 1'b1;
                        end
                    end

                    // Giai đoạn 2: Cốt truyện / Người Dẫn Chuyện (Narrator Lore)
                    `STATE_NARRATOR: begin
                        if (cmd_type == 4'd1) begin
                            if (cmd_param1 == 8'd2 || cmd_param1 == "2" || cmd_param1 == "h" || cmd_param1 == "H")
                                is_hard_mode_reg <= 1'b1;
                            else if (cmd_param1 == 8'd1 || cmd_param1 == "1" || cmd_param1 == "n" || cmd_param1 == "N")
                                is_hard_mode_reg <= 1'b0;
                            state_reg <= `STATE_DRAFT; // Chuyển sang chọn bạn đồng hành
                        end
                    end

                    // Giai đoạn 3: Bốc thăm Bạn đồng hành (Companion Draft)
                    `STATE_DRAFT: begin
                        ram_draft_p0_id <= draft_candidates[(cmd_param1 > 0 && cmd_param1 <= 5) ? (cmd_param1 - 1) : 0];
                        ram_draft_p1_id <= draft_candidates[(cmd_param2 > 0 && cmd_param2 <= 5) ? (cmd_param2 - 1) : 1];
                        ram_draft_p2_id <= draft_candidates[(cmd_param3 > 0 && cmd_param3 <= 5) ? (cmd_param3 - 1) : 2];
                        ram_draft_p3_id <= draft_candidates[3];

                        ram_draft_p0_max <= is_hard_mode_reg ? raw_draft_p0_max : (raw_draft_p0_max + (raw_draft_p0_max >> 2));
                        ram_draft_p1_max <= is_hard_mode_reg ? raw_draft_p1_max : (raw_draft_p1_max + (raw_draft_p1_max >> 2));
                        ram_draft_p2_max <= is_hard_mode_reg ? raw_draft_p2_max : (raw_draft_p2_max + (raw_draft_p2_max >> 2));
                        ram_draft_p3_max <= is_hard_mode_reg ? raw_draft_p3_max : (raw_draft_p3_max + (raw_draft_p3_max >> 2));
                        ram_draft_load   <= 1'b1;

                        player_x  <= 32'd2;
                        player_y  <= 32'd2;
                        state_reg <= `STATE_MAP;
                    end

                    // Giai đoạn 4: Khám phá Mê cung 60x80
                    `STATE_MAP: begin
                        if (cmd_type == 4'd4) begin
                            if (!col_blocked) begin
                                step_count <= step_count + 1'b1;

                                if (col_exit) begin
                                    if (inv_key_qty >= 8'd3) begin
                                        player_x        <= col_next_x;
                                        player_y        <= col_next_y;
                                        state_reg       <= `STATE_VICTORY;
                                        is_victory_flag <= 1'b1;
                                    end else begin
                                        // Cổng ngục tối yêu cầu đủ 3 chìa khóa Runic Key! Giữ nguyên vị trí, không lọt vào tường biên
                                        last_event_flag <= 3'd4;
                                    end
                                end else if (col_chest) begin
                                    player_x <= col_next_x;
                                    player_y <= col_next_y;
                                    // Tiếp tế hòm đồ: Rơi Chìa khóa Runic Key (nếu chưa đủ 3) hoặc Poppy / Marijuana
                                    ram_item_receive <= 1'b1;
                                    if (inv_key_qty < 8'd3 && rng_val[0]) begin
                                        ram_recv_type <= `ITEM_KEY;
                                        ram_recv_qty  <= 8'd1;
                                    end else if (rng_val[1]) begin
                                        ram_recv_type <= `ITEM_MARIJUANA;
                                        ram_recv_qty  <= 8'd1;
                                    end else begin
                                        ram_recv_type <= `ITEM_POPPY;
                                        ram_recv_qty  <= 8'd1;
                                    end
                                    cleared_coords_x[cleared_head*8 +: 8] <= col_next_x[7:0];
                                    cleared_coords_y[cleared_head*8 +: 8] <= col_next_y[7:0];
                                    cleared_valid[cleared_head]           <= 1'b1;
                                    cleared_head                          <= (cleared_head + 1'b1) & 4'd15;
                                    if (col_next_y * `MAP_WIDTH + col_next_x >= 0 && col_next_y * `MAP_WIDTH + col_next_x < 720)
                                        cleared_mask[col_next_y * `MAP_WIDTH + col_next_x] <= 1'b1;
                                end else if (col_monster) begin
                                    player_x <= col_next_x;
                                    player_y <= col_next_y;
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
                                end else begin
                                    player_x <= col_next_x;
                                    player_y <= col_next_y;
                                end

                                // Xung sát thương đói khát (Starvation damage) khi đói >= 90%
                                if (top_starve_pulse && cur_pal_hp > 8'd5) begin
                                    ram_target_idx <= inv_active_idx;
                                    ram_new_hp     <= cur_pal_hp - 8'd5;
                                    ram_hp_update  <= 1'b1;
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
                            if (inv_normal_qty > 0 && cmd_param1 <= 8'd3) begin
                                ram_target_idx   <= map_target_idx;
                                ram_new_hp       <= map_heal_normal;
                                ram_hp_update    <= 1'b1;
                                ram_consume_type <= `ITEM_NORMAL;
                                ram_item_consume <= 1'b1;
                            end
                        end else if (cmd_type == 4'd2) begin
                            // Dùng Strong Crystal (+50 HP)
                            if (inv_strong_qty > 0 && cmd_param1 <= 8'd3) begin
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
                                        if (player_y * `MAP_WIDTH + player_x >= 0 && player_y * `MAP_WIDTH + player_x < 720)
                                            cleared_mask[player_y * `MAP_WIDTH + player_x] <= 1'b1;

                                        // Rơi chìa khóa Runic Key khi diệt quái (Hệ thống Pity quái 3, 6, 8 hoặc 37.5% RNG)
                                        if (inv_key_qty < 8'd3 && (defeated_monsters_count == 8'd2 || defeated_monsters_count == 8'd5 || defeated_monsters_count == 8'd7 || rng_val[3:0] < 4'd6)) begin
                                            ram_item_receive <= 1'b1;
                                            ram_recv_type    <= `ITEM_KEY;
                                            ram_recv_qty     <= 8'd1;
                                        end
                                        defeated_monsters_count <= defeated_monsters_count + 8'd1;
                                        state_reg                             <= `STATE_MAP;
                                    end

                                    last_dmg_dealt  <= alu_dmg_to_p2;
                                    last_dmg_taken  <= alu_dmg_to_p1;
                                    last_event_flag <= 3'd1;
                                    battle_turn     <= battle_turn + 1'b1;
                                end else if (!inv_all_fainted) begin
                                    // Pal đã gục không thể tấn công, tự động đổi sang Pal còn sống (Fix B3, hỗ trợ 4 nhân vật)
                                    if (inv_p0_hp > 0)      ram_active_idx_req <= 2'd0;
                                    else if (inv_p1_hp > 0) ram_active_idx_req <= 2'd1;
                                    else if (inv_p2_hp > 0) ram_active_idx_req <= 2'd2;
                                    else if (inv_p3_hp > 0) ram_active_idx_req <= 2'd3;
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

                            4'd5: begin // [5] Đổi Quái Giữa Trận (Switch Pal Mid-Battle, hỗ trợ slot 0-3)
                                if (cmd_param1 <= 8'd3) begin
                                    ram_active_idx_req <= cmd_param1[1:0];
                                    last_dmg_dealt     <= 8'd0;
                                    last_dmg_taken     <= 8'd0;
                                    last_event_flag    <= 3'd5;
                                    battle_turn        <= battle_turn + 1'b1;
                                end
                            end
                        endcase

                        // Kiểm tra kết quả trận đấu sau hành động
                        if (inv_all_fainted) begin
                            // Cả đội hình Pals đều gục -> Game Over (loại bỏ bẫy kẹt soft-lock khi còn thuốc)
                            state_reg         <= `STATE_GAME_OVER;
                            is_game_over_flag <= 1'b1;
                        end else if (cur_pal_hp == 8'd0) begin
                            // Tự động chuyển sang Pal còn sống đầu tiên (hỗ trợ slot 0-3)
                            if (inv_p0_hp > 0)      ram_active_idx_req <= 2'd0;
                            else if (inv_p1_hp > 0) ram_active_idx_req <= 2'd1;
                            else if (inv_p2_hp > 0) ram_active_idx_req <= 2'd2;
                            else if (inv_p3_hp > 0) ram_active_idx_req <= 2'd3;
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

    assign pal3_id_out           = inv_p3_id;
    assign pal3_hp_out           = inv_p3_hp;
    assign pal3_max_hp_out       = inv_p3_max;

    assign normal_herb_qty_out   = inv_normal_qty;
    assign strong_crys_qty_out   = inv_strong_qty;
    assign key_qty_out           = inv_key_qty;

    assign battle_turn_out       = battle_turn;
    assign battle_status_out     = combat_status;
    assign game_finished_out     = is_game_over_flag || is_victory_flag;
    assign is_victory_out        = is_victory_flag;

    assign last_dmg_dealt_out    = last_dmg_dealt;
    assign last_dmg_taken_out    = last_dmg_taken;
    assign last_event_flag_out   = last_event_flag;

endmodule
