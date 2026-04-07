__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "08.04.2026"
__email__ = "m@hler.eu"
__status__ = "Development"


from enum import IntEnum


# Source:
# https://github.com/SteamTracking/GameTracking-CS2/blob/master/game/csgo/pak01_dir/resource/csgo_english.txt
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
    def get_name(cls, value: int, context: str = "weapon") -> str:
        """
        Get the localized name for a rarity value based on the item context.
        Possible contexts: 'weapon', 'character', 'other'
        """
        # Gold/Extraordinary items use special logic
        if value == cls.GOLD:
            if context == "character":
                return "Master"
            if context == "other":
                return "Extraordinary"
            return "Extraordinary"

        tracks = {
            "weapon": {
                cls.STOCK: "Stock",
                cls.CONSUMER_GRADE: "Consumer Grade",
                cls.INDUSTRIAL_GRADE: "Industrial Grade",
                cls.MIL_SPEC_GRADE: "Mil-Spec Grade",
                cls.RESTRICTED: "Restricted",
                cls.CLASSIFIED: "Classified",
                cls.COVERT: "Covert",
                cls.CONTRABAND: "Contraband",
            },
            "character": {
                cls.STOCK: "Default",
                cls.MIL_SPEC_GRADE: "Distinguished",
                cls.RESTRICTED: "Exceptional",
                cls.CLASSIFIED: "Superior",
                cls.COVERT: "Master",
                cls.CONTRABAND: "Contraband",
            },
            "other": {
                cls.STOCK: "Default",
                cls.CONSUMER_GRADE: "Base Grade",
                cls.INDUSTRIAL_GRADE: "Medium Grade",
                cls.MIL_SPEC_GRADE: "High Grade",
                cls.RESTRICTED: "Remarkable",
                cls.CLASSIFIED: "Exotic",
                cls.COVERT: "Extraordinary",
                cls.CONTRABAND: "Contraband",
            }
        }

        # Fallback to weapon track if context is unknown
        track = tracks.get(context, tracks["weapon"])
        return track.get(value, "Unknown")

    @classmethod
    def parse(cls, value: str | int) -> int:
        """Parse rarity from string name or integer ID supporting all tracks."""
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            clean_name = value.upper().replace(" ", "_").replace("-", "_")
            try:
                # Direct check against enum members (Weapon track mostly)
                return cls[clean_name].value
            except KeyError:
                # Context-aware aliases from all 3 tracks
                aliases = {
                    # ID 6: Ancient
                    "MASTER": 6,
                    "EXTRAORDINARY": 6,
                    "ANCIENT": 6,
                    "UNUSUAL": 99, # Special case for Gloves/Knives Star

                    # ID 5: Legendary
                    "SUPERIOR": 5,
                    "EXOTIC": 5,
                    "LEGENDARY": 5,

                    # ID 4: Mythical
                    "EXCEPTIONAL": 4,
                    "REMARKABLE": 4,
                    "MYTHICAL": 4,

                    # ID 3: Rare
                    "DISTINGUISHED": 3,
                    "HIGH_GRADE": 3,
                    "RARE": 3,
                    "MIL_SPEC": 3,

                    # ID 2: Uncommon
                    "MEDIUM_GRADE": 2,
                    "UNCOMMON": 2,
                    "INDUSTRIAL": 2,

                    # ID 1: Common
                    "BASE_GRADE": 1,
                    "COMMON": 1,
                    "CONSUMER": 1,

                    # ID 0: Default
                    "DEFAULT": 0,
                }
                if clean_name in aliases:
                    return aliases[clean_name]
                raise ValueError(f"Unknown rarity name: {value}. Use integer IDs (0-7, 99) or standardized names.")
        raise TypeError(f"Rarity must be str or int, got {type(value)}")


