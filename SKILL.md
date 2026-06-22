---
name: flame-game-dev
description: Build 2D games with the Flutter Flame engine (flame ^1.37.0) AND design them well — level design, difficulty/pacing, game feel, progression/retention, and professional process. Use when creating, scaffolding, designing, or extending any Flame game — game loop, components, sprites/animations, input, collision, camera/world, audio, overlays/routing, flame_bloc, performance, level/wave design, difficulty tuning, and AI asset generation. Triggers on "new game", "Flame game", "FlameGame", "add a level/enemy/player", "level design", "difficulty curve", "game over screen", "sprite/animation", "generate game assets".
when_to_use: Use whenever working on a Flame-based game in the games workspace — starting a new game, designing levels/waves/difficulty, adding game features (player, enemies, levels, HUD, collision, audio), wiring state with flame_bloc, optimizing for 60 FPS, or generating sprite/audio assets. Skip for non-game Flutter UI work.
---

# Flame Game Development (seri üretim)

Bu skill, Flutter **Flame** motoruyla **çok sayıda, farklı konseptte** oyun üretmek içindir. İki doğrulanmış bilgi tabanını (KB) üretim kuralı olarak kullanır: **teknik (Flame motoru)** ve **tasarım (level design + profesyonel süreç)**.

> **Bu skill self-contained'dir.** Tüm KB'ler ve referanslar skill klasörünün içindedir (`references/`). Skill'i kopyaladığında tüm referanslar eksiksiz gelir; harici `docs/` klasörüne bağımlı değildir.

## ⛔ STUDIO-GRADE MANDATE (sert kapı — pazarlık yok)

Bu skill **amatör, kısa, "MVP-as-product", tek-mekanik tech-demo** oyunlar ÜRETMEZ. Üretilen her oyun, **15+ yıllık kıdemli ekiplerin çalıştığı büyük bir stüdyodan çıkmış gibi**: production-ready, içerik-zengin, çok-asset'li, **tam sürüm** olmalıdır. Gerçek bir stüdyo gibi çalış (design+art+animation+VFX+audio+UI/UX+engineering+QA+live-ops disiplinlerini bilinçle giy).

- **Zorunlu çıta ve "definition of done": `references/production-standards.md`.** Bu dokümanın maddeleri **release blocker**'dır; her oyunda uygula.
- **MVP/prototip yalnızca preproduction'da "fun"ı bulmak içindir** — asla teslim edilen ürün değildir. Teslim daima tam, cilalı, içerik-zengin.
- **Scope tabanları (launch minimumu):** puzzle 100–200 level · hybrid-casual 3–5 ayrı mekanik · idle 40–60 saat + 2–4 prestige · wave/arena 8–15 düşman tipi + 3+ biome. Başlangıç+orta+**geç oyun** birlikte.
- **Tam sistem yığını launch'ta:** core loop + ilerleme omurgası + 2 para birimi + shop/IAP + ads mediation + daily reward + FTUE + settings + save(+cloud) + analytics (battle pass/event/leaderboard scaffold'lu fast-follow).
- **Cila her yerde:** her etkileşimde juice (easing/hit-stop/screenshake/ses/haptic), tek style-guide (placeholder/varsayılan font yok), animasyonlu UI, adaptive audio, kilitli 60 FPS, input latency < 100ms.
- **Bitirilebilirlik = sistemler:** data-driven/parametrik içerik + yeniden-kullanılan sistemler (motoru bir kez kur, içeriği veri olarak dök). Hırslı ol AMA bitir.
- **Üretim sırası:** vertical slice (near-final kalite) → content production → korunmuş polish → soft-launch okuması → launch.

## Mutlak kurallar (workspace CLAUDE.md ile uyumlu)

