# cs2inspect Output Model

This document defines the structure of the result dictionary returned by the `parse()` function. The output varies depending on the item type and whether enrichment (schema-based lookup) is enabled.

---

## 1. Standard (Raw) Model
The fields extracted during a standard parse depend heavily on whether the link is **Masked** (Modern CS2) or **Unmasked** (Legacy).

### 1.1 Masked (Modern) Links
These links contain a binary protobuf payload with full item properties.

| Field | Type | Source | Status | Description |
| :--- | :--- | :--- | :--- | :--- |
| `defindex` | `int` | Standard | Mandatory | Weapon or Item definition ID. |
| `paintindex` | `int` | Standard | Mandatory* | Pattern/Paint ID (Defaulted to 0 if missing). |
| `paintseed` | `int` | Standard | Mandatory* | Random seed for pattern placement (Defaulted to 0). |
| `paintwear` | `int` | Standard | Mandatory* | Raw integer representation of item wear (Defaulted to 0). |
| `floatvalue` | `float` | Standard | Derived | Human-readable wear value (0.0 to 1.0). |
| `rarity` | `int` | Standard | Mandatory | Internal rarity ID. |
| `quality` | `int` | Standard | Mandatory | Internal quality ID (e.g., 9 for StatTrak). |
| `inventory` | `int` | Standard | Mandatory | Internal inventory position/mask. |
| `origin` | `int` | Standard | Mandatory | How the item was obtained (e.g., 8 for Crate). |
| `itemid` | `int` | Standard | Mandatory | Unique Item ID. |
| `accountid` | `int` | Standard | Optional | Account ID of the owner. |
| `customname` | `str` | Standard | Optional | Custom name tag applied to the item. |
| `musicindex` | `int` | Standard | Optional | Track ID for Music Kits. |
| `killeatervalue` | `int` | Standard | Optional | Total kills recorded (for StatTrak items). |
| `killeaterscoretype` | `int` | Standard | Optional | Type of score tracked (usually 0 for Kills).|
| `questid` | `int` | Standard | Optional | ID associated with an active quest or operation. |
| `dropreason` | `int` | Standard | Optional | Internal ID for how the item was obtained. |
| `entindex` | `int` | Standard | Optional | Entity index (legacy). |
| `petindex` | `int` | Standard | Optional | Pet index (legacy). |
| `style` | `int` | Standard | Optional | Selected style index for multi-style items. |
| `upgrade_level` | `int` | Standard | Optional | Badge or item upgrade level. |
| `stickers` | `list` | Standard | Optional | A list of [Attachment Objects](#3-attachment-objects). |
| `keychains` | `list` | Standard | Optional | A list of [Attachment Objects](#3-attachment-objects). |
| `variations` | `list` | Standard | Optional | A list of item variation dictionaries. |

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
| `slot` | `int` | Standard | Mandatory | The physical slot index (0-4 for stickers, 0 for charms). |
| `stickerId` | `int` | Standard | Mandatory | The definition ID of the attachment (Sticker or Charm). |
| `wear` | `float` | Standard | Mandatory | Wear/Scrape value (0.0 to 1.0). Defaults to 0.0. |
| `pattern` | `int` | Standard | Optional* | Unique pattern ID (Defaulted to `0` for regular charms during enrichment). |
| `rotation` | `float` | Standard | Optional | Custom rotation value. |
| `scale` | `float` | Standard | Optional | Custom scale value. |
| `offset_x` / `y` / `z`| `float` | Standard | Optional | Precise coordinate offsets. |
| `highlight_reel` | `int` | Standard | Optional | Event ID (Highlight Charms only). |
| `tint_id` | `int` | Standard | Optional | Color ID (Graffiti only). |
| `wrapped_sticker`| `int` | Standard | Optional | Original sticker ID (Sticker Slabs only). |
| `name` | `str` | Enriched | Mandatory | Full localized name of the attachment. |
| `codename` | `str` | Enriched | Mandatory | Internal developer code name. |
| `material` | `str` | Enriched | Mandatory | Internal material path. |
| `imageurl` | `str` | Enriched | Optional | Persistent Icon URL for the attachment. |
| `collection_name`| `str` | Enriched | Optional | Originating capsule or collection. |
