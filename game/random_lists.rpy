init -2:
    python:

        def VrenNullAction(): #For some reason the NullAction still returns None, so it still transitions screens.
            pass

        def get_random_from_list(list):
            if len(list) > 0:
                return list[renpy.random.randint(0,len(list)-1)]
            else:
                return None

        def get_random_from_weighted_list(list, return_everything = False): #Passed a list of parameters which are ["Thing", weighted value, anything_else,...]
            #If return_everything is True, returns the entire tuple instead of just an action
            if len(list) == 0:
                return None

            total_value = 0
            for item in list:
                total_value += item[1] #Get the total weighting value that we use to determine what thing we've picked.

            random_value = renpy.random.randint(0,total_value) #Gets us a value somewhere inside of our probability space.
            running_total = 0
            for item in list:
                if random_value <= (item[1]+running_total):
                    if return_everything:
                        return item
                    else:
                        return item[0]
                else:
                    running_total += item[1]

        def is_in_weighted_list(test_item,list):
            for item in list:
                if test_item == item[0]:
                    return True
            return False

        def index_in_weighted_list(test_item,list):
            for item in list:
                if test_item == item[0]:
                    return list.index(item)
            raise ValueError("{!r} is not in weighted list".format(test_item))

        def get_random_job(): #TODO: Replace this with a more directed fucntion that distributes jobs based on stats.
            return get_random_from_list(list_of_jobs)
                        



        technobabble_list = []
        technobabble_list.append("optimize the electromagnetic pathways")
        technobabble_list.append("correct for the nanowave signature")
        technobabble_list.append("de-scramble the thermal injector")
        technobabble_list.append("crosslink the long chain polycarbons")
        technobabble_list.append("carbonate the ethyl groups")
        technobabble_list.append("oxdize the functional group")
        technobabble_list.append("resynchronize the autosequencers")
        technobabble_list.append("invert the final power spike")
        technobabble_list.append("kickstart the process a half second early")
        technobabble_list.append("stall the process by a half second")
        technobabble_list.append("apply a small machine learning algorithm")
        technobabble_list.append("hit the thing in just the right spot")
        technobabble_list.append("wait patiently for it to finish")





        font_list = []
        font_list.append("fonts/Avara.ttf")
        font_list.append("fonts/GlacialIndifference-Regular.otf")
        font_list.append("fonts/FantasqueSansMono-Regular.ttf")
        font_list.append("fonts/TruenoRg.otf")
        font_list.append("fonts/TruenoBd.otf")
        font_list.append("fonts/Crimson-Roman.ttf")
        font_list.append("fonts/Crimson-Bold.ttf")
        font_list.append("fonts/HKVenetian-Regular.otf")
        font_list.append("fonts/HKVenetian-Italic.otf")
        font_list.append("fonts/AAntiCorona-L3Ax3.ttf")



        def get_random_font():
            return get_random_from_list(font_list)


        #https://snook.ca/technical/colour_contrast/colour.html A good site to generate colour contrast examples to make sure thigns are readable. Our text background is roughly #3459d2
        readable_color_list = [] #Colors that are easily readable on our blue background.
        readable_color_list.append("#ffffff") #White
        readable_color_list.append("#dddddd") #Grey
        readable_color_list.append("#ffff6e") #Yellow
        readable_color_list.append("#8fff66") #Green
        readable_color_list.append("#cf3232") #Red
        readable_color_list.append("#ffd4d4") #Pink
        readable_color_list.append("#FFB1F8") #Hotpink
        readable_color_list.append("#73ffdf") #Teal
        readable_color_list.append("#d62cff") #Purple
        readable_color_list.append("#87cefa") #Light Blue (Replaces pure blue)


        def get_random_readable_color():
            return get_random_from_list(readable_color_list)


        def format_group_of_people(list_of_people): # Returns a string made up of people titles like "PersonA, PersonB, and PersonC." or just "PersonA and PersonB" if there are two people. (or PersonA if it's just one person)
            #Note: the list is formatted in the order it is handed over. renpy.random.scramble() it beforehand if you want it in a random order.
            return_string = ""
            if len(list_of_people) == 1:
                return_string += list_of_people[0].title
            elif len(list_of_people) == 2:
                return_string += list_of_people[0].title + " and " + list_of_people[1].title
            else:
                for a_person in list_of_people:
                    if a_person is not list_of_people[-1]: #If they're not the last person:
                        return_string += a_person.title + ", "
                    else:
                        return_string += "and " + a_person.title

            #TODO: Add a varient of this that lets you set a max number of people. A kind of "blah, blah, blah, and 7 more people..." response.
            return return_string

        def format_list_of_clothing(the_list): # Takes a list of strings and formats them to the form "ThingA, thingB, and ThingC"
            return_string = ""
            if len(the_list) == 1:
                return_string = the_list[0].display_name
            elif len(the_list) ==2:
                return_string = the_list[0].display_name + " and " + the_list[1].display_name
            else:
                for an_item in the_list:
                    if an_item is the_list[-1]:
                        return_string += "and " + an_item.display_name
                    else:
                        return_string += an_item.display_name + ", "
            return return_string



