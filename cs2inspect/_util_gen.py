from typing import Any

from cs2inspect._util_hex import bytes_to_float
from cs2inspect.econ_pb2 import CEconItemPreviewDataBlock


def _format_float(value: float, precision: int = 8) -> str:
    formatted = f"{value:.{precision}f}".rstrip("0").rstrip(".")
    return formatted or "0"


def _serialize_item_pairs(items: list[dict[str, Any]], pad_to: int | None = None) -> list[str]:
    serialized: list[str] = []
    filtered_items = [item for item in items if item.get("sticker_id")]

    if pad_to is not None:
        slot_map = {item.get("slot", 0): item for item in filtered_items}
        for slot in range(pad_to):
            item = slot_map.get(slot)
            if item:
                serialized.append(str(item.get("sticker_id", 0)))
                serialized.append(_format_float(float(item.get("wear", 0.0))))
            else:
                serialized.extend(["0", "0"])
    else:
        for item in sorted(filtered_items, key=lambda itm: itm.get("slot", 0)):
            serialized.append(str(item.get("sticker_id", 0)))
            serialized.append(_format_float(float(item.get("wear", 0.0))))

    return serialized


def _build_gen_string(data: dict[str, Any], stickers: list[dict[str, Any]], keychains: list[dict[str, Any]]) -> str:
    """
    Build the item data string from the given data and attachments.

    :param data: The parsed data dictionary containing the defindex, paintindex, paintseed, and paintwear.
    :type data: dict[str, Any]
    :param stickers: List of stickers appended to the weapon.
    :type stickers: list[dict[str, Any]]
    :param keychains: List of keychains appended to the weapon.
    :type keychains: list[dict[str, Any]]

    :return: The formatted gen command string.
    :rtype: str
    """
    paintwear = _format_float(float(data["paintwear"]))
    parts: list[str] = [
        str(data["defindex"]),
        str(data["paintindex"]),
        str(data["paintseed"]),
        paintwear,
    ]

    parts.extend(_serialize_item_pairs(stickers, pad_to=5))
    parts.extend(_serialize_item_pairs(keychains))

    return " ".join(parts)


def build_gen_from_dict(data: dict[str, Any]) -> str | None:
    """
    Extract properties and format them automatically into a gen command parsing properties dynamically.

    :param data: The inspect data dictionary.
    :type data: dict[str, Any]

    :return: The generated gen string, or None if essential properties are missing.
    :rtype: str | None
    """
    required_keys = {"defindex", "paintindex", "paintseed", "paintwear"}
    if not required_keys.issubset(data.keys()):
        return None

    stickers = data.get("stickers", [])
    keychains = data.get("keychains", [])
    return _build_gen_string(data, stickers, keychains)


def build_gen_from_datablock(data: CEconItemPreviewDataBlock) -> str:
    """
    Produce the equivalent schema-less generating standard sequence string from raw protobuf payload blocks directly.

    :param data: The datablock instance populated with internal data.
    :type data: CEconItemPreviewDataBlock

    :return: The generated gen string.
    :rtype: str
    """
    data_dict = {
        "defindex": data.defindex,
        "paintindex": data.paintindex,
        "paintseed": data.paintseed,
        "paintwear": bytes_to_float(data.paintwear),
        "stickers": [{"slot": s.slot, "sticker_id": s.sticker_id, "wear": s.wear} for s in data.stickers],
        "keychains": [{"slot": k.slot, "sticker_id": k.sticker_id, "wear": k.wear} for k in data.keychains],
    }
    return _build_gen_string(data_dict, data_dict["stickers"], data_dict["keychains"])


if __name__ == "__main__":
    exit(1)
