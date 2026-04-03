__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "04.04.2026"
__email__ = "m@hler.eu"
__status__ = "Development"


import unittest

import cs2inspect


class TestHexRoundtrip(unittest.TestCase):

    def test_protobuf_hex_roundtrip(self):
        builder = cs2inspect.Builder(
            defindex=7,
            paintindex=941,
            paintseed=2,
            paintwear=0.22540508210659027,
            rarity=5,
            stickers=[{'slot': 2, 'sticker_id': 7203, 'wear': 0}],
            keychains=[{'slot': 0, 'sticker_id': 36,
                        'offset_x': 4.515311241149902,
                        'offset_y': 0.5914779901504517,
                        'offset_z': 8.906611442565918}]
        )

        protobuf_original = builder.build()
        # Normal (non-masked) hex starts with 00
        hex_string = cs2inspect.to_hex(protobuf_original)
        self.assertTrue(hex_string.startswith("00"))

        protobuf_recreated = cs2inspect.from_hex(hex_string)
        self.assertEqual(protobuf_original, protobuf_recreated)

if __name__ == '__main__':
    unittest.main()
