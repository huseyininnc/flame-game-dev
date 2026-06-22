# Flame: Input & Gestures

This document covers Flame's current input API. **Important:** Flame has deprecated the old `Tappable` / `HasTappables` and `Draggable` / `HasDraggables` mixins. The current approach uses the **`TapCallbacks`** and **`DragCallbacks`** mixins added to a component; these mixins do not require a separate "has..." mixin on the game side.

## 1. Tap Events — TapCallbacks

The `TapCallbacks` mixin makes a component responsive to tap interactions. Overridable methods:

- `onTapDown(TapDownEvent event)` — the first touch on the screen
- `onTapUp(TapUpEvent event)` — when the tap completes successfully
- `onTapCancel(TapCancelEvent event)` — when the tap fails (e.g., the finger moves and turns into a drag)
- `onLongTapDown(TapDownEvent event)` — when held for ~300ms (default `TapConfig.longTapDelay`)

```dart
class MyComponent extends PositionComponent with TapCallbacks {
  MyComponent() : super(size: Vector2(80, 60));

  @override
  void onTapUp(TapUpEvent event) {
    // respond to the tap event
  }
}
```

The `onTapDown` event provides `localPosition` (component coordinate) and `canvasPosition` (canvas coordinate). With `event.continuePropagation = true`, it can be forwarded to the components beneath.

### Hit detection

Components implement `containsLocalPoint()` for tap validity. `PositionComponent` provides this automatically; for a raw `Component`, it must be written manually.

```dart
class MyComponent extends Component with TapCallbacks {
  final _rect = const Rect.fromLTWH(0, 0, 100, 100);
  final _paint = Paint();
  bool _isPressed = false;

  @override
  bool containsLocalPoint(Vector2 point) => _rect.contains(point.toOffset());

  @override
  void onTapDown(TapDownEvent event) => _isPressed = true;

  @override
  void onTapUp(TapUpEvent event) => _isPressed = false;

  @override
  void onTapCancel(TapCancelEvent event) => _isPressed = false;

  @override
  void render(Canvas canvas) {
    _paint.color = _isPressed ? Colors.red : Colors.white;
    canvas.drawRect(_rect, _paint);
  }
}
```

Multiple simultaneous touches are tracked independently via the `pointerId` on the events.

## 2. Drag Events — DragCallbacks

The `DragCallbacks` mixin enables drag gestures. The component must again implement `containsLocalPoint()` (provided out of the box on `PositionComponent`).

Methods:
- `onDragStart(DragStartEvent event)` — start of the drag; forwarded to the topmost component
- `onDragUpdate(DragUpdateEvent event)` — fired continuously throughout the drag
- `onDragEnd(DragEndEvent event)` — when the finger is lifted (no position data)
- `onDragCancel(DragCancelEvent event)` — converted to `onDragEnd` by default

`DragUpdateEvent` provides: `localPosition` (NaN if it leaves the component), `delta` / `localDelta` (movement since the previous update), `canvasPosition`, `devicePosition`, `timestamp`.

```dart
class MyComponent extends PositionComponent with DragCallbacks {
  MyComponent() : super(size: Vector2(180, 120));

  @override
  void onDragStart(DragStartEvent event) {
    // respond to the drag event
  }
}
```

Moving a component by dragging it:

```dart
class InteractiveRectangle extends RectangleComponent
    with ScaleCallbacks, DragCallbacks {
  double _initialAngle = 0;

  @override
  void onDragUpdate(DragUpdateEvent event) {
    position += event.localDelta;
  }

  @override
  void onScaleStart(ScaleStartEvent event) {
    super.onScaleStart(event);
    _initialAngle = angle;
  }

  @override
  void onScaleUpdate(ScaleUpdateEvent event) {
    angle = _initialAngle + event.rotation;
  }
}
```

The `isDragged` getter returns `true` during an active drag (useful for visual feedback). A single-finger drag produces a drag event, while two fingers produce both drag and scale events.

## 3. Keyboard Input

There are two approaches: `KeyboardEvents` at the game level, or `KeyboardHandler` at the component level (together with `HasKeyboardHandlerComponents`).

### Game level — KeyboardEvents

Override `onKeyEvent(KeyEvent event, Set<LogicalKeyboardKey> keysPressed)` and return a `KeyEventResult` (`handled`, `ignored`, `skipRemainingHandlers`).

