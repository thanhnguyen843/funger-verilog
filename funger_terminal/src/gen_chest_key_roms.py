import os
from PIL import Image

# 1. Key (11 x 22)
im_k = Image.open(r'C:/Users/hi/.gemini/antigravity/brain/e7aa01d5-17c0-46c3-b4f7-15641a3b0a0f/.user_uploaded/media_1791991427623_5a06b733.png')
cell_k = 561 / 22.0
key_pixels = []
for r in range(22):
    row = []
    for c in range(11):
        x = int(203 + c * cell_k + cell_k/2)
        y = int(268 + r * cell_k + cell_k/2)
        p = im_k.getpixel((x, y))
        if p[0] > 230 and p[1] > 230 and p[2] > 230:
            row.append(None)
        else:
            row.append((p[0], p[1], p[2]))
    key_pixels.append(row)

# 2. Chest (20 x 23)
im_c = Image.open(r'C:/Users/hi/.gemini/antigravity/brain/e7aa01d5-17c0-46c3-b4f7-15641a3b0a0f/.user_uploaded/media_1791991426264_21025375.png')
cw = 459.0 / 20.0
ch = 518.0 / 23.0
chest_pixels = []
for r in range(23):
    row = []
    for c in range(20):
        x = int(149 + c * cw + cw/2)
        y = int(95 + r * ch + ch/2)
        p = im_c.getpixel((x, y))
        if p[0] > 235 and p[1] > 235 and p[2] > 235:
            row.append(None)
        else:
            row.append((p[0], p[1], p[2]))
    chest_pixels.append(row)

# Generate key_sprite_rom.v
key_v = """// ============================================================================
// Module: key_sprite_rom.v
// Model for Dungeon Key (Chìa khóa hầm ngục) from image (11x22 Pixels)
// Supports TrueColor 24-bit RGB and Transparency
// ============================================================================

`timescale 1ns / 1ps

module key_sprite_rom (
    input  wire [5:0]  row,
    input  wire [5:0]  col,
    output reg  [23:0] color_rgb,
    output reg         is_transparent
);
    always @(*) begin
        is_transparent = 1'b1;
        color_rgb      = 24'h000000;
        case (row)
"""

for r in range(22):
    row_pix = [(c, key_pixels[r][c]) for c in range(11) if key_pixels[r][c] is not None]
    if row_pix:
        key_v += f"            6'd{r}: begin\n"
        key_v += "                case (col)\n"
        for c, rgb in row_pix:
            key_v += f"                    6'd{c}: begin is_transparent = 1'b0; color_rgb = 24'h{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}; end\n"
        key_v += "                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end\n"
        key_v += "                endcase\n"
        key_v += "            end\n"

key_v += """            default: begin
                is_transparent = 1'b1;
                color_rgb      = 24'h000000;
            end
        endcase
    end
endmodule
"""

with open('pkm/src/key_sprite_rom.v', 'w', encoding='utf-8') as f:
    f.write(key_v)

# Generate chest_sprite_rom.v
chest_v = """// ============================================================================
// Module: chest_sprite_rom.v
// Model for Opened Treasure Chest from image (20x23 Pixels)
// Supports TrueColor 24-bit RGB and Transparency
// ============================================================================

`timescale 1ns / 1ps

module chest_sprite_rom (
    input  wire [5:0]  row,
    input  wire [5:0]  col,
    output reg  [23:0] color_rgb,
    output reg         is_transparent
);
    always @(*) begin
        is_transparent = 1'b1;
        color_rgb      = 24'h000000;
        case (row)
"""

for r in range(23):
    row_pix = [(c, chest_pixels[r][c]) for c in range(20) if chest_pixels[r][c] is not None]
    if row_pix:
        chest_v += f"            6'd{r}: begin\n"
        chest_v += "                case (col)\n"
        for c, rgb in row_pix:
            chest_v += f"                    6'd{c}: begin is_transparent = 1'b0; color_rgb = 24'h{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}; end\n"
        chest_v += "                    default: begin is_transparent = 1'b1; color_rgb = 24'h000000; end\n"
        chest_v += "                endcase\n"
        chest_v += "            end\n"

chest_v += """            default: begin
                is_transparent = 1'b1;
                color_rgb      = 24'h000000;
            end
        endcase
    end
endmodule
"""

with open('pkm/src/chest_sprite_rom.v', 'w', encoding='utf-8') as f:
    f.write(chest_v)

print("Generated pkm/src/key_sprite_rom.v and pkm/src/chest_sprite_rom.v")
