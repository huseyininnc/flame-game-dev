# Flame: Girdi ve Hareketler (Input & Gestures)

Bu doküman Flame'in güncel girdi API'sini kapsar. **Önemli:** Flame, eski `Tappable` / `HasTappables` ve `Draggable` / `HasDraggables` mixin'lerini kullanımdan kaldırmıştır. Güncel yaklaşım, component üzerine eklenen **`TapCallbacks`** ve **`DragCallbacks`** mixin'leridir; bu mixin'ler game tarafında ayrı bir "has..." mixin gerektirmez.

## 1. Tap Olayları — TapCallbacks

`TapCallbacks` mixin'i bir component'i tap etkileşimlerine duyarlı yapar. Override edilebilir metotlar:

- `onTapDown(TapDownEvent event)` — ekrana ilk dokunuş
- `onTapUp(TapUpEvent event)` — tap başarıyla tamamlandığında
- `onTapCancel(TapCancelEvent event)` — tap başarısız olduğunda (örn. parmak hareket edip drag'e dönerse)
- `onLongTapDown(TapDownEvent event)` — ~300ms basılı tutunca (varsayılan `TapConfig.longTapDelay`)

```dart
class MyComponent extends PositionComponent with TapCallbacks {
  MyComponent() : super(size: Vector2(80, 60));

  @override
  void onTapUp(TapUpEvent event) {
    // tap olayına yanıt
  }
}
```

`onTapDown` olayı `localPosition` (component koordinatı) ve `canvasPosition` (canvas koordinatı) sağlar. `event.continuePropagation = true` ile alttaki component'lere iletilebilir.

### Hit detection

Component'ler tap geçerliliği için `containsLocalPoint()` uygular. `PositionComponent` bunu otomatik sağlar; ham `Component` için elle yazılmalıdır.

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

Çoklu eşzamanlı dokunuşlar olaylardaki `pointerId` ile bağımsız izlenir.

## 2. Drag Olayları — DragCallbacks

`DragCallbacks` mixin'i drag hareketlerini etkinleştirir. Component yine `containsLocalPoint()` uygulamalıdır (`PositionComponent`'te hazır gelir).

Metotlar:
- `onDragStart(DragStartEvent event)` — drag başlangıcı; en üstteki component'e iletilir
- `onDragUpdate(DragUpdateEvent event)` — sürükleme boyunca sürekli tetiklenir
- `onDragEnd(DragEndEvent event)` — parmak kaldırılınca (konum verisi yok)
- `onDragCancel(DragCancelEvent event)` — varsayılan olarak `onDragEnd`'e dönüştürülür

`DragUpdateEvent` şunları sağlar: `localPosition` (component dışına çıkarsa NaN), `delta` / `localDelta` (önceki güncellemeden bu yana hareket), `canvasPosition`, `devicePosition`, `timestamp`.

```dart
class MyComponent extends PositionComponent with DragCallbacks {
  MyComponent() : super(size: Vector2(180, 120));

  @override
  void onDragStart(DragStartEvent event) {
    // drag olayına yanıt
  }
}
```

Bir component'i sürükleyerek hareket ettirme:

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

`isDragged` getter'ı aktif sürükleme sırasında `true` döner (görsel geri bildirim için kullanışlıdır). Tek parmak drag olayı, iki parmak hem drag hem scale olayı üretir.

## 3. Klavye Girdisi

İki yaklaşım vardır: game seviyesinde `KeyboardEvents`, veya component seviyesinde `KeyboardHandler` (`HasKeyboardHandlerComponents` ile birlikte).

### Game seviyesi — KeyboardEvents

`onKeyEvent(KeyEvent event, Set<LogicalKeyboardKey> keysPressed)` override edilir ve `KeyEventResult` döner (`handled`, `ignored`, `skipRemainingHandlers`).

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

### Component seviyesi — KeyboardHandler

Component'ler `KeyboardHandler` mixin'i ile klavye olayı alır, ancak yalnızca `HasKeyboardHandlerComponents` ile mixin'lenmiş bir oyuna eklenmelidir. Component'teki `onKeyEvent` aynı imzaya sahiptir ama `bool` döner (`true` propagasyona izin verir, `false` durdurur).

> **Çakışma uyarısı:** `HasKeyboardHandlerComponents` kullanılıyorsa, oyunun mixin listesinden `KeyboardEvents` kaldırılmalıdır.

```dart
class MyGame extends FlameGame with HasKeyboardHandlerComponents { }
```

### KeyboardListenerComponent

Component tabanlı kullanım için hazır bileşen. `keyDown` ve `keyUp` map'leri ile `LogicalKeyboardKey` -> callback eşlemesi yapılır.

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

> `GameWidget` opsiyonel `focusNode` ve `autofocus` (varsayılan `true`) parametreleri ile klavye odağını kontrol eder.

## 4. Sanal Joystick — JoystickComponent

Flame, dokunmatik girdi için sanal joystick component'i sağlar.

Parametreler:
- `knob`: sürüklenen kontrol elemanı (genelde `SpriteComponent`)
- `background`: joystick tabanı
- `margin`: ekran konumu (`EdgeInsets`)
- `knobRadius`: opsiyonel knob yarıçapı

Durum property'leri:
- `intensity`: knob'un merkezden kenara çekilme yüzdesi `[0.0, 1.0]`
- `delta`: knob'un merkezden mutlak çekilme miktarı (`Vector2`)
- `relativeDelta`: çekilme yüzdesi ve yönü (`Vector2`)
- `direction`: `JoystickDirection` enum değeri (`JoystickDirection.idle` ile kontrol edilir)

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

Oyuncuyu joystick ile hareket ettirme (`update` döngüsünde):

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

Mutlak koordinat yerine viewport kenarlarına göre `margin` ile konumlanan buton.

Parametreler: `button` (boştayken gösterilen `PositionComponent`), `buttonDown` (basılıyken, opsiyonel), `margin`, `onPressed`, `onReleased`, `respectCamera` (kamera ile hareket için `true`; HUD davranışı için varsayılan `false`).

```dart
final button = HudButtonComponent(
  button: CircleComponent(radius: 30),
  buttonDown: CircleComponent(radius: 30, paint: Paint()..color = Colors.red),
  margin: const EdgeInsets.only(right: 40, bottom: 40),
  onPressed: () => player.jump(),
);
add(button);
```

Alternatif olarak callback yerine component'i extend edip `onTapDown`, `onTapUp`, `onTapCancel` override edilebilir.

## Kaynaklar

- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/inputs/tap_events.md
- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/inputs/drag_events.md
- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/inputs/keyboard_input.md
- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/inputs/inputs.md
- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/inputs/other_inputs.md
