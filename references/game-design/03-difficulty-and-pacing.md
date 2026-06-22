# Difficulty Curve, Pacing, and Balancing

This document covers how to design difficulty and the rhythm across a game/session. Within-level pacing and gating → `02-level-design-principles.md`; casual/puzzle-specific numerical tuning → `08-level-design-for-2d-casual.md`.

---

## 1. Flow channel

Csikszentmihalyi: on one axis the player's **skill**, on the other the **challenge**. The "flow channel" is the diagonal band where the two stay roughly equal.
- Challenge ≫ skill → **anxiety/frustration.**
- Challenge ≪ skill → **boredom.**
- As the player plays, skill **rises**; that's why **constant difficulty quickly becomes boring.** Difficulty must climb together with the player.

Practical metric: think of difficulty as **(game difficulty − player skill)**; keep this gap ~constant/narrow throughout the session.

---

## 2. The good curve: fractal / sawtooth

A good difficulty curve **is not a straight line** — it's an overall-rising trend made of **small peaks and valleys** (fractal). The macro trend climbs, the micro texture breathes.

- **Sawtooth:** a few levels of increasing difficulty → deliberately **drop one or two levels** → climb again. The valley gives relief, recovery, and a sense of mastery, and makes the next climb feel fresh.
- **Application:** drive difficulty from a formula (linear / `sqrt` / `pow`) + subtract a periodic sawtooth dip at fixed intervals.

### Difficulty spike — good vs bad
- **Good spike:** a deliberate peak (boss/gauntlet) **immediately followed by a valley** → the player tastes victory and feels mastery. The valley makes the spike satisfying rather than exhausting.
- **Bad spike:** an unplanned wall. The classic example is the **opening control-learning spike** ("difficulty curves start at their peak") — complex controls, the hardest thing placed first before the player has invested. Solution: **fewer buttons/simpler controls** at the start, teach mechanics one at a time, lean on skills the player already knows (tap, swipe).

---

## 3. Interest curve (Jesse Schell)

Plot the player's interest against time:
1. **Hook** — an early sharp jump (grab attention; a quick win).
2. **Rising action** — peaks each higher than the last, with small valleys between.
3. **Climax** — the highest point near the end.
4. **Resolution** — a short descent, an ending that "leaves them wanting more."

**It's fractal:** the whole game, each level, and each session should have its own interest curve. **Use it as a diagnostic tool:** draw the expected curve, find the flat/sagging regions — those are your pacing problem points.

**Apply to the session (critical for mobile):** a hook in the first seconds → a few rising beats → a satisfying peak (boss/combo/big reward) → a small high point to pull into the next one.

---

## 4. Intensity ramps / "breathing"

- **Core law:** perception is **relative** — 5→11 is a huge jump, 10→11 is nothing. Constant high intensity resets the baseline.
- **In-out-in (Schell):** open with a burst → **pull back** (let the player adapt) → rise with ever-growing beats → a peak that exceeds expectation. Then repeat at a higher scale.
- **Rest ≠ inactivity:** it's a relative drop. To make a peak felt, **lower** intensity beforehand — design the negative space (the lull) first, then place the peak against it.

---

## 5. Dynamic Difficulty Adjustment (DDA) & rubber-banding

DDA: automatically tunes the game to player performance to keep them in the flow channel. **Rubber-banding** is its best-known simple form (racing games: the trailing AI speeds up).

Techniques: scale enemy health/damage/spawn rate, adjust aim-assist, tune resource/ammo drops to need, nudge level selection based on success rate.

- **Pros:** keeps a wider range of players in flow; variety/replayability.
- **Risks:** feels **unfair** if noticed; players can **exploit** the system (deliberately falling behind to get a boost); **monetization-driven hidden difficulty adjustment is unethical — don't do it.**
- **Do it well:** keep it **invisible**; limited/subtle adjustment; good for accessibility (helping a struggling player); be careful in competitive PvP and anywhere the perception of fairness is core; where possible, leave the player an opt-in/choice.

---

## 6. Balancing

- **Fairness:** all meaningful options should be comparably viable; the player should feel a loss is **their own fault** (an AI that visibly "cheats" breaks this).
- **Readability & telegraphing:** telegraph everything dangerous (wind-up animation, audio tell, hit zone) → reaction becomes **skill**, not luck. Health/cooldown/threat are visually clear.
- **Risk/reward:** power must carry a cost (long cooldown, resource cost, recovery window, positional opening). If you can't write down its cost, it's **overpowered**.
- **Dominant-strategy hunting:** if one strategy consistently beats the others, expression collapses → nerf it or buff its counter. Actively hunt for this in playtests.
- **Symmetric vs asymmetric:** symmetric (same tools for everyone; easy to balance; competitive puzzle) vs asymmetric ("different but equally viable"; hard to balance, high variety). **Intransitivity (rock-paper-scissors)** is a workhorse tool: build circular counter-play so no option dominates.

---

## One-page summary

1. Climb difficulty together with the player (flow channel); keep the **(difficulty − skill)** gap narrow.
2. The curve is a **sawtooth**: climb → deliberately drop → climb. After a spike, **always a valley**.
3. Avoid the opening **control spike**: few buttons, teach one at a time, lean on known skills.
4. **The interest curve is fractal** (game/level/session); draw it, fix the flat regions; build the session with hook→rise→peak→pull.
5. **Relativity:** to make a peak felt, lower intensity first (in-out-in).
6. If you use DDA, keep it **invisible & ethical**.
7. Telegraph every danger; write a **cost** for every power; hunt the dominant strategy; where possible an intransitive counter-loop.

---

## Sources

- Flow theory (Csikszentmihalyi) — Yu-kai Chou: https://yukaichou.com/gamification-analysis/flow-theory-complete-guide-csikszentmihalyi-optimal-experience/
- Difficulty Curves Start At Their Peak — Game Developer: https://www.gamedeveloper.com/design/difficulty-curves-start-at-their-peak
- Doing Difficulty Right: Fractal Curves — Game Developer: https://www.gamedeveloper.com/design/doing-difficulty-right-fractal-curves
- Rising Difficulty Curve — abagames: https://abagames.github.io/joys-of-small-game-development-en/difficulty/curve.html
- Game Changers: Dynamic Difficulty — Game Developer: https://www.gamedeveloper.com/design/game-changers-dynamic-difficulty
- Interest Curve — Game Studies Wiki: https://game-studies.fandom.com/wiki/Interest_Curve
- Trinity Part 6: Intensity Ramps — Game Developer: https://www.gamedeveloper.com/design/trinity-part-6---intensity-ramps
- Game Balance — Game Studies Wiki: https://game-studies.fandom.com/wiki/Game_Balance
- Symmetrical vs Asymmetrical Balance — David Gagnon: https://davidgagnon.wordpress.com/2009/08/16/symmetrical-vs-asymmetrical-balance-in-game-design/
