# Example Usage

This document provides comprehensive examples for creating, parsing, and enriching CS2 inspect links using `cs2inspect`.

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

## 3. Schema Enrichment

Resolve numeric IDs to human-readable names using an external metadata schema. Enrichment is **disabled by default** to keep parsing fast and lightweight; you must either set `enrich=True` or provide a valid `schema` instance/path.

### Automatic Schema Loading
If you have a `cs2schema.json` file in your current directory, you can simply enable enrichment with the `enrich` flag.

```python
import cs2inspect
import json

link = "steam://run/730//+csgo_econ_action_preview%200D1DC5E9CAE5BB0C150A2D860525093D043599ADABE20E4DBB0E450D5DD0076F19050C1DD43510C0C1013230710D96B0488D33ABB66F19050D1DD0351030071A3230BD25CAB0480D99D8376F19050E1DE03510C0C1013230D0F0A73348ED1813316F19050E1DE4351088E61C3230FBB9443348F58BAA306F19050F1D9C341088E61C3230014B1A33484DE99EB6650C7D05AF0C1A050D1D2230EC64104C4828251932404AB2884D5D8E880CEBE9FCE9"

# Download the latest item/skin schema (one-time setup)
cs2inspect.download_schema()

# Parse with enrichment enabled (searches for 'cs2schema.json' by default)
info = cs2inspect.parse(link, enrich=True)
```

### Custom Schema Paths
You can also pass a path directly to the `schema` parameter. This **automatically enables enrichment**, even if `enrich=True` is omitted.

```python
# Providing a path automatically enables enrichment
info = cs2inspect.parse(link, schema="data/my_custom_schema.json")
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
            "sticker_id": 7257,
            "codename": "cph2024_team_navi_gold",
            "material": "econ/stickers/cph2024/navi_gold",
            "name": "Sticker | Natus Vincere (Gold) | Copenhagen 2024",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMmxPSnHtwI6-obi42bgThH10JWwqHQDu6f4PPU8IfLFDWLAlOtysuQwSiyywB8hsT6BzYz9c3LDOwY-Sswn4fCOG2o",
            "collection_name": "Copenhagen 2024 Legends Sticker Capsule",
            "wear": 0.550000011920929,
            "offset_x": -0.07568451762199402,
            "offset_y": -0.005073368549346924
        },
        {
            "slot": 0,
            "sticker_id": 7261,
            "codename": "cph2024_team_vp_gold",
            "material": "econ/stickers/cph2024/vp_gold",
            "name": "Sticker | Virtus.pro (Gold) | Copenhagen 2024",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMmxPSnHtwI64pfL7VbrRVPwyJflqnNfv6StOf05cKmXV2SWxLdytrM7GnHqkU8l52nUmImqd3mWcEZ-XUXT9D_W",
            "collection_name": "Copenhagen 2024 Legends Sticker Capsule",
            "wear": 0.5899999737739563,
            "offset_x": -0.09724557399749756,
            "offset_y": 0.001629471778869629
        },
        {
            "slot": 3,
            "sticker_id": 7277,
            "codename": "cph2024_team_vita_gold",
            "material": "econ/stickers/cph2024/vita_gold",
            "name": "Sticker | Vitality (Gold) | Copenhagen 2024",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMmxPSnHtwI64o7g62bgThH10M7ipHZdvKT9MPQ6JvWQDz-Sl-pytLQ6GC_gzEtw62zVyY39eH2WbwA-SswneFne1lk",
            "collection_name": "Copenhagen 2024 Legends Sticker Capsule",
            "wear": 0.550000011920929,
            "offset_x": 0.33396807312965393,
            "offset_y": 0.009648770093917847
        },
        {
            "slot": 3,
            "sticker_id": 7273,
            "codename": "cph2024_team_spir_gold",
            "material": "econ/stickers/cph2024/spir_gold",
            "name": "Sticker | Team Spirit (Gold) | Copenhagen 2024",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMmxPSnHtwI655f9-GbgThH10MGw-HIKv6T6baFucfPFC2KUkO905uRvGnrllkp-5TjQzo6qJH6XPFM-SswnKK8h7Zw",
            "collection_name": "Copenhagen 2024 Legends Sticker Capsule",
            "wear": 0.5699999928474426,
            "offset_x": 0.1969793736934662,
            "offset_y": 0.08180040121078491
        },
        {
            "slot": 2,
            "sticker_id": 7313,
            "codename": "cph2024_team_gl_gold",
            "material": "econ/stickers/cph2024/gl_gold",
            "name": "Sticker | GamerLegion (Gold) | Copenhagen 2024",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMmxPSnHtwI684vL7VbrRVP1x5K1rHoOu6P-PPY6JfHKXTLEmOovs-M4S3HjkElz5DuBydmsJXuVcEZ-XYJJFe58",
            "collection_name": "Copenhagen 2024 Challengers Sticker Capsule",
            "wear": 0.5699999928474426,
            "offset_x": 0.14772814512252808,
            "offset_y": -0.004513293504714966
        }
    ],
    "keychains": [
        {
            "slot": 0,
            "sticker_id": 47,
            "codename": "kc_missinglink_lilhothead",
            "material": "econ/keychains/missinglink_community_01/kc_missinglink_lilhothead",
            "name": "Charm | Magmatude",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGI6zwki4Uf_a0IWsPGiE7Fhy-I764WbkThD8i5jp6Ttkv6PhY6dSLfmAHW6exuJ_vupWQyC_nRIzuziEnsGgJymSZwd0CZpyQu5buxO9wNbmPrzm5wCLg95Fmyz_3y1Nuydq4OZXT-N7raqdv_up",
            "collection_name": "Missing Link Community Charm Collection",
            "wear": 0.0,
            "offset_x": 9.838349342346191,
            "offset_y": 0.5787375569343567,
            "offset_z": 4.179599285125732,
            "pattern": 17027
        }
    ],
    "floatvalue": 0.11404433846473694,
    "wear_name": "Minimal Wear",
    "rarity_name": "Restricted",
    "origin_name": "Found in Crate",
    "quality_name": "StatTrak™",
    "weapon_type": "AK-47",
    "item_name": "Slate",
    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3UqlXOLrxM-vMGmW8VNxu5Dx60noTyLwlcK3wiVI0POlPPNSMOKcCGKD0ud5vuBlcCW6khUz_W3Sytb4cCqTOFUpWJtzTOUD5hPsw9a0Yrnrs1SK3ooXzy6shilM5311o7FVYrIufmI",
    "min": 0,
    "max": 1,
    "collection_name": "The Snakebite Collection",
    "full_item_name": "StatTrak™ AK-47 | Slate (Minimal Wear)"
}
```
</details>
