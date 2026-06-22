# Onboarding / FTUE (First-Time User Experience)

Oyunun en yüksek-kaldıraçlı kısmı. İlk oturumda uygulamaların **%70–90'ı** kullanıcı kaybeder; **D1 retention sonraki her metriğe tavan koyar** (%80 D1-kaybı, D7'yi %20 altına sıkıştırır). FTUE kabaca **ilk 60 saniye** (hook) + **ilk 15 dakika** (derinliği kanıtlama).

> İlgili: ilk oturumun interest curve'ü → `03-difficulty-and-pacing.md`; sözsüz öğretme/teach-then-test → `02-level-design-principles.md`.

---

## Kurallar

- **Show, don't tell.** Metin duvarıyla değil aksiyonla öğret. İlk düşman gelince combat'ı anlatmak yerine saldırı tuşunda görsel ipucu yak (kinesthetic learning — yaparak öğrenme).
- **Tek seferde tek mekanik ("skill atom").** İzole beceriyi tanıt, küçük bir başarıya kadar denet, sonra bir sonrakini. Aynı anda çok yeni mekanik istifleme (Cook'un skill-chain'i: basit zıplama → platform zıplama → engel → level bitirme).
- **Progressive disclosure.** Yalnızca o anki görevin kontrol/UI'sini göster. Meta sistemleri (shop, upgrade, sosyal) ihtiyaç doğana dek gizle — meta katmanı ilk 3–5 oturumda aç, ekran 1'de değil.
- **Time-to-fun'ı agresif düşür.** Oyuncu ~10–15 saniyede gerçekten oynuyor olsun. Hedef: "devam etmek istenen deneyime en kısa yol."
- **Contextual > forced tutorial.** Rehberliği bağlamda tetikle (just-in-time), uzun öne-yığılmış zorunlu akış yerine. Zorunluysa kısa/atlanabilir tut.
- **Sıkı feedback loop.** Her aksiyona hızlı, juicy feedback; ustalık-öncesi hüsran fazında öğrenmeyi hızlandırır.
- **Tutorial drop-off'u ölç.** Hangi adımda terk ediliyor adım-adım izle; her düşüş noktası düzeltilebilir bir funnel sızıntısıdır.
- **Önce eğlence, sonra monetizasyon.** İlk oturumlarda az/sıfır reklam, paywall yok; erken agresif monetizasyon düşük D1'in baş sebebidir.

---

## Kaçınılacak failure mode'lar

- Metin-ağırlıklı giriş ekranları.
- Oyuncunun henüz kullanamayacağı mekaniği öğretmek (düşük algılanan değer → hızlı hüsran).
- İlk gerçek kazanımı geciktiren aşırı-uzun tutorial.

---

## Implicit-tutorial felsefesi (Valve/Portal ile uyumlu)

- **Level'ın kendisi tutorial'dır:** tek mantıklı aksiyonun ders olduğu bir durum tasarla, oyuncuya keşfettir.
- Çıkarımı ödüllendir — "anladım!" anı ödülün kendisidir.
- Güvenli öğret, baskı altında sına. Yeni mekanikleri tek tek; birden istifleyince test oyuncuları frustre oldu (Portal erken build'leri).

---

## Kaynaklar

- Best Practices for Mobile Game Onboarding — Adrian Crook: https://adriancrook.com/best-practices-for-mobile-game-onboarding/
- FTUE & Onboarding — Mobile Game Doctor: https://mobilegamedoctor.com/2025/05/30/ftue-onboarding-whats-in-a-name/
- The Chemistry of Game Design (skill atoms) — Daniel Cook: https://lostgarden.com/2007/07/19/the-chemistry-of-game-design/
- Game Mechanics (Portal 2) — Valve Developer Wiki: https://developer.valvesoftware.com/wiki/Game_Mechanics_(Portal_2)
