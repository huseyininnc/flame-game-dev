# AI Asset Generation (Vertex GenAI)

> The generator tools and `.env.example` are **embedded** within this skill (`scripts/`, relative to the skill root). For open source, the tools are **generic & config (manifest) driven** — you don't write a separate script per game; you write a JSON manifest and run a single tool. Setup: `cd scripts && pip install -r requirements.txt && cp .env.example .env` (put `VERTEX_API_KEY` in `.env`; `.env` is not committed). Full usage: `scripts/README.md`.

Two generic tools:
- **`scripts/asset_gen.py`** — images via Vertex GenAI (Gemini image, `gemini-3-pro-image-preview`); prompt-driven; opaque or chroma-key transparent; saves webp.
- **`scripts/audio_gen.py`** — synthesized sfx/bgm (`.wav`) using only the Python stdlib; no dependencies.

## Image generation (manifest)

```bash
python asset_gen.py --manifest mygame_assets.json --out <game>/assets/images
```

Manifest:
```json
{
  "style": "global style-guide appended to every prompt (optional)",
  "assets": [
    {"name":"bg",    "aspect":"9:16","mode":"opaque",  "prompt":"..."},
    {"name":"hero",  "aspect":"1:1", "mode":"magenta", "prompt":"..."},
    {"name":"enemy", "aspect":"1:1", "mode":"green",   "prompt":"..."}
  ]
}
```
- `mode: opaque` → opaque webp (background, icon, full-frame scene).
- `mode: green | magenta` → generated on that chroma screen, then a **transparent** webp via cutout. (This model does not produce real alpha from a "transparent background" prompt; transparency comes from chroma + cutout.)
- **Choose the chroma color so it does not clash with the subject:** green/cyan/blue subject → `magenta`; red/magenta subject → `green`. (If you generate a green subject on a green screen, it gets keyed out and deleted.)
- `name` may contain a sub-folder (`ui/button`). Flags: `--model --delay --overwrite --api-key`.

## Art direction is free (AUTOMATIC per game)

The style is chosen according to the game's content/theme — modern flat/vector, painterly, cartoon, isometric, pixel-art, etc. **Pixel-art is not mandatory/default.** For each game, define a **single consistent style-guide** (the manifest `style` field) and apply it to all assets. Per-game visual identity rules: `references/game-design/09-art-ui-identity-and-orientation.md`.

## Image prompt pattern
```
<subject>, <style-guide: modern flat / painterly / vector / pixel art ...>,
<palette/color>, centered, single subject,
no text, no watermark, fully original, no existing characters or brands.
```
(`asset_gen.py` automatically appends the chroma-screen sentence based on `mode` — don't write it again in the manifest.)

## Audio generation (manifest)

```bash
python audio_gen.py --manifest mygame_audio.json --out <game>/assets/audio
```
`sfx` = a `tone` `ops` array (`freq` or chord `freqs`, `dur`, ops: `vol/shape(sine|square|tri)/glide/attack/release`); `music` = an ambient pad (`voices`, `seconds`). sfx short (`assets/audio/sfx/`), bgm loop (`assets/audio/music/`). Engine side: `FlameAudio.play` / `FlameAudio.bgm` (see `references/flame/08`).

## Security / credentials

- The API key goes in `scripts/.env` (protected by `.gitignore`) or via `--api-key` / env — **never committed**, never embedded inside a prompt/manifest.
- Always add `fully original, no existing IP, no brand logos, no copyrighted characters, no text` to prompts (copyright safety; see game-greenlight `copyright-clearance`).
- Do not let raw PNG outputs bloat the repo; only the final webp/wav go under `assets/`.

## Flow

1. Define the game's style-guide + art direction + per-game identity (KB/09).
2. Write the image + audio **manifests** (game-specific; choose chroma modes based on the subject).
3. Run `asset_gen.py` / `audio_gen.py` → review → they land under `assets/images/` (webp) and `assets/audio/`.
4. Add `assets/` to `pubspec.yaml`; preload with `Sprite.load` in `onLoad`.
