# Responsive Design — Flutter + Flame (her oyunda ZORUNLU)

Üretilen her oyun; her telefon/tablet/foldable/desktop, her aspect-ratio, DPI, orientation ve çentik (notch) altında **bozulmadan** çalışmalı, görseller distorte olmamalı, widget'lar taşmamalı. **Sanat yönü oyunun içeriğine göre otomatik seçilir** (modern flat, painterly, vektör, cartoon, pixel-art vb. — pixel-art zorunlu DEĞİL); bu doküman seçilen stilden **bağımsız** responsive reçetesidir. Pixel-art seçilirse §4'teki opsiyonel alt başlığı uygula.

---

## 0. Zihinsel model — 3 koordinat uzayı

Flame'de responsive = her öğenin hangi uzayda yaşadığına karar vermek.

```
GameWidget (Flutter, fiziksel px)
 └── FlameGame.size  (mantıksal ekran boyutu = canvas / devicePixelRatio)
      └── CameraComponent
           ├── Viewport   ── EKRAN uzayı (statik). HUD burada; kenarlara sabitlenir.
           ├── Viewfinder ── world'e bakış (position / zoom / anchor / angle)
           └── World      ── OYUN uzayı. Oynanış nesneleri; kamerayla dönüşür.
```

**Altın kurallar:**
- **Oynanış nesneleri → `world`.** Kamera/zoom/letterbox otomatik çalışır.
- **HUD/UI → `camera.viewport`.** Ekran-uzayı; kamera oynayınca yerinde kalır.
- **Asla hardcode piksel konum yok.** Konumu `world` (oynanış) veya `camera.viewport.size` (HUD) **yüzdesiyle** ver.
- **Oyun başına TEK design resolution seç** ve viewport ölçeklesin. En kritik karar budur.

---

## 1. CameraComponent + Viewport'lar

`FlameGame` zaten `camera` ve `world` verir. Kamera 3 parçalı: `viewport`, `viewfinder`, `backdrop`.

| Viewport | Davranış | Aspect uyumsuzluğu | Ne zaman |
|---|---|---|---|
| **MaxViewport** (varsayılan) | Tüm canvas'ı doldurur | Daha çok/az **dünya görünür** (bar yok, distorsiyon yok) | Serbest-kaydırmalı dünyalar ("daha çok ekran = daha çok gör") |
| **FixedResolutionViewport** | Logical çözünürlük + aspect kilitler, fit'e ölçekler | **Letterbox** (kısa kenarda bar); asla esnemez | Çoğu arcade/puzzle/board; herkes **aynı** alanı görür |
| **FixedAspectRatioViewport** | Canvas'ı doldurur ama **aspect korur** | Letterbox, distorsiyon yok; boyut dinamik, oran sabit | Oran önemli ama tam piksel çözünürlük değil |
| **FixedSizeViewport** | Sabit konum+boyutta dikdörtgen | Adapte olmaz (alt-pencere) | Split-screen, minimap, PiP |
| **CircularViewport** | Sabit boyutlu dairesel kırpma | Sabit | Spotlight/dürbün efekti |

**Önerilen responsive varsayılan:** `CameraComponent.withFixedResolution` — tutarlı, adil oynanış; kalan alanı letterbox'lar (ayrıca tek-render ölçek = ucuz).

```dart
final camera = CameraComponent.withFixedResolution(
  world: world, width: 720, height: 1280, // DESIGN resolution
)..viewfinder.anchor = Anchor.topLeft;
```

**Viewfinder (bakış kontrolü):** `position`, `anchor`, `zoom` (master ölçek), `angle`, ve responsive için en önemlisi **`visibleGameSize`** — "en az şu kadar world birimi görünsün" dersin, Flame zoom'u senin için hesaplar (sihirli zoom sayısı yok):

```dart
camera.viewfinder.visibleGameSize = Vector2(16, 9); // ekran ne olursa olsun ≥16×9 world görünür
```
Görünür dünya dikdörtgeni: `camera.visibleWorldRect` (culling + yüzde-yerleşim için).

---

## 2. World (kamera-dönüşümlü) vs Viewport (ekran-uzayı HUD)

```dart
world.add(Player()..position = Vector2(0, 0));        // oynanış → world
camera.viewport.add(ScoreLabel());                     // HUD → viewport
```

