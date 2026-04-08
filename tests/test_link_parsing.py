import unittest

import cs2inspect


class TestLinkParsing(unittest.TestCase):

    def test_unlink_masked_link(self):
        # Test unlinking a masked link (should return a CEconItemPreviewDataBlock)
        masked_link = "steam://run/730//+csgo_econ_action_preview%206A7AC7C6BEDED06B72704ACE6F426F5A635296868780692AAC6C226A3A6A02E9EAEAEA661A625E7EE646"
        data = cs2inspect.unlink(masked_link)

        self.assertTrue(isinstance(data, cs2inspect.econ_pb2.CEconItemPreviewDataBlock), "Unlink of masked link did not return a protobuf data block")
        self.assertEqual(data.defindex, 26)
        self.assertEqual(data.paintindex, 676)

    def test_unlink_unmasked_link(self):
        # Test unlinking an unmasked link (should return a dictionary)
        unmasked_link = "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198066322090A38350177019D9385506221951591925"
        data = cs2inspect.unlink(unmasked_link)

        self.assertTrue(isinstance(data, dict), "Unlink of unmasked link did not return a dictionary")
        self.assertEqual(data['owner_id'], '76561198066322090')
        self.assertEqual(data['asset_id'], '38350177019')

    def test_parse_masked_roundtrip(self):
        # Test parse (friendly dictionary output) for a masked link
        masked_link = "steam://run/730//+csgo_econ_action_preview%206A7AC7C6BEDED06B72704ACE6F426F5A635296868780692AAC6C226A3A6A02E9EAEAEA661A625E7EE646"
        data = cs2inspect.parse(masked_link)

        self.assertTrue(isinstance(data, dict), "parse did not return a dictionary")
        self.assertEqual(data['defindex'], 26)
        self.assertEqual(data['paintwear'], 1029404284)
        self.assertAlmostEqual(data['floatvalue'], 0.053579792, places=8)

    def test_unlink_agent(self):
        link = "steam://run/730//+csgo_econ_action_preview%20ACBC2675184201ADB430868CAC84AA9CA8CEA6A4ADBC408F899E512593C486DCBB45C46EBD"
        data = cs2inspect.unlink(link)
        self.assertEqual(data.defindex, 5404)

    def test_unlink_sticker(self):
        link = "steam://run/730//+csgo_econ_action_preview%20889888903181A888A08CB88CEA8D8088984193E088F880F5194CD2"
        data = cs2inspect.unlink(link)
        self.assertEqual(data.defindex, 1209)

    def test_unlink_charm_on_gun(self):
        link = "steam://run/730//+csgo_econ_action_preview%2080902F68726C3C8198BCA03D83A885B084B8014B626683C05B87E8DEF084228196888090A5BDDAF600BFC5BD6E44BECD0AF47BC0E000A20C63A9EA"
        data = cs2inspect.unlink(link)
        self.assertEqual(data.defindex, 60)
        self.assertTrue(len(data.keychains) > 0)

    def test_parse_legacy_unmasked_link(self):
        # Test a standard legacy link with S/A/D components
        link = "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198342167318A49511393803D7532878161036823080"
        data = cs2inspect.parse(link)

        self.assertEqual(data['owner_id'], '76561198342167318')
        self.assertEqual(data['asset_id'], '49511393803')
        self.assertEqual(data['class_id'], '7532878161036823080')

    def test_parse_zero_seed(self):
        # Test a link that explicitly omits the paintseed field (should default to 0)
        link = "steam://run/730//+csgo_econ_action_preview%2081915B282B79C699A9A17C80A982B185B9467A585F82E9020101018DF185AEA6C671"
        data = cs2inspect.parse(link)

        self.assertIn('paintseed', data)
        self.assertEqual(data['paintseed'], 0)
        self.assertEqual(data['defindex'], 40)
        self.assertEqual(data['paintindex'], 253)

if __name__ == '__main__':
    unittest.main()
