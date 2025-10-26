__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "26.10.2025"
__email__ = "m@hler.eu"
__status__ = "Development"


import unittest

import cs2inspect


class TestConsoleCommand(unittest.TestCase):

    def test_console_from_protobuf_matches_link_payload(self):
        builder = cs2inspect.Builder(
            defindex=9,
            paintindex=1222,
            paintseed=659,
            paintwear=0.03650335595011711,
            rarity=5,
            stickers=[{'slot': 2, 'sticker_id': 7203, 'wear': 0.0}],
        )
        proto = builder.build()

        console_command = cs2inspect.link_console(proto)
        inspect_link = cs2inspect.link(proto)
        self.assertIsNotNone(inspect_link)

        payload = inspect_link.split('%20', 1)[1]
        expected_command = f"csgo_econ_action_preview {payload}"
        self.assertEqual(console_command, expected_command)

    def test_console_from_dict_matches_link_payload(self):
        link_data = {
            'asset_id': '38350177019',
            'class_id': '9385506221951591925',
            'owner_id': '76561198066322090',
        }

        console_command = cs2inspect.link_console(link_data)
        inspect_link = cs2inspect.link(link_data)
        self.assertIsNotNone(inspect_link)

        payload = inspect_link.split('%20', 1)[1]
        expected_command = f"csgo_econ_action_preview {payload}"
        self.assertEqual(console_command, expected_command)

    def test_console_accepts_inspect_link_string(self):
        inspect_link = (
            "steam://rungame/730/76561202255233023/+"
            "csgo_econ_action_preview%20S76561198111020129A46325653038D13837422153024819341"
        )
        expected = (
            "csgo_econ_action_preview S76561198111020129A46325653038D13837422153024819341"
        )
        self.assertEqual(cs2inspect.link_console(inspect_link), expected)


if __name__ == '__main__':
    unittest.main()
