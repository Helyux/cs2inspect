__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "04.04.2026"
__email__ = "m@hler.eu"
__status__ = "Development"


import json
from enum import IntEnum


class Rarity(IntEnum):
    STOCK = 0
    CONSUMER_GRADE = 1
    INDUSTRIAL_GRADE = 2
    MIL_SPEC_GRADE = 3
    RESTRICTED = 4
    CLASSIFIED = 5
    COVERT = 6
    CONTRABAND = 7
    GOLD = 99

    @classmethod
    def get_name(cls, value: int) -> str:
        names = {
            cls.STOCK: "Stock",
            cls.CONSUMER_GRADE: "Consumer Grade",
            cls.INDUSTRIAL_GRADE: "Industrial Grade",
            cls.MIL_SPEC_GRADE: "Mil-Spec Grade",
            cls.RESTRICTED: "Restricted",
            cls.CLASSIFIED: "Classified",
            cls.COVERT: "Covert",
            cls.CONTRABAND: "Contraband",
            cls.GOLD: "Extraordinary",
        }
        return names.get(value, "Unknown")

    @classmethod
    def parse(cls, value: str | int) -> int:
        """Parse rarity from string name or integer ID."""
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            clean_name = value.upper().replace(" ", "_").replace("-", "_")
            try:
                return cls[clean_name].value
            except KeyError:
                # Handle aliases
                aliases = {
                    "EXTRAORDINARY": cls.GOLD.value,
                    "UNUSUAL": cls.GOLD.value # Gloves/Knives use Gold rarity 99
                }
                if clean_name in aliases:
                    return aliases[clean_name]
                raise ValueError(f"Unknown rarity name: {value}")
        raise TypeError(f"Rarity must be str or int, got {type(value)}")


class Quality(IntEnum):
    NORMAL = 0
    GENUINE = 1
    VINTAGE = 2
    UNUSUAL = 3
    UNIQUE = 4
    COMMUNITY = 5
    DEVELOPER = 6
    SELF_MADE = 7
    VALVE = 8
    STATTRAK = 9
    RECYCLED = 10
    TOURNAMENT = 12
    HAUNTED = 13
    COLLECTORS = 14
    PAINTKIT_WEAPON = 15

    @classmethod
    def get_name(cls, value: int) -> str:
        names = {
            cls.NORMAL: "Normal",
            cls.GENUINE: "Genuine",
            cls.VINTAGE: "Vintage",
            cls.UNUSUAL: "Unusual",
            cls.UNIQUE: "Unique",
            cls.COMMUNITY: "Community",
            cls.DEVELOPER: "Developer",
            cls.SELF_MADE: "Self-Made",
            cls.VALVE: "Valve",
            cls.STATTRAK: "StatTrak™",
            cls.TOURNAMENT: "Souvenir",
            cls.COLLECTORS: "Collector's",
        }
        return names.get(value, "Standard")


class Origin(IntEnum):
    DROPPED = 0
    PURCHASED = 2
    TRADED = 3
    CRAFTED = 4
    STORE_BOUGHT = 5
    CRATE_OPENED = 7
    EXTERNAL = 8
    FOUND_IN_CRATE = 14
    TRADE_UP = 20

    @classmethod
    def get_name(cls, value: int) -> str:
        names = {
            cls.DROPPED: "Dropped",
            cls.PURCHASED: "Purchased",
            cls.TRADED: "Traded",
            cls.CRAFTED: "Crafted",
            cls.STORE_BOUGHT: "Store Bought",
            cls.CRATE_OPENED: "Unboxed",
            cls.EXTERNAL: "External",
            cls.FOUND_IN_CRATE: "Found in Crate",
            cls.TRADE_UP: "Trade-up",
        }
        return names.get(value, "Unknown")



def get_wear_name(wear: float) -> str:
    if wear < 0.07:
        return "Factory New"
    if wear < 0.15:
        return "Minimal Wear"
    if wear < 0.38:
        return "Field-Tested"
    if wear < 0.45:
        return "Well-Worn"
    return "Battle-Scarred"


CATEGORY_IDS = {
    1209: "Sticker",
    1349: "Graffiti",
    4609: "Patch",
    62: "Charm"
}


if __name__ == '__main__':
    exit(1)
