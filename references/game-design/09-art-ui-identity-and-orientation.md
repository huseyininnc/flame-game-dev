# Per-Game Design Identity — Tema, UI/HUD, Tipografi, Orientation (ZORUNLU)

> **Her oyun KENDİ markası gibi görünmeli — bir öncekinin reskin'i DEĞİL.** Düşman: "üst stat-pill'ler + alt bar + aynı yuvarlak font + aynı palet"i her oyuna uygulamak. Tema, UI, HUD düzeni, font, palet, hareket kişiliği ve **çekirdek mekanik** oyunun içeriğine göre değişmeli. Orientation (portrait/landscape) da oyuna göre seçilir.

**Mutlak kural:** Oyunlar arası **ortak `overlay_widgets`/HUD/palette/font yeniden kullanımı YOK.** Kod konvansiyonları (mimari, Bloc, pooling, responsive disiplini) paylaşılır; **görsel/etkileşim kimliği paylaşılmaz.** Marka testi (§6) geçilmeden oyun "done" sayılmaz.

---

## 1. HUD diegesis taksonomisi (Fagerholt & Lorentzon) — önce bunu seç

İki eksen: **kurgu** (karakter farkında mı?) × **geometri** (dünyada mı, düz overlay mı?).

| | Kurgu içi (karakter farkında) | Kurgu dışı (sadece oyuncu) |
|---|---|---|
| **Dünya geometrisinde** | **Diegetic** (Dead Space sırt canı) | **Spatial** (duvar arkası parıltı, waypoint) |
| **Düz overlay** | **Meta** (kan sıçraması, düşük-can vignette) | **Non-diegetic** (klasik HUD bar/pill) |

- **Diegetic:** maksimum immersion, yüksek maliyet, küçük ölçekte okunabilirlik riski; preproduction'da karar ver.
- **Non-diegetic:** en ucuz/net, en az immersion; bilgi-yoğun/strateji/top-down için iyi — ama dünyanın görsel diline bürünsün, context'e göre sönüp açılsın.
- **Spatial:** navigasyon/çok-oyunculu farkındalık; aşırı kullanım görsel gürültü.
- **Meta:** ekran efektiyle duygu; **daima erişilebilirlik toggle'ı**, can en düşükken bilgiyi gizleyen ağır distortion yapma.

**Distinctness kuralı:** Her yeni oyuna **bir öncekinden FARKLI birincil diegesis** ata. (Ör. A = meta-ağırlıklı / neredeyse overlay yok; B = diegetic in-world readout; C = context-fading non-diegetic.) Aynı mekanik bile olsa samey olamaz.

---

## 2. Türüne göre HUD düzeni

İlke: hızlı oyun → minimal, glanceable, kenara yaslı; yavaş oyun → katmanlı bilgi. **Refleks "köşeye doldur"dan kaç** — sık değişen kritik bilgiyi merkeze yakın veya diegetic yap; köşe yalnızca beynin filtrelediği statik bilgi için.

| Tür | Bilgi nerede | Miktar | Girdi | Ayırt edici hamle |
|---|---|---|---|---|
| Survivor/bullet-heaven | XP bar üst kenar (tam genişlik), timer üst-orta, level kompakt | Run'da az, level-up modalinde yoğun | tek joystick (auto-fire) | Aksiyonu merkeze al, HUD'u ince üst şeride it; seçimler upgrade kartlarında |
| Match-3/puzzle | Skor+hamle üstte, hedefler yan ray/üst şerit; board merkez | Az-orta, statik | board'a tap/swipe | Board'ı "masa" gibi çerçevele; diegetic board chrome (yüzen pill yok) |
| Idle/merge | Para üst bar (büyük sayılar), board merkez, prestige+shop alt sekmeler | Yüksek ama statik | tap; alt tab nav | Sayı readout'larını kahraman-UI yap; tab bar burada meşru |
| Runner | Skor/mesafe üst-orta, coin köşe | Minimal | swipe/tap, tek el | Neredeyse sıfır HUD; hız çizgileri+ekran FX (meta) |
| Tower defense | Kaynak üst, dalga/can köşe, build paleti alt/yan dock | Orta-yüksek | tap yerleştir; tray'den sürükle | Build tray = kimlik; jenerik bar değil diegetic "kontrol paneli" |
| Arcade | Skor üst-orta (büyük), can ikon | Az | yön/tap | Cesur numerik tipografiyi tüm estetik yap |
| Narrative/IF | Diyalog kutusu alt (veya tam overlay), state sübtil | Çok az | tap ilerle, seçim butonları | HUD = metin çerçevesi; imza öğe diyalog paneli |

