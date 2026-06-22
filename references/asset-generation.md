# AI Asset Üretimi (Vertex GenAI)

> Tüm üreticiler ve `.env` (VERTEX_API_KEY) bu skill'in içinde **gömülüdür** (`scripts/`, skill köküne göreli). Skill self-contained'dir. Çalıştırmak için skill'in `scripts/` dizinine `cd` et (`load_dotenv()` `.env`'i oradan okur). Her generator'ın `OUTPUT_DIR`'i ilgili oyunun `assets/` klasörüne mutlak yol verir.

`scripts/` altında Vertex GenAI tabanlı üreticiler bulunur. Mevcut başlangıç noktaları: `scripts/create_image_with_gemini_api.py` (tek görsel) ve `scripts/generate_slime_assets.py` (çoklu prompt + PNG→şeffaf webp dönüşümü; örnek). Model: `gemini-3-pro-image-preview`, Vertex `genai.Client(vertexai=True, api_key=...)`.

Her oyun için bu scriptleri **türeterek** projeye özel asset üreticileri oluştur (görsel + ses). Kaynak betiği bozma; kopyala/genişlet.

## Sanat yönü serbesttir

Sanat stili **oyuna göre** seçilir — modern (yumuşak/glossy 3D, flat, vektör), pixel-art, el-çizimi vb. Pixel-art zorunlu değildir. Önemli olan **her oyunda tutarlı bir style-guide** belirleyip tüm asset'lere aynı cümleyi uygulamaktır.

## Üretim ilkeleri

- **Webp formatı.** Model PNG döndürür; üretim sonrası webp'e dönüştür (Pillow: `img.save(path, "WEBP")`). Şeffaflık gerekiyorsa webp alpha'yı korur (`lossless=True`).
- **Şeffaf arka plan** sprite'lar için: prompt'a "isolated, centered, plain background" ekle; model temiz şeffaf vermezse köşeden flood-fill ile arka planı temizle (bkz. `generate_slime_assets.py` `cutout_background`).
- **Tutarlı stil:** Aynı oyunun tüm asset'lerinde aynı style-guide cümlesini (palet, ışık, ton, form dili) kullan.
- **Sprite sheet** gerekiyorsa kareleri ayrı üretip kodda `SpriteSheet`/`SpriteAnimationData` ile birleştir; ya da tek sheet üretip `srcSize`/`srcPosition` ile dilimle.
- **Boyut/anchor:** Asset boyutunu oyunun logical/fixed-resolution uzayına göre planla (ör. tile 256px kaynak, oyunda hücre boyutuna ölçeklenir).

## Görsel prompt kalıbı

```
<konu>, <stil-rehberi: ör. modern soft 3D glossy / flat vector / pixel art>,
<palet/renk>, centered, isolated, plain background,
no text, no watermark, fully original, no existing characters or brands.
```

## Ses üretimi

Vertex/GenAI ses üretimi için ayrı bir script türet; sfx (kısa, `assets/audio/sfx/`) ve bgm (döngü, `assets/audio/music/`) ayrımını koru. Üretilen ses motor tarafında `FlameAudio.play` (sfx) / `FlameAudio.bgm` (müzik) ile kullanılır (bkz. `references/flame/08`).

## Güvenlik / kimlik bilgisi notu

- API anahtarı `scripts/.env` içinde tutulur (`python-dotenv` ile yüklenir), `.gitignore` ile korunur — **commit edilmez.** Yeni üreticilerde anahtarı `os.environ`'dan oku.
- Üretilen prompt'lara daima `fully original, no existing IP, no brand logos, no copyrighted characters, no text` ekle (telif güvenliği).
- Ham PNG çıktıları repo'yu şişirmesin; yalnızca son webp/ses asset'lerini `assets/` altına al.

## Akış

1. Oyunun style-guide cümlesini ve sanat yönünü belirle.
2. Bir üreticiyi kopyalayıp oyuna özel yaz (çoklu prompt + webp dönüşümü + gerekiyorsa şeffaflık + çıktı klasörü).
3. Üret → gözden geçir → `assets/images/` (webp) ve `assets/audio/` altına yerleştir.
4. `pubspec.yaml`'a kaydet (`assets/images/`), `onLoad`'da `Sprite.load` ile preload et.
