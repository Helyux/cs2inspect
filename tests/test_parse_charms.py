import unittest
from pathlib import Path

import cs2inspect


class TestCharms(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load schema for enriched tests - skip if not found
        schema_path = "cs2schema.json"
        if not Path(schema_path).exists():
            cls.schema = None
        else:
            cls.schema = cs2inspect.load_schema(schema_path)

    def skip_if_no_schema(self):
        if self.schema is None:
            self.skipTest("cs2schema.json not found, skipping enriched tests")

    def test_charms(self):
        self.skip_if_no_schema()

        # 1. Highlight charm
        link1 = (
            "steam://run/730//+csgo_econ_action_preview%20809080984B8AA080A883B08CE880F095228187888090D3D85C86FE064298"
        )
        res1 = cs2inspect.parse(link1, schema=self.schema)
        expected1 = {
            "itemid": 0,
            "defindex": 1355,
            "paintindex": 83,
            "rarity": 3,
            "quality": 12,
            "inventory": 0,
            "origin": 21,
            "paintseed": 0,
            "paintwear": 0,
            "floatvalue": 0.0,
            "rarity_name": "High Grade",
            "origin_name": "Tournament Drop",
            "quality_name": "Souvenir",
            "weapon_type": "Charm",
            "item_name": "Souvenir Charm | Budapest 2025 Highlight | karrigan vs Vitality on Overpass",
            "full_item_name": "Souvenir Charm | Budapest 2025 Highlight | karrigan vs Vitality on Overpass",
            "collection_name": "Budapest 2025",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGI6zwki4Uf_a0IWjIH_FtQQgu4z31VvyRU-hzMOurHcDvfOrOPFucfWWDDaTxbwl5LBvSnrgxhsk4TjSn437J3zGOFcmCYwwG7A7om1dgw",
        }
        self.assertEqual(res1, expected1)

        # 2. Regular Charm
        link2 = "steam://run/730//+csgo_econ_action_preview%20D3C3645A58066BD2CB18D9F3D3FBD6E3D7BB50535353DFA3D371D2D4DBD3C3DA8328B35075EE77"
        res2 = cs2inspect.parse(link2, schema=self.schema)
        expected2 = {
            "itemid": 49570563255,
            "defindex": 1355,
            "paintindex": 9,
            "rarity": 5,
            "quality": 4,
            "inventory": 3221225475,
            "origin": 0,
            "paintseed": 12411,
            "paintwear": 0,
            "floatvalue": 0.0,
            "rarity_name": "Exotic",
            "origin_name": "Timed Drop",
            "quality_name": "Unique",
            "weapon_type": "Charm",
            "item_name": "Charm | Lil' Monster",
            "full_item_name": "Charm | Lil' Monster",
            "collection_name": "Missing Link Charm Collection",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGI6zwki4Uf_a0IWsPGiE7Fhy-I764RbsQiL8l4Xz9Cxc4_ugY5tgL_6AGmKCj79wtOVrTijixU0m5m3UntioI3PEZldzCpd1FOJfsxXtmtCxNezk5gTAy9USJfGXAGI",
        }
        self.assertEqual(res2, expected2)

        # 3. Sticker Slab
        link3 = (
            "steam://run/730//+csgo_econ_action_preview%205949594192537959715A695131592959FB585E5159497C39B858F260BD11"
        )
        res3 = cs2inspect.parse(link3, schema=self.schema)
        expected_res3 = {
            "itemid": 0,
            "defindex": 1355,
            "paintindex": 225,
            "rarity": 3,
            "quality": 8,
            "inventory": 0,
            "origin": 0,
            "paintseed": 0,
            "paintwear": 0,
            "floatvalue": 0.0,
            "rarity_name": "High Grade",
            "origin_name": "Timed Drop",
            "quality_name": "Customized",
            "weapon_type": "Charm",
            "item_name": "Sticker Slab | iBUYPOWER | DreamHack 2014",
            "full_item_name": "Sticker Slab | iBUYPOWER | DreamHack 2014",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjM6pIinHtAI6_YXh80noVhjjocezqHdkvKXgMfI8JamXWjLAkbd05LVvFnG1xB9-tTvQztatc3mRbAUmDsAmTLVfsw74zIN3tXHXgw",
        }
        self.assertEqual(res3, expected_res3)


if __name__ == "__main__":
    unittest.main()
