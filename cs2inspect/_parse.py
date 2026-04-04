__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "04.04.2026"
__email__ = "m@hler.eu"
__status__ = "Development"


import re
from typing import Any, Dict, Optional, Union

from cs2inspect._metadata import CATEGORY_IDS, Origin, Quality, Rarity, get_wear_name
from cs2inspect._schema import ItemSchema, load_schema
from cs2inspect._util_hex import bytes_to_float, from_hex
from cs2inspect._util_link import _link_valid_and_type, unquote_link
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


def parse(
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

    if (enrich or schema) and result:
        # Load schema if path provided or if enrich requested
        if isinstance(schema, str):
            schema = load_schema(schema)
        elif schema is None:
            schema = load_schema()  # Try to load from default config

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

            # Prioritized Resolution
            w_name = schema.get_weapon_name(defindex)
            a_name = schema.get_agent_name(defindex)
            is_standalone = defindex in CATEGORY_IDS

            # Selection Logic:
            # a. If it's a skin (paintindex > 0), it's definitely a weapon
            if paintindex > 0:
                result["weapon_type"] = w_name
            # b. If it matches an Agent, prefer that (Agents never have paintindex)
            elif a_name != "Unknown":
                result["weapon_type"] = a_name
            # c. Handle Category IDs (Sticker, Patch, etc.)
            elif is_standalone:
                result["weapon_type"] = CATEGORY_IDS[defindex]
            else:
                result["weapon_type"] = w_name

        if schema:
            if "stickers" in result:
                enriched_stickers = []
                for s in result["stickers"]:
                    s_id = s.get("sticker_id")
                    if s_id is not None:
                        # Patches and sticker slabs (e.g. on Charms) use sticker_slab maps
                        s_info = schema.get_sticker_info(s_id) or schema.get_sticker_slab_info(s_id)
                        if s_info:
                            sticker_obj = {
                                "slot": s.get("slot"),
                                "stickerId": s_id,
                                "codename": s_info.get("codename"),
                                "material": s_info.get("material"),
                                "name": s_info.get("name"),
                                "image": s_info.get("image"),
                                "wear": s.get("wear", 0.0)
                            }
                            enriched_stickers.append(sticker_obj)
                        else:
                            s["stickerId"] = s_id
                            enriched_stickers.append(s)
                result["stickers"] = enriched_stickers

            if "keychains" in result:
                enriched_keychains = []
                for k in result["keychains"]:
                    k_id = k.get("sticker_id")
                    w_id = k.get("wrapped_sticker")
                    look_id = w_id if w_id is not None else k_id

                    if look_id is not None:
                        k_info = schema.get_charm_info(look_id) or schema.get_sticker_slab_info(look_id) or schema.get_sticker_info(look_id)
                        if k_info:
                            keychain_obj = {
                                "slot": k.get("slot"),
                                "stickerId": look_id,
                                "codename": k_info.get("codename"),
                                "material": k_info.get("material"),
                                "name": k_info.get("name"),
                                "image": k_info.get("image"),
                                "wear": k.get("wear", 0.0)
                            }
                            if w_id is not None:
                                keychain_obj["wrapped_sticker"] = w_id
                            enriched_keychains.append(keychain_obj)
                        else:
                            k["stickerId"] = k_id
                            enriched_keychains.append(k)
                result["keychains"] = enriched_keychains

        # 3. Name Construction
        if schema and "defindex" in result:
            defindex = result["defindex"]
            paintindex = result.get("paintindex", 0)

            skin_info = schema.get_skin_info(defindex, paintindex)
            if skin_info:
                result["item_name"] = skin_info.get("name", "Unknown")
                result["imageurl"] = schema.get_image_url(skin_info.get("image", ""))
                result["min"] = skin_info.get("min_float")
                result["max"] = skin_info.get("max_float")

            w_name = schema.get_weapon_name(defindex)
            a_name = schema.get_agent_name(defindex)
            is_standalone = defindex in CATEGORY_IDS

            quality_val = result.get("quality", 0)
            prefix = ""
            if quality_val == Quality.UNUSUAL:
                prefix += "★ "
            if "killeaterscoretype" in result:
                prefix += "StatTrak™ "
            if quality_val == Quality.TOURNAMENT:
                prefix += "Souvenir "
            if quality_val == Quality.GENUINE:
                prefix += "Genuine "

            weapon = result.get("weapon_type", "Unknown")
            skin = result.get("item_name")
            wear = f" ({result['wear_name']})" if "wear_name" in result else ""

            if a_name != "Unknown" and weapon == a_name:
                result["full_item_name"] = weapon
            elif is_standalone:
                if weapon == "Sticker" and result.get("stickers"):
                    sticker = result["stickers"][0]
                    result["full_item_name"] = sticker.get("name", weapon)
                    result["item_name"] = sticker.get("name")
                    result["imageurl"] = schema.get_image_url(sticker.get("image"))
                    result["stickers"] = []
                elif weapon == "Charm" and result.get("keychains"):
                    charm = result["keychains"][0]
                    result["full_item_name"] = charm.get("name", weapon)
                    result["item_name"] = charm.get("name")
                    result["imageurl"] = schema.get_image_url(charm.get("image"))
                    result["keychains"] = []
                else:
                    result["full_item_name"] = weapon
            elif skin and skin != "Unknown":
                result["full_item_name"] = f"{prefix}{weapon} | {skin}{wear}"
            else:
                result["full_item_name"] = f"{prefix}{weapon}{wear}"


        # Compatibility and field normalization
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
