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
        position_size_dict = { #Holds the maximum size of each position image, for use when an image is being displayed.
        "stand1":(420,1080),
        "stand2":(500,1080),
        "stand3":(500,1080),
        "stand4":(450,1080),
        "stand5":(550,1080),
        "walking_away":(500,1080),
        "back_peek":(500,1080),
        "sitting":(700,1080),
        "kissing":(550,1080),
        "doggy":(700,1080),
        "missionary":(800,1080),
        "blowjob":(500,1080),
        "against_wall":(600,1080),
        "standing_doggy":(700,1080),
        "kneeling1":(700,1080),
        "cowgirl":(700,1080)
        }

        ##NAKED BODIES##
        white_skin = Clothing("white skin", 1, True, True, "white", True, False, 0)

        tan_skin = Clothing("tan skin", 1, True, True, "tan", True, False, 0)

        black_skin = Clothing("black skin", 1, True, True, "black", True, False, 0)


        ##Region Weight "Clothing" items##
        #These clothing items are used to map animations to specific parts of the body.

        #Specific region weights
        breast_region = Clothing("Breast region", 1, False, False, "Breast_Region_Weight", True, False, 0)
        butt_region = Clothing("Butt region", 1, False, False, "Butt_Region_Weight", False, False, 0)

        #General region weights
        all_regions = Clothing("All regions", 1, False, False, "All_Regions_Weight", True, False, 0)
        torso_region = Clothing("Torso region", 1, False, False, "Torso_Region_Weight", True, False, 0)
        stomach_region = Clothing("Stomach region", 1, False, False, "Stomach_Region_Weight", False, False, 0)
        pelvis_region = Clothing("Pelvis region", 1, False, False, "Pelvis_Region_Weight", False, False, 0)
        upper_leg_region = Clothing("Upper leg region", 1, False, False, "Upper_Leg_Region_Weight", False, False, 0)
        lower_leg_region = Clothing("Lower leg region", 1, False, False, "Lower_Leg_Region_Weight", False, False, 0)
        foot_region = Clothing("Foot region", 1, False, False, "Foot_Region_Weight", False, False, 0)
        upper_arm_region = Clothing("Upper arm region", 1, False, False, "Upper_Arm_Region_Weight", True, False, 0) #Counts as "draws breasts" because it is very often covered by them. All region masks might eventually take this approach.
        lower_arm_region = Clothing("Lower arm region", 1, False, False, "Lower_Arm_Region_Weight", False, False, 0)
        hand_region = Clothing("Hand region", 1, False, False, "Hand_Region_Weight", False, False, 0)

        #NOTE: The autocropt scripts seem to trim a trailing "_", which catches both the end of weight -> weigh and region -> regio. Something to note and fix next time we image things.
        skirt_region = Clothing("Skirt region", 1, False, False, "Skirt_Region_Weight", False, False, 0) # A "Region" that includes everything between the characters legs from hips to about a little above knee level.
        wet_nipple_region = Clothing("Wet nipple region", 1, False, False, "Wet_Nipple_Region", True, False, 0)
        vagina_region = Clothing("Vagina region", 1, False, False, "Vagina_Region", False, False, 0) # TODO: Add this in once images are prepared..

        ##HAIR STYLES##
        #TODO: Implement ordering_variable for hair to decide on hair length for hair cuts.
        hair_styles =  []

        bobbed_hair = Clothing("Bobbed Hair", 1, True, True, "Bobbed_Hair", False, False, 0, whiteness_adjustment = 0.15, contrast_adjustment = 1.3)
        hair_styles.append(bobbed_hair)

        bowl_hair = Clothing("Bowl Hair", 1, True, True, "Coco_Hair", False, False, 0, whiteness_adjustment = 0.15, contrast_adjustment = 1.25)
        hair_styles.append(bowl_hair)

        curly_bun = Clothing("Curly Bun Hair", 1, True, True, "Curly_Bun", False, False, 0, whiteness_adjustment = 0.1, contrast_adjustment = 1.15)
        hair_styles.append(curly_bun)

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

        braided_bun = Clothing("Braided Hair", 1, True, True, "Braided_Bun", False, False, 0, whiteness_adjustment = 0.15, contrast_adjustment = 1.25) #TODO: Double check this has a proper offset dict entry
        hair_styles.append(braided_bun)

        windswept_hair = Clothing("Messy Short Hair", 1, True, True, "Wind_Swept_Hair", False, False, 0, whiteness_adjustment = 0.15, contrast_adjustment = 1.25)
        hair_styles.append(windswept_hair)

        ##PUBES STYLES##
        # NOTE: The oredering variable here is the relative size/length of pubes. Styles with lower numbers are "smaller" than larger, requiring an arbitrary amount of time to grow into larger styles
        pube_styles = []

        shaved_pubes = Clothing("Shaved Pubic Hair", 1, True, True, None, False, False, 0, ordering_variable = 0) #Default pubes used when she is clean shaven. Every girl before v0.23.
        pube_styles.append(shaved_pubes)

        landing_strip_pubes = Clothing("Landing Strip Pubic Hair", 1, True, True, "Landing_Strip_Pubes", False, False, 0, ordering_variable = 2)
        pube_styles.append(landing_strip_pubes)

        diamond_pubes = Clothing("Diamond Shaped Pubic Hair", 1, True, True, "Diamond_Pubes", False, False, 0, ordering_variable = 3)
        pube_styles.append(diamond_pubes)

        trimmed_pubes = Clothing("Neatly Trimmed Pubic Hair", 1, True, True, "Trimmed_Pubes", False, False, 0, ordering_variable = 5)
        pube_styles.append(trimmed_pubes)

        default_pubes = Clothing("Untrimmed Pubic Hair", 1, True, True, "Default_Pubes", False, False, 0, ordering_variable = 10)
        pube_styles.append(default_pubes)


        bow_hair = Clothing("Bow Hair", 1, True, True, "Bow_Hair", False, False, 0) #NO IMAGES
        # hair_styles.append(bow_hair) #TODO: Still falls into the uncanny valley.


        ##CLOTHING##

        ##Panties
        panties_list = []

        plain_panties = Clothing("Plain Panties", 1, True, True, "Plain_Panties", False, True, 0, tucked = True, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "panties",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        panties_list.append(plain_panties)

        cotton_panties = Clothing("Cotton Panties", 1, True, True, "Cotton_Panties", False, True, 0, tucked = True, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "panties",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        panties_list.append(cotton_panties)

        panties = Clothing("Panties", 1, True, True, "Panties", False, True, 0, tucked = True, whiteness_adjustment = 0.2, contrast_adjustment = 1.4, supported_patterns = {"Two Toned":"Pattern_1","Text":"Pattern_2"}, display_name = "panties",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        panties_list.append(panties)

        boy_shorts = Clothing("Boy Panties", 1, True, True, "Boy_Shorts", False, True, 0, tucked = True, display_name = "panties",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        panties_list.append(boy_shorts)

        cute_panties = Clothing("Cute Panties", 1, True, True, "Cute_Panties", False, True, 0, tucked = True, display_name = "panties",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        panties_list.append(cute_panties)

        kitty_panties = Clothing("Kitty Panties", 1, True, True, "Kitty_Panties", False, True, 1, tucked = True, display_name = "panties", whiteness_adjustment = 0.1,
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        panties_list.append(kitty_panties)

        lace_panties = Clothing("Lace Panties", 1, True, True, "Lace_Panties", False, True, 2, tucked = True, whiteness_adjustment = 0.2, supported_patterns = {"Two Toned":"Pattern_1"},  display_name = "panties",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        panties_list.append(lace_panties)

        cute_lace_panties = Clothing("Cute Lace Panties", 1, True, True, "Cute_Lace_Panties", False, True, 2, tucked = True, display_name = "panties",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        panties_list.append(cute_lace_panties)

        tiny_lace_panties = Clothing("Tiny Lace Panties", 1, True, True, "Tiny_Lace_Panties", False, True, 3, tucked = True, display_name = "panties",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        panties_list.append(tiny_lace_panties)

        thin_panties = Clothing("Thin Panties", 1, True, True, "Thin_Panties", False, True, 1, tucked = True, contrast_adjustment = 1.25, supported_patterns = {"Two Toned":"Pattern_1"},  display_name = "panties",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        panties_list.append(thin_panties)

        thong = Clothing("Thong", 1, True, True, "Thong", False, True, 3, tucked = True, supported_patterns = {"Two Toned":"Pattern_1"},  display_name = "thong",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        panties_list.append(thong)

        tiny_g_string = Clothing("G String", 1, True, True, "Tiny_G_String", False, True, 4, tucked = True, whiteness_adjustment = -0.1, display_name = "g-string",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        panties_list.append(tiny_g_string)

        string_panties = Clothing("String Panties", 1, True, True, "String_Panties", False, True, 4, tucked = True, display_name = "g-string",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        panties_list.append(string_panties)

        strappy_panties = Clothing("Strappy Panties", 1, True, True, "Strappy_Panties", False, True, 3, tucked = True, display_name = "panties",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        panties_list.append(strappy_panties)

        crotchless_panties = Clothing("Crotchless Panties", 1, False, False, "Crotchless_Panties", False, True, 2, tucked = True, whiteness_adjustment = 0.15, contrast_adjustment = 1.1, display_name = "panties",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        panties_list.append(crotchless_panties)


        ##Bras
        bra_list = []

        bra = Clothing("Bra", 1, True, True, "Bra", True, True, 0, supported_patterns = {"Lacey":"Pattern_1"}, display_name = "bra",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_gives_access = True, half_off_reveals = True)
        bra_list.append(bra)

        bralette = Clothing("Bralette", 1, True, True, "Bralette", True, True, 0, display_name = "bra",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_gives_access = True, half_off_reveals = True)
        bra_list.append(bralette)

        sports_bra = Clothing("Sports Bra", 1, True, True, "Sports_Bra", True, True, 0, whiteness_adjustment = 0.35, contrast_adjustment = 1.3, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "bra",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_gives_access = True, half_off_reveals = True)
        bra_list.append(sports_bra)

        strapless_bra = Clothing("Strapless Bra", 1, True, True, "Strapless_Bra", True, True, 1, whiteness_adjustment = 0.2, supported_patterns = {"Two Tone":"Pattern_1"}, display_name = "bra",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_gives_access = True, half_off_reveals = True)
        bra_list.append(strapless_bra)

        lace_bra = Clothing("Lace Bra", 1, True, True, "Lace_Bra", True, True, 2, whiteness_adjustment = 0.2, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "bra",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_gives_access = True, half_off_reveals = True)
        bra_list.append(lace_bra)

        thin_bra = Clothing("Thin Bra", 1, True, True, "Thin_Bra", True, True, 2, whiteness_adjustment = 0.0, contrast_adjustment = 1.3, display_name = "bra",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_gives_access = True, half_off_reveals = True)
        bra_list.append(thin_bra)

        strappy_bra = Clothing("Strappy Bra", 1, True, True, "Strappy_Bra", True, True, 3, display_name = "bra",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_gives_access = True, half_off_reveals = True)
        bra_list.append(strappy_bra)

        quarter_cup_bustier = Clothing("Quarter Cup Bustier", 1, False, False, "Quarter_Cup_Bra", True, True, 8, whiteness_adjustment = 0.3, contrast_adjustment = 0.9, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "bustier")
        bra_list.append(quarter_cup_bustier)

        corset = Clothing("Corset", 1, True, True, "Corset", True, True, 5, whiteness_adjustment = 0.0, contrast_adjustment = 1.4, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "corset")
        bra_list.append(corset)

        teddy = Clothing("Teddy", 1, True, True, "Teddy", True, True, 4, whiteness_adjustment = 0.0, contrast_adjustment = 1.0, display_name = "teddy",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True)
        bra_list.append(teddy)

        kitty_babydoll = Clothing("Kitty Babydoll", 1, True, True, "Kitty_Babydoll", True, True, 4, whiteness_adjustment = 0.1, display_name = "babydoll",
            can_be_half_off = True, half_off_regions = [stomach_region, breast_region], half_off_gives_access = True, half_off_reveals = True)
        bra_list.append(kitty_babydoll)

        cincher = Clothing("Cincher", 1, False, False, "Cincher", True, False, 5, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "corset")
        bra_list.append(cincher)

        heart_pasties = Clothing("Heart Pasties", 1, False, False, "Heart_Pasties", True, True, 8, display_name = "pasties")
        bra_list.append(heart_pasties)


        ##Pants
        pants_list = []

        leggings = Clothing("Leggings", 2, True, True, "Leggings", False, False, 1, whiteness_adjustment = 0.2, contrast_adjustment = 1.8, supported_patterns = {"Cougar Print":"Pattern_1"}, display_name = "leggings",
            can_be_half_off = True, half_off_regions = [pelvis_region, stomach_region], half_off_ignore_regions = [upper_leg_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [upper_leg_region, lower_leg_region, pelvis_region])
        pants_list.append(leggings)

        capris = Clothing("Capris", 2, True, True, "Capris", False, False, 1, whiteness_adjustment = 0.3, contrast_adjustment = 1.1, display_name = "pants",
            can_be_half_off = True, half_off_regions = [pelvis_region, stomach_region], half_off_ignore_regions = [upper_leg_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [upper_leg_region, lower_leg_region, pelvis_region])
        pants_list.append(capris)

        booty_shorts = Clothing("Booty Shorts", 2, True, True, "Booty_Shorts", False, False, 6, whiteness_adjustment = 0.25, contrast_adjustment = 1.1, supported_patterns = {"Text":"Pattern_1"}, display_name = "shorts",
            can_be_half_off = True, half_off_regions = [pelvis_region], half_off_ignore_regions = [upper_leg_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [pelvis_region])
        pants_list.append(booty_shorts)

        jean_hotpants = Clothing("Jean Hotpants", 2, True, True, "Jean_Hotpants", False, False, 4, whiteness_adjustment = 0.1, display_name = "shorts",
            can_be_half_off = True, half_off_regions = [pelvis_region], half_off_ignore_regions = [upper_leg_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [pelvis_region])
        pants_list.append(jean_hotpants)

        daisy_dukes = Clothing("Daisy Dukes", 2, True, True, "Daisy_Dukes", False, False, 6, display_name = "shorts",
            can_be_half_off = True, half_off_regions = [stomach_region, vagina_region], half_off_ignore_regions = [upper_leg_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [pelvis_region])
        pants_list.append(daisy_dukes)

        jeans = Clothing("Jeans", 2, True, True, "Jeans", False, False, 0, display_name = "jeans",
            can_be_half_off = True, half_off_regions = [pelvis_region], half_off_ignore_regions = [upper_leg_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [upper_leg_region, lower_leg_region, pelvis_region])
        pants_list.append(jeans)

        suitpants = Clothing("Suit Pants", 2, True, True, "Suit_Pants", False, False, 0, display_name = "pants",
            can_be_half_off = True, half_off_regions = [pelvis_region], half_off_ignore_regions = [upper_leg_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [upper_leg_region, lower_leg_region, pelvis_region])
        pants_list.append(suitpants)


        ##Skirts
        skirts_list = []

        skirt = Clothing("Skirt", 2, True, False, "Skirt", False, False, 1, display_name = "skirt",
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region, lower_leg_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [skirt_region])
        skirts_list.append(skirt)

        long_skirt = Clothing("Long Skirt", 2, True, True, "Long_Skirt", False, False, 0, whiteness_adjustment = 0.0, contrast_adjustment = 1.0, display_name = "skirt",
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region, lower_leg_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [skirt_region, lower_leg_region])
        skirts_list.append(long_skirt)

        pencil_skirt = Clothing("Pencil Skirt", 2, True, False, "Pencil_Skirt", False, False, 0, whiteness_adjustment = 0.2, display_name = "skirt",
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region, lower_leg_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [skirt_region])
        skirts_list.append(pencil_skirt)

        belted_skirt = Clothing("Belted Skirt", 2, True, False, "Belted_Skirt", False, False, 1, contrast_adjustment = 1.15, supported_patterns = {"Belt":"Pattern_1"}, display_name = "skirt",
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region, lower_leg_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [skirt_region])
        skirts_list.append(belted_skirt)

        lace_skirt = Clothing("Lace Skirt", 2, True, False, "Lace_Skirt", False, False, 1, whiteness_adjustment = 0.15, display_name = "skirt",
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region, lower_leg_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [skirt_region])
        skirts_list.append(lace_skirt)

        mini_skirt = Clothing("Mini Skirt", 2, True, False, "Mini_Skirt", False, False, 5, whiteness_adjustment = 0.4, display_name = "skirt",
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [skirt_region])
        skirts_list.append(mini_skirt)

        micro_skirt = Clothing("Micro Skirt", 2, False, False, "Micro_Skirt", False, False, 8, whiteness_adjustment = 0.2, supported_patterns = {"Two Tone":"Pattern_1"}, display_name = "skirt",
            constrain_regions = [skirt_region])
        skirts_list.append(micro_skirt)




        ##Dresses
        #TODO: Check if the extension or the main piece should have the whiteness adjusments etc.
        dress_list = []

        pinafore_bottom = Clothing("pinafore dress bottom", 2, True, False, "Pinafore_bot", False, False, 0, is_extension = True, display_name = "dress bottom",
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True)
        pinafore = Clothing("pinafore", 3, False, False, "Pinafore", True, False, 0, has_extension = pinafore_bottom, display_name = "pinafore",
            can_be_half_off = True, half_off_regions = [torso_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, stomach_region, skirt_region])
        dress_list.append(pinafore)

        sweater_dress_bottom = Clothing("sweater dress bottom", 2, True, False, "Sweater_Dress_Bot", False, False, 0, is_extension = True, display_name = "dress bottom",
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True)
        sweater_dress = Clothing("sweater dress", 2, True, True, "Sweater_Dress", True, False, 0, has_extension = sweater_dress_bottom, whiteness_adjustment = 0.2, contrast_adjustment = 1.2, supported_patterns = {"Two Toned":"Pattern_1", "Hearts":"Pattern_2"}, display_name = "dress",
            constrain_regions = [torso_region, stomach_region, upper_arm_region, lower_arm_region, skirt_region])
        dress_list.append(sweater_dress)

        summer_dress_bottom = Clothing("summer dress bottom", 2, True, False, "Summer_Dress_Bot", False, False, 0, is_extension = True, display_name = "dress bottom",
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region, lower_leg_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True)
        summer_dress = Clothing("summer dress", 2, True, False, "Summer_Dress", True, False, 0, has_extension = summer_dress_bottom, whiteness_adjustment = 0.1, display_name = "dress",
            can_be_half_off = True, half_off_regions = [torso_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, stomach_region, skirt_region])
        dress_list.append(summer_dress)

        frilly_dress_bottom = Clothing("frilly dress bottom", 2, True, False, "Frilly_Dress_Bot", False, False, 0, is_extension = True, display_name = "dress bottom",
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region, lower_leg_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True)
        frilly_dress = Clothing("frilly dress", 2, True, False, "Frilly_Dress", True, False, 2, has_extension = frilly_dress_bottom, display_name = "dress",
            can_be_half_off = True, half_off_regions = [torso_region], half_off_ignore_regions = [stomach_region, upper_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, stomach_region, skirt_region, upper_arm_region])
        dress_list.append(frilly_dress)

        two_part_dress_bottom = Clothing("two part dress bottom", 2, True, False, "Two_Piece_Dress_Bot", False, False, 0, is_extension = True, display_name = "dress bottom",
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region, lower_leg_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True)
        two_part_dress = Clothing("two part dress", 2, True, True, "Two_Piece_Dress", True, False, 6, has_extension = two_part_dress_bottom, display_name = "dress",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, stomach_region, skirt_region])
        dress_list.append(two_part_dress)

        thin_dress_bottom = Clothing("thin dress bottom", 2, True, False, "Thin_Dress_Bot", False, False, 0, is_extension = True, display_name = "dress bottom",
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region, lower_leg_region], half_off_ignore_regions = [stomach_region, upper_arm_region, lower_arm_region], half_off_gives_access = True, half_off_reveals = True)
        thin_dress = Clothing("thin dress", 2, True, True, "Thin_Dress", True, False, 4, has_extension = thin_dress_bottom, whiteness_adjustment = 0.3, contrast_adjustment = 1.15, display_name = "dress",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_ignore_regions = [stomach_region, upper_arm_region, lower_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region, skirt_region])
        dress_list.append(thin_dress)

        virgin_killer_bottom = Clothing("virgin killer bottom", 3, True, False, "Virgin_Killer_Bot", False, False, 0, is_extension = True, display_name = "dress bottom",
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region, lower_leg_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True)
        virgin_killer = Clothing("Virgin Killer", 2, True, True, "Virgin_Killer", True, False, 5, has_extension = virgin_killer_bottom, display_name = "dress",
            can_be_half_off = True, half_off_regions = [torso_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, stomach_region, skirt_region])
        dress_list.append(virgin_killer)

        evening_dress_bottom = Clothing("evening dress bottom", 2, True, False, "Evening_Dress_Bot", False, False, 0, is_extension = True, display_name = "dress bottom",
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region, lower_leg_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True)
        evening_dress = Clothing("evening dress", 2, True, True, "Evening_Dress", True, False, 2, has_extension = evening_dress_bottom, whiteness_adjustment = 0.4, display_name = "dress",
            can_be_half_off = True, half_off_regions = [torso_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, stomach_region, skirt_region])
        dress_list.append(evening_dress)

        leotard_bottom = Clothing("Leotard bottom", 1, True, True, "Leotard_Bot", False, True, 0, is_extension = True, display_name = "leotard crotch",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        leotard = Clothing("Leotard", 2, True, True, "Leotard", True, False, 5, has_extension = leotard_bottom, tucked = True, display_name = "leotard",
            constrain_regions = [torso_region, stomach_region, pelvis_region, upper_arm_region, lower_arm_region])
        dress_list.append(leotard)

        nightgown_dress_bottom = Clothing("Nightgown bottom", 2, False, False, "Nightgown_Bot", False, True, 0, is_extension = True, display_name = "nightgown bottom",
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region, lower_leg_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True)
        nightgown_dress = Clothing("Nightgown", 2, False, True, "Nightgown", True, True, 3, has_extension = nightgown_dress_bottom, whiteness_adjustment = 0.1, contrast_adjustment = 1.1, display_name = "nightgown",
            can_be_half_off = True, half_off_regions = [torso_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, stomach_region, skirt_region])
        dress_list.append(nightgown_dress)

        bath_robe_bottom = Clothing("Bathrobe bottom", 2, False, False, "Bath_Robe_Bot", False, False, 0, is_extension = True, display_name = "rob bottom",
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region, lower_leg_region], half_off_ignore_regions = [lower_arm_region, stomach_region], half_off_gives_access = True, half_off_reveals = True)
        bath_robe = Clothing("Bathrobe", 2, False, True, "Bath_Robe", True, True, 1, has_extension = bath_robe_bottom, supported_patterns = {"Flowers":"Pattern_1"}, display_name = "robe",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_ignore_regions = [upper_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region, skirt_region])
        dress_list.append(bath_robe)

        lacy_one_piece_underwear_bottom = Clothing("lacy one piece bottom", 1, True, True, "Lacy_One_Piece_Underwear_Bot", False, True, 0, is_extension = True, display_name = "underwear crotch",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        lacy_one_piece_underwear = Clothing("lacy one piece", 1, True, True, "Lacy_One_Piece_Underwear", True, True, 4, tucked = True, has_extension = lacy_one_piece_underwear_bottom, whiteness_adjustment = 0.2, display_name = "underwear",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_gives_access = True, half_off_reveals = True)
        dress_list.append(lacy_one_piece_underwear)

        lingerie_one_piece_bottom = Clothing("lingerie one piece bottom", 1, True, True, "Lingerie_One_Piece_Bot", False, True, 0, is_extension = True, display_name = "underwear crotch",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        lingerie_one_piece = Clothing("lingerie one piece", 1, True, True, "Lingerie_One_Piece", True, True, 8, tucked = True, has_extension = lingerie_one_piece_bottom, supported_patterns = {"Flowers":"Pattern_1"}, display_name = "underwear",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, stomach_region, pelvis_region])
        dress_list.append(lingerie_one_piece)

        bodysuit_underwear_bottom = Clothing("bodysuit underwear bottom", 1, True, True, "Bodysuit_Underwear_Bot", False, True, 0, is_extension = True, display_name = "bodysuit crotch",
            can_be_half_off = True, half_off_regions = [vagina_region], half_off_gives_access = True, half_off_reveals = True)
        bodysuit_underwear = Clothing("bodysuit underwear", 1, True, True, "Bodysuit_Underwear", True, True, 6, tucked = True, has_extension = bodysuit_underwear_bottom, whiteness_adjustment = 0.2, display_name = "bodysuit",
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region, pelvis_region])
        dress_list.append(bodysuit_underwear)

        towel_bottom = Clothing("Towel bottom", 1, True, True, "Towel_Bot", False, False, 0, is_extension = True, display_name = "towel bottom",
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region], half_off_gives_access = True, half_off_reveals = True)
        towel = Clothing("Towel", 1, True, True, "Towel", True, False, 1, has_extension = towel_bottom, display_name = "towel",
            can_be_half_off = True, half_off_regions = [torso_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, stomach_region, skirt_region])
        # dress_list.append(towel) #Not a standard dress item, so not on the list.

        apron_bottom = Clothing("Apron", 3, False, False, "Apron_Bot", False, False, 0, is_extension = True,
            can_be_half_off = True, half_off_regions = [pelvis_region, upper_leg_region], half_off_gives_access = True, half_off_reveals = True, display_name = "arpon bottom")
        apron = Clothing("Apron", 3, False, True, "Apron", True, False, 0, has_extension = apron_bottom, supported_patterns = {"Plaid":"Pattern_1"}, whiteness_adjustment = -0.1, display_name = "apron",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [stomach_region])
        dress_list.append(apron)

        ##Shirts
        shirts_list = []

        tshirt = Clothing("Tshirt", 2, True, True, "Tshirt", True, False, 1, whiteness_adjustment = 0.35, supported_patterns = {"Striped":"Pattern_2","Text":"Pattern_3"}, display_name = "shirt",
            can_be_half_off = True, half_off_regions = [breast_region, stomach_region, pelvis_region], half_off_ignore_regions = [upper_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, upper_arm_region, stomach_region])
        shirts_list.append(tshirt)

        lace_sweater = Clothing("Lace Sweater", 2, True, True, "Lace_Sweater", True, False, 2, opacity_adjustment = 1.08, whiteness_adjustment = 0.18, display_name = "sweater",
            can_be_half_off = True, half_off_regions = [breast_region, stomach_region], half_off_ignore_regions = [upper_arm_region, lower_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region])
        shirts_list.append(lace_sweater)

        long_sweater = Clothing("Long Sweater", 2, True, True, "Long_Sweater", True, False, 0, whiteness_adjustment = 0.2, supported_patterns = {"Striped":"Pattern_1"}, display_name = "sweater",
            can_be_half_off = True, half_off_regions = [breast_region, stomach_region, pelvis_region, upper_leg_region], half_off_ignore_regions = [upper_arm_region, lower_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region])
        shirts_list.append(long_sweater)

        sleeveless_top = Clothing ("Sleeveless Top", 2, True, True, "Sleveless_Top", True, False, 0, tucked = True, display_name = "shirt",
            can_be_half_off = True, half_off_regions = [breast_region, stomach_region, pelvis_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, stomach_region])
        shirts_list.append(sleeveless_top)

        long_tshirt = Clothing("Long Tshirt", 2, True, True, "Long_Tshirt", True, False, 0, whiteness_adjustment = 0.25, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "shirt",
            can_be_half_off = True, half_off_regions = [breast_region, stomach_region, pelvis_region, upper_leg_region], half_off_ignore_regions = [upper_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, stomach_region])
        shirts_list.append(long_tshirt)

        frilly_longsleeve_shirt = Clothing("frilly longsleeve shirt", 2, True, True, "Frilly_Longsleeve_Shirt", True, False, 0, display_name = "shirt",
            can_be_half_off = True, half_off_regions = [breast_region, stomach_region, pelvis_region], half_off_ignore_regions = [upper_arm_region, lower_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, stomach_region, upper_arm_region, lower_arm_region])
        shirts_list.append(frilly_longsleeve_shirt)

        sweater = Clothing("Sweater", 2, True, True, "Sweater", True, False, 1, whiteness_adjustment = 0.1, display_name = "sweater",
            can_be_half_off = True, half_off_regions = [breast_region, stomach_region], half_off_ignore_regions = [upper_arm_region, lower_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, upper_arm_region, stomach_region, upper_arm_region, lower_arm_region])
        shirts_list.append(sweater)

        belted_top = Clothing("Belted Top", 2, True, True, "Belted_Top", True, False, 5, contrast_adjustment = 1.1, display_name = "vest",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region])
        shirts_list.append(belted_top)

        lace_crop_top = Clothing("Lace Crop Top", 2, True, True, "Lace_Crop_Top", True, False, 2, whiteness_adjustment = 0.1, contrast_adjustment = 1.1, display_name = "top",
            can_be_half_off = True, half_off_regions = [breast_region, stomach_region], half_off_ignore_regions = [upper_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, upper_arm_region])
        shirts_list.append(lace_crop_top)

        tanktop = Clothing("Tanktop", 2, True, True, "Tanktop", True, False, 3, display_name = "top",
            can_be_half_off = True, half_off_regions = [breast_region, stomach_region, pelvis_region], half_off_ignore_regions = [upper_arm_region, lower_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, stomach_region])
        shirts_list.append(tanktop)

        camisole = Clothing("Camisole", 2, True, True, "Camisole", True, False, 1, whiteness_adjustment = 0.2, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "camisole",
            can_be_half_off = True, half_off_regions = [breast_region, stomach_region, pelvis_region, upper_leg_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, stomach_region, skirt_region])
        shirts_list.append(camisole)

        long_sleeve_blouse = Clothing("Buttoned Blouse", 2, True, True, "Long_Sleeve_Blouse", True, False, 0, whiteness_adjustment = 0.2, display_name = "blouse",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_ignore_regions = [upper_arm_region, lower_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region])
        shirts_list.append(long_sleeve_blouse)

        short_sleeve_blouse = Clothing("Short Sleeve Blouse", 2, True, True, "Short_Sleeve_Blouse", True, False, 0, whiteness_adjustment = 0.3, display_name = "blouse",
            can_be_half_off = True, half_off_regions = [breast_region, stomach_region, pelvis_region], half_off_ignore_regions = [upper_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, upper_arm_region, stomach_region])
        shirts_list.append(short_sleeve_blouse)

        wrapped_blouse = Clothing("Wrapped Blouse", 2, True, True, "Wrapped_Blouse", True, False, 0, whiteness_adjustment = 0.25, contrast_adjustment = 1.05, display_name = "blouse",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_ignore_regions = [upper_arm_region, lower_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region])
        shirts_list.append(wrapped_blouse)

        tube_top = Clothing("Tube Top", 2, True, True, "Tube_Top", True, False, 4, supported_patterns = {"Cougar Print":"Pattern_1","Text":"Pattern_2"}, display_name = "top",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_ignore_regions = [stomach_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [breast_region, stomach_region])
        shirts_list.append(tube_top)

        tie_sweater = Clothing("Tied Sweater", 2, True, True, "Tie_Sweater", True, False, 0, whiteness_adjustment = 0.3, contrast_adjustment = 1.1, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "sweater",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_ignore_regions = [upper_arm_region, lower_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region])
        shirts_list.append(tie_sweater)

        dress_shirt = Clothing("Dress Shirt", 2, True, True, "Dress_Shirt", True, False, 0, tucked = True, opacity_adjustment = 1.12, display_name = "shirt",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_ignore_regions = [upper_arm_region, lower_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region])
        shirts_list.append(dress_shirt)

        lab_coat = Clothing("Lab Coat", 3, True, True, "Lab_Coat", True, False, 0, opacity_adjustment = 1.08, display_name = "coat",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_ignore_regions = [upper_arm_region, lower_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region, skirt_region])
        shirts_list.append(lab_coat)

        suit_jacket = Clothing("Suit Jacket", 3, True, True, "Suit_Jacket", True, False, 0, display_name = "jacket",
            can_be_half_off = True, half_off_regions = [breast_region], half_off_ignore_regions = [upper_arm_region, lower_arm_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region])
        shirts_list.append(suit_jacket)

        vest = Clothing("Vest", 3, False, True, "Vest", True, False, 0, display_name = "vest",
            constrain_regions = [torso_region])
        shirts_list.append(vest)

        business_vest = Clothing("Business Vest", 3, True, True, "Tight_Vest", True, False, 2, whiteness_adjustment = 0.15, opacity_adjustment = 1.3, display_name = "vest",
            can_be_half_off = True, half_off_regions = [breast_region, stomach_region], half_off_gives_access = True, half_off_reveals = True,
            constrain_regions = [torso_region])
        shirts_list.append(business_vest)


        ##Socks##
        socks_list = []

        short_socks = Clothing("Short Socks", 1, True, True, "Short_Socks", False, False, 0, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "socks")
        socks_list.append(short_socks)

        medium_socks = Clothing("Medium Socks", 1, True, True, "Long_Socks", False, False, 0, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "socks")
        socks_list.append(medium_socks)

        high_socks = Clothing("High Socks", 1, True, True, "High_Socks", False, False, 0, contrast_adjustment = 1.2, supported_patterns = {"Two Toned":"Pattern_1", "Gradient":"Pattern_2"}, display_name = "socks")
        socks_list.append(high_socks)

        thigh_highs = Clothing("Thigh Highs", 1, True, True, "Thigh_Highs", False, False, 5, whiteness_adjustment = 0.1, display_name = "stockings")
        socks_list.append(thigh_highs)

        fishnets = Clothing("Fishnets", 1, True, True, "Fishnets", False, False, 10, whiteness_adjustment = 0.2, display_name = "fishnets")
        socks_list.append(fishnets)

        garter_with_fishnets = Clothing("Garter and Fishnets", 1, True, True, "Garter_and_Fishnets", False, False, 12, whiteness_adjustment = 0.2, contrast_adjustment = 1.0, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "fishnets")
        socks_list.append(garter_with_fishnets)


#        ##Shoes##

        shoes_list = []

        sandles = Clothing("Sandals", 2, True, True, "Sandles", False, False, 0, display_name = "sandals",
            constrain_regions = [foot_region])
        shoes_list.append(sandles)

        shoes = Clothing("Shoes", 2, True, True, "Shoes", False, False, 0, display_name = "shoes",
            constrain_regions = [foot_region])
        shoes_list.append(shoes)

        slips = Clothing("Slips", 2, True, True, "Slips", False, False, 0, display_name = "slips",
            constrain_regions = [foot_region])
        shoes_list.append(slips)

        sneakers = Clothing("Sneakers", 2, True, True, "Sneakers", False, False, 0, whiteness_adjustment = 0.2, supported_patterns = {"Laces":"Pattern_1"}, display_name = "shoes",
            constrain_regions = [foot_region])
        shoes_list.append(sneakers)

        sandle_heels = Clothing("Sandal Heels", 2, True, True, "Sandal_Heels", False, False, 1, display_name = "heels",
            constrain_regions = [foot_region])
        shoes_list.append(sandle_heels)

        pumps = Clothing("Pumps", 2, True, True, "Pumps", False, False, 1, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "pumps",
            constrain_regions = [foot_region])
        shoes_list.append(pumps)

        heels = Clothing("Heels", 2, True, True, "Heels", False, False, 1, whiteness_adjustment = 0.2, display_name = "heels",
            constrain_regions = [foot_region])
        shoes_list.append(heels)

        high_heels = Clothing("High Heels", 2, True, True, "High_Heels", False, False, 3, display_name = "heels",
            constrain_regions = [foot_region])
        shoes_list.append(high_heels)

        boot_heels = Clothing("Boot Heels", 2, True, True, "Boot_Heels", False, False, 1, whiteness_adjustment = 0.1, contrast_adjustment = 1.1, display_name = "boots",
            constrain_regions = [foot_region])
        shoes_list.append(boot_heels)

        tall_boots = Clothing("Tall Boots", 2, True, True, "High_Boots", False, False, 0, display_name = "boots",
            constrain_regions = [foot_region, lower_leg_region])
        shoes_list.append(tall_boots)

        thigh_high_boots = Clothing("Thigh High Boots", 2, True, True, "Thigh_Boots", False, False, 3, display_name = "boots",
            constrain_regions = [foot_region, lower_leg_region, upper_leg_region])
        shoes_list.append(thigh_high_boots)


        ##Accessories##
        earings_list = [] #Note: now more properly known as facial accessories

        chandelier_earings = Clothing("Chandelier Earrings", 2, False, False, "Chandelier_Earings", False, False, 0, body_dependant = False, display_name = "earings")
        earings_list.append(chandelier_earings)

        gold_earings = Clothing("Gold Earings", 2 , False, False, "Gold_Earings", False, False, 0, body_dependant = False, display_name = "earings")
        earings_list.append(gold_earings)

        modern_glasses = Facial_Accessory("Modern Glasses", 2, False, False, "Modern_Glasses", False, False, 0, display_name = "earings")
        earings_list.append(modern_glasses)

        big_glasses = Facial_Accessory("Big Glasses", 2, False, False, "Big_Glasses", False, False, 0, display_name = "glasses")
        earings_list.append(big_glasses)

        sunglasses = Facial_Accessory("Sunglasses", 2, False, False, "Sunglasses", False, False, 0, display_name = "sunglasses")
        earings_list.append(sunglasses)

        head_towel = Clothing("Head Towel", 2, False, False, "Head_Towel", False, False, 0, body_dependant = False, display_name = "head towel")
        # earings_list.append(head_towel) #TEMPORARY FOR TESTING

        ball_gag = Facial_Accessory("Ball Gag", 2, False, False, "Ball_Gag", False, False, 15, display_name = "Gag", modifier_lock = "blowjob") #TODO: Get the ball gag text modifier working
        #earings_list.append(ball_gag) #TEMPORARY FOR TESTING


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

        copper_bracelet = Clothing("Copper Bracelet", 2, False, False, "Copper_Bracelet", False, False, 0, display_name = "bracelet")
        bracelet_list.append(copper_bracelet)

        gold_bracelet = Clothing("Gold Bracelet", 2, False, False, "Gold_Bracelet", False, False, 0, display_name = "bracelet")
        bracelet_list.append(gold_bracelet)

        spiked_bracelet = Clothing("Spiked Bracelet", 2, False, False, "Spiked_Bracelet", False, False, 2, display_name = "bracelet")
        bracelet_list.append(spiked_bracelet)

        bead_bracelet = Clothing("Bead Bracelet", 2, False, False, "Bead_Bracelet", False, False, 0, display_name = "bracelet")
        bracelet_list.append(bead_bracelet)

        colourful_bracelets = Clothing("Colourful Bracelets", 2, False, False, "Colourful_Bracelets", False, False, 0, display_name = "bracelets")
        bracelet_list.append(colourful_bracelets)

        forearm_gloves = Clothing("Forearm Gloves", 2, False, False, "Forearm_Gloves", False, False, 2, supported_patterns = {"Two Tone":"Pattern_1"}, display_name = "gloves")
        bracelet_list.append(forearm_gloves)


        rings_list = []

        diamond_ring = Clothing("Diamond Ring", 2, False, False, "Diamond_Ring", False, False, 0, display_name = "ring")
        rings_list.append(diamond_ring)

        garnet_ring = Clothing("Garnet Ring", 2, False, False, "Garnet_Ring", False, False, 0, display_name = "ring")
        rings_list.append(garnet_ring)

        copper_ring_set = Clothing("Copper Ring Set", 2, False, False, "Copper_Ring_Set", False, False, 0, display_name = "rings")
        rings_list.append(copper_ring_set)


        neckwear_list = []

        wool_scarf = Clothing("Wool Scarf", 3, False, False, "Wool_Scarf", False, False, 0, display_name = "scarf")
        neckwear_list.append(wool_scarf)

        necklace_set = Clothing("Necklace Set", 3, False, False, "Necklace_Set", True, False, 0, display_name = "necklaces")
        neckwear_list.append(necklace_set)

        gold_chain_necklace = Clothing("Gold Chain Necklace", 3, False, False, "Gold_Chain_Necklace", False, False, 0, display_name = "necklace")
        neckwear_list.append(gold_chain_necklace)

        spiked_choker = Clothing("Spiked Choker", 3, False, False, "Spiked_Choker", False, False, 3, display_name = "choker")
        neckwear_list.append(spiked_choker)

        lace_choker = Clothing("Lace Choker", 2, False, False, "Lace_Choker", False, False, 3, whiteness_adjustment = 0.1, display_name = "choker")
        neckwear_list.append(lace_choker)

        wide_choker = Clothing("Wide Choker", 2, False, False, "Wide_Choker", False, False, 3, display_name = "choker")
        neckwear_list.append(wide_choker)

        breed_collar = Clothing("Breed Me Collar", 3, False, False, "Collar_Breed", False, False, 8, supported_patterns = {"Two Tone":"Pattern_1"}, display_name = "collar")
        neckwear_list.append(breed_collar)

        cum_slut_collar = Clothing("Cum Slut Collar", 3, False, False, "Collar_Cum_Slut", False, False, 8, supported_patterns = {"Two Tone":"Pattern_1"}, display_name = "collar")
        neckwear_list.append(cum_slut_collar)

        fuck_doll_collar = Clothing("Fuck Doll Collar", 3, False, False, "Collar_Fuck_Doll", False, False, 8, supported_patterns = {"Two Tone":"Pattern_1"}, display_name = "collar")
        neckwear_list.append(fuck_doll_collar)




        ##Non Clothing Accessories##
        ass_cum = Clothing("Ass Cum", 1, False, False, "Ass_Covered", False, False, 10, whiteness_adjustment = 0.2)

        tits_cum = Clothing("Tit Cum", 1, False, False, "Tits_Covered", True, False, 10, whiteness_adjustment = 0.2)

        stomach_cum = Clothing("Stomach Cum", 1, False, False, "Stomach_Covered", False, False, 10, whiteness_adjustment = 0.2)

        creampie_cum = Clothing("Creampie", 1, False, False, "Creampie", False, False, 10, whiteness_adjustment = 0.2)

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

        def wardrobe_from_xml(xml_filename, in_import = False):
            # file_path = os.path.abspath(os.path.join(config.basedir, "game"))
            # file_path = os.path.join(file_path,"wardrobes")
            # file_name = os.path.join(file_path, xml_filename + ".xml")
            wardrobe_file = None
            if in_import:
                modified_filename = "wardrobes/imports/" + xml_filename + ".xml"
            else:
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

        default_wardrobe = wardrobe_from_xml("Master_Default_Wardrobe")

        lingerie_wardrobe = wardrobe_from_xml("Lingerie_Wardrobe")

        insta_wardrobe = wardrobe_from_xml("Insta_Wardrobe")
