__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "04.04.2026"
__email__ = "m@hler.eu"
__status__ = "Development"


import json
import os
import urllib.request
from pathlib import Path
from typing import Any, Optional


class ItemSchema:
    def __init__(self, data: dict[str, Any]):
        self._data = data
        self._weapons = {}
        self._skins = {}
        self._agents = {}
        self._stickers = {}
        self._charms = {}
        self._sticker_slabs = {}
        self._initialize()

    def _initialize(self):
        for key, item in self._data.items():
            weapon_def = item.get("weapon", {})
            weapon_id = weapon_def.get("weapon_id")
            def_index = item.get("def_index")

            if key.startswith("agent-") and def_index is not None:
                self._agents[int(def_index)] = item.get("name")

            elif (key.startswith("sticker_slab-") or key.startswith("patch-")) and def_index is not None:
                original = item.get("original", {})
                self._sticker_slabs[int(def_index)] = {
                    "name": item.get("name", "Unknown"),
                    "codename": original.get("name", "Unknown"),
                    "material": original.get("image_inventory", "Unknown"),
                    "image": item.get("image", "")
                }

            elif key.startswith("sticker-") and def_index is not None:
                original = item.get("original", {})
                self._stickers[int(def_index)] = {
                    "name": item.get("name", "Unknown"),
                    "codename": original.get("name", "Unknown"),
                    "material": original.get("image_inventory", "Unknown"),
                    "image": item.get("image", "")
                }

            elif (key.startswith("charm-") or key.startswith("keychain-")) and def_index is not None:
                original = item.get("original", {})
                self._charms[int(def_index)] = {
                    "name": item.get("name", "Unknown"),
                    "codename": original.get("name", "Unknown"),
                    "material": original.get("image_inventory", "Unknown"),
                    "image": item.get("image", "")
                }

            if weapon_id is not None:
                w_id = int(weapon_id)
                w_name = weapon_def.get("name")
                if w_name:
                    self._weapons[w_id] = w_name

                paint_index = item.get("paint_index")
                if paint_index is not None:
                    p_id = int(paint_index)
                    pattern_def = item.get("pattern", {})
                    skin_name = pattern_def.get("name") or item.get("name")

                    if skin_name:
                        self._skins[(w_id, p_id)] = {
                            "name": skin_name,
                            "image": item.get("image", ""),
                            "min_float": item.get("min_float"),
                            "max_float": item.get("max_float")
                        }

    def get_weapon_name(self, weapon_id: int) -> str:
        return self._weapons.get(weapon_id, "Unknown")

    def get_agent_name(self, defindex: int) -> str:
        return self._agents.get(defindex, "Unknown")

    def get_skin_info(self, weapon_id: int, paint_index: int) -> Optional[dict[str, Any]]:
        return self._skins.get((weapon_id, paint_index))

    def get_sticker_info(self, sticker_id: int) -> Optional[dict[str, Any]]:
        return self._stickers.get(sticker_id)

    def get_sticker_slab_info(self, defindex: int) -> Optional[dict[str, Any]]:
        return self._sticker_slabs.get(defindex)

    def get_charm_info(self, charm_id: int) -> Optional[dict[str, Any]]:
        return self._charms.get(charm_id)

    @staticmethod
    def get_image_url(icon_url: str) -> str:
        return icon_url if icon_url else ""


def get_config_path() -> Path:
    new_path = Path(__file__).parent / ".cs2inspect.json"
    old_path = Path(__file__).parent / ".cs2inspect_config.json"

    if not new_path.exists() and old_path.exists():
        try:
            old_path.rename(new_path)
        except Exception:
            return old_path

    return new_path


def save_schema_path(path: str):
    config_path = get_config_path()
    try:
        config = {"schema_path": str(Path(path).absolute())}
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception:
        pass


def load_schema_path() -> Optional[str]:
    config_path = get_config_path()
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                path = config.get("schema_path")
                if path and Path(path).exists():
                    return path
        except Exception:
            pass

    fallbacks = [
        Path.cwd() / "cs2_schema.json",
        Path(__file__).parent.parent / "cs2_schema.json",
        Path(__file__).parent / "cs2_schema.json"
    ]

    for f in fallbacks:
        if f.exists():
            return str(f.absolute())

    return None


def download_schema(destination: str = "cs2_schema.json", language: str = "en") -> str:
    url = f"https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/{language}/all.json"
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())

    abs_path = str(Path(destination).absolute())
    with open(abs_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    save_schema_path(abs_path)
    return abs_path


def load_schema(path: Optional[str] = None) -> Optional[ItemSchema]:
    if path is None:
        path = load_schema_path()

    if not path or not Path(path).exists():
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return ItemSchema(data)
    except Exception:
        return None


if __name__ == '__main__':
    exit(1)
