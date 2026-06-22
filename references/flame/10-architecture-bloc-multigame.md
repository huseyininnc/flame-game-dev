# Flame + flame_bloc: Katmanli Mimari ve Çok-Oyunlu Monorepo

Bu bolum iki konuyu birlestirir:

1. **flame_bloc** ile oyun mantigini Bloc/Cubit'lerde, render'i ise Flame component'lerinde tutmak (Very Good Ventures katmanli mimarisiyle uyumlu).
2. Cok sayida kucuk oyunu hizli uretmek icin **paylasilan `game_core` paketi + oyun basina paket** seklinde yeniden kullanilabilir bir monorepo yapisi.

---

## 1. flame_bloc — Dogrulanmis API

`flame_bloc`, `flutter_bloc`'a benzer sekilde Bloc ve Cubit'leri `FlameGame` icinde kullanmayi saglar. Tum sinif adlari asagida flame_bloc kaynagindan dogrulanmistir.

### 1.1 Bloc saglama: `FlameBlocProvider`

```dart
class MyGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    await add(
      FlameBlocProvider<PlayerInventoryBloc, PlayerInventoryState>(
        create: () => PlayerInventoryBloc(),
        children: [
          Player(),
          // ...
        ],
      ),
    );
  }
}
```

Bu provider'in `children'i olan tum component'ler bloc'a erisir. Var olan bir bloc ornegini paylasmak icin `.value` constructor'i kullanilir (örn. Flutter agacindaki bir bloc'u Flame'e tasimak):

```dart
FlameBlocProvider<ScoreBloc, ScoreState>.value(
  value: existingScoreBloc,
  children: [GameWorld()],
);
```

### 1.2 Birden cok bloc: `FlameMultiBlocProvider`

```dart
class MyGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    await add(
      FlameMultiBlocProvider(
        providers: [
          FlameBlocProvider<PlayerInventoryBloc, PlayerInventoryState>(
            create: () => PlayerInventoryBloc(),
          ),
          FlameBlocProvider<PlayerStatsBloc, PlayerStatsState>(
            create: () => PlayerStatsBloc(),
          ),
        ],
        children: [
          Player(),
          // ...
        ],
      ),
    );
  }
}
```

### 1.3 State'i dinleme — uc yaklasim

**(a) `FlameBlocListener` component'i** (`listenWhen` filtresi destekler):

```dart
class Player extends PositionComponent {
  @override
  Future<void> onLoad() async {
    await add(
      FlameBlocListener<PlayerInventoryBloc, PlayerInventoryState>(
        onNewState: (state) {
          updateGear(state);
        },
        listenWhen: (previous, current) => previous.gear != current.gear,
      ),
    );
  }
}
```

**(b) `FlameBlocListenable` mixin'i** — `onNewState`, ayrica opsiyonel `onInitialState` ve `listenWhen` override'lari vardir:

```dart
class Player extends PositionComponent
    with FlameBlocListenable<PlayerInventoryBloc, PlayerInventoryState> {

  @override
  void onInitialState(PlayerInventoryState state) {
    // Component mount edildiginde mevcut state ile bir kez cagrilir.
    updateGear(state);
  }

  @override
  bool listenWhen(PlayerInventoryState previous, PlayerInventoryState current) {
    return previous.gear != current.gear;
  }

  @override
  void onNewState(PlayerInventoryState state) {
    updateGear(state);
  }
}
```

**(c) `FlameBlocReader` mixin'i** — sadece bloc'a erisip event gondermek icin (state degisikligi dinlemez). **Tek bir bloc** ile sinirlidir:

```dart
class Player extends PositionComponent
    with FlameBlocReader<PlayerStatsBloc, PlayerStatsState> {

  void takeHit() {
    bloc.add(const PlayerDamaged());
  }
}
```

> Sinif adlarini ezberden uretmeyin; dogru adlar: `FlameBlocProvider`, `FlameBlocProvider.value`, `FlameMultiBlocProvider`, `FlameBlocListener` (parametre `onNewState`), `FlameBlocListenable` (mixin, `onNewState`/`onInitialState`/`listenWhen`), `FlameBlocReader` (mixin, `bloc` getter).

