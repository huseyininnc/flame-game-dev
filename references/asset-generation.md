# AI Asset Üretimi (Vertex GenAI)

> Üretici araçlar ve `.env.example` bu skill içinde **gömülüdür** (`scripts/`, skill köküne göreli). Açık kaynak için araçlar **generic & config (manifest) güdümlüdür** — her oyuna ayrı betik yazılmaz; bir JSON manifest yazıp tek aracı çalıştırırsın. Kurulum: `cd scripts && pip install -r requirements.txt && cp .env.example .env` (`.env`'e `VERTEX_API_KEY` koy; `.env` commit edilmez). Tam kullanım: `scripts/README.md`.

İki generic araç:
- **`scripts/asset_gen.py`** — Vertex GenAI (Gemini image, `gemini-3-pro-image-preview`) ile görseller; prompt-driven; opaque veya chroma-key şeffaf; webp kaydeder.
- **`scripts/audio_gen.py`** — sadece Python stdlib ile sentez sfx/bgm (`.wav`); bağımlılık yok.

## Görsel üretimi (manifest)

```bash
python asset_gen.py --manifest mygame_assets.json --out <oyun>/assets/images
```

Manifest:
```json
{
  "style": "her prompt'a eklenen global style-guide (opsiyonel)",
  "assets": [
    {"name":"bg",    "aspect":"9:16","mode":"opaque",  "prompt":"..."},
    {"name":"hero",  "aspect":"1:1", "mode":"magenta", "prompt":"..."},
    {"name":"enemy", "aspect":"1:1", "mode":"green",   "prompt":"..."}
  ]
}
```
- `mode: opaque` → opak webp (arka plan, ikon, full-frame sahne).
- `mode: green | magenta` → o chroma ekranda üretilir, sonra cutout ile **şeffaf** webp. (Bu model "transparent background" prompt'undan gerçek alfa vermez; şeffaflık chroma + cutout iledir.)
- **Chroma rengini özneyle çakışmayacak şekilde seç:** yeşil/cyan/mavi özne → `magenta`; kırmızı/magenta özne → `green`. (Yeşil özneyi yeşil ekranda üretirsen keylenip silinir.)
- `name` alt-klasör içerebilir (`ui/button`). Bayraklar: `--model --delay --overwrite --api-key`.

## Sanat yönü serbesttir (oyuna göre OTOMATİK)

Stil oyunun içeriğine/temasına göre seçilir — modern flat/vektör, painterly, cartoon, izometrik, pixel-art vb. **Pixel-art zorunlu/varsayılan değil.** Her oyunda **tutarlı tek style-guide** belirle (manifest `style` alanı) ve tüm asset'lere uygula. Per-game görsel kimlik kuralları: `references/game-design/09-art-ui-identity-and-orientation.md`.

## Görsel prompt kalıbı
```
<konu>, <stil-rehberi: modern flat / painterly / vektör / pixel art ...>,
<palet/renk>, centered, single subject,
no text, no watermark, fully original, no existing characters or brands.
```
(Chroma ekran cümlesini `asset_gen.py` `mode`'a göre otomatik ekler — manifest'te tekrar yazma.)

## Ses üretimi (manifest)

```bash
python audio_gen.py --manifest mygame_audio.json --out <oyun>/assets/audio
```
`sfx` = tone `ops` dizisi (`freq` veya akor `freqs`, `dur`, ops: `vol/shape(sine|square|tri)/glide/attack/release`); `music` = ambient pad (`voices`, `seconds`). sfx kısa (`assets/audio/sfx/`), bgm döngü (`assets/audio/music/`). Motor tarafı: `FlameAudio.play` / `FlameAudio.bgm` (bkz. `references/flame/08`).

## Güvenlik / kimlik bilgisi

- API anahtarı `scripts/.env` (`.gitignore` ile korunur) veya `--api-key` / env — **asla commit edilmez**, asla prompt/manifest içine gömülmez.
- Prompt'lara daima `fully original, no existing IP, no brand logos, no copyrighted characters, no text` ekle (telif güvenliği; bkz. game-greenlight `copyright-clearance`).
- Ham PNG çıktıları repo'yu şişirmesin; yalnızca son webp/wav `assets/` altına.

## Akış

1. Oyunun style-guide'ını + sanat yönünü + per-game kimliğini belirle (KB/09).
2. Görsel + ses **manifest**'lerini yaz (oyuna özel; chroma mode'larını özneye göre seç).
3. `asset_gen.py` / `audio_gen.py` çalıştır → gözden geçir → `assets/images/` (webp) ve `assets/audio/` altına yerleşir.
4. `pubspec.yaml`'a `assets/` ekle; `onLoad`'da `Sprite.load` ile preload.
