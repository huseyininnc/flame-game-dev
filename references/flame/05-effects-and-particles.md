# Flame: Effects and Particles

This document covers Flame's effect system (`Effect`, `EffectController`, and concrete effects) along with the particle system.

## 1. Effect Basics

An effect is a special component that, when attached to another component, changes its properties or appearance over time. The abstract `Effect` class provides the common functionality:

- **Pause/resume:** `effect.pause()`, `effect.resume()`, state: `effect.isPaused`
- **Auto-removal:** `removeOnFinish` (defaults to `true`) removes the effect component when it finishes
- **Completion callback:** the optional `onComplete` runs when the effect finishes (before removal)
- **Completion future:** the `completed` future resolves when the effect finishes
- **Reset:** `reset()` returns to the initial state for reuse

## 2. EffectController

`EffectController` defines how the effect progresses over time. Standard factory constructor parameters:

- `duration` (required): the 0→100% progress duration (seconds)
- `curve`: nonlinear progression (defaults to `Curves.linear`)
- `reverseDuration`: the reverse-phase duration (100%→0)
- `reverseCurve`: the reverse-phase curve (defaults to `curve.flipped`)
- `alternate`: a boolean equivalent to `reverseDuration == duration`
- `atMaxDuration`: the hold time at 100%
- `atMinDuration`: the hold time at 0%
- `repeatCount`: the number of repeats
- `infinite`: an infinite-repeat boolean
- `startDelay`: the wait time before starting
- `onMax` / `onMin`: callbacks at maximum/minimum progress

```dart
EffectController(
  duration: 0.75,
  reverseDuration: 0.5,
  curve: Curves.easeInOut,
  alternate: true,
  repeatCount: 3,
  startDelay: 0.2,
);
```

### Specialized controllers

| Controller | Purpose |
|---|---|
| `LinearEffectController(duration)` | Linear 0→1 |
| `ReverseLinearEffectController(duration)` | Linear 1→0 |
| `CurvedEffectController(duration, curve)` | Curved 0→1 |
| `ReverseCurvedEffectController(duration, curve)` | Curved 1→0 |
| `PauseEffectController(duration, progress)` | Constant progress |
| `RepeatedEffectController(child, count)` | Repeats the child N times |
| `InfiniteEffectController(child)` | Repeats the child infinitely |
| `SequenceEffectController([...])` | Chains controllers in sequence |
| `SpeedEffectController(child, speed)` | Sets the duration based on speed |
| `DelayedEffectController(child, delay)` | Delays the child |
| `ZigzagEffectController(period)` | 0→1→-1→0 oscillation |
| `SineEffectController(period)` | A single sine period |
| `NoiseEffectController(duration, frequency)` | Random oscillation |
| `RandomEffectController.uniform(child, min, max)` | Random-duration wrapper |

## 3. Move Effects

`MoveEffect.by` (relative) and `MoveEffect.to` (absolute). The underlying classes are `MoveByEffect` and `MoveToEffect`.

```dart
// Shift relative to the current position
final moveBy = MoveEffect.by(
  Vector2(30, 30),
  EffectController(duration: 1.0),
);

// Go to a specific target
final moveTo = MoveEffect.to(
  Vector2(100, 500),
  EffectController(duration: 3),
);
```

### MoveAlongPathEffect

Moves the component along the specified path. `absolute: true` uses absolute canvas coordinates; `oriented: true` rotates the target to follow the path.

```dart
final pathEffect = MoveAlongPathEffect(
  Path()..quadraticBezierTo(100, 0, 50, -50),
  EffectController(duration: 1.5),
  oriented: true,
);
```

## 4. Scale Effects

