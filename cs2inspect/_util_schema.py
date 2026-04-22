import json
import urllib.request
from typing import Any

from ._util_base import HIGHLIGHTS_URL, SCHEMA_URL

# Keys to KEEP in each item to minimize footprint while preserving enrichment capability.
SCHEMA_PRUNE_KEYS = {
    "id",
    "def_index",
    "name",
    "image",
    "thumbnail",
    "phase",
    "weapon",
    "paint_index",
    "pattern",
    "min_float",
    "max_float",
    "original",
    "collections",
    "crates",
    "contains",
    "contains_rare",
    "loot_list",
    "market_hash_name",
}

# Structural keys that only need the 'id' for internal linking (collection resolution).
# We strip everything else from objects within these lists to save space.
STRUCTURAL_LISTS = {"crates", "contains", "contains_rare", "loot_list"}


def prune_item(item: Any) -> Any:
    """
    Strip unnecessary metadata from a schema item entry.

    :param item: The raw dictionary entry for an item.
    :type item: Any

    :return: An optimized dictionary with only essential keys.
    :rtype: Any
    """

    if not isinstance(item, dict):
        return item

    # Prune top level
    pruned = {k: v for k, v in item.items() if k in SCHEMA_PRUNE_KEYS}

    # Deep prune structural lists to only keep 'id'
    for k in STRUCTURAL_LISTS:
        if k in pruned and isinstance(pruned[k], list):
            new_list = []
            for child in pruned[k]:
                if isinstance(child, dict) and "id" in child:
                    new_list.append({"id": child["id"]})
                else:
                    new_list.append(child)
            pruned[k] = new_list

    # Specifically prune 'collections' to keep only id and name (strip image)
    if "collections" in pruned and isinstance(pruned["collections"], list):
        new_cols = []
        for col in pruned["collections"]:
            if isinstance(col, dict):
                new_cols.append({k: v for k, v in col.items() if k in {"id", "name"}})
            else:
                new_cols.append(col)
        pruned["collections"] = new_cols

    return pruned


def prune_and_bundle(raw_schema: dict[str, Any], highlights_data: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Consolidate the raw schema and external highlights into a single optimized blob.

    Highlights are bundled separately because they are not included in the 'all.json' schema data,
    but are required for Souvenir Highlight resolution.

    :param raw_schema: The external all schema file.
    :type raw_schema: dict[str, Any]
    :param highlights_data: The external highlight schema file.
    :type highlights_data: list[dict[str, Any]]

    :return: A consolidated dictionary structured as {'items': ..., 'highlights': ...}.
    :rtype: dict[str, Any]
    """

    pruned_items = {}
    for key, item in raw_schema.items():
        pruned_items[key] = prune_item(item)

    return {"items": pruned_items, "highlights": highlights_data}


def fetch_and_update_schema(output_path: str, timeout: float = 60.0) -> bool:
    """
    Fetch the latest remote data, optimize it, and save to disk.

    :param output_path: Where to save the resulting .json file.
    :type output_path: str
    :param timeout: Network timeout in seconds.
    :type timeout: float

    :return: True if successful, False otherwise.
    :rtype: bool
    """

    try:
        headers = {"User-Agent": "cs2inspect"}

        # 1. Download Schema
        req_s = urllib.request.Request(SCHEMA_URL, headers=headers)
        with urllib.request.urlopen(req_s, timeout=timeout) as resp:
            raw_schema = json.loads(resp.read().decode("utf-8"))

        # 2. Download Highlights
        req_h = urllib.request.Request(HIGHLIGHTS_URL, headers=headers)
        with urllib.request.urlopen(req_h, timeout=timeout) as resp:
            highlights = json.loads(resp.read().decode("utf-8"))

        # 3. Optimize
        bundled = prune_and_bundle(raw_schema, highlights)

        # 4. Save
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(bundled, f, separators=(",", ":"))

        return True
    except Exception as e:
        # We don't want to crash the main library if update fails
        import sys

        print(f"cs2inspect: Failed to update schema: {e}", file=sys.stderr)
        return False
