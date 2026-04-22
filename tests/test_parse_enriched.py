import unittest
from pathlib import Path

import cs2inspect


class TestEnrichedParsing(unittest.TestCase):
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

    def test_souvenir_dragon_lore(self):
        self.skip_if_no_schema()
        link = "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%2000180920D8022806300C38A3F3C2EB0340D101620A080010AC011D00000000620A0801108F011D00000000620A0802108B011D0000000062090803103C1D00000000E605A3C0"
        res = cs2inspect.parse(link, schema=self.schema)

        expected = {
            "defindex": 9,
            "paintindex": 344,
            "rarity": 6,
            "quality": 12,
            "paintwear": 1030797731,
            "paintseed": 209,
            "stickers": [
                {
                    "slot": 0,
                    "sticker_id": 172,
                    "codename": "cologne2014_esl_c",
                    "material": "econ/stickers/cologne2014/esl_c",
                    "name": "Sticker | ESL One Cologne 2014 (Gold)",
                    "imageurl": "https://cdn.steamstatic.com/apps/730/icons/econ/stickers/cologne2014/esl_c.10931e51b1bc7dbfa327168a517ce74337f9092c.png",
                    "wear": 0.0,
                },
                {
                    "slot": 1,
                    "sticker_id": 143,
                    "codename": "cologne2014_ibuypower_holo",
                    "material": "econ/stickers/cologne2014/ibuypower_holo",
                    "name": "Sticker | iBUYPOWER (Holo) | Cologne 2014",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMmuOXSQ61MnpNagpVDlVAThkYHl7x1T4P6hJqU0dqfKWWHCmbZz5Lc4Hyrjwk0j4zuGn9moJCnGbwYjWcRwFu5Y5hWm0oqwCnjbiRQ",
                    "collection_name": "ESL One Cologne 2014 Challengers",
                    "wear": 0.0,
                },
                {
                    "slot": 2,
                    "sticker_id": 139,
                    "codename": "cologne2014_datteam_holo",
                    "material": "econ/stickers/cologne2014/datteam_holo",
                    "name": "Sticker | dAT team (Holo) | Cologne 2014",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMmuOXSQ61MnpNagpV3mVQn0n5vf9S1X4LyrPPc8dfKWXWLCwrZw5-VoSSyxlkwl5z_WnI36dX7DagMmWJslRLRbrFDmxb6Jc4yR",
                    "collection_name": "ESL One Cologne 2014 Challengers",
                    "wear": 0.0,
                },
                {
                    "slot": 3,
                    "sticker_id": 60,
                    "codename": "kat2014_ibuypower_holo",
                    "material": "econ/stickers/emskatowice2014/ibuypower_holo",
                    "name": "Sticker | iBUYPOWER (Holo) | Katowice 2014",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjM-sJnCW8Vli_YTxuAm2FVL4nIP57S1M6uCRYKthL77KW2XAkr91tLQ-S33iwhly62jcn9yrcy2fOlBxA5JyRuVf40W7xoC2Kaq8sK3FB_Eg",
                    "collection_name": "EMS Katowice 2014 Challengers",
                    "wear": 0.0,
                },
            ],
            "floatvalue": 0.058770786970853806,
            "wear_name": "Factory New",
            "rarity_name": "Covert",
            "quality_name": "Souvenir",
            "weapon_type": "AWP",
            "item_name": "Dragon Lore",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3UqlXOLrxM-vMGmW8VNxu5Dx60noTyLwiYbf_jdk4veqYaF7IfysCnWRxuF4j-B-Xxa_nBovp3Pdwtj9cC_GaAd0DZdwQu9fuhS4kNy0NePntVTbjYpCyyT_3CgY5i9j_a9cBkcCWUKV",
            "min": 0,
            "max": 0.7,
            "collection_name": "The Cobblestone Collection",
            "full_item_name": "Souvenir AWP | Dragon Lore (Factory New)",
        }
        self.assertEqual(res, expected)

    def test_stattrak_gut_knife(self):
        self.skip_if_no_schema()
        link = "steam://run/730//+csgo_econ_action_preview%207363FED6ABCEDA726B897053D7705B7543704BD384AF937033DD703B7323731BF0F3F3F37F037B6DC7A246"
        res = cs2inspect.parse(link, schema=self.schema)

        expected = {
            "itemid": 45494964877,
            "defindex": 506,
            "paintindex": 420,
            "rarity": 6,
            "quality": 3,
            "paintwear": 1008155552,
            "paintseed": 430,
            "killeaterscoretype": 0,
            "killeatervalue": 0,
            "inventory": 3221225475,
            "origin": 8,
            "floatvalue": 0.00923052430152893,
            "wear_name": "Factory New",
            "rarity_name": "Covert",
            "origin_name": "Found in Crate",
            "quality_name": "★",
            "weapon_type": "Gut Knife",
            "item_name": "Doppler",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3UqlXOLrxM-vMGmW8VNxu5Dx60noTyL6kJ_m-B1c-uaRaalSJP-DHmuV09FmuOB6SnqMmRQguynLw96hIC2VagV0W5dzQ7VYsBiwldyyZO3m5VaLiN8WxXmt33sd5y5j4vFCD_RERtuZEw",
            "min": 0,
            "max": 0.08,
            "collection_name": "The Chroma Collection",
            "full_item_name": "★ StatTrak™ Gut Knife | Doppler (Factory New)",
        }
        self.assertEqual(res, expected)

    def test_specialist_gloves(self):
        self.skip_if_no_schema()
        link = "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%200018AA27209E0B2806300338E2F182F00340024BDF3FA4"
        res = cs2inspect.parse(link, schema=self.schema)

        expected = {
            "defindex": 5034,
            "paintindex": 1438,
            "rarity": 6,
            "quality": 3,
            "paintwear": 1040234722,
            "paintseed": 2,
            "floatvalue": 0.1257052719593048,
            "wear_name": "Minimal Wear",
            "rarity_name": "Covert",
            "quality_name": "★",
            "weapon_type": "Specialist Gloves",
            "item_name": "Pillow Punchers",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3UqlXOLrxM-vMGmW8VNxu5Tk71ruQBH4jYLf-i5U-fe9V6NhL-aWMXSAxO1_se1gXD2MhAguvymAnrDuKSLTO2l8U8UoAfkK5BKxkNyyZu7r4VGP3Y8UzSX_iC4av3trtbtWV_Vxq6SEh1mVN7c9_9Bdc6ulT-fJ",
            "min": 0.06,
            "max": 0.8,
            "collection_name": "The Dead Hand Collection",
            "full_item_name": "★ Specialist Gloves | Pillow Punchers (Minimal Wear)",
        }
        self.assertEqual(res, expected)

    def test_agent_ricksaw_with_patch(self):
        self.skip_if_no_schema()
        link = "steam://run/730//+csgo_econ_action_preview%20ACBC2675184201ADB430868CAC84AA9CA8CEA6A4ADBC408F899E512593C486DCBB45C46EBD"
        res = cs2inspect.parse(link, schema=self.schema)

        expected = {
            "itemid": 46670883978,
            "defindex": 5404,
            "paintindex": 0,
            "rarity": 6,
            "quality": 4,
            "inventory": 42,
            "origin": 23,
            "paintseed": 0,
            "paintwear": 0,
            "stickers": [
                {
                    "slot": 1,
                    "sticker_id": 4588,
                    "codename": "patch_suprememaster",
                    "material": "econ/patches/case_skillgroups/patch_suprememaster",
                    "name": "Patch | Metal Supreme Master",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJW3z0i4VeWbwMuyMESE7l95-IDm5Uz3UlLhn4Lj9R1I-uK8baloLfGAGmKCj-0j5LlrG3Dnxkpz5WnRmdirdnuSaVMlA5R5Q-MOukG4xILgMbvm4lPAy9USsZqlN38",
                    "collection_name": "Metal Skill Group Patch Collection",
                    "wear": 0.0,
                    "scale": 1.0780394077301025,
                }
            ],
            "floatvalue": 0.0,
            "rarity_name": "Master",
            "origin_name": "Quest Reward",
            "quality_name": "Unique",
            "weapon_type": "Lt. Commander Ricksaw | NSWC SEAL",
            "collection_name": "Shattered Web Agents",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIa-2lmxU-LR0dnuNm6E8Vl45Iv181z1fh7lk6nz6XRk-fO8YaVjNPndVz-Ul74hsbNoHi21kUly6mrQzNagcijBPQEnCsciTOdY4Rm6m4XvN_SiuVLIl2LQXw",
            "full_item_name": "Lt. Commander Ricksaw | NSWC SEAL",
        }
        self.assertEqual(res, expected)

    def test_standalone_sticker_liquid(self):
        self.skip_if_no_schema()
        link = "steam://run/730//+csgo_econ_action_preview%20889888903181A888A08CB88CEA8D8088984193E088F880F5194CD2"
        res = cs2inspect.parse(link, schema=self.schema)

        expected = {
            "itemid": 0,
            "defindex": 1209,
            "paintindex": 0,
            "rarity": 4,
            "quality": 4,
            "inventory": 0,
            "origin": 8,
            "paintseed": 0,
            "paintwear": 0,
            "stickers": [],
            "floatvalue": 0.0,
            "rarity_name": "Remarkable",
            "origin_name": "Found in Crate",
            "quality_name": "Unique",
            "weapon_type": "Sticker",
            "item_name": "Team Liquid (Holo) | Katowice 2019",
            "full_item_name": "Sticker | Team Liquid (Holo) | Katowice 2019",
            "collection_name": "Katowice 2019 Legends (Holo/Foil)",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMGgIXSA7FVwptelsxbrSAzOlpns8mwLufGoPfE_dfWWDz6WmLkl6eNtHXqxkE506jvQz92td3KeawN0D5t5W6dU5XuG2_2o",
        }
        self.assertEqual(res, expected)

    def test_m4a1s_hot_rod_with_charm_sticker_slab(self):
        self.skip_if_no_schema()
        link = "steam://run/730//+csgo_econ_action_preview%2080902F68726C3C8198BCA03D83A885B084B8014B626683C05B87E8DEF084228196888090A5BDDAF600BFC5BD6E44BECD0AF47BC0E000A20C63A9EA"
        res = cs2inspect.parse(link, schema=self.schema)

        expected = {
            "itemid": 50694239279,
            "defindex": 60,
            "paintindex": 445,
            "rarity": 5,
            "quality": 4,
            "paintwear": 1020831105,
            "paintseed": 987,
            "inventory": 94,
            "origin": 4,
            "keychains": [
                {
                    "slot": 0,
                    "sticker_id": 4352,
                    "codename": "berlin2019_signature_dickstacy_foil",
                    "material": "econ/stickers/berlin2019/sig_dickstacy_foil_1355_37",
                    "name": "Sticker Slab | DickStacy (Foil) | Berlin 2019",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMikJ3ee6wQlpd67-VDgfhn4nZ3z6SNY9s2oZ61hH6HAWzKvkrk457doTSjjkB516znXytj9JS6WbVMiX8F0Re4IskKwk4flNrvqsgLd3ZUFk3uXVEUc9A",
                    "wear": 0.0,
                    "offset_x": 1.0036118030548096,
                    "offset_y": 0.38463011384010315,
                    "offset_z": 7.857975959777832,
                    "wrapped_sticker": 4352,
                }
            ],
            "floatvalue": 0.026446105912327766,
            "wear_name": "Factory New",
            "rarity_name": "Classified",
            "origin_name": "Crafted",
            "quality_name": "Unique",
            "weapon_type": "M4A1-S",
            "item_name": "Hot Rod",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3UqlXOLrxM-vMGmW8VNxu5Dx60noTyL8ypexwjFS4_ega6F_H_GdMXWVxdF75OA4XBa_nBovp3PXyt2uJ32QaQciDZUhReUM5hLskdy2Pu_n4wLe2doXm3j-2i5A7X5i_a9cBuWkb97d",
            "min": 0,
            "max": 0.08,
            "collection_name": "The Chop Shop Collection",
            "full_item_name": "M4A1-S | Hot Rod (Factory New)",
        }
        self.assertEqual(res, expected)
        # Base rarity of the weapon is not verified here as it is tested elsewhere

    def test_ak47_slate_full_enrichment(self):
        self.skip_if_no_schema()
        # AK-47 | Slate with 5 Gold Stickers and Magmatude Charm
        link = "steam://run/730//+csgo_econ_action_preview%200D1DC5E9CAE5BB0C150A2D860525093D043599ADABE20E4DBB0E450D5DD0076F19050C1DD43510C0C1013230710D96B0488D33ABB66F19050D1DD0351030071A3230BD25CAB0480D99D8376F19050E1DE03510C0C1013230D0F0A73348ED1813316F19050E1DE4351088E61C3230FBB9443348F58BAA306F19050F1D9C341088E61C3230014B1A33484DE99EB6650C7D05AF0C1A050D1D2230EC64104C4828251932404AB2884D5D8E880CEBE9FCE9"
        res = cs2inspect.parse(link, schema=self.schema)

        expected = {
            "itemid": 49074532936,
            "defindex": 7,
            "paintindex": 1035,
            "rarity": 4,
            "quality": 9,
            "paintwear": 1038716948,
            "paintseed": 438,
            "killeaterscoretype": 0,
            "killeatervalue": 1373,
            "inventory": 1,
            "origin": 8,
            "stickers": [
                {
                    "slot": 1,
                    "sticker_id": 7257,
                    "codename": "cph2024_team_navi_gold",
                    "material": "econ/stickers/cph2024/navi_gold",
                    "name": "Sticker | Natus Vincere (Gold) | Copenhagen 2024",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMmxPSnHtwI6-obi42bgThH10JWwqHQDu6f4PPU8IfLFDWLAlOtysuQwSiyywB8hsT6BzYz9c3LDOwY-Sswn4fCOG2o",
                    "collection_name": "Copenhagen 2024 Legends Sticker Capsule",
                    "wear": 0.550000011920929,
                    "offset_x": -0.07568451762199402,
                    "offset_y": -0.005073368549346924,
                },
                {
                    "slot": 0,
                    "sticker_id": 7261,
                    "codename": "cph2024_team_vp_gold",
                    "material": "econ/stickers/cph2024/vp_gold",
                    "name": "Sticker | Virtus.pro (Gold) | Copenhagen 2024",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMmxPSnHtwI64pfL7VbrRVPwyJflqnNfv6StOf05cKmXV2SWxLdytrM7GnHqkU8l52nUmImqd3mWcEZ-XUXT9D_W",
                    "collection_name": "Copenhagen 2024 Legends Sticker Capsule",
                    "wear": 0.5899999737739563,
                    "offset_x": -0.09724557399749756,
                    "offset_y": 0.001629471778869629,
                },
                {
                    "slot": 3,
                    "sticker_id": 7277,
                    "codename": "cph2024_team_vita_gold",
                    "material": "econ/stickers/cph2024/vita_gold",
                    "name": "Sticker | Vitality (Gold) | Copenhagen 2024",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMmxPSnHtwI64o7g62bgThH10M7ipHZdvKT9MPQ6JvWQDz-Sl-pytLQ6GC_gzEtw62zVyY39eH2WbwA-SswneFne1lk",
                    "collection_name": "Copenhagen 2024 Legends Sticker Capsule",
                    "wear": 0.550000011920929,
                    "offset_x": 0.33396807312965393,
                    "offset_y": 0.009648770093917847,
                },
                {
                    "slot": 3,
                    "sticker_id": 7273,
                    "codename": "cph2024_team_spir_gold",
                    "material": "econ/stickers/cph2024/spir_gold",
                    "name": "Sticker | Team Spirit (Gold) | Copenhagen 2024",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMmxPSnHtwI655f9-GbgThH10MGw-HIKv6T6baFucfPFC2KUkO905uRvGnrllkp-5TjQzo6qJH6XPFM-SswnKK8h7Zw",
                    "collection_name": "Copenhagen 2024 Legends Sticker Capsule",
                    "wear": 0.5699999928474426,
                    "offset_x": 0.1969793736934662,
                    "offset_y": 0.08180040121078491,
                },
                {
                    "slot": 2,
                    "sticker_id": 7313,
                    "codename": "cph2024_team_gl_gold",
                    "material": "econ/stickers/cph2024/gl_gold",
                    "name": "Sticker | GamerLegion (Gold) | Copenhagen 2024",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMmxPSnHtwI684vL7VbrRVP1x5K1rHoOu6P-PPY6JfHKXTLEmOovs-M4S3HjkElz5DuBydmsJXuVcEZ-XYJJFe58",
                    "collection_name": "Copenhagen 2024 Challengers Sticker Capsule",
                    "wear": 0.5699999928474426,
                    "offset_x": 0.14772814512252808,
                    "offset_y": -0.004513293504714966,
                },
            ],
            "keychains": [
                {
                    "slot": 0,
                    "sticker_id": 47,
                    "codename": "kc_missinglink_lilhothead",
                    "material": "econ/keychains/missinglink_community_01/kc_missinglink_lilhothead",
                    "name": "Charm | Magmatude",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGI6zwki4Uf_a0IWsPGiE7Fhy-I764WbkThD8i5jp6Ttkv6PhY6dSLfmAHW6exuJ_vupWQyC_nRIzuziEnsGgJymSZwd0CZpyQu5buxO9wNbmPrzm5wCLg95Fmyz_3y1Nuydq4OZXT-N7raqdv_up",
                    "collection_name": "Missing Link Community Charm Collection",
                    "wear": 0.0,
                    "offset_x": 9.838349342346191,
                    "offset_y": 0.5787375569343567,
                    "offset_z": 4.179599285125732,
                    "pattern": 17027,
                }
            ],
            "floatvalue": 0.11404433846473694,
            "wear_name": "Minimal Wear",
            "rarity_name": "Restricted",
            "origin_name": "Found in Crate",
            "quality_name": "StatTrak™",
            "weapon_type": "AK-47",
            "item_name": "Slate",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3UqlXOLrxM-vMGmW8VNxu5Dx60noTyLwlcK3wiVI0POlPPNSMOKcCGKD0ud5vuBlcCW6khUz_W3Sytb4cCqTOFUpWJtzTOUD5hPsw9a0Yrnrs1SK3ooXzy6shilM5311o7FVYrIufmI",
            "min": 0,
            "max": 1,
            "collection_name": "The Snakebite Collection",
            "full_item_name": "StatTrak™ AK-47 | Slate (Minimal Wear)",
        }

        # Exhaustive 1:1 Parity Check
        self.assertEqual(res, expected)

    def test_modify_m4a4_howl_with_charm(self):
        self.skip_if_no_schema()
        # Original M4A4 | Howl (StatTrak, Contraband)
        original_link = "steam://run/730//+csgo_econ_action_preview%204F5FD39F99841E575F6FFA4D67487F46779CF4C1BB4C0FF248074F1F4F2D4B474C5F2827CCCFCFCF433F471FBECC3E"

        # 1. Unlink to get protobuf
        proto = cs2inspect.unlink(original_link)
        self.assertEqual(proto.defindex, 16)  # M4A4
        self.assertEqual(proto.paintindex, 309)  # Howl

        # 2. Add Charm (Magmatude ID 47) using Builder/Protobuf
        proto.keychains.add(
            slot=0,
            sticker_id=47,
            offset_x=4.5,
            offset_y=0.5,
            offset_z=8.9,
        )

        # 3. Generate new masked link
        new_link = cs2inspect.link(proto)

        # 4. Parse new link with enrichment and verify EVERYTHING
        res = cs2inspect.parse(new_link, schema=self.schema)

        expected = {
            "itemid": 21901977628,
            "defindex": 16,
            "paintindex": 309,
            "rarity": 7,
            "quality": 9,
            "paintwear": 1048813011,
            "paintseed": 957,
            "killeaterscoretype": 0,
            "killeatervalue": 0,
            "inventory": 3221225475,
            "origin": 8,
            "stickers": [
                {
                    "slot": 3,
                    "sticker_id": 103,
                    "codename": "comm01_howling_dawn",
                    "material": "econ/stickers/community01/howling_dawn",
                    "name": "Sticker | Howling Dawn",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMmuOHaC619h7delpVHoVhH4kJHf-SNM4bz9bKY_dPWQWDCUkLxy57g_H3DgkB5w42uAzIv4I3meOAQlApdwFO5YrFDmxUNp_lL7",
                    "wear": 0.0,
                }
            ],
            "keychains": [
                {
                    "slot": 0,
                    "sticker_id": 47,
                    "codename": "kc_missinglink_lilhothead",
                    "material": "econ/keychains/missinglink_community_01/kc_missinglink_lilhothead",
                    "name": "Charm | Magmatude",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGI6zwki4Uf_a0IWsPGiE7Fhy-I764WbkThD8i5jp6Ttkv6PhY6dSLfmAHW6exuJ_vupWQyC_nRIzuziEnsGgJymSZwd0CZpyQu5buxO9wNbmPrzm5wCLg95Fmyz_3y1Nuydq4OZXT-N7raqdv_up",
                    "collection_name": "Missing Link Community Charm Collection",
                    "wear": 0.0,
                    "offset_x": 4.5,
                    "offset_y": 0.5,
                    "offset_z": 8.899999618530273,
                    "pattern": 0,
                }
            ],
            "floatvalue": 0.25706347823143005,
            "wear_name": "Field-Tested",
            "rarity_name": "Contraband",
            "origin_name": "Found in Crate",
            "quality_name": "StatTrak™",
            "weapon_type": "M4A4",
            "item_name": "Howl",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3UqlXOLrxM-vMGmW8VNxu5Dx60noTyL8ypexwiFO0P_6afVSKP-EAm6extF7teVgWiT9wh5_5zyAwo6oeSrDawUkCMN0QbEM5BO-wNazMe3qsgHZg4wQyy-t2jQJsHi3nDJ37A",
            "min": 0,
            "max": 0.4,
            "full_item_name": "StatTrak™ M4A4 | Howl (Field-Tested)",
        }
        self.assertEqual(res, expected)

    def test_custom_placement_stickers_and_charms(self):
        self.skip_if_no_schema()
        # Example with custom placements (M4A1-S | Cyrex)
        link = "steam://run/730//+csgo_econ_action_preview%209D8D390E592F379C85A1BD759FB59BAD94A5215634729EDDCCD59DCD439EFF98959C8D50B9FF98959F8D50B9FF98959E8D50B9FF8995998D41D8B09D9D5D5DA01F3546A3D8811D57A0FF9295998D75D8A0567616A3D89DE9CF27F5F2ED953F9C8B959D8DB9A0834170DDD85EFB4FA3D02D672BDDC56A9F56EC4C0C"
        res = cs2inspect.parse(link, schema=self.schema)

        expected = {
            "itemid": 45740001700,
            "defindex": 60,
            "paintindex": 360,
            "rarity": 6,
            "quality": 9,
            "paintwear": 1038771644,
            "paintseed": 81,
            "killeaterscoretype": 0,
            "killeatervalue": 478,
            "inventory": 111,
            "origin": 8,
            "stickers": [
                {
                    "slot": 1,
                    "sticker_id": 4685,
                    "codename": "broken_fang_battle_scarred",
                    "material": "econ/stickers/broken_fang/battle_scarred",
                    "name": "Sticker | Battle Scarred",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMizOnCS62lz9YnzpVvmVQn9m6nz_iNJ_feqJv09eKfKWGbDkeh1sbVtFnC2xE9_4mvdwtf9IHmVPFN0A5QmRuID5EOm0oqw3DPInuo",
                    "collection_name": "Broken Fang Sticker Collection",
                    "wear": 0.0,
                },
                {
                    "slot": 2,
                    "sticker_id": 4685,
                    "codename": "broken_fang_battle_scarred",
                    "material": "econ/stickers/broken_fang/battle_scarred",
                    "name": "Sticker | Battle Scarred",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMizOnCS62lz9YnzpVvmVQn9m6nz_iNJ_feqJv09eKfKWGbDkeh1sbVtFnC2xE9_4mvdwtf9IHmVPFN0A5QmRuID5EOm0oqw3DPInuo",
                    "collection_name": "Broken Fang Sticker Collection",
                    "wear": 0.0,
                },
                {
                    "slot": 3,
                    "sticker_id": 4685,
                    "codename": "broken_fang_battle_scarred",
                    "material": "econ/stickers/broken_fang/battle_scarred",
                    "name": "Sticker | Battle Scarred",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMizOnCS62lz9YnzpVvmVQn9m6nz_iNJ_feqJv09eKfKWGbDkeh1sbVtFnC2xE9_4mvdwtf9IHmVPFN0A5QmRuID5EOm0oqw3DPInuo",
                    "collection_name": "Broken Fang Sticker Collection",
                    "wear": 0.0,
                },
                {
                    "slot": 4,
                    "sticker_id": 8924,
                    "codename": "aus2025_signature_ex3rcice_1_foil",
                    "material": "econ/stickers/aus2025/sig_ex3rcice_foil",
                    "name": "Sticker | Ex3rcice (Foil) | Austin 2025",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMu0JinHtwM6547z1Vz_Eg_yl5XlwiRU5v7gOvM_eKeWWz6WmLZ05LdsGn61k0Uh5jnSzIuqJS3DPwF2AsZ4ReAN5w74zIOfgBGfzg",
                    "collection_name": "Austin 2025 Challengers Autograph Capsule",
                    "wear": 0.0,
                    "rotation": -6.0,
                    "offset_x": 0.4290199875831604,
                    "offset_y": 0.09887716174125671,
                },
                {
                    "slot": 4,
                    "sticker_id": 8936,
                    "codename": "aus2025_signature_bodyy_1_foil",
                    "material": "econ/stickers/aus2025/sig_bodyy_foil",
                    "name": "Sticker | bodyy (Foil) | Austin 2025",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMu0JinHtwM6547z1VvoRQTooZDv9C4V6ausPv0_dqPLV2bHmLwu5eBoTXrnx0V-4GrTmYuqeXKUPwMlDZJ3E_lK7EeLoenddg",
                    "collection_name": "Austin 2025 Challengers Autograph Capsule",
                    "wear": 0.0,
                    "offset_x": 0.27328333258628845,
                    "offset_y": -0.0008028149604797363,
                },
            ],
            "keychains": [
                {
                    "slot": 0,
                    "sticker_id": 36,
                    "codename": "souvenir_highlight",
                    "material": "econ/keychains/aus2025/kc_aus2025",
                    "name": "Souvenir Charm | Austin 2025 Highlight | apEX: Help Is Here",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGI6zwki4Uf_a0IWgIGjFtQQgu4z31VjyUk-hzMOu-3APtqX8a_U6c6SRW2TGlL4k5uI-TXzhxEUm6mqDzN2pcC6WZwR0A4wwG7BUDwUFHQ",
                    "collection_name": "Austin 2025",
                    "wear": 0.0,
                    "offset_x": 7.433119773864746,
                    "offset_y": 0.4109402596950531,
                    "offset_z": 5.718101501464844,
                    "highlight_reel": 375,
                }
            ],
            "floatvalue": 0.11445185542106628,
            "wear_name": "Minimal Wear",
            "rarity_name": "Covert",
            "origin_name": "Found in Crate",
            "quality_name": "StatTrak™",
            "weapon_type": "M4A1-S",
            "item_name": "Cyrex",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3UqlXOLrxM-vMGmW8VNxu5Dx60noTyL8ypexwjFS4_ega6F_H_OGMWrEwL9lj-JwXSyrqhEutDWR1N77cimSbQQgC8F5QLYCsELpltTnZuvk7wbcjdhDzy_43yMb6ilvt7kcEf1yDWu2yf8",
            "min": 0,
            "max": 0.5,
            "collection_name": "The Breakout Collection",
            "full_item_name": "StatTrak™ M4A1-S | Cyrex (Minimal Wear)",
        }
        self.assertEqual(res, expected)

    def test_m4a1s_solitude_complex_enrichment(self):
        self.skip_if_no_schema()
        # M4A1-S | Solitude with Vitality Holo, 3x FlameZ Gold, and Souvenir Charm
        link = "steam://run/730//+csgo_econ_action_preview%20B7A756531C120DB6AF8B970DBD9FB287B38F58302D44B4F732B1D5A3BFB3A76984AA13C78A888A6D1F6189F2B7AB298BD5AEBFB3A768FEAA8484C4889AB7B7C7F68A508E6689F2B7CFEF8ED5AEBFB3A768FEAA419FEB889AB7B777F78A60196189F20F6EBD8AD5AEBFB3A768FEAA8ABDE0889AB7B7A7F68A28746489F2D760C18BDF34373737BBC7A015B6A1BFB7A7938A1CBBCE88F21B511E89FA990F5CF7EF74B575FCB257"
        res = cs2inspect.parse(link, schema=self.schema)

        expected = {
            "itemid": 50007306849,
            "defindex": 60,
            "paintindex": 1338,
            "rarity": 5,
            "quality": 4,
            "paintwear": 1046905839,
            "paintseed": 773,
            "inventory": 3221225475,
            "origin": 23,
            "stickers": [
                {
                    "slot": 4,
                    "sticker_id": 6622,
                    "codename": "paris2023_team_vita_holo",
                    "material": "econ/stickers/paris2023/vita_holo",
                    "name": "Sticker | Vitality (Holo) | Paris 2023",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjNqgJ3KEtwYnp8ji403mfhX-kpmuqnUKv_aoMaFocfTGXjeSxOwi6LlsTi2ywR4ksTyHyYyuc3OTZ1cpC4wwG7DqvnpuVg",
                    "collection_name": "Paris 2023 Legends Sticker Capsule",
                    "wear": 0.7400000095367432,
                    "offset_x": 0.4192569851875305,
                    "offset_y": 0.019300460815429688,
                },
                {
                    "slot": 4,
                    "sticker_id": 9439,
                    "codename": "aus2025_signature_flamez_32",
                    "material": "econ/stickers/aus2025/sig_flamez_champion",
                    "name": "Sticker | FlameZ (Champion) | Austin 2025",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMu0JinHtwM6547z1V_rQBD0hKnj9SNW__uhZuo_efXHDGGWwO0vs-U6SnuywUoitmzdyNavIy6QblUjCpQhQuIJ5hTujJS5YB_Eu2hd",
                    "collection_name": "Austin 2025 Champions Autograph Capsule",
                    "wear": 0.949999988079071,
                    "rotation": 15.0,
                    "offset_x": 0.4086448848247528,
                    "offset_y": 0.00020644068717956543,
                },
                {
                    "slot": 4,
                    "sticker_id": 9439,
                    "codename": "aus2025_signature_flamez_32",
                    "material": "econ/stickers/aus2025/sig_flamez_champion",
                    "name": "Sticker | FlameZ (Champion) | Austin 2025",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMu0JinHtwM6547z1V_rQBD0hKnj9SNW__uhZuo_efXHDGGWwO0vs-U6SnuywUoitmzdyNavIy6QblUjCpQhQuIJ5hTujJS5YB_Eu2hd",
                    "collection_name": "Austin 2025 Champions Autograph Capsule",
                    "wear": 0.8600000143051147,
                    "rotation": 6.0,
                    "offset_x": 0.41930267214775085,
                    "offset_y": 0.03389903903007507,
                },
                {
                    "slot": 4,
                    "sticker_id": 9439,
                    "codename": "aus2025_signature_flamez_32",
                    "material": "econ/stickers/aus2025/sig_flamez_champion",
                    "name": "Sticker | FlameZ (Champion) | Austin 2025",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMu0JinHtwM6547z1V_rQBD0hKnj9SNW__uhZuo_efXHDGGWwO0vs-U6SnuywUoitmzdyNavIy6QblUjCpQhQuIJ5hTujJS5YB_Eu2hd",
                    "collection_name": "Austin 2025 Champions Autograph Capsule",
                    "wear": 0.8399999737739563,
                    "rotation": 9.0,
                    "offset_x": 0.4136018455028534,
                    "offset_y": 0.015065997838973999,
                },
            ],
            "keychains": [
                {
                    "slot": 0,
                    "sticker_id": 36,
                    "codename": "souvenir_highlight",
                    "material": "econ/keychains/aus2025/kc_aus2025",
                    "name": "Souvenir Charm | Austin 2025 Highlight | flameZ Double Train Kill",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGI6zwki4Uf_a0IWgIGjFtQQgu4z31VjyUk-hzMOu-3APtqX8a_U6c6SRW2TGlL4k5uI-TXzhxEUm6mqDzN2pcC6WZwR0A4wwG7BUDwUFHQ",
                    "collection_name": "Austin 2025",
                    "wear": 0.0,
                    "offset_x": 0.9728495478630066,
                    "offset_y": 0.3318380117416382,
                    "offset_z": 7.366232872009277,
                    "highlight_reel": 323,
                }
            ],
            "floatvalue": 0.2251126617193222,
            "wear_name": "Field-Tested",
            "rarity_name": "Classified",
            "origin_name": "Quest Reward",
            "quality_name": "Unique",
            "weapon_type": "M4A1-S",
            "item_name": "Solitude",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3UqlXOLrxM-vMGmW8VNxu5Dx60noTyL8ypexwjFS4_ega6F_H-OcDW-vzOFjvvVoRiegqhBzsmyWpYL8JSLSMxgmXJB5Qe8O5hLrkoDlNOix5wTcg4JHzXr5inxJvy5vtr4CV6Ytq63fkUifZonb9V4d",
            "min": 0,
            "max": 0.7,
            "collection_name": "Limited Edition Item",
            "full_item_name": "M4A1-S | Solitude (Field-Tested)",
        }

        # Exhaustive 1:1 Parity Check
        self.assertEqual(res, expected)

    def test_m4a1s_black_lotus_with_sticker_slab_collision(self):
        self.skip_if_no_schema()
        # M4A1-S | Black Lotus with Sticker Slab wrapping Lucky 13 (ID 13 collision)
        # Verify it resolves to "Lucky 13" slab, not "Dinner Dog" charm.
        link = "steam://run/730//+csgo_econ_action_preview%208292215C625139839ABEA20C8BAA87B286BA1F003E7B81C24C84EA90F28A2083978A8292A7BFD6EC02BDC718642BBCCF47CE6FC2E28FBBF3E916"
        res = cs2inspect.parse(link, schema=self.schema)

        expected = {
            "itemid": 50373078819,
            "defindex": 60,
            "paintindex": 1166,
            "rarity": 5,
            "quality": 4,
            "paintwear": 1060045085,
            "paintseed": 846,
            "inventory": 18,
            "origin": 8,
            "keychains": [
                {
                    "slot": 0,
                    "sticker_id": 13,
                    "codename": "std_thirteen",
                    "material": "econ/stickers/standard/thirteen_1355_37",
                    "name": "Sticker Slab | Lucky 13",
                    "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjNm1NHWT5ERxu5P840vzRBj_ocezqHdkvKXgOPw1dabBWTfBkL8ntrY8HXnjxR5-4DjXntioeX-WbAckCcBzE-MLsQ74zIMGCxgywg",
                    "wear": 0.0,
                    "offset_x": 1.0033669471740723,
                    "offset_y": 0.3318374752998352,
                    "offset_z": 7.415621280670166,
                    "wrapped_sticker": 13,
                }
            ],
            "floatvalue": 0.683610737323761,
            "wear_name": "Battle-Scarred",
            "weapon_type": "M4A1-S",
            "rarity_name": "Classified",
            "origin_name": "Found in Crate",
            "quality_name": "Unique",
            "item_name": "Black Lotus",
            "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3UqlXOLrxM-vMGmW8VNxu5Dx60noTyL8ypexwjFS4_ega6F_H_3HDzaD_ux6seJicCW8gQg0jDWAm5ngbynCalJyDpMlQONYtkPpldTlYr7qtAPc2NhByiX4jikav3tj5O4LU6A7uvqArAmeAQg",
            "min": 0,
            "max": 0.7,
            "collection_name": "The Kilowatt Collection",
            "full_item_name": "M4A1-S | Black Lotus (Battle-Scarred)",
        }

        self.assertEqual(res, expected)

    def test_m4a1s_black_lotus_with_diner_dog_charm_collision_proof(self):
        self.skip_if_no_schema()
        # 1. Start with the EXACT SAME Sticker Slab link as the test above
        link = "steam://run/730//+csgo_econ_action_preview%208292215C625139839ABEA20C8BAA87B286BA1F003E7B81C24C84EA90F28A2083978A8292A7BFD6EC02BDC718642BBCCF47CE6FC2E28FBBF3E916"

        # Parse original to get base data (to prove only keychains differ)
        slab_res = cs2inspect.parse(link, schema=self.schema)

        # 2. Unlink to get the protobuf
        proto = cs2inspect.unlink(link)

        # 3. Modify: Swap the Sticker Slab for a regular "Diner Dog" charm (ID 13)
        # We preserve the exact offsets from the original link for perfect parity.
        orig_kc = slab_res["keychains"][0]
        del proto.keychains[:]
        proto.keychains.add(
            slot=0,
            sticker_id=13,
            offset_x=orig_kc["offset_x"],
            offset_y=orig_kc["offset_y"],
            offset_z=orig_kc["offset_z"],
        )

        # 4. Generate new link and parse it
        new_link = cs2inspect.link(proto)
        res = cs2inspect.parse(new_link, schema=self.schema)

        # 5. Construct expected from original but with swapped keychain metadata
        expected = slab_res.copy()
        expected["keychains"] = [
            {
                "slot": 0,
                "sticker_id": 13,
                "codename": "kc_missinglink_sam_shape",
                "material": "econ/keychains/missinglink/kc_missinglink_sam_shape",
                "name": "Charm | Diner Dog",
                "imageurl": "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGI6zwki4Uf_a0IWsPGiE7Fhy-I764RbsQiL8l4Xz9Cxc4_ugY5t-If2sHW-R0es44ec6GCziw0om4W7TzNuqcX2UZg9xA5RzF-QDsRa9ktXvYevg7wPe2JUFk3ucEH-vmw",
                "collection_name": "Missing Link Charm Collection",
                "wear": 0.0,
                "offset_x": orig_kc["offset_x"],
                "offset_y": orig_kc["offset_y"],
                "offset_z": orig_kc["offset_z"],
                "pattern": 0,
            }
        ]

        # Verify full parity - the only difference should be the keychain info
        self.assertEqual(res, expected)


if __name__ == "__main__":
    unittest.main()
