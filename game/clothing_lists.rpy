##Standard standing images taken at 1920x420 regardless of item size, so they can be tiled.

init -1:
    define mannequin_average = Image("mannequin_average.png") #Define the mannequin image we use for preview in all of the option selects.

    ## COLOUR DEFINES ##
    # Here we define colours as a 0 to 1 float for red, green, blue, and alpha. 0,0,0,1 would corriospond to perfect black everywhere, 1,1,1,1 corrisponds to no modification to the original greyscale.

    define colour_white = [1.0,1.0,1.0,1.0] #True white, don't change anything.

    define colour_black = [0.1,0.1,0.1,1] #A soft, natural fabric black.
    define colour_red = [0.6,0.1,0.1,1]
    define colour_green = [0.2,0.4,0.2,1]
    define colour_sky_blue = [0.4,0.6,0.9,1]
    define colour_dark_blue = [0.15,0.20,0.80,1]
    define colour_yellow = [0.9,0.8,0.05,1]
    define colour_pink = [1.0,0.8,0.85,1]

    define clothing_colours = [
        [colour_white,"White","#ffffff"],
        [colour_black,"Black","#000000"],
        [colour_red,"Red","#b20000"],
        [colour_green,"Green","#00b200"],
        [colour_sky_blue,"Sky Blue","#7ec0ee"],
        [colour_dark_blue,"Dark Blue","#000080"],
        [colour_yellow, "Yellow","#e5e500"],
        [colour_pink, "Pink","#ff78bb"]
        ]

    define colour_black_sheer = [0.1,0.1,0.1,0.96] #Makes use of the alpha channel to give us translucent material that very slightly shows what's underneath.


##NOTE/REMINDER##
#stand1 positions are taken as 420x1080 images with 800 offset ##LEGACY! NO LONGER USED!
#stand2 positions are taken as 500x1080 images with 800 offset
#stand3 positions are taken as 500x1080 images with 750 offset
#stand4 positions are taken as 450x1080 images with 750 offset
#stand5 positions are taken as 550x1080 images with 750 offset
#walking_away positions are taken as 500x1080 with 750 offset
#back_peek positions are taken as 500x1080 with 725 offset
#sitting positions are taken as 700x1080 with 575 offset

