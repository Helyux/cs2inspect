# cs2inspect Output Model

This document defines the structure of the result dictionary returned by the `parse()` function. The output varies depending on the item type and whether enrichment (schema-based lookup) is enabled.

---

## 1. Standard (Raw) Model
The fields extracted during a standard parse depend heavily on whether the link is **Masked** (Modern CS2) or **Unmasked** (Legacy).

### 1.1 Masked (Modern) Links
These links contain a binary protobuf payload with full item properties.

| Field | Type | Source | Status | Description |
| :--- | :--- | :--- | :--- | :--- |
| `defindex` | `int` | Standard | Mandatory | Item definition index (from proto). |
| `paintindex` | `int` | Standard | Mandatory* | Appearance/Paint ID (Defaulted to 0 if missing). |
| `paintseed` | `int` | Standard | Mandatory* | Random seed for pattern generation (Defaulted to 0). |
| `paintwear` | `int` | Standard | Mandatory* | Raw IEEE float (uint32) bytes of wear (Defaulted to 0). |
| `floatvalue` | `float` | Standard | Derived | Human-readable float wear (computed from `paintwear`). |
| `rarity` | `int` | Standard | Mandatory | Numerical rarity ID. |
| `quality` | `int` | Standard | Mandatory | Numerical quality ID (e.g., 9 for StatTrak). |
| `inventory` | `int` | Standard | Mandatory | Bitmask for inventory state/pos. |
| `origin` | `int` | Standard | Mandatory | Acquisition source ID. |
| `itemid` | `int` | Standard | Mandatory | Unique uint64 Item ID. |
| `accountid` | `int` | Standard | Optional | Owner account ID. |
| `customname` | `str` | Standard | Optional | User-applied name tag. |
| `musicindex` | `int` | Standard | Optional | ID for Music Kits. |
| `killeatervalue` | `int` | Standard | Optional | StatTrak value (kills/points). |
| `killeaterscoretype` | `int` | Standard | Optional | Score tracking type ID (usually 0). |
| `questid` | `int` | Standard | Optional | Associated Quest/Operation ID. |
| `dropreason` | `int` | Standard | Optional | How the drop was triggered. |
| `entindex` | `int` | Standard | Optional | Legacy entity index. |
| `petindex` | `int` | Standard | Optional | Legacy pet index. |
| `style` | `int` | Standard | Optional | Selected item style index. |
| `upgrade_level` | `int` | Standard | Optional | Badge or item level. |
| `stickers` | `list` | Standard | Optional | List of `Sticker` messages (mapped to [Attachment Objects](#3-attachment-objects)). |
| `keychains` | `list` | Standard | Optional | List of `Sticker` messages (mapped to [Attachment Objects](#3-attachment-objects)). |
| `variations` | `list` | Standard | Optional | List of variation `Sticker` messages. |

### 1.2 Unmasked (Legacy) Links
Legacy links (containing `S` or `M` prefixes) do **not** carry any property data. They are simple pointers that require external GC resolution.

| Field | Type | Source | Status | Description |
| :--- | :--- | :--- | :--- | :--- |
| `owner_id` | `str` | Standard | Optional | SteamID64 (Only for `S` links). |
| `market_id` | `str` | Standard | Optional | Market Listing ID (Only for `M` links). |
| `asset_id` | `str` | Standard | Mandatory | The Asset ID of the item. |
| `class_id` | `str` | Standard | Mandatory | The Inspect ID / D-Parameter. |

---

## 2. Enriched Model
These fields are added when a `schema` is provided (or `enrich=True` is used) and the link contains a property payload.

> [!WARNING]
> Enrichment only works for **Masked** links. **Unmasked** links lack the technical properties (like `defindex`) required to perform metadata lookups. For legacy links, the result will only contain the raw IDs listed in Section 1.2.

> [!NOTE]
> Following the v0.5.0 update, enriched fields that are not applicable to the item (return `None` or `""`) are omitted from the dictionary to keep the output clean.

| Field | Type | Source | Status | Description |
| :--- | :--- | :--- | :--- | :--- |
| `full_item_name` | `str` | Enriched | Mandatory | Formatted name (e.g., `StatTrak™ AK-47 | Slate (Minimal Wear)`). |
| `weapon_type` | `str` | Enriched | Optional | The item category (e.g., `AK-47`, `Agent`). |
| `item_name` | `str` | Enriched | Optional | The specific skin or kit name (e.g., `Dragon Lore`). |
| `rarity_name` | `str` | Enriched | Mandatory | Human-readable rarity (e.g., `Covert`). |
| `origin_name` | `str` | Enriched | Mandatory | Human-readable origin (e.g., `Found in Crate`). |
| `quality_name` | `str` | Enriched | Mandatory | Human-readable quality (e.g., `StatTrak™`). |
| `imageurl` | `str` | Enriched | Optional | Persistent URL to the item Icon. |
| `collection_name`| `str` | Enriched | Optional | The collection the item belongs to. |
| `wear_name` | `str` | Enriched | Optional | Skin wear category (e.g., `Factory New`). |
| `min` / `max` | `float` | Enriched | Optional | The supported float range for the skin. |

---

## 3. Attachment Objects
Stickers and Keychains (Charms) use a shared sub-structure.

| Field | Type | Source | Status | Description |
| :--- | :--- | :--- | :--- | :--- |
| `slot` | `int` | Standard | Mandatory | Slot index (0-4 for stickers, 0 for charms). |
| `sticker_id` | `int` | Standard | Mandatory | The unique definition ID of the attachment. |
| `wear` | `float` | Standard | Mandatory | Standard float wear (0.0 to 1.0). |
| `pattern` | `int` | Standard | Optional* | Unique pattern ID (Defaulted to `0` for regular charms during enrichment). |
| `highlight_reel` | `int` | Standard | Optional | Event ID (From `highlight_reel` proto field). |
| `tint_id` | `int` | Standard | Optional | Color ID (From `tint_id` proto field). |
| `rotation` | `float` | Standard | Optional | Custom rotation (Proto field). |
| `scale` | `float` | Standard | Optional | Custom scale (Proto field). |
| `offset_x` / `y` / `z`| `float` | Standard | Optional | Coordinate offsets (Proto fields). |
| `wrapped_sticker`| `int` | Standard | Optional | Original ID for Slabs (Proto field). |
| `name` | `str` | Enriched | Mandatory | Full localized name from schema. |
| `codename` | `str` | Enriched | Mandatory | Internal code name from schema. |
| `material` | `str` | Enriched | Mandatory | Internal material path from schema. |
| `imageurl` | `str` | Enriched | Optional | Icon URL from schema. |
| `collection_name`| `str` | Enriched | Optional | Collection name from schema. |
