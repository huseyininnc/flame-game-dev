import io
import os
import time
from collections import deque

from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from PIL import Image

load_dotenv()

API_KEY = os.environ["VERTEX_API_KEY"]
MODEL = "gemini-3-pro-image-preview"
OUTPUT_DIR = r"C:\workspace\zeynsoft_projects\projects\games\emberhollow\assets\images"

STYLE = (
    "2D pixel art, medieval dark fantasy, moody torchlit color palette, cohesive, "
    "detailed but clean readable pixels, atmospheric, no text, no watermark, fully "
    "original, no existing game character or brand"
)
CHAR_STYLE = (
    "full body single character, " + STYLE + ", plain flat solid teal background, "
    "centered, full figure visible, not resembling any existing character"
)
ITEM_STYLE = "single game item icon, " + STYLE + ", plain flat solid teal background, centered"

ASSETS = [
    {"name": "bg_title", "aspect": "9:16", "w": 360, "h": 640, "alpha": False,
     "prompt": "title screen background: silhouette of an old stone keep at night on a "
               "hill with a faint dying ember glow at its top, fog over a small medieval "
               "village below, starry sky, " + STYLE},
    {"name": "bg_road_dusk", "aspect": "9:16", "w": 360, "h": 640, "alpha": False,
     "prompt": "a wooden village gate set in a stone wall seen from the muddy road "
               "outside at dusk, hanging lanterns, drifting fog, " + STYLE},
    {"name": "bg_tavern", "aspect": "9:16", "w": 360, "h": 640, "alpha": False,
     "prompt": "cozy medieval tavern interior with a warm glowing hearth, wooden tables, "
               "hanging lanterns and barrels, " + STYLE},
    {"name": "bg_forest", "aspect": "9:16", "w": 360, "h": 640, "alpha": False,
     "prompt": "a dark cursed forest path at night, twisted bare trees, thick fog, faint "
               "eerie blue gloom mist, " + STYLE},
    {"name": "bg_keep", "aspect": "9:16", "w": 360, "h": 640, "alpha": False,
     "prompt": "interior hall of an ancient stone keep with a large iron brazier holding "
               "a dying sacred ember flame at the center, cracked pillars, deep shadows, "
               + STYLE},
    {"name": "bg_dawn", "aspect": "9:16", "w": 360, "h": 640, "alpha": False,
     "prompt": "a small medieval village at warm golden dawn, smoke from chimneys, the "
               "keep on the hill glowing with a restored flame, hopeful mood, " + STYLE},
    {"name": "char_bram", "aspect": "3:4", "w": 200, "h": 280, "alpha": True,
     "prompt": "a gruff bearded medieval gatekeeper guard in worn leather armor holding "
               "a spear, stern expression, " + CHAR_STYLE},
    {"name": "char_mara", "aspect": "3:4", "w": 200, "h": 280, "alpha": True,
     "prompt": "a kind middle-aged medieval innkeeper woman wearing an apron and "
               "headscarf, holding a small lantern, warm expression, " + CHAR_STYLE},
    {"name": "char_stranger", "aspect": "3:4", "w": 200, "h": 280, "alpha": True,
     "prompt": "a mysterious tall hooded figure in a dark traveling cloak, face hidden "
               "in shadow with faint glowing eyes, " + CHAR_STYLE},
    {"name": "item_lantern", "aspect": "1:1", "w": 48, "h": 48, "alpha": True,
     "prompt": "an old brass medieval lantern with a small warm flame inside, " + ITEM_STYLE},
    {"name": "item_oil", "aspect": "1:1", "w": 48, "h": 48, "alpha": True,
     "prompt": "a small clay oil flask with a cork stopper, " + ITEM_STYLE},
    {"name": "item_medallion", "aspect": "1:1", "w": 48, "h": 48, "alpha": True,
     "prompt": "an ornate bronze medallion engraved with an ember flame emblem on a "
               "chain, " + ITEM_STYLE},
    {"name": "icon", "aspect": "1:1", "w": 512, "h": 512, "alpha": False,
     "prompt": "app icon: a glowing ember flame inside a brass lantern on a dark medieval "
               "stone background, high contrast, centered, no logos, " + STYLE},
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


def cutout_background(image, tolerance=42):
    rgba = image.convert("RGBA")
    width, height = rgba.size
    pixels = rgba.load()
    corners = [(0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)]
    if all(pixels[x, y][3] < 12 for x, y in corners):
        return rgba
    reference = pixels[0, 0]

    def is_background(color):
        return all(abs(a - b) <= tolerance for a, b in zip(color[:3], reference[:3]))

    visited = bytearray(width * height)
    queue = deque(corners)
    while queue:
        x, y = queue.popleft()
        if x < 0 or x >= width or y < 0 or y >= height:
            continue
        index = y * width + x
        if visited[index]:
            continue
        visited[index] = 1
        color = pixels[x, y]
        if is_background(color):
            pixels[x, y] = (color[0], color[1], color[2], 0)
            queue.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    return rgba


def pixelize(image, final_w, final_h, alpha):
    mode = "RGBA" if alpha else "RGB"
    image = image.convert(mode)
    base = image.resize((max(1, final_w // 2), max(1, final_h // 2)), Image.LANCZOS)
    return base.resize((final_w, final_h), Image.NEAREST)


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
        image = pixelize(image, asset["w"], asset["h"], asset["alpha"])
        image.save(path, "WEBP", lossless=asset["alpha"], quality=92)
        print(f"  OK: {path} ({image.size[0]}x{image.size[1]})", flush=True)
        time.sleep(12)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
