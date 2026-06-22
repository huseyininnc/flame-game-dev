# Studio-Grade Production Standards (ZORUNLU ÇITA)

> **Bu skill amatör, kısa, "MVP-as-product", tek-mekanik tech-demo oyunlar ÜRETMEZ.** Üretilen her oyun; 15+ yıllık kıdemli ekiplerin çalıştığı büyük bir stüdyodan çıkmış gibi — **production-ready, içerik-zengin, çok-asset'li, tam sürüm** olmalıdır. Bu doküman çıtayı ve "definition of done"u tanımlar; maddeleri **release blocker** sayılır.

**Temel tez:** Profesyonel kalite tek bir büyük şey değildir — amatörün tek tek atladığı **onlarca küçük cila katmanının toplamıdır.** MVP/prototip yalnızca preproduction'da "fun"ı bulmak içindir; **teslim edilen ürün her zaman tam, cilalı, içerik-zengin** olmalı. "Tatsız meyveden iyi su çıkmaz" — cila sağlam çekirdeği büyütür, yerini tutmaz.

---

## 1. İçerik scope tabanları (launch'ta minimum)

Prototip bir mekaniği 2–5 dk'da kanıtlar. Tam oyun **saatlerce yapılandırılmış ilerleme** sunar — başlangıç/orta/geç oyun. Fark: **doğrulanmış içerik hacmi + onu besleyen sistem treadmill'i.**

| Tür | Launch içerik tabanı | Not |
|---|---|---|
| **Match-3 / puzzle** | **100–200 elle kurulmuş level** | Candy Crush Soda 150 ile çıktı; 100+ "gerçek" puzzle için inandırıcı minimum |
| **Hybrid-casual (arena/aksiyon)** | **3–5 ayrı mekanik** + 1 ilerleme omurgası + 1 meta katman; tekrara düşmeden 30–60 dk | Tek mekanik = hypercasual = ince |
| **Idle / incremental** | **40–60 saat içerik**, **2–4 prestige katmanı**, **30–50 upgrade/node**, skill tree | Her prestige katmanı yeni MEKANİK açsın, sadece büyük sayı değil |
| **Wave / arena defense** | **3+ biome/tema**, **8–15 düşman/birim tipi**, artan dalga kompozisyonu | Tek düşmanın reskin'i = demo |

