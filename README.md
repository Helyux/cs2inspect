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

`cs2inspect` is a python package used for creating and working with CS2 inspect links and gen codes.

## Features

- Creating 'unmasked' inspect links (containing the owners steam id)
- Creating 'masked' (XOR-capable) inspect links
- Decoding/Unparsing inspect links back into data or protobuf objects
- **Smart Enrichment**: Resolve numeric IDs to human-readable names (Weapon, Skin, Rarity, etc.)
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

```python
import cs2inspect

# Works with both the new masked CS2 links and the old traditional unmasked inspect links
masked_link = "steam://run/730//+csgo_econ_action_preview%206A7AC7C6BEDED06B72704ACE6F426F5A635296868780692AAC6C226A3A6A02E9EAEAEA661A625E7EE646"

# 1. Get a normalized dictionary (best for human reading or passing back to Builder)
data_dict = cs2inspect.parse_link(masked_link)
print(data_dict['defindex'])  # 26
print(data_dict['paintwear']) # 0.053579...

# 2. Get the raw protobuf data block (Inverse of cs2inspect.link())
proto = cs2inspect.unlink(masked_link)
print(proto.itemid) # 50039428653
```

### Smart Enrichment

Resolve numeric IDs to real names (Weapon, Skin, Rarity, Wear, etc.) using an optional schema.

```python
import cs2inspect

# One-time setup: download the latest item/skin names (using ByMykel/CSGO-API)
# This is saved locally and remembered across restarts
cs2inspect.download_schema()

# Parse with enrichment enabled
link = "steam://run/730//+csgo_econ_action_preview%206A7AC7C..."
info = cs2inspect.parse_link(link, enrich=True)

print(info['full_item_name']) # "PP-Bizon | High Roller (Factory New)"
print(info['weapon_type'])    # "PP-Bizon"
print(info['item_name'])      # "High Roller"
print(info['rarity_name'])    # "Classified"
print(info['wear_name'])      # "Factory New"
print(info['imageurl'])       # "https://..."
```

## Contributing
Contributions are welcome! Open an issue or submit a pull request.

## License
GPLv3 License. See the LICENSE file for details.

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
