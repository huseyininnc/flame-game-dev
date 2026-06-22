# Game Feel & "Juice"

The layer of satisfaction added **after** the mechanic works correctly. The same mechanic feels completely different with juice (Vlambeer's Breakout demo: same rules, transformed by juice). In Flame, most of this is implemented with `Effect`/`EffectController` + particles + sound (see `references/flame/05-effects-and-particles.md`, `08-audio-and-tiled.md`).

---

## 1. The 3 pillars of game feel (Swink)

1. **Real-time control** — responsive input; the correction loop should feel under ~100 ms. **This is the foundation**; without responsive control, juice feels hollow.
2. **Simulated space** — a world with movement, collision, weight, gravity, and momentum.
3. **Polish** — an audiovisual layer that emphasizes every interaction.

**Golden rule:** "You can't squeeze good juice from a flavorless fruit." Control + core mechanic first; polish after.

---

## 2. Juice checklist (actionable list)

**Movement / animation**
- **Squash & stretch:** deformation on jump, landing, and collision → a sense of weight and force. (Flame: non-uniform `ScaleEffect`.)
- **Easing / tweening:** never move anything linearly; use ease-in/out curves (easings.net). Exponential for snappy, quadratic for soft. (Flame: `CurvedEffectController`, `Curves.easeOut`.)
- **Anticipation & follow-through:** a wind-up before the action, an overshoot/settle after (wobble/jiggle).
- **Trail:** a trail on a fast object — but **cut the trail** on impact (it softens the hit otherwise).
- **Scale pulse/bounce:** liveliness on spawn, pickup, UI. (The merge flash in Mitomerge is an example of this.)

**Impact / timing**
- **Screenshake:** shake the camera for a moment on a punch/explosion/big jump. Scale magnitude to the event, keep it **short**, avoid nausea. (Flame: a short `MoveEffect`/noise on top of `camera.viewfinder`.)
- **Hit-stop / freeze frame ("hold"):** freeze the game for a moment on a strong collision/kill. Bigger hit = longer hold. The cheapest, most powerful impact tool.
- **Knockback / recoil:** on both the striker and the struck.

**Particles & trails**
- **Dust** on landing/running, **sparks/stars** on collision, **debris/splash** on impact.
- Persistent ground marks (footprints, landing decals) reinforce the mechanic.

**Color / shading**
- **Hit flash** (flash to white/red on damage), a saturation pop on an important element against a muted background.

**Sound (half of the juice — don't neglect it)**
- **Every player interaction must have clear audio feedback.**
- Lightly compress the SFX / bring forward the bass-mid so it "pops."
- A subtle ambient loop beneath the music.

---

## 3. Juice principles

- **Match the genre/core loop:** bold screenshake for action; subtle motion for narrative/horror.
- **Synergy > excess:** stack wobble + particles + sound + hit-stop **together** on the same event; don't overuse a single effect everywhere.
- **Foundation first:** no polishing before control and the core mechanic are solid.
- **Accessibility:** consider an off switch for screenshake/flash (photosensitivity, nausea).

---

## Sources

- Game Feel — Steve Swink (Ch.1, PDF): http://mycours.es/gamedesign2014/files/2014/10/Game-Feel-Steve-Swink-chapter-1.pdf
- Squeezing More Juice Out of Your Game Design — Game Developer: https://www.gamedeveloper.com/design/squeezing-more-juice-out-of-your-game-design-
- Juice it or lose it / The Art of Screenshake — Vlambeer (Jonasson & Purho)
- Easing reference: https://easings.net/
- Designing Game Feel: A Survey — arXiv: https://arxiv.org/pdf/2011.09201
