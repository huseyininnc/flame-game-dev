# Flame: Overlays, Routing, and In-Game Screen Management

This section explains how to manage screens such as **menu / HUD / pause / game over** in a Flame game using two complementary mechanisms:

1. **Overlays** — Layering Flutter widgets on top of the game canvas (ideal for menus, buttons, and dialogs).
2. **RouterComponent** — Stack-based transitions *inside* the game, between Flame components (menu -> playing -> paused -> game over).

The rule for rapidly producing many small games: **Flutter UI = Overlays**, **in-game scene transitions = RouterComponent**. The two can be combined via `OverlayRoute`.

---

## 1. Overlays: Flutter Widgets on Top of the Game

Because the Flame game lives inside a Flutter widget tree, you can place any Flutter widget on top of the canvas. The `Game.overlays` API makes this easy by toggling named overlays on and off.

### 1.1 On the GameWidget side: `overlayBuilderMap`

Each overlay is defined by a `String` key and mapped to a builder function inside `overlayBuilderMap`. The builder signature is: `(BuildContext context, MyGame game) => Widget`.

```dart
import 'package:flame/game.dart';
import 'package:flutter/material.dart';

final game = MyGame();

class GameView extends StatelessWidget {
  const GameView({super.key});

  @override
  Widget build(BuildContext context) {
    return GameWidget<MyGame>(
      game: game,
      overlayBuilderMap: {
        'PauseMenu': (context, game) => PauseMenu(game: game),
        'GameOver': (context, game) => GameOverMenu(game: game),
        'Hud': (context, game) => Hud(game: game),
      },
      initialActiveOverlays: const ['Hud'],
    );
  }
}
```

`initialActiveOverlays` is the list of overlay keys that will be active when the game first loads (in the example, the HUD is visible initially).

> Render order is determined by the **order of the keys** in `overlayBuilderMap`; a key added later is drawn on top.

### 1.2 On the game side: toggle overlays on and off

The methods on `game.overlays`:

```dart
class MyGame extends FlameGame {
  void pause() {
    pauseEngine();
    overlays.add('PauseMenu');
  }

  void resume() {
    overlays.remove('PauseMenu');
    resumeEngine();
  }

  void onPlayerDied() {
    overlays.add('GameOver');
  }
}
```

API summary:

```dart
// Render 'SecondaryMenu' (priority 1 -> on top).
overlays.add('SecondaryMenu', priority: 1);

// Render 'PauseMenu'. priority = 0 (default) -> below SecondaryMenu.
overlays.add('PauseMenu');

// Do not render 'PauseMenu'.
overlays.remove('PauseMenu');

// Toggle the open/closed state of 'PauseMenu'.
overlays.toggle('PauseMenu');

// Is 'PauseMenu' currently being rendered?
final hasPauseMenu = overlays.isActive('PauseMenu');

// Set activity conditionally.
overlays.setActive('SecondaryMenu', active: !hasPauseMenu);
```

The `priority` parameter determines the stacking order of overlays relative to one another: a higher `priority` is drawn on top.

### 1.3 Example overlay widgets (pause / game over / HUD)

Because overlays are plain Flutter widgets, the entire Flutter ecosystem (buttons, animation, theming) can be used here.

```dart
class PauseMenu extends StatelessWidget {
  const PauseMenu({required this.game, super.key});

  final MyGame game;

  @override
  Widget build(BuildContext context) {
    return ColoredBox(
      color: Colors.black54,
      child: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('Paused', style: TextStyle(fontSize: 32)),
            ElevatedButton(
              onPressed: game.resume,
              child: const Text('Resume'),
            ),
          ],
        ),
      ),
    );
  }
}

class GameOverMenu extends StatelessWidget {
  const GameOverMenu({required this.game, super.key});

  final MyGame game;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: ElevatedButton(
        onPressed: () {
          game.overlays.remove('GameOver');
          game.restart();
        },
        child: const Text('Play Again'),
      ),
    );
  }
}
```

> **Pause pattern:** `pauseEngine()` is called together with `overlays.add('PauseMenu')`; when the menu is closed, `overlays.remove(...)` + `resumeEngine()`. This stops the game update while keeping the Flutter UI interactive (see the Performance section for details).

---

## 2. RouterComponent: In-Game Screen/Scene Management

`RouterComponent` provides a **stack-based** navigation model similar to Flutter's `Navigator` class; the difference is that it works with **Flame components** instead of Flutter widgets. It organizes all destinations such as splash, main menu, settings, game screen, and pop-ups.

The router internally maintains a route stack. When a route is shown, it is placed on top of the stack; `pop()` removes the page on top. Routes are addressed by their unique names.

### 2.1 Setup

```dart
import 'package:flame/components.dart';
import 'package:flame/game.dart';
// To avoid clashing with Flutter's Route class:
import 'package:flutter/material.dart' hide Route;

class MyGame extends FlameGame {
  late final RouterComponent router;

  @override
  Future<void> onLoad() async {
    add(
      router = RouterComponent(
        routes: {
          'home': Route(HomePage.new),
          'level-selector': Route(LevelSelectorPage.new),
          'settings': Route(SettingsPage.new, transparent: true),
          'pause': PauseRoute(),
          'confirm-dialog': OverlayRoute.existing(),
        },
        initialRoute: 'home',
      ),
    );
  }
}
```

