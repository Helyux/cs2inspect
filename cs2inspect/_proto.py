from dataclasses import dataclass, field
from typing import Any

from cs2inspect._metadata import Rarity
from cs2inspect._util_hex import float_to_bytes
from cs2inspect.econ_pb2 import CEconItemPreviewDataBlock

_COSMETIC_FIELDS = (
    "slot",
    "sticker_id",
    "wear",
    "scale",
    "rotation",
    "tint_id",
    "offset_x",
    "offset_y",
    "offset_z",
    "pattern",
    "highlight_reel",
    "wrapped_sticker",
)


@dataclass
class Builder:
    defindex: int
    paintindex: int
    paintseed: int
    paintwear: float
    rarity: str | int
    quality: int | None = None
    accountid: int | None = None
    itemid: int | None = None
    killeaterscoretype: int | None = None
    killeatervalue: int | None = None
    customname: str | None = None
    inventory: int | None = None
    origin: int | None = None
    questid: int | None = None
    dropreason: int | None = None
    musicindex: int | None = None
    entindex: int | None = None
    petindex: int | None = None
    style: int | None = None
    upgrade_level: int | None = None
    stickers: list[dict[str, Any]] = field(default_factory=list)
    keychains: list[dict[str, Any]] = field(default_factory=list)
    variations: list[dict[str, Any]] = field(default_factory=list)

    def build(self) -> CEconItemPreviewDataBlock:
        data = {
            "defindex": self.defindex,
            "paintindex": self.paintindex,
            "paintseed": self.paintseed,
            "paintwear": float_to_bytes(self.paintwear),
            "rarity": Rarity.parse(self.rarity),
        }

        optional_fields = {
            "quality": self.quality,
            "accountid": self.accountid,
            "itemid": self.itemid,
            "killeaterscoretype": self.killeaterscoretype,
            "killeatervalue": self.killeatervalue,
            "customname": self.customname,
            "inventory": self.inventory,
            "origin": self.origin,
            "questid": self.questid,
            "dropreason": self.dropreason,
            "musicindex": self.musicindex,
            "entindex": self.entindex,
            "petindex": self.petindex,
            "style": self.style,
            "upgrade_level": self.upgrade_level,
        }

        for field_name, value in optional_fields.items():
            if value is not None:
                data[field_name] = value

        # Process repeated collections
        if self.stickers:
            data["stickers"] = self._build_preview_collection(self.stickers)
        if self.keychains:
            data["keychains"] = self._build_preview_collection(self.keychains)
        if self.variations:
            data["variations"] = self._build_preview_collection(self.variations)

        return CEconItemPreviewDataBlock(**data)

    @staticmethod
    def _build_preview_collection(items: list[dict[str, Any]]) -> list[CEconItemPreviewDataBlock.Sticker]:
        preview_items: list[CEconItemPreviewDataBlock.Sticker] = []
        for item in items:
            if not isinstance(item, dict):
                raise TypeError(f"Preview item must be a dict, received {type(item)!r}")

            slot = item.get("slot")
            sticker_id = item.get("sticker_id")
            if slot is None or sticker_id is None:
                raise ValueError("Preview items require 'slot' and 'sticker_id'")

            preview_kwargs: dict[str, Any] = {"slot": slot, "sticker_id": sticker_id}

            for field_name in _COSMETIC_FIELDS:
                if field_name in ("slot", "sticker_id"):
                    continue

                value = item.get(field_name)
                if value is None:
                    continue
                preview_kwargs[field_name] = value

            if "wear" not in preview_kwargs:
                preview_kwargs["wear"] = 0.0

            preview_items.append(CEconItemPreviewDataBlock.Sticker(**preview_kwargs))

        return preview_items


if __name__ == "__main__":
    exit(1)
