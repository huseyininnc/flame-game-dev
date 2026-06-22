# flame-game-dev

A self-contained **Claude Code skill** for building studio-grade 2D games with the Flutter **Flame** engine — and designing them well. It bundles two verified knowledge bases (engine + game design), production standards, an asset-generation pipeline, and hard quality gates so every game ships production-ready, content-rich, and with its own distinct identity.

## What's inside

```
flame-game-dev/
├── SKILL.md                         # the skill: rules, KB index, new-game flow
├── references/
│   ├── flame/                       # technical KB (Flame engine) — 11 docs + README
│   ├── game-design/                 # design KB — 9 docs + README
│   │   ├── 01 foundations (MDA, loops, pillars, juice)
│   │   ├── 02 level design principles
│   │   ├── 03 difficulty & pacing
│   │   ├── 04 game feel & juice
│   │   ├── 05 onboarding / FTUE
│   │   ├── 06 progression / economy / retention
│   │   ├── 07 professional process
│   │   ├── 08 level design for 2D/casual/idle
│   │   └── 09 per-game art/UI/HUD/font identity + orientation
│   ├── production-standards.md       # studio-grade definition-of-done (hard gate)
│   ├── responsive-design.md          # Flutter + Flame responsive (art-style agnostic)
│   ├── asset-generation.md           # Vertex GenAI asset pipeline + chroma-key
│   ├── level-design-checklist.md
│   └── new-game-checklist.md
└── scripts/                          # Vertex GenAI asset/audio generators (Python)
    ├── generate_*_assets.py
    ├── requirements.txt
    └── .env.example                  # copy to .env and add your key (NOT committed)
```

## Core mandates (hard gates)

- **No comments in code**; SOLID/DRY/KISS/YAGNI; strictest lint (`very_good_analysis`).
- **Studio-grade only** — no amateur / MVP-as-product / single-mechanic demos. Full content scope + full systems stack + polish (`references/production-standards.md`).
- **Per-game identity (anti-reskin)** — each game gets its own theme, palette, HUD layout, UI/button style, font trio, motion personality, core mechanic, and orientation (portrait or landscape). No shared widget kit/HUD/palette/font across titles (`references/game-design/09-...`).
- **Responsive on every device**, art style auto-selected from game content (pixel-art not mandatory).
- **Original assets** generated from scratch via the `scripts/` Vertex pipeline.

## Asset generation setup

The generators use Vertex GenAI (`gemini-3-pro-image-preview`). Provide your key locally:

```bash
cd scripts
cp .env.example .env          # then edit .env and set VERTEX_API_KEY=...
pip install -r requirements.txt
python generate_<game>_assets.py
```

> `.env` is git-ignored on purpose — never commit your API key.

## Usage

Place this folder under `~/.claude/skills/flame-game-dev/`. In Claude Code, the skill activates for Flame game work; it reads its bundled `references/` as production rules. Pairs with the [`game-greenlight`](https://github.com/huseyininnc/game-greenlight) skill, which produces the Game PRD this skill builds.

## Contributing

Open source and open to development — contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

- Open an issue to propose ideas/changes, or fork and send a pull request.
- Follow the conventions in `SKILL.md`: **no code comments**, SOLID/DRY/KISS, `very_good_analysis`-clean Dart.
- **Never commit secrets** — `.env` is git-ignored; use `scripts/.env.example`.
- Improve the `references/` knowledge bases with **sourced, actionable** rules (cite real URLs); keep docs practical.
- Keep each game's identity distinct (see `references/game-design/09-...`) — no reskins.

## License

[MIT](LICENSE) © huseyininnc — free to use, modify, and build upon.
