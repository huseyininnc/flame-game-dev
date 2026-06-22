# Oyun Tasarımı & Level Design — Bilgi Tabanı (Knowledge Base)

Bu klasör, **profesyonel oyun geliştirme süreçleri** ve **level design** için derlenmiş referans dokümanlarını içerir. İçerik; GDC konuşmaları, Game Maker's Toolkit, The Level Design Book, Nintendo/Valve tasarım felsefesi, Jesse Schell (*The Art of Game Design*), Steve Swink (*Game Feel*), MDA makalesi (Hunicke/LeBlanc/Zubek), Daniel Cook, ve casual/mobil sektör kaynaklarından (Game Developer/Gamasutra, Socialpoint, Mobile Free To Play vb.) derinlemesine internet araştırmasıyla doğrulanmıştır.

> Bu KB **tasarım** bilgisidir (ne ve neden). Motor/teknik (nasıl, Flame API) için kardeş KB: `references/flame/`.
> `flame-game-dev` skill'i bu iki KB'yi de üretim kuralı olarak referanslar.

## İçindekiler

| # | Dosya | Konu |
|---|---|---|
| 01 | [01-design-foundations.md](01-design-foundations.md) | MDA, 8 estetik, core/meta/session loop, design pillars, juice (giriş) |
| 02 | [02-level-design-principles.md](02-level-design-principles.md) | **Level design çekirdeği:** introduce/develop/twist/conclude, Kishōtenketsu, teach-then-test, signposting/affordance, gating/locks&keys, level-içi pacing, blockout süreci, sık hatalar |
| 03 | [03-difficulty-and-pacing.md](03-difficulty-and-pacing.md) | Flow channel, sawtooth/fractal eğri, difficulty spike, interest curve, intensity ramp, DDA, balancing |
| 04 | [04-game-feel-and-juice.md](04-game-feel-and-juice.md) | Swink 3 sütun, juice checklist (screenshake, hit-stop, squash&stretch, easing, ses) |
| 05 | [05-onboarding-and-tutorialization.md](05-onboarding-and-tutorialization.md) | FTUE, show-don't-tell, skill atom, progressive disclosure, time-to-fun |
| 06 | [06-progression-economy-retention.md](06-progression-economy-retention.md) | Core/meta loop tür şablonları, progression, reward schedule, ekonomi (soft/hard, source/sink, idle), D1/D7/D30, etik |
| 07 | [07-professional-process.md](07-professional-process.md) | Yaşam döngüsü, prototip vs vertical slice, milestone'lar (alpha/beta freeze), lean GDD, playtest/iterasyon, scoping (MVP/MoSCoW) |
| 08 | [08-level-design-for-2d-casual.md](08-level-design-for-2d-casual.md) | **2D/puzzle/casual/idle uygulaması:** levels-as-data (JSON/Tiled, LevelConfig), sawtooth şablonu, match-3 tuning, telemetri, Flame eşlemesi |
| 09 | [09-art-ui-identity-and-orientation.md](09-art-ui-identity-and-orientation.md) | **Per-game kimlik (ZORUNLU):** HUD diegesis, türe-göre HUD düzeni, tipografi (3 rol/font üçlüsü), görsel kimlik 5 sütun, orientation (portrait/landscape) seçimi, anti-reskin checklist |

## Nasıl kullanılır

- **Yeni oyundan önce (game-greenlight ile birlikte):** 01 (pillar/estetik/loop) + 07 (scope/prototip).
- **Level/wave/zorluk tasarlarken:** 02 + 03 + 08 (en kritik üçlü).
- **Cila ve tutundurma:** 04 (juice) + 05 (onboarding) + 06 (progression/retention).
- Bu KB ayrıca `flame-game-dev` Claude Code skill'i ile kullanılır; skill bu dokümanları üretim kuralları olarak referanslar.
