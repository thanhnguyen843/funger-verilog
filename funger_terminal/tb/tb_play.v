// ============================================================================
// Interactive Gameplay Testbench: tb_play.v
// Fear & Hunger: Terminal Labyrinth - Pure Verilog Solo Explorer Edition
// Hardware-Accelerated RTL Gameplay Matching Python Solo Explorer UX 1:1:
//   1. Boxed Title & Difficulty Selection ([W/S] + [Enter], Zero Yellow Glare)
//   2. Dual Split-Box Solo Hero Selector (1 of 8 Heroes + Live Sprite Model)
//   3. 36x20 Labyrinth Map (2-Tier Torchlight, # Barricade, Seal, Crevice, [G] Guide)
//   4. Dual Split-Box Survival Pouch ([I], Hero Model, 4 Bars, 8 Items + Totem)
//   5. Pokemon-Style Solo Combat Arena (5-Option Hierarchical Menu, Limb Targeting,
//      4 Hero Skills, Tri-State Monster Model, Coin Flip, Hero Asymmetry)
//   6. Zero Scroll & Zero Prompt Overflow (<= 29 Rows x 100 Cols)
// ============================================================================

`timescale 1ns / 1ps
`include "battle_defs.vh"

module tb_play;

    reg clk;
    reg rst_n;

    always #5 clk = ~clk;

    // Submodules (ROM Databases & UI Peripheral)
    terminal_ui   ui();
    character_rom char_db(.char_id(4'd1), .is_hard_mode(1'b0), .char_hp(), .char_atk(), .char_def(), .char_name(), .char_class());
    map_rom       map_db(.in_x(32'sd0), .in_y(32'sd0), .out_tile());

    reg  [5:0] mon_lookup_id;
    reg        mon_lookup_elite;
    wire [7:0] mon_rom_hp, mon_rom_atk, mon_rom_def, mon_rom_weight;
    wire       mon_rom_def_elite;
    wire [1:0] mon_rom_arch;

    monster_rom mon_db (
        .monster_id      (mon_lookup_id),
        .is_elite        (mon_lookup_elite),
        .base_hp         (mon_rom_hp),
        .base_atk        (mon_rom_atk),
        .base_def        (mon_rom_def),
        .spawn_weight    (mon_rom_weight),
        .is_default_elite(mon_rom_def_elite),
        .archetype       (mon_rom_arch)
    );

    // Solo Explorer State
    reg [3:0]   hero_id;
    reg [127:0] hero_name;
    reg [191:0] hero_role, dummy_pr, dummy_mr;
    reg [255:0] hero_trait_s, hero_buff_s;
    reg [479:0] dummy_a1, dummy_a2;
    reg [7:0]   hero_hp, hero_max;
    reg [7:0]   hero_atk, hero_def, hero_dodge, hero_bag_cap;
    reg [7:0]   hero_mind, hero_max_mind;
    reg [7:0]   hero_hunger;
    reg [7:0]   hero_tox, hero_max_tox;
    reg         hero_is_guarding;
    reg         hero_has_bleed;
    reg         hero_has_poison;
    reg         limb_head, limb_torso, limb_arm_r, limb_arm_l, limb_legs;
    reg [2:0]   legarde_ale_buff_turns;
    reg [2:0]   scent_dodge_turns;
    reg         girl_100_dodge;
    reg         foe_half_atk_debuff;

    // Solo Survival Satchel (8 Slots Unified)
    reg [7:0]   bag_totem;
    reg [7:0]   bag_poppy;
    reg [7:0]   bag_herb;
    reg [7:0]   bag_bread;
    reg [7:0]   bag_meat;
    reg [7:0]   bag_vial;
    reg [7:0]   bag_keys;

    // Player & Map State
    reg signed [31:0] player_x;
    reg signed [31:0] player_y;
    reg [31:0]        step_count;
    reg [31:0]        monsters_defeated_count;
    reg [31:0]        chests_looted_count;
    reg [719:0]       cleared_mask;
    reg [36:0]        encountered_mask;

    // Hardware Galois LFSR 32-bit PRNG
    reg         rng_step_en;
    reg  [31:0] rng_seed;
    wire [31:0] hw_lfsr_val;
    wire        hw_rand_50;
    wire [6:0]  hw_rand_pct;
    wire [5:0]  hw_rand_mon_id;

    rng_unit u_rng (
        .clk            (clk),
        .rst_n          (rst_n),
        .step_en        (rng_step_en),
        .seed_val       (rng_seed),
        .lfsr_val       (hw_lfsr_val),
        .rand_bit_50    (hw_rand_50),
        .rand_pct       (hw_rand_pct),
        .rand_monster_id(hw_rand_mon_id)
    );

    // Hardware Combat ALU
    reg  [1:0] alu_p1_action;
    reg  [1:0] alu_p2_action;
    reg  [7:0] alu_p1_base_atk;
    reg  [7:0] alu_p2_base_atk;
    reg  [7:0] alu_p1_def;
    reg  [7:0] alu_p2_def;
    reg  [3:0] alu_rng_bits;
    reg  [7:0] alu_p1_curr_hp;
    reg        alu_is_flee_failed;
    reg  [2:0] alu_limb_target;
    reg        alu_is_lethal;
    reg        alu_disarmed;
    reg  [1:0] alu_archetype;
    wire [7:0] alu_p1_damage;
    wire [7:0] alu_p2_damage;
    wire [7:0] alu_p1_flee_penalty;

    damage_alu u_alu (
        .p1_action      (alu_p1_action),
        .p2_action      (alu_p2_action),
        .p1_base_atk    (alu_p1_base_atk),
        .p2_base_atk    (alu_p2_base_atk),
        .p1_def         (alu_p1_def),
        .p2_def         (alu_p2_def),
        .rng_bits       (alu_rng_bits),
        .p1_curr_hp     (alu_p1_curr_hp),
        .is_flee_failed (alu_is_flee_failed),
        .limb_target    (alu_limb_target),
        .is_lethal_mode (alu_is_lethal),
        .enemy_disarmed (alu_disarmed),
        .enemy_archetype(alu_archetype),
        .p1_damage      (alu_p1_damage),
        .p2_damage      (alu_p2_damage),
        .p1_flee_penalty(alu_p1_flee_penalty)
    );

    // Hardware Collision Unit
    reg signed [31:0]  col_dx, col_dy;
    wire signed [31:0] col_next_x, col_next_y;
    wire       col_blocked, col_monster, col_chest, col_gate;
    wire [2:0] col_dest_tile;

    collision_unit u_col (
        .curr_x          (player_x),
        .curr_y          (player_y),
        .dir_dx          (col_dx),
        .dir_dy          (col_dy),
        .cleared_valid   (16'd0),
        .cleared_coords_x(128'd0),
        .cleared_coords_y(128'd0),
        .cleared_mask    (cleared_mask),
        .next_x          (col_next_x),
        .next_y          (col_next_y),
        .is_blocked      (col_blocked),
        .is_monster      (col_monster),
        .is_chest        (col_chest),
        .is_gate         (col_gate),
        .dest_tile       (col_dest_tile)
    );

    // Hardware Inventory RAM (Solo Explorer synced at Slot 0)
    reg        inv_draft_load;
    reg [3:0]  inv_d_c0, inv_d_c1, inv_d_c2, inv_d_c3;
    reg [7:0]  inv_d_m0, inv_d_m1, inv_d_m2, inv_d_m3;
    reg        inv_hp_update;
    reg [1:0]  inv_target_idx;
    reg [7:0]  inv_new_hp;
    reg        inv_consume_en;
    reg [3:0]  inv_consume_type;
    reg        inv_recv_en;
    reg [3:0]  inv_recv_type;
    reg [7:0]  inv_recv_amt;
    wire [1:0] inv_active_out;
    wire [3:0] inv_c0_id, inv_c1_id, inv_c2_id, inv_c3_id;
    wire [7:0] inv_c0_hp, inv_c1_hp, inv_c2_hp, inv_c3_hp;
    wire [7:0] inv_c0_max, inv_c1_max, inv_c2_max, inv_c3_max;
    wire [7:0] inv_poppy_qty, inv_marijuana_qty, inv_key_qty;
    wire       inv_all_fainted;

    inventory_ram u_inv (
        .clk              (clk),
        .rst_n            (rst_n),
        .active_idx_in    (2'd0),
        .active_idx_out   (inv_active_out),
        .char0_id         (inv_c0_id),
        .char1_id         (inv_c1_id),
        .char2_id         (inv_c2_id),
        .char3_id         (inv_c3_id),
        .char0_hp         (inv_c0_hp),
        .char1_hp         (inv_c1_hp),
        .char2_hp         (inv_c2_hp),
        .char3_hp         (inv_c3_hp),
        .char0_max_hp     (inv_c0_max),
        .char1_max_hp     (inv_c1_max),
        .char2_max_hp     (inv_c2_max),
        .char3_max_hp     (inv_c3_max),
        .poppy_qty        (inv_poppy_qty),
        .marijuana_qty    (inv_marijuana_qty),
        .key_qty          (inv_key_qty),
        .draft_load_en    (inv_draft_load),
        .draft_c0_id      (inv_d_c0),
        .draft_c1_id      (inv_d_c1),
        .draft_c2_id      (inv_d_c2),
        .draft_c3_id      (inv_d_c3),
        .draft_c0_max     (inv_d_m0),
        .draft_c1_max     (inv_d_m1),
        .draft_c2_max     (inv_d_m2),
        .draft_c3_max     (inv_d_m3),
        .hp_update_en     (inv_hp_update),
        .target_char_idx  (inv_target_idx),
        .new_hp_val       (inv_new_hp),
        .item_consume_en  (inv_consume_en),
        .consume_item_type(inv_consume_type),
        .item_receive_en  (inv_recv_en),
        .receive_item_type(inv_recv_type),
        .receive_amount   (inv_recv_amt),
        .team_all_fainted (inv_all_fainted)
    );

    reg        is_hard_mode;

    // Hardware Tactical Stance Coprocessor
    reg        stance_cmd_en;
    reg  [1:0] stance_select_reg;
    wire [1:0] hw_curr_stance;
    wire [7:0] hw_stance_eff_atk;
    wire [7:0] hw_stance_eff_def;
    wire [6:0] hw_stance_evasion;
    wire [6:0] hw_stance_flee_pct;
    wire [7:0] hw_stance_regen_hp;

    tactical_stance_unit u_stance (
        .clk             (clk),
        .rst_n           (rst_n),
        .stance_cmd_en   (stance_cmd_en),
        .stance_select   (stance_select_reg),
        .base_atk        (hero_atk),
        .base_def        (hero_def),
        .is_hard_mode    (is_hard_mode),
        .curr_stance     (hw_curr_stance),
        .eff_atk         (hw_stance_eff_atk),
        .eff_def         (hw_stance_eff_def),
        .evasion_pct     (hw_stance_evasion),
        .flee_success_pct(hw_stance_flee_pct),
        .turn_regen_hp   (hw_stance_regen_hp)
    );

    // Hardware Sanity & Hunger Coprocessor
    reg        sanity_step_pulse;
    reg        sanity_encounter_pulse;
    reg        sanity_panic_strike_pulse;
    reg        sanity_mind_restore_en;
    reg  [7:0] sanity_mind_restore_val;
    reg        sanity_hunger_restore_en;
    reg  [7:0] sanity_hunger_restore_val;
    wire [7:0] hw_mind_level;
    wire [7:0] hw_hunger_level;
    wire       hw_is_panic;
    wire       hw_is_starving;
    wire [6:0] hw_atk_penalty_pct;
    wire       hw_starve_dmg_pulse;

    sanity_meter_unit u_sanity (
        .clk               (clk),
        .rst_n             (rst_n),
        .is_hard_mode      (is_hard_mode),
        .step_pulse        (sanity_step_pulse),
        .encounter_pulse   (sanity_encounter_pulse),
        .panic_strike_pulse(sanity_panic_strike_pulse),
        .mind_restore_en   (sanity_mind_restore_en),
        .mind_restore_val  (sanity_mind_restore_val),
        .hunger_restore_en (sanity_hunger_restore_en),
        .hunger_restore_val(sanity_hunger_restore_val),
        .mind_level        (hw_mind_level),
        .hunger_level      (hw_hunger_level),
        .is_panic          (hw_is_panic),
        .is_starving       (hw_is_starving),
        .atk_penalty_pct   (hw_atk_penalty_pct),
        .starve_dmg_pulse  (hw_starve_dmg_pulse)
    );

    // Input / Loop State Variables
    integer scan_ret;
    integer int_choice;
    reg [127:0] str_input;
    reg [7:0]   cmd_char;
    reg signed [31:0] target_x, target_y;
    integer     target_idx;
    reg [2:0]   target_tile, obs_tile;

    // Combat State
    reg [5:0]   cur_enemy_id;
    reg [1:0]   cur_enemy_arch;
    reg [7:0]   cur_enemy_hp, cur_enemy_max;
    reg [7:0]   cur_enemy_atk, cur_enemy_def;
    reg         cur_enemy_is_elite;
    reg         cur_enemy_drops_key;
    reg [143:0] cur_enemy_short_name;
    reg [63:0]  dummy_arch_s;
    reg [343:0] dummy_m_trait;
    reg [255:0] killer_name;
    reg [3:0]   combat_turn;
    reg         in_combat;
    reg         combat_fled;
    integer     calc_dmg;
    integer     r_roll;
    reg [7:0]   heal_poppy_val;
    reg [7:0]   heal_herb_val;

    // Enemy Limbs
    reg [7:0]   enemy_head_hp, enemy_head_max;
    reg [7:0]   enemy_torso_hp, enemy_torso_max;
    reg [7:0]   enemy_arm_r_hp, enemy_arm_r_max;
    reg [7:0]   enemy_arm_l_hp, enemy_arm_l_max;
    reg [7:0]   enemy_leg_r_hp, enemy_leg_r_max;
    reg         enemy_is_crawling;
    reg         enemy_is_disarmed;

    // Fixed-width log buffers (strict <= 96 chars to never wrap 100-col boxes)
    reg [767:0] map_log_msg;
    reg [767:0] combat_log_msg;
    reg [767:0] pouch_status_msg;

    // UI Cursors & Menus
    reg [1:0]   onboard_state; // 0: Title, 1: Difficulty, 2: Solo Select
    reg         onboard_done, onboard_quit;
    reg         title_cursor, diff_cursor;
    reg [3:0]   solo_sel_id;
    reg [1:0]   cmenu_mode;    // 0: MAIN, 1: LIMB, 2: SKILL
    reg [2:0]   menu_cursor;
    reg         coin_cursor, coin_selected, coin_confirmed;
    reg         action_taken, sub_used_item, skip_retal;
    reg         game_running, game_victory, game_over;

    // ------------------------------------------------------------------------
    // Hardware Drive Helpers
    // ------------------------------------------------------------------------
    task step_rng;
        integer s_idx;
        begin
            rng_step_en = 1'b1;
            for (s_idx = 0; s_idx < 32; s_idx = s_idx + 1) @(posedge clk);
            rng_step_en = 1'b0;
            @(posedge clk);
        end
    endtask

    task hw_sync_hero_hp;
        input [7:0] new_val;
        begin
            hero_hp        = new_val;
            inv_target_idx = 2'd0;
            inv_new_hp     = new_val;
            inv_hp_update  = 1'b1;
            @(posedge clk);
            inv_hp_update  = 1'b0;
            @(posedge clk);
        end
    endtask

    task hw_sync_item_consume;
        input [3:0] itype;
        begin
            inv_consume_type = itype;
            inv_consume_en   = 1'b1;
            @(posedge clk);
            inv_consume_en   = 1'b0;
            @(posedge clk);
        end
    endtask

    task hw_sync_item_receive;
        input [3:0] itype;
        input [7:0] amt;
        begin
            inv_recv_type = itype;
            inv_recv_amt  = amt;
            inv_recv_en   = 1'b1;
            @(posedge clk);
            inv_recv_en   = 1'b0;
            @(posedge clk);
        end
    endtask

    task hw_sync_stance;
        input [1:0] next_st;
        begin
            stance_select_reg = next_st;
            @(posedge clk);
            stance_cmd_en <= 1'b1;
            @(posedge clk);
            stance_cmd_en <= 1'b0;
            @(posedge clk);
        end
    endtask

    task hw_sync_step_pulse;
        begin
            @(posedge clk);
            sanity_step_pulse <= 1'b1;
            @(posedge clk);
            sanity_step_pulse <= 1'b0;
            @(posedge clk);
        end
    endtask

    task hw_sync_encounter_pulse;
        begin
            @(posedge clk);
            sanity_encounter_pulse <= 1'b1;
            @(posedge clk);
            sanity_encounter_pulse <= 1'b0;
            @(posedge clk);
        end
    endtask

    task hw_sync_panic_pulse;
        begin
            @(posedge clk);
            sanity_panic_strike_pulse <= 1'b1;
            @(posedge clk);
            sanity_panic_strike_pulse <= 1'b0;
            @(posedge clk);
        end
    endtask

    task hw_sync_restore_mind;
        input [7:0] val;
        begin
            sanity_mind_restore_val = val;
            @(posedge clk);
            sanity_mind_restore_en <= 1'b1;
            @(posedge clk);
            sanity_mind_restore_en <= 1'b0;
            @(posedge clk);
        end
    endtask

    task hw_sync_restore_hunger;
        input [7:0] val;
        begin
            sanity_hunger_restore_val = val;
            @(posedge clk);
            sanity_hunger_restore_en <= 1'b1;
            @(posedge clk);
            sanity_hunger_restore_en <= 1'b0;
            @(posedge clk);
        end
    endtask

    task apply_mind_delta;
        input integer delta_signed;
        integer tmp;
        begin
            tmp = hero_mind + delta_signed;
            if (tmp < 0) tmp = 0;
            if (tmp > hero_max_mind) tmp = hero_max_mind;
            hero_mind = tmp[7:0];
            if (delta_signed > 0) hw_sync_restore_mind(delta_signed[7:0]);
        end
    endtask

    task apply_hunger_delta;
        input integer delta_signed;
        integer tmp;
        begin
            if (hero_id == 4'd8) begin
                hero_hunger = 8'd0; // Nas'hrah never hungers
            end else begin
                tmp = hero_hunger + delta_signed;
                if (tmp < 0) tmp = 0;
                if (tmp > 100) tmp = 100;
                hero_hunger = tmp[7:0];
                if (delta_signed < 0) hw_sync_restore_hunger((-delta_signed) & 8'hFF);
            end
        end
    endtask

    // Check Totem of Undying Emergency Auto-Revive (returns revived=1 if saved)
    task try_totem_revive;
        output revived;
        begin
            if (bag_totem > 0) begin
                bag_totem       = bag_totem - 1;
                hw_sync_hero_hp(hero_max);
                hero_tox        = 8'd0;
                hero_has_bleed  = 1'b0;
                hero_has_poison = 1'b0;
                limb_head       = 1'b1;
                limb_torso      = 1'b1;
                limb_arm_r      = 1'b1;
                limb_arm_l      = 1'b1;
                limb_legs       = 1'b1;
                revived         = 1'b1;
            end else begin
                revived = 1'b0;
            end
        end
    endtask

    // Wait for a single key press cleanly without extra prompt overflow
    task wait_any_key;
        begin
            $fflush();
            scan_ret = $fscanf(32'h80000000, "%s", str_input);
            if (scan_ret <= 0) game_running = 1'b0;
        end
    endtask

    task init_enemy_limbs;
        input [7:0] total_hp;
        begin
            enemy_head_max  = total_hp >> 2;
            if (enemy_head_max < 8'd16) enemy_head_max = 8'd16;
            enemy_head_hp   = enemy_head_max;

            enemy_torso_max = (total_hp >> 1) + (total_hp >> 2);
            if (enemy_torso_max < 8'd40) enemy_torso_max = 8'd40;
            enemy_torso_hp  = enemy_torso_max;

            enemy_arm_r_max = (total_hp >> 2) + (total_hp >> 3);
            if (enemy_arm_r_max < 8'd20) enemy_arm_r_max = 8'd20;
            enemy_arm_r_hp  = enemy_arm_r_max;

            enemy_arm_l_max = (total_hp >> 2) + (total_hp >> 4);
            if (enemy_arm_l_max < 8'd18) enemy_arm_l_max = 8'd18;
            enemy_arm_l_hp  = enemy_arm_l_max;

            enemy_leg_r_max = (total_hp >> 2) + (total_hp >> 4);
            if (enemy_leg_r_max < 8'd18) enemy_leg_r_max = 8'd18;
            enemy_leg_r_hp  = enemy_leg_r_max;

            enemy_is_crawling = 1'b0;
            enemy_is_disarmed = 1'b0;
        end
    endtask

    // Hardware ALU player attack (guaranteed non-softlock solo glancing chip vs Spectral/Armored)
    task hw_calc_player_attack;
        input  [2:0] target_limb;
        output [7:0] out_dmg;
        reg [7:0]    eff_a;
        begin
            eff_a = hw_stance_eff_atk;
            if (hero_id == 4'd4 && ({1'b0, hero_hp} * 9'd3 <= {1'b0, hero_max}))
                eff_a = eff_a + (eff_a >> 1); // Ragnvaldr Bloodlust +50%
            if (legarde_ale_buff_turns > 0)
                eff_a = eff_a + (eff_a >> 1); // Le'garde Tactical / Ale +50%

            alu_p1_action      = `ACTION_ATTACK;
            alu_p2_action      = `ACTION_ATTACK;
            alu_p1_base_atk    = eff_a;
            alu_p2_base_atk    = cur_enemy_atk;
            alu_p1_def         = hw_stance_eff_def;
            alu_p2_def         = cur_enemy_def;
            alu_rng_bits       = hw_lfsr_val[3:0];
            alu_p1_curr_hp     = hero_hp;
            alu_is_flee_failed = 1'b0;
            alu_limb_target    = target_limb;
            alu_is_lethal      = 1'b0;
            alu_disarmed       = enemy_is_disarmed;
            alu_archetype      = cur_enemy_arch;
            #1;
            out_dmg = alu_p2_damage;
            // Solo anti-softlock: blades deal reduced glancing spirit/armor damage if Mind exhausted
            if (cur_enemy_arch == `ARCHETYPE_SPECTRAL && out_dmg < 8'd12) begin
                out_dmg = eff_a >> 1;
                if (out_dmg < 8'd12) out_dmg = 8'd12;
            end else if (cur_enemy_arch == `ARCHETYPE_ARMORED && out_dmg < 8'd10) begin
                out_dmg = eff_a >> 2;
                if (out_dmg < 8'd10) out_dmg = 8'd10;
            end
            if (hw_is_panic && out_dmg > (out_dmg >> 2))
                out_dmg = out_dmg - (out_dmg >> 2);
        end
    endtask

    // Hardware ALU enemy retaliation + Solo Hero Defense Affinities (Bit-Shift only)
    task hw_calc_enemy_retaliation;
        input        is_lethal;
        input        guarding;
        output [7:0] out_dmg;
        reg [7:0]    raw_d;
        begin
            alu_p1_action      = guarding ? `ACTION_DEFEND : `ACTION_ATTACK;
            alu_p2_action      = `ACTION_ATTACK;
            alu_p1_base_atk    = hw_stance_eff_atk;
            alu_p2_base_atk    = foe_half_atk_debuff ? ((cur_enemy_atk >> 1) < 8'd4 ? 8'd4 : (cur_enemy_atk >> 1)) : cur_enemy_atk;
            alu_p1_def         = hw_stance_eff_def;
            alu_p2_def         = cur_enemy_def;
            alu_rng_bits       = hw_lfsr_val[7:4];
            alu_p1_curr_hp     = hero_hp;
            alu_is_flee_failed = 1'b0;
            alu_limb_target    = 3'd0;
            alu_is_lethal      = is_lethal;
            alu_disarmed       = enemy_is_disarmed;
            alu_archetype      = `ARCHETYPE_NORMAL;
            #1;
            raw_d = alu_p1_damage;
            // Hero Armor / Fragility Affinities via exact binary shifts
            case (hero_id)
                4'd2: raw_d = raw_d - (raw_d >> 2) - (raw_d >> 3); // D'arce -37.5% phys armor
                4'd3: raw_d = raw_d + (raw_d >> 2);                // Enki +25% frail
                4'd4: raw_d = raw_d - (raw_d >> 3);                // Ragnvaldr -12.5% muscle
                4'd6: raw_d = raw_d - (raw_d >> 3);                // Moonless -12.5% hide
                4'd7: raw_d = raw_d - (raw_d >> 2);                // The Girl -25% ward
                4'd8: raw_d = raw_d + (raw_d >> 2);                // Nas'hrah +25% fragile skull
                default: raw_d = raw_d;
            endcase
            if (raw_d < 8'd2) raw_d = 8'd2;
            out_dmg = raw_d;
        end
    endtask

    // ------------------------------------------------------------------------
    // Persistent Dual-Box Pouch Loop (In-Place Update, Closes ONLY on Request)
    // ------------------------------------------------------------------------
    task run_solo_pouch;
        input  in_arena;
        output used_turn_item;
        reg [2:0] pouch_cursor;
        reg       pouch_open;
        reg [7:0] tmp_heal, tmp_tox;
        begin
            used_turn_item   = 1'b0;
            pouch_cursor     = 3'd0;
            pouch_open       = 1'b1;
            pouch_status_msg = 0;

            while (pouch_open && game_running) begin
                ui.render_solo_pouch_screen(
                    pouch_cursor, is_hard_mode,
                    hero_id, hero_hp, hero_max, hero_mind, hero_max_mind,
                    hero_hunger, hero_tox, hero_max_tox, hero_atk, hero_def,
                    hero_has_bleed, hero_has_poison,
                    limb_head, limb_torso, limb_arm_r, limb_arm_l, limb_legs,
                    bag_totem, bag_poppy, bag_herb, bag_bread, bag_meat, bag_vial, bag_keys,
                    pouch_status_msg
                );
                $fflush();
                scan_ret = $fscanf(32'h80000000, "%s", str_input);
                if (scan_ret <= 0) begin
                    game_running = 1'b0;
                    pouch_open   = 1'b0;
                end else begin
                    cmd_char = str_input[7:0];
                    if (cmd_char == "w" || cmd_char == "W" || cmd_char == "k") begin
                        pouch_cursor = (pouch_cursor == 3'd0) ? 3'd7 : (pouch_cursor - 3'd1);
                    end else if (cmd_char == "s" || cmd_char == "S" || cmd_char == "j") begin
                        pouch_cursor = (pouch_cursor == 3'd7) ? 3'd0 : (pouch_cursor + 3'd1);
                    end else if (cmd_char == "a" || cmd_char == "A" || cmd_char == "d" || cmd_char == "D") begin
                        // Left/Right harmless in vertical pouch list
                    end else if (cmd_char >= "1" && cmd_char <= "8") begin
                        pouch_cursor = (cmd_char - "1");
                    end else if (cmd_char == "i" || cmd_char == "I" || cmd_char == "b" || cmd_char == "B" || cmd_char == "x" || cmd_char == "X" || cmd_char == "q" || cmd_char == "Q") begin
                        pouch_open = 1'b0;
                    end else if (cmd_char == "e" || cmd_char == "E" || cmd_char == " ") begin
                        if (pouch_cursor == 3'd7) begin
                            pouch_open = 1'b0; // [ CLOSE POUCH ]
                        end else if (pouch_cursor == 3'd6) begin
                            $sformat(pouch_status_msg, "[RUNIC KEY]: Holding %0d/3 Runic Keys. Bring 3 Keys to Eastern Gate!", bag_keys);
                        end else if (pouch_cursor == 3'd0) begin
                            if (bag_totem > 0) begin
                                bag_totem       = bag_totem - 1;
                                hw_sync_hero_hp(hero_max);
                                hero_tox        = 8'd0;
                                hero_has_bleed  = 1'b0;
                                hero_has_poison = 1'b0;
                                limb_head       = 1'b1; limb_torso = 1'b1; limb_arm_r = 1'b1; limb_arm_l = 1'b1; limb_legs = 1'b1;
                                used_turn_item  = 1'b1;
                                $sformat(pouch_status_msg, "* [TOTEM]: Golden amber restores %s to %0d/%0d HP & mends all limbs!", hero_name, hero_hp, hero_max);
                                if (in_arena) pouch_open = 1'b0;
                            end else begin
                                pouch_status_msg = "[DEPLETED]: No Totem of Undying remaining in satchel!";
                            end
                        end else if (pouch_cursor == 3'd1) begin
                            if (bag_poppy > 0) begin
                                bag_poppy = bag_poppy - 1;
                                hw_sync_item_consume(`ITEM_POPPY);
                                used_turn_item = 1'b1;
                                if (hero_id == 4'd8) begin
                                    pouch_status_msg = "[POPPY FLOWER]: Nas'hrah scoffs: 'No mortal weeds!' (0 HP).";
                                end else if (hero_tox >= hero_max_tox) begin
                                    hw_sync_hero_hp((hero_hp > 8'd5) ? (hero_hp - 8'd5) : 8'd1);
                                    pouch_status_msg = "[OVERDOSE!]: Stomach convulses! Poppy ineffective (-5 HP toxin). Use Vial!";
                                end else begin
                                    tmp_heal = (hero_id == 4'd1) ? (is_hard_mode ? 8'd37 : 8'd65) : heal_poppy_val;
                                    tmp_tox  = (hero_id == 4'd6) ? 8'd0 : ((hero_id == 4'd4) ? 8'd15 : 8'd35);
                                    hw_sync_hero_hp(({1'b0, hero_hp} + {1'b0, tmp_heal} > {1'b0, hero_max}) ? hero_max : (hero_hp + tmp_heal));
                                    hero_tox = ({1'b0, hero_tox} + {1'b0, tmp_tox} > {1'b0, hero_max_tox}) ? hero_max_tox : (hero_tox + tmp_tox);
                                    hero_has_bleed = 1'b0;
                                    $sformat(pouch_status_msg, "[POPPY]: Restored +%0d HP & stopped bleeding! (%0d/%0d HP, Tox %0d%%)", tmp_heal, hero_hp, hero_max, hero_tox);
                                end
                                if (in_arena) pouch_open = 1'b0;
                            end else begin
                                pouch_status_msg = "[DEPLETED]: No Poppy Flowers left in satchel!";
                            end
                        end else if (pouch_cursor == 3'd2) begin
                            if (bag_herb > 0) begin
                                bag_herb = bag_herb - 1;
                                hw_sync_item_consume(`ITEM_MARIJUANA);
                                used_turn_item = 1'b1;
                                if (hero_id == 4'd8) begin
                                    pouch_status_msg = "[MEDICINAL HERB]: Nas'hrah rejects mortal medicine (0 HP).";
                                end else if (hero_tox >= hero_max_tox) begin
                                    hw_sync_hero_hp((hero_hp > 8'd5) ? (hero_hp - 8'd5) : 8'd1);
                                    pouch_status_msg = "[OVERDOSE!]: Too toxic for Herbs (-5 HP)! Cleanse with Alchemical Vial!";
                                end else begin
                                    tmp_heal = (hero_id == 4'd1) ? (is_hard_mode ? 8'd95 : 8'd150) : heal_herb_val;
                                    tmp_tox  = (hero_id == 4'd6) ? 8'd0 : ((hero_id == 4'd4) ? 8'd25 : 8'd50);
                                    hw_sync_hero_hp(({1'b0, hero_hp} + {1'b0, tmp_heal} > {1'b0, hero_max}) ? hero_max : (hero_hp + tmp_heal));
                                    hero_tox = ({1'b0, hero_tox} + {1'b0, tmp_tox} > {1'b0, hero_max_tox}) ? hero_max_tox : (hero_tox + tmp_tox);
                                    apply_mind_delta(15);
                                    $sformat(pouch_status_msg, "[MEDICINAL HERB]: +%0d HP & +15 Mind! (%0d/%0d HP, Tox %0d%%)", tmp_heal, hero_hp, hero_max, hero_tox);
                                end
                                if (in_arena) pouch_open = 1'b0;
                            end else begin
                                pouch_status_msg = "[DEPLETED]: No Medicinal Herbs left in satchel!";
                            end
                        end else if (pouch_cursor == 3'd3) begin
                            if (bag_bread > 0) begin
                                bag_bread = bag_bread - 1;
                                used_turn_item = 1'b1;
                                if (hero_id == 4'd8) begin
                                    pouch_status_msg = "[MOLDY BREAD]: Nas'hrah has no stomach for mortal bread!";
                                end else if (hero_id == 4'd4) begin
                                    apply_hunger_delta(-20);
                                    $sformat(pouch_status_msg, "[MOLDY BREAD]: Ragnvaldr swallows bread (-20 Hunger - craves Meat!). (%0d/100)", hero_hunger);
                                end else if (hero_id == 4'd1) begin
                                    apply_hunger_delta(-50);
                                    $sformat(pouch_status_msg, "[MOLDY BREAD]: Cahara enjoys rations (-50 Hunger). (%0d/100)", hero_hunger);
                                end else begin
                                    apply_hunger_delta(-40);
                                    $sformat(pouch_status_msg, "[MOLDY BREAD]: Ate dungeon ration (-40 Hunger). (%0d/100)", hero_hunger);
                                end
                                if (in_arena) pouch_open = 1'b0;
                            end else begin
                                pouch_status_msg = "[DEPLETED]: No Moldy Bread remaining!";
                            end
                        end else if (pouch_cursor == 3'd4) begin
                            if (bag_meat > 0) begin
                                bag_meat = bag_meat - 1;
                                used_turn_item = 1'b1;
                                if (hero_id == 4'd8) begin
                                    pouch_status_msg = "[DRIED MEAT]: Nas'hrah refuses mortal flesh!";
                                end else begin
                                    tmp_heal = (hero_id == 4'd4 || hero_id == 4'd6) ? 8'd40 : 8'd20;
                                    apply_hunger_delta(-60);
                                    hw_sync_hero_hp(({1'b0, hero_hp} + {1'b0, tmp_heal} > {1'b0, hero_max}) ? hero_max : (hero_hp + tmp_heal));
                                    $sformat(pouch_status_msg, "[DRIED MEAT]: -60 Hunger & +%0d HP restored! (%0d/%0d HP, Hng %0d/100)", tmp_heal, hero_hp, hero_max, hero_hunger);
                                end
                                if (in_arena) pouch_open = 1'b0;
                            end else begin
                                pouch_status_msg = "[DEPLETED]: No Dried Meat remaining!";
                            end
                        end else if (pouch_cursor == 3'd5) begin
                            if (bag_vial > 0) begin
                                bag_vial = bag_vial - 1;
                                used_turn_item = 1'b1;
                                apply_mind_delta(35);
                                hero_tox        = (hero_tox > 8'd25) ? (hero_tox - 8'd25) : 8'd0;
                                hero_has_bleed  = 1'b0;
                                hero_has_poison = 1'b0;
                                if (hero_id == 4'd8) begin
                                    hw_sync_hero_hp(({1'b0, hero_hp} + 8'd15 > {1'b0, hero_max}) ? hero_max : (hero_hp + 8'd15));
                                    $sformat(pouch_status_msg, "[ALCHEMICAL VIAL]: Nas'hrah absorbs spirits (+15 HP, +35 Mind)!");
                                end else if (hero_id == 4'd5) begin
                                    legarde_ale_buff_turns = 3'd3;
                                    $sformat(pouch_status_msg, "[ALCHEMICAL VIAL]: Le'garde enters +50%% ATK Tactician Rush & +35 Mind!");
                                end else begin
                                    $sformat(pouch_status_msg, "[ALCHEMICAL VIAL]: +35 Mind, -25%% Tox, purged Bleeding & Poison!");
                                end
                                if (in_arena) pouch_open = 1'b0;
                            end else begin
                                pouch_status_msg = "[DEPLETED]: No Alchemical Vials remaining!";
                            end
                        end
                    end
                end
            end
        end
    endtask

    // ------------------------------------------------------------------------
    // MAIN PURE VERILOG SOLO EXPLORER SIMULATION
    // ------------------------------------------------------------------------
    initial begin
        $write("\033[2J\033[3J\033[?25l\033[H");
        clk   = 0;
        rst_n = 0;

        rng_step_en     = 1'b0;
        rng_seed        = 32'h5A82_7999;
        mon_lookup_id   = 6'd1;
        mon_lookup_elite= 1'b0;
        inv_draft_load  = 1'b0;
        inv_d_c0 = 4'd1; inv_d_c1 = 4'd2; inv_d_c2 = 4'd3; inv_d_c3 = 4'd4;
        inv_d_m0 = 8'd150; inv_d_m1 = 8'd150; inv_d_m2 = 8'd118; inv_d_m3 = 8'd190;
        inv_hp_update   = 1'b0;
        inv_target_idx  = 2'd0;
        inv_new_hp      = 8'd150;
        inv_consume_en  = 1'b0;
        inv_consume_type= `ITEM_NONE;
        inv_recv_en     = 1'b0;
        inv_recv_type   = `ITEM_NONE;
        inv_recv_amt    = 8'd0;
        col_dx          = 32'sd0;
        col_dy          = 32'sd0;

        stance_cmd_en             = 1'b0;
        stance_select_reg         = `STANCE_BALANCED;
        sanity_step_pulse         = 1'b0;
        sanity_encounter_pulse    = 1'b0;
        sanity_panic_strike_pulse = 1'b0;
        sanity_mind_restore_en    = 1'b0;
        sanity_mind_restore_val   = 8'd0;
        sanity_hunger_restore_en  = 1'b0;
        sanity_hunger_restore_val = 8'd0;

        #20 rst_n = 1;
        #10;

        is_hard_mode            = 1'b0;
        player_x                = 2;
        player_y                = 2;
        step_count              = 0;
        monsters_defeated_count = 0;
        chests_looted_count     = 0;
        cleared_mask            = 720'd0;
        encountered_mask        = 37'd0;
        in_combat               = 1'b0;
        game_running            = 1'b1;
        game_victory            = 1'b0;
        game_over               = 1'b0;
        killer_name             = "DARKNESS";

        // 1-3. ONBOARDING FSM (0: TITLE <-> 1: DIFFICULTY <-> 2: SOLO SELECT)
        onboard_state = 2'd0;
        onboard_done  = 1'b0;
        onboard_quit  = 1'b0;
        title_cursor  = 1'b0;
        diff_cursor   = 1'b0;
        solo_sel_id   = 4'd1;

        while (!onboard_done) begin
            if (onboard_state == 2'd0)
                ui.render_title_screen(title_cursor);
            else if (onboard_state == 2'd1)
                ui.render_difficulty_select_screen(diff_cursor);
            else
                ui.render_solo_select_screen(solo_sel_id, diff_cursor);
            $fflush();

            scan_ret = $fscanf(32'h80000000, "%s", str_input);
            if (scan_ret <= 0) begin
                onboard_quit = 1'b1;
                onboard_done = 1'b1;
            end else begin
                cmd_char = str_input[7:0];
                if (onboard_state == 2'd0) begin
                    // STATE 0: TITLE SCREEN
                    if (cmd_char == "w" || cmd_char == "W" || cmd_char == "s" || cmd_char == "S" || cmd_char == "k" || cmd_char == "j") begin
                        title_cursor = ~title_cursor;
                    end else if (cmd_char == "1") begin
                        title_cursor  = 1'b0;
                        onboard_state = 2'd1;
                    end else if (cmd_char == "2" || cmd_char == "0" || cmd_char == "q" || cmd_char == "Q") begin
                        title_cursor = 1'b1;
                        onboard_quit = 1'b1;
                        onboard_done = 1'b1;
                    end else if (cmd_char == "e" || cmd_char == "E" || cmd_char == " ") begin
                        if (title_cursor == 1'b0) begin
                            onboard_state = 2'd1;
                        end else begin
                            onboard_quit = 1'b1;
                            onboard_done = 1'b1;
                        end
                    end
                    // Note: "x"/"b" (Esc/Backspace) intentionally does NOT start the game.
                end else if (onboard_state == 2'd1) begin
                    // STATE 1: DIFFICULTY SCREEN
                    if (cmd_char == "w" || cmd_char == "W" || cmd_char == "s" || cmd_char == "S" || cmd_char == "k" || cmd_char == "j") begin
                        diff_cursor = ~diff_cursor;
                    end else if (cmd_char == "1") begin
                        diff_cursor   = 1'b0;
                        onboard_state = 2'd2;
                    end else if (cmd_char == "2" || cmd_char == "h" || cmd_char == "H") begin
                        diff_cursor   = 1'b1;
                        onboard_state = 2'd2;
                    end else if (cmd_char == "e" || cmd_char == "E" || cmd_char == " ") begin
                        onboard_state = 2'd2;
                    end else if (cmd_char == "b" || cmd_char == "B" || cmd_char == "x" || cmd_char == "X") begin
                        onboard_state = 2'd0;
                    end else if (cmd_char == "q" || cmd_char == "Q") begin
                        onboard_quit = 1'b1;
                        onboard_done = 1'b1;
                    end
                end else begin
                    // STATE 2: SOLO EXPLORER SELECTOR
                    if (cmd_char == "w" || cmd_char == "W" || cmd_char == "k") begin
                        solo_sel_id = (solo_sel_id == 4'd1) ? 4'd8 : (solo_sel_id - 4'd1);
                    end else if (cmd_char == "s" || cmd_char == "S" || cmd_char == "j") begin
                        solo_sel_id = (solo_sel_id == 4'd8) ? 4'd1 : (solo_sel_id + 4'd1);
                    end else if (cmd_char >= "1" && cmd_char <= "8") begin
                        solo_sel_id = cmd_char - "0";
                    end else if (cmd_char == "e" || cmd_char == "E" || cmd_char == " ") begin
                        onboard_done = 1'b1;
                    end else if (cmd_char == "b" || cmd_char == "B" || cmd_char == "x" || cmd_char == "X") begin
                        onboard_state = 2'd1;
                    end else if (cmd_char == "q" || cmd_char == "Q") begin
                        onboard_quit = 1'b1;
                        onboard_done = 1'b1;
                    end
                end
            end
        end

        if (!onboard_quit) begin
            if (diff_cursor == 1'b1) begin
                is_hard_mode   = 1'b1;
                heal_poppy_val = 8'd30;
                heal_herb_val  = 8'd75;
            end else begin
                is_hard_mode   = 1'b0;
                heal_poppy_val = 8'd50;
                heal_herb_val  = 8'd120;
            end

        // Initialize Solo Hero Dossier & Hardware RAM
        hero_id = solo_sel_id;
        ui.get_solo_hero_dossier(
            hero_id, is_hard_mode,
            hero_max, hero_atk, hero_def, hero_dodge, hero_max_tox, hero_bag_cap,
            hero_name, hero_role, dummy_pr, dummy_mr, hero_trait_s, hero_buff_s, dummy_a1, dummy_a2
        );
        hero_hp                = hero_max;
        hero_max_mind          = (hero_id == 4'd3) ? 8'd130 : ((hero_id == 4'd8) ? 8'd150 : 8'd100);
        hero_mind              = hero_max_mind;
        hero_hunger            = 8'd0;
        hero_tox               = 8'd0;
        hero_is_guarding       = 1'b0;
        hero_has_bleed         = 1'b0;
        hero_has_poison        = 1'b0;
        limb_head              = 1'b1; limb_torso = 1'b1; limb_arm_r = 1'b1; limb_arm_l = 1'b1; limb_legs = 1'b1;
        legarde_ale_buff_turns = 3'd0;
        scent_dodge_turns      = 3'd0;
        girl_100_dodge         = 1'b0;

        // Starter Pouch (Matches master_game.py: Cahara 2x supplies, others baseline, 1 Totem)
        bag_totem = 8'd1;
        bag_keys  = 8'd0;
        if (hero_id == 4'd1) begin
            bag_poppy = 8'd5; bag_herb = 8'd3; bag_bread = 8'd6; bag_meat = 8'd4; bag_vial = 8'd3;
        end else begin
            bag_poppy = 8'd3; bag_herb = 8'd2; bag_bread = 8'd4; bag_meat = 8'd2; bag_vial = 8'd2;
        end

        // Load Solo Hero into Hardware Inventory RAM Slot 0
        inv_d_c0 = hero_id; inv_d_m0 = hero_max;
        inv_draft_load = 1'b1;
        @(posedge clk);
        inv_draft_load = 1'b0;
        @(posedge clk);

        $sformat(map_log_msg, "%0s [%0s] steps alone into the pitch-black Labyrinth.", hero_name, hero_role);

        // 4. MAIN LABYRINTH EXPLORATION LOOP
        while (game_running && !game_victory && !game_over) begin
            ui.render_solo_map_screen(
                is_hard_mode, player_x, player_y,
                step_count, monsters_defeated_count,
                hero_id, hero_hp, hero_max, hero_mind, hero_hunger,
                bag_keys, cleared_mask, map_log_msg
            );
            $fflush();
            scan_ret = $fscanf(32'h80000000, "%s", str_input);
            if (scan_ret <= 0) begin
                game_running = 1'b0;
                cmd_char     = "q";
            end else begin
                cmd_char = str_input[7:0];
            end

            if (cmd_char == "q" || cmd_char == "Q") begin
                game_running = 1'b0;
            end else if (cmd_char == "g" || cmd_char == "G") begin
                ui.render_guide_modal_screen();
                wait_any_key();
                map_log_msg = "[GUIDE]: Returned to dungeon exploration.";
            end else if (cmd_char == "i" || cmd_char == "I") begin
                run_solo_pouch(1'b0, sub_used_item);
                map_log_msg = "[SURVIVAL POUCH]: Returned cleanly to Labyrinth exploration.";
            end else if (cmd_char == "w" || cmd_char == "W" || cmd_char == "a" || cmd_char == "A" || cmd_char == "s" || cmd_char == "S" || cmd_char == "d" || cmd_char == "D") begin
                col_dx = (cmd_char == "a" || cmd_char == "A") ? -32'sd1 : (cmd_char == "d" || cmd_char == "D") ? 32'sd1 : 32'sd0;
                col_dy = (cmd_char == "w" || cmd_char == "W") ? -32'sd1 : (cmd_char == "s" || cmd_char == "S") ? 32'sd1 : 32'sd0;
                #1;
                target_x    = col_next_x;
                target_y    = col_next_y;
                target_tile = col_dest_tile;
                target_idx  = target_x + (target_y * `MAP_WIDTH);
                ui.solo_tile_obstacle(target_x, target_y, obs_tile);

                if (col_blocked) begin
                    map_log_msg = "[COLLISION]: Solid damp stone wall obstructs your path.";
                end else if (col_gate) begin
                    if (bag_keys >= 8'd3) begin
                        game_victory = 1'b1;
                    end else begin
                        $sformat(map_log_msg, "[GATE LOCKED]: Massive Runic Portal requires 3 Runic Keys (Holding %0d/3).", bag_keys);
                    end
                end else if (obs_tile == `OBSTACLE_BARRICADE && !cleared_mask[target_idx]) begin
                    cleared_mask[target_idx] = 1'b1;
                    player_x = target_x; player_y = target_y; step_count = step_count + 1;
                    $sformat(map_log_msg, "[%0s]: Smashes through heavy rock barricade! Passage cleared!", hero_name);
                end else if (obs_tile == `OBSTACLE_SEAL && !cleared_mask[target_idx]) begin
                    cleared_mask[target_idx] = 1'b1;
                    player_x = target_x; player_y = target_y; step_count = step_count + 1;
                    if (hero_id == 4'd3 || hero_id == 4'd8) begin
                        $sformat(map_log_msg, "[%0s]: Chants arcane counter-curse, dispelling Hexen Seal safely!", hero_name);
                    end else begin
                        hw_sync_hero_hp((hero_hp > 8'd10) ? (hero_hp - 8'd10) : 8'd1);
                        $sformat(map_log_msg, "[HEXEN SEAL]: Arcane ward burns %0s (-10 HP) before shattering!", hero_name);
                    end
                end else if (obs_tile == `OBSTACLE_CRAWLSPACE) begin
                    player_x = target_x; player_y = target_y; step_count = step_count + 1;
                    if (hero_id == 4'd6 || hero_id == 4'd7)
                        $sformat(map_log_msg, "[%0s]: Slips effortlessly through the narrow stone crevice!", hero_name);
                    else
                        $sformat(map_log_msg, "[%0s]: Wedges carefully through the tight subterranean crevice.", hero_name);
                end else if (target_tile == `TILE_CHEST && !cleared_mask[target_idx]) begin
                    player_x = target_x; player_y = target_y; step_count = step_count + 1;
                    chests_looted_count = chests_looted_count + 1;
                    cleared_mask[target_idx] = 1'b1;

                    // 3 Guaranteed Key Vaults with Spring Needle Traps: (6,11), (12,17), (26,17)
                    if ((target_x == 6 && target_y == 11) || (target_x == 12 && target_y == 17) || (target_x == 26 && target_y == 17)) begin
                        if (bag_keys < 8'd3) begin
                            bag_keys = bag_keys + 1;
                            hw_sync_item_receive(`ITEM_KEY, 8'd1);
                        end
                        if (hero_id == 4'd1 || hero_id == 4'd5) begin
                            $sformat(map_log_msg, "[DISARMED!]: %0s disarmed spring needle trap! Got Runic Key (%0d/3)!", hero_name, bag_keys);
                        end else if (hero_hp <= 8'd20) begin
                            try_totem_revive(sub_used_item);
                            if (sub_used_item) begin
                                $sformat(map_log_msg, "* [TOTEM SAVED YOU!]: Spring trap negated! Full HP + Key (%0d/3)!", bag_keys);
                            end else begin
                                hw_sync_hero_hp(8'd0);
                                game_over   = 1'b1;
                                killer_name = "SPRING NEEDLE TRAP";
                            end
                        end else begin
                            hw_sync_hero_hp(hero_hp - 8'd20);
                            $sformat(map_log_msg, "[TRAP TRIGGERED]: Spring needle hit (-20 HP)! Got Runic Key (%0d/3)!", bag_keys);
                        end
                    end else begin
                        step_rng;
                        r_roll = hw_rand_pct;
                        if (r_roll < 25 && !encountered_mask[23]) begin
                            // 25% Mimic Ambush!
                            encountered_mask[23] = 1'b1;
                            cur_enemy_id       = 6'd23;
                            cur_enemy_is_elite = 1'b0;
                            cur_enemy_drops_key= 1'b0;
                            mon_lookup_id      = 6'd23;
                            mon_lookup_elite   = 1'b0;
                            #1;
                            cur_enemy_hp   = mon_rom_hp;
                            cur_enemy_max  = mon_rom_hp;
                            cur_enemy_atk  = mon_rom_atk;
                            cur_enemy_def  = mon_rom_def;
                            cur_enemy_arch = mon_rom_arch;
                            init_enemy_limbs(cur_enemy_hp);
                            in_combat      = 1'b1;
                            combat_turn    = 4'd1;
                            combat_fled    = 1'b0;
                            cmenu_mode     = 2'd0;
                            menu_cursor    = 3'd0;
                            combat_log_msg = "MIMIC TRAP! The ancient vault chest sprouts fangs and lunges!";
                        end else begin
                            // Safe Supply Vault
                            $write("\033[H");
                            step_rng;
                            r_roll = hw_rand_pct;
                            if (r_roll < 35) begin
                                bag_keys = bag_keys + 1;
                                hw_sync_item_receive(`ITEM_KEY, 8'd1);
                                ui.render_chest_open_screen(1'b0, "Runic Dungeon Key", 8'd1);
                                ui.notify_receive_item("Ancient Vault Chest", "Dungeon Key", 8'd1);
                                $sformat(map_log_msg, "[VAULT]: Looted Runic Dungeon Key (%0d/3) from chest (%0d,%0d)!", bag_keys, target_x, target_y);
                            end else if (r_roll < 65) begin
                                bag_bread = bag_bread + 2; bag_meat = bag_meat + 1;
                                ui.render_chest_open_screen(1'b0, "Moldy Bread x2 & Dried Meat x1", 8'd3);
                                ui.notify_receive_item("Ancient Vault Chest", "Moldy Bread x2 & Dried Meat x1", 8'd3);
                                $sformat(map_log_msg, "[CHEST]: Looted +2 Moldy Bread & +1 Dried Meat at (%0d,%0d).", target_x, target_y);
                            end else if (r_roll < 85) begin
                                bag_herb = bag_herb + 1; hw_sync_item_receive(`ITEM_MARIJUANA, 8'd1); bag_vial = bag_vial + 1;
                                ui.render_chest_open_screen(1'b0, "Medicinal Herb & Alchemical Vial", 8'd2);
                                ui.notify_receive_item("Ancient Vault Chest", "Medicinal Herb & Alchemical Vial", 8'd2);
                                $sformat(map_log_msg, "[CHEST]: Looted +1 Medicinal Herb & +1 Alchemical Vial at (%0d,%0d).", target_x, target_y);
                            end else begin
                                bag_poppy = bag_poppy + 2; hw_sync_item_receive(`ITEM_POPPY, 8'd2);
                                ui.render_chest_open_screen(1'b0, "White Poppy Flowers", 8'd2);
                                ui.notify_receive_item("Ancient Vault Chest", "Poppy Flower x2", 8'd2);
                                $sformat(map_log_msg, "[CHEST]: Looted +2 White Poppy Flowers at (%0d,%0d).", target_x, target_y);
                            end
                            $write("  \033[1;33m>> Press [Enter] to collect supplies and continue: \033[0m\033[K\033[J");
                            $fflush();
                            wait_any_key();
                        end
                    end
                end else if (target_tile == `TILE_MONSTER && !cleared_mask[target_idx]) begin
                    player_x = target_x; player_y = target_y; step_count = step_count + 1;

                    // Boss Gatekeepers vs Progressive Non-Repeating Roaming Foes
                    if (target_x == 34 && target_y == 6) begin
                        cur_enemy_id        = 6'd20; // Abyssal Overlord
                        cur_enemy_is_elite  = 1'b1;
                        cur_enemy_drops_key = 1'b1;
                    end else if (target_x == 34 && target_y == 14) begin
                        cur_enemy_id        = 6'd36; // Cthulhu Titan
                        cur_enemy_is_elite  = 1'b1;
                        cur_enemy_drops_key = 1'b1;
                    end else begin
                        cur_enemy_id = 6'd8;
                        for (int_choice = 35; int_choice >= 1; int_choice = int_choice - 1) begin
                            if (!encountered_mask[int_choice] && int_choice != 23 && int_choice != 20) begin
                                cur_enemy_id = int_choice[5:0];
                            end
                        end
                        step_rng;
                        cur_enemy_is_elite  = (hw_rand_pct < 25);
                        cur_enemy_drops_key = 1'b0;
                    end

                    encountered_mask[cur_enemy_id] = 1'b1;
                    mon_lookup_id    = cur_enemy_id;
                    mon_lookup_elite = cur_enemy_is_elite;
                    #1;
                    cur_enemy_is_elite = cur_enemy_is_elite | mon_rom_def_elite;
                    cur_enemy_hp   = mon_rom_hp;
                    cur_enemy_max  = mon_rom_hp;
                    cur_enemy_atk  = mon_rom_atk;
                    cur_enemy_def  = mon_rom_def;
                    cur_enemy_arch = mon_rom_arch;
                    init_enemy_limbs(cur_enemy_hp);
                    hw_sync_encounter_pulse();
                    apply_mind_delta(is_hard_mode ? -6 : -2);

                    in_combat              = 1'b1;
                    combat_turn            = 4'd1;
                    combat_fled            = 1'b0;
                    cmenu_mode             = 2'd0;
                    menu_cursor            = 3'd0;
                    hero_is_guarding       = 1'b0;
                    foe_half_atk_debuff    = 1'b0;
                    girl_100_dodge         = 1'b0;
                    scent_dodge_turns      = 3'd0;
                    ui.get_mon_card_meta(cur_enemy_id, cur_enemy_arch, cur_enemy_short_name, dummy_arch_s, dummy_m_trait);
                    $sformat(combat_log_msg, "Battle initiated! %0s confronts #%-2d %0s!", hero_name, cur_enemy_id, cur_enemy_short_name);
                end else begin
                    player_x = target_x; player_y = target_y; step_count = step_count + 1;
                    hw_sync_step_pulse();
                    if (hero_id != 4'd8) begin
                        if (step_count[4:0] == 5'd0) apply_hunger_delta(10);
                        if (hw_starve_dmg_pulse || hero_hunger >= 8'd90) begin
                            if (step_count[2:0] == 3'd0) begin
                                if (hero_hp <= 8'd5) begin
                                    try_totem_revive(sub_used_item);
                                    if (sub_used_item) begin
                                        apply_hunger_delta(-100);
                                        map_log_msg = "* [TOTEM OF UNDYING]: Starvation reversed! Full HP & strength restored!";
                                    end else begin
                                        hw_sync_hero_hp(8'd0);
                                        game_over   = 1'b1;
                                        killer_name = "STARVATION";
                                    end
                                end else begin
                                    hw_sync_hero_hp(hero_hp - 8'd5);
                                    map_log_msg = "[STARVATION]: Stomach cramps drain -5 HP! Eat Bread/Meat in Pouch [I]!";
                                end
                            end
                        end else begin
                            $sformat(map_log_msg, "%0s explores the pitch-black catacombs.", hero_name);
                        end
                    end else begin
                        $sformat(map_log_msg, "Nas'hrah floats effortlessly along the dark corridor.");
                    end
                end
            end else begin
                map_log_msg = "[CONTROLS]: Use [W/A/S/D] Move, [I] Pouch, [G] Survival Guide, [Q] Quit.";
            end

            // ================================================================
            // 5. POKEMON-STYLE SOLO COMBAT LOOP (HIERARCHICAL W/S + ENTER)
            // ================================================================
            while (in_combat && !game_over) begin
                ui.render_solo_combat_screen(
                    is_hard_mode, combat_turn, cmenu_mode, menu_cursor,
                    hero_id, hero_hp, hero_max, hero_mind, hero_max_mind,
                    hero_hunger, hero_tox, hero_max_tox, hero_atk, hero_def,
                    hw_curr_stance, hero_is_guarding, hero_has_bleed, hero_has_poison,
                    cur_enemy_id, cur_enemy_arch, cur_enemy_is_elite,
                    cur_enemy_hp, cur_enemy_max, cur_enemy_atk, cur_enemy_def,
                    enemy_head_hp, enemy_torso_hp, enemy_arm_r_hp, enemy_arm_l_hp, enemy_leg_r_hp,
                    enemy_is_crawling, enemy_is_disarmed, combat_log_msg
                );
                $fflush();
                scan_ret = $fscanf(32'h80000000, "%s", str_input);
                if (scan_ret <= 0) begin
                    in_combat    = 1'b0;
                    game_running = 1'b0;
                end else begin
                    cmd_char     = str_input[7:0];
                    action_taken = 1'b0;
                    skip_retal   = 1'b0;

                    if (cmd_char == "q" || cmd_char == "Q") begin
                        in_combat    = 1'b0;
                        game_running = 1'b0;
                    end else if (cmd_char == "w" || cmd_char == "W" || cmd_char == "k") begin
                        if (cmenu_mode == 2'd1)      menu_cursor = (menu_cursor == 3'd0) ? 3'd5 : (menu_cursor - 3'd1);
                        else                         menu_cursor = (menu_cursor == 3'd0) ? 3'd4 : (menu_cursor - 3'd1);
                    end else if (cmd_char == "s" || cmd_char == "S" || cmd_char == "j") begin
                        if (cmenu_mode == 2'd1)      menu_cursor = (menu_cursor == 3'd5) ? 3'd0 : (menu_cursor + 3'd1);
                        else                         menu_cursor = (menu_cursor == 3'd4) ? 3'd0 : (menu_cursor + 3'd1);
                    end else if (cmd_char == "b" || cmd_char == "B" || cmd_char == "x" || cmd_char == "X") begin
                        if (cmenu_mode != 2'd0) begin
                            cmenu_mode  = 2'd0;
                            menu_cursor = 3'd0;
                        end
                    end else if (cmd_char >= "1" && cmd_char <= "6") begin
                        if ((cmenu_mode == 2'd1 && cmd_char <= "6") || (cmenu_mode != 2'd1 && cmd_char <= "5"))
                            menu_cursor = (cmd_char - "1");
                    end else if (cmd_char == "z" || cmd_char == "Z") begin
                        hw_sync_stance((hw_curr_stance == `STANCE_AGILE) ? `STANCE_BALANCED : (hw_curr_stance + 2'd1));
                        case (hw_curr_stance)
                            `STANCE_BALANCED:   combat_log_msg = "[STANCE]: Switched to BALANCED (Standard 1.0x ATK & DEF).";
                            `STANCE_BERSERK:    combat_log_msg = "[STANCE]: Switched to BERSERK (+25% ATK, -25% DEF)!";
                            `STANCE_IRON_GUARD: combat_log_msg = "[STANCE]: Switched to IRON GUARD (+50% DEF, HP regen/turn)!";
                            `STANCE_AGILE:      combat_log_msg = "[STANCE]: Switched to AGILE (+25% Dodge & +25% Flee)!";
                        endcase
                    end else if (cmd_char == "e" || cmd_char == "E" || cmd_char == " ") begin
                        // ----------------------------------------------------
                        // HIERARCHICAL SELECTION EXECUTION
                        // ----------------------------------------------------
                        if (cmenu_mode == 2'd0) begin
                            // MAIN MENU (5 Options: ATTACK, GUARD, SKILL, ITEM, FLEE)
                            if (menu_cursor == 3'd0) begin
                                cmenu_mode  = 2'd1;
                                menu_cursor = 3'd0;
                            end else if (menu_cursor == 3'd1) begin
                                if (hero_id == 4'd8) begin
                                    action_taken     = 1'b0;
                                    hero_is_guarding = 1'b0;
                                    combat_log_msg   = "NAS'HRAH REFUSES TO GUARD! 'I bow to no subterranean worm!'";
                                end else begin
                                    action_taken     = 1'b1;
                                    hero_is_guarding = 1'b1;
                                    $sformat(combat_log_msg, "%0s raises guard! Incoming damage reduced by 70%%!", hero_name);
                                end
                            end else if (menu_cursor == 3'd2) begin
                                cmenu_mode  = 2'd2;
                                menu_cursor = 3'd0;
                            end else if (menu_cursor == 3'd3) begin
                                run_solo_pouch(1'b1, sub_used_item);
                                if (sub_used_item) begin
                                    action_taken   = 1'b1;
                                    combat_log_msg = pouch_status_msg;
                                end else begin
                                    combat_log_msg = "Closed Survival Pouch without expending your turn.";
                                end
                                cmenu_mode  = 2'd0;
                                menu_cursor = 3'd0;
                            end else if (menu_cursor == 3'd4) begin
                                step_rng;
                                r_roll = hw_rand_pct;
                                if (enemy_is_crawling || hero_id == 4'd1 || r_roll < hw_stance_flee_pct) begin
                                    combat_fled = 1'b1;
                                    in_combat   = 1'b0;
                                    skip_retal  = 1'b1;
                                    $sformat(map_log_msg, "[TACTICAL RETREAT]: Disengaged cleanly from %0s back to corridor.", cur_enemy_short_name);
                                end else begin
                                    action_taken   = 1'b1;
                                    combat_log_msg = "ESCAPE FAILED! Foe blocks the narrow corridor and strikes!";
                                end
                            end
                        end else if (cmenu_mode == 2'd1) begin
                            // SUBMENU 1: TARGET LIMB (0:Head, 1:Torso, 2:R-Arm, 3:L-Arm, 4:Legs, 5:Back)
                            if (menu_cursor == 3'd5) begin
                                cmenu_mode  = 2'd0;
                                menu_cursor = 3'd0;
                            end else begin
                                action_taken = 1'b1;
                                if (menu_cursor == 3'd0) begin // HEAD
                                    step_rng;
                                    r_roll = hw_rand_pct;
                                    if (enemy_is_crawling || r_roll < 30) begin
                                        hw_calc_player_attack(`LIMB_HEAD, calc_dmg);
                                        if (enemy_is_crawling) begin
                                            enemy_head_hp = 8'd0; cur_enemy_hp = 8'd0;
                                            $sformat(combat_log_msg, "CRITICAL FINISH! Crouched foe decapitated instantly!");
                                        end else begin
                                            if (enemy_head_hp > calc_dmg) enemy_head_hp = enemy_head_hp - calc_dmg;
                                            else enemy_head_hp = 8'd0;
                                            if (enemy_head_hp == 0) begin
                                                cur_enemy_hp = 8'd0;
                                                combat_log_msg = "DECAPITATION! Fatal strike severs foe's head completely!";
                                            end else begin
                                                cur_enemy_hp = (cur_enemy_hp > calc_dmg) ? (cur_enemy_hp - calc_dmg) : 8'd0;
                                                $sformat(combat_log_msg, "%0s struck HEAD for %0d DMG! (Head HP %0d/%0d)", hero_name, calc_dmg, enemy_head_hp, enemy_head_max);
                                            end
                                        end
                                    end else begin
                                        combat_log_msg = "[MISSED]: Foe ducked away from your head strike!";
                                    end
                                end else if (menu_cursor == 3'd1) begin // TORSO
                                    step_rng;
                                    if (hw_rand_pct < 95) begin
                                        hw_calc_player_attack(`LIMB_TORSO, calc_dmg);
                                        enemy_torso_hp = (enemy_torso_hp > calc_dmg) ? (enemy_torso_hp - calc_dmg) : 8'd0;
                                        cur_enemy_hp   = (cur_enemy_hp > calc_dmg)   ? (cur_enemy_hp - calc_dmg)   : 8'd0;
                                        if (enemy_torso_hp == 0) cur_enemy_hp = 8'd0;
                                        $sformat(combat_log_msg, "%0s pierced TORSO for %0d DMG!", hero_name, calc_dmg);
                                    end else begin
                                        combat_log_msg = "[MISSED]: Strike to torso glanced off stone!";
                                    end
                                end else if (menu_cursor == 3'd2) begin // RIGHT ARM
                                    step_rng;
                                    if (hw_rand_pct < 80) begin
                                        hw_calc_player_attack(`LIMB_ARM_R, calc_dmg);
                                        enemy_arm_r_hp = (enemy_arm_r_hp > calc_dmg) ? (enemy_arm_r_hp - calc_dmg) : 8'd0;
                                        cur_enemy_hp   = (cur_enemy_hp > calc_dmg)   ? (cur_enemy_hp - calc_dmg)   : 8'd0;
                                        if (enemy_arm_r_hp == 0) begin
                                            enemy_is_disarmed = 1'b1;
                                            combat_log_msg    = "DISARMED! Weapon arm severed - Enemy ATK crippled!";
                                        end else begin
                                            $sformat(combat_log_msg, "Slashed RIGHT ARM for %0d DMG!", calc_dmg);
                                        end
                                    end else begin
                                        combat_log_msg = "[MISSED]: Strike to Right Arm deflected!";
                                    end
                                end else if (menu_cursor == 3'd3) begin // LEFT ARM
                                    step_rng;
                                    if (hw_rand_pct < 80) begin
                                        hw_calc_player_attack(`LIMB_ARM_L, calc_dmg);
                                        enemy_arm_l_hp = (enemy_arm_l_hp > calc_dmg) ? (enemy_arm_l_hp - calc_dmg) : 8'd0;
                                        cur_enemy_hp   = (cur_enemy_hp > calc_dmg)   ? (cur_enemy_hp - calc_dmg)   : 8'd0;
                                        if (enemy_arm_l_hp == 0) begin
                                            cur_enemy_def  = (cur_enemy_def > 8'd10) ? (cur_enemy_def - 8'd10) : 8'd4;
                                            combat_log_msg = "GUARD BROKEN! Left arm severed - Foe DEF shattered!";
                                        end else begin
                                            $sformat(combat_log_msg, "Slashed LEFT ARM for %0d DMG!", calc_dmg);
                                        end
                                    end else begin
                                        combat_log_msg = "[MISSED]: Strike to Left Arm missed!";
                                    end
                                end else if (menu_cursor == 3'd4) begin // LEGS
                                    step_rng;
                                    if (hw_rand_pct < 85) begin
                                        hw_calc_player_attack(`LIMB_LEGS, calc_dmg);
                                        enemy_leg_r_hp = (enemy_leg_r_hp > calc_dmg) ? (enemy_leg_r_hp - calc_dmg) : 8'd0;
                                        cur_enemy_hp   = (cur_enemy_hp > calc_dmg)   ? (cur_enemy_hp - calc_dmg)   : 8'd0;
                                        if (enemy_leg_r_hp == 0) begin
                                            enemy_is_crawling = 1'b1;
                                            combat_log_msg    = "LEGS SEVERED! Foe crawls -> 100% HEAD HIT & 100% FLEE!";
                                        end else begin
                                            $sformat(combat_log_msg, "Slashed LEGS for %0d DMG!", calc_dmg);
                                        end
                                    end else begin
                                        combat_log_msg = "[MISSED]: Beast leapt back from your leg sweep!";
                                    end
                                end
                                cmenu_mode  = 2'd0;
                                menu_cursor = 3'd0;
                            end
                        end else if (cmenu_mode == 2'd2) begin
                            // SUBMENU 2: 4 UNIQUE HERO SKILLS + BACK (0..4)
                            if (menu_cursor == 3'd4) begin
                                cmenu_mode  = 2'd0;
                                menu_cursor = 3'd2;
                            end else begin
                                case (hero_id)
                                    4'd1: begin // CAHARA
                                        if (menu_cursor == 3'd0 && hero_mind >= 8'd12) begin
                                            apply_mind_delta(-12); calc_dmg = 38;
                                            cur_enemy_hp = (cur_enemy_hp > 38) ? (cur_enemy_hp - 38) : 0;
                                            combat_log_msg = "TWIN DAGGERS! (-12 Mind) Cahara strikes twice for 38 Phys DMG!";
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd1 && hero_mind >= 8'd15) begin
                                            apply_mind_delta(-15);
                                            cur_enemy_hp  = (cur_enemy_hp > 28) ? (cur_enemy_hp - 28) : 0;
                                            cur_enemy_atk = (cur_enemy_atk > 5) ? (cur_enemy_atk - 5) : 4;
                                            combat_log_msg = "POISON DART! (-15 Mind) 28 Chem DMG bypasses armor & weakens (-5 ATK)!";
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd2 && hero_mind >= 8'd15) begin
                                            apply_mind_delta(-15);
                                            step_rng;
                                            if (hw_rand_pct < 50) begin
                                                if (bag_poppy < hero_bag_cap) bag_poppy = bag_poppy + 1;
                                                combat_log_msg = "STEAL! (-15 Mind) Pickpocketed +1 White Poppy & sliced for 14 DMG!";
                                            end else begin
                                                if (bag_bread < hero_bag_cap) bag_bread = bag_bread + 1;
                                                combat_log_msg = "STEAL! (-15 Mind) Pickpocketed +1 Moldy Bread & sliced for 14 DMG!";
                                            end
                                            cur_enemy_hp = (cur_enemy_hp > 14) ? (cur_enemy_hp - 14) : 0;
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd3 && hero_mind >= 8'd20) begin
                                            apply_mind_delta(-20);
                                            combat_fled = 1'b1; in_combat = 1'b0; skip_retal = 1'b1;
                                            $sformat(map_log_msg, "[SMOKE BOMB]: Cahara blinded %0s and vanished cleanly!", cur_enemy_short_name);
                                        end else begin
                                            combat_log_msg = "[INSUFFICIENT MIND]: Cannot cast skill! Recover Mind with Vial.";
                                        end
                                    end
                                    4'd2: begin // D'ARCE
                                        if (menu_cursor == 3'd0 && hero_mind >= 8'd10) begin
                                            apply_mind_delta(-10); hero_is_guarding = 1'b1;
                                            hw_sync_hero_hp(({1'b0, hero_hp} + 8'd15 > {1'b0, hero_max}) ? hero_max : (hero_hp + 8'd15));
                                            combat_log_msg = "DEFENSE STANCE! (-10 Mind) Iron Vow (-70% DMG next hit & +15 HP)!";
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd1 && hero_mind >= 8'd20) begin
                                            apply_mind_delta(-20);
                                            hw_sync_hero_hp(({1'b0, hero_hp} + 8'd45 > {1'b0, hero_max}) ? hero_max : (hero_hp + 8'd45));
                                            combat_log_msg = "HEALING PRAYER! (-20 Mind) Divine light restores +45 HP with 0% Tox!";
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd2 && hero_mind >= 8'd22) begin
                                            apply_mind_delta(-22);
                                            calc_dmg = (cur_enemy_arch == `ARCHETYPE_ARMORED || cur_enemy_arch == `ARCHETYPE_SPECTRAL) ? 56 : 44;
                                            if (cur_enemy_arch == `ARCHETYPE_ARMORED) begin
                                                cur_enemy_arch = `ARCHETYPE_NORMAL; cur_enemy_def = 8'd12;
                                            end
                                            cur_enemy_hp = (cur_enemy_hp > calc_dmg) ? (cur_enemy_hp - calc_dmg) : 0;
                                            $sformat(combat_log_msg, "HOLY SMITE! (-22 Mind) Sanctified blade deals %0d Divine DMG!", calc_dmg);
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd3 && hero_mind >= 8'd12) begin
                                            apply_mind_delta(-12);
                                            hw_sync_hero_hp((hero_hp > 8) ? (hero_hp - 8) : 1);
                                            cur_enemy_hp = (cur_enemy_hp > 38) ? (cur_enemy_hp - 38) : 0;
                                            combat_log_msg = "KNIGHT CHARGE! (-12 Mind, -8 Recoil HP) Slammed foe for 38 Phys DMG!";
                                            action_taken = 1'b1;
                                        end else begin
                                            combat_log_msg = "[INSUFFICIENT MIND]: Pray or drink Vial before casting!";
                                        end
                                    end
                                    4'd3: begin // ENKI
                                        if (menu_cursor == 3'd0 && hero_mind >= 8'd25) begin
                                            apply_mind_delta(-25);
                                            calc_dmg = (cur_enemy_arch == `ARCHETYPE_SPECTRAL || cur_enemy_arch == `ARCHETYPE_ARMORED) ? 78 : 52;
                                            cur_enemy_hp = (cur_enemy_hp > calc_dmg) ? (cur_enemy_hp - calc_dmg) : 0;
                                            $sformat(combat_log_msg, "BLACK ORB! (-25 Mind) True Magic pierces armor for %0d DMG!", calc_dmg);
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd1) begin
                                            apply_mind_delta(15);
                                            cur_enemy_hp = (cur_enemy_hp > 20) ? (cur_enemy_hp - 20) : 0;
                                            combat_log_msg = "RITUAL DAGGER! Enki slashes for 20 Phys DMG & siphons +15 Mind!";
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd2 && hero_hp > 8'd20) begin
                                            hw_sync_hero_hp(hero_hp - 8'd20);
                                            apply_mind_delta(40);
                                            combat_log_msg = "BLOOD SACRIFICE! (-20 HP) Forbidden blood magic harvests +40 Mind!";
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd3 && hero_mind >= 8'd15) begin
                                            apply_mind_delta(-15);
                                            enemy_is_crawling = 1'b1;
                                            combat_log_msg = "HEXEN BIND! (-15 Mind) Eldritch chains root legs (100% Head & Flee)!";
                                            action_taken = 1'b1;
                                        end else begin
                                            combat_log_msg = "[CANNOT CAST]: Check HP/Mind requirements!";
                                        end
                                    end
                                    4'd4: begin // RAGNVALDR
                                        if (menu_cursor == 3'd0) begin
                                            if (hero_mind >= 8'd14) apply_mind_delta(-14);
                                            else hw_sync_hero_hp((hero_hp > 15) ? (hero_hp - 15) : 1);
                                            calc_dmg = ({1'b0, hero_hp} * 9'd3 <= {1'b0, hero_max}) ? 72 : 48;
                                            cur_enemy_hp = (cur_enemy_hp > calc_dmg) ? (cur_enemy_hp - calc_dmg) : 0;
                                            $sformat(combat_log_msg, "WAR AXE! Brutal chop inflicts %0d DMG!", calc_dmg);
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd1 && hero_mind >= 8'd16) begin
                                            apply_mind_delta(-16);
                                            cur_enemy_hp = (cur_enemy_hp > 32) ? (cur_enemy_hp - 32) : 0;
                                            combat_log_msg = "SPIRIT TOTEM! (-16 Mind) Ancestral magic inflicts 32 True DMG!";
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd2 && hero_mind >= 8'd14) begin
                                            apply_mind_delta(-14);
                                            cur_enemy_atk = (cur_enemy_atk > 8) ? (cur_enemy_atk - (cur_enemy_atk >> 2) - (cur_enemy_atk >> 3)) : 4;
                                            combat_log_msg = "FERAL ROAR! (-14 Mind) Savage bellow lowers enemy ATK!";
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd3) begin
                                            hero_tox = ({1'b0, hero_tox} + 15 > {1'b0, hero_max_tox}) ? hero_max_tox : (hero_tox + 15);
                                            hw_sync_hero_hp(({1'b0, hero_hp} + 35 > {1'b0, hero_max}) ? hero_max : (hero_hp + 35));
                                            apply_hunger_delta(-25);
                                            combat_log_msg = "DEVOUR FLESH! (+15% Tox) Recovered +35 HP & -25 Hunger!";
                                            action_taken = 1'b1;
                                        end else begin
                                            combat_log_msg = "[INSUFFICIENT MIND]: Cannot cast skill!";
                                        end
                                    end
                                    4'd5: begin // LE'GARDE
                                        if (menu_cursor == 3'd0 && hero_mind >= 8'd12) begin
                                            apply_mind_delta(-12);
                                            calc_dmg = (legarde_ale_buff_turns > 0) ? 57 : 38;
                                            cur_enemy_hp = (cur_enemy_hp > calc_dmg) ? (cur_enemy_hp - calc_dmg) : 0;
                                            $sformat(combat_log_msg, "FENCING THRUST! (-12 Mind) Precision rapier deals %0d DMG!", calc_dmg);
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd1 && hero_mind >= 8'd20) begin
                                            apply_mind_delta(-20);
                                            cur_enemy_hp = (cur_enemy_hp > 35) ? (cur_enemy_hp - 35) : 0;
                                            combat_log_msg = "LEGION LIGHT! (-20 Mind) Solar flame burns foe for 35 Magic DMG!";
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd2 && hero_mind >= 8'd15) begin
                                            apply_mind_delta(-15);
                                            legarde_ale_buff_turns = 3'd2;
                                            combat_log_msg = "TACTICAL FOCUS! (-15 Mind) Le'garde boosts next ATK by +50%!";
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd3 && hero_mind >= 8'd14) begin
                                            apply_mind_delta(-14);
                                            cur_enemy_def = (cur_enemy_def > 6) ? (cur_enemy_def - (cur_enemy_def >> 2)) : 0;
                                            apply_mind_delta(10);
                                            combat_log_msg = "WAR CRY! Shattered enemy DEF & rallied +10 Mind!";
                                            action_taken = 1'b1;
                                        end else begin
                                            combat_log_msg = "[INSUFFICIENT MIND]: Cannot cast skill!";
                                        end
                                    end
                                    4'd6: begin // MOONLESS
                                        if (menu_cursor == 3'd0) begin
                                            apply_hunger_delta(15);
                                            cur_enemy_hp = (cur_enemy_hp > 40) ? (cur_enemy_hp - 40) : 0;
                                            combat_log_msg = "FERAL BITE! (+15 Hunger) Savage jaws tear flesh for 40 Phys DMG!";
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd1 && hero_mind >= 8'd15) begin
                                            apply_mind_delta(-15);
                                            cur_enemy_hp = (cur_enemy_hp > 30) ? (cur_enemy_hp - 30) : 0;
                                            step_rng;
                                            if (hw_rand_pct < 45) begin
                                                enemy_is_crawling = 1'b1;
                                                combat_log_msg    = "MOON HOWL! (-15 Mind) 30 Magic DMG & stunned beast crouched!";
                                            end else begin
                                                combat_log_msg    = "MOON HOWL! (-15 Mind) Eerie lunar scream inflicts 30 Magic DMG!";
                                            end
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd2 && hero_mind >= 8'd12) begin
                                            apply_mind_delta(-12);
                                            calc_dmg = enemy_is_crawling ? 55 : 35;
                                            cur_enemy_hp = (cur_enemy_hp > calc_dmg) ? (cur_enemy_hp - calc_dmg) : 0;
                                            $sformat(combat_log_msg, "SHADOW POUNCE! (-12 Mind) Leapt from shadows for %0d DMG!", calc_dmg);
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd3 && hero_mind >= 8'd10) begin
                                            apply_mind_delta(-10);
                                            scent_dodge_turns = 3'd2;
                                            combat_log_msg = "SCENT DANGER! (-10 Mind) +35% Evasion active for 2 turns!";
                                            action_taken = 1'b1;
                                        end else begin
                                            combat_log_msg = "[INSUFFICIENT MIND]: Cannot cast skill!";
                                        end
                                    end
                                    4'd7: begin // THE GIRL
                                        if (menu_cursor == 3'd0 && hero_mind >= 8'd12) begin
                                            apply_mind_delta(-12);
                                            girl_100_dodge = 1'b1;
                                            combat_log_msg = "NIMBLE DODGE! (-12 Mind) The Girl guarantees 100% Evasion next hit!";
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd1 && hero_mind >= 8'd15) begin
                                            apply_mind_delta(-15);
                                            hw_sync_hero_hp(({1'b0, hero_hp} + 35 > {1'b0, hero_max}) ? hero_max : (hero_hp + 35));
                                            combat_log_msg = "LOVING EMBRACE! (-15 Mind) Serenity heals +35 HP & calms terror!";
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd2 && hero_mind >= 8'd20) begin
                                            apply_mind_delta(-20);
                                            calc_dmg = (cur_enemy_arch == `ARCHETYPE_SPECTRAL || cur_enemy_arch == `ARCHETYPE_TERROR) ? 51 : 32;
                                            cur_enemy_hp = (cur_enemy_hp > calc_dmg) ? (cur_enemy_hp - calc_dmg) : 0;
                                            $sformat(combat_log_msg, "PURE LIGHT! (-20 Mind) Sacred radiance burns for %0d Magic DMG!", calc_dmg);
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd3 && hero_mind >= 8'd10) begin
                                            apply_mind_delta(-10);
                                            foe_half_atk_debuff = 1'b1;
                                            combat_log_msg = "DISTRACT FOE! (-10 Mind) Lantern flare cuts enemy ATK by 50%!";
                                            action_taken = 1'b1;
                                        end else begin
                                            combat_log_msg = "[INSUFFICIENT MIND]: Cannot cast skill!";
                                        end
                                    end
                                    default: begin // NAS'HRAH (8)
                                        if (menu_cursor == 3'd0 && hero_mind >= 8'd25) begin
                                            apply_mind_delta(-25);
                                            cur_enemy_hp = (cur_enemy_hp > 62) ? (cur_enemy_hp - 62) : 0;
                                            combat_log_msg = "COMBUSTION! (-25 Mind) Hellfire incinerates foe for 62 Unstoppable DMG!";
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd1 && hero_mind >= 8'd20) begin
                                            apply_mind_delta(-20);
                                            cur_enemy_hp = (cur_enemy_hp > 32) ? (cur_enemy_hp - 32) : 0;
                                            combat_log_msg = "CURSE OF DECAY! (-20 Mind) Ancient hex inflicts 32 Dark Magic DMG!";
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd2) begin
                                            cur_enemy_hp = (cur_enemy_hp > 24) ? (cur_enemy_hp - 24) : 0;
                                            hw_sync_hero_hp(({1'b0, hero_hp} + 15 > {1'b0, hero_max}) ? hero_max : (hero_hp + 15));
                                            apply_mind_delta(10);
                                            combat_log_msg = "HEAD GNAW! Nas'hrah bites for 24 DMG & siphons +15 HP/+10 Mind!";
                                            action_taken = 1'b1;
                                        end else if (menu_cursor == 3'd3 && hero_mind >= 8'd15) begin
                                            apply_mind_delta(-15);
                                            cur_enemy_def = cur_enemy_def >> 1;
                                            combat_log_msg = "MOCK FOE! (-15 Mind) Enraged beast loses 50% Defense!";
                                            action_taken = 1'b1;
                                        end else begin
                                            combat_log_msg = "[INSUFFICIENT MIND]: Cannot cast skill!";
                                        end
                                    end
                                endcase
                                if (action_taken) begin
                                    cmenu_mode  = 2'd0;
                                    menu_cursor = 3'd0;
                                end
                            end
                        end
                    end

                    // --------------------------------------------------------
                    // ENEMY RETALIATION TURN & SOLO SURVIVAL ASYMMETRY
                    // --------------------------------------------------------
                    if (action_taken && !skip_retal && in_combat && cur_enemy_hp > 0 && !combat_fled) begin
                        // Passives & Turn Upkeep
                        if (hero_id == 4'd7 && hero_tox > 0)
                            hero_tox = (hero_tox > 10) ? (hero_tox - 10) : 0;
                        if (hero_id == 4'd3) apply_mind_delta(5);
                        if (cur_enemy_arch == `ARCHETYPE_TERROR && hero_id != 4'd7 && hero_id != 4'd8)
                            apply_mind_delta(-12);
                        if (hero_has_bleed)  hw_sync_hero_hp((hero_hp > 4) ? (hero_hp - 4) : 0);
                        if (hero_has_poison) hw_sync_hero_hp((hero_hp > 5) ? (hero_hp - 5) : 0);

                        // Dodge Check
                        if (hero_hp > 0) begin
                            step_rng;
                            r_roll = hw_rand_pct;
                            if (girl_100_dodge || (r_roll < (hero_dodge + hw_stance_evasion + ((scent_dodge_turns > 0) ? 35 : 0)))) begin
                                girl_100_dodge = 1'b0;
                                $sformat(combat_log_msg, "%0s deftly evaded %0s's counter-attack (+0 DMG)!", hero_name, cur_enemy_short_name);
                            end else begin
                                // Coin Flip Lethal Strike (25% chance if arms intact & not guarding)
                                step_rng;
                                if (hw_rand_pct < 25 && !enemy_is_disarmed && !hero_is_guarding) begin
                                    coin_cursor    = 1'b0;
                                    coin_confirmed = 1'b0;
                                    while (!coin_confirmed && game_running) begin
                                        ui.render_coin_flip_prompt(coin_cursor, cur_enemy_short_name, "LETHAL CLEAVE");
                                        $fflush();
                                        scan_ret = $fscanf(32'h80000000, "%s", str_input);
                                        if (scan_ret <= 0) begin
                                            coin_selected  = coin_cursor;
                                            coin_confirmed = 1'b1;
                                        end else begin
                                            cmd_char = str_input[7:0];
                                            if (cmd_char == "w" || cmd_char == "W" || cmd_char == "s" || cmd_char == "S" || cmd_char == "k" || cmd_char == "j")
                                                coin_cursor = ~coin_cursor;
                                            else if (cmd_char == "1") begin
                                                coin_selected = `COIN_HEADS; coin_confirmed = 1'b1;
                                            end else if (cmd_char == "2") begin
                                                coin_selected = `COIN_TAILS; coin_confirmed = 1'b1;
                                            end else if (cmd_char == "e" || cmd_char == "E" || cmd_char == " ") begin
                                                coin_selected = coin_cursor; coin_confirmed = 1'b1;
                                            end
                                        end
                                    end
                                    step_rng;
                                    r_roll = hw_rand_50;
                                    $write("\033[H");
                                    ui.render_coin_animation(coin_selected, r_roll[0]);
                                    if (coin_selected == r_roll[0]) begin
                                        cur_enemy_hp = (cur_enemy_hp > 20) ? (cur_enemy_hp - 20) : 0;
                                        ui.notify_coin_result(1'b1, hero_name, 8'd20, hero_hp, hero_max, hero_mind);
                                        $sformat(combat_log_msg, "[COIN PARRY!]: %0s deflected lethal cleave & countered +20 DMG!", hero_name);
                                    end else begin
                                        hw_sync_panic_pulse();
                                        apply_mind_delta(-20);
                                        hw_calc_enemy_retaliation(1'b1, hero_is_guarding, calc_dmg);
                                        hw_sync_hero_hp((hero_hp > calc_dmg) ? (hero_hp - calc_dmg) : 8'd0);
                                        if (hero_id != 4'd8) hero_has_bleed = 1'b1;
                                        ui.notify_coin_result(1'b0, hero_name, calc_dmg[7:0], hero_hp, hero_max, hero_mind);
                                        $sformat(combat_log_msg, "[COIN FAILED!]: Took -%0d DMG, -20 Mind & Bleeding!", calc_dmg);
                                    end
                                    $write("  \033[1;33m>> Press [Enter] to continue combat: \033[0m\033[K\033[J");
                                    $fflush();
                                    wait_any_key();
                                end else begin
                                    // Normal Enemy Strike routed through Hardware ALU
                                    hw_calc_enemy_retaliation(1'b0, hero_is_guarding, calc_dmg);
                                    hw_sync_hero_hp((hero_hp > calc_dmg) ? (hero_hp - calc_dmg) : 8'd0);
                                    step_rng;
                                    if (hero_id != 4'd8 && hw_rand_pct < 25) begin
                                        hero_has_bleed = 1'b1;
                                        $sformat(combat_log_msg, "%0s struck back for -%0d DMG & inflicted Bleeding!", cur_enemy_short_name, calc_dmg);
                                    end else begin
                                        $sformat(combat_log_msg, "%0s retaliated, striking %0s for -%0d DMG!", cur_enemy_short_name, hero_name, calc_dmg);
                                    end
                                end
                            end
                        end

                        hero_is_guarding    = 1'b0;
                        foe_half_atk_debuff = 1'b0;
                        if (legarde_ale_buff_turns > 0) legarde_ale_buff_turns = legarde_ale_buff_turns - 1;
                        if (scent_dodge_turns > 0)      scent_dodge_turns      = scent_dodge_turns - 1;
                        if (hw_stance_regen_hp > 0 && hero_hp > 0)
                            hw_sync_hero_hp(({1'b0, hero_hp} + {1'b0, hw_stance_regen_hp} > {1'b0, hero_max}) ? hero_max : (hero_hp + hw_stance_regen_hp));
                        combat_turn = combat_turn + 1;
                    end

                    // Totem of Undying Emergency Revive Check if Hero HP dropped to 0
                    if (hero_hp == 0 && in_combat) begin
                        try_totem_revive(sub_used_item);
                        if (sub_used_item) begin
                            $sformat(combat_log_msg, "* [TOTEM OF UNDYING]: Golden dust defies death! Full %0d/%0d HP!", hero_hp, hero_max);
                        end else begin
                            in_combat   = 1'b0;
                            game_over   = 1'b1;
                            killer_name = cur_enemy_short_name;
                        end
                    end

                    // Victory Resolution
                    if (in_combat && cur_enemy_hp == 0) begin
                        in_combat                = 1'b0;
                        cleared_mask[target_idx] = 1'b1;
                        monsters_defeated_count  = monsters_defeated_count + 1;

                        $write("\033[H");
                        $display("\033[1;32m+==================================================================================================+\033[0m\033[K");
                        $display("\033[1;32m|  \033[42;1;37m >>> VICTORY: %-18s HAS BEEN SLAIN! SPOILS CLAIMED! <<< \033[0m\033[1;32m                           |\033[0m\033[K", cur_enemy_short_name);
                        $display("\033[1;32m+==================================================================================================+\033[0m\033[K");

                        step_rng;
                        r_roll = hw_rand_pct;
                        if (cur_enemy_drops_key && bag_keys < 8'd3) begin
                            bag_keys = bag_keys + 1;
                            hw_sync_item_receive(`ITEM_KEY, 8'd1);
                            ui.notify_receive_item("Gatekeeper Boss Bounty (Guaranteed Key)", "Dungeon Key", 8'd1);
                        end else if (cur_enemy_is_elite || cur_enemy_id == 6'd23) begin
                            if (r_roll < 60 && bag_keys < 8'd3) begin
                                bag_keys = bag_keys + 1;
                                hw_sync_item_receive(`ITEM_KEY, 8'd1);
                                ui.notify_receive_item("Elite Adversary Remains (60% Drop)", "Dungeon Key", 8'd1);
                            end
                            bag_meat = bag_meat + 1; bag_vial = bag_vial + 1;
                            ui.notify_receive_item("Elite Adversary Bounty", "Dried Meat x1 & Alchemical Vial x1", 8'd2);
                        end else begin
                            if (r_roll < 25 && bag_keys < 8'd3) begin
                                bag_keys = bag_keys + 1;
                                hw_sync_item_receive(`ITEM_KEY, 8'd1);
                                ui.notify_receive_item("Monster Remains (25% Drop)", "Dungeon Key", 8'd1);
                            end else if (r_roll < 60) begin
                                bag_bread = bag_bread + 1;
                                ui.notify_receive_item("Monster Bounty", "Moldy Bread", 8'd1);
                            end else begin
                                bag_poppy = bag_poppy + 1;
                                hw_sync_item_receive(`ITEM_POPPY, 8'd1);
                                ui.notify_receive_item("Monster Bounty", "Poppy Flower", 8'd1);
                            end
                        end

                        // Pity safety net for 3 keys
                        if (bag_keys < 8'd3) begin
                            if (((10 - monsters_defeated_count) <= (3 - bag_keys)) ||
                                (monsters_defeated_count >= 3 && bag_keys == 0) ||
                                (monsters_defeated_count >= 6 && bag_keys <= 1) ||
                                (monsters_defeated_count >= 8 && bag_keys <= 2)) begin
                                bag_keys = bag_keys + 1;
                                hw_sync_item_receive(`ITEM_KEY, 8'd1);
                                ui.notify_receive_item("Labyrinth Guarantee (Pity Safety Net)", "Dungeon Key", 8'd1);
                            end
                        end

                        $sformat(map_log_msg, "[VICTORY]: %0s neutralized #%-2d %0s! (Keys: %0d/3)", hero_name, cur_enemy_id, cur_enemy_short_name, bag_keys);
                        $write("  \033[1;33m>> Press [Enter] to collect spoils and return to Labyrinth: \033[0m\033[K\033[J");
                        $fflush();
                        wait_any_key();
                    end
                end
            end
        end

        // 6. END-GAME SCREENS
        if (game_victory) begin
            ui.render_solo_victory_screen(is_hard_mode, hero_id, hero_hp, hero_max, hero_mind, step_count, monsters_defeated_count, chests_looted_count);
            $fflush();
            wait_any_key();
        end else if (game_over) begin
            ui.render_solo_game_over_screen(hero_id, is_hard_mode, killer_name);
            $fflush();
            wait_any_key();
        end
        end

        $write("\033[2J\033[3J\033[H\033[?25h");
        if (onboard_quit)
            $display("[OK] Expedition abandoned before entering the darkness.");
        else if (!game_victory && !game_over)
            $display("[OK] Labyrinth Expedition suspended cleanly.");
        $finish;
    end

endmodule
