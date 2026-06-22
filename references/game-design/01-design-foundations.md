# Oyun Tasarımı Temelleri — MDA, Loop'lar, Pillar'lar

Bu doküman, bir oyuna kod yazmadan **önce** netleştirilmesi gereken tasarım çerçevesini verir. Level design (02, 08) ve diğer dokümanlar bu temelin üzerine kurulur.

> Bu bilgi tabanı motor (Flame) değil, **tasarım** bilgisidir. Flame API'si için `references/flame/` KB'sine bak.

---

## 1. MDA Çerçevesi (Mechanics → Dynamics → Aesthetics)

Hunicke, LeBlanc & Zubek'in çerçevesi bir oyunu üç katmana ayırır ve kritik bir gözlem yapar: **tasarımcı ile oyuncu bu katmanları ters yönde okur.**

- **Mechanics (Mekanikler):** Kurallar, oyuncunun yapabildiği her aksiyon, motordaki algoritma ve veri yapıları. **Kodda doğrudan yazdığın tek katman budur.** (Block-puzzle: ızgara boyutu, parça şekilleri, satır-temizleme kuralı, skor formülü, spawn mantığı.)
- **Dynamics (Dinamikler):** Mekaniklerin oyuncu girdisine ve birbirine tepki vererek ortaya çıkardığı **çalışma-zamanı davranışı.** Doğrudan yazılamaz; **emerge eder** (ör. oyuncu büyük combo kurmak için parça biriktirir; "hamle limiti" oyuncuyu planlamaya zorlar).
- **Aesthetics (Estetik / "fun"):** Oyuncuda uyanan **duygusal tepki** — gerçekte hissedilen eğlence.

**Yön (en kritik içgörü):**
- Tasarımcı: **Mechanics → Dynamics → Aesthetics** yazar.
- Oyuncu: **Aesthetics → Dynamics → Mechanics** yaşar.
- Sonuç: Önce bir **his** hedeflersin, sonra geriye doğru çalışıp o hissi üretecek dinamikleri doğuracak mekanikleri bulursun. Mekaniği tune eder, playtest'te istenen estetiğin gerçekten çıkıp çıkmadığını gözlersin.

### "Fun" yerine 8 estetik
"Eğlenceli" belirsizdir; bunun yerine hedef estetiği adlandır:

1. **Sensation** — duyusal haz (juicy feedback, partikül, ses, screenshake).
2. **Fantasy** — rol/inanış.
3. **Narrative** — dram, hikâye itkisi.
4. **Challenge** — engel/ustalaşma, tekrar oynanabilirlik. *(Çoğu puzzle oyununun ana sürücüsü.)*
5. **Fellowship** — sosyal çerçeve (multiplayer, leaderboard).
6. **Discovery** — keşif, yeni mekanik bulma.
7. **Expression** — kendini ifade, özelleştirme.
8. **Submission** — zaman geçirme, rahat/otomatik oynanış. *(Casual-puzzle'ın çekirdek estetiği — "otobüste oynanır".)*

**Nasıl kullanılır:**
- Kod yazmadan önce **2–3 hedef estetik** yaz, öncelik sırasıyla (ör. block-puzzle = **Challenge + Submission + Sensation**). Bu senin **kesme filtrendir**.
- Bir mekanik önerildiğinde sor: *hangi dinamiği yaratıyor, o dinamik hangi estetiğe hizmet ediyor?* Hedef estetiklerden hiçbiri değilse → **kes**.
- Playtest "ters" hissettiriyorsa, mekaniğe dokunmadan önce **dinamik katmanında teşhis koy** (hangi davranış emerge etti?). Aynı mekanik, küçük parametre değişikliğiyle farklı dinamik üretir.
- Not: 8 estetik "keyfi bir liste"dir ve MDA mekaniği fazla öne çıkarabilir. Yasa değil, **düşünme aracı** olarak kullan.

---

## 2. Loop'lar: Core / Meta / Session

- **Core loop (çekirdek döngü):** Birincil deneyim olarak tekrarlanan an-be-an aksiyon zinciri (eşleştir / birleştir / vur / inşa et). **Oyuncuyu 5 dakika tutar.**
- **Meta loop:** Çekirdeğin etrafına sarılan uzun-vadeli hedefler (unlock, hikâye, prestige, koleksiyon). **Oyuncuyu 5 ay tutar.**
- **Session loop:** Tek bir oturumun baştan sona şekli (giriş kancası → birkaç yükselen beat → tatmin edici doruk → bir sonrakine çekecek küçük yüksek nokta).

**Kurallar:**
- **Core loop'u tek cümleyle özetle**; 5 saniyelik bir videoda okunur olsun. Olmuyorsa fazla karmaşıktır.
- Core loop'u **kısa, basit, anında anlaşılır** tut; ikincil sistemler oynanışı çekirdekten KOPARMASIN.
- Meta, çekirdeği **pekiştirsin** (dağıtmasın): her meta ödülü oyuncuyu bir sebeple çekirdeğe geri göndersin.
- Katmanları bilinçli kur: core → dual loop (çatallanan seçim) → nested loop (çekirdeğe dönen yan yol) → compulsion loop (alışkanlık kancaları).

Tür şablonları için → `06-progression-economy-retention.md`.

---

## 3. Design Pillars (Tasarım sütunları)

3–5 kısa kelime/öbek; oyunun hedef duygularını/deneyimini yakalar (doğrudan MDA estetiklerine eşlenir). Her sonraki karar bunlara karşı sınanır: bir sütunla çelişen özellik **kötü tasarımdır, kesilir.**

- **Non-goals** da yaz: oyunun açıkça NE OLMAYACAĞI.
- Pillar'lar tek-sayfalık tasarımın (bkz. `07-professional-process.md`) çekirdeğidir ve scope creep'e karşı en güçlü kalkandır.

Örnek (Mitomerge): *Sürükle-birleştir tatmini · Kısa otururumda anlamlı ilerleme · Bırakınca da çalışan savunma (idle) · Okunur, sade biyo-estetik.*

---

## 4. Game Feel / "Juice" (kısa giriş)

Mekanik doğru çalıştıktan **sonra** eklenen tatmin katmanı. Her oyuncu etkileşimi anında, çok-duyulu geri bildirim üretmeli. Ayrıntılı teknik liste (screenshake, hit-stop, squash&stretch, easing) → `04-game-feel-and-juice.md`.

Altın kural: **"Tatsız meyveden iyi suyu çıkmaz."** Önce kontrol ve çekirdek mekanik; sonra cila.

---

## Sürecin altın sıralaması (özet)

1. Hedef **estetikleri** seç (MDA) → kesme filtresi.
2. **Pillar'ları** + non-goal'ları yaz (tek sayfa).
3. **Core loop**'u tek cümleye indir; meta'yı çekirdeği pekiştirecek şekilde tasarla.
4. **Prototiple** "fun"ı bul (bkz. 07), sonra üret.
5. **Level design** ile öğretme/zorluk eğrisini kur (02, 03, 08).
6. **Juice + playtest + telemetri** ile cilala ve ayarla (04, 07).

---

## Kaynaklar

- MDA: A Formal Approach to Game Design — Hunicke, LeBlanc, Zubek: https://www.researchgate.net/publication/228884866_MDA_A_Formal_Approach_to_Game_Design_and_Game_Research
- MDA framework — Wikipedia: https://en.wikipedia.org/wiki/MDA_framework
- The 8 Kinds of Fun — Skeleton Code Machine: https://www.skeletoncodemachine.com/p/the-8-kinds-of-fun
- The Chemistry of Game Design — Daniel Cook: https://lostgarden.com/2007/07/19/the-chemistry-of-game-design/
- What is a Core Loop in a Mobile Game? — Homa Games: https://www.homagames.com/blog/what-is-a-core-loop-in-a-mobile-game
- The Art of Game Design (interest curve, pacing) — Jesse Schell (notes): https://notesbylex.com/the-art-of-game-design-a-book-of-lenses-2nd-edition-by-jesse-schell
