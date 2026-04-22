from typing import Any

from ._schema import ItemSchema, load_schema
from ._util_hex import from_hex
from ._util_link import _link_valid_and_type, unquote_link
from ._util_parse import (
    RE_MASKED_PAYLOAD,
    RE_UNMASKED_PAYLOAD,
    UnsupportedItemError,  # noqa: F401 — re-exported via __init__.py
    build_full_name,
    enrich_attachments,
    enrich_enums,
    extract_payload,
)
from .econ_pb2 import CEconItemPreviewDataBlock


def parse(inspect_link: str, enrich: bool = False, schema: ItemSchema | str | None = None) -> dict[str, Any]:
    """
    Parse a valid inspect link and extract its properties as a dictionary.

    :param inspect_link: The inspect link to parse.
    :type inspect_link: str
    :param enrich: Whether to enrich the parsed data with string representations via the schema.
    :type enrich: bool
    :param schema: An optional ItemSchema instance or file path to be used for enrichment.
    :type schema: ItemSchema | str | None

    :return: A dictionary containing the parsed item properties.
    :rtype: dict[str, Any]
    """

    is_valid, type_str = _link_valid_and_type(inspect_link)

    if not is_valid or type_str is None:
        raise ValueError("Invalid inspect link format")

    inspect_link = unquote_link(inspect_link)
    result = extract_payload(inspect_link, type_str)

    if (enrich or schema) and result:
        # Load schema if path provided or if enrich requested
        if isinstance(schema, str):
            schema = load_schema(schema, raise_on_error=True)
        elif schema is None:
            schema = load_schema()

        # If we have a schema (either provided or loaded from default location),
        # we perform full enrichment.
        if schema:
            enrich_enums(result, schema)
            enrich_attachments(result, schema)
            build_full_name(result, schema)
        else:
            # Fallback for when no schema is available: basic metadata enums only
            enrich_enums(result, None)

        # Final cleanup: omit optional enriched fields if they are missing, None, or empty
        optional_fields = ["collection_name", "imageurl", "wear_name", "min", "max", "item_name", "weapon_type"]
        for field in optional_fields:
            if field in result and result[field] in (None, ""):
                del result[field]

    return result


def unlink(inspect_link: str) -> dict[str, Any] | CEconItemPreviewDataBlock:
    """
    Reverse-engineer an inspect link back into its original data structure.
    Returns a protobuf datablock for masked links, and a dictionary of IDs for unmasked links.

    :param inspect_link: The inspect link to parse.
    :type inspect_link: str

    :return: The original data block from the inspect link.
    :rtype: dict[str, Any] | CEconItemPreviewDataBlock
    """

    is_valid, type_str = _link_valid_and_type(inspect_link)

    if not is_valid or type_str is None:
        raise ValueError("Invalid inspect link format")

    inspect_link = unquote_link(inspect_link)

    if type_str == "masked":
        match = RE_MASKED_PAYLOAD.search(inspect_link)
        if match:
            return from_hex(match.group(1))
    elif type_str == "unmasked":
        match = RE_UNMASKED_PAYLOAD.search(inspect_link)
        if match:
            location_type = match.group(1).upper()
            location_id = match.group(2)
            asset_id = match.group(3)
            class_id = match.group(4)
            data = {"asset_id": asset_id, "class_id": class_id}
            if location_type == "M":
                data["market_id"] = location_id
            else:
                data["owner_id"] = location_id
            return data

    raise ValueError("Could not unlink the provided string")
