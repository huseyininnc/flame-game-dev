# Flame: Efektler ve Partiküller

Bu doküman Flame'in efekt sistemi (`Effect`, `EffectController` ve somut efektler) ile partikül sistemini kapsar.

## 1. Efekt Temelleri

Efekt, başka bir component'e iliştirilerek onun özelliklerini veya görünümünü zaman içinde değiştiren özel bir component'tir. Soyut `Effect` sınıfı ortak işlevselliği sağlar:

- **Duraklatma/devam:** `effect.pause()`, `effect.resume()`, durum: `effect.isPaused`
- **Otomatik kaldırma:** `removeOnFinish` (varsayılan `true`) bitince efekt component'ini kaldırır
- **Tamamlanma callback'i:** opsiyonel `onComplete`, efekt bitince (kaldırılmadan önce) çalışır
- **Tamamlanma future'ı:** `completed` future'ı efekt bittiğinde çözülür
- **Sıfırlama:** `reset()` ile yeniden kullanım için başlangıç durumuna döner

## 2. EffectController

`EffectController`, efektin zaman içindeki ilerleyişini tanımlar. Standart factory constructor parametreleri:

- `duration` (zorunlu): 0→%100 ilerleme süresi (saniye)
- `curve`: doğrusal olmayan ilerleme (varsayılan `Curves.linear`)
- `reverseDuration`: ters aşama süresi (%100→0)
- `reverseCurve`: ters aşama eğrisi (varsayılan `curve.flipped`)
- `alternate`: `reverseDuration == duration` ile eşdeğer boolean
- `atMaxDuration`: %100'de bekleme süresi
- `atMinDuration`: %0'da bekleme süresi
- `repeatCount`: tekrar sayısı
- `infinite`: sonsuz tekrar boolean
- `startDelay`: başlamadan önce bekleme süresi
- `onMax` / `onMin`: maksimum/minimum ilerlemede callback

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

### Özelleşmiş controller'lar

| Controller | Amaç |
|---|---|
| `LinearEffectController(duration)` | Doğrusal 0→1 |
| `ReverseLinearEffectController(duration)` | Doğrusal 1→0 |
| `CurvedEffectController(duration, curve)` | Eğrili 0→1 |
| `ReverseCurvedEffectController(duration, curve)` | Eğrili 1→0 |
| `PauseEffectController(duration, progress)` | Sabit ilerleme |
| `RepeatedEffectController(child, count)` | Child'ı N kez tekrarlar |
| `InfiniteEffectController(child)` | Child'ı sonsuz tekrarlar |
| `SequenceEffectController([...])` | Controller'ları sırayla zincirler |
| `SpeedEffectController(child, speed)` | Hıza göre süreyi ayarlar |
| `DelayedEffectController(child, delay)` | Child'ı geciktirir |
| `ZigzagEffectController(period)` | 0→1→-1→0 salınımı |
| `SineEffectController(period)` | Tek sinüs periyodu |
| `NoiseEffectController(duration, frequency)` | Rastgele salınım |
| `RandomEffectController.uniform(child, min, max)` | Rastgele süre sarmalayıcı |

## 3. Move Efektleri

`MoveEffect.by` (göreli) ve `MoveEffect.to` (mutlak). Alttaki sınıflar `MoveByEffect` ve `MoveToEffect`.

```dart
// Mevcut konuma göre kaydır
final moveBy = MoveEffect.by(
  Vector2(30, 30),
  EffectController(duration: 1.0),
);

// Belirli bir hedefe git
final moveTo = MoveEffect.to(
  Vector2(100, 500),
  EffectController(duration: 3),
);
```

### MoveAlongPathEffect

Component'i belirtilen yol boyunca hareket ettirir. `absolute: true` mutlak canvas koordinatları, `oriented: true` hedefi yola göre döndürür.

```dart
final pathEffect = MoveAlongPathEffect(
  Path()..quadraticBezierTo(100, 0, 50, -50),
  EffectController(duration: 1.5),
  oriented: true,
);
```

## 4. Scale Efektleri

`ScaleEffect.by` (göreli), `ScaleEffect.to` (mutlak). Scale tüm child component'leri etkiler (size yalnızca parent boyutunu).

```dart
// %50 büyüt
final scaleBy = ScaleEffect.by(
  Vector2.all(1.5),
  EffectController(duration: 0.3),
);

// Mutlak ölçeğe ayarla
final scaleTo = ScaleEffect.to(
  Vector2.all(0.5),
  EffectController(duration: 0.5),
);
```

## 5. Rotate Efektleri

Açı **radyan** cinsindendir (`tau/4` = 90°). Yön referansı: 0º = kuzey, tau/4 = doğu.

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

## 6. Opacity ve Color Efektleri

`OpacityEffect`, yalnızca `OpacityProvider` arabirimini uygulayan component'lere uygulanabilir. `HasPaint` mixin'i `OpacityProvider`'ı uygular. Opacity 0 = tam saydam, 1 = tam opak.

