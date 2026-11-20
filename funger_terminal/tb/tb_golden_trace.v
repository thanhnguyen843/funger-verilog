`timescale 1ns / 1ps
`include "battle_defs.vh"

module tb_golden_trace;
    reg  [1:0] p1_action;
    reg  [1:0] p2_action;
    reg  [7:0] p1_base_atk;
    reg  [7:0] p2_base_atk;
    reg  [7:0] p1_def;
    reg  [7:0] p2_def;
    reg  [3:0] rng_bits;
    reg  [7:0] p1_curr_hp;
    reg        is_flee_failed;
    reg  [2:0] limb_target;
    reg        is_lethal_mode;
    reg        enemy_disarmed;

    wire [7:0] p1_damage;
    wire [7:0] p2_damage;
    wire [7:0] p1_flee_penalty;

    damage_alu dut_alu (
        .p1_action      (p1_action),
        .p2_action      (p2_action),
        .p1_base_atk    (p1_base_atk),
        .p2_base_atk    (p2_base_atk),
        .p1_def         (p1_def),
        .p2_def         (p2_def),
        .rng_bits       (rng_bits),
        .p1_curr_hp     (p1_curr_hp),
        .is_flee_failed (is_flee_failed),
        .limb_target    (limb_target),
        .is_lethal_mode (is_lethal_mode),
        .enemy_disarmed (enemy_disarmed),
        .p1_damage      (p1_damage),
        .p2_damage      (p2_damage),
        .p1_flee_penalty(p1_flee_penalty)
    );

    integer file_trace;
    integer i;

    task dump_vector;
        input integer test_id;
        begin
            #1;
            $fdisplay(file_trace, "%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d",
                test_id, p1_action, p2_action, p1_base_atk, p2_base_atk,
                p1_def, p2_def, rng_bits, p1_curr_hp, is_flee_failed,
                limb_target, is_lethal_mode, enemy_disarmed,
                p1_damage, p2_damage, p1_flee_penalty
            );
        end
    endtask

    initial begin
        file_trace = $fopen("sim/alu_trace.csv", "w");
        $fdisplay(file_trace, "test_id,p1_act,p2_act,p1_atk,p2_atk,p1_def,p2_def,rng,hp,flee_fail,limb,lethal,disarm,p1_dmg,p2_dmg,flee_pen");

        // Edge Case 1: Minimum ATK vs Maximum DEF (Saturation Underflow Check)
        p1_action = `ACTION_ATTACK; p2_action = `ACTION_ATTACK;
        p1_base_atk = 8'd0; p2_base_atk = 8'd0; p1_def = 8'd255; p2_def = 8'd255;
        rng_bits = 4'd1; p1_curr_hp = 8'd100; is_flee_failed = 0; limb_target = `LIMB_TORSO;
        is_lethal_mode = 0; enemy_disarmed = 0;
        dump_vector(1);

        // Edge Case 2: Maximum ATK vs Minimum DEF + 1.5x Crit (Overflow Check)
        p1_base_atk = 8'd255; p2_base_atk = 8'd255; p1_def = 8'd0; p2_def = 8'd0;
        rng_bits = 4'b1111; // Hardware crit
        dump_vector(2);

        // Edge Case 3: Head Strike (1.5x Multiplier) vs Normal Guard
        p1_base_atk = 8'd30; p2_base_atk = 8'd20; p1_def = 8'd10; p2_def = 8'd10;
        p2_action = `ACTION_DEFEND; limb_target = `LIMB_HEAD; rng_bits = 4'd1;
        dump_vector(3);

        // Edge Case 4: Disarmed Enemy Strike
        p1_action = `ACTION_ATTACK; p2_action = `ACTION_ATTACK;
        p1_base_atk = 8'd25; p2_base_atk = 8'd40; p1_def = 8'd10; p2_def = 8'd10;
        limb_target = `LIMB_TORSO; enemy_disarmed = 1;
        dump_vector(4);

        // Edge Case 5: Flee Penalty Edge Cases (HP = 1, 2, 3, 90, 255)
        is_flee_failed = 1;
        p1_curr_hp = 8'd1; dump_vector(5);
        p1_curr_hp = 8'd2; dump_vector(6);
        p1_curr_hp = 8'd3; dump_vector(7);
        p1_curr_hp = 8'd90; dump_vector(8);
        p1_curr_hp = 8'd255; dump_vector(9);

        // 100 Random Vectors
        is_flee_failed = 0; enemy_disarmed = 0;
        for (i = 10; i < 200; i = i + 1) begin
            p1_action   = (i % 3 == 0) ? `ACTION_DEFEND : `ACTION_ATTACK;
            p2_action   = (i % 4 == 0) ? `ACTION_DEFEND : `ACTION_ATTACK;
            p1_base_atk = (i * 17) % 256;
            p2_base_atk = (i * 23) % 256;
            p1_def      = (i * 11) % 256;
            p2_def      = (i * 13) % 256;
            rng_bits    = i % 16;
            p1_curr_hp  = (i * 7) % 256;
            limb_target = (i % 5);
            is_lethal_mode = (i % 17 == 0);
            enemy_disarmed = (i % 7 == 0);
            dump_vector(i);
        end

        $fclose(file_trace);
        $finish;
    end
endmodule