**Anti-samey:** Ardışık iki oyun **aynı anchor desenini** kullanmasın. Önceki "üst pill + alt tab bar" idiyse, sonraki "ince üst şerit + merkez aksiyon + modal seçim" veya "diegetic in-world readout + alt bar yok" olsun.

---

## 3. Tipografi (her oyuna kendi font üçlüsü)

**3 rol — ayrı tut:** **Display/başlık** (karakterli; logo/splash/başlık — markayı taşır) · **UI/gövde** (temiz, netlik önce; menü/diyalog/HUD label) · **Numeric** (yüksek okunur, **tabular/monospace** ki skor/timer rakam değişince zıplamasın).

**Türüne göre ton:** fantasy→ornate/el-çizimi · sci-fi→geometrik modüler sans · yarış/spor→bold condensed · casual/çocuk→yuvarlak · horror→distressed display (UI yine okunur) · retro→pixel/blocky · zarif/romance→yüksek-kontrast serif.

**Kurallar:** bir karakterli display + bir temiz text (iki display eşleştirme yok). Küçük boyutta: büyük x-height, düşük stroke-kontrast, kerning/hinting cihazda doğrula; 50–80 char/satır, %130–150 satır aralığı; medium ağırlık. **Varsayılan/sistem font (Roboto/SF/Arial) başlıkta = #1 düşük-efor tell'i — asla.** Lisans: Google Fonts çoğunlukla **OFL** (ticari+gömme serbest); `.ttf`'i `assets/fonts/`'a koy, OFL metnini yanına, pubspec'te tanımla; hedef dil glyph'lerini (TR: ş/ğ/ı) doğrula + fallback.

**Distinctness:** her oyun **kendi display+UI+numeric üçlüsünü** alır. Aynı font stack'i tekrar = reskin.

---

## 4. Per-game görsel kimlik (5 sütun)

1. **Palet:** sıkı/kasıtlı — 1 primary, 1 accent, 2–3 nötr, + semantik (iyi/kötü/uyarı). Her oyun **farklı hue ailesi + doygunluk + açık/koyu taban**.
2. **Form dili:** birini seç ve uygula (keskin-açısal / yumuşak-yuvarlak / organik-blob / beveled-skeuomorphic). Panel, buton, ikon hepsi aynı dili konuşsun.
3. **İkonografi:** tutarlı set (line/filled/chunky), form diline uygun. Bir oyunun ikonu diğerine düşmemeli.
4. **Buton/panel stili:** corner radius, stroke, fill (flat/gradient/glass), depth/shadow, pressed state. En çok tekrar eden (ve en ele veren) kit — bilerek değiştir.
5. **Hareket kişiliği:** easing eğrileri, geçiş stili, idle/hover mikro-animasyon, juice. Snappy/punchy vs floaty/elegant vs springy/playful. Hareket bir marka sinyalidir.

**Marka testi:** oynanışı sustur; sadece bir buton + panel + ikon + sayı göster. Ekip "bu hangi oyun?" diyebilmeli. Diyemiyorsa → reskin, başarısız.

---

## 5. Orientation: portrait vs landscape (oyuna göre seç)

Hepsini portrait yapma — orientation bir distinctness kaldıracıdır ve grip/oynanışı belirler.

- **Portrait** = genelde **tek el**, baş parmak; hareket halinde; tap-merkezli/düşük-aktif-alan. Etkileşimli kontrolleri **alt ve kenarlara** koy (üst-orta küçük ele uzak).
- **Landscape** = genelde **iki el**, iki kenar başparmak (konsol-grip); oturmuş/odaklı; geniş yatay alan, aktif oynanış çok. Oyun ne kadar aktifse landscape o kadar mantıklı.

