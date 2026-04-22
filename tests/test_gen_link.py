import unittest

import cs2inspect
from cs2inspect.econ_pb2 import CEconItemPreviewDataBlock


class TestCS2InspectLinkCreation(unittest.TestCase):
    def test_link_creation_from_dict_unmasked(self):
        """Test creating an unmasked (S A D M) inspect link from a dictionary."""
        link_data = {"asset_id": "38350177019", "class_id": "9385506221951591925", "owner_id": "76561198066322090"}
        expected_output = (
            "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20"
            "S76561198066322090A38350177019D9385506221951591925"
        )
        result = cs2inspect.link(link_data)

        self.assertEqual(result, expected_output, "Dict link creation failed: output does not match expected format")
        self.assertTrue(
            result.startswith("steam://rungame/730/"), "Dict link does not start with expected Steam protocol"
        )
        self.assertIn("S76561198066322090", result, "Owner ID not found in link")
        self.assertIn("A38350177019", result, "Asset ID not found in link")
        self.assertIn("D9385506221951591925", result, "Class ID not found in link")

    def test_link_creation_from_datablock_masked(self):
        """Test creating a masked (hex) inspect link from a CEconItemPreviewDataBlock."""
        masked_data = CEconItemPreviewDataBlock(
            defindex=7, paintindex=281, rarity=3, quality=4, paintwear=1045220557, paintseed=106
        )

        expected_output = "steam://run/730//+csgo_econ_action_preview%200018072099022803300438CD99B3F203406A9B1E6090"
        result = cs2inspect.link(masked_data)

        self.assertEqual(
            result, expected_output, "Datablock link creation failed: output does not match expected format"
        )
        self.assertTrue(
            result.startswith("steam://run/730/"), "Datablock link does not start with expected Steam protocol"
        )

    def test_link_creation_from_builder_masked(self):
        """Test creating a masked (hex) inspect link from a Builder protobuf block."""
        proto_base = cs2inspect.Builder(
            defindex=7,
            paintindex=941,
            paintseed=2,
            paintwear=0.22540508210659027,
            rarity=5,
            stickers=[{"slot": 2, "sticker_id": 7203, "wear": 0}],
        )
        protobuf = proto_base.build()

        expected_output = (
            "steam://run/730//+csgo_econ_action_preview%20"
            "00180720AD0728053897A19BF3034002620A080210A3381D000000006B570344"
        )
        result = cs2inspect.link(protobuf)

        self.assertEqual(result, expected_output, "Builder link creation failed: output does not match expected format")
        self.assertTrue(
            result.startswith("steam://run/730/"), "Builder link does not start with expected Steam protocol"
        )


if __name__ == "__main__":
    unittest.main()
