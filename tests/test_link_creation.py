__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "06.03.2026"
__email__ = "m@hler.eu"
__status__ = "Development"


import cs2inspect
import unittest


class TestCS2InspectLinkCreation(unittest.TestCase):

    def test_link_creation(self):

        # Test 1: Datablock version (unmasked inspect link)
        link_data = {
            'asset_id': '38350177019',
            'class_id': '9385506221951591925',
            'owner_id': '76561198066322090'
        }
        expected_datablock_output = (
            "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20"
            "S76561198066322090A38350177019D9385506221951591925"
        )
        datablock_result = cs2inspect.link(link_data)

        self.assertEqual(
            datablock_result,
            expected_datablock_output,
            "Datablock link creation failed: output does not match expected format"
        )
        self.assertTrue(
            datablock_result.startswith("steam://rungame/730/"),
            "Datablock link does not start with expected Steam protocol"
        )
        self.assertIn("S76561198066322090", datablock_result, "Owner ID not found in datablock link")
        self.assertIn("A38350177019", datablock_result, "Asset ID not found in datablock link")
        self.assertIn("D9385506221951591925", datablock_result, "Class ID not found in datablock link")

        # Test 2: Protobuf version (masked inspect link)
        proto_base = cs2inspect.Builder(
            defindex=7,
            paintindex=941,
            paintseed=2,
            paintwear=0.22540508210659027,
            rarity=5,
            stickers=[{'slot': 2, 'sticker_id': 7203, 'wear': 0}]
        )
        protobuf = proto_base.build()
        expected_protobuf_output = (
            "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20"
            "00180720AD0728053897A19BF3034002620A080210A3381D000000006B570344"
        )
        protobuf_result = cs2inspect.link(protobuf)

        self.assertEqual(
            protobuf_result,
            expected_protobuf_output,
            "Protobuf link creation failed: output does not match expected format"
        )
        self.assertTrue(
            protobuf_result.startswith("steam://rungame/730/"),
            "Protobuf link does not start with expected Steam protocol"
        )

if __name__ == '__main__':
    unittest.main()
