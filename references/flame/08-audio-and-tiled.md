# Flame Audio and Tiled Maps

This document covers two bridge packages: **`flame_audio`** for sound effects and background music, and **`flame_tiled`** for loading maps authored in the Tiled editor.

> Verified against **flame_audio 2.12.1** and **flame_tiled 3.1.1** (both targeting flame ^1.37.0).

---

## Part 1 — Audio with `flame_audio`

`flame_audio` is a thin wrapper around the `audioplayers` package, tuned for game use.

### Setup

```yaml
dependencies:
  flame: ^1.37.0
  flame_audio: ^2.12.1

flutter:
  assets:
    - assets/audio/
```

By default `flame_audio` looks for files under `assets/audio/`, so paths you pass are relative to that folder.

```dart
import 'package:flame_audio/flame_audio.dart';
```

### Sound effects: `FlameAudio.play`

`play` and `loop` are optimized for short clips and avoid gaps when looping:

```dart
FlameAudio.play('explosion.mp3');
FlameAudio.play('explosion.mp3', volume: 0.5);

FlameAudio.loop('engine.mp3');
```

For long audio files (where the short-clip optimization causes problems) use the long-audio variants — note these can cause minor frame drops and small looping gaps:

```dart
FlameAudio.playLongAudio('cutscene.mp3');
FlameAudio.loopLongAudio('ambience.mp3');
```

### Background music: `FlameAudio.bgm`

The `Bgm` class manages looping music and automatically pauses when the app goes to the background, resuming when it returns to focus.

Initialize it once (it needs a `WidgetsBinding`, so do this in `onLoad`), and dispose it when done:

```dart
class MyGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    FlameAudio.bgm.initialize();
    FlameAudio.bgm.play('music/world-map.mp3', volume: 0.25);
  }

  @override
  void onRemove() {
    FlameAudio.bgm.dispose();
    super.onRemove();
  }
}
```

Control methods:

```dart
FlameAudio.bgm.stop();   // halt the current track
FlameAudio.bgm.pause();  // manual pause (won't auto-resume on focus)
FlameAudio.bgm.resume(); // manual resume
```

### Preloading with `audioCache.loadAll`

Loading audio on first play introduces a hitch. Preload during initialization to eliminate it:

```dart
@override
Future<void> onLoad() async {
  await FlameAudio.audioCache.loadAll([
    'explosion.mp3',
    'jump.mp3',
    'coin.mp3',
  ]);
}

// Single file:
await FlameAudio.audioCache.load('explosion.mp3');

// Free memory when no longer needed:
FlameAudio.audioCache.clear('explosion.mp3');
```

### Rapid sound effects with `AudioPool`

For sounds that fire very frequently or simultaneously (gunfire, footsteps, coin pickups), an `AudioPool` keeps a set of pre-warmed players so each shot starts instantly.

Create the pool with `AudioPool.createFromAsset` (or `AudioPool.create` from a `Source`):

```dart
late final AudioPool _shootPool;

@override
Future<void> onLoad() async {
  _shootPool = await AudioPool.createFromAsset(
    path: 'sfx/shoot.mp3',
    maxPlayers: 4,
    minPlayers: 1,
  );
}
```

`start` plays a sound and returns a `StopFunction` you can call to stop that instance early:

```dart
Future<void> shoot() async {
  final stop = await _shootPool.start(volume: 0.8);
  // ... later, if needed:
  // stop();
}
```

The exact factory signatures:

```dart
static Future<AudioPool> create({
  required Source source,
  required int maxPlayers,
  AudioCache? audioCache,
  AudioContext? audioContext,
  int minPlayers = 1,
  PlayerMode playerMode = PlayerMode.mediaPlayer,
});

static Future<AudioPool> createFromAsset({
  required String path,
  required int maxPlayers,
  AudioCache? audioCache,
  int minPlayers = 1,
  PlayerMode playerMode = PlayerMode.mediaPlayer,
});

Future<StopFunction> start({double volume = 1.0});
```

- `maxPlayers` caps concurrent instances; requests beyond it are dropped until one frees up.
- `minPlayers` is how many players are pre-created up front.

---

## Part 2 — Tiled maps with `flame_tiled`

`flame_tiled` renders maps authored in the [Tiled](https://www.mapeditor.org/) editor. It wraps the `tiled` Dart package (which parses TMX/XML) and provides `TiledComponent` to render tile layers (with rotation and flip support) and to reach object data.

### Setup

```yaml
dependencies:
  flame: ^1.37.0
  flame_tiled: ^3.1.1

flutter:
  assets:
    - assets/tiles/   # .tmx maps and .tsx tilesets
    - assets/images/  # tileset images
```

By default maps are loaded from `assets/tiles/`.

### Loading a map: `TiledComponent.load`

The second argument is the **destination tile size** (a `Vector2`) — how large each tile is rendered, independent of the source tile size:

```dart
import 'package:flame/components.dart';
import 'package:flame_tiled/flame_tiled.dart';

class MyGame extends FlameGame {
  late final TiledComponent mapComponent;

  @override
  Future<void> onLoad() async {
    mapComponent = await TiledComponent.load(
      'map.tmx',
      Vector2.all(16),
    );
    world.add(mapComponent);
  }
}
```

### Accessing object layers

Object layers (object groups in Tiled) are reached through `mapComponent.tileMap.getLayer<ObjectGroup>('name')`. Iterate the group's `objects` to spawn game entities at the positions you laid out in the editor:

```dart
final objectGroup = mapComponent.tileMap.getLayer<ObjectGroup>(
  'AnimatedCoins',
);

for (final obj in objectGroup!.objects) {
  world.add(
    Coin()
      ..position = Vector2(obj.x, obj.y)
      ..size = Vector2(obj.width, obj.height),
  );
}
```

`getLayer<T>(name)` is generic over the layer type and returns `null` if no layer with that name/type exists — always null-check before use.

### Reading object and layer properties

Tiled custom properties come through on each object (and on layers/tiles). Read them via the `properties` collection:

```dart
for (final obj in objectGroup.objects) {
  final isBoss = obj.properties.getValue<bool>('isBoss') ?? false;
  final speed = obj.properties.getValue<int>('speed') ?? 0;
  // class/type and name are first-class fields:
  final type = obj.class_;
  final name = obj.name;
}
```

> Not: `obj.properties.getValue<T>(...)` ve `obj.class_` adlandırmaları `tiled` paketinden gelir ve majör sürümler arasında değişebilir; flame_tiled 3.1.1'in çözdüğü tiled sürümüne karşı derleyerek doğrulayın.

### Accessing tile layers

Tile layers use the same `getLayer` accessor with `TileLayer`:

```dart
final ground = mapComponent.tileMap.getLayer<TileLayer>('Ground');
final width = mapComponent.tileMap.map.width;   // in tiles
final height = mapComponent.tileMap.map.height; // in tiles
```

`mapComponent.tileMap` is a `RenderableTiledMap`; its `.map` field is the parsed `TiledMap` from the `tiled` package, giving access to dimensions, layers, and tilesets.

## Kaynaklar

- https://raw.githubusercontent.com/flame-engine/flame/main/doc/bridge_packages/flame_audio/audio.md
- https://raw.githubusercontent.com/flame-engine/flame/main/doc/bridge_packages/flame_audio/bgm.md
- https://pub.dev/packages/flame_audio (flame_audio 2.12.1)
- https://pub.dev/documentation/flame_audio/latest/flame_audio/AudioPool-class.html
- https://docs.flame-engine.org/latest/bridge_packages/flame_tiled/tiled.html
- https://pub.dev/packages/flame_tiled (flame_tiled 3.1.1)
