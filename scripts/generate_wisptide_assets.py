import io
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from PIL import Image

load_dotenv()

API_KEY = os.environ["VERTEX_API_KEY"]
MODEL = "gemini-3-pro-image-preview"
OUTPUT_DIR = r"C:\workspace\zeynsoft_projects\projects\games\wisptide\assets\images"

STYLE = (
    "painterly stylized digital game art, soft bioluminescent glow, smooth gradient "
    "shading, vibrant, clean readable silhouette, single subject centered and filling "
    "most of the frame, fully original, no existing IP, no brand logos, no text, "
    "no watermark"
)


def screen(color_word, hexcode):
    return (
        f"the subject stands alone on a perfectly flat uniform solid pure chroma key "
        f"{color_word} background, hex {hexcode}, the entire background is one single "
        f"flat {color_word} color, no scenery, no props, no cast shadow, no glow spill "
        f"onto the background, isolated studio cutout, centered"
    )


MAGENTA = screen("magenta", "#FF00FF")
GREEN = screen("green", "#00FF00")

ASSETS = [
    {"name": "wisp_hero", "aspect": "1:1", "key": "magenta",
     "prompt": "a cute glowing wisp light-being hero mascot, small round luminous "
               "core with a soft wispy trailing tail, warm gold (#FFD56B) and cyan "
               "(#5BE0FF) bioluminescent glow, friendly dot eyes, " + STYLE + ", "
               + MAGENTA},
    {"name": "enemy_shade", "aspect": "1:1", "key": "green",
     "prompt": "a small dark shadow creature enemy, deep violet-black blob body with "
               "magenta (#FF3DA6) rim light, glowing angry little eyes, " + STYLE
               + ", " + GREEN},
    {"name": "enemy_brute", "aspect": "1:1", "key": "green",
     "prompt": "a big bulky dark shadow brute enemy, heavy violet-black mass, thick "
               "magenta (#FF3DA6) rim light, menacing, " + STYLE + ", " + GREEN},
    {"name": "enemy_swift", "aspect": "1:1", "key": "green",
     "prompt": "a small sleek fast dark shadow wisp enemy, streamlined violet-black "
               "body, sharp magenta (#FF3DA6) rim light, " + STYLE + ", " + GREEN},
    {"name": "boss_maw", "aspect": "1:1", "key": "green",
     "prompt": "a large menacing shadow boss, dark violet-black bulbous mass with a "
               "glowing magenta (#FF3DA6) maw and eyes, spikes, intimidating "
               "silhouette, " + STYLE + ", " + GREEN},
    {"name": "bg_void", "aspect": "1:1", "key": "opaque",
     "prompt": "a seamless tileable top-down dark moody painterly void ground, deep "
               "navy-violet (#160E2A to #241640), subtle faint bioluminescent "
               "particles and soft glow specks, non-distracting, opaque full-bleed, "
               "no text, fully original"},
    {"name": "icon", "aspect": "1:1", "key": "opaque",
     "prompt": "modern painterly square mobile app icon, a single glowing gold-cyan "
               "wisp light-being facing a dark magenta-rimmed shadow swarm, high "
               "contrast, soft glow, readable at small size, rounded composition, "
               "no text, no logos, fully original"},
]


def generate_image(client, prompt, aspect, retries=5):
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["Text", "Image"],
                    image_config=types.ImageConfig(aspect_ratio=aspect),
                ),
            )
        except genai_errors.ClientError as error:
            if getattr(error, "code", None) == 429 and attempt < retries - 1:
                wait = 30 * (attempt + 1)
                print(f"  429, waiting {wait}s ...", flush=True)
                time.sleep(wait)
                continue
            raise
        candidates = getattr(response, "candidates", None) or []
        if not candidates:
            return None
        parts = getattr(getattr(candidates[0], "content", None), "parts", None) or []
        for part in parts:
            inline = getattr(part, "inline_data", None)
            if inline and getattr(inline, "data", None):
                return Image.open(io.BytesIO(inline.data))
        return None
    return None


def cutout_background(image, key):
    rgba = image.convert("RGBA")
    hsv = image.convert("RGB").convert("HSV")
    width, height = rgba.size
    pixels = rgba.load()
    hsv_pixels = hsv.load()
    for y in range(height):
        for x in range(width):
            hue, saturation, value = hsv_pixels[x, y]
            r, g, b, a = pixels[x, y]
            if key == "green":
                is_key = 55 <= hue <= 120 and saturation >= 55 and value >= 55
                if is_key:
                    pixels[x, y] = (r, g, b, 0)
                elif g > r and g > b:
                    pixels[x, y] = (r, min(g, (r + b) // 2 + 14), b, a)
            else:
                is_key = 195 <= hue <= 240 and saturation >= 55 and value >= 55
                if is_key:
                    pixels[x, y] = (r, g, b, 0)
                elif r > g:
                    pixels[x, y] = (min(r, g + 22), g, b, a)
    return rgba


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    client = genai.Client(vertexai=True, api_key=API_KEY)
    for asset in ASSETS:
        path = os.path.join(OUTPUT_DIR, f"{asset['name']}.webp")
        if os.path.exists(path):
            print(f"SKIP {asset['name']}", flush=True)
            continue
        print(f"Generating {asset['name']} (key={asset['key']}) ...", flush=True)
        image = generate_image(client, asset["prompt"], asset["aspect"])
        if image is None:
            print(f"  FAIL {asset['name']}", flush=True)
            continue
        if asset["key"] == "opaque":
            image.convert("RGB").save(path, "WEBP", quality=95)
        else:
            image = cutout_background(image, asset["key"])
            image.save(path, "WEBP", lossless=True)
        print(f"  OK {path} ({image.size[0]}x{image.size[1]})", flush=True)
        time.sleep(10)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