| Tür | Tercih | Neden |
|---|---|---|
| Idle/merge/tycoon | Portrait | tap, tek el, hareket halinde |
| Match-3/puzzle | Portrait | board portrait'te oturur, tek el |
| Runner | Portrait veya landscape | lane geometrisine göre |
| Survivor/bullet-heaven | **Landscape** | arena için geniş aktif alan, iki başparmak |
| Tower defense | **Landscape** | geniş harita + build tray |
| Arcade | Mekaniğe göre | grip'e uydur |
| Narrative/IF | Portrait | okuma + tek el ilerleme |

Orientation **HUD/kontrol düzenini** değiştirir (sadece aspect değil): portrait → kontroller alt/kenar, HUD üst şerit; landscape → iki kenar başparmak, HUD geniş üstte. **Flame/Flutter:** `main()`'de `runApp` öncesi `SystemChrome.setPreferredOrientations(...)` ile oyuna özel kilitle; HUD'u **tek bir orientation için** tasarla (tek HUD iki orientation'a hizmet etmesin); fixed-resolution kamera + viewport kenarına anchor. Genel responsive: `references/responsive-design.md`.

---

## 6. Anti-reskin (bespoke-identity) kontrol listesi — her oyundan önce

Reskin/asset-flip görünümü oyuncular tarafından anında "ucuz" damgalanır (ve mağaza keşfine zarar verir). Her yeni oyunda:

- [ ] Birincil **diegesis** seçildi ve **bir öncekinden farklı**
- [ ] Benzersiz **display** font (sistem değil, son oyunun fontu değil)
- [ ] Benzersiz **UI/gövde** font, cihazda küçük boyutta okunur
- [ ] **Numeric** font tabular/monospace; hedef-dil glyph'leri doğrulandı
- [ ] Ayırt edici palet (1 primary/1 accent/nötr/semantik) — farklı hue/taban
- [ ] Form dili ilan edildi (açısal/yuvarlak/organik/beveled) ve panel+buton+ikona uygulandı
- [ ] Buton/panel kiti görsel olarak farklı (radius/fill/depth/pressed)
- [ ] İkon seti bespoke — başka oyuna düşmez
- [ ] Hareket kişiliği tanımlı (easing/geçiş/juice) — global default değil
- [ ] **HUD anchor deseni bir öncekinden farklı**
- [ ] Orientation türe/grip'e göre seçildi; HUD o orientation için kuruldu
- [ ] Meta/ekran-efekti feedback'inde erişilebilirlik toggle'ı
- [ ] **Marka testi geçti:** izole buton+panel+ikon+sayı bu oyuna ait tanınıyor
- [ ] Çekirdek mekanik bir önceki oyundan farklı (portföy çeşitliliği)

---

## Kaynaklar

- Beyond the HUD — Fagerholt & Lorentzon (2009): https://www.researchgate.net/publication/277202228_Beyond_the_HUD_-_User_Interfaces_for_Increased_Player_Immersion_in_FPS_Games
- Types of UI: Diegetic/Non-Diegetic/Spatial/Meta: https://medium.com/@lorenzoardeni/types-of-ui-in-gaming-diegetic-non-diegetic-spatial-and-meta-5024ce6362d0
- Crusade against corner-based HUD — Game Developer: https://www.gamedeveloper.com/design/my-personal-crusade-against-mini-maps-and-other-corner-based-hud-elements-in-immersive-games-
- Mastering Game HUD Design — Polydin: https://polydin.com/game-hud-design/
- Game UI Database: https://www.gameuidatabase.com/
- Choosing fonts for games — NoahType: https://noahtype.com/how-to-choose-the-right-font-for-video-games/
- Fonts for games — 99designs: https://99designs.com/blog/design-history-movements/gaming-fonts/
- Google Fonts FAQ (licensing): https://developers.google.com/fonts/faq · OFL FAQ: https://openfontlicense.org/ofl-faq/
- Games and Visual Identity — Game Developer: https://www.gamedeveloper.com/business/games-and-visual-identity
- Touch Control Design (orientation/grip) — Mobile Free To Play: https://mobilefreetoplay.com/control-mechanics/
- Portrait vs landscape — Brian Pagan: https://brianpagan.net/2012/interface-design-for-mobile-and-tablets-landscape-vs-portrait/
- Asset flip (anti-pattern) — Wikipedia: https://en.wikipedia.org/wiki/Asset_flip
