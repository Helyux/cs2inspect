__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "26.10.2025"
__email__ = "m@hler.eu"
__status__ = "Development"


import unittest

import cs2inspect


class TestGenCommand(unittest.TestCase):

    def test_gen_includes_keychains_and_pads_stickers(self):
        builder = cs2inspect.Builder(
            defindex=7,
            paintindex=941,
            paintseed=2,
            paintwear=0.22540508210659027,
            rarity=5,
            stickers=[{'slot': 2, 'sticker_id': 7203, 'wear': 0}],
            keychains=[{
                'slot': 0,
                'sticker_id': 36,
                'offset_x': 4.515311241149902,
                'offset_y': 0.5914779901504517,
                'offset_z': 8.906611442565918,
            }],
        )

        proto = builder.build()
        expected = "!g 7 941 2 0.22540508 0 0 0 0 7203 0 0 0 0 0 36 0"

        self.assertEqual(cs2inspect.gen(proto, prefix="!g"), expected)

    def test_gen_accepts_dict_with_keychains(self):
        item_dict = {
            'defindex': 7,
            'paintindex': 941,
            'paintseed': 2,
            'paintwear': 0.22540508710659027,
            'stickers': [{'slot': 3, 'sticker_id': 111, 'wear': 0.2}],
            'keychains': [{'slot': 0, 'sticker_id': 16}],
        }

        gen_string = cs2inspect.gen(item_dict, prefix="!g")
        self.assertEqual(gen_string, "!g 7 941 2 0.22540509 0 0 0 0 0 0 111 0.2 0 0 16 0")


if __name__ == '__main__':
    unittest.main()
