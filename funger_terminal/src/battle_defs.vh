// ============================================================================
// Pokemon Lite: Terror & Starvation - Global Header (battle_defs.vh)
// Definitions for States, Actions, Items, Map Grid, 4-Character Squad
// ============================================================================

`ifndef BATTLE_DEFS_VH
`define BATTLE_DEFS_VH

// Top-Level Game States (4-bit)
`define STATE_TITLE         4'd0   // Title Screen
`define STATE_NARRATOR      4'd1   // Story Narrator Lore
`define STATE_DRAFT         4'd2   // Draft Team (Pick 4 Characters)
`define STATE_MAP           4'd3   // Labyrinth Exploration
`define STATE_MAP_BAG       4'd4   // Open Bag on Map
`define STATE_BATTLE_LOAD   4'd5   // Battle Init & Enemy Spawn
`define STATE_BATTLE_LOOP   4'd6   // Turn-based Combat Loop
`define STATE_GAME_OVER     4'd7   // Game Over Screen
`define STATE_VICTORY       4'd8   // Victory / Labyrinth Escape

// Battle Sub-States
`define B_STATE_MENU        3'd0   // Main Action Menu (Move / Bag / Flee)
`define B_STATE_MOVE_SEL    3'd1   // Move Select (Attack / Defend)
`define B_STATE_BAG_SEL     3'd2   // Bag Select (Item choice)
`define B_STATE_TARGET_SEL  3'd3   // Target Character Select
`define B_STATE_CONFIRM     3'd4   // Confirm Action
`define B_STATE_CALC        3'd5   // Damage & Heal Calculation
`define B_STATE_RESOLVE     3'd6   // Resolve HP & Log Update
`define B_STATE_CHECK       3'd7   // Outcome Check (Victory / Faint / Swap)

// Standalone 1v1 Battle FSM Controller States (3-bit) - Module 1 Specification
`define STATE_INIT          3'b000
`define STATE_INPUT         3'b001
`define STATE_CALC          3'b010
`define STATE_RENDER        3'b011
`define STATE_CHECK         3'b100
`define STATE_END           3'b101

// Action Encodings
`define ACTION_NONE         2'b00
`define ACTION_ATTACK       2'b01
`define ACTION_DEFEND       2'b10
`define ACTION_ITEM_OR_FLEE 2'b11

// Combat Status Codes
`define STATUS_ONGOING      2'b00
`define STATUS_PLAYER_WIN   2'b01
`define STATUS_ENEMY_WIN    2'b10
`define STATUS_DRAW         2'b11

// Healing Items, Food, Mind Restoratives & Dungeon Keys (4-bit)
`define ITEM_NONE           4'd0
`define ITEM_POPPY          4'd1   // Poppy Flower (+30/+50 HP)
`define ITEM_MARIJUANA      4'd2   // Marijuana Herb (+70/+120 HP, +20 Mind)
`define ITEM_KEY            4'd3   // Dungeon Key (3 needed for Gate)
`define ITEM_BREAD          4'd4   // Moldy Bread (-40 Hunger)
`define ITEM_MEAT           4'd5   // Dried Meat (-60 Hunger, +15 HP)
`define ITEM_ALE            4'd6   // Ale Flask (+35 Mind)
`define ITEM_NORMAL         `ITEM_POPPY      // Backward compatibility alias
`define ITEM_STRONG         `ITEM_MARIJUANA  // Backward compatibility alias

