// ============================================================================
// Funger Hardware Engine: Hardware Galois LFSR PRNG Unit (rng_unit.v)
// 32-bit Galois LFSR generating hardware pseudo-random bitstream:
//   - Polynomial: x^32 + x^22 + x^2 + x^1 + 1 (Taps: 32, 22, 2, 1)
//   - 50% Boolean bit (Coin-flip & Mimic vs Loot check)
//   - 0..99 Percentage output for hit rates, item drops, and dice rolls
//   - Weighted Pseudo-random Monster ID (1 to 36)
// ============================================================================

`include "battle_defs.vh"

module rng_unit (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        step_en,
    input  wire [31:0] seed_val,
    output reg  [31:0] lfsr_val,
    output wire        rand_bit_50,        // 50% chance bit (Coin Flip / Mimic check)
    output wire [6:0]  rand_pct,           // 0 to 99 percentage value
    output reg  [5:0]  rand_monster_id     // Pseudo-random monster ID 1 to 36
);

    // 32-bit Galois Polynomial: x^32 + x^22 + x^2 + x^1 + 1 (Taps: 32, 22, 2, 1)
    wire lfsr_feedback = lfsr_val[31];

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            if (seed_val != 32'd0)
                lfsr_val <= seed_val;
            else
                lfsr_val <= 32'hACE1_5729;
        end else if (step_en) begin
            if (lfsr_feedback)
                lfsr_val <= (lfsr_val << 1) ^ 32'h0040_0007;
            else
                lfsr_val <= (lfsr_val << 1);
        end
    end

    // 50% boolean outcome (Bit 0 of Galois LFSR has ideal uniform distribution)
    assign rand_bit_50 = lfsr_val[0];

    // 0..99 percentage modulo
    assign rand_pct = lfsr_val[15:0] % 100;

    // Weighted spawn distribution for 36 monsters:
    // Exclude ID 23 (Mimic) from open dungeon encounters
    always @(*) begin
        if ((lfsr_val[7:0] % 36) + 6'd1 == 6'd23)
            rand_monster_id = 6'd24;
        else
            rand_monster_id = (lfsr_val[7:0] % 36) + 6'd1;
    end

endmodule
