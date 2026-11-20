// ============================================================================
// Funger Hardware Engine: Collision & Navigation Unit (collision_unit.v)
// Synthesizable combinational unit for boundary, walls, encounters, chests, and gates
// Supports both 720-bit Cleared Mask (36x20 Labyrinth) and legacy circular buffer
// ============================================================================

`include "battle_defs.vh"

module collision_unit (
    input  wire signed [31:0] curr_x,
    input  wire signed [31:0] curr_y,
    input  wire signed [31:0] dir_dx,   // -1, 0, 1
    input  wire signed [31:0] dir_dy,   // -1, 0, 1
    input  wire [15:0]        cleared_valid,
    input  wire [127:0]       cleared_coords_x,
    input  wire [127:0]       cleared_coords_y,
    input  wire [719:0]       cleared_mask,
    output reg  signed [31:0] next_x,
    output reg  signed [31:0] next_y,
    output reg                is_blocked,
    output reg                is_monster,
    output reg                is_chest,
    output reg                is_gate,
    output reg  [2:0]         dest_tile
);

    map_rom u_map();

    integer target_x;
    integer target_y;
    reg [2:0] raw_tile;
    integer k;
    reg is_cleared;
    integer target_idx;

    always @(*) begin
        target_x   = curr_x + dir_dx;
        target_y   = curr_y + dir_dy;
        raw_tile   = u_map.get_tile(target_x, target_y);
        target_idx = target_y * `MAP_WIDTH + target_x;

        // Check if target tile has been defeated or opened
        is_cleared = 1'b0;

        // 1. Check 720-bit cleared mask (Fast hardware bit-index)
        if (target_idx >= 0 && target_idx < 720) begin
            if (cleared_mask[target_idx]) is_cleared = 1'b1;
        end

        // 2. Check legacy circular buffer (for battle_top.v compatibility)
        for (k = 0; k < 16; k = k + 1) begin
            if (cleared_valid[k] && 
                target_x == {24'd0, cleared_coords_x[k*8 +: 8]} && 
                target_y == {24'd0, cleared_coords_y[k*8 +: 8]}) begin
                is_cleared = 1'b1;
            end
        end

        if (is_cleared && (raw_tile == `TILE_MONSTER || raw_tile == `TILE_CHEST)) begin
            raw_tile = `TILE_PATH;
        end

        dest_tile = raw_tile;

        if (raw_tile == `TILE_WALL) begin
            // Blocked by green wall -> maintain current position
            next_x     = curr_x;
            next_y     = curr_y;
            is_blocked = 1'b1;
            is_monster = 1'b0;
            is_chest   = 1'b0;
            is_gate    = 1'b0;
        end else begin
            // Free to enter -> update position and flags
            next_x     = target_x;
            next_y     = target_y;
            is_blocked = 1'b0;
            is_monster = (raw_tile == `TILE_MONSTER);
            is_chest   = (raw_tile == `TILE_CHEST);
            is_gate    = (raw_tile == `TILE_GATE);
        end
    end

endmodule
