# Contributing to flame-game-dev

Thanks for your interest — this is an open, evolving Claude Code skill and
contributions are welcome, whether that's fixing a typo, sharpening a knowledge-base
doc, improving the asset tools, or proposing a new reference.

## Ways to contribute

- **Report / discuss:** open an [issue](https://github.com/huseyininnc/flame-game-dev/issues)
  for bugs, gaps, or ideas before a large change.
- **Improve the knowledge bases** (`references/flame/`, `references/game-design/`):
  add sourced, actionable rules; fix inaccuracies; expand coverage.
- **Improve the tools** (`scripts/asset_gen.py`, `scripts/audio_gen.py`).
- **Improve the skill rules** (`SKILL.md`, checklists, `production-standards.md`).

## Workflow

1. Fork the repo and create a branch: `git checkout -b feat/short-description`.
2. Make your change (keep it focused — one logical change per PR).
3. Commit with a clear message: `type(scope): description`
   (`feat`, `fix`, `docs`, `refactor`, `chore`). Example: `docs(game-design): add HUD diegesis examples`.
4. Open a pull request describing **what** changed and **why**.

## Documentation conventions (`references/**`)

The knowledge bases are the heart of this skill. Keep them:

- **Sourced** — cite real, authoritative URLs (GDC, gamedeveloper.com, official docs,
  books). Add them to the doc's `## Sources` section.
- **Actionable** — concrete DO/DON'T rules, tables, and checklists over vague prose.
- **Accurate** — verify API/version claims against the stated package versions.
- **English** — all prose in clear, professional English.
- **Structured** — follow the existing numbering, headings, and table style; update the
  folder `README.md` index when you add a doc.

## Code conventions

**Dart examples** in the docs follow the skill's own rules so they stay copy-pasteable:

- No comments in example code (self-documenting names).
- SOLID / DRY / KISS / YAGNI; `very_good_analysis`-clean; no `any`/`dynamic`.
- Current Flame API (`CameraComponent` + `World`, `TapCallbacks`/`DragCallbacks`,
  `HasGameReference`).

**Python tools** (`scripts/`): keep them generic and config (manifest) driven — no
game-specific hardcoding, no personal absolute paths. Provide `argparse` help for any
new flag. Standard library preferred; new dependencies need a good reason.

## Design principles to respect

- **Per-game identity (anti-reskin):** keep guidance pushing each game toward its own
  theme/HUD/font/palette/motion/orientation — see
  `references/game-design/09-art-ui-identity-and-orientation.md`.
- **Studio-grade bar:** the skill targets production-ready, content-rich games, not
  MVP-as-product demos — see `references/production-standards.md`.
- **Art direction is per game** (pixel-art is not mandatory).

## Security — never commit secrets

- **Never commit `.env` or API keys.** `.env` is git-ignored; use
  `scripts/.env.example` as the template.
- Never paste keys into issues, PRs, prompts, or manifests.
- Generated asset prompts must stay copyright-safe (`fully original, no existing IP,
  no brand logos, no copyrighted characters, no text`).

## Code of conduct

Be respectful and constructive. Assume good faith, keep discussions about the work,
and help newcomers.

## License

By contributing, you agree your contributions are licensed under the project's
[MIT License](LICENSE).
