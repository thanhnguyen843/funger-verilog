// ============================================================================
// Unit Test: Damage ALU Verification (tb_damage_alu.v)
// Verifies Section 2.2 Damage Matrix & Action Resolution:
//   Case 1: Attack  vs Attack  -> Damage P1: 20, P2: 20
//   Case 2: Attack  vs Defend  -> Damage P1:  0, P2:  5
//   Case 3: Defend  vs Attack  -> Damage P1:  5, P2:  0
//   Case 4: Defend  vs Defend  -> Damage P1:  0, P2:  0
// ============================================================================

`timescale 1ns / 1ps
`include "battle_defs.vh"

module tb_damage_alu;

    reg  [1:0] p1_action;
    reg  [1:0] p2_action;
    wire [7:0] p1_damage;
    wire [7:0] p2_damage;

    integer errors = 0;

    damage_alu dut (
        .p1_action(p1_action),
        .p2_action(p2_action),
        .p1_damage(p1_damage),
        .p2_damage(p2_damage)
    );

    initial begin
        $display("\n========================================================");
        $display("   TESTBENCH: DAMAGE ALU 2x2 COMBAT MATRIX VERIFICATION");
        $display("========================================================");

        // Case 1: Attack vs Attack
        p1_action = `ACTION_ATTACK; p2_action = `ACTION_ATTACK; #10;
        if (p1_damage === 8'd20 && p2_damage === 8'd20)
            $display("[PASS] Case 1 (Attack vs Attack): P1 Dmg = %0d, P2 Dmg = %0d", p1_damage, p2_damage);
        else begin
            $display("[FAIL] Case 1: Expected (20, 20), Got (%0d, %0d)", p1_damage, p2_damage);
            errors = errors + 1;
        end

        // Case 2: Attack vs Defend
        p1_action = `ACTION_ATTACK; p2_action = `ACTION_DEFEND; #10;
        if (p1_damage === 8'd0 && p2_damage === 8'd5)
            $display("[PASS] Case 2 (Attack vs Defend): P1 Dmg = %0d, P2 Dmg = %0d", p1_damage, p2_damage);
        else begin
            $display("[FAIL] Case 2: Expected (0, 5), Got (%0d, %0d)", p1_damage, p2_damage);
            errors = errors + 1;
        end

        // Case 3: Defend vs Attack
        p1_action = `ACTION_DEFEND; p2_action = `ACTION_ATTACK; #10;
        if (p1_damage === 8'd5 && p2_damage === 8'd0)
            $display("[PASS] Case 3 (Defend vs Attack): P1 Dmg = %0d, P2 Dmg = %0d", p1_damage, p2_damage);
        else begin
            $display("[FAIL] Case 3: Expected (5, 0), Got (%0d, %0d)", p1_damage, p2_damage);
            errors = errors + 1;
        end

        // Case 4: Defend vs Defend
        p1_action = `ACTION_DEFEND; p2_action = `ACTION_DEFEND; #10;
        if (p1_damage === 8'd0 && p2_damage === 8'd0)
            $display("[PASS] Case 4 (Defend vs Defend): P1 Dmg = %0d, P2 Dmg = %0d", p1_damage, p2_damage);
        else begin
            $display("[FAIL] Case 4: Expected (0, 0), Got (%0d, %0d)", p1_damage, p2_damage);
            errors = errors + 1;
        end

        $display("--------------------------------------------------------");
        if (errors == 0)
            $display(">>> ALL ALU TEST CASES PASSED SUCCESSFULLY! <<<\n");
        else
            $display(">>> TEST FAILED WITH %0d ERRORS! <<<\n", errors);

        $finish;
    end

endmodule
