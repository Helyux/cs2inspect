__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "26.10.2025"
__email__ = "m@hler.eu"
__status__ = "Development"


import unittest

import cs2inspect

EXPECTED_CONSOLE_1 = ("csgo_econ_action_preview "
                      "00180920C6092805388C89D6E803409305621408031094341D000000003D00623CBC4500930B"
                      "3B621908001094341D000000002D000034433DD94B92BE453037AFBD621408001094341D0000"
                      "00003DA82AFEBD4594C3A4BD621908001094341D000000002D000034C33D704BD3BD45E810AE"
                      "BD621908041094341D6E00383F2D00002E433D583808BD45B05E363D32D14088")

EXPECTED_CONSOLE_2 = ("csgo_econ_action_preview "
                      "00180920D401280538AB8AD0E30340F4066209080310321D00000000A20118080010241D0000"
                      "00003D6E7D9040451A6B173F4D7B810E41839189F8")


class TestProtoBuilder(unittest.TestCase):

    def test_builder_rejects_invalid_sticker_entry(self):
        builder = cs2inspect.Builder(
            defindex=1,
            paintindex=2,
            paintseed=3,
            paintwear=0.1,
            rarity=0,
            stickers=[{"sticker_id": 10}],
        )

        with self.assertRaises(ValueError):
            builder.build()

    def test_builder_rejects_non_dict_sticker(self):
        builder = cs2inspect.Builder(
            defindex=1,
            paintindex=2,
            paintseed=3,
            paintwear=0.1,
            rarity=0,
            stickers=["invalid"],
        )

        with self.assertRaises(TypeError):
            builder.build()

    def test_console_command_matches_expected_payload(self):
        builder = cs2inspect.Builder(
            defindex=9,
            paintindex=1222,
            paintseed=659,
            paintwear=0.03650336,
            rarity=5,
            stickers=[
              {
                "slot": 3,
                "offset_x": -0.011497974395751953,
                "offset_y": 0.0021297335624694824,
                "sticker_id": 6676,
              },
              {
                "slot": 0,
                "rotation": 180,
                "offset_x": -0.2857349216938019,
                "offset_y": -0.08555448055267334,
                "sticker_id": 6676,
              },
              {
                "slot": 0,
                "offset_x": -0.12410479784011841,
                "offset_y": -0.08045116066932678,
                "sticker_id": 6676,
              },
              {
                "slot": 0,
                "rotation": -180,
                "offset_x": -0.10317122936248779,
                "offset_y": -0.08499318361282349,
                "sticker_id": 6676,
              },
              {
                "slot": 4,
                "wear": 0.7187565565109253,
                "rotation": 174,
                "offset_x": -0.033256858587265015,
                "offset_y": 0.04452389478683472,
                "sticker_id": 6676,
              }
            ],
        )

        proto = builder.build()
        console_command = cs2inspect.link_console(proto)
        self.assertEqual(console_command, EXPECTED_CONSOLE_1)

    def test_builder_adds_keychain_data(self):

        builder = cs2inspect.Builder(
            defindex=9,
            paintindex=212,
            paintseed=884,
            paintwear=0.01489381,
            rarity=5,
            stickers=[{
                "slot": 3,
                "sticker_id": 50,
            }],
            keychains=[{
                "slot": 0,
                "sticker_id": 36,
                "offset_x": 4.515311241149902,
                "offset_y": 0.5914779901504517,
                "offset_z": 8.906611442565918,
            }],
        )

        proto = builder.build()
        self.assertEqual(len(proto.keychains), 1)

        console_command = cs2inspect.link_console(proto)
        self.assertEqual(console_command, EXPECTED_CONSOLE_2)


if __name__ == '__main__':
    unittest.main()
