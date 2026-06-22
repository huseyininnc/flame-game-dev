# Responsive Design — Flutter + Flame (MANDATORY in every game)

Every game produced must work **without breaking** on every phone/tablet/foldable/desktop, every aspect ratio, DPI, orientation, and notch — images must not be distorted, and widgets must not overflow. **Art direction is chosen automatically based on the game's content** (modern flat, painterly, vector, cartoon, pixel-art, etc. — pixel-art is NOT mandatory); this document is a responsive recipe **independent** of the chosen style. If pixel-art is chosen, apply the optional sub-heading in §4.

---

## 0. Mental model — 3 coordinate spaces

In Flame, responsive design = deciding which space each element lives in.

```
GameWidget (Flutter, physical px)
 └── FlameGame.size  (logical screen size = canvas / devicePixelRatio)
      └── CameraComponent
           ├── Viewport   ── SCREEN space (static). The HUD goes here; pinned to the edges.
           ├── Viewfinder ── the view into the world (position / zoom / anchor / angle)
           └── World      ── GAME space. Gameplay objects; transformed with the camera.
```

**Golden rules:**
- **Gameplay objects → `world`.** Camera/zoom/letterbox work automatically.
- **HUD/UI → `camera.viewport`.** Screen-space; stays in place when the camera moves.
- **Never hardcode pixel positions.** Express position as a **percentage** of the `world` (gameplay) or of `camera.viewport.size` (HUD).
- **Pick ONE design resolution per game** and let the viewport scale. This is the most critical decision.

---

## 1. CameraComponent + Viewports

`FlameGame` already provides `camera` and `world`. The camera has three parts: `viewport`, `viewfinder`, `backdrop`.

| Viewport | Behavior | Aspect mismatch | When |
|---|---|---|---|
| **MaxViewport** (default) | Fills the entire canvas | More/less of the **world is visible** (no bars, no distortion) | Free-scrolling worlds ("more screen = see more") |
| **FixedResolutionViewport** | Locks logical resolution + aspect, scales to fit | **Letterbox** (bar on the short edge); never stretches | Most arcade/puzzle/board; everyone sees the **same** area |
| **FixedAspectRatioViewport** | Fills the canvas but **preserves aspect** | Letterbox, no distortion; size dynamic, ratio fixed | Ratio matters but exact pixel resolution does not |
| **FixedSizeViewport** | Rectangle at a fixed position+size | Does not adapt (sub-window) | Split-screen, minimap, PiP |
| **CircularViewport** | Fixed-size circular clip | Fixed | Spotlight/binocular effect |

**Recommended responsive default:** `CameraComponent.withFixedResolution` — consistent, fair gameplay; letterboxes the remaining area (and single-render scale = cheap).

```dart
final camera = CameraComponent.withFixedResolution(
  world: world, width: 720, height: 1280, // DESIGN resolution
)..viewfinder.anchor = Anchor.topLeft;
```

**Viewfinder (view control):** `position`, `anchor`, `zoom` (master scale), `angle`, and — most important for responsiveness — **`visibleGameSize`** — you say "at least this many world units should be visible" and Flame computes the zoom for you (no magic zoom number):

```dart
camera.viewfinder.visibleGameSize = Vector2(16, 9); // ≥16×9 world is visible regardless of screen
```
The visible world rectangle: `camera.visibleWorldRect` (for culling + percentage-layout).

---

## 2. World (camera-transformed) vs Viewport (screen-space HUD)

```dart
world.add(Player()..position = Vector2(0, 0));        // gameplay → world
camera.viewport.add(ScoreLabel());                     // HUD → viewport
```

**Pin the HUD to the edges responsively:**
- **`AlignComponent`** (preferred; automatically reflows on resize):
```dart
camera.viewport.add(AlignComponent(alignment: Anchor.topRight, child: ScoreLabel()));
camera.viewport.add(AlignComponent(alignment: Anchor.bottomCenter, child: Joystick()));
```
- **`HudMarginComponent` / `HudButtonComponent`** (margin-based): these are measured against `viewport.size` and stay stuck to the edge even if the zoom changes.

