# cs2inspect Output Model

This document defines the structure of the result dictionary returned by the `parse()` function. The output varies depending on the item type and whether enrichment (schema-based lookup) is enabled.

---

## 1. Standard (Raw) Model
The fields extracted during a standard parse depend heavily on whether the link is **Masked** (Modern CS2) or **Unmasked** (Legacy).

### 1.1 Masked (Modern) Links
These links contain a binary protobuf payload with full item properties.

| Field | Type | Description | Status |
| :--- | :--- | :--- | :--- |
| `defindex` | `int` | Weapon or Item definition ID. | Mandatory |
| `paintindex` | `int` | Pattern/Paint ID (e.g., 344 for Dragon Lore). | Mandatory (Default: 0) |
| `paintseed` | `int` | Random seed for pattern placement (0-1000). | Mandatory (Default: 0) |
| `paintwear` | `int` | Raw integer representation of item wear. | Mandatory (Default: 0) |
| `floatvalue` | `float` | Human-readable wear value (usually 0.0 to 1.0). | Mandatory (Derived) |
| `rarity` | `int` | Internal rarity ID. | Mandatory (Default: 0) |
| `quality` | `int` | Internal quality ID (e.g., 9 for StatTrak). | Mandatory (Default: 0) |
| `inventory` | `int` | Internal inventory position/mask. | Mandatory (Default: 0) |
| `origin` | `int` | How the item was obtained (e.g., 8 for Crate). | Mandatory (Default: 0) |
| `itemid` | `int` | Unique Item ID. | Mandatory (Default: 0) |
| `accountid` | `int` | Account ID of the owner. | Optional |
| `customname` | `str` | Custom name tag applied to the item. | Optional |
| `musicindex` | `int` | Track ID for Music Kits. | Optional |
| `killeatervalue` | `int` | Total kills recorded (for StatTrak items). | Optional |
| `killeaterscoretype` | `int` | Type of score tracked (usually 0 for Kills).| Optional |
| `questid` | `int` | ID associated with an active quest or operation. | Optional |
| `dropreason` | `int` | Internal ID for how the item was obtained. | Optional |
| `entindex` | `int` | Entity index (legacy). | Optional |
| `petindex` | `int` | Pet index (legacy). | Optional |
| `style` | `int` | Selected style index for multi-style items. | Optional |
| `upgrade_level` | `int` | Badge or item upgrade level. | Optional |
| `stickers` | `list` | A list of [Attachment Objects](#3-attachment-objects). | Optional |
| `keychains` | `list` | A list of [Attachment Objects](#3-attachment-objects). | Optional |
| `variations` | `list` | A list of item variation dictionaries. | Optional |

### 1.2 Unmasked (Legacy) Links
Legacy links (containing `S` or `M` prefixes) do **not** carry any property data. They are simple pointers that require external GC resolution.

| Field | Type | Description | Status |
| :--- | :--- | :--- | :--- |
| `owner_id` | `str` | SteamID64 of the owner (Only for `S` links). | Optional |
| `market_id` | `str` | Market Listing ID (Only for `M` links). | Optional |
| `asset_id` | `str` | The Asset ID of the item. | Mandatory |
| `class_id` | `str` | The Inspect ID / D-Parameter. | Mandatory |

---

## 2. Enriched Model
These fields are added when a `schema` is provided (or `enrich=True` is used) and the link contains a property payload.

> [!WARNING]
> Enrichment only works for **Masked** links. **Unmasked** links lack the technical properties (like `defindex`) required to perform metadata lookups. For legacy links, the result will only contain the raw IDs listed in Section 1.2.

> [!NOTE]
> Following the v0.5.0 update, enriched fields that are not applicable to the item (return `None` or `""`) are omitted from the dictionary to keep the output clean.

| Field | Type | Description | Status |
| :--- | :--- | :--- | :--- |
| `full_item_name` | `str` | Complete formatted name (e.g., `StatTrak™ AK-47 | Slate (Minimal Wear)`). | Mandatory |
| `weapon_type` | `str` | The item category or weapon base (e.g., `AK-47`, `Agent`, `Music Kit`). | Optional (Omitted if N/A) |
| `item_name` | `str` | The specific skin or kit name (e.g., `Dragon Lore`). | Optional (Omitted if N/A) |
| `rarity_name` | `str` | Human-readable rarity (e.g., `Covert`, `Master`). | Mandatory |
| `origin_name` | `str` | Human-readable origin (e.g., `Found in Crate`). | Mandatory |
| `quality_name` | `str` | Human-readable quality (e.g., `StatTrak™`, `Souvenir`). | Mandatory |
| `imageurl` | `str` | Persistent URL to the item Icon. | Optional (Omitted if N/A) |
| `collection_name`| `str` | The collection the item belongs to. | Optional (Omitted if N/A) |
| `wear_name` | `str` | Skin wear category (e.g., `Factory New`). | Optional (Omitted if N/A) |
| `min` / `max` | `float` | The minimum/maximum possible float range for the skin. | Optional (Omitted if N/A) |

---

## 3. Attachment Objects
Stickers and Keychains (Charms) use a shared sub-structure. Fields are optional and depend on whether the links are enriched.

| Field | Type | Description |
| :--- | :--- | :--- |
| `slot` | `int` | The physical slot index (0-4 for stickers, 0 for charms). |
| `stickerId` | `int` | The definition ID of the attachment. |
| `name` | `str` | Full name of the sticker/charm (Enriched only). |
| `codename` | `str` | Internal code name (Enriched only). |
| `imageurl` | `str` | Icon URL (Enriched only). |
| `collection_name`| `str` | Originating capsule or collection (Enriched only). |
| `wear` | `float` | Wear/Scrape value of the sticker (0.0 to 1.0). |
| `rotation` | `float` | Custom rotation applied (Stickers 2.0). |
| `offset_x` / `y` / `z`| `float` | Precise coordinate offsets (Stickers 2.0 and Charms). |
| `highlight_reel` | `int` | Event ID for Souvenir Highlight Charms. |