1. **Kodda yorum YOK.** Inline, blok, doc — hiçbiri. Kod, açık isimlendirme ile kendini anlatır.
2. **Mevcut desenleri taklit et.** Yeni kod yazmadan önce çevredeki kodu incele; mimari ve stilini birebir izle.
3. **SOLID + DRY + KISS + YAGNI.** Component'ler tek sorumluluk; oyun mantığı Bloc/Cubit'te, render component'te.
4. **`any`/`dynamic` yasak.** En sıkı lint: `very_good_analysis`.
5. **Yeni kütüphane/mimari değişikliği için önce onay al.**
6. **Her oyun özgün olmalı.** Mekanik/kurgu oyundan oyuna farklı; yalnızca kod konvansiyonları (mimari/stil) ortaktır — oyun tasarımını kopyalama.
7. **Studio-grade çıta zorunlu.** Amatör/kısa/MVP-as-product yok; `references/production-standards.md`'i her oyunda uygula.
8. **Her oyun KENDİ kimliğine sahip (anti-reskin).** Tema, palet, **HUD düzeni**, UI/buton/panel stili, **font üçlüsü**, hareket kişiliği ve **çekirdek mekanik** oyunun içeriğine göre değişir; bir önceki oyundan farklı olur. **Oyunlar arası ortak `overlay_widgets`/HUD/palette/font yeniden kullanımı YASAK** (kod mimarisi paylaşılır, görsel kimlik paylaşılmaz). **Orientation (portrait VEYA landscape) oyuna göre seçilir** — hepsini portrait yapma. Kural + marka testi: `references/game-design/09-art-ui-identity-and-orientation.md`.

## Bilgi tabanı — önce oku

KB'ler skill içindedir; yollar skill köküne görelidir (`references/...`).

### A) Teknik KB — `references/flame/` (NASIL inşa edilir)
- Kurulum, `FlameGame`, oyun döngüsü, asset yapısı → `references/flame/01-overview-and-setup.md`
- FCS, `PositionComponent`, yaşam döngüsü, mixin'ler → `references/flame/02-components-and-lifecycle.md`
- Sprite/animasyon/metin → `references/flame/03-rendering-sprites-text.md`
- Girdi (tap/drag/klavye/joystick) → `references/flame/04-input-and-gestures.md`
- Efektler ve partiküller → `references/flame/05-effects-and-particles.md`
- Çarpışma → `references/flame/06-collision-detection.md`
- Kamera/World/viewport/HUD → `references/flame/07-camera-world-viewport.md`
- Ses + Tiled haritalar → `references/flame/08-audio-and-tiled.md`
- Overlays/Router/oyun durumu → `references/flame/09-overlays-router-state.md`
- flame_bloc + katmanlı mimari + monorepo → `references/flame/10-architecture-bloc-multigame.md`
- Performans (60 FPS) → `references/flame/11-performance-optimization.md`

