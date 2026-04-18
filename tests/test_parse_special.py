import unittest
from pathlib import Path

import cs2inspect


class TestUnsupportedAndSpecial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema_path = "cs2schema.json"
        if not Path(schema_path).exists():
            cls.schema = None
        else:
            cls.schema = cs2inspect.load_schema(schema_path)

    def skip_if_no_schema(self):
        if self.schema is None:
            self.skipTest("cs2schema.json not found, skipping enriched tests")

    def test_music_kit_valve_ez4ence(self):
        self.skip_if_no_schema()
        # Music Kit | Valve, CS:GO (The index in link is 70)
        link = "steam://run/730//+csgo_econ_action_preview%205242524AF05872527A5162563A522252DA531411018CAB"
        res = cs2inspect.parse(link, schema=self.schema)

        expected = {
            "itemid": 0,
            "defindex": 1314,
            "paintindex": 0,
            "rarity": 3,
            "quality": 4,
            "paintwear": 0,
            "paintseed": 0,
            "inventory": 0,
            "origin": 0,
            "musicindex": 70,
            "floatvalue": 0.0,
            "rarity_name": "High Grade",
            "origin_name": "Timed Drop",
            "quality_name": "Unique",
            "weapon_type": "Music Kit",
            "item_name": "Valve, CS:GO",
            "imageurl": "https://cdn.steamstatic.com/apps/730/icons/econ/music_kits/valve_01.a22bb7e41ed9f28f93ac66f80f74716560236318.png",
            "full_item_name": "Music Kit | Valve, CS:GO"
        }
        self.assertEqual(res, expected)

    def test_pin_cobblestone(self):
        self.skip_if_no_schema()
        # Cobblestone Pin
        link = "steam://run/730//+csgo_econ_action_preview%204E5E4E56AB616E4E664A7E4A264E3E46BB2746AE"
        res = cs2inspect.parse(link, schema=self.schema)

        expected = {
            "itemid": 0,
            "defindex": 6117,
            "paintindex": 0,
            "rarity": 4,
            "quality": 4,
            "paintwear": 0,
            "paintseed": 0,
            "inventory": 0,
            "origin": 8,
            "floatvalue": 0.0,
            "rarity_name": "Remarkable",
            "origin_name": "Found in Crate",
            "quality_name": "Unique",
            "weapon_type": "Pin",
            "item_name": "Cobblestone Pin",
            "full_item_name": "Cobblestone Pin"
        }
        self.assertEqual(res, expected)

    def test_graffiti_popdog_wire_blue(self):
        self.skip_if_no_schema()
        # Graffiti
        link = "steam://run/730//+csgo_econ_action_preview%209A8A9A825F90BA9AB29BAA9EF89D929A8A5997AA91F29AEA82F934C556"
        res = cs2inspect.parse(link, schema=self.schema)

        expected = {
            "itemid": 0,
            "defindex": 1349,
            "paintindex": 0,
            "rarity": 1,
            "quality": 4,
            "paintwear": 0,
            "paintseed": 0,
            "inventory": 0,
            "origin": 24,
            "stickers": [],
            "floatvalue": 0.0,
            "rarity_name": "Base Grade",
            "origin_name": "Level Up Reward",
            "quality_name": "Unique",
            "weapon_type": "Graffiti",
            "item_name": "Popdog (Wire Blue)",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/IzMF03bi9WpSBq-S-ekoE33L-iLqGFHVaU25ZzQNQcXdB2ozio1RrlIWFK3UfvMYB8UsvjiMXojflsZalyxSh31CIyHz2GZ-KuFpPsrTzBG0se2dGHvwJjKWe3nYRQ4_H-JcNDmK-Tvw5u3AFD7PROt5FltQdfQE8m1JaMrYNxEjlNlc7Wa3m0tvEwMkZsxWfBbmySUQYL50EaZR17I",
            "full_item_name": "Graffiti | Popdog (Wire Blue)"
        }
        self.assertEqual(res, expected)

    def test_unsupported_season_medal(self):
        self.skip_if_no_schema()
        link = "steam://run/730//+csgo_econ_action_preview%20C1D10F64634476C0D968E9E1C1E9C7F1C5A9FEB1C802B9D731"
        with self.assertRaises(cs2inspect.UnsupportedItemError) as cm:
            cs2inspect.parse(link, schema=self.schema)

    def test_unsupported_service_medal(self):
        self.skip_if_no_schema()
        link = "steam://run/730//+csgo_econ_action_preview%20B0A01F734E412BB1A8689690B098B680B4D896C0B941A93E64"
        with self.assertRaises(cs2inspect.UnsupportedItemError):
            cs2inspect.parse(link, schema=self.schema)

    def test_unsupported_storage_unit(self):
        self.skip_if_no_schema()
        link = "steam://run/730//+csgo_econ_action_preview%20F3E3F3EB42FAD3F3DBF2C3F79BF383F112ED7A33"
        with self.assertRaises(cs2inspect.UnsupportedItemError):
            cs2inspect.parse(link, schema=self.schema)

    def test_unsupported_coin(self):
        self.skip_if_no_schema()
        link = "steam://run/730//+csgo_econ_action_preview%201E0EC0BFD1859D1F06D7193E1E36182E1A76306E1E32CAC8D7"
        with self.assertRaises(cs2inspect.UnsupportedItemError):
            cs2inspect.parse(link, schema=self.schema)

    def test_unsupported_pickem_trophy(self):
        self.skip_if_no_schema()
        link = "steam://run/730//+csgo_econ_action_preview%20F0E04914707EF7E877F7D0F0D8F6C0F498AD80F9A1D9AF04"
        with self.assertRaises(cs2inspect.UnsupportedItemError):
            cs2inspect.parse(link, schema=self.schema)

if __name__ == "__main__":
    unittest.main()
