__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "08.04.2026"
__email__ = "m@hler.eu"
__status__ = "Development"


import json
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
        # Build crate-to-collection mapping
        crate_to_col = {}
        for key, item in self._data.items():
            if key.startswith("collection-") and "crates" in item and isinstance(item["crates"], list):
                col_name = item.get("name")
                if col_name:
                    for crate in item["crates"]:
                        crate_id = crate.get("id")
                        if crate_id:
                            crate_to_col[crate_id] = col_name

        # Second pass: Associate all nested items with their parent collection or container name.
        nested_to_col = {}
        for key, item in self._data.items():
            # Possible child lists in the schema: contains, contains_rare, loot_list
            children_keys = ["contains", "contains_rare", "loot_list"]
            all_children = []
            for ck in children_keys:
                 c_list = item.get(ck)
                 if c_list and isinstance(c_list, list):
                      all_children.extend(c_list)

            if all_children:
                # Priority: Collection Name (inherited) > Own Name
                col_name = item.get("name")
                if key.startswith("crate-") and key in crate_to_col:
                     col_name = crate_to_col[key]

                if col_name:
                    for child in all_children:
                        child_id = child.get("id")
                        if child_id:
                             # Don't overwrite if a primary collection- level mapping was already found
                             if not (child_id in nested_to_col and key.startswith("crate-")):
                                  nested_to_col[child_id] = col_name

        self._nested_to_col = nested_to_col

        # Final pass: Process all items using the built mapping
        for key, item in self._data.items():
            self._process_item(key, item)

    def _process_item(self, key: str, item: dict[str, Any], parent_collection: Optional[str] = None):
        weapon_def = item.get("weapon", {})
        weapon_id = weapon_def.get("weapon_id")
        def_index = item.get("def_index")

        # Associate item with its collection based on its ID or parent context
        col_name = parent_collection
        if not col_name:
            # Check if this key matches a nested ID (remove wear-level suffix for skins e.g. '_0')
            check_key = key
            wear_tier = None
            if "_" in key and key.startswith("skin-"):
                parts = key.rsplit("_", 1)
                check_key = parts[0]
                # Detect wear tier from suffix (_0 to _4)
                if parts[1].isdigit():
                    wear_tier = int(parts[1])

            col_name = self._nested_to_col.get(check_key)

            # Fallback to direct 'collections' list if present (common for Agents)
            if not col_name:
                cols = item.get("collections", [])
                if cols and isinstance(cols, list) and len(cols) > 0:
                    col_name = cols[0].get("name")

        if key.startswith("agent-") and def_index is not None:
            d_idx = int(def_index)
            agent_data = {
                "name": item.get("name"),
                "image": item.get("image", "")
            }
            if col_name:
                agent_data["collection"] = col_name

            if d_idx in self._agents:
                self._agents[d_idx].update(agent_data)
            else:
                self._agents[d_idx] = agent_data

        elif (key.startswith("sticker_slab-") or key.startswith("patch-")) and def_index is not None:
            d_idx = int(def_index)
            original = item.get("original", {})
            slab_data = {
                "name": item.get("name", "Unknown"),
                "codename": original.get("name", "Unknown"),
                "material": original.get("image_inventory", "Unknown"),
                "image": item.get("image", "")
            }
            if col_name:
                slab_data["collection"] = col_name

            if d_idx in self._sticker_slabs:
                self._sticker_slabs[d_idx].update(slab_data)
            else:
                self._sticker_slabs[d_idx] = slab_data

        elif key.startswith("sticker-") and def_index is not None:
            d_idx = int(def_index)
            original = item.get("original", {})
            codename = original.get("name") or original.get("loc_name") or "Unknown"
            if codename.startswith("#"):
                codename = codename[1:]

            sticker_data = {
                "name": item.get("name", "Unknown"),
                "codename": codename,
                "material": original.get("image_inventory", "Unknown"),
                "image": item.get("image", "")
            }
            if col_name:
                sticker_data["collection"] = col_name

            if d_idx in self._stickers:
                self._stickers[d_idx].update(sticker_data)
            else:
                self._stickers[d_idx] = sticker_data

        elif (key.startswith("charm-") or key.startswith("keychain-")) and def_index is not None:
            d_idx = int(def_index)
            original = item.get("original", {})
            codename = original.get("name") or original.get("loc_name") or "Unknown"
            if codename.startswith("#"):
                codename = codename[1:]

            # Clean up the keychain_ prefix if it exists to get better codenames
            if codename.startswith("keychain_"):
                codename = codename[len("keychain_"):]

            charm_data = {
                "name": item.get("name", "Unknown"),
                "codename": codename,
                "material": original.get("image_inventory", "Unknown"),
                "image": item.get("image", "")
            }
            if col_name:
                charm_data["collection"] = col_name

            if d_idx in self._charms:
                self._charms[d_idx].update(charm_data)
            else:
                self._charms[d_idx] = charm_data

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
                    s_key = (w_id, p_id)
                    if s_key not in self._skins:
                        self._skins[s_key] = {
                            "name": skin_name,
                            "images": {}, # Wear-specific images (0-4)
                            "min_float": item.get("min_float"),
                            "max_float": item.get("max_float")
                        }

                    # Update base info
                    self._skins[s_key]["name"] = skin_name
                    if item.get("min_float") is not None:
                        self._skins[s_key]["min_float"] = item.get("min_float")
                    if item.get("max_float") is not None:
                        self._skins[s_key]["max_float"] = item.get("max_float")
                    if col_name:
                        self._skins[s_key]["collection"] = col_name

                    # Store image variant if wear_tier detected
                    img = item.get("image", "")
                    if img:
                        if wear_tier is not None:
                            self._skins[s_key]["images"][wear_tier] = img
                        else:
                            # Fallback if no tier suffix found
                            self._skins[s_key]["image_default"] = img

        # Traverse nested children for structural resolution
        children_keys = ["contains", "contains_rare", "loot_list"]
        for ck in children_keys:
             c_list = item.get(ck)
             if c_list and isinstance(c_list, list):
                  for child in c_list:
                       child_id = child.get("id", "")
                       if child_id:
                            self._process_item(child_id, child, parent_collection=col_name)

    def get_weapon_name(self, weapon_id: int) -> str:
        return self._weapons.get(weapon_id, "Unknown")

    def get_agent_name(self, defindex: int) -> str:
        info = self._agents.get(defindex)
        if isinstance(info, dict):
            return info.get("name", "Unknown")
        return "Unknown"

    def get_agent_info(self, defindex: int) -> Optional[dict[str, Any]]:
        return self._agents.get(defindex)

    def get_wear_tier(self, float_val: float) -> int:
        """Map a float value (0.0 - 1.0) to a wear tier (0-4)."""
        if float_val < 0.07: return 0 # Factory New
        if float_val < 0.15: return 1 # Minimal Wear
        if float_val < 0.38: return 2 # Field-Tested
        if float_val < 0.45: return 3 # Well-Worn
        return 4 # Battle-Scarred

    def get_skin_info(self, weapon_id: int, paint_index: int, float_val: Optional[float] = None) -> Optional[dict[str, Any]]:
        skin = self._skins.get((weapon_id, paint_index))
        if not skin:
            return None

        # Clone to avoid modifying the cached entry
        res = dict(skin)

        # Select image based on wear_tier
        images = skin.get("images", {})
        if float_val is not None and images:
            tier = self.get_wear_tier(float_val)
            # Find the closest tier if exact one missing
            if tier in images:
                res["image"] = images[tier]
            else:
                # Fallback to default or closest tier
                available = sorted(images.keys())
                if available:
                    # Pick default if exists, else first available
                    res["image"] = skin.get("image_default", images[available[0]])
        else:
            res["image"] = skin.get("image_default", "")
            # If no default, try Factory New (tier 0) as fallback
            if not res["image"] and 0 in images:
                res["image"] = images[0]

        return res

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


def download_schema(path: str = "cs2_schema.json") -> str:
    url = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/all.json"
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())

    abs_path = str(Path(path).absolute())
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
