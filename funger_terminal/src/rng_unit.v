// ============================================================================
// Pokemon Lite: Terror & Starvation - RNG Unit (rng_unit.v)
// 32-bit Galois LFSR generating pseudo-random values for drafts, weighted spawns & flee
// ============================================================================

`include "battle_defs.vh"

module rng_unit (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        step_en,
    input  wire [31:0] seed_val,
    output reg  [31:0] lfsr_val,
    output wire        rand_bit_50,        // 50% chance bit (Flee check)
    output reg  [4:0]  rand_monster_id     // Weighted pseudo-random monster ID 1 to 25
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

    // 50% boolean outcome
    assign rand_bit_50 = lfsr_val[0];

    // Weighted spawn distribution:
    // 0..165   (64.8%): Common low-tier creatures (IDs 1..10)
    // 166..237 (28.1%): Mid-tier creatures (IDs 11..20)
    // 238..255 ( 7.0%): Rare / Boss creatures (IDs 21..25)
    always @(*) begin
        if (lfsr_val[7:0] < 8'd166) begin
            rand_monster_id = (lfsr_val[7:0] % 10) + 5'd1;
        end else if (lfsr_val[7:0] < 8'd238) begin
            rand_monster_id = ((lfsr_val[7:0] - 8'd166) % 10) + 5'd11;
        end else begin
            rand_monster_id = ((lfsr_val[7:0] - 8'd238) % 5) + 5'd21;
        end
    end

endmodule
