# Flame Engine — Knowledge Base

This folder contains reference documents compiled for producing games in series (many games, of different concepts) with the Flutter **Flame** game engine. All content has been verified against the official Flame documentation, the pub.dev API references, and the flame_bloc source code.

> Target versions: **flame `^1.37.0`**, **flame_audio `^2.12.1`**, **flame_tiled `^3.1.1`**, **flame_bloc** (current API).
> Important API changes: `Camera` → `CameraComponent` + `World`; `Tappable`/`Draggable` → `TapCallbacks`/`DragCallbacks`; `HasGameRef` → `HasGameReference`.

## Table of Contents

| # | File | Topic |
|---|---|---|
| 01 | [01-overview-and-setup.md](01-overview-and-setup.md) | Setup, `GameWidget`, `FlameGame`, game loop, asset structure |
| 02 | [02-components-and-lifecycle.md](02-components-and-lifecycle.md) | FCS, `PositionComponent`, lifecycle, mixins (`HasGameReference`, etc.) |
| 03 | [03-rendering-sprites-text.md](03-rendering-sprites-text.md) | `Sprite`, `SpriteComponent`, sprite sheet, animation, `TextComponent` |
| 04 | [04-input-and-gestures.md](04-input-and-gestures.md) | `TapCallbacks`, `DragCallbacks`, keyboard, `JoystickComponent`, `HudButtonComponent` |
| 05 | [05-effects-and-particles.md](05-effects-and-particles.md) | `Effect`, `EffectController`, `SequenceEffect`, particle system |
| 06 | [06-collision-detection.md](06-collision-detection.md) | `HasCollisionDetection`, hitboxes, `CollisionType`, quad-tree, raycast |
| 07 | [07-camera-world-viewport.md](07-camera-world-viewport.md) | `CameraComponent`, `World`, viewport/viewfinder, HUD, fixed-resolution |
| 08 | [08-audio-and-tiled.md](08-audio-and-tiled.md) | `flame_audio` (sfx/bgm/AudioPool), `flame_tiled` maps |
| 09 | [09-overlays-router-state.md](09-overlays-router-state.md) | Overlays, `RouterComponent`, game state flow |
| 10 | [10-architecture-bloc-multigame.md](10-architecture-bloc-multigame.md) | `flame_bloc`, layered architecture, multi-game monorepo strategy |
| 11 | [11-performance-optimization.md](11-performance-optimization.md) | 60 FPS, preloading, object pooling, `RecycledQueue`, FPS measurement |

## How to use

- When starting a new game, read files **01**, **02**, and **10** first (setup + architectural skeleton).
- During production, refer to the file for the relevant topic.
- This knowledge base is also used together with the `flame-game-dev` Claude Code skill — the skill references these documents as production rules.
