# Flame Engine — Components & Lifecycle

The **Flame Component System (FCS)** is the heart of the engine. Everything in a Flame game is a `Component` arranged in a tree whose root is the `FlameGame`. Components encapsulate their own state, update logic, and rendering, and they can contain child components. This is Flame's take on a node/entity tree — comparable to Flutter's widget tree, but for game objects.

This document covers the component classes, the parent/child tree, the full lifecycle, and the key mixins.

---

## 4. Components & `PositionComponent`

### `Component`

`Component` is the base class for everything in the tree. A bare `Component` has no position or visual representation — it is a logical container or a behavior. You subclass it and override lifecycle methods (`onLoad`, `update`, `render`, …) to give it behavior.

### `PositionComponent`

`PositionComponent` is the most commonly used base class. The API docs describe it as "a `Component` implementation that represents an object that can be freely moved around the screen, rotated, and scaled." It has no inherent appearance, but it owns the spatial properties that nearly every visible object needs, and it is the parent class of `SpriteComponent`, `SpriteAnimationComponent`, `RectangleComponent`, `TextComponent`, and most other rendered components.

Constructor parameters (all optional):

```dart
PositionComponent({
  Vector2? position,
  Vector2? size,
  Vector2? scale,
  double? angle,
  double nativeAngle = 0,
  Anchor? anchor,
  int? priority,
  Iterable<Component>? children,
  ComponentKey? key,
});
```

Key spatial properties:

| Property | Type | Meaning |
|---|---|---|
| `position` | `Vector2` | Position of the component's **anchor** in the parent's coordinate space. |
| `size` | `Vector2` | Logical width/height; also used for collision detection and `containsPoint`. |
| `scale` | `Vector2` | Scale factor along x and y. |
| `angle` | `double` | Rotation in **radians**; positive is clockwise. |
| `nativeAngle` | `double` | The orientation the art is drawn at (0 = pointing up/north); used so `angle`/`lookAt` line up with the sprite. |
| `anchor` | `Anchor` | The reference point used both for `position` and for rotation/scaling. Defaults to `Anchor.topLeft`. |
| `priority` | `int` | Render/iteration order among siblings; higher priority is rendered last (on top). |

```dart
class Player extends PositionComponent {
  Player()
      : super(
          position: Vector2(100, 200),
          size: Vector2(48, 48),
          anchor: Anchor.center, // position & rotation now refer to the center
          priority: 1,
        );

  @override
  void update(double dt) {
    super.update(dt);
    angle += 0.5 * dt;        // rotate half a radian per second
    position.x += 20 * dt;    // move 20 logical px/second to the right
  }
}
```

The `anchor` choice matters: with `Anchor.topLeft` (the default), `position` is the top-left corner; with `Anchor.center`, the same `position` value refers to the component's center, and rotation pivots around the center. Useful methods include `toRect()` (bounding rectangle) and `containsPoint(Vector2)` / `containsLocalPoint(Vector2)` for hit-testing.

### The parent/child tree

Components form a tree. Each component exposes its `parent`, its read-only `children` set, and helpers like `ancestors()`. Adding and removing is done through these methods:

```dart
// Add a single child (returns a Future you can await until it's mounted/loaded)
await add(Enemy());

// Add many children at once
addAll([Enemy(), Coin(), Coin()]);

// Pass children directly via the constructor
final hud = PositionComponent(children: [ScoreLabel(), HealthBar()]);

// Remove a specific child
remove(enemy);

// Remove this component from whatever its parent is
enemy.removeFromParent();
```

`add` and `remove` are **scheduled**, not immediate: the child is queued and actually inserted/removed at the start of the next game tick (so the tree is never mutated mid-frame). The returned `Future` completes once the child is fully loaded and mounted. You can inspect `component.isLoaded` and `component.isMounted` to know its state, and `changeParent(newParent)` to reparent without a full remove/add cycle.

---

## 5. The full component lifecycle

The methods below fire in a well-defined order. For a regular `Component`, the **first-time** order when it is added to the tree is:

```
onLoad  →  onGameResize  →  onMount  →  (per frame: update → render)*  →  onRemove
```

(Recall from the setup doc that `FlameGame` reverses the first two: `onGameResize` before `onLoad`.)

| Method | Signature | When it fires |
|---|---|---|
| `onLoad` | `FutureOr<void> onLoad()` | **Once**, the first time the component is added to the tree. The async "constructor" — load sprites, build children here. Awaited before the component is mounted. |
| `onGameResize` | `void onGameResize(Vector2 size)` | When the game surface size changes — and also once when the component is (re-)added, after `onLoad`. Propagated to the whole subtree. |
| `onMount` | `void onMount()` | After loading completes and the parent is itself mounted. Runs **again** if the component is removed and re-added (possibly to a different parent). Good for setup that depends on having a live parent. |
| `update` | `void update(double dt)` | Every tick while the component is mounted, with `dt` in seconds. |
| `render` | `void render(Canvas canvas)` | Every tick, after all components have finished `update`. Draw here. |
| `onRemove` | `void onRemove()` | Right before the component is removed from its parent (and before a parent change). Use for cleanup. |
| `onChildrenChanged` | `void onChildrenChanged(Component child, ChildrenChangeType type)` | When a child is added to or removed from this component's `children`. `type` distinguishes added vs. removed. |