# Sources:
# https://raw.githubusercontent.com/SteamTracking/GameTracking-CS2/refs/heads/master/game/csgo/pak01_dir/scripts/items/items_game.txt
# https://raw.githubusercontent.com/SteamDatabase/SteamTracking/b5cba7a22ab899d6d423380cff21cec707b7c947/ItemSchema/CounterStrikeGlobalOffensive.json
# https://raw.githubusercontent.com/SteamTracking/GameTracking-CS2/refs/heads/master/game/csgo/pak01_dir/resource/csgo_english.txt
class Quality(IntEnum):
    NORMAL = 0
    GENUINE = 1
    VINTAGE = 2
    UNUSUAL = 3
    UNIQUE = 4
    COMMUNITY = 5
    DEVELOPER = 6
    SELFMADE = 7
    CUSTOMIZED = 8
    STRANGE = 9
    COMPLETED = 10
    HAUNTED = 11
    TOURNAMENT = 12
    HIGHLIGHT = 13
    VOLATILE = 14

    @classmethod
    def get_name(cls, value: int) -> str:
        names = {
            cls.NORMAL: "Normal",
            cls.GENUINE: "Genuine",
            cls.VINTAGE: "Vintage",
            cls.UNUSUAL: "★",
            cls.UNIQUE: "Unique",
            cls.COMMUNITY: "Community",
            cls.DEVELOPER: "Valve",
            cls.SELFMADE: "Prototype",
            cls.CUSTOMIZED: "Customized",
            cls.STRANGE: "StatTrak™",
            cls.COMPLETED: "Completed",
            cls.HAUNTED: "Haunted",
            cls.TOURNAMENT: "Souvenir",
            cls.HIGHLIGHT: "Highlight",
            cls.VOLATILE: "Volatile",
        }
        return names.get(value, "Unknown")

# Source:
# https://raw.githubusercontent.com/SteamDatabase/SteamTracking/b5cba7a22ab899d6d423380cff21cec707b7c947/ItemSchema/CounterStrikeGlobalOffensive.json
class Origin(IntEnum):
    TIMED_DROP = 0
    ACHIEVEMENT = 1
    PURCHASED = 2
    TRADED = 3
    CRAFTED = 4
    STORE_PROMOTION = 5
    GIFTED = 6
    SUPPORT_GRANTED = 7
    FOUND_IN_CRATE = 8
    EARNED = 9
    THIRD_PARTY_PROMOTION = 10
    WRAPPED_GIFT = 11
    HALLOWEEN_DROP = 12
    STEAM_PURCHASE = 13
    FOREIGN_ITEM = 14
    CD_KEY = 15
    COLLECTION_REWARD = 16
    PREVIEW_ITEM = 17
    STEAM_WORKSHOP_CONTRIBUTION = 18
    PERIODIC_SCORE_REWARD = 19
    RECYCLING = 20
    TOURNAMENT_DROP = 21
    STOCK_ITEM = 22
    QUEST_REWARD = 23
    LEVEL_UP_REWARD = 24

    @classmethod
    def get_name(cls, value: int) -> str:
        names = {
            cls.TIMED_DROP: "Timed Drop",
            cls.ACHIEVEMENT: "Achievement",
            cls.PURCHASED: "Purchased",
            cls.TRADED: "Traded",
            cls.CRAFTED: "Crafted",
            cls.STORE_PROMOTION: "Store Promotion",
            cls.GIFTED: "Gifted",
            cls.SUPPORT_GRANTED: "Support Granted",
            cls.FOUND_IN_CRATE: "Found in Crate",
            cls.EARNED: "Earned",
            cls.THIRD_PARTY_PROMOTION: "Third-Party Promotion",
            cls.WRAPPED_GIFT: "Wrapped Gift",
            cls.HALLOWEEN_DROP: "Halloween Drop",
            cls.STEAM_PURCHASE: "Steam Purchase",
            cls.FOREIGN_ITEM: "Foreign Item",
            cls.CD_KEY: "CD Key",
            cls.COLLECTION_REWARD: "Collection Reward",
            cls.PREVIEW_ITEM: "Preview Item",
            cls.STEAM_WORKSHOP_CONTRIBUTION: "Steam Workshop Contribution",
            cls.PERIODIC_SCORE_REWARD: "Periodic Score Reward",
            cls.RECYCLING: "Recycling",
            cls.TOURNAMENT_DROP: "Tournament Drop",
            cls.STOCK_ITEM: "Stock Item",
            cls.QUEST_REWARD: "Quest Reward",
            cls.LEVEL_UP_REWARD: "Level Up Reward",
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
