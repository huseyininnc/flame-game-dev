---
name: flame-game-dev
description: Build 2D games with the Flutter Flame engine (flame ^1.37.0) AND design them well — level design, difficulty/pacing, game feel, progression/retention, and professional process. Use when creating, scaffolding, designing, or extending any Flame game — game loop, components, sprites/animations, input, collision, camera/world, audio, overlays/routing, flame_bloc, performance, level/wave design, difficulty tuning, and AI asset generation. Triggers on "new game", "Flame game", "FlameGame", "add a level/enemy/player", "level design", "difficulty curve", "game over screen", "sprite/animation", "generate game assets".
when_to_use: Use whenever working on a Flame-based game in the games workspace — starting a new game, designing levels/waves/difficulty, adding game features (player, enemies, levels, HUD, collision, audio), wiring state with flame_bloc, optimizing for 60 FPS, or generating sprite/audio assets. Skip for non-game Flutter UI work.
---

# Flame Game Development (series production)

This skill is for producing **many games, of different concepts**, with the Flutter **Flame** engine. It uses two verified knowledge bases (KBs) as production rules: **technical (the Flame engine)** and **design (level design + professional process)**.

> **This skill is self-contained.** All KBs and references are inside the skill folder (`references/`). When you copy the skill, all references come with it intact; it does not depend on an external `docs/` folder.

## ⛔ STUDIO-GRADE MANDATE (hard gate — non-negotiable)

This skill does NOT produce **amateur, short, "MVP-as-product", single-mechanic tech-demo** games. Every game produced must be **as if it came out of a large studio staffed by senior teams with 15+ years of experience**: production-ready, content-rich, multi-asset, a **full release**. Work like a real studio (deliberately wear the design+art+animation+VFX+audio+UI/UX+engineering+QA+live-ops disciplines).

- **The required bar and "definition of done": `references/production-standards.md`.** The items in this document are **release blockers**; apply them in every game.
- **An MVP/prototype is only for finding the "fun" during preproduction** — it is never the delivered product. The delivery is always full, polished, and content-rich.
- **Scope floors (launch minimum):** puzzle 100–200 levels · hybrid-casual 3–5 distinct mechanics · idle 40–60 hours + 2–4 prestige · wave/arena 8–15 enemy types + 3+ biomes. Early + mid + **late game** together.
- **Full system stack at launch:** core loop + progression backbone + 2 currencies + shop/IAP + ads mediation + daily reward + FTUE + settings + save(+cloud) + analytics (with battle pass/event/leaderboard scaffolding as a fast-follow).
- **Polish everywhere:** juice on every interaction (easing/hit-stop/screenshake/sound/haptics), a single style guide (no placeholder/default fonts), animated UI, adaptive audio, locked 60 FPS, input latency < 100ms.
- **Finishability = systems:** data-driven/parametric content + reused systems (build the engine once, pour content in as data). Be ambitious BUT finish.
- **Production order:** vertical slice (near-final quality) → content production → protected polish → soft-launch reading → launch.

## Absolute rules (aligned with the workspace CLAUDE.md)

1. **NO comments in code.** Inline, block, doc — none. The code explains itself through clear naming.
2. **Mimic the existing patterns.** Before writing new code, study the surrounding code; follow its architecture and style exactly.
3. **SOLID + DRY + KISS + YAGNI.** Components have a single responsibility; game logic lives in Bloc/Cubit, rendering in the component.
4. **`any`/`dynamic` forbidden.** The strictest lint: `very_good_analysis`.
5. **Get approval first for any new library/architecture change.**
6. **Every game must be original.** Mechanics/narrative differ from game to game; only the code conventions (architecture/style) are shared — do not copy game design.
7. **The studio-grade bar is mandatory.** No amateur/short/MVP-as-product; apply `references/production-standards.md` in every game.
8. **Every game has ITS OWN identity (anti-reskin).** Theme, palette, **HUD layout**, UI/button/panel style, **font trio**, motion personality, and **core mechanic** change according to the game's content; they differ from the previous game. **Reusing `overlay_widgets`/HUD/palette/font across games is FORBIDDEN** (code architecture is shared, visual identity is not). **Orientation (portrait OR landscape) is chosen per game** — do not make them all portrait. Rule + brand test: `references/game-design/09-art-ui-identity-and-orientation.md`.

## Knowledge base — read first

The KBs are inside the skill; paths are relative to the skill root (`references/...`).

