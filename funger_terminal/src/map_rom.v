// ============================================================================
// Pokemon Lite: Terror & Starvation - Redesigned Map ROM (map_rom.v)
// Completely in English:
//   - TILE_WALL: Green blocks with no text (\033[42m  \033[0m)
//   - TILE_PATH: Path with grid dots (\033[90m .\033[0m)
//   - TILE_MONSTER: Purple 'M' encounter tiles
//   - TILE_CHEST: Brown 'C' treasure chest tiles (50% Mimic / 50% Loot)
//   - TILE_GATE: Cyan 'G' exit gates EMBEDDED DIRECTLY ON THE RIGHTMOST WALL (x=35)
//     GUARANTEED to have a gatekeeper monster directly guarding in front at (34, y)
//     with narrow walls blocking any path around it!
// ============================================================================

`timescale 1ns / 1ps
`include "battle_defs.vh"

module map_rom (
    input  wire signed [31:0] in_x,
    input  wire signed [31:0] in_y,
    output wire [2:0]         out_tile
);

    function [2:0] get_tile;
        input integer x;
        input integer y;
        begin
            // 1. GATES EMBEDDED ON THE RIGHTMOST OUTER WALL (x = 35)
            // Gate 1 at (35, 6)
            if (x == (`MAP_WIDTH - 1) && y == 6) begin
                get_tile = `TILE_GATE;
            end
            // Gate 2 at (35, 14)
            else if (x == (`MAP_WIDTH - 1) && y == 14) begin
                get_tile = `TILE_GATE;
            end

            // 2. OUTER BOUNDARY WALLS (Right wall except for Gates)
            else if (x <= 0 || x >= (`MAP_WIDTH - 1) || y <= 0 || y >= (`MAP_HEIGHT - 1)) begin
                get_tile = `TILE_WALL;
            end

            // 3. GATEKEEPER MONSTERS DIRECTLY IN FRONT OF GATES (x = 34)
            // Guaranteed gatekeeper at (34, 6) for Gate 1
            else if (x == (`MAP_WIDTH - 2) && y == 6) begin
                get_tile = `TILE_MONSTER;
            end
            // Guaranteed gatekeeper at (34, 14) for Gate 2
            else if (x == (`MAP_WIDTH - 2) && y == 14) begin
                get_tile = `TILE_MONSTER;
            end

            // 4. FUNNEL WALLS AROUND GATEKEEPERS (Forces player through the monster)
            else if (x == (`MAP_WIDTH - 2) && (y == 5 || y == 7 || y == 13 || y == 15)) begin
                get_tile = `TILE_WALL;
            end

            // 5. PLAYER STARTING SANCTUARY (Safe area around (2, 2))
            else if (x >= 1 && x <= 4 && y >= 1 && y <= 3) begin
                get_tile = `TILE_PATH;
            end

            // 6. TREASURE CHESTS ('C' - 50% Mimic Horror / 50% Precious Loot)
            else if ((x == 8  && y == 2)  ||
                     (x == 22 && y == 3)  ||
                     (x == 6  && y == 11) ||
                     (x == 18 && y == 11) ||
                     (x == 28 && y == 10) ||
                     (x == 12 && y == 17) ||
                     (x == 26 && y == 17)) begin
                get_tile = `TILE_CHEST;
            end

            // 7. DUNGEON ROAMING MONSTERS ('M')
            else if ((x == 14 && y == 2)  ||
                     (x == 10 && y == 6)  ||
                     (x == 20 && y == 7)  ||
                     (x == 28 && y == 4)  ||
                     (x == 14 && y == 11) ||
                     (x == 24 && y == 11) ||
                     (x == 8  && y == 15) ||
                     (x == 20 && y == 15)) begin
                get_tile = `TILE_MONSTER;
            end

            // 8. INTERNAL MAZE WALL DIVIDERS
            else if ((x == 6  && y >= 4 && y <= 9) ||
                     (x == 12 && y >= 3 && y <= 8) ||
                     (x == 16 && y >= 1 && y <= 5) ||
                     (x == 16 && y >= 8 && y <= 13) ||
                     (x == 22 && y >= 5 && y <= 9) ||
                     (x == 26 && y >= 2 && y <= 7) ||
                     (x == 30 && y >= 1 && y <= 4) ||
                     (x == 30 && y >= 8 && y <= 12) ||
                     (y == 4  && x >= 7 && x <= 10) ||
                     (y == 9  && x >= 1 && x <= 4) ||
                     (y == 13 && x >= 7 && x <= 14) ||
                     (y == 13 && x >= 18 && x <= 22) ||
                     (y == 15 && x >= 10 && x <= 16) ||
                     (x == 4  && y >= 14 && y <= 17) ||
                     (x == 10 && y >= 16 && y <= 18) ||
                     (x == 22 && y >= 14 && y <= 17) ||
                     (x == 30 && y >= 16 && y <= 18)) begin
                get_tile = `TILE_WALL;
            end

            // 9. OPEN LABYRINTH PATHWAYS (Path with grid dot)
            else begin
                get_tile = `TILE_PATH;
            end
        end
    endfunction

    assign out_tile = get_tile(in_x, in_y);

endmodule
