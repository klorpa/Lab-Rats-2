init -1 python:
    def make_person(requirement_dict = None): #This will generate a person, using a pregen body some of the time if they are available.
        split_proportion = 20 #1/5 characters generated will be a premade character.
        return_character = None
        if renpy.random.randint(1,100) < split_proportion:
            return_character = get_premade_character(requirement_dict)
        if return_character is None: #Either we aren't getting a premade, or we are out of them.
            if requirement_dict is None:
                requirement_dict = {}
            return_character = create_random_person(**requirement_dict)
        return return_character

    # create_random_person is used to generate a Person object from a list of random or provided stats. use "make_a_person" to properly get premade characters mixed with randoms.
    def create_random_person(name = None, name_list = None, last_name = None, last_name_list = None, age = None, age_range = None, body_type = None, body_type_list = None, face_style = None, face_style_list = None, tits = None, tits_range = None, height = None, height_range = None,
        hair_colour = None, hair_colour_list = None, hair_style = None, hair_style_list = None, pubes_colour = None, pubes_colour_list = None, pubes_style = None, pubes_style_list = None, skin = None, skin_list = None, eyes = None, eyes_list = None, job = None, job_list = None,
        personality = None, personality_list = None, custom_font = None, custom_font_list = None, name_color = None, name_color_list = None, dial_color = None, dial_color_list = None, starting_wardrobe = None, starting_wardrobe_list = None, stat_array = None, stat_range_array = None, skill_array = None, skill_range_array = None,
        sex_skill_array = None, sex_skill_range_array = None, sluttiness = None, sluttiness_range = None, obedience = None, obedience_range = None, happiness = None, happiness_range = None, love = None, love_range = None, start_home = None,
        title = None, title_list = None, possessive_title = None, possessive_title_list = None, mc_title = None, mc_title_list = None, relationship = None, relationship_list = None, kids = None, kids_range = None, kids_floor = None, kids_ceiling = None, SO_name = None, SO_name_list = None, base_outfit = None, base_outfit_list = None,
        generate_insta = None, generate_dikdok = None, generate_onlyfans = None,
        suggestibility = None, suggestibility_range = None, work_experience = None, work_experience_range = None, type="random"):

        
        if personality is None:
            if personality_list is None:
                personality = get_random_personality()
            else:
                personality =  get_random_from_list(personality_list)

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
            if name_list is None:
                name = Person.get_random_name()
            else:
                name = get_random_from_list(name_list)
        if last_name is None:
            if last_name_list is None:
                last_name = Person.get_random_last_name()
            else:
                last_name = get_random_from_list(last_name_list)
        if age is None:
            if age_range is None:
                age = renpy.random.randint(Person.get_age_floor(),Person.get_age_ceiling())
            else:
                if (age_range[0] > age_range[1]): #Make sure range is correct order 
                    age_range.reverse()
                age = renpy.random.randint(age_range[0],age_range[1])
        if body_type is None:
            if body_type_list is None:
                body_type = Person.get_random_body_type()
            else:
                body_type_list =  get_random_from_list(body_type)
        if tits is None:
            if tits_range is None:
                tits = Person.get_random_tit()
            else:
                tits = get_random_from_weighted_list(tits_range)
        if height is None:
            if height_range is None:
                height = renpy.random.uniform(Person.get_height_floor(),Person.get_height_ceiling())
            else:
                if (height_range[0] > height_range[1]):
                    height_range.reverse()
                height = renpy.random.uniform(height_range[0],height_range[1])
        if hair_colour is None: #If we pass nothing we can pick a random hair colour
            if hair_colour_list is None:
                hair_colour = Person.generate_hair_colour() #Hair colour is a list of [string, [colour]], generated with variations by this function,
            else:
                hair_colour = get_random_from_list(hair_colour_list)
        if isinstance(hair_colour, basestring):
            hair_colour = Person.generate_hair_colour(hair_colour) #If we pass a string assume we want to generate a variation based on that colour.
        #else: we assume a full colour list was passed and everything is okay.

        if hair_style is None:
            if hair_style_list is None:
                hair_style = get_random_from_list(hair_styles)
            else:
                hair_style = get_random_from_list(hair_style_list)
        hair_style = hair_style.get_copy() #Get a copy so we don't modify the master.

        hair_style.colour = hair_colour[1]

        if pubes_style is None:
            if pubes_style_list is None:
                pubes_style = get_random_from_list(pube_styles).get_copy()
            else:
                pubes_style = get_random_from_list(pubes_style_list).get_copy()
            
        pubes_colour = Person.get_darkened_colour(hair_style.colour)
        pubes_style.colour = pubes_colour

        if eyes is None:
            if eyes_list is None:
                eyes = Person.generate_eye_colour()
            else:
                eyes = get_random_from_list(eyes_list)
        if isinstance(eyes, basestring):
            eyes = Person.generate_eye_colour(eyes) #If it's a string assume we want a variation within that eye catagory
        # else: we assume at this point what was passed is a correct [description, colour] list.

        if skin is None:
            if skin_list is None:
                skin = Person.get_random_skin()
            else:
                skin = get_random_from_list(skin_list)

        if skin == "white":
            body_images = white_skin
        elif skin == "tan":
            body_images = tan_skin
        else:
            body_images = black_skin

        if face_style is None:
            if face_style_list is None:
                face_style = Person.get_random_face()
            else:
                face_style = get_random_from_list(face_style_list)

        emotion_images = Expression(name+"\'s Expression Set", skin, face_style)

        #if eyes is None:
        #    eyes = Person.get_random_eye()

        if job is None:
            if job_list is None:
                job = get_random_job()
            else:
                job = get_random_from_list(job_list)

        if custom_font is None:
            if custom_font_list is None:
                #Get a font
                custom_font = get_random_font()
            else:
                custom_font = get_random_from_list(custom_font_list)
        if name_color is None:
            if name_color_list is None:
                # Get a color
                name_color = get_random_readable_color()
            else:
                name_color = get_random_from_list(name_color_list)

        if dial_color is None:
            if dial_color_list is None:
                # Use name_color
                dial_color = copy.copy(name_color) #Take a copy
            else:
                dial_color = get_random_from_list(dial_color)


        if skill_array is None:
            if skill_range_array is None:
                skill_range_array = [[Person.get_skill_floor(),Person.get_skill_ceiling()] for x in range(0,5)]
            skill_array = [renpy.random.randint(skill_range[0],skill_range[1]) for skill_range in skill_range_array]
            
        if stat_array is None:
            if stat_range_array is None:
                stat_range_array = [[Person.get_stat_floor(),Person.get_stat_ceiling()] for x in range(0,3)]
            stat_array = [renpy.random.randint(stat_range[0],stat_range[1]) for stat_range in stat_range_array]

        if sex_skill_array is None:
            if sex_skill_range_array is None:
                sex_skill_range_array = [[Person.get_sex_skill_floor(),Person.get_sex_skill_ceiling()] for x in range(0,4)]
            sex_skill_array = [renpy.random.randint(sex_skill_range[0],sex_skill_range[1]) for sex_skill_range in sex_skill_range_array]

        if love is None:
            if love_range is None:
                love_range = [Person.get_love_floor(),Person.get_love_ceiling()]
            love = renpy.random.randint(love_range[0],love_range[1])

        if happiness is None:
            if happiness_range is None:
                happiness_range = [Person.get_happiness_floor(),Person.get_happiness_ceiling()]
            happiness = renpy.random.randint(happiness_range[0],happiness_range[1])

        if suggestibility is None:
            if suggestibility_range is None:
                suggestibility_range = [Person.get_suggestibility_floor(),Person.get_suggestibility_ceiling()]
            suggestibility = renpy.random.randint(suggestibility_range[0],suggestibility_range[1])

        if obedience is None:
            if obedience_range is None:
                obedience_range = [Person.get_obedience_floor(),Person.get_obedience_ceiling()]
            obedience = renpy.random.randint(obedience_range[0],obedience_range[1])

        if sluttiness is None:
            if sluttiness_range is None:
                sluttiness_range = [Person.get_sluttiness_floor(),Person.get_sluttiness_ceiling()]
            sluttiness = renpy.random.randint(sluttiness_range[0],sluttiness_range[1])

        if work_experience is None:
            if work_experience_range is None:
                work_experience_range =  [Person.get_work_experience_floor(),Person.get_work_experience_ceiling()]
            work_experience = renpy.random.randint(work_experience_range[0], work_experience_range[1])

        if relationship is None:
            if relationship_list is None:
                relationship_list = Person.get_potential_relationships_list()
            relationship_list = Person.finalize_relationships_weight(relationship_list,age)
            relationship = get_random_from_weighted_list(relationship_list)

        if starting_wardrobe is None:
            if starting_wardrobe_list is None:
                starting_wardrobe = Wardrobe(name +"'s Wardrobe")
                starting_wardrobe = starting_wardrobe.merge_wardrobes(default_wardrobe.get_random_selection(25))
            else:
                starting_wardrobe = get_random_from_list(starting_wardrobe_list)

        if base_outfit is None:
            if base_outfit_list is None:
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
                    the_glasses.colour = Person.get_random_glasses_frame_colour()
                    base_outfit.add_accessory(the_glasses)
            else:
                base_outfit = get_random_from_list(base_outfit_list)
        if kids is None:
            #Need to define these if unkown
            if age_range is None:
                age_range = [age,age]
            if relationship_list is None:
                relationship_list = [relationship]
            if kids_range is None:
                kids_range = Person.get_initial_kids_range(age_range,relationship_list)
            kids_range = Person.finalize_kids_range(kids_range,age_range,relationship_list,age,relationship)
            kids = renpy.random.randint(kids_range[0],kids_range[1])
            if kids_floor is None:
                kids_floor = 0
            if kids < kids_floor:
                kids = kids_floor
            if kids_ceiling is not None:
                if kids > kids_ceiling:
                    kids = kids_ceiling

        if relationship != "Single":
            if SO_name is None:
                if SO_name_list is None:
                    SO_name = Person.get_random_male_name()
                else:
                    SO_name = get_random_from_list(SO_name_list)

        return Person(name,last_name,age,body_type,tits,height,body_images,emotion_images,hair_colour,hair_style,pubes_colour,pubes_style,skin,eyes,job,starting_wardrobe,personality,
            stat_array,skill_array,sex_skill_list=sex_skill_array,sluttiness=sluttiness,obedience=obedience,suggest=suggestibility, love=love, happiness=happiness, home = start_home,
            font = custom_font, name_color = name_color , dialogue_color = dial_color,
            face_style = face_style,
            title = title, possessive_title = possessive_title, mc_title = mc_title,
            relationship = relationship, kids = kids, SO_name = SO_name, base_outfit = base_outfit,
            generate_insta = generate_insta, generate_dikdok = generate_dikdok, generate_onlyfans = generate_onlyfans,
            work_experience = work_experience,type=type)
