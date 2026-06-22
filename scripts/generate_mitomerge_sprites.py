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
OUTPUT_DIR = r"C:\workspace\zeynsoft_projects\projects\games\mitomerge\assets\images"

STYLE = (
    "modern flat vector game art with soft bioluminescent inner glow, microscope "
    "petri aesthetic, rounded organic blobby form, smooth gradient shading, no "
    "harsh outline, single subject centered and filling most of the frame, fully "
    "original, no existing IP, no brand logos, no text, no watermark"
)


def screen(color_word, hexcode):
    return (
        f"the subject stands alone on a perfectly flat uniform solid pure chroma "
        f"key {color_word} background, hex {hexcode}, the entire background is one "
        f"single flat {color_word} color, no scenery, no props, no cast shadow, no "
        f"vignette, no glow spill onto the background, isolated studio green screen "
        f"style cutout, centered"
    )


MAGENTA = screen("magenta", "#FF00FF")
GREEN = screen("green", "#00FF00")

ASSETS = [
    {"name": "cell_antibody", "size": 256, "key": "magenta",
     "prompt": "a cute friendly Y-shaped antibody immune defender mascot, glowing "
               "mint green (#7BFF9E) body, smooth rounded arms, simple happy dot "
               "eyes, " + STYLE + ", " + MAGENTA},
    {"name": "cell_macrophage", "size": 256, "key": "magenta",
     "prompt": "a cute friendly macrophage immune defender cell, big rounded "
               "teal-cyan (#3DE0D5) blob body with tiny pseudopod bumps, simple "
               "happy dot eyes, " + STYLE + ", " + MAGENTA},
    {"name": "cell_tcell", "size": 256, "key": "magenta",
     "prompt": "a cute T-cell immune defender, rounded glowing aqua (#4DD0E1) body "
               "with a soft pulsing aura ring, simple confident dot eyes, " + STYLE
               + ", " + MAGENTA},
    {"name": "cell_interferon", "size": 256, "key": "magenta",
     "prompt": "a cute interferon signal cell, soft glowing ice blue (#80D8FF) "
               "wavy rounded body with a gentle frost aura, simple calm dot eyes, "
               + STYLE + ", " + MAGENTA},
    {"name": "pathogen_virus", "size": 256, "key": "green",
     "prompt": "a menacing virus particle enemy, magenta-red (#FF4D6D) spiky "
               "rounded shell with a glowing core and angry tiny eyes, " + STYLE
               + ", " + GREEN},
    {"name": "pathogen_bacteria", "size": 256, "key": "green",
     "prompt": "a tanky bacteria pathogen enemy, dark red (#C81D5A) rounded "
               "capsule rod shape with a thick membrane and grumpy tiny eyes, "
               + STYLE + ", " + GREEN},
    {"name": "pathogen_boss", "size": 256, "key": "green",
     "prompt": "a large menacing mutant pathogen boss, bulbous red-magenta "
               "(#FF1E56) body with spikes and a glowing shield aura, intimidating "
               "eyes, " + STYLE + ", " + GREEN},
    {"name": "nucleus_core", "size": 320, "key": "green",
     "prompt": "a glowing protective cell nucleus orb, warm gold core (#FFE08A) "
               "with a cyan rim (#3DE0D5) and a rounded crystalline membrane, "
               "radial bloom, " + STYLE + ", " + GREEN},
]


def generate_image(client, prompt, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["Text", "Image"],
                    image_config=types.ImageConfig(aspect_ratio="1:1"),
                ),
            )
        except genai_errors.ClientError as error:
            if getattr(error, "code", None) == 429 and attempt < max_retries - 1:
                wait = 30 * (attempt + 1)
                print(f"  429 rate limit, waiting {wait}s ...", flush=True)
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
                elif r > g and b > g:
                    pixels[x, y] = (min(r, g + 22), g, min(b, g + 60), a)
    return rgba


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    client = genai.Client(vertexai=True, api_key=API_KEY)
    for asset in ASSETS:
        path = os.path.join(OUTPUT_DIR, f"{asset['name']}.webp")
        if os.path.exists(path):
            print(f"SKIP {asset['name']} (exists)", flush=True)
            continue
        print(f"Generating {asset['name']} (key={asset['key']}) ...", flush=True)
        image = generate_image(client, asset["prompt"])
        if image is None:
            print(f"  FAIL: no image for {asset['name']}", flush=True)
            continue
        image = cutout_background(image, asset["key"])
        image = image.resize((asset["size"], asset["size"]), Image.LANCZOS)
        image.save(path, "WEBP", lossless=True)
        print(f"  OK: {path} ({image.size[0]}x{image.size[1]})", flush=True)
        time.sleep(12)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
