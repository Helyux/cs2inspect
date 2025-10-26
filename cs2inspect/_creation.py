__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "26.10.2025"
__email__ = "m@hler.eu"
__status__ = "Development"


from typing import Any, Optional, Union

from cs2inspect._gen_util import build_gen_from_datablock, build_gen_from_dict
from cs2inspect._hex import to_hex
from cs2inspect._link_util import is_link_valid
from cs2inspect.econ_pb2 import CEconItemPreviewDataBlock

INSPECT_BASE = "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20"


def _link_from_dict(data: dict[str, Any]) -> Optional[str]:
    """Generate an inspect link from a dictionary"""
    required_keys = {"asset_id", "class_id"}
    if not required_keys.issubset(data.keys()):
        return None
    if 'market_id' not in data and 'owner_id' not in data:
        return None
    return link_unmasked(
        asset_id=data['asset_id'],
        class_id=data['class_id'],
        market_id=data.get('market_id'),
        owner_id=data.get('owner_id')
    )


def link(data: Union[dict[str, Any], CEconItemPreviewDataBlock]) -> Optional[str]:
    """Generate an inspect link from the provided data"""
    if isinstance(data, dict):
        return _link_from_dict(data)
    elif isinstance(data, CEconItemPreviewDataBlock):
        return link_masked(data)
    return None


def gen(data: Union[dict[str, Any], CEconItemPreviewDataBlock], prefix: str = "!gen") -> Optional[str]:
    """Generate a gen command string for the given item"""
    if isinstance(data, dict):
        gen_payload = build_gen_from_dict(data)
        if gen_payload is None:
            return None
        return f"{prefix} {gen_payload}"
    elif isinstance(data, CEconItemPreviewDataBlock):
        return f"{prefix} {build_gen_from_datablock(data)}"
    return None


def link_console(data: Union[str, dict[str, Any], CEconItemPreviewDataBlock]) -> Optional[str]:
    """Generate a console-pastable command string for the given item"""
    if isinstance(data, (dict, CEconItemPreviewDataBlock)):
        inspect_link = link(data).split("/+")[1].replace("%20", " ")
        return inspect_link
    elif isinstance(data, str):
        return data.split("/+")[1].replace("%20", " ")
    else:
        return None


def link_masked(data_block: CEconItemPreviewDataBlock) -> Optional[str]:
    """Generate a masked inspect link from the given data block"""
    hex_string = to_hex(data_block)
    inspect_link = f"{INSPECT_BASE}{hex_string}"
    return inspect_link if is_link_valid(inspect_link) else None


def link_unmasked(asset_id: str, class_id: str,
                  market_id: Optional[str] = None, owner_id: Optional[str] = None) -> Optional[str]:
    """Generate an unmasked inspect link from the given asset and class id and either the owner or the market id"""
    location = f"M{market_id}" if market_id else f"S{owner_id}"
    inspect_link = f"{INSPECT_BASE}{location}A{asset_id}D{class_id}"
    return inspect_link if is_link_valid(inspect_link) else None


if __name__ == '__main__':
    exit(1)