init 1 python:
    def character_meets_requirements(character,requirements_dict = None):
        if requirements_dict == None:
            return True
        
        age_range = requirements_dict.get("age_range")
        if age_range is not None and not (age_range[0] <= character.age <= age_range[1]):
            return False

        height_range = requirements_dict.get("height_range")
        if height_range is not None and not (height_range[0] <= character.height <= height_range[1]):
            return False
         
        stat_range_array = requirements_dict.get("stat_range_array")
        if stat_range_array is not None:
            if not (stat_range_array[0][0] <= character.charisma <= stat_range_array[0][1]):
                return False

            if not (stat_range_array[1][0] <= character.int <= stat_range_array[1][1]):
                return False

            if not (stat_range_array[2][0] <= character.focus <= stat_range_array[2][1]):
                return False

        skill_range_array = requirements_dict.get("skill_range_array")
        if skill_range_array is not None:
            if not (skill_range_array[0][0] <= character.hr_skill <= skill_range_array[0][1]):
                return False

            if not (skill_range_array[1][0] <= character.market_skill <= skill_range_array[1][1]):
                return False

            if not (skill_range_array[2][0] <= character.research_skill <= skill_range_array[2][1]):
                return False

            if not (skill_range_array[3][0] <= character.production_skill <= skill_range_array[3][1]):
                return False

            if not (skill_range_array[4][0] <= character.supply_skill <= skill_range_array[4][1]):
                return False

        sex_skill_range_array = requirements_dict.get("sex_skill_range_array")
        if sex_skill_range_array is not None:
            if not (sex_skill_range_array[0][0] <= character.sex_skills["Foreplay"] <= sex_skill_range_array[0][1]):
                return False

            if not (sex_skill_range_array[1][0] <= character.sex_skills["Oral"] <= sex_skill_range_array[1][1]):
                return False

            if not (sex_skill_range_array[2][0] <= character.sex_skills["Vaginal"] <= sex_skill_range_array[2][1]):
                return False

            if not (sex_skill_range_array[3][0] <= character.sex_skills["Anal"] <= sex_skill_range_array[3][1]):
                return False

        happiness_range = requirements_dict.get("happiness_range")
        if happiness_range is not None and not (happiness_range[0] <= character.happiness <= happiness_range[1]):
            return False

        suggestibility_range = requirements_dict.get("suggestibility_range")
        if suggestibility_range is not None and not (suggestibility_range[0] <= character.suggestibility <= suggestibility_range[1]):
            return False

        sluttiness_range = requirements_dict.get("sluttiness_range")
        if sluttiness_range is not None and not (sluttiness_range[0] <= character.sluttiness <= sluttiness_range[1]):
            return False

        love_range = requirements_dict.get("love_range")
        if love_range is not None and not (love_range[0] <= character.love <= love_range[1]):
            return False

        obedience_range = requirements_dict.get("obedience_range")
        if obedience_range is not None and not (obedience_range[0] <= character.obedience <= obedience_range[1]):
            return False

        tits_range = requirements_dict.get("tits_range")
        if tits_range is not None:
            if not is_in_weighted_list(character.tits,tits_range):
                return False

        relationship_list = requirements_dict.get("relationship_list")
        if relationship_list is not None:
            if not is_in_weighted_list(character.relationship,relationship_list):
                return False

        kids_range = requirements_dict.get("kids_range")[:] #Copy because we're going to alter this depending on the test characters age
        if kids_range is not None:
            kids_range = character.finalize_kids_range(kids_range,age_range,relationship_list,character.age,character.relationship)
            if not (kids_range[0] <= character.kids <= kids_range [1]):
                return False

        kids_floor = requirements_dict.get("kids_floor")
        if kids_floor is not None:
            if character.kids < kids_floor:
                return False

        kids_ceiling = requirements_dict.get("kids_ceiling")
        if kids_ceiling is not None:
            if character.kids > kids_ceiling:
                return False

        return True

    def get_premade_character(requirement_dict = None): #Get a premade character and return them when the function is called.
        filtered_list_of_unique_characters = [character for character in list_of_unique_characters if character_meets_requirements(character,requirement_dict)]
        person = get_random_from_list(filtered_list_of_unique_characters)
        if person is not None:
            list_of_unique_characters.remove(person)
            return person

        filtered_list_of_premade_characters = [character for character in list_of_premade_characters if character_meets_requirements(character,requirement_dict)]
        person = get_random_from_list(filtered_list_of_premade_characters)
        if person is not None:
            list_of_premade_characters.remove(person)
        return person
