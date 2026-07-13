# enemies/

Full-size vehicle artwork (tanks, jeeps, helicopters, etc.) copied over from
the main project's asset library. **Not wired into the demo yet.**

The demo's `Enemy` entity currently gets its look by cutting a small
32x32 cell out of `characters.png` (see `engine/resource_loader.py` ->
`slice_sheet`). These files are full standalone images instead of sheet
cells, so loading one is simpler, not harder:

```python
tank_image = resources.load_image(
    config.ASSETS_DIR / "images" / "enemies" / "HeavyTank.png",
    convert_alpha=True,
)
```

A good next exercise: give `Enemy` an optional `image` override so some
enemies use a full art asset like `BossTank.png` instead of the sheet-cut
sprite, without changing `EntityManager` or `CollisionSystem` at all.
