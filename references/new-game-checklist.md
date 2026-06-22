# Yeni Flame Oyunu — Kontrol Listesi

## 0. Konsept
- [ ] Tür ve temel döngü tek cümlede tanımlandı.
- [ ] Girdi modeli: dokunmatik / joystick / klavye / tap.
- [ ] Yönlendirme (portrait/landscape) ve hedef çözünürlük (fixed-resolution mı?).
- [ ] Platform hedefleri (Android/iOS/web/desktop).

## 1. İskele
- [ ] VGV `create-project` (`flame_game`) ile oluşturuldu; org + ad (`_` ile).
- [ ] `analysis_options.yaml` → `very_good_analysis` include.
- [ ] Bağımlılıklar: `flame`, gerekiyorsa `flame_audio`, `flame_bloc`, `flame_tiled`.
- [ ] `pubspec.yaml` asset klasörleri: `assets/images/`, `assets/audio/`, `assets/tiles/`.

## 2. Mimari (references/flame/10)
- [ ] Oyun `game_core`'daki `BaseFlameGame`'i extend ediyor.
- [ ] Oyuna özel kod `apps/<game>/lib/game` altında.
- [ ] Kalıcılık (yüksek skor vb.) `*_repository` paketinde, Flame'den bağımsız.
- [ ] Bağımlılık yönü tek yönlü: feature → core → repository.

## 3. Durum
- [ ] Skor/can/faz Bloc veya Cubit'te.
- [ ] `FlameBlocProvider`/`FlameMultiBlocProvider` ile sağlandı.
- [ ] Component'ler `FlameBlocReader` (event) / `FlameBlocListenable` (state) ile bağlı.
- [ ] Component'ler karar vermiyor; yalnızca okuyup çiziyor.

## 4. Ekranlar
- [ ] Menü/ayar/level → `RouterComponent` + `Route`/`WorldRoute`.
- [ ] HUD → kalıcı overlay veya `camera.viewport`.
- [ ] Pause → `pauseEngine()` + `overlays.add`.
- [ ] Game over → overlay; tekrar oyna akışı.
- [ ] **Her overlay `Material(type: MaterialType.transparency, child: ...)` ile sarıldı** (yoksa çıplak `Text`'ler sarı altı-çizgiyle çıkar).
- [ ] Overlay'ler `SafeArea` + `ConstrainedBox(maxWidth)` ile responsive.

## 5. Assetler
- [ ] Görseller webp (sanat yönü oyuna göre), `assets/images/` altında, pubspec'te kayıtlı.
- [ ] Ses sfx/bgm `assets/audio/` altında.
- [ ] Tüm asset `onLoad`'da preload (`images.loadAll`, `audioCache.loadAll`).

## 6. Performans (references/flame/11)
- [ ] `update()` içinde yeni `Vector2`/liste/closure yok.
- [ ] Sık nesnelerde object pooling / `RecycledQueue`.
- [ ] Çok sayıda statik gövdede `HasQuadTreeCollisionDetection` ölçüldü.
- [ ] Geliştirmede `FpsTextComponent`; yayında `debugMode = false`.

## 7. Doğrulama
- [ ] `run`/`verify` ile gerçek cihaz/emülatörde çalıştırıldı.
- [ ] 60 FPS gözlemlendi.
- [ ] `dart` MCP ile runtime hatası kontrolü (gerekirse).
- [ ] Lint temiz; kodda yorum yok.
