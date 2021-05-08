init -2 python:
    #How the character responds to various actions
    class Personality():
        def __init__(self, personality_type_prefix, default_prefix = None,
            common_likes = None, common_dislikes = None, common_sexy_likes = None, common_sexy_dislikes = None,
            titles_function = None, possessive_titles_function = None, player_titles_function = None,
            insta_chance = 0, dikdok_chance = 0):

            self.personality_type_prefix = personality_type_prefix
            self.default_prefix = default_prefix

            self.titles_function = titles_function
            self.possessive_titles_function = possessive_titles_function
            self.player_titles_function = player_titles_function

            self.insta_chance = insta_chance
            self.dikdok_chance = dikdok_chance
            #NOTE: Girls never generate with Onlyfans naturally

            #These are the labels we will be trying to get our dialogue. If the labels do not exist we will get their defaults instead. A default should _always_ exist, if it does not our debug check will produce an error.
            self.response_label_ending = ["greetings",
            "sex_responses_foreplay", "sex_responses_oral", "sex_responses_vaginal", "sex_responses_anal",
            "climax_responses_foreplay", "climax_responses_oral", "climax_responses_vaginal", "climax_responses_anal",
            "clothing_accept", "clothing_reject", "clothing_review",
            "strip_reject", "strip_obedience_accept", "grope_body_reject", "sex_accept", "sex_obedience_accept", "sex_gentle_reject", "sex_angry_reject",
            "seduction_response", "seduction_accept_crowded", "seduction_accept_alone", "seduction_refuse",
            "flirt_response", "flirt_response_low", "flirt_response_mid", "flirt_response_high", "flirt_response_girlfriend", "flirt_response_affair", "flirt_response_text",
            "condom_demand", "condom_ask", "condom_bareback_ask", "condom_bareback_demand",
            "cum_face", "cum_mouth", "cum_pullout", "cum_condom", "cum_vagina", "cum_anal", "surprised_exclaim", "talk_busy",
            "improved_serum_unlock", "sex_strip", "sex_watch", "being_watched", "work_enter_greeting", "date_seduction", "sex_end_early", "sex_take_control", "sex_beg_finish", "sex_review" ,"introduction",
            "kissing_taboo_break", "touching_body_taboo_break", "touching_penis_taboo_break", "touching_vagina_taboo_break", "sucking_cock_taboo_break", "licking_pussy_taboo_break", "vaginal_sex_taboo_break", "anal_sex_taboo_break",
            "condomless_sex_taboo_break", "underwear_nudity_taboo_break", "bare_tits_taboo_break", "bare_pussy_taboo_break",
            "facial_cum_taboo_break", "mouth_cum_taboo_break", "body_cum_taboo_break", "creampie_taboo_break", "anal_creampie_taboo_break"]

            self.response_dict = {}
            for ending in self.response_label_ending:
                if renpy.has_label(self.personality_type_prefix + "_" + ending):
                    self.response_dict[ending] = self.personality_type_prefix + "_" + ending
                elif default_prefix is not None: #A default is used when one personality is similar to anouther and has only specific responses overwritten (ex. Stephanie is a modified wild personality).
                    self.response_dict[ending] = self.default_prefix + "_" + ending
                else:
                    self.response_dict[ending] = "relaxed_" + ending #If nothing is given we assume we don't want to crash and we should put in some sort of value.



            #Establish our four classes of favoured likes and dislikes. Intensity (ie. love vs like, dislike vs hate) is decided on a person to person basis.
            if common_likes:
                self.common_likes = common_likes
            else:
                self.common_likes = []

            if common_sexy_likes:
                self.common_sexy_likes = common_sexy_likes
            else:
                self.common_sexy_likes = []

            if common_dislikes:
                self.common_dislikes = common_dislikes
            else:
                self.common_dislikes = []

            if common_sexy_dislikes:
                self.common_sexy_dislikes = common_sexy_dislikes
            else:
                self.common_sexy_dislikes = []

        def get_dialogue(self, the_person, type, **extra_args):
            renpy.call(self.response_dict[type], the_person, **extra_args)
            return

        def generate_default_opinion(self):
            if renpy.random.randint(1,2) == 1:
                #Positive
                degree = renpy.random.randint(1,2)
                the_key = get_random_from_list(self.common_likes)
                return (the_key,[degree,False])

            else:
                #Negative
                degree = renpy.random.randint(-2,-1)
                the_key = get_random_from_list(self.common_dislikes)
                return (the_key,[degree,False])


        def generate_default_sexy_opinion(self):
            if renpy.random.randint(1,2) == 1:
                #Positive
                degree = renpy.random.randint(1,2)
                the_key = get_random_from_list(self.common_sexy_likes)
                return (the_key,[degree,False])

            else:
                #Negative
                degree = renpy.random.randint(-2,-1)
                the_key = get_random_from_list(self.common_sexy_dislikes)
                return (the_key,[degree,False])

        def get_personality_titles(self, the_person): #This should be a function defined for each
            if self.titles_function:
                return self.titles_function(the_person)
            else:
                return the_person.name

        def get_personality_possessive_titles(self, the_person):
            if self.possessive_titles_function:
                return self.possessive_titles_function(the_person)
            else:
                return the_person.name

        def get_personality_player_titles(self, the_person):
            if self.player_titles_function:
                return self.player_titles_function(the_person)
            else:
                return mc.name
