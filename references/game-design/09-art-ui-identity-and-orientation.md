# Per-Game Design Identity — Theme, UI/HUD, Typography, Orientation (MANDATORY)

> **Each game must look like ITS OWN brand — NOT a reskin of the previous one.** The enemy: applying "top stat-pills + bottom bar + the same rounded font + the same palette" to every game. Theme, UI, HUD layout, font, palette, motion personality, and the **core mechanic** must vary with the game's content. Orientation (portrait/landscape) is also chosen per game.

**Absolute rule:** **NO shared reuse of `overlay_widgets`/HUD/palette/font across games.** Code conventions (architecture, Bloc, pooling, responsive discipline) are shared; **visual/interaction identity is not.** A game is not "done" until the brand test (§6) passes.

---

## 1. HUD diegesis taxonomy (Fagerholt & Lorentzon) — choose this first

Two axes: **fiction** (is the character aware?) × **geometry** (in the world, or a flat overlay?).

| | In-fiction (character aware) | Out-of-fiction (player only) |
|---|---|---|
| **In world geometry** | **Diegetic** (Dead Space back-mounted health) | **Spatial** (glow behind a wall, waypoint) |
| **Flat overlay** | **Meta** (blood splatter, low-health vignette) | **Non-diegetic** (classic HUD bar/pill) |

- **Diegetic:** maximum immersion, high cost, readability risk at small scale; decide in preproduction.
- **Non-diegetic:** the cheapest/clearest, the least immersive; good for information-dense/strategy/top-down — but it should adopt the world's visual language and fade in/out by context.
- **Spatial:** navigation/multiplayer awareness; overuse becomes visual noise.
- **Meta:** emotion via screen effects; **always an accessibility toggle**, don't apply heavy distortion that hides information when health is lowest.

**Distinctness rule:** assign each new game a **different primary diegesis from the previous one**. (E.g. A = meta-heavy / almost no overlay; B = diegetic in-world readout; C = context-fading non-diegetic.) Even with the same mechanic, it can't be samey.

---

## 2. HUD layout by genre

Principle: fast game → minimal, glanceable, edge-aligned; slow game → layered information. **Avoid the reflexive "fill the corners"** — make frequently-changing critical information near-center or diegetic; the corner is only for static information the brain filters out.

| Genre | Where the info is | Amount | Input | Distinguishing move |
|---|---|---|---|---|
| Survivor/bullet-heaven | XP bar top edge (full width), timer top-center, level compact | Little during a run, dense in the level-up modal | single joystick (auto-fire) | Center the action, push the HUD to a thin top strip; choices live on upgrade cards |
| Match-3/puzzle | Score+moves on top, objectives on a side rail/top strip; board centered | Low-medium, static | tap/swipe the board | Frame the board like a "table"; diegetic board chrome (no floating pills) |
| Idle/merge | Currency top bar (big numbers), board centered, prestige+shop bottom tabs | High but static | tap; bottom tab nav | Make the number readouts hero-UI; a tab bar is legitimate here |
| Runner | Score/distance top-center, coins in a corner | Minimal | swipe/tap, one hand | Almost zero HUD; speed lines + screen FX (meta) |
| Tower defense | Resources on top, wave/health in a corner, build palette docked bottom/side | Medium-high | tap to place; drag from the tray | The build tray = identity; a diegetic "control panel," not a generic bar |
| Arcade | Score top-center (big), lives icon | Little | direction/tap | Make bold numeric typography the entire aesthetic |
| Narrative/IF | Dialogue box at bottom (or a full overlay), state subtle | Very little | tap to advance, choice buttons | HUD = the text frame; the signature element is the dialogue panel |

**Anti-samey:** two consecutive games shouldn't use the **same anchor pattern**. If the previous one was "top pill + bottom tab bar," the next should be "thin top strip + center action + modal choice" or "diegetic in-world readout + no bottom bar."

---

## 3. Typography (a font trio of its own for each game)

