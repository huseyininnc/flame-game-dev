# Flame + flame_bloc: Layered Architecture and Multi-Game Monorepo

This section combines two topics:

1. Using **flame_bloc** to keep game logic in Blocs/Cubits and rendering in Flame components (aligned with Very Good Ventures layered architecture).
2. A reusable monorepo structure in the form of a **shared `game_core` package + a package per game** for rapidly producing many small games.

---

## 1. flame_bloc — Verified API

`flame_bloc` lets you use Blocs and Cubits inside a `FlameGame`, similar to `flutter_bloc`. All class names below are verified against the flame_bloc source.

### 1.1 Providing a Bloc: `FlameBlocProvider`

```dart
class MyGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    await add(
      FlameBlocProvider<PlayerInventoryBloc, PlayerInventoryState>(
        create: () => PlayerInventoryBloc(),
        children: [
          Player(),
          // ...
        ],
      ),
    );
  }
}
```

All components that are `children` of this provider can access the bloc. To share an existing bloc instance, use the `.value` constructor (e.g. to carry a bloc from the Flutter tree into Flame):

```dart
FlameBlocProvider<ScoreBloc, ScoreState>.value(
  value: existingScoreBloc,
  children: [GameWorld()],
);
```

### 1.2 Multiple blocs: `FlameMultiBlocProvider`

```dart
class MyGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    await add(
      FlameMultiBlocProvider(
        providers: [
          FlameBlocProvider<PlayerInventoryBloc, PlayerInventoryState>(
            create: () => PlayerInventoryBloc(),
          ),
          FlameBlocProvider<PlayerStatsBloc, PlayerStatsState>(
            create: () => PlayerStatsBloc(),
          ),
        ],
        children: [
          Player(),
          // ...
        ],
      ),
    );
  }
}
```

### 1.3 Listening to state — three approaches

**(a) `FlameBlocListener` component** (supports a `listenWhen` filter):

```dart
class Player extends PositionComponent {
  @override
  Future<void> onLoad() async {
    await add(
      FlameBlocListener<PlayerInventoryBloc, PlayerInventoryState>(
        onNewState: (state) {
          updateGear(state);
        },
        listenWhen: (previous, current) => previous.gear != current.gear,
      ),
    );
  }
}
```

**(b) `FlameBlocListenable` mixin** — has `onNewState`, plus optional `onInitialState` and `listenWhen` overrides:

```dart
class Player extends PositionComponent
    with FlameBlocListenable<PlayerInventoryBloc, PlayerInventoryState> {

  @override
  void onInitialState(PlayerInventoryState state) {
    // Called once with the current state when the component is mounted.
    updateGear(state);
  }

  @override
  bool listenWhen(PlayerInventoryState previous, PlayerInventoryState current) {
    return previous.gear != current.gear;
  }

  @override
  void onNewState(PlayerInventoryState state) {
    updateGear(state);
  }
}
```

**(c) `FlameBlocReader` mixin** — for accessing the bloc and sending events only (does not listen for state changes). Limited to **a single bloc**:

```dart
class Player extends PositionComponent
    with FlameBlocReader<PlayerStatsBloc, PlayerStatsState> {

  void takeHit() {
    bloc.add(const PlayerDamaged());
  }
}
```

> Do not produce class names from memory; the correct names are: `FlameBlocProvider`, `FlameBlocProvider.value`, `FlameMultiBlocProvider`, `FlameBlocListener` (parameter `onNewState`), `FlameBlocListenable` (mixin, `onNewState`/`onInitialState`/`listenWhen`), `FlameBlocReader` (mixin, `bloc` getter).

### 1.4 Separation of responsibilities (alignment with VGV)

| Layer | Responsibility | flame_bloc role |
|---|---|---|
| **Repository / Data** | Data sources (high-score persistence, settings, audio preferences) | Consumed by the Bloc |
| **Bloc / Cubit** | Game *state* and *rules* (score, health, inventory, phase) | Provided via `FlameBlocProvider` |
| **Component (Flame)** | **Render** only and input -> event | Sends events via `FlameBlocReader`, reacts to state via `FlameBlocListenable` |

The rule: **Components do not make decisions; they read state and draw.** Decisions such as damage, score, and phase transitions are made in the Bloc. This keeps game logic widget/testable and separated from rendering.

---

## 2. Multi-Game Monorepo: Reuse Strategy

The goal: rapidly produce many small games on top of a **shared core**. VGV conventions are followed (Melos monorepo, Bloc, layered architecture, `very_good_analysis`).

### 2.1 Folder tree