### A) Technical KB — `references/flame/` (HOW it is built)
- Setup, `FlameGame`, game loop, asset structure → `references/flame/01-overview-and-setup.md`
- FCS, `PositionComponent`, lifecycle, mixins → `references/flame/02-components-and-lifecycle.md`
- Sprite/animation/text → `references/flame/03-rendering-sprites-text.md`
- Input (tap/drag/keyboard/joystick) → `references/flame/04-input-and-gestures.md`
- Effects and particles → `references/flame/05-effects-and-particles.md`
- Collision → `references/flame/06-collision-detection.md`
- Camera/World/viewport/HUD → `references/flame/07-camera-world-viewport.md`
- Audio + Tiled maps → `references/flame/08-audio-and-tiled.md`
- Overlays/Router/game state → `references/flame/09-overlays-router-state.md`
- flame_bloc + layered architecture + monorepo → `references/flame/10-architecture-bloc-multigame.md`
- Performance (60 FPS) → `references/flame/11-performance-optimization.md`

### B) Design KB — `references/game-design/` (WHAT and WHY)
- MDA, aesthetics, core/meta/session loop, pillars, juice (intro) → `references/game-design/01-design-foundations.md`
- **Level design core** (introduce/develop/twist/conclude, Kishōtenketsu, teach-then-test, signposting, gating, in-level pacing, blockout, common mistakes) → `references/game-design/02-level-design-principles.md`
- Difficulty curve, flow channel, sawtooth, interest curve, DDA, balancing → `references/game-design/03-difficulty-and-pacing.md`
- Game feel & juice (screenshake, hit-stop, squash & stretch, easing, sound) → `references/game-design/04-game-feel-and-juice.md`
- Onboarding / FTUE (show-don't-tell, skill atom, time-to-fun) → `references/game-design/05-onboarding-and-tutorialization.md`
- Progression / economy / retention (loop templates, reward schedule, source/sink, D1/D7/D30, ethics) → `references/game-design/06-progression-economy-retention.md`
- Professional process (preprod→prod→liveops, prototype vs vertical slice, milestones, lean GDD, playtest, MVP) → `references/game-design/07-professional-process.md`
- **Level design practice for 2D/puzzle/casual/idle** (levels-as-data, LevelConfig, sawtooth template, match-3 tuning, telemetry, Flame mapping) → `references/game-design/08-level-design-for-2d-casual.md`
- **Per-game design identity (MANDATORY)** — HUD diegesis, genre-based HUD layout, typography/font trio, the 5 columns of visual identity, orientation (portrait/landscape) choice, anti-reskin checklist → `references/game-design/09-art-ui-identity-and-orientation.md`

**Which one when:** when designing structure/levels/difficulty/waves, use **B (especially 02, 03, 08)**; for coding/engine work, use **A**. Use both together — good code does not save bad design.

## Version and current-API requirements

- **flame `^1.37.0`**, flame_audio `^2.12.1`, flame_tiled `^3.1.1`, flame_bloc (current). (The existing workspace games use flame `^1.35.1` — for a new game, align with the version of the existing game.)
- **Camera:** use `CameraComponent` + `World`; NO old `Camera`.
- **Input:** the `TapCallbacks` / `DragCallbacks` mixins; NO old `Tappable`/`Draggable`.
- **Game access:** `HasGameReference<MyGame>` (the `game` getter); the old `HasGameRef` is deprecated.
- Game objects are added to `world`, the HUD to `camera.viewport`.
- `update(dt)` is frame-rate independent: movement/physics always `* dt`.
- **Responsive (MANDATORY in every game, independent of art style):** gameplay in `world` / HUD in `camera.viewport`; no hardcoded pixel positions (percentages + `onGameResize`); `CameraComponent.withFixedResolution` or a deliberate `MaxViewport`+`visibleGameSize`; sprites in world units; **FilterQuality according to the chosen art style** (soft/vector/painterly = `medium`/`high`; if pixel-art is chosen = `none` + nearest); Flutter overlays with `MediaQuery.sizeOf` breakpoints (600/840) + clamp + `SafeArea` + `Material` wrapping; images `cover/contain` (never `fill`) + `cacheWidth×dpr` + density buckets. Full recipe: `references/responsive-design.md`. Verify on phone + tablet + two extreme aspect ratios.
- **Overlay text must be wrapped in Material (mandatory):** Flame `GameWidget` overlays are rendered OUTSIDE the Material context of `MaterialApp`; bare `Text`s appear with a yellow double underline. Wrap every overlay in `overlayBuilderMap` with `Material(type: MaterialType.transparency, child: ...)`.

## New-game startup flow

1. **Concept & identity (before code):** target aesthetics (MDA), 3–5 design pillars + non-goals, a single-sentence core loop (`references/game-design/01`). **Choose this game's specific identity (different from the previous one): theme, palette, HUD diegesis + layout, UI/button/panel style, font trio (display/UI/numeric), motion personality, and orientation (portrait OR landscape — by genre/grip)** — `references/game-design/09`. The core mechanic, too, must not repeat across the portfolio.
2. **Level/difficulty design (before code):** design the core loop's teach→test→twist flow, the **sawtooth difficulty curve**, and the level/wave structure (`references/game-design/02`, `03`, `08`). Model levels as **data (config/JSON)** — do not hardcode them.
3. **Scaffold:** use the VGV `create-project` skill for the `flame_game` template (or `flutter create` if unavailable). Use `_` instead of dashes in the project name.
4. **Architecture:** the Bloc + layered strategy from `references/flame/10`. Game state in Bloc/Cubit; real-time sim in components; component↔Bloc with the workspace convention (existing games use a direct `game.gameBloc` reference).
5. **Scene/screen:** menu/level → `RouterComponent`; pause/game-over/HUD → overlays (`references/flame/09`).
6. **Assets:** write a visual + audio **manifest** and generate with `scripts/asset_gen.py` and `scripts/audio_gen.py` (`references/asset-generation.md`). **The art direction is chosen AUTOMATICALLY based on the game's content/theme/target audience** (modern flat, painterly, vector, cartoon, isometric, pixel-art… — **pixel-art is not the default/required**); define a single style guide consistent with the chosen style and apply it to all assets. Whatever the style, the responsive rules (`references/responsive-design.md`) apply.
7. **Game feel:** add juice to every interaction — feedback, screenshake, hit-stop, easing, sound (`references/game-design/04`). Controls + mechanics first, then polish.
8. **Onboarding:** design the first 60 seconds with show-don't-tell, introducing one mechanic at a time (`references/game-design/05`).
9. **Performance:** preload in `onLoad`; no allocation in `update`; pooling for frequent objects; `FpsTextComponent`.
10. **Verify:** run it and observe real behavior (`run`/`verify`, and the `dart` MCP if needed). If possible, playtest with a fresh player and observe the behavior (`references/game-design/07`).

Detailed checklists: `references/production-standards.md` (**studio-grade bar / definition-of-done — hard gate**) + `references/game-design/09-art-ui-identity-and-orientation.md` (**per-game identity / anti-reskin — brand test**) + `references/new-game-checklist.md` (production) + `references/level-design-checklist.md` (design).

## Level / wave design rules (summary)

- **One new idea per level:** Introduce(safe)→Develop→Twist(recombine)→Conclude(mastery)→discard.
- **Difficulty = sawtooth** (not linear): climb → deliberately drop → climb; relief after a spike.
- **Levels-as-data:** a single generic `LevelConfig` + a single loader; no per-level code. In a real-time game, a "level" ≈ a wave/zone (wave count, spawn interval, HP/speed scale, boss cadence).
- **Teach with geometry/feedback, not text;** guide the eye with contrast + a reserved guide color.
- **Telemetry:** instrument attempts + drop-off per level/wave; reorder/retune with the data.

## Asset generation

Two **generic, manifest-driven** tools are inside the skill: `scripts/asset_gen.py` (images via Vertex `gemini-3-pro-image-preview`; opaque or chroma-key transparent webp) and `scripts/audio_gen.py` (sfx/bgm wav via stdlib). Do NOT write a separate script per game — write a JSON manifest and run the tool:
`cd scripts && pip install -r requirements.txt && cp .env.example .env` (VERTEX_API_KEY into `.env`) → `python asset_gen.py --manifest <game>.json --out <game>/assets/images`. Chroma: a color that does not clash with the subject (green/cyan subject→`magenta`, red subject→`green`). Details/schema: `references/asset-generation.md` + `scripts/README.md`. (`.env` is not committed.)

## Component authoring rules

- Single responsibility; split a component over 200 lines into sub-components/services.
- `onLoad` for async setup; `update`/`render` thin and allocation-free.
- Choose the anchor deliberately (`Anchor.center` for movement/rotation).
- Route the collision reaction to a Bloc event where possible, not into the component.
- Always call `super` in lifecycle overrides.