---

## 3. Reacting to resize + percentage-layout

`onGameResize(Vector2 size)` fires on every `PositionComponent` and on the game when the canvas/orientation changes. **Call `super.onGameResize(size)` first.**

```dart
class ResponsiveBoard extends PositionComponent with HasGameReference<MyGame> {
  @override
  void onGameResize(Vector2 size) {
    super.onGameResize(size);
    if (!isMounted) return;                 // onGameResize can arrive BEFORE onLoad — guard
    final vp = game.camera.viewport.size;
    final side = math.min(vp.x, vp.y) * 0.9; // 90% of the short edge
    this
      ..size = Vector2.all(side)
      ..position = vp / 2
      ..anchor = Anchor.center;
  }
}
```
- For HUD layout read **`camera.viewport.size`**; for in-world layout read **`camera.visibleWorldRect`** (`game.size` ignores letterbox bars).
- Detect orientation via `size.x` vs `size.y` and reflow (if you haven't locked orientation).

```dart
extension Pct on Vector2 { Vector2 pct(double x, double y) => Vector2(this.x * x, this.y * y); }
label.position = game.camera.viewport.size.pct(0.95, 0.05);
```

---

## 4. Responsive asset/sprite (in the world) — style-agnostic

**Decouple the art pixel from the world unit.** Size the sprite **in world units** (component.size); pre-scale the source image.

```dart
final player = SpriteComponent(
  sprite: await Sprite.load('player.webp'), // may be 256px art
  size: Vector2(1, 1),                       // but 1 world unit
  anchor: Anchor.center,
);
```

**Set FilterQuality according to the chosen art style:**
- **Soft / hi-res / vector / painterly art (the default for most games):** `FilterQuality.medium` (`.high` if needed). **Produce large, scale down** — downscaling stays sharp, upscaling blurs.
  ```dart
  component.paint.filterQuality = FilterQuality.medium;
  ```
- **(Optional) If pixel-art is chosen:** nearest-neighbor — `FilterQuality.none` + `isAntiAlias = false`; scale the whole frame **in one pass** with `FixedResolutionViewport(clip:false)` (not per-sprite); place the asset at 1× (non-integer scale = shimmer). This is a valid sub-method only when pixel-art is chosen; it is not mandatory.

**Avoid distortion:** match the size to the source's aspect (don't give `Vector2(2,1)` to a square sprite). For tile stitching/seams use "bleeding" (a 1px transparent/duplicated margin on the cell edge) or `clip:false`. Flame already converts DPI into logical units via `devicePixelRatio`.

---

## 5. Design resolution & scaling strategy

- **A) Fixed resolution (fairness-first, default):** `withFixedResolution(w,h)` — everyone sees the same area; extreme ratios get letterboxed. For puzzle/board/arcade/competitive.
- **B) Adaptive "reveal more" (immersion-first):** `MaxViewport` + `visibleGameSize`. A wide screen sees more of the world (no bars). For exploration/sandbox; unfair in competition.
- **Safe-zone compromise:** place critical gameplay inside a **guaranteed-visible "safe rect"** (e.g. 9:16 / 16:9); the extra area in other ratios should be **margin/decorative** (not an advantage). Hide the letterbox bar with a thematic `backgroundColor` + an optional decorative frame overlay (`CustomPainter` + `IgnorePointer`).
- If a single orientation makes sense, lock it: `Flame.device.setPortrait()` / `setLandscape()` in `main()`.

---

## 6. Flutter overlay/widget responsiveness (HUD/menu)

Flame overlays are standard Flutter widgets. **One rule:** branch the layout by **window-width breakpoints** — NOT by device type, orientation, or hardcoded pixels.