**HUD'u kenarlara responsive sabitle:**
- **`AlignComponent`** (tercih; resize'da otomatik yeniden akar):
```dart
camera.viewport.add(AlignComponent(alignment: Anchor.topRight, child: ScoreLabel()));
camera.viewport.add(AlignComponent(alignment: Anchor.bottomCenter, child: Joystick()));
```
- **`HudMarginComponent` / `HudButtonComponent`** (margin tabanlı): bunlar `viewport.size`'a göre ölçülür, zoom değişse de kenara yapışık kalır.

---

## 3. Resize'a tepki + yüzde-yerleşim

`onGameResize(Vector2 size)` her `PositionComponent`'te ve oyunda canvas/orientation değişince tetiklenir. **Önce `super.onGameResize(size)`.**

```dart
class ResponsiveBoard extends PositionComponent with HasGameReference<MyGame> {
  @override
  void onGameResize(Vector2 size) {
    super.onGameResize(size);
    if (!isMounted) return;                 // onGameResize onLoad ÖNCESİ gelebilir — guard
    final vp = game.camera.viewport.size;
    final side = math.min(vp.x, vp.y) * 0.9; // kısa kenarın %90'ı
    this
      ..size = Vector2.all(side)
      ..position = vp / 2
      ..anchor = Anchor.center;
  }
}
```
- HUD yerleşiminde **`camera.viewport.size`**, dünya-içi yerleşimde **`camera.visibleWorldRect`** oku (`game.size` letterbox barlarını yok sayar).
- Orientation'ı `size.x` vs `size.y` ile algıla ve yeniden akıt (orientation'ı kilitlemediysen).

```dart
extension Pct on Vector2 { Vector2 pct(double x, double y) => Vector2(this.x * x, this.y * y); }
label.position = game.camera.viewport.size.pct(0.95, 0.05);
```

---

## 4. Responsive asset/sprite (dünya içinde) — stil-agnostik

**Sanat pikselini world biriminden ayır.** Sprite'ı **world birimiyle** boyutla (component.size); kaynak görseli ön-ölçekleme.

```dart
final player = SpriteComponent(
  sprite: await Sprite.load('player.webp'), // 256px art olabilir
  size: Vector2(1, 1),                       // ama 1 world birimi
  anchor: Anchor.center,
);
```

**FilterQuality'i seçilen sanat stiline göre belirle:**
- **Yumuşak / hi-res / vektörel / painterly art (varsayılan çoğu oyun):** `FilterQuality.medium` (gerekirse `.high`). **Büyük üret, küçült** — downscale keskin kalır, upscale bulanıklaştırır.
  ```dart
  component.paint.filterQuality = FilterQuality.medium;
  ```
- **(Opsiyonel) Pixel-art seçildiyse:** nearest-neighbor — `FilterQuality.none` + `isAntiAlias = false`; tüm frame'i `FixedResolutionViewport(clip:false)` ile **tek seferde** ölçekle (per-sprite değil); asset'i 1× yerleştir (non-integer ölçek = shimmer). Bu yalnızca pixel-art seçildiğinde geçerli bir alt-yöntemdir; zorunlu değil.

**Distorsiyondan kaçın:** boyutu kaynağın aspect'iyle eşle (kare sprite'a `Vector2(2,1)` verme). Tile dikiş/seam için "bleeding" (hücre kenarına 1px şeffaf/çoğaltılmış margin) veya `clip:false`. DPI'yi Flame zaten `devicePixelRatio` ile mantıksal birime çevirir.

---

## 5. Design resolution & ölçekleme stratejisi

- **A) Fixed resolution (adalet-önce, varsayılan):** `withFixedResolution(w,h)` — herkes aynı alanı görür; uç oranlar letterbox. Puzzle/board/arcade/rekabetçi için.
- **B) Adaptive "reveal more" (immersion-önce):** `MaxViewport` + `visibleGameSize`. Geniş ekran daha çok dünya görür (bar yok). Keşif/sandbox için; rekabette adaletsiz.
- **Safe-zone uzlaşması:** kritik oynanışı **garanti-görünür "safe rect"** içine koy (ör. 9:16 / 16:9); diğer oranlardaki fazla alan **margin/dekoratif** olsun (avantaj değil). Letterbox barını temasal `backgroundColor` + opsiyonel dekoratif çerçeve overlay (`CustomPainter` + `IgnorePointer`) ile gizle.
- Tek orientation mantıklıysa kilitle: `main()`'de `Flame.device.setPortrait()` / `setLandscape()`.

---

## 6. Flutter overlay/widget responsiveness (HUD/menü)

