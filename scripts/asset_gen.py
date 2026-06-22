import argparse
import io
import json
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from PIL import Image

DEFAULT_MODEL = "gemini-3-pro-image-preview"

CHROMA = {
    "green": {
        "desc": "solid pure chroma key green background, hex #00FF00",
        "hue": (55, 120),
    },
    "magenta": {
        "desc": "solid pure chroma key magenta background, hex #FF00FF",
        "hue": (195, 240),
    },
}

SCREEN_SUFFIX = (
    "the subject stands alone on a perfectly flat uniform {desc}; the entire "
    "background is one single flat color, no scenery, no props, no cast shadow, "
    "no glow spill onto the background, isolated studio cutout, centered"
)


def generate(client, model, prompt, aspect, retries):
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["Text", "Image"],
                    image_config=types.ImageConfig(aspect_ratio=aspect),
                ),
            )
        except genai_errors.ClientError as error:
            if getattr(error, "code", None) == 429 and attempt < retries - 1:
                wait = 30 * (attempt + 1)
                print(f"  rate limited, waiting {wait}s", flush=True)
                time.sleep(wait)
                continue
            raise
        candidates = getattr(response, "candidates", None) or []
        if not candidates:
            return None
        content = getattr(candidates[0], "content", None)
        for part in getattr(content, "parts", None) or []:
            inline = getattr(part, "inline_data", None)
            if inline and getattr(inline, "data", None):
                return Image.open(io.BytesIO(inline.data))
        return None
    return None


def chroma_cutout(image, mode):
    hue_low, hue_high = CHROMA[mode]["hue"]
    rgba = image.convert("RGBA")
    hsv = image.convert("RGB").convert("HSV")
    width, height = rgba.size
    pixels = rgba.load()
    hsv_pixels = hsv.load()
    for y in range(height):
        for x in range(width):
            hue, saturation, value = hsv_pixels[x, y]
            r, g, b, a = pixels[x, y]
            if hue_low <= hue <= hue_high and saturation >= 55 and value >= 55:
                pixels[x, y] = (r, g, b, 0)
            elif mode == "green" and g > r and g > b:
                pixels[x, y] = (r, min(g, (r + b) // 2 + 14), b, a)
            elif mode == "magenta" and r > g and b > g:
                pixels[x, y] = (min(r, g + 25), g, b, a)
    return rgba


def run(manifest, out_dir, model, delay, overwrite, api_key):
    client = genai.Client(vertexai=True, api_key=api_key)
    style = manifest.get("style", "")
    os.makedirs(out_dir, exist_ok=True)
    for asset in manifest["assets"]:
        name = asset["name"]
        mode = asset.get("mode", "opaque")
        aspect = asset.get("aspect", "1:1")
        path = os.path.join(out_dir, f"{name}.webp")
        if os.path.exists(path) and not overwrite:
            print(f"skip {name}", flush=True)
            continue
        prompt = asset["prompt"]
        if style:
            prompt = f"{prompt}, {style}"
        if mode in CHROMA:
            prompt = f"{prompt}. {SCREEN_SUFFIX.format(desc=CHROMA[mode]['desc'])}"
        print(f"generate {name} (mode={mode}, aspect={aspect})", flush=True)
        image = generate(client, model, prompt, aspect, retries=5)
        if image is None:
            print(f"  FAILED {name}", flush=True)
            continue
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        if mode == "opaque":
            image.convert("RGB").save(path, "WEBP", quality=95)
        else:
            chroma_cutout(image, mode).save(path, "WEBP", lossless=True)
        print(f"  saved {path} ({image.size[0]}x{image.size[1]})", flush=True)
        time.sleep(delay)
    print("done", flush=True)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generate original game image assets with Vertex GenAI (Gemini image "
            "model). Prompt-driven; opaque or chroma-key transparent (webp)."
        ),
    )
    parser.add_argument(
        "--manifest",
        required=True,
        help='JSON: {"style"?: str, "assets":[{"name","prompt","aspect"?,"mode"?}]}'
        ' where mode is "opaque" | "green" | "magenta".',
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output directory for .webp files (name may include subfolders).",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Image model id.")
    parser.add_argument(
        "--delay",
        type=float,
        default=8.0,
        help="Seconds to wait between generations (rate-limit friendly).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Regenerate assets even if the output file already exists.",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="Vertex API key (falls back to VERTEX_API_KEY env / .env).",
    )
    args = parser.parse_args()
    load_dotenv()
    api_key = args.api_key or os.environ.get("VERTEX_API_KEY")
    if not api_key:
        raise SystemExit("VERTEX_API_KEY not set (use --api-key, env var, or .env).")
    with open(args.manifest, encoding="utf-8") as handle:
        manifest = json.load(handle)
    run(manifest, args.out, args.model, args.delay, args.overwrite, api_key)


if __name__ == "__main__":
    main()