#kissing positions are taken as 550x1080 with 600 offset
#doggy positions are taken as 700x1080 images with 600 offset
#missionary positions are taken as 800x1080 images with 575 offset
#blowjob positions are taken as 500x1080 images with 700 offset
#against_wall positions are taken as 600x1080 images with 700 offset
#upright_doggy positions are taken as 700x1080 images with 675 offset

    python:

        ##NAKED BODIES##
        white_skin = Clothing("white skin", 1, True, True, "white", True, False, 0) #ADDED

        tan_skin = Clothing("tan skin", 1, True, True, "tan", True, False, 0) #ADDED

        black_skin = Clothing("black skin", 1, True, True, "black", True, False, 0) #ADDED

        ##HAIR STYLES##
        hair_styles =  []

        short_hair = Clothing("Short Hair", 1, True, True, "Short_Hair",False, False, 0,  whiteness_adjustment = 0.1, contrast_adjustment = 1.2)
        hair_styles.append(short_hair)

        messy_hair = Clothing("Messy Hair", 1, True, True, "Messy_Long_Hair", False, False, 0, whiteness_adjustment = 0.1, contrast_adjustment = 1.4)
        hair_styles.append(messy_hair)

        messy_short_hair = Clothing("Messy Short Hair", 1, True, True, "Messy_Short_Hair", False, False, 0, whiteness_adjustment = 0.1, contrast_adjustment = 1.1)
        hair_styles.append(messy_short_hair)

        shaved_side_hair = Clothing("Shaved Side Hair", 1, True, True, "Shaved_Side_Hair", False, False, 0)
        hair_styles.append(shaved_side_hair)

        messy_ponytail = Clothing("Messy Ponytail", 1, True, True, "Messy_Ponytail", False, False, 0, whiteness_adjustment = 0.3, contrast_adjustment = 1.1)
        hair_styles.append(messy_ponytail)

        twintail = Clothing("Twintails", 1, True, True, "Twin_Ponytails", False, False, 0, whiteness_adjustment = 0.1, contrast_adjustment = 1.1)
        hair_styles.append(twintail)

        ponytail = Clothing("Ponytail", 1, True, True, "Ponytail", False, False, 0, whiteness_adjustment = 0.3, contrast_adjustment = 1.3)
        hair_styles.append(ponytail)

        long_hair = Clothing("Long Hair", 1, True, True, "Long_Hair", False, False, 0, whiteness_adjustment = 0.2, contrast_adjustment = 1.8)
        hair_styles.append(long_hair)

        bobbed_hair = Clothing("Bobbed Hair", 1, True, True, "Bobbed_Hair", False, False, 0, whiteness_adjustment = 0.15, contrast_adjustment = 1.3)
        hair_styles.append(bobbed_hair)

        bowl_hair = Clothing("Bowl Hair", 1, True, True, "Coco_Hair", False, False, 0, whiteness_adjustment = 0.15, contrast_adjustment = 1.25)
        hair_styles.append(bowl_hair)

        bow_hair = Clothing("Bow Hair", 1, True, True, "Bow_Hair", False, False, 0) #NO IMAGES
        hair_styles.append(bow_hair) #TODO: Still falls into the uncanny valley.


        ##CLOTHING##

        ##Panties
        panties_list = []

        plain_panties = Clothing("Plain Panties", 1, True, True, "Plain_Panties", False, True, 0, tucked = True)
        panties_list.append(plain_panties)

        cotton_panties = Clothing("Cotton Panties", 1, True, True, "Cotton_Panties", False, True, 0, tucked = True)
        panties_list.append(cotton_panties)

        panties = Clothing("Panties", 1, True, True, "Panties", False, True, 0, tucked = True, whiteness_adjustment = 0.2, contrast_adjustment = 1.4)
        panties_list.append(panties)

        cute_panties = Clothing("Cute Panties", 1, True, True, "Cute_Panties", False, True, 0, tucked = True)
        panties_list.append(cute_panties)

        lace_panties = Clothing("Lace Panties", 1, True, True, "Lace_Panties", False, True, 2, tucked = True, whiteness_adjustment = 0.2, supported_patterns = {"Two Toned":"Pattern_1"})
        panties_list.append(lace_panties)

        cute_lace_panties = Clothing("Cute Lace Panties", 1, True, True, "Cute_Lace_Panties", False, True, 2, tucked = True)
        panties_list.append(cute_lace_panties)

        tiny_lace_panties = Clothing("Tiny Lace Panties", 1, True, True, "Tiny_Lace_Panties", False, True, 3, tucked = True)
        panties_list.append(tiny_lace_panties)

        thin_panties = Clothing("Thin Panties", 1, True, True, "Thin_Panties", False, True, 1, tucked = True, whiteness_adjustment = -0.1, contrast_adjustment = 1.3, supported_patterns = {"Two Toned":"Pattern_1"})
        panties_list.append(thin_panties)

        thong = Clothing("Thong", 1, True, True, "Thong", False, True, 3, tucked = True, supported_patterns = {"Two Toned":"Pattern_1"})
        panties_list.append(thong)

        tiny_g_string = Clothing("G String", 1, True, True, "Tiny_G_String", False, True, 4, tucked = True)
        panties_list.append(tiny_g_string)




        ##Bras
        bra_list = []

        bra = Clothing("Bra", 1, True, True, "Bra", True, True, 0, supported_patterns = {"Lacey":"Pattern_1"})
        bra_list.append(bra)

        bralette = Clothing("Bralette", 1, True, True, "Bralette", True, True, 0)
        bra_list.append(bralette)

        sports_bra = Clothing("Sports Bra", 1, True, True, "Sports_Bra", True, True, 0, whiteness_adjustment = 0.35, contrast_adjustment = 1.3, supported_patterns = {"Two Toned":"Pattern_1"})
        bra_list.append(sports_bra)

        strapless_bra = Clothing("Strapless Bra", 1, True, True, "Strapless_Bra", True, True, 1, whiteness_adjustment = 0.2, supported_patterns = {"Two Tone":"Pattern_1"})
        bra_list.append(strapless_bra)

        lace_bra = Clothing("Lace Bra", 1, True, True, "Lace_Bra", True, True, 2, whiteness_adjustment = 0.2, supported_patterns = {"Two Toned":"Pattern_1"})
        bra_list.append(lace_bra)

        thin_bra = Clothing("Thin Bra", 1, True, True, "Thin_Bra", True, True, 2, whiteness_adjustment = 0.0, contrast_adjustment = 1.3)
        bra_list.append(thin_bra)

        corset = Clothing("Corset", 1, True, True, "Corset", True, True, 5, whiteness_adjustment = 0.0, contrast_adjustment = 1.4, supported_patterns = {"Two Toned":"Pattern_1"})
        bra_list.append(corset)

        teddy = Clothing("Teddy", 1, True, True, "Teddy", True, True, 4, whiteness_adjustment = 0.0, contrast_adjustment = 1.0)
        bra_list.append(teddy)


        ##Pants
        pants_list = []

        leggings = Clothing("Leggings", 2, True, True, "Leggings", False, False, 1, whiteness_adjustment = 0.2, contrast_adjustment = 1.8)
        pants_list.append(leggings)

        capris = Clothing("Capris", 2, True, True, "Capris", False, False, 1, whiteness_adjustment = 0.3, contrast_adjustment = 1.1)
        pants_list.append(capris)

        booty_shorts = Clothing("Booty Shorts", 2, True, True, "Booty_Shorts", False, False, 6, whiteness_adjustment = 0.25, contrast_adjustment = 1.1)
        pants_list.append(booty_shorts)

        jean_hotpants = Clothing("Jean Hotpants", 2, True, True, "Jean_Hotpants", False, False, 4, whiteness_adjustment = 0.1)
        pants_list.append(jean_hotpants)

        jeans = Clothing("Jeans", 2, True, True, "Jeans", False, False, 0)
        pants_list.append(jeans)

        suitpants = Clothing("Suit Pants", 2, True, True, "Suit_Pants", False, False, 0)
        pants_list.append(suitpants)


        ##Skirts
        skirts_list = []

        pencil_skirt = Clothing("Pencil Skirt", 2, True, False, "Pencil_Skirt", False, False, 0, whiteness_adjustment = 0.1)
        skirts_list.append(pencil_skirt)

        belted_skirt = Clothing("Belted Skirt", 2, True, False, "Belted_Skirt", False, False, 1, contrast_adjustment = 1.15, supported_patterns = {"Belt":"Pattern_1"})
        skirts_list.append(belted_skirt)

        lace_skirt = Clothing("Lace Skirt", 2, True, False, "Lace_Skirt", False, False, 1, whiteness_adjustment = 0.15)
        skirts_list.append(lace_skirt)

        mini_skirt = Clothing("Mini Skirt", 2, False, False, "Mini_Skirt", False, False, 5, whiteness_adjustment = 0.2)
        skirts_list.append(mini_skirt)

        skirt = Clothing("Skirt", 2, True, False, "Skirt", False, False, 1)
        skirts_list.append(skirt)

        long_skirt = Clothing("Long Skirt", 2, True, True, "Long_Skirt", False, False, 0, whiteness_adjustment = 0.2, contrast_adjustment = 1.2)
        skirts_list.append(long_skirt)


        ##Dresses
        #TODO: Check if the extension or the main piece should have the whiteness adjusments etc.
        dress_list = []

        sweater_dress_bottom = Clothing("sweater dress", 2, True, False, "Sweater_Dress", False, False, 0, is_extension = True)
        sweater_dress = Clothing("sweater dress", 2, True, True, "Sweater_Dress", True, False, 0, has_extension = sweater_dress_bottom, whiteness_adjustment = 0.2, contrast_adjustment = 1.2, supported_patterns = {"Two Toned":"Pattern_1", "Hearts":"Pattern_2"})
        dress_list.append(sweater_dress)

        two_part_dress_bottom = Clothing("two part dress", 2, True, False, "Two_Piece_Dress", False, False, 0, is_extension = True)
        two_part_dress = Clothing("two part dress", 2, True, True, "Two_Piece_Dress", True, False, 6, has_extension = two_part_dress_bottom)
        dress_list.append(two_part_dress)

        thin_dress_bottom = Clothing("thin dress", 2, False, False, "Thin_Dress", False, False, 0, is_extension = True)
        thin_dress = Clothing("thin dress", 2, True, True, "Thin_Dress", True, False, 4, has_extension = thin_dress_bottom, whiteness_adjustment = 0.2, contrast_adjustment = 1.1)
        dress_list.append(thin_dress)

        summer_dress_bottom = Clothing("summer dress", 2, False, False, "Summer_Dress", False, False, 0, is_extension = True)
        summer_dress = Clothing("summer dress", 2, False, False, "Summer_Dress", True, False, 0, has_extension = summer_dress_bottom, whiteness_adjustment = -0.1)
        dress_list.append(summer_dress)

        nightgown_dress_bottom = Clothing("Nightgown", 2, False, False, "Nightgown", False, True, 0, is_extension = True)
        nightgown_dress = Clothing("Nightgown", 2, False, True, "Nightgown", True, True, 3, has_extension = nightgown_dress_bottom, whiteness_adjustment = 0.1, contrast_adjustment = 1.1)
        dress_list.append(nightgown_dress)

        bath_robe_bottom = Clothing("Bathrobe", 2, False, False, "Bath_Robe", False, False, 0, is_extension = True)
        bath_robe = Clothing("Bathrobe", 2, False, True, "Bath_Robe", True, True, 1, has_extension = bath_robe_bottom, whiteness_adjustment = 0.4, contrast_adjustment = 1.2)
        dress_list.append(bath_robe)

        lacy_one_piece_underwear_bottom = Clothing("lacy one piece", 1, True, True, "Lacy_One_Piece_Underwear", False, True, 0, is_extension = True)
        lacy_one_piece_underwear = Clothing("lacy one piece", 1, True, True, "Lacy_One_Piece_Underwear", True, True, 4, tucked = True, has_extension = lacy_one_piece_underwear_bottom, whiteness_adjustment = 0.2)
        dress_list.append(lacy_one_piece_underwear)

        lingerie_one_piece_bottom = Clothing("lingerie one piece", 1, True, True, "Lingerie_One_Piece", False, True, 0, is_extension = True)
        lingerie_one_piece = Clothing("lingerie one piece", 1, True, True, "Lingerie_One_Piece", True, True, 8, tucked = True, has_extension = lingerie_one_piece_bottom)
        dress_list.append(lingerie_one_piece)

        towel_bottom = Clothing("Towel", 1, True, True, "Towel", False, False, 0, is_extension = True)
        towel = Clothing("Towel", 1, True, True, "Towel", True, False, 1, has_extension = towel_bottom)
        dress_list.append(towel) #TEMPORARY FOR TESTING

        ##Shirts
        shirts_list = []

        tshirt = Clothing("Tshirt", 2, True, True, "Tshirt", True, False, 1, whiteness_adjustment = 0.35, supported_patterns = {"Striped":"Pattern_2"})
        shirts_list.append(tshirt)

        lace_sweater = Clothing("Lace Sweater", 2, True, True, "Lace_Sweater", True, False, 2, opacity_adjustment = 1.08, whiteness_adjustment = 0.15)
        shirts_list.append(lace_sweater)

        long_sweater = Clothing("Long Sweater", 2, True, True, "Long_Sweater", True, False, 0, whiteness_adjustment = 0.1, supported_patterns = {"Striped":"Pattern_1"})
        shirts_list.append(long_sweater)

        sleeveless_top = Clothing ("Sleeveless Top", 2, True, True, "Sleveless_Top", True, False, 0, tucked = True)
        shirts_list.append(sleeveless_top)

        long_tshirt = Clothing("Long Tshirt", 2, True, True, "Long_Tshirt", True, False, 0, whiteness_adjustment = 0.25, supported_patterns = {"Two Toned":"Pattern_1"})
        shirts_list.append(long_tshirt)

        sweater = Clothing("Sweater", 2, True, True, "Sweater", True, False, 1, whiteness_adjustment = 0.1)
        shirts_list.append(sweater)

        belted_top = Clothing("Belted Top", 2, True, True, "Belted_Top", True, False, 5, contrast_adjustment = 1.1)
        shirts_list.append(belted_top)

        lace_crop_top = Clothing("Lace Crop Top", 2, True, True, "Lace_Crop_Top", True, False, 2, whiteness_adjustment = 0.1, contrast_adjustment = 1.1)
        shirts_list.append(lace_crop_top)

        tanktop = Clothing("Tanktop", 2, True, True, "Tanktop", True, False, 3)
        shirts_list.append(tanktop)

        camisole = Clothing("Camisole", 2, True, True, "Camisole", True, False, 1, whiteness_adjustment = 0.2, supported_patterns = {"Two Toned":"Pattern_1"})
        shirts_list.append(camisole)

        tube_top = Clothing("Tube Top", 2, True, True, "Tube_Top", True, False, 4)
        shirts_list.append(tube_top)

        tie_sweater = Clothing("Tied Sweater", 2, True, True, "Tie_Sweater", True, False, 0, whiteness_adjustment = 0.3, contrast_adjustment = 1.1, supported_patterns = {"Two Toned":"Pattern_1"})
        shirts_list.append(tie_sweater)

        dress_shirt = Clothing("Dress Shirt", 2, True, True, "Dress_Shirt", True, False, 0, tucked = True, opacity_adjustment = 1.12)
        shirts_list.append(dress_shirt)

        business_vest = Clothing("Business Vest", 2, True, True, "Tight_Vest", True, False, 2, opacity_adjustment = 1.3)
        shirts_list.append(business_vest)

        lab_coat = Clothing("Lab Coat", 3, True, True, "Lab_Coat", True, False, 0, opacity_adjustment = 1.08)
        shirts_list.append(lab_coat)

        suit_jacket = Clothing("Suit Jacket", 3, True, True, "Suit_Jacket", True, False, 0)
        shirts_list.append(suit_jacket)

        vest = Clothing("Vest", 3, False, True, "Vest", True, False, 0)
        shirts_list.append(vest)


        ##Socks##
        socks_list = []

        fishnets = Clothing("Fishnets", 1, True, True, "Fishnets", False, False, 10, whiteness_adjustment = 0.2)
        socks_list.append(fishnets)

        high_socks = Clothing("High Socks", 1, True, True, "High_Socks", False, False, 0, contrast_adjustment = 1.2)
        socks_list.append(high_socks)

        thigh_highs = Clothing("Thigh Highs", 1, True, True, "Thigh_Highs", False, False, 5, whiteness_adjustment = 0.1)
        socks_list.append(thigh_highs)

        garter_with_fishnets = Clothing("Garter and Fishnets", 1, True, True, "Garter_and_Fishnets", False, False, 12, whiteness_adjustment = 0.2, contrast_adjustment = 1.0, supported_patterns = {"Two Toned":"Pattern_1"})
        socks_list.append(garter_with_fishnets)


