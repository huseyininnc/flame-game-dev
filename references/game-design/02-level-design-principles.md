# Level Design Principles

Level design = the art of **motivating the player to take action through spaces/situations that reinforce a mechanic**. It is not about visuals; it is about layout, encounters, and **flow**. This document defines this workspace's level design production rules.

> 2D/casual/puzzle-specific application (levels-as-data, difficulty templates, tuning) → `08-level-design-for-2d-casual.md`. Difficulty curve/pacing theory → `03-difficulty-and-pacing.md`.

---

## 1. Level loop: Introduce → Develop → Twist → Conclude

Nintendo's reusable single-mechanic structure (Koichi Hayashida; popularized in the West by Mark Brown/GMTK). **One level = one core idea.**

1. **Introduce:** The new mechanic appears in a **safe, consequence-free** area; the player cannot die and discovers it through experimentation.
2. **Develop:** The same mechanic in a slightly more complex scenario / mild risk.
3. **Twist:** Recontextualize the mechanic — invert it, pair it with another element; force the player to "rethink." ("A doozy that surprises them.")
4. **Conclude (mastery):** Usually right before the goal, a final challenge that **proves** the taught skill. Then **discard** the mechanic — the next level introduces a new idea.

**Rules:**
- **Do not stack more than one new mechanic** in a single level.
- The first encounter with a mechanic must be **fail-proof**.
- Increase difficulty by **recontextualizing** (twist), not by piling on unrelated difficulty.
- End every idea with a "victory lap" that **requires** that skill = your exam.
- Once an idea is complete, **throw the toy away**; reusing the same mechanic over and over after the twist feels like padding.

> The labels (introduce/develop/twist/conclude) are Mark Brown's framing; the "Dan Emmons" attribution is unverified. Source: Hayashida (Gamasutra) + GMTK.

### Kishōtenketsu (conflict-free 4-act)
起承転結 — the skeleton of Mario levels. **It requires no conflict**; tension comes from contrast and discovery.
- **Ki (起):** establish the subject/setting. **Shō (承):** deepen/expand, no surprises. **Ten (転):** an unexpected, often **unrelated** new element — the heart of the curve; it reframes everything. **Ketsu (結):** **reconcile** Ten with Ki+Shō into a satisfying whole (not conflict resolution).
- **Design the Ten (twist) first**, then backfill the intro/development — the design effort should concentrate there.
- You can build a level **without enemy/fail pressure** — let the idea itself be the hero.

### "Teach, then test" (wordless teaching)
Introduce+Develop = **teach** (safe practice); Twist+Conclude = **test** (apply under pressure). The mechanisms that make it work: safe sandbox (failure impossible) · audiovisual affordance (hitting a brick makes it bounce+sound → interactable) · reward placement (a coin positioned to teach the desired action) · cheap/recoverable first fail · assessment before progression.

