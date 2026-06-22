import io
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()

API_KEY = os.environ["VERTEX_API_KEY"]
MODEL = "gemini-3-pro-image-preview"
OUTPUT_DIR = r"C:\workspace\zeynsoft_projects\projects\games\mitomerge\assets\images"

ASSETS = [
    {"name": "bg_plasma", "aspect": "9:16",
     "prompt": (
         "modern flat tall vertical mobile game background, dark blood plasma, deep "
         "teal and navy vertical gradient (#0B1B2B at top to #0F2C3A at bottom), faint "
         "soft floating particle bokeh, subtle radial glow near the center, clean and "
         "non-distracting microscope petri aesthetic, no text, no characters, fully "
         "original, opaque full-bleed background filling the entire frame"
     )},
    {"name": "icon", "aspect": "1:1",
     "prompt": (
         "modern flat square mobile app icon, a single glowing cyan antibody cell "
         "mascot with simple friendly dot eyes centered on a dark teal plasma "
         "rounded-square background (#0B1B2B), high contrast, soft bioluminescent glow, "
         "readable at small size, no text, no logos, fully original, opaque background "
         "filling the full square"
     )},
]


def generate_image(client, prompt, aspect):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["Text", "Image"],
            image_config=types.ImageConfig(aspect_ratio=aspect),
        ),
    )
    candidates = getattr(response, "candidates", None) or []
    if not candidates:
        return None
    parts = getattr(getattr(candidates[0], "content", None), "parts", None) or []
    for part in parts:
        inline = getattr(part, "inline_data", None)
        if inline and getattr(inline, "data", None):
            return Image.open(io.BytesIO(inline.data))
    return None


def generate_with_retry(client, prompt, aspect, retries=5):
    for attempt in range(retries):
        try:
            image = generate_image(client, prompt, aspect)
            if image is not None:
                return image
        except Exception as error:
            print(f"  attempt {attempt + 1} error: {error}")
        wait = 30 * (attempt + 1)
        print(f"  retrying in {wait}s ...")
        time.sleep(wait)
    return None


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    client = genai.Client(vertexai=True, api_key=API_KEY)

    for asset in ASSETS:
        path = os.path.join(OUTPUT_DIR, f"{asset['name']}.webp")
        if os.path.exists(path):
            print(f"Skip existing {asset['name']}")
            continue

        print(f"Generating {asset['name']} ...")
        image = generate_with_retry(client, asset["prompt"], asset["aspect"])
        if image is None:
            print(f"  FAIL: no image for {asset['name']}")
            continue

        image.convert("RGB").save(path, "WEBP", quality=95)
        print(f"  OK: {path} ({image.size[0]}x{image.size[1]})")
        time.sleep(8)


if __name__ == "__main__":
    main()