#        ##Shoes##

        shoes_list = []

        sandles = Clothing("Sandals", 2, True, True, "Sandles", False, False, 0)
        shoes_list.append(sandles)

        shoes = Clothing("Shoes", 2, True, True, "Shoes", False, False, 0)
        shoes_list.append(shoes)

        slips = Clothing("Slips", 2, True, True, "Slips", False, False, 0)
        shoes_list.append(slips)

        sneakers = Clothing("Sneakers", 2, True, True, "Sneakers", False, False, 0, whiteness_adjustment = 0.2, supported_patterns = {"Laces":"Pattern_1"})
        shoes_list.append(sneakers)

        heels = Clothing("Heels", 2, True, True, "Heels", False, False, 1, whiteness_adjustment = 0.2)
        shoes_list.append(heels)

        high_heels = Clothing("High Heels", 2, True, True, "High_Heels", False, False, 3)
        shoes_list.append(high_heels)

        sandle_heels = Clothing("Sandal Heels", 2, True, True, "Sandal_Heels", False, False, 1)
        shoes_list.append(sandle_heels)

        boot_heels = Clothing("Boot Heels", 2, True, True, "Boot_Heels", False, False, 1, whiteness_adjustment = 0.1, contrast_adjustment = 1.1)
        shoes_list.append(boot_heels)


        ##Accessories##
        earings_list = [] #Note: now more properly known as facial accessories

        chandelier_earings = Clothing("Chandelier Earrings", 2, False, False, "Chandelier_Earings", False, False, 0, body_dependant = False) #TODO: Modify this to handle earings which don't vary based on facial type (Should they?)
        earings_list.append(chandelier_earings)

        gold_earings = Clothing("Gold Earings", 2 , False, False, "Gold_Earings", False, False, 0, body_dependant = False)
        earings_list.append(gold_earings)

        modern_glasses = Facial_Accessory("Modern Glasses", 2, False, False, "Modern_Glasses", False, False, 0)
        earings_list.append(modern_glasses)

        big_glasses = Facial_Accessory("Big Glasses", 2, False, False, "Big_Glasses", False, False, 0)
        earings_list.append(big_glasses)

        sunglasses = Facial_Accessory("Sunglasses", 2, False, False, "Sunglasses", False, False, 0)
        earings_list.append(sunglasses)

        head_towel = Clothing("Head Towel", 2, False, False, "Head_Towel", False, False, 0, body_dependant = False)
        earings_list.append(head_towel) #TEMPORARY FOR TESTING


        #TODO: Add a makeup section
        light_eye_shadow = Facial_Accessory("Light Eyeshadow", 1, False, False, "Upper_Eye_Shadow", False, False, 0, opacity_adjustment = 0.5)
        earings_list.append(light_eye_shadow)

        heavy_eye_shadow = Facial_Accessory("Heavy Eyeshadow", 1, False, False, "Full_Shimmer", False, False, 1, opacity_adjustment = 0.5)
        earings_list.append(heavy_eye_shadow)

        blush = Facial_Accessory("Blush", 1, False, False, "Blush", False, False, 0, opacity_adjustment = 0.5)
        earings_list.append(blush)

        lipstick = Facial_Accessory("Lipstick", 1, False, False, "Lipstick", False, False, 1, opacity_adjustment = 0.5)
        earings_list.append(lipstick)


        bracelet_list = []

        copper_bracelet = Clothing("Copper Bracelet", 2, False, False, "Copper_Bracelet", False, False, 0)
        bracelet_list.append(copper_bracelet)

        gold_bracelet = Clothing("Gold Bracelet", 2, False, False, "Gold_Bracelet", False, False, 0)
        bracelet_list.append(gold_bracelet)

        spiked_bracelet = Clothing("Spiked Bracelet", 2, False, False, "Spiked_Bracelet", False, False, 2)
        bracelet_list.append(spiked_bracelet)

        bead_bracelet = Clothing("Bead Bracelet", 2, False, False, "Bead_Bracelet", False, False, 0)
        bracelet_list.append(bead_bracelet)


        rings_list = []

        diamond_ring = Clothing("Diamond Ring", 2, False, False, "Diamond_Ring", False, False, 0)
        rings_list.append(diamond_ring)

        garnet_ring = Clothing("Garnet Ring", 2, False, False, "Garnet_Ring", False, False, 0)
        rings_list.append(garnet_ring)

        copper_ring_set = Clothing("Copper Ring Set", 2, False, False, "Copper_Ring_Set", False, False, 0)
        rings_list.append(copper_ring_set)


        neckwear_list = []

        wool_scarf = Clothing("Wool Scarf", 3, False, False, "Wool_Scarf", False, False, 0)
        neckwear_list.append(wool_scarf)

        necklace_set = Clothing("Necklace Set", 3, False, False, "Necklace_Set", True, False, 0)
        neckwear_list.append(necklace_set)

        gold_chain_necklace = Clothing("Gold Chain Necklace", 3, False, False, "Gold_Chain_Necklace", False, False, 0)
        neckwear_list.append(gold_chain_necklace)

        spiked_choker = Clothing("Spiked Choker", 3, False, False, "Spiked_Choker", False, False, 3)
        neckwear_list.append(spiked_choker)

        lace_choker = Clothing("Lace Choker", 2, False, False, "Lace_Choker", False, False, 3, whiteness_adjustment = 0.1)
        neckwear_list.append(lace_choker)

        wide_choker = Clothing("Wide Choker", 2, False, False, "Wide_Choker", False, False, 3)
        neckwear_list.append(wide_choker)




        ##Non Clothing Accessories##
        ass_cum = Clothing("Ass Cum", 1, False, False, "Ass_Covered", False, False, 10, whiteness_adjustment = 0.2)

        tits_cum = Clothing("Tit Cum", 1, False, False, "Tits_Covered", True, False, 10, whiteness_adjustment = 0.2)

        stomach_cum = Clothing("Stomach Cum", 1, False, False, "Stomach_Covered", False, False, 10, whiteness_adjustment = 0.2)

        mouth_cum = Facial_Accessory("Mouth Cum", 1, False, False, "Mouth_Dribble", False, False, 10, whiteness_adjustment = 0.2)

        face_cum = Facial_Accessory("Face Cum", 1, False, False, "Face_Covered", False, False, 10, whiteness_adjustment = 0.2)


        ##Creating outfits from XML##
        def proper_name_to_clothing_copy(proper_name):
            for potential_match in panties_list + bra_list + pants_list + skirts_list + dress_list + shirts_list + socks_list + shoes_list + earings_list + bracelet_list + rings_list + neckwear_list:
                if potential_match.proper_name == proper_name:
                    return potential_match.get_copy()

        def outfit_from_xml(outfit_element):
            return_outfit = Outfit(outfit_element.attrib["name"])
            clothing_mapping = {"UpperBody":Outfit.add_upper, "LowerBody":Outfit.add_lower, "Feet":Outfit.add_feet, "Accessories":Outfit.add_accessory}

            for location in clothing_mapping:
                for item_element in outfit_element.find(location):
                    clothing_copy = proper_name_to_clothing_copy(item_element.attrib["name"])
                    if clothing_copy:
                        clothing_colour = [float(item_element.attrib["red"]), float(item_element.attrib["green"]), float(item_element.attrib["blue"]), float(item_element.attrib["alpha"])]
                        pattern = item_element.get("pattern",None)
                        if pattern is not None:

                            colour_pattern = [float(item_element.attrib["pred"]), float(item_element.attrib["pgreen"]), float(item_element.attrib["pblue"]), float(item_element.attrib["palpha"])]
                        else:
                            colour_pattern = None
                        clothing_mapping[location](return_outfit, clothing_copy, clothing_colour, pattern, colour_pattern)

            return return_outfit

        def wardrobe_from_xml(xml_filename):
            # file_path = os.path.abspath(os.path.join(config.basedir, "game"))
            # file_path = os.path.join(file_path,"wardrobes")
            # file_name = os.path.join(file_path, xml_filename + ".xml")
            wardrobe_file = None
            modified_filename = "wardrobes/" + xml_filename+".xml"
            if renpy.loadable(modified_filename):
                wardrobe_file = renpy.file(modified_filename)

            #if not os.path.isfile(file_name): #This is likely where the outfit problem on android is.
            if wardrobe_file is None:
                return Wardrobe(xml_filename) #If there is no wardrobe present we return an empty wardrobe with the name of our file.

            #wardrobe_tree = ET.parse(file_name)
            wardrobe_tree = ET.parse(wardrobe_file)
            tree_root = wardrobe_tree.getroot()

            return_wardrobe = Wardrobe(tree_root.attrib["name"])
            for outfit_element in tree_root.find("FullSets"):
                return_wardrobe.add_outfit(outfit_from_xml(outfit_element))
            for outfit_element in tree_root.find("UnderwearSets"):
                return_wardrobe.add_underwear_set(outfit_from_xml(outfit_element))
            for outfit_element in tree_root.find("OverwearSets"):
                return_wardrobe.add_overwear_set(outfit_from_xml(outfit_element))
            return return_wardrobe


        ##OUTFITS##

        ##Predefined Full Outfits##
        default_outfit = Outfit("Default Outfit") #Used in case there is literatly no other outfit that is valid to prevent the game from crashing entirely (or girls from walking around naked.)
        default_outfit.add_lower(panties.get_copy(),colour_white)
        default_outfit.add_upper(bra.get_copy(),colour_white)
        default_outfit.add_lower(capris.get_copy(),colour_black)
        default_outfit.add_upper(long_tshirt.get_copy(),colour_black)
        default_outfit.add_feet(sandles.get_copy(),colour_black)


        # These are the old outfit declarations before we moved over to an xml based system.
        #
        # nude_1 = Outfit("Nude 1") #A default nude look, so slutty girls can look slutty.
        #
        # conservative_1 = Outfit("Conservative 1")
        # conservative_1.add_lower(panties.get_copy(),colour_white)
        # conservative_1.add_lower(leggings.get_copy(),colour_black)
        # conservative_1.add_upper(bra.get_copy(),colour_pink)
        # conservative_1.add_upper(long_sweater.get_copy(),colour_sky_blue)
        # conservative_1.add_feet(high_socks.get_copy(),colour_white)
        # conservative_1.add_feet(sneakers.get_copy(),colour_white)
        #
        # conservative_2 = Outfit("Conservative 2")
        # conservative_2.add_lower(panties.get_copy(),colour_white)
        # conservative_2.add_upper(bra.get_copy(),colour_pink)
        # conservative_2.add_dress(sweater_dress.get_copy(),colour_red)
        # conservative_2.add_feet(high_socks.get_copy(),colour_white)
        # conservative_2.add_feet(sneakers.get_copy(),colour_white)
        #
        # conservative_3 = Outfit("Conservative 3")
        # conservative_3.add_lower(panties.get_copy(),colour_red)
        # conservative_3.add_upper(bra.get_copy(),colour_red)
        # conservative_3.add_lower(capris.get_copy(),colour_black)
        # conservative_3.add_upper(lace_sweater.get_copy(),colour_black)
        # conservative_3.add_feet(sandles.get_copy(),colour_red)
        #
        # conservative_4 = Outfit("Conservative 4")
        # conservative_4.add_lower(panties.get_copy(),colour_red)
        # conservative_4.add_upper(bra.get_copy(),colour_pink)
        # conservative_4.add_lower(capris.get_copy(),colour_sky_blue)
        # conservative_4.add_upper(long_tshirt.get_copy(),colour_black)
        # conservative_4.add_feet(sandles.get_copy(),colour_white)
        #
        # conservative_5 = Outfit("Conservative 5")
        # conservative_5.add_lower(thin_panties.get_copy(),colour_pink)
        # conservative_5.add_upper(thin_bra.get_copy(),colour_pink)
        # conservative_5.add_lower(jeans.get_copy(),colour_sky_blue)
        # conservative_5.add_upper(tshirt.get_copy(),colour_white)
        # conservative_5.add_feet(sneakers.get_copy(),colour_white)
        #
        # conservative_6 = Outfit("Conservative 6")
        # conservative_6.add_lower(thin_panties.get_copy(),colour_pink)
        # conservative_6.add_upper(thin_bra.get_copy(),colour_pink)
        # conservative_6.add_lower(lace_skirt.get_copy(),colour_black)
        # conservative_6.add_upper(tie_sweater.get_copy(),colour_green)
        # conservative_6.add_feet(high_socks.get_copy(),colour_green)
        # conservative_6.add_feet(sneakers.get_copy(),colour_white)
        #
        # conservative_7 = Outfit("Conservative 7")
        # conservative_7.add_lower(plain_panties.get_copy(),colour_dark_blue)
        # conservative_7.add_upper(thin_bra.get_copy(),colour_dark_blue)
        # conservative_7.add_feet(sandle_heels.get_copy(),colour_black)
        # conservative_7.add_lower(belted_skirt.get_copy(),colour_sky_blue)
        # conservative_7.add_upper(long_sweater.get_copy(),colour_black)
        #
        # business_1 = Outfit("Business 1")
        # business_1.add_lower(plain_panties.get_copy(),colour_sky_blue)
        # business_1.add_upper(bra.get_copy(),colour_sky_blue)
        # business_1.add_upper(dress_shirt.get_copy(),colour_black)
        # business_1.add_feet(heels.get_copy(),colour_black)
        # business_1.add_lower(pencil_skirt.get_copy(),colour_black)
        # business_1.add_accessory(blush.get_copy(), [0.6,0.1,0.1,0.8])
        # business_1.add_accessory(lipstick.get_copy(), [0.6,0.1,0.1,0.8])
        # business_1.add_accessory(light_eye_shadow.get_copy(), [0.1,0.1,0.1,0.8])
        #
        # business_2 = Outfit("Business 2")
        # business_2.add_lower(plain_panties.get_copy(),colour_sky_blue)
        # business_2.add_upper(bra.get_copy(),colour_sky_blue)
        # business_2.add_upper(dress_shirt.get_copy(),colour_black)
        # business_2.add_feet(heels.get_copy(),colour_black)
        # business_2.add_lower(suitpants.get_copy(),colour_black)
        # business_2.add_accessory(blush.get_copy(), [0.6,0.1,0.1,0.8])
        # business_2.add_accessory(lipstick.get_copy(), [0.6,0.1,0.1,0.8])
        # business_2.add_accessory(light_eye_shadow.get_copy(), [0.1,0.1,0.1,0.8])
        #
        # business_3 = Outfit("Business 3")
        # business_3.add_feet(high_socks.get_copy(),colour_white)
        # business_3.add_lower(plain_panties.get_copy(),colour_red)
        # business_3.add_upper(bra.get_copy(),colour_red)
        # business_3.add_upper(dress_shirt.get_copy(),colour_red)
        # business_3.add_feet(sneakers.get_copy(),colour_black)
        # business_3.add_lower(jeans.get_copy(),colour_black)
        # business_3.add_accessory(blush.get_copy(), [0.6,0.1,0.1,0.8])
        # business_3.add_accessory(lipstick.get_copy(), [0.6,0.1,0.1,0.8])
        # business_3.add_accessory(light_eye_shadow.get_copy(), [0.1,0.1,0.1,0.8])
        #
        #
        # risque_1 = Outfit("Risque 1")
        # risque_1.add_lower(panties.get_copy(),colour_black)
        # risque_1.add_lower(mini_skirt.get_copy(),colour_red)
        # risque_1.add_upper(bra.get_copy(),colour_black)
        # risque_1.add_upper(tanktop.get_copy(),colour_black)
        # risque_1.add_feet(sandles.get_copy(),colour_black)
        #
        # risque_2 = Outfit("Risque 2")
        # risque_2.add_lower(panties.get_copy(),colour_black)
        # risque_2.add_upper(corset.get_copy(),colour_black)
        # risque_2.add_feet(heels.get_copy(),colour_black)
        # risque_2.add_dress(thin_dress.get_copy(),colour_black)
        #
        # risque_3 = Outfit("Risque 3")
        # risque_3.add_lower(thin_panties.get_copy(),colour_black)
        # risque_3.add_upper(thin_bra.get_copy(),colour_black)
        # risque_3.add_feet(sandle_heels.get_copy(),colour_white)
        # risque_3.add_lower(lace_skirt.get_copy(),colour_black)
        # risque_3.add_upper(lace_crop_top.get_copy(),colour_green)
        #
        # risque_4 = Outfit("Risque 4")
        # risque_4.add_lower(plain_panties.get_copy(),colour_pink)
        # risque_4.add_upper(thin_bra.get_copy(),colour_pink)
        # risque_4.add_feet(sandles.get_copy(),colour_black)
        # risque_4.add_lower(capris.get_copy(),colour_black)
        # risque_4.add_upper(camisole.get_copy(),colour_red)
        #
        # risque_5 = Outfit("Risque 5")
        # risque_5.add_lower(thong.get_copy(), colour_black)
        # risque_5.add_upper(lace_bra.get_copy(), colour_black)
        # risque_5.add_feet(sneakers.get_copy(), [0.24,0.24,0.24,1.0])
        # risque_5.add_lower(leggings.get_copy(), [0.79, 0.79, 0.79, 0.8])
        # risque_5.add_upper(tanktop.get_copy(), [0.61, 0.79, 0.79, 0.8])
        #
        # risque_6 = Outfit("Risque 6")
        # risque_6.add_lower(thong.get_copy(), colour_black)
        # risque_6.add_accessory(lipstick.get_copy(), colour_black)
        # risque_6.add_accessory(heavy_eye_shadow.get_copy(), colour_black)
        # risque_6.add_accessory(blush.get_copy(), [0.76, 0.376, 0.368, 0.8])
        # risque_6.add_feet(garter_with_fishnets.get_copy(), colour_black)
        # risque_6.add_accessory(bead_bracelet.get_copy(), colour_white)
        # risque_6.add_accessory(spiked_bracelet.get_copy(), colour_white)
        # risque_6.add_accessory(copper_ring_set.get_copy(), colour_white)
        # risque_6.add_feet(boot_heels.get_copy(), colour_white)
        # risque_6.add_lower(jean_hotpants.get_copy(), colour_black)
        # risque_6.add_upper(tube_top.get_copy(), colour_black)
        # risque_6.add_accessory(spiked_choker.get_copy(), colour_black)
        # risque_6.add_upper(vest.get_copy(), colour_black)
        #
        # slutty_1 = Outfit("Slutty 1")
        # slutty_1.add_upper(bra.get_copy(),colour_red)
        # slutty_1.add_lower(panties.get_copy(),colour_red)
        # slutty_1.add_feet(heels.get_copy(),colour_red)
        #
        #
        # ##Underwear Sets##
        # no_underwear_1 = Outfit("No Underwear")
        #
        # underwear_1 = Outfit("Underwear 1")
        # underwear_1.add_upper(bra.get_copy(),colour_red)
        # underwear_1.add_lower(panties.get_copy(),colour_red)
        #
        # underwear_2 = Outfit("Underwear 2")
        # underwear_2.add_upper(bra.get_copy(),colour_black)
        # underwear_2.add_lower(panties.get_copy(),colour_black)
        #
        # simple_underwear_1 = Outfit("Simple Underwear 1")
        # simple_underwear_1.add_lower(plain_panties.get_copy(), colour_black)
        # simple_underwear_1.add_upper(bra.get_copy(),colour_black)
        #
        # simple_underwear_2 = Outfit("Simple Underwear 2")
        # simple_underwear_2.add_lower(panties.get_copy(),colour_pink)
        # simple_underwear_2.add_upper(bra.get_copy(),colour_pink)
        # simple_underwear_2.add_feet(high_socks.get_copy(),colour_white)
        #
        # simple_underwear_3 = Outfit("Simple Underwear 3")
        # simple_underwear_3.add_lower(panties.get_copy(),colour_black)
        # simple_underwear_3.add_upper(bra.get_copy(),colour_red)
        #
        # simple_underwear_4 = Outfit("Simple Underwear 4")
        # simple_underwear_4.add_lower(thin_panties.get_copy(),colour_black)
        # simple_underwear_4.add_upper(bra.get_copy(),colour_pink)
        # simple_underwear_4.add_feet(high_socks.get_copy(),colour_sky_blue)
        #
        # sexy_underwear_1 = Outfit("Sexy Underwear 1")
        # sexy_underwear_1.add_lower(panties.get_copy(),colour_sky_blue)
        # sexy_underwear_1.add_upper(bra.get_copy(),colour_sky_blue)
        # sexy_underwear_1.add_feet(thigh_highs.get_copy(),colour_sky_blue)
        #
        # sexy_underwear_2 = Outfit("Sexy Underwear 2")
        # sexy_underwear_2.add_lower(thong.get_copy(), colour_black)
        # sexy_underwear_2.add_upper(thin_bra.get_copy(), colour_black)
        # sexy_underwear_2.add_feet(high_socks.get_copy(),colour_black)
        #
        # white_underwear_1 = Outfit("White Underwear 1")
        # white_underwear_1.add_lower(lace_panties.get_copy(),colour_white)
        # white_underwear_1.add_upper(lace_bra.get_copy(),colour_white)
        # white_underwear_1.add_feet(thigh_highs.get_copy(),colour_white)
        #
        # white_underwear_2 = Outfit("White Underwear 2")
        # white_underwear_2.add_lower(plain_panties.get_copy(),colour_white)
        # white_underwear_2.add_upper(lace_bra.get_copy(),colour_white)
        # white_underwear_2.add_feet(high_socks.get_copy(),colour_white)
        #
        # white_underwear_3 = Outfit("White Underwear 3")
        # white_underwear_3.add_lower(lace_panties.get_copy(),colour_white)
        # white_underwear_3.add_upper(lace_bra.get_copy(),colour_white)
        #
        # white_underwear_4 = Outfit("White Underwear 4")
        # white_underwear_4.add_lower(thong.get_copy(),colour_white)
        #
        # white_underwear_5 = Outfit("White Underwear 5")
        # white_underwear_5.add_lower(thong.get_copy(), colour_white)
        # white_underwear_5.add_feet(garter_with_fishnets.get_copy(), colour_white)
        # white_underwear_5.add_upper(bra.get_copy(), colour_white)
        #
        # thong_underwear_1 = Outfit("Thong Underwear 1")
        # thong_underwear_1.add_lower(thong.get_copy(),colour_black)
        #
        # pink_underwear_1 = Outfit("Pink Underwear 1")
        # pink_underwear_1.add_lower(plain_panties.get_copy(),colour_pink)
        # pink_underwear_1.add_upper(thin_bra.get_copy(),colour_pink)
        # pink_underwear_1.add_feet(high_socks.get_copy(),colour_white)
        #
        # pink_underwear_2 = Outfit("Pink Underwear 2")
        # pink_underwear_2.add_lower(plain_panties.get_copy(),colour_pink)
        # pink_underwear_2.add_feet(fishnets.get_copy(),colour_pink)
        #
        # blue_underwear_1 = Outfit("Blue Underwear 1")
        # blue_underwear_1.add_lower(panties.get_copy(),colour_dark_blue)
        # blue_underwear_1.add_upper(bra.get_copy(), colour_dark_blue)
        # blue_underwear_1.add_feet(high_socks.get_copy(), colour_black)
        #
        # blue_underwear_2 = Outfit("Blue Underwear 2")
        # blue_underwear_2.add_lower(plain_panties.get_copy(),colour_dark_blue)
        # blue_underwear_2.add_upper(lace_bra.get_copy(),colour_dark_blue)
        # blue_underwear_2.add_feet(high_socks.get_copy(),colour_sky_blue)
        #
        # mismatched_underwear_1 = Outfit("Mismatched Underwear 1")
        # mismatched_underwear_1.add_lower(thin_panties.get_copy(),colour_green)
        # mismatched_underwear_1.add_upper(bra.get_copy(), colour_black)
        #
        # mismatched_underwear_2 = Outfit("Mismatched Underwear 2")
        # mismatched_underwear_2.add_lower(lace_panties.get_copy(),colour_red)
        # mismatched_underwear_2.add_upper(bra.get_copy(),colour_black)
        #
        # mismatched_underwear_3 = Outfit("Mismatched Underwear 3")
        # mismatched_underwear_3.add_lower(panties.get_copy(),colour_white)
        # mismatched_underwear_3.add_upper(bra.get_copy(),colour_pink)
        # mismatched_underwear_3.add_feet(high_socks.get_copy(),colour_red)
        #
        # lingerie_underwear_1 = Outfit("Lingerie Underwear 1")
        # lingerie_underwear_1.add_lower(thong.get_copy(),colour_white)
        # lingerie_underwear_1.add_upper(corset.get_copy(),colour_white)
        # lingerie_underwear_1.add_feet(fishnets.get_copy(),colour_white)
        #
        # lingerie_underwear_2 = Outfit("Lingerie Underwear 2")
        # lingerie_underwear_2.add_lower(thong.get_copy(),colour_red)
        # lingerie_underwear_2.add_upper(corset.get_copy(),colour_red)
        # lingerie_underwear_2.add_feet(fishnets.get_copy(),colour_red)
        #
        # lingerie_underwear_3 = Outfit("Lingerie Underwear 3")
        # lingerie_underwear_3.add_lower(thong.get_copy(),colour_black)
        # lingerie_underwear_3.add_upper(corset.get_copy(),colour_black)
        # lingerie_underwear_3.add_feet(fishnets.get_copy(),colour_black)
        #
        # lingerie_underwear_4 = Outfit("Lingerie Underwear 4")
        # lingerie_underwear_4.add_lower(thong.get_copy(),colour_black)
        # lingerie_underwear_4.add_feet(fishnets.get_copy(),colour_black)
        #
        # lingerie_underwear_5 = Outfit("Lingerie Underwear 5")
        # lingerie_underwear_5.add_upper(corset.get_copy(),colour_black)
        #
        # lingerie_underwear_6 = Outfit("Lingerie Underwear 6")
        # lingerie_underwear_6.add_lower(thin_panties.get_copy(),colour_black)
        #
        # lingerie_underwear_7 = Outfit("Lingerie Underwear 7")
        # lingerie_underwear_7.add_dress(lacy_one_piece_underwear.get_copy(), [1.0,0.25,0.26,1.0])
        # lingerie_underwear_7.add_feet(garter_with_fishnets.get_copy(), [0.75,0.22,0.22,1.0])
        #
        # lingerie_underwear_8 = Outfit("Lingerie Underwear 8")
        # lingerie_underwear_8.add_lower(thong.get_copy(),colour_black)
        # lingerie_underwear_8.add_feet(garter_with_fishnets.get_copy(), [0.22,0.22,0.22, 1.0])
        # lingerie_underwear_8.add_upper(thin_bra.get_copy(), colour_black)
        #
        # lingerie_underwear_9 = Outfit("Lingerie Underwear 9")
        # lingerie_underwear_9.add_lower(thin_panties.get_copy(), [0.0,0.315,0.60, 1.0])
        # lingerie_underwear_9.add_feet(high_socks.get_copy(), colour_white)
        # lingerie_underwear_9.add_upper(corset.get_copy(), [0.0, 0.315, 0.60, 1.0])
        #
        # lingerie_underwear_10 = Outfit("Lingerie Underwear 10")
        # lingerie_underwear_10.add_dress(lingerie_one_piece.get_copy(), colour_white)
        # lingerie_underwear_10.add_feet(thigh_highs.get_copy(), colour_white)
        #
        # yellow_underwear_1 = Outfit("Yellow Underwear 1")
        # yellow_underwear_1.add_lower(thong.get_copy(),colour_yellow)
        # yellow_underwear_1.add_upper(thin_bra.get_copy(),colour_yellow)
        # yellow_underwear_1.add_feet(high_socks.get_copy(),colour_black)
        #
        # green_underwear_1 = Outfit("Green Underwear 1")
        # green_underwear_1.add_lower(panties.get_copy(),colour_green)
        # green_underwear_1.add_upper(bra.get_copy(),colour_green)
        # green_underwear_1.add_feet(high_socks.get_copy(),colour_green)
        #
        # black_underwear_1 = Outfit("Black Underwear 1")
        # black_underwear_1.add_lower(panties.get_copy(),colour_black)
        # black_underwear_1.add_upper(bra.get_copy(),colour_black)
        # black_underwear_1.add_feet(thigh_highs.get_copy(),colour_black)
        #
        # red_underwear_1 = Outfit("Red Underwear 1")
        # red_underwear_1.add_lower(plain_panties.get_copy(),colour_red)
        # red_underwear_1.add_upper(lace_bra.get_copy(),colour_red)
        # red_underwear_1.add_feet(high_socks.get_copy(),colour_red)
        #
        #
        #
        # ##Overwear Sets##
        # no_overwear_1 = Outfit("No Overwear")
        #
        # overwear_1 = Outfit("Overwear 1")
        # overwear_1.add_upper(lace_sweater.get_copy(),colour_black)
        # overwear_1.add_lower(capris.get_copy(),colour_black)
        # overwear_1.add_feet(sandles.get_copy(),colour_red)
        #
        # overwear_2 = Outfit("Overwear 2")
        # overwear_2.add_upper(long_tshirt.get_copy(),colour_black)
        # overwear_2.add_lower(capris.get_copy(),colour_sky_blue)
        # overwear_2.add_feet(sandles.get_copy(),colour_white)
        #
        # rocker_1 = Outfit("Rocker 1")
        # rocker_1.add_upper(belted_top.get_copy(),colour_black)
        # rocker_1.add_lower(jean_hotpants.get_copy(),colour_black)
        # rocker_1.add_feet(boot_heels.get_copy(), colour_black)
        # rocker_1.add_accessory(spiked_bracelet.get_copy(), colour_white)
        # rocker_1.add_accessory(gold_chain_necklace.get_copy(), colour_white)
        # rocker_1.add_accessory(garnet_ring.get_copy(), colour_white)
        #
        # rocker_2 = Outfit("Rocker 2")
        # rocker_2.add_accessory(spiked_bracelet.get_copy(), colour_white)
        # rocker_2.add_accessory(garnet_ring.get_copy(), colour_white)
        # rocker_2.add_feet(boot_heels.get_copy(), colour_black)
        # rocker_2.add_lower(jean_hotpants.get_copy(), colour_black)
        # rocker_2.add_upper(belted_top.get_copy(), colour_black)
        # rocker_2.add_accessory(spiked_choker.get_copy(), colour_white)
        #
        # business_overwear_1 = Outfit("Business Overwear 1")
        # business_overwear_1.add_upper(dress_shirt.get_copy(),colour_sky_blue)
        # business_overwear_1.add_accessory(gold_earings.get_copy(),colour_white)
        # business_overwear_1.add_feet(heels.get_copy(),colour_black)
        # business_overwear_1.add_lower(pencil_skirt.get_copy(),colour_black)
        #
        # business_overwear_2 = Outfit("Business Overwear 2")
        # business_overwear_2.add_upper(dress_shirt.get_copy(),colour_white)
        # business_overwear_2.add_accessory(gold_earings.get_copy(),colour_white)
        # business_overwear_2.add_feet(heels.get_copy(),colour_black)
        # business_overwear_2.add_lower(pencil_skirt.get_copy(),colour_red)
        #
        # casual_overwear_1 = Outfit("Casual Overwear 1")
        # casual_overwear_1.add_feet(sandle_heels.get_copy(), colour_green)
        # casual_overwear_1.add_lower(long_skirt.get_copy(), colour_black)
        # casual_overwear_1.add_upper(long_sweater.get_copy(), colour_green)
        # casual_overwear_1.add_accessory(necklace_set.get_copy(), colour_white)
        #
        # casual_overwear_2 = Outfit("Casual Overwear 2")
        # casual_overwear_2.add_accessory(bead_bracelet.get_copy(), colour_white)
        # casual_overwear_2.add_feet(sandle_heels.get_copy(), colour_white)
        # casual_overwear_2.add_lower(long_skirt.get_copy(), colour_pink)
        # casual_overwear_2.add_upper(lace_crop_top.get_copy(), colour_pink)
        #
        # casual_overwear_3 = Outfit("Casual Overwear 3")
        # casual_overwear_3.add_accessory(chandelier_earings.get_copy(), colour_white)
        # casual_overwear_3.add_feet(sandle_heels.get_copy(), colour_white)
        # casual_overwear_3.add_dress(sweater_dress.get_copy(), colour_dark_blue)
        #
        # casual_overwear_4 = Outfit("Casual Overwear 4")
        # casual_overwear_4.add_accessory(chandelier_earings.get_copy(), colour_white)
        # casual_overwear_4.add_feet(heels.get_copy(), colour_red)
        # casual_overwear_4.add_lower(belted_skirt.get_copy(), colour_black)
        # casual_overwear_4.add_upper(tshirt.get_copy(), colour_black)
        #
        # casual_overwear_5 = Outfit("Casual Overwear 5")
        # casual_overwear_5.add_accessory(copper_bracelet.get_copy(), colour_white)
        # casual_overwear_5.add_accessory(bead_bracelet.get_copy(), colour_black)
        # casual_overwear_5.add_feet(sandle_heels.get_copy(), colour_black)
        # casual_overwear_5.add_lower(skirt.get_copy(), colour_pink)
        # casual_overwear_5.add_upper(tshirt.get_copy(), colour_sky_blue)
        # casual_overwear_5.add_accessory(gold_chain_necklace.get_copy(), colour_white)
        #
        # casual_overwear_6 = Outfit("Casual Overwear 6")
        # casual_overwear_6.add_accessory(copper_bracelet.get_copy(), colour_white)
        # casual_overwear_6.add_accessory(garnet_ring.get_copy(), colour_white)
        # casual_overwear_6.add_accessory(copper_ring_set.get_copy(), colour_white)
        # casual_overwear_6.add_feet(sandle_heels.get_copy(), colour_black)
        # casual_overwear_6.add_lower(leggings.get_copy(), colour_black)
        # casual_overwear_6.add_upper(tanktop.get_copy(), colour_white)
        # casual_overwear_6.add_accessory(gold_chain_necklace.get_copy(), colour_white)
        #
        # casual_overwear_7 = Outfit("Casual Overwear 7")
        # casual_overwear_7.add_accessory(copper_bracelet.get_copy(), colour_white)
        # casual_overwear_7.add_accessory(garnet_ring.get_copy(), colour_white)
        # casual_overwear_7.add_accessory(copper_ring_set.get_copy(), colour_white)
        # casual_overwear_7.add_feet(sandle_heels.get_copy(), colour_black)
        # casual_overwear_7.add_lower(jeans.get_copy(), colour_sky_blue)
        # casual_overwear_7.add_upper(camisole.get_copy(), colour_black)
        # casual_overwear_7.add_accessory(gold_chain_necklace.get_copy(), colour_white)
        #
        # casual_overwear_8 = Outfit("Casual Overwear 8")
        # casual_overwear_8.add_accessory(copper_bracelet.get_copy(), colour_white)
        # casual_overwear_8.add_accessory(diamond_ring.get_copy(), colour_white)
        # casual_overwear_8.add_feet(shoes.get_copy(), colour_black)
        # casual_overwear_8.add_lower(capris.get_copy(), colour_black)
        # casual_overwear_8.add_upper(tie_sweater.get_copy(), colour_red)
        # casual_overwear_8.add_accessory(gold_chain_necklace.get_copy(), colour_white)
        #
        # casual_overwear_9 = Outfit("Casual Overwear 9")
        # casual_overwear_9.add_feet(sandles.get_copy(), colour_yellow)
        # casual_overwear_9.add_lower(belted_skirt.get_copy(), colour_yellow)
        # casual_overwear_9.add_upper(long_tshirt.get_copy(), colour_green)
        #
        # casual_overwear_10 = Outfit("Casual Overwear 10")
        # casual_overwear_10.add_feet(high_heels.get_copy(), colour_dark_blue)
        # casual_overwear_10.add_lower(jeans.get_copy(), colour_sky_blue)
        # casual_overwear_10.add_upper(sweater.get_copy(), colour_white)
        #
        # casual_overwear_11 = Outfit("Casual Overwear 11")
        # casual_overwear_11.add_accessory(diamond_ring.get_copy(), colour_white)
        # casual_overwear_11.add_feet(heels.get_copy(), colour_black)
        # casual_overwear_11.add_lower(capris.get_copy(), colour_black)
        # casual_overwear_11.add_upper(lace_sweater.get_copy(), colour_sky_blue)
        # casual_overwear_11.add_accessory(wool_scarf.get_copy(), colour_black)
        #
        # casual_overwear_12 = Outfit("Casual Overwear 12")
        # casual_overwear_12.add_feet(sandles.get_copy(), colour_white)
        # casual_overwear_12.add_lower(skirt.get_copy(), colour_white)
        # casual_overwear_12.add_upper(long_sweater.get_copy(), colour_yellow)
        #
        # sexy_overwear_1 = Outfit("Sexy Overwear 1")
        # sexy_overwear_1.add_feet(high_heels.get_copy(), colour_red)
        # sexy_overwear_1.add_lower(mini_skirt.get_copy(), colour_black)
        # sexy_overwear_1.add_upper(lace_crop_top.get_copy(), colour_red)
        #
        # sexy_overwear_2 = Outfit("Sexy Overwear 2")
        # sexy_overwear_2.add_accessory(lace_choker.get_copy(), colour_black)
        # sexy_overwear_2.add_feet(high_heels.get_copy(), colour_black)
        # sexy_overwear_2.add_lower(booty_shorts.get_copy(), colour_black)
        # sexy_overwear_2.add_upper(tanktop.get_copy(), colour_black)
        #
        # sexy_overwear_3 = Outfit("Sexy Overwear 3")
        # sexy_overwear_3.add_accessory(lace_choker.get_copy(), colour_black)
        # sexy_overwear_3.add_accessory(copper_ring_set.get_copy(), colour_white)
        # sexy_overwear_3.add_accessory(gold_earings.get_copy(), colour_white)
        # sexy_overwear_3.add_feet(heels.get_copy(), colour_red)
        # sexy_overwear_3.add_dress(two_part_dress.get_copy(), colour_red)
        #
        # sexy_overwear_4 = Outfit("Sexy Overwear 4")
        # sexy_overwear_4.add_accessory(copper_ring_set.get_copy(), colour_white)
        # sexy_overwear_4.add_accessory(gold_earings.get_copy(), colour_black)
        # sexy_overwear_4.add_feet(sandles.get_copy(), colour_black)
        # sexy_overwear_4.add_lower(mini_skirt.get_copy(), colour_sky_blue)
        # sexy_overwear_4.add_upper(belted_top.get_copy(), colour_black)
        # sexy_overwear_4.add_accessory(spiked_choker.get_copy(), colour_white)
        #
        # sexy_overwear_5 = Outfit("Sexy Overwear 5")
        # sexy_overwear_5.add_upper(dress_shirt.get_copy(), colour_black)
        # sexy_overwear_5.add_accessory(lace_choker.get_copy(), colour_black)
        # sexy_overwear_5.add_accessory(diamond_ring.get_copy(), colour_white)
        # sexy_overwear_5.add_feet(heels.get_copy(), colour_black)
        # sexy_overwear_5.add_lower(long_skirt.get_copy(), colour_black)
        #
        # sexy_overwear_6 = Outfit("Sexy Overwear 6")
        # sexy_overwear_6.add_feet(heels.get_copy(), colour_black)
        # sexy_overwear_6.add_dress(thin_dress.get_copy(), colour_black)
        # sexy_overwear_6.add_accessory(necklace_set.get_copy(), colour_white)
        #
        # slutty_overwear_1 = Outfit("Slutty Overwear 1")
        # slutty_overwear_1.add_feet(sandles.get_copy(), colour_black)
        # slutty_overwear_1.add_lower(jean_hotpants.get_copy(), colour_black)
        #
        # slutty_overwear_2 = Outfit("Slutty Overwear 2")
        # slutty_overwear_2.add_lower(booty_shorts.get_copy(), colour_dark_blue)
        # slutty_overwear_2.add_feet(sandles.get_copy(), colour_black)
        #
        # slutty_overwear_3 = Outfit("Slutty Overwear 3")
        # slutty_overwear_3.add_upper(camisole.get_copy(), colour_red)
        # slutty_overwear_3.add_feet(sandles.get_copy(), colour_black)
        #
        # slutty_overwear_4 = Outfit("Slutty Overwear 4")
        # slutty_overwear_4.add_feet(shoes.get_copy(), colour_black)
        # slutty_overwear_4.add_upper(long_tshirt.get_copy(), colour_red)
        #
        # slutty_overwear_5 = Outfit("Slutty Overwear 5")
        # slutty_overwear_5.add_accessory(spiked_choker.get_copy(), colour_white)
        # slutty_overwear_5.add_feet(heels.get_copy(), colour_black)
        #
        # slutty_overwear_6 = Outfit("Slutty Overwear 6")
        # slutty_overwear_6.add_accessory(lace_choker.get_copy(), colour_black)
        # slutty_overwear_6.add_feet(heels.get_copy(), colour_black)



        ##WARDROBES##

        # default_wardrobe = Wardrobe("Default Wardrobe", [nude_1, conservative_1, conservative_2, conservative_3, conservative_4, conservative_5, conservative_6, conservative_7, business_1, business_2 , business_3, risque_1, risque_2, risque_3, risque_4, risque_5, risque_6, slutty_1],
        #     [no_underwear_1, underwear_1,underwear_2, simple_underwear_1, simple_underwear_2, simple_underwear_3, simple_underwear_4, sexy_underwear_1, sexy_underwear_2, white_underwear_1, white_underwear_2, white_underwear_3, white_underwear_4, white_underwear_5, thong_underwear_1, pink_underwear_1, pink_underwear_2, blue_underwear_1, blue_underwear_2, mismatched_underwear_1, mismatched_underwear_2, mismatched_underwear_3, lingerie_underwear_1, lingerie_underwear_2, lingerie_underwear_3, lingerie_underwear_4, lingerie_underwear_5, lingerie_underwear_6, lingerie_underwear_7, lingerie_underwear_8, lingerie_underwear_9, lingerie_underwear_10, yellow_underwear_1, green_underwear_1, black_underwear_1, red_underwear_1],
        #     [no_overwear_1, overwear_1,overwear_2, rocker_1, rocker_2, casual_overwear_1, casual_overwear_2, casual_overwear_3, casual_overwear_4, casual_overwear_5, casual_overwear_6, casual_overwear_7, casual_overwear_8, casual_overwear_9, casual_overwear_10, casual_overwear_11, casual_overwear_12, sexy_overwear_1, sexy_overwear_2, sexy_overwear_3, sexy_overwear_4, sexy_overwear_5, sexy_overwear_6, slutty_overwear_1, slutty_overwear_2, slutty_overwear_3, slutty_overwear_4, slutty_overwear_5, slutty_overwear_6 ])

        default_wardrobe = wardrobe_from_xml("Master_Default_Wardrobe")

        lingerie_wardrobe = wardrobe_from_xml("Lingerie_Wardrobe")
