# Example Usage

This guide provides comprehensive examples for creating, parsing, and enriching CS2 inspect links using `cs2inspect`.

---

## 1. Creating Links

### Simple 'Unmasked' Links
Build an inspect link from known IDs (Account, Asset, and Class/D). Note: These links do not contain property data like floats or paint seeds.

```python
import cs2inspect

link_data = {
    'asset_id': '38350177019',
    'class_id': '9385506221951591925',
    'owner_id': '76561198066322090'
}
link_str = cs2inspect.link(link_data)
print(link_str) 
# steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198066322090A38350177019D9385506221951591925
```

### Complex 'Masked' Links
Use the `Builder` to create binary-packed links containing full technical properties.

```python
import cs2inspect

proto_base = cs2inspect.Builder(
    defindex=7,
    paintindex=941,
    paintseed=2,
    paintwear=0.22540508,
    rarity=5,
)

# Add attachments (Stickers and Charms)
proto_base.stickers.append({'slot': 2, 'sticker_id': 7203, 'wear': 0})
proto_base.keychains.append({
    'slot': 0,
    'sticker_id': 36,
    'offset_x': 4.515,
    'offset_y': 0.591,
    'offset_z': 8.906
})

# Build the protobuf and generate the link
try:
    protobuf = proto_base.build()
    link_str = cs2inspect.link(protobuf)
    print(link_str)
except Exception as e:
    print(f"Build failed: {e}")

# Get a command for the in-game console
console_str = cs2inspect.link_console(protobuf)
print(console_str)

# Generate a !gen code
gen_str = cs2inspect.gen(protobuf, prefix="!g")
print(gen_str) # !g 7 941 2 0.22540508 0 0 0 0 7203 0 0 0 0 0 36 0
```

---

## 2. Parsing Links

Supports both legacy unmasked links and modern masked links. The `parse()` function returns a dictionary following the [Output Model](output_model.md).

```python
import cs2inspect

# 1. Parse a traditional unmasked link (S A D format)
unmasked_link = "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198066322090A38350177019D9385506221951591925"
ids = cs2inspect.parse(unmasked_link)
print(ids['owner_id'])    # 76561198066322090
print(ids['asset_id'])    # 38350177019

# 2. Parse a new masked CS2 link (contains full item properties)
masked_link = "steam://run/730//+csgo_econ_action_preview%206A7AC7C6BEDED06B72704ACE6F426F5A635296868780692AAC6C226A3A6A02E9EAEAEA661A625E7EE646"
data = cs2inspect.parse(masked_link)
print(data['defindex'])    # 26 (PP-Bizon)
print(data['floatvalue'])  # 0.05357979

# 3. Get the raw protobuf data block (Inverse of cs2inspect.link())
proto = cs2inspect.unlink(masked_link)
print(proto.paintseed)  # 838
```

---

## 3. Smart Enrichment

Resolve numeric IDs to human-readable names using an external metadata schema.

```python
import cs2inspect
import json

# One-time setup: download the latest item/skin database
# The library automatically remembers this path locally across restarts!
cs2inspect.download_schema(path="my_schema.json") # Default is 'cs2schema.json'

# Parse with enrichment enabled
link = "steam://run/730//+csgo_econ_action_preview%200D1DC5E9CAE5BB0C150A2D860525093D043599ADABE20E4DBB0E450D5DD0076F19050C1DD43510C0C1013230710D96B0488D33ABB66F19050D1DD0351030071A3230BD25CAB0480D99D8376F19050E1DE03510C0C1013230D0F0A73348ED1813316F19050E1DE4351088E61C3230FBB9443348F58BAA306F19050F1D9C341088E61C3230014B1A33484DE99EB6650C7D05AF0C1A050D1D2230EC64104C4828251932404AB2884D5D8E880CEBE9FCE9"
info = cs2inspect.parse(link, enrich=True)

print(json.dumps(info, indent=4, ensure_ascii=False))
```

<details>
<summary>Click to view full JSON output</summary>

```json
{
    "itemid": 49074532936,
    "defindex": 7,
    "paintindex": 1035,
    "rarity": 4,
    "quality": 9,
    "paintwear": 1038716948,
    "paintseed": 438,
    "killeaterscoretype": 0,
    "killeatervalue": 1373,
    "inventory": 1,
    "origin": 8,
    "stickers": [
        {
            "slot": 1,
            "stickerId": 7257,
            "codename": "cph2024_team_navi_gold",
            "name": "Sticker | Natus Vincere (Gold) | Copenhagen 2024",
            "imageurl": "...",
            "collection_name": "Copenhagen 2024 Legends Sticker Capsule",
            "wear": 0.55
        }
        ...
    ],
    "floatvalue": 0.11404433,
    "wear_name": "Minimal Wear",
    "rarity_name": "Restricted",
    "weapon_type": "AK-47",
    "item_name": "Slate",
    "collection_name": "The Snakebite Collection",
    "full_item_name": "StatTrak™ AK-47 | Slate (Minimal Wear)"
}
```
</details>
