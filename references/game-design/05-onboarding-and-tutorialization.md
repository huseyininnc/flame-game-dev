# Onboarding / FTUE (First-Time User Experience)

The highest-leverage part of the game. **70–90%** of apps lose the user in the first session; **D1 retention caps every later metric** (an 80% D1-loss squeezes D7 below 20%). FTUE is roughly the **first 60 seconds** (hook) + the **first 15 minutes** (proving the depth).

> Related: the interest curve of the first session → `03-difficulty-and-pacing.md`; wordless teaching/teach-then-test → `02-level-design-principles.md`.

---

## Rules

- **Show, don't tell.** Teach with action, not a wall of text. When the first enemy arrives, instead of explaining combat, light a visual cue on the attack button (kinesthetic learning — learning by doing).
- **One mechanic at a time ("skill atom").** Introduce an isolated skill, test until a small success, then the next. Don't stack many new mechanics at once (Cook's skill chain: basic jump → platform jump → obstacle → finishing the level).
- **Progressive disclosure.** Show only the controls/UI of the current task. Hide meta systems (shop, upgrade, social) until the need arises — open the meta layer over the first 3–5 sessions, not on screen 1.
- **Aggressively reduce time-to-fun.** The player should actually be playing within ~10–15 seconds. Goal: "the shortest path to the experience worth continuing."
- **Contextual > forced tutorial.** Trigger guidance in context (just-in-time) rather than a long front-loaded mandatory flow. If mandatory, keep it short/skippable.
- **Tight feedback loop.** Fast, juicy feedback on every action; it accelerates learning during the pre-mastery frustration phase.
- **Measure tutorial drop-off.** Track step-by-step where it's abandoned; every drop point is a fixable funnel leak.
- **Fun first, monetization later.** Few/zero ads and no paywall in the first sessions; early aggressive monetization is a leading cause of low D1.

---

## Failure modes to avoid

- Text-heavy intro screens.
- Teaching a mechanic the player can't use yet (low perceived value → quick frustration).
- An over-long tutorial that delays the first real reward.

---

## Implicit-tutorial philosophy (aligned with Valve/Portal)

- **The level itself is the tutorial:** design a situation where the only sensible action is the lesson, and let the player discover it.
- Reward the inference — the "I get it!" moment is the reward itself.
- Teach safely, test under pressure. New mechanics one at a time; stacking them at once frustrated test players (early Portal builds).

---

## Sources

- Best Practices for Mobile Game Onboarding — Adrian Crook: https://adriancrook.com/best-practices-for-mobile-game-onboarding/
- FTUE & Onboarding — Mobile Game Doctor: https://mobilegamedoctor.com/2025/05/30/ftue-onboarding-whats-in-a-name/
- The Chemistry of Game Design (skill atoms) — Daniel Cook: https://lostgarden.com/2007/07/19/the-chemistry-of-game-design/
- Game Mechanics (Portal 2) — Valve Developer Wiki: https://developer.valvesoftware.com/wiki/Game_Mechanics_(Portal_2)
