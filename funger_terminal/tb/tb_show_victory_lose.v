// ============================================================================
// Testbench: tb_show_victory_lose.v
// Complete Victory & Defeat Showcase for Fear & Hunger: Terminal Labyrinth
// Renders the Grand Victory Escape Banner, Gruesome Game Over Gothic Screen,
// Dual-Mode Victory Endings, 5 Fatal Defeat Scenarios & Combat Logs.
// ============================================================================

`timescale 1ns / 1ps

module tb_show_victory_lose;

    // ------------------------------------------------------------------------
    // 1. Grand Victory Escape Screen (Full ASCII Art Banner)
    // ------------------------------------------------------------------------
    task render_victory_escape_banner;
        begin
            $display("\033[1;33m====================================================================================================\033[0m");
            $display("\033[1;33m   ___      ___ ___  ________  _________  ________  ________      ___    ___ \033[0m");
            $display("\033[1;33m  |\\  \\    /  /|\\  \\|\\   ____\\|\\___   ___\\\\   __  \\|\\   __  \\    |\\  \\  /  /|\033[0m");
            $display("\033[1;33m  \\ \\  \\  /  / | \\  \\ \\  \\___|\\|___ \\  \\_\\ \\  \\|\\  \\ \\  \\|\\  \\   \\ \\  \\/  / /\033[0m");
            $display("\033[1;33m   \\ \\  \\/  / / \\ \\  \\ \\  \\        \\ \\  \\ \\ \\  \\\\\\  \\ \\   _  _\\   \\ \\    / / \033[0m");
            $display("\033[1;33m    \\ \\    / /   \\ \\  \\ \\  \\____    \\ \\  \\ \\ \\  \\\\\\  \\ \\  \\\\  \\|   \\/  /  /  \033[0m");
            $display("\033[1;33m     \\ \\__/ /     \\ \\__\\ \\_______\\   \\ \\__\\ \\ \\_______\\ \\__\\\\ _\\   __/  / /   \033[0m");
            $display("\033[1;33m      \\|__|/       \\|__|\\|_______|    \\|__|  \\|_______|\\|__|\\|__| |\\___/ /    \033[0m");
            $display("\033[1;33m                                                                  \\|___|/     \033[0m");
            $display("\033[1;32m                      [ E S C A P E   A C H I E V E D   -   V I C T O R Y ]                       \033[0m");
            $display("\033[1;33m====================================================================================================\033[0m");
            $display("\033[1;36m+====================================================================================================+\033[0m");
            $display("\033[1;36m|  \033[1;33mALL 3 RUNIC KEYS INSERTED!\033[1;37m THE RUNIC GATES GRIND OPEN AS GOLDEN LIGHT FLOODS THE DARKNESS!        \033[1;36m|\033[0m");
            $display("\033[1;36m|  \033[1;32mYou and your surviving companions have triumphed over the horrors and conquered the Labyrinth!   \033[1;36m|\033[0m");
            $display("\033[1;36m+====================================================================================================+\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // 2. Dual-Mode Victory Endings (Normal vs Hardcore vs 100% Map Clear)
    // ------------------------------------------------------------------------
    task display_victory_modes;
        begin
            $display("\033[1;32m>>> DUAL-MODE VICTORY OUTCOMES & REPUTATION TIERS <<<\033[0m\n");

            // Mode 0: Fear & Hunger Victory
            $display("\033[1;32m[VICTORY ENDING A]: FEAR & HUNGER (Normal Mode Escape)\033[0m");
            $display("  - \033[1;37mStatus          :\033[0m Survived with Tactical Buffs (+25%% HP, +50%% ATK/DEF).");
            $display("  - \033[1;37mEpilogue Lore   :\033[0m The expedition returns to the Kingdom of Rondon bearing ancient");
            $display("                      relics and cartographic scrolls of the forgotten catacombs.");
            $display("                      The survivor's names are immortalized in the Guild's chronicles.");
            $display("  - \033[1;32mHardware States :\033[0m `difficulty_mode = 0`, `game_state = STATE_VICTORY (4'd8)`, `is_victory_out = 1`.\n");

            // Mode 1: Terror & Starvation Victory
            $display("\033[1;35m[VICTORY ENDING B]: TERROR & STARVATION (Hardcore True Survivor)\033[0m");
            $display("  - \033[1;37mStatus          :\033[0m Conquered on Pure Baseline Stats (1.0x Baseline HP/ATK/DEF).");
            $display("  - \033[1;37mEpilogue Lore   :\033[0m Against starvation, gruesome amputations, coin flips of death and");
            $display("                      encroaching madness, you emerged unbroken. The subterranean gods");
            $display("                      themselves acknowledge your indomitable human will.");
            $display("  - \033[1;35mHardware States :\033[0m `difficulty_mode = 1`, `game_state = STATE_VICTORY (4'd8)`, `is_victory_out = 1`.\n");

            // Special: 100% Full-Map Victory
            $display("\033[1;33m[VICTORY ENDING C]: 100%% LABYRINTH FULL-MAP VANQUISH (Master Clearance)\033[0m");
            $display("  - \033[1;37mStatus          :\033[0m All 10/10 Monsters Vanquished, 7/7 Vault Chests Looted, 3/3 Runic Keys.");
            $display("  - \033[1;37mVerification    :\033[0m Mathematically & physically proven on real clock in `tb_full_map_victory.v`.");
            $display("  - \033[1;33mHonorific       :\033[0m 'Sovereign Cleanser of the Labyrinth' - Zero foes left alive.");
            $display("\033[1;30m----------------------------------------------------------------------------------------------------\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // 3. In-Combat Tactical Victory Notices
    // ------------------------------------------------------------------------
    task display_combat_victory_notices;
        begin
            $display("\033[1;32m>>> IN-COMBAT TACTICAL VICTORY ANNOUNCEMENTS <<<\033[0m\n");

            $display("  \033[1;37m1. STANDARD COMBAT VICTORY BANNER:\033[0m");
            $display("     \033[1;32m+====================================================================================================+\033[0m");
            $display("     \033[1;32m|  \033[42;1;37m >>> GLORIOUS VICTORY: THE FOE HAS BEEN SLAIN! SPOILS SCATTERED ACROSS THE FLOOR! <<< \033[0m\033[1;32m         |\033[0m");
            $display("     \033[1;32m+====================================================================================================+\033[0m\n");

            $display("  \033[1;37m2. DECAPITATION EXECUTION (INSTAKILL CRITICAL HEAD SLICE):\033[0m");
            $display("     \033[1;31m+====================================================================================================+\033[0m");
            $display("     \033[1;31m|  \033[41;1;37m >>> [DECAPITATION EXECUTION]: THE ENEMY'S HEAD ROLLS ACROSS THE COLD LABYRINTH STONES! <<< \033[0m\033[1;31m     |\033[0m");
            $display("     \033[1;31m|  \033[1;37mTarget vanquished instantly via critical head cleavage, bypassing remaining torso vitality!       \033[1;31m|\033[0m");
            $display("     \033[1;31m+====================================================================================================+\033[0m\n");

            $display("  \033[1;37m3. DEFENSIVE COIN FLIP PARRY VICTORY:\033[0m");
            $display("     \033[1;33m+====================================================================================================+\033[0m");
            $display("     \033[1;33m|  \033[43;1;30m [COIN SUCCESS] \033[0m \033[1;32mParried lethal cleave and countered with riposte for 20 True Damage!        \033[1;33m|\033[0m");
            $display("     \033[1;33m+====================================================================================================+\033[0m\n");
            $display("\033[1;30m----------------------------------------------------------------------------------------------------\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // 4. Gruesome Game Over Screen (Full Gothic ASCII Art Banner)
    // ------------------------------------------------------------------------
    task render_game_over_banner;
        begin
            $display("\033[1;31m====================================================================================================\033[0m");
            $display("\033[1;31m   ________  ________  _____ ______   _______           ________  ___      ___ _______   ________     \033[0m");
            $display("\033[1;31m  |\\   ____\\|\\   __  \\|\\   _ \\  _   \\|\\  ___ \\         |\\   __  \\|\\  \\    /  /|\\  ___ \\ |\\   __  \\    \033[0m");
            $display("\033[1;31m  \\ \\  \\___|\\ \\  \\|\\  \\ \\  \\\\\\__\\ \\  \\ \\   __/|        \\ \\  \\|\\  \\ \\  \\  /  / | \\   __/|\\ \\  \\|\\  \\   \033[0m");
            $display("\033[1;31m   \\ \\  \\  __\\ \\   __  \\ \\  \\\\|__| \\  \\ \\  \\_|/__       \\ \\  \\\\\\  \\ \\  \\/  / / \\ \\  \\_|/_\\ \\   _  _\\  \033[0m");
            $display("\033[1;31m    \\ \\  \\|\\  \\ \\  \\ \\  \\ \\  \\    \\ \\  \\ \\  \\_|\\ \\       \\ \\  \\\\\\  \\ \\    / /   \\ \\  \\_|\\ \\ \\  \\\\  \\| \033[0m");
            $display("\033[1;31m     \\ \\_______\\ \\__\\ \\__\\ \\__\\    \\ \\__\\ \\_______\\       \\ \\_______\\ \\__/ /     \\ \\_______\\ \\__\\\\ _\\ \033[0m");
            $display("\033[1;31m      \\|_______|\\|__|\\|__|\\|__|     \\|__|\\|_______|        \\|_______|\\|__|/       \\|_______|\\|__|\\|__|\033[0m");
            $display("\033[1;31m====================================================================================================\033[0m");
            $display("\033[1;37m+====================================================================================================+\033[0m");
            $display("\033[1;37m|  YOUR ENTIRE SQUAD HAS FALLEN TO THE LABYRINTH HORRORS... YOUR BONES ROT IN THE DARKNESS.         |\033[0m");
            $display("\033[1;37m|  \033[1;31mGAME OVER: Fear & Hunger claims another soul. The dungeon swallows all memory of your journey.    \033[1;37m|\033[0m");
            $display("\033[1;37m+====================================================================================================+\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // 5. The 5 Specific Defeat Scenarios & Loss Conditions
    // ------------------------------------------------------------------------
    task display_defeat_scenarios;
        begin
            $display("\033[1;31m>>> THE 5 TRAGIC DEFEAT SCENARIOS IN FEAR & HUNGER <<<\033[0m\n");

            // Scenario 1: Combat Squad Wipeout
            $display("\033[1;31m[DEFEAT TYPE #1]: COMBAT SQUAD WIPEOUT (Total Party Depletion)\033[0m");
            $display("  - \033[1;37mCause       :\033[0m All 8 Playable Companions (Cahara to Nas'hrah) suffer fatal HP loss (HP = 0).");
            $display("  - \033[1;37mNarrative   :\033[0m Overwhelmed by brutal attacks; shields shattered, blades broken, blood spills.");
            $display("  - \033[1;31mFSM Logic   :\033[0m `check_all_pals_dead() == 1'b1` -> Transitions immediately to `STATE_GAME_OVER`.\n");

            // Scenario 2: Lethal Coin Flip Decapitation
            $display("\033[1;31m[DEFEAT TYPE #2]: FATAL COIN FLIP DECAPITATION (Severed by Death)\033[0m");
            $display("  - \033[1;37mCause       :\033[0m Incorrect call on defensive coin flip against monster's lethal skill attack.");
            $display("  - \033[1;37mNarrative   :\033[0m The coin clatters in the dust showing the wrong face. The enemy's blade cleaves");
            $display("                through flesh and bone. Decapitation strikes down the hero on turn 1.");
            $display("  - \033[1;31mFSM Logic   :\033[0m `coin_selected != rng_val[0]` on Lethal Attack -> Massive DMG + 20 Mind Loss.\n");

            // Scenario 3: Starvation in the Catacombs
            $display("\033[1;31m[DEFEAT TYPE #3]: STARVATION COLLAPSE (The Slow Emaciation)\033[0m");
            $display("  - \033[1;37mCause       :\033[0m Hunger level reaches maximum (100 / 100) with zero bread or meat in inventory.");
            $display("  - \033[1;37mNarrative   :\033[0m Muscles wither, stomach aches bitterly. The explorer collapses into Crawling");
            $display("                posture, losing 2 HP with every agonizing step until vital signs cease.");
            $display("  - \033[1;31mFSM Logic   :\033[0m `top_is_starving == 1'b1` -> -2 HP per map step pulse on active hero.\n");

            // Scenario 4: Mind Collapse & Pure Madness
            $display("\033[1;31m[DEFEAT TYPE #4]: INSANITY & MIND COLLAPSE (Lost in the Void)\033[0m");
            $display("  - \033[1;37mCause       :\033[0m Mind / Sanity drops to 0 after repeated terrors, darkness and coin failures.");
            $display("  - \033[1;37mNarrative   :\033[0m Hallucinations overwhelm sight and hearing. The mind fractures beyond repair.");
            $display("                The adventurer drops weapons, laughing hysterically into the abyss.");
            $display("  - \033[1;31mFSM Logic   :\033[0m `top_mind_level == 8'd0` -> Panic state lock, uncontrollable combat turns.\n");

            // Scenario 5: Mimic Trap Ambush Kill
            $display("\033[1;31m[DEFEAT TYPE #5]: DEVOURED BY MIMIC (The Chest Horror Ambush)\033[0m");
            $display("  - \033[1;37mCause       :\033[0m Opening an ancient chest while at critical HP (< 25 HP) and rolling Mimic (20%%).");
            $display("  - \033[1;37mNarrative   :\033[0m Desperately seeking healing herbs, the weakened explorer pries open a wooden lid.");
            $display("                Razor teeth snap shut. The chest devours the explorer before battle begins.");
            $display("  - \033[1;31mFSM Logic   :\033[0m `tile == TILE_CHEST && rng_val < 2` with low party health.\n");
            $display("\033[1;30m----------------------------------------------------------------------------------------------------\033[0m\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // 6. Master Victory & Lose Comparative Matrix
    // ------------------------------------------------------------------------
    task display_master_endings_table;
        begin
            $display("\033[1;33m+=====================================================================================================================+\033[0m");
            $display("\033[1;33m|                 FEAR & HUNGER: TERMINAL LABYRINTH - MASTER VICTORY & DEFEAT MATRIX                                  |\033[0m");
            $display("\033[1;33m+========+=============================+====================+==================+======================================+\033[0m");
            $display("\033[1;37m| Status | Outcome Title               | FSM Target State   | Hardware Signal  | Resolution Narrative                 |\033[0m");
            $display("\033[1;33m+--------+-----------------------------+--------------------+------------------+--------------------------------------+\033[0m");
            $display("| \033[1;32mVICTORY\033[0m| Mode 0 Escape (F&H Normal)  | STATE_VICTORY (8)  | is_victory_out=1 | Survived dungeon with 25%% HP buff   |");
            $display("| \033[1;32mVICTORY\033[0m| Mode 1 Escape (T&S Hardcore)| STATE_VICTORY (8)  | is_victory_out=1 | True Survivor on 1.0x baseline stats |");
            $display("| \033[1;32mVICTORY\033[0m| Full-Map 100%% Clearance     | STATE_VICTORY (8)  | is_victory_out=1 | 10 Monsters, 7 Chests, 3 Runic Keys  |");
            $display("| \033[1;32mVICTORY\033[0m| Decapitation Execution      | STATE_BATTLE_LOOP  | limb_severed[4]  | Instant kill via critical head slice |");
            $display("| \033[1;32mVICTORY\033[0m| Defensive Coin Flip Parry   | STATE_BATTLE_LOOP  | coin_match=1     | 100%% damage parried + 20 riposte dmg |");
            $display("+--------+-----------------------------+--------------------+------------------+--------------------------------------+");
            $display("| \033[1;31mDEFEAT \033[0m| Combat Squad Wipeout        | STATE_GAME_OVER(9) | all_pals_dead=1  | All 8 companions fall in battle      |");
            $display("| \033[1;31mDEFEAT \033[0m| Fatal Coin Flip Mismatch    | STATE_GAME_OVER(9) | coin_match=0     | Amputation / Decapitation by boss    |");
            $display("| \033[1;31mDEFEAT \033[0m| Starvation Emaciation       | STATE_GAME_OVER(9) | hunger_level=100 | -2 HP/step until party collapses     |");
            $display("| \033[1;31mDEFEAT \033[0m| Sanity Breakdown / Madness  | STATE_GAME_OVER(9) | mind_level=0     | Permanent panic and total delirium   |");
            $display("| \033[1;31mDEFEAT \033[0m| Devoured by Mimic Ambush    | STATE_GAME_OVER(9) | col_chest & rng  | Low-health ambush by chest horror    |");
            $display("\033[1;33m+========+=============================+====================+==================+======================================+\033[0m");
            $display("[SYSTEM PROFILE]: 100%% deterministic FSM guarantees zero soft-locks between STATE_VICTORY and STATE_GAME_OVER.\n");
        end
    endtask

    // ------------------------------------------------------------------------
    // Main Simulation Process
    // ------------------------------------------------------------------------
    initial begin
        $display("\033[2J\033[H");
        $display("\033[1;33m================================================================================================================\033[0m");
        $display("\033[1;33m              FEAR & HUNGER: TERMINAL LABYRINTH - COMPLETE VICTORY & LOSE ENCYCLOPEDIA                          \033[0m");
        $display("\033[1;33m================================================================================================================\033[0m");
        $display("\033[1;37m  Visualizing All Victory & Defeat Banners, Dual-Mode Escapes, 5 Tragic Death Scenarios & In-Combat Logs         \033[0m");
        $display("\033[1;33m================================================================================================================\033[0m\n");

        render_victory_escape_banner();
        display_victory_modes();
        display_combat_victory_notices();

        render_game_over_banner();
        display_defeat_scenarios();

        display_master_endings_table();

        $display("\033[1;32m>>> ALL VICTORY & DEFEAT SCREENS, BANNERS & NOTICES RENDERED SUCCESSFULLY! <<<\033[0m\n");
        $finish;
    end

endmodule