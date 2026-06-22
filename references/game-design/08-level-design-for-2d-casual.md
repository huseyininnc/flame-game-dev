# Level Design for 2D / Puzzle / Casual / Idle (implementation)

This document applies the principles from 02 and 03 in a **code-driven engine (Flutter Flame)**. It is the most practical file for the serial production of this workspace.

---

## 1. Handcrafted vs procedural

- The industry designs puzzle levels **overwhelmingly by hand.** Pure procedural generation usually produces impossible/trivial/boring levels. Match-3, block-puzzle, and merge studios author by hand, then **tune with data.**
- Procedural is suitable for an **infinite/endless mode** or as a **content assistant** (generate candidates → curate by hand), not for the main campaign.

---

## 2. Levels-as-data (engine architecture rule)

**Separate level data from engine code.** Levels are config (JSON / Tiled / custom DSL), parsed at runtime — **never hardcoded.** This lets the designer iterate without recompiling, and lets live-ops ship new packs **as data.**

- **Tiled + JSON** is the de-facto pipeline: design visually in Tiled → export JSON → parse in the engine. In Flame, `flame_tiled` (see `references/flame/08-audio-and-tiled.md`).
- **A single generic `LevelConfig` schema + a single `LevelLoader`** should drive every level — **parametric/template-based levels** beat per-level custom code.

**Example `LevelConfig` (conceptual):**
```dart
class LevelConfig {
  final int index;
  final int columns;
  final int rows;
  final ObjectiveType objective;   // collect / clearAll / survive / reachScore
  final int objectiveTarget;
  final int moveLimit;             // or timeLimit
  final List<BlockerSpec> blockers;
  final List<PieceType> allowedPieces;
  final Map<String, Object> extra; // genre-specific parameters
}
```
Store levels as `assets/levels/levelXXX.json`; have `LevelLoader.load(index)` parse and return a `LevelConfig`; feed component spawning from this config. New level = new JSON; the code doesn't change.

---

## 3. Difficulty curve template (casual/puzzle)

- **Sawtooth, not linear** (see 03): a few levels of rising difficulty → a deliberate **drop** → climb again. Monotone difficulty creates churn.
- **Casual template:** **Levels 1–20 easy** (build confidence + teach), **~20–30 the first hard spike**, gradual rise, **big difficulty/paywall gates after ~50.** Place hard levels deliberately, and put a "reward" (easy) level right after.
- Player skill rises over a lifetime: levels numbered 1–100 and 1000–1100 are **not at the same effective difficulty.** Recalibrate.

---

## 4. Moves vs objective (match-3 numbers)

- The modern standard is **~15–20 moves/level** (it was ~50 a decade ago) — respecting the player's time.
- Tune **moves** as the primary difficulty dial; as moves drop, win rate drops.
- Track **attempts-per-level (mean & median)** as the difficulty index, not a binary pass/fail.

---

## 5. The hands-on tuning loop (a concrete recipe)

- After building a level, **play it ~10 times back to back.** On losses, record the remaining objective; on wins, record the remaining moves.
- Red flag: **2 reshuffles** in one attempt = the level is problematic; on a "hard" level, frequently **winning with many moves left** = too easy.
- Budget: initial setup ~10–20 min; **final balance ~1 hour per level** of extra tuning/testing. **Peer review is mandatory** (a second designer).
- Build each level like a **mini-story**: it should showcase the property of a single mechanic/element (dropping, blocking, color reaction); don't repeat the same idea. **Change the board shape** so there's no "same level, different skin" fatigue.

---

## 6. Data-driven tuning (post soft-launch)

- Model the **win rate ↔ moves** relationship with a **shifted negative binomial** (shift = the minimum moves required). It predicts the effect of a move change on WR before shipping.
- Use **"vanilla win rate"** as the modeling base (exclude attempts where boosters were used) — players spend boosters when moves run out, distorting the raw data near the limit.
- Keep monitoring after every rebalance (~1.5% error/move, frequent outliers). With live data, **reorder the levels** and smooth out the churn points (the specific levels where players quit/uninstall).

---

## 7. Genre-specific structuring

- **Match-3:** grid + objective (collect X, clear jelly, drop ingredients) + move/time limit; blockers & boosters add complexity; varied grid shapes.
- **Block puzzle:** usually endless/score-driven rather than discrete authored levels; difficulty emerges from board pressure; "levels" are parametric (board size, piece pool, spawn weighting).
- **Merge:** core = two low items → higher tier; ~3 layers of mechanics; progression is not per-level-authored but **unlock/economy-paced.**
- **Idle/incremental:** there are no "levels"; difficulty comes from the **economy curve** (cost/production formulas); the prestige wall sets the pacing. Curve design = this genre's equivalent of level design.

---

## 8. Mapping to Flame (implementation rules)

1. **A single generic level schema (JSON), a single loader; no per-level code.** (Flame: `assets/levels/*.json` + `LevelLoader`.)
2. Adjust difficulty with a small **parameter set** (moves, objective target, board shape, blocker/booster set, allowed pieces).
3. Author by hand; use procedural only for endless mode.
4. Difficulty = **sawtooth**; teach in 1–20, first spike ~20–30, a relief level after the spike.
5. **Instrument attempts-per-level + drop-off from day one;** reorder/retune with telemetry.
6. Each level teaches/showcases a single idea; diversify the shapes; peer-review every level.
7. In real-time action games (e.g. a Mitomerge-type merge-defense), a "level" ≈ **wave/zone**: wave count, spawn interval, enemy HP/speed scaling, boss cadence = your LevelConfig. The same sawtooth + teach-then-test principles apply (introduce a new enemy/mechanic in a safe wave, then combine).

---

## Sources

- Smart & Casual: The State of Tile Puzzle Games Level Design — Game Developer / Room 8: https://www.gamedeveloper.com/design/smart-casual-the-state-of-tile-puzzle-games-level-design-part-1
- Tuning Level Difficulty in Match-3: A Data-Driven Framework — Socialpoint: https://socialpoint-analytics.medium.com/tuning-level-difficulty-in-match-3-games-a-data-driven-framework-7b3cc07b2116
- Match-3 Level Design Principles — Gamigion: https://www.gamigion.com/match-3-level-design-principles/
- Playrix: Creating levels for match-3 — Game World Observer: https://gameworldobserver.com/2019/09/27/playrix-levels-elements-match-3
- JSON Map Format — Tiled docs: https://doc.mapeditor.org/en/stable/reference/json-map-format/
