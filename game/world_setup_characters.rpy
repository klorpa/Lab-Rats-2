init 1:
    python:

        def setup_stephanie():
           ### STEPHANIE ###
            stephanie_wardrobe = wardrobe_from_xml("Stephanie_Wardrobe")

            #original height = 0.94
            global stephanie
            stephanie = create_random_person(name = "Stephanie", age = 29, body_type = "standard_body", face_style = "Face_3",  tits="C", height = 0.96, hair_colour="brown", hair_style = messy_short_hair, skin="white" , \
                eyes = "brown", personality = stephanie_personality, name_color = "#cf3232", dial_color = "#cf3232" , starting_wardrobe = stephanie_wardrobe, \
                stat_array = [3,4,3], skill_array = [1,1,4,2,1], sex_skill_array = [3,4,2,1], sluttiness = 14, obedience = 112, happiness = 119, love = 7, \
                title = "Stephanie", possessive_title = "Your friend", mc_title = mc.name, relationship = "Single", kids = 0,
                work_experience = 3,type="story")
            stephanie.generate_home()
            stephanie.add_role(steph_role)
            stephanie.change_job(steph_lab_assistant)
            #NOTE: Stepahnie is hired in an event at the start of the game.
            stephanie.set_opinion("research work", 2, True) #Steph always loves research work, which you know

        def setup_nora():
            ### NORA ##
            nora_wardrobe = wardrobe_from_xml("Nora_Wardrobe")
            #original height = 0.98
            global nora
            nora_base = Outfit("Nora's accessories")
            nora_glasses = modern_glasses.get_copy()
            nora_glasses.colour = [0.45,0.53,0.6,1.0]
            nora_earrings = gold_earings.get_copy()
            nora_earrings.colour = [1.0,1.0,0.93,1.0]
            nora_base.add_accessory(nora_glasses)
            nora_base.add_accessory(nora_earrings)
            nora = create_random_person(name = "Nora", age = 47, body_type = "standard_body", face_style = "Face_4", tits = "D", height = 1.02, hair_colour="black", hair_style = bowl_hair, skin = "white", \
                eyes = "grey", personality = nora_personality, name_color = "#dddddd", dial_color = "#dddddd", starting_wardrobe = nora_wardrobe, \
                stat_array = [1,5,4], skill_array = [1,1,5,3,1], sex_skill_array = [3,2,4,1], sluttiness = 4, obedience = 102, happiness = 0, love = 3, \
                title = "Nora", possessive_title = "Your old boss", mc_title = mc.name, relationship = "Single", kids = 0, base_outfit = nora_base,
                work_experience = 4,type="story")

            nora.generate_home()
            nora.add_role(nora_role)
            nora.set_override_schedule(nora.home) #Sets her to stay at home so she doesn't wander around the city
            nora.change_job(nora_professor_job)
            nora.home.add_person(nora)
            #Add Job and Set override schedule so Nora doesn't become available until appropriate time
            nora.set_opinion("research work", 2, True) #Always loves research work


            reintro_event = Action("Nora cash reintro", nora_reintro_requirement, "nora_research_cash_intro", args = [nora, False])
            mc.business.mandatory_crises_list.append(reintro_event) #Reintro her if you don't take the option to visit her. Provides access to her special traits eventually.


        def setup_tutee():
            ### EMILY (18) ###
            emily_wardrobe = wardrobe_from_xml("Emily_Wardrobe")
            #original height = 0.91
            global emily
            emily_base = Outfit("Emily's accessories") #TODO: Decide on what her wardrobe should look like. Also decide on name colour
            emily = create_random_person(name = "Emily", last_name = "Vandenberg", age = 19, body_type = "thin_body", face_style = "Face_8", tits = "C", height = 0.915, hair_colour = "chestnut", hair_style = twintail, pubes_style = shaved_pubes, skin = "white", \
                eyes = "light blue", personality = relaxed_personality, starting_wardrobe = emily_wardrobe, stat_array = [3,2,1], skill_array = [2,1,1,1,2], sex_skill_array = [3,1,1,0], \
                sluttiness = 6, obedience = 100, happiness = 100, love = 0, relationship = "Single", kids = 0, base_outfit = emily_base,
                work_experience = 1,type="story")
            #Remember base Focus/Int so you get credit for any academic enhancing things you do (or punished for reducing them)
            emily.event_triggers_dict["initial_int"] = emily.int
            emily.event_triggers_dict["initial_focus"] = emily.focus
            emily.generate_home().add_person(emily)
            emily.change_job(emily_student_job)
            emily.set_schedule(emily.home, the_times = [0,1,2,3,4])
            emily.add_role(student_role)

        def setup_tutee_mother():
            ### CHRISTINA (EMILY'S MOM) ###
            christina_wardrobe = wardrobe_from_xml("Christina_Wardrobe")
            #original height = 0.94
            global christina
            christina_base = Outfit("Christina's accessories")
            christina_base.add_accessory(diamond_ring.get_copy())

            christina = create_random_person(name = "Christina", last_name = "Vandenberg", age = 47, body_type = "standard_body", face_style = "Face_8", tits = "DD", height = 0.96, hair_colour = "chestnut", hair_style = braided_bun, pubes_style = diamond_pubes, skin = "white", \
                eyes = "light blue", personality = reserved_personality, starting_wardrobe = christina_wardrobe, stat_array = [4,2,3], skill_array = [2,1,1,1,1], sex_skill_array = [2,3,3,2], \
                sluttiness = 10, obedience = 105, happiness = 85, love = 0, start_home = emily.home, relationship = "Married", kids = 1, base_outfit = christina_base,
                work_experience = 2,type="story")

            christina.set_schedule(christina.home) #She's a stay-at-home Mom.
            christina.home.add_person(christina)
            #Note: She plays an important role to Emily's story, but she is just given the normal affair role during the game.



        def setup_lily():
           ### LILY ###
            lily_wardrobe = wardrobe_from_xml("Lily_Wardrobe")
            #height = 0.90
            global lily
            lily = create_random_person(name = "Lily", last_name = mc.last_name, age = 19, body_type = "thin_body", face_style = "Face_6", tits = "B", height = 0.90, hair_colour="blond", hair_style = ponytail, skin="white", \
                eyes = "light blue", personality = lily_personality, name_color = "#FFB1F8", dial_color = "#FFB1F8", starting_wardrobe = lily_wardrobe, start_home = lily_bedroom, \
                stat_array = [5,2,2], skill_array = [2,2,0,1,1], sex_skill_array = [2,1,0,0], sluttiness = 8, obedience = 74, happiness = 122, love = 8, \
                title = "Lily", possessive_title = "Your sister", mc_title = mc.name, relationship = "Single", kids = 0,
                work_experience = 1,type="story")

            lily.add_role(sister_role)
            lily.change_job(sister_student_job)
            lily.set_schedule(lily.home, the_times = [0,3,4])

            sister_intro_crisis = Action("sister_intro_crisis", sister_intro_crisis_requirements, "sister_intro_crisis_label", args=lily, requirement_args = [lily, renpy.random.randint(7,14)]) #Def is in roles.rpy
            sister_strip_intro_crisis = Action("sister_strip_intro_crisis", sister_strip_intro_requirement, "sister_strip_intro_label", args=lily, requirement_args = lily)

            mc.business.mandatory_crises_list.append(sister_intro_crisis) #Introduces Lily one to two weeks into the game. She will test serum for cash.
            mc.business.mandatory_crises_list.append(sister_strip_intro_crisis) #Lily comes asking for more money. She will strip (to varying degrees) for cash)

            instathot_intro_action = Action("Instathot intro", instathot_intro_requirement, "sister_instathot_intro_label") #Event to introduce Lily taking pictures on the internet for money.
            lily.on_room_enter_event_list.append(instathot_intro_action)

            lily.home.add_person(lily)
            mc.phone.register_number(lily)

        def setup_mom():
            ### MOM ###
            mom_wardrobe = wardrobe_from_xml("Mom_Wardrobe")
            #original height = 0.94
            #adjusted height = 0.96
            global mom
            mom_base = Outfit("Jennifer's accessories")
            mom_base.add_accessory(diamond_ring.get_copy())
            mom = create_random_person(name = "Jennifer", last_name = mc.last_name, age = 42, body_type = "standard_body", face_style = "Face_1", tits = "DD", height = 0.96, hair_colour = "black", hair_style = long_hair, skin="white", \
                eyes = "brown", personality = mom_personality, name_color = "#8fff66", dial_color = "#8fff66", starting_wardrobe = mom_wardrobe, start_home = mom_bedroom, \
                stat_array = [3,2,4], skill_array = [5,2,0,0,2], sex_skill_array = [2,1,3,0], sluttiness = 7, obedience = 112, happiness = 108, love = 8, \
                title = "Mom", possessive_title = "Your mother", mc_title = "Sweetheart", relationship = "Single", kids = 2, base_outfit = mom_base,
                work_experience = 3,type="story")

            mom.add_role(mother_role)
            mom.change_job(mom_associate_job)
            mom.set_schedule(mom.home, the_times = [0,4])
            mom.set_schedule(kitchen, the_times = 3)

            mom_weekly_pay_action = Action("mom weekly pay", mom_weekly_pay_requirement, "mom_weekly_pay_label", args=mom, requirement_args =[mom])
            mc.business.mandatory_morning_crises_list.append(mom_weekly_pay_action)

            mom_promotion_one_crisis = Action("mom promotion one crisis", mom_work_promotion_one_requirement, "mom_work_promotion_one")
            mom.on_talk_event_list.append(mom_promotion_one_crisis)

            mom_find_serum_crisis = Action("mom find serum", mom_found_serums_requirement, "mom_found_serums", requirement_args = 3)
            mc.business.mandatory_morning_crises_list.append(mom_find_serum_crisis)


            mom.home.add_person(mom)
            mc.phone.register_number(mom)

        def setup_aunt():
            ### AUNT ###
            aunt_wardrobe = wardrobe_from_xml("Aunt_Wardrobe")
            #original height = 0.92
            global aunt
            aunt = create_random_person(name = "Rebecca", last_name = Person.get_random_last_name(), age = 39, body_type = "thin_body", face_style = "Face_1", tits = "DD", height = 0.93, hair_colour = "blond", hair_style = bobbed_hair, skin="white", \
                eyes = "brown", personality = aunt_personality, name_color = "#66FF8A", dial_color = "#66FF8A", starting_wardrobe = aunt_wardrobe, start_home = aunt_bedroom, \
                stat_array = [5,2,1], skill_array = [1,2,0,0,0], sex_skill_array = [3,5,3,2], sluttiness = 11, obedience = 100, happiness = 70, love = 5, \
                title = "Rebecca", possessive_title = "Your aunt", mc_title = mc.name, relationship = "Single", kids = 1,
                work_experience = 3,type="story")


            aunt.add_role(aunt_role) #Note that her "Hire" event is actually held by her aunt role, which just checks if she has the aunt_unemployed_job Job. Avoids needing a new Role just for her non-job.
            aunt.change_job(aunt_unemployed_job)
            aunt.set_schedule(aunt_bedroom) #Hide them in their bedroom off the map until they're ready.
            aunt.home.add_person(aunt)

            aunt_intro_action = Action("Aunt introduction", aunt_intro_requirement, "aunt_intro_label", requirement_args = renpy.random.randint(15,20))
            mc.business.mandatory_crises_list.append(aunt_intro_action) #Aunt and cousin will be visiting tomorrow in the morning

            family_games_night_intro_action = Action("Family games night intro", family_games_night_intro_requirement, "family_games_night_intro")
            aunt.on_room_enter_event_list.append(family_games_night_intro_action)


        def setup_cousin():
            ### COUSIN ###
            cousin_wardrobe = wardrobe_from_xml("Cousin_Wardrobe")

            global cousin
            cousin = create_random_person(name = "Gabrielle", last_name = aunt.last_name, age = 18, body_type = "curvy_body", face_style = "Face_3", tits = "DDD", height = 0.90, hair_colour = "black", hair_style = messy_short_hair, skin="white",\
                eyes = "brown", personality = cousin_personality, name_color = "#9c4dea", dial_color = "#9c4dea", starting_wardrobe = cousin_wardrobe, start_home = cousin_bedroom, \
                stat_array = [0,4,2], skill_array = [0,0,2,1,0], sex_skill_array = [3,0,0,0], sluttiness = 8, obedience = 70, happiness = 70, love = -20, \
                title = "Gabrielle", possessive_title = "Your cousin", mc_title = mc.name, relationship = "Single", kids = 0,type="story")

            cousin.add_role(cousin_role)
            cousin.change_job(unemployed_job)
            cousin.set_schedule(cousin_bedroom) #Hide them in their bedroom off the map until they're ready
            cousin.home.add_person(cousin)


        def setup_alexia():
            ### ALEXIA ###
            alexia_wardrobe = wardrobe_from_xml("Alexia_Wardrobe")
            #original height = 0.92
            global alexia
            alexia_base = Outfit("Alexia's accessories")
            alexia_glasses = big_glasses.get_copy()
            big_glasses.colour = [0.1,0.1,0.1,1.0]
            alexia_base.add_accessory(alexia_glasses)
            alexia = create_random_person(name = "Alexia", age = 21, body_type = "thin_body", face_style = "Face_2", tits = "C", height = 0.93, hair_colour = "blond", hair_style = short_hair, skin="white",\
                eyes = "brown", personality = alexia_personality, name_color = "#ffff6e", dial_color = "#ffff6e", starting_wardrobe = alexia_wardrobe, \
                stat_array = [4,3,3], skill_array = [1,3,2,1,1], sex_skill_array = [2,2,1,0], sluttiness = 3, obedience = 100, happiness = 102, love = 3, \
                title = "Alexia", possessive_title = "Your old classmate",mc_title = mc.name, relationship = "Girlfriend", SO_name = Person.get_random_male_name(), kids = 0, base_outfit = alexia_base,
                work_experience = 2,type="story")
            alexia.generate_home()

            alexia_intro_phase_zero_action = Action("Alexia Set Schedule", alexia_intro_phase_zero_requirement, "alexia_phase_zero_label", requirement_args = renpy.random.randint(14, 21))
            mc.business.mandatory_crises_list.append(alexia_intro_phase_zero_action)

            alexia_intro_phase_one_action = Action("Alexia Intro Phase One", alexia_intro_phase_one_requirement, "alexia_intro_phase_one_label")
            alexia.on_room_enter_event_list.append(alexia_intro_phase_one_action)

            alexia.add_role(alexia_role)
            alexia.change_job(alexia_barista_job)

            alexia.home.add_person(alexia)
            alexia.set_override_schedule(alexia.home) #Hide them in their bedroom off the map until they're ready / #Stay at hom until we clear this.
            alexia.set_opinion("marketing work", 2, False) #loves marketing work, but you don't now that right away.

        def setup_lily_rival():
            ### IRIS ###
            #iris_wardrobe = wardrobe_from_xml("Iris_Wardrobe")
            iris_base = Outfit("Iris's accessories") #TODO: Decide what accessories we want her to haven

            global iris
            iris = create_random_person(name = "Iris", age = 18, body_type = "thin_body", face_style = "Face_7", tits = "DD", height = 0.9, hair_colour = "blond", hair_style = twintail, pubes_style = shaved_pubes, skin = "white", \
                eyes = "green", personality = relaxed_personality, stat_array = [6,2,1], skill_array = [1,4,0,0,1], sex_skill_array = [4,4,0,0], \
                sluttiness = 5, obedience = 80, happiness = 120, love = 0, relationship = "Single", kids = 0,
                work_experience = 1)

            iris.add_role(instapic_role)
            iris.add_role(dikdok_role)
            #iris.change_job(influencer_job)
            iris.change_job(unemployed_job)

            iris.generate_home()
            iris.set_override_schedule(iris.home) #Hides her at home so she doesn't wander the city by accident.
            #iris.home.add_person(iris) #NOTE: We don't put her on the map yet, so her stats will be as intended when you first meet her and she is added to the electronics store location.


        def setup_university_characters():
            #Lab
            setup_stephanie()
            setup_nora()
            town_relationships.update_relationship(nora, stephanie, "Friend")

            #Tutee Storyline
            setup_tutee()
            setup_tutee_mother()
            town_relationships.update_relationship(christina, emily, "Daughter", "Mother")

        def setup_family_characters():


            #Home
            setup_lily()
            setup_mom()
            town_relationships.update_relationship(mom,lily, "Daughter", "Mother")

            #Aunt's Family
            setup_aunt()
            town_relationships.update_relationship(mom,aunt, "Sister")
            town_relationships.update_relationship(aunt, lily, "Niece", "Aunt")
            setup_cousin()
            town_relationships.update_relationship(mom, cousin, "Niece", "Aunt")
            town_relationships.update_relationship(aunt, cousin, "Daughter", "Mother")
            town_relationships.update_relationship(lily, cousin, "Cousin")




        def setup_city_rep():
            ### ??? ###
            city_rep_wardrobe = wardrobe_from_xml("City_Rep_Wardrobe")
            city_rep_base = city_rep_wardrobe.get_outfit_with_name("City_Rep_Accessories")
            #original height = 0.98
            global city_rep
            city_rep = create_random_person(age = 34, body_type = "thin_body", face_style = "Face_9", tits = "D", height = 1.02, hair_colour = "black", hair_style = ponytail, pubes_style = trimmed_pubes, skin = "white", \
                starting_wardrobe = city_rep_wardrobe, base_outfit = city_rep_base, \
                personality = introvert_personality, stat_array = [1,4,4], skill_array = [5,0,0,0,2], sex_skill_array = [1,4,3,0], \
                sluttiness = 0, obedience = 80, happiness = 100, love = -20,
                work_experience = 4,type="story")

            city_rep.add_role(city_rep_role)
            city_rep.change_job(city_rep_job)
            city_rep.generate_home().add_person(city_rep)
            city_rep.set_schedule(city_rep.home)

            city_rep.set_title("???")
            city_rep.set_mc_title("Mr."+mc.last_name)
            city_rep.set_possessive_title("???")




        def setup_storyline_characters():

            setup_university_characters()
            setup_family_characters()

            setup_alexia()

            setup_lily_rival()

            setup_city_rep()


        def generate_premade_list():
            global list_of_premade_characters
            list_of_premade_characters = []
            list_of_premade_characters.append(create_random_person(body_type = "curvy_body", height=1.035, skin="tan", tits="DD",hair_colour="chestnut",hair_style=messy_hair,type="premade")) #original height = 0.99
            list_of_premade_characters.append(create_random_person(body_type = "thin_body", height=1.05, skin="white", tits="B",hair_colour="chestnut",hair_style=messy_hair,type="premade")) #original_height = 1
            list_of_premade_characters.append(create_random_person(body_type = "curvy_body", height=0.99, skin="white", tits="DD",hair_colour="brown",hair_style=twintail,type="premade")) #original height = 0.96
            list_of_premade_characters.append(create_random_person(body_type = "standard_body", height=0.99, skin="white", tits="DD", hair_colour="chestnut",hair_style=messy_hair,type="premade")) #original height = 0.96
            list_of_premade_characters.append(create_random_person(body_type = "thin_body", height=0.93, skin="tan", tits="B", hair_colour="black", hair_style=ponytail,type="premade")) #original height = 0.92
            list_of_premade_characters.append(create_random_person(body_type = "standard_body", height=0.90, skin="white", tits="DD", hair_colour="blond", hair_style=messy_hair,type="premade")) #original height = 0.9
            list_of_premade_characters.append(create_random_person(body_type = "curvy_body", height=1.05, skin="white", tits="DD", hair_colour="chestnut", hair_style=messy_hair,type="premade")) #original height = 1.0
            list_of_premade_characters.append(create_random_person(body_type = "thin_body", height=0.96, skin="white", tits="FF", hair_colour="blond", hair_style=long_hair,type="premade")) #oriignal_height = 0.94
            list_of_premade_characters.append(create_random_person(body_type = "standard_body", height=0.975, skin="tan", tits="FF", hair_colour="brown", hair_style=ponytail,type="premade")) #original height = 0.95


        def generate_unique_characters_list():
            global list_of_unique_characters
            # Patron reward characters! #
            list_of_unique_characters = []

            #original height 0.99
            dinah_wardrobe = wardrobe_from_xml("Dinah_Wardrobe")
            person_dinah = create_random_person(name = "Dinah", last_name = "Midari", body_type = "standard_body", height=1.035, skin="black", tits="D", hair_colour="black", hair_style=short_hair, starting_wardrobe = dinah_wardrobe,type="unique")
            list_of_unique_characters.append(person_dinah)

            #original height 0.96
            sylvia_wardrobe = wardrobe_from_xml("Sylvia_Wardrobe")
            person_sylvia = create_random_person(name = "Sylvia", last_name = "Weissfeldt", body_type = "curvy_body", height=0.99, skin="white", tits="C", hair_colour="blond", hair_style = long_hair, starting_wardrobe = sylvia_wardrobe,
                personality = reserved_personality,type="unique")
            list_of_unique_characters.append(person_sylvia)

            #origianl height 0.98
            paige_wardrobe = wardrobe_from_xml("Paige_Wardrobe")
            # Well educated and raised in a very middle-class family.
            # Paige is a cool-headed young woman who has confidence without exuberance or extraversion.
            # her favourite activities are generally calm and solitary: reading, playing musical instruments, watching TV, etc.
            # She doesn't make friends quickly, but she is pleasant and easy to get along with, and the bonds she does cultivate are likely to last for life.
            # She has no passion for her work, but she is good at it and takes pride in that fact.
            person_paige = create_random_person(name = "Paige", last_name = "Sallow", body_type = "thin_body", height = 1.02, skin = "white", tits="A", hair_colour="brown", hair_style = messy_ponytail, starting_wardrobe = paige_wardrobe,
                personality = reserved_personality, stat_array = [1,4,3], skill_array = [5,1,2,3,2], sex_skill_array = [2,1,4,2],type="unique")
            list_of_unique_characters.append(person_paige)

            #original height 0.94
            kendra_wardrobe = wardrobe_from_xml("Kendra_Wardrobe")
            # Kendra's family owns one of the largest pharmaceutical companies in the country. All of the Rivera children went to the finest prep schools.
            # Unlike her siblings, Kendra didn't inherit her parent's good looks or their general attitudes. She also disagreed with her families' viewpoint that being rich makes you better than everyone else.
            # This point of view put her at odds with everyone in her social class so she mostly hung out with the outcasts of her school.
            # By the time Kendra turned 16, she had grown into a stunningly beautiful woman and enjoyed the newfound attention she was receiving from boys. She was a free spirit, who just wanted to enjoy life.
            # When she graduated High School, she decided that college was not for her and pursued a career as glamor model. Kendra's parents were not pleased and cut her off financially but Kendra didn't care.
            # She was ready to be free and live her life.
            person_kendra = create_random_person(name = "Kendra", last_name = "Rivera", age = 18, body_type = "curvy_body", height = 0.96, skin = "tan", hair_colour = "chestnut", hair_style = shaved_side_hair, starting_wardrobe = kendra_wardrobe,
                personality = relaxed_personality, stat_array = [4,3,1], skill_array = [5,3,1,2,2], sex_skill_array = [2,2,4,1], face_style = "Face_4",type="unique")
            list_of_unique_characters.append(person_kendra)

            #original height 1.00
            svetlanna_wardrobe = wardrobe_from_xml("Svetlanna_Wardrobe")
            # Svetlanna moved to the fictional city from a fictional Russian land at the age of 16. She was always fascinated with biochemistry and when her mother became ill, she dove even deeper into her studies.
            # After graduating from public education, she immediately moved to higher studies. She was hell-bent to learn all she could to help her mother.
            # Unfortunately, her mother died before Svetlanna could find a cure for her mysterious disease, which put her into a deep depression.
            # After some time, she met a woman that rekindled her love for biotechnology and put her on the path of a wild woman, never tied down with any one man or woman.
            person_svetlanna = create_random_person(name = "Svetlanna", last_name = "Ivanova", body_type= "thin_body", height = 1.05, skin = "white", tits="E", hair_colour = "blond", hair_style = long_hair, starting_wardrobe = svetlanna_wardrobe,
                personality = wild_personality, stat_array = [3,1,4], skill_array = [1,3,5,2,2], sex_skill_array = [2,1,2,4],type="unique")
            person_svetlanna.set_opinion("research work", 2, False) #Always loves research work # Patron reward
            list_of_unique_characters.append(person_svetlanna)

            #original height 0.98
            kelly_wardrobe = wardrobe_from_xml("Kelly_Wardrobe")
            #
            person_kelly = create_random_person(name = "Kelly", last_name = "Uhls", body_type = "curvy_body", height = 1.02, skin = "white", eyes = "dark blue", tits = "E", hair_colour = "chestnut", hair_style = ponytail, starting_wardrobe = kelly_wardrobe,
                personality = reserved_personality, stat_array = [2,2,4], skill_array = [2,1,2,1,5], sex_skill_array = [3,4,2,1],type="unique")
            list_of_unique_characters.append(person_kelly)

            #original height 0.90
            #sativa_wardrobe = wardrobe_from_xml("Sativa_Wardrobe") #TODO: Give her a wardrobe if the patron responds
            # Sativa's parents are very strict and traditional. They were determined to protect her from all the bad things in life, such as boys and booze.
            #When she turned 18,  Sativa moved out on her own.  Now she is determined to experience everything that she was previously denied.
            person_sativa = create_random_person(name = "Sativa", last_name = "Menendez", body_type = "curvy_body", face_style = "Face_7", height = 0.90, skin = "tan", eyes = "green", tits = "FF", hair_colour = "black", hair_style = bobbed_hair,
                personality = wild_personality, stat_array = [3,1,4], skill_array = [2,2,1,1,5], sex_skill_array = [4,3,2,1],type="unique")
            list_of_unique_characters.append(person_sativa)

            #original height 0.96
            #nuoyi_wardrobe = wardrobe_from_xml("Nuoyi_Wardrobe") #NOTE: Patron did not want a specific wardrobe, she'll draw her wardrobe randomly as normal.
            person_nuyoi = create_random_person(name = "Nuoyi", last_name = "Pan", body_type = "thin_body", height = 0.99, skin = "white", eyes = "dark blue", tits = "FF", hair_colour = "black", hair_style = long_hair,
                personality = wild_personality, stat_array = [4,3,1], skill_array = [5,2,2,1,1], sex_skill_array = [1,3,4,2],type="unique")
            list_of_unique_characters.append(person_nuyoi)

            #original height 0.94
            lynn_wardrobe = wardrobe_from_xml("Lynn_Wardrobe")
            # An exchange student who is doing a year abroad at a Catholic school. Especially to get away from her helicopter parents.
            person_lynn = create_random_person(name = "Lynn", last_name = "Borch", body_type = "thin_body", height = 0.96, age = 19, skin = "white", eyes = "brown", tits = "C", hair_colour = "brown", hair_style = long_hair, starting_wardrobe = lynn_wardrobe,
                personality = introvert_personality, stat_array = [1,3,4], skill_array = [1,2,1,5,2], sex_skill_array = [2,1,5,1],type="unique")
            person_lynn.set_opinion("cheating on men", -2, False) #Always hates cheating on men, you don't know this
            list_of_unique_characters.append(person_lynn)

            #original height 0.95
            # Olga is a young library employee who likes to dress colorfully and is childish by behavior.
            # As if she wants to overplay something.
            olga_wardrobe = wardrobe_from_xml("Olga_Wardrobe")
            person_olga = create_random_person(name = "Olga", last_name = "Schaad", body_type = "standard_body", height = 0.975, skin = "tan", eyes = "green", tits = "E", hair_colour = "blond", hair_style = messy_ponytail, starting_wardrobe = olga_wardrobe,
                personality = wild_personality, stat_array = [4,1,3], skill_array = [2,5,2,1,1], sex_skill_array = [2,4,1,1],type="unique")
            person_olga.set_opinion("working", 1, False) #Always likes working, you don't know this
            list_of_unique_characters.append(person_olga)

            #original height 0.92
            # Svenja wants to become a fashion designer; she dropped out of college to do so and started working in a fashion boutique. She is 18 years old.
            # svenja_wardrobe = wardrobe_from_xml("Svenja_Wardrobe") #NOTE: Patron did not want a specific wardrobe, she'll draw her wardrobe randomly as normal.
            person_svenja = create_random_person(name = "Svenja", last_name = "Beitel",  body_type = "standard_body", height = 0.93, skin = "white", eyes = "dark blue", tits = "B", hair_colour = "blond", hair_style = ponytail,
                personality = wild_personality, stat_array = [3,1,4], skill_array = [1,3,1,5,1], sex_skill_array = [3,4,1,1], type="unique")
            list_of_unique_characters.append(person_svenja)

            # anna_wardrobe = wardrobe_from_xml("Anna_Wardrobe") #NOTE: Patron did not provide a specific wardrobe; she'll draw from the default pool.
            person_anna = create_random_person(name = "Anna", last_name = "Kostenko", body_type = "thin_body", height = 0.93, skin = "white", eyes = "light blue", tits = "A", hair_colour = "blond", hair_style = ponytail,
                personality = introvert_personality, stat_array = [1,3,4], skill_array = [1,1,3,3,5], sex_skill_array = [1,3,4,1], type = "unique")
            list_of_unique_characters.append(person_anna)



        def create_random_stripper():
            a_stripper = create_random_person(sluttiness = renpy.random.randint(15,30), job = stripper_job)
            a_stripper.generate_home()
            strip_club.add_person(a_stripper)
            return a_stripper
