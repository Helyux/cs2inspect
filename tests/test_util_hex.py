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
            stickers=[{"slot": 2, "sticker_id": 7203, "wear": 0}],
            keychains=[
                {
                    "slot": 0,
                    "sticker_id": 36,
                    "offset_x": 4.515311241149902,
                    "offset_y": 0.5914779901504517,
                    "offset_z": 8.906611442565918,
                }
            ],
        )

        protobuf_original = builder.build()
        # Normal (non-masked) hex starts with 00
        hex_string = cs2inspect.to_hex(protobuf_original)
        self.assertTrue(hex_string.startswith("00"))

        protobuf_recreated = cs2inspect.from_hex(hex_string)
        self.assertEqual(protobuf_original, protobuf_recreated)

    def test_from_hex_rejects_corrupted_crc(self):
        builder = cs2inspect.Builder(
            defindex=7,
            paintindex=941,
            paintseed=2,
            paintwear=0.22540508210659027,
            rarity=5,
        )
        hex_string = cs2inspect.to_hex(builder.build())

        # Corrupt the last byte of the CRC
        corrupted = hex_string[:-2] + ("00" if hex_string[-2:] != "00" else "FF")
        with self.assertRaises(ValueError, msg="CRC checksum mismatch"):
            cs2inspect.from_hex(corrupted)

    def test_from_hex_rejects_oversized_payload(self):
        # 100001 hex chars = way beyond the 100000 limit
        huge_hex = "A" * 100_001
        with self.assertRaises(ValueError, msg="Hex payload too large"):
            cs2inspect.from_hex(huge_hex)

    def test_from_hex_rejects_empty_string(self):
        with self.assertRaises(ValueError):
            cs2inspect.from_hex("")

    def test_from_hex_rejects_too_short_payload(self):
        with self.assertRaises(ValueError):
            cs2inspect.from_hex("00AABB")


if __name__ == "__main__":
    unittest.main()
