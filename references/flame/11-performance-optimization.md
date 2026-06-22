# Flame: 60 FPS Performans Optimizasyonu

Cok sayida kucuk oyunu uretirken her birinin akici (hedef **60 FPS**) calismasi icin tekrarlanabilir performans kurallari. Asagidaki API'ler Flame kaynagindan dogrulanmistir.

---

## 1. Asset'leri `onLoad` icinde onceden yukleyin

Oyun calisirken (`update`/`render` sirasinda) gorsel/ses yuklemek frame dususune yol acar. Tum image ve audio'yu `onLoad` icinde, oyun baslamadan once preload edin.

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

Boylece runtime sirasinda disk/cozme gecikmesi olmaz; tum kareler hazir bellekteki kaynaklari kullanir.

---

## 2. `update()` icinde tahsisattan (allocation) kacinin

`update(double dt)` saniyede ~60 kez calisir. Her karede yeni nesne (`Vector2`, liste, closure) yaratmak garbage collector'i tetikler ve jank olusturur. Nesneleri **bir kez** olusturup yeniden kullanin.

```dart
class Player extends PositionComponent {
  // Her karede yeniden yaratmak yerine bir kez tahsis et.
  final Vector2 _velocity = Vector2.zero();

  @override
  void update(double dt) {
    super.update(dt);
    // KOTU:  position += Vector2(0, speed * dt);   // her karede yeni Vector2
    // IYI:
    _velocity.setValues(0, speed);
    position.addScaled(_velocity, dt);
  }
}
```

`Vector2` uzerinde `setValues`, `add`, `addScaled`, `scale` gibi *in-place* metotlari tercih edin; operatorler (`+`, `*`) yeni nesne uretir.

---

## 3. Nesne havuzu (object pooling): ekle/cikar churn'undan kacinin

Mermi, parcacik, dusman gibi sik olusup yok olan nesnelerde `add()`/`removeFromParent()` dongusu hem GC baskisi hem de component agaci yeniden yapilandirma maliyeti yaratir. Bunun yerine **havuzdan yeniden kullanin**: nesneyi yok etmek yerine pasiflestirip (ornek: ekran disina alip `removeFromParent` yapmadan) tekrar aktive edin.

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

Anahtar fikir: nesneyi component agacindan cikarmak yerine `isActive` bayragiyla pasiflestirip yeniden kullanmak. Bu, hot-path'te tahsisi sifirlar.

### 3.1 `RecycledQueue` ile yerlesik geri donusum

Flame, ayni amac icin yerlesik bir `RecycledQueue<T extends Disposable>` sunar: elemanlari **olusturup sahiplenen**, kuyruktan cikinca yok etmek yerine `dispose` edip yeniden kullanim havuzuna birakan FIFO kuyrugu. Yeni eleman eklendiginde onceden dispose edilmis elemanlar tekrar kullanilir.

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
  // addLast yeni (veya geri donusturulmus) bir eleman uretir, doldurmasi sizde.
  final p = particles.addLast()
    ..x = px
    ..y = py
    ..life = 1.0;
}

void tick(double dt) {
  for (final p in particles) {
    p.life -= dt;
    if (p.life <= 0) {
      particles.removeCurrent(); // iterasyon sirasinda guvenli
    }
  }
}
```

> `RecycledQueue` API'si klasik Queue'dan farklidir: `addLast` yeni eleman uretip doldurmaniz icin geri verir; `removeFirst` ilk elemani **dondurmeden** siler (oncesinde `first` ile alin). Iterasyon sirasinda `removeCurrent` ve `addLast` ile degistirilebilir; ayni anda yalnizca bir iterator desteklenir.

---

## 4. Cok sayida statik gövde icin `HasQuadTreeCollisionDetection`

Çok sayida collidable nesnesi olan genis oyun alanlarinda (yuzlercesi, ozellikle statik govdeler) varsayilan sweep-and-prune yavaşlar. Bu durumda standart `HasCollisionDetection` yerine `HasQuadTreeCollisionDetection` kullanip baslatın.

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

`initializeCollisionDetection` parametreleri:

- **`mapDimensions`** (zorunlu): Quad tree'nin uzamsal sinirlari (`Rect`).
- **`minimumDistance`** (ops.): Carpisma kontrolu oncesi minimum mesafe; `null` (varsayilan) kontrolu kapatir.
- **`maxObjects`** (ops., varsayilan 25): Bir kadran basina maksimum nesne.
- **`maxDepth`** (ops., varsayilan 10): Kadran ic ice yuvalanma derinligi.

Hitbox'larda `onComponentTypeCheck` override ederek uyumsuz tipleri carpisma kontrolu oncesi eleyebilirsiniz (ek hizlanma).

> Flame dokumantasyonu uyarir: "Her zaman farkli yaklasimları deneyin ve oyununuzda nasil performans gosterdiklerini olcun. Daha sofistike yaklasimin her zaman daha hizli olacagini varsaymayin." Az nesneli oyunlarda varsayilan algoritma daha hizli olabilir.

---

## 5. `pauseEngine` / `resumeEngine` ile bos islemden kacinma

Oyun pause edildiginde veya bir Flutter overlay/dialog acikken `update` dongusunu durdurmak hem CPU/GPU hem de pil tasarrufu saglar.

```dart
class MyGame extends FlameGame {
  void openPauseMenu() {
    pauseEngine();              // update/render dongusunu durdurur
    overlays.add('PauseMenu');
  }

  void closePauseMenu() {
    overlays.remove('PauseMenu');
    resumeEngine();
  }
}
```

`paused` getter'i ile durum okunabilir; `paused = true/false` ile de ayarlanabilir. Pause sirasinda Flutter overlay'leri etkilesimli kalir.

---

## 6. FPS olcumu: `FpsTextComponent` ve `debugMode`

Optimizasyonu **olcerek** dogrulayin. Flame, ekranda anlik FPS gosteren `FpsTextComponent` sunar (`FpsComponent` salt-hesap versiyonudur).

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

`debugMode` ile component sinirlari, anchor'lar ve hitbox'lar cizilir — yerlesim/carpisma sorunlarini ayiklamak icin:

```dart
class MyGame extends FlameGame {
  @override
  bool get debugMode => true;
}
```

Ayrica bir component bazinda `component.debugMode = true` ayarlanabilir. Yayina cikmadan once `debugMode`'u kapatin (ek cizim maliyeti).

---

## 7. Hizli kontrol listesi (her oyun icin)

- [ ] Tum image/audio `onLoad` icinde `loadAll` ile preload edildi.
- [ ] `update()` icinde yeni `Vector2`/liste/closure tahsisi yok; in-place metotlar kullanildi.
- [ ] Sik olusan nesneler (mermi, parcacik) havuzdan/`RecycledQueue` ile yeniden kullaniliyor; `add`/`remove` churn'u yok.
- [ ] Yuzlerce collidable varsa `HasQuadTreeCollisionDetection` denendi ve olculdu.
- [ ] Pause/overlay aciklarken `pauseEngine()` cagriliyor.
- [ ] Gelistirmede `FpsTextComponent` ile 60 FPS dogrulandi; yayinda `debugMode = false`.

---

## Kaynaklar

- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/collision_detection.md
- https://raw.githubusercontent.com/flame-engine/flame/main/packages/flame/lib/src/components/core/recycled_queue.dart
- https://raw.githubusercontent.com/flame-engine/flame/main/packages/flame/lib/src/components/fps_text_component.dart
- https://docs.flame-engine.org/latest/
