from typing import Any

from ._util_base import INSPECT_BASE_MASKED, INSPECT_BASE_UNMASKED
from ._util_gen import build_gen_from_datablock, build_gen_from_dict
from ._util_hex import to_hex
from ._util_link import is_link_valid
from .econ_pb2 import CEconItemPreviewDataBlock


def _link_from_dict(data: dict[str, Any]) -> str | None:
    """
    Generate an inspect link from a data dictionary.

    :param data: The dictionary containing item data.
    :type data: dict[str, Any]

    :return: The generated inspect link or None.
    :rtype: str | None
    """

    required_keys = {"asset_id", "class_id"}
    if not required_keys.issubset(data.keys()):
        return None
    if "market_id" not in data and "owner_id" not in data:
        return None
    return link_unmasked(
        asset_id=data["asset_id"],
        class_id=data["class_id"],
        market_id=data.get("market_id"),
        owner_id=data.get("owner_id"),
        base=data.get("base", INSPECT_BASE_UNMASKED),
    )


def link(data: dict[str, Any] | CEconItemPreviewDataBlock, base: str | None = None) -> str | None:
    """
    Generate an inspect link from an item data dictionary or protobuf datablock.

    :param data: The input datablock or data dictionary.
    :type data: dict[str, Any] | CEconItemPreviewDataBlock
    :param base: The base URL for the inspect link.
    :type base: str

    :return: The generated inspect link, or None if invalid.
    :rtype: str | None
    """

    if isinstance(data, dict):
        return _link_from_dict(data)
    elif isinstance(data, CEconItemPreviewDataBlock):
        return link_masked(data, base=base or INSPECT_BASE_MASKED)
    return None


def gen(data: dict[str, Any] | CEconItemPreviewDataBlock, prefix: str = "!gen") -> str | None:
    """
    Generate a bot-compatible server command string (e.g., '!gen') from the given item data.

    :param data: The parsed data dictionary or protobuf block to generate from.
    :type data: dict[str, Any] | CEconItemPreviewDataBlock
    :param prefix: The prefix command string (default: "!gen").
    :type prefix: str

    :return: The gen command string, or None if the payload could not be built.
    :rtype: str | None
    """

    if isinstance(data, dict):
        gen_payload = build_gen_from_dict(data)
        if gen_payload is None:
            return None
        return f"{prefix} {gen_payload}"
    elif isinstance(data, CEconItemPreviewDataBlock):
        return f"{prefix} {build_gen_from_datablock(data)}"
    return None


def link_console(data: str | dict[str, Any] | CEconItemPreviewDataBlock) -> str | None:
    """
    Generate a console-pastable inspect link for the given item (e.g., 'csgo_econ_action_preview ...').

    :param data: An existing inspect link, an unmasked properties dict, or a CEconItemPreviewDataBlock.
    :type data: str | dict[str, Any] | CEconItemPreviewDataBlock

    :return: The console-pastable inspect link, or None if it cannot be generated.
    :rtype: str | None
    """

    if isinstance(data, (dict, CEconItemPreviewDataBlock)):
        if (raw := link(data)) is None:
            return None
        return raw.split("/+")[1].replace("%20", " ")
    elif isinstance(data, str):
        return data.split("/+")[1].replace("%20", " ")
    else:
        return None


def link_masked(data_block: CEconItemPreviewDataBlock, base: str = INSPECT_BASE_MASKED) -> str | None:
    """
    Generate a masked inspect link (hexadecimal payload) from a protobuf datablock.

    :param data_block: The CEconItemPreviewDataBlock protobuf object.
    :type data_block: CEconItemPreviewDataBlock
    :param base: The base URL for the inspect link.
    :type base: str

    :return: The generated inspect link, or None if invalid.
    :rtype: str | None
    """

    hex_string = to_hex(data_block)
    inspect_link = f"{base}{hex_string}"
    return inspect_link if is_link_valid(inspect_link) else None


def link_unmasked(
    asset_id: str,
    class_id: str,
    market_id: str | None = None,
    owner_id: str | None = None,
    base: str = INSPECT_BASE_UNMASKED,
) -> str | None:
    """
    Generate an unmasked inspect link using Asset, Class, and Market/Owner IDs (S/A/D/M format).

    :param asset_id: The asset ID ('A' block).
    :type asset_id: str
    :param class_id: The class ID ('D' block).
    :type class_id: str
    :param market_id: Optional market ID ('M' block).
    :type market_id: str | None
    :param owner_id: Optional owner ID ('S' block).
    :type owner_id: str | None
    :param base: The base inspect link URL.
    :type base: str

    :return: The generated inspect link, or None if invalid.
    :rtype: str | None
    """

    location = f"M{market_id}" if market_id else f"S{owner_id}"
    inspect_link = f"{base}{location}A{asset_id}D{class_id}"
    return inspect_link if is_link_valid(inspect_link) else None
