# Profesyonel Oyun Geliştirme Süreci

Konseptten yayına ve live-ops'a uzanan iş akışı; prototip/vertical slice, milestone'lar, GDD, iterasyon/playtest ve scoping.

---

## 1. Geliştirme yaşam döngüsü

**Kural:** bir tasarım kararını değiştirme maliyeti, bu fazlarda sağa gittikçe kat kat artar. **Orantısız çoğu emeği preproduction'a harca.**

- **Concept / Ideation:** tür, kitle, tema, kanca, çekirdek fantezi; fizibilite/kârlılık kontrolü. Çıktı: kısa pitch + hedef estetikler (MDA, bkz. 01).
- **Preproduction (en önemli faz):** *ne inşa edileceğini, maliyetini ve eğlenceli olup olmadığını* — yani **"find the fun"** — pahalı üretimden ÖNCE çöz. Riski ucuza öldür. Aktivite: prototip, core-loop, motor/teknoloji seçimi, art-direction testi, tek-sayfa GDD, ideal olarak **vertical slice**. Çıkış: oyunun inşaya değer olduğunu ve kabaca maliyetini bilirsin; "eğlenceli mi?" sorusu açık kalmamalı.
- **Production:** blueprint ölçekte içeriğe dönüşür (tüm sistem/level/art/audio). Maliyet ve kafa-sayısının çoğu burada. Playtest sürekli.
- **Post-production:** Alpha → Beta → Release stabilizasyon (bug fix, balance, optimize, certification).
- **Live-Ops / bakım (casual/mobil için şart):** lansman sonrası sürekli içerik + event (yeni level paketi, sezon, turnuva, indirim). Doğası gereği **agile, döngüsel**. Match-3/casual'da **ayda ~40–80 yeni level**, haftalık/iki-haftalık kadansla beklenir (bkz. 08).

---

## 2. Prototip & Vertical slice

- **Paper prototype:** en ucuz test; kart/token/grid ile **mekaniği** test et (grafik değil). Hızlı başarısız ol, zayıf fikri at.
- **Greybox/blockout:** sıfır yeni sanatla **oynanabilir**; tek mekaniği izole et. (Bkz. 02 §5.)
- **"Find the fun" prototype:** atılabilir dijital build; tek işi core loop'un eğlenceli olduğunu, değiştirmek hâlâ ucuzken doğrulamak. Bulamazsan üretime **geçme**.
- **Vertical slice:** küçük ama **final-kalite** dilim (art+gameplay+sistem+UI+audio birlikte, ship kalitesinde) = "tek-level ama gerçek". Neden: preprod→prod **geçiş kapısı**; pipeline'ı ve kalite çıtasını kanıtlar; publisher/yönetim pitch artefaktı. Kapsamı **küçük** tut (pahalıdır).
- **Ayrım:** prototip = *"eğlenceli mi?"* (çirkin, atılabilir). Vertical slice = *"bu kaliteyi ölçekte üretebilir miyiz, finanse edilmeli mi?"* (temsilî, cilalı).

---

## 3. Milestone'lar (tanım & çıkış kriteri)

| Milestone | Tanım | Çıkış kriteri |
|---|---|---|
| **Prototype** | Çekirdek mekanik izole, atılabilir kod/art | Core loop kanıtlanmış şekilde eğlenceli |
| **First Playable** | Temsilî oynanış + placeholder, baştan sona oynanır | Ana oynanış öğeleri çalışıyor, okunur |
| **Vertical Slice** | Final-kalite temsilî bölüm | Kalite çıtası + pipeline kanıtlı; greenlight kararı |
| **Alpha (Feature Complete)** | Tüm özellikler var; baştan sona oynanır; asset placeholder olabilir | **Feature freeze** — sonrasında yeni özellik yok |
| **Beta (Content Complete)** | Tüm özellik + final asset; sadece bug-fix/balance | **Content freeze**; ship-blocker yok |
| **Release Candidate / Gold** | Final build, certification geçti | Sıfır bilinen blocker; cert geçer; onaylı |