- **Correct MediaQuery accessors (perf):** `MediaQuery.sizeOf` / `.paddingOf` / `.viewInsetsOf` / `.textScalerOf` / `.devicePixelRatioOf` — NOT `MediaQuery.of` (it rebuilds on every change; expensive in a ticking HUD).
- **Breakpoints (Material 3 window size class):** compact `<600` · medium `600–839` · expanded `≥840`. For a mobile game these three are enough.
- **Percentage + clamp (mandatory):** pure percentage breaks at extreme ratios → always clamp.
  ```dart
  final w = MediaQuery.sizeOf(context).width;
  final panel = (w * 0.4).clamp(280.0, 480.0);
  final scale = (w / 390).clamp(0.85, 1.4); // a single uiScale: padding/gap/radius/font all use this
  ```
- **`LayoutBuilder`** = relative to the parent box (docked panel); **`MediaQuery.sizeOf`** = the whole window (HUD variant selection).
- **SafeArea over full-bleed canvas:** the canvas is full-screen, only the interactive HUD is inside `SafeArea`:
  ```dart
  Stack(children: [
    Positioned.fill(child: GameWidget(game: game)),
    SafeArea(child: HudOverlay()),
  ]);
  ```
- **Material wrapping (mandatory):** wrap every overlay in `overlayBuilderMap` with `Material(type: MaterialType.transparency, child: ...)` (so a bare `Text` doesn't get a yellow underline, and the theme font is applied).
- Constrain panels with `ConstrainedBox(maxWidth: ...)` + `Align` (so they don't balloon on a tablet); use `Wrap` for toolbars; distribute Row/Column with `Flexible/Expanded/Spacer`.
- **Touch target ≥ 48dp/44pt.**

---

## 7. Responsive image/asset (Flutter UI side) — memory critical

- **`BoxFit`:** background → `cover`; icon/logo/UI sprite → `contain` or `scaleDown`; **never `fill`** (the only mode that distorts).
- **`cacheWidth`/`cacheHeight` (the biggest memory lever):** **decode** the image at its display size. 4K→384px drops from ~33MB to ~330KB. Provide logical size × devicePixelRatio:
  ```dart
  Image.asset('assets/ui/panel.webp',
    width: panelW, fit: BoxFit.cover,
    cacheWidth: (panelW * MediaQuery.devicePixelRatioOf(context)).round());
  ```
- **Density buckets:** provide `1.5x/2.0x/3.0x` folder variants; only the base path in pubspec; Flutter selects based on DPI. (Don't just ship 4× and rely on downscaling.)
- **Vector/SVG (flutter_svg):** for flat UI chrome (icons, logos, simple frames, glyphs) a single file, sharp at every DPI; use `.svg.vec` for perf. Don't use it for complex/painterly or pixel-art → raster (+density+cacheWidth).
- **9-slice frame/button:** in-code `BoxDecoration` (gradient/border/radius/shadow — zero memory, preferred) or `DecorationImage(centerSlice: Rect)` (corners stay fixed, the center stretches). Scale the `BoxDecoration` values with `uiScale`.
- **Monochrome UI glyphs:** `Icon`/icon-font (vector, scales with `color`/`size`, almost zero memory) — use image/SVG only for multi-color/branded art.

---

## 8. Text responsiveness & accessibility

- **Respect the OS font scale, but clamp:** `textScaleFactor` is deprecated; use `MediaQuery.textScalerOf`. To protect a dense HUD, clamp:
  ```dart
  MediaQuery.withClampedTextScaling(minScaleFactor: 0.9, maxScaleFactor: 1.3, child: hud);
  ```
  (Disabling with a global `TextScaler.noScaling` — an accessibility regression.)
- **Prevent overflow in a fixed slot (score/counter):** `FittedBox(fit: BoxFit.scaleDown, child: Text('$score', maxLines: 1))`. In a paragraph use `maxLines + ellipsis` (don't wrap a paragraph in FittedBox).

---

## 9. Recipes

**Responsive HUD (Flame, corners reflow automatically):**
```dart
camera.viewport.addAll([
  AlignComponent(alignment: Anchor.topLeft,     child: HealthBar()),
  AlignComponent(alignment: Anchor.topRight,    child: ScoreLabel()),
  AlignComponent(alignment: Anchor.bottomLeft,  child: Joystick()),
  AlignComponent(alignment: Anchor.bottomRight, child: FireButton()),
]);
```

**Responsive grid/board (Flame):** the `onGameResize` from §3 + a square cell that fits the short edge.

**Responsive Flutter overlay panel (compact↔tablet, clamp, SafeArea):**
```dart
final size = MediaQuery.sizeOf(context);
final isCompact = size.width < 600;
final scale = (size.width / 390).clamp(0.85, 1.4);
return SafeArea(child: isCompact
  ? Column(children: [stats, const Spacer(), const ActionBar()])
  : Row(children: [const ActionBar(), const Spacer(), stats]));
```

**Responsive button (scales + a11y target):** size `(48*scale).clamp(48, 88)`, icon `FittedBox`, radius/shadow `*scale`.

**Notch/safe-area:** canvas full-bleed; HUD in `SafeArea`; if needed, pass the `MediaQuery.paddingOf` insets into the game and add them to the edge-HUD margin. Critical HUD inside the safe-rect; only decorative art extends under the notch.

---

## Checklist (for every game)

- [ ] Gameplay in `world`, HUD in `camera.viewport`. No hardcoded pixel positions (use %).
- [ ] Single design resolution; `withFixedResolution` (or a deliberate `MaxViewport`+`visibleGameSize`).
- [ ] Layout components apply `onGameResize` (`super` first, `isMounted` guard).
- [ ] HUD via `AlignComponent`/`HudMarginComponent` (zoom-resilient).
- [ ] Sprites in world units; **FilterQuality per style** (soft=`medium`/`high`, `none` if pixel-art is chosen). Produce large, scale down. No distortion (match aspect).
- [ ] Flutter overlay: `MediaQuery.sizeOf` breakpoints (600/840) + clamp + `uiScale`; `SafeArea`; `Material` wrapping; `maxWidth`.
- [ ] Images: `cover/contain` (never `fill`), `cacheWidth×dpr`, density buckets; SVG/icon-font for flat UI.
- [ ] Text: `textScalerOf` clamp; `FittedBox` in a fixed slot.
- [ ] Verify with screenshots on a phone (tall) + tablet (wide) + two extreme aspects: no stretching/overflow/bar issues.

---

## Sources

- Camera & World — Flame docs: https://docs.flame-engine.org/latest/flame/camera.html
- Viewfinder / FixedResolutionViewport — Flame API: https://pub.dev/documentation/flame/latest/camera/Viewfinder-class.html
- AlignComponent — Flame docs: https://docs.flame-engine.org/latest/flame/layout/align_component.html
- HudButton/HudMargin — Flame docs: https://docs.flame-engine.org/latest/flame/inputs/other_inputs.html
- Flame device orientation & resolution — Craig Oda: https://medium.com/codecakes/flame-game-device-orientation-and-resolution-2ada9daebef5
- Best practices for adaptive design — Flutter: https://docs.flutter.dev/ui/adaptive-responsive/best-practices
- SafeArea & MediaQuery — Flutter: https://docs.flutter.dev/ui/adaptive-responsive/safearea-mediaquery
- Adding assets and images (density buckets) — Flutter: https://docs.flutter.dev/ui/assets/assets-and-images
- ImageCache large images (cacheWidth) — Flutter: https://docs.flutter.dev/release/breaking-changes/imagecache-large-images
- BoxFit — Flutter API: https://api.flutter.dev/flutter/painting/BoxFit.html
- MediaQuery.withClampedTextScaling — Flutter API: https://api.flutter.dev/flutter/widgets/MediaQuery/withClampedTextScaling.html
- Window size classes — Material 3: https://m3.material.io/foundations/layout/applying-layout/window-size-classes
- flutter_svg: https://pub.dev/packages/flutter_svg · flutter_screenutil: https://pub.dev/packages/flutter_screenutil
