# Game Feel & "Juice"

Mekanik doğru çalıştıktan **sonra** eklenen tatmin katmanı. Aynı mekanik, juice ile bambaşka hissettirir (Vlambeer'in Breakout demosu: aynı kurallar, juice ile dönüşür). Flame'de bunların çoğu `Effect`/`EffectController` + partikül + ses ile uygulanır (bkz. `references/flame/05-effects-and-particles.md`, `08-audio-and-tiled.md`).

---

## 1. Game feel'in 3 sütunu (Swink)

1. **Real-time control** — duyarlı girdi; düzeltme döngüsü ~100 ms altında hissedilmeli. **Temel budur**; duyarlı kontrol olmadan juice boş hisseder.
2. **Simulated space** — hareket, çarpışma, ağırlık, yerçekimi, momentum olan dünya.
3. **Polish** — her etkileşimi vurgulayan audiovisual katman.

**Altın kural:** "Tatsız meyveden iyi su çıkmaz." Önce kontrol + çekirdek mekanik; sonra cila.

---

## 2. Juice checklist (uygulanabilir liste)

**Hareket / animasyon**
- **Squash & stretch:** zıplama, iniş, çarpışmada deformasyon → ağırlık ve kuvvet hissi. (Flame: `ScaleEffect` non-uniform.)
- **Easing / tweening:** hiçbir şeyi lineer hareket ettirme; ease-in/out eğrileri (easings.net). Snappy için exponential, yumuşak için quadratic. (Flame: `CurvedEffectController`, `Curves.easeOut`.)
- **Anticipation & follow-through:** aksiyon öncesi wind-up, sonrası overshoot/settle (wobble/jiggle).
- **Trail:** hızlı nesnede iz — ama vuruşta **trail'i kes** (darbeyi yumuşatır).
- **Scale pulse/bounce:** spawn, pickup, UI'da canlılık. (Mitomerge'deki merge flash bunun bir örneği.)

**Darbe / zamanlama**
- **Screenshake:** yumruk/patlama/büyük zıplamada kamerayı bir an salla. Büyüklüğü olaya ölçekle, **kısa** tut, mide bulandırma. (Flame: `camera.viewfinder` üstünde kısa `MoveEffect`/noise.)
- **Hit-stop / freeze frame ("hold"):** güçlü çarpışma/öldürmede oyunu bir an dondur. Daha büyük vuruş = daha uzun hold. En ucuz, en güçlü darbe aracı.
- **Knockback / recoil:** hem vurana hem vurulana.

**Partikül & izler**
- İniş/koşuda **toz**, çarpışmada **kıvılcım/yıldız**, darbede **debris/splash**.
- Kalıcı yer izleri (ayak izi, iniş decal'i) mekaniği pekiştirir.

**Renk / shading**
- **Hit flash** (hasarda beyaza/kırmızıya flash), önemli öğede sönük arka plana karşı doygunluk pop'u.

**Ses (juice'un yarısı — ihmal etme)**
- **Her oyuncu etkileşiminin net ses feedback'i** olmalı.
- SFX'i hafif compress et / bass-mid'i öne çıkar ki "pop"lasın.
- Müziğin altında sübtil ortam loop'u.

---

## 3. Juice ilkeleri

- **Türe/çekirdek loop'a uydur:** aksiyon için cesur screenshake; anlatı/horror için sübtil hareket.
- **Sinerji > aşırılık:** aynı olayda wobble + partikül + ses + hit-stop'u **birlikte** yığ; tek efekti her yerde aşırı kullanma.
- **Önce temel:** kontrol ve çekirdek mekanik oturmadan cilalama.
- **Erişilebilirlik:** screenshake/flash için bir kapatma seçeneği düşün (foto-duyarlılık, mide bulantısı).

---

## Kaynaklar

- Game Feel — Steve Swink (Ch.1, PDF): http://mycours.es/gamedesign2014/files/2014/10/Game-Feel-Steve-Swink-chapter-1.pdf
- Squeezing More Juice Out of Your Game Design — Game Developer: https://www.gamedeveloper.com/design/squeezing-more-juice-out-of-your-game-design-
- Juice it or lose it / The Art of Screenshake — Vlambeer (Jonasson & Purho)
- Easing reference: https://easings.net/
- Designing Game Feel: A Survey — arXiv: https://arxiv.org/pdf/2011.09201
