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
OUTPUT_DIR = r"C:\workspace\zeynsoft_projects\projects\games\bluehour\assets\images"

STYLE = (
    "modern romantic painterly digital illustration, soft cinematic gradient "
    "lighting, dreamy Mediterranean blue hour palette of deep indigo, warm rose "
    "pink and golden light, atmospheric, elegant, high detail, smooth shading, "
    "no text, no watermark, fully original, no existing characters or brands"
)
GREEN_SCREEN = (
    "standing alone on a perfectly flat uniform solid pure chroma key green "
    "screen, hex #00FF00, the entire background is one single flat green color, "
    "no scenery, no backdrop, no architecture, no arch, no window, no wall, no "
    "floor line, no horizon, no props, no cast shadow, no vignette, isolated "
    "studio green screen cutout, centered, full figure visible"
)
CHAR_RENDER = (
    "modern romantic painterly digital illustration, soft warm rim lighting, "
    "rose-gold and indigo accents on the figure, high detail, smooth shading, "
    "no text, no watermark, fully original, no existing characters or brands"
)
CHAR_STYLE = (
    "full body single person, " + CHAR_RENDER + ", " + GREEN_SCREEN + ", "
    "tasteful elegant summer attire, warm inviting expression, not resembling "
    "any real or fictional person"
)
ITEM_STYLE = (
    "single small keepsake object, " + CHAR_RENDER + ", " + GREEN_SCREEN
)

ASSETS = [
    {"name": "bg_title", "aspect": "9:16", "w": 1080, "h": 1920, "alpha": False,
     "prompt": "a boutique hotel rooftop terrace overlooking a calm sea at the "
               "blue hour, string lights glowing, two empty lounge chairs, soft "
               "twilight, romantic and inviting, " + STYLE},
    {"name": "bg_terrace", "aspect": "9:16", "w": 1080, "h": 1920, "alpha": False,
     "prompt": "a cozy Mediterranean rooftop cocktail terrace at dusk, lanterns "
               "and warm string lights, low tables, sea horizon behind, " + STYLE},
    {"name": "bg_beach", "aspect": "9:16", "w": 1080, "h": 1920, "alpha": False,
     "prompt": "a secluded rocky cove beach at golden sunset, gentle waves, warm "
               "reflections on the water, intimate and serene, " + STYLE},
    {"name": "bg_market", "aspect": "9:16", "w": 1080, "h": 1920, "alpha": False,
     "prompt": "a lively coastal night market street, glowing paper lanterns, "
               "warm bokeh crowd lights, festive romantic mood, " + STYLE},
    {"name": "bg_vineyard", "aspect": "9:16", "w": 1080, "h": 1920, "alpha": False,
     "prompt": "a hillside vineyard in warm late afternoon light, rows of "
               "grapevines, distant sea, soft golden haze, " + STYLE},
    {"name": "bg_pier", "aspect": "9:16", "w": 1080, "h": 1920, "alpha": False,
     "prompt": "a long wooden pier reaching into a calm sea under a starry night "
               "sky, moored boats, moonlight on the water, " + STYLE},
    {"name": "bg_festival", "aspect": "9:16", "w": 1080, "h": 1920, "alpha": False,
     "prompt": "a seaside summer festival at night, warm festival lights and "
               "garlands, distant fireworks over the bay, joyful romantic "
               "atmosphere, " + STYLE},
    {"name": "bg_dawn", "aspect": "9:16", "w": 1080, "h": 1920, "alpha": False,
     "prompt": "a boutique hotel balcony at soft pink dawn over a calm sea, gentle "
               "morning light, peaceful and hopeful mood, " + STYLE},
    {"name": "char_selin", "aspect": "3:4", "w": 768, "h": 1024, "alpha": True,
     "prompt": "a confident adventurous woman travel photographer in her late "
               "twenties, a camera hanging around her neck, breezy light summer "
               "dress, tousled hair, playful warm smile, " + CHAR_STYLE},
    {"name": "char_kaan", "aspect": "3:4", "w": 768, "h": 1024, "alpha": True,
     "prompt": "a brooding soulful man musician in his early thirties holding an "
               "acoustic guitar, open linen shirt, tousled dark hair, thoughtful "
               "intense gaze, " + CHAR_STYLE},
    {"name": "char_eda", "aspect": "3:4", "w": 768, "h": 1024, "alpha": True,
     "prompt": "a warm sunny woman in her late twenties, vineyard owner's "
               "daughter, flowing sundress, a wildflower in her hair, grounded "
               "radiant smile, " + CHAR_STYLE},
    {"name": "char_nilufer", "aspect": "3:4", "w": 768, "h": 1024, "alpha": True,
     "prompt": "a warm elegant older woman hotelier in her late fifties, draped "
               "shawl, silver-streaked hair in a loose bun, knowing gentle smile, "
               + CHAR_STYLE},
    {"name": "item_photo", "aspect": "1:1", "w": 256, "h": 256, "alpha": True,
     "prompt": "a single instant polaroid-style photograph keepsake with a white "
               "border, " + ITEM_STYLE},
    {"name": "item_pick", "aspect": "1:1", "w": 256, "h": 256, "alpha": True,
     "prompt": "a single worn wooden guitar pick keepsake, " + ITEM_STYLE},
    {"name": "item_cork", "aspect": "1:1", "w": 256, "h": 256, "alpha": True,
     "prompt": "a single wine bottle cork with a small pressed flower tied to it, "
               + ITEM_STYLE},
    {"name": "icon", "aspect": "1:1", "w": 512, "h": 512, "alpha": False,
     "prompt": "app icon: two romantic silhouettes facing each other at the blue "
               "hour under an arch of glowing string lights forming a subtle "
               "heart, deep indigo and rose sky, high contrast, centered, no "
               "text, " + STYLE},
]


def generate_image(client, prompt, aspect, max_retries=5):
    for attempt in range(max_retries):
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


def cutout_background(image):
    rgba = image.convert("RGBA")
    hsv = image.convert("RGB").convert("HSV")
    width, height = rgba.size
    pixels = rgba.load()
    hsv_pixels = hsv.load()
    for y in range(height):
        for x in range(width):
            hue, saturation, value = hsv_pixels[x, y]
            r, g, b, a = pixels[x, y]
            is_green = 55 <= hue <= 120 and saturation >= 55 and value >= 55
            if is_green:
                pixels[x, y] = (r, g, b, 0)
            elif g > r and g > b:
                pixels[x, y] = (r, min(g, (r + b) // 2 + 14), b, a)
    return rgba


def fit(image, final_w, final_h, alpha):
    mode = "RGBA" if alpha else "RGB"
    return image.convert(mode).resize((final_w, final_h), Image.LANCZOS)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    client = genai.Client(vertexai=True, api_key=API_KEY)
    for asset in ASSETS:
        path = os.path.join(OUTPUT_DIR, f"{asset['name']}.webp")
        if os.path.exists(path):
            print(f"SKIP {asset['name']} (exists)", flush=True)
            continue
        print(f"Generating {asset['name']} ...", flush=True)
        image = generate_image(client, asset["prompt"], asset["aspect"])
        if image is None:
            print(f"  FAIL: no image for {asset['name']}", flush=True)
            continue
        if asset["alpha"]:
            image = cutout_background(image)
        image = fit(image, asset["w"], asset["h"], asset["alpha"])
        image.save(path, "WEBP", lossless=asset["alpha"], quality=92)
        print(f"  OK: {path} ({image.size[0]}x{image.size[1]})", flush=True)
        time.sleep(12)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
