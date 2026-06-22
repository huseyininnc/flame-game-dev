# Flame Camera, World, and Viewport

The modern Flame camera is `CameraComponent`. It renders a `World` through a **viewport** (the on-screen window) and a **viewfinder** (the in-world position/zoom/rotation). Multiple cameras can observe the same world simultaneously.

> Verified against **flame 1.37.0**.

## The mental model

- **`World`** — hosts every component that belongs to the game world (the player, enemies, terrain). The world itself is not rendered directly; a camera observes it.
- **`CameraComponent`** — looks at a `World` and draws it.
- **`viewport`** — the rectangular region of the screen the camera draws into. Components added to the *viewport* are screen-fixed → this is how you build a **HUD**.
- **`viewfinder`** — where in the world the camera is looking, plus `zoom`, `angle`, and `anchor`.

```dart
import 'package:flame/camera.dart';
import 'package:flame/components.dart';
import 'package:flame/game.dart';

class MyGame extends FlameGame {
  late final World world;
  late final CameraComponent camera;

  @override
  Future<void> onLoad() async {
    world = World();
    camera = CameraComponent(world: world);
    addAll([world, camera]);

    final player = Player();
    world.add(player);

    camera.follow(player);
  }
}
```

`FlameGame` already exposes a default `world` and `camera`, so for simple games you can use `world.add(...)` and `camera.follow(...)` without constructing them yourself. Construct them explicitly when you need custom viewports or multiple cameras.

## World vs. viewport (HUD)

```dart
// In-world content — moves with the camera, affected by zoom/pan:
world.add(Player());
world.add(EnemySpawner());

// HUD content — fixed to the screen, NOT affected by camera movement/zoom:
camera.viewport.add(ScoreText());
camera.viewport.add(JoystickComponent(...));
```

Anything added to `camera.viewport` stays put on screen while the world scrolls beneath it — the canonical way to render a HUD in modern Flame.

## Viewport types

You set the viewport via the `CameraComponent` constructor (or `CameraComponent.withFixedResolution`).

| Viewport | Behavior |
|---|---|
| `MaxViewport` (default) | Expands to the full size allowed by the game canvas |
| `FixedResolutionViewport` | Locks resolution + aspect ratio, letterboxing with black bars |
| `FixedSizeViewport` | A rectangle of a fixed pixel size |
| `FixedAspectRatioViewport` | Grows to fit the canvas while preserving an aspect ratio |
| `CircularViewport` | A fixed-size circular window |

```dart
final camera = CameraComponent(
  world: world,
  viewport: FixedResolutionViewport(resolution: Vector2(640, 360)),
);
```

### Fixed-resolution layout across screen sizes

For a consistent layout regardless of device size, use the convenience constructor. It sets up a `FixedResolutionViewport` and a matching viewfinder so one logical resolution maps onto any screen (with letterboxing):

```dart
final camera = CameraComponent.withFixedResolution(
  world: world,
  width: 640,
  height: 360,
);
```

Everything you position in the world is now in a 640×360 coordinate space; Flame scales and letterboxes it to fit the actual screen.

## Following a target, bounds, and manual moves

```dart
// Follow the player. maxSpeed limits how fast the camera catches up;
// snap jumps instantly to the target on the first frame.
camera.follow(player, maxSpeed: 250, snap: true);

// Stop following and move manually:
camera.stop();
camera.moveTo(Vector2(500, 300), speed: 200);

// Constrain where the camera can go (e.g. to the map rectangle):
camera.setBounds(
  Rectangle.fromLTRB(0, 0, mapWidth, mapHeight),
);
```

- `follow(target, {maxSpeed, snap, horizontalOnly, verticalOnly})` — keep the viewfinder locked onto a component.
- `moveTo(point, {speed})` — glide the camera to a world point.
- `setBounds(shape)` — restrict the viewfinder so it cannot show beyond the given `Shape` (commonly a `Rectangle`). Pass `null` to clear bounds.

## Zoom and anchor (the viewfinder)

Zoom, rotation, and the "logical center" all live on the viewfinder:

```dart
// Zoom in 2x (larger value = more zoomed in):
camera.viewfinder.zoom = 2.0;

// Rotate the view (radians):
camera.viewfinder.angle = 0;

// Which point of the viewport is the logical center the camera aims at.
// Default is Anchor.center; use topLeft for a "screen origin" feel.
camera.viewfinder.anchor = Anchor.center;
```

Animating zoom can be done by tweening `viewfinder.zoom` over time in `update`, or with an effect attached to the viewfinder.

## Putting it together

```dart
import 'package:flame/camera.dart';
import 'package:flame/components.dart';
import 'package:flame/game.dart';

class PlatformerGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    final gameWorld = World();
    final cam = CameraComponent.withFixedResolution(
      world: gameWorld,
      width: 480,
      height: 270,
    );
    addAll([gameWorld, cam]);

    final player = Player()..position = Vector2(100, 100);
    gameWorld.add(player);
    gameWorld.add(Level());

    cam.viewfinder.zoom = 1.0;
    cam.follow(player, maxSpeed: 300);
    cam.setBounds(Rectangle.fromLTRB(0, 0, 2000, 270));

    cam.viewport.add(HudScore());
  }
}
```

## Kaynaklar

- https://docs.flame-engine.org/latest/flame/camera_component.html
- https://docs.flame-engine.org/latest/
- https://pub.dev/packages/flame (flame 1.37.0)