### 1.4 Sorumluluk ayrimi (VGV ile hizalama)

| Katman | Sorumluluk | flame_bloc rolu |
|---|---|---|
| **Repository / Data** | Veri kaynaklari (yuksek skor kalicilik, ayarlar, ses tercihleri) | Bloc tarafindan tuketilir |
| **Bloc / Cubit** | Oyun *durumu* ve *kurallari* (skor, can, envanter, faz) | `FlameBlocProvider` ile saglanir |
| **Component (Flame)** | Yalnizca **render** ve girdi -> event | `FlameBlocReader` ile event gonderir, `FlameBlocListenable` ile state'e tepki verir |

Kural: **Component'ler karar vermez; durumu okur ve cizer.** Hasar, skor, faz gecisi gibi kararlar Bloc'ta verilir. Bu, oyun mantigini widget/test edilebilir tutar ve render'dan ayirir.

---

## 2. Çok-Oyunlu Monorepo: Yeniden Kullanim Stratejisi

Hedef: Cok sayida kucuk oyunu **paylasilan bir cekirdek** uzerine hizla uretmek. VGV konvansiyonlari (Melos monorepo, Bloc, katmanli mimari, `very_good_analysis`) izlenir.

### 2.1 Klasor agaci

```text
games_monorepo/
├── melos.yaml
├── pubspec.yaml
├── analysis_options.yaml          # include: package:very_good_analysis/analysis_options.yaml
│
├── packages/
│   ├── game_core/                 # PAYLASILAN cekirdek (UI/oyun-bagimsiz)
│   │   ├── lib/
│   │   │   ├── src/
│   │   │   │   ├── base/
│   │   │   │   │   └── base_flame_game.dart      # ortak FlameGame taban sinifi
│   │   │   │   ├── components/                    # yeniden kullanilabilir component'ler
│   │   │   │   │   ├── fade_in_component.dart
│   │   │   │   │   ├── parallax_background.dart
│   │   │   │   │   └── pooled/                     # nesne havuzu yardimcilari
│   │   │   │   ├── services/
│   │   │   │   │   ├── audio_service.dart          # ses calma soyutlamasi
│   │   │   │   │   └── asset_manager.dart          # onbellekli asset yukleme
│   │   │   │   ├── state/                          # ortak Bloc/Cubit'ler
│   │   │   │   │   ├── score/
│   │   │   │   │   │   ├── score_bloc.dart
│   │   │   │   │   │   ├── score_event.dart
│   │   │   │   │   │   └── score_state.dart
│   │   │   │   │   └── game_phase/
│   │   │   │   │       └── game_phase_cubit.dart   # menu/playing/paused/gameOver
│   │   │   │   └── overlays/
│   │   │   │       ├── pause_menu.dart             # paylasilan Flutter overlay'leri
│   │   │   │       └── game_over_menu.dart
│   │   │   └── game_core.dart                      # public barrel export
│   │   ├── pubspec.yaml
│   │   └── test/
│   │
│   ├── scores_repository/         # DATA + REPOSITORY katmani (kalicilik)
│   │   ├── lib/
│   │   │   ├── src/
│   │   │   │   ├── scores_repository.dart
│   │   │   │   └── models/score_entry.dart
│   │   │   └── scores_repository.dart
│   │   └── pubspec.yaml
│   │
│   └── game_ui/                   # paylasilan tema/buton/dialog (Flutter)
│       └── ...
│
└── apps/
    ├── flappy_clone/              # OYUN BASINA paket (feature katmani)
    │   ├── lib/
    │   │   ├── game/
    │   │   │   ├── flappy_game.dart            # extends BaseFlameGame
    │   │   │   ├── components/                  # bu oyuna ozel component'ler
    │   │   │   └── state/                       # bu oyuna ozel Bloc'lar
    │   │   ├── view/
    │   │   │   └── flappy_page.dart             # GameWidget + overlayBuilderMap
    │   │   └── main.dart
    │   ├── assets/
    │   └── pubspec.yaml            # depends on: game_core, scores_repository, game_ui
    │
    └── brick_breaker/
        └── ... (ayni iskelet)
```