> **Important:** If `material.dart` (or another package) exports a class named `Route`, use `import '...' hide Route;`.

### 2.2 Route (opaque vs transparent, maintainState)

A `Route`'s primary property is its `builder`: the function that produces the component making up the page content. Routes are mounted as children of the `RouterComponent`.

- **Opaque (default):** The route below it is not rendered and does not receive pointer (tap/drag) events. Use for full-screen pages.
- **Transparent:** The route below it is rendered and receives events. Use for modal dialogs, inventory, and dialog UI. If you want it visually transparent but do not want events to pass through to what is below, add a background component to the route that captures events.
- **`maintainState`:** Defaults to `true` — state is preserved after the page is popped, and `builder` runs only on the first activation. If you set it to `false`, the component is discarded after a pop and `builder` is called again on every activation.

```dart
class HomePage extends Component with HasGameReference<MyGame> {
  @override
  Future<void> onLoad() async {
    add(StartButton(onPressed: () => game.router.pushNamed('level-selector')));
  }
}
```

To replace the current route, use `pushReplacementNamed` or `pushReplacement` (both first `pop` the current route, then push).

```dart
// Scene transitions:
game.router.pushNamed('settings');        // new page on top
game.router.pop();                          // remove the page on top
game.router.pushReplacementNamed('home');  // replace the current page
```

### 2.3 WorldRoute (switching levels/worlds)

`WorldRoute` allows you to switch the active game `World` through the router. It is ideal for transitioning between levels written as separate `World`s. By default it replaces the current world with a new one and preserves its state after a pop (with `maintainState: false` it is recreated on every activation). If you are not using the built-in `CameraComponent`, you can pass the camera explicitly to the constructor.

```dart
final router = RouterComponent(
  routes: {
    'level1': WorldRoute(MyWorld1.new),
    'level2': WorldRoute(MyWorld2.new, maintainState: false),
  },
  initialRoute: 'level1',
);

class MyWorld1 extends World {
  @override
  Future<void> onLoad() async {
    add(BackgroundComponent());
    add(PlayerComponent());
  }
}
```

### 2.4 OverlayRoute (a Flutter overlay through a route)

`OverlayRoute` allows game overlays to be added through the router; these routes are **transparent** by default. There are two constructors:

- One that takes a builder function (where you define the overlay widget),
- `OverlayRoute.existing()` — if the overlay is already defined in the `GameWidget`'s `overlayBuilderMap`.

```dart
final router = RouterComponent(
  routes: {
    'ok-dialog': OverlayRoute(
      (context, game) {
        return Center(child: OkDialog());
      },
    ),
    'confirm-dialog': OverlayRoute.existing(),
  },
);
```

Overlays defined inside the `GameWidget` do not even need to be pre-registered in the route map: `RouterComponent.pushOverlay()` does this for you. A registered overlay route can be activated with both the normal `.pushNamed()` and `.pushOverlay()` (both do the same thing; `.pushOverlay()` makes the intent clearer in the code). The current overlay can be replaced with `pushReplacementOverlay`.

```dart
game.router.pushOverlay('confirm-dialog');
```

This is the bridge point that **combines the Overlays API with the RouterComponent**: you integrate the Flutter UI (overlay) into the game's navigation stack.

### 2.5 ValueRoute (a route that returns a value on pop)

`ValueRoute<T>` is a route that returns a `T` value when it is popped from the stack — ideal for dialogs that obtain confirmation from the user.

Two steps:

1. Derive from `ValueRoute<T>`, override the `build()` method, and create the component to be shown. The component calls `completeWith(value)` to pop the route and return the value.

```dart
class YesNoDialog extends ValueRoute<bool> {
  YesNoDialog(this.text) : super(value: false);
  final String text;

  @override
  Component build() {
    return PositionComponent(
      children: [
        RectangleComponent(),
        TextComponent(text: text),
        Button(text: 'Yes', action: () => completeWith(true)),
        Button(text: 'No', action: () => completeWith(false)),
      ],
    );
  }
}
```

2. Show it with `Router.pushAndWait()`; it returns a future that resolves with the value returned from the route.

```dart
Future<void> confirmQuit() async {
  final result = await game.router.pushAndWait(YesNoDialog('Are you sure?'));
  if (result) {
    // ... user is sure
  } else {
    // ... user backed out
  }
}
```

---

## 3. Recommended Game-State Flow (Rapid Production Pattern)

A repeatable pattern across many small games:

| State | Mechanism |
|---|---|
| Main menu, settings, level selection | `RouterComponent` + `Route` |
| Level/world transition | `WorldRoute` |
| In-game HUD (score, health) | Persistent overlay (`initialActiveOverlays`) or Flame layout components |
| Pause menu | `overlays.add('PauseMenu')` + `pauseEngine()` |
| Game over | `overlays.add('GameOver')` |
| Confirmation dialog (quit, etc.) | `ValueRoute` + `pushAndWait` |

This separation cleanly distinguishes the UI (Flutter, easy to style) from the game-logic scenes (Flame components), and it is reusable in every new game.

---

## Sources

- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/overlays.md
- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/router.md
- https://docs.flame-engine.org/latest/
