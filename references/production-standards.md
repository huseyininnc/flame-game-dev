# Studio-Grade Production Standards (MANDATORY BAR)

> **This skill DOES NOT PRODUCE amateur, short, "MVP-as-product", single-mechanic tech-demo games.** Every game produced must feel like it came out of a large studio staffed by senior teams with 15+ years of experience — **production-ready, content-rich, multi-asset, full release.** This document defines the bar and the "definition of done"; its items count as **release blockers.**

**Core thesis:** Professional quality is not one big thing — it is **the sum of dozens of small polish layers that the amateur skips one by one.** The MVP/prototype exists only to find the "fun" during preproduction; **the delivered product must always be complete, polished, content-rich.** "You can't make good juice from a flavorless fruit" — polish amplifies a solid core, it does not replace it.

---

## 1. Content scope baselines (minimum at launch)

A prototype proves one mechanic in 2–5 min. A full game offers **hours of structured progression** — early/mid/late game. The difference: **validated content volume + the system treadmill that feeds it.**

| Genre | Launch content baseline | Note |
|---|---|---|
| **Match-3 / puzzle** | **100–200 hand-built levels** | Candy Crush Soda shipped with 150; 100+ is a credible minimum for "real" puzzles |
| **Hybrid-casual (arena/action)** | **3–5 distinct mechanics** + 1 progression backbone + 1 meta layer; 30–60 min without repetition | Single mechanic = hypercasual = thin |
| **Idle / incremental** | **40–60 hours of content**, **2–4 prestige layers**, **30–50 upgrades/nodes**, skill tree | Each prestige layer should unlock a new MECHANIC, not just bigger numbers |
| **Wave / arena defense** | **3+ biomes/themes**, **8–15 enemy/unit types**, escalating wave composition | A reskin of a single enemy = demo |

**Rules:**
- **Ship early + mid + LATE game.** Strong D1 + a sharp D7 drop = the signature of "no content depth beyond the core loop." Late-game systems (prestige, mastery, endless, collection) produce D30.
- **Distinct mechanics, not reskins.** New "things" to learn should keep arriving throughout the early game (Royal Match introduces a new blocker/power-up every 1–3 levels).
- **Collection/set** as a long-tail hook.
- **Post-launch cadence:** new content every **1–2 weeks** (industry rhythm); rotating event archetypes (competitive / recurring / collectible).

---

## 2. Full system stack (Definition of Done — not MVP)

The MVP proves the core loop. **A full game ships with ALL of the support systems below.** ★ = mandatory at launch; the rest may be fast-follow as long as their scaffold is in place at launch.

**Core:** ★ core loop · ★ level/wave/stage progression backbone · ★ difficulty curve/dynamic tuning.
**Meta progression:** ★ player level/XP/mastery · ★ persistent upgrade/unlock path · prestige/rebirth (★ in idle) · collection/album/set.
**Economy & monetization:** ★ at least **2 currencies** (soft+hard) · ★ shop/IAP (server validation) · ★ ads mediation (rewarded core; interstitial AFTER the player is hooked) · battle/season pass · LTO · monetization streak.
**Engagement/retention:** ★ daily reward/login streak · ★ tutorial/FTUE (the biggest D1 lever) · events system · achievements · leaderboard/social.
**Infrastructure:** ★ settings (audio/language/privacy) · ★ save/persistence (+cloud strongly recommended) · ★ analytics + funnel instrumentation (step-by-step tutorial drop-off is mandatory) · A/B test harness.

**Launch must-have summary:** core loop + progression backbone + 2 currencies + shop/IAP + ads mediation + daily reward + FTUE + settings + save(+cloud) + analytics. Battle pass/events/leaderboard/achievement can be fast-follow, but **leave their sockets in place at launch** (a system you can build on with live-ops).