### Case study — Super Mario Bros. 1-1 (zero text)
Run right (eye-guided by contrast) → first jump = first Goomba (measured speed allowing reaction time) → ? block hit by accident (bounce+sound+coin → reward loop) → the mushroom **bounces off the right pipe and rolls back**, hitting the player (geometry **guarantees** the power-up) → telegraphed small pit → flagpole = "the exam." **Lesson:** put a microcosm of all the mechanics on the opening screen; **force** the key lesson with geometry (don't hope, build it); make the first fail cheap; telegraph danger generously the first time, then tighten the margins.

---

## 2. Player guidance — wordless direction

### Affordance vs Signifier (Norman, adapted to games)
- **Affordance:** what *can be done*, read from an object's form (a ledge affords grabbing, a gap affords jumping).
- **Signifier:** a **perceptible cue** telling where/how to take action (yellow paint, glow, sound). Norman: "for the designer, signifiers are far more important than affordances." Goal: *you shouldn't need to put a sign on the door.*
- Because virtual objects can't be touched, games lean more heavily on signifiers.

### Guiding the eye (the most reliable tools)
- **Contrast** (brightness/color/motion) draws the eye involuntarily. Light the path, darken the dead end (Half-Life 2). In 2D: brighter/higher-contrast tiles along the target route.
- **Reserved "guide color":** a single accent used only for the path/interactables over a muted palette (Mirror's Edge red, Uncharted yellow handholds). Keep the color **exclusive** (never put it on a non-interactive prop) and back it with a **second channel for color-blind safety** (shape/brightness/outline).
- **Leading lines:** converge geometry (pipes, rails, tile edges, lava flow) toward the goal. In 2D, the **shape** of the solid tiles is your leading line.
- **Framing & reveal:** position a tunnel exit so it frames a landmark ("exit the cave, see the castle").
- **Motion** is the strongest attractor (smoke, fire) — use it sparingly, only on what you want looked at.

### Landmark / "weenie" and breadcrumb
- **Weenie** (Disney): a tall visual magnet that pulls you forward. **Density metric:** during the journey the player should be pulled by something **at least every ~30 seconds** — set landmark spacing accordingly.
- **Breadcrumb:** a short-range trail of pickups (coins/rings); for local guidance. Laying breadcrumbs onto a path that **looks** dangerous breaks hesitation ("following the jingle is rewarding").

### Environmental storytelling
Use the space itself as narrative; the story is **inferred**, not told. The player filling the gap (closure) creates investment. Techniques: staged vignettes, causal chains (a blood trail), **environmental telegraphing** (a sparking corpse = electrical hazard — simultaneously teaches safety). Rule: *every anonymous environmental-narrative moment wastes a chance to say something about the game* — no generic décor.

---

## 3. Gating & locks/keys

A "lock" = any obstacle the player can't currently pass; a "key" = the ability/item/**knowledge** that overcomes it. Mark Brown's *Boss Keys* charts every map as a **graph** (room=node, connection=edge): readable but not trivially-linear — it branches and loops.

**Gate types (use precise vocabulary):**

| Type | Definition |
|---|---|
| **Hard gate** | Cannot pass without completion |
| **Soft gate** | Can leave early but usually doesn't |
| **Lock-and-key** | A hard gate requiring a key from elsewhere |
| **Forward gate** | Closes off the critical path |
| **Backward / one-way** | No return; forces flow |
| **Shortcut** | A hard gate opened from the far side (collapses backtracking) |
| **Hidden exit** | Exploration required to find the exit |

**Rules:** **deliberately** choose the gate type of every obstacle; **foreshadow the lock before giving the key** (see it early, return later); let one key open multiple follow-up paths; **collapse backtracking with far-side shortcuts** (the structure that most improves flow).

**Gate complexity:** Teach → Test → Twist. One new concept at a time (don't introduce a new mechanic + new hazard + new enemy at once — the player can't tell what killed them). Combine learned mechanics only after each has been individually proven.

---

## 4. Pacing — tension/rest rhythm (within a level)

- **Intensity** = the excitement of a single event; **pacing** = the timing between peaks.
- **Contrast rule:** flat intensity bores; *constant* maximum intensity numbs ("if 11 is always on, 11 becomes the new 5"). Valleys make the next peak felt.
- **Sawtooth:** a sequence of peaks/valleys with a rising envelope but preserved teeth. A smooth ramp is undesirable — it has no contrast.
- **Rest beat = an engineering tool:** place a guaranteed low-intensity/reward interval after a boss. Rest ≠ inactivity; it's a relative drop (a safe room, traversal, a loot moment).
- **Draw the intensity graph first:** plan the peaks precisely, place the valleys roughly, put story/reward beats **on the peaks**.
- Genre roughly sets the tension:rest ratio — horror ~3:1, comedy ~1:1, action in between.
- **Variety:** also vary the *type* of difficulty (combat → puzzle → traversal); repetition = boredom.

---

## 5. Process: pen&paper → blockout → playtest

Roles (large studio): Level Designer (interaction) · Level Artist · Environment/Lighting Artist · Encounter Designer. Solo, all of these are you — but **keep the phases separate.**

1. **Pen & paper (concept):** think without engine constraints; clarify the mechanics, regions, and progression. Steve Lee: design the level **in text first**.
2. **Blockout / greybox (prototype):** zero new art; **playable** with primitive geometry. The ideal blockout: plays by the rules · clear navigation/landmarks · critical path vs side content defined · readable from both top-down and player view. **Graybox** = abstract blocking with no signature art (flexibility); **whitebox** = with silhouette/key art that gives context.
3. **Metrics:** anchor the scale with a **human-figure reference** (passages neither too narrow nor cavernous). In 2D: tile/grid size, jump range, player speed = the metrics that govern the level.
4. **Playtest (at every phase):** with a fresh player; **no briefing, no interrupting, no taking it personally.** Watch what they **do**, not what they say (hesitation, getting stuck, dying, quitting). Their proposed fix may be wrong, but *the problem it points to is almost always real.*
5. **Art last:** once the layout survives multiple playtests unchanged. *Deleting a rough blockout is cheap; throwing away art-passed work is expensive.*

---

## 6. Common mistakes (fun-killers)

- **Landmark-less mazes** (the #1 readability killer). · **Unfair/unreadable deaths** (hidden spike, off-screen instakill). · **Walls of text** (if you have to explain it with text, the design failed to teach). · **Directionless sandbox** (open space + no pull = paralysis). · **Difficulty spikes** (before introduce-test-combine). · **Dead ends / pointless corridors** ("good on paper, crawls on foot" — always **walk the level at player speed**, don't judge from the editor camera). · **Monotony.** · **Producing art before the layout works** (the most expensive mistake).

---

## One-page summary (2D level construction)

1. **One mechanic per level**: Introduce(safe)→Develop→Twist(recombine)→Conclude(mastery)→discard.
2. Teach **not with text** but with geometry, reward, and feedback. Put a microcosm in the opening, force the key lesson with geometry.
3. **Guide the eye:** contrast/brightness, a reserved guide color (+second channel), tile-shape leading lines, framing.
4. **Weenie density:** something should pull every ~30 sec.
5. Name the **gate type** of every obstacle; foreshadow the lock before the key; collapse backtracking with shortcuts.
6. **Intensity graph first** — precise peaks, rough valleys, rewards on the peaks; the rest beat is a tool.
7. **Blockout first** (massing, metrics+figure, wayfinding, playtest). **Walk** the level, don't fly.
8. **Playtest with a fresh player;** no briefing/interrupting/taking offense; the problem the feedback points to is real.
9. Kill mazes/unfair deaths/dead ends/monotony; the golden path is readable, exploration sits beside it.

---

## Sources

- The secret to Mario level design — Game Developer: https://www.gamedeveloper.com/design/the-secret-to-i-mario-i-level-design
- Kishōtenketsu in Mario — Still Eating Oranges: https://stilleatingoranges.tumblr.com/post/76178051254/kish%C5%8Dtenketsu-in-mario
- Super Mario 3D World's 4-step level design — GMTK (Mark Brown)
- Analysis of Super Mario Bros 1-1 — Medium: https://medium.com/creating-immersive-worlds/analysis-of-super-mario-bros-1-1-2eb9a70fbeb4
- Gates typology — The Level Design Book: https://book.leveldesignbook.com/process/layout/typology/gates
- Pacing — The Level Design Book: https://book.leveldesignbook.com/process/preproduction/pacing
- Blockout & playtesting — The Level Design Book: https://book.leveldesignbook.com/process/blockout
- A taxonomy of weenies — Game Developer: https://www.gamedeveloper.com/design/a-taxonomy-of-weenies-the-landmarks-that-define-i-ghost-of-tsushima-i-
- What Happened Here? (environmental storytelling) — Worch & Smith: https://www.witchboy.net/articles/what-happened-here/
- Level Design 101: The Language of Location Development — MY.GAMES: https://medium.com/my-games-company/level-design-101-the-language-of-location-development-6d940a01b949
- The Art of Level Design — SAE: https://www.sae.edu/gbr/insights/the-art-of-level-design-in-video-games/
- Fortnite/UEFN Level Design Fundamentals — Epic: https://dev.epicgames.com/community/learning/tutorials/3VKJ/unreal-engine-fortnite-level-design-fundamentals
- Holistic Level Design (GDC 2017) — Steve Lee: https://www.youtube.com/watch?v=CpOoTAVeEcU
