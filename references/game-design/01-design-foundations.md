# Game Design Foundations — MDA, Loops, Pillars

This document provides the design framework that must be clarified **before** writing any code for a game. Level design (02, 08) and the other documents build on top of this foundation.

> This knowledge base is **design** knowledge, not engine (Flame) knowledge. For the Flame API, see the `references/flame/` KB.

---

## 1. The MDA Framework (Mechanics → Dynamics → Aesthetics)

The framework by Hunicke, LeBlanc & Zubek splits a game into three layers and makes a critical observation: **the designer and the player read these layers in opposite directions.**

- **Mechanics:** The rules, every action the player can take, the algorithm and data structures in the engine. **This is the only layer you write directly in code.** (Block-puzzle: grid size, piece shapes, the line-clear rule, the score formula, spawn logic.)
- **Dynamics:** The **run-time behavior** that emerges as the mechanics react to player input and to each other. It cannot be written directly; it **emerges** (e.g. the player hoards pieces to build a big combo; a "move limit" forces the player to plan).
- **Aesthetics ("fun"):** The **emotional response** evoked in the player — the fun that is actually felt.

**Direction (the most critical insight):**
- Designer: writes **Mechanics → Dynamics → Aesthetics**.
- Player: experiences **Aesthetics → Dynamics → Mechanics**.
- Conclusion: You first target a **feeling**, then work backward to find the mechanics that will give rise to the dynamics that produce that feeling. You tune the mechanic and observe in playtest whether the intended aesthetic actually emerges.

### 8 aesthetics instead of "fun"
"Fun" is vague; instead, name the target aesthetic:

1. **Sensation** — sensory pleasure (juicy feedback, particles, sound, screenshake).
2. **Fantasy** — role/make-believe.
3. **Narrative** — drama, story drive.
4. **Challenge** — obstacle/mastery, replayability. *(The main driver of most puzzle games.)*
5. **Fellowship** — social framing (multiplayer, leaderboard).
6. **Discovery** — exploration, finding new mechanics.
7. **Expression** — self-expression, customization.
8. **Submission** — passing time, relaxed/automatic play. *(The core aesthetic of casual-puzzle — "playable on the bus".)*

**How to use:**
- Before writing code, write down **2–3 target aesthetics**, in priority order (e.g. block-puzzle = **Challenge + Submission + Sensation**). This is your **cut filter**.
- When a mechanic is proposed, ask: *which dynamic does it create, and which aesthetic does that dynamic serve?* If it serves none of the target aesthetics → **cut it**.
- If a playtest feels "off", **diagnose at the dynamics layer** (which behavior emerged?) before touching the mechanic. The same mechanic produces a different dynamic with a small parameter change.
- Note: the 8 aesthetics are "an arbitrary list" and MDA can overemphasize the mechanic. Use it as a **thinking tool**, not a law.

---

## 2. Loops: Core / Meta / Session

- **Core loop:** The moment-to-moment action chain repeated as the primary experience (match / merge / shoot / build). **Keeps the player for 5 minutes.**
- **Meta loop:** The long-term goals wrapped around the core (unlock, story, prestige, collection). **Keeps the player for 5 months.**
- **Session loop:** The shape of a single session from start to finish (entry hook → a few rising beats → a satisfying peak → a small high point that pulls toward the next).

**Rules:**
- **Summarize the core loop in a single sentence**; it should be readable in a 5-second video. If not, it's too complex.
- Keep the core loop **short, simple, instantly understandable**; secondary systems must NOT SEPARATE play from the core.
- The meta should **reinforce** the core (not scatter it): every meta reward should send the player back to the core for a reason.
- Build the layers deliberately: core → dual loop (a branching choice) → nested loop (a side path that returns to the core) → compulsion loop (habit hooks).

For genre templates → `06-progression-economy-retention.md`.

---

## 3. Design Pillars

3–5 short words/phrases; they capture the game's target feelings/experience (mapping directly to the MDA aesthetics). Every subsequent decision is tested against them: a feature that conflicts with a pillar is **bad design, and is cut.**

- Also write the **non-goals**: what the game explicitly WILL NOT be.
- The pillars are the core of the one-page design (see `07-professional-process.md`) and the strongest shield against scope creep.

Example (Mitomerge): *Drag-merge satisfaction · Meaningful progress in a short session · A defense that keeps working when you leave (idle) · A readable, clean bio-aesthetic.*

---

## 4. Game Feel / "Juice" (short intro)

The satisfaction layer added **after** the mechanic works correctly. Every player interaction must produce immediate, multi-sensory feedback. For the detailed technical list (screenshake, hit-stop, squash&stretch, easing) → `04-game-feel-and-juice.md`.

The golden rule: **"You can't make good juice from a flavorless fruit."** Control and the core mechanic first; polish after.

---

## The golden ordering of the process (summary)

1. Choose the target **aesthetics** (MDA) → cut filter.
2. Write the **pillars** + non-goals (one page).
3. Reduce the **core loop** to a single sentence; design the meta to reinforce the core.
4. **Prototype** to find the "fun" (see 07), then produce.
5. Build the teaching/difficulty curve with **level design** (02, 03, 08).
6. Polish and tune with **juice + playtest + telemetry** (04, 07).

---

## Resources

- MDA: A Formal Approach to Game Design — Hunicke, LeBlanc, Zubek: https://www.researchgate.net/publication/228884866_MDA_A_Formal_Approach_to_Game_Design_and_Game_Research
- MDA framework — Wikipedia: https://en.wikipedia.org/wiki/MDA_framework
- The 8 Kinds of Fun — Skeleton Code Machine: https://www.skeletoncodemachine.com/p/the-8-kinds-of-fun
- The Chemistry of Game Design — Daniel Cook: https://lostgarden.com/2007/07/19/the-chemistry-of-game-design/
- What is a Core Loop in a Mobile Game? — Homa Games: https://www.homagames.com/blog/what-is-a-core-loop-in-a-mobile-game
- The Art of Game Design (interest curve, pacing) — Jesse Schell (notes): https://notesbylex.com/the-art-of-game-design-a-book-of-lenses-2nd-edition-by-jesse-schell
