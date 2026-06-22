# Progression, Ekonomi & Retention

Kârlı 2D mobil oyunlar (casual / hypercasual / hybrid-casual / idle) için. Loop tanımları → `01-design-foundations.md`. Monetizasyon/ASO iş tarafı game-greenlight skill'inde.

---

## 1. Loop'lar ve tür şablonları

- **Core loop** 5 dakika, **meta loop** 5 ay tutar (bkz. 01).
- **Session loop:** bir oturumun şekli; **oyuncuyu daha fazlasını isteyerek bırakacak** biçimde bitir.

**Tür şablonları:**
- **Hypercasual:** Core = tek tap/swipe → skor. Meta minimal (tema unlock, high score). (Stack: oyna → diamond → tema aç.)
- **Puzzle/match:** Core = eşleştir → kaynak. Meta = harca → yenile/inşa + anlatı (Homescapes).
- **Idle/incremental:** Core = tap/bekle → kazan → upgrade → daha hızlı kazan. Meta = **prestige** reset'leri kazanç çarpanı.
- **Merge:** Core = iki düşük öğeyi birleştir → üst tier → yeni zincir. Meta = board genişletme, sipariş, koleksiyon.
- **Builder/strategy:** Core = topla → inşa et → savaş → daha çok topla. Meta = base ilerleme, guild.

---

## 2. Progression sistemleri

İçeriği gate'leyen ve sürekli ilerleme hissi veren "tur rehberi"; sunk-cost yatırımı yaratır.

**Türler (birkaçını karıştır):** linear/vertical (power) · branching (skill tree, agency) · horizontal (güç artırmadan çeşitlilik: kozmetik, yeni mekanik) · collection/achievement/leaderboard/guild/narrative/building/time-gated.

**Kurallar:**
- Progression'ı **çekirdek mekanikle hizala** — onu uzatsın, rakip olmasın.
- **Unlock cadence = beklenti.** Heyecanlı içeriği "hemen köşede" tut; her zaman yakın-vadeli hedef olsun.
- **Mastery arc'ını yönet:** pre-mastery (hüsran) → mastery (zirve eğlence) → burnout (sıkıntı). Mevcut beceri trivial olmadan **önce** yeni skill atom tanıt; eğlenceyi sabrı aşan grind'in arkasına gizleme.
- **Görünür milestone'lar:** progress bar, level no, achievement listesi.
- **Skill vs grind dengesi:** progression skill'i alakasız kılmasın (Fortnite Battle Pass kozmetik tutar).
- **Prestige loop'ları** uzun ömür için (idle'ın D30 derinliği): ilerlemeyi kalıcı çarpan için sıfırla.

---

## 3. Reward schedule'ları (alışkanlık psikolojisi)

| Schedule | Tetik | Etki | Örnek |
|---|---|---|---|
| **Fixed ratio** | N aksiyon sonrası | Öngörülebilir | Satır başına Tetris puanı |
| **Variable ratio** | Rastgele sayıda aksiyon sonrası | **En güçlü alışkanlık; bırakmaya en dirençli** | Loot/drop, crit, gacha, merge sürprizi |
| **Fixed interval** | Sabit südede bir | Öngörülebilir, oturum pacing | Günlük login, +24s bonus |
| **Variable interval** | Rastgele zamanlarda | Tek başına nadir | Sürpriz bonus |

**Kurallar:** çekirdek heyecan (loot, crit, merge sürprizi) için **variable-ratio**; alışkanlık/randevu (günlük ödül, enerji) için **fixed-interval**. Katmanla (günlük login = fixed-interval, içinde random loot = variable-ratio) ama test et. Ödül tipini ihtiyaca eşle (soft = ilerleme, hard = premium/hız, kozmetik = ifade, power = vertical, narrative = duygu). **Ödül anını juicy yap** (ses/partikül/animasyon). Daily reward + streak loss-aversion'ı kullanır — etik sınırda (bkz. §6).

---

## 4. Ekonomi tasarımı

**"Enflasyon, ekonomi tasarımcısının düşmanıdır."** İş, para birimlerini sürekli **arzulanır** tutmak.