**3 roles — keep them separate:** **Display/heading** (characterful; logo/splash/title — carries the brand) · **UI/body** (clean, clarity first; menu/dialogue/HUD labels) · **Numeric** (highly legible, **tabular/monospace** so the score/timer doesn't jump when digits change).

**Tone by genre:** fantasy→ornate/hand-drawn · sci-fi→geometric modular sans · racing/sports→bold condensed · casual/kids→rounded · horror→distressed display (UI still legible) · retro→pixel/blocky · elegant/romance→high-contrast serif.

**Rules:** one characterful display + one clean text (no pairing of two displays). At small sizes: large x-height, low stroke-contrast, verify kerning/hinting on-device; 50–80 chars/line, 130–150% line spacing; medium weight. **A default/system font (Roboto/SF/Arial) in a heading = the #1 low-effort tell — never.** Licensing: Google Fonts are mostly **OFL** (commercial use + embedding free); put the `.ttf` in `assets/fonts/`, the OFL text alongside it, declare it in pubspec; verify the target-language glyphs (TR: ş/ğ/ı) + fallback.

**Distinctness:** each game gets **its own display+UI+numeric trio.** Reusing the same font stack = a reskin.

---

## 4. Per-game visual identity (5 pillars)

1. **Palette:** tight/intentional — 1 primary, 1 accent, 2–3 neutrals, + semantic (good/bad/warning). Each game gets a **different hue family + saturation + light/dark base**.
2. **Form language:** pick one and apply it (sharp-angular / soft-rounded / organic-blob / beveled-skeuomorphic). Panels, buttons, and icons should all speak the same language.
3. **Iconography:** a consistent set (line/filled/chunky), matching the form language. One game's icons shouldn't fall into another's.
4. **Button/panel style:** corner radius, stroke, fill (flat/gradient/glass), depth/shadow, pressed state. The most-repeated (and most revealing) kit — change it deliberately.
5. **Motion personality:** easing curves, transition style, idle/hover micro-animation, juice. Snappy/punchy vs floaty/elegant vs springy/playful. Motion is a brand signal.

**Brand test:** mute the gameplay; show only a button + panel + icon + number. The team should be able to say "which game is this?" If they can't → reskin, failed.

---

## 5. Orientation: portrait vs landscape (choose per game)

Don't make everything portrait — orientation is a distinctness lever and it determines grip/gameplay.

- **Portrait** = usually **one hand**, thumb; on the go; tap-centric/low active area. Place interactive controls at the **bottom and edges** (top-center is far from a one-handed grip).
- **Landscape** = usually **two hands**, two-edge thumbs (console grip); seated/focused; wide horizontal area, lots of active play. The more active the game, the more landscape makes sense.

| Genre | Preference | Why |
|---|---|---|
| Idle/merge/tycoon | Portrait | tap, one hand, on the go |
| Match-3/puzzle | Portrait | the board fits in portrait, one hand |
| Runner | Portrait or landscape | depends on lane geometry |
| Survivor/bullet-heaven | **Landscape** | wide active area for the arena, two thumbs |
| Tower defense | **Landscape** | wide map + build tray |
| Arcade | Depends on the mechanic | match it to the grip |
| Narrative/IF | Portrait | reading + one-handed advancing |

Orientation changes the **HUD/control layout** (not just the aspect): portrait → controls bottom/edge, HUD a top strip; landscape → two-edge thumbs, HUD wide on top. **Flame/Flutter:** lock it per game with `SystemChrome.setPreferredOrientations(...)` before `runApp` in `main()`; design the HUD **for a single orientation** (one HUD shouldn't serve two orientations); fixed-resolution camera + anchor to the viewport edge. General responsive: `references/responsive-design.md`.

---

## 6. Anti-reskin (bespoke-identity) checklist — before every game

A reskin/asset-flip look is instantly branded "cheap" by players (and hurts store discovery). For every new game:

- [ ] Primary **diegesis** chosen and **different from the previous one**
- [ ] Unique **display** font (not system, not the last game's font)
- [ ] Unique **UI/body** font, legible at small size on-device
- [ ] **Numeric** font tabular/monospace; target-language glyphs verified
- [ ] Distinctive palette (1 primary/1 accent/neutrals/semantic) — different hue/base
- [ ] Form language declared (angular/rounded/organic/beveled) and applied to panel+button+icon
- [ ] Button/panel kit visually different (radius/fill/depth/pressed)
- [ ] Icon set bespoke — doesn't fall into another game
- [ ] Motion personality defined (easing/transition/juice) — not the global default
- [ ] **HUD anchor pattern different from the previous one**
- [ ] Orientation chosen by genre/grip; HUD built for that orientation
- [ ] Accessibility toggle on meta/screen-effect feedback
- [ ] **Brand test passed:** an isolated button+panel+icon+number is recognizable as belonging to this game
- [ ] Core mechanic different from the previous game (portfolio variety)

---

## Sources

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