`OpacityEffect.to(double, controller)`, `OpacityEffect.fadeOut(controller)` (tam saydamlığa) ve `OpacityEffect.fadeIn(controller)` (tam görünürlüğe).

```dart
class MyComponent extends SpriteComponent with HasPaint {
  MyComponent(Sprite sprite) : super(sprite: sprite);
}

final fadeIn = OpacityEffect.fadeIn(EffectController(duration: 1.5));
final fadeOut = OpacityEffect.fadeOut(EffectController(duration: 0.5));
final toHalf = OpacityEffect.to(0.5, EffectController(duration: 0.75));
```

### ColorEffect

Component'i bir renge boyar. **Not:** Flutter'ın `ColorFilter` yapısı nedeniyle birden çok `ColorEffect` birlikte kullanılamaz; yalnızca sonuncusu etkili olur.

```dart
final colorEffect = ColorEffect(
  const Color(0xFF00FF00),
  EffectController(duration: 1.5),
  opacityFrom: 0.2,
  opacityTo: 0.8,
);
```

## 7. SequenceEffect

Birden çok efekti sırayla çalıştırır. Constituent efektler farklı tiplerde olabilir. `alternate: true` (controller üzerinde) ileri-geri çalıştırır; tekrar `repeatCount` veya `infinite` ile kontrol edilir.

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

Efektin tamamlanmasını dinleme:

```dart
final effect = MoveEffect.by(
  Vector2(0, -100),
  EffectController(duration: 1.0),
  onComplete: () => print('hareket bitti'),
);
add(effect);
await effect.completed;
```

## 8. Partikül Sistemi

Partikül sistemi `Particle` sınıfı etrafında döner. `ParticleSystemComponent`, Component yaşam döngüsü kancalarını Particle'a eşler ve bitince component'i kaldırır.

```dart
import 'package:flame/components.dart';

game.add(
  ParticleSystemComponent(
    particle: CircleParticle(),
  ),
);
```

### Particle.generate

Birden çok partikül örneği üretir.

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

Tüm partiküller saniye cinsinden `lifespan` alır (mikrosaniye hassasiyet). `setLifespan()` sıfırlar, `progress` getter'ı 0.0–1.0 arası ömrü izler.

```dart
final particle = CircleParticle()..setLifespan(2); // 2 saniye
```

### Yaygın partikül tipleri

```dart
// Sabit konuma çevirir (konumu değiştirmeden)
TranslatedParticle(offset: game.size / 2, child: Particle());

// from -> to arası hareket ettirir
MovingParticle(
  from: Vector2.zero(),
  to: game.size,
  child: CircleParticle(radius: 2.0, paint: Paint()..color = Colors.red),
);

// Fizik tabanlı (position, speed, acceleration -> logical px/s)
AcceleratedParticle(
  position: game.canvasSize / 2,
  speed: Vector2(rnd.nextDouble() * 200 - 100, -rnd.nextDouble() * 100),
  child: CircleParticle(radius: 2.0, paint: Paint()..color = Colors.red),
);

// Daire çizer
CircleParticle(
  radius: game.size.x / 2,
  paint: Paint()..color = Colors.red.withValues(alpha: .5),
);

// 1 -> to arası ölçekler
ScalingParticle(
  lifespan: 2,
  to: 0,
  curve: Curves.easeIn,
  child: CircleParticle(radius: 2.0, paint: Paint()..color = Colors.red),
);

// Sprite gömer
SpriteParticle(sprite: mySprite, size: Vector2(64, 64));

// dart:ui Image gömer
ImageParticle(size: Vector2.all(24), image: image);

// SpriteAnimation oynatır
SpriteAnimationParticle(
  animation: spriteSheet.createAnimation(0, stepTime: 0.1),
);

// Component gömer (kendi update/render'ı ile)
ComponentParticle(component: longLivingRect);
```

### ComputedParticle

Tam özel render için. `progress` ile zaman bazlı interpolasyon yapılır.

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

### Kompozisyon ve iç içe yerleştirme

Flame, Flutter widget'larına benzer kompozisyon kullanır. Özel partiküller için `SingleChildParticle` mixin'i, çoklu davranış birleştirme için `ComposedParticle` kullanılır.

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

## Kaynaklar

- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/effects/effects.md
- https://docs.flame-engine.org/latest/flame/effects/move_effects.html
- https://docs.flame-engine.org/latest/flame/effects/scale_effects.html
- https://docs.flame-engine.org/latest/flame/effects/rotate_effects.html
- https://docs.flame-engine.org/latest/flame/effects/sequence_effect.html
- https://docs.flame-engine.org/latest/flame/effects/effect_controllers.html
- https://docs.flame-engine.org/latest/flame/effects/color_effects.html
- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/rendering/particles.md