- **Soft currency:** oyunla kazanılır (coin); kaynak: login, hedef, performans, idle. Geniş harcama: upgrade, item.
- **Hard/premium currency:** parayla alınır (gem); hız/exclusive/timer-skip.
- **Dual-currency:** ödemeyen sabırla, ödeyen hızla ilerler; ikisi de aynı içeriğe ulaşır.

**Sources (faucet):** login, level/hedef, **idle/offline kazanç**, reklam ödülü, event.
**Sinks (drain):** power item, kozmetik, exclusive, timer skip, retry/continue.

**Kurallar:** faucet↔sink dengesi — yeterince biriksin ki anlamlı harcansın, ama o kadar çok değil ki satın alma anlamsızlaşsın. **Ekonomiyi göndermeden önce tabloda modelle** (level-up başına gereken oynama, oturum başına kazanç/harcama; günler/haftalar simüle et). Enflasyona karşı **bilinçli sink** ekle (uzun upgrade merdiveni, kozmetik, prestige). **Idle/offline kazanç = comeback hook** (genelde birkaç saatle cap'li; cap'in kendisi dönüş-sıklığı kaldıracı).

---

## 5. Retention metrikleri & sürücüleri

**Benchmark (UA maliyetleriyle yükseliyor):** klasik D1 %40 / D7 %20 / D30 %10; artık D1 %50+ çıta. Tür: hypercasual ~D1 %38–40, D30 ~0; hybrid-casual ~D1 %35–45 / D7 ~%20 / D30 ~%10. **D1 matematiksel olarak D7/D30'a tavan koyar; D30 uzun-vade sağlığının ana göstergesi.**

- **D1 (ilk izlenim):** onboarding kalitesi, hızlı time-to-fun, net rehberlik, az friction, doğru kitle (UA hedefleme). Kötü D1'in 4 kökü: fun bulunmamış · oyuncu fun'a yönlendirilmemiş · çok engel · yanlış kitle.
- **D7 (orta oyun):** ödüllendiren progression/meta (event, PvP, sezon), iyi içerik pacing (ne tükenmiş ne grind), sosyal.
- **D30 (yaşam tarzı entegrasyonu):** meta derinliği (ekonomi, sosyal, kompleks sistemler), içerik çeşitliliği + limited-time event, sosyal baskı, biriken yatırım (sunk cost).

**Session & comeback:** enerji/timer sistemi oturumu paslar (~5–20 dk, 4–8 saatte bir; öğle/akşam ritmine oturur). Comeback hook'ları: offline/idle kazanç, daily reward, streak, enerji refill, limited-time event. **Yokluğu cezalandırmak yerine dönüşü ödüllendir** (daha sağlıklı çekim).

---

## 6. Etik (ve 2025+ regülasyon baskısı)

- **Dark pattern'lerden kaçın:** core challenge'ı pay-to-skip, zorunlu grind, "randevuyla oynama" (yokluğu cezalandırma), opak para birimi, kumara benzeyen loot box, sosyal zorlama.
- UK/EU 2025'te bunları tüketici-koruma altında incelemeye başladı (özellikle loot box ve gizlenmiş para çevrimi, genç kitle).
- **Sağlıklı alternatif:** yokluğu cezalandırmak yerine varlığı ödüllendir; şeffaf para/odds; cömert offline kazanç; opsiyonel (zorunlu değil) enerji; oyuncu zamanına saygılı progression. Etik retention + kârlılık çelişmez (resentment-churn ve regülasyon riskini düşürür).

---

## Kaynaklar

- Reward Schedules and When to Use Them — Game Developer: https://www.gamedeveloper.com/business/reward-schedules-and-when-to-use-them
- Power Progression in Games — Game Developer: https://www.gamedeveloper.com/design/power-progression-in-games-crafting-rewarding-player-experiences
- Progression Systems in Mobile Games — Udonis: https://www.blog.udonis.co/mobile-marketing/mobile-games/progression-systems
- The True Drivers of D1, D7, D30 Retention — Solsten: https://solsten.io/blog/d1-d7-d30-retention-in-gaming
- Building a Lasting Free-to-Play Economy — Mobile Free To Play: https://mobilefreetoplay.com/bible/building-lasting-free-play-economy/
- Game Economy Design in F2P — Machinations: https://machinations.io/articles/game-economy-design-free-to-play-games
- A Game of Dark Patterns — ACM: https://dl.acm.org/doi/fullHtml/10.1145/3491101.3519837
