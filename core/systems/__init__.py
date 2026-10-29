"""Per-frame behaviors that operate on entities: animation, collision, spawning."""


"""
TODO: 20261029
 You've got core/game.py and core/scene.py working. The main work left is the imports in core/resource_loader.py and gameplay/scenes/tiled_play_scene.py. I haven't edited anything. I checked by importing each module from the repo root.

  Works
  - core.game, core.scene, core.systems/__init__.py (new) and gameplay/scenes/ are all in place.
  - core/game.py now has the __init__ docstring and the run() → _game_loop() split. It looks fine.

  Still broken
  1. core/resource_loader.py:13 has from . import config, which fails with ImportError: cannot import name 'config' from 'core'. Change it to from config import config, the same fix as in game.py.
  2. gameplay/scenes/tiled_play_scene.py:17-26 has two kinds of stale imports. It fails with No module named 'engine'.
     - The engine.* ones (resource_loader, entity_manager, camera, tilemap, collision) need the new locations, e.g. from core.resource_loader import ResourceLoader.
     - The bare entities.* ones (player, enemy, missile, stone) need to become gameplay.entities.*.
  3. core/game.py:27 has from core import scene, which does nothing here. Nothing in game.py uses it, and the scene parameter in run() shadows it. Delete the line.

  Not moved yet
  - From engine/: entity_manager.py, tilemap.py, spawner.py and input.py aren't under core/ yet. core/camera/camera.py and core/systems/collision.py are the older versions, so those two still need the diff-and-merge.
  - From entities/: gameplay/entities/ doesn't exist, so stone.py and enemy.py have no home yet.
  - Data files: the .tmj / .tsj files and enemies.json haven't moved yet.

  Leftovers
  - Duplicate files: utils/resource_loader.py (empty) and gameplay/spawner/enemy_spawner.py (probably superseded).
  - Old root main.py: it still imports game.actions..., a path that no longer exists.
  - Stale old mains: game/main.py is deleted but unstaged, game/ official_main.py still has the leading space in its name, and games/main.py is new.

  Suggested order
  1. Fix the resource_loader import and delete the game.py line.
  2. Move entity_manager, tilemap and the entities.
  3. Fix the scene's imports.
  4. Write the root main.py, a short entry point that creates Game() and runs TiledPlayScene().
  5. Run it, and merge camera, collision and entity last.

  I can do steps 1-3 if you'd like.

   You've got core/game.py and core/scene.py working. The main work left is the imports in core/resource_loader.py and gameplay/scenes/tiled_play_scene.py. I haven't edited anything. I checked by importing each module from the repo root.

  Works
  - core.game, core.scene, core.systems/__init__.py (new) and gameplay/scenes/ are all in place.
  - core/game.py now has the __init__ docstring and the run() → _game_loop() split. It looks fine.

  Still broken
  1. core/resource_loader.py:13 has from . import config, which fails with ImportError: cannot import name 'config' from 'core'. Change it to from config import config, the same fix as in game.py.
  2. gameplay/scenes/tiled_play_scene.py:17-26 has two kinds of stale imports. It fails with No module named 'engine'.
     - The engine.* ones (resource_loader, entity_manager, camera, tilemap, collision) need the new locations, e.g. from core.resource_loader import ResourceLoader.
     - The bare entities.* ones (player, enemy, missile, stone) need to become gameplay.entities.*.
  3. core/game.py:27 has from core import scene, which does nothing here. Nothing in game.py uses it, and the scene parameter in run() shadows it. Delete the line.

  Not moved yet
  - From engine/: entity_manager.py, tilemap.py, spawner.py and input.py aren't under core/ yet. core/camera/camera.py and core/systems/collision.py are the older versions, so those two still need the diff-and-merge.
  - From entities/: gameplay/entities/ doesn't exist, so stone.py and enemy.py have no home yet.
  - Data files: the .tmj / .tsj files and enemies.json haven't moved yet.

  Leftovers
  - Duplicate files: utils/resource_loader.py (empty) and gameplay/spawner/enemy_spawner.py (probably superseded).
  - Old root main.py: it still imports game.actions..., a path that no longer exists.
  - Stale old mains: game/main.py is deleted but unstaged, game/ official_main.py still has the leading space in its name, and games/main.py is new.

  Suggested order
  1. Fix the resource_loader import and delete the game.py line.
  2. Move entity_manager, tilemap and the entities.
  3. Fix the scene's imports.
  4. Write the root main.py, a short entry point that creates Game() and runs TiledPlayScene().
  5. Run it, and merge camera, collision and entity last.

  I can do steps 1-3 if you'd like.

"""