`ScaleEffect.by` (relative), `ScaleEffect.to` (absolute). Scale affects all child components (size affects only the parent's dimensions).

```dart
// Grow by 50%
final scaleBy = ScaleEffect.by(
  Vector2.all(1.5),
  EffectController(duration: 0.3),
);

// Set to an absolute scale
final scaleTo = ScaleEffect.to(
  Vector2.all(0.5),
  EffectController(duration: 0.5),
);
```

## 5. Rotate Effects

The angle is in **radians** (`tau/4` = 90°). Direction reference: 0º = north, tau/4 = east.

```dart
final rotateBy = RotateEffect.by(
  tau / 4,
  EffectController(duration: 2),
);

final rotateTo = RotateEffect.to(
  tau / 4,
  EffectController(duration: 2),
);
```

## 6. Opacity and Color Effects

`OpacityEffect` can only be applied to components that implement the `OpacityProvider` interface. The `HasPaint` mixin implements `OpacityProvider`. Opacity 0 = fully transparent, 1 = fully opaque.

`OpacityEffect.to(double, controller)`, `OpacityEffect.fadeOut(controller)` (to full transparency), and `OpacityEffect.fadeIn(controller)` (to full visibility).

```dart
class MyComponent extends SpriteComponent with HasPaint {
  MyComponent(Sprite sprite) : super(sprite: sprite);
}

final fadeIn = OpacityEffect.fadeIn(EffectController(duration: 1.5));
final fadeOut = OpacityEffect.fadeOut(EffectController(duration: 0.5));
final toHalf = OpacityEffect.to(0.5, EffectController(duration: 0.75));
```

### ColorEffect

Tints the component with a color. **Note:** Due to Flutter's `ColorFilter` structure, multiple `ColorEffect`s cannot be used together; only the last one takes effect.

```dart
final colorEffect = ColorEffect(
  const Color(0xFF00FF00),
  EffectController(duration: 1.5),
  opacityFrom: 0.2,
  opacityTo: 0.8,
);
```

## 7. SequenceEffect

Runs multiple effects in sequence. The constituent effects can be of different types. `alternate: true` (on the controller) runs it back and forth; repetition is controlled with `repeatCount` or `infinite`.

```dart
final effect = SequenceEffect([
  ScaleEffect.by(
    Vector2.all(1.5),
    EffectController(duration: 0.2, alternate: true),
  ),
  MoveEffect.by(
    Vector2(30, -50),
    EffectController(duration: 0.5),
  ),
  OpacityEffect.to(
    0,
    EffectController(duration: 0.3),
  ),
  RemoveEffect(),
]);

add(effect);
```

Listening for the effect to complete:

```dart
final effect = MoveEffect.by(
  Vector2(0, -100),
  EffectController(duration: 1.0),
  onComplete: () => print('move complete'),
);
add(effect);
await effect.completed;
```

## 8. Particle System

The particle system revolves around the `Particle` class. `ParticleSystemComponent` maps the Component lifecycle hooks onto the Particle and removes the component when it finishes.

```dart
import 'package:flame/components.dart';

game.add(
  ParticleSystemComponent(
    particle: CircleParticle(),
  ),
);
```

### Particle.generate

Generates multiple particle instances.

```dart
final rnd = Random();
Vector2 randomVector2() => (Vector2.random(rnd) - Vector2.random(rnd)) * 200;

game.add(
  ParticleSystemComponent(
    particle: Particle.generate(
      count: 10,
      generator: (i) => AcceleratedParticle(
        acceleration: randomVector2(),
        child: CircleParticle(
          paint: Paint()..color = Colors.red,
        ),
      ),
    ),
  ),
);
```

### Lifespan

All particles take a `lifespan` in seconds (microsecond precision). `setLifespan()` resets it, and the `progress` getter tracks the lifetime in the range 0.0–1.0.

```dart
final particle = CircleParticle()..setLifespan(2); // 2 seconds
```

### Common particle types

```dart
// Translates to a fixed position (without changing the position)
TranslatedParticle(offset: game.size / 2, child: Particle());

// Moves between from -> to
MovingParticle(
  from: Vector2.zero(),
  to: game.size,
  child: CircleParticle(radius: 2.0, paint: Paint()..color = Colors.red),
);

// Physics-based (position, speed, acceleration -> logical px/s)
AcceleratedParticle(
  position: game.canvasSize / 2,
  speed: Vector2(rnd.nextDouble() * 200 - 100, -rnd.nextDouble() * 100),
  child: CircleParticle(radius: 2.0, paint: Paint()..color = Colors.red),
);

// Draws a circle
CircleParticle(
  radius: game.size.x / 2,
  paint: Paint()..color = Colors.red.withValues(alpha: .5),
);

// Scales between 1 -> to
ScalingParticle(
  lifespan: 2,
  to: 0,
  curve: Curves.easeIn,
  child: CircleParticle(radius: 2.0, paint: Paint()..color = Colors.red),
);

// Embeds a sprite
SpriteParticle(sprite: mySprite, size: Vector2(64, 64));

// Embeds a dart:ui Image
ImageParticle(size: Vector2.all(24), image: image);

// Plays a SpriteAnimation
SpriteAnimationParticle(
  animation: spriteSheet.createAnimation(0, stepTime: 0.1),
);

// Embeds a Component (with its own update/render)
ComponentParticle(component: longLivingRect);
```

### ComputedParticle

For fully custom rendering. Time-based interpolation is done via `progress`.

```dart
game.add(
  ParticleSystemComponent(
    particle: ComputedParticle(
      renderer: (canvas, particle) => canvas.drawCircle(
        Offset.zero,
        particle.progress * 10,
        Paint()
          ..color = Color.lerp(Colors.red, Colors.blue, particle.progress)!,
      ),
    ),
  ),
);
```

### Composition and nesting

Flame uses composition similar to Flutter widgets. For custom particles, use the `SingleChildParticle` mixin; for combining multiple behaviors, use `ComposedParticle`.

```dart
final rnd = Random();

class GlitchParticle extends Particle with SingleChildParticle {
  @override
  final Particle child;

  GlitchParticle({required this.child, super.lifespan});

  @override
  void render(Canvas canvas) {
    canvas.save();
    canvas.translate(rnd.nextDouble() * 100, rnd.nextDouble() * 100);
    super.render(canvas);
    canvas.restore();
  }
}
```

## Resources

- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/effects/effects.md
- https://docs.flame-engine.org/latest/flame/effects/move_effects.html
- https://docs.flame-engine.org/latest/flame/effects/scale_effects.html
- https://docs.flame-engine.org/latest/flame/effects/rotate_effects.html
- https://docs.flame-engine.org/latest/flame/effects/sequence_effect.html
- https://docs.flame-engine.org/latest/flame/effects/effect_controllers.html
- https://docs.flame-engine.org/latest/flame/effects/color_effects.html
- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/rendering/particles.md