```dart
class Enemy extends PositionComponent {
  late final Sprite _sprite;

  @override
  Future<void> onLoad() async {
    _sprite = await Sprite.load('enemy.png');
  }

  @override
  void onMount() {
    super.onMount();
    // parent is now guaranteed live; e.g. register with a manager
  }

  @override
  void update(double dt) {
    super.update(dt);
    position.x -= 60 * dt;
    if (position.x < -size.x) removeFromParent();
  }

  @override
  void render(Canvas canvas) {
    _sprite.render(canvas, size: size);
  }

  @override
  void onRemove() {
    super.onRemove();
    // release references, stop sounds, etc.
  }

  @override
  void onChildrenChanged(Component child, ChildrenChangeType type) {
    super.onChildrenChanged(child, type);
    // react to a child being added/removed
  }
}
```

**Re-adding semantics:** `onLoad` is the only one of these that is guaranteed to run a single time. If you remove a component and add it again, `onGameResize`, `onMount`, and the loop callbacks all run again, but `onLoad` does **not** repeat (its loaded state is preserved). Always call `super` in lifecycle overrides so the framework can propagate the call to children.

---

## 6. Key mixins & accessing the game

Mixins add cross-cutting capabilities to a component without changing its base class.

### `HasGameReference<T extends FlameGame>` — reach the game

This mixin adds a type-safe `game` getter that points to the `FlameGame` at the top of the tree. It is the recommended way to access the game from any component.

```dart
class ScoreLabel extends TextComponent with HasGameReference<MyGame> {
  @override
  void update(double dt) {
    super.update(dt);
    text = 'Score: ${game.score}'; // strongly typed access to MyGame
  }
}
```

> **Deprecation note:** The older `HasGameRef` mixin (with a `gameRef` getter) is **deprecated** in favor of `HasGameReference` (with a `game` getter). Use `HasGameReference` in new code. There is also a `findGame()` method on every component for the rare case where you need the game without the mixin (it returns a nullable, untyped game).

### `HasWorldReference<T extends World>` — reach the world

When a component needs to talk to the `World` ancestor it lives in, add this mixin to get a type-safe `world` getter:

```dart
class Spawner extends Component with HasWorldReference<MyWorld> {
  void spawnEnemy() => world.add(Enemy());
}
```

### `HasVisibility` — toggle rendering

Adds an `isVisible` flag. When `isVisible` is `false`, the component is **not rendered**, but it remains in the tree and **still receives `update` and all other lifecycle events**. This is for hiding something temporarily without removing it.

```dart
class Shield extends PositionComponent with HasVisibility {
  void activate()   => isVisible = true;
  void deactivate() => isVisible = false; // hidden but still updating
}
```

### `HasPaint<T>` — manage paints, opacity & tint

Adds "a collection of paints and paint layers to a component," giving you opacity, color, and tint control out of the box. `SpriteComponent` and friends already mix this in. Key members:

- `paint` — the main `Paint` object (getter/setter).
- `getPaint(id)` / `setColor(color, paintId)` — manage named paints (the generic `T` identifies them).
- `opacity` (getter/setter) and `setOpacity(double)` — transparency in the `0.0`–`1.0` range.
- `makeTransparent()` / `makeOpaque()` — fully hide / fully show.
- `tint(Color)` — apply a color filter overlay (e.g. flash red when hit).

```dart
class Hero extends SpriteComponent with HasPaint {
  void takeDamage() {
    tint(const Color(0xFFFF0000)); // flash red
  }

  void fadeOut() {
    opacity = 0.3; // 70% transparent
  }
}
```

> `HasPaint` controls *how* a component is painted (alpha, color, filters); `HasVisibility` controls *whether* it is painted at all. They compose cleanly.

---

## Kaynaklar
- https://pub.dev/documentation/flame/latest/components/Component-class.html (lifecycle method signatures, add/addAll/remove, parent/children/isMounted/isLoaded/priority)
- https://pub.dev/documentation/flame/latest/components/PositionComponent-class.html (PositionComponent constructor & properties, default anchor)
- https://pub.dev/documentation/flame/latest/components/HasGameRef-mixin.html (HasGameReference vs deprecated HasGameRef)
- https://pub.dev/documentation/flame/latest/components/HasPaint-mixin.html (HasPaint members)
- https://docs.flame-engine.org/latest/flame/components.html (FCS overview, HasVisibility / HasWorldReference behavior)
