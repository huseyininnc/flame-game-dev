# Flame: Overlays, Routing ve Oyun Içi Ekran Yonetimi

Bu bolum, bir Flame oyununda **menu / HUD / pause / game over** gibi ekranlari iki tamamlayici mekanizmayla nasil yonetecegimizi anlatir:

1. **Overlays** — Oyun canvas'inin uzerine Flutter widget'lari bindirme (menuler, butonlar, dialoglar icin idealdir).
2. **RouterComponent** — Oyunun *icinde*, Flame component'leri arasinda yigin (stack) tabanli gecis (menu -> playing -> paused -> game over).

Cok sayida kucuk oyunu hizli uretmek icin kural: **Flutter UI = Overlays**, **oyun-ici sahne gecisleri = RouterComponent**. Ikisi `OverlayRoute` ile birlestirilebilir.

---

## 1. Overlays: Oyun Uzerine Flutter Widget'lari

Flame oyunu bir Flutter widget agacinin icinde yasadigi icin, canvas'in uzerine herhangi bir Flutter widget'i yerlestirebilirsiniz. `Game.overlays` API'si bunu isimlendirilmis (named) overlay'leri ac/kapa yaparak kolaylastirir.

### 1.1 GameWidget tarafinda: `overlayBuilderMap`

Her overlay bir `String` anahtariyla tanimlanir ve `overlayBuilderMap` icinde bir builder fonksiyonuna eslenir. Builder imzasi: `(BuildContext context, MyGame game) => Widget`.

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

`initialActiveOverlays`, oyun ilk yuklendiginde acik olacak overlay anahtarlarinin listesidir (ornekte HUD basta gorunur).

> Render sirasi `overlayBuilderMap` icindeki **anahtar sirasina** gore belirlenir; sonradan eklenen anahtar ustte cizilir.

### 1.2 Oyun tarafinda: overlay'leri ac/kapa

`game.overlays` uzerindeki metotlar:

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

API ozeti:

```dart
// 'SecondaryMenu' render edilsin (priority 1 -> ustte).
overlays.add('SecondaryMenu', priority: 1);

// 'PauseMenu' render edilsin. priority = 0 (varsayilan) -> SecondaryMenu altinda.
overlays.add('PauseMenu');

// 'PauseMenu' render edilmesin.
overlays.remove('PauseMenu');

// 'PauseMenu' acik/kapali durumunu tersine cevir.
overlays.toggle('PauseMenu');

// 'PauseMenu' su anda render ediliyor mu?
final hasPauseMenu = overlays.isActive('PauseMenu');

// Kosula gore aktiflik ayarla.
overlays.setActive('SecondaryMenu', active: !hasPauseMenu);
```

`priority` parametresi overlay'lerin birbirine gore yigin sirasini belirler: yuksek `priority` ustte cizilir.

### 1.3 Ornek overlay widget'lari (pause / game over / HUD)

Overlay'ler dogrudan Flutter widget'i oldugu icin tum Flutter ekosistemi (butonlar, animasyon, tema) burada kullanilabilir.

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
            const Text('Duraklatildi', style: TextStyle(fontSize: 32)),
            ElevatedButton(
              onPressed: game.resume,
              child: const Text('Devam Et'),
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
        child: const Text('Tekrar Oyna'),
      ),
    );
  }
}
```

> **Pause kalibi:** `overlays.add('PauseMenu')` ile birlikte `pauseEngine()` cagrilir; menu kapatilirken `overlays.remove(...)` + `resumeEngine()`. Bu, oyun guncellemesini durdururken Flutter UI'nin etkilesimli kalmasini saglar (detay icin Performans bolumune bakin).

---

## 2. RouterComponent: Oyun Içi Ekran/Sahne Yonetimi

`RouterComponent`, Flutter'in `Navigator` sinifina benzeyen, **yigin tabanli** bir gezinme modeli sunar; fark, Flutter widget'lari yerine **Flame component'leri** ile calismasidir. Splash, ana menu, ayarlar, oyun ekrani, pop-up'lar gibi tum hedefleri organize eder.

Router icsel olarak bir route yigini tutar. Bir route gosterildiginde yiginin tepesine konur; `pop()` ile tepedeki sayfa kaldirilir. Route'lar benzersiz isimleriyle adreslenir.

### 2.1 Kurulum

```dart
import 'package:flame/components.dart';
import 'package:flame/game.dart';
// Flutter'in Route sinifiyla cakismayi onlemek icin:
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

> **Önemli:** `material.dart` (veya baska bir paket) `Route` adinda bir sinif export ediyorsa, `import '...' hide Route;` kullanin.

### 2.2 Route (opaque vs transparent, maintainState)

`Route`'un ana ozelligi `builder`'idir: sayfanin icerigini olusturan component'i ureten fonksiyon. Route'lar `RouterComponent`'e cocuk olarak mount edilir.

