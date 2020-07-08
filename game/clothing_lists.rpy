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

        skirt_region = Clothing("Skirt region", 1, False, False, "Skirt_Region_Weight", False, False, 0) # A "Region" that includes everything between the characters legs from hips to about a little above knee level.
        wet_nipple_region = Clothing("Wet nipple region", 1, False, False, "Wet_Nipple_Region", True, False, 0)

        ##HAIR STYLES##
        #TODO: Implement ordering_variable for hair to decide on hair length for hair cuts.
        hair_styles =  []

        bobbed_hair = Clothing("Bobbed Hair", 1, True, True, "Bobbed_Hair", False, False, 0, whiteness_adjustment = 0.15, contrast_adjustment = 1.3,
            crop_offset_dict = {"cowgirl":(229,123), "missionary":(307,31), "kissing":(247,12), "sitting":(367,118), "against_wall":(169,0), "back_peek":(142,37), "blowjob":(195,192), "stand4":(204,34), "stand5":(225,24), "kneeling1":(229,141), "walking_away":(179,36), "doggy":(223,73), "stand2":(160,44), "stand3":(170,6)})
        hair_styles.append(bobbed_hair)

        bowl_hair = Clothing("Bowl Hair", 1, True, True, "Coco_Hair", False, False, 0, whiteness_adjustment = 0.15, contrast_adjustment = 1.25,
            crop_offset_dict = {"cowgirl":(209,137), "missionary":(291,39), "kissing":(234,17), "sitting":(350,129), "against_wall":(157,8), "back_peek":(123,48), "blowjob":(174,201), "stand4":(189,46), "stand5":(209,33), "kneeling1":(207,152), "walking_away":(164,46), "doggy":(206,78), "stand2":(143,57), "stand3":(159,15)})
        hair_styles.append(bowl_hair)

        curly_bun = Clothing("Curly Bun Hair", 1, True, True, "Curly_Bun", False, False, 0, whiteness_adjustment = 0.1, contrast_adjustment = 1.15,
            crop_offset_dict = {"cowgirl":(250,56), "missionary":(326,0), "kissing":(261,0), "sitting":(380,66), "against_wall":(190,0), "back_peek":(131,0), "blowjob":(212,131), "stand4":(220,0), "stand5":(240,0), "kneeling1":(222,84), "walking_away":(189,0), "doggy":(211,28), "stand2":(145,2), "stand3":(191,0)})
        hair_styles.append(curly_bun)

        short_hair = Clothing("Short Hair", 1, True, True, "Short_Hair",False, False, 0,  whiteness_adjustment = 0.1, contrast_adjustment = 1.2,
            crop_offset_dict = {"cowgirl":(241,128), "missionary":(317,31), "kissing":(260,10), "sitting":(372,119), "against_wall":(182,0), "back_peek":(140,41), "blowjob":(204,198), "stand4":(214,37), "stand5":(232,25), "kneeling1":(231,145), "walking_away":(181,38), "doggy":(219,77), "stand2":(158,51), "stand3":(184,8)})
        hair_styles.append(short_hair)

        messy_hair = Clothing("Messy Hair", 1, True, True, "Messy_Long_Hair", False, False, 0, whiteness_adjustment = 0.1, contrast_adjustment = 1.4,
            crop_offset_dict = {"cowgirl":(200,117), "missionary":(283,28), "kissing":(221,9), "sitting":(341,115), "against_wall":(150,0), "back_peek":(133,37), "blowjob":(164,186), "stand4":(185,32), "stand5":(200,21), "kneeling1":(198,137), "walking_away":(178,34), "doggy":(221,68), "stand2":(141,46), "stand3":(152,3)})
        hair_styles.append(messy_hair)

        messy_short_hair = Clothing("Messy Short Hair", 1, True, True, "Messy_Short_Hair", False, False, 0, whiteness_adjustment = 0.1, contrast_adjustment = 1.1,
            crop_offset_dict = {"cowgirl":(217,127), "missionary":(298,31), "kissing":(243,12), "sitting":(356,119), "against_wall":(164,0), "back_peek":(129,40), "blowjob":(181,195), "stand4":(195,37), "stand5":(216,24), "kneeling1":(207,142), "walking_away":(168,38), "doggy":(209,76), "stand2":(142,49), "stand3":(166,7)})
        hair_styles.append(messy_short_hair)

        shaved_side_hair = Clothing("Shaved Side Hair", 1, True, True, "Shaved_Side_Hair", False, False, 0,
            crop_offset_dict = {"cowgirl":(234,120), "missionary":(312,28), "kissing":(248,7), "sitting":(367,115), "against_wall":(178,0), "back_peek":(138,36), "blowjob":(197,186), "stand4":(205,31), "stand5":(224,21), "kneeling1":(217,137), "walking_away":(193,33), "doggy":(216,67), "stand2":(149,46), "stand3":(180,3)})
        hair_styles.append(shaved_side_hair)

        messy_ponytail = Clothing("Messy Ponytail", 1, True, True, "Messy_Ponytail", False, False, 0, whiteness_adjustment = 0.3, contrast_adjustment = 1.1,
            crop_offset_dict = {"cowgirl":(239,134), "missionary":(314,39), "kissing":(252,20), "sitting":(372,124), "against_wall":(176,6), "back_peek":(99,46), "blowjob":(200,201), "stand4":(212,42), "stand5":(227,29), "kneeling1":(229,151), "walking_away":(180,42), "doggy":(211,79), "stand2":(160,55), "stand3":(181,12)})
        hair_styles.append(messy_ponytail)

        twintail = Clothing("Twintails", 1, True, True, "Twin_Ponytails", False, False, 0, whiteness_adjustment = 0.1, contrast_adjustment = 1.1,
            crop_offset_dict = {"cowgirl":(216,119), "missionary":(298,40), "kissing":(249,18), "sitting":(354,122), "against_wall":(164,5), "back_peek":(124,33), "blowjob":(183,183), "stand4":(190,35), "stand5":(220,24), "kneeling1":(202,146), "walking_away":(168,40), "doggy":(207,65), "stand2":(134,37), "stand3":(167,7)})
        hair_styles.append(twintail)

        ponytail = Clothing("Ponytail", 1, True, True, "Ponytail", False, False, 0, whiteness_adjustment = 0.3, contrast_adjustment = 1.3,
            crop_offset_dict = {"cowgirl":(248,79), "missionary":(322,24), "kissing":(267,5), "sitting":(385,97), "against_wall":(188,0), "back_peek":(105,23), "blowjob":(215,146), "stand4":(214,6), "stand5":(245,7), "kneeling1":(243,131), "walking_away":(195,16), "doggy":(224,30), "stand2":(169,22), "stand3":(190,0)})
        hair_styles.append(ponytail)

        long_hair = Clothing("Long Hair", 1, True, True, "Long_Hair", False, False, 0, whiteness_adjustment = 0.2, contrast_adjustment = 1.8,
            crop_offset_dict = {"cowgirl":(148,138), "missionary":(233,42), "kissing":(151,22), "sitting":(303,128), "against_wall":(102,10), "back_peek":(118,49), "blowjob":(105,207), "stand4":(159,46), "stand5":(140,33), "kneeling1":(194,154), "walking_away":(117,46), "doggy":(211,84), "stand2":(144,59), "stand3":(101,16)})
        hair_styles.append(long_hair)

        braided_bun = Clothing("Braided Hair", 1, True, True, "Braided_Bun", False, False, 0, whiteness_adjustment = 0.15, contrast_adjustment = 1.25)
        hair_styles.append(braided_bun)

        windswept_hair = Clothing("Messy Short Hair", 1, True, True, "Wind_Swept_Hair", False, False, 0, whiteness_adjustment = 0.15, contrast_adjustment = 1.25,
            crop_offset_dict = {"cowgirl":(228,126), "missionary":(307,33), "kissing":(250,13), "sitting":(363,121), "against_wall":(173,1), "back_peek":(138,46), "blowjob":(192,196), "stand4":(203,38), "stand5":(224,25), "kneeling1":(216,146), "walking_away":(175,39), "doggy":(216,77), "stand2":(149,55), "stand3":(176,8)})
        hair_styles.append(windswept_hair)

        ##PUBES STYLES##
        # NOTE: The oredering variable here is the relative size/length of pubes. Styles with lower numbers are "smaller" than larger, requiring an arbitrary amount of time to grow into larger styles
        pube_styles = []

        shaved_pubes = Clothing("Shaved Pubic Hair", 1, True, True, None, False, False, 0, ordering_variable = 0) #Default pubes used when she is clean shaven. Every girl before v0.23.
        pube_styles.append(shaved_pubes)

        landing_strip_pubes = Clothing("Landing Strip Pubic Hair", 1, True, True, "Landing_Strip_Pubes", False, False, 0, ordering_variable = 2,
            crop_offset_dict = {"cowgirl":(320,641), "missionary":(364,474), "kissing":(316,516), "sitting":(0,0), "against_wall":(260,511), "back_peek":(0,0), "blowjob":(260,665), "stand4":(244,531), "stand5":(248,509), "kneeling1":(294,692), "walking_away":(0,0), "doggy":(323,632), "stand2":(172,541), "stand3":(269,498)})
        pube_styles.append(landing_strip_pubes)

        diamond_pubes = Clothing("Diamond Shaped Pubic Hair", 1, True, True, "Diamond_Pubes", False, False, 0, ordering_variable = 3,
            crop_offset_dict = {"cowgirl":(313,638), "missionary":(356,465), "kissing":(309,514), "sitting":(0,0), "against_wall":(253,508), "back_peek":(0,0), "blowjob":(253,663), "stand4":(239,527), "stand5":(241,506), "kneeling1":(288,691), "walking_away":(235,523), "doggy":(316,453), "stand2":(166,537), "stand3":(262,494)})
        pube_styles.append(diamond_pubes)

        trimmed_pubes = Clothing("Neatly Trimmed Pubic Hair", 1, True, True, "Trimmed_Pubes", False, False, 0, ordering_variable = 5,
            crop_offset_dict = {"cowgirl":(312,653), "missionary":(357,493), "kissing":(314,525), "sitting":(0,0), "against_wall":(253,521), "back_peek":(0,0), "blowjob":(253,674), "stand4":(238,540), "stand5":(245,516), "kneeling1":(287,698), "walking_away":(234,523), "doggy":(319,455), "stand2":(173,547), "stand3":(261,510)})
        pube_styles.append(trimmed_pubes)

        default_pubes = Clothing("Untrimmed Pubic Hair", 1, True, True, "Default_Pubes", False, False, 0, ordering_variable = 10,
            crop_offset_dict = {"cowgirl":(296,640), "missionary":(338,473), "kissing":(298,514), "sitting":(398,596), "against_wall":(237,508), "back_peek":(0,0), "blowjob":(237,662), "stand4":(230,526), "stand5":(227,506), "kneeling1":(273,685), "walking_away":(0,0), "doggy":(303,628), "stand2":(156,533), "stand3":(244,496)})
        pube_styles.append(default_pubes)


        bow_hair = Clothing("Bow Hair", 1, True, True, "Bow_Hair", False, False, 0) #NO IMAGES
        # hair_styles.append(bow_hair) #TODO: Still falls into the uncanny valley.


        ##CLOTHING##

        ##Panties
        panties_list = []

        plain_panties = Clothing("Plain Panties", 1, True, True, "Plain_Panties", False, True, 0, tucked = True, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "panties",
            crop_offset_dict = {"cowgirl":(229,534), "missionary":(277,387), "kissing":(223,397), "sitting":(353,509), "against_wall":(170,408), "back_peek":(135,422), "blowjob":(159,555), "stand4":(190,417), "stand5":(164,398), "kneeling1":(241,562), "walking_away":(162,402), "doggy":(291,295), "stand2":(122,424), "stand3":(171,390)})
        panties_list.append(plain_panties)

        cotton_panties = Clothing("Cotton Panties", 1, True, True, "Cotton_Panties", False, True, 0, tucked = True, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "panties",
            crop_offset_dict = {"cowgirl":(223,548), "missionary":(251,424), "kissing":(220,405), "sitting":(354,528), "against_wall":(155,418), "back_peek":(109,439), "blowjob":(141,562), "stand4":(147,431), "stand5":(158,402), "kneeling1":(179,566), "walking_away":(140,428), "doggy":(230,306), "stand2":(103,442), "stand3":(156,420)})
        panties_list.append(cotton_panties)

        panties = Clothing("Panties", 1, True, True, "Panties", False, True, 0, tucked = True, whiteness_adjustment = 0.2, contrast_adjustment = 1.4, supported_patterns = {"Two Toned":"Pattern_1","Text":"Pattern_2"}, display_name = "panties",
            crop_offset_dict = {"cowgirl":(224,570), "missionary":(255,443), "kissing":(222,420), "sitting":(356,546), "against_wall":(158,427), "back_peek":(123,458), "blowjob":(142,563), "stand4":(152,447), "stand5":(160,416), "kneeling1":(182,590), "walking_away":(142,441), "doggy":(275,326), "stand2":(107,453), "stand3":(157,432)})
        panties_list.append(panties)

        boy_shorts = Clothing("Boy Panties", 1, True, True, "Boy_Shorts", False, True, 0, tucked = True, display_name = "panties",
            crop_offset_dict = {"cowgirl":(171,563), "missionary":(243,425), "kissing":(221,410), "sitting":(352,542), "against_wall":(146,423), "back_peek":(109,448), "blowjob":(135,563), "stand4":(131,441), "stand5":(154,406), "kneeling1":(158,591), "walking_away":(128,434), "doggy":(200,313), "stand2":(93,450), "stand3":(146,423)})
        panties_list.append(boy_shorts)

        cute_panties = Clothing("Cute Panties", 1, True, True, "Cute_Panties", False, True, 0, tucked = True, display_name = "panties",
            crop_offset_dict = {"cowgirl":(223,563), "missionary":(254,445), "kissing":(221,414), "sitting":(319,543), "against_wall":(156,425), "back_peek":(129,455), "blowjob":(141,563), "stand4":(150,446), "stand5":(159,411), "kneeling1":(180,591), "walking_away":(142,443), "doggy":(289,319), "stand2":(104,458), "stand3":(156,437)})
        panties_list.append(cute_panties)

        lace_panties = Clothing("Lace Panties", 1, True, True, "Lace_Panties", False, True, 2, tucked = True, whiteness_adjustment = 0.2, supported_patterns = {"Two Toned":"Pattern_1"},  display_name = "panties",
            crop_offset_dict = {"cowgirl":(224,546), "missionary":(259,430), "kissing":(223,402), "sitting":(354,520), "against_wall":(160,417), "back_peek":(144,433), "blowjob":(145,563), "stand4":(162,428), "stand5":(161,401), "kneeling1":(241,563), "walking_away":(149,422), "doggy":(295,301), "stand2":(110,440), "stand3":(161,416)})
        panties_list.append(lace_panties)

        cute_lace_panties = Clothing("Cute Lace Panties", 1, True, True, "Cute_Lace_Panties", False, True, 2, tucked = True, display_name = "panties",
            crop_offset_dict = {"cowgirl":(223,570), "missionary":(255,442), "kissing":(221,412), "sitting":(355,544), "against_wall":(156,424), "back_peek":(129,450), "blowjob":(142,563), "stand4":(149,443), "stand5":(159,409), "kneeling1":(179,591), "walking_away":(141,438), "doggy":(297,316), "stand2":(103,453), "stand3":(156,432)})
        panties_list.append(cute_lace_panties)

        tiny_lace_panties = Clothing("Tiny Lace Panties", 1, True, True, "Tiny_Lace_Panties", False, True, 3, tucked = True, display_name = "panties",
            crop_offset_dict = {"cowgirl":(223,574), "missionary":(253,447), "kissing":(221,420), "sitting":(362,551), "against_wall":(154,427), "back_peek":(121,457), "blowjob":(142,563), "stand4":(144,447), "stand5":(159,414), "kneeling1":(176,591), "walking_away":(137,445), "doggy":(304,322), "stand2":(98,460), "stand3":(155,439)})
        panties_list.append(tiny_lace_panties)

        thin_panties = Clothing("Thin Panties", 1, True, True, "Thin_Panties", False, True, 1, tucked = True, whiteness_adjustment = -0.1, contrast_adjustment = 1.3, supported_patterns = {"Two Toned":"Pattern_1"},  display_name = "panties",
            crop_offset_dict = {"cowgirl":(222,563), "missionary":(251,439), "kissing":(221,414), "sitting":(352,541), "against_wall":(155,422), "back_peek":(113,457), "blowjob":(141,560), "stand4":(145,446), "stand5":(158,411), "kneeling1":(176,591), "walking_away":(137,437), "doggy":(229,324), "stand2":(103,450), "stand3":(155,429)})
        panties_list.append(thin_panties)

        thong = Clothing("Thong", 1, True, True, "Thong", False, True, 3, tucked = True, supported_patterns = {"Two Toned":"Pattern_1"},  display_name = "thong",
            crop_offset_dict = {"cowgirl":(226,559), "missionary":(260,439), "kissing":(223,412), "sitting":(353,541), "against_wall":(161,422), "back_peek":(140,449), "blowjob":(146,563), "stand4":(165,439), "stand5":(162,409), "kneeling1":(244,618), "walking_away":(149,434), "doggy":(301,318), "stand2":(113,445), "stand3":(162,425)})
        panties_list.append(thong)

        tiny_g_string = Clothing("G String", 1, True, True, "Tiny_G_String", False, True, 4, tucked = True,  display_name = "g-string",
            crop_offset_dict = {"cowgirl":(223,574), "missionary":(256,447), "kissing":(221,420), "sitting":(362,551), "against_wall":(155,427), "back_peek":(132,457), "blowjob":(142,563), "stand4":(149,447), "stand5":(160,414), "kneeling1":(179,592), "walking_away":(144,445), "doggy":(304,322), "stand2":(105,460), "stand3":(157,439)})
        panties_list.append(tiny_g_string)

        string_panties = Clothing("String Panties", 1, True, True, "String_Panties", False, True, 4, tucked = True, display_name = "g-string",
            crop_offset_dict = {"cowgirl":(223,581), "missionary":(250,450), "kissing":(220,445), "sitting":(352,546), "against_wall":(153,437), "back_peek":(118,481), "blowjob":(140,586), "stand4":(142,466), "stand5":(158,433), "kneeling1":(177,589), "walking_away":(136,463), "doggy":(226,350), "stand2":(100,473), "stand3":(153,457)})
        panties_list.append(string_panties)

        strappy_panties = Clothing("Strappy Panties", 1, True, True, "Strappy_Panties", False, True, 3, tucked = True, display_name = "panties",
            crop_offset_dict = {"cowgirl":(224,530), "missionary":(257,385), "kissing":(222,392), "sitting":(327,498), "against_wall":(159,406), "back_peek":(134,415), "blowjob":(144,550), "stand4":(159,412), "stand5":(161,392), "kneeling1":(187,562), "walking_away":(146,400), "doggy":(291,285), "stand2":(111,422), "stand3":(159,387)})
        panties_list.append(strappy_panties)

        crotchless_panties = Clothing("Crotchless Panties", 1, False, False, "Crotchless_Panties", False, True, 2, tucked = True, whiteness_adjustment = 0.15, contrast_adjustment = 1.1, display_name = "panties",
            crop_offset_dict = {"cowgirl":(224,548), "missionary":(271,431), "kissing":(229,409), "sitting":(354,534), "against_wall":(167,419), "back_peek":(149,438), "blowjob":(155,566), "stand4":(180,432), "stand5":(165,406), "kneeling1":(242,628), "walking_away":(156,420), "doggy":(305,313), "stand2":(118,441), "stand3":(169,412)})
        panties_list.append(crotchless_panties)


        ##Bras
        bra_list = []

        bra = Clothing("Bra", 1, True, True, "Bra", True, True, 0, supported_patterns = {"Lacey":"Pattern_1"}, display_name = "bra",
            crop_offset_dict = {"cowgirl":(142,277), "missionary":(249,202), "kissing":(153,181), "sitting":(281,286), "against_wall":(142,168), "back_peek":(150,212), "blowjob":(112,318), "stand4":(169,204), "stand5":(109,187), "kneeling1":(210,324), "walking_away":(128,196), "doggy":(256,167), "stand2":(105,213), "stand3":(127,183)})
        bra_list.append(bra)

        bralette = Clothing("Bralette", 1, True, True, "Bralette", True, True, 0, display_name = "bra",
            crop_offset_dict = {"cowgirl":(145,279), "missionary":(250,202), "kissing":(154,181), "sitting":(283,286), "against_wall":(147,168), "back_peek":(151,212), "blowjob":(113,319), "stand4":(170,204), "stand5":(110,187), "kneeling1":(207,325), "walking_away":(128,196), "doggy":(255,168), "stand2":(107,213), "stand3":(128,183)})
        bra_list.append(bralette)

        sports_bra = Clothing("Sports Bra", 1, True, True, "Sports_Bra", True, True, 0, whiteness_adjustment = 0.35, contrast_adjustment = 1.3, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "bra",
            crop_offset_dict = {"cowgirl":(147,275), "missionary":(250,201), "kissing":(154,179), "sitting":(283,280), "against_wall":(142,167), "back_peek":(156,204), "blowjob":(113,325), "stand4":(169,197), "stand5":(110,183), "kneeling1":(238,318), "walking_away":(128,187), "doggy":(257,167), "stand2":(106,209), "stand3":(128,174)})
        bra_list.append(sports_bra)

        strapless_bra = Clothing("Strapless Bra", 1, True, True, "Strapless_Bra", True, True, 1, whiteness_adjustment = 0.2, supported_patterns = {"Two Tone":"Pattern_1"}, display_name = "bra",
            crop_offset_dict = {"cowgirl":(205,425), "missionary":(249,233), "kissing":(153,279), "sitting":(281,378), "against_wall":(143,264), "back_peek":(157,293), "blowjob":(112,452), "stand4":(169,300), "stand5":(108,267), "kneeling1":(249,460), "walking_away":(128,298), "doggy":(257,204), "stand2":(105,307), "stand3":(127,272)})
        bra_list.append(strapless_bra)

        lace_bra = Clothing("Lace Bra", 1, True, True, "Lace_Bra", True, True, 2, whiteness_adjustment = 0.2, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "bra",
            crop_offset_dict = {"cowgirl":(199,277), "missionary":(250,204), "kissing":(155,182), "sitting":(283,286), "against_wall":(144,169), "back_peek":(151,211), "blowjob":(114,319), "stand4":(169,204), "stand5":(111,188), "kneeling1":(217,324), "walking_away":(128,195), "doggy":(258,167), "stand2":(107,213), "stand3":(128,182)})
        bra_list.append(lace_bra)

        thin_bra = Clothing("Thin Bra", 1, True, True, "Thin_Bra", True, True, 2, whiteness_adjustment = 0.0, contrast_adjustment = 1.3, display_name = "bra",
            crop_offset_dict = {"cowgirl":(152,279), "missionary":(250,203), "kissing":(152,181), "sitting":(280,287), "against_wall":(143,168), "back_peek":(151,212), "blowjob":(113,318), "stand4":(169,205), "stand5":(107,188), "kneeling1":(212,325), "walking_away":(128,196), "doggy":(258,168), "stand2":(107,214), "stand3":(127,183)})
        bra_list.append(thin_bra)

        strappy_bra = Clothing("Strappy Bra", 1, True, True, "Strappy_Bra", True, True, 3, display_name = "bra",
            crop_offset_dict = {"cowgirl":(152,276), "missionary":(250,201), "kissing":(152,179), "sitting":(280,283), "against_wall":(147,169), "back_peek":(151,208), "blowjob":(112,324), "stand4":(170,201), "stand5":(107,185), "kneeling1":(232,320), "walking_away":(128,191), "doggy":(258,166), "stand2":(106,210), "stand3":(127,178)})
        bra_list.append(strappy_bra)

        quarter_cup_bustier = Clothing("Quarter Cup Bustier", 1, False, False, "Quarter_Cup_Bra", True, True, 8, whiteness_adjustment = 0.3, contrast_adjustment = 0.9, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "bustier",
            crop_offset_dict = {"cowgirl":(211,428), "missionary":(250,269), "kissing":(156,296), "sitting":(284,400), "against_wall":(154,279), "back_peek":(169,315), "blowjob":(115,461), "stand4":(170,313), "stand5":(112,295), "kneeling1":(251,467), "walking_away":(128,309), "doggy":(260,229), "stand2":(107,325), "stand3":(129,285)})
        bra_list.append(quarter_cup_bustier)

        corset = Clothing("Corset", 1, True, True, "Corset", True, True, 5, whiteness_adjustment = 0.0, contrast_adjustment = 1.4, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "corset",
            crop_offset_dict = {"cowgirl":(150,422), "missionary":(249,229), "kissing":(154,270), "sitting":(282,370), "against_wall":(144,256), "back_peek":(157,284), "blowjob":(113,448), "stand4":(169,292), "stand5":(109,259), "kneeling1":(239,454), "walking_away":(128,296), "doggy":(257,199), "stand2":(106,300), "stand3":(128,265)})
        bra_list.append(corset)

        teddy = Clothing("Teddy", 1, True, True, "Teddy", True, True, 4, whiteness_adjustment = 0.0, contrast_adjustment = 1.0, display_name = "teddy",
            crop_offset_dict = {"cowgirl":(143,273), "missionary":(233,201), "kissing":(154,179), "sitting":(283,281), "against_wall":(138,167), "back_peek":(105,206), "blowjob":(113,318), "stand4":(126,198), "stand5":(110,183), "kneeling1":(143,319), "walking_away":(127,189), "doggy":(182,163), "stand2":(88,208), "stand3":(127,174)})
        bra_list.append(teddy)

        cincher = Clothing("Cincher", 1, False, False, "Cincher", True, False, 5, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "corset",
            crop_offset_dict = {"cowgirl":(224,480), "missionary":(272,309), "kissing":(211,344), "sitting":(340,449), "against_wall":(168,334), "back_peek":(150,356), "blowjob":(157,511), "stand4":(183,360), "stand5":(165,338), "kneeling1":(239,539), "walking_away":(157,342), "doggy":(291,239), "stand2":(122,365), "stand3":(164,329)})
        bra_list.append(cincher)

        heart_pasties = Clothing("Heart Pasties", 1, False, False, "Heart_Pasties", True, True, 8, display_name = "pasties",
            crop_offset_dict = {"cowgirl":(205,439), "missionary":(257,230), "kissing":(155,281), "sitting":(283,382), "against_wall":(153,268), "back_peek":(309,293), "blowjob":(114,467), "stand4":(175,302), "stand5":(111,271), "kneeling1":(282,475), "walking_away":(249,214), "doggy":(259,198), "stand2":(108,309), "stand3":(139,273)})
        bra_list.append(heart_pasties)


        ##Pants
        pants_list = []

        leggings = Clothing("Leggings", 2, True, True, "Leggings", False, False, 1, whiteness_adjustment = 0.2, contrast_adjustment = 1.8, supported_patterns = {"Cougar Print":"Pattern_1"}, display_name = "leggings",
            constrain_regions = [upper_leg_region, lower_leg_region, pelvis_region],
            crop_offset_dict = {"cowgirl":(49,539), "missionary":(92,375), "kissing":(219,394), "sitting":(141,507), "against_wall":(114,411), "back_peek":(106,425), "blowjob":(113,558), "stand4":(129,421), "stand5":(138,394), "kneeling1":(111,560), "walking_away":(127,410), "doggy":(96,291), "stand2":(87,430), "stand3":(83,398)})
        pants_list.append(leggings)

        capris = Clothing("Capris", 2, True, True, "Capris", False, False, 1, whiteness_adjustment = 0.3, contrast_adjustment = 1.1, display_name = "pants",
            constrain_regions = [upper_leg_region, lower_leg_region, pelvis_region],
            crop_offset_dict = {"cowgirl":(53,563), "missionary":(99,429), "kissing":(217,415), "sitting":(166,527), "against_wall":(116,426), "back_peek":(106,464), "blowjob":(116,559), "stand4":(128,449), "stand5":(141,412), "kneeling1":(114,583), "walking_away":(127,447), "doggy":(113,328), "stand2":(87,452), "stand3":(96,438)})
        pants_list.append(capris)

        booty_shorts = Clothing("Booty Shorts", 2, True, True, "Booty_Shorts", False, False, 6, whiteness_adjustment = 0.25, contrast_adjustment = 1.1, supported_patterns = {"Text":"Pattern_1"}, display_name = "shorts",
            constrain_regions = [pelvis_region],
            crop_offset_dict = {"cowgirl":(223,546), "missionary":(246,437), "kissing":(220,401), "sitting":(353,519), "against_wall":(151,416), "back_peek":(111,434), "blowjob":(138,562), "stand4":(135,427), "stand5":(157,400), "kneeling":(166,563), "walking_away":(131,423), "doggy":(210,300), "stand2":(96,440), "stand3":(150,416)})
        pants_list.append(booty_shorts)

        jean_hotpants = Clothing("Jean Hotpants", 2, True, True, "Jean_Hotpants", False, False, 4, whiteness_adjustment = 0.1, display_name = "shorts",
            constrain_regions = [upper_leg_region, pelvis_region],
            crop_offset_dict = {"cowgirl":(166,546), "missionary":(225,399), "kissing":(219,401), "sitting":(334,517), "against_wall":(143,417), "back_peek":(108,429), "blowjob":(134,561), "stand4":(129,427), "stand5":(150,398), "kneeling1":(153,562), "walking_away":(127,419), "doggy":(198,297), "stand2":(90,439), "stand3":(142,410)})
        pants_list.append(jean_hotpants)

        daisy_dukes = Clothing("Daisy Dukes", 2, True, True, "Daisy_Dukes", False, False, 6, display_name = "shorts",
            constrain_regions = [pelvis_region],
            crop_offset_dict = {"cowgirl":(181,548), "missionary":(246,427), "kissing":(219,405), "sitting":(353,528), "against_wall":(148,418), "back_peek":(110,439), "blowjob":(137,562), "stand4":(129,431), "stand5":(156,402), "kneeling1":(161,566), "walking_away":(127,426), "doggy":(205,306), "stand2":(95,438), "stand3":(145,416)})
        pants_list.append(daisy_dukes)

        jeans = Clothing("Jeans", 2, True, True, "Jeans", False, False, 0, display_name = "jeans",
            constrain_regions = [upper_leg_region, lower_leg_region, pelvis_region],
            crop_offset_dict = {"cowgirl":(56,545), "missionary":(100,398), "kissing":(219,400), "sitting":(146,516), "against_wall":(109,415), "back_peek":(108,429), "blowjob":(116,561), "stand4":(128,425), "stand5":(136,398), "kneeling1":(115,561), "walking_away":(127,419), "doggy":(90,297), "stand2":(88,437), "stand3":(82,409)})
        pants_list.append(jeans)

        suitpants = Clothing("Suit Pants", 2, True, True, "Suit_Pants", False, False, 0, display_name = "pants",
            constrain_regions = [upper_leg_region, lower_leg_region, pelvis_region],
            crop_offset_dict = {"cowgirl":(52,543), "missionary":(96,400), "kissing":(216,399), "sitting":(125,518), "against_wall":(109,413), "back_peek":(109,432), "blowjob":(117,560), "stand4":(129,425), "stand5":(131,397), "kneeling1":(107,563), "walking_away":(127,417), "doggy":(82,301), "stand2":(89,434), "stand3":(72,404)})
        pants_list.append(suitpants)


        ##Skirts
        skirts_list = []

        skirt = Clothing("Skirt", 2, True, False, "Skirt", False, False, 1, display_name = "skirt",
            constrain_regions = [skirt_region],
            crop_offset_dict = {"cowgirl":(87,513), "missionary":(141,343), "kissing":(206,382), "sitting":(244,487), "against_wall":(110,392), "back_peek":(108,404), "blowjob":(100,539), "stand4":(125,402), "stand5":(121,386), "kneeling1":(108,561), "walking_away":(111,388), "doggy":(151,276), "stand2":(68,411), "stand3":(98,374)})
        skirts_list.append(skirt)

        long_skirt = Clothing("Long Skirt", 2, True, True, "Long_Skirt", False, False, 0, whiteness_adjustment = 0.0, contrast_adjustment = 1.0, display_name = "skirt",
            constrain_regions = [skirt_region, lower_leg_region],
            crop_offset_dict = {"cowgirl":(53,519), "missionary":(82,346), "kissing":(216,389), "sitting":(118,494), "against_wall":(91,399), "back_peek":(107,411), "blowjob":(94,542), "stand4":(106,409), "stand5":(109,389), "kneeling1":(111,559), "walking_away":(122,392), "doggy":(59,286), "stand2":(46,416), "stand3":(59,378)})
        skirts_list.append(long_skirt)

        pencil_skirt = Clothing("Pencil Skirt", 2, True, False, "Pencil_Skirt", False, False, 0, whiteness_adjustment = 0.2, display_name = "skirt",
            constrain_regions = [skirt_region],
            crop_offset_dict = {"cowgirl":(82,499), "missionary":(139,329), "kissing":(216,370), "sitting":(233,475), "against_wall":(137,378), "back_peek":(107,392), "blowjob":(120,524), "stand4":(125,389), "stand5":(146,376), "kneeling1":(123,552), "walking_away":(127,376), "doggy":(162,267), "stand2":(83,396), "stand3":(124,361)})
        skirts_list.append(pencil_skirt)

        belted_skirt = Clothing("Belted Skirt", 2, True, False, "Belted_Skirt", False, False, 1, contrast_adjustment = 1.15, supported_patterns = {"Belt":"Pattern_1"}, display_name = "skirt",
            half_off_regions = [pelvis_region, upper_leg_region, lower_leg_region], half_off_ignore_regions = [stomach_region],
            constrain_regions = [skirt_region],
            crop_offset_dict = {"cowgirl":(118,526), "missionary":(167,348), "kissing":(214,390), "sitting":(279,504), "against_wall":(121,402), "back_peek":(108,412), "blowjob":(105,547), "stand4":(114,410), "stand5":(132,391), "kneeling1":(126,560), "walking_away":(123,394), "doggy":(164,294), "stand2":(66,416), "stand3":(113,380)})
        skirts_list.append(belted_skirt)

        lace_skirt = Clothing("Lace Skirt", 2, True, False, "Lace_Skirt", False, False, 1, whiteness_adjustment = 0.15, display_name = "skirt",
            constrain_regions = [skirt_region],
            crop_offset_dict = {"cowgirl":(100,513), "missionary":(150,343), "kissing":(206,382), "sitting":(259,487), "against_wall":(111,392), "back_peek":(108,404), "blowjob":(100,539), "stand4":(125,402), "stand5":(122,386), "kneeling1":(109,561), "walking_away":(111,388), "doggy":(153,276), "stand2":(68,411), "stand3":(100,374)})
        skirts_list.append(lace_skirt)

        mini_skirt = Clothing("Mini Skirt", 2, True, False, "Mini_Skirt", False, False, 5, whiteness_adjustment = 0.4, display_name = "skirt",
            constrain_regions = [skirt_region],
            crop_offset_dict = {"cowgirl":(137,539), "missionary":(185,362), "kissing":(210,399), "sitting":(302,514), "against_wall":(120,412), "back_peek":(101,430), "blowjob":(118,559), "stand4":(118,423), "stand5":(135,397), "kneeling1":(125,561), "walking_away":(126,410), "doggy":(165,295), "stand2":(72,429), "stand3":(137,399)})
        skirts_list.append(mini_skirt)

        micro_skirt = Clothing("Micro Skirt", 2, False, False, "Micro_Skirt", False, False, 8, whiteness_adjustment = 0.2, supported_patterns = {"Two Tone":"Pattern_1"}, display_name = "skirt",
            constrain_regions = [skirt_region],
            crop_offset_dict = {"cowgirl":(163,563), "missionary":(216,441), "kissing":(210,414), "sitting":(330,539), "against_wall":(133,424), "back_peek":(102,458), "blowjob":(135,559), "stand4":(115,447), "stand5":(143,410), "kneeling1":(144,585), "walking_away":(127,449), "doggy":(186,323), "stand2":(81,456), "stand3":(138,439)})
        skirts_list.append(micro_skirt)




        ##Dresses
        #TODO: Check if the extension or the main piece should have the whiteness adjusments etc.
        dress_list = []

        sweater_dress_bottom = Clothing("sweater dress", 2, True, False, "Sweater_Dress", False, False, 0, is_extension = True)
        sweater_dress = Clothing("sweater dress", 2, True, True, "Sweater_Dress", True, False, 0, has_extension = sweater_dress_bottom, whiteness_adjustment = 0.2, contrast_adjustment = 1.2, supported_patterns = {"Two Toned":"Pattern_1", "Hearts":"Pattern_2"}, display_name = "dress",
            constrain_regions = [torso_region, stomach_region, upper_arm_region, lower_arm_region, skirt_region],
            crop_offset_dict = {"cowgirl":(127,273), "missionary":(161,199), "kissing":(88,177), "sitting":(238,276), "against_wall":(47,161), "back_peek":(104,198), "blowjob":(98,317), "stand4":(94,194), "stand5":(108,182), "kneeling1":(133,317), "walking_away":(99,180), "doggy":(137,165), "stand2":(51,206), "stand3":(94,171)})
        dress_list.append(sweater_dress)

        two_part_dress_bottom = Clothing("two part dress", 2, True, False, "Two_Piece_Dress", False, False, 0, is_extension = True)
        two_part_dress = Clothing("two part dress", 2, True, True, "Two_Piece_Dress", True, False, 6, has_extension = two_part_dress_bottom, display_name = "dress",
            constrain_regions = [torso_region, stomach_region, skirt_region],
            crop_offset_dict = {"cowgirl":(134,283), "missionary":(189,195), "kissing":(152,173), "sitting":(280,273), "against_wall":(136,163), "back_peek":(106,198), "blowjob":(111,337), "stand4":(127,190), "stand5":(108,178), "kneeling1":(138,318), "walking_away":(127,178), "doggy":(176,173), "stand2":(88,208), "stand3":(127,164)})
        dress_list.append(two_part_dress)

        thin_dress_bottom = Clothing("thin dress", 2, True, False, "Thin_Dress", False, False, 0, is_extension = True)
        thin_dress = Clothing("thin dress", 2, True, True, "Thin_Dress", True, False, 4, has_extension = thin_dress_bottom, whiteness_adjustment = 0.3, contrast_adjustment = 1.15, display_name = "dress",
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region, skirt_region],
            crop_offset_dict = {"cowgirl":(150,273), "missionary":(160,201), "kissing":(88,177), "sitting":(243,283), "against_wall":(48,167), "back_peek":(109,207), "blowjob":(97,318), "stand4":(96,200), "stand5":(110,185), "kneeling1":(149,320), "walking_away":(101,191), "doggy":(140,164), "stand2":(57,210), "stand3":(98,178)})
        dress_list.append(thin_dress)

        summer_dress_bottom = Clothing("summer dress", 2, True, False, "Summer_Dress", False, False, 0, is_extension = True)
        summer_dress = Clothing("summer dress", 2, True, False, "Summer_Dress", True, True, 0, has_extension = summer_dress_bottom, whiteness_adjustment = 0.1, display_name = "dress",
            constrain_regions = [torso_region, stomach_region, skirt_region],
            crop_offset_dict = {"cowgirl":(136,276), "missionary":(202,201), "kissing":(155,179), "sitting":(283,282), "against_wall":(130,168), "back_peek":(107,206), "blowjob":(113,319), "stand4":(128,199), "stand5":(111,184), "kneeling1":(150,319), "walking_away":(126,189), "doggy":(163,166), "stand2":(76,209), "stand3":(95,175)})
        dress_list.append(summer_dress)

        virgin_killer_bottom = Clothing("virgin killer", 2, True, False, "Virgin_Killer", False, False, 0, is_extension = True)
        virgin_killer = Clothing("Virgin Killer", 2, True, True, "Virgin_Killer", True, False, 5, has_extension = virgin_killer_bottom, display_name = "dress",
            constrain_regions = [torso_region, stomach_region, skirt_region],
            crop_offset_dict = {"cowgirl":(140,268), "missionary":(192,165), "kissing":(158,142), "sitting":(285,243), "against_wall":(129,128), "back_peek":(103,160), "blowjob":(112,326), "stand4":(126,162), "stand5":(115,151), "kneeling1":(136,300), "walking_away":(126,142), "doggy":(176,160), "stand2":(80,160), "stand3":(133,126)})
        dress_list.append(virgin_killer)

        evening_dress_bottom = Clothing("evening dress", 2, True, False, "Evening_Dress", False, False, 0, is_extension = True)
        evening_dress = Clothing("evening dress", 2, True, True, "Evening_Dress", True, False, 2, has_extension = evening_dress_bottom, whiteness_adjustment = 0.4, display_name = "dress",
            constrain_regions = [torso_region, stomach_region, skirt_region],
            crop_offset_dict = {"cowgirl":(116,276), "missionary":(172,201), "kissing":(153,177), "sitting":(279,285), "against_wall":(136,167), "back_peek":(107,210), "blowjob":(113,318), "stand4":(128,203), "stand5":(109,187), "kneeling1":(134,323), "walking_away":(127,194), "doggy":(171,166), "stand2":(88,212), "stand3":(126,181)})
        dress_list.append(evening_dress)

        leotard_bottom = Clothing("Leotard", 1, True, True, "Leotard", False, True, 0, is_extension = True)
        leotard = Clothing("Leotard", 2, True, True, "Leotard", True, False, 5, has_extension = leotard_bottom, tucked = True, display_name = "leotard",
            constrain_regions = [torso_region, stomach_region, pelvis_region, upper_arm_region, lower_arm_region],
            crop_offset_dict = {"cowgirl":(140,274), "missionary":(162,186), "kissing":(88,175), "sitting":(239,276), "against_wall":(47,150), "back_peek":(109,190), "blowjob":(98,318), "stand4":(97,183), "stand5":(110,180), "kneeling1":(179,316), "walking_away":(100,169), "doggy":(138,165), "stand2":(52,209), "stand3":(98,152)})
        dress_list.append(leotard)

        nightgown_dress_bottom = Clothing("Nightgown", 2, False, False, "Nightgown", False, True, 0, is_extension = True)
        nightgown_dress = Clothing("Nightgown", 2, False, True, "Nightgown", True, True, 3, has_extension = nightgown_dress_bottom, whiteness_adjustment = 0.1, contrast_adjustment = 1.1, display_name = "nightgown",
            constrain_regions = [torso_region, stomach_region, skirt_region],
            crop_offset_dict = {"cowgirl":(61,278), "missionary":(109,200), "kissing":(155,180), "sitting":(220,286), "against_wall":(111,167), "back_peek":(107,211), "blowjob":(97,318), "stand4":(123,205), "stand5":(111,187), "kneeling1":(104,325), "walking_away":(127,196), "doggy":(142,167), "stand2":(71,212), "stand3":(100,183)})
        dress_list.append(nightgown_dress)

        bath_robe_bottom = Clothing("Bathrobe", 2, False, False, "Bath_Robe", False, False, 0, is_extension = True)
        bath_robe = Clothing("Bathrobe", 2, False, True, "Bath_Robe", True, True, 1, has_extension = bath_robe_bottom, supported_patterns = {"Flowers":"Pattern_1"}, display_name = "robe",
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region, skirt_region],
            crop_offset_dict = {"cowgirl":(130,274), "missionary":(158,183), "kissing":(89,158), "sitting":(252,255), "against_wall":(49,141), "back_peek":(101,171), "blowjob":(98,318), "stand4":(98,173), "stand5":(104,161), "kneeling1":(136,311), "walking_away":(107,155), "doggy":(145,165), "stand2":(65,177), "stand3":(99,140)})
        dress_list.append(bath_robe)

        lacy_one_piece_underwear_bottom = Clothing("lacy one piece", 1, True, True, "Lacy_One_Piece_Underwear", False, True, 0, is_extension = True)
        lacy_one_piece_underwear = Clothing("lacy one piece", 1, True, True, "Lacy_One_Piece_Underwear", True, True, 4, tucked = True, has_extension = lacy_one_piece_underwear_bottom, whiteness_adjustment = 0.2, display_name = "underwear",
            crop_offset_dict = {"cowgirl":(146,276), "missionary":(250,199), "kissing":(155,177), "sitting":(283,280), "against_wall":(145,167), "back_peek":(151,204), "blowjob":(113,323), "stand4":(170,197), "stand5":(111,182), "kneeling1":(221,319), "walking_away":(128,187), "doggy":(257,166), "stand2":(107,209), "stand3":(95,173)})
        dress_list.append(lacy_one_piece_underwear)

        lingerie_one_piece_bottom = Clothing("lingerie one piece", 1, True, True, "Lingerie_One_Piece", False, True, 0, is_extension = True)
        lingerie_one_piece = Clothing("lingerie one piece", 1, True, True, "Lingerie_One_Piece", True, True, 8, tucked = True, has_extension = lingerie_one_piece_bottom, supported_patterns = {"Flowers":"Pattern_1"}, display_name = "underwear",
            constrain_regions = [torso_region, stomach_region, pelvis_region],
            crop_offset_dict = {"cowgirl":(148,275), "missionary":(250,202), "kissing":(154,181), "sitting":(283,284), "against_wall":(144,168), "back_peek":(126,207), "blowjob":(113,318), "stand4":(153,202), "stand5":(111,186), "kneeling1":(186,321), "walking_away":(129,192), "doggy":(258,165), "stand2":(106,211), "stand3":(101,179)})
        dress_list.append(lingerie_one_piece)

        bodysuit_underwear_bottom = Clothing("bodysuit underwear", 1, True, True, "Bodysuit_Underwear", False, True, 0, is_extension = True)
        bodysuit_underwear = Clothing("bodysuit underwear", 1, True, True, "Bodysuit_Underwear", True, True, 6, tucked = True, has_extension = bodysuit_underwear_bottom, whiteness_adjustment = 0.2, display_name = "bodysuit",
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region, pelvis_region],
            crop_offset_dict = {"cowgirl":(145,275), "missionary":(162,199), "kissing":(91,176), "sitting":(236,281), "against_wall":(51,159), "back_peek":(113,206), "blowjob":(99,320), "stand4":(99,199), "stand5":(109,185), "kneeling1":(181,319), "walking_away":(99,188), "doggy":(134,166), "stand2":(50,203), "stand3":(99,176)})
        dress_list.append(bodysuit_underwear)

        towel_bottom = Clothing("Towel", 1, True, True, "Towel", False, False, 0, is_extension = True)
        towel = Clothing("Towel", 1, True, True, "Towel", True, False, 1, has_extension = towel_bottom, display_name = "towel",
            constrain_regions = [torso_region, stomach_region, skirt_region],
            crop_offset_dict = {"cowgirl":(122,414), "missionary":(177,223), "kissing":(152,263), "sitting":(280,365), "against_wall":(135,249), "back_peek":(106,277), "blowjob":(110,428), "stand4":(127,285), "stand5":(109,255), "kneeling1":(134,430), "walking_away":(125,282), "doggy":(169,185), "stand2":(86,295), "stand3":(124,258)})
        # dress_list.append(towel) #TEMPORARY FOR TESTING

        apron_bottom = Clothing("Apron", 3, False, False, "Apron", False, False, 0, is_extension = True)
        apron = Clothing("Apron", 3, False, True, "Apron", True, False, 0, has_extension = apron_bottom, supported_patterns = {"Plaid":"Pattern_1"}, whiteness_adjustment = -0.1, display_name = "apron",
            constrain_regions = [stomach_region],
            crop_offset_dict = {"cowgirl":(194,284), "missionary":(246,190), "kissing":(154,167), "sitting":(266,266), "against_wall":(146,155), "back_peek":(74,186), "blowjob":(118,335), "stand4":(131,185), "stand5":(108,175), "kneeling1":(183,316), "walking_away":(141,167), "doggy":(241,171), "stand2":(70,189), "stand3":(157,155)})
        dress_list.append(apron)

        ##Shirts
        shirts_list = []

        tshirt = Clothing("Tshirt", 2, True, True, "Tshirt", True, False, 1, whiteness_adjustment = 0.35, supported_patterns = {"Striped":"Pattern_2","Text":"Pattern_3"}, display_name = "shirt",
            half_off_regions = [breast_region, stomach_region, pelvis_region, upper_leg_region], half_off_ignore_regions = upper_arm_region,
            constrain_regions = [torso_region, upper_arm_region, stomach_region],
            crop_offset_dict = {"cowgirl":(145,272), "missionary":(232,197), "kissing":(153,175), "sitting":(281,277), "against_wall":(103,165), "back_peek":(149,200), "blowjob":(111,317), "stand4":(146,194), "stand5":(109,180), "kneeling1":(183,314), "walking_away":(127,184), "doggy":(198,164), "stand2":(105,207), "stand3":(112,171)})
        shirts_list.append(tshirt)

        lace_sweater = Clothing("Lace Sweater", 2, True, True, "Lace_Sweater", True, False, 2, opacity_adjustment = 1.08, whiteness_adjustment = 0.18, display_name = "sweater",
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region],
            crop_offset_dict = {"cowgirl":(142,273), "missionary":(159,193), "kissing":(87,170), "sitting":(238,272), "against_wall":(47,158), "back_peek":(149,196), "blowjob":(97,316), "stand4":(96,189), "stand5":(107,177), "kneeling1":(174,317), "walking_away":(98,177), "doggy":(137,165), "stand2":(50,207), "stand3":(98,164)})
        shirts_list.append(lace_sweater)

        long_sweater = Clothing("Long Sweater", 2, True, True, "Long_Sweater", True, False, 0, whiteness_adjustment = 0.2, supported_patterns = {"Striped":"Pattern_1"}, display_name = "sweater",
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region],
            crop_offset_dict = {"cowgirl":(144,275), "missionary":(159,200), "kissing":(89,177), "sitting":(237,282), "against_wall":(49,161), "back_peek":(107,204), "blowjob":(99,319), "stand4":(98,199), "stand5":(110,184), "kneeling1":(160,317), "walking_away":(98,188), "doggy":(136,166), "stand2":(50,209), "stand3":(99,176)})
        shirts_list.append(long_sweater)

        sleeveless_top = Clothing ("Sleeveless Top", 2, True, True, "Sleveless_Top", True, False, 0, tucked = True, display_name = "shirt",
            constrain_regions = [torso_region, stomach_region],
            crop_offset_dict = {"cowgirl":(143,274), "missionary":(248,200), "kissing":(151,178), "sitting":(280,279), "against_wall":(144,166), "back_peek":(133,202), "blowjob":(110,318), "stand4":(158,196), "stand5":(108,183), "kneeling1":(186,317), "walking_away":(126,184), "doggy":(247,165), "stand2":(104,209), "stand3":(96,174)})
        shirts_list.append(sleeveless_top)

        long_tshirt = Clothing("Long Tshirt", 2, True, True, "Long_Tshirt", True, False, 0, whiteness_adjustment = 0.25, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "shirt",
            constrain_regions = [torso_region, stomach_region],
            crop_offset_dict = {"cowgirl":(145,273), "missionary":(218,201), "kissing":(153,177), "sitting":(281,281), "against_wall":(114,167), "back_peek":(102,205), "blowjob":(111,318), "stand4":(122,199), "stand5":(109,184), "kneeling1":(144,319), "walking_away":(127,189), "doggy":(191,166), "stand2":(84,210), "stand3":(99,176)})
        shirts_list.append(long_tshirt)

        sweater = Clothing("Sweater", 2, True, True, "Sweater", True, False, 1, whiteness_adjustment = 0.1, display_name = "sweater",
            constrain_regions = [torso_region, upper_arm_region, stomach_region, upper_arm_region, lower_arm_region],
            crop_offset_dict = {"cowgirl":(143,274), "missionary":(159,193), "kissing":(87,170), "sitting":(238,273), "against_wall":(47,159), "back_peek":(149,196), "blowjob":(97,317), "stand4":(97,190), "stand5":(107,178), "kneeling1":(175,318), "walking_away":(99,177), "doggy":(137,165), "stand2":(51,207), "stand3":(98,164)})
        shirts_list.append(sweater)

        belted_top = Clothing("Belted Top", 2, True, True, "Belted_Top", True, False, 5, contrast_adjustment = 1.1, display_name = "vest",
            constrain_regions = [torso_region],
            crop_offset_dict = {"cowgirl":(147,265), "missionary":(248,186), "kissing":(153,163), "sitting":(280,261), "against_wall":(135,150), "back_peek":(150,181), "blowjob":(112,315), "stand4":(161,177), "stand5":(108,167), "kneeling1":(179,302), "walking_away":(127,163), "doggy":(211,157), "stand2":(105,185), "stand3":(113,154)})
        shirts_list.append(belted_top)

        lace_crop_top = Clothing("Lace Crop Top", 2, True, True, "Lace_Crop_Top", True, False, 2, whiteness_adjustment = 0.1, contrast_adjustment = 1.1, display_name = "top",
            constrain_regions = [torso_region, upper_arm_region],
            crop_offset_dict = {"cowgirl":(143,324), "missionary":(189,211), "kissing":(124,184), "sitting":(279,313), "against_wall":(66,184), "back_peek":(138,238), "blowjob":(108,347), "stand4":(120,231), "stand5":(106,211), "kneeling1":(172,370), "walking_away":(120,235), "doggy":(170,165), "stand2":(105,222), "stand3":(95,214)})
        shirts_list.append(lace_crop_top)

        tanktop = Clothing("Tanktop", 2, True, True, "Tanktop", True, False, 3, display_name = "top",
            constrain_regions = [torso_region, stomach_region],
            crop_offset_dict = {"cowgirl":(148,275), "missionary":(249,202), "kissing":(151,180), "sitting":(279,285), "against_wall":(145,167), "back_peek":(142,210), "blowjob":(112,317), "stand4":(167,203), "stand5":(107,186), "kneeling1":(206,323), "walking_away":(128,194), "doggy":(256,167), "stand2":(106,212), "stand3":(127,182)})
        shirts_list.append(tanktop)

        camisole = Clothing("Camisole", 2, True, True, "Camisole", True, False, 1, whiteness_adjustment = 0.2, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "camisole",
            constrain_regions = [torso_region, stomach_region, skirt_region],
            crop_offset_dict = {"cowgirl":(141,257), "missionary":(192,185), "kissing":(150,162), "sitting":(280,274), "against_wall":(104,153), "back_peek":(88,200), "blowjob":(104,298), "stand4":(93,197), "stand5":(109,173), "kneeling1":(127,316), "walking_away":(101,191), "doggy":(170,148), "stand2":(38,200), "stand3":(105,174)})
        shirts_list.append(camisole)

        long_sleeve_blouse = Clothing("Buttoned Blouse", 2, True, True, "Long_Sleeve_Blouse", True, False, 0, whiteness_adjustment = 0.2, display_name = "blouse",
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region],
            crop_offset_dict = {"cowgirl":(148,273), "missionary":(158,192), "kissing":(88,168), "sitting":(238,269), "against_wall":(48,158), "back_peek":(107,190), "blowjob":(98,314), "stand4":(96,186), "stand5":(111,174), "kneeling1":(156,313), "walking_away":(100,172), "doggy":(135,164), "stand2":(51,204), "stand3":(99,160)})
        shirts_list.append(long_sleeve_blouse)

        short_sleeve_blouse = Clothing("Short Sleeve Blouse", 2, True, True, "Short_Sleeve_Blouse", True, False, 0, whiteness_adjustment = 0.3, display_name = "blouse",
            constrain_regions = [torso_region, upper_arm_region, stomach_region],
            crop_offset_dict = {"cowgirl":(153,274), "missionary":(224,187), "kissing":(154,162), "sitting":(282,264), "against_wall":(96,151), "back_peek":(108,185), "blowjob":(113,317), "stand4":(129,181), "stand5":(110,167), "kneeling1":(160,309), "walking_away":(124,167), "doggy":(193,165), "stand2":(91,186), "stand3":(104,154)})
        shirts_list.append(short_sleeve_blouse)

        wrapped_blouse = Clothing("Wrapped Blouse", 2, True, True, "Wrapped_Blouse", True, False, 0, whiteness_adjustment = 0.25, contrast_adjustment = 1.05, display_name = "blouse",
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region],
            crop_offset_dict = {"cowgirl":(142,275), "missionary":(160,201), "kissing":(90,177), "sitting":(236,283), "against_wall":(50,155), "back_peek":(108,208), "blowjob":(99,319), "stand4":(99,200), "stand5":(111,185), "kneeling1":(154,320), "walking_away":(99,190), "doggy":(132,166), "stand2":(49,199), "stand3":(99,177)})
        shirts_list.append(wrapped_blouse)

        tube_top = Clothing("Tube Top", 2, True, True, "Tube_Top", True, False, 4, supported_patterns = {"Cougar Print":"Pattern_1","Text":"Pattern_2"}, display_name = "top",
            constrain_regions = [breast_region, stomach_region],
            crop_offset_dict = {"cowgirl":(144,394), "missionary":(250,228), "kissing":(152,278), "sitting":(281,381), "against_wall":(143,264), "back_peek":(164,290), "blowjob":(113,454), "stand4":(170,298), "stand5":(109,268), "kneeling1":(241,453), "walking_away":(126,299), "doggy":(257,221), "stand2":(107,307), "stand3":(129,270)})
        shirts_list.append(tube_top)

        tie_sweater = Clothing("Tied Sweater", 2, True, True, "Tie_Sweater", True, False, 0, whiteness_adjustment = 0.3, contrast_adjustment = 1.1, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "sweater",
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region],
            crop_offset_dict = {"cowgirl":(137,276), "missionary":(152,200), "kissing":(71,176), "sitting":(254,280), "against_wall":(33,165), "back_peek":(125,204), "blowjob":(90,317), "stand4":(84,197), "stand5":(111,183), "kneeling1":(163,317), "walking_away":(108,186), "doggy":(141,166), "stand2":(70,209), "stand3":(93,173)})
        shirts_list.append(tie_sweater)

        dress_shirt = Clothing("Dress Shirt", 2, True, True, "Dress_Shirt", True, False, 0, tucked = True, opacity_adjustment = 1.12, display_name = "shirt",
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region],
            crop_offset_dict = {"cowgirl":(149,273), "missionary":(158,185), "kissing":(88,161), "sitting":(236,262), "against_wall":(48,148), "back_peek":(122,182), "blowjob":(94,314), "stand4":(97,180), "stand5":(109,167), "kneeling1":(174,310), "walking_away":(98,166), "doggy":(136,163), "stand2":(51,184), "stand3":(96,152)})
        shirts_list.append(dress_shirt)

        lab_coat = Clothing("Lab Coat", 3, True, True, "Lab_Coat", True, False, 0, opacity_adjustment = 1.08, display_name = "coat",
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region, skirt_region],
            crop_offset_dict = {"cowgirl":(111,268), "missionary":(144,180), "kissing":(86,158), "sitting":(231,255), "against_wall":(44,142), "back_peek":(104,179), "blowjob":(89,316), "stand4":(96,174), "stand5":(103,163), "kneeling1":(130,304), "walking_away":(95,160), "doggy":(125,157), "stand2":(50,177), "stand3":(91,146)})
        shirts_list.append(lab_coat)

        suit_jacket = Clothing("Suit Jacket", 3, True, True, "Suit_Jacket", True, False, 0, display_name = "jacket",
            constrain_regions = [torso_region, upper_arm_region, lower_arm_region, stomach_region],
            crop_offset_dict = {"cowgirl":(145,268), "missionary":(160,191), "kissing":(88,170), "sitting":(259,270), "against_wall":(48,157), "back_peek":(95,192), "blowjob":(97,312), "stand4":(96,186), "stand5":(103,173), "kneeling1":(153,308), "walking_away":(110,176), "doggy":(150,161), "stand2":(74,203), "stand3":(95,163)})
        shirts_list.append(suit_jacket)

        vest = Clothing("Vest", 3, False, True, "Vest", True, False, 0, display_name = "vest",
            constrain_regions = [torso_region, stomach_region],
            crop_offset_dict = {"cowgirl":(154,270), "missionary":(247,188), "kissing":(150,165), "sitting":(279,265), "against_wall":(141,153), "back_peek":(146,186), "blowjob":(107,311), "stand4":(166,182), "stand5":(110,172), "kneeling1":(199,313), "walking_away":(121,167), "doggy":(247,161), "stand2":(101,187), "stand3":(125,154)})
        shirts_list.append(vest)

        business_vest = Clothing("Business Vest", 3, True, True, "Tight_Vest", True, False, 2, whiteness_adjustment = 0.15, opacity_adjustment = 1.3, display_name = "vest",
            constrain_regions = [torso_region, stomach_region],
            crop_offset_dict = {"cowgirl":(198,271), "missionary":(248,191), "kissing":(151,170), "sitting":(280,271), "against_wall":(142,161), "back_peek":(150,192), "blowjob":(110,319), "stand4":(168,187), "stand5":(107,175), "kneeling1":(210,311), "walking_away":(128,175), "doggy":(257,164), "stand2":(104,205), "stand3":(127,164)})
        shirts_list.append(business_vest)


        ##Socks##
        socks_list = []

        short_socks = Clothing("Short Socks", 1, True, True, "Short_Socks", False, False, 0, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "socks",
            crop_offset_dict = {"cowgirl":(95,697), "missionary":(78,816), "kissing":(296,887), "sitting":(87,812), "against_wall":(87,718), "back_peek":(166,896), "blowjob":(113,684), "stand4":(208,926), "stand5":(97,882), "kneeling1":(268,733), "walking_away":(196,824), "doggy":(28,766), "stand2":(91,906), "stand3":(45,893)})
        socks_list.append(short_socks)

        medium_socks = Clothing("Medium Socks", 1, True, True, "Long_Socks", False, False, 0, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "socks",
            crop_offset_dict = {"cowgirl":(59,697), "missionary":(77,677), "kissing":(272,762), "sitting":(86,712), "against_wall":(85,656), "back_peek":(166,775), "blowjob":(112,684), "stand4":(178,797), "stand5":(96,761), "kneeling1":(123,733), "walking_away":(172,713), "doggy":(25,636), "stand2":(90,784), "stand3":(43,767)})
        socks_list.append(medium_socks)

        high_socks = Clothing("High Socks", 1, True, True, "High_Socks", False, False, 0, contrast_adjustment = 1.2, supported_patterns = {"Two Toned":"Pattern_1", "Gradient":"Pattern_2"}, display_name = "socks",
            crop_offset_dict = {"cowgirl":(57,695), "missionary":(78,490), "kissing":(253,620), "sitting":(88,560), "against_wall":(86,527), "back_peek":(162,635), "blowjob":(112,684), "stand4":(158,638), "stand5":(95,607), "kneeling1":(117,704), "walking_away":(146,580), "doggy":(27,501), "stand2":(91,635), "stand3":(45,616)})
        socks_list.append(high_socks)

        thigh_highs = Clothing("Thigh Highs", 1, True, True, "Thigh_Highs", False, False, 5, whiteness_adjustment = 0.1, display_name = "stockings",
            crop_offset_dict = {"cowgirl":(58,697), "missionary":(79,483), "kissing":(248,606), "sitting":(89,555), "against_wall":(88,515), "back_peek":(155,622), "blowjob":(114,681), "stand4":(154,624), "stand5":(96,591), "kneeling1":(119,689), "walking_away":(145,574), "doggy":(29,488), "stand2":(93,622), "stand3":(47,603)})
        socks_list.append(thigh_highs)

        fishnets = Clothing("Fishnets", 1, True, True, "Fishnets", False, False, 10, whiteness_adjustment = 0.2, display_name = "fishnets",
            crop_offset_dict = {"cowgirl":(58,695), "missionary":(78,492), "kissing":(254,625), "sitting":(88,561), "against_wall":(87,529), "back_peek":(163,637), "blowjob":(114,680), "stand4":(159,640), "stand5":(95,609), "kneeling1":(118,707), "walking_away":(148,583), "doggy":(27,505), "stand2":(91,638), "stand3":(46,621)})
        socks_list.append(fishnets)

        garter_with_fishnets = Clothing("Garter and Fishnets", 1, True, True, "Garter_and_Fishnets", False, False, 12, whiteness_adjustment = 0.2, contrast_adjustment = 1.0, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "fishnets",
            crop_offset_dict = {"cowgirl":(59,541), "missionary":(79,407), "kissing":(223,397), "sitting":(90,512), "against_wall":(88,413), "back_peek":(110,427), "blowjob":(113,561), "stand4":(156,422), "stand5":(96,397), "kneeling1":(118,562), "walking_away":(147,414), "doggy":(29,296), "stand2":(93,437), "stand3":(47,405)})
        socks_list.append(garter_with_fishnets)


