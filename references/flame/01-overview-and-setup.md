# Flame Engine — Overview, Setup & Game Loop

Flame is a minimalist 2D game engine built on top of Flutter. It does not replace Flutter — it runs *inside* a Flutter widget tree and gives you the building blocks that a game needs (a game loop, a component/entity system, a camera, sprites, input handling, collision detection, audio, effects, and more) as a set of independent, opt-in modules. Because it is "just Flutter," a Flame game ships to every Flutter target (iOS, Android, web, desktop) with the same codebase, and you can freely mix Flame surfaces with ordinary Flutter widgets.

This document covers installation, the recommended project/asset structure, and the `FlameGame` class with its game loop.

> **Version note:** The current stable release at the time of writing is **`flame: ^1.37.0`** (verified-publisher `flame-engine.org` on pub.dev). Flame went through significant API changes on the road to 1.x — most importantly the old `Camera` was replaced by the `CameraComponent` + `World` model, which is what this documentation uses throughout.

---

## 1. Installing Flame & a minimal app

Add the package with the Flutter CLI:

```bash
flutter pub add flame
```

This adds the dependency to your `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  flame: ^1.37.0
```

### Minimal `main.dart`

A Flame game is rendered by placing a `GameWidget` somewhere in your Flutter tree. The simplest possible app instantiates a `FlameGame` and hands it to a `GameWidget`:

```dart
import 'package:flame/game.dart';
import 'package:flutter/widgets.dart';

void main() {
  final game = FlameGame();
  runApp(GameWidget(game: game));
}
```

In practice you subclass `FlameGame` so you have a place to load assets and build your component tree:

```dart
import 'package:flame/components.dart';
import 'package:flame/game.dart';
import 'package:flutter/widgets.dart';

class MyGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    // Add the root-level components / set up the world & camera here.
  }
}

void main() {
  runApp(GameWidget(game: MyGame()));
}
```

`GameWidget` is a normal Flutter widget, so you can embed it inside any layout — it does not have to be the root of the app. It also accepts useful builders such as `overlayBuilderMap` (to draw Flutter widgets on top of the game) and `loadingBuilder` (shown while `onLoad` runs).

> **Tip — `GameWidget.controlled`:** When the game's lifetime should match the widget's lifetime, use `GameWidget.controlled(gameFactory: MyGame.new)`. This lets the widget create and dispose the game for you, which avoids holding on to a stale game instance across rebuilds.

---

## 2. Recommended project & asset structure

Flame expects game assets to live under a top-level `assets/` directory, conventionally split by asset type:

```
my_game/
├── assets/
│   ├── audio/
│   │   └── explosion.mp3
│   ├── images/
│   │   ├── player.png
│   │   ├── enemy.png
│   │   └── spritesheet.png
│   └── tiles/
│       ├── level.tmx
│       └── map.json
├── lib/
│   └── main.dart
└── pubspec.yaml
```

- **`assets/images/`** — sprites, sprite sheets, backgrounds. This is the default folder that `Flame.images` / the `Images` cache reads from.
- **`assets/audio/`** — sound effects and music, read by the `AudioCache` (from the `flame_audio` package). You may optionally split it into `assets/audio/music/` and `assets/audio/sfx/`.
- **`assets/tiles/`** — Tiled map files (`.tmx`) and JSON map data, read by `flame_tiled`.

### Registering assets in `pubspec.yaml`

As with any Flutter project, the asset folders must be declared under the `flutter:` section, otherwise they will not be bundled:

```yaml
flutter:
  assets:
    - assets/images/
    - assets/audio/
    - assets/tiles/
```

### Customizing asset locations

The default folders are a convention, not a hard rule. The caches (`Images`, `AssetsCache`, `AudioCache`) all accept a `prefix` parameter so you can point them at a different directory, and they accept a custom `AssetBundle`, which means you can even load assets from the filesystem instead of `rootBundle`:

```dart
final images = Images(prefix: 'assets/sprites/');
final sprite = await Sprite.load('player.png', images: images);
```

When you call `Sprite.load('player.png')` without arguments, Flame resolves it relative to `assets/images/`, so you reference files by name only — not by their full path.

---

## 3. `FlameGame`, the game loop & resizing

