// ============================================================================
// Testbench: tb_show_monster_states.v
// Tri-State Postural Morphology & Amber Palette Hardware Showcase
// Hardware RTL Verification for Fear & Hunger: Terminal Labyrinth
// ============================================================================

`timescale 1ns / 1ps

module tb_show_monster_states;

    reg  [5:0] mid;
    reg  [1:0] st_norm = 2'b00;
    reg  [1:0] st_inj  = 2'b01;
    reg  [1:0] st_dead = 2'b10;

    reg  [4:0] r_top, r_bot, col_idx;

    // Normal instance (State 0 - Phosphor White)
    wire       px_n_t, trans_n_t, px_n_b, trans_n_b;
    wire [4:0] w_n, h_n;
    wire [7:0] rn_t, gn_t, bn_t, rn_b, gn_b, bn_b;

    monster_state_model u_mod_norm_t (
        .monster_id(mid), .state(st_norm), .row(r_top), .col(col_idx),
        .pixel_val(px_n_t), .is_transparent(trans_n_t),
        .width(w_n), .height(h_n),
        .r(rn_t), .g(gn_t), .b(bn_t)
    );
    monster_state_model u_mod_norm_b (
        .monster_id(mid), .state(st_norm), .row(r_bot), .col(col_idx),
        .pixel_val(px_n_b), .is_transparent(trans_n_b),
        .width(), .height(),
        .r(rn_b), .g(gn_b), .b(bn_b)
    );

    // Injured instance (State 1 - Technical Amber)
    wire       px_i_t, trans_i_t, px_i_b, trans_i_b;
    wire [4:0] w_i, h_i;
    wire [7:0] ri_t, gi_t, bi_t, ri_b, gi_b, bi_b;

    monster_state_model u_mod_inj_t (
        .monster_id(mid), .state(st_inj), .row(r_top), .col(col_idx),
        .pixel_val(px_i_t), .is_transparent(trans_i_t),
        .width(w_i), .height(h_i),
        .r(ri_t), .g(gi_t), .b(bi_t)
    );
    monster_state_model u_mod_inj_b (
        .monster_id(mid), .state(st_inj), .row(r_bot), .col(col_idx),
        .pixel_val(px_i_b), .is_transparent(trans_i_b),
        .width(), .height(),
        .r(ri_b), .g(gi_b), .b(bi_b)
    );

    // Dead instance (State 2 - Deactivated Ash Gray)
    wire       px_d_t, trans_d_t, px_d_b, trans_d_b;
    wire [4:0] w_d, h_d;
    wire [7:0] rd_t, gd_t, bd_t, rd_b, gd_b, bd_b;

    monster_state_model u_mod_dead_t (
        .monster_id(mid), .state(st_dead), .row(r_top), .col(col_idx),
        .pixel_val(px_d_t), .is_transparent(trans_d_t),
        .width(w_d), .height(h_d),
        .r(rd_t), .g(gd_t), .b(bd_t)
    );
    monster_state_model u_mod_dead_b (
        .monster_id(mid), .state(st_dead), .row(r_bot), .col(col_idx),
        .pixel_val(px_d_b), .is_transparent(trans_d_b),
        .width(), .height(),
        .r(rd_b), .g(gd_b), .b(bd_b)
    );

    task print_hb_pixel;
        input        tt;
        input [7:0]  rt, gt, bt;
        input        tb;
        input [7:0]  rb, gb, bb;
        begin
            if (!tt && !tb) begin
                $write("\033[38;2;%0d;%0d;%0dm\033[48;2;%0d;%0d;%0dm\342\226\200\033[0m", rt, gt, bt, rb, gb, bb);
            end else if (!tt && tb) begin
                $write("\033[0m\033[38;2;%0d;%0d;%0dm\342\226\200\033[0m", rt, gt, bt);
            end else if (tt && !tb) begin
                $write("\033[0m\033[38;2;%0d;%0d;%0dm\342\226\204\033[0m", rb, gb, bb);
            end else begin
                $write(" ");
            end
        end
    endtask

    // Helper task to get Monster Name
    task get_monster_name;
        input  [5:0] id;
        output [159:0] name;
        begin
            case (id)
                6'd1:  name = "Mage Ghost";
                6'd2:  name = "Classic Ghost";
                6'd3:  name = "Maw Slime";
                6'd4:  name = "Brachio Titan";
                6'd5:  name = "Antler Totem";
                6'd6:  name = "Kraken Octopus";
                6'd7:  name = "Beholder Eye";
                6'd8:  name = "Shadow Swordsman";
                6'd9:  name = "Giant Snail";
                6'd10: name = "Grave Spider";
                6'd11: name = "Dungeon Ant";
                6'd12: name = "Battle Llama";
                6'd13: name = "Shadow Hound";
                6'd14: name = "Forest Stag";
                6'd15: name = "Cave Gnome";
                6'd16: name = "Mini Knight";
                6'd17: name = "Little Drake";
                6'd18: name = "Shadow Slug";
                6'd19: name = "Dark Construct";
                6'd20: name = "Abyssal Overlord";
                6'd21: name = "Wyvern";
                6'd22: name = "Gargoyle";
                6'd23: name = "Chest Mimic";
                6'd24: name = "Hydra Serpent";
                6'd25: name = "Imp Demon";
                6'd26: name = "Spectral Beast";
                6'd27: name = "Ancient Treant";
                6'd28: name = "Abyss Beholder";
                6'd29: name = "Dungeon Basilisk";
                6'd30: name = "Chimera Horror";
                6'd31: name = "Cave Manticore";
                6'd32: name = "Cathedral Gargoyle";
                6'd33: name = "Troll Berserker";
                6'd34: name = "Crypt Vampire";
                6'd35: name = "Lich Necromancer";
                6'd36: name = "Dark Dragon";
                default: name = "Unknown Horror";
            endcase
        end
    endtask

    integer i, r, c;
    reg [159:0] m_name;
    reg [4:0] max_w, max_h;

    initial begin
        $display("");
        $display("\033[1;30m+====================================================================================================+\033[0m");
        $display("\033[1;30m| \033[1;37m     FEAR & HUNGER: TRI-STATE POSTURAL MORPHOLOGY SHOWCASE (NORMAL vs INJURED vs DEAD)        \033[1;30m|\033[0m");
        $display("\033[1;30m+====================================================================================================+\033[0m");
        $display("");

        // Showcase all 36 foes in Tri-State layout
        for (i = 1; i <= 36; i = i + 1) begin
            mid = i[5:0];
            get_monster_name(mid, m_name);
            #2;
            max_w = w_n;
            max_h = h_n;

            $display("\033[1;33m>>> FOE #%02d: %s \033[90m(Dimensions: %0dx%0d pixels)\033[0m", mid, m_name, max_w, max_h);
            $display("\033[90m+---------------------------+    +---------------------------+    +---------------------------+\033[0m");
            $display("\033[1;37m|    [STATE 0: NORMAL]      |    \033[1;33m|    [STATE 1: INJURED]     |    \033[90m|     [STATE 2: DEAD]       |\033[0m");
            $display("\033[90m| Phosphor White (Standing) |    | White Body + Amber Joints |    | Ash Gray (Neutralized)    |\033[0m");
            $display("\033[90m+---------------------------+    +---------------------------+    +---------------------------+\033[0m");

            // Render each monster side-by-side (2 rows of pixels per character row)
            for (r = 0; r < max_h; r = r + 2) begin
                r_top = r[4:0];
                r_bot = (r + 1 < max_h) ? (r[4:0] + 5'd1) : 5'd31;

                // --- 1. STATE 0: NORMAL (Phosphor White) ---
                $write("  ");
                for (c = 0; c < 24; c = c + 1) begin
                    col_idx = c[4:0];
                    #1;
                    if (c < max_w)
                        print_hb_pixel(trans_n_t, rn_t, gn_t, bn_t, (r_bot == 5'd31) ? 1'b1 : trans_n_b, rn_b, gn_b, bn_b);
                    else
                        $write(" ");
                end

                // --- 2. STATE 1: INJURED (Technical Amber) ---
                $write("       ");
                for (c = 0; c < 24; c = c + 1) begin
                    col_idx = c[4:0];
                    #1;
                    if (c < max_w)
                        print_hb_pixel(trans_i_t, ri_t, gi_t, bi_t, (r_bot == 5'd31) ? 1'b1 : trans_i_b, ri_b, gi_b, bi_b);
                    else
                        $write(" ");
                end

                // --- 3. STATE 2: DEAD (Ash Gray) ---
                $write("       ");
                for (c = 0; c < 24; c = c + 1) begin
                    col_idx = c[4:0];
                    #1;
                    if (c < max_w)
                        print_hb_pixel(trans_d_t, rd_t, gd_t, bd_t, (r_bot == 5'd31) ? 1'b1 : trans_d_b, rd_b, gd_b, bd_b);
                    else
                        $write(" ");
                end
                $display("");
            end

            $display("\033[90m----------------------------------------------------------------------------------------------------\033[0m");
            $display("");
        end

        $display("\033[1;32m[OK] Tri-State Postural Morphology & Amber Palette showcase complete for all 36 monsters!\033[0m\n");
        $finish;
    end

endmodule
