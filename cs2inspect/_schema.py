__date__ = "03.04.2026"
import json
import os
import urllib.request
from pathlib import Path
from typing import Any, Optional


class ItemSchema:
    def __init__(self, data: dict[str, Any]):
        self._data = data
        self._weapons = {}  # {defindex: name}
        self._skins = {}  # {(defindex, paintindex): {data}}
        self._initialize()

    def _initialize(self):
        # ByMykel CSGO-API /all.json structure
        for key, item in self._data.items():
            # 1. Try to get defindex
            # Assets like weapons have it in weapon.weapon_id
            # Assets like stickers have it in def_index
            weapon_def = item.get("weapon", {})
            defindex = weapon_def.get("weapon_id")
            if defindex is None:
                defindex = item.get("def_index")

            if defindex is not None:
                defindex = int(defindex)

                # Store weapon name
                weapon_name = weapon_def.get("name")
                if weapon_name:
                    self._weapons[defindex] = weapon_name

                # 2. Try to get paintindex (for skins)
                paintindex = item.get("paint_index")
                if paintindex is not None:
                    paintindex = int(paintindex)
                    # We store skin info. We use the pattern name for the "item_name"
                    pattern_def = item.get("pattern", {})
                    # If it's a skin, we want the pattern name (e.g. "Seasons")
                    # but the item name in the API might be "XM1014 | Seasons (Factory New)"
                    skin_name = pattern_def.get("name")
                    if not skin_name:
                        skin_name = item.get("name")

                    if skin_name:
                        self._skins[(defindex, paintindex)] = {
                            "name": skin_name,
                            "image": item.get("image", ""),
                            "min_float": item.get("min_float"),
                            "max_float": item.get("max_float")
                        }

    def get_weapon_name(self, defindex: int) -> str:
        return self._weapons.get(defindex, "Unknown")

    def get_skin_info(self, defindex: int, paintindex: int) -> Optional[dict[str, Any]]:
        return self._skins.get((defindex, paintindex))

    @staticmethod
    def get_image_url(icon_url: str) -> str:
        if not icon_url:
            return ""
        # The API already provides the full URL or a relative one
        return icon_url


def get_config_path() -> Path:
    # Near the library: in the package's parent directory or inside the package
    return Path(__file__).parent / ".cs2inspect_config.json"


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
                return config.get("schema_path")
        except Exception:
            return None
    return None


def download_schema(destination: str = "cs2_schema.json", language: str = "en") -> str:
    url = f"https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/{language}/all.json"

    print(f"Downloading CS2 schema from {url}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())

    abs_path = str(Path(destination).absolute())
    with open(abs_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    save_schema_path(abs_path)
    print(f"Schema saved to {abs_path}")
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
