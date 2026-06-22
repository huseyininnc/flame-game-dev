# Flame: 60 FPS Performance Optimization

Repeatable performance rules so that, when producing many small games, each one runs smoothly (target **60 FPS**). The APIs below are verified against the Flame source.

---

## 1. Preload assets inside `onLoad`

Loading images/audio while the game is running (during `update`/`render`) causes frame drops. Preload all images and audio inside `onLoad`, before the game starts.

```dart
class MyGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    await images.loadAll([
      'player.png',
      'enemy.png',
      'background.png',
    ]);

    await FlameAudio.audioCache.loadAll([
      'jump.wav',
      'hit.wav',
      'bgm.mp3',
    ]);
  }
}
```

This way there is no disk/decode latency at runtime; every frame uses resources already in memory.

---

## 2. Avoid allocation inside `update()`

`update(double dt)` runs ~60 times per second. Creating a new object (`Vector2`, list, closure) every frame triggers the garbage collector and causes jank. Create objects **once** and reuse them.

```dart
class Player extends PositionComponent {
  // Allocate once instead of recreating every frame.
  final Vector2 _velocity = Vector2.zero();

  @override
  void update(double dt) {
    super.update(dt);
    // BAD:  position += Vector2(0, speed * dt);   // a new Vector2 every frame
    // GOOD:
    _velocity.setValues(0, speed);
    position.addScaled(_velocity, dt);
  }
}
```

Prefer *in-place* methods on `Vector2` such as `setValues`, `add`, `addScaled`, and `scale`; operators (`+`, `*`) produce new objects.

---

## 3. Object pooling: avoid add/remove churn

For objects that are created and destroyed frequently, such as bullets, particles, and enemies, the `add()`/`removeFromParent()` cycle creates both GC pressure and the cost of restructuring the component tree. Instead, **reuse from a pool**: rather than destroying the object, deactivate it (e.g. move it off-screen without calling `removeFromParent`) and reactivate it later.

```dart
class BulletPool {
  BulletPool(this._world, {int size = 64})
      : _pool = List.generate(size, (_) => Bullet()..deactivate());

  final World _world;
  final List<Bullet> _pool;

  Bullet? acquire(Vector2 position, Vector2 direction) {
    final bullet = _pool.cast<Bullet?>().firstWhere(
          (b) => b != null && !b.isActive,
          orElse: () => null,
        );
    if (bullet == null) return null;
    bullet.activate(position, direction);
    if (bullet.parent == null) _world.add(bullet);
    return bullet;
  }
}
```

The key idea: instead of removing the object from the component tree, deactivate it with an `isActive` flag and reuse it. This zeroes out allocation in the hot path.

### 3.1 Built-in recycling with `RecycledQueue`

For the same purpose, Flame offers a built-in `RecycledQueue<T extends Disposable>`: a FIFO queue that **creates and owns** its elements, and that, instead of destroying an element when it leaves the queue, `dispose`s it and returns it to the reuse pool. When a new element is added, previously disposed elements are reused.

```dart
class Particle implements Disposable {
  double x = 0, y = 0, life = 0;

  @override
  void dispose() {
    life = 0;
  }
}

final particles = RecycledQueue<Particle>(Particle.new, initialCapacity: 128);

void spawn(double px, double py) {
  // addLast produces a new (or recycled) element; filling it is up to you.
  final p = particles.addLast()
    ..x = px
    ..y = py
    ..life = 1.0;
}

void tick(double dt) {
  for (final p in particles) {
    p.life -= dt;
    if (p.life <= 0) {
      particles.removeCurrent(); // safe during iteration
    }
  }
}
```

> The `RecycledQueue` API differs from a classic Queue: `addLast` produces a new element and hands it back for you to fill; `removeFirst` deletes the first element **without returning it** (get it beforehand with `first`). It can be modified during iteration with `removeCurrent` and `addLast`; only one iterator is supported at a time.

---

## 4. `HasQuadTreeCollisionDetection` for many static bodies

In large game areas with many collidable objects (hundreds of them, especially static bodies), the default sweep-and-prune slows down. In that case, use `HasQuadTreeCollisionDetection` instead of the standard `HasCollisionDetection`, and initialize it.

```dart
class MyGame extends FlameGame with HasQuadTreeCollisionDetection {
  @override
  void onLoad() {
    initializeCollisionDetection(
      mapDimensions: const Rect.fromLTWH(0, 0, mapWidth, mapHeight),
      minimumDistance: 10,
    );
  }
}
```

`initializeCollisionDetection` parameters:

- **`mapDimensions`** (required): The spatial bounds of the quad tree (`Rect`).
- **`minimumDistance`** (opt.): Minimum distance before a collision check; `null` (default) disables the check.
- **`maxObjects`** (opt., default 25): Maximum objects per quadrant.
- **`maxDepth`** (opt., default 10): Quadrant nesting depth.

On hitboxes, you can override `onComponentTypeCheck` to eliminate incompatible types before the collision check (additional speedup).

> The Flame documentation warns: "Always try out different approaches and measure how they perform in your game. Do not assume that the more sophisticated approach will always be faster." In games with few objects, the default algorithm may be faster.

---

## 5. Avoiding idle work with `pauseEngine` / `resumeEngine`

When the game is paused or a Flutter overlay/dialog is open, stopping the `update` loop saves both CPU/GPU and battery.

```dart
class MyGame extends FlameGame {
  void openPauseMenu() {
    pauseEngine();              // stops the update/render loop
    overlays.add('PauseMenu');
  }

  void closePauseMenu() {
    overlays.remove('PauseMenu');
    resumeEngine();
  }
}
```

The state can be read with the `paused` getter; it can also be set with `paused = true/false`. During a pause, Flutter overlays remain interactive.

---

## 6. FPS measurement: `FpsTextComponent` and `debugMode`

Verify optimization **by measuring**. Flame offers `FpsTextComponent`, which shows the instantaneous FPS on screen (`FpsComponent` is the compute-only version).

```dart
class MyGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    add(
      FpsTextComponent(
        position: Vector2(8, 8),
      ),
    );
  }
}
```

With `debugMode`, component bounds, anchors, and hitboxes are drawn — for debugging layout/collision problems:

```dart
class MyGame extends FlameGame {
  @override
  bool get debugMode => true;
}
```

You can also set `component.debugMode = true` on a per-component basis. Turn `debugMode` off before release (additional draw cost).

---

## 7. Quick checklist (for each game)

- [ ] All images/audio preloaded with `loadAll` inside `onLoad`.
- [ ] No new `Vector2`/list/closure allocation inside `update()`; in-place methods used.
- [ ] Frequently created objects (bullets, particles) reused via a pool/`RecycledQueue`; no `add`/`remove` churn.
- [ ] If there are hundreds of collidables, `HasQuadTreeCollisionDetection` tried and measured.
- [ ] `pauseEngine()` is called when opening a pause/overlay.
- [ ] 60 FPS verified in development with `FpsTextComponent`; `debugMode = false` in release.

---

## Sources

- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/collision_detection.md
- https://raw.githubusercontent.com/flame-engine/flame/main/packages/flame/lib/src/components/core/recycled_queue.dart
- https://raw.githubusercontent.com/flame-engine/flame/main/packages/flame/lib/src/components/fps_text_component.dart
- https://docs.flame-engine.org/latest/
