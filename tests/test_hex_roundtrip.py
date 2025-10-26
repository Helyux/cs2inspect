__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "26.10.2025"
__email__ = "m@hler.eu"
__status__ = "Development"


import unittest

import cs2inspect


class TestHexRoundtrip(unittest.TestCase):

    def test_proto_roundtrip_via_hex_preserves_payload(self):
        builder = cs2inspect.Builder(
            defindex=7,
            paintindex=941,
            paintseed=2,
            paintwear=0.22540508,
            rarity=5,
            stickers=[{"slot": 2, "sticker_id": 7203, "wear": 0.01}],
            keychains=[{"slot": 0, "sticker_id": 36, "offset_x": 1.0}],
        )

        original_proto = builder.build()
        hex_payload = cs2inspect.to_hex(original_proto)

        self.assertTrue(hex_payload.startswith("00"))
        self.assertEqual(hex_payload, hex_payload.upper())

        roundtripped_proto = cs2inspect.from_hex(hex_payload)
        self.assertEqual(
            roundtripped_proto.SerializeToString(),
            original_proto.SerializeToString(),
        )


if __name__ == '__main__':
    unittest.main()