### 2.2 Katman sinirlari (bagimlilik yonu)

```text
apps/<game>  ->  game_core  ->  scores_repository  ->  (data sources)
   (feature)      (engine)        (repository)            (data)
```

- **`scores_repository` (data/repository):** Flame'i bilmez. Yuksek skoru kaydeder/okur, domain modelleri doner. Test edilebilir, saf Dart.
- **`game_core` (engine):** Tum oyunlarin paylastigi tabandir — `BaseFlameGame`, yeniden kullanilabilir component'ler, `AudioService`, `AssetManager`, ortak Bloc'lar (`ScoreBloc`, `GamePhaseCubit`), paylasilan overlay'ler. Belirli bir oyunu bilmez.
- **`apps/<game>` (feature):** Yalnizca o oyuna ozgu component'ler, Bloc'lar ve `GameWidget` kablolamasi. `game_core` ve `scores_repository`'a bagimlidir.

Bu yon **tek yonludur**: feature -> core -> repository. Core asla bir oyuna geri bagimli olmaz; yeni oyun eklemek mevcut core'u bozmaz (Open/Closed).

### 2.3 Paylasilan taban oyun sinifi

```dart
// game_core/lib/src/base/base_flame_game.dart
abstract class BaseFlameGame extends FlameGame {
  BaseFlameGame({required this.audioService, required this.assetManager});

  final AudioService audioService;
  final AssetManager assetManager;

  @override
  Future<void> onLoad() async {
    await assetManager.preloadCommon();
    await super.onLoad();
  }
}
```

Oyun basina paket bunu genisletir:

```dart
// apps/flappy_clone/lib/game/flappy_game.dart
class FlappyGame extends BaseFlameGame {
  FlappyGame({required super.audioService, required super.assetManager});

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    await add(
      FlameMultiBlocProvider(
        providers: [
          FlameBlocProvider<ScoreBloc, ScoreState>(create: ScoreBloc.new),
          FlameBlocProvider<GamePhaseCubit, GamePhase>(create: GamePhaseCubit.new),
        ],
        children: [FlappyWorld()],
      ),
    );
  }
}
```

### 2.4 Paylasilan servisler (soyutlama uzerinden bagimlilik)

`AudioService` ve `AssetManager`, somut Flame cagrilarini soyutlayip oyunlara enjekte edilir (Dependency Inversion). Boylece her oyun ayni servisleri tekrar yazmaz ve testte mock'lanabilir.

```dart
// game_core/lib/src/services/audio_service.dart
abstract class AudioService {
  Future<void> preload(List<String> files);
  void playSfx(String file);
  Future<void> playBgm(String file);
}
```

### 2.5 VGV konvansiyonlari ozeti

- **Bloc/Cubit** ile durum yonetimi; oyun mantigi component'te degil Bloc'ta.
- **Katmanli mimari:** data (`*_repository` icindeki kaynaklar) -> repository -> business (Bloc) -> feature (oyun paketi). Her katman yalnizca bir altindakine bagimli.
- **Paket basina tek sorumluluk:** `scores_repository` sadece kalicilik, `game_core` sadece yeniden kullanilabilir motor.
- **`very_good_analysis`** kok `analysis_options.yaml`'da en sıkı lint kurali olarak include edilir.
- **Melos** ile paketler arasi bootstrap/test/format tek komutla.
- **Yeni oyun = yeni `apps/<game>` paketi**; core kopyalanmaz, bagimlilikla cekilir.

---

## Kaynaklar

- https://raw.githubusercontent.com/flame-engine/flame/main/packages/flame_bloc/README.md
- https://pub.dev/packages/flame_bloc
- https://verygood.ventures/blog/flame-bloc-new-api