`FlameGame` is the root of your game. It plays a role analogous to Flutter's `MaterialApp`: it is the top-level object, it owns the game loop, and it is the root of the **Flame Component System (FCS)** component tree. It is itself a `Component`, so everything you can do with a component you can also do with the game.

### The game loop: `update(dt)` and `render(canvas)`

On every frame ("tick") Flame calls two methods in sequence on the whole component tree:

- **`update(double dt)`** — `dt` is the *delta time* in **seconds** since the previous frame. Advance your game state here. Always multiply movement/physics by `dt` so the game runs at the same speed regardless of frame rate.
- **`render(Canvas canvas)`** — draw the current state onto the Flutter `Canvas`.

```dart
class MyGame extends FlameGame {
  @override
  void update(double dt) {
    super.update(dt); // propagates update() to all children — don't forget this
    // global per-frame logic
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas); // propagates render() to all children
    // global drawing (e.g. background)
  }
}
```

In a component-based game you usually do *not* override these on `FlameGame` itself; you let each component handle its own `update`/`render`. Movement is typically frame-rate independent, e.g. `position += velocity * dt`.

### `onLoad` — the async constructor

`onLoad()` returns a `Future` and is the right place for any asynchronous setup (loading sprites, audio, building the initial tree). It runs **once** when the game is first attached to a `GameWidget`. While it is running, the `GameWidget`'s `loadingBuilder` (if provided) is shown.

```dart
@override
Future<void> onLoad() async {
  await add(Player());
  await world.add(Enemy());
}
```

### `onGameResize` — reacting to size changes

`onGameResize(Vector2 size)` is called whenever the rendering surface changes size — including the very first layout, on device rotation, and on window resize. It is propagated to every component in the tree, so each component can adapt its layout.

```dart
@override
void onGameResize(Vector2 size) {
  super.onGameResize(size);
  // reposition HUD elements relative to the new size
}
```

> **Lifecycle ordering caveat:** For a normal `Component`, `onLoad` runs *before* `onGameResize`. For `FlameGame` the order is **reversed**: `onGameResize` runs first (so sizes are known before assets load), then `onLoad`, then `onMount`. After that the per-frame `update → render` loop begins. On detach, `onRemove` runs.

### World & camera (the current API)

Modern Flame separates *what* exists in the game (`World`) from *how it is viewed* (`CameraComponent`). `FlameGame` ships with a built-in `world` and `camera`:

```dart
import 'package:flame/components.dart';
import 'package:flame/game.dart';
import 'package:flutter/widgets.dart';

class MyCrate extends SpriteComponent {
  MyCrate() : super(size: Vector2.all(16));

  @override
  Future<void> onLoad() async {
    sprite = await Sprite.load('crate.png');
  }
}

class MyWorld extends World {
  @override
  Future<void> onLoad() async {
    await add(MyCrate());
  }
}

void main() {
  final myGame = FlameGame(world: MyWorld());
  runApp(GameWidget(game: myGame));
}
```

Game objects are added to the `world` (which the camera observes), while HUD/overlay components that should stay fixed on screen are added to `camera.viewport`. By passing a custom `World` subclass as a type argument — `class MyGame extends FlameGame<MyWorld>` — you get type-safe access to your world without casting.

### Pausing, resuming & debug mode

```dart
game.pauseEngine();   // stop the update/render loop
game.resumeEngine();  // resume it
game.paused;          // bool getter/setter
game.stepEngine();    // advance a single frame (useful while paused)

game.debugMode = true; // draw debug info (bounding boxes, etc.) for all components
```

By default a game pauses automatically when the app is backgrounded; set `pauseWhenBackgrounded = false` to opt out.

### Cleanup

`onRemove()` runs when the game is detached. Use it (or `game.dispose()`, which handles common cleanup) to release caches and child components:

```dart
@override
void onRemove() {
  removeAll(children);
  Flame.images.clearCache();
  Flame.assets.clearCache();
  super.onRemove();
}
```

---

## Kaynaklar
- https://pub.dev/packages/flame (current version `1.37.0` and install snippet)
- https://docs.flame-engine.org/latest/flame/game.html (FlameGame, game loop, world/camera, lifecycle order, pause/resume, cleanup)
- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/structure.md (recommended asset folder structure & pubspec registration)
- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/flame.md (Flame overview / module list)