```dart
class MyGame extends FlameGame with KeyboardEvents {
  @override
  KeyEventResult onKeyEvent(
    KeyEvent event,
    Set<LogicalKeyboardKey> keysPressed,
  ) {
    final isKeyDown = event is KeyDownEvent;
    final isSpace = keysPressed.contains(LogicalKeyboardKey.space);

    if (isSpace && isKeyDown) {
      if (keysPressed.contains(LogicalKeyboardKey.altLeft) ||
          keysPressed.contains(LogicalKeyboardKey.altRight)) {
        shootHarder();
      } else {
        shoot();
      }
      return KeyEventResult.handled;
    }
    return KeyEventResult.ignored;
  }
}
```

### Component level — KeyboardHandler

Components receive keyboard events via the `KeyboardHandler` mixin, but they must be added to a game that is mixed in with `HasKeyboardHandlerComponents`. The component's `onKeyEvent` has the same signature but returns a `bool` (`true` allows propagation, `false` stops it).

> **Conflict warning:** If `HasKeyboardHandlerComponents` is used, `KeyboardEvents` must be removed from the game's mixin list.

```dart
class MyGame extends FlameGame with HasKeyboardHandlerComponents { }
```

### KeyboardListenerComponent

A ready-made component for component-based usage. The `keyDown` and `keyUp` maps map `LogicalKeyboardKey` -> callback.

```dart
add(
  KeyboardListenerComponent(
    keyDown: {
      LogicalKeyboardKey.keyA: (keysPressed) => true,
      LogicalKeyboardKey.keyD: (keysPressed) => true,
      LogicalKeyboardKey.keyW: (keysPressed) => true,
      LogicalKeyboardKey.keyS: (keysPressed) => true,
    },
    keyUp: {
      LogicalKeyboardKey.keyA: (keysPressed) => true,
      LogicalKeyboardKey.keyD: (keysPressed) => true,
    },
  ),
);
```

> `GameWidget` controls keyboard focus via the optional `focusNode` and `autofocus` (defaults to `true`) parameters.

## 4. Virtual Joystick — JoystickComponent

Flame provides a virtual joystick component for touch input.

Parameters:
- `knob`: the dragged control element (usually a `SpriteComponent`)
- `background`: the joystick base
- `margin`: screen position (`EdgeInsets`)
- `knobRadius`: optional knob radius

State properties:
- `intensity`: the percentage the knob is pulled from center to edge `[0.0, 1.0]`
- `delta`: the absolute amount the knob is pulled from center (`Vector2`)
- `relativeDelta`: the percentage and direction of the pull (`Vector2`)
- `direction`: a `JoystickDirection` enum value (checked against `JoystickDirection.idle`)

```dart
final joystick = JoystickComponent(
  knob: SpriteComponent(
    sprite: sheet.getSpriteById(1),
    size: Vector2.all(100),
  ),
  background: SpriteComponent(
    sprite: sheet.getSpriteById(0),
    size: Vector2.all(150),
  ),
  margin: const EdgeInsets.only(left: 40, bottom: 40),
);
```

Moving the player with the joystick (in the `update` loop):

```dart
@override
void update(double dt) {
  super.update(dt);
  if (joystick.direction != JoystickDirection.idle) {
    position.add(joystick.relativeDelta * maxSpeed * dt);
    angle = joystick.delta.screenAngle();
  }
}
```

## 5. HudButtonComponent

A button positioned relative to the viewport edges via `margin` rather than absolute coordinates.

Parameters: `button` (the `PositionComponent` shown when idle), `buttonDown` (shown when pressed, optional), `margin`, `onPressed`, `onReleased`, `respectCamera` (`true` to move with the camera; defaults to `false` for HUD behavior).

```dart
final button = HudButtonComponent(
  button: CircleComponent(radius: 30),
  buttonDown: CircleComponent(radius: 30, paint: Paint()..color = Colors.red),
  margin: const EdgeInsets.only(right: 40, bottom: 40),
  onPressed: () => player.jump(),
);
add(button);
```

Alternatively, instead of using callbacks, you can extend the component and override `onTapDown`, `onTapUp`, and `onTapCancel`.

## Resources

- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/inputs/tap_events.md
- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/inputs/drag_events.md
- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/inputs/keyboard_input.md
- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/inputs/inputs.md
- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/inputs/other_inputs.md
