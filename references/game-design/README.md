# Game Design & Level Design — Knowledge Base

This folder contains reference documents compiled for **professional game development processes** and **level design**. The content has been verified through in-depth internet research from GDC talks, Game Maker's Toolkit, The Level Design Book, Nintendo/Valve design philosophy, Jesse Schell (*The Art of Game Design*), Steve Swink (*Game Feel*), the MDA paper (Hunicke/LeBlanc/Zubek), Daniel Cook, and casual/mobile industry sources (Game Developer/Gamasutra, Socialpoint, Mobile Free To Play, etc.).

> This KB is **design** knowledge (what and why). For engine/technical knowledge (how, the Flame API), see the sibling KB: `references/flame/`.
> The `flame-game-dev` skill references both of these KBs as production rules.

## Contents

| # | File | Topic |
|---|---|---|
| 01 | [01-design-foundations.md](01-design-foundations.md) | MDA, the 8 aesthetics, core/meta/session loop, design pillars, juice (intro) |
| 02 | [02-level-design-principles.md](02-level-design-principles.md) | **Level design core:** introduce/develop/twist/conclude, Kishōtenketsu, teach-then-test, signposting/affordance, gating/locks&keys, in-level pacing, blockout process, common mistakes |
| 03 | [03-difficulty-and-pacing.md](03-difficulty-and-pacing.md) | Flow channel, sawtooth/fractal curve, difficulty spike, interest curve, intensity ramp, DDA, balancing |
| 04 | [04-game-feel-and-juice.md](04-game-feel-and-juice.md) | Swink's 3 pillars, juice checklist (screenshake, hit-stop, squash&stretch, easing, sound) |
| 05 | [05-onboarding-and-tutorialization.md](05-onboarding-and-tutorialization.md) | FTUE, show-don't-tell, skill atom, progressive disclosure, time-to-fun |
| 06 | [06-progression-economy-retention.md](06-progression-economy-retention.md) | Core/meta loop genre templates, progression, reward schedule, economy (soft/hard, source/sink, idle), D1/D7/D30, ethics |
| 07 | [07-professional-process.md](07-professional-process.md) | Lifecycle, prototype vs vertical slice, milestones (alpha/beta freeze), lean GDD, playtest/iteration, scoping (MVP/MoSCoW) |
| 08 | [08-level-design-for-2d-casual.md](08-level-design-for-2d-casual.md) | **2D/puzzle/casual/idle application:** levels-as-data (JSON/Tiled, LevelConfig), sawtooth template, match-3 tuning, telemetry, Flame mapping |
| 09 | [09-art-ui-identity-and-orientation.md](09-art-ui-identity-and-orientation.md) | **Per-game identity (MANDATORY):** HUD diegesis, genre-based HUD layout, typography (3 roles/font trio), 5 pillars of visual identity, orientation (portrait/landscape) choice, anti-reskin checklist |

## How to use

- **Before a new game (together with game-greenlight):** 01 (pillar/aesthetic/loop) + 07 (scope/prototype).
- **When designing levels/waves/difficulty:** 02 + 03 + 08 (the most critical trio).
- **Polish and retention:** 04 (juice) + 05 (onboarding) + 06 (progression/retention).
- This KB is also used together with the `flame-game-dev` Claude Code skill; the skill references these documents as production rules.
