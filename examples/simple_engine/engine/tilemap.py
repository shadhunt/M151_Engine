"""
TiledMap -- loads a map authored in Tiled (mapeditor.org) and exported as
JSON (.tmj): an image layer for the background plus one or more object
layers for spawn points, drawn and named visually instead of hand-typed
into a JSON file like data/enemies.json.

This only reads the two layer types this engine actually uses --
"imagelayer" and "objectgroup". Tile layers (painted-tile maps, as
opposed to one big background image) aren't parsed here; see the Tiled
tutorial in docs/ for why that's a deliberate, separate next step.
"""
import json
from pathlib import Path


class TiledMap:
    def __init__(self, tmj_path):
        self._path = Path(tmj_path)
        with open(self._path) as f:
            self._data = json.load(f)

        if self._data.get("infinite"):
            raise ValueError(
                f"{self._path.name}: infinite maps aren't supported by this "
                "loader -- uncheck 'Infinite map' when creating the map in Tiled."
            )

        self.tile_width  = self._data["tilewidth"]
        self.tile_height = self._data["tileheight"]
        self.width_px    = self._data["width"] * self.tile_width
        self.height_px   = self._data["height"] * self.tile_height

    def image_layer(self, name: str | None = None) -> dict:
        """
        Return {"path": Path, "x": int, "y": int} for the first image
        layer found (or the one matching `name`). The path is resolved
        relative to the .tmj file's own folder, matching how Tiled stores
        image references relative to the map file.
        """
        for layer in self._data["layers"]:
            if layer["type"] != "imagelayer":
                continue
            if name is not None and layer["name"] != name:
                continue
            return {
                "path": (self._path.parent / layer["image"]).resolve(),
                "x": layer.get("x", 0),
                "y": layer.get("y", 0),
            }
        raise KeyError(f"No image layer named {name!r} in {self._path.name}")

    def object_layer(self, name: str) -> list[dict]:
        """
        Return every object in the object layer called `name` as plain
        dicts: {"name", "type", "x", "y", "properties"}. `properties` is
        flattened from Tiled's [{"name", "type", "value"}, ...] list into
        a simple {name: value} dict, since that's what call sites want.
        """
        for layer in self._data["layers"]:
            if layer["type"] == "objectgroup" and layer["name"] == name:
                return [self._simplify_object(obj) for obj in layer["objects"]]
        raise KeyError(f"No object layer named {name!r} in {self._path.name}")

    @staticmethod
    def _simplify_object(obj: dict) -> dict:
        properties = {p["name"]: p["value"] for p in obj.get("properties", [])}
        return {
            "name": obj.get("name", ""),
            # Tiled's editor panel calls this field "Class" since v1.9, but
            # the JSON key is still "type" for backward compatibility.
            "type": obj.get("type", obj.get("class", "")),
            "x": obj["x"],
            "y": obj["y"],
            "width": obj.get("width",0),
            "height":obj.get("height",0),
            "properties": properties,
        }
