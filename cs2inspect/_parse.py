__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "03.04.2026"
__email__ = "m@hler.eu"
__status__ = "Development"

import re
from typing import Any, Dict, Union

from cs2inspect._hex import bytes_to_float, from_hex
from cs2inspect._link_util import _link_valid_and_type, unquote_link
from cs2inspect.econ_pb2 import CEconItemPreviewDataBlock


def _proto_to_dict(proto: CEconItemPreviewDataBlock) -> Dict[str, Any]:
    """Convert a CEconItemPreviewDataBlock protobuf to a dictionary compatible with Builder."""

    # Map proto field names to Builder parameter names
    mapping = {
        "accountid": "account_id",
        "itemid": "item_id",
        "defindex": "defindex",
        "paintindex": "paintindex",
        "rarity": "rarity",
        "quality": "quality",
        "paintwear": "paintwear",
        "paintseed": "paintseed",
        "killeaterscoretype": "killeaterscoretype",
        "killeatervalue": "killeatervalue",
        "customname": "customname",
        "inventory": "inventory",
        "origin": "origin",
        "questid": "questid",
        "dropreason": "dropreason",
        "musicindex": "musicindex",
        "entindex": "entindex",
        "petindex": "petindex",
        "style": "style",
        "upgrade_level": "upgrade_level",
    }

    result = {}

    # Process scalar fields
    for proto_name, builder_name in mapping.items():
        if proto.HasField(proto_name):
            val = getattr(proto, proto_name)
            if proto_name == "paintwear":
                val = bytes_to_float(val)
            result[builder_name] = val

    # Process repeated fields (stickers, keychains, variations)
    for collection_name in ["stickers", "keychains", "variations"]:
        items = getattr(proto, collection_name)
        if items:
            result[collection_name] = []
            for item in items:
                # Stickers in proto are CEconItemPreviewDataBlock.Sticker
                sticker_dict = {}
                for field in item.DESCRIPTOR.fields:
                    if item.HasField(field.name):
                        sticker_dict[field.name] = getattr(item, field.name)
                result[collection_name].append(sticker_dict)

    return result


def parse_link(inspect_link: str) -> Dict[str, Any]:
    """Parse a valid inspect link and extract its properties as a dictionary."""
    is_valid, type_str = _link_valid_and_type(inspect_link)

    if not is_valid or type_str is None:
        raise ValueError("Invalid inspect link format")

    inspect_link = unquote_link(inspect_link)

    if type_str == 'masked':
        # extract the hex payload - find the hex after "preview" possibly with space/%20 in between
        match = re.search(r'csgo_econ_action_preview(?:\s+|%20|)([0-9A-F]+)$', inspect_link, re.IGNORECASE)
        if match:
            proto = from_hex(match.group(1))
            return _proto_to_dict(proto)
    elif type_str == 'unmasked':
        # extract S/M and ID, A ID, D ID
        match = re.search(r'csgo_econ_action_preview(?:\s+|%20|)([SM])(\d+)A(\d+)D(\d+)$', inspect_link, re.IGNORECASE)
        if match:
            location_type = match.group(1).upper()
            location_id = match.group(2)
            asset_id = match.group(3)
            class_id = match.group(4)
            data = {'asset_id': asset_id, 'class_id': class_id}
            if location_type == 'M':
                data['market_id'] = location_id
            else:
                data['owner_id'] = location_id
            return data

    raise ValueError("Could not parse link")

def unlink(inspect_link: str) -> Union[Dict[str, Any], CEconItemPreviewDataBlock]:
    """
    Parse a valid inspect link and return its original data block.
    Matches the input types accepted by the `link()` function:
    - Returns `CEconItemPreviewDataBlock` for masked links.
    - Returns `dict` for unmasked links.
    """
    is_valid, type_str = _link_valid_and_type(inspect_link)

    if not is_valid or type_str is None:
        raise ValueError("Invalid inspect link format")

    inspect_link = unquote_link(inspect_link)

    if type_str == 'masked':
        match = re.search(r'csgo_econ_action_preview(?:\s+|%20|)([0-9A-F]+)$', inspect_link, re.IGNORECASE)
        if match:
            return from_hex(match.group(1))
    elif type_str == 'unmasked':
        match = re.search(r'csgo_econ_action_preview(?:\s+|%20|)([SM])(\d+)A(\d+)D(\d+)$', inspect_link, re.IGNORECASE)
        if match:
            location_type = match.group(1).upper()
            location_id = match.group(2)
            asset_id = match.group(3)
            class_id = match.group(4)
            data = {'asset_id': asset_id, 'class_id': class_id}
            if location_type == 'M':
                data['market_id'] = location_id
            else:
                data['owner_id'] = location_id
            return data

    raise ValueError("Could not unlink the provided string")


if __name__ == '__main__':
    exit(1)
