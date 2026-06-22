# Zorluk Eğrisi, Pacing ve Denge (Balancing)

Bu doküman zorluğun ve oyun boyu/oturum boyu ritmin nasıl tasarlanacağını verir. Level-içi pacing ve gating → `02-level-design-principles.md`; casual/puzzle'a özel sayısal tuning → `08-level-design-for-2d-casual.md`.

---

## 1. Flow channel (akış kanalı)

Csikszentmihalyi: bir eksende oyuncu **skill**, diğerinde **challenge**. "Flow channel", ikisinin yaklaşık eşit kaldığı çapraz banttır.
- Challenge ≫ skill → **anksiyete/hüsran.**
- Challenge ≪ skill → **can sıkıntısı.**
- Oyuncu oynadıkça skill **yükselir**; bu yüzden **sabit zorluk hızla sıkıcı** olur. Zorluk oyuncuyla birlikte tırmanmalı.

Pratik ölçüt: zorluğu **(oyun zorluğu − oyuncu becerisi)** olarak düşün; oturum boyunca bu farkı ~sabit/dar tut.

---

## 2. İyi eğri: fractal / sawtooth (testere)

İyi zorluk eğrisi **düz çizgi değildir** — genel olarak yükselen, **küçük doruk ve çukurlardan** oluşan bir trend (fractal). Makro trend tırmanır, mikro doku nefes alır.

- **Sawtooth:** birkaç level artan zorluk → bilerek **bir-iki level düşür** → tekrar tırman. Çukur; rahatlama, toparlanma ve ustalık hissi verir, sonraki tırmanışı taze kılar.
- **Uygulama:** zorluğu bir formülden sür (linear / `sqrt` / `pow`) + sabit aralıklı periyodik bir sawtooth dip çıkar.

### Difficulty spike — iyi vs kötü
- **İyi spike:** bilinçli doruk (boss/gauntlet) **hemen ardından bir çukur** → oyuncu zaferi tadar, ustalık hisseder. Çukur, spike'ı yorucu değil tatmin edici yapar.
- **Kötü spike:** plansız duvar. Klasik örnek **açılış kontrol-öğrenme spike'ı** ("zorluk eğrileri tepede başlar") — karmaşık kontroller, oyuncu yatırım yapmadan en zoru başa koyar. Çözüm: başta **daha az buton/basit kontrol**, mekanikleri tek tek öğret, oyuncunun zaten bildiği becerilere yaslan (tap, swipe).

---

## 3. Interest curve (Jesse Schell)

Oyuncunun ilgisini zamana karşı çiz:
1. **Hook** — erken keskin sıçrama (dikkat yakala; hızlı bir kazanç).
2. **Rising action** — her biri öncekinden yüksek doruklar, aralarda küçük çukurlar.
3. **Climax** — sona yakın en yüksek nokta.
4. **Resolution** — kısa iniş, "daha fazlasını isteten" son.

**Fractal'dır:** tüm oyunun, her level'ın, her oturumun kendi interest curve'ü olmalı. **Teşhis aracı olarak kullan:** beklenen eğriyi çiz, düz/sarkan bölgeleri bul — pacing problem noktaların onlardır.

**Oturuma uygula (mobil için kritik):** ilk saniyelerde hook → birkaç yükselen beat → tatmin edici doruk (boss/combo/büyük ödül) → bir sonrakine çekecek küçük yüksek nokta.

---

## 4. Intensity ramps / "nefes alma"

- **Ana yasa:** algı **görecelidir** — 5→11 büyük sıçrama, 10→11 hiçtir. Sürekli yüksek yoğunluk taban çizgisini sıfırlar.
- **In-out-in (Schell):** patlamayla aç → **geri çekil** (oyuncu adapte olsun) → giderek büyüyen beat'lerle yüksel → beklentiyi aşan doruk. Sonra bir üst ölçekte tekrar.
- **Rest ≠ hareketsizlik:** göreceli düşüş. Bir doruğu hissettirmek için öncesinde yoğunluğu **düşür** — önce negatif boşluğu (lull) tasarla, doruğu ona karşı yerleştir.

---

## 5. Dynamic Difficulty Adjustment (DDA) & rubber-banding

DDA: oyuncu performansına göre oyunu otomatik ayarlayıp onu flow channel'da tutar. **Rubber-banding** en bilinen basit biçimdir (yarış oyunları: geride kalan AI hızlanır).

