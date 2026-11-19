// ============================================================================
// Module: sprite_router.v
// Dynamic Sprite Router connecting:
//   1. 8 Standalone Fear & Hunger Player Character ROMs (TrueColor 24-bit)
//   2. 20 Monochrome Retro Monsters from monster.v
//   3. 16 Classic Fantasy Creatures from fantasy_creatures.v (including Mimic)
// ============================================================================

`timescale 1ns / 1ps

module sprite_router;

    // --- Fear & Hunger 8 Character Instances (Top and Bot scan) ---
    reg [5:0] cr_t, cc_t, cr_b, cc_b;
    reg       cfh;

    // Cahara
    wire [7:0] cr_cah_t, cg_cah_t, cb_cah_t, cr_cah_b, cg_cah_b, cb_cah_b;
    wire t_cahara_t, t_cahara_b;
    funger_cahara_rom u_cahara_t (.flip_h(cfh), .row(cr_t), .col(cc_t), .pixel_val(), .is_transparent(t_cahara_t), .r(cr_cah_t), .g(cg_cah_t), .b(cb_cah_t));
    funger_cahara_rom u_cahara_b (.flip_h(cfh), .row(cr_b), .col(cc_b), .pixel_val(), .is_transparent(t_cahara_b), .r(cr_cah_b), .g(cg_cah_b), .b(cb_cah_b));

    // D'arce
    wire [7:0] cr_dar_t, cg_dar_t, cb_dar_t, cr_dar_b, cg_dar_b, cb_dar_b;
    wire t_darce_t, t_darce_b;
    funger_darce_rom u_darce_t (.flip_h(cfh), .row(cr_t), .col(cc_t), .pixel_val(), .is_transparent(t_darce_t), .r(cr_dar_t), .g(cg_dar_t), .b(cb_dar_t));
    funger_darce_rom u_darce_b (.flip_h(cfh), .row(cr_b), .col(cc_b), .pixel_val(), .is_transparent(t_darce_b), .r(cr_dar_b), .g(cg_dar_b), .b(cb_dar_b));

    // Enki
    wire [7:0] cr_enk_t, cg_enk_t, cb_enk_t, cr_enk_b, cg_enk_b, cb_enk_b;
    wire t_enki_t, t_enki_b;
    funger_enki_rom u_enki_t (.flip_h(cfh), .row(cr_t), .col(cc_t), .pixel_val(), .is_transparent(t_enki_t), .r(cr_enk_t), .g(cg_enk_t), .b(cb_enk_t));
    funger_enki_rom u_enki_b (.flip_h(cfh), .row(cr_b), .col(cc_b), .pixel_val(), .is_transparent(t_enki_b), .r(cr_enk_b), .g(cg_enk_b), .b(cb_enk_b));

    // Ragnvaldr
    wire [7:0] cr_rag_t, cg_rag_t, cb_rag_t, cr_rag_b, cg_rag_b, cb_rag_b;
    wire t_ragn_t, t_ragn_b;
    funger_ragnvaldr_rom u_ragn_t (.flip_h(cfh), .row(cr_t), .col(cc_t), .pixel_val(), .is_transparent(t_ragn_t), .r(cr_rag_t), .g(cg_rag_t), .b(cb_rag_t));
    funger_ragnvaldr_rom u_ragn_b (.flip_h(cfh), .row(cr_b), .col(cc_b), .pixel_val(), .is_transparent(t_ragn_b), .r(cr_rag_b), .g(cg_rag_b), .b(cb_rag_b));

    // Le'garde
    wire [7:0] cr_leg_t, cg_leg_t, cb_leg_t, cr_leg_b, cg_leg_b, cb_leg_b;
    wire t_leg_t, t_leg_b;
    funger_legarde_rom u_leg_t (.flip_h(cfh), .row(cr_t), .col(cc_t), .pixel_val(), .is_transparent(t_leg_t), .r(cr_leg_t), .g(cg_leg_t), .b(cb_leg_t));
    funger_legarde_rom u_leg_b (.flip_h(cfh), .row(cr_b), .col(cc_b), .pixel_val(), .is_transparent(t_leg_b), .r(cr_leg_b), .g(cg_leg_b), .b(cb_leg_b));

    // Moonless
    wire [7:0] cr_moo_t, cg_moo_t, cb_moo_t, cr_moo_b, cg_moo_b, cb_moo_b;
    wire t_moon_t, t_moon_b;
    funger_moonless_rom u_moon_t (.flip_h(cfh), .row(cr_t), .col(cc_t), .pixel_val(), .is_transparent(t_moon_t), .r(cr_moo_t), .g(cg_moo_t), .b(cb_moo_t));
    funger_moonless_rom u_moon_b (.flip_h(cfh), .row(cr_b), .col(cc_b), .pixel_val(), .is_transparent(t_moon_b), .r(cr_moo_b), .g(cg_moo_b), .b(cb_moo_b));

    // The Girl
    wire [7:0] cr_gir_t, cg_gir_t, cb_gir_t, cr_gir_b, cg_gir_b, cb_gir_b;
    wire t_girl_t, t_girl_b;
    funger_thegirl_rom u_girl_t (.flip_h(cfh), .row(cr_t), .col(cc_t), .pixel_val(), .is_transparent(t_girl_t), .r(cr_gir_t), .g(cg_gir_t), .b(cb_gir_t));
    funger_thegirl_rom u_girl_b (.flip_h(cfh), .row(cr_b), .col(cc_b), .pixel_val(), .is_transparent(t_girl_b), .r(cr_gir_b), .g(cg_gir_b), .b(cb_gir_b));

    // Nas'hrah
    wire [7:0] cr_nas_t, cg_nas_t, cb_nas_t, cr_nas_b, cg_nas_b, cb_nas_b;
    wire t_nash_t, t_nash_b;
    funger_nashrah_rom u_nash_t (.flip_h(cfh), .row(cr_t), .col(cc_t), .pixel_val(), .is_transparent(t_nash_t), .r(cr_nas_t), .g(cg_nas_t), .b(cb_nas_t));
    funger_nashrah_rom u_nash_b (.flip_h(cfh), .row(cr_b), .col(cc_b), .pixel_val(), .is_transparent(t_nash_b), .r(cr_nas_b), .g(cg_nas_b), .b(cb_nas_b));

    // --- Monster Instances (monster.v) ---
    reg [4:0] m_id_m; reg [4:0] mr_t, mc_t, mr_b, mc_b;
    wire m_pv_t, m_pv_b, m_trans_t, m_trans_b;
    wire [4:0] mw_t, mh_t, mw_b, mh_b;
    wire [7:0] mr_rt, mg_gt, mb_bt, mr_rb, mg_gb, mb_bb;
    monster u_mon_t (.monster_id(m_id_m), .row(mr_t), .col(mc_t), .pixel_val(m_pv_t), .is_transparent(m_trans_t), .width(mw_t), .height(mh_t), .r(mr_rt), .g(mg_gt), .b(mb_bt));
    monster u_mon_b (.monster_id(m_id_m), .row(mr_b), .col(mc_b), .pixel_val(m_pv_b), .is_transparent(m_trans_b), .width(mw_b), .height(mh_b), .r(mr_rb), .g(mg_gb), .b(mb_bb));

    // --- Fantasy Creatures Instances (fantasy_creatures.v) ---
    reg [3:0] fc_id; reg [3:0] fcr_t, fcc_t, fcr_b, fcc_b;
    wire fc_pv_t, fc_pv_b, fc_trans_t, fc_trans_b;
    wire [7:0] fcr_rt, fcg_gt, fcb_bt, fcr_rb, fcg_gb, fcb_bb;
    fantasy_creatures u_fc_t (.creature_id(fc_id), .row(fcr_t), .col(fcc_t), .pixel_val(fc_pv_t), .is_transparent(fc_trans_t), .r(fcr_rt), .g(fcg_gt), .b(fcb_bt));
    fantasy_creatures u_fc_b (.creature_id(fc_id), .row(fcr_b), .col(fcc_b), .pixel_val(fc_pv_b), .is_transparent(fc_trans_b), .r(fcr_rb), .g(fcg_gb), .b(fcb_bb));

    // Task to get Funger Player Character Dimensions
    task get_funger_dim;
        input  [3:0] cid;
        output [5:0] w, h;
        begin
            case (cid)
                4'd1: begin w = 6'd26; h = 6'd24; end // Cahara
                4'd2: begin w = 6'd24; h = 6'd24; end // D'arce
                4'd3: begin w = 6'd14; h = 6'd24; end // Enki
                4'd4: begin w = 6'd22; h = 6'd28; end // Ragnvaldr
                4'd5: begin w = 6'd26; h = 6'd26; end // Le'garde
                4'd6: begin w = 6'd22; h = 6'd24; end // Moonless
                4'd7: begin w = 6'd12; h = 6'd20; end // The Girl
                4'd8: begin w = 6'd12; h = 6'd20; end // Nas'hrah
                default: begin w = 6'd20; h = 6'd20; end
            endcase
        end
    endtask

    // Task to sample Funger Character Pixel (Top & Bottom half-block)
    task sample_funger_pixel;
        input  [3:0]  cid;
        input  [5:0]  r_t, r_b, col;
        input         flip_h;
        output        t_t; output [23:0] rgb_t;
        output        t_b; output [23:0] rgb_b;
        begin
            cr_t = r_t; cr_b = r_b; cc_t = col; cc_b = col; cfh = flip_h;
            #1;
            case (cid)
                4'd1: begin t_t = t_cahara_t; rgb_t = {cr_cah_t, cg_cah_t, cb_cah_t}; t_b = t_cahara_b; rgb_b = {cr_cah_b, cg_cah_b, cb_cah_b}; end
                4'd2: begin t_t = t_darce_t;  rgb_t = {cr_dar_t, cg_dar_t, cb_dar_t}; t_b = t_darce_b;  rgb_b = {cr_dar_b, cg_dar_b, cb_dar_b}; end
                4'd3: begin t_t = t_enki_t;   rgb_t = {cr_enk_t, cg_enk_t, cb_enk_t}; t_b = t_enki_b;   rgb_b = {cr_enk_b, cg_enk_b, cb_enk_b}; end
                4'd4: begin t_t = t_ragn_t;   rgb_t = {cr_rag_t, cg_rag_t, cb_rag_t}; t_b = t_ragn_b;   rgb_b = {cr_rag_b, cg_rag_b, cb_rag_b}; end
                4'd5: begin t_t = t_leg_t;    rgb_t = {cr_leg_t, cg_leg_t, cb_leg_t}; t_b = t_leg_b;    rgb_b = {cr_leg_b, cg_leg_b, cb_leg_b}; end
                4'd6: begin t_t = t_moon_t;   rgb_t = {cr_moo_t, cg_moo_t, cb_moo_t}; t_b = t_moon_b;   rgb_b = {cr_moo_b, cg_moo_b, cb_moo_b}; end
                4'd7: begin t_t = t_girl_t;   rgb_t = {cr_gir_t, cg_gir_t, cb_gir_t}; t_b = t_girl_b;   rgb_b = {cr_gir_b, cg_gir_b, cb_gir_b}; end
                4'd8: begin t_t = t_nash_t;   rgb_t = {cr_nas_t, cg_nas_t, cb_nas_t}; t_b = t_nash_b;   rgb_b = {cr_nas_b, cg_nas_b, cb_nas_b}; end
                default: begin t_t = 1'b1; rgb_t = 0; t_b = 1'b1; rgb_b = 0; end
            endcase
        end
    endtask

    // Task to get Monster Dimensions
    task get_monster_dim;
        input  [5:0] mid;
        output [5:0] w, h;
        begin
            if (mid <= 6'd20) begin
                m_id_m = mid[4:0] - 5'd1; mr_t = 0; mc_t = 0; #1;
                w = mw_t; h = mh_t;
            end else begin
                w = 6'd16; h = 6'd16;
            end
        end
    endtask

    // Task to sample Monster Pixel (Top & Bottom half-block)
    task sample_monster_pixel;
        input  [5:0]  mid;
        input  [5:0]  r_t, r_b, col;
        output        t_t; output [23:0] rgb_t;
        output        t_b; output [23:0] rgb_b;
        begin
            if (mid <= 6'd20) begin
                // From monster.v
                m_id_m = mid[4:0] - 5'd1;
                mr_t   = r_t[4:0]; mc_t = col[4:0];
                mr_b   = r_b[4:0]; mc_b = col[4:0];
                #1;
                t_t   = m_trans_t; rgb_t = {mr_rt, mg_gt, mb_bt};
                t_b   = m_trans_b; rgb_b = {mr_rb, mg_gb, mb_bb};
            end else begin
                // From fantasy_creatures.v (creature_id = mid - 21)
                fc_id = mid - 6'd21;
                fcr_t = r_t[3:0]; fcc_t = col[3:0];
                fcr_b = r_b[3:0]; fcc_b = col[3:0];
                #1;
                t_t   = fc_trans_t; rgb_t = {fcr_rt, fcg_gt, fcb_bt};
                t_b   = fc_trans_b; rgb_b = {fcr_rb, fcg_gb, fcb_bb};
            end
        end
    endtask

endmodule
