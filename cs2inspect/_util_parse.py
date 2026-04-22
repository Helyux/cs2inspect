from typing import Any

from cs2inspect._metadata import CATEGORY_IDS, GRAFFITI_TINTS, Origin, Quality, Rarity, get_wear_name
from cs2inspect._schema import ItemSchema
from cs2inspect._util_base import RE_MASKED_PAYLOAD, RE_UNMASKED_PAYLOAD
from cs2inspect._util_hex import bytes_to_float, from_hex
from cs2inspect.econ_pb2 import CEconItemPreviewDataBlock


class UnsupportedItemError(Exception):
    """Raised when an enriched parse encounters an unknown/unsupported item type."""
    pass


def _proto_to_dict(proto: CEconItemPreviewDataBlock) -> dict[str, Any]:
    """
    Convert a CEconItemPreviewDataBlock protobuf object to a dictionary.

    :param proto: The protobuf data block.
    :type proto: CEconItemPreviewDataBlock

    :return: A dictionary containing the parsed fields.
    :rtype: dict[str, Any]
    """

    # Map proto field names to result dictionary keys
    mapping = {
        "accountid": "accountid",
        "itemid": "itemid",
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
    for proto_name, result_key in mapping.items():
        if proto.HasField(proto_name):
            val = getattr(proto, proto_name)
            result[result_key] = val

    # Ensure cosmetic 'Big Three' default to 0 for consistency if missing
    for key in ["paintindex", "paintseed", "paintwear"]:
        if key not in result:
            result[key] = 0

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


def extract_payload(inspect_link: str, type_str: str) -> dict[str, Any]:
    """
    Extract raw field data from a validated, unquoted inspect link.

    :param inspect_link: The inspect link payload.
    :type inspect_link: str
    :param type_str: The type of the link ('masked' or 'unmasked').
    :type type_str: str

    :return: A dictionary with the extracted raw fields.
    :rtype: dict[str, Any]
    """

    result = {}

    if type_str == 'masked':
        match = RE_MASKED_PAYLOAD.search(inspect_link)
        if match:
            proto = from_hex(match.group(1))
            result = _proto_to_dict(proto)
    elif type_str == 'unmasked':
        match = RE_UNMASKED_PAYLOAD.search(inspect_link)
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

    if "paintwear" in result:
        result["floatvalue"] = bytes_to_float(result["paintwear"])

    return result


def enrich_enums(result: dict[str, Any], schema: ItemSchema | None) -> None:
    """
    Resolve enum IDs to human-readable names in the result dictionary.

    :param result: The dictionary containing raw extracted properties.
    :type result: dict[str, Any]
    :param schema: Optional schema instance for looking up names.
    :type schema: ItemSchema | None

    :return: None. The result dictionary is mutated in-place.
    :rtype: None
    """

    context = "weapon"
    if schema and "defindex" in result:
        defindex = result["defindex"]
        paintindex = result.get("paintindex", 0)

        w_name = schema.get_weapon_name(defindex)
        a_info = schema.get_agent_info(defindex)
        is_standalone = defindex in CATEGORY_IDS

        if a_info:
            context = "character"
        elif is_standalone:
            context = "other"

        # Apply wear metadata only for weapons/gloves (non-standalone, non-agent items)
        # Note: Paintindex > 0 or standard weapon defindexes typically imply wear support.
        if not is_standalone and not a_info:
            if "floatvalue" in result:
                result["wear_name"] = get_wear_name(result["floatvalue"])
            elif "paintwear" in result:
                result["wear_name"] = get_wear_name(bytes_to_float(result["paintwear"]))

        # wear_name is now an optional field omitted for non-weapon items.

    if "rarity" in result:
        result["rarity_name"] = Rarity.get_name(result["rarity"], context)
    if "origin" in result:
        result["origin_name"] = Origin.get_name(result["origin"])
    if "quality" in result:
        result["quality_name"] = Quality.get_name(result["quality"])

    if schema and "defindex" in result:
        if paintindex > 0:
            result["weapon_type"] = w_name
        elif a_info:
            result["weapon_type"] = a_info.get("name")
            result["collection_name"] = a_info.get("collection")
            result["imageurl"] = schema.get_image_url(a_info.get("image", ""))
        elif is_standalone:
            result["weapon_type"] = CATEGORY_IDS[defindex]
            if defindex == 1314: # Music Kit
                m_idx = result.get("musicindex")
                if m_idx is not None:
                    m_info = schema.get_music_kit_info(m_idx)
                    if m_info:
                        result["item_name"] = m_info.get("name")
                        result["imageurl"] = m_info.get("image")
                        result["collection_name"] = m_info.get("collection")
            else:
                result["item_name"] = w_name
        else:
            result["weapon_type"] = w_name

    # Final validation: If enrichment was requested, ensure the item is a supported type.
    # Unsupported items include Medals, Coins, Storage Units, Trophies, etc.
    if schema:
        supported_standalone = ["Sticker", "Graffiti", "Patch", "Charm", "Music Kit", "Pin"]
        w_type = result.get("weapon_type", "Unknown")

        # An item is considered supported if it is:
        # 1. A known standalone category (Stickers, Charms, etc.)
        # 2. An Agent
        # 3. A standard weapon that is not part of a blacklisted set.

        # Most unsupported items in the schema have specific keywords in their name.
        # If an item doesn't fit the above categories, or matches a blacklist,
        # it is treated as an unsupported item for the purpose of enriched parsing.

        is_agent = schema.get_agent_info(result.get("defindex", 0)) is not None
        is_known_standalone = w_type in supported_standalone

        # Determine if it's a weapon safely
        local_w_name = "Unknown"
        if "defindex" in result:
            local_w_name = schema.get_weapon_name(result["defindex"])

        is_weapon = local_w_name != "Unknown" and not is_known_standalone and not is_agent

        # Blacklist common "Bad" types that get registered as "weapons" in schema
        bad_keywords = ["Medal", "Trophy", "Coin", "Storage Unit", "Music Kit Box"]
        is_bad = any(k in w_type for k in bad_keywords)

        # Only raise UnsupportedItemError if we have a defindex to identify the item.
        # Unmasked links (S/M links) lack defindex in the payload and should not fail here.
        if "defindex" in result:
            if (w_type == "Unknown") or (is_weapon and is_bad):
                raise UnsupportedItemError(f"Unsupported item type: {w_type} (defindex {result.get('defindex')})")


def enrich_attachments(result: dict[str, Any], schema: ItemSchema) -> None:
    """
    Resolve sticker and keychain IDs to full metadata via schema lookups.

    :param result: The dictionary containing raw extracted properties.
    :type result: dict[str, Any]
    :param schema: The schema instance for looking up names.
    :type schema: ItemSchema

    :return: None. The result dictionary is mutated in-place.
    :rtype: None
    """

    if "stickers" in result:
        enriched_stickers = []
        for s in result["stickers"]:
            s_id = s.get("sticker_id")
            if s_id is not None:
                s_info = schema.get_sticker_info(s_id) or schema.get_sticker_slab_info(s_id)
                if s_info:
                    sticker_obj = {
                        "slot": s.get("slot"),
                        "sticker_id": s_id,
                        "codename": s_info.get("codename"),
                        "material": s_info.get("material"),
                        "name": s_info.get("name"),
                        "imageurl": s_info.get("image"),
                        "collection_name": s_info.get("collection"),
                        "wear": s.get("wear", 0.0),
                        "scale": s.get("scale"),
                        "rotation": s.get("rotation"),
                        "tint_id": s.get("tint_id"),
                        "offset_x": s.get("offset_x"),
                        "offset_y": s.get("offset_y"),
                        "offset_z": s.get("offset_z"),
                        "pattern": s.get("pattern"),
                        "highlight_reel": s.get("highlight_reel"),
                    }
                    # Remove None values to keep the output clean
                    sticker_obj = {k: v for k, v in sticker_obj.items() if v is not None}

                    # Special handling for Graffiti color naming via tint_id
                    t_id = sticker_obj.get("tint_id")
                    if t_id and t_id in GRAFFITI_TINTS:
                        color_name = GRAFFITI_TINTS[t_id]
                        base_name = sticker_obj.get("name", "Graffiti")

                        # Thorough cleaning of the base name
                        # 1. Strip common prefixes
                        for pref in ["Sealed Graffiti | ", "Graffiti | ", "Sealed "]:
                            if base_name.startswith(pref):
                                base_name = base_name[len(pref):]
                                break

                        # 2. Strip existing color suffix like " (Shark White)"
                        if " (" in base_name:
                            base_name = base_name.split(" (", 1)[0]

                        # 3. Construct the FULL name: Graffiti | [Design] ([Color])
                        sticker_obj["name"] = f"Graffiti | {base_name} ({color_name})"

                    enriched_stickers.append(sticker_obj)
                else:
                    s["sticker_id"] = s_id
                    enriched_stickers.append(s)
        result["stickers"] = enriched_stickers

    if "keychains" in result:
        enriched_keychains = []
        for k in result["keychains"]:
            k_id = k.get("sticker_id")
            w_id = k.get("wrapped_sticker")
            look_id = w_id if w_id is not None else k_id

            if look_id is not None:
                # Prioritize charm lookup.
                k_info = schema.get_charm_info(look_id)
                highlight_reel = k.get("highlight_reel")
                is_regular_charm = k_info is not None

                # If it's a keychain and contains a highlight_reel, it's a Souvenir Highlight.
                # Avoid falling back to sticker_slabs/stickers as they often share legacy IDs.
                if k_info is None and highlight_reel is not None:
                    h_info = schema.get_highlight_info(highlight_reel)
                    if h_info:
                        k_info = {
                            "name": h_info.get("name", "Souvenir Highlight Charm"),
                            "codename": "souvenir_highlight",
                            "material": h_info.get("original", {}).get("image_inventory", "econ/stickers/default"),
                            "image": h_info.get("image", ""),
                            "collection": h_info.get("tournament_event")
                        }
                    else:
                        k_info = {
                            "name": "Souvenir Highlight Charm",
                            "codename": "souvenir_highlight",
                            "material": "econ/stickers/default",
                            "image": "",
                            "collection": None
                        }
                else:
                    # Generic fallback for standard charms (e.g. Sticker Slabs)
                    fallback_info = schema.get_sticker_slab_info(look_id) or schema.get_sticker_info(look_id)
                    if not k_info and fallback_info:
                        k_info = fallback_info
                        is_regular_charm = False

                if k_info:
                    keychain_obj = {
                        "slot": k.get("slot"),
                        "sticker_id": look_id,
                        "codename": k_info.get("codename"),
                        "material": k_info.get("material"),
                        "name": k_info.get("name"),
                        "imageurl": k_info.get("image"),
                        "collection_name": k_info.get("collection"),
                        "wear": k.get("wear", 0.0),
                        "scale": k.get("scale"),
                        "rotation": k.get("rotation"),
                        "tint_id": k.get("tint_id"),
                        "offset_x": k.get("offset_x"),
                        "offset_y": k.get("offset_y"),
                        "offset_z": k.get("offset_z"),
                        "pattern": k.get("pattern", 0 if is_regular_charm else None),
                        "highlight_reel": k.get("highlight_reel"),
                    }
                    # Remove None values to keep the output clean
                    keychain_obj = {k: v for k, v in keychain_obj.items() if v is not None}
                    if w_id is not None:
                        keychain_obj["wrapped_sticker"] = w_id
                    enriched_keychains.append(keychain_obj)
                else:
                    k["sticker_id"] = k_id
                    enriched_keychains.append(k)
        result["keychains"] = enriched_keychains


def build_full_name(result: dict[str, Any], schema: ItemSchema) -> None:
    """
    Construct the full_item_name string from enriched result data.

    :param result: The dictionary containing enriched properties.
    :type result: dict[str, Any]
    :param schema: The schema instance for fallback name verification.
    :type schema: ItemSchema

    :return: None. The result dictionary is mutated in-place.
    :rtype: None
    """

    if "defindex" not in result:
        return

    defindex = result["defindex"]
    paintindex = result.get("paintindex", 0)

    skin_info = schema.get_skin_info(defindex, paintindex, result.get("floatvalue"))
    if skin_info:
        result["item_name"] = skin_info.get("name", "Unknown")
        result["imageurl"] = schema.get_image_url(skin_info.get("image", ""))
        result["min"] = skin_info.get("min_float")
        result["max"] = skin_info.get("max_float")
        if skin_info.get("collection"):
            result["collection_name"] = skin_info.get("collection")

    w_name = schema.get_weapon_name(defindex)
    a_name = schema.get_agent_name(defindex)
    is_standalone = defindex in CATEGORY_IDS

    quality_val = result.get("quality", 0)
    prefix = ""
    if quality_val == Quality.UNUSUAL:
        prefix += "★ "
    if "killeaterscoretype" in result or quality_val == Quality.STRANGE:
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
        if weapon in ["Sticker", "Graffiti", "Patch"] and result.get("stickers"):
            sticker = result["stickers"][0]
            full_name = sticker.get("name", weapon)
            result["full_item_name"] = full_name

            # Strip "Type | " or "Sealed Type | " prefix for a clean item_name
            clean_name = full_name
            prefixes = [f"{weapon} | ", f"Sealed {weapon} | "]
            for p in prefixes:
                if clean_name.startswith(p):
                    clean_name = clean_name[len(p):]
                    break
            result["item_name"] = clean_name
            result["collection_name"] = sticker.get("collection_name")
            result["imageurl"] = schema.get_image_url(sticker.get("imageurl"))
            result["stickers"] = []
        elif weapon == "Charm" and result.get("keychains"):
            charm = result["keychains"][0]
            result["paintseed"] = charm.get("pattern", 0)
            result["paintindex"] = charm.get("sticker_id",0)
            result["full_item_name"] = charm.get("name", weapon)
            result["item_name"] = charm.get("name")
            result["collection_name"] = charm.get("collection_name")
            result["imageurl"] = schema.get_image_url(charm.get("imageurl"))
            del result["keychains"]  # Remove the keychain list for standalone charms
        elif weapon == "Music Kit" and result.get("item_name"):
            result["full_item_name"] = f"Music Kit | {result['item_name']}"
        elif weapon == "Pin" and result.get("item_name"):
            result["full_item_name"] = result["item_name"]
        else:
            result["full_item_name"] = weapon
    elif skin and skin != "Unknown":
        result["full_item_name"] = f"{prefix}{weapon} | {skin}{wear}"
    else:
        result["full_item_name"] = f"{prefix}{weapon}{wear}"


if __name__ == '__main__':
    exit(1)
