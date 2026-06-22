# Level / Wave Design Checklist

Run through this list when designing a level (or a wave/zone in a real-time game). Theory: `references/game-design/02`, `03`, `08`.

## Design first (before code)
- [ ] Does this level have **one clear purpose**? (teach a mechanic / introduce an enemy / deliver a story/reward beat — never "filler")
- [ ] Is it aligned with the target aesthetic(s) and pillars?
- [ ] Is it **a single new idea**? (don't introduce a new mechanic + new hazard + new enemy at the same time)

## Teach → Test → Twist (single-mechanic arc)
- [ ] **Introduce:** is the new element introduced in a **safe/fail-proof** space?
- [ ] **Develop:** is it developed with mild risk?
- [ ] **Twist:** is the mechanic recontextualized (not piling on unrelated difficulty)?
- [ ] **Conclude:** is there a finale/victory lap that requires the skill you taught?
- [ ] When the idea is exhausted, is the mechanic **dropped** (no padding)?

## Difficulty & pacing
- [ ] Is the overall curve **sawtooth** (climb→deliberately dip→climb), not a flat ramp?
- [ ] Is there a **trough/relief after every spike**?
- [ ] Is the opening **control spike** avoided (few buttons, known skill)?
- [ ] Is it **recalibrated** to the player's lifetime skill growth (level 100 ≠ level 1000)?
- [ ] Session interest curve: hook → rising beats → peak → pull?

## Player guidance (wordless)
- [ ] Does it teach with **geometry/feedback/reward** rather than text?
- [ ] Is the eye guided with **contrast + a reserved guide color** (+ a second channel for color-blind players)?
- [ ] Is the **golden path readable**; is exploration rewarded alongside it?
- [ ] Weenie/landmark density: does something pull you roughly every ~30 sec?

## Gating
- [ ] Is each obstacle's **gate type** deliberate (hard/soft/lock-key/one-way/shortcut/hidden)?
- [ ] Is the **lock foreshadowed before the key**?
- [ ] If there is backtracking, is it collapsed with a **shortcut**, and is the return paired with a **meaningful reward**?

## Levels-as-data (implementation)
- [ ] Is the level **config/JSON** (not hardcoded)? One generic `LevelConfig` + loader?
- [ ] Is difficulty tuned with a small **parameter set** (moves/objective/board/blocker/allowed)?
- [ ] If real-time, are the wave parameters (count, interval, HP/speed scale, boss cadence) in config?

## Game feel
- [ ] Does every player action have immediate, multi-sensory feedback (visual+audio)?
- [ ] On an important hit/kill, is there juice (screenshake/hit-stop/flash/particles), without overdoing it?

## Verification
- [ ] Was the level verified by **walking/playing it at player speed** (not from the editor camera)?
- [ ] If possible, playtested with a **fresh player**; was behavior observed (hesitation/getting stuck/quitting)?
- [ ] Telemetry: are **attempts + drop-off** instrumented per level/wave?
- [ ] Have the common mistakes been eliminated: maze, unfair death, dead end, monotony, directionless sandbox?