#        ##Shoes##

        shoes_list = []

        sandles = Clothing("Sandals", 2, True, True, "Sandles", False, False, 0, display_name = "sandals",
            constrain_regions = [foot_region],
            crop_offset_dict = {"cowgirl":(94,691), "missionary":(78,837), "kissing":(297,911), "sitting":(75,828), "against_wall":(84,719), "back_peek":(162,922), "blowjob":(114,675), "stand4":(207,954), "stand5":(95,906), "kneeling1":(272,730), "walking_away":(194,844), "doggy":(24,797), "stand2":(90,933), "stand3":(40,918)})
        shoes_list.append(sandles)

        shoes = Clothing("Shoes", 2, True, True, "Shoes", False, False, 0, display_name = "shoes",
            constrain_regions = [foot_region],
            crop_offset_dict = {"cowgirl":(92,688), "missionary":(58,843), "kissing":(295,933), "sitting":(73,828), "against_wall":(84,715), "back_peek":(155,941), "blowjob":(110,668), "stand4":(207,978), "stand5":(78,917), "kneeling1":(268,726), "walking_away":(194,864), "doggy":(23,809), "stand2":(90,956), "stand3":(34,934)})
        shoes_list.append(shoes)

        slips = Clothing("Slips", 2, True, True, "Slips", False, False, 0, display_name = "slips",
            constrain_regions = [foot_region],
            crop_offset_dict = {"cowgirl":(94,691), "missionary":(71,844), "kissing":(297,941), "sitting":(72,829), "against_wall":(87,718), "back_peek":(163,945), "blowjob":(114,678), "stand4":(208,993), "stand5":(91,933), "kneeling1":(268,728), "walking_away":(195,871), "doggy":(26,820), "stand2":(91,969), "stand3":(40,943)})
        shoes_list.append(slips)

        sneakers = Clothing("Sneakers", 2, True, True, "Sneakers", False, False, 0, whiteness_adjustment = 0.2, supported_patterns = {"Laces":"Pattern_1"}, display_name = "shoes",
            constrain_regions = [foot_region],
            crop_offset_dict = {"cowgirl":(93,687), "missionary":(64,834), "kissing":(294,909), "sitting":(74,825), "against_wall":(84,714), "back_peek":(160,915), "blowjob":(108,675), "stand4":(206,954), "stand5":(89,905), "kneeling1":(241,724), "walking_away":(194,842), "doggy":(23,796), "stand2":(89,932), "stand3":(41,917)})
        shoes_list.append(sneakers)

        sandle_heels = Clothing("Sandal Heels", 2, True, True, "Sandal_Heels", False, False, 1, display_name = "heels",
            constrain_regions = [foot_region],
            crop_offset_dict = {"cowgirl":(94,674), "missionary":(81,864), "kissing":(298,963), "sitting":(76,834), "against_wall":(85,719), "back_peek":(166,965), "blowjob":(113,674), "stand4":(207,1010), "stand5":(98,941), "kneeling1":(270,726), "walking_away":(196,887), "doggy":(26,817), "stand2":(90,984), "stand3":(42,963)})
        shoes_list.append(sandle_heels)

        pumps = Clothing("Pumps", 2, True, True, "Pumps", False, False, 1, supported_patterns = {"Two Toned":"Pattern_1"}, display_name = "pumps",
            constrain_regions = [foot_region],
            crop_offset_dict = {"cowgirl":(92,652), "missionary":(66,840), "kissing":(291,933), "sitting":(78,827), "against_wall":(86,717), "back_peek":(166,937), "blowjob":(109,644), "stand4":(207,978), "stand5":(93,928), "kneeling1":(272,710), "walking_away":(194,863), "doggy":(26,808), "stand2":(90,955), "stand3":(43,943)})
        shoes_list.append(pumps)

        heels = Clothing("Heels", 2, True, True, "Heels", False, False, 1, whiteness_adjustment = 0.2, display_name = "heels",
            constrain_regions = [foot_region],
            crop_offset_dict = {"cowgirl":(96,666), "missionary":(80,842), "kissing":(297,936), "sitting":(89,829), "against_wall":(88,718), "back_peek":(165,942), "blowjob":(114,674), "stand4":(209,988), "stand5":(93,926), "kneeling1":(268,725), "walking_away":(197,868), "doggy":(29,817), "stand2":(93,963), "stand3":(47,940)})
        shoes_list.append(heels)

        high_heels = Clothing("High Heels", 2, True, True, "High_Heels", False, False, 3, display_name = "heels",
            constrain_regions = [foot_region],
            crop_offset_dict = {"cowgirl":(94,674), "missionary":(82,842), "kissing":(294,909), "sitting":(89,826), "against_wall":(86,716), "back_peek":(166,921), "blowjob":(121,655), "stand4":(208,954), "stand5":(92,907), "kneeling1":(272,727), "walking_away":(196,843), "doggy":(28,794), "stand2":(91,930), "stand3":(45,919)})
        shoes_list.append(high_heels)

        boot_heels = Clothing("Boot Heels", 2, True, True, "Boot_Heels", False, False, 1, whiteness_adjustment = 0.1, contrast_adjustment = 1.1, display_name = "boots",
            constrain_regions = [foot_region],
            crop_offset_dict = {"cowgirl":(94,675), "missionary":(74,842), "kissing":(290,930), "sitting":(78,827), "against_wall":(87,717), "back_peek":(163,938), "blowjob":(112,657), "stand4":(207,974), "stand5":(96,918), "kneeling1":(268,722), "walking_away":(196,861), "doggy":(28,805), "stand2":(91,951), "stand3":(44,935)})
        shoes_list.append(boot_heels)

        tall_boots = Clothing("Tall Boots", 2, True, True, "High_Boots", False, False, 0, display_name = "boots",
            constrain_regions = [foot_region, lower_leg_region],
            crop_offset_dict = {"cowgirl":(66,682), "missionary":(74,706), "kissing":(274,789), "sitting":(87,735), "against_wall":(84,667), "back_peek":(160,799), "blowjob":(111,676), "stand4":(181,824), "stand5":(88,785), "kneeling1":(242,726), "walking_away":(176,737), "doggy":(25,661), "stand2":(90,810), "stand3":(41,794)})
        shoes_list.append(tall_boots)

        thigh_high_boots = Clothing("Thigh High Boots", 2, True, True, "Thigh_Boots", False, False, 3, display_name = "boots",
            constrain_regions = [foot_region, lower_leg_region, upper_leg_region],
            crop_offset_dict = {"cowgirl":(51,659), "missionary":(69,502), "kissing":(265,647), "sitting":(82,565), "against_wall":(84,549), "back_peek":(162,661), "blowjob":(109,678), "stand4":(168,667), "stand5":(88,636), "kneeling1":(113,721), "walking_away":(154,599), "doggy":(24,518), "stand2":(88,663), "stand3":(44,644)})
        shoes_list.append(thigh_high_boots)


        ##Accessories##
        earings_list = [] #Note: now more properly known as facial accessories

        chandelier_earings = Clothing("Chandelier Earrings", 2, False, False, "Chandelier_Earings", False, False, 0, body_dependant = False, display_name = "earings",
            crop_offset_dict = {"cowgirl":(262,263), "missionary":(333,143), "kissing":(272,112), "sitting":(391,226), "against_wall":(197,107), "back_peek":(182,157), "blowjob":(223,321), "stand4":(232,145), "stand5":(247,126), "kneeling1":(264,271), "walking_away":(200,136), "doggy":(254,177), "stand2":(191,148), "stand3":(198,111)}) #TODO: Modify this to handle earings which don't vary based on facial type (Should they?)
        earings_list.append(chandelier_earings)

        gold_earings = Clothing("Gold Earings", 2 , False, False, "Gold_Earings", False, False, 0, body_dependant = False, display_name = "earings",
            crop_offset_dict = {"cowgirl":(263,262), "missionary":(334,142), "kissing":(274,111), "sitting":(390,225), "against_wall":(199,106), "back_peek":(186,133), "blowjob":(224,320), "stand4":(232,144), "stand5":(248,125), "kneeling1":(261,270), "walking_away":(199,135), "doggy":(251,174), "stand2":(188,147), "stand3":(200,110)})
        earings_list.append(gold_earings)

        modern_glasses = Facial_Accessory("Modern Glasses", 2, False, False, "Modern_Glasses", False, False, 0, display_name = "earings",
            crop_offset_dict = {"cowgirl":(266,221), "missionary":(338,100), "kissing":(282,69), "sitting":(388,192), "against_wall":(202,71), "back_peek":(169,107), "blowjob":(228,283), "stand4":(231,111), "stand5":(250,93), "kneeling1":(250,228), "walking_away":(191,105), "doggy":(224,144), "stand2":(175,115), "stand3":(205,78)})
        earings_list.append(modern_glasses)

        big_glasses = Facial_Accessory("Big Glasses", 2, False, False, "Big_Glasses", False, False, 0, display_name = "glasses",
            crop_offset_dict = {"cowgirl":(266,221), "missionary":(338,93), "kissing":(283,62), "sitting":(388,192), "against_wall":(202,64), "back_peek":(169,103), "blowjob":(228,283), "stand4":(231,111), "stand5":(250,91), "kneeling1":(248,219), "walking_away":(190,103), "doggy":(221,144), "stand2":(172,115), "stand3":(205,77)})
        earings_list.append(big_glasses)

        sunglasses = Facial_Accessory("Sunglasses", 2, False, False, "Sunglasses", False, False, 0, display_name = "sunglasses",
            crop_offset_dict = {"cowgirl":(265,220), "missionary":(337,95), "kissing":(282,64), "sitting":(387,192), "against_wall":(202,66), "back_peek":(167,103), "blowjob":(227,281), "stand4":(230,110), "stand5":(250,92), "kneeling1":(248,221), "walking_away":(190,104), "doggy":(222,144), "stand2":(173,114), "stand3":(204,76)})
        earings_list.append(sunglasses)

        head_towel = Clothing("Head Towel", 2, False, False, "Head_Towel", False, False, 0, body_dependant = False, display_name = "head towel")
        # earings_list.append(head_towel) #TEMPORARY FOR TESTING




        #TODO: Add a makeup section
        light_eye_shadow = Facial_Accessory("Light Eyeshadow", 1, False, False, "Upper_Eye_Shadow", False, False, 0, opacity_adjustment = 0.5,
            crop_offset_dict = {"cowgirl":(286,249), "missionary":(354,102), "kissing":(296,74), "sitting":(403,200), "against_wall":(217,73), "back_peek":(222,114), "blowjob":(245,320), "stand4":(250,127), "stand5":(264,100), "kneeling1":(269,231), "walking_away":(0,0), "doggy":(240,181), "stand2":(191,138), "stand3":(220,85)})
        earings_list.append(light_eye_shadow)

        heavy_eye_shadow = Facial_Accessory("Heavy Eyeshadow", 1, False, False, "Full_Shimmer", False, False, 1, opacity_adjustment = 0.5,
            crop_offset_dict = {"cowgirl":(279,244), "missionary":(349,97), "kissing":(291,69), "sitting":(398,196), "against_wall":(212,67), "back_peek":(214,110), "blowjob":(239,316), "stand4":(244,123), "stand5":(259,95), "kneeling1":(264,224), "walking_away":(0,0), "doggy":(238,178), "stand2":(187,135), "stand3":(215,80)})
        earings_list.append(heavy_eye_shadow)

        blush = Facial_Accessory("Blush", 1, False, False, "Blush", False, False, 0, opacity_adjustment = 0.5,
            crop_offset_dict = {"cowgirl":(270,245), "missionary":(341,110), "kissing":(282,81), "sitting":(393,204), "against_wall":(205,79), "back_peek":(198,122), "blowjob":(231,312), "stand4":(237,127), "stand5":(253,102), "kneeling1":(259,238), "walking_away":(199,129), "doggy":(239,176), "stand2":(184,134), "stand3":(207,88)})
        earings_list.append(blush)

        lipstick = Facial_Accessory("Lipstick", 1, False, False, "Lipstick", False, False, 1, opacity_adjustment = 0.5,
            crop_offset_dict = {"cowgirl":(302,302), "missionary":(366,145), "kissing":(302,115), "sitting":(417,241), "against_wall":(228,115), "back_peek":(239,157), "blowjob":(258,367), "stand4":(265,168), "stand5":(273,141), "kneeling1":(297,286), "walking_away":(0,0), "doggy":(0,0), "stand2":(215,181), "stand3":(231,127)})
        earings_list.append(lipstick)


        bracelet_list = []

        copper_bracelet = Clothing("Copper Bracelet", 2, False, False, "Copper_Bracelet", False, False, 0, display_name = "bracelet",
            crop_offset_dict = {"cowgirl":(388,664), "missionary":(525,438), "kissing":(419,456), "sitting":(456,378), "against_wall":(466,163), "back_peek":(337,348), "blowjob":(392,652), "stand4":(373,511), "stand5":(399,479), "kneeling1":(368,615), "walking_away":(97,489), "doggy":(136,457), "stand2":(268,206), "stand3":(388,460)})
        bracelet_list.append(copper_bracelet)

        gold_bracelet = Clothing("Gold Bracelet", 2, False, False, "Gold_Bracelet", False, False, 0, display_name = "bracelet",
            crop_offset_dict = {"cowgirl":(397,617), "missionary":(518,408), "kissing":(414,427), "sitting":(487,389), "against_wall":(452,197), "back_peek":(327,338), "blowjob":(383,610), "stand4":(365,477), "stand5":(387,444), "kneeling1":(397,586), "walking_away":(101,455), "doggy":(143,432), "stand2":(284,229), "stand3":(373,427)})
        bracelet_list.append(gold_bracelet)

        spiked_bracelet = Clothing("Spiked Bracelet", 2, False, False, "Spiked_Bracelet", False, False, 2, display_name = "bracelet",
            crop_offset_dict = {"cowgirl":(381,635), "missionary":(518,425), "kissing":(416,438), "sitting":(454,372), "against_wall":(457,155), "back_peek":(331,344), "blowjob":(386,626), "stand4":(368,493), "stand5":(393,458), "kneeling1":(362,599), "walking_away":(97,473), "doggy":(133,442), "stand2":(266,196), "stand3":(380,442)})
        bracelet_list.append(spiked_bracelet)

        bead_bracelet = Clothing("Bead Bracelet", 2, False, False, "Bead_Bracelet", False, False, 0, display_name = "bracelet",
            crop_offset_dict = {"cowgirl":(186,590), "missionary":(161,436), "kissing":(122,260), "sitting":(237,506), "against_wall":(91,294), "back_peek":(345,407), "blowjob":(100,627), "stand4":(149,401), "stand5":(130,229), "kneeling1":(223,749), "walking_away":(331,439), "doggy":(497,626), "stand2":(51,490), "stand3":(103,464)})
        bracelet_list.append(bead_bracelet)

        forearm_gloves = Clothing("Forearm Gloves", 2, False, False, "Forearm_Gloves", False, False, 2, supported_patterns = {"Two Tone":"Pattern_1"}, display_name = "gloves",
            crop_offset_dict = {"cowgirl":(154,495), "missionary":(161,349), "kissing":(91,263), "sitting":(215,340), "against_wall":(53,107), "back_peek":(310,344), "blowjob":(81,525), "stand4":(105,327), "stand5":(133,174), "kneeling1":(185,519), "walking_away":(100,376), "doggy":(134,381), "stand2":(47,177), "stand3":(99,365)})
        bracelet_list.append(forearm_gloves)


        rings_list = []

        diamond_ring = Clothing("Diamond Ring", 2, False, False, "Diamond_Ring", False, False, 0, display_name = "ring",
            crop_offset_dict = {"cowgirl":(425,727), "missionary":(570,514), "kissing":(454,511), "sitting":(447,344), "against_wall":(506,109), "back_peek":(375,382), "blowjob":(427,724), "stand4":(385,567), "stand5":(463,491), "kneeling1":(321,678), "walking_away":(109,550), "doggy":(129,464), "stand2":(292,166), "stand3":(420,533)})
        rings_list.append(diamond_ring)

        garnet_ring = Clothing("Garnet Ring", 2, False, False, "Garnet_Ring", False, False, 0, display_name = "ring",
            crop_offset_dict = {"cowgirl":(228,676), "missionary":(174,539), "kissing":(136,270), "sitting":(199,548), "against_wall":(149,327), "back_peek":(393,430), "blowjob":(81,721), "stand4":(140,484), "stand5":(169,163), "kneeling1":(258,872), "walking_away":(332,510), "doggy":(325,430), "stand2":(51,579), "stand3":(116,555)})
        rings_list.append(garnet_ring)

        copper_ring_set = Clothing("Copper Ring Set", 2, False, False, "Copper_Ring_Set", False, False, 0, display_name = "rings",
            crop_offset_dict = {"cowgirl":(354,698), "missionary":(563,514), "kissing":(417,484), "sitting":(433,334), "against_wall":(451,102), "back_peek":(352,349), "blowjob":(408,697), "stand4":(374,566), "stand5":(429,492), "kneeling1":(310,632), "walking_away":(110,535), "doggy":(129,461), "stand2":(276,162), "stand3":(384,509)})
        rings_list.append(copper_ring_set)


        neckwear_list = []

        wool_scarf = Clothing("Wool Scarf", 3, False, False, "Wool_Scarf", False, False, 0, display_name = "scarf",
            crop_offset_dict = {"cowgirl":(234,268), "missionary":(311,180), "kissing":(223,156), "sitting":(353,253), "against_wall":(177,144), "back_peek":(162,174), "blowjob":(185,322), "stand4":(209,172), "stand5":(188,162), "kneeling1":(245,302), "walking_away":(176,155), "doggy":(266,161), "stand2":(171,176), "stand3":(171,140)})
        neckwear_list.append(wool_scarf)

        necklace_set = Clothing("Necklace Set", 3, False, False, "Necklace_Set", True, False, 0, display_name = "necklaces",
            crop_offset_dict = {"cowgirl":(254,280), "missionary":(333,191), "kissing":(222,169), "sitting":(355,267), "against_wall":(196,157), "back_peek":(175,188), "blowjob":(210,336), "stand4":(229,185), "stand5":(194,176), "kneeling1":(261,314), "walking_away":(200,171), "doggy":(296,167), "stand2":(192,204), "stand3":(192,158)})
        neckwear_list.append(necklace_set)

        gold_chain_necklace = Clothing("Gold Chain Necklace", 3, False, False, "Gold_Chain_Necklace", False, False, 0, display_name = "necklace",
            crop_offset_dict = {"cowgirl":(272,287), "missionary":(341,195), "kissing":(276,171), "sitting":(398,273), "against_wall":(204,162), "back_peek":(179,198), "blowjob":(234,350), "stand4":(238,190), "stand5":(248,179), "kneeling1":(268,321), "walking_away":(208,177), "doggy":(317,173), "stand2":(206,208), "stand3":(198,164)})
        neckwear_list.append(gold_chain_necklace)

        spiked_choker = Clothing("Spiked Choker", 3, False, False, "Spiked_Choker", False, False, 3, display_name = "choker",
            crop_offset_dict = {"cowgirl":(253,273), "missionary":(326,180), "kissing":(264,162), "sitting":(387,261), "against_wall":(188,154), "back_peek":(172,182), "blowjob":(218,330), "stand4":(224,178), "stand5":(240,166), "kneeling1":(253,302), "walking_away":(195,163), "doggy":(284,161), "stand2":(194,186), "stand3":(187,154)})
        neckwear_list.append(spiked_choker)

        lace_choker = Clothing("Lace Choker", 2, False, False, "Lace_Choker", False, False, 3, whiteness_adjustment = 0.1, display_name = "choker",
            crop_offset_dict = {"cowgirl":(276,294), "missionary":(345,186), "kissing":(281,162), "sitting":(402,258), "against_wall":(207,150), "back_peek":(182,181), "blowjob":(0,0), "stand4":(243,180), "stand5":(256,167), "kneeling1":(277,317), "walking_away":(212,160), "doggy":(294,170), "stand2":(210,182), "stand3":(206,147)})
        neckwear_list.append(lace_choker)

        wide_choker = Clothing("Wide Choker", 2, False, False, "Wide_Choker", False, False, 3, display_name = "choker",
            crop_offset_dict = {"cowgirl":(274,289), "missionary":(342,181), "kissing":(278,157), "sitting":(401,256), "against_wall":(205,145), "back_peek":(180,175), "blowjob":(237,356), "stand4":(240,176), "stand5":(254,162), "kneeling1":(271,316), "walking_away":(210,155), "doggy":(290,167), "stand2":(209,178), "stand3":(201,141)})
        neckwear_list.append(wide_choker)

        breed_collar = Clothing("Breed Me Collar", 3, False, False, "Collar_Breed", False, False, 8, supported_patterns = {"Two Tone":"Pattern_1"}, display_name = "collar",
            crop_offset_dict = {"cowgirl":(273,285), "missionary":(340,182), "kissing":(277,158), "sitting":(400,255), "against_wall":(204,147), "back_peek":(178,173), "blowjob":(236,349), "stand4":(238,177), "stand5":(253,164), "kneeling1":(268,313), "walking_away":(208,156), "doggy":(287,166), "stand2":(207,179), "stand3":(199,143)})
        neckwear_list.append(breed_collar)

        cum_slut_collar = Clothing("Cum Slut Collar", 3, False, False, "Collar_Cum_Slut", False, False, 8, supported_patterns = {"Two Tone":"Pattern_1"}, display_name = "collar",
            crop_offset_dict = {"cowgirl":(273,285), "missionary":(340,182), "kissing":(277,158), "sitting":(400,255), "against_wall":(204,147), "back_peek":(178,173), "blowjob":(236,349), "stand4":(238,177), "stand5":(253,164), "kneeling1":(268,314), "walking_away":(208,156), "doggy":(287,166), "stand2":(207,179), "stand3":(199,143)})
        neckwear_list.append(cum_slut_collar)

        fuck_doll_collar = Clothing("Fuck Doll Collar", 3, False, False, "Collar_Fuck_Doll", False, False, 8, supported_patterns = {"Two Tone":"Pattern_1"}, display_name = "collar",
            crop_offset_dict = {"cowgirl":(273,285), "missionary":(340,182), "kissing":(277,158), "sitting":(400,255), "against_wall":(204,147), "back_peek":(178,173), "blowjob":(236,349), "stand4":(238,177), "stand5":(253,164), "kneeling1":(268,314), "walking_away":(208,156), "doggy":(287,166), "stand2":(207,179), "stand3":(199,143)})
        neckwear_list.append(fuck_doll_collar)




        ##Non Clothing Accessories##
        ass_cum = Clothing("Ass Cum", 1, False, False, "Ass_Covered", False, False, 10, whiteness_adjustment = 0.2,
            crop_offset_dict = {"cowgirl":(472,614), "missionary":(286,567), "kissing":(456,487), "sitting":(515,607), "against_wall":(0,0), "back_peek":(109,468), "blowjob":(0,0), "stand4":(0,0), "stand5":(266,451), "kneeling1":(0,0), "walking_away":(132,454), "doggy":(201,325), "stand2":(333,547), "stand3":(0,0)})

        tits_cum = Clothing("Tit Cum", 1, False, False, "Tits_Covered", True, False, 10, whiteness_adjustment = 0.2,
            crop_offset_dict = {"cowgirl":(201,378), "missionary":(249,222), "kissing":(155,220), "sitting":(283,335), "against_wall":(145,224), "back_peek":(276,254), "blowjob":(113,411), "stand4":(169,256), "stand5":(111,229), "kneeling1":(250,436), "walking_away":(128,300), "doggy":(258,293), "stand2":(107,266), "stand3":(128,224)})

        stomach_cum = Clothing("Stomach Cum", 1, False, False, "Stomach_Covered", False, False, 10, whiteness_adjustment = 0.2,
            crop_offset_dict = {"cowgirl":(258,528), "missionary":(297,327), "kissing":(220,397), "sitting":(340,496), "against_wall":(183,382), "back_peek":(326,416), "blowjob":(172,566), "stand4":(222,407), "stand5":(166,387), "kneeling1":(254,597), "walking_away":(0,0), "doggy":(292,661), "stand2":(130,401), "stand3":(198,366)})

        creampie_cum = Clothing("Creampie", 1, False, False, "Creampie", False, False, 10, whiteness_adjustment = 0.2,
            crop_offset_dict = {"cowgirl":(228,675), "missionary":(285,538), "kissing":(335,540), "sitting":(359,614), "against_wall":(231,540), "back_peek":(198,546), "blowjob":(231,690), "stand4":(242,562), "stand5":(231,530), "kneeling1":(263,705), "walking_away":(232,523), "doggy":(305,431), "stand2":(183,566), "stand3":(220,538)})

        mouth_cum = Facial_Accessory("Mouth Cum", 1, False, False, "Mouth_Dribble", False, False, 10, whiteness_adjustment = 0.2,
            crop_offset_dict = {"cowgirl":(298,261), "missionary":(363,114), "kissing":(298,89), "sitting":(413,210), "against_wall":(225,84), "back_peek":(238,140), "blowjob":(254,332), "stand4":(262,139), "stand5":(269,118), "kneeling1":(290,266), "walking_away":(0,0), "doggy":(0,0), "stand2":(209,156), "stand3":(227,97)})

        face_cum = Facial_Accessory("Face Cum", 1, False, False, "Face_Covered", False, False, 10, whiteness_adjustment = 0.2,
            crop_offset_dict = {"cowgirl":(273,228), "missionary":(344,90), "kissing":(285,62), "sitting":(394,189), "against_wall":(207,61), "back_peek":(203,116), "blowjob":(233,303), "stand4":(239,117), "stand5":(255,88), "kneeling1":(258,222), "walking_away":(199,130), "doggy":(241,192), "stand2":(182,140), "stand3":(210,73)})

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