**Pratik kural:** *feature freeze (alpha)* ve *content freeze (beta)* sert kapılardır. En sık üretim hatası: alpha'dan sonra özellik eklemek (stabilizasyon saatini sıfırlar).

---

## 4. GDD — modern, hafif yaklaşım

Lean, **yaşayan** iletişim aracı; 100-sayfalık veritabanı değil.

- **Tek sayfayla başla** (Stone Librande disiplini): başlık + tagline, tek-paragraf elevator pitch, **design pillars**, kitle/platform, core loop, ana mekanikler, ikincil sistemler, progression, art/audio yönü, kaba roadmap. **Görsel** (harita/akış şeması) > yoğun metin. Okuyan çekirdeği ~30 saniyede kavramalı.
- **Pillars:** 3–5 kısa öbek (MDA estetiklerine eşlenir); her karar bunlara karşı sınanır. **Non-goals** da yaz.
- **Katman katman büyüt:** 1 sayfa → ~10 sayfa → tam doküman; baştan tam doküman yazma.
- **Kaçın:** test edilmemiş mekaniği prototipten önce aşırı-spesifikleştirme; büyük/erken eskiyen doküman; sistem ilişkilerini dağınık wiki sayfalarına gömme.

---

## 5. İterasyon & playtest

**Döngü:** hipotez → en küçük test edilebilir sürümü kur → playtest/gözle → ölç → kes/ayarla → tekrar. **Tasarımlar hipotezdir; playtest deneydir (Valve).**

- **Türler:** internal (oynanır olur olmaz devler) · external/taze oyuncu (şart; dev kendi oyununa kördür) · **Kleenex testing** (her test oyuncusunu **bir kez** kullan — ilk-izlenim/onboarding bir kez yaşanır) · usability ("kullanabiliyor mu?") vs experience ("hedef estetik çıkıyor mu?").
- **Ne gözlemlenir:** söylediği değil **yaptığı** — kafa karışıklığı, tereddüt, takılma/çıkma, bölüm başına süre, fail sıklığı. Protokol: gözlem → kısa anket → kısa Q&A. Biyometri gerekmez. Valve level tasarımcıları **her hafta** playtest yapar.
- **Telemetri:** fail noktaları, level başına deneme, drop-off, oturum süresi, churn'ü logla; soft-launch sonrası retune et ve **level sırasını değiştir** (bkz. 08).

---

## 6. Scoping & kesme (MVP)

- **MVP** = sadece çekirdek özellikler, en hızlı şekilde test oyuncusuna.
- **Kill your darlings:** vizyona hizmet etmeyen sevgili özellikleri atmaya razı ol. "Yapabiliyor olman yapmalısın demek değil — şişkinlik oyunu öldürür."
- **MoSCoW:** Must / Should / Could / Won't. "Must"ı kilitle; gerisi kesilebilir.
- Scope creep solo/indie'nin varsayılan başarısızlık modudur — pillar'lara ve MVP tanımına karşı aktif yönet.

---

## Kaynaklar

- What Is the Game Development Life Cycle? — Game Developer: https://www.gamedeveloper.com/business/what-is-the-game-development-life-cycle-
- What you should take out of Pre-Production — Game Developer: https://gamedeveloper.com/blogs/what-you-should-take-out-of-pre-production
- Vertical Slice in Game Development — Nineva: https://ninevastudios.com/blog/vertical-slice-game-development-guide
- Milestones: Alpha, Beta and Gold — Experimental Game Studio: https://mycours.es/gamedesign2021/milestone-beta/
- How to write a game design document — Game Dev Beginner: https://gamedevbeginner.com/how-to-write-a-game-design-document-with-examples/
- Valve's philosophy with User Research — Steve Bromley: https://www.stevebromley.com/blog/2011/09/01/valves-philosophy-with-user-research-in-games-habe-newell-and-mike-ambinder/
- Playtest / Kleenex testing — Wikipedia: https://en.wikipedia.org/wiki/Playtest
- Solving Scope Creep with Iterative Game Planning — Wayline: https://www.wayline.io/blog/scope-creep-iterative-game-planning