```text
games_monorepo/
├── melos.yaml
├── pubspec.yaml
├── analysis_options.yaml          # include: package:very_good_analysis/analysis_options.yaml
│
├── packages/
│   ├── game_core/                 # SHARED core (UI/game-agnostic)
│   │   ├── lib/
│   │   │   ├── src/
│   │   │   │   ├── base/
│   │   │   │   │   └── base_flame_game.dart      # common FlameGame base class
│   │   │   │   ├── components/                    # reusable components
│   │   │   │   │   ├── fade_in_component.dart
│   │   │   │   │   ├── parallax_background.dart
│   │   │   │   │   └── pooled/                     # object pool helpers
│   │   │   │   ├── services/
│   │   │   │   │   ├── audio_service.dart          # audio playback abstraction
│   │   │   │   │   └── asset_manager.dart          # cached asset loading
│   │   │   │   ├── state/                          # common Blocs/Cubits
│   │   │   │   │   ├── score/
│   │   │   │   │   │   ├── score_bloc.dart
│   │   │   │   │   │   ├── score_event.dart
│   │   │   │   │   │   └── score_state.dart
│   │   │   │   │   └── game_phase/
│   │   │   │   │       └── game_phase_cubit.dart   # menu/playing/paused/gameOver
│   │   │   │   └── overlays/
│   │   │   │       ├── pause_menu.dart             # shared Flutter overlays
│   │   │   │       └── game_over_menu.dart
│   │   │   └── game_core.dart                      # public barrel export
│   │   ├── pubspec.yaml
│   │   └── test/
│   │
│   ├── scores_repository/         # DATA + REPOSITORY layer (persistence)
│   │   ├── lib/
│   │   │   ├── src/
│   │   │   │   ├── scores_repository.dart
│   │   │   │   └── models/score_entry.dart
│   │   │   └── scores_repository.dart
│   │   └── pubspec.yaml
│   │
│   └── game_ui/                   # shared theme/button/dialog (Flutter)
│       └── ...
│
└── apps/
    ├── flappy_clone/              # PER-GAME package (feature layer)
    │   ├── lib/
    │   │   ├── game/
    │   │   │   ├── flappy_game.dart            # extends BaseFlameGame
    │   │   │   ├── components/                  # components specific to this game
    │   │   │   └── state/                       # Blocs specific to this game
    │   │   ├── view/
    │   │   │   └── flappy_page.dart             # GameWidget + overlayBuilderMap
    │   │   └── main.dart
    │   ├── assets/
    │   └── pubspec.yaml            # depends on: game_core, scores_repository, game_ui
    │
    └── brick_breaker/
        └── ... (same skeleton)
```

### 2.2 Layer boundaries (dependency direction)

```text
apps/<game>  ->  game_core  ->  scores_repository  ->  (data sources)
   (feature)      (engine)        (repository)            (data)
```

- **`scores_repository` (data/repository):** Knows nothing about Flame. Saves/reads the high score, returns domain models. Testable, pure Dart.
- **`game_core` (engine):** The base shared by all games — `BaseFlameGame`, reusable components, `AudioService`, `AssetManager`, common Blocs (`ScoreBloc`, `GamePhaseCubit`), shared overlays. Knows nothing about a specific game.
- **`apps/<game>` (feature):** Only the components, Blocs, and `GameWidget` wiring specific to that game. Depends on `game_core` and `scores_repository`.

This direction is **one-way**: feature -> core -> repository. The core never depends back on a game; adding a new game does not break the existing core (Open/Closed).

### 2.3 Shared base game class

```dart
// game_core/lib/src/base/base_flame_game.dart
abstract class BaseFlameGame extends FlameGame {
  BaseFlameGame({required this.audioService, required this.assetManager});

  final AudioService audioService;
  final AssetManager assetManager;

  @override
  Future<void> onLoad() async {
    await assetManager.preloadCommon();
    await super.onLoad();
  }
}
```

The per-game package extends this:

```dart
// apps/flappy_clone/lib/game/flappy_game.dart
class FlappyGame extends BaseFlameGame {
  FlappyGame({required super.audioService, required super.assetManager});

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    await add(
      FlameMultiBlocProvider(
        providers: [
          FlameBlocProvider<ScoreBloc, ScoreState>(create: ScoreBloc.new),
          FlameBlocProvider<GamePhaseCubit, GamePhase>(create: GamePhaseCubit.new),
        ],
        children: [FlappyWorld()],
      ),
    );
  }
}
```

### 2.4 Shared services (dependency through abstraction)

`AudioService` and `AssetManager` abstract the concrete Flame calls and are injected into games (Dependency Inversion). This way each game does not rewrite the same services and they can be mocked in tests.

```dart
// game_core/lib/src/services/audio_service.dart
abstract class AudioService {
  Future<void> preload(List<String> files);
  void playSfx(String file);
  Future<void> playBgm(String file);
}
```

### 2.5 Summary of VGV conventions

- State management with **Bloc/Cubit**; game logic in the Bloc, not in the component.
- **Layered architecture:** data (the sources inside `*_repository`) -> repository -> business (Bloc) -> feature (game package). Each layer depends only on the one beneath it.
- **Single responsibility per package:** `scores_repository` is only persistence, `game_core` is only the reusable engine.
- **`very_good_analysis`** is included as the strictest lint rule in the root `analysis_options.yaml`.
- **Melos** for bootstrap/test/format across packages with a single command.
- **A new game = a new `apps/<game>` package**; the core is not copied, it is pulled in as a dependency.

---

## Sources

- https://raw.githubusercontent.com/flame-engine/flame/main/packages/flame_bloc/README.md
- https://pub.dev/packages/flame_bloc
- https://verygood.ventures/blog/flame-bloc-new-api
