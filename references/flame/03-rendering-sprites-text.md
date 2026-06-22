# Flame: Sprite, Image, and Text Rendering

This document covers image loading, `Sprite`, `SpriteComponent`, sprite sheets, animation, and text rendering with Flame (stable 1.x).

## 1. Image Loading

Flame provides an `Images` helper class that loads images from assets and caches them. Images must be located under `assets/images/` and declared in `pubspec.yaml`.

### The Images class and the global cache

```dart
import 'package:flame/cache.dart';

final imagesLoader = Images();
final image = await imagesLoader.load('yourImage.png');
```

`Images` cache management methods: `load`, `loadAll`, `clear`, `clearCache`, `fromCache`, `add`, and the `keys` getter.

Via the global singleton:

```dart
import 'package:flame/flame.dart';
import 'package:flame/sprite.dart';

final image = await Flame.images.load('player.png');
final playerSprite = Sprite(image);
```

### Image management at the game level

The `Game` class holds an `images` instance that automatically clears its cache when the game is removed from the widget tree.

```dart
class MyGame extends FlameGame {
  late Sprite player;

  @override
  Future<void> onLoad() async {
    final playerImage = await images.load('player.png');
    player = Sprite(playerImage);
  }
}
```

To retrieve a cached image during gameplay, use `images.fromCache`:

```dart
@override
Future<void> onLoad() async {
  await images.load('bullet.png');
}

void shoot() {
  final bulletSprite = Sprite(images.fromCache('bullet.png'));
}
```

## 2. Sprite

A `Sprite` represents an image or a region of an image.

```dart
final image = await images.load('player.png');
final player = Sprite(image);
```

### Taking a region from a sprite sheet

`srcPosition` defaults to `(0.0, 0.0)`, and `srcSize` defaults to `null` (the full image size).

```dart
final image = await images.load('player.png');
final playerFrame = Sprite(
  image,
  srcPosition: Vector2(32.0, 0),
  srcSize: Vector2(16.0, 16.0),
);
```

### Render

The `render` method takes a canvas, width, and height; it also has optional `overridePaint` and `bleed` parameters, the latter of which prevents "ghost lines".

```dart
final block = Sprite(await images.load('block.png'));
block.render(canvas, 16.0, 16.0);

// Prevent sprite bleeding (edge overflow)
playerFrame.render(canvas, 16.0, 16.0, bleed: 1.0);
```

## 3. SpriteComponent

`SpriteComponent` is the primary implementation of `PositionComponent` for displaying a static sprite.

Key constructor parameters: `sprite`, `size`, `position` (defaults to `Vector2(0,0)`), `angle` (radians, defaults to `0`), `anchor`, and `bleed` for sprite bleeding.

```dart
@override
Future<void> onLoad() async {
  final sprite = await Sprite.load('player.png');
  final size = Vector2.all(128.0);
  final player = SpriteComponent(size: size, sprite: sprite);

  player.position = Vector2(10, 20);
  player.angle = 0;

  add(player);
}
```

Applying bleeding on the component:

```dart
final spriteComponent = SpriteComponent(
  sprite: sprite,
  size: Vector2.all(16.0),
  bleed: 1.0,
);
```

## 4. SpriteSheet

`SpriteSheet` simplifies extracting sprites and animations from a sprite sheet.

```dart
import 'package:flame/sprite.dart';

final spriteSheet = SpriteSheet(
  image: imageInstance,
  srcSize: Vector2.all(16.0),
);

// Create an animation from a row (row index 0)
final animation = spriteSheet.createAnimation(0, stepTime: 0.1);
```

Extracting a static sprite:

```dart
spriteSheet.getSpriteById(2); // by id
spriteSheet.getSprite(0, 0);  // by row, column
```

## 5. SpriteAnimation

Creates a looping animation from equally sized sprites.

### From a list of sprites

```dart
final animation = SpriteAnimation.spriteList(sprites, stepTime: 0.02);
```

### With frame data (from a sprite sheet)

```dart
const amountOfFrames = 8;
final animation = SpriteAnimation.fromFrameData(
  imageInstance,
  SpriteAnimationData.sequenced(
    amount: amountOfFrames,
    textureSize: Vector2(16.0, 16.0),
    stepTime: 0.1,
  ),
);
```

### SpriteAnimationTicker

`SpriteAnimationTicker` manages the time progression of an animation. It can be used directly when managing your own animation outside of a component.