**Staggered onboarding (don't dump everything at once):** ~**20 levels of pure fun**, then the first live-op/monetization. Earn the right to monetize. Adding a permanent reward source **requires a rebalance** (inflation); design source and sink together.

---

## 3. Polish / game-feel bar (the real differentiator)

The *most loaded* difference between amateur and professional. Apply the layers below to **every interaction** (detail: `references/game-design/04-game-feel-and-juice.md`).

- **Easing on everything** (no linear/snap): tween position, scale, rotation, color, opacity (Flame `EffectController`+curve). · **Hit-stop / freeze** (~30–80ms) on strong impacts. · **Screenshake** scaled to the event, with decay (not fixed/excessive). · **Knockback + recoil** (bidirectional). · **Camera lerp + kick.** · **Anticipation + follow-through.** · **Secondary motion** (trail, jiggle, debris). · **Permanence** (lasting marks). · **Sound on every action** + **haptics** (mobile). · particles/VFX scaled to the event and randomized.

**Visual consistency (the biggest amateur tell = inconsistency):**
- **One style guide, mandatory:** locked palette, single light direction, consistent ratio/PPU, consistent icon language. · **NO placeholder/programmer-art/default fonts.** · Mixed styles (asset-store + custom, pixel + smooth-vector) = reads as broken. · Animation on everything (idle, enter/exit, anticipation). · Strong silhouette + contrast (readability).

**UI/UX polish:** **animated transitions** between screens (no hard-cut) · one design system · juicy buttons (press/release/sound/haptic/disabled/loading) · all states (default/press/disabled/loading/empty/error) · no default/themeless widgets · large touch targets & thumb-zone.

**Audio:** sound on every interaction · layered + pitch-randomized SFX · adaptive/looping music + crossfade · mixing/ducking · separate Music/SFX volume + respect for silent mode.

**"Professional feel" — measurable targets:**
- **Input latency:** ≤ **66ms** at 60fps; never > **133ms** (action). First feedback < **100ms**.
- **Locked 60 FPS** (unless slow/turn-based), no jank/GC-stall. Steady 30 > stuttering 45–60.

---

## 4. Launch-readiness checklist (release blocker)

**Stability:** crash-free session ≥ **99.7%** (crash ≤ 0.3%) · Google Play vitals: user-perceived crash < **1.09%**, ANR < **0.47%** · zero crashes on the FTUE/first 15 min path · no memory-leak/OOM in long sessions · crash reporting (symbolicated) working.
**Performance:** locked target fps holds on a mid-tier device · cold start a few sec, level transition <1s where possible (loading indicator if >1s) · memory budget, no growth (leak) curve · no battery/thermal throttling · App Bundle if >150MB.
**Device coverage:** low/mid/high tier, multiple screens/aspects/notch/OS · portrait/landscape correct · Play Pre-launch report clean.
**Store assets:** icon 512×512 (≤1024KB) · ≥2 (4+ recommended) screenshots, first 2–3 as conversion drivers · feature graphic · preview video 30–120s · keyword-optimized title/description (ASO).
**Rating/privacy:** content/age rating · active **privacy policy URL** (even if no data is collected) · Data Safety / ATT · IAP disclosure + "restore" tested.
**Accessibility (numeric):** touch target ≥ **48dp (Android) / 44pt (iOS)** · color alone does not carry information (shape/icon/pattern) · text scales (OS dynamic type) · **reduce-motion** option, no flashing · captions/subtitles (customizable) · separate SFX/Music/speech volume · TalkBack/VoiceOver verified in menus.
**Localization:** all strings externalized (Flutter ARB) · UTF-8 + locale formatting · text-expansion tolerance (+30–40% DE) · RTL (Arabic/Hebrew, `Directionality`) · font coverage (no tofu) · pseudo-localization pass.
**QA & telemetry:** alpha=feature-freeze → beta=content-freeze · regression (fps/memory/load numeric) on every build · soft-launch (limited geo) to read D1/D7/D30 + funnel · event taxonomy (progression/economy/business/error) + FTUE funnel + app-version tag · A/B harness (remote config).
**Live-ops:** remote config (balance/pricing/FTUE/flag without a client update) · data-driven content pipeline · event cadence (per the team; 72-hour Fri–Sun is the golden window) · rollback/kill-switch + staged rollout.

---

## 5. Scope discipline: ambitious BUT finishable

The way to produce volume without drowning is **systems, not handcraft**:
- **Data-driven content:** define level/wave/enemy/upgrade as **config (data)**, not code. Build the engine once; pour content out as data forever. (See `references/game-design/08-level-design-for-2d-casual.md`.)
- **Parametric/template content:** generate level configs from a parametric model ("level design as a service").
- **Reused systems:** one event framework (competitive+recurring+collectible), one currency, one shop, one reward dispenser — parameterized.
- **Modular content:** biome = palette-swap + new data; new enemy = a data row + sprite, not a new code path.
- **Set a KPI target** (retention/funnel), avoid data-inspired drift.
- **Protect the polish budget:** plan it as a fixed phase (≥ ~2 months equivalent effort); don't let content production eat it.

**Production order:** vertical slice (near-final quality, not a prototype) → content production (alpha=all features present) → **protected polish** → soft launch (read D1/D7/D30, iterate) → launch (RC → gold).

**One-line scope formula:** Bring reusable, data-driven systems to vertical-slice quality; then pour modular content as data up to launch volume (e.g. 100–200 puzzle levels / 3–5 mechanics / 40–60 idle hours / 8–15 enemies+3 biomes); wrap it with the must-have system stack; stagger meta/monetization (~20 levels of fun first); feed it on a 1–2 week cadence.

---

## 6. Amateur tells (ABSOLUTELY avoid)

- Default font/background · mixed/mismatched art · placeholder/programmer-art in a shipped build · inconsistent light/palette · snapping static sprites · low contrast/weak silhouette.
- Linear/snap movement (no easing) · weightless impact (no hit-stop/knockback/shake) · rigid 1:1 camera · a world that leaves no marks · either no juice at all or excessive shake.
- Hard-cut screen transition · themeless/default widgets · static/silent buttons · empty/frozen loading/dead-end error · small touch targets.
- Silent interaction · a single repeating clip · hard-restart music · no audio setting · flat/clipping mix.
- Unmeasured/>133ms latency · stuttering fps/jank · no feedback · wall-of-text/no onboarding · dead micro-interactions.
- **A single mechanic + a few screens shipped as a "full game"** (demo smell) · only "early" game, no mid/late · no content variety.

---

## Resources

- The Art of Screenshake — Vlambeer (Jan Willem Nijman): https://www.youtube.com/watch?v=AJdEqssNZ-U
- Juice It or Lose It — Jonasson & Purho: https://www.youtube.com/watch?v=Fy0aCDmgnxg
- Measuring Responsiveness in Video Games (latency) — Game Developer: https://www.gamedeveloper.com/design/measuring-responsiveness-in-video-games
- Mobile Game Testing Checklist for Pre-Launch — Kobiton: https://kobiton.com/guides/mobile-game-testing-checklist-pre-launch-success/
- Understand your pre-launch report — Google Play Console: https://support.google.com/googleplay/android-developer/answer/9844487
- 2025 Mobile Gaming Benchmarks — GameAnalytics: https://www.gameanalytics.com/reports/2025-mobile-gaming-benchmarks
- Full list — Game Accessibility Guidelines: https://gameaccessibilityguidelines.com/full-list/
- App Screenshot/Icon/Video Guidelines (iOS & Android) — AppTweak: https://www.apptweak.com/en/aso-blog/app-screenshot-icon-video-guidelines-ios-gp
- App Localization Best Practices — Circle Translations: https://circletranslations.com/blog/app-localization-best-practices
- Why does Royal Match wait 22 levels for the first live-op? — Gamigion: https://www.gamigion.com/why-does-royal-match-wait-22-levels-to-introduce-their-first-live-op/
- Converging Live Ops Trends in Mobile Puzzle — Naavik: https://naavik.co/digest/live-ops-trends-powering-mobile-puzzle/
- Getting Started With Hybrid-Casual LiveOps — Supersonic: https://supersonic.com/learn/blog/getting-started-with-basic-hybrid-casual-liveops
- The True Drivers of D1, D7, D30 Retention — Solsten: https://solsten.io/blog/d1-d7-d30-retention-in-gaming
- Game Production Pipeline — GDKeys: https://gdkeys.com/game-development-process/
- Is data-driven design good for games? — Paolo's Blog: https://paolos.blog/data-driven-designed-games/
