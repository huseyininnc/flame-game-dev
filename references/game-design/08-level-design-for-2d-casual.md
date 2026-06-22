# 2D / Puzzle / Casual / Idle için Level Design (uygulama)

Bu doküman 02 ve 03'teki ilkeleri **kod güdümlü bir motorda (Flutter Flame)** uygular. Bu workspace'in seri üretimi için en pratik dosyadır.

---

## 1. Handcrafted vs procedural

- Sektör puzzle level'larını **ezici çoğunlukla elle tasarlar.** Saf prosedürel üretim genelde imkânsız/trivial/sıkıcı level üretir. Match-3, block-puzzle, merge stüdyoları elle yazar, sonra **veriyle tune eder.**
- Prosedürel; **sonsuz/endless mod** için veya **içerik-asisti** (aday üret → elle ayıkla) olarak uygundur, ana kampanya için değil.

---

## 2. Levels-as-data (motor mimari kuralı)

**Level verisini motor kodundan ayır.** Level'lar config'tir (JSON / Tiled / custom DSL), runtime'da parse edilir — **asla hardcode edilmez.** Böylece tasarımcı yeniden derlemeden iterate eder ve live-ops yeni paketleri **veri olarak** gönderir.

- **Tiled + JSON** de-facto pipeline'dır: Tiled'da görsel tasarla → JSON export → motorda parse. Flame'de `flame_tiled` (bkz. `references/flame/08-audio-and-tiled.md`).
- **Tek generic `LevelConfig` şeması + tek `LevelLoader`** her level'ı sürsün — **parametrik/şablon-tabanlı level'lar** her-level-için-özel-kod'u yener.

**Örnek `LevelConfig` (kavramsal):**
```dart
class LevelConfig {
  final int index;
  final int columns;
  final int rows;
  final ObjectiveType objective;   // collect / clearAll / survive / reachScore
  final int objectiveTarget;
  final int moveLimit;             // veya timeLimit
  final List<BlockerSpec> blockers;
  final List<PieceType> allowedPieces;
  final Map<String, Object> extra; // tür-özel parametreler
}
```
Levelları `assets/levels/levelXXX.json` olarak tut; `LevelLoader.load(index)` parse edip `LevelConfig` döndürsün; component spawn'ı bu config'ten beslensin. Yeni level = yeni JSON; kod değişmez.

---

## 3. Zorluk eğrisi şablonu (casual/puzzle)

- **Sawtooth, lineer değil** (bkz. 03): birkaç level artan zorluk → bilerek **bir düşür** → tekrar tırman. Monoton zorluk churn yaratır.
- **Casual şablonu:** **Level 1–20 kolay** (güven inşa + öğret), **~20–30 ilk hard spike**, kademeli yükseliş, **~50 sonrası büyük zorluk/paywall gate'leri.** Zor level'ı bilinçli yerleştir, ardına bir "ödül" (kolay) level koy.
- Oyuncu becerisi yaşam boyu yükselir: 1–100 numaralı level ile 1000–1100 **aynı efektif zorlukta değildir.** Yeniden kalibre et.

---

## 4. Moves vs objective (match-3 sayıları)

