init -1 python:
    def make_person(requirement_dict = None): #This will generate a person, using a pregen body some of the time if they are available.
        split_proportion = 20 #1/5 characters generated will be a premade character.
        return_character = None
        if renpy.random.randint(1,100) < split_proportion and requirement_dict is None:
            return_character = get_premade_character() #NOTE: We don't use premades if there are character requirements at the moment. TODO: Properly skim them to grab valid people.

        if return_character is None: #Either we aren't getting a premade, or we are out of them.
            if requirement_dict is None:
                requirement_dict = {}
            return_character = create_random_person(**requirement_dict)
        return return_character

    # create_random_person is used to generate a Person object from a list of random or provided stats. use "make_a_person" to properly get premade characters mixed with randoms.
    def create_random_person(name = None, last_name = None, age = None, body_type = None, face_style = None, tits = None, height = None,
        hair_colour = None, hair_style = None, pubes_colour = None, pubes_style = None, skin = None, eyes = None, job = None,
        personality = None, custom_font = None, name_color = None, dial_color = None, starting_wardrobe = None, stat_array = None, skill_array = None, sex_array = None,
        start_sluttiness = None, start_obedience = None, start_happiness = None, start_love = None, start_home = None,
        title = None, possessive_title = None, mc_title = None, relationship = None, kids = None, SO_name = None, base_outfit = None,
        generate_insta = None, generate_dikdok = None, generate_onlyfans = None,
        bonus_kids = 0, bonus_sluttiness = 0, bonus_obedience = 0, bonus_happiness = 0, bonus_suggest = 0, bonus_love = 0,
        stat_cap = 5, skill_cap = 5, age_floor = 18, age_ceiling = 50):

        if personality is None:
            personality = get_random_personality()

        if generate_insta is None:
            if renpy.random.randint(0,100) < personality.insta_chance:
                generate_insta = True
            else:
                generate_insta = False

        if generate_dikdok is None:
            if renpy.random.randint(0,100) < personality.dikdok_chance:
                generate_dikdok = True
            else:
                generate_dikdok = False

        if generate_onlyfans is None:
            generate_onlyfans = False


        if name is None:
            name = get_random_name()
        if last_name is None:
            last_name = get_random_last_name()
        if age is None:
            if age_ceiling < age_floor:
                age_ceiling = age_floor # Make sure our range is actually a range and not inverted.
            age = renpy.random.randint(age_floor,age_ceiling)
        if body_type is None:
            body_type = get_random_body_type()
        if tits is None:
            tits = get_random_tit()
        if height is None:
            height = 0.9 + (renpy.random.random()/10)

        if hair_colour is None: #If we pass nothing we can pick a random hair colour
            hair_colour = generate_hair_colour() #Hair colour is a list of [string, [colour]], generated with variations by this function,
        elif isinstance(hair_colour, basestring):
            hair_colour = generate_hair_colour(hair_colour) #If we pass a string assume we want to generate a variation based on that colour.
        #else: we assume a full colour list was passed and everything is okay.

        if hair_style is None:
            hair_style = get_random_from_list(hair_styles).get_copy()
        else:
            hair_style = hair_style.get_copy() #Get a copy so we don't modify the master.

        hair_style.colour = hair_colour[1]

        if pubes_style is None:
            pubes_style = get_random_from_list(pube_styles).get_copy()

        pubes_colour = get_darkened_colour(hair_colour[1])
        pubes_style.colour = pubes_colour

        if eyes is None:
            eyes = generate_eye_colour()
        elif isinstance(eyes, basestring):
            eyes = generate_eye_colour(eyes) #If it's a string assume we want a variation within that eye catagory
        # else: we assume at this point what was passed is a correct [description, colour] list.

        if skin is None:
            skin = get_random_skin()
        if face_style is None:
            face_style = get_random_face()
        if skin == "white":
            body_images = white_skin
        elif skin == "tan":
            body_images = tan_skin
        else:
            body_images = black_skin

        emotion_images = Expression(name+"\'s Expression Set", skin, face_style)

        if eyes is None:
            eyes = get_random_eye()

        if job is None:
            job = get_random_job()


        if custom_font is None:
            #Get a font
            my_custom_font = get_random_font()

        if name_color is None:
            # Get a color
            name_color = get_random_readable_color()

        if dial_color is None:
            # Use name_color
            dial_color = copy.copy(name_color) #Take a copy


        # if recruitment_skill_improvement_policy.is_active():
        #     skill_cap += 2
        #
        # if recruitment_stat_improvement_policy.is_active():
        #     stat_cap += 2

        if skill_array is None:
            skill_array = [renpy.random.randint(1,skill_cap),renpy.random.randint(1,skill_cap),renpy.random.randint(1,skill_cap),renpy.random.randint(1,skill_cap),renpy.random.randint(1,skill_cap)]

        if stat_array is None:
            stat_array = [renpy.random.randint(1,stat_cap),renpy.random.randint(1,stat_cap),renpy.random.randint(1,stat_cap)]

        if sex_array is None:
            sex_array = [renpy.random.randint(0,5),renpy.random.randint(0,5),renpy.random.randint(0,5),renpy.random.randint(0,5)]

        if start_love is None:
            start_love = 0
        start_love += bonus_love

        if start_happiness is None:
            start_happiness = 100 + renpy.random.randint(-10,10)
        start_happiness += bonus_happiness

        start_suggest = 0 + bonus_suggest

        if start_obedience is None:
            start_obedience = renpy.random.randint(-10,10)
        start_obedience += bonus_obedience

        if start_sluttiness is None:
            start_sluttiness = renpy.random.randint(0,10)
        start_sluttiness += bonus_sluttiness

        if relationship is None:
            relationship = get_random_from_weighted_list([["Single",120-age],["Girlfriend",50],["Fiancée",120-(age*2)],["Married",20+(age*4)]]) #Age plays a major factor.

        if starting_wardrobe is None:
            starting_wardrobe = Wardrobe(name +"'s Wardrobe")
            starting_wardrobe = starting_wardrobe.merge_wardrobes(default_wardrobe.get_random_selection(25))

        if base_outfit is None:
            base_outfit = Outfit(name + "'s base accessories")
            if relationship == "Fiancée" or relationship == "Married":
                base_outfit.add_accessory(diamond_ring.get_copy())

            if renpy.random.randint(0,100) < age:
                #They need/want glasses.
                the_glasses = None
                if renpy.random.randint(0,100) < 50:
                    the_glasses = modern_glasses.get_copy()
                else:
                    the_glasses = big_glasses.get_copy()
                the_glasses.colour = get_random_glasses_frame_colour()
                base_outfit.add_accessory(the_glasses)

        if kids is None:
            kids = 0
            if age >=28:
                kids += renpy.random.randint(0,1) #Young characters don't have as many kids

            if age >= 38:
                kids += renpy.random.randint(0,1) #As you get older you're more likely to have one

            if relationship == "Girlfriend":
                kids += renpy.random.randint(0,1) #People who are dating have kids more often than single people

            elif relationship != "Single":
                kids += renpy.random.randint(0,3) #And married/engaged people have more kids still

            if age <= 22:
                kids += -1 #Young people have less time to have kids in general, so modify their number down a bit.
                if kids < 0:
                    kids = 0

            kids += bonus_kids

        if SO_name is None and relationship != "Single":
            SO_name = get_random_male_name()

        return Person(name,last_name,age,body_type,tits,height,body_images,emotion_images,hair_colour,hair_style,pubes_colour,pubes_style,skin,eyes,job,starting_wardrobe,personality,
            stat_array,skill_array,sex_list=sex_array,sluttiness=start_sluttiness,obedience=start_obedience,suggest=start_suggest, love=start_love, happiness=start_happiness, home = start_home,
            font = my_custom_font, name_color = name_color , dialogue_color = dial_color,
            face_style = face_style,
            title = title, possessive_title = possessive_title, mc_title = mc_title,
            relationship = relationship, kids = kids, SO_name = SO_name, base_outfit = base_outfit,
            generate_insta = generate_insta, generate_dikdok = generate_dikdok, generate_onlyfans = generate_onlyfans)
