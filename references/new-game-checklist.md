# New Flame Game — Checklist

## 0. Concept
- [ ] Genre and core loop defined in a single sentence.
- [ ] Input model: touch / joystick / keyboard / tap.
- [ ] Orientation (portrait/landscape) and target resolution (fixed-resolution?).
- [ ] Platform targets (Android/iOS/web/desktop).

## 1. Scaffold
- [ ] Created with VGV `create-project` (`flame_game`); org + name (with `_`).
- [ ] `analysis_options.yaml` → `very_good_analysis` include.
- [ ] Dependencies: `flame`, plus `flame_audio`, `flame_bloc`, `flame_tiled` if needed.
- [ ] `pubspec.yaml` asset folders: `assets/images/`, `assets/audio/`, `assets/tiles/`.

## 2. Architecture (references/flame/10)
- [ ] The game extends `BaseFlameGame` from `game_core`.
- [ ] Game-specific code lives under `apps/<game>/lib/game`.
- [ ] Persistence (high score, etc.) in the `*_repository` package, independent of Flame.
- [ ] Dependency direction is one-way: feature → core → repository.

## 3. State
- [ ] Score/lives/phase in a Bloc or Cubit.
- [ ] Provided via `FlameBlocProvider`/`FlameMultiBlocProvider`.
- [ ] Components are wired with `FlameBlocReader` (event) / `FlameBlocListenable` (state).
- [ ] Components don't make decisions; they only read and render.

## 4. Screens
- [ ] Menu/settings/level → `RouterComponent` + `Route`/`WorldRoute`.
- [ ] HUD → persistent overlay or `camera.viewport`.
- [ ] Pause → `pauseEngine()` + `overlays.add`.
- [ ] Game over → overlay; play-again flow.
- [ ] **Every overlay wrapped in `Material(type: MaterialType.transparency, child: ...)`** (otherwise bare `Text`s render with a yellow underline).
- [ ] Overlays responsive with `SafeArea` + `ConstrainedBox(maxWidth)`.

## 5. Assets
- [ ] Images as webp (art direction per game), under `assets/images/`, registered in pubspec.
- [ ] Audio sfx/bgm under `assets/audio/`.
- [ ] All assets preloaded in `onLoad` (`images.loadAll`, `audioCache.loadAll`).

## 6. Performance (references/flame/11)
- [ ] No new `Vector2`/list/closure inside `update()`.
- [ ] Object pooling / `RecycledQueue` for frequent objects.
- [ ] `HasQuadTreeCollisionDetection` measured for many static bodies.
- [ ] `FpsTextComponent` in development; `debugMode = false` in release.

## 7. Verification
- [ ] Run on a real device/emulator with `run`/`verify`.
- [ ] 60 FPS observed.
- [ ] Runtime error check with the `dart` MCP (if needed).
- [ ] Lint clean; no comments in code.
