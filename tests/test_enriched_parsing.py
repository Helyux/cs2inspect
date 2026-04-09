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
        self.assertEqual(res["full_item_name"], "Souvenir AWP | Dragon Lore (Factory New)")
        self.assertEqual(res["collection_name"], "The Cobblestone Collection")
        self.assertEqual(res["imageurl"], "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3UqlXOLrxM-vMGmW8VNxu5Dx60noTyLwiYbf_jdk4veqYaF7IfysCnWRxuF4j-B-Xxa_nBovp3Pdwtj9cC_GaAd0DZdwQu9fuhS4kNy0NePntVTbjYpCyyT_3CgY5i9j_a9cBkcCWUKV")

    def test_stattrak_gut_knife(self):
        self.skip_if_no_schema()
        link = "steam://run/730//+csgo_econ_action_preview%207363FED6ABCEDA726B897053D7705B7543704BD384AF937033DD703B7323731BF0F3F3F37F037B6DC7A246"
        res = cs2inspect.parse(link, schema=self.schema)
        self.assertEqual(res["full_item_name"], "★ StatTrak™ Gut Knife | Doppler (Factory New)")
        self.assertEqual(res["collection_name"], "The Chroma Collection")
        self.assertEqual(res["imageurl"], "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3UqlXOLrxM-vMGmW8VNxu5Dx60noTyL6kJ_m-B1c-uaRaalSJP-DHmuV09FmuOB6SnqMmRQguynLw96hIC2VagV0W5dzQ7VYsBiwldyyZO3m5VaLiN8WxXmt33sd5y5j4vFCD_RERtuZEw")

    def test_specialist_gloves(self):
        self.skip_if_no_schema()
        link = "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%200018AA27209E0B2806300338E2F182F00340024BDF3FA4"
        res = cs2inspect.parse(link, schema=self.schema)
        self.assertEqual(res["full_item_name"], "★ Specialist Gloves | Pillow Punchers (Minimal Wear)")
        self.assertEqual(res["collection_name"], "The Dead Hand Collection")
        self.assertEqual(res["imageurl"], "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3UqlXOLrxM-vMGmW8VNxu5Tk71ruQBH4jYLf-i5U-fe9V6NhL-aWMXSAxO1_se1gXD2MhAguvymAnrDuKSLTO2l8U8UoAfkK5BKxkNyyZu7r4VGP3Y8UzSX_iC4av3trtbtWV_Vxq6SEh1mVN7c9_9Bdc6ulT-fJ")

    def test_agent_ricksaw_with_patch(self):
        self.skip_if_no_schema()
        link = "steam://run/730//+csgo_econ_action_preview%20ACBC2675184201ADB430868CAC84AA9CA8CEA6A4ADBC408F899E512593C486DCBB45C46EBD"
        res = cs2inspect.parse(link, schema=self.schema)
        self.assertEqual(res["full_item_name"], "Lt. Commander Ricksaw | NSWC SEAL")
        self.assertEqual(res["rarity_name"], "Master")
        self.assertEqual(res["collection_name"], "Shattered Web Agents")
        self.assertEqual(res["imageurl"], "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIa-2lmxU-LR0dnuNm6E8Vl45Iv181z1fh7lk6nz6XRk-fO8YaVjNPndVz-Ul74hsbNoHi21kUly6mrQzNagcijBPQEnCsciTOdY4Rm6m4XvN_SiuVLIl2LQXw")
        self.assertTrue(any(s["name"] == "Patch | Metal Supreme Master" for s in res["stickers"]))

    def test_standalone_sticker_liquid(self):
        self.skip_if_no_schema()
        link = "steam://run/730//+csgo_econ_action_preview%20889888903181A888A08CB88CEA8D8088984193E088F880F5194CD2"
        res = cs2inspect.parse(link, schema=self.schema)
        self.assertEqual(res["full_item_name"], "Sticker | Team Liquid (Holo) | Katowice 2019")
        self.assertEqual(res["rarity_name"], "Remarkable")
        self.assertEqual(res["imageurl"], "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGJai0ki7VeTHjMGgIXSA7FVwptelsxbrSAzOlpns8mwLufGoPfE_dfWWDz6WmLkl6eNtHXqxkE506jvQz92td3KeawN0D5t5W6dU5XuG2_2o")
        self.assertEqual(res["stickers"], []) # Hoisted and cleared

    def test_m4a1s_hot_rod_with_charm_sticker_slab(self):
        self.skip_if_no_schema()
        link = "steam://run/730//+csgo_econ_action_preview%2080902F68726C3C8198BCA03D83A885B084B8014B626683C05B87E8DEF084228196888090A5BDDAF600BFC5BD6E44BECD0AF47BC0E000A20C63A9EA"
        res = cs2inspect.parse(link, schema=self.schema)
        self.assertEqual(res["full_item_name"], "M4A1-S | Hot Rod (Factory New)")
        self.assertEqual(res["collection_name"], "The Chop Shop Collection")
        self.assertEqual(res["imageurl"], "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3UqlXOLrxM-vMGmW8VNxu5Dx60noTyL8ypexwjFS4_ega6F_H_GdMXWVxdF75OA4XBa_nBovp3PXyt2uJ32QaQciDZUhReUM5hLskdy2Pu_n4wLe2doXm3j-2i5A7X5i_a9cBuWkb97d")
        self.assertEqual(res["keychains"][0]["name"], "Sticker Slab | DickStacy (Foil) | Berlin 2019")
        # Note: We don't verify base rarity of the weapon here as it's tested elsewhere

    def test_ak47_slate_full_enrichment(self):
        self.skip_if_no_schema()
        # AK-47 | Slate with 5 Gold Stickers and Magmatude Charm
        link = "steam://run/730//+csgo_econ_action_preview%200D1DC5E9CAE5BB0C150A2D860525093D043599ADABE20E4DBB0E450D5DD0076F19050C1DD43510C0C1013230710D96B0488D33ABB66F19050D1DD0351030071A3230BD25CAB0480D99D8376F19050E1DE03510C0C1013230D0F0A73348ED1813316F19050E1DE4351088E61C3230FBB9443348F58BAA306F19050F1D9C341088E61C3230014B1A33484DE99EB6650C7D05AF0C1A050D1D2230EC64104C4828251932404AB2884D5D8E880CEBE9FCE9"
        res = cs2inspect.parse(link, schema=self.schema)

        # Base IDs
        self.assertEqual(res["itemid"], 49074532936)
        self.assertEqual(res["defindex"], 7)
        self.assertEqual(res["paintindex"], 1035)
        self.assertEqual(res["rarity"], 4)
        self.assertEqual(res["quality"], 9)
        self.assertEqual(res["paintwear"], 1038716948)
        self.assertEqual(res["paintseed"], 438)

        # KillEater (StatTrak)
        self.assertEqual(res["killeaterscoretype"], 0)
        self.assertEqual(res["killeatervalue"], 1373)

        # Meta
        self.assertEqual(res["inventory"], 1)
        self.assertEqual(res["origin"], 8)
        self.assertEqual(res["floatvalue"], 0.11404433846473694)

        # Enrichment Results
        self.assertEqual(res["full_item_name"], "StatTrak™ AK-47 | Slate (Minimal Wear)")
        self.assertEqual(res["collection_name"], "The Snakebite Collection")
        self.assertEqual(res["weapon_type"], "AK-47")
        self.assertEqual(res["item_name"], "Slate")
        self.assertEqual(res["wear_name"], "Minimal Wear")
        self.assertEqual(res["rarity_name"], "Restricted")
        self.assertEqual(res["quality_name"], "StatTrak™")
        self.assertEqual(res["origin_name"], "Found in Crate")
        self.assertEqual(res["imageurl"], "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3UqlXOLrxM-vMGmW8VNxu5Dx60noTyLwlcK3wiVI0POlPPNSMOKcCGKD0ud5vuBlcCW6khUz_W3Sytb4cCqTOFUpWJtzTOUD5hPsw9a0Yrnrs1SK3ooXzy6shilM5311o7FVYrIufmI")
        self.assertEqual(res["min"], 0)
        self.assertEqual(res["max"], 1)

        # Counts
        self.assertEqual(len(res["stickers"]), 5)
        self.assertEqual(len(res["keychains"]), 1)

        # Sticker Details (First one)
        sticker = res["stickers"][0]
        self.assertEqual(sticker["slot"], 1)
        self.assertEqual(sticker["stickerId"], 7257)
        self.assertEqual(sticker["name"], "Sticker | Natus Vincere (Gold) | Copenhagen 2024")
        self.assertEqual(sticker["collection_name"], "Copenhagen 2024 Legends Sticker Capsule")

        # Charm Details
        charm = res["keychains"][0]
        self.assertEqual(charm["slot"], 0)
        self.assertEqual(charm["stickerId"], 47)
        self.assertEqual(charm["name"], "Charm | Magmatude")
        self.assertEqual(charm["codename"], "kc_missinglink_lilhothead")
        self.assertEqual(charm["collection_name"], "Missing Link Community Charm Collection")

    def test_modify_m4a4_howl_with_charm(self):
        self.skip_if_no_schema()
        # Original M4A4 | Howl (StatTrak, Contraband)
        original_link = "steam://run/730//+csgo_econ_action_preview%204F5FD39F99841E575F6FFA4D67487F46779CF4C1BB4C0FF248074F1F4F2D4B474C5F2827CCCFCFCF433F471FBECC3E"

        # 1. Unlink to get protobuf
        proto = cs2inspect.unlink(original_link)
        self.assertEqual(proto.defindex, 16) # M4A4
        self.assertEqual(proto.paintindex, 309) # Howl

        # 2. Add Charm (Magmatude ID 47) using Builder/Protobuf
        proto.keychains.add(
            slot=0,
            sticker_id=47,
            offset_x=4.5,
            offset_y=0.5,
            offset_z=8.9
        )

        # 3. Generate new masked link
        new_link = cs2inspect.link(proto)

        # 4. Parse new link with enrichment and verify EVERYTHING
        res = cs2inspect.parse(new_link, schema=self.schema)

        # Base IDs
        self.assertEqual(res["defindex"], 16)
        self.assertEqual(res["paintindex"], 309)
        self.assertEqual(res["rarity"], 7)
        self.assertEqual(res["quality"], 9)
        self.assertEqual(res["paintwear"], 1048813011)
        self.assertEqual(res["paintseed"], 957)
        self.assertEqual(res["killeaterscoretype"], 0)
        self.assertEqual(res["killeatervalue"], 0)

        # Enrichment Results
        self.assertEqual(res["full_item_name"], "StatTrak™ M4A4 | Howl (Field-Tested)")
        self.assertEqual(res["weapon_type"], "M4A4")
        self.assertEqual(res["item_name"], "Howl")
        self.assertEqual(res["wear_name"], "Field-Tested")
        self.assertEqual(res["rarity_name"], "Contraband")
        self.assertEqual(res["quality_name"], "StatTrak™")
        self.assertEqual(res["floatvalue"], 0.25706347823143005)
        self.assertEqual(res["min"], 0)
        self.assertEqual(res["max"], 0.4)
        self.assertEqual(res["imageurl"], "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGIGz3UqlXOLrxM-vMGmW8VNxu5Dx60noTyL8ypexwiFO0P_6afVSKP-EAm6extF7teVgWiT9wh5_5zyAwo6oeSrDawUkCMN0QbEM5BO-wNazMe3qsgHZg4wQyy-t2jQJsHi3nDJ37A")

        # Note: Contraband items like the Howl are often detached from collections in schema exports
        self.assertIsNone(res.get("collection_name"))

        # Stickers (Original Howl has 1 Howling Dawn at slot 3)
        self.assertEqual(len(res["stickers"]), 1)
        sticker = res["stickers"][0]
        self.assertEqual(sticker["slot"], 3)
        self.assertEqual(sticker["name"], "Sticker | Howling Dawn")
        self.assertEqual(sticker["codename"], "comm01_howling_dawn")
        self.assertEqual(sticker["material"], "econ/stickers/community01/howling_dawn")

        # Charms (The one we added)
        self.assertEqual(len(res["keychains"]), 1)
        charm = res["keychains"][0]
        self.assertEqual(charm["slot"], 0)
        self.assertEqual(charm["name"], "Charm | Magmatude")
        self.assertEqual(charm["codename"], "kc_missinglink_lilhothead")
        self.assertEqual(charm["collection_name"], "Missing Link Community Charm Collection")
        self.assertEqual(charm["imageurl"], "https://community.akamai.steamstatic.com/economy/image/i0CoZ81Ui0m-9KwlBY1L_18myuGuq1wfhWSaZgMttyVfPaERSR0Wqmu7LAocGI6zwki4Uf_a0IWsPGiE7Fhy-I764WbkThD8i5jp6Ttkv6PhY6dSLfmAHW6exuJ_vupWQyC_nRIzuziEnsGgJymSZwd0CZpyQu5buxO9wNbmPrzm5wCLg95Fmyz_3y1Nuydq4OZXT-N7raqdv_up")

    def test_custom_placement_stickers_and_charms(self):
        self.skip_if_no_schema()
        # Example with custom placements (M4A1-S | Cyrex)
        link = "steam://run/730//+csgo_econ_action_preview%209D8D390E592F379C85A1BD759FB59BAD94A5215634729EDDCCD59DCD439EFF98959C8D50B9FF98959F8D50B9FF98959E8D50B9FF8995998D41D8B09D9D5D5DA01F3546A3D8811D57A0FF9295998D75D8A0567616A3D89DE9CF27F5F2ED953F9C8B959D8DB9A0834170DDD85EFB4FA3D02D672BDDC56A9F56EC4C0C"
        res = cs2inspect.parse(link, schema=self.schema)

        # Check Ex3rcice Foil sticker (Austin 2025) for custom placement
        sticker = next(s for s in res["stickers"] if s["stickerId"] == 8924)
        self.assertEqual(sticker["slot"], 4)
        self.assertAlmostEqual(sticker["offset_x"], 0.4290199875831604, places=5)
        self.assertAlmostEqual(sticker["offset_y"], 0.09887716174125671, places=5)
        self.assertEqual(sticker["rotation"], -6.0)

        # Check charm for correct "Souvenir Highlight Charm" identification
        charm = res["keychains"][0]
        self.assertEqual(charm["stickerId"], 36)
        self.assertEqual(charm["name"], "Souvenir Charm | Austin 2025 Highlight | apEX: Help Is Here")
        self.assertEqual(charm["highlight_reel"], 375)
        self.assertAlmostEqual(charm["offset_z"], 5.718101501464844, places=5)

if __name__ == '__main__':
    unittest.main()