Flame overlay'leri standart Flutter widget'larıdır. **Tek kural:** layout'u **pencere genişliği breakpoint'lerine** göre dallandır — cihaz tipine, orientation'a, hardcode piksele göre DEĞİL.

- **Doğru MediaQuery erişimcileri (perf):** `MediaQuery.sizeOf` / `.paddingOf` / `.viewInsetsOf` / `.textScalerOf` / `.devicePixelRatioOf` — `MediaQuery.of` DEĞİL (her değişimde rebuild eder; tikleyen HUD'da pahalı).
- **Breakpoint'ler (Material 3 window size class):** compact `<600` · medium `600–839` · expanded `≥840`. Mobil oyun için bu üçü yeter.
- **Yüzde + clamp (zorunlu):** saf yüzde uç oranlarda bozar → daima clamp'le.
  ```dart
  final w = MediaQuery.sizeOf(context).width;
  final panel = (w * 0.4).clamp(280.0, 480.0);
  final scale = (w / 390).clamp(0.85, 1.4); // tek uiScale: padding/gap/radius/font hep bununla
  ```
- **`LayoutBuilder`** = parent kutusuna göre (docked panel); **`MediaQuery.sizeOf`** = tüm pencere (HUD varyantı seçimi).
- **SafeArea over full-bleed canvas:** canvas tam ekran, yalnızca etkileşimli HUD `SafeArea` içinde:
  ```dart
  Stack(children: [
    Positioned.fill(child: GameWidget(game: game)),
    SafeArea(child: HudOverlay()),
  ]);
  ```
- **Material sarma (zorunlu):** her overlay'i `overlayBuilderMap`'te `Material(type: MaterialType.transparency, child: ...)` ile sar (çıplak `Text` sarı altı-çizgi olmasın, tema fontu uygulansın).
- Panelleri `ConstrainedBox(maxWidth: ...)` + `Align` ile sınırla (tablette balonlaşmasın); araç çubukları `Wrap`; Row/Column dağılımı `Flexible/Expanded/Spacer`.
- **Dokunma hedefi ≥ 48dp/44pt.**

---

## 7. Responsive görsel/asset (Flutter UI tarafı) — bellek kritik

- **`BoxFit`:** background → `cover`; ikon/logo/UI sprite → `contain` veya `scaleDown`; **asla `fill`** (tek distorte eden mod).
- **`cacheWidth`/`cacheHeight` (en büyük bellek kaldıracı):** görseli gösterim boyutunda **decode** et. 4K→384px ~33MB'tan ~330KB'a düşer. Mantıksal boyut × devicePixelRatio ver:
  ```dart
  Image.asset('assets/ui/panel.webp',
    width: panelW, fit: BoxFit.cover,
    cacheWidth: (panelW * MediaQuery.devicePixelRatioOf(context)).round());
  ```
- **Density buckets:** `1.5x/2.0x/3.0x` klasör varyantları sağla; pubspec'te yalnız base path; Flutter DPI'ye göre seçer. (Sadece 4× gönderip downscale'e güvenme.)
- **Vektör/SVG (flutter_svg):** düz UI chrome (ikon, logo, basit çerçeve, glyph) için tek dosya, her DPI'de keskin; perf için `.svg.vec`. Karmaşık/painterly veya pixel-art için kullanma → raster (+density+cacheWidth).
- **9-slice çerçeve/buton:** kod-içi `BoxDecoration` (gradient/border/radius/shadow — sıfır bellek, tercih) veya `DecorationImage(centerSlice: Rect)` (köşeler sabit, orta esner). `BoxDecoration` değerlerini `uiScale` ile ölçekle.
- **Monokrom UI glyph'leri:** `Icon`/icon-font (vektör, `color`/`size` ile ölçeklenir, neredeyse sıfır bellek) — sadece çok-renkli/markalı art için image/SVG.

---

## 8. Metin responsiveness & erişilebilirlik

- **OS font ölçeğine saygı, ama clamp:** `textScaleFactor` deprecated; `MediaQuery.textScalerOf`. Yoğun HUD'u korumak için clamp:
  ```dart
  MediaQuery.withClampedTextScaling(minScaleFactor: 0.9, maxScaleFactor: 1.3, child: hud);
  ```
  (Global `TextScaler.noScaling` ile kapatma — erişilebilirlik gerilemesi.)
- **Sabit slot'ta taşmayı önle (skor/sayaç):** `FittedBox(fit: BoxFit.scaleDown, child: Text('$score', maxLines: 1))`. Paragrafta `maxLines + ellipsis` kullan (FittedBox'a paragraf sarma).

---

## 9. Reçeteler

**Responsive HUD (Flame, köşeler otomatik akar):**
```dart
camera.viewport.addAll([
  AlignComponent(alignment: Anchor.topLeft,     child: HealthBar()),
  AlignComponent(alignment: Anchor.topRight,    child: ScoreLabel()),
  AlignComponent(alignment: Anchor.bottomLeft,  child: Joystick()),
  AlignComponent(alignment: Anchor.bottomRight, child: FireButton()),
]);
```

**Responsive grid/board (Flame):** §3'teki `onGameResize` + kısa kenara sığan kare hücre.

**Responsive Flutter overlay paneli (compact↔tablet, clamp, SafeArea):**
```dart
final size = MediaQuery.sizeOf(context);
final isCompact = size.width < 600;
final scale = (size.width / 390).clamp(0.85, 1.4);
return SafeArea(child: isCompact
  ? Column(children: [stats, const Spacer(), const ActionBar()])
  : Row(children: [const ActionBar(), const Spacer(), stats]));
```

**Responsive buton (ölçeklenir + a11y hedef):** boyut `(48*scale).clamp(48, 88)`, ikon `FittedBox`, radius/shadow `*scale`.

**Notch/safe-area:** canvas full-bleed; HUD `SafeArea`; gerekiyorsa `MediaQuery.paddingOf` insets'ini oyuna geçirip kenar-HUD margin'ine ekle. Kritik HUD safe-rect içinde; yalnız dekoratif art çentik altına taşar.

---

## Kontrol listesi (her oyunda)

- [ ] Oynanış `world`, HUD `camera.viewport`. Hardcode piksel konum yok (% ile).
- [ ] Tek design resolution; `withFixedResolution` (veya bilinçli `MaxViewport`+`visibleGameSize`).
- [ ] Layout component'leri `onGameResize` uygular (önce `super`, `isMounted` guard).
- [ ] HUD `AlignComponent`/`HudMarginComponent` ile (zoom'a dayanıklı).
- [ ] Sprite'lar world biriminde; **FilterQuality stile göre** (yumuşak=`medium`/`high`, pixel-art seçiliyse=`none`). Büyük üret-küçült. Distorsiyon yok (aspect eşle).
- [ ] Flutter overlay: `MediaQuery.sizeOf` breakpoint (600/840) + clamp + `uiScale`; `SafeArea`; `Material` sarma; `maxWidth`.
- [ ] Görseller: `cover/contain` (asla `fill`), `cacheWidth×dpr`, density buckets; düz UI'da SVG/icon-font.
- [ ] Metin: `textScalerOf` clamp; sabit slot'ta `FittedBox`.
- [ ] Telefon (uzun) + tablet (geniş) + iki uç aspect'te ekran görüntüsüyle doğrula: esneme/taşma/bar sorunu yok.

---

## Kaynaklar

- Camera & World — Flame docs: https://docs.flame-engine.org/latest/flame/camera.html
- Viewfinder / FixedResolutionViewport — Flame API: https://pub.dev/documentation/flame/latest/camera/Viewfinder-class.html
- AlignComponent — Flame docs: https://docs.flame-engine.org/latest/flame/layout/align_component.html
- HudButton/HudMargin — Flame docs: https://docs.flame-engine.org/latest/flame/inputs/other_inputs.html
- Flame device orientation & resolution — Craig Oda: https://medium.com/codecakes/flame-game-device-orientation-and-resolution-2ada9daebef5
- Best practices for adaptive design — Flutter: https://docs.flutter.dev/ui/adaptive-responsive/best-practices
- SafeArea & MediaQuery — Flutter: https://docs.flutter.dev/ui/adaptive-responsive/safearea-mediaquery
- Adding assets and images (density buckets) — Flutter: https://docs.flutter.dev/ui/assets/assets-and-images
- ImageCache large images (cacheWidth) — Flutter: https://docs.flutter.dev/release/breaking-changes/imagecache-large-images
- BoxFit — Flutter API: https://api.flutter.dev/flutter/painting/BoxFit.html
- MediaQuery.withClampedTextScaling — Flutter API: https://api.flutter.dev/flutter/widgets/MediaQuery/withClampedTextScaling.html
- Window size classes — Material 3: https://m3.material.io/foundations/layout/applying-layout/window-size-classes
- flutter_svg: https://pub.dev/packages/flutter_svg · flutter_screenutil: https://pub.dev/packages/flutter_screenutil