- **Opaque (varsayilan):** Altindaki route render edilmez ve pointer (tap/drag) olayi almaz. Tam ekran sayfalar icin kullanin.
- **Transparent:** Altindaki route render edilir ve olay alir. Modal dialog, envanter, dialog UI icin kullanin. Görsel olarak transparan ama altina olay gecmemesini istiyorsaniz, route'a olaylari yakalayan bir arka plan component'i ekleyin.
- **`maintainState`:** Varsayilan `true` — sayfa pop'landiktan sonra state korunur ve `builder` yalnizca ilk aktivasyonda calisir. `false` yaparsaniz pop sonrasi component atilir ve `builder` her aktivasyonda yeniden cagrilir.

```dart
class HomePage extends Component with HasGameReference<MyGame> {
  @override
  Future<void> onLoad() async {
    add(StartButton(onPressed: () => game.router.pushNamed('level-selector')));
  }
}
```

Mevcut route'u degistirmek icin `pushReplacementNamed` veya `pushReplacement` kullanilir (her ikisi de once mevcut route'ta `pop`, sonra push yapar).

```dart
// Sahne gecisleri:
game.router.pushNamed('settings');        // ustte yeni sayfa
game.router.pop();                          // tepedeki sayfayi kaldir
game.router.pushReplacementNamed('home');  // mevcut sayfayi degistir
```

### 2.3 WorldRoute (level/dunya degistirme)

`WorldRoute`, router uzerinden aktif oyun `World`'unu degistirmeyi saglar. Ayri `World` olarak yazilmis level'lar arasinda gecis icin idealdir. Varsayilan olarak mevcut dunyayi yenisiyle degistirir ve pop sonrasi state'ini korur (`maintainState: false` ile her aktivasyonda yeniden olusturulur). Yerlesik `CameraComponent` kullanmiyorsaniz kamerayi constructor'a acikca gecebilirsiniz.

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

### 2.4 OverlayRoute (Flutter overlay'i route uzerinden)

`OverlayRoute`, oyun overlay'lerini router uzerinden eklemeyi saglar; bu route'lar varsayilan olarak **transparent**'tir. Iki constructor vardir:

- Builder fonksiyonu alan (overlay widget'ini burada tanimlarsiniz),
- `OverlayRoute.existing()` — overlay zaten `GameWidget`'in `overlayBuilderMap`'inde tanimliysa.

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

`GameWidget` icinde tanimli overlay'lerin route map'inde onceden tanimlanmasi bile gerekmez: `RouterComponent.pushOverlay()` bunu sizin yerinize yapar. Kayitli bir overlay route'u hem normal `.pushNamed()` hem de `.pushOverlay()` ile aktive edilebilir (ikisi ayni isi yapar; `.pushOverlay()` niyeti kodda daha acik kilar). Mevcut overlay `pushReplacementOverlay` ile degistirilebilir.

```dart
game.router.pushOverlay('confirm-dialog');
```

Bu, **Overlays API'si ile RouterComponent'i birlestiren** kopru noktasidir: Flutter UI'yi (overlay) oyunun navigasyon yiginina entegre edersiniz.

### 2.5 ValueRoute (pop'ta deger donen route)

`ValueRoute<T>`, yigindan cikarildiginda bir `T` degeri donen route'tur — kullanicidan onay alan dialoglar icin idealdir.

Iki adim:

1. `ValueRoute<T>`'den turetin, `build()` metodunu override edin ve gosterilecek component'i olusturun. Component, route'u pop edip degeri dondurmek icin `completeWith(value)` cagirir.

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

2. `Router.pushAndWait()` ile gosterin; route'tan donen degerle resolve olan bir future doner.

```dart
Future<void> confirmQuit() async {
  final result = await game.router.pushAndWait(YesNoDialog('Emin misiniz?'));
  if (result) {
    // ... kullanici emin
  } else {
    // ... kullanici vazgecti
  }
}
```

---

## 3. Onerilen Oyun-Durum Akisi (Hizli Uretim Kalibi)

Cok sayida kucuk oyunda tekrarlanabilir bir kalip:

| Durum | Mekanizma |
|---|---|
| Ana menu, ayarlar, level secimi | `RouterComponent` + `Route` |
| Level/dunya gecisi | `WorldRoute` |
| Oyun-ici HUD (skor, can) | Kalici overlay (`initialActiveOverlays`) veya Flame layout component'leri |
| Pause menu | `overlays.add('PauseMenu')` + `pauseEngine()` |
| Game over | `overlays.add('GameOver')` |
| Onay dialogu (cikis vb.) | `ValueRoute` + `pushAndWait` |

Bu ayrim, UI'yi (Flutter, kolay stillenebilir) oyun mantigi sahnelerinden (Flame component'leri) net biçimde ayirir ve her yeni oyunda yeniden kullanilabilir.

---

## Kaynaklar

- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/overlays.md
- https://raw.githubusercontent.com/flame-engine/flame/main/doc/flame/router.md
- https://docs.flame-engine.org/latest/
