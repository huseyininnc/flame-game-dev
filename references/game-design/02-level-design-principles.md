# Level Design İlkeleri

Level design = **oyuncuyu, mekaniği pekiştiren mekânlar/durumlar aracılığıyla aksiyon almaya motive etme** sanatı. Görsellik değil; layout, encounter (karşılaşma) ve **akış (flow)** ile ilgilidir. Bu doküman bu workspace'in level design üretim kurallarıdır.

> 2D/casual/puzzle'a özel uygulama (levels-as-data, zorluk şablonu, tuning) → `08-level-design-for-2d-casual.md`. Zorluk eğrisi/pacing teorisi → `03-difficulty-and-pacing.md`.

---

## 1. Level döngüsü: Introduce → Develop → Twist → Conclude

Nintendo'nun (Koichi Hayashida; Batı'da Mark Brown/GMTK ile yaygınlaşan) tek-mekaniğe dair tekrar kullanılabilir yapısı. **Bir level = bir çekirdek fikir.**

1. **Introduce (Tanıt):** Yeni mekanik **güvenli, sonuçsuz** bir alanda belirir; oyuncu ölemez, deneyerek keşfeder.
2. **Develop (Geliştir):** Aynı mekanik, biraz daha karmaşık senaryo / hafif risk.
3. **Twist (Çevir):** Mekaniği yeniden bağlamlandır — ters çevir, başka bir öğeyle eşle; oyuncuyu "yeniden düşünmeye" zorla. ("Onları şaşırtan bir doozy.")
4. **Conclude (Ustalaşma):** Genelde hedeften hemen önce, öğretilen beceriyi **kanıtlatan** final challenge. Sonra mekaniği **at** — sıradaki level yeni bir fikir tanıtır.

**Kurallar:**
- Bir level'da **birden fazla yeni mekanik istifleme.**
- Bir mekanikle ilk karşılaşma **fail edilemez** olmalı.
- Zorluğu **recontextualize ederek** artır (twist), alakasız zorluk yığarak değil.
- Her fikri, o beceriyi **gerektiren** bir "zafer turu" ile bitir = senin sınavın.
- Fikir tamamlanınca **oyuncağı çöpe at**; aynı mekaniği yaydan sonra tekrar tekrar kullanmak padding hissi verir.

> Etiketler (introduce/develop/twist/conclude) Mark Brown'ın çerçevelemesidir; "Dan Emmons" atıfı doğrulanmamıştır. Kaynak: Hayashida (Gamasutra) + GMTK.

### Kishōtenketsu (çatışmasız 4-act)
起承転結 — Mario level'larının iskeleti. **Çatışma gerektirmez**; gerilim kontrast ve keşiften gelir.
- **Ki (起):** konuyu/ortamı kur. **Shō (承):** derinleştir/genişlet, sürpriz yok. **Ten (転):** beklenmedik, çoğu kez **alakasız** yeni öğe — eğrinin kalbi; her şeyi yeniden çerçeveler. **Ketsu (結):** Ki+Shō ile Ten'i tatmin edici bütünde **uzlaştır** (çatışma çözme değil).
- **Önce Ten'i (twist) tasarla**, sonra giriş/gelişmeyi geriye doldur — tasarım emeği oraya yoğunlaşmalı.
- Bir level'ı **düşman/fail baskısı olmadan** kurabilirsin — fikrin kendisi kahraman olsun.

### "Teach, then test" (sözsüz öğretme)
Introduce+Develop = **öğret** (güvenli pratik); Twist+Conclude = **sına** (baskı altında uygula). Çalışmasını sağlayan mekanizmalar: güvenli sandbox (fail imkânsız) · audiovisual affordance (tuğlaya vurunca zıpla+ses → etkileşilebilir) · ödül yerleşimi (istenen aksiyonu öğretecek konumda coin) · ucuz/telafi edilebilir ilk fail · ilerlemeden önce değerlendirme.