```dart
class MyGame extends Game {
  late SpriteAnimationTicker ticker;

  MyGame() {
    ticker = SpriteAnimationTicker(SpriteAnimation.spriteList(sprites, stepTime: 0.02));
  }

  @override
  void update(double dt) => ticker.update(dt);

  @override
  void render(Canvas c) => ticker.getSprite().render(c);
}
```

## 6. SpriteAnimationComponent

Displays multi-frame looping animations.

Key constructor parameters:
- `animation`: the `SpriteAnimation` to play
- `size`: Vector2 size
- `autoPlay`: whether to start automatically
- `playing`: the current playback state
- `removeOnFinish`: whether to remove the component when the animation finishes
- `resetOnRemove`: whether to return to the first frame when removed

```dart
@override
Future<void> onLoad() async {
  final sprites = [0, 1, 2].map((i) => Sprite.load('player_$i.png'));
  final animation = SpriteAnimation.spriteList(
    await Future.wait(sprites),
    stepTime: 0.01,
  );
  final player = SpriteAnimationComponent(
    animation: animation,
    size: Vector2.all(64.0),
  );
  add(player);
}
```

### animationTicker and callbacks

The component exposes an internal `SpriteAnimationTicker` through the `animationTicker` property. The ticker provides `onStart`, `onFrame(int index)`, and `onComplete` callbacks, along with a `completed` future.

```dart
final ticker = SpriteAnimationTicker(animation)
  ..onStart = () { /* started */ }
  ..onFrame = (index) { /* frame changed */ }
  ..onComplete = () { /* finished */ };

await ticker.completed; // resolves when finished
```

### SpriteAnimationGroupComponent

Manages multiple named animations and transitions between them. The active state is set via `current`.

```dart
enum RobotState { idle, running }

final robot = SpriteAnimationGroupComponent<RobotState>(
  animations: {
    RobotState.running: runningAnimation,
    RobotState.idle: idleAnimation,
  },
  current: RobotState.idle,
);

robot.current = RobotState.running; // change animation

// State-based ticker callbacks
robot.animationTickers?[RobotState.running]?.onStart = () {};
robot.animationTickers?[RobotState.idle]?.onFrame = (index) {};
```

### SpriteGroupComponent

The static-sprite counterpart of `SpriteAnimationGroupComponent`.

```dart
class PlayerComponent extends SpriteGroupComponent<ButtonState> {
  @override
  Future<void> onLoad() async {
    sprites = {
      ButtonState.pressed: await game.loadSprite('pressed.png'),
      ButtonState.unpressed: await game.loadSprite('unpressed.png'),
    };
    current = ButtonState.unpressed;
  }
}
```

## 7. Text Rendering

### TextComponent

`TextComponent` renders a single line of text.

```dart
class MyGame extends FlameGame {
  @override
  void onLoad() {
    add(
      TextComponent(
        text: 'Hello, Flame',
        position: Vector2.all(16.0),
      ),
    );
  }
}
```

### TextPaint and styling

A `TextRenderer` is supplied to customize render properties. Its simplest implementation is `TextPaint`, which takes a Flutter `TextStyle`.

```dart
import 'package:flame/text.dart';

final regular = TextPaint(
  style: TextStyle(
    fontSize: 48.0,
    color: BasicPalette.white.color,
  ),
);

class MyGame extends FlameGame {
  @override
  void onLoad() {
    add(
      TextComponent(
        text: 'Hello, Flame',
        textRenderer: regular,
        anchor: Anchor.topCenter,
        position: Vector2(size.x / 2, 32.0),
      ),
    );
  }
}
```

Commonly used `TextStyle` properties: `fontFamily` (including custom fonts from pubspec), `fontSize` (defaults to 24.0), `height` (line-height multiplier), `color` (defaults to white).

```dart
const textPaint = TextPaint(
  style: TextStyle(
    fontSize: 48.0,
    fontFamily: 'Awesome Font',
  ),
);
```

### TextRenderer

`TextRenderer` is the abstract class that converts text into a render-ready `TextElement`. Key methods: `TextElement format(String text)`, `LineMetrics getLineMetrics(String text)`, and `render(...)`.

```dart
textRenderer.render(
  canvas,
  'Flame is awesome',
  Vector2(10, 10),
  anchor: Anchor.topCenter,
);
```

Ready-made implementations: `TextPaint` (Flutter-based), `SpriteFontRenderer` (bitmap font), `DebugTextRenderer` (golden tests).

## Resources

- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/rendering/images.md
- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/rendering/text_rendering.md
- https://docs.flame-engine.org/latest/flame/components/sprite_components.html
- https://pub.dev/documentation/flame/latest/components/SpriteAnimationComponent-class.html
