# Asset generation tools

Two generic, config-driven generators for original game assets. No game-specific
code — describe what you want in a JSON manifest and point the tool at an output
directory.

- `asset_gen.py` — images via Vertex GenAI (Gemini image model), prompt-driven,
  opaque or chroma-key transparent, saved as `.webp`.
- `audio_gen.py` — royalty-free SFX/BGM (`.wav`) synthesized with the Python
  standard library only (no dependencies).

## Setup (images only)

```bash
pip install -r requirements.txt
cp .env.example .env        # then set VERTEX_API_KEY=...
```

`.env` is git-ignored — never commit your API key.

## Images

```bash
python asset_gen.py --manifest examples/assets.example.json --out ./assets/images
```

Manifest:

```json
{
  "style": "appended to every prompt (optional global style guide)",
  "assets": [
    { "name": "bg",    "aspect": "9:16", "mode": "opaque",  "prompt": "..." },
    { "name": "hero",  "aspect": "1:1",  "mode": "magenta", "prompt": "..." },
    { "name": "enemy", "aspect": "1:1",  "mode": "green",   "prompt": "..." }
  ]
}
```

- `mode: opaque` → saved as opaque webp (backgrounds, icons, full-frame scenes).
- `mode: green | magenta` → generated on that chroma screen, then cut out to a
  transparent webp.
- **Pick the chroma color that does NOT clash with the subject's color.** A green
  subject on a green screen gets keyed out. Rule of thumb: green/cyan/blue
  subjects → `magenta`; red/magenta subjects → `green`.
- `name` may include subfolders (e.g. `ui/button`).
- Flags: `--model`, `--delay`, `--overwrite`, `--api-key`.

> Note: this model does not produce real alpha from a "transparent background"
> prompt — that is why transparency uses a chroma screen + cutout.

## Audio

```bash
python audio_gen.py --manifest examples/audio.example.json --out ./assets/audio
```

Manifest: each `sfx` is a sequence of tone `ops` (`freq` or chord `freqs`, `dur`,
optional `vol`/`shape`(`sine|square|tri`)/`glide`/`attack`/`release`); each
`music` entry is an ambient pad (`voices`, `seconds`).

## License

[MIT](../LICENSE) — part of the `flame-game-dev` skill.
