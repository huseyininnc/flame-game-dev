import io
import os
from collections import deque

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()

API_KEY = os.environ["VERTEX_API_KEY"]
MODEL = "gemini-3-pro-image-preview"
OUTPUT_DIR = r"C:\workspace\zeynsoft_projects\projects\games\slime_blocks\assets\images"

STYLE = (
    "modern soft 3D glossy slime cube mascot, smooth rounded corners, cute simple "
    "dot eyes, soft studio lighting, subtle gradient body with a glossy highlight, "
    "clean minimal vector-like style, centered, isolated subject, plain flat white "
    "background, no shadow on ground, no text, no watermark, fully original "
    "character, no existing brand or character"
)

ASSETS = [
    {"name": "slime_mint", "aspect": "1:1", "cutout": True,
     "prompt": f"vibrant mint green (#7BD389) {STYLE}"},
    {"name": "slime_teal", "aspect": "1:1", "cutout": True,
     "prompt": f"vibrant teal (#3FB8AF) {STYLE}"},
    {"name": "slime_coral", "aspect": "1:1", "cutout": True,
     "prompt": f"warm coral (#FF8C7A) {STYLE}"},
    {"name": "slime_honey", "aspect": "1:1", "cutout": True,
     "prompt": f"golden honey yellow (#FFCB6B) {STYLE}"},
    {"name": "slime_lavender", "aspect": "1:1", "cutout": True,
     "prompt": f"soft lavender purple (#B79CED) {STYLE}"},
    {"name": "background", "aspect": "9:16", "cutout": False,
     "prompt": (
         "modern minimal calm background, deep dark purple-gray (#2B2440), very "
         "subtle smooth gradient, faint soft bokeh dots, clean and non-distracting, "
         "no text, no characters, fully original"
     )},
    {"name": "icon", "aspect": "1:1", "cutout": False,
     "prompt": (
         "modern app icon, single glossy mint green slime cube mascot with cute eyes "
         "centered on a dark rounded square background (#2B2440), clean high-contrast "
         "design, no text, no logos, fully original"
     )},
]

TILE_SIZE = 256
ICON_SIZE = 512
BG_SIZE = (1080, 1920)


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


def cutout_background(image, tolerance=38):
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


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    client = genai.Client(vertexai=True, api_key=API_KEY)

    for asset in ASSETS:
        print(f"Generating {asset['name']} ...")
        image = generate_image(client, asset["prompt"], asset["aspect"])
        if image is None:
            print(f"  FAIL: no image for {asset['name']}")
            continue

        if asset["cutout"]:
            image = cutout_background(image)
            image = image.resize((TILE_SIZE, TILE_SIZE), Image.LANCZOS)
        elif asset["name"] == "icon":
            image = image.convert("RGB").resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS)
        else:
            image = image.convert("RGB").resize(BG_SIZE, Image.LANCZOS)

        path = os.path.join(OUTPUT_DIR, f"{asset['name']}.webp")
        image.save(path, "WEBP", lossless=asset["cutout"], quality=95)
        print(f"  OK: {path} ({image.size[0]}x{image.size[1]})")


if __name__ == "__main__":
    main()
