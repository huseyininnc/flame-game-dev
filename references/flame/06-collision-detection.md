# Flame Collision Detection

Flame ships with a standard sweep-and-prune collision system built around hitboxes attached to components. This document covers enabling detection, reacting to collisions, hitbox shapes, collision types, and the quad-tree broadphase for large worlds.

> Verified against **flame 1.37.0**.

## Enabling collision detection

Add the `HasCollisionDetection` mixin to your `FlameGame` (or to a `World`). Hitboxes connect to the **closest parent** that has this mixin, so if you attach it to a `World`, hitboxes inside that world report there rather than to the game.

```dart
import 'package:flame/collisions.dart';
import 'package:flame/game.dart';

class MyGame extends FlameGame with HasCollisionDetection {
  @override
  Future<void> onLoad() async {
    add(ScreenHitbox());
    add(Player());
    add(Enemy());
  }
}
```

`ScreenHitbox` is a hitbox that matches the edges of the visible area, so components can detect when they reach the screen boundary.

## Reacting to collisions: `CollisionCallbacks`

Add the `CollisionCallbacks` mixin to any component that needs to know about collisions. It exposes three overridable methods:

- `onCollisionStart` — called once when two hitboxes begin overlapping.
- `onCollision` — called every tick while they keep overlapping.
- `onCollisionEnd` — called once when they stop overlapping.

```dart
import 'package:flame/collisions.dart';
import 'package:flame/components.dart';
import 'package:flutter/material.dart';

class Player extends PositionComponent with CollisionCallbacks {
  Player() : super(size: Vector2.all(48), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    add(RectangleHitbox());
  }

  @override
  void onCollisionStart(
    Set<Vector2> intersectionPoints,
    PositionComponent other,
  ) {
    super.onCollisionStart(intersectionPoints, other);
    if (other is Enemy) {
      debugColor = Colors.red;
    } else if (other is ScreenHitbox) {
      // hit the edge of the screen
    }
  }

  @override
  void onCollision(Set<Vector2> intersectionPoints, PositionComponent other) {
    super.onCollision(intersectionPoints, other);
  }

  @override
  void onCollisionEnd(PositionComponent other) {
    super.onCollisionEnd(other);
    if (other is Enemy) {
      debugColor = Colors.green;
    }
  }
}
```

`intersectionPoints` is the set of world-space points where the two hitboxes overlap. `other` is the `PositionComponent` that owns the colliding hitbox (Flame walks up to the parent component, controlled by `triggersParentCollision`, default `true`).

You can also implement the callbacks directly on a hitbox instead of the parent component if you want per-hitbox handling.

## Hitbox shapes

Flame provides three concrete hitbox shapes, all subclasses of `ShapeHitbox`:

| Hitbox | Shape | Notes |
|---|---|---|
| `RectangleHitbox` | Axis-aligned (relative to parent) rectangle | Cheapest; defaults to parent size |
| `CircleHitbox` | Circle | Cheap radial test |
| `PolygonHitbox` | Arbitrary polygon | **Must be convex** for correct results |

```dart
import 'package:flame/collisions.dart';
import 'package:flame/components.dart';

class Enemy extends PositionComponent with CollisionCallbacks {
  Enemy() : super(size: Vector2.all(64), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    add(
      RectangleHitbox(
        size: Vector2(40, 50),
        position: Vector2(12, 7),
      ),
    );
  }
}

class Coin extends PositionComponent with CollisionCallbacks {
  Coin() : super(size: Vector2.all(32), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    add(CircleHitbox());
  }
}
```

`RectangleHitbox` has two convenience constructors that derive their shape from the parent's bounding box:

```dart
add(RectangleHitbox.relative(Vector2.all(0.8), parentSize: size));
```

A `PolygonHitbox` is defined either by explicit vertices or relative to the parent size:

```dart
add(
  PolygonHitbox([
    Vector2(0, 0),
    Vector2(64, 0),
    Vector2(64, 32),
    Vector2(32, 64),
    Vector2(0, 32),
  ]),
);

add(
  PolygonHitbox.relative(
    [
      Vector2(0.0, -1.0),
      Vector2(1.0, 0.0),
      Vector2(0.0, 1.0),
      Vector2(-1.0, 0.0),
    ],
    parentSize: size,
  ),
);
```

### Combining hitboxes

A single component can carry multiple hitboxes. To make a group of hitboxes act as one logical collision object, wrap them in a `CompositeHitbox`.

## `CollisionType` — performance tuning

Every hitbox has a `collisionType` (the `CollisionType` enum). It controls which hitboxes are checked against which, and it is the primary performance lever.

| Value | Behavior |
|---|---|
| `CollisionType.active` | Collides with other `active` **and** `passive` hitboxes |
| `CollisionType.passive` | Collides only with `active` hitboxes (never with other `passive`) |
| `CollisionType.inactive` | Skipped entirely — no collision checks |

The default is `active`. The rule of thumb: things that move and need to react (player, projectiles) should be `active`; large static objects that only need to *be* hit (walls, pickups, terrain) should be `passive`; temporarily-disabled hitboxes should be `inactive`.

```dart
class Wall extends PositionComponent with CollisionCallbacks {
  @override
  Future<void> onLoad() async {
    add(RectangleHitbox(collisionType: CollisionType.passive));
  }
}

class Bullet extends PositionComponent with CollisionCallbacks {
  final RectangleHitbox _hitbox = RectangleHitbox();

  @override
  Future<void> onLoad() async {
    add(_hitbox);
  }

  void deactivate() => _hitbox.collisionType = CollisionType.inactive;
}
```

Because two `passive` hitboxes never test against each other, marking the bulk of your static scenery as `passive` removes a large number of pairwise checks.

## Quad-tree broadphase for many static bodies

The default broadphase is fine for a few hundred hitboxes. For large maps with many static collidables, swap to the quad-tree broadphase by using `HasQuadTreeCollisionDetection` and initializing it in `onLoad`:

```dart
import 'dart:ui';
import 'package:flame/collisions.dart';
import 'package:flame/game.dart';

class MyGame extends FlameGame with HasQuadTreeCollisionDetection {
  @override
  Future<void> onLoad() async {
    initializeCollisionDetection(
      mapDimensions: const Rect.fromLTWH(0, 0, mapWidth, mapHeight),
      minimumDistance: 10,
    );
    // add components...
  }
}
```

- `mapDimensions` — the world rectangle the quad tree covers.
- `minimumDistance` — optional minimum distance below which the broadphase skips precise checks.

To filter which component types are even considered against each other (a big optimization), override `onComponentTypeCheck` on the colliding components:

```dart
class Ball extends PositionComponent with CollisionCallbacks {
  @override
  bool onComponentTypeCheck(PositionComponent other) {
    if (other is Player || other is Wall) {
      return false; // never collide with these
    }
    return super.onComponentTypeCheck(other);
  }
}
```

Periodically call `QuadTree.optimize()` (via `collisionDetection.broadphase.tree.optimize()`) to prune empty quadrants as bodies move around.

> Caveat: the quad-tree broadphase can be **slower** than the default for some workloads. Profile both before committing to it.

## Ray casting and ray tracing

The collision detection system also supports rays, useful for line-of-sight, bullets, and reflections:

```dart
final ray = Ray2(origin: Vector2(0, 0), direction: Vector2(1, 0)..normalize());
final result = collisionDetection.raycast(ray);

final results = collisionDetection.raycastAll(
  Vector2(0, 0),
  numberOfRays: 360,
);

final reflections = collisionDetection.raytrace(ray, maxDepth: 10);
```

- `raycast` returns the first hit along a single ray.
- `raycastAll` casts rays in all directions from a point (useful for visibility/lighting).
- `raytrace` follows a ray and computes successive reflections off hitboxes.

## Kaynaklar

- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/collision_detection.md
- https://docs.flame-engine.org/latest/