**Kurallar:**
- **Başlangıç + orta + GEÇ oyun gönder.** Güçlü D1 + sert D7 düşüşü = "çekirdek loop ötesinde içerik derinliği yok" imzası. Geç-oyun sistemleri (prestige, mastery, endless, koleksiyon) D30 üretir.
- **Reskin değil, ayrı mekanikler.** Öğrenilecek yeni "şeyler" erken oyun boyunca sürekli gelsin (Royal Match her 1–3 level'da yeni blocker/power-up tanıtır).
- **Koleksiyon/set** uzun-kuyruk kancası olarak.
- **Lansman sonrası kadans:** her **1–2 haftada** yeni içerik (industry ritmi); rotasyonlu event arketipleri (competitive / recurring / collectible).

---

## 2. Tam sistem yığını (Definition of Done — MVP değil)

MVP çekirdek loop'u kanıtlar. **Tam oyun aşağıdaki destek sistemlerinin HEPSİYLE çıkar.** ★ = launch'ta zorunlu; diğerleri scaffold'u launch'ta olmak kaydıyla fast-follow olabilir.

**Çekirdek:** ★ core loop · ★ level/wave/stage ilerleme omurgası · ★ zorluk eğrisi/dinamik tuning.
**Meta ilerleme:** ★ player level/XP/mastery · ★ kalıcı upgrade/unlock yolu · prestige/rebirth (idle'da ★) · koleksiyon/album/set.
**Ekonomi & monetizasyon:** ★ en az **2 para birimi** (soft+hard) · ★ shop/IAP (server doğrulama) · ★ ads mediation (rewarded çekirdek; interstitial oyuncu kancalandıktan SONRA) · battle/season pass · LTO · monetization streak.
**Engagement/retention:** ★ daily reward/login streak · ★ tutorial/FTUE (en büyük D1 kaldıracı) · events sistemi · achievements · leaderboard/sosyal.
**Altyapı:** ★ settings (audio/dil/privacy) · ★ save/persistence (+cloud şiddetle önerilir) · ★ analytics + funnel enstrümantasyonu (tutorial adım-adım drop-off zorunlu) · A/B test harness.

**Launch must-have özeti:** core loop + ilerleme omurgası + 2 para birimi + shop/IAP + ads mediation + daily reward + FTUE + settings + save(+cloud) + analytics. Battle pass/events/leaderboard/achievement fast-follow olabilir ama **soketleri launch'ta dursun** (live-ops üzerine inşa edilebilir sistem ister).

**Staggered onboarding (her şeyi birden dökme):** ~**20 level saf eğlence**, sonra ilk live-op/monetizasyon. Monetize etme hakkını kazan. Kalıcı ödül kaynağı eklemek **rebalance gerektirir** (enflasyon); source ve sink'i birlikte tasarla.

---

## 3. Cila / game-feel çıtası (asıl ayrım)

Amatör ile profesyonel arasındaki *en yüklü* fark. Aşağıdaki katmanları **her etkileşime** uygula (detay: `references/game-design/04-game-feel-and-juice.md`).

- **Her şeye easing** (lineer/snap yok): pozisyon, scale, rotasyon, renk, opacity tween'le (Flame `EffectController`+curve). · **Hit-stop / freeze** (~30–80ms) güçlü darbede. · **Screenshake** olaya ölçekli, decay'li (sabit/aşırı değil). · **Knockback + recoil** (iki yönlü). · **Camera lerp + kick.** · **Anticipation + follow-through.** · **Secondary motion** (trail, jiggle, debris). · **Permanence** (kalıcı izler). · **Her aksiyona ses** + **haptics** (mobil). · partikül/VFX olaya ölçekli ve randomize.

**Görsel tutarlılık (en büyük amatör tell = tutarsızlık):**
- **Tek style guide, zorunlu:** kilitli palet, tek ışık yönü, tutarlı oran/PPU, tutarlı ikon dili. · **Placeholder/programmer-art/varsayılan font YOK.** · Karışık stil (asset-store + custom, pixel + smooth-vector) = bozuk okunur. · Her şeyde animasyon (idle, giriş/çıkış, anticipation). · Güçlü silüet + kontrast (okunabilirlik).

**UI/UX cila:** ekranlar arası **animasyonlu geçiş** (hard-cut yok) · tek design system · juicy buton (press/release/ses/haptic/disabled/loading) · tüm durumlar (default/press/disabled/loading/empty/error) · varsayılan/temasız widget yok · dokunma hedefi büyük & thumb-zone.

**Audio:** her etkileşimde ses · katmanlı + pitch-randomize SFX · adaptive/looping müzik + crossfade · mixing/ducking · Music/SFX ayrı volume + sessiz-mod saygısı.

**"Profesyonel hissi" — ölçülebilir hedefler:**
- **Input latency:** 60fps'te ≤ **66ms**; asla > **133ms** (aksiyon). İlk feedback < **100ms**.
- **Kilitli 60 FPS** (yavaş/turn-based değilse), jank/GC-stall yok. Sabit 30 > titreyen 45–60.

---

## 4. Launch-readiness checklist (release blocker)

**Stabilite:** crash-free session ≥ **%99.7** (crash ≤ %0.3) · Google Play vitals: user-perceived crash < **%1.09**, ANR < **%0.47** · FTUE/ilk 15 dk yolunda sıfır crash · uzun oturumda memory-leak/OOM yok · crash reporting (symbolicated) çalışıyor.
**Performans:** kilitli hedef fps mid-tier cihazda tutuyor · cold start birkaç sn, level geçişi mümkünse <1sn (>1sn ise loading göstergesi) · memory bütçesi, büyüme (leak) eğrisi yok · battery/thermal throttling yok · >150MB ise App Bundle.
**Cihaz kapsamı:** low/mid/high tier, çoklu ekran/aspect/notch/OS · portrait/landscape doğru · Play Pre-launch report temiz.
**Store assets:** icon 512×512 (≤1024KB) · ≥2 (4+ önerilen) screenshot, ilk 2–3 dönüşüm sürücüsü · feature graphic · preview video 30–120sn · keyword-optimize başlık/açıklama (ASO).
**Rating/privacy:** içerik/yaş rating · aktif **privacy policy URL** (veri toplanmasa bile) · Data Safety / ATT · IAP açıklama + "restore" test.
**Erişilebilirlik (sayısal):** dokunma hedefi ≥ **48dp (Android) / 44pt (iOS)** · renk-tek-başına bilgi taşımaz (şekil/ikon/desen) · metin ölçeklenir (OS dynamic type) · **reduce-motion** seçeneği, flashing yok · caption/subtitle (özelleştirilebilir) · SFX/Music/speech ayrı ses · TalkBack/VoiceOver menüde doğrulandı.
**Lokalizasyon:** tüm string externalize (Flutter ARB) · UTF-8 + locale formatlama · metin genişlemesi toleransı (+%30–40 DE) · RTL (Arapça/İbranice, `Directionality`) · font kapsamı (tofu yok) · pseudo-localization pass.
**QA & telemetri:** alpha=feature-freeze → beta=content-freeze · regression (fps/memory/load sayısal) her build · soft-launch (sınırlı geo) ile D1/D7/D30 + funnel okunur · event taksonomisi (progression/economy/business/error) + FTUE funnel + app-version tag · A/B harness (remote config).
**Live-ops:** remote config (balance/pricing/FTUE/flag client güncellemesiz) · data-driven content pipeline · event kadansı (ekibe göre; 72 saat Cuma–Pazar altın pencere) · rollback/kill-switch + staged rollout.

---

## 5. Scope disiplini: hırslı AMA bitirilebilir

Hacmi boğulmadan üretmenin yolu **el-işçiliği değil, sistemler**:
- **Data-driven content:** level/wave/düşman/upgrade'i **config (veri)** olarak tanımla, kod değil. Motoru bir kez kur; içeriği sonsuza dek veri olarak dök. (Bkz. `references/game-design/08-level-design-for-2d-casual.md`.)
- **Parametrik/şablon içerik:** level config'lerini parametrik modelden üret ("level design as a service").
- **Yeniden kullanılan sistemler:** tek event framework (competitive+recurring+collectible), tek currency, tek shop, tek reward dispenser — parametreli.
- **Modüler içerik:** biome = palet-swap + yeni data; yeni düşman = data satırı + sprite, yeni kod yolu değil.
- **KPI hedefi koy** (retention/funnel), data-inspired drift'ten kaçın.
- **Polish bütçesini koru:** sabit faz olarak planla (≥ ~2 ay eşdeğeri emek); içerik üretimi onu yemesin.

**Üretim sırası:** vertical slice (near-final kalite, prototip değil) → content production (alpha=tüm özellik var) → **korunmuş polish** → soft launch (D1/D7/D30 oku, iterate) → launch (RC → gold).

**Tek-satır scope formülü:** Yeniden-kullanılır, data-driven sistemleri vertical-slice kalitesine getir; sonra modüler içeriği veri olarak launch hacmine dök (ör. 100–200 puzzle level / 3–5 mekanik / 40–60 idle saat / 8–15 düşman+3 biome); must-have sistem yığınıyla sar; meta/monetizasyonu stagger'la (~20 level önce eğlence); 1–2 hafta kadansla besle.

---

## 6. Amatör tell'leri (KESİNLİKLE kaçın)

- Varsayılan font/arka plan · karışık/uyumsuz sanat · shipped build'de placeholder/programmer-art · tutarsız ışık/palet · snap'leyen statik sprite · düşük kontrast/zayıf silüet.
- Lineer/snap hareket (easing yok) · ağırlıksız darbe (hit-stop/knockback/shake yok) · rigid 1:1 kamera · iz bırakmayan dünya · ya hiç juice ya aşırı shake.
- Hard-cut ekran geçişi · temasız/varsayılan widget · statik/sessiz buton · boş/donmuş loading/dead-end error · küçük dokunma hedefi.
- Sessiz etkileşim · tek tekrar eden klip · hard-restart müzik · ses ayarı yok · düz/clipping mix.
- Ölçülmemiş/>133ms latency · titreyen fps/jank · feedback yok · metin-duvarı/yok onboarding · ölü mikro-etkileşim.
- **Tek mekanik + birkaç ekran "tam oyun" diye gönderilmiş** (demo smell) · sadece "başlangıç" oyun, orta/geç yok · içerik çeşitliliği yok.

---

## Kaynaklar

- The Art of Screenshake — Vlambeer (Jan Willem Nijman): https://www.youtube.com/watch?v=AJdEqssNZ-U
- Juice It or Lose It — Jonasson & Purho: https://www.youtube.com/watch?v=Fy0aCDmgnxg
- Measuring Responsiveness in Video Games (latency) — Game Developer: https://www.gamedeveloper.com/design/measuring-responsiveness-in-video-games
- Mobile Game Testing Checklist for Pre-Launch — Kobiton: https://kobiton.com/guides/mobile-game-testing-checklist-pre-launch-success/
- Understand your pre-launch report — Google Play Console: https://support.google.com/googleplay/android-developer/answer/9844487
- 2025 Mobile Gaming Benchmarks — GameAnalytics: https://www.gameanalytics.com/reports/2025-mobile-gaming-benchmarks
- Full list — Game Accessibility Guidelines: https://gameaccessibilityguidelines.com/full-list/
- App Screenshot/Icon/Video Guidelines (iOS & Android) — AppTweak: https://www.apptweak.com/en/aso-blog/app-screenshot-icon-video-guidelines-ios-gp
- App Localization Best Practices — Circle Translations: https://circletranslations.com/blog/app-localization-best-practices
- Why does Royal Match wait 22 levels for the first live-op? — Gamigion: https://www.gamigion.com/why-does-royal-match-wait-22-levels-to-introduce-their-first-live-op/
- Converging Live Ops Trends in Mobile Puzzle — Naavik: https://naavik.co/digest/live-ops-trends-powering-mobile-puzzle/
- Getting Started With Hybrid-Casual LiveOps — Supersonic: https://supersonic.com/learn/blog/getting-started-with-basic-hybrid-casual-liveops
- The True Drivers of D1, D7, D30 Retention — Solsten: https://solsten.io/blog/d1-d7-d30-retention-in-gaming
- Game Production Pipeline — GDKeys: https://gdkeys.com/game-development-process/
- Is data-driven design good for games? — Paolo's Blog: https://paolos.blog/data-driven-designed-games/
