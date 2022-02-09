init -2 python:
    class Person(renpy.store.object): #Everything that needs to be known about a person.
        global_character_number = 0 #This is increased for each character that is created.
        def __init__(self,name,last_name,age,body_type,tits,height,body_images,expression_images,hair_colour,hair_style,pubes_colour,pubes_style,skin,eyes,job,wardrobe,personality,stat_list,skill_list,
            sluttiness=0,obedience=0,suggest=0,sex_list=[0,0,0,0], love = 0, happiness = 100, home = None,
            font = "fonts/Avara.tff", name_color = "#ffffff", dialogue_color = "#ffffff",
            face_style = "Face_1",
            special_role = None,
            title = None, possessive_title = None, mc_title = None,
            relationship = None, SO_name = None, kids = None, base_outfit = None,
            generate_insta = False, generate_dikdok = False, generate_onlyfans = False):

            ## Personality stuff, name, ect. Non-physical stuff.
            self.name = name
            self.last_name = last_name
            self.character_number = Person.global_character_number #This is a gunique number for each character. Used as a tag when showing a character to identify if they are already drawn (and thus need to be hidden)
            Person.global_character_number += 1

            self.event_triggers_dict = {} #A dict used to store extra parameters used by events, like how many days has it been since a performance review.

            self.title = title #Note: We format these down below!
            self.possessive_title = possessive_title #The way the girl is refered to in relation to you. For example "your sister", "your head researcher", or just their title again.
            if mc_title:
                self.mc_title = mc_title #What they call the main character. Ie. "first name", "mr.last name", "master", "sir".
            else:
                self.mc_title = "Stranger"

            self.home = home #The room the character goes to at night. If none a random public location is picked.

            self.schedule = Schedule()

            self.override_schedule = Schedule() #The mandatory place a person will go EVEN if they have work (useful for giving days off or requiring weekend work)



            # Relationship and family stuff
            if relationship:
                self.relationship = relationship
            else:
                self.relationship = "Single" #Should be Single, Girlfriend, Fiancée, or Married.

            if SO_name:
                self.SO_name = SO_name
            else:
                self.SO_name = None #If not single, name of their SO (for guilt purposes or future events).

            if kids:
                self.kids = kids
            else:
                self.kids = 0


            self.personality = personality


            # Loves, likes, dislikes, and hates determine some reactions in conversations, options, etc. Some are just fluff.
            self.opinions = {} #Key is the name of the opinion (see random list), value is a list holding [value, known]. Value ranges from -2 to 2 going from hate to love (things not on the list are assumed 0). Known is a bool saying if the player knows about their opinion.

            self.sexy_opinions = {}
            # We establish random opinions first and will overwrite any that conflict with generated personality opinions.
            for x in __builtin__.range(1,5):
                the_opinion_key = get_random_opinion()
                degree = renpy.random.randint(-2,2)
                if not degree == 0: #ie. ignore 0 value opinions.
                    self.opinions[the_opinion_key] = [degree, False]

            for x in __builtin__.range(1,2):
                the_opinion_key = get_random_sexy_opinion()
                degree = renpy.random.randint(-2,2)
                if not degree == 0: #ie. ignore 0 value opinions.
                    self.sexy_opinions[the_opinion_key] = [degree, False]

            #Now we get our more likely default personality ones.
            for x in __builtin__.range(1,4):
                the_opinion_key, opinion_list = self.personality.generate_default_opinion()
                if the_opinion_key:
                    self.opinions[the_opinion_key] = opinion_list

            for x in __builtin__.range(1,3):
                the_opinion_key, opinion_list = self.personality.generate_default_sexy_opinion()
                if the_opinion_key:
                    self.sexy_opinions[the_opinion_key] = opinion_list



            #TODO: Relationship with other people (List of known people plus relationship with them.)

            #Using char instead of a string lets us customize the font and colour we are using for the character.
            self.char = Character("???", #The name to be displayed above the dialogue.
                what_font = font, #The font to be used for the character.
                who_font = font,
                color = name_color, #The colour of the character's NAME section
                what_color = dialogue_color, #The colour of the character's dialogue.
                what_style = "general_dialogue_style") #Used to describe everything that isn't character specific.

            self.what_font = font
            self.who_font = font
            self.what_color = dialogue_color

            if title: #Format the given titles, if any, so they appear correctly the first time you meet at person.
                self.set_title(title) #The way the girl is refered to by the MC. For example: "Mrs. Whatever", "Lily", or "Mom". Will reset "???" if appropriate
            else:
                self.char.name = self.create_formatted_title("???")
            if possessive_title:
                self.set_possessive_title(possessive_title)

            self.text_modifiers = [] #A list of functions, each of which take Person, String and return a modified String. Used to modify text to dynamically highlight words, or reflect a speech difference.

            ## Physical things.
            self.age = age
            self.body_type = body_type
            self.tits = tits
            self.height = height * 0.8 #This is the scale factor for height, with the talest girl being 0.8 and the shortest being 0.64
            self.body_images = body_images.get_copy() #instance of Clothing class, which uses full body shots.
            self.face_style = face_style
            self.expression_images = expression_images #instance of the Expression class, which stores facial expressions for different skin colours

            self.pubes_colour = None

            self.hair_style = hair_style
            if pubes_style is None:
                self.pubes_style = shaved_pubes #An empty image place holder so we can always call on them to draw.
            else:
                self.pubes_style = pubes_style

            self.set_hair_colour(Color(rgb=(hair_colour[1][0],hair_colour[1][1],hair_colour[1][2])))


            self.skin = skin
            self.set_eye_colour(Color(rgb=(eyes[1][0], eyes[1][1], eyes[1][2])))
            # self.eyes = eyes #A list of [description, color value], where colour value is a standard RGBA list.
            #TODO: Tattoos eventually

            self.serum_tolerance = 2 #How many active serums this person can tolerate before they start to suffer negative effects.
            self.serum_effects = [] #A list of all of the serums we are under the effect of.

            if not special_role:  #Characters may have a special role that unlocks additional actions. By default this is an empty list.
                self.special_role = []
            elif isinstance(special_role, Role):
                self.special_role = [special_role] #Support handing a non-list special role, in case we forget to wrap it in a list one day.
            elif isinstance(special_role, list):
                self.special_role = special_role #Otherwise we've handed it a list
            else:
                self.special_role = []
                log_message("Person \"" + name + " " + last_name + "\" was handed an incorrect special role parameter.")

            self.job = None
            self.add_job(job)

            self.on_room_enter_event_list = [] #Checked when you enter a room with this character. If an event is in this list and enabled it is run (and no other event is until the room is reentered)
                # If handed a list of [action, positive_int], the integer is how many turns this action is kept around before being removed, triggered or not.
            self.on_talk_event_list = [] #Checked when you start to interact with a character. If an event is in this list and enabled it is run (and no other event is until you talk to the character again.)\
                # If handed a list of [action, positive_int], the integer is how many turns this action is kept around before being removed, triggered or not.

            ##Mental stats##
            #Mental stats are generally fixed and cannot be changed permanently. Ranges from 1 to 5 at start, can go up or down (min 0)
            self.charisma = stat_list[0] #How likeable the person is. Mainly influences marketing, also determines how well interactions with other characters go. Main stat for HR and sales
            self.int = stat_list[1] #How smart the person is. Mainly influences research, small bonuses to most tasks. #Main stat for research and production.
            self.focus = stat_list[2] #How on task the person stays. Influences most tasks slightly. #Main stat for supplies

            self.charisma_debt = 0 #Tracks how far into the negative a characters stats are, for the purposes of serum effects. Effective stats are never lower than 0.
            self.int_debt = 0
            self.focus_debt = 0

            ##Work Skills##
            #Skills can be trained up over time, but are limited by your raw stats. Ranges from 1 to 5 at start, can go up or down (min 0)
            self.hr_skill = skill_list[0]
            self.market_skill = skill_list[1]
            self.research_skill = skill_list[2]
            self.production_skill = skill_list[3]
            self.supply_skill = skill_list[4]

            self.max_energy = 100
            self.energy = self.max_energy

            self.salary_modifier = 1.0 # Set by events for what this character considers "fair" for their skill, and/or reflects what they were promised.
            self.salary = self.calculate_base_salary()


            self.idle_pose = get_random_from_list(["stand2","stand3","stand4","stand5"]) #Get a random idle pose that you will use while people are talking to you.
            self.idle_animation = idle_wiggle_animation #If we support animation we use this to jiggle their tits and ass just a little to give the screen some movement.
            #self.idle_animation.innate_animation_strength += 0.05 * rank_tits(self.tits) # Larger tits swing more #TODO: Implement region specific weighting.

            self.personal_region_modifiers = {"breasts":0.1+0.1 * rank_tits(self.tits)} #A dict that stores information about modifiers that should be used for specific regions of animations. Default is 1.

            ##Personality Stats##
            #Things like sugestability, that change over the course of the game when the player interacts with the girl
            self.suggestibility = 0 + suggest #How quickly/efficently bleeding temporary sluttiness is turned into core sluttiness.
            self.suggest_bag = [] #This will store a list of ints which are the different suggestion values fighting for control. Only the highest is used, maintained when serums are added and removed.

            self.happiness = happiness #Higher happiness makes a girl less likely to quit and more willing to put up with you pushing her using obedience.
            self.love = love
            self.sluttiness = 0 + sluttiness #How slutty the girl is by default. Higher will have her doing more things just because she wants to or you asked.
            self.core_sluttiness = self.sluttiness #Core sluttiness is the base level of what a girl considers normal. normal "sluttiness" is the more variable version, technically refered to as "temporary slutiness".
            self.obedience = 100 + obedience #How likely the girl is to listen to commands. Default is 100 (normal person), lower actively resists commands, higher follows them.

            #Situational modifiers are handled by events. These dicts and related functions provide a convenient way to avoid double contributions. Remember to clear your situational modifiers when you're done with them!!
            self.situational_sluttiness = {} #A dict that stores a "situation" string and the corrisponding amount it is contributing to the girls sluttiness.
            self.situational_obedience = {} #A dict that stores a "situation" string and a corrisponding amount that it has affected their obedience by.

            ##Sex Stats##
            #These are physical stats about the girl that impact how she behaves in a sex scene. Future values might include things like breast sensitivity, pussy tighness, etc.
            self.arousal = 0 #How actively horny a girl is, and how close she is to orgasm.
            self.max_arousal = 100 #Her maximum arousal. TODO: Keep this hidden until you make her cum the first time?

            self.novelty = 100 #How novel this girl making you cum is. Breaking taboos and time increases it, the girl making you cum decreases it.

            ##Sex Skills##
            #These represent how skilled a girl is at different kinds of intimacy, ranging from kissing to anal. The higher the skill the closer she'll be able to bring you to orgasm (whether you like it or not!)
            self.sex_skills = {}
            self.sex_skills["Foreplay"] = sex_list[0] #A catch all for everything that goes on before blowjobs, sex, etc. Includes things like kissing and strip teases.
            self.sex_skills["Oral"] = sex_list[1] #The girls skill at giving head.
            self.sex_skills["Vaginal"] = sex_list[2] #The girls skill at different positions that involve vaginal sex.
            self.sex_skills["Anal"] = sex_list[3] #The girls skill at different positions that involve anal sex.

            self.sex_record = {}
            self.sex_record["Handjobs"] = 0
            self.sex_record["Blowjobs"] = 0
            self.sex_record["Cunnilingus"] = 0
            self.sex_record["Tit Fucks"] = 0
            self.sex_record["Vaginal Sex"] = 0
            self.sex_record["Anal Sex"] = 0
            self.sex_record["Cum Facials"] = 0
            self.sex_record["Cum in Mouth"] = 0
            self.sex_record["Cum Covered"] = 0
            self.sex_record["Vaginal Creampies"] = 0
            self.sex_record["Anal Creampies"] = 0

            self.broken_taboos = [] #Taboos apply a penalty to the _first_ time you are trying to push some boundry (first time touching her pussy, first time seeing her tits, etc.), and trigger special dialogue when broken.

            bc_chance = 100 - (self.age + (self.get_opinion_score("bareback sex")*15))
            if persistent.pregnancy_pref == 2 and renpy.random.randint(0,100) > bc_chance:
                self.on_birth_control = False #If this character is on birth control or not. Note that this may be overridden by a game wide setting preventing pregnancy. (and on other settings may not be 100% effective)
            else:
                self.on_birth_control = True
            self.bc_penalty = 0 #Lowers the chance of birht control preventing a pregnancy. (Default is 100% if predictable or 90% if realistic). #TODO: Add serum traits that affect this.
            self.fertility_percent = 20.0 - ((self.age-18.0)/3.0) #The chance, per creampie, that a girl gets pregnant.
            self.ideal_fertile_day = renpy.random.randint(0,30) #Influences a girls fertility chance. It is double on the exact day of the month, dropping down to half 15 days before/after. Only applies on realistic setting.

            self.lactation_sources = 0 #How many things are causing this girl to lactate. Mainly serum traits, side effects, or pregnancy.

            ## Clothing things.
            self.wardrobe = copy.copy(wardrobe) #Note: we overwrote default copy behaviour for wardrobes so they do not have any interference issues with eachother.
            if base_outfit is None:
                self.base_outfit = Outfit(name + "'s Base Outfit")
            else:
                self.base_outfit = base_outfit


            self.infractions = [] #List of infractions this character has committed.

            self.planned_outfit = self.wardrobe.decide_on_outfit(self.sluttiness) #planned_outfit is the outfit the girl plans to wear today while not at work. She will change back into it after work or if she gets stripped. Cop0y it in case the outfit is changed during the day.
            self.planned_uniform = None #The uniform the person was planning on wearing for today, so they can return to it if they need to while at work.
            self.apply_outfit(self.planned_outfit)


            ## Internet things ##
            if generate_insta: #NOTE: By default all of these are not visible to the player.
                self.special_role.append(instapic_role)
            if generate_dikdok:
                self.special_role.append(dikdok_role)
            if generate_onlyfans:
                self.special_role.append(onlyfans_role)

            ## Conversation things##
            self.sexed_count = 0

            self.training_log = defaultdict(int) #Contains a list of Trainable.training_tag's that this person has had trained already, which is used to increase the cost of future training in similar things.



        def __call__(self, what, *args, **kwargs): #Required to play nicely with statement equivalent say() when passing only Person object.
            new_what = what #keep the old what as a reference in case we need it.
            new_colour = Color(self.what_color) #Multiple sections may modify the colour of the entire string, so we apply it once at the end.

            #Tags that are applied are generally applied to the inner most parts up here, more general as we go down.
            if self.has_role(trance_role): #Desaturate her dialogue as she falls deeper into a trance.
                if self.has_exact_role(trance_role):
                    new_colour = new_colour.multiply_hsv_saturation(0.7)
                elif self.has_exact_role(heavy_trance_role):
                    new_colour = new_colour.multiply_hsv_saturation(0.4)
                elif self.has_exact_role(heavy_trance_role):
                    new_colour = new_colour.multiply_hsv_saturation(0.1)

            flattened_phrase = remove_punctuation(what).lower() #Strip the entire phrase so we can check for individual words.
            if "knocked up" in new_what.lower():
                if self.arousal > 40 - (10*self.get_opinion_score("bareback sex") + self.get_opinion_score("creampies")) or self.has_role(breeder_role):
                    start_index = new_what.lower().find("knocked up")
                    start_substring = new_what[start_index:start_index + len("knocked up")]
                    replace_substring = "{sc=1}"+self.wrap_string(start_substring, the_colour = new_colour)+"{/sc}"
                    new_what = new_what.replace(start_substring, replace_substring)

            if "knock me up" in new_what.lower():
                if self.arousal > 40 - (10*self.get_opinion_score("bareback sex") + self.get_opinion_score("creampies")) or self.has_role(breeder_role):
                    start_index = new_what.lower().find("knock me up")
                    start_substring = new_what[start_index:start_index + len("knock me up")]
                    replace_substring = "{sc=1}"+self.wrap_string(start_substring, the_colour = new_colour)+"{/sc}"
                    new_what = new_what.replace(start_substring, replace_substring)

            if "preg me" in new_what.lower():
                if self.arousal > 40 - (10*self.get_opinion_score("bareback sex") + self.get_opinion_score("creampies")) or self.has_role(breeder_role):
                    start_index = new_what.lower().find("preg me")
                    start_substring = new_what[start_index:start_index + len("preg me")]
                    replace_substring = "{sc=1}"+self.wrap_string(start_substring, the_colour = new_colour)+"{/sc}"
                    new_what = new_what.replace(start_substring, replace_substring)

            if "oh god" in new_what.lower():
                if self.arousal > 40 - (10*self.get_opinion_score("bareback sex") + self.get_opinion_score("creampies")) or self.has_role(breeder_role):
                    start_index = new_what.lower().find("oh god")
                    start_substring = new_what[start_index:start_index + len("oh god")]
                    replace_substring = "{sc=1}"+self.wrap_string(start_substring, the_colour = new_colour)+"{/sc}"
                    new_what = new_what.replace(start_substring, replace_substring)

            if "oh my god" in new_what.lower():
                if self.arousal > 40 - (10*self.get_opinion_score("bareback sex") + self.get_opinion_score("creampies")) or self.has_role(breeder_role):
                    start_index = new_what.lower().find("oh my god")
                    start_substring = new_what[start_index:start_index + len("oh my god")]
                    replace_substring = "{sc=1}"+self.wrap_string(start_substring, the_colour = new_colour)+"{/sc}"
                    new_what = new_what.replace(start_substring, replace_substring)


            temp_what = ""
            for word in new_what.split(): #Per word modifications
                flattened_word = remove_punctuation(word).lower() #Stripped and lower case for easy comparison, we use the full raw word (including punctaiton) for replacement.
                modified_word = False
                effect_strength = str(int(6*(self.arousal/self.max_arousal)) + 2) #If an effect triggers this scales the effect with arousal.
                if word[0] == "{" and word [-1] == "}":
                    pass #Don't do anything to tags.

                elif flattened_word == "cum" or flattened_word == "cumming": #Strip punctuation, avoids us catching phrases like "cumming" and only shaking the front.
                    if self.arousal > (40 - 10*(self.get_opinion_score("drinking cum")+self.get_opinion_score("being covered in cum")+self.get_opinion_score("cum facials")+self.get_opinion_score("creampies"))):
                        modified_word = True
                        cum_color = Color("#e5e5d6")

                        word_replace = self.wrap_string(word, the_colour = cum_color, the_font = "fonts/plasdrip.ttf")
                        word_replace = "{atl=0.3,drop_text~#~ 2.0, bounce_text~" + effect_strength + "}" + word_replace + "{/atl}"
                        temp_what += word_replace + " "

                elif flattened_word == "cock" or flattened_word == "dick":
                    if self.arousal > (40 - 20*(self.get_opinion_score("big dicks"))):
                        modified_word = True
                        word_replace = self.wrap_string(word, the_colour = new_colour, size_mod = effect_strength)
                        word_replace = "{sc=1}{bt=" + effect_strength + "}" + word_replace + "{/bt}{/sc}"
                        temp_what += word_replace + " "

                elif flattened_word == "pussy" or flattened_word == "vagina" or flattened_word == "cunt":
                    if self.arousal > (50):
                        modified_word = True
                        word_replace = self.wrap_string(word, the_colour = new_colour)
                        word_replace = "{bt=" + effect_strength + "}" + word_replace + "{/bt}"
                        temp_what += word_replace + " "

                elif any(flattened_word == target_word for target_word in ["tit","tits","boob","boobs","breast","breasts","mommy milkers"]):
                    if self.arousal > 40 - 10*self.get_opinion_score("showing her tits"):
                        modified_word = True
                        tit_effect_strength = str(int(6*(self.arousal/self.max_arousal)) + rank_tits(self.tits))
                        word_replace = self.wrap_string(word, the_colour = new_colour)
                        word_replace = "{atl=bounce_text~" + tit_effect_strength + "}" + word_replace + "{/atl}"
                        temp_what += word_replace + " "

                elif flattened_word == "fuck":
                    if self.arousal > 60:
                        modified_word = True
                        word_replace = self.wrap_string(word, the_colour = new_colour, size_mod = effect_strength)
                        temp_what += word_replace + " "

                elif flattened_word == "pregnant" or flattened_word == "bred" or flattened_word == "breed": #TODO: Add a word effect that swells through the middle?
                    if self.arousal > 40 - (10*self.get_opinion_score("bareback sex") + self.get_opinion_score("creampies")) or self.has_role(breeder_role):
                        modified_word = True
                        word_replace = self.wrap_string(word, the_colour = new_colour, size_mod = effect_strength)
                        word_replace = "{sc=1}" + word_replace + "{/sc}"
                        temp_what += word_replace + " "

                if not modified_word:
                    temp_what += word + " "

            new_what = temp_what #[:-1] #STrip the last character, which is an unused space.
            new_what = self.wrap_string(new_what, the_colour = new_colour)

            self.char(new_what, *args, **kwargs)

        def wrap_string(self, string, the_colour = None, the_font = None, size_mod = None): #Useful for wrapping a piece of advanced tag dialogue with the proper font, colour, style.
            return_string = string
            if the_colour is None:
                the_colour = self.what_color.hexcode
            else:
                the_colour = the_colour.hexcode

            if the_font is None:
                the_font = self.who_font
            return_string = "{color=" + the_colour + "}" + return_string + "{/color}"
            return_string = "{font=" + the_font + "}" + return_string + "{/font}" #Then set the font
            if size_mod is not None:
                size_string = str(size_mod)
                if size_mod > 0:
                    size_string = "+" + size_string
                return_string = "{size=" + size_string + "}" + return_string + "{/size}"
            return_string = "{=general_dialogue_style}" + return_string + "{/=general_dialogue_style}"
            return return_string

        def __getattr__(self, attr):
            if attr == "core_sluttiness": #Helps maintain mod support after v0.43 removed core_sluttiness as an attribute
                return self.sluttiness
            else:
                raise AttributeError



        def generate_home(self, set_home_time = True): #Creates a home location for this person and adds it to the master list of locations so their turns are processed.
            if self.home is None:
                start_home = Room(self.name+"'s home", self.name+"'s home", [], standard_bedroom_backgrounds[:], [],[],[],False,[0.5,0.5], visible = False, hide_in_known_house_map = False, lighting_conditions = standard_indoor_lighting)
                #start_home.link_locations_two_way(downtown)

                start_home.add_object(make_wall())
                start_home.add_object(make_floor())
                start_home.add_object(make_bed())
                start_home.add_object(make_window())

                self.home = start_home
                if set_home_time:
                    self.set_schedule(start_home, the_times = [0,4])
                list_of_places.append(start_home)
            return self.home

        def generate_daughter(self, force_live_at_home = False): #Generates a random person who shares a number of similarities to the mother
            age = renpy.random.randint(18, self.age-16)

            if renpy.random.randint(0,100) < 60:
                if self.body_type == "standard_preg_body":
                    body_type = self.event_triggers_dict.get("pre_preg_body", "standard_body")
                else:
                    body_type = self.body_type

            else:
                body_type = None

            if renpy.random.randint(0,100) < 40: #Slightly lower for facial similarities to keep characters looking distinct
                face_style = self.face_style
            else:
                face_style = None

            if renpy.random.randint(0,100) < 60: #60% of the time they share hair colour
                hair_colour = self.hair_colour
            else:
                hair_colour = None

            if renpy.random.randint(0,100) < 60: # 60% they share the same breast size
                tits = self.tits
            else:
                tits = None

            if renpy.random.randint(0,100) < 60: #Share the same eye colour
                eyes = self.eyes
            else:
                eyes = None

            if renpy.random.randint(0,100) < 60: #Have heights that roughly match (but not exactly, and readjusted for the the general scaling factor.)
                height = (self.height/0.8) * (renpy.random.randint(95,105)/100.0)
                if height > 1.0:
                    height = 1.0
                elif height < 0.9:
                    height = 0.9
            else:
                height = None

            if renpy.random.randint(0,100) < 85 - age or force_live_at_home: #It is less likely she lives at home the older she is.
                start_home = self.home
            else:
                start_home = None


            the_daughter = create_random_person(last_name = self.last_name, age = age, body_type = body_type, face_style = face_style, tits = tits, height = height,
                hair_colour = hair_colour, skin = self.skin, eyes = eyes, start_home = start_home)

            if start_home is None:
                the_daughter.generate_home()
            the_daughter.home.add_person(the_daughter)

            for sister in town_relationships.get_existing_children(self): #First find all of the other kids this person has
                town_relationships.update_relationship(the_daughter, sister, "Sister") #Set them as sisters

            town_relationships.update_relationship(self, the_daughter, "Daughter", "Mother") #Now set the mother/daughter relationship (not before, otherwise she's a sister to herself!)

            return the_daughter


        def run_turn(self):
            self.change_energy(20, add_to_log = False)

            remove_list = []
            for serum in self.serum_effects: #Compute the effects of all of the serum that the girl is under.
                serum.run_on_turn(self) #Run the serum's on_turn funcion if it has one.
                if serum.duration_expired(): #Returns true if the serum effect is suppose to expire in this time, otherwise returns false. Always updates duration counter when called.
                    remove_list.append(serum) #Use a holder "remove" list to avoid modifying list while iterating.

            for serum in remove_list:
                serum.run_on_remove(self)
                self.serum_effects.remove(serum)

            # Check for serum overdoses after expired effects have been removed.
            over_tolerance_count = len(self.serum_effects) - self.serum_tolerance
            if over_tolerance_count > 0:
                self.change_happiness(over_tolerance_count*5, add_to_log = False)
                self.add_situational_slut("over serum tolerance", over_tolerance_count*-5, "My body feels strange...")
                self.add_situational_obedience("over serum tolerance", over_tolerance_count*-5, "My body feels strange...")
            else:
                self.clear_situational_slut("over serum tolerance")
                self.clear_situational_obedience("over serum tolerance")

            for a_role in self.special_role:
                a_role.run_turn(self)



        def run_move(self,location): #Move to the apporpriate place for the current time unit, ie. where the player should find us.

            #Move the girl the appropriate location on the map. For now this is either a division at work (chunks 1,2,3) or downtown (chunks 0,5). TODO: add personal homes to all girls that you know above a certain amount.
            for serum in self.serum_effects: #Compute the effects of all of the serum that the girl is under.
                serum.run_on_move(self) #Run the serum's on_move function if one exists


            self.sexed_count = 0 #Reset the counter for how many times you've been seduced, you might be seduced multiple times in one day!

            if time_of_day == 0: #It's a new day, get a new outfit out to wear!
                self.planned_outfit = self.wardrobe.decide_on_outfit(self.sluttiness)
                self.apply_outfit(self.planned_outfit)
                self.planned_uniform = None

            destination = self.get_destination() #None destination means they have free time
            # if destination == self.work and not mc.business.is_open_for_business():
            #     destination = None #TODO: We can now do day-of-the-week scheduling, so this is no longer needed.

            if destination is not None: #We have somewhere scheduled to be for this turn. Let's move over there.
                location.move_person(self, destination) #Always go where you're scheduled to be.
                if self.job and self.get_destination() == self.job.job_location: #We're going to work.
                    if self.should_wear_uniform(): #Get a uniform if we should be wearing one.
                        self.wear_uniform()
                        self.change_happiness(self.get_opinion_score("work uniforms"),add_to_log = False)
                        if self.planned_uniform and self.planned_uniform.slut_requirement > self.sluttiness*0.75: #A skimpy outfit/uniform is defined as the top 25% of a girls natural sluttiness.
                            self.change_slut(self.get_opinion_score("skimpy uniforms"), 30, add_to_log = False)

                elif destination == self.home:
                    self.apply_outfit(self.planned_outfit)

                #NOTE: There is no else here because all of the desitnations should be set. If it's just a location they travel there and that's the end of it.

            else:
                #She finds somewhere to burn some time
                self.apply_outfit(self.planned_outfit)
                available_locations = [] #Check to see where is public (or where you are white listed) and move to one of those locations randomly
                for potential_location in list_of_places:
                    if potential_location.public:
                        available_locations.append(potential_location)
                location.move_person(self, get_random_from_list(available_locations))

            #We do uniform/outfit checks in run move because it happens at the _start_ of the turn. The girl looks forward to wearing her outfit (or dreads it) rather than responds to actually doing it.
            if self.outfit and self.planned_outfit.slut_requirement > self.sluttiness*0.75: #A skimpy outfit is defined as the top 25% of a girls natural sluttiness.
                self.change_slut(self.get_opinion_score("skimpy outfits"), 30, add_to_log = False)
            elif self.outfit and self.planned_outfit.slut_requirement < self.sluttiness*0.25: #A conservative outfit is defined as the bottom 25% of a girls natural sluttiness.
                self.change_happiness(self.get_opinion_score("conservative outfits"), add_to_log = False)

            if self.outfit.tits_available() and self.outfit.tits_visible() and self.outfit.vagina_available() and self.outfit.vagina_visible():
                self.change_slut(self.get_opinion_score("not wearing anything"), 50, add_to_log = False)

            if not self.outfit.wearing_bra() or not self.outfit.wearing_panties(): #We need to determine how much underwear they are not wearing. Each piece counts as half, so a +2 "love" is +1 slut per chunk.
                underwear_bonus = 0
                if not self.outfit.wearing_bra():
                    underwear_bonus += self.get_opinion_score("not wearing underwear")
                if not self.outfit.wearing_panties():
                    underwear_bonus += self.get_opinion_score("not wearing underwear")
                underwear_bonus = __builtin__.int(underwear_bonus/2.0) #I believe this rounds towards 0. No big deal if it doesn't, very minor detail.
                self.change_slut(underwear_bonus, 40, add_to_log = False)

            if self.outfit.tits_visible():
                self.change_slut(self.get_opinion_score("showing her tits"), 60, add_to_log = False)
            if self.outfit.vagina_visible():
                self.change_slut(self.get_opinion_score("showing her ass"), 60, add_to_log = False)

            for event_list in [self.on_room_enter_event_list, self.on_talk_event_list]: #Go through both of these lists and curate them, ie trim out events that should have expired.
                removal_list = [] #So we can iterate through without removing and damaging the list.
                for an_action in event_list:
                    if isinstance(an_action, Limited_Time_Action): #It's a LTA holder, so it has a turn counter
                        an_action.turns_valid += -1
                        if an_action.turns_valid <= 0:
                            removal_list.append(an_action)

                for action_to_remove in removal_list:
                    event_list.remove(action_to_remove)

            for a_role in self.special_role:
                a_role.run_move(self)

        def run_day(self): #Called at the end of the day.
            #self.outfit = self.wardrobe.decide_on_outfit(self.sluttiness) #Put on a new outfit for the day!

            self.change_energy(60, add_to_log = False)
            self.change_novelty(1, add_to_log = False)

            #Now we will normalize happiness towards 100 over time. Every 5 points of happiness above or below 100 results in a -+1 per turn, rounded towards 0.
            hap_diff = self.happiness - 100
            hap_diff = __builtin__.int(hap_diff/5.0) #python defaults to truncation towards 0, so this gives us the number we should be changing our happinss by
            self.change_happiness(-hap_diff, add_to_log = False) #Apply the change

            if self.arousal > (self.max_arousal/2): #If her arousal is high she masturbates at night, generating a small amount of sluttiness #TODO: Have this trigger an LTE where girls might be getting off when you walk in.
                self.arousal = 0
                if self.get_opinion_score("masturbating") > 0: # Masturbating turns her on, so just getting off turns her back on!
                    self.arousal = 15*self.get_opinion_score("masturbating")
                self.change_happiness(5+5*self.get_opinion_score("masturbating"), add_to_log = False)
                self.run_orgasm(show_dialogue = False, trance_chance_modifier = self.get_opinion_score("masturbating"), add_to_log = False, fire_event = False)


            remove_list = []
            for serum in self.serum_effects:
                serum.run_on_turn(self) #If a run_on_turn is called and the serum has expired no effects are calculated, so we can safely call this as many times as we want.
                serum.run_on_turn(self) #Night is 3 turn chunks, but one is already called when time progresses. Run serums twice more, and if we've gotten here we also run the on day function.
                serum.run_on_day(self) #Serums that effect people at night must effect two of the three turns.
                if serum.duration_expired(): #Night is 3 segments, but 1 is allready called when run_turn is called.
                    remove_list.append(serum)

            for serum in remove_list:
                serum.run_on_remove(self)
                self.serum_effects.remove(serum)

            for infraction in self.infractions:
                infraction.days_existed += 1
                if infraction.days_existed > infraction.days_valid:
                    self.remove_infraction(infraction)


            if day%7 == 0: #If the new day is Monday
                self.change_happiness(self.get_opinion_score("Mondays")*10, add_to_log = False)

            elif day%7 == 5: #If the new day is Friday
                self.change_happiness(self.get_opinion_score("Fridays")*10, add_to_log = False)

            elif day%7 == 6 or day%7 == 7: #If the new day is a weekend day
                self.change_happiness(self.get_opinion_score("the weekend")*10, add_to_log = False)

            for a_role in self.special_role:
                a_role.run_day(self)

        def get_display_colour_code(self, saturation = 1.0, given_alpha = 1.0):
            the_colour = Color(self.char.what_args["color"])
            the_colour = the_colour.multiply_hsv_saturation(saturation)
            the_colour = the_colour.multiply_value(saturation)
            the_colour = the_colour.replace_opacity(given_alpha)

            return the_colour.hexcode


        def build_person_displayable(self,position = None, emotion = None, special_modifier = None, lighting = None): #Encapsulates what is done when drawing a person and produces a single displayable.
            if position is None:
                position = self.idle_pose #Easiest change is to call this and get a random standing posture instead of a specific idle pose. We redraw fairly frequently so she will change position frequently.

            displayable_list = [] # We will be building up a list of displayables passed to us by the various objects on the person (their body, clothing, etc.)

            if emotion is None:
                emotion = self.get_emotion()

            forced_special_modifier = self.outfit.get_forced_modifier()
            if forced_special_modifier is not None:
                special_modifier = forced_special_modifier # Overrides all other things, supports people with ball gags always having an open mouth (mechanically, not emotionally)

            x_size = position_size_dict.get(position)[0]
            y_size = position_size_dict.get(position)[1]

            displayable_list.append(self.body_images.generate_item_displayable(self.body_type,self.tits,position,lighting)) #Add the body displayable
            displayable_list.append(self.expression_images.generate_emotion_displayable(position,emotion, special_modifier = special_modifier, eye_colour = self.eyes[1], lighting = lighting)) #Get the face displayable
            displayable_list.append(self.pubes_style.generate_item_displayable(self.body_type,self.tits, position, lighting = lighting)) #Add in her pubes. #TODO: See if we need to mask this with her body profile for particularly bush-y bushes to prevent clothing overflow.

            displayable_list.extend(self.outfit.generate_draw_list(self,position,emotion,special_modifier, lighting = lighting)) #Get the displayables for everything we wear. Note that extnsions do not return anything because they have nothing to show.
            displayable_list.append(self.hair_style.generate_item_displayable("standard_body",self.tits,position, lighting = lighting)) #Get hair
            #NOTE: Positional modifiers like xanchor that expect pixles need to be given ints, they do not auto convert from floats.

            composite_list = [(x_size,y_size)] #Now we build a list of our parameters, done like this so they are arbitrarily long

            for display in displayable_list:
                if isinstance(display, __builtin__.tuple):
                    composite_list.extend(display)
                else:
                    composite_list.append((0,0)) #Displayables are all handed over as composites with the image centered, so no extra work is needed here.
                    composite_list.append(display) #Append the actual displayable

            character_composite = Composite(*composite_list)

            if persistent.vren_display_pref == "Float" or persistent.vren_display_pref == "Frame":
                character_raw_body = im.Composite((x_size, y_size),
                    (0,0), self.body_images.generate_raw_image(self.body_type,self.tits,position),
                    (0,0), self.expression_images.generate_raw_image(position, emotion, special_modifier = special_modifier),
                    self.hair_style.get_crop_offset(position), self.hair_style.generate_raw_image("standard_body",self.tits,position))

                blurred_image = im.Blur(character_raw_body, 6)
                aura_colour = self.get_display_colour_code()
                recoloured_blur = im.MatrixColor(blurred_image, im.matrix.colorize(aura_colour, aura_colour))

                final_composite = Composite((x_size, y_size), (0,0), recoloured_blur, (0,0), character_composite)

            else:
                final_composite = character_composite

            final_image = Flatten(final_composite) # Create a composite image using all of the displayables
            return final_image

        def build_weight_mask(self, the_animation, position, animation_effect_strength): #Builds a weight mask displayable that highlights the sections of a character that should be animated.
            x_size, y_size = position_size_dict.get(position)

            composite_components = []
            region_weight_items_dict = the_animation.get_weight_items()
            for region_weight_name in region_weight_items_dict: #Goes through each region ie. "breasts", "butt", and others to come, and applies the animation strength, the personal region strength, and animation region strength
                the_weight_item = region_weight_items_dict[region_weight_name]
                composite_components.append(the_weight_item.crop_offset_dict.get(position, (0,0)))
                region_weight_modifier = animation_effect_strength * self.personal_region_modifiers.get(region_weight_name, 1) * the_animation.innate_animation_strength * the_animation.region_specific_weights.get(region_weight_name, 1)
                if region_weight_modifier > 1:
                    region_weight_modifier = 1

                region_brightness_matrix = im.matrix.brightness(-1 + region_weight_modifier)
                region_mask = the_weight_item.generate_raw_image(self.body_type, self.tits, position)
                region_mask = im.MatrixColor(region_mask, region_brightness_matrix)
                composite_components.append(region_mask)

            the_mask_composite = im.Composite((x_size, y_size), *composite_components)

            weight_mask = im.Blur(the_mask_composite, 2)

            return weight_mask

        def draw_person(self,position = None, emotion = None, special_modifier = None, show_person_info = True, lighting = None, background_fill = "auto", the_animation = None, animation_effect_strength = 1.0,
            draw_layer = "solo", display_transform = None, extra_at_arguments = None, display_zorder = None, wipe_scene = True): #Draw the person, standing as default if they aren't standing in any other position
            #log_message(self.name + " | Start | " + str(time.time()))

            if position is None:
                position = self.idle_pose #Easiest change is to call this and get a random standing posture instead of a specific idle pose. We redraw fairly frequently so she will change position frequently.

            if the_animation is None:
                the_animation = self.idle_animation

            if not can_use_animation():
                the_animation = None

            if lighting is None:
                lighting = mc.location.get_lighting_conditions()

            character_image = self.build_person_displayable(position, emotion, special_modifier, lighting) #The static 2D displayable.

            if not the_animation is None:
                weight_mask = self.build_weight_mask(the_animation, position, animation_effect_strength)

            else:
                weight_mask = Solid("#000000") #Black mask = no influence.

            x_size, y_size = position_size_dict[position]

            animated_image = ShaderPerson(character_image, weight_mask)
            if background_fill == "auto":
                if persistent.vren_display_pref == "Frame":
                    background_fill = self.get_display_colour_code(saturation = 0.8, given_alpha = 0.6) # Sets it to be partially transparent.
                else:
                    background_fill = None

            if background_fill is not None: #If a background colour is given we add a solid to the back and a frame around the entire thing.
                bg_colour =  Composite((x_size, y_size), (0,0), Solid(background_fill))
                image_frame = Composite((x_size, y_size), (0,0), Frame("/gui/Character_Window_Frame.png", 12, 12))

            if display_transform is None:
                display_transform = character_right

            frame_at_arguments = [display_transform, scale_person(self.height)] # A list without basic_bounce to use for the background and the frame.
            at_arguments = [display_transform, scale_person(self.height)]
            if the_animation is not None:
                at_arguments.append(basic_bounce(the_animation))

            if extra_at_arguments:
                if isinstance(extra_at_arguments, list):
                    frame_arguments.extend(extra_at_arguments)
                    at_arguments.extend(extra_at_arguments)
                else:
                    frame_arguments.append(extra_at_arguments)
                    at_arguments.append(extra_at_arguments)
            else:
                extra_at_arguments = []

            if display_zorder is None:
                display_zorder = 0

            character_tag = str(self.character_number)

            self.hide_person()
            if wipe_scene:
                clear_scene() #Make sure no other characters are drawn either.

            if background_fill is not None:
                renpy.show(character_tag+"_bg_fill", at_list=frame_at_arguments, layer=draw_layer, what=bg_colour, zorder = display_zorder, tag=character_tag+"_bg_fill")
            renpy.show(character_tag, at_list=at_arguments, layer=draw_layer, what=animated_image, zorder = display_zorder, tag=character_tag)
            if background_fill is not None:
                renpy.show(character_tag+"_frame", at_list=frame_at_arguments, layer=draw_layer, what=image_frame, zorder = display_zorder, tag=character_tag+"_frame")

            if show_person_info:
                renpy.show_screen("person_info_ui",self)

        def hide_person(self, draw_layer = "solo"): #Hides the person. Makes sure to hide all posible known tags for the character.
            # We keep track of tags used to display a character so that they can always be unique, but still tied to them so they can be hidden
            character_tag = str(self.character_number)
            renpy.hide(character_tag, draw_layer)
            renpy.hide(character_tag+"_extra", draw_layer)


        def draw_animated_removal(self, the_clothing, position = None, emotion = None, special_modifier = None, show_person_info = True, lighting = None, background_fill = "auto", the_animation = None, animation_effect_strength = 1.0, half_off_instead = False,
            draw_layer = "solo", display_transform = None, extra_at_arguments = None, display_zorder = None, wipe_scene = True):
            #The new animated_removal method generates two image, one with the clothing item and one without. It then stacks them and layers one on top of the other and blends between them.

            if position is None:
                position = self.idle_pose

            if not can_use_animation():
                the_animation = None
            elif the_animation is None:
                the_animation = self.idle_animation

            if background_fill == "auto":
                if persistent.vren_display_pref == "Frame":
                    background_fill = self.get_display_colour_code(saturation = 0.8, given_alpha = 0.6) # Sets it to be partially transparent.
                else:
                    background_fill = None

            if lighting is None:
                lighting = mc.location.get_lighting_conditions()

            global draw_layers
            if draw_layer not in draw_layers:
                add_draw_layer(draw_layer)

            if display_transform is None:
                display_transform = character_right

            x_size, y_size = position_size_dict[position]

            frame_at_arguments = [display_transform, scale_person(self.height)]
            at_arguments = [display_transform, scale_person(self.height)] #TODO: make sure this works with a None animation.
            if the_animation is not None:
                at_arguments.append(basic_bounce(the_animation))

            if extra_at_arguments:
                if isinstance(extra_at_arguments, list):
                    frame_at_arguments.extend(extra_at_arguments)
                    at_arguments.extend(extra_at_arguments)
                else:
                    frame_at_arguments.append(extra_at_arguments)
                    at_arguments.append(extra_at_arguments)
            else:
                extra_at_arguments = []

            if display_zorder is None:
                display_zorder = 0

            if wipe_scene:
                clear_scene()

            if show_person_info:
                renpy.show_screen("person_info_ui",self)

            bottom_displayable = Flatten(self.build_person_displayable(position, emotion, special_modifier, lighting)) #Get the starting image
            if isinstance(the_clothing, list):
                for cloth in the_clothing:
                    if half_off_instead:
                        self.outfit.half_off_clothing(cloth) #Half-off the clothing
                    else:
                        self.outfit.remove_clothing(cloth) #Remove the clothing
            else:
                if half_off_instead:
                    self.outfit.half_off_clothing(the_clothing) #Half-off the clothing
                else:
                    self.outfit.remove_clothing(the_clothing) #Remove the clothing
            top_displayable = self.build_person_displayable(position, emotion, special_modifier, lighting) #Get the top image

            if not the_animation is None:
                weight_mask = self.build_weight_mask(the_animation, position, animation_effect_strength)
            else:
                weight_mask = weight_mask = Solid("#000000") #Black mask = no influence.

            bottom_animation = ShaderPerson(bottom_displayable, weight_mask)
            top_animation = ShaderPerson(top_displayable, weight_mask)

            self.hide_person()
            character_tag = str(self.character_number)

            if background_fill is not None: #If a background colour is given we add a solid to the back and a frame around the entire thing.
                bg_colour =  Composite((x_size, y_size), (0,0), Solid(background_fill))
                renpy.show(character_tag + "_bg_fill", at_list=frame_at_arguments, layer = draw_layer, what = bg_colour, zorder = display_zorder, tag = character_tag + "_bg_fill")

            renpy.show(character_tag, at_list=at_arguments, layer = draw_layer, what = top_animation, zorder = display_zorder, tag = character_tag)
            fade_at_arguments = at_arguments[:]
            fade_at_arguments.append(clothing_fade)
            renpy.show(character_tag + "_extra", at_list=fade_at_arguments, layer = draw_layer, what = bottom_animation, zorder = display_zorder, tag = character_tag + "_extra") #Blend from old to new.

            if background_fill is not None:
                image_frame = Composite((x_size, y_size), (0,0), Frame("/gui/Character_Window_Frame.png", 12, 12))
                renpy.show(character_tag + "_frame", at_list=frame_at_arguments, layer = draw_layer, what = image_frame, zorder = display_zorder, tag = character_tag + "_frame") #Uses an at_list copy that does not include the clothing_fade.
            return

        def get_emotion(self): # Get the emotion state of a character, used when the persons sprite is drawn and no fixed emotion is required.
            if self.arousal>= self.max_arousal:
                return "orgasm"

            elif self.happiness > 100:
                return "happy"

            elif self.happiness < 80:
                if self.love > 0:
                    return "sad"
                else:
                    return "angry"

            else:
                return "default"

        def call_dialogue(self, type, **extra_args): #Passes the paramater along to the persons personality and gets the correct dialogue for the event if it exists in the dict.
            self.personality.get_dialogue(self, type, **extra_args)

        def get_known_opinion_score(self, topic):
            the_topic = self.get_opinion_topic(topic)
            if the_topic is None:
                return 0
            else:
                if the_topic[1]:
                    return the_topic[0]
                else:
                    return 0

        def has_unknown_opinions(self, normal_opinions = True, sexy_opinions = True):
            if normal_opinions:
                for topic in self.opinions:
                    if not self.opinions[topic][1]:
                        return True

            if sexy_opinions:
                for topic in self.sexy_opinions:
                    if not self.sexy_opinions[topic][1]:
                        return True

            return False

        def get_opinion_score(self, topic): #Like get_opinion_topic, but only returns the score and not a tuple. Use this when determining a persons reaction to a relavent event.
            return_value = 0
            if isinstance(topic, list):
                for a_topic in topic:
                    return_value += self.get_opinion_score(a_topic)
            else:
                if topic in self.opinions:
                    return_value += self.opinions[topic][0]

                if topic in self.sexy_opinions:
                    return_value += self.sexy_opinions[topic][0]

            return return_value

        def get_opinion_topics_list(self, include_unknown = True, include_normal = True, include_sexy = True, include_hate = True, include_dislike = True, include_like = True, include_love = True):
            #TODO: Needs unit testing
            opinion_return_list = []
            lists_to_check = []
            if include_normal:
                for topic in self.opinions:
                    if self.opinions[topic][1] or include_unknown:
                        if self.opinions[topic][0] == -2 and include_hate:
                            opinion_return_list.append(topic)
                        elif self.opinions[topic][0] == -1 and include_dislike:
                            opinion_return_list.append(topic)
                        elif self.opinions[topic][0] == 1 and include_like:
                            opinion_return_list.append(topic)
                        elif self.opinions[topic][0] == 2 and include_love:
                            opinion_return_list.append(topic)
            if include_sexy:
                for topic in self.sexy_opinions:
                    if self.sexy_opinions[topic][1] or include_unknown:
                        if self.sexy_opinions[topic][0] == -2 and include_hate:
                            opinion_return_list.append(topic)
                        elif self.sexy_opinions[topic][0] == -1 and include_dislike:
                            opinion_return_list.append(topic)
                        elif self.sexy_opinions[topic][0] == 1 and include_like:
                            opinion_return_list.append(topic)
                        elif self.sexy_opinions[topic][0] == 2 and include_love:
                            opinion_return_list.append(topic)
            return opinion_return_list

        def get_opinion_topic(self, topic): #topic is a string matching the topics given in our random list (ie. "the colour blue", "sports"). Returns a tuple containing the score: -2 for hates, -1 for dislikes, 0 for no opinion, 1 for likes, and 2 for loves, and a bool to say if the opinion is known or not.
            if topic in self.opinions:
                return self.opinions[topic]

            if topic in self.sexy_opinions:
                return self.sexy_opinions[topic]

            return None

        def get_random_opinion(self, include_known = True, include_sexy = False, include_normal = True, only_positive = False, only_negative = False): #Gets the topic string of a random opinion this character holds. Includes options to include known opinions and sexy opinions. Returns None if no valid opinion can be found.
            the_dict = {} #Start our list of valid opinions to be listed as empty

            if include_normal: #if we include normal opinions build a dict out of the two
                the_dict = dict(the_dict, **self.opinions)

            if include_sexy: #If we want sexy opinions add them in too.
                the_dict = dict(the_dict, **self.sexy_opinions)


            known_keys = []
            if not include_known: #If we do not want to talk about known values
                for k in the_dict: #Go through each value in our combined normal and sexy opinion dict
                    if the_dict[k][1]: #Check if we know about it...
                        known_keys.append(k) #We build a temporary list of keys to remove because otehrwise we are modifying the dict while we traverse it.
                for del_key in known_keys:
                    del the_dict[del_key]

            remove_keys = []
            if only_positive or only_negative: # Let's us filter opinions so they only include possitive or negative ones.
                if only_positive:
                    for k in the_dict:
                        if self.get_opinion_score(k) < 0:
                            remove_keys.append(k)

                if only_negative:
                    for k in the_dict:
                        if self.get_opinion_score(k) > 0:
                            remove_keys.append(k)

                for del_key in remove_keys:
                    del the_dict[del_key]

            if the_dict:
                return get_random_from_list(the_dict.keys()) #If we have something in the list we can return the topic string we used as a key for it. This can then be used with get_opinion_score to get the actual opinion
            else:
                return None #If we have nothing return None, make sure to deal with this when we use this function.


        def discover_opinion(self, topic, add_to_log = True): #topic is a string matching the topics given in our random list (ie. "the colour blue"). If the opinion is in either of our opinion dicts we will set it to known, otherwise we do nothing. Returns True if the opinion was updated, false if nothing was changed.
            display_name = self.create_formatted_title("???")
            updated = False
            if self.title:
                display_name = self.title
            if topic in self.opinions:
                if not self.opinions[topic][1]:
                    updated = True
                    if add_to_log and self.title is not None:
                        mc.log_event("Discovered: " + display_name + " " + opinion_score_to_string(self.opinions[topic][0]) + " " + topic,"float_text_grey")
                self.opinions[topic][1] = True

            if topic in self.sexy_opinions:
                if not self.sexy_opinions[topic][1]:
                    updated = True
                    if add_to_log and self.title is not None:
                        mc.log_event("Discovered: " + display_name + " " + opinion_score_to_string(self.sexy_opinions[topic][0]) + " " + topic,"float_text_grey")
                self.sexy_opinions[topic][1] = True

            return updated

        def set_opinion(self, topic, strength, known = False): #override function to set an opinion to a known value, mainly used to set up characters before they are introduced
            is_sexy_opinion = False
            if topic in sexy_opinions_list:
                is_sexy_opinion = True

            if not strength == 0:
                if is_sexy_opinion:
                    self.sexy_opinions[topic] = [strength, known]
                else:
                    self.opinions[topic] = [strength, known]

            else:
                if topic in self.opinions:
                    self.opinions.pop(topic)
                if topic in self.sexy_opinions:
                    self.sexy_opinions.pop(topic)



        def strengthen_opinion(self, topic, add_to_log = True):
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title

            display_string = ""

            old_opinion = self.get_opinion_topic(topic)
            if old_opinion is None: #You cannot strengthen an opinion of 0, for that make a new one entirely.
                return False

            updated = False
            if old_opinion[0] == 1 or old_opinion[0] == -1:
                updated = True
                new_opinion_value = 2*old_opinion[0]
                if topic in self.opinions:
                    self.opinions[topic] = [new_opinion_value, old_opinion[1]]
                else:
                    self.sexy_opinions[topic] = [new_opinion_value, old_opinion[1]]
                display_string += "Opinion Strengthened: " + display_name + " now " + opinion_score_to_string(self.get_opinion_score(topic)) + " " + topic

            if add_to_log and display_string:
                mc.log_event(display_string, "float_text_grey")

            return updated

        def weaken_opinion(self, topic, add_to_log = True):
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title

            display_string = ""

            old_opinion = self.get_opinion_topic(topic)
            if old_opinion is None: #You cannot strengthen an opinion of 0, for that make a new one entirely.
                return False

            updated = False
            if old_opinion[0] == 2 or old_opinion[0] == -2:
                updated = True
                new_opinion_value = int(old_opinion[0]/2)
                if topic in self.opinions:
                    self.opinions[topic] = [new_opinion_value, old_opinion[1]]
                else:
                    self.sexy_opinions[topic] = [new_opinion_value, old_opinion[1]]
                display_string += "Opinion Weakened: " + display_name + " now " + opinion_score_to_string(self.get_opinion_score(topic)) + " " + topic

            else: #ie it was -1 or 1, because 0 already returned
                updated = True
                if topic in self.opinions:
                    self.opinions.pop(topic)
                elif topic in self.sexy_opinions:
                    self.sexy_opinions.pop(topic)
                display_string += "Opinion Weakened: " + display_name + " now " + opinion_score_to_string(self.get_opinion_score(topic)) + " " + topic

            if add_to_log and display_string:
                mc.log_event(display_string, "float_text_grey")

            return updated

        def create_opinion(self, topic, start_positive = True, start_known = True, add_to_log = True):
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title

            start_value = 1
            if not start_positive:
                start_value = -1 #Determines if the opinion starts as like or dislike.
            if not self.get_opinion_score(topic) == 0: #She already has an opinion
                return False

            is_sexy_opinion = False
            if topic in sexy_opinions_list:
                is_sexy_opinion = True

            opinion_tuple = [start_value, start_known]
            if is_sexy_opinion:
                self.sexy_opinions[topic] = opinion_tuple
            else:
                self.opinions[topic] = opinion_tuple

            if add_to_log:
                mc.log_event("Opinion Inspired: " + display_name + " now " + opinion_score_to_string(self.get_opinion_score(topic)) + " " + topic, "float_text_grey")

            return True

        def has_taboo(self, the_taboos):
            if the_taboos is None:
                return False

            if isinstance(the_taboos, basestring):
                the_taboos = [the_taboos]

            for a_taboo in the_taboos: #We also handle lists, if we wnat to check if someone has _any_ of several taboos at once
                if a_taboo not in self.broken_taboos:
                    return True
            return False

        def has_broken_taboo(self, the_taboos):
            if the_taboos is None:
                return False

            if isinstance(the_taboos, basestring):
                the_taboos = [the_taboos]

            for a_taboo in the_taboos: #We also handle lists, if we wnat to check if someone has _any_ of several taboos at once
                if a_taboo in self.broken_taboos:
                    return True
            return False

        def break_taboo(self, the_taboo, add_to_log = True, fire_event = True):
            if the_taboo not in self.broken_taboos:
                self.broken_taboos.append(the_taboo)
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                if add_to_log:
                    mc.log_event(" Taboo broken with " + display_name + "!", "float_text_red")

                self.change_novelty(5, add_to_log)

                if fire_event:
                    mc.listener_system.fire_event("girl_taboo_break", the_taboo = the_taboo)
                return True
            return False

        def restore_taboo(self, the_taboo, add_to_log = True):
            if the_taboo in self.broken_taboos:
                while the_taboo in self.broken_taboos:
                    self.broken_taboos.remove(the_taboo)
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                if add_to_log:
                    mc.log_event(" Taboo reasserted with " + display_name + "!", "float_text_red")
                return True
            return False

        def pick_position_comment(self, the_report): #Takes a report and has the person pick the most notable thing out of it. Generally used to then have them comment on it.
            highest_slut_position = None
            highest_slut_opinion = 0
            for position in the_report.get("positions_used", []):
                slut_opinion = position.slut_requirement
                if position.opinion_tags is not None:
                    for opinion_tag in position.opinion_tags:
                        slut_opinion += 5*self.get_opinion_score(opinion_tag)
                if highest_slut_position is None or slut_opinion > highest_slut_opinion:
                    highest_slut_position = position
                    highest_slut_opinion = slut_opinion

            return highest_slut_position


        def add_outfit(self,the_outfit, outfit_type = "full"):
            if outfit_type == "under":
                self.wardrobe.add_underwear_set(the_outfit)
            elif outfit_type == "over":
                self.wardrobe.add_overwear_set(the_outfit)
            else: #outfit_type = full
                self.wardrobe.add_outfit(the_outfit)

        def set_outfit(self,new_outfit):
            if new_outfit is not None:
                self.planned_outfit = new_outfit.get_copy() #Get a copy to return to when we are done.
                self.apply_outfit(new_outfit)

        def set_uniform(self,uniform, wear_now = False):
            if uniform is not None:
                self.planned_uniform = uniform.get_copy()
                if wear_now:
                    self.wear_uniform()

        def apply_outfit(self, the_outfit = None, ignore_base = False, update_taboo = False): #Hand over an outfit, we'll take a copy and apply it to the person, along with their base accessories unless told otherwise.
            if the_outfit is None:
                if self.should_wear_uniform():
                    the_outfit = self.planned_uniform;
                else:
                    the_outfit = self.planned_outfit

                if the_outfit is None:
                    return #We don't have a planned outfit, so trying to return to it makes no sense.
            if ignore_base:
                self.outfit = the_outfit.get_copy()
            else:
                self.outfit = the_outfit.get_copy().merge_outfit(self.base_outfit)

            if update_taboo: #If True, we assume this outfit is being put on or shown to the MC. It can break taboos about showing underwear, tits, pussy.
                self.update_outfit_taboos()

        def update_outfit_taboos(self):
            return_value = False
            if self.outfit.tits_visible():
                if self.break_taboo("bare_tits"):
                    return_value = True
            if self.outfit.vagina_visible():
                if self.break_taboo("bare_pussy"):
                    return_value = True
            if (self.outfit.wearing_panties() and not self.outfit.panties_covered()) or (self.outfit.wearing_bra() and not self.outfit.bra_covered()):
                if self.break_taboo("underwear_nudity"):
                    return_value = True
            return return_value


        def give_serum(self,the_serum_design, add_to_log = True): ##Make sure you are passing a copy of the serum, not a reference.
            self.serum_effects.append(the_serum_design)
            the_serum_design.run_on_apply(self)

        def is_under_serum_effect(self):
            if self.serum_effects:
                return True
            else:
                return False

        def apply_serum_study(self, add_to_log = True): #Called when the person is studied by the MC. Raises mastery level of all traits used in active serums by 0.2
            studied_something = False
            for serum in self.serum_effects:
                for trait in serum.traits:
                    trait.add_mastery(0.2)
                    studied_something = True
            if studied_something and add_to_log:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                mc.log_event("Observed " + display_name + ", mastery of all active serum traits increased by 0.2", "float_text_blue")


        def change_suggest(self,amount, add_to_log = True): #This changes the base, usually permanent suggest. Use add_suggest_effect to add temporary, only-highest-is-used, suggestion values
            self.suggestibility += amount
            if add_to_log and amount != 0 and self.title:
                if amount > 0:
                    mc.log_event(self.title + ": Suggestibility increased permanently by +" + str(amount) + "%", "float_text_blue")
                else:
                    mc.log_event(self.title + ": Suggestibility decreased permanently by " + str(amount) + "%", "float_text_blue")

            # Note that suggestability can be negative, representing someone who is _resistant_ to trances for some reason.

        def add_suggest_effect(self,amount, add_to_log = True):
            if amount > __builtin__.max(self.suggest_bag or [0]):
                self.change_suggest(-__builtin__.max(self.suggest_bag or [0]), add_to_log = False) #Subtract the old max and...
                self.change_suggest(amount, add_to_log = False) #add our new suggest.
                if add_to_log and amount != 0 and self.title:
                    mc.log_event(self.title + ": Suggestibility increased, now " + str(amount), "float_text_blue")
            else:
                if add_to_log and amount != 0 and self.title:
                    mc.log_event(self.title + ": Suggestiblity " + str(amount) + " lower than current " + str(self.suggestibility) + " amount. Suggestibility unchanged.", "float_text_blue")
            self.suggest_bag.append(amount) #Add it to the bag, so we can check to see if it is max later.


        def remove_suggest_effect(self,amount):
            if amount in self.suggest_bag: # Avoid removing the "amount" if we don't actually have it in the bag.
                self.change_suggest(- __builtin__.max(self.suggest_bag or [0]), add_to_log = False) #Subtract the max
                self.suggest_bag.remove(amount)
                self.change_suggest(__builtin__.max(self.suggest_bag or [0]), add_to_log = False) # Add the new max. If we were max, it is now lower, otherwie it cancels out.

        def change_happiness(self,amount, add_to_log = True):
            self.happiness += amount*self.get_trance_multiplier()
            if self.happiness < 0:
                self.happiness = 0

            log_string = ""
            if amount > 0:
                log_string = "+" + str(amount) + " Happiness"
            else:
                log_string = str(amount) + " Happiness"

            if self.get_trance_multiplier() != 1:
                log_string += "\nChange amplified by " + str(int((self.get_trance_multiplier()*100)-100)) + "% due to trance."

            if add_to_log and amount != 0:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                mc.log_event(display_name + ": " + log_string, "float_text_yellow")

        def change_love(self, amount, add_to_log = True, max_modified_to = None):
            log_string = ""
            amount = __builtin__.int(amount)
            if max_modified_to is not None and self.love + amount > max_modified_to:
                if amount != 0:
                    log_string += "Love limit reached for interaction. "
                amount = max_modified_to - self.love
                if amount < 0: #Never subtract love because of a cap, only limit how much they gain.
                    amount = 0


            self.love += amount
            if self.love < -100:
                self.love = -100
            elif self.love > 100:
                self.love = 100

            if amount > 0:
                log_string += "+" + str(amount) + " Love"
            else:
                log_string += str(amount) + " Love"

            if add_to_log and amount != 0:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                mc.log_event(display_name + ": " + log_string, "float_text_pink")

        def change_slut(self, amount, max_modified_to = None, add_to_log = True):
            return_report = "" #This is the string that is returned that will report what the final value of the change was.
            if max_modified_to is None:
                if amount > 0:
                    max_modified_to = 9999
                else:
                    max_modified_to = -9999

            if amount > 0:
                if amount + self.sluttiness > max_modified_to:
                    amount = max_modified_to - self.sluttiness
                    if amount < 0:
                        amount = 0

            if amount < 0:
                if amount + self.sluttiness < max_modified_to:
                    amount = max_modified_to - self.sluttiness
                    if amount > 0:
                        amount = 0

            if amount > 0:
                self.sluttiness += amount
                return_report = "+" + str(amount) + " Sluttiness"

            elif amount < 0:
                self.sluttiness += amount
                return_report = str(amount) + " Sluttiness"

            else: #It is exactly 0
                return_report = "No Effect on Sluttiness"

            if add_to_log:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                mc.log_event(display_name + ": " + return_report, "float_text_pink")

        def change_slut_temp(self, *args, **kwargs): #Adds the amount to our slut value. If over our max, add only to the max instead (but don't lower). If subtracting, don't go lower than 0.
            self.change_slut(*args, **kwargs) #Renamed change_slut_temp to change_slut, keeping this alias to avoid breaking mods where possible.


        def change_slut_core(self, amount, add_to_log = True, fire_event = True): #Exists only to help preserve mod support during the transition.
            self.change_slut(ammount, add_to_log)
            return

        def add_situational_slut(self, source, amount, description = ""):
            self.situational_sluttiness[source] = (amount,description)

        def clear_situational_slut(self, source):
            self.add_situational_slut(source, 0) #We don't actually ever care if we remove the key, we just want to set the amount to 0.

        def add_situational_obedience(self, source, amount, description = ""):
            if source in self.situational_obedience:
                difference = amount - self.situational_obedience[source][0]
                self.change_obedience(difference, add_to_log = False)
            else:
                self.change_obedience(amount, add_to_log = False)
            self.situational_obedience[source] = (amount,description)

        def clear_situational_obedience(self, source):
            self.add_situational_obedience(source, 0)

        def change_obedience(self,amount, add_to_log = True):
            self.obedience += amount
            if self.obedience < 0:
                self.obedience = 0
            log_string = ""
            if add_to_log and amount != 0: #If we don't know the title don't add it to the log, because we know nothing about the person
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                if amount > 0:
                    log_string = display_name + ": +" + str(amount) + " Obedience"
                else:
                    log_string = display_name + ": " + str(amount) + " Obedience"

                mc.log_event(log_string,"float_text_grey")

        def change_cha(self, amount, add_to_log = True):
            self.charisma += self.charisma_debt #Set our charisma to be our net score
            self.charisma_debt = 0 #We are currently holding no stat debt.

            self.charisma += amount #Adjust our stat now, may be positive or negative.
            if self.charisma < 0:
                self.charisma_debt = self.charisma #If we are less than 0 store it as a debt.
                self.charisma = 0

            log_string = ""
            if amount != 0 and add_to_log:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                if amount > 0:
                    log_string = display_name + ": +" + str(amount) + " Charisma"
                else:
                    log_string = display_name + ": " + str(amount) + " Charisma"

                mc.log_event(log_string, "float_text_grey")

        def change_int(self, amount, add_to_log = True):
            self.int += self.int_debt
            self.int_debt = 0

            self.int += amount
            if self.int < 0:
                self.int_debt = self.int
                self.int = 0

            log_string = ""

            if amount != 0 and add_to_log:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title

                if amount > 0:
                    log_string = display_name + ": +" + str(amount) + " Intelligence"
                else:
                    log_string = display_name + ": " + str(amount) + " Intelligence"

                mc.log_event(log_string, "float_text_grey")

        def change_focus(self, amount, add_to_log = True): #See charisma for full comments
            self.focus += self.focus_debt
            self.focus_debt = 0

            self.focus += amount
            if self.focus < 0:
                self.focus_debt = self.focus
                self.focus = 0

            log_string = ""

            if amount != 0 and add_to_log:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title

                if amount > 0:
                    log_string = display_name + ": +" + str(amount) + " Focus"
                else:
                    log_string = display_name + ": " + str(amount) + " Focus"


                mc.log_event(log_string, "float_text_grey")

        def change_hr_skill(self, amount, add_to_log = True):
            if amount + self.hr_skill < 0:
                amount = -self.hr_skill #Min 0
            self.hr_skill += amount

            log_string = ""
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title
            if amount > 0:
                log_string +=  display_name + ": +" + str(amount) + " HR Skill"
            else:
                log_string +=  display_name + ": " + str(amount) + " HR Skill"

            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_yellow")

        def change_market_skill(self, amount, add_to_log = True):
            if amount + self.market_skill < 0:
                amount = -self.market_skill #Min 0
            self.market_skill += amount

            log_string = ""
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title
            if amount > 0:
                log_string +=  display_name + ": +" + str(amount) + " Market Skill"
            else:
                log_string +=  display_name + ": " + str(amount) + " Market Skill"

            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_yellow")

        def change_research_skill(self, amount, add_to_log = True):
            if amount + self.research_skill < 0:
                amount = -self.research_skill #Min 0
            self.research_skill += amount

            log_string = ""
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title
            if amount > 0:
                log_string +=  display_name + ": +" + str(amount) + " Research Skill"
            else:
                log_string +=  display_name + ": " + str(amount) + " Research Skill"

            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_yellow")

        def change_production_skill(self, amount, add_to_log = True):
            if amount + self.production_skill < 0:
                amount = -self.production_skill #Min 0
            self.production_skill += amount

            log_string = ""
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title
            if amount > 0:
                log_string +=  display_name + ": +" + str(amount) + " Production Skill"
            else:
                log_string +=  display_name + ": " + str(amount) + " Production Skill"

            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_yellow")

        def change_supply_skill(self, amount, add_to_log = True):
            if amount + self.supply_skill < 0:
                amount = -self.supply_skill #Min 0
            self.supply_skill += amount

            log_string = ""
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title
            if amount > 0:
                log_string +=  display_name + ": +" + str(amount) + " Supply Skill"
            else:
                log_string +=  display_name + ": " + str(amount) + " Supply Skill"

            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_yellow")

        def change_sex_skill(self, skill_name, amount, add_to_log = True): #NOTE: We assume we pass a proper skill name here, otherwise we crash out.
            # ["Foreplay","Oral","Vaginal","Anal"]
            if amount + self.sex_skills[skill_name] < 0:
                amount = -self.sex_skills[skill_name] #At most we make it 0. No negative values.
            self.sex_skills[skill_name] += amount

            log_string = ""
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title
            if amount > 0:
                log_string +=  display_name + ": +" + str(amount) + " " + skill_name + " Skill"
            else:
                log_string +=  display_name + ": " + str(amount) + " " + skill_name + " Skill"

            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_yellow")
            return

        def change_arousal(self,amount, add_to_log = True):
            self.arousal += int(__builtin__.round(amount)) #Round it to an integer if it isn't one already.
            if self.arousal < 0:
                self.arousal = 0

            log_string = ""
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title

            if amount > 0:
                log_string = display_name + ": +" + str(amount) + " Arousal"
            else:
                log_string = display_name + ": " + str(amount) + " Arousal"

            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_red")

        def reset_arousal(self):
            self.arousal = 0

        def change_max_arousal(self, amount, add_to_log = True):
            if amount + self.max_arousal < 20:
                amount = -(self.max_arousal - 20)

            self.max_arousal += amount

            log_string = ""
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title

            if amount > 0:
                log_string = display_name + ": +" + str(amount) + " Max Arousal"
            else:
                log_string = display_name + ": " + str(amount) + " Max Arousal"

            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_red")

        def change_novelty(self, amount, add_to_log = True):
            amount = int(__builtin__.round(amount))

            log_string = ""
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title

            if amount + self.novelty > 100:
                amount = 100 - self.novelty
            elif amount + self.novelty < 0:
                amount = -self.novelty

            self.novelty += amount

            if amount > 0:
                log_string = display_name + ": +" + str(amount) + " Novelty"
            else:
                log_string = display_name + ": " + str(amount) + " Novelty" #TODO: Design a novelty token



            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_yellow")

        def change_energy(self, amount, add_to_log = True):
            amount = __builtin__.round(amount)
            self.energy += amount
            if self.energy > self.max_energy:
                self.energy = self.max_energy
            elif self.energy < 0:
                self.energy = 0

            log_string = ""
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title
            if amount > 0:
                log_string +=  display_name+ ": +" + str(amount) + " Energy"
            else:
                log_string +=  display_name + ": " + str(amount) + " Energy"
            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_yellow")
            return

        def change_max_energy(self, amount, add_to_log = True):
            amount = __builtin__.round(amount)
            self.max_energy += amount

            if self.energy > self.max_energy: #No having more energy than max
                self.energy = self.max_energy

            log_string = ""
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title
            if amount > 0:
                log_string +=  display_name + ": +" + str(amount) + " Max Energy"
            else:
                log_string +=  display_name + ": " + str(amount) + " Max Energy"
            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_yellow")
            return

        def review_outfit(self, dialogue = True, draw_person = True):
            if self.should_wear_uniform() and not self.is_wearing_uniform():
                self.wear_uniform()#Reset uniform
                if draw_person:
                    self.draw_person()
                if dialogue:
                    self.call_dialogue("clothing_review")

            elif not self.judge_outfit(self.outfit):
                self.apply_outfit()
                if draw_person:
                    self.draw_person()

                if dialogue:
                   self.call_dialogue("clothing_review")



        def judge_outfit(self, outfit, temp_sluttiness_boost = 0, use_taboos = True, as_underwear = False, as_overwear = False): #Judge an outfit and determine if it's too slutty or not. Can be used to judge other people's outfits to determine if she thinks they look like a slut.
            # temp_sluttiness can be used in situations (mainly crises) where an outfit is allowed to be temporarily more slutty than a girl is comfortable wearing all the time.
            #Returns true if the outfit is wearable, false otherwise
            if as_underwear or as_overwear:
                use_taboos = False

            if use_taboos and not (outfit.bra_covered() and outfit.panties_covered()) and "underwear_nudity" not in self.broken_taboos:
                taboo_modifier = "underwear_nudity"
            elif use_taboos and outfit.tits_visible() and "bare_tits" not in self.broken_taboos:
                taboo_modifier = "bare_tits"
            elif use_taboos and outfit.vagina_visible() and "bare_pussy" not in self.broken_taboos:
                taboo_modifier = "bare_pussy"
            else:
                taboo_modifier = None

            slut_require = outfit.slut_requirement
            if as_underwear:
                slut_require = outfit.get_underwear_slut_score()

            elif as_overwear:
                slut_require = outfit.get_overwear_slut_score()

            if (outfit.get_bra() or outfit.get_panties()) and not as_overwear: #Girls who like lingerie judge outfits with lingerie as less slutty than normal
                lingerie_bonus = 0
                if outfit.get_bra() and outfit.get_bra().slut_value > 2: #We consider underwear with an innate sluttiness of 3 or higher "lingerie" rather than just underwear.
                    lingerie_bonus += self.get_opinion_score("lingerie")
                if outfit.get_panties() and outfit.get_panties().slut_value > 2:
                    lingerie_bonus += self.get_opinion_score("lingerie")
                lingerie_bonus = __builtin__.int(lingerie_bonus*2) # Up to an 8 point swing in either direction
                slut_require += -lingerie_bonus #Treated as less slutty if she likes it, more slutty if she dislikes lingerie

            # Considers the outfit less slutty if she likes showing her tits and ass and that's what it would do.
            if outfit.vagina_visible() or (outfit.wearing_panties() and not outfit.panties_covered()):
                slut_require += -2*self.get_opinion_score("showing her ass")

            if outfit.tits_visible() or (outfit.wearing_bra() and not outfit.bra_covered()):
                slut_require += -2*self.get_opinion_score("showing her tits")


            if slut_require > (self.effective_sluttiness(taboo_modifier) + temp_sluttiness_boost): #Arousal is important for judging potential changes to her outfit while being stripped down during sex.
                return False
            else:
                return True

        def is_wearing_uniform(self): # Returns True if the clothing the girl is wearing contains all of the uniform clothing items. #TODO: may want to support more flexibility for over/underwear sets that had optional bits chosen by the girl.
            #May want to make this a Business side check. Make "is_valid_uniform" check like this against all uniforms available for the character. Would provide the flexiblity I mentioned above.
            if self.planned_uniform is None:
                return False #If no uniform is set you aren't wearing one at all.

            uniform_wardrobe = mc.business.get_uniform_wardrobe_for_person(self)
            matching_full = False
            full_set = False #Boolean used to track if we have at least one full set we _could_ have been wearing

            matching_overwear = False
            overwear_set = False #Tracks if we had at least one overwear we _could_ have been wearing

            matching_underwear = False
            underwear_set = False #Tracks if we had an underwear set we could have been wearing

            for potential_uniform in uniform_wardrobe.get_valid_outfit_list(): #Check if we match any of the full uniforms
                full_set = True
                if not matching_full:
                    matching_full = True #Assume they match, then find a counter example. When we do, break and try the next one.
                    for cloth in potential_uniform.generate_clothing_list():
                        if not self.outfit.has_clothing(cloth):
                            matching_full = False
                            break

            for potential_uniform in uniform_wardrobe.get_valid_overwear_sets_list(): #Check if we match the overwear and underwear sets.
                overwear_set = True
                if not matching_overwear:
                    matching_overwear = True
                    for cloth in potential_uniform.generate_clothing_list():
                        if not self.outfit.has_clothing(cloth):
                            matching_overwear = False
                            break

            for potential_uniform in uniform_wardrobe.get_valid_underwear_sets_list():
                underwear_set = True
                if not matching_underwear:
                    matching_underwear = True
                    for cloth in potential_uniform.generate_clothing_list():
                        if not self.outfit.has_clothing(cloth):
                            matching_underwear = False
                            break

            if matching_full:
                return True

            elif matching_overwear and matching_underwear:
                return True

            elif matching_overwear or matching_underwear: #Sometimes this is okay
                if matching_overwear and not underwear_set:
                    return True
                elif matching_underwear and not overwear_set:
                    return True

            return False

        def should_wear_uniform(self):
            #Check to see if we are: 1) Employed by the PC. 2) At work right now. 3) there is a uniform set for our department.
            employment_title = mc.business.get_employee_title(self)
            if employment_title != "None":
                if mc.business.is_open_for_business(): #We should be at work right now, so if there is a uniform we should wear it.
                    if mc.business.get_uniform_wardrobe(employment_title).get_count() > 0 or self.event_triggers_dict.get("forced_uniform", False): #Check to see if there's anything stored in the uniform section.
                        return True

            return False #If we fail to meet any of the above conditions we should return false.

        def wear_uniform(self): #Puts the girl into her uniform, if it exists.
            if self.planned_uniform is None:
                the_uniform = mc.business.get_uniform_wardrobe(mc.business.get_employee_title(self)).decide_on_uniform(self)
                if self.event_triggers_dict.get("forced_uniform", False):
                    the_uniform = self.event_triggers_dict.get("forced_uniform")
                self.set_uniform(the_uniform, False) #If we don't have a uniform planned for today get one.

            if self.planned_uniform is not None: #If our planned uniform is STILL None it means we are unable to construct a valid uniform. Only assign it as our outfit if we have managed to construct a uniform.
                self.apply_outfit(self.planned_uniform) #We apply clothing taboos to uniforms because the character is assumed to have seen them in them.

        def get_job_happiness_score(self):
            happy_points = self.happiness - 100 #Happiness over 100 gives a bonus to staying, happiness less than 100 gives a penalty
            happy_points += self.obedience - 95 #A more obedient character is more likely to stay, even if they're unhappy. Default characters can be a little disobedint without any problems.
            happy_points += self.salary - self.calculate_base_salary() #A real salary greater than her base is a bonus, less is a penalty. TODO: Make this dependent on salary fraction, not abosolute pay.

            if (day - self.event_triggers_dict.get("employed_since",0)) < 14:
                happy_points += 14 - (day - self.event_triggers_dict.get("employed_since",0)) #Employees are much less likely to quit over the first two weeks.
            return happy_points

        def get_no_condom_threshold(self, situational_modifier = 0):
            if self.has_role(pregnant_role) and self.event_triggers_dict.get("preg_knows", False):
                return 0 #You can't get more pregnant, so who cares?

            if self.has_role(breeder_role):
                return 0 #She _wants_ to get knocked up. This will probably trigger other dialogue as well.

            no_condom_threshold = 50 + (self.get_opinion_score("bareback sex") * -10) + situational_modifier
            if any(relationship in [sister_role,mother_role,aunt_role,cousin_role] for relationship in self.special_role):
                no_condom_threshold += 10

            if persistent.pregnancy_pref == 0:
                no_condom_threshold += 10 #If pregnancy content is being ignored we return to the baseline of 60
            elif self.on_birth_control: #If there is pregnancy content then a girl is less likely to want a condom when using BC, much more likely to want it when not using BC.
                no_condom_threshold -= 20

            return no_condom_threshold

        def wants_condom(self, situational_modifier = 0, use_taboos = True):
            taboo_modifier = 0
            if use_taboos and self.effective_sluttiness("condomless_sex") < self.get_no_condom_threshold(situational_modifier = situational_modifier):
                return True
            elif self.effective_sluttiness() < self.get_no_condom_threshold(situational_modifier = situational_modifier):
                return True
            else:
                return False

        def has_family_taboo(self): #A check to see if we should use an incest taboo modifier.
            if self.get_opinion_score("incest") > 0: #If she thinks incest is hot she doesn't have an incest taboo modifier. Maybe she should, but it should just be reduced? For now this is fine.
                return False

            elif self.is_family():
                return True

            return False

        def is_family(self):
            if any(relationship in [sister_role,mother_role,aunt_role,cousin_role] for relationship in self.special_role):
                return True

        def has_large_tits(self): #Returns true if the girl has large breasts. "D" cups and up are considered large enough for titfucking, swinging, etc.
            if self.tits == "D" or self.tits == "DD" or self.tits == "DDD" or self.tits == "E" or self.tits == "F" or self.tits == "FF":
                return True
            else:
                return False

        def wants_creampie(self): #Returns True if the girl is going to use dialogue where she wants you to creampie her, False if she's going to be angry about it. Used to help keep dialogue similar throughout events
            creampie_threshold = 75
            effective_slut = self.effective_sluttiness("creampie") + (10*self.get_opinion_score("creampies"))
            if self.on_birth_control:
                creampie_threshold += -20 #Much more willing to let you creampie her if she's on BC

            if affair_role in self.special_role:
                creampie_threshold += 5 - (10 * self.get_opinion_score("cheating on men"))
            elif self.relationship != "Single": # Less likely to want to be creampied if she's in a relationship, but cares less if you're officially cheating.
                creampie_threshold += 15 - (10 * self.get_opinion_score("cheating on men"))

            if girlfriend_role in self.special_role:
                creampie_threshold += -(10 + (5*self.get_opinion_score("being submissive"))) #Desire to be a "good wife"

            if self.is_family():
                creampie_threshold += 10 - (10 * self.get_opinion_score("incest"))

            if effective_slut >= creampie_threshold or self.event_triggers_dict.get("preg_knows", False):
                return True

            return False

        def calculate_realistic_fertility(self):
            day_difference = self.days_from_ideal_fertility() # Gets the distance between the current day and the ideal fertile day.
            multiplier = 2 - (float(day_difference)/10.0) # The multiplier is 2 when the day difference is 0, 0.5 when the day difference is 15.
            effective_fertility = self.fertility_percent * multiplier
            return effective_fertility

        def days_from_ideal_fertility(self):
            day_difference = abs((day % 30) - self.ideal_fertile_day)
            if day_difference > 15:
                day_difference = 30 - day_difference #Wrap around to get correct distance between months.
            return day_difference

        def fertility_cycle_string(self): #Turns the difference of days from her ideal fertile day into a string
            day_difference = self.days_from_ideal_fertility
            if day_difference >= 12:
                return "Very Safe"
            elif day_difference >= 8:
                return "Safe"
            elif day_difference >= 3:
                return "Normal"
            else:
                return "Risky"

        def update_birth_control_knowledge(self, force_known_state = None, force_known_day = None): #Called any time a girl gives you information about her BC. Allows for an up to date detailed info screen that doesn't give more than you know
            if force_known_state is None: #Useful when you an event changes a girls BC and you can expect that she's not going to be on birth control the next day.
                known_state = self.on_birth_control
            else:
                known_state = force_known_day

            if force_known_day is None:
                known_day = day
            else:
                known_day = force_known_day

            self.event_triggers_dict["birth_control_status"] = known_state
            self.event_triggers_dict["birth_control_known_day"] = known_day


        def effective_sluttiness(self, taboos = None): #Used in sex scenes where the girl will be more aroused, making it easier for her to be seduced.
            if taboos is None:
                taboos = []
            elif not isinstance(taboos, list): #Handles handing over a single item without pre-wrapping it for "iteration".
                taboos = [taboos]

            return_amount = __builtin__.int(self.sluttiness + (self.arousal/4))

            for taboo in taboos:
                if taboo not in self.broken_taboos: #If any of the taboo handed over are not already broken this person has a -15 effective sluttiness.
                    return_amount += -10
                    break #Only appies once, so break once the mallus is applied.


            for source in self.situational_sluttiness:
                return_amount += self.situational_sluttiness[source][0]

            return return_amount

        def run_orgasm(self, show_dialogue = True, force_trance = False, trance_chance_modifier = 0, add_to_log = True, sluttiness_increase_limit = 30, reset_arousal = True, fire_event = True):
            self.change_slut(1, sluttiness_increase_limit, add_to_log = add_to_log)
            mc.listener_system.fire_event("girl_climax", the_person = self)
            if renpy.random.randint(0,100) < self.suggestibility + trance_chance_modifier or force_trance:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title

                if not self.has_role(trance_role):
                    self.add_role(trance_role)
                    if add_to_log:
                        mc.log_event(display_name + " sinks into a trance!", "float_text_red")
                    if show_dialogue:
                        renpy.say("", self.possessive_title + "'s eyes lose focus slightly as she slips into a climax induced trance.")

                elif self.has_exact_role(trance_role):
                    self.remove_role(trance_role)
                    self.add_role(heavy_trance_role)
                    if add_to_log:
                        mc.log_event(display_name + " sinks deeper into a trance!", "float_text_red")
                    if show_dialogue:
                        renpy.say("", self.possessive_title + " seems to lose all focus as her brain slips deeper into a post-orgasm trance.")


                elif self.has_exact_role(heavy_trance_role):
                    self.remove_role(heavy_trance_role)
                    self.add_role(very_heavy_trance_role)
                    if add_to_log:
                        mc.log_event(display_name + " sinks deeper into a trance!", "float_text_red")
                    if show_dialogue:
                        renpy.say("", self.possessive_title + " eyes glaze over, and she sinks completely into a cum addled trance.")

            if reset_arousal:
                self.reset_arousal() #TODO: Decide if resetting should only halve it, like making a girl cum yoruself.

        def get_trance_multiplier(self):
            if self.has_exact_role(trance_role):
                return 1.5
            elif self.has_exact_role(heavy_trance_role):
                return 2.0
            elif self.has_exact_role(very_heavy_trance_role):
                return 3.0
            else:
                return 1.0


        def cum_in_mouth(self, add_to_record = True): #Add the appropriate stuff to their current outfit, and peform any personal checks if rquired.
            mc.listener_system.fire_event("sex_cum_mouth", the_person = self)
            if self.outfit.can_add_accessory(mouth_cum):
                the_cumshot = mouth_cum.get_copy()
                the_cumshot.layer = 0
                self.outfit.add_accessory(the_cumshot)

            self.change_slut(self.get_opinion_score("drinking cum"))
            self.change_happiness(5*self.get_opinion_score("drinking cum"))
            self.discover_opinion("drinking cum")

            if add_to_record:
                self.sex_record["Cum in Mouth"] += 1


        def cum_in_vagina(self, add_to_record = True):
            mc.listener_system.fire_event("sex_cum_vagina", the_person = self)
            if self.outfit.can_add_accessory(creampie_cum):
                the_cumshot = creampie_cum.get_copy()
                the_cumshot.layer = 0
                self.outfit.add_accessory(the_cumshot)

            slut_change_amount =  self.get_opinion_score("creampies")

            if self.wants_creampie():
                self.change_happiness(5*self.get_opinion_score("creampies"))
            else:
                self.change_happiness(-5 + (5*self.get_opinion_score("creampies")))
                self.change_love(-2 + self.get_opinion_score("creampies"))
                slut_change_amount += self.get_opinion_score("being_submissive")

            self.change_slut(slut_change_amount)
            self.discover_opinion("creampies")

            if add_to_record:
                self.sex_record["Vaginal Creampies"] += 1

            # Pregnancy Check #
            if persistent.pregnancy_pref > 0 and pregnant_role not in self.special_role:
                if persistent.pregnancy_pref == 1 and self.on_birth_control: #Establish how likely her birth contorl is to work (if needed, and if present)
                    bc_percent = 100 - self.bc_penalty
                elif persistent.pregnancy_pref == 2 and self.on_birth_control:
                    bc_percent = 90 - self.bc_penalty
                else:
                    bc_percent = 0

                preg_chance = renpy.random.randint(0,100)
                bc_chance = renpy.random.randint(0,100)
                if persistent.pregnancy_pref == 2: # On realistic pregnancy a girls chance to become pregnant fluctuates over the month.
                    modified_fertility = self.calculate_realistic_fertility()
                else:
                    modified_fertility = self.fertility_percent

                if preg_chance < modified_fertility and pregnant_role not in self.special_role: #There's a chance she's pregnant
                    if bc_chance >= bc_percent : # Birth control failed to prevent the pregnancy
                        become_pregnant(self) #Function in role_pregnant establishes all of the pregnancy related variables and events.


        def cum_in_ass(self, add_to_record = True):
            mc.listener_system.fire_event("sex_cum_ass", the_person = self)
            #TODO: Add an anal specific cumshot once we have renders for it.
            if self.outfit.can_add_accessory(creampie_cum):
                the_cumshot = creampie_cum.get_copy()
                the_cumshot.layer = 0
                self.outfit.add_accessory(the_cumshot)
            self.change_slut(self.get_opinion_score("anal creampies"))
            self.change_happiness(5*self.get_opinion_score("anal creampies"))
            self.discover_opinion("anal creampies")

            if add_to_record:
                self.sex_record["Anal Creampies"] += 1

        def cum_on_face(self, add_to_record = True):
            if self.outfit.can_add_accessory(face_cum):
                the_cumshot = face_cum.get_copy()
                the_cumshot.layer = 0
                self.outfit.add_accessory(the_cumshot)

            self.change_slut(self.get_opinion_score("cum facials"))
            self.change_happiness(5*self.get_opinion_score("cum facials"))
            self.discover_opinion("cum facials")

            self.change_slut(self.get_opinion_score("being covered in cum"))
            self.change_happiness(5*self.get_opinion_score("being covered in cum"))
            self.discover_opinion("being covered in cum")

            if add_to_record:
                self.sex_record["Cum Facials"] += 1

        def cum_on_tits(self, add_to_record = True):
            if self.outfit.can_add_accessory(tits_cum):
                the_cumshot = tits_cum.get_copy()
                if self.outfit.get_upper_visible():
                    top_layer = self.outfit.get_upper_visible()[0].layer #Get the top most pice of clothing and get it's layer.
                else:
                    top_layer = -1
                the_cumshot.layer = top_layer+1 #The cumshot lives on a layer it hit, above the one it hit. Accessories are drawn first in the hirearchy, so they have to be on a level higehr than what they hit.
                self.outfit.add_accessory(the_cumshot)

            self.change_slut(self.get_opinion_score("being covered in cum"))
            self.change_happiness(5*self.get_opinion_score("being covered in cum"))
            self.discover_opinion("being covered in cum")

            if add_to_record:
                self.sex_record["Cum Covered"] += 1

        def cum_on_stomach(self, add_to_record = True):
            if self.outfit.can_add_accessory(stomach_cum):
                the_cumshot = stomach_cum.get_copy()
                if self.outfit.get_upper_visible():
                    top_layer = self.outfit.get_upper_visible()[0].layer #Get the top most pice of clothing and get it's layer.
                else:
                    top_layer = -1
                the_cumshot.layer = top_layer+1 #The cumshot lives on a layer it hit, above the one it hit. Accessories are drawn first in the hirearchy, so they have to be on a level higehr than what they hit.
                self.outfit.add_accessory(the_cumshot)

            self.change_slut(self.get_opinion_score("being covered in cum"))
            self.change_happiness(5*self.get_opinion_score("being covered in cum"))
            self.discover_opinion("being covered in cum")

            if add_to_record:
                self.sex_record["Cum Covered"] += 1

        def cum_on_ass(self, add_to_record = True):
            if self.outfit.can_add_accessory(ass_cum):
                the_cumshot = ass_cum.get_copy()
                if self.outfit.get_lower_visible():
                    top_layer = self.outfit.get_lower_visible()[0].layer #Get the top most pice of clothing and get it's layer.
                else:
                    top_layer = -1
                the_cumshot.layer = top_layer+1 #The cumshot lives on a layer it hit, above the one it hit. Accessories are drawn first in the hirearchy, so they have to be on a level higehr than what they hit.
                self.outfit.add_accessory(the_cumshot)

            self.change_slut(self.get_opinion_score("being covered in cum"))
            self.change_happiness(5*self.get_opinion_score("being covered in cum"))
            self.discover_opinion("being covered in cum")

            if add_to_record:
                self.sex_record["Cum Covered"] += 1

        def change_salary(self, amount, add_to_log = True):
            amount = __builtin__.round(amount)
            self.salary += amount
            if self.salary < 0:
                self.salary = 0

            log_string = ""
            display_name = self.create_formatted_title("???")
            if self.title:
                display_name = self.title
            if amount > 0:
                log_string = display_name + ": +$" + str(amount) + "/Day"
            else:
                log_string = display_name + ": -$" + str(-amount) + "/Day"

            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_green")

        #TODO: We should add an "expected salary modifier" field, so people who are interns don't get angry about it.
        def calculate_base_salary(self): #returns the default value this person should be worth on a per day basis.
            return __builtin__.int((self.int + self.focus + self.charisma)*2 + (self.hr_skill + self.market_skill + self.research_skill + self.production_skill + self.supply_skill) * self.salary_modifier)

        def set_schedule(self, the_location, the_days = None, the_times = None):
            self.schedule.set_schedule(the_location, the_days, the_times)

        def set_override_schedule(self, the_location, the_days = None, the_times = None):
            self.override_schedule.set_schedule(the_location, the_days, the_times)

        def copy_schedule(self): #Returns a properly formatted dict without references to the current schedule.
            return self.schedule.get_copy()
            #TODO: Should this return some sort of overlapped work/life schedule?

        def get_destination(self, specified_day = None, specified_time = None): #TODO: Needs to check against personal and work schedule
            override_return = self.override_schedule.get_destination(specified_day, specified_time)
            if override_return is not None:
                return override_return

            work_return = self.job.schedule.get_destination(specified_day, specified_time)
            if work_return is not None:
                return work_return #our job is telling us to be somewhere, so go there

            return self.schedule.get_destination(specified_day, specified_time) #Otherwise, go where we want.

        def get_next_destination(self):
            override_return = self.override_schedule.get_next_destination()
            if override_return is not None:
                return override_return
            work_return = self.job.schedule.get_next_destination()
            if work_return is not None:
                return work_return
            else:
                return self.schedule.get_next_destination()

        def person_meets_requirements(self, slut_required = 0, core_slut_required = 0, obedience_required = 0, obedience_max = 2000, love_required = -200):
            if self.sluttiness >= slut_required and self.obedience >= obedience_required and self.obedience <= obedience_max and self.love >= love_required:
                return True
            return False

        def valid_role_actions(self):
            count = 0
            for role in self.special_role:
                for act in role.actions:
                    if act.is_action_enabled(self) or act.is_disabled_slug_shown(self): #We should also check if a non-action disabled slug would be available so that the player can check what the requirement would be.
                        count += 1
                return count

        def create_formatted_title(self, the_title):
            formatted_title = "{color=" + self.char.who_args["color"] + "}" + "{font=" + self.char.what_args["font"] + "}" + the_title + "{/font}{/color}"
            return formatted_title

        def set_title(self, new_title): #Takes the given title and formats it so that it will use the characters font colours when the_person.title is used.
            self.char.name = new_title #This ensures the dialogue name is correct for the new title.
            self.title = self.create_formatted_title(new_title)

        def set_possessive_title(self, new_title):
            self.possessive_title = self.create_formatted_title(new_title)

        def set_mc_title(self, new_title):
            self.mc_title = new_title

        def personalise_text(self, what):
            for text_modifier in self.text_modifiers:
                what = text_modifier(self, what)

            return what

        def has_job(self, the_job):
            if self.job and self.job == the_job:
                return True
            return False


        def add_job(self, new_job, job_known = True): #Start a new job, quitting your old one if nessesary #TODO: REname this to "change_job"?
            if self.job and new_job == self.job: #Don't do anything if we already have this job.
                return

            if self.job:
                if self.job.quit_function:
                    self.job.quit_function(self)

                if not new_job.job_role == self.job.job_role: # If the new job has the same job role we don't change roles (which might otherwise remove linked roles.
                    self.remove_role(self.job.job_role)


            if new_job.hire_function:
                new_job.hire_function(self)

            if (self.job and not new_job.job_role == self.job.job_role) or not self.job: #Only add the role if it differs from our current job.
                self.add_role(new_job.job_role)

            self.job = new_job
            self.event_triggers_dict["job_known"] = job_known

        def quit_job(self, job_known = True): #Quit and become unemployed
            self.add_job(unemployed_job)


        def add_role(self, the_role):
            self.special_role.append(the_role)

        def remove_role(self, the_role, remove_all = False, remove_linked = True):
            if the_role in self.special_role:
                self.special_role.remove(the_role)
                if remove_linked:
                    for linked_role in the_role.linked_roles:
                        self.remove_role(linked_role, remove_all, remove_linked)
                if remove_all:
                    self.remove_role(the_role, remove_all, remove_linked)

        def has_role(self, the_role):
            if the_role in self.special_role:
                return True
            else:
                for a_role in self.special_role:
                    if a_role.check_looks_like(the_role):
                        return True

            return False

        def has_exact_role(self, the_role): #As has_role, but checks against all roles and all of their looks_like roles.
            if the_role in self.special_role:
                return True
            else:
                return False

        def get_role_reference(self, the_role):
            for role in self.special_role:
                if the_role == role:
                    return role
            return None

        def get_role_reference_by_name(self, the_role):
            for role in self.special_role:
                if role.role_name == the_role:
                    return role
            return None

        def has_queued_event(self, the_event):
            for an_event in self.on_talk_event_list:
                if an_event == the_event:
                    return True

            for an_event in self.on_room_enter_event_list:
                if an_event == the_event:
                    return True

            return False

        def has_queued_event_with_name(self, the_name):
            for an_event in self.on_talk_event_list:
                if an_event.name == the_name:
                    return True

            for an_event in self.on_room_enter_event_list:
                if an_event.name == the_name:
                    return True

            return False

        def add_infraction(self, the_infraction, add_to_log = True, require_policy = True):
            if office_punishment.is_active() or not require_policy:
                self.infractions.append(the_infraction)
                if add_to_log:
                    display_name = self.create_formatted_title("???")
                    if self.title:
                        display_name = self.title
                    mc.log_event(display_name + " committed infraction: " + the_infraction.name + ", Severity " + str(the_infraction.severity), "float_text_grey")

        def remove_infraction(self, the_infraction):
            if the_infraction in self.infractions:
                self.infractions.remove(the_infraction)

        def set_eye_colour(self, new_colour):
            new_colour = Color(rgb=(new_colour.rgb)) #Make sure we don't have any alpha problems.
            eye_colour_name = closest_colour(new_colour).capitalize()
            eye_colour_list = [new_colour.rgb[0], new_colour.rgb[1], new_colour.rgb[2], 1.0]

            self.eyes = [eye_colour_name, eye_colour_list]

        def set_hair_colour(self, new_colour, change_pubes = True, darken_pubes_amount = 0.07):
            #NOTE: new_colour should be a Ren'py colour.
            new_colour = Color(rgb=(new_colour.rgb)) #Make sure we don't have any alpha problems.
            hair_colour_name = closest_colour(new_colour).capitalize()
            hair_colour_list = [new_colour.rgb[0], new_colour.rgb[1], new_colour.rgb[2], 1.0]

            self.hair_colour = [hair_colour_name, hair_colour_list]

            if change_pubes:
                pubes_colour = new_colour.shade(1.0-darken_pubes_amount)
                self.pubes_colour = [pubes_colour.rgb[0], pubes_colour.rgb[1], pubes_colour.rgb[2], 1.0]
                self.pubes_colour = pubes_colour
            self.hair_style.colour = hair_colour_list

        def get_milk_trait(self): # Generates a milk trait that can be used any time you harvest lactating milk. #TODO: Add ways to give this trait augments, like +duration or it suppresses side effects.
            milk_trait = SerumTrait(self.title + "'s Breast Milk",
                "Fresh breast milk produced by " +  self.possessive_title + ". Valuable to the right sort of person.",
                sexual_aspect = 2, medical_aspect = 2)
            return milk_trait
