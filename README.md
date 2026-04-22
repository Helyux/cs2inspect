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
- Schema Enrichment (Parsing): Resolve numeric IDs to human-readable names (Weapon, Skin, Rarity, Origin, Quality, etc.)
- Creating gen codes
- Creating console pasteable inspect links
- Checking inspect link validity (robust regex supporting modern CS2 formats)

## Installation

```bash
pip install cs2inspect
```


## Quick Start

### Link Creation
```python
import cs2inspect

# Create a modern 'masked' link using the Builder
proto = cs2inspect.Builder(
    defindex=7,
    paintindex=941,
    paintseed=0,
    paintwear=0.15,
    rarity=5
)
link = cs2inspect.link(proto.build())
print(link) # steam://run/730//+csgo_econ_action_preview%2000180720AD072805389AB3E6F00340006F59908E
```

### Basic Parsing
```python
import cs2inspect

# Parse a modern 'masked' inspect link
link = "steam://run/730//+csgo_econ_action_preview%206A7AC7C6BEDED06B72704ACE6F426F5A635296868780692AAC6C226A3A6A02E9EAEAEA661A625E7EE646"
data = cs2inspect.parse(link)

print(data['defindex'])    # 26 (PP-Bizon)
print(data['floatvalue'])  # 0.05357979
```

### Schema Enrichment
```python
import cs2inspect

# Resolve IDs to names using an external schema
cs2inspect.download_schema()
info = cs2inspect.parse(link, enrich=True)

print(info['full_item_name']) # StatTrak™ PP-Bizon | High Roller (Factory New)
```

## Documentation

For detailed information, please refer to the following docs:
- [**Example Usage**](docs/example_usage.md): Comprehensive examples for link creation, parsing, and enrichment.
- [**Output Model**](docs/output_model.md): Detailed specification of the dictionary structure returned by `parse()`.

---


## Technical Limitations (Parsing)
`cs2inspect` is a local, offline decoder. **Masked/Modern links** (binary Protobuf payload) are fully supported with offline enrichment of stickers, floats, and charms. **Unmasked/Legacy links** (S/M A D pointers) have only minimal support as they contain no binary property data; resolving their attributes requires a call to the **GameCoordinator (GC)**, which is outside the scope of this offline library.

## Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

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
