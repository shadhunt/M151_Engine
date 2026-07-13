# Simple Engine

A small, complete reference implementation of what a "basic game engine"
needs, built to consolidate the lessons from the other examples in this
repo (camera/coordinate spaces, delta-time movement, sprite-sheet
cutting, JSON-driven spawning) into ONE reusable structure instead of
several copy-pasted prototypes.

**Read `docs/M151_Simple_Engine_Guide.pdf` for the full walkthrough** --
folder-by-folder, system-by-system, with worked examples and diagrams.
This README is just the quick map + quick start.

**Read `docs/M151_Simple_Engine_StudyGuide.pdf` if you're studying this
offline** -- a four-week, self-paced curriculum (Check-Yourself Q&A,
drills, and a file-by-file migration map) for working through this
engine and porting each lesson into the main M151_Engine project.

**Read `docs/M151_Tiled_Tutorial.pdf` to learn Tiled** -- draw a map with
objects in the free Tiled editor, export it as JSON, and load it with
`engine/tilemap.py`. Run `python main_tiled_demo.py` to see it working:
the same enemies as `main.py`, sourced from `data/level1.tmj` instead of
a flat image + hand-typed JSON offsets.

## Quick start

```bash
cd examples/simple_engine
python main.py
```

Controls: **WASD** to move, **SPACE** to shoot, **F1** to toggle hitbox
outlines, **ESC** to quit. Walk your tank around and shoot the four
enemies -- each one uses a different movement "trail" (patrol / bounce /
zigzag) so you can watch the difference.

## Folder structure

```
simple_engine/
├── main.py              entry point -- ~5 lines, wires Game to PlayScene
├── main_tiled_demo.py   same demo, level sourced from data/level1.tmj (Tiled) instead
├── engine/               reusable systems -- copy this folder into a new project as-is
│   ├── game.py           owns the window, clock, and the run loop
│   ├── scene.py          base class for a game screen/mode
│   ├── entity.py         base class every game object inherits from
│   ├── entity_manager.py registry of all live entities, grouped by name
│   ├── camera.py         world <-> screen coordinate conversion, edge-clamped scrolling
│   ├── animation.py       picks the right sprite frame for the current direction
│   ├── collision.py      rectangle overlap checks between entity groups
│   ├── resource_loader.py loads + caches images, cuts sprite sheets
│   ├── input.py          polls WASD into a normalized 8-directional vector
│   ├── spawner.py        turns a JSON file into live entities via a factory function
│   ├── tilemap.py        loads a Tiled (.tmj) map: image layer + object layers
│   └── config.py         every tunable constant in one place
├── entities/             THIS game's objects -- built on top of engine/entity.py
│   ├── player.py
│   ├── enemy.py
│   └── missile.py
├── scenes/
│   ├── play_scene.py       wires engine systems + entities into one playable scene
│   └── tiled_play_scene.py same scene, sourced from a Tiled level instead
├── data/
│   ├── enemies.json      enemy spawn positions/speeds/trails -- edit this, not the code
│   └── level1.tmj        the same 4 enemies, authored as a Tiled map instead
├── assets/
│   ├── images/           art, copied from the main project (see per-folder README.md
│   │                     for which images the demo actually uses vs. which are there
│   │                     for you to wire in next)
│   ├── sounds/           empty -- see assets/sounds/README.md before adding a sound system
│   └── fonts/            empty -- see assets/fonts/README.md before adding a real font
└── docs/
    ├── M151_Simple_Engine_Guide.pdf        the full instruction guide
    ├── M151_Simple_Engine_StudyGuide.pdf   offline 4-week study curriculum
    └── M151_Tiled_Tutorial.pdf             how to draw a map + objects in Tiled and load it
```

## The one rule that makes this an "engine" and not another prototype

`engine/` never imports from `entities/` or `scenes/`. Systems only see
generic `Entity` objects (position, size, `update()`, `draw()`,
`get_hitbox()`) -- they have no idea a "Player" or "Enemy" exists. That's
what lets `EntityManager` and `CollisionSystem` work unchanged no matter
what you build in `entities/` next.

## What's deliberately NOT here yet

No sound, no menu/title screen, no save system, no particle effects, no
spatial-partitioning for collision. These are all real next steps, not
oversights -- see "Chapter 6 -- Where To Go Next" in the PDF guide for
why each one was left out and what adding it would look like.
