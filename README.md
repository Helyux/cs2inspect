<div id="shields" align="center">

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Downloads][downloads-shield]][downloads-url]
[![GPLv3 License][license-shield]][license-url]
</div>

# cs2inspect

## Overview

`cs2inspect` is a python package used for creating and working with counter-strike inspect links and gen codes.

## Features

- Creating 'unmasked' inspect links (containing the owners steam id)
- Creating 'masked' (XOR-capable) inspect links
- Decoding/Parsing inspect links back into data or protobuf objects
- Parsing Enrichment: Resolve numeric IDs to human-readable names (Weapon, Skin, Rarity, Origin, Quality, etc.)
- Creating gen codes
- Creating console pasteable inspect links
- Checking inspect link validity (robust regex supporting modern CS2 formats)

## Installation

```bash
pip install cs2inspect
```

> [!IMPORTANT]
> Since version 7.x of Protobuf, this package now requires **Python 3.10+**.

## Example Usage

### Creating Links

```python
import cs2inspect

# Build an inspect link from a known steam id ('unmasked' inspect link)
link_data = {
    'asset_id': '38350177019',
    'class_id': '9385506221951591925',
    'owner_id': '76561198066322090'
}
link_str = cs2inspect.link(link_data)
print(link_str)  # = steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198066322090A38350177019D9385506221951591925

# Or build an inspect link from data only ('masked' inspect link)
proto_base = cs2inspect.Builder(
    defindex=7,
    paintindex=941,
    paintseed=2,
    paintwear=0.22540508210659027,
    rarity=5,
)

# You can also change and add attributes of the proto_base after creation
proto_base.stickers.append({'slot': 2, 'sticker_id': 7203, 'wear': 0})
proto_base.keychains.append({'slot': 0,'sticker_id': 36,
                             'offset_x': 4.515311241149902,
                             'offset_y': 0.5914779901504517,
                             'offset_z': 8.906611442565918})

try:
    # Build the protobuf
    protobuf = proto_base.build()
except Exception as e:
    print(f"Build failed: {e}")
    exit(1)

link_str = cs2inspect.link(protobuf)
print(link_str)  # = steam://rungame/730/76561202255233023/+csgo_econ_action_preview%2000180720AD0728053897A19BF3034002620A080210A3381D00000000A20118080010241D000000003D6E7D9040451A6B173F4D7B810E4191B1FE6E

# Get a command you can paste directly into the in-game console
console_str = cs2inspect.link_console(protobuf)
print(console_str)  # = csgo_econ_action_preview 00180720AD0728053897A19BF3034002620A080210A3381D00000000A20118080010241D000000003D6E7D9040451A6B173F4D7B810E4191B1FE6E

# You can also create gen codes from the protobuf
gen_str = cs2inspect.gen(protobuf, prefix="!g")  # You can omit the prefix to get '!gen'
print(gen_str)   # = !g 7 941 2 0.22540508 0 0 0 0 7203 0 0 0 0 0 36 0
```

### Parsing Links

Supports both legacy unmasked links (limited data; see [Limitations](#technical-limitations-parsing)) and modern masked links.

```python
import cs2inspect

# 1. Parse a traditional unmasked link (S A D format)
unmasked_link = "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198066322090A38350177019D9385506221951591925"
ids = cs2inspect.parse(unmasked_link)
print(ids['owner_id'])    # 76561198066322090
print(ids['asset_id'])    # 38350177019
print(ids['class_id'])    # 9385506221951591925

# 2. Parse a new masked CS2 link (contains full item properties)
masked_link = "steam://run/730//+csgo_econ_action_preview%206A7AC7C6BEDED06B72704ACE6F426F5A635296868780692AAC6C226A3A6A02E9EAEAEA661A625E7EE646"
data = cs2inspect.parse(masked_link)
print(data['defindex'])    # 26 (PP-Bizon)
print(data['floatvalue'])  # 0.05357979238033295

# 3. Get the raw protobuf data block from a masked link (Inverse of cs2inspect.link())
proto = cs2inspect.unlink(masked_link)
print(proto.itemid)     # 50039428653
print(proto.defindex)   # 26
print(proto.paintwear)  # 1029404284 (the proto doesnt contain the calculated float value)
print(proto.paintseed)  # 838
```

### Smart Enrichment

Resolve numeric IDs to real names (Weapon, Skin, Rarity, Wear, etc.) using an optional schema file.

```python
import cs2inspect
import json

# One-time setup: download the latest item/skin names (using ByMykel/CSGO-API)
# This is saved locally and remembered across restarts
cs2inspect.download_schema(path="cs2schema.json")

# Parse with enrichment enabled for a complex weapon (StatTrak™ AK-47 | Slate / with Stickers and a Charm)
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
            "stickerId": 7261,
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
            "stickerId": 7277,
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
            "stickerId": 7273,
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
            "stickerId": 7313,
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
            "stickerId": 47,
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

## Technical Limitations (Parsing)
`cs2inspect` is a local, offline decoder. **Masked/Modern links** (binary Protobuf payload) are fully supported with offline enrichment of stickers, floats, and charms. **Unmasked/Legacy links** (S/M A D pointers) have only minimal support as they contain no binary property data; resolving their attributes requires a call to the **GameCoordinator (GC)**, which is outside the scope of this offline library.

## Contributing
Contributions are welcome! Open an issue or submit a pull request.

## License
GPLv3 License. See the LICENSE file for details.

## Acknowledgements
Special thanks to these projects for their foundational work and metadata tracking:
- [csfloat/inspect](https://github.com/csfloat/inspect) - Foundational skin inspect library
- [ByMykel/CSGO-API](https://github.com/ByMykel/CSGO-API) - Primary source for the schema files
- [SteamTracking/GameTracking-CS2](https://github.com/SteamTracking/GameTracking-CS2) - Source for `Rarity` and `Quality` enums
- [SteamDatabase/SteamTracking](https://github.com/SteamDatabase/SteamTracking) - Source for `Origin` enum

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Helyux/cs2inspect.svg?style=for-the-badge
[contributors-url]: https://github.com/Helyux/cs2inspect/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Helyux/cs2inspect.svg?style=for-the-badge
[forks-url]: https://github.com/Helyux/cs2inspect/network/members
[stars-shield]: https://img.shields.io/github/stars/Helyux/cs2inspect.svg?style=for-the-badge
[stars-url]: https://github.com/Helyux/cs2inspect/stargazers
[issues-shield]: https://img.shields.io/github/issues/Helyux/cs2inspect.svg?style=for-the-badge
[issues-url]: https://github.com/Helyux/cs2inspect/issues
[downloads-shield]: https://img.shields.io/pepy/dt/cs2inspect?style=for-the-badge
[downloads-url]: https://pepy.tech/project/cs2inspect
[license-shield]: https://img.shields.io/badge/License-GPLv3-red.svg?style=for-the-badge
[license-url]: https://github.com/Helyux/cs2inspect/blob/master/LICENSE
