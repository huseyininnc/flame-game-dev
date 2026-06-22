# Level / Wave Tasarım Kontrol Listesi

Bir level (veya real-time oyunda wave/zone) tasarlarken bu listeyi geç. Teori: `references/game-design/02`, `03`, `08`.

## Önce tasarla (kod öncesi)
- [ ] Bu level'ın **tek net amacı** var mı? (bir mekanik öğret / bir düşman tanıt / bir hikâye/ödül beat'i ver — asla "dolgu" değil)
- [ ] Hedef estetik(ler) ve pillar'larla uyumlu mu?
- [ ] **Tek yeni fikir** mi? (yeni mekanik + yeni tehlike + yeni düşmanı aynı anda sokma)

## Teach → Test → Twist (tek-mekanik yayı)
- [ ] **Introduce:** yeni öğe **güvenli/fail-edilemez** alanda tanıtılıyor mu?
- [ ] **Develop:** hafif riskle geliştiriliyor mu?
- [ ] **Twist:** mekanik recontextualize ediliyor mu (alakasız zorluk yığma değil)?
- [ ] **Conclude:** öğretilen beceriyi gerektiren bir final/zafer turu var mı?
- [ ] Fikir bitince mekanik **bırakılıyor** mu (padding yok)?

## Zorluk & pacing
- [ ] Genel eğri **sawtooth** mı (tırman→bilerek düşür→tırman), düz rampa değil?
- [ ] Her **spike'tan sonra çukur/relief** var mı?
- [ ] Açılış **kontrol spike**'ından kaçınılıyor mu (az buton, bilinen beceri)?
- [ ] Oyuncu becerisinin yaşam-boyu artışına göre **yeniden kalibre** edildi mi (level 100 ≠ level 1000)?
- [ ] Oturum interest curve'ü: hook → yükselen beat'ler → doruk → çekiş?

## Player guidance (sözsüz)
- [ ] Metinle değil **geometri/feedback/ödül** ile mi öğretiyor?
- [ ] Göz, **kontrast + rezerve rehber renk** (+ renk körü için ikinci kanal) ile yönlendiriliyor mu?
- [ ] **Golden path okunur** mu; keşif onun yanında ödüllendiriliyor mu?
- [ ] Weenie/landmark yoğunluğu: ~30 sn'de bir bir şey çekiyor mu?

## Gating
- [ ] Her engelin **gate türü** bilinçli mi (hard/soft/lock-key/one-way/shortcut/hidden)?
- [ ] **Key'den önce lock foreshadow** ediliyor mu?
- [ ] Backtracking varsa **shortcut** ile çökertilmiş, dönüş **anlamlı ödülle** mi?

## Levels-as-data (uygulama)
- [ ] Level **config/JSON** olarak mı (hardcode değil)? Tek generic `LevelConfig` + loader?
- [ ] Zorluk küçük bir **parametre setiyle** mi ayarlanıyor (moves/objective/board/blocker/allowed)?
- [ ] Real-time ise wave parametreleri (sayı, aralık, HP/hız ölçeği, boss kadansı) config'te mi?

## Game feel
- [ ] Her oyuncu aksiyonunun anında, çok-duyulu feedback'i (görsel+ses) var mı?
- [ ] Önemli darbe/öldürmede juice (screenshake/hit-stop/flash/partikül) var mı, abartısız?

## Doğrulama
- [ ] Level **oyuncu hızında yürünüp/oynanıp** doğrulandı mı (editör kamerasından değil)?
- [ ] Mümkünse **taze oyuncuyla** playtest; davranış gözlendi mi (tereddüt/takılma/çıkma)?
- [ ] Telemetri: level/wave başına **deneme + drop-off** enstrümante mi?
- [ ] Sık hatalar elendi mi: labirent, haksız ölüm, çıkmaz, monotonluk, yönsüz sandbox?
