# Flame: Sprite, Görsel ve Metin Render

Bu doküman Flame (kararlı 1.x) ile görsel yükleme, `Sprite`, `SpriteComponent`, sprite sheet, animasyon ve metin render konularını kapsar.

## 1. Görsel Yükleme

Flame, asset'lerden görsel yükleyip önbelleğe alan bir `Images` yardımcı sınıfı sağlar. Görseller `assets/images/` altında bulunmalı ve `pubspec.yaml` içinde tanımlanmalıdır.

### Images sınıfı ve global cache

```dart
import 'package:flame/cache.dart';

final imagesLoader = Images();
final image = await imagesLoader.load('yourImage.png');
```

`Images` cache yönetim metodları: `load`, `loadAll`, `clear`, `clearCache`, `fromCache`, `add` ve `keys` getter'ı.

Global singleton üzerinden:

```dart
import 'package:flame/flame.dart';
import 'package:flame/sprite.dart';

final image = await Flame.images.load('player.png');
final playerSprite = Sprite(image);
```

### Oyun seviyesinde görsel yönetimi

`Game` sınıfı, widget ağacından kaldırıldığında cache'i otomatik temizleyen bir `images` örneği barındırır.

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

Cache'lenmiş görseli oyun sırasında almak için `images.fromCache`:

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

`Sprite`, bir görseli ya da görselin bir bölgesini temsil eder.

```dart
final image = await images.load('player.png');
final player = Sprite(image);
```

### Sprite sheet'ten bölge alma

`srcPosition` varsayılan `(0.0, 0.0)`, `srcSize` varsayılan `null`'dur (tam görsel boyutu).

```dart
final image = await images.load('player.png');
final playerFrame = Sprite(
  image,
  srcPosition: Vector2(32.0, 0),
  srcSize: Vector2(16.0, 16.0),
);
```

### Render

`render` metodu canvas, genişlik ve yükseklik alır; isteğe bağlı `overridePaint` ve "ghost line"ları önleyen `bleed` parametreleri vardır.

```dart
final block = Sprite(await images.load('block.png'));
block.render(canvas, 16.0, 16.0);

// Sprite bleeding (kenar taşması) önleme
playerFrame.render(canvas, 16.0, 16.0, bleed: 1.0);
```

## 3. SpriteComponent

`SpriteComponent`, statik sprite göstermek için `PositionComponent`'in birincil uygulamasıdır.

Önemli constructor parametreleri: `sprite`, `size`, `position` (varsayılan `Vector2(0,0)`), `angle` (radyan, varsayılan `0`), `anchor`, ve sprite bleeding için `bleed`.

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

Bleeding'i component üzerinde uygulamak:

```dart
final spriteComponent = SpriteComponent(
  sprite: sprite,
  size: Vector2.all(16.0),
  bleed: 1.0,
);
```

## 4. SpriteSheet

`SpriteSheet`, sprite sheet'ten sprite ve animasyon çıkarımını basitleştirir.

```dart
import 'package:flame/sprite.dart';

final spriteSheet = SpriteSheet(
  image: imageInstance,
  srcSize: Vector2.all(16.0),
);

// Bir satırdan animasyon oluştur (row index 0)
final animation = spriteSheet.createAnimation(0, stepTime: 0.1);
```

Statik sprite çıkarımı:

```dart
spriteSheet.getSpriteById(2); // id ile
spriteSheet.getSprite(0, 0);  // satır, sütun ile
```

## 5. SpriteAnimation

Eşit boyutlu sprite'lardan döngüsel animasyon oluşturur.

### Sprite listesinden

```dart
final animation = SpriteAnimation.spriteList(sprites, stepTime: 0.02);
```

### Frame data ile (sprite sheet'ten)

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

Animasyonun zaman ilerlemesini `SpriteAnimationTicker` yönetir. Bir component dışında kendi animasyonunu yönetirken doğrudan kullanılabilir.

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

Çok kareli döngüsel animasyonları gösterir.

Önemli constructor parametreleri:
- `animation`: oynatılacak `SpriteAnimation`
- `size`: Vector2 boyut
- `autoPlay`: otomatik başlasın mı
- `playing`: anlık oynatma durumu
- `removeOnFinish`: animasyon bitince component kaldırılsın mı
- `resetOnRemove`: kaldırılınca ilk kareye dönsün mü

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

### animationTicker ve callback'ler

Component, dahili bir `SpriteAnimationTicker`'ı `animationTicker` property'si ile sunar. Ticker `onStart`, `onFrame(int index)` ve `onComplete` callback'leri ile `completed` future'ını sağlar.

```dart
final ticker = SpriteAnimationTicker(animation)
  ..onStart = () { /* başladı */ }
  ..onFrame = (index) { /* kare değişti */ }
  ..onComplete = () { /* bitti */ };

await ticker.completed; // bitince çözülür
```

### SpriteAnimationGroupComponent

Birden çok adlandırılmış animasyonu yönetir ve aralarında geçiş yapar. `current` ile aktif durum belirlenir.

```dart
enum RobotState { idle, running }

final robot = SpriteAnimationGroupComponent<RobotState>(
  animations: {
    RobotState.running: runningAnimation,
    RobotState.idle: idleAnimation,
  },
  current: RobotState.idle,
);

robot.current = RobotState.running; // animasyon değiştir

// Durum bazlı ticker callback'leri
robot.animationTickers?[RobotState.running]?.onStart = () {};
robot.animationTickers?[RobotState.idle]?.onFrame = (index) {};
```

### SpriteGroupComponent

`SpriteAnimationGroupComponent`'in statik sprite karşılığı.

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

## 7. Metin Render

### TextComponent

`TextComponent` tek satır metin render eder.

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

### TextPaint ve styling

Render özelliklerini özelleştirmek için bir `TextRenderer` verilir. En basit uygulaması, Flutter `TextStyle`'ını alan `TextPaint`'tir.

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

Sık kullanılan `TextStyle` özellikleri: `fontFamily` (pubspec'teki özel fontlar dahil), `fontSize` (varsayılan 24.0), `height` (satır yüksekliği çarpanı), `color` (varsayılan beyaz).

```dart
const textPaint = TextPaint(
  style: TextStyle(
    fontSize: 48.0,
    fontFamily: 'Awesome Font',
  ),
);
```

### TextRenderer

`TextRenderer`, metni render'a hazır `TextElement`'e dönüştüren soyut sınıftır. Anahtar metotlar: `TextElement format(String text)`, `LineMetrics getLineMetrics(String text)`, ve `render(...)`.

```dart
textRenderer.render(
  canvas,
  'Flame is awesome',
  Vector2(10, 10),
  anchor: Anchor.topCenter,
);
```

Hazır uygulamalar: `TextPaint` (Flutter tabanlı), `SpriteFontRenderer` (bitmap font), `DebugTextRenderer` (golden testleri).

## Kaynaklar

- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/rendering/images.md
- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/rendering/text_rendering.md
- https://docs.flame-engine.org/latest/flame/components/sprite_components.html
- https://pub.dev/documentation/flame/latest/components/SpriteAnimationComponent-class.html