// Targetable Body Parts (3-bit) - Unified ALU & Engine Mapping
`define LIMB_TORSO          3'd0   // Torso (95% Hit | Core vitals | 1.0x baseline)
`define LIMB_HEAD           3'd1   // Head (25% Hit | LETHAL Decapitation | 1.5x crit)
`define LIMB_ARM_R          3'd2   // Right Arm (80% Hit | Weapon arm | Disarms ATK)
`define LIMB_ARM_L          3'd3   // Left Arm (80% Hit | Shield/Offhand | Breaks Guard)
`define LIMB_LEGS           3'd4   // Legs (85% Hit | Mobility | Forces Crawling)
`define LIMB_LEG_R          3'd4   // Alias for Right Leg
`define LIMB_LEG_L          3'd4   // Alias for Left Leg

// Coin Flip Choices (1-bit)
`define COIN_HEADS          1'b0   // Heads (Sylvian Face)
`define COIN_TAILS          1'b1   // Tails (Gro-goroth Face)

// Special Hexen & Class Skills (3-bit)
`define SKILL_NONE          3'd0
`define SKILL_STEAL         3'd1   // Cahara: Steal item + minor strike
`define SKILL_FAST_STANCE   3'd2   // D'arce: 2 consecutive strikes in 1 turn
`define SKILL_LOVING_WHISPER 3'd3  // D'arce: Heal ally 45 HP (costs 15 Mind)
`define SKILL_HURTING       3'd4   // Enki: 45 pure damage to chosen limb (costs 15 Mind)
`define SKILL_BLACK_ORB     3'd5   // Enki: 60 dark magic damage split across limbs (costs 25 Mind)
`define SKILL_DEVOUR        3'd6   // Ragnvaldr: 35 damage, -40 Hunger, +20 HP
`define SKILL_COMBUSTION    3'd7   // Nas'hrah: 50 AOE fire damage to all limbs (costs 30 Mind)

// Map Tile Types (3-bit)
`define TILE_WALL           3'd0   // Green Labyrinth Wall
`define TILE_PATH           3'd1   // Open Pathway with Grid Dots
`define TILE_MONSTER        3'd2   // 'M' Purple Monster Encounter Zone
`define TILE_CHEST          3'd3   // 'C' Brown Chest (50% Mimic / 50% Loot)
`define TILE_GATE           3'd4   // 'G' Cyan Dungeon Exit Gate (requires 3 Keys)
`define TILE_CLEARED        3'd5   // Cleared Tile (opened / defeated, no respawn)

// Map Dimensions
`define MAP_HEIGHT          20
`define MAP_WIDTH           36

// Monster Sprite Orientation (Direction)
`define DIR_LEFT            1'b0  // Opponent Monster (Faces Left)
`define DIR_RIGHT           1'b1  // Active Character (Faces Right)

// Tactical Stances (2-bit) - Hardware Stance Coprocessor
`define STANCE_BALANCED     2'd0   // Neutral standard stance
`define STANCE_BERSERK      2'd1   // +25% ATK, -25% DEF
`define STANCE_IRON_GUARD   2'd2   // +50% DEF, -12.5% ATK, HP regen per turn
`define STANCE_AGILE        2'd3   // +25% Evasion, +25% Flee probability

// Monster Archetypes (2-bit) - 4 Pillar System
`define ARCHETYPE_NORMAL    2'd0   // Standard physical combatant
`define ARCHETYPE_SPECTRAL  2'd1   // Ghost/Spirit: 100% immune to physical blades; weak to Occult Magic
`define ARCHETYPE_ARMORED   2'd2   // Stone/Iron Titan: Deflects blades (DEF 99); weak to Holy Smite & Magic
`define ARCHETYPE_TERROR    2'd3   // Eldritch Horror: Aura drains Mind; weak to Innocent Aura / Empathy

// Role-Locked Exploration Obstacles (3-bit)
`define OBSTACLE_NONE       3'd0
`define OBSTACLE_MIMIC      3'd1   // Mimic Chest: Cahara disarms safely; others take -30 HP bite
`define OBSTACLE_BARRICADE  3'd2   // Iron Barricade: D'arce shatters; others blocked
`define OBSTACLE_SEAL       3'd3   // Hexen Magic Seal: Enki dispels; others blocked & burned
`define OBSTACLE_CRAWLSPACE 3'd4   // Narrow Crevice: The Girl squeezes through; others cannot fit

// Squad Size
`define SQUAD_SIZE          4

`endif // BATTLE_DEFS_VH
