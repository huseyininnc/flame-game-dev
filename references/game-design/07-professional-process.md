# Professional Game Development Process

The workflow from concept to launch and live-ops; prototype/vertical slice, milestones, GDD, iteration/playtest, and scoping.

---

## 1. Development life cycle

**Rule:** the cost of changing a design decision multiplies the further right you move through these phases. **Spend a disproportionate share of the effort on preproduction.**

- **Concept / Ideation:** genre, audience, theme, hook, core fantasy; feasibility/profitability check. Output: a short pitch + target aesthetics (MDA, see 01).
- **Preproduction (the most important phase):** figure out *what will be built, what it will cost, and whether it is fun* — i.e. **"find the fun"** — BEFORE expensive production. Kill risk cheaply. Activities: prototype, core-loop, engine/technology selection, art-direction testing, a one-page GDD, and ideally a **vertical slice**. Exit: you know the game is worth building and roughly what it will cost; the question "is it fun?" must not remain open.
- **Production:** the blueprint turns into content at scale (all systems/levels/art/audio). Most of the cost and headcount sits here. Playtesting is continuous.
- **Post-production:** Alpha → Beta → Release stabilization (bug fixing, balancing, optimization, certification).
- **Live-Ops / maintenance (a must for casual/mobile):** continuous post-launch content + events (new level packs, seasons, tournaments, discounts). By nature **agile and cyclical**. In match-3/casual, **~40–80 new levels per month** is expected, at a weekly/biweekly cadence (see 08).

---

## 2. Prototype & vertical slice

- **Paper prototype:** the cheapest test; test the **mechanic** with cards/tokens/grids (not graphics). Fail fast, discard the weak idea.
- **Greybox/blockout:** **playable** with zero new art; isolate a single mechanic. (See 02 §5.)
- **"Find the fun" prototype:** a throwaway digital build; its only job is to verify that the core loop is fun while changing it is still cheap. If you can't find it, **do not** proceed to production.
- **Vertical slice:** a small but **final-quality** slice (art+gameplay+systems+UI+audio together, at ship quality) = "one level, but real." Why: the preprod→prod **gating decision**; it proves the pipeline and the quality bar; it's a publisher/management pitch artifact. Keep its scope **small** (it's expensive).
- **Distinction:** prototype = *"is it fun?"* (ugly, throwaway). Vertical slice = *"can we produce this quality at scale, should it be funded?"* (representative, polished).

---

## 3. Milestones (definition & exit criteria)

| Milestone | Definition | Exit criteria |
|---|---|---|
| **Prototype** | Core mechanic isolated, throwaway code/art | Core loop demonstrably fun |
| **First Playable** | Representative gameplay + placeholders, playable start to finish | Main gameplay elements working, readable |
| **Vertical Slice** | Final-quality representative section | Quality bar + pipeline proven; greenlight decision |
| **Alpha (Feature Complete)** | All features present; playable start to finish; assets may be placeholder | **Feature freeze** — no new features afterward |
| **Beta (Content Complete)** | All features + final assets; bug-fix/balance only | **Content freeze**; no ship-blockers |
| **Release Candidate / Gold** | Final build, passed certification | Zero known blockers; passes cert; approved |

**Practical rule:** *feature freeze (alpha)* and *content freeze (beta)* are hard gates. The most common production mistake: adding features after alpha (it resets the stabilization clock).

---

## 4. GDD — the modern, lightweight approach

A lean, **living** communication tool; not a 100-page database.

- **Start with one page** (the Stone Librande discipline): title + tagline, a one-paragraph elevator pitch, **design pillars**, audience/platform, core loop, main mechanics, secondary systems, progression, art/audio direction, a rough roadmap. **Visuals** (map/flowchart) > dense text. A reader should grasp the core in ~30 seconds.
- **Pillars:** 3–5 short phrases (mapped to MDA aesthetics); every decision is tested against them. Write down the **non-goals** too.
- **Grow it layer by layer:** 1 page → ~10 pages → full document; don't write the full document up front.
- **Avoid:** over-specifying an untested mechanic before prototyping; a large document that goes stale early; burying system relationships across scattered wiki pages.

---

## 5. Iteration & playtest

**The loop:** hypothesis → build the smallest testable version → playtest/observe → measure → cut/adjust → repeat. **Designs are hypotheses; the playtest is the experiment (Valve).**

- **Types:** internal (devs, as soon as it's playable) · external/fresh players (a must; the dev is blind to their own game) · **Kleenex testing** (use each test player **once** — first-impression/onboarding happens once) · usability ("can they use it?") vs experience ("is the target aesthetic coming through?").
- **What to observe:** what they **do**, not what they say — confusion, hesitation, getting stuck/quitting, time per section, failure frequency. Protocol: observe → short survey → short Q&A. Biometrics aren't needed. Valve's level designers playtest **every week**.
- **Telemetry:** log failure points, attempts per level, drop-off, session length, churn; retune after soft-launch and **reorder the levels** (see 08).

---

## 6. Scoping & cutting (MVP)

- **MVP** = only the core features, to a test player as fast as possible.
- **Kill your darlings:** be willing to cut beloved features that don't serve the vision. "Being able to do something doesn't mean you should — bloat kills the game."
- **MoSCoW:** Must / Should / Could / Won't. Lock the "Must"; the rest is cuttable.
- Scope creep is the default failure mode of solo/indie — actively manage it against the pillars and the MVP definition.

---

## Sources

- What Is the Game Development Life Cycle? — Game Developer: https://www.gamedeveloper.com/business/what-is-the-game-development-life-cycle-
- What you should take out of Pre-Production — Game Developer: https://gamedeveloper.com/blogs/what-you-should-take-out-of-pre-production
- Vertical Slice in Game Development — Nineva: https://ninevastudios.com/blog/vertical-slice-game-development-guide
- Milestones: Alpha, Beta and Gold — Experimental Game Studio: https://mycours.es/gamedesign2021/milestone-beta/
- How to write a game design document — Game Dev Beginner: https://gamedevbeginner.com/how-to-write-a-game-design-document-with-examples/
- Valve's philosophy with User Research — Steve Bromley: https://www.stevebromley.com/blog/2011/09/01/valves-philosophy-with-user-research-in-games-habe-newell-and-mike-ambinder/
- Playtest / Kleenex testing — Wikipedia: https://en.wikipedia.org/wiki/Playtest
- Solving Scope Creep with Iterative Game Planning — Wayline: https://www.wayline.io/blog/scope-creep-iterative-game-planning
