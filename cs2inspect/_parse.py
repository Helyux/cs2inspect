__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "03.04.2026"
__email__ = "m@hler.eu"
__status__ = "Development"

import re
from typing import Any, Dict, Optional, Union

from cs2inspect._hex import bytes_to_float, from_hex
from cs2inspect._link_util import _link_valid_and_type, unquote_link
from cs2inspect._metadata import Origin, Quality, Rarity, get_wear_name
from cs2inspect._schema import ItemSchema, load_schema
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


def parse_link(
    inspect_link: str,
    enrich: bool = False,
    schema: Optional[Union[ItemSchema, str]] = None
) -> Dict[str, Any]:
    """Parse a valid inspect link and extract its properties as a dictionary."""
    is_valid, type_str = _link_valid_and_type(inspect_link)

    if not is_valid or type_str is None:
        raise ValueError("Invalid inspect link format")

    inspect_link = unquote_link(inspect_link)
    result = {}

    if type_str == 'masked':
        # extract the hex payload - find the hex after "preview" possibly with space/%20 in between
        match = re.search(r'csgo_econ_action_preview(?:\s+|%20|)([0-9A-F]+)$', inspect_link, re.IGNORECASE)
        if match:
            proto = from_hex(match.group(1))
            result = _proto_to_dict(proto)
    elif type_str == 'unmasked':
        # extract S/M and ID, A ID, D ID
        match = re.search(r'csgo_econ_action_preview(?:\s+|%20|)([SM])(\d+)A(\d+)D(\d+)$', inspect_link, re.IGNORECASE)
        if match:
            location_type = match.group(1).upper()
            location_id = match.group(2)
            asset_id = match.group(3)
            class_id = match.group(4)
            result = {'asset_id': asset_id, 'class_id': class_id}
            if location_type == 'M':
                result['market_id'] = location_id
            else:
                result['owner_id'] = location_id
    else:
        raise ValueError("Could not parse link")

    if enrich and result:
        # Load schema if path provided
        if isinstance(schema, str):
            schema = load_schema(schema)
        elif schema is None:
            schema = load_schema()  # Try to load from config

        # 1. Map basic enums
        if "paintwear" in result:
            result["wear_name"] = get_wear_name(result["paintwear"])
        if "rarity" in result:
            result["rarity_name"] = Rarity.get_name(result["rarity"])
        if "origin" in result:
            result["origin_name"] = Origin.get_name(result["origin"])
        if "quality" in result:
            result["quality_name"] = Quality.get_name(result["quality"])

        # 2. Schema-based names
        if schema and "defindex" in result:
            defindex = result["defindex"]
            paintindex = result.get("paintindex", 0)

            result["weapon_type"] = schema.get_weapon_name(defindex)

            skin_info = schema.get_skin_info(defindex, paintindex)
            if skin_info:
                result["item_name"] = skin_info.get("name", "Unknown")
                result["imageurl"] = schema.get_image_url(skin_info.get("image", ""))
                result["min"] = skin_info.get("min_float")
                result["max"] = skin_info.get("max_float")

                # Full name construction
                quality_val = result.get("quality", 0)
                prefix = ""
                if quality_val == Quality.STRANGE:
                    prefix = "StatTrak™ "
                elif quality_val == Quality.TOURNAMENT:
                    prefix = "Souvenir "
                elif quality_val == Quality.UNUSUAL:
                    prefix = "★ "
                elif quality_val == Quality.GENUINE:
                    prefix = "Genuine "

                weapon = result["weapon_type"]
                skin = result["item_name"]
                wear = f" ({result['wear_name']})" if "wear_name" in result else ""

                if skin and skin != "Unknown":
                    result["full_item_name"] = f"{prefix}{weapon} | {skin}{wear}"
                else:
                    result["full_item_name"] = f"{prefix}{weapon}{wear}"

        # 3. Compatibility fields (matching user's request)
        if "account_id" in result:
            result["accountid"] = result["account_id"]
        if "item_id" in result:
            result["itemid"] = str(result["item_id"])
        if "paintwear" in result:
            result["floatvalue"] = result["paintwear"]

        # Ensure stickers is always a list
        if "stickers" not in result:
            result["stickers"] = []

    return result

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
