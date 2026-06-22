import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.environ["VERTEX_API_KEY"]
MODEL = "gemini-3-pro-image-preview"
PROMPT = (
    "A breathtaking cinematic wide shot of an ancient floating library hovering above "
    "a misty turquoise lake at golden hour. The library is built from weathered marble "
    "and dark oak with countless floor-to-ceiling bookshelves, ornate brass spiral "
    "staircases winding between five glass-domed levels, and waterfalls of glowing "
    "magical scrolls cascading from open balconies into the lake below. A lone scholar "
    "in a deep burgundy robe stands on the highest balcony reading a luminous book that "
    "emits soft blue particles drifting into the sky. Distant snow-capped mountains "
    "frame the horizon, flocks of paper cranes fly between the towers, and shafts of "
    "warm sunlight pierce the rolling fog. Hyper-detailed, photorealistic, octane "
    "render quality, dramatic volumetric lighting, sharp focus, 16:9 cinematic "
    "composition, rich color grading."
)
ASPECT_RATIO = "16:9"
OUTPUT_PATH = r"C:\workspace\ai_image_video_editing_projects\scripts\test_output.png"

client = genai.Client(vertexai=True, api_key=API_KEY)

response = client.models.generate_content(
    model=MODEL,
    contents=PROMPT,
    config=types.GenerateContentConfig(
        response_modalities=["Text", "Image"],
        image_config=types.ImageConfig(aspect_ratio=ASPECT_RATIO),
    ),
)

if response is None:
    print("FAIL: response is None")
    raise SystemExit(1)

prompt_feedback = getattr(response, "prompt_feedback", None)
if prompt_feedback and getattr(prompt_feedback, "block_reason", None):
    print(f"FAIL: blocked by safety filter -> {prompt_feedback.block_reason}")
    raise SystemExit(2)

candidates = getattr(response, "candidates", None) or []
if not candidates:
    print("FAIL: no candidates")
    raise SystemExit(3)

candidate = candidates[0]
parts = getattr(getattr(candidate, "content", None), "parts", None) or []

saved = False
text_collected = []
for part in parts:
    text_value = getattr(part, "text", None)
    if text_value:
        text_collected.append(text_value)
    inline_data = getattr(part, "inline_data", None)
    if inline_data and getattr(inline_data, "data", None) and not saved:
        with open(OUTPUT_PATH, "wb") as f:
            f.write(inline_data.data)
        saved = True

if text_collected:
    print("TEXT:", "".join(text_collected)[:200])

if saved:
    size = os.path.getsize(OUTPUT_PATH)
    print(f"OK: image saved -> {OUTPUT_PATH} ({size} bytes)")
else:
    print("FAIL: no image part in response")
    raise SystemExit(4)