### B) Tasarım KB — `references/game-design/` (NE ve NEDEN)
- MDA, estetik, core/meta/session loop, pillar, juice (giriş) → `references/game-design/01-design-foundations.md`
- **Level design çekirdeği** (introduce/develop/twist/conclude, Kishōtenketsu, teach-then-test, signposting, gating, level-içi pacing, blockout, sık hatalar) → `references/game-design/02-level-design-principles.md`
- Zorluk eğrisi, flow channel, sawtooth, interest curve, DDA, balancing → `references/game-design/03-difficulty-and-pacing.md`
- Game feel & juice (screenshake, hit-stop, squash&stretch, easing, ses) → `references/game-design/04-game-feel-and-juice.md`
- Onboarding / FTUE (show-don't-tell, skill atom, time-to-fun) → `references/game-design/05-onboarding-and-tutorialization.md`
- Progression / ekonomi / retention (loop şablonları, reward schedule, source/sink, D1/D7/D30, etik) → `references/game-design/06-progression-economy-retention.md`
- Profesyonel süreç (preprod→prod→liveops, prototip vs vertical slice, milestone, lean GDD, playtest, MVP) → `references/game-design/07-professional-process.md`
- **2D/puzzle/casual/idle level design uygulaması** (levels-as-data, LevelConfig, sawtooth şablonu, match-3 tuning, telemetri, Flame eşlemesi) → `references/game-design/08-level-design-for-2d-casual.md`
- **Per-game design identity (ZORUNLU)** — HUD diegesis, türe-göre HUD düzeni, tipografi/font üçlüsü, görsel kimlik 5 sütun, orientation (portrait/landscape) seçimi, anti-reskin checklist → `references/game-design/09-art-ui-identity-and-orientation.md`

**Ne zaman hangisi:** Yapı/level/zorluk/wave tasarlarken **B (özellikle 02, 03, 08)**; kodlama/motor işinde **A**. İkisini birlikte kullan — iyi kod kötü tasarımı kurtarmaz.

## Sürüm ve güncel API zorunlulukları

- **flame `^1.37.0`**, flame_audio `^2.12.1`, flame_tiled `^3.1.1`, flame_bloc (güncel). (Mevcut workspace oyunları flame `^1.35.1` kullanır — yeni oyunda var olan oyunun sürümüyle hizalan.)
- **Kamera:** `CameraComponent` + `World` kullan; eski `Camera` YOK.
- **Girdi:** `TapCallbacks` / `DragCallbacks` mixin'leri; eski `Tappable`/`Draggable` YOK.
- **Game erişimi:** `HasGameReference<MyGame>` (`game` getter); eski `HasGameRef` deprecated.
- Oyun nesneleri `world`'e, HUD `camera.viewport`'a eklenir.
- `update(dt)` frame-rate bağımsız: hareket/fizik daima `* dt`.
- **Responsive (her oyunda ZORUNLU, sanat-stilinden bağımsız):** oynanış `world` / HUD `camera.viewport`; hardcode piksel konum yok (yüzde + `onGameResize`); `CameraComponent.withFixedResolution` veya bilinçli `MaxViewport`+`visibleGameSize`; sprite world biriminde; **FilterQuality seçilen sanat stiline göre** (yumuşak/vektör/painterly = `medium`/`high`; pixel-art seçildiyse = `none` + nearest); Flutter overlay'leri `MediaQuery.sizeOf` breakpoint (600/840) + clamp + `SafeArea` + `Material` sarma; görseller `cover/contain` (asla `fill`) + `cacheWidth×dpr` + density buckets. Tam reçete: `references/responsive-design.md`. Telefon + tablet + iki uç aspect'te doğrula.
- **Overlay metinleri Material'a sarılmalı (zorunlu):** Flame `GameWidget` overlay'leri `MaterialApp`'in Material bağlamı DIŞINDA render edilir; çıplak `Text`'ler sarı çift altı-çizgiyle çıkar. Her overlay'i `overlayBuilderMap`'te `Material(type: MaterialType.transparency, child: ...)` ile sar.

## Yeni oyun başlatma akışı

1. **Konsept & kimlik (kod öncesi):** hedef estetikleri (MDA), 3–5 design pillar + non-goal, tek-cümle core loop (`references/game-design/01`). **Bu oyuna özel kimliği seç (bir öncekinden farklı): tema, palet, HUD diegesis + düzeni, UI/buton/panel stili, font üçlüsü (display/UI/numeric), hareket kişiliği, ve orientation (portrait VEYA landscape — türe/grip'e göre)** — `references/game-design/09`. Çekirdek mekanik de portföyde tekrar olmasın.
2. **Level/zorluk tasarımı (kod öncesi):** çekirdek loop'un teach→test→twist akışını, **sawtooth zorluk eğrisini**, level/wave yapısını tasarla (`references/game-design/02`, `03`, `08`). Level'ları **veri (config/JSON)** olarak modelle — hardcode etme.
3. **İskele:** `flame_game` template'i için VGV `create-project` skill'ini kullan (yoksa `flutter create`). Proje adında çizgi yerine `_`.
4. **Mimari:** `references/flame/10`'daki Bloc + katmanlı strateji. Oyun durumu Bloc/Cubit'te; real-time sim component'lerde; component↔Bloc workspace konvansiyonuyla (mevcut oyunlar `game.gameBloc` doğrudan referansı kullanır).
5. **Sahne/ekran:** menü/level → `RouterComponent`; pause/game-over/HUD → overlays (`references/flame/09`).
6. **Assetler:** görsel + ses **manifest**'i yazıp `scripts/asset_gen.py` ve `scripts/audio_gen.py` ile üret (`references/asset-generation.md`). **Sanat yönü oyunun içeriğine/temasına/hedef kitlesine göre OTOMATİK seçilir** (modern flat, painterly, vektör, cartoon, izometrik, pixel-art… — **pixel-art varsayılan/zorunlu değil**); seçilen stille tutarlı tek bir style-guide belirle ve tüm asset'lere uygula. Stil ne olursa olsun responsive kuralları (`references/responsive-design.md`) geçerli.
7. **Game feel:** her etkileşime juice ekle — feedback, screenshake, hit-stop, easing, ses (`references/game-design/04`). Önce kontrol+mekanik, sonra cila.
8. **Onboarding:** ilk 60 saniyeyi show-don't-tell ile tasarla, tek-mekanik-tanıt (`references/game-design/05`).
9. **Performans:** `onLoad` preload; `update`'te allocation yok; sık nesnelerde pooling; `FpsTextComponent`.
10. **Doğrula:** çalıştırıp gerçek davranışı gözlemle (`run`/`verify`, gerekirse `dart` MCP). Mümkünse taze oyuncuyla playtest, davranışı gözle (`references/game-design/07`).

Ayrıntılı kontrol listeleri: `references/production-standards.md` (**studio-grade çıta / definition-of-done — sert kapı**) + `references/game-design/09-art-ui-identity-and-orientation.md` (**per-game kimlik / anti-reskin — marka testi**) + `references/new-game-checklist.md` (üretim) + `references/level-design-checklist.md` (tasarım).

## Level / wave tasarım kuralları (özet)

- **Level başına tek yeni fikir:** Introduce(güvenli)→Develop→Twist(recombine)→Conclude(ustalık)→at.
- **Zorluk = sawtooth** (lineer değil): tırman → bilerek düşür → tırman; spike'tan sonra relief.
- **Levels-as-data:** tek generic `LevelConfig` + tek loader; per-level kod yok. Real-time oyunda "level" ≈ wave/zone (dalga sayısı, spawn aralığı, HP/hız ölçeği, boss kadansı).
- **Metinle değil geometri/feedback ile öğret;** gözü kontrast + rezerve rehber renk ile yönlendir.
- **Telemetri:** level/wave başına deneme + drop-off'u enstrümante et; veriyle reorder/retune.

## Asset üretimi

İki **generic, manifest-güdümlü** araç skill içinde: `scripts/asset_gen.py` (Vertex `gemini-3-pro-image-preview` ile görsel; opaque veya chroma-key şeffaf webp) ve `scripts/audio_gen.py` (stdlib ile sfx/bgm wav). Her oyuna ayrı betik YAZMA — bir JSON manifest yaz, aracı çalıştır:
`cd scripts && pip install -r requirements.txt && cp .env.example .env` (`.env`'e VERTEX_API_KEY) → `python asset_gen.py --manifest <oyun>.json --out <oyun>/assets/images`. Chroma: özneyle çakışmayan renk (yeşil/cyan özne→`magenta`, kırmızı özne→`green`). Detay/şema: `references/asset-generation.md` + `scripts/README.md`. (`.env` commit edilmez.)

## Component yazım kuralları

- Tek sorumluluk; 200 satır üstü component'i alt component/servise böl.
- `onLoad` async kurulum; `update`/`render` ince ve allocation'sız.
- Anchor'ı bilinçli seç (`Anchor.center` hareket/rotasyon için).
- Çarpışma reaksiyonu component'te değil, mümkünse Bloc event'ine yönlendir.
- Yaşam döngüsü override'larında daima `super` çağır.
