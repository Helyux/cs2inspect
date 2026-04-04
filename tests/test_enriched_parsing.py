__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "04.04.2026"
__email__ = "m@hler.eu"
__status__ = "Development"


import unittest
from pathlib import Path

import cs2inspect


class TestEnrichedParsing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load schema for enriched tests - skip if not found
        schema_path = "cs2_schema.json"
        if not Path(schema_path).exists():
            cls.schema = None
        else:
            cls.schema = cs2inspect.load_schema(schema_path)

    def skip_if_no_schema(self):
        if self.schema is None:
            self.skipTest("cs2_schema.json not found, skipping enriched tests")

    def test_souvenir_dragon_lore(self):
        self.skip_if_no_schema()
        link = "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%2000180920D8022806300C38A3F3C2EB0340D101620A080010AC011D00000000620A0801108F011D00000000620A0802108B011D0000000062090803103C1D00000000E605A3C0"
        res = cs2inspect.parse(link, schema=self.schema)
        self.assertEqual(res["full_item_name"], "Souvenir AWP | Dragon Lore (Factory New)")

    def test_stattrak_gut_knife(self):
        self.skip_if_no_schema()
        link = "steam://run/730//+csgo_econ_action_preview%207363FED6ABCEDA726B897053D7705B7543704BD384AF937033DD703B7323731BF0F3F3F37F037B6DC7A246"
        res = cs2inspect.parse(link, schema=self.schema)
        self.assertEqual(res["full_item_name"], "★ StatTrak™ Gut Knife | Doppler (Factory New)")

    def test_specialist_gloves(self):
        self.skip_if_no_schema()
        link = "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%200018AA27209E0B2806300338E2F182F00340024BDF3FA4"
        res = cs2inspect.parse(link, schema=self.schema)
        self.assertEqual(res["full_item_name"], "★ Specialist Gloves | Pillow Punchers (Minimal Wear)")

    def test_agent_ricksaw_with_patch(self):
        self.skip_if_no_schema()
        link = "steam://run/730//+csgo_econ_action_preview%20ACBC2675184201ADB430868CAC84AA9CA8CEA6A4ADBC408F899E512593C486DCBB45C46EBD"
        res = cs2inspect.parse(link, schema=self.schema)
        self.assertEqual(res["full_item_name"], "Lt. Commander Ricksaw | NSWC SEAL")
        self.assertTrue(any(s["name"] == "Patch | Metal Supreme Master" for s in res["stickers"]))

    def test_standalone_sticker_liquid(self):
        self.skip_if_no_schema()
        link = "steam://run/730//+csgo_econ_action_preview%20889888903181A888A08CB88CEA8D8088984193E088F880F5194CD2"
        res = cs2inspect.parse(link, schema=self.schema)
        self.assertEqual(res["full_item_name"], "Sticker | Team Liquid (Holo) | Katowice 2019")
        self.assertEqual(res["stickers"], []) # Hoisted and cleared

    def test_m4a1s_hot_rod_with_charm_sticker_slab(self):
        self.skip_if_no_schema()
        link = "steam://run/730//+csgo_econ_action_preview%2080902F68726C3C8198BCA03D83A885B084B8014B626683C05B87E8DEF084228196888090A5BDDAF600BFC5BD6E44BECD0AF47BC0E000A20C63A9EA"
        res = cs2inspect.parse(link, schema=self.schema)
        self.assertEqual(res["full_item_name"], "M4A1-S | Hot Rod (Factory New)")
        self.assertEqual(res["keychains"][0]["name"], "Sticker Slab | DickStacy (Foil) | Berlin 2019")

if __name__ == '__main__':
    unittest.main()