### Vaka — Super Mario Bros. 1-1 (sıfır metin)
Sağa koş (kontrastla göz yönlendirme) → ilk zıplama = ilk Goomba (ölçülü hızla reaksiyon süresi) → ? blok kazara vurulur (zıpla+ses+coin → ödül döngüsü) → mantar **sağ borudan sekip geri yuvarlanır**, oyuncuya çarpar (geometri büyümeyi **garanti eder**) → telegraflı küçük çukur → flagpole = "sınav". **Ders:** açılış ekranına tüm mekaniklerin mikrokozmosunu koy; kilit dersi **geometriyle zorla** (umma, inşa et); ilk fail'i ucuz yap; ilk seferde tehlikeyi cömertçe telegraph et, sonra marjları daralt.

---

## 2. Player guidance — sözsüz yönlendirme

### Affordance vs Signifier (Norman, oyuna uyarlı)
- **Affordance:** bir nesnenin formundan okunan, *yapılabilecek* şey (kenar tutunmayı, boşluk zıplamayı sunar).
- **Signifier:** nerede/nasıl aksiyon alınacağını söyleyen **algılanabilir ipucu** (sarı boya, parıltı, ses). Norman: "tasarımcı için signifier'lar affordance'tan çok daha önemlidir." Hedef: *kapıya tabela koymana gerek kalmasın.*
- Sanal nesneler dokunulamadığı için oyunlar signifier'a daha çok yaslanır.

### Gözü yönlendirme (en güvenilir araçlar)
- **Kontrast** (parlaklık/renk/hareket) gözü istemsiz çeker. Yolu aydınlat, çıkmazı karart (Half-Life 2). 2D'de: hedef rotada daha parlak/kontrast tile'lar.
- **Rezerve "rehber renk":** sönük palet üzerinde yalnızca yol/etkileşilebilir için kullanılan tek aksan (Mirror's Edge kırmızı, Uncharted sarı tutamaklar). Rengi **özel** tut (etkileşimsiz prop'a asla koyma) ve **renk körü güvenliği için ikinci kanalla** (şekil/parlaklık/outline) destekle.
- **Leading lines:** geometriyi (boru, ray, tile kenarları, lav akışı) hedefe yakınsat. 2D'de katı tile'ların **şekli** senin leading line'ındır.
- **Framing & reveal:** tünel çıkışını bir landmark'ı çerçeveleyecek konumlandır ("mağaradan çık, kaleyi gör").
- **Hareket** en güçlü çekicidir (duman, ateş) — yalnızca bakılmasını istediğin şeyde, az kullan.

### Landmark / "weenie" ve breadcrumb
- **Weenie** (Disney): ileri çeken uzun görsel mıknatıs. **Yoğunluk metriği:** yolculuk sırasında oyuncu **en az ~30 saniyede bir** bir şey tarafından çekilmeli — landmark aralığını buna göre ayarla.
- **Breadcrumb:** kısa menzilli pickup izi (coin/ring); yerel yönlendirme için. Tehlikeli **görünen** bir yola breadcrumb döşemek tereddüdü kırar ("şıkırtıyı takip etmek ödüllendirir").

### Environmental storytelling
Mekânın kendisini anlatı olarak kullan; hikâye **çıkarsanır**, anlatılmaz. Oyuncunun boşluğu doldurması (closure) yatırımı yaratır. Teknikler: sahnelenmiş vinyetler, nedensel zincirler (kan izi), **environmental telegraphing** (kıvılcımlı ceset = elektrikli tehlike — aynı anda güvenlik öğretir). Kural: *her anonim çevre-anlatı anı, oyun hakkında bir şey söyleme fırsatını ziyan eder* — jenerik dekor yok.

---

## 3. Gating & locks/keys

