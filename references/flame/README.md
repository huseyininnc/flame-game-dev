# Flame Engine — Bilgi Tabanı (Knowledge Base)

Bu klasör, Flutter **Flame** oyun motoruyla seri (çok sayıda, farklı konseptte) oyun üretmek için derlenmiş referans dokümanlarını içerir. Tüm içerik resmi Flame dokümanları, pub.dev API referansları ve flame_bloc kaynak kodundan doğrulanmıştır.

> Hedef sürümler: **flame `^1.37.0`**, **flame_audio `^2.12.1`**, **flame_tiled `^3.1.1`**, **flame_bloc** (mevcut API).
> Önemli API değişimleri: `Camera` → `CameraComponent` + `World`; `Tappable`/`Draggable` → `TapCallbacks`/`DragCallbacks`; `HasGameRef` → `HasGameReference`.

## İçindekiler

| # | Dosya | Konu |
|---|---|---|
| 01 | [01-overview-and-setup.md](01-overview-and-setup.md) | Kurulum, `GameWidget`, `FlameGame`, oyun döngüsü, asset yapısı |
| 02 | [02-components-and-lifecycle.md](02-components-and-lifecycle.md) | FCS, `PositionComponent`, yaşam döngüsü, mixin'ler (`HasGameReference` vb.) |
| 03 | [03-rendering-sprites-text.md](03-rendering-sprites-text.md) | `Sprite`, `SpriteComponent`, sprite sheet, animasyon, `TextComponent` |
| 04 | [04-input-and-gestures.md](04-input-and-gestures.md) | `TapCallbacks`, `DragCallbacks`, klavye, `JoystickComponent`, `HudButtonComponent` |
| 05 | [05-effects-and-particles.md](05-effects-and-particles.md) | `Effect`, `EffectController`, `SequenceEffect`, partikül sistemi |
| 06 | [06-collision-detection.md](06-collision-detection.md) | `HasCollisionDetection`, hitbox'lar, `CollisionType`, quad-tree, raycast |
| 07 | [07-camera-world-viewport.md](07-camera-world-viewport.md) | `CameraComponent`, `World`, viewport/viewfinder, HUD, fixed-resolution |
| 08 | [08-audio-and-tiled.md](08-audio-and-tiled.md) | `flame_audio` (sfx/bgm/AudioPool), `flame_tiled` haritalar |
| 09 | [09-overlays-router-state.md](09-overlays-router-state.md) | Overlays, `RouterComponent`, oyun durum akışı |
| 10 | [10-architecture-bloc-multigame.md](10-architecture-bloc-multigame.md) | `flame_bloc`, katmanlı mimari, çok-oyunlu monorepo stratejisi |
| 11 | [11-performance-optimization.md](11-performance-optimization.md) | 60 FPS, preloading, object pooling, `RecycledQueue`, FPS ölçümü |

## Nasıl kullanılır

- Yeni bir oyun başlatırken önce **01**, **02**, **10** dosyalarını okuyun (kurulum + mimari iskelet).
- Üretim sırasında ilgili konunun dosyasına başvurun.
- Bu bilgi tabanı ayrıca `flame-game-dev` Claude Code skill'i ile birlikte kullanılır — skill, bu dokümanları üretim kuralları olarak referanslar.