Teknikler: düşman can/hasar/spawn oranını ölçekle, aim-assist ayarla, kaynak/ammo drop'unu ihtiyaca göre tune et, level seçimini başarı oranına göre nudge et.

- **Artılar:** daha geniş oyuncu yelpazesini flow'da tutar; çeşitlilik/replay.
- **Riskler:** fark edilirse **haksız** hissettirir; oyuncular sistemi **suistimal** edebilir (kasten geri kalıp boost almak); **monetizasyon güdümlü gizli zorluk ayarı etik dışıdır — yapma.**
- **İyi uygula:** **görünmez** olsun; sınırlı/sübtil ayar; erişilebilirlik (zorlanan oyuncuya yardım) için iyi; rekabetçi PvP'de ve adalet algısının çekirdek olduğu yerde dikkatli ol; mümkünse oyuncuya opt-in/seçim bırak.

---

## 6. Balancing (denge)

- **Fairness:** tüm anlamlı seçenekler kıyaslanabilir derecede uygulanabilir olmalı; oyuncu kaybın **kendi hatası** olduğunu hissetmeli (görünür "hile" yapan AI bunu bozar).
- **Readability & telegraphing:** tehlikeli her şeyi telegraph et (wind-up animasyonu, ses tell'i, vuruş bölgesi) → reaksiyon şans değil **skill** olsun. Can/cooldown/tehdit görsel olarak net.
- **Risk/reward:** güç bir bedel taşımalı (uzun cooldown, kaynak maliyeti, toparlanma penceresi, pozisyonel açık). Bedelini yazamıyorsan **overpowered**'dır.
- **Dominant strategy avı:** bir strateji diğerlerini sürekli yeniyorsa ifade çöker → nerf et ya da counter'ını buff et. Playtest'te aktif olarak ara.
- **Symmetric vs asymmetric:** simetrik (herkese aynı araç; dengelemesi kolay; rekabetçi puzzle) vs asimetrik ("farklı ama eşit uygulanabilir"; dengelemesi zor, çeşitlilik yüksek). **Intransitivity (taş-kâğıt-makas)** iş gören araçtır: dairesel counter-play kur, hiçbir seçenek domine etmesin.

---

## Tek-sayfa özet

1. Zorluğu oyuncuyla birlikte tırmandır (flow channel); **(zorluk − beceri)** farkını dar tut.
2. Eğri **sawtooth**: tırman → bilerek düşür → tırman. Spike'tan sonra **mutlaka çukur**.
3. Açılış **kontrol spike**'ından kaç: az buton, tek tek öğret, bilinen becerilere yaslan.
4. **Interest curve fractal'dır** (oyun/level/oturum); çiz, düz bölgeleri düzelt; oturumu hook→yüksel→doruk→çekiş ile kur.
5. **Görecelik:** doruğu hissettirmek için önce yoğunluğu düşür (in-out-in).
6. DDA kullanırsan **görünmez & etik** olsun.
7. Her tehlikeyi telegraph et; her güce bir **bedel** yaz; dominant strategy'yi avla; mümkünse intransitive counter-loop.

---

## Kaynaklar

- Flow theory (Csikszentmihalyi) — Yu-kai Chou: https://yukaichou.com/gamification-analysis/flow-theory-complete-guide-csikszentmihalyi-optimal-experience/
- Difficulty Curves Start At Their Peak — Game Developer: https://www.gamedeveloper.com/design/difficulty-curves-start-at-their-peak
- Doing Difficulty Right: Fractal Curves — Game Developer: https://www.gamedeveloper.com/design/doing-difficulty-right-fractal-curves
- Rising Difficulty Curve — abagames: https://abagames.github.io/joys-of-small-game-development-en/difficulty/curve.html
- Game Changers: Dynamic Difficulty — Game Developer: https://www.gamedeveloper.com/design/game-changers-dynamic-difficulty
- Interest Curve — Game Studies Wiki: https://game-studies.fandom.com/wiki/Interest_Curve
- Trinity Part 6: Intensity Ramps — Game Developer: https://www.gamedeveloper.com/design/trinity-part-6---intensity-ramps
- Game Balance — Game Studies Wiki: https://game-studies.fandom.com/wiki/Game_Balance
- Symmetrical vs Asymmetrical Balance — David Gagnon: https://davidgagnon.wordpress.com/2009/08/16/symmetrical-vs-asymmetrical-balance-in-game-design/