"Lock" = oyuncunun şu an geçemediği herhangi engel; "key" = onu aşan yetenek/eşya/**bilgi**. Mark Brown'ın *Boss Keys*'i her haritayı bir **graf** olarak çizer (oda=düğüm, bağlantı=kenar): okunur ama trivial-lineer değil — dallanır ve loop yapar.

**Gate türleri (kesin sözlük kullan):**

| Tür | Tanım |
|---|---|
| **Hard gate** | Tamamlamadan geçilmez |
| **Soft gate** | Erken çıkılabilir ama genelde çıkılmaz |
| **Lock-and-key** | Başka yerden gelen key isteyen hard gate |
| **Forward gate** | Kritik yolu kapatır |
| **Backward / one-way** | Geri dönülmez; akışı zorlar |
| **Shortcut** | Uzak taraftan açılan hard gate (backtrack'i çökertir) |
| **Hidden exit** | Çıkışı bulmak için keşif gerekir |

**Kurallar:** her engelin gate türünü **bilinçle** seç; **key'i vermeden önce lock'u foreshadow et** (erken gör, sonra dön); bir key birden çok takip yolunu açsın; **uzak-taraf shortcut'larıyla backtracking'i çökert** (akışı en çok iyileştiren yapı).

**Karmaşıklığı gate'le:** Teach → Test → Twist. Tek seferde tek yeni kavram (yeni mekanik + yeni tehlike + yeni düşmanı aynı anda sokma — oyuncuyu neyin öldürdüğü anlaşılmaz). Öğrenilen mekanikleri ancak her biri tek tek kanıtlandıktan sonra birleştir.

---

## 4. Pacing — gerilim/dinlenme ritmi (level içi)

- **Intensity** = tek olayın heyecanı; **pacing** = doruklar arası zamanlama.
- **Kontrast kuralı:** düz yoğunluk sıkar; *sürekli* maksimum yoğunluk uyuşturur ("11 sürekli açıksa, 11 yeni 5 olur"). Çukurlar bir sonraki doruğu hissettirir.
- **Sawtooth:** zarfı yükselen, dişleri korunan doruk/çukur dizisi. Pürüzsüz rampa istenmez — kontrastı yoktur.
- **Rest beat = mühendislik aracı:** boss sonrası garanti bir düşük-yoğunluk/ödül aralığı koy. Rest = aktivitesizlik değil; göreceli düşüş (güvenli oda, traversal, loot anı).
- **Önce intensity grafiğini çiz:** doruğu kesin planla, çukuru kabaca yerleştir, hikâye/ödül beat'lerini **doruklara** koy.
- Tür kabaca tension:rest oranı — horror ~3:1, komedi ~1:1, aksiyon arası.
- **Çeşitlilik:** zorluğun türünü de değiştir (combat → puzzle → traversal); tekrar = sıkıntı.

---

## 5. Süreç: pen&paper → blockout → playtest

Roller (büyük stüdyo): Level Designer (etkileşim) · Level Artist · Environment/Lighting Artist · Encounter Designer. Solo'da hepsi sende — ama **aşamaları ayrı tut.**

1. **Pen & paper (kavram):** motor kısıtı olmadan düşün; mekanikleri, bölgeleri, ilerlemeyi netleştir. Steve Lee: level'ı **önce metinle** tasarla.
2. **Blockout / greybox (prototip):** sıfır yeni sanat; primitive geometri ile **oynanabilir**. İdeal blockout: kurallara göre oynanır · net navigasyon/landmark · kritik yol vs yan içerik tanımlı · hem top-down hem oyuncu-bakışından okunur. **Graybox** = imza-sanatsız soyut blocking (esneklik); **whitebox** = bağlamı veren silüet/anahtar sanatla.
3. **Metrics:** ölçeği bir **insan-figürü referansıyla** sabitle (geçitler ne çok dar ne mağaramsı). 2D'de: tile/grid boyutu, zıplama menzili, oyuncu hızı = level'ı yöneten metrikler.
4. **Playtest (her aşamada):** taze oyuncuyla; **brief verme, kesme, kişisel alma.** Söylediğini değil **yaptığını** gözle (tereddüt, takılma, ölüm, çıkış). Önerilen çözüm yanlış olabilir ama *işaret ettiği sorun neredeyse her zaman gerçektir.*
5. **Sanat en son:** layout birden çok playtest'ten değişmeden geçince. *Kaba blockout'u silmek ucuz; art-pass'lenmiş işi atmak pahalı.*

---

## 6. Sık hatalar (fun-killer'lar)

- **Landmark'sız labirentler** (#1 okunabilirlik katili). · **Haksız/okunamaz ölümler** (gizli diken, ekran-dışı instakill). · **Metin duvarları** (metinle açıklamak zorundaysan tasarım öğretemedi). · **Yönsüz sandbox** (açık alan + çekim yok = felç). · **Difficulty spike'ları** (introduce-test-combine'dan önce). · **Çıkmazlar / anlamsız koridorlar** ("kâğıtta iyi, yürürken sürünüyor" — level'ı her zaman **oyuncu hızında yürü**, editör kamerasından yargılama). · **Monotonluk.** · **Layout çalışmadan sanat üretmek** (en pahalı hata).

---

## Tek-sayfa özet (2D level inşası)

1. Level başına **tek mekanik**: Introduce(güvenli)→Develop→Twist(recombine)→Conclude(ustalık)→at.
2. **Metinle değil**; geometri, ödül ve feedback ile öğret. Açılışa mikrokozmos koy, kilit dersi geometriyle zorla.
3. **Gözü yönlendir:** kontrast/parlaklık, rezerve rehber renk (+ikinci kanal), tile-şekli leading line, framing.
4. **Weenie yoğunluğu:** ~30 sn'de bir bir şey çeksin.
5. Her engelin **gate türünü** adlandır; lock'u key'den önce foreshadow et; shortcut'la backtrack'i çökert.
6. **Önce intensity grafiği** — kesin doruk, kaba çukur, ödül doruklarda; rest beat bir araçtır.
7. **Önce blockout** (massing, metrics+figür, wayfinding, playtest). Level'ı **yürü, uçma.**
8. **Taze oyuncuyla playtest;** brief/kesme/alınma yok; feedback'in işaret ettiği sorun gerçektir.
9. Labirent/haksız ölüm/çıkmaz/monotonluğu öldür; golden path okunur, keşif onun yanında.

---

## Kaynaklar

- The secret to Mario level design — Game Developer: https://www.gamedeveloper.com/design/the-secret-to-i-mario-i-level-design
- Kishōtenketsu in Mario — Still Eating Oranges: https://stilleatingoranges.tumblr.com/post/76178051254/kish%C5%8Dtenketsu-in-mario
- Super Mario 3D World's 4-step level design — GMTK (Mark Brown)
- Analysis of Super Mario Bros 1-1 — Medium: https://medium.com/creating-immersive-worlds/analysis-of-super-mario-bros-1-1-2eb9a70fbeb4
- Gates typology — The Level Design Book: https://book.leveldesignbook.com/process/layout/typology/gates
- Pacing — The Level Design Book: https://book.leveldesignbook.com/process/preproduction/pacing
- Blockout & playtesting — The Level Design Book: https://book.leveldesignbook.com/process/blockout
- A taxonomy of weenies — Game Developer: https://www.gamedeveloper.com/design/a-taxonomy-of-weenies-the-landmarks-that-define-i-ghost-of-tsushima-i-
- What Happened Here? (environmental storytelling) — Worch & Smith: https://www.witchboy.net/articles/what-happened-here/
- Level Design 101: The Language of Location Development — MY.GAMES: https://medium.com/my-games-company/level-design-101-the-language-of-location-development-6d940a01b949
- The Art of Level Design — SAE: https://www.sae.edu/gbr/insights/the-art-of-level-design-in-video-games/
- Fortnite/UEFN Level Design Fundamentals — Epic: https://dev.epicgames.com/community/learning/tutorials/3VKJ/unreal-engine-fortnite-level-design-fundamentals
- Holistic Level Design (GDC 2017) — Steve Lee: https://www.youtube.com/watch?v=CpOoTAVeEcU
