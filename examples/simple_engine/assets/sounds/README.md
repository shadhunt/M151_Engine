# sounds/

Empty on purpose -- the main M151_Engine project has no sound assets or
sound system yet, so there's nothing to copy over.

There's also no `engine/audio.py` in this example, because the engine
should never grow a system before there's something real to test it
against. When you're ready to add sound:

1. Drop a `.wav` or `.ogg` file in here (e.g. `missile_fire.wav`).
2. Add a tiny `engine/audio.py` wrapping `pygame.mixer.Sound`, with the
   same "load once, cache forever" pattern as `ResourceLoader`.
3. Call it from `PlayScene._fire_missile()` and
   `PlayScene._on_missile_hit_enemy()` -- the two moments that already
   know exactly when a sound should play.

Building the system around a real sound file (so you can hear whether
your volume/timing choices are actually right) will teach you more than
writing the audio wrapper first and guessing.