- Modern standart **~15–20 hamle/level** (10 yıl önce ~50'ydi) — oyuncunun zamanına saygı.
- **Hamleyi** birincil zorluk düğmesi olarak tune et; hamle azaldıkça win rate düşer.
- Zorluk indeksi olarak **attempts-per-level (ortalama & medyan)** izle, ikili pass/fail değil.

---

## 5. Elde tuning döngüsü (somut reçete)

- Level'ı kurduktan sonra **~10 kez üst üste oyna.** Kayıplarda kalan hedefi, kazançlarda kalan hamleyi kaydet.
- Kırmızı bayrak: bir denemede **2 reshuffle** = level sorunlu; "zor" level'da sık sık **çok hamle kalmışken kazanmak** = fazla kolay.
- Bütçe: ilk kurulum ~10–20 dk; **final balance level başına ~1 saat** ek tuning/test. **Zorunlu peer review** (ikinci tasarımcı).
- Her level'ı **bir mini-hikâye** gibi kur: tek bir mekanik/öğenin özelliğini (düşme, bloklama, renk reaksiyonu) sergilesin; aynı fikri tekrarlama. **Board şeklini değiştir** ki "aynı level, farklı kaplama" yorgunluğu olmasın.

---

## 6. Veri güdümlü tuning (soft-launch sonrası)

- **Win rate ↔ moves** ilişkisini **shifted negative binomial** ile modelle (shift = gereken minimum hamle). Bir hamle değişiminin WR'a etkisini göndermeden öngörür.
- Modelleme tabanı olarak **"vanilla win rate"** kullan (booster kullanılan denemeleri hariç tut) — oyuncular hamle biterken booster harcar, ham veriyi limit civarında bozar.
- Her rebalance sonrası izlemeye devam (~%1.5 hata/hamle, sık outlier). Canlı veriyle **level sırasını değiştir** ve churn noktalarını (oyuncuların bıraktığı/uninstall ettiği spesifik level'lar) yumuşat.

---

## 7. Tür-özel yapılaştırma

- **Match-3:** ızgara + objective (X topla, jöle temizle, ingredient düşür) + hamle/süre limiti; blocker & booster artan karmaşıklık; çeşitli ızgara şekilleri.
- **Block puzzle:** genelde endless/score-güdümlü, ayrık authored level yerine; zorluk board baskısından emerge eder; "level"lar parametrik (board boyutu, parça havuzu, spawn ağırlığı).
- **Merge:** core = iki düşük öğe → üst tier; ~3 mekanik katmanı; ilerleme per-level-authored değil **unlock/ekonomi-paced.**
- **Idle/incremental:** "level" yoktur; zorluk **ekonomi eğrisinden** gelir (maliyet/üretim formülleri); prestige duvarı pacing'i belirler. Eğri tasarımı = level design'ın bu türdeki karşılığıdır.

---

## 8. Flame'e eşleme (uygulama kuralları)

1. **Tek generic level şeması (JSON), tek loader; per-level kod yok.** (Flame: `assets/levels/*.json` + `LevelLoader`.)
2. Zorluğu küçük bir **parametre setiyle** ayarla (moves, objective target, board şekli, blocker/booster seti, izinli parçalar).
3. Elle yaz; prosedürel'i yalnızca endless mod için.
4. Zorluk = **sawtooth**; 1–20 öğret, ilk spike ~20–30, spike'tan sonra relief level.
5. **Attempts-per-level + drop-off'u ilk günden enstrümante et;** telemetriyle reorder/retune.
6. Her level tek fikir öğretir/sergiler; şekilleri çeşitlendir; her level'ı peer-review et.
7. Real-time aksiyon oyunlarında (örn. Mitomerge tipi merge-defense) "level" ≈ **wave/zone**: dalga sayısı, spawn aralığı, düşman HP/hız ölçeği, boss kadansı = senin LevelConfig'in. Aynı sawtooth + teach-then-test ilkeleri geçerli (yeni düşman/mekaniği güvenli bir dalgada tanıt, sonra kombinle).

---

## Kaynaklar

- Smart & Casual: The State of Tile Puzzle Games Level Design — Game Developer / Room 8: https://www.gamedeveloper.com/design/smart-casual-the-state-of-tile-puzzle-games-level-design-part-1
- Tuning Level Difficulty in Match-3: A Data-Driven Framework — Socialpoint: https://socialpoint-analytics.medium.com/tuning-level-difficulty-in-match-3-games-a-data-driven-framework-7b3cc07b2116
- Match-3 Level Design Principles — Gamigion: https://www.gamigion.com/match-3-level-design-principles/
- Playrix: Creating levels for match-3 — Game World Observer: https://gameworldobserver.com/2019/09/27/playrix-levels-elements-match-3
- JSON Map Format — Tiled docs: https://doc.mapeditor.org/en/stable/reference/json-map-format/
