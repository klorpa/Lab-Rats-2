#How the new position code is set up:
#Each clothing set now has a dictionary of images. The only one that is required is "standing", which is used when you are talking to the person most of the time.
#Each position has a "position_tag". When you start having sex with someone the draw_person code will check it's dictionaryto see if it has a position_tag entry. If yes, it uses that set.
#Otherwise, it uses the default standing images. Right now, this should have changed absolutely nothing about the way the game works.

init -2 python:

    import os
    import copy
    import math
    import __builtin__
    import xml.etree.ElementTree as ET
    import time
    import zipfile
#    import shader

    config.image_cache_size = 16
    config.layers.insert(1,"Active") ## The "Active" layer is used to display the girls images when you talk to them. The next two lines signal it is to be hidden when you bring up the menu and when you change contexts (like calling a screen)
    config.menu_clear_layers.append("Active")
    config.context_clear_layers.append("Active")
    config.has_autosave = False
    config.autosave_frequency = None
    config.has_quicksave = True
    config.rollback_enabled = True

    if persistent.colour_palette is None:
        persistent.colour_palette = [[1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1]]

    config.autoreload = False

    #config.debug_text_overflow = True
    config.debug_text_overflow = False #If enabled finds locations with text overflow. Turns out I have a lot, kind of blows up when enabled and generates a large text file. A problem for another day.

    config.debug_image_cache = True
    config.debug = True

    # THIS IS WHAT PREVENTS IT FROM INDEXING IMAGES
    # SEE 00images.rpy for where this is created
    config.images_directory = None

    preferences.gl_tearing = True ## Prevents juttery animation with text while using advanced shaders to display images


    def get_obedience_plaintext(obedience_amount):
        obedience_string = "ERROR - Please Tell Vren!"
        if obedience_amount < 50: #49 or less
            obedience_string = "Completely Wild"

        elif obedience_amount < 70: #50 to 69
            obedience_string = "Disobedient"

        elif obedience_amount < 95: #70 to 94
            obedience_string = "Free Spirited"

        elif obedience_amount < 105: #95 to 104
            obedience_string = "Respectful"

        elif obedience_amount < 130: #105 to 129
            obedience_string = "Loyal"

        elif obedience_amount < 150: #130 to 149
            obedience_string = "Docile"

        else: #150 or more
            obedience_string = "Subservient"

        return obedience_string

    def format_titles(the_person):
        person_title = the_person.title
        if person_title is None:
            person_title = "???"
        return_title = "{color=" + the_person.char.who_args["color"] + "}" + "{font=" + the_person.char.what_args["font"] + "}" + person_title + "{/font}{/color}"
        return return_title


    def get_coloured_arrow(direction):
        if direction < 0:
            return "{image=gui/heart/Red_Down.png}"

        elif direction > 0:
            return "{image=gui/heart/Green_Up.png}"

        else:
            return "{image=gui/heart/Grey_Steady.png}"

    def get_red_heart(sluttiness): #A recursive function, feet it a sluttiness and it will return a string of all red heart images for it. Heatrts taht are entirely empty are left out.
        the_final_string = ""
        if sluttiness >= 20:
            the_final_string += "{image=gui/heart/red_heart.png}"
            the_final_string += get_red_heart(sluttiness - 20) #Call it recursively if we might have another heart after this.
        elif sluttiness >= 15:
            the_final_string += "{image=gui/heart/three_quarter_red_quarter_empty_heart.png}"
        elif sluttiness >= 10:
            the_final_string += "{image=gui/heart/half_red_half_empty_heart.png}"
        elif sluttiness >= 5:
            the_final_string += "{image=gui/heart/quarter_red_three_quarter_empty_heart.png}"

        return the_final_string

    def get_gold_heart(sluttiness):
        the_final_string = ""
        if sluttiness >= 20:
            the_final_string += "{image=gui/heart/gold_heart.png}"
            the_final_string += get_gold_heart(sluttiness - 20) #Call it recursively if we might have another heart after this.
        elif sluttiness >= 15:
            the_final_string += "{image=gui/heart/three_quarter_gold_quarter_empty_heart.png}"
        elif sluttiness >= 10:
            the_final_string += "{image=gui/heart/half_gold_half_empty_heart.png}"
        elif sluttiness >= 5:
            the_final_string += "{image=gui/heart/quarter_gold_three_quarter_empty_heart.png}"

        return the_final_string


    def get_heart_image_list(the_person): ##Returns a formatted string that will add coloured hearts in line with text, perfect for menu choices, ect.
        heart_string = "{image=" + get_individual_heart(the_person.core_sluttiness, the_person.sluttiness, the_person.core_sluttiness+the_person.suggestibility) + "}"
        heart_string += "{image=" + get_individual_heart(the_person.core_sluttiness-20, the_person.sluttiness-20, the_person.core_sluttiness+the_person.suggestibility-20) + "}"
        heart_string += "{image=" + get_individual_heart(the_person.core_sluttiness-40, the_person.sluttiness-40, the_person.core_sluttiness+the_person.suggestibility-40) + "}"
        heart_string += "{image=" + get_individual_heart(the_person.core_sluttiness-60, the_person.sluttiness-60, the_person.core_sluttiness+the_person.suggestibility-60) + "}"
        heart_string += "{image=" + get_individual_heart(the_person.core_sluttiness-80, the_person.sluttiness-80, the_person.core_sluttiness+the_person.suggestibility-80) + "}"

        # if the_person.suggestibility <= 0:
        #     heart_string += "{image=gui/heart/Grey_Steady.png}"
        # elif the_person.sluttiness > the_person.core_sluttiness:
        #     heart_string += "{image=gui/heart/Green_Up.png}"
        # elif the_person.sluttiness < the_person.core_sluttiness:
        #     heart_string += "{image=gui/heart/Red_Down.png}"
        # else:
        #     heart_string += "{image=gui/heart/Grey_Steady.png}"
        return heart_string


    def get_individual_heart(core_slut, temp_slut, suggest_slut): #Give this the core, temp, core+suggest slut, minus 20*(current heart-1) each and it will find out the current heart status for that chunk of the heart array.
        image_string = "gui/heart/"
        #suggest_slut += 10 #Add 10, which is the default limit to temp slut if they have no serum in them. #No longer added, testing more direct way of increasing sluttiness.
        #None of the core heart statuses were reached. We must be in a duel or tri-colour heart state.
        if core_slut < 5:
            #There is no gold to draw.
            if temp_slut < 5:
                #There's no temp to draw either.
                if suggest_slut < 5:
                    image_string += "empty_heart.png"
                    #can't happen, we checked for this above, it's a pure heart.

                elif suggest_slut < 10:
                    #It's a quarter grey, three quarter empty
                    image_string += "quarter_grey_three_quarter_empty_heart.png"

                elif suggest_slut < 15:
                    #It's half grey, half empty
                    image_string += "half_grey_half_empty_heart.png"

                elif suggest_slut < 20:
                    #It's three quarters grey, 1 quarter empty
                    image_string += "three_quarter_grey_quarter_empty_heart.png"

                else:
                    image_string += "grey_heart.png"

            elif temp_slut < 10:
                #It's a quarter red and...
                if suggest_slut < 10:
                    #There's no suggest to draw, the rest is empty.
                    image_string += "quarter_red_three_quarter_empty_heart.png"

                elif suggest_slut < 15:
                    #it's got a half grey, then empty
                    image_string += "quarter_red_quarter_grey_half_empty_heart.png"

                elif suggest_slut < 20:
                    #the rest is grey
                    image_string += "quarter_red_half_grey_quarter_empty_heart.png"

                else:
                    #It's three quarters grey
                    image_string += "quarter_red_three_quarter_grey_heart.png"

            elif temp_slut < 15:
                #It's two quarters red and...
                if suggest_slut < 15:
                    # Nothing, it's half red, half empty
                    image_string += "half_red_half_empty_heart.png"

                elif suggest_slut < 20:
                    # half red, quarter grey, quarter empty
                    image_string += "half_red_quarter_grey_quarter_empty_heart.png"

                else:
                    # half red, half grey
                    image_string += "half_red_half_grey_heart.png"

            elif temp_slut < 20:
                #It's three quarters red and...
                if suggest_slut < 15:
                    # three quarters red and 1 empty
                    image_string += "three_quarter_red_quarter_empty_heart.png"

                else:
                    # three quarters red and 1 grey
                    image_string += "three_quarter_red_quarter_grey_heart.png"

            else:
                image_string += "red_heart.png"

        elif core_slut < 10:
            #It fits in the 5 catagory
            if temp_slut < 10:
                #There's no temp slut worth worrying about
                if suggest_slut < 10:
                    # quarter gold, rest empty.
                    image_string += "quarter_gold_three_quarter_empty_heart.png"

                elif suggest_slut < 15:
                    #quarter gold, quarter grey, empty.
                    image_string += "quarter_gold_quarter_grey_half_empty_heart.png"

                elif suggest_slut < 20:
                    #quarter gold, half grey, empty
                    image_string += "quarter_gold_half_grey_quarter_empty_heart.png"

                else:
                    #quarter gold, rest grey
                    image_string += "quarter_gold_three_quarter_grey_heart.png"

            elif temp_slut < 15:
                #quarter gold, quarter red, and...
                if suggest_slut < 15:
                    #quarter gold, quarter red, rest empty
                    image_string += "quarter_gold_quarter_red_half_empty_heart.png"
                elif suggest_slut < 20:
                    #quarter gold, quarter red, quarter grey, rest empty
                    image_string += "quarter_gold_quarter_red_quarter_grey_quarter_empty_heart.png"
                else:
                    #quarter gold, quarter red, half grey
                    image_string += "quarter_gold_quarter_red_half_grey_heart.png"

            elif temp_slut < 20:
                #quarter gold, half red, and..
                if suggest_slut < 20:
                    #quarter gold, half red, empty
                    image_string += "quarter_gold_half_red_quarter_empty_heart.png"
                else:
                    #quarter gold, half red, quarter grey
                    image_string += "quarter_gold_half_red_quarter_grey_heart.png"

            else:
                #quarter gold, rest red
                image_string += "quarter_gold_three_quarter_red_heart.png"

        elif core_slut < 15:
            #It fits in the 10 catagory, half is gold
            if temp_slut < 15:
                #No temp slut
                if suggest_slut < 15:
                    #half gold, rest empty
                    image_string += "half_gold_half_empty_heart.png"
                elif suggest_slut < 20:
                    # half gold, quarter grey, empty
                    image_string += "half_gold_quarter_grey_quarter_empty_heart.png"
                else:
                    #Half gold, half grey
                    image_string += "half_gold_half_grey_heart.png"
            elif temp_slut < 20:
                #half gold, quarter red...
                if suggest_slut < 20:
                    #half gold, quarter red, rest empty
                    image_string += "half_gold_quarter_red_quarter_empty_heart.png"
                else:
                    #half gold, quarter red, rest grey
                    image_string += "half_gold_quarter_red_quarter_grey_heart.png"
            else:
                #half gold, half red
                image_string += "half_gold_half_red_heart.png"

        elif core_slut < 20:
            #three quarters gold and..
            if temp_slut < 20:
                #No temp slut
                if suggest_slut < 20:
                    #three quarters gold, rest empty
                    image_string += "three_quarter_gold_quarter_empty_heart.png"
                else:
                    #three quarters gold, rest grey
                    image_string += "three_quarter_gold_quarter_grey_heart.png"
            else:
                image_string += "three_quarter_gold_quarter_red_heart.png"
                #three quarters gold, rest red

        else:
            image_string += "gold_heart.png"

        return image_string

    def opinion_score_to_string(the_score): #Takes an opinion score and puts it into a plain string.
        if the_score == -2:
            return "hates"

        elif the_score == -1:
            return "dislikes"

        elif the_score == 0:
            return "has no opinion on"

        elif the_score == 1:
            return "likes"

        else: #the_score == 2:
            return "loves"

    def SO_relationship_to_title(relationship_string): #Takes a character relationship (Girlfriend, Fiancée, Married) and returns the male equivalent
        if relationship_string == "Girlfriend":
            return "boyfriend"
        elif relationship_string == "Fiancée":
            return "fiancé"
        elif relationship_string == "Married":
            return "husband"
        else:
            return "ERROR - relationship incorrectly defined"

    class Business(renpy.store.object):
        # main jobs to start with:
        # 1) buying raw supplies.
        # 2) researching new serums.
        # 2a) The player (only) designs new serums to be researched.
        # 3) working in the lab to produce serums.
        # 4) Working in marketing. Increases volumn you can sell, and max price you can sell for.
        # 5) Packaging and selling serums that have been produced.
        # 6) General secretary work. Starts at none needed, grows as your company does (requires an "HR", eventually). Maybe a general % effectivness rating.
        def __init__(self, name, m_div, p_div, r_div, s_div, h_div):
            self.name = name
            self.funds = 1000 #Your starting wealth.

            self.bankrupt_days = 0 #How many days you've been bankrupt. If it hits the max value you lose.
            self.max_bankrupt_days = 3 #How many days you can be negative without loosing the game. Can be increased through research.

            self.m_div = m_div #The phsyical locations of all of the teams, so you can move to different offices in the future.
            self.p_div = p_div
            self.r_div = r_div
            self.s_div = s_div
            self.h_div = h_div

            #Uniforms are stored as a wardrobe specific to each department. There is also a company wide wardrobe that can be accessed.
#            self.all_uniform = Wardrobe(self.name + " All Wardrobe")
            self.m_uniform = Wardrobe(self.name + " Marketing Wardrobe")
            self.p_uniform = Wardrobe(self.name + " Production Wardrobe")
            self.r_uniform = Wardrobe(self.name + " Research Wardrobe")
            self.s_uniform = Wardrobe(self.name + " Supply Wardrobe")
            self.h_uniform = Wardrobe(self.name + " HR Wardrobe")
            self.all_uniform = Wardrobe(self.name + " Shared Uniform Wardrobe")

            self.m_serum = None #These are the serums given to the different departments if the daily serum dosage policy is researched.
            self.p_serum = None
            self.r_serum = None
            self.s_serum = None
            self.h_serum = None

            self.research_team = [] #Researches new serums that the player designs, does theoretical research into future designs, or improves old serums slightly over time
            self.market_team = [] # Increases company marketability. Raises max price serum can be sold for, and max volumn that can be sold.
            self.supply_team = [] # Buys the raw supplies used by the other departments.
            self.production_team = [] # Physically makes the serum and sends it off to be sold.
            self.hr_team = [] # Manages everyone else and improves effectiveness. Needed as company grows.

            self.head_researcher = None #A reference to the head researcher is stored here, for use in important events.

            self.max_employee_count = 5

            self.supply_count = 0
            self.supply_goal = 250
            self.auto_sell_threshold = None
            self.marketability = 0
            #self.production_points = 0 Use to be used to store partial progress on serum. is now stored in the assembly line array
            self.team_effectiveness = 100 #Ranges from 50 (Chaotic, everyone functions at 50% speed) to 200 (masterfully organized). Normal levels are 100, special traits needed to raise it higher.
            self.effectiveness_cap = 100 #Max cap, can be raised.

            self.research_tier = 0 #The tier of research the main charcter has unlocked with storyline events. 0 is starting, 3 is max.

            self.serum_designs = [] #Holds serum designs that you have researched.
            self.active_research_design = None #The current research (serum design or serum trait) the business is working on

            self.batch_size = 5 #How many serums are produced in each production batch
            self.production_lines = 2 #How many different production lines the player has access to.
            self.serum_production_array = {} #This dict will hold tuples of int(line number):[SerumDesign, int(weight), int(production points), int(autosell)]


            self.inventory = SerumInventory([])
            self.sale_inventory = SerumInventory([])

            self.policy_list = [] #This is a list of Policy objects.

            self.message_list = [] #This list of strings is shown at the end of each day on the business update screen. Cleared each day.
            self.counted_message_list = {} #This is a dict holding the count of each message stored in it. Used when you want to have a message that is counted and the total shown at the end of the day.
            self.production_potential = 0 #How many production points the team was capable of
            self.supplies_purchased = 0
            self.production_used = 0 #How many production points were actually used to make something.
            self.research_produced = 0 #How much research the team produced today.
            self.sales_made = 0
            self.serums_sold = 0

            self.sales_multipliers = [] #This list holds ["Source_type",multiplier_as_float]. The multiplier is applied to the value of serums when they are sold.
            # Only the most positive modifier of any source type is used. (This means a 1.0 modifier can be used to replace a negative modifier).


            self.mandatory_crises_list = [] #A list of crises to be resolved at the end of the turn, generally generated by events that have taken place.
            self.mandatory_morning_crises_list = [] #A list of specifically morning crises that need to be resolved.

            self.event_triggers_dict = {} #This dictionary will be used to hold flags for story events and triggers. In general a string is the key and a bool is the value stored.
            self.event_triggers_dict["policy_tutorial"] = 1 #We have a policy tutorial.
            self.event_triggers_dict["research_tutorial"] = 1 #We have a research tutorial.
            self.event_triggers_dict["design_tutorial"] = 1 #We have a serum design tutorial.
            self.event_triggers_dict["production_tutorial"] = 1 #We have a production tutorial.
            self.event_triggers_dict["outfit_tutorial"] = 1 #We have an outfit design tutorial.
            self.event_triggers_dict["hiring_tutorial"] = 1 #We have an outfit design tutorial.

            self.listener_system = Listener_Management_System()

        def run_turn(self): #Run each time the time segment changes. Most changes are done here.

            #Compute efficency drop
            for person in self.supply_team + self.research_team + self.production_team + self.market_team:
                if person in self.s_div.people + self.r_div.people + self.p_div.people + self.m_div.people: #Only people in the office lower effectiveness, no loss on weekends, not in for the day, etc.
                    self.team_effectiveness += -1 #TODO: Make this dependant on charisma (High charisma have a lower impact on effectiveness) and happiness.

            #Compute effiency rise from HR
            for person in self.hr_team:
                if person in self.h_div.people:
                    self.hr_progress(person.charisma,person.int,person.hr_skill)
                    person.change_happiness(person.get_opinion_score("working")+person.get_opinion_score("HR work"), add_to_log = False)

            if self.team_effectiveness < 50:
                self.team_effectiveness = 50

            if self.team_effectiveness > self.effectiveness_cap:
                self.team_effectiveness = self.effectiveness_cap

            #Compute other deparement effects
            for person in self.supply_team:
                if person in self.s_div.people: #Check to see if the person is in the room, otherwise don't count their progress (they are at home, dragged away by PC, weekend, etc.)
                    self.supply_purchase(person.focus,person.charisma,person.supply_skill)
                    person.change_happiness(person.get_opinion_score("working")+person.get_opinion_score("supply work"), add_to_log = False)

            for person in self.research_team:
                if person in self.r_div.people:
                    self.research_progress(person.int,person.focus,person.research_skill)
                    person.change_happiness(person.get_opinion_score("working")+person.get_opinion_score("research work"), add_to_log = False)

            for person in self.production_team:
                if person in self.p_div.people:
                    self.production_progress(person.focus,person.int,person.production_skill)
                    person.change_happiness(person.get_opinion_score("working")+person.get_opinion_score("production work"), add_to_log = False)

            self.mark_autosale() #Mark extra serums to be sold by marketing.

            for person in self.market_team:
                if person in self.m_div.people:
                    if person.should_wear_uniform():
                        self.sale_progress(person.charisma,person.focus, person.market_skill, slut_modifier = person.outfit.slut_requirement) #If there is a uniform pass it's sluttiness along.
                    else:
                        self.sale_progress(person.charisma, person.focus, person.market_skill) #Otherwise their standard outfit provides no bonuses.
                    person.change_happiness(person.get_opinion_score("working")+person.get_opinion_score("marketing work"), add_to_log = False)

        def run_day(self): #Run at the end of the day.
            #Pay everyone for the day
            if mc.business.is_work_day():
                cost = self.calculate_salary_cost()
                self.funds += -cost
            return

        def is_open_for_business(self): #Checks to see if employees are currently working
            if not self.is_work_day(): #It is the weekend, people have the day off.
                return False

            elif time_of_day == 1 or time_of_day == 2 or time_of_day == 3: #It is the work period of the day
                return True

            return False #If all else fails, give them some time off.

        def is_work_day(self):
            if day % 7 == 5 or day % 7 == 6: #TODO: add support for expanding workdays
                return False
            return True

        def is_weekend(self):#TODO: add support for expanding/changing the weekend
            if day % 7 == 5 or day % 7 == 6: #Checks to see if it is saturday or sunday. Note that days might eventually be both neither weekend or workday, or both weekend AND workday!
                return True
            return False

        def get_uniform_wardrobe(self,title): #Takes a division (a room) and returns the correct uniform for that division, if one exists. If it is None, returns false. TODO: get this working.
            if title == "Marketing":
                return self.m_uniform.merge_wardrobes(self.all_uniform)
            elif title == "Researcher":
                return self.r_uniform.merge_wardrobes(self.all_uniform)
            elif title == "Production":
                return self.p_uniform.merge_wardrobes(self.all_uniform)
            elif title == "Supply":
                return self.s_uniform.merge_wardrobes(self.all_uniform)
            elif title == "Human Resources":
                return self.h_uniform.merge_wardrobes(self.all_uniform)
            else:
                return None

        def clear_messages(self): #clear all messages for the day.
            self.message_list = []
            self.counted_message_list = {}
            self.production_potential = 0
            self.supplies_purchased = 0
            self.production_used = 0
            self.research_produced = 0
            self.sales_made = 0
            self.serums_sold =0

        def add_counted_message(self,message,new_count):
            if message in self.counted_message_list:
                self.counted_message_list[message] += new_count
            else:
                self.counted_message_list[message] = new_count

        def add_normal_message(self,message): #Adds an uncounted message, only ever listed once per day
            if message not in self.message_list:
                self.message_list.append(message)

        def calculate_salary_cost(self):
            daily_cost = 0
            for person in self.supply_team + self.research_team + self.production_team + self.market_team + self.hr_team:
                daily_cost += person.salary
            return daily_cost

        def add_serum_design(self,the_serum):
            self.serum_designs.append(the_serum)

        def remove_serum_design(self,the_serum):
            self.serum_designs.remove(the_serum)
            if the_serum is self.active_research_design:
                self.active_research_design = None

            delete_list = []
            for line in self.serum_production_array:
                if the_serum is self.serum_production_array[line][0]:
                    delete_list.append(line) #Store a list of all the keys we need to delete to avoid modifying while interating. Needed in case two lines are making the same serum.

            for key in delete_list: #Now delete the production lines.
                del self.serum_production_array[key]

        def set_serum_research(self,new_research):
            self.active_research_design = new_research

        def research_progress(self,int,focus,skill):
            research_amount = __builtin__.round(((3*int) + (focus) + (2*skill) + 10) * (self.team_effectiveness))/100

            if self.head_researcher:
                bonus_percent = (self.head_researcher.int - 2)*0.05
                research_amount = research_amount * (1.0 + bonus_percent) #Every point above int 2 gives a 5% bonus.
                if bonus_percent > 0:
                    self.add_normal_message("Head researcher " + self.head_researcher.title + "'s intelligence resulted in a " + str(bonus_percent*100) + "% increase in research produced!")
                else:
                    self.add_normal_message("Head researcher " + self.head_researcher.title + "'s intelligence resulted in a " + str(bonus_percent*100) + "% change in research produced.")
            else:
                research_amount = research_amount * 0.9 #No head researcher is treated like int 0.
                self.add_normal_message("No head researcher resulted in a 10% reduction in research produced! Assign a head researcher at R&D!")

            if self.active_research_design is not None:
                the_research = self.active_research_design
                is_researched = the_research.researched # If it was researched before we added any research then we are increasing the mastery level of a trait (does nothing to serum designs)
                self.research_produced += research_amount
                if the_research.add_research(research_amount): #Returns true if the research is completed by this amount'
                    if isinstance(the_research, SerumDesign):
                        the_research.generate_side_effects() #The serum will generate any side effects that are needed.
                        self.mandatory_crises_list.append(Action("Research Finished Crisis",serum_creation_crisis_requirement,"serum_creation_crisis_label",the_research)) #Create a serum finished crisis, it will trigger at the end of the round
                        self.add_normal_message("New serum design researched: " + the_research.name)
                        self.active_research_design = None
                    elif isinstance(the_research, SerumTrait):
                        if is_researched: #We've reseached it already, increase mastery level instead.
                            self.add_normal_message("Serum trait mastery improved: " + the_research.name + ", Now " + str(the_research.mastery_level))
                        else:
                            self.add_normal_message("New serum trait researched: " + the_research.name)
                            self.active_research_design = None #If it's a newly discovered trait clear it so we don't start mastering it without player input.

            else:
                research_amount = 0 #We didn't actually research anything because there is nothing to research!

            return research_amount

        def player_research(self):
            amount_researched = self.research_progress(mc.int,mc.focus,mc.research_skill)
            self.listener_system.fire_event("general_work")
            self.listener_system.fire_event("player_research", amount = amount_researched)
            renpy.say("","You spend time in the lab, experimenting with different chemicals and techniques and producing " + str(amount_researched) + " research points.")
            return amount_researched

        def player_buy_supplies(self):
            amount_bought = self.supply_purchase(mc.focus,mc.charisma,mc.supply_skill)
            self.listener_system.fire_event("general_work")
            self.listener_system.fire_event("player_supply_purchase", amount = amount_bought)
            renpy.say("","You spend time securing new supplies for the lab, purchasing " + str(amount_bought) + " units of serum supplies.")
            return amount_bought

        def supply_purchase(self,focus,cha,skill):
            max_supply = __builtin__.round(((3*focus) + (cha) + (2*skill) + 10) * (self.team_effectiveness))/100
            max_supply = int(max_supply)
            if max_supply + self.supply_count > self.supply_goal:
                max_supply = self.supply_goal - self.supply_count
                if max_supply <= 0:
                    return 0

            self.funds += -max_supply
            self.supply_count += max_supply
            self.supplies_purchased += max_supply #Used for end of day reporting
            return max_supply

        def player_market(self):
            amount_sold = self.sale_progress(mc.charisma,mc.focus,mc.market_skill)
            self.listener_system.fire_event("player_serums_sold_count", amount = amount_sold)
            self.listener_system.fire_event("general_work")
            renpy.say("","You spend time making phone calls to clients and shipping out orders. You sell " + str(amount_sold) + " doses of serum.")
            return amount_sold

        def sale_progress(self,cha,focus,skill, slut_modifier = 0):

            serum_value_multiplier = 1.00 #For use with value boosting policies. Multipliers are multiplicative.
            if male_focused_marketing_policy.is_owned(): #Increase value by the character's outfit sluttiness if you own that policy.
                sluttiness_multiplier = (slut_modifier/100.0) + 1
                serum_value_multiplier = serum_value_multiplier * (sluttiness_multiplier)

            multipilers_used = {} #Generate a dict with only the current max multipiers of each catagory.
            for multiplier_source in self.sales_multipliers:
                if not multiplier_source[0] in multipilers_used:
                    multipilers_used[multiplier_source[0]] = multiplier_source[1]
                elif multiplier_source[1] > multipliers_used.get(multiplier_source[0]):
                    multipilers_used[multiplier_source[0]] = multiplier_source[1]

            for maxed_multiplier in multipilers_used:
                value_change = multipilers_used.get(maxed_multiplier)
                serum_value_multiplier = serum_value_multiplier * value_change
                if value_change > 1:
                    self.add_normal_message("+" + str((value_change-1)*100) + "% serum value due to " + maxed_multiplier + ".")
                elif value_change < 1: #No message shown for exactly 1.
                    self.add_normal_message(str((value_change-1)*100) + "% serum value due to " + maxed_multiplier + ".") #Duplicate normal messages are not shown twice, so this should only exist once per turn, per multiplier.

            serum_sale_count = __builtin__.round(((3*cha) + (focus) + (2*skill) + 5) * (self.team_effectiveness))/100 #Total number of doses of serum that can be sold by this person.
            serum_sale_count = __builtin__.int(serum_sale_count)
            sorted_by_value = sorted(self.sale_inventory.serums_held, key = lambda serum: serum[0].value) #List of tuples [SerumDesign, count], sorted by the value of each design. Used so most valuable serums are sold first.
            if self.sale_inventory.get_any_serum_count() < serum_sale_count:
                serum_sale_count = self.sale_inventory.get_any_serum_count()

            this_batch_serums_sold = 0
            if serum_sale_count > 0: #ie. we have serum in our inventory to sell, and the capability to sell them.
                for serum in sorted_by_value:
                    if serum_sale_count <= serum[1]:
                        #There are enough to satisfy order. Remove, add value to wallet, and break
                        value_sold = serum_sale_count * serum[0].value * serum_value_multiplier
                        if value_sold < 0:
                            value_sold = 0
                        self.funds += value_sold
                        self.sales_made += value_sold
                        self.listener_system.fire_event("serums_sold_value", amount = value_sold)
                        self.serums_sold += serum_sale_count
                        this_batch_serums_sold += serum_sale_count
                        self.sale_inventory.change_serum(serum[0],-serum_sale_count)
                        serum_sale_count = 0
                        break
                    else:
                        #There are not enough in this single order, remove _all_ of them, add value, go onto next thing.
                        serum_sale_count += -serum[1] #We were able to sell this number of serum.
                        value_sold = serum[1] * serum[0].value * serum_value_multiplier
                        if value_sold < 0:
                            value_sold = 0
                        self.funds += value_sold
                        self.sales_made += value_sold
                        self.listener_system.fire_event("serums_sold_value", amount = value_sold)
                        self.serums_sold += serum_sale_count
                        this_batch_serums_sold += serum_sale_count
                        self.sale_inventory.change_serum(serum[0],-serum[1]) #Should set serum count to 0.
                        #Don't break, we haven't used up all of the serum count
            return this_batch_serums_sold



        def production_progress(self,focus,int,skill):
            #First, figure out how many production points we can produce total. Subtract that much supply and mark that much production down for the end of day report.
            production_amount = __builtin__.round(((3*focus) + (int) + (2*skill) + 10) * (self.team_effectiveness))/100
            self.production_potential += production_amount

            if self.serum_production_array is None:
                return #If we don't have anything in production just tally how much we could have produced and move on.

            if production_amount > self.supply_count:
                production_amount = self.supply_count #Figure out our total available production, before we split it up between tasks (which might not have 100% usage!)

            #Now go through each production line we have marked.
            for production_line in self.serum_production_array:
                # A production line is a tuple of [SerumDesign, production weight (int), production point progress (int)].
                serum_weight = self.serum_production_array[production_line][1]
                the_serum = self.serum_production_array[production_line][0]

                proportional_production = (serum_weight/100.0) * production_amount #Get the closest integer value for the weighted production we put into the serum
                self.production_used += proportional_production #Update our usage stats and subract supply needed.
                self.supply_count += -proportional_production

                self.serum_production_array[production_line][2] += proportional_production
                serum_count = self.serum_production_array[production_line][2]//the_serum.production_cost #Calculates the number of batches we have made (previously for individual serums, now for entire batches)
                if serum_count > 0:
                    self.add_counted_message("Produced " + self.serum_production_array[production_line][0].name,serum_count*self.batch_size) #Give a note to the player on the end of day screen for how many we made.
                    self.serum_production_array[production_line][2] -= serum_count * self.serum_production_array[production_line][0].production_cost
                    self.inventory.change_serum(self.serum_production_array[production_line][0],serum_count*self.batch_size) #Add the number serums we made to our inventory.

            return production_amount

        def change_production(self,new_serum,production_line):
            if production_line in self.serum_production_array: #If it already exists, change the serum type and production points stored, but keep the weight for that line (it can be changed later)
                self.serum_production_array[production_line][0] = new_serum
                self.serum_production_array[production_line][1] = int(100 - self.get_used_line_weight() + self.serum_production_array[production_line][1]) #Set the production weight to everything we have remaining
                self.serum_production_array[production_line][2] = 0 #Set production points stored to 0 for the new serum
                self.serum_production_array[production_line][3] = -1 #Set autosell to -1, ie. don't auto sell.
            else: #If the production line didn't exist before, add a key for that line.
                self.serum_production_array[production_line] = [new_serum, int(100 - self.get_used_line_weight()), 0, -1]

        def get_used_line_weight(self):
            used_production = 0
            for existing_lines in self.serum_production_array:
                used_production += self.serum_production_array[existing_lines][1] #Tally how much weight we are using so far.
            return used_production

        def change_line_weight(self,line,weight_change):
            if line in self.serum_production_array:
                used_production = self.get_used_line_weight()
                if weight_change > 0 and weight_change + used_production > 100:
                    weight_change = 100 - used_production #If the full weight change would put us above our 100% max cap it at as much as can be assigned.

                self.serum_production_array[line][1] += weight_change
                if self.serum_production_array[line][1] < 0:
                    self.serum_production_array[line][1] = 0 #We cannot have a value less than 0%

        def change_line_autosell(self, line, threshold_change):
            if line in self.serum_production_array:
                if threshold_change > 0 and self.serum_production_array[line][3] < 0: #We use negative values as a marker for no threshold. If it's negative always treat it as -1 when we start adding again.
                    self.serum_production_array[line][3] = -1
                self.serum_production_array[line][3] += threshold_change

        def mark_autosale(self):
            for line in self.serum_production_array:
                if self.serum_production_array[line][3] >= 0: #There is an auto sell threshold set.
                    if self.inventory.get_serum_count(self.serum_production_array[line][0]) > self.serum_production_array[line][3]:
                        difference = int(self.inventory.get_serum_count(self.serum_production_array[line][0]) - self.serum_production_array[line][3]) #Check how many serums we need to sell to bring us to the threshold.
                        self.inventory.change_serum(self.serum_production_array[line][0], -difference) #Remove them from the production inventory.
                        self.sale_inventory.change_serum(self.serum_production_array[line][0], difference) #Add them to the sales inventory.

        def get_random_weighed_production_serum(self): #Return the serum design of one of our activly produced serums, relative probability by weight.
            used_production = 0
            for key in self.serum_production_array:
                used_production += self.serum_production_array[key][1] #Sum how much production we are using, usually 100%
            if used_production == 0:
                return None #If we are not _actually_ producing anything, return None.

            random_serum_number = renpy.random.randint(0,used_production)
            for key in self.serum_production_array:
                if random_serum_number <= self.serum_production_array[key][1]:
                    return self.serum_production_array[key][0]
                else:
                    random_serum_number -= self.serum_production_array[key][1] #Subtract the probability of this one from our number to make progress in our search.




        def player_production(self):
            production_amount = self.production_progress(mc.focus,mc.int,mc.production_skill)
            self.listener_system.fire_event("player_production", amount = production_amount)
            self.listener_system.fire_event("general_work")
            renpy.say("","You spend time in the lab synthesizing serum from the it's raw chemical precursors. You generate " + str(production_amount) + " production points.")
            return production_amount

        def player_hr(self):
            eff_amount = self.hr_progress(mc.charisma,mc.int,mc.hr_skill)
            self.listener_system.fire_event("player_efficiency_restore", amount = eff_amount)
            self.listener_system.fire_event("general_work")
            renpy.say("","You settle in and spend a few hours filling out paperwork, raising company efficency by " + str(eff_amount )+ "%%.")
            return eff_amount

        def hr_progress(self,cha,int,skill): #Don't compute efficency cap here so that player HR effort will be applied against any efficency drop even though it's run before the rest of the end of the turn.
            restore_amount = (3*cha) + (int) + (2*skill) + 5
            self.team_effectiveness += restore_amount
            return restore_amount

        def add_employee_research(self, new_person):
            self.research_team.append(new_person)
            new_person.job = self.get_employee_title(new_person)

        def add_employee_production(self, new_person):
            self.production_team.append(new_person)
            new_person.job = self.get_employee_title(new_person)

        def add_employee_supply(self, new_person):
            self.supply_team.append(new_person)
            new_person.job = self.get_employee_title(new_person)

        def add_employee_marketing(self, new_person):
            self.market_team.append(new_person)
            new_person.job = self.get_employee_title(new_person)

        def add_employee_hr(self, new_person):
            self.hr_team.append(new_person)
            new_person.job = self.get_employee_title(new_person)

        def remove_employee(self, the_person):
            if the_person in self.research_team:
                self.research_team.remove(the_person)
            elif the_person in self.production_team:
                self.production_team.remove(the_person)
            elif the_person in self.supply_team:
                self.supply_team.remove(the_person)
            elif the_person in self.market_team:
                self.market_team.remove(the_person)
            elif the_person in self.hr_team:
                self.hr_team.remove(the_person)

            the_person.set_work(None,None)
            the_person.special_role.remove(employee_role)

            if the_person == self.head_researcher:
                renpy.call("fire_head_researcher", the_person) #Call the lable we use for firing the person as a role action. This should trigger it any time you fire or move your head researcher.



        def get_employee_list(self):
            return self.research_team + self.production_team + self.supply_team + self.market_team + self.hr_team

        def get_employee_count(self):
            return len(self.get_employee_list())

        def get_max_employee_slut(self):
            max = -1 #Set to -1 for an empty business, all calls should require at least sluttiness 0
            for person in self.get_employee_list():
                if person.sluttiness > max:
                    max = person.sluttiness
            return max

        def get_employee_title(self, the_person):
            if the_person in self.research_team:
                return "Researcher"

            elif the_person in self.market_team:
                return "Marketing"

            elif the_person in self.supply_team:
                return "Supply"

            elif the_person in self.production_team:
                return "Production"

            elif the_person in self.hr_team:
                return "Human Resources"
            else:
                return "None"

        def get_employee_workstation(self, the_person): #Returns the location a girl should be working at, or "None" if the girl does not work for you
            if the_person in self.research_team:
                return self.r_div

            elif the_person in self.market_team:
                return self.m_div

            elif the_person in self.supply_team:
                return self.s_div

            elif the_person in self.production_team:
                return self.p_div

            elif the_person in self.hr_team:
                return self.h_div
            else:
                return None

        def get_requirement_employee_list(self, exclude_list = None, **kargs): #Get a list of employees who pass the validrequirements. Pass the same arguments as person_meets_requirements expects as named args.
            employees_meeting_requirement = []
            if exclude_list is None:
                exclude_list = []
            for person in self.get_employee_list():
                if person not in exclude_list:
                    if person.person_meets_requirements(**kargs):
                        employees_meeting_requirement.append(person)
            return employees_meeting_requirement

        def give_daily_serum(self):
            if self.r_serum:
                the_serum = self.r_serum
                for person in self.research_team:
                    if self.inventory.get_serum_count(the_serum) > 0:
                        self.inventory.change_serum(the_serum,-1)
                        person.give_serum(copy.copy(the_serum), add_to_log = False) #use a copy rather than the main class, so we can modify and delete the effects without changing anything else.
                    else:
                        the_message = "Stockpile ran out of [the_serum.name] to give to the research division."
                        if not the_message in self.message_list:
                            self.add_normal_message(the_message)

            if self.m_serum:
                the_serum = self.m_serum
                for person in self.market_team:
                    if self.inventory.get_serum_count(the_serum) > 0:
                        self.inventory.change_serum(the_serum,-1)
                        person.give_serum(copy.copy(the_serum), add_to_log = False) #use a copy rather than the main class, so we can modify and delete the effects without changing anything else.
                    else:
                        the_message = "Stockpile ran out of [the_serum.name] to give to the marketing division."
                        if not the_message in self.message_list:
                            self.add_normal_message(the_message)

            if self.p_serum:
                the_serum = self.p_serum
                for person in self.production_team:
                    if self.inventory.get_serum_count(the_serum) > 0:
                        self.inventory.change_serum(the_serum,-1)
                        person.give_serum(copy.copy(the_serum), add_to_log = False) #use a copy rather than the main class, so we can modify and delete the effects without changing anything else.
                    else:
                        the_message = "Stockpile ran out of [the_serum.name] to give to the production division."
                        if not the_message in self.message_list:
                            self.add_normal_message(the_message)

            if self.s_serum:
                the_serum = self.s_serum
                for person in self.supply_team:
                    if self.inventory.get_serum_count(the_serum) > 0:
                        self.inventory.change_serum(the_serum,-1)
                        person.give_serum(copy.copy(the_serum), add_to_log = False) #use a copy rather than the main class, so we can modify and delete the effects without changing anything else.
                    else:
                        the_message = "Stockpile ran out of [the_serum.name] to give to the supply procurement division."
                        if not the_message in self.message_list:
                            self.add_normal_message(the_message)

            if self.h_serum:
                the_serum = self.h_serum
                for person in self.hr_team:
                    if self.inventory.get_serum_count(the_serum) > 0:
                        self.inventory.change_serum(the_serum,-1)
                        person.give_serum(copy.copy(the_serum), add_to_log = False) #use a copy rather than the main class, so we can modify and delete the effects without changing anything else.
                    else:
                        the_message = "Stockpile ran out of [the_serum.name] to give to the human resources division."
                        if not the_message in self.message_list:
                            self.add_normal_message(the_message)

        def advance_tutorial(self, tutorial_name):
            self.event_triggers_dict[tutorial_name] += 1 #advance our tutorial slot.

        def reset_tutorial(self, tutorial_name):
            self.event_triggers_dict[tutorial_name] = 1 #Reset it when the reset tutorial button is used.

        def add_sales_multiplier(self, multiplier_class, multiplier):
            mc.log_event("Serum sale value increased by " + str((multiplier - 1) * 100) + "% due to " + multiplier_class + ".", "float_text_grey")
            self.sales_multipliers.append([multiplier_class, multiplier])

        def remove_sales_multiplier(self, multiplier_class, multiplier):
            if [multiplier_class, multiplier] in self.sales_multipliers:
                mc.log_event("No longer reciving " + str((multiplier - 1) * 100) + "% serum value increase from " + multiplier_class + ".", "float_text_grey")
                self.sales_multipliers.remove([multiplier_class, multiplier])

    class SerumDesign(renpy.store.object): #A class that represents a design for a serum built up from serum traits.
        def __init__(self):
            self.name = ""
            self.traits = []
            self.side_effects = []

            self.researched = False
            self.obsolete = False
            self.current_research = 0

            self.research_needed = 0
            self.slots = 0
            self.value = 0
            self.production_cost = 0

            self.duration = 0
            self.duration_counter = 0

            self.expires = True #If set to false the serum does not tick up the duration_counter, meaning it will never expire.

        def reset(self): #Resets the serum to the default serum values.
            self.__init__()

        def has_tag(self, the_tag): #Returns true if at least one of the traits has the tag "the_tag". Used to confirm a production trait is included.
            for trait in self.traits:
                if the_tag in trait.exclude_tags:
                    return True
            return False

        def add_trait(self, the_trait, is_side_effect = False): #Used when the serum is being built in the serum designer.
            if the_trait not in self.traits or the_trait not in self.side_effects:
                if is_side_effect:
                    self.side_effects.append(the_trait)
                else:
                    self.traits.append(the_trait) #Add the trait to the serums list of traits.

                #Add the trait effects on the core develpment stats of the serum.
                self.research_needed += the_trait.research_added
                self.value += the_trait.value_added
                self.slots += the_trait.slots
                self.production_cost += the_trait.production_cost
                self.duration += the_trait.duration

        def remove_trait(self, the_trait): #Used when the serum is being built in the serum designer.
            if the_trait in self.traits or the_trait in self.side_effects:
                if the_trait in self.traits:
                    self.traits.remove(the_trait) #Remove the trait from our list of traits.
                else:
                    self.side_effects.remove(the_trait)

                #Remove the trait effects on the core development stats of the serum.
                self.research_needed += -the_trait.research_added
                self.value += -the_trait.value_added
                self.slots += -the_trait.slots
                self.production_cost += -the_trait.production_cost
                self.duration += -the_trait.duration

        def duration_expired(self): #Returns true if the serum has expired (ie. duration counter equal to or over duration.).
            if self.duration_counter >= self.duration:
                return True #Returns true when it has expired
            else:
                return False #Returns false when there is more time to go

        def run_on_turn(self,the_person): #Increases the counter, applies serum effect if there is still some duration left
            if self.duration_counter < self.duration:
                for trait in self.traits + self.side_effects:
                    trait.run_on_turn(the_person)
            if self.expires:
                self.duration_counter += 1

        def run_on_apply(self, the_person, add_to_log = True):
            for trait in self.traits + self.side_effects:
                trait.run_on_apply(the_person, add_to_log)

        def run_on_remove(self, the_person):
            for trait in self.traits + self.side_effects:
                trait.run_on_remove(the_person)

        def run_on_day(self, the_person):
            for trait in self.traits + self.side_effects:
                trait.run_on_day(the_person)

        def add_research(self, amount): #Returns true if "amount" research completes the research
            self.current_research += amount
            if self.current_research >= self.research_needed:
                self.researched = True
                return True
            else:
                return False

        def generate_side_effects(self): #Called when a serum is finished development. Tests all traits against their side effect chance and adds an effect for any that fail.
            for trait in self.traits:
                if trait.test_effective_side_effect_chance():
                    the_side_effect = get_random_from_list(list_of_side_effects)
                    self.add_trait(the_side_effect, is_side_effect = True)
                    mc.log_event(self.name + " developed side effect " + the_side_effect.name + " due to " + trait.name, "float_text_blue")

        def build_positive_slug(self):
            the_slug = ""
            traits_with_slugs = []
            for trait in self.traits + self.side_effects:
                if trait.positive_slug is not None and trait.positive_slug != "":
                    traits_with_slugs.append(trait)

            for trait in traits_with_slugs:
                the_slug += trait.positive_slug
                if trait is not traits_with_slugs[-1]: #If it isn't the last element.
                        the_slug += ", " #This gets us a nice formatted string in the form A, B, C, D.

        def build_negative_slug(self):
            the_slug = ""
            traits_with_slugs = []
            for trait in self.traits + self.side_effects:
                if trait.negative_slug is not None and trait.negative_slug != "":
                    traits_with_slugs.append(trait)

            for trait in traits_with_slugs:
                the_slug += trait.negative_slug
                if trait is not traits_with_slugs[-1]: #If it isn't the last element.
                        the_slug += ", " #This gets us a nice formatted string in the form A, B, C, D.



    class SerumInventory(renpy.store.object): #A bag class that lets businesses and people hold onto different types of serums, and move them around.
        def __init__(self,starting_list):
            self.serums_held = starting_list ##Starting list is a list of tuples, going [SerumDesign,count]. Count should be possitive.

        def get_serum_count(self, serum_design):
            for design in self.serums_held:
                if design[0] == serum_design:
                    return design[1]
            return 0

        def get_any_serum_count(self):
            count = 0
            for design in self.serums_held:
                count += design[1]
            return count

        def change_serum(self, serum_design,change_amount): ##Serum count must be greater than 0. Adds to stockpile of serum_design if it is already there, creates it otherwise.
            found = False
            for design in self.serums_held:
                if design[0] == serum_design and not found:
                    design[1] += int(change_amount)
                    found = True
                    if design[1] <= 0:
                        self.serums_held.remove(design)

            if not found:
                if change_amount > 0:
                    self.serums_held.append([serum_design,int(change_amount)])


        def get_serum_type_list(self): ## returns a list of all the serum types that are in the inventory, without their counts.
            return_values = []
            for design in self.serums_held:
                return_values.append(design[0])
            return return_values


    class SerumTrait(renpy.store.object):
        def __init__(self,name,desc, positive_slug = "", negative_slug = "", value_added = 0, research_added = 0, slots_added = 0, production_added = 0, duration_added = 0, base_side_effect_chance = 0, on_apply = None, on_remove = None, on_turn = None, on_day = None ,requires= None, tier = 0, start_researched=False,research_needed=50,exclude_tags=None, is_side_effect = False): #effect is a function that takes a serumDesign as a parameter and modifies it based on whatever effect this trait has.

            self.name = name
            self.desc = desc #A fluff text description.
            self.positive_slug = positive_slug #A short numerical list of positive effects
            self.negative_slug = negative_slug #The negative costs

            self.value_added = value_added
            self.research_added = research_added
            self.slots = slots_added
            self.production_cost = production_added
            self.duration = duration_added
            self.base_side_effect_chance = base_side_effect_chance #A percentage chance that this trait will introduce a side effect to the finished design.
            self.mastery_level = 1.0 #The amount of experience the MC has with this serum. Divide base side effect chance by mastery level to get effective side effect chance.


            self.on_apply = on_apply #The function applied to the person when the serum is first applied.
            self.on_remove = on_remove #The function applied to the person when the serum is removed (it should generally undo the on_apply effects)
            self.on_turn = on_turn #The function applied to the person at the end of a turn under the effect of the serum.
            self.on_day = on_day #The function applied to the person at the end of the day.


            if requires is None: #A list of other traits that must be researched before this.
                self.requires = []
            elif isinstance(requires, list):
                self.requires = requires
            else:
                self.requires = [requires]

            self.tier = tier #The tier of research that the business must have unlocked to research this, in addition to the other prerequisits.
            self.researched = start_researched
            self.research_needed = research_needed
            self.current_research = 0

            if exclude_tags is None:#A list of tags (strings) that this trait cannot be paired with. If a trait has the same excluded tag this cannot be added to a trait.
                self.exclude_tags = []
            elif isinstance(exclude_tags, list):
                self.exclude_tags = exclude_tags
            else:
                self.exclude_tags = [exclude_tags]

            self.is_side_effect = is_side_effect #If true this trait is a side effect and not counted towards serum max traits and such. It also cannot be added to a serum on purpose.


        def run_on_apply(self, the_person, add_to_log = True):
            if self.on_apply is not None:
                self.on_apply(the_person, add_to_log)

        def run_on_remove(self, the_person, add_to_log = False):
            if self.on_remove is not None:
                self.on_remove(the_person, add_to_log)

        def run_on_turn(self, the_person, add_to_log = False):
            if self.on_turn is not None:
                self.on_turn(the_person, add_to_log)

        def run_on_day(self, the_person, add_to_log = False):
            if self.on_day is not None:
                self.on_day(the_person, add_to_log)

        def add_research(self, amount):
            self.current_research += amount
            if self.current_research >= self.research_needed:
                if self.researched:
                    while (self.current_research >= self.research_needed): #For large businesses when the research produced is much larger than the total research needed you can gain multiple levels.
                        self.add_mastery(0.5)
                        self.current_research += -self.research_needed
                else:
                    self.current_research += -self.research_needed
                self.researched = True

                return True
            else:
                return False

        def add_mastery(self, amount):
            self.mastery_level += amount

        def get_effective_side_effect_chance(self): #Generates the effective side effect chance percent as an integer.
            the_chance = self.base_side_effect_chance/self.mastery_level
            return __builtin__.int(the_chance)

        def test_effective_side_effect_chance(self): #Gets the effective side effect chance and tests it against a random 1 to 100 roll
            the_chance = self.get_effective_side_effect_chance()
            the_roll = renpy.random.randint(0,100)
            if the_roll < the_chance:
                return True
            else:
                return False

        def build_negative_slug(self):
            if self.is_side_effect:
                return self.negative_slug #For side effects we do not want to display the side effect chance as a negative modifier.
            else:
                return self.negative_slug + ", " + str(self.get_effective_side_effect_chance()) + "% Chance of Side Effect"

        def has_required(self):
            has_prereqs = True
            for trait in self.requires:
                if not trait.researched:
                    has_prereqs = False
            if self.tier > mc.business.research_tier:
                has_prereqs = False
            return has_prereqs

    class MainCharacter(renpy.store.object):
        def __init__(self, location, name, last_name, business, stat_array, skill_array, sex_array):
            self.location = location
            self.name = name
            self.last_name = last_name
            self.energy = 50
            self.designed_wardrobe = Wardrobe("Designed Wardrobe")
            self.money = 100 ## Personal money that can be spent however you wish. Company funds are seperate (but can be manipulated in your favour)
            self.business = business
            self.inventory = SerumInventory([])

            ##Mental stats##
            #Mental stats are generally fixed and cannot be changed permanently.
            self.charisma = stat_array[0]#How likeable the person is. Mainly influences marketing, also determines how well interactions with other characters go. Main stat for HR and sales
            self.int = stat_array[1] #How smart the person is. Mainly influences research, small bonuses to most tasks. #Main stat for research and production.
            self.focus = stat_array[2]#How on task the person stays. Influences most tasks slightly. #Main stat for supplies

            ##Work Skills##
            #Skills can be trained up over time, but are limited by your raw stats.
            self.hr_skill = skill_array[0]
            self.market_skill = skill_array[1]
            self.research_skill = skill_array[2]
            self.production_skill = skill_array[3]
            self.supply_skill = skill_array[4]

            ##Sex Stats##
            # These are phyical stats about the character that impact how they behave in a sex scene. Future values might include penis size or sensitivity.
            self.arousal = 0 #How close to an orgasm you are. You are forced to cum when you reach 100, after which it generally resets to 0.

            ##Sex Skills##
            # These skill represent your knowledge and experience with different types of intimacy. Useful for raising a girls arousal faster than your own.
            self.sex_skills = {}
            self.sex_skills["Foreplay"] = sex_array[0] # A catch all for everything that goes on before blowjobs, sex, etc. Includes things like kissing, massages, etc.
            self.sex_skills["Oral"] = sex_array[1] # Your skill at eating a girl out.
            self.sex_skills["Vaginal"] = sex_array[2] # Your skill at different positions that involve vaginal sex.
            self.sex_skills["Anal"] = sex_array[3] # Your skill skill at different positions that involve anal sex.

            self.max_stamina = 2 # How many times you can seduce someone each day
            self.current_stamina = 2 # Current stamina.

            self.condom = False #True if you currently have a condom on. (maintained by sex scenes). TODO: Allow a third "broken" state and add dialgoue and descriptions for that.

            self.known_home_locations = [] #When the MC learns a character's home location the room reference should be added here. They can then get to it from the map.

            self.listener_system = Listener_Management_System() #A listener manager to let us enroll to events and update goals when they are triggered.

            #How many free points does the main character have to spend on their skills/abilities
            self.free_stat_points = 0
            self.free_work_points = 0
            self.free_sex_points = 0

            #The maximum score you can have in each of the major skill catagories
            self.max_stats = 8
            self.max_work_skills = 8
            self.max_sex_skills = 8

            #The current goals set for the player to achieve. On completion they gain 1 point towards that class of skills
            self.stat_goal = None
            self.work_goal = None
            self.sex_goal = None

            #The difficulty of goals. Some goals will be removed once the difficulty is highe enough, others will be added, and some will have completion requirements based on the difficulty.
            self.stat_goal_difficulty = 0
            self.work_goal_difficulty = 0
            self.sex_goal_difficulty = 0

            self.log_items = [] #A list of items to display as a log. is a tuple of: [string_to_display, text_style, unix_time]
            self.log_max_size = 20

            self.scrap_goal_available = True

            self.can_skip_time = False #A flag used to determine when it is safe to skip time and when it is not. Left in as of v0.19.0 to ensure missed references do not cause a crash; has no function.

        def change_location(self,new_location):
            self.location = new_location

        def use_energy(self,amount):
            self.energy = self.energy - amount
            if self.energy < 0:
                self.energy = 0

        def change_arousal(self,amount):
            self.arousal += amount
            if self.arousal < 0:
                self.arousal = 0

        def reset_arousal(self):
            self.arousal = 0

        def save_design(self, the_outfit, new_name, outfit_type = "full"):
            the_outfit.name = new_name
            if outfit_type == "under":
                self.designed_wardrobe.add_underwear_set(the_outfit)
            elif outfit_type == "over":
                self.designed_wardrobe.add_overwear_set(the_outfit)
            else: #Generally outfit_type == full, or some other uncaught error.
                self.designed_wardrobe.add_outfit(the_outfit)

        def is_at_work(self): #Checks to see if the main character is at work, generally used in crisis checks.
            if self.location == self.business.m_div or self.location == self.business.p_div or self.location == self.business.r_div or self.location == self.business.s_div or self.location == self.business.h_div:
                return True
            else:
                return False

        def run_turn(self):
            self.listener_system.fire_event("time_advance")
            self.change_arousal(-20)
            return

        def run_day(self):
            self.listener_system.fire_event("end_of_day")
            self.current_stamina = self.max_stamina
            self.reset_arousal()
            self.scrap_goal_available = True



        def complete_goal(self, the_finished_goal):
            if the_finished_goal == self.stat_goal:
                self.free_stat_points += 1 #The player gets some new points to spend
                self.stat_goal_difficulty += 1 #Future goals become more difficult
                self.stat_goal = create_new_stat_goal(self.stat_goal_difficulty) #Generate a new goal

            elif the_finished_goal == self.work_goal:
                self.free_work_points += 1
                self.work_goal_difficulty += 1
                self.work_goal = create_new_work_goal(self.work_goal_difficulty)

            elif the_finished_goal == self.sex_goal:
                self.free_sex_points += 1
                self.sex_goal_difficulty += 1
                self.sex_goal = create_new_sex_goal(self.sex_goal_difficulty)

        def scrap_goal(self, the_finished_goal):
            if the_finished_goal == self.stat_goal:
                self.stat_goal = create_new_stat_goal(self.stat_goal_difficulty) #Generate a new goal

            elif the_finished_goal == self.work_goal:
                self.work_goal = create_new_work_goal(self.work_goal_difficulty)

            elif the_finished_goal == self.sex_goal:
                self.sex_goal = create_new_sex_goal(self.sex_goal_difficulty)

            self.scrap_goal_available = False

        def generate_goals(self):
            self.stat_goal = create_new_stat_goal(self.stat_goal_difficulty)
            self.work_goal = create_new_work_goal(self.work_goal_difficulty)
            self.sex_goal = create_new_sex_goal(self.sex_goal_difficulty)

        def improve_stat(self, stat_string, amount = 1):
            if amount > self.free_stat_points:
                amount = self.free_stat_points
            if stat_string == "int":
                self.int += amount
            elif stat_string == "cha":
                self.charisma += amount
            elif stat_string == "foc":
                self.focus += amount

            self.free_stat_points += -amount

        def improve_work_skill(self, skill_string, amount = 1):
            if amount > self.free_work_points:
                amount = self.free_work_points

            if skill_string == "hr":
                self.hr_skill += amount
            elif skill_string == "market":
                self.market_skill += amount
            elif skill_string == "research":
                self.research_skill += amount
            elif skill_string == "production":
                self.production_skill += amount
            elif skill_string == "supply":
                self.supply_skill += amount

            self.free_work_points += -amount

        def improve_sex_skill(self, sex_string, amount = 1):
            if amount > self.free_sex_points:
                amount = self.free_sex_points

            if sex_string in self.sex_skills:
                self.sex_skills[sex_string] += amount
            elif sex_string == "stam":
                self.max_stamina += amount
                self.current_stamina += amount

            self.free_sex_points += -amount


        def log_event(self, the_text, the_text_style):
            #Event_tuple is a tuple of text_string,colour_string,person
            event_tuple = (the_text, the_text_style, time.time()) #Stores the unix time the event was added so we can run a little animation.
            self.log_items.insert(0,event_tuple)
            while len(self.log_items) > self.log_max_size:
                self.log_items.pop() #Pop off extra items until we are down to size.



    class Person(renpy.store.object): #Everything that needs to be known about a person.
        def __init__(self,name,last_name,age,body_type,tits,height,body_images,expression_images,hair_colour,hair_style,skin,eyes,job,wardrobe,personality,stat_list,skill_list,
            sluttiness=0,obedience=0,suggest=0,sex_list=[0,0,0,0], love = 0, happiness = 100, home = None, work = None,
            font = "Avara.tff", name_color = "#ffffff", dialogue_color = "#ffffff",
            face_style = "Face_1",
            special_role = None,
            title = None, possessive_title = None, mc_title = None,
            relationship = None, SO_name = None, kids = None):

            ## Personality stuff, name, ect. Non-physical stuff.
            self.name = name
            self.last_name = last_name

            self.title = title #Note: We format these down below!
            self.possessive_title = possessive_title #The way the girl is refered to in relation to you. For example "your sister", "your head researcher", or just their title again.
            if mc_title:
                self.mc_title = mc_title #What they call the main character. Ie. "first name", "mr.last name", "master", "sir".
            else:
                self.mc_title = "Stranger"

            self.home = home #The room the character goes to at night. If none a default location is used.
            self.work = work #The room the character goes to for work.
            self.schedule = {0:home,1:None,2:None,3:None,4:home} #A character's schedule is a dict of 0,1,2,3,4 (time periods) mapped to locations.
            #If there is a place in the schedule the character will go there. Otherwise they have free time and will do whatever they want.
            self.job = job

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
                self.kids = 0 #If she has kids, how many. (More likely for older characters.


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
                what_color = dialogue_color) #The colour of the character's dialogue.

            if title: #Format the given titles, if any, so they appear correctly the first time you meet at person.
                self.set_title(title) #The way the girl is refered to by the MC. For example: "Mrs. Whatever", "Lily", or "Mom". Will reset "???" if appropriate
            else:
                self.char.name = self.create_formatted_title("???")
            if possessive_title:
                self.set_possessive_title(possessive_title)

            ## Physical things.
            self.age = age
            self.body_type = body_type
            self.tits = tits
            self.height = height #This is the scale factor for height, with the talest girl being 1.0 and the shortest being 0.8
            self.body_images = body_images #instance of Clothing class, which uses full body shots.
            self.face_style = face_style
            self.expression_images = expression_images #instance of the Expression class, which stores facial expressions for different skin colours
            self.hair_colour = hair_colour #A list of [description, color value], where colour value is a standard RGBA list.
            self.hair_style = hair_style
            self.skin = skin
            self.eyes = eyes
            #TODO: Tattoos eventually

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


            self.on_room_enter_event_list = [] #Checked when you enter a room with this character. If an event is in this list and enabled it is run (and no other event is until the room is reentered)
            self.on_talk_event_list = [] #Checked when you start to interact with a character. If an event is in this list and enabled it is run (and no other event is until you talk to the character again.)

            self.event_triggers_dict = {} #A dict used to store extra parameters used by events, like how many days has it been since a performance review.
            self.event_triggers_dict["employed_since"] = 0
            self.event_triggers_dict["wants_titlechange"] = False

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

            self.salary = self.calculate_base_salary()

            # self.employed_since = 0 #Default this to 0, it will almost always be overwritten but in case it sneaks through this makes sure that nothing breaks.

            self.idle_pose = get_random_from_list(["stand2","stand3","stand4","stand5"]) #Get a random idle pose that you will use while people are talking to you.

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
            self.situational_obedience = {} #A dictthat stores a "situation" string and a corrisponding amount that it has affected their obedience by.

            ##Sex Stats##
            #These are physical stats about the girl that impact how she behaves in a sex scene. Future values might include things like breast sensitivity, pussy tighness, etc.
            self.arousal = 0 #How actively horny a girl is, and how close she is to orgasm. Generally resets to 0 after orgasming, and decreases over time while not having sex (or having bad sex).

            ##Sex Skills##
            #These represent how skilled a girl is at different kinds of intimacy, ranging from kissing to anal. The higher the skill the closer she'll be able to bring you to orgasm (whether you like it or not!)
            self.sex_skills = {}
            self.sex_skills["Foreplay"] = sex_list[0] #A catch all for everything that goes on before blowjobs, sex, etc. Includes things like kissing and strip teases.
            self.sex_skills["Oral"] = sex_list[1] #The girls skill at giving head.
            self.sex_skills["Vaginal"] = sex_list[2] #The girls skill at different positions that involve vaginal sex.
            self.sex_skills["Anal"] = sex_list[3] #The girls skill at different positions that involve anal sex.

            ## Clothing things.
            self.wardrobe = copy.copy(wardrobe) #Note: we overwrote default copy behaviour for wardrobes so they do not have any interference issues with eachother.

            self.planned_outfit = self.wardrobe.decide_on_outfit(self.sluttiness) #planned_outfit is the outfit the girl plans to wear today while not at work. She will change back into it after work or if she gets stripped. Cop0y it in case the outfit is changed during the day.
            self.planned_uniform = None #The uniform the person was planning on wearing for today, so they can return to it if they need to while at work.
            self.outfit = self.planned_outfit.get_copy() #Keep a seperate copy of hte outfit as the one that is being worn.


            ## Conversation things##
            self.sexed_count = 0

        def run_turn(self):

            self.bleed_slut() #if our sluttiness is over our core slut, bleed some off and, if we have suggest, turn it into core slut.

            remove_list = []
            for serum in self.serum_effects: #Compute the effects of all of the serum that the girl is under.
                serum.run_on_turn(self) #Run the serum's on_turn funcion if it has one.
                if serum.duration_expired(): #Returns true if the serum effect is suppose to expire in this time, otherwise returns false. Always updates duration counter when called.
                    remove_list.append(serum) #Use a holder "remove" list to avoid modifying list while iterating.

            for serum in remove_list:
                serum.run_on_remove(self)
                self.serum_effects.remove(serum)

            #Now we want to see if she's unhappy enough to quit. We will tally her "happy points", a negative number means a chance to quit.

            if mc.business.get_employee_workstation(self) is not None and mc.business.is_work_day(): #Only let people who work for us quit their job.
                happy_points = self.get_job_happiness_score()
                if happy_points < 0: #We have a chance of quitting.
                    chance_to_quit = happy_points * -2 #there is a %2*unhappiness chance that the girl will quit.
                    if renpy.random.randint(0,100) < chance_to_quit: #She is quitting
                        potential_quit_action = Action(self.name + " is quitting.", quiting_crisis_requirement, "quitting_crisis_label", self)
                        if potential_quit_action not in mc.business.mandatory_crises_list:
                            mc.business.mandatory_crises_list.append(potential_quit_action)

                    else: #She's not quitting, but we'll let the player know she's unhappy TODO: Only present this message with a certain research/policy.
                        warning_message = self.title + " (" +mc.business.get_employee_title(self) + ") " + " is unhappy with her job and is considering quitting."
                        if warning_message not in mc.business.message_list:
                            mc.business.add_normal_message(warning_message)

        def run_move(self,location): #Move to the apporpriate place for the current time unit, ie. where the player should find us.

            #Move the girl the appropriate location on the map. For now this is either a division at work (chunks 1,2,3) or downtown (chunks 0,5). TODO: add personal homes to all girls that you know above a certain amount.

            self.sexed_count = 0 #Reset the counter for how many times you've been seduced, you might be seduced multiple times in one day!

            if time_of_day == 0: #It's a new day, get a new outfit out to wear!
                self.planned_outfit = self.wardrobe.decide_on_outfit(self.sluttiness)
                self.outfit = self.planned_outfit.get_copy()
                self.planned_uniform = None

            destination = self.schedule[time_of_day] #None destination means they have free time
            if destination == self.work and not mc.business.is_open_for_business(): #NOTE: Right now we give everyone time off based on when the mc has work scheduled.
                destination = None

            if destination is not None: #We have somewhere scheduled to be for this time chunk. Let's move over there.
                location.move_person(self, destination) #Always go where you're scheduled to be.
                if self.schedule[time_of_day] == self.work: #We're going to work.
                    if self.should_wear_uniform(): #Get a uniform if we should be wearing one.
                        self.wear_uniform()
                        self.change_happiness(self.get_opinion_score("work uniforms"),add_to_log = False)
                        if self.planned_uniform and self.planned_uniform.slut_requirement > self.sluttiness*0.75: #A skimpy outfit/uniform is defined as the top 25% of a girls natural sluttiness.
                            self.change_slut_temp(self.get_opinion_score("skimpy uniforms"), add_to_log = False)

                elif destination == self.home:
                    self.outfit = self.planned_outfit.get_copy() #We're at home, so we can get back into our casual outfit.

                #NOTE: There is no else here because all of the desitnations should be set. If it's just a location they travel there and that's the end of it.

            else:
                #She finds somewhere to burn some time
                self.outfit = self.planned_outfit.get_copy() #Get changed back into our proper outfit if we aren't in it already.
                available_locations = [] #Check to see where is public (or where you are white listed) and move to one of those locations randomly
                for potential_location in list_of_places:
                    if potential_location.public:
                        available_locations.append(potential_location)
                location.move_person(self, get_random_from_list(available_locations))

            #We do uniform/outfit checks in run move because it happens at the _start_ of the time chunk. The girl looks forward to wearing her outfit (or dreads it) rather than responds to actually doing it.
            if self.outfit and self.planned_outfit.slut_requirement > self.sluttiness*0.75: #A skimpy outfit is defined as the top 25% of a girls natural sluttiness.
                self.change_slut_temp(self.get_opinion_score("skimpy outfits"), add_to_log = False)
            elif self.outfit and self.planned_outfit.slut_requirement < self.sluttiness*0.25: #A conservative outfit is defined as the bottom 25% of a girls natural sluttiness.
                self.change_happiness(self.get_opinion_score("conservative outfits"), add_to_log = False)

            if self.outfit.tits_available() and self.outfit.tits_visible() and self.outfit.vagina_available() and self.outfit.vagina_visible():
                self.change_slut_temp(self.get_opinion_score("not wearing anything"), add_to_log = False)

            if not self.outfit.wearing_bra() or not self.outfit.wearing_panties(): #We need to determine how much underwear they are not wearing. Each piece counts as half, so a +2 "love" is +1 slut per chunk.
                underwear_bonus = 0
                if not self.outfit.wearing_bra():
                    underwear_bonus += self.get_opinion_score("not wearing underwear")
                if not self.outfit.wearing_panties():
                    underwear_bonus += self.get_opinion_score("not wearing underwear")
                underwear_bonus = __builtin__.int(underwear_bonus/2.0) #I believe this rounds towards 0. No big deal if it doesn't, very minor detail.
                self.change_slut_temp(underwear_bonus, add_to_log = False)

            if self.outfit.tits_visible():
                self.change_slut_temp(self.get_opinion_score("showing her tits"), add_to_log = False)
            if self.outfit.vagina_visible():
                self.change_slut_temp(self.get_opinion_score("showing her ass"), add_to_log = False)

            if self.outfit.get_bra() or self.outfit.get_panties():
                lingerie_bonus = 0
                if self.outfit.get_bra() and self.outfit.get_bra().slut_value > 1: #We consider underwear with an innate sluttiness of 2 or higher "lingerie" rather than just underwear.
                    lingerie_bonus += self.get_opinion_score("lingerie")
                if self.outfit.get_panties() and self.outfit.get_panties().slut_value > 1:
                    lingerie_bonus += self.get_opinion_score("lingerie")
                lingerie_bonus = __builtin__.int(lingerie_bonus/2.0)
                self.change_slut_temp(lingerie_bonus, add_to_log = False)


        def run_day(self): #Called at the end of the day.
            if renpy.random.randint(0,100) < 8 and self.title: #There's an 8% chance they want a title change on any given day, if they are already introduced. TODO: Tweak this or make it dependent on other stuff.
                self.event_triggers_dict["wants_titlechange"] = True
            else:
                self.event_triggers_dict["wants_titlechange"] = False

            #Now we will normalize happiness towards 100 over time. Every 5 points of happiness above or below 100 results in a -+1 per time chunk, rounded towards 0.
            hap_diff = self.happiness - 100
            hap_diff = __builtin__.int(hap_diff/5.0) #python defaults to truncation towards 0, so this gives us the number we should be changing our happinss by
            self.change_happiness(-hap_diff, add_to_log = False) #Apply the change

            remove_list = []
            for serum in self.serum_effects:
                serum.run_on_turn(self) #If a run_on_turn is called and the serum has expired no effects are calculated, so we can safely call this as many times as we want.
                serum.run_on_turn(self) #Night is 3 turn chunks, but one is already called when time progresses. Run serums twice more, and if we've gotten here we also run the on day function.
                serum.run_on_day(self) #Serums that effect people at night must effect two of the three time chunks.
                if serum.duration_expired(): #Night is 3 segments, but 1 is allready called when run_turn is called.
                    remove_list.append(serum)

            for serum in remove_list:
                serum.run_on_remove(self)
                self.serum_effects.remove(serum)


            if day%7 == 0: #If the new day is Monday
                self.change_happiness(self.get_opinion_score("Mondays"), add_to_log = False)

            elif day%7 == 4: #If the new day is Friday
                self.change_happiness(self.get_opinion_score("Fridays"), add_to_log = False)

            elif day%7 == 5 or day%7 == 6: #If the new day is a weekend day
                self.change_happiness(self.get_opinion_score("the weekend"), add_to_log = False)

        def build_person_displayable(self,position = None, emotion = None, special_modifier = None, show_person_info = True): #Encapsulates what is done when drawing a person and produces a single displayable.
            if position is None:
                position = self.idle_pose #Easiest change is to call this and get a random standing posture instead of a specific idle pose. We redraw fairly frequently so she will change position frequently.

            displayable_list = [] # We will be building up a list of displayables passed to us by the various objects on the person (their body, clothing, etc.)

            if emotion is None:
                emotion = self.get_emotion()

            displayable_list.append(self.body_images.generate_item_displayable(self.body_type,self.tits,position)) #Add the body displayable

            displayable_list.append(self.expression_images.generate_emotion_displayable(position,emotion, special_modifier = special_modifier)) #Get the face displayable

            size_render = renpy.render(displayable_list[0], 10, 10, 0, 0) #We need a render object to check the actual size of the body displayable so we can build our composite accordingly.
            the_size = size_render.get_size() # Get the size. Without it our displayable would be stuck in the top left when we changed the size ofthings inside it.
            x_size = __builtin__.int(the_size[0])
            y_size = __builtin__.int(the_size[1])

            displayable_list.extend(self.outfit.generate_draw_list(self,position,emotion,special_modifier)) #Get the displayables for everything we wear. Note that extnsions do not return anything because they have nothing to show.
            displayable_list.append(self.hair_style.generate_item_displayable("standard_body",self.tits,position)) #Get hair

            #NOTE: default return for the_size is floats, even though it is in exact pixels. Use int here otherwise positional modifiers like xanchor and yalign do not work (no displayable is shown at all!)
            composite_list = [(x_size,y_size)] #Now we build a list of our parameters, done like this so they are arbitrarily long
            for display in displayable_list:
                composite_list.append((0,0)) #Center all displaybles on the top left corner, because of how they are rendered they will all line up.
                composite_list.append(display) #Append the actual displayable

            final_image = Composite(*composite_list) # Create a composite image using all of the displayables
            return final_image

        def draw_person(self,position = None, emotion = None, special_modifier = None, show_person_info = True): #Draw the person, standing as default if they aren't standing in any other position.
            renpy.scene("Active")
            if show_person_info:
                renpy.show_screen("person_info_ui",self)

            final_image = self.build_person_displayable(position, emotion, special_modifier, show_person_info)

            # NOTE: FUTURE FEATURE, HIGHLY EXPERIMENTAL
            # animation_surface = renpy.load_surface(final_image)
            #
            # Forgive me, this is a really hack-y part of the game needed to get ShaderDisplayable working properly.
            # It expects an image, and I was unable to find any way to make it easily accept a surface or any other type of displayable.
            # So we take the surface and save it as a .png then hand the name of the .png to ShaderDisplayable.
            # name = "animation/CHARACTER_1_IMAGE.png"
            # file_path = os.path.abspath(os.path.join(config.basedir, "game"))
            # file_name = os.path.join(file_path,name)
            # pygame.image.save(animation_surface, file_name)
            #
            # #BUG: Character image does not refresh when draw_person() is called and it already had an image. Likely the displayable is being cached and it does not notice that it should be loading a new image now.
            # animated_image = ShaderDisplayable(shader.MODE_2D, name, shader.VS_2D,PS_WALK_2D, textures={"tex1":"animation/proof_of_concept_shader.png"}, uniforms={})
            # renpy.show(self.name,at_list=[character_right, scale_person(self.height)],layer="Active",what=animated_image,tag=self.name) #Show the image, make sure to scale it ot the height of our person.
            # NOTE: END OF FUTURE FEATURE.

            renpy.show(self.name,at_list=[character_right, scale_person(self.height)],layer="Active",what=final_image,tag=self.name)


        def draw_animated_removal(self, the_clothing, position = None, emotion = None, special_modifier = None): #A special version of draw_person, removes the_clothing and animates it floating away. Otherwise draws as normal.
            #Note: this function includes a call to remove_clothing, it is not needed seperately.
            renpy.scene("Active")
            renpy.show_screen("person_info_ui",self)
            if position is None:
                position = self.idle_pose

            bottom_displayable = [] #Displayables under the piece of clothing being removed.
            top_displayable = []

            if emotion is None:
                emotion = self.get_emotion()

            bottom_displayable.append(self.expression_images.generate_emotion_displayable(position,emotion, special_modifier = special_modifier)) #Get the face displayable, also always under clothing.

            bottom_displayable.append(self.body_images.generate_item_displayable(self.body_type,self.tits,position))  #Body is always under clothing
            size_render = renpy.render(bottom_displayable[1], 10, 10, 0, 0) #We need a render object to check the actual size of the body displayable so we can build our composite accordingly.
            the_size = size_render.get_size()
            x_size = __builtin__.int(the_size[0])
            y_size = __builtin__.int(the_size[1])

            bottom_clothing, split_clothing, top_clothing = self.outfit.generate_split_draw_list(the_clothing, self, position, emotion, special_modifier) #Gets a split list of all of our clothing items.
            #We should remember that middle item can be None.
            for item in bottom_clothing:
                bottom_displayable.append(item)

            for item in top_clothing:
                top_displayable.append(item)

            top_displayable.append(self.hair_style.generate_item_displayable("standard_body",self.tits,position)) #Hair is always on top

            #Now we build our two composites, one for the bottom image and one for the top.
            composite_bottom_params = [(x_size,y_size)]
            for display in bottom_displayable:
                composite_bottom_params.append((0,0))
                composite_bottom_params.append(display)

            composite_top_params = [(x_size,y_size)]
            for display in top_displayable:
                composite_top_params.append((0,0))
                composite_top_params.append(display)

            final_bottom = Composite(*composite_bottom_params)
            final_top = Composite(*composite_top_params)

            renpy.show("Bottom Composite", at_list= [character_right, scale_person(self.height)],layer="Active",what=final_bottom,tag=self.name+"Bottom")
            if split_clothing: #Only show this if we actually had something returned to us.
                renpy.show("Removed Item", at_list= [character_right, scale_person(self.height), clothing_fade],layer="Active",what=split_clothing,tag=self.name+"Middle")
                self.outfit.remove_clothing(the_clothing)
            renpy.show("Top Composite", at_list= [character_right, scale_person(self.height)],layer="Active",what=final_top,tag=self.name+"Top")


        def get_emotion(self): # Get the emotion state of a character, used when the persons sprite is drawn and no fixed emotion is required.
            if self.arousal>= 100:
                return "orgasm"

            if self.happiness > 100:
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

        def get_opinion_score(self, topic): #topic is a string matching the topics given in our random list (ie. "the colour blue", "sports"). Returns a tuple containing the score: -2 for hates, -1 for dislikes, 0 for no opinion, 1 for likes, and 2 for loves, and a bool to say if the opinion is known or not.
            if topic in self.opinions:
                return self.opinions[topic][0]

            if topic in self.sexy_opinions:
                return self.sexy_opinions[topic][0]

            return 0

        def get_opinion_topic(self, topic):
            if topic in self.opinions:
                return self.opinions[topic]

            if topic in self.sexy_opinions:
                return self.sexy_opinions[topic]

            return None

        def get_random_opinion(self, include_known = True, include_sexy = False, include_normal = True): #Gets the topic string of a random opinion this character holds. Includes options to include known opinions and sexy opinions. Returns None if no valid opinion can be found.
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

            if the_dict:
                return get_random_from_list(the_dict.keys()) #If we have something in the list we can return the topic string we used as a key for it. This can then be used with get_opinion_score to get the actual opinion
            else:
                return None #If we have nothing return None, make sure to deal with this when we use this function.


        def discover_opinion(self, topic, add_to_log = True): #topic is a string matching the topics given in our random list (ie. "the colour blue"). If the opinion is in either of our opinion dicts we will set it to known, otherwise we do nothing. Returns True if the opinion was updated, false if nothing was changed.
            updated = False
            if topic in self.opinions:
                if not self.opinions[topic][1]:
                    updated = True
                    if add_to_log:
                        mc.log_event("Discovered: " + self.title + " " + opinion_score_to_string(self.opinions[topic][0]) + " " + topic,"float_text_grey")
                self.opinions[topic][1] = True

            if topic in self.sexy_opinions:
                if not self.sexy_opinions[topic][1]:
                    updated = True
                    if add_to_log:
                        mc.log_event("Discovered: " + self.title + " " + opinion_score_to_string(self.sexy_opinions[topic][0]) + " " + topic,"float_text_grey")
                self.sexy_opinions[topic][1] = True

            return updated

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
                self.outfit = new_outfit.get_copy() #We're handed a properly formatted copy already, use it to wear right away.

        def set_uniform(self,uniform, wear_now):
            if uniform is not None:
                self.planned_uniform = uniform.get_copy()
                if wear_now:
                    self.outfit = uniform.get_copy()

        def give_serum(self,the_serum_design, add_to_log = True): ##Make sure you are passing a copy of the serum, not a reference.
            self.serum_effects.append(the_serum_design)
            the_serum_design.run_on_apply(self, add_to_log)

        def is_under_serum_effect(self):
            if self.serum_effects:
                return True
            else:
                return False

        def apply_serum_study(self, add_to_log = True): #Called when the person is studied by the MC. Raises mastery level of all traits used in active serums by 0.1
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


        def change_suggest(self,amount): #This changes the base, usually permanent suggest. Use add_suggest_effect to add temporary, only-highest-is-used, suggestion values
            self.suggestibility += amount
            if self.suggestibility < 0:
                self.suggestibility = 0

        def add_suggest_effect(self,amount, add_to_log = True):
            if amount > __builtin__.max(self.suggest_bag or [0]):
                self.change_suggest(-__builtin__.max(self.suggest_bag or [0])) #Subtract the old max and...
                self.change_suggest(amount) #add our new suggest.
                if add_to_log and amount != 0 and self.title:
                    mc.log_event(self.title + ": Suggestibility increased, now " + str(amount), "float_text_blue")
            else:
                if add_to_log and amount != 0 and self.title:
                    mc.log_event(self.title + ": Suggestiblity " + str(amount) + " lower than current " + str(self.suggestibility) + " amount. Suggestibility unchanged.", "float_text_blue")
            self.suggest_bag.append(amount) #Add it to the bag, so we can check to see if it is max later.


        def remove_suggest_effect(self,amount):
            self.change_suggest(- __builtin__.max(self.suggest_bag or [0])) #Subtract the max
            self.suggest_bag.remove(amount)
            self.change_suggest(__builtin__.max(self.suggest_bag or [0])) # Add the new max. If we were max, it is now lower, otherwie it cancels out.

        def change_happiness(self,amount, add_to_log = True):
            self.happiness += amount
            if self.happiness < 0:
                self.happiness = 0

            log_string = ""
            if amount > 0:
                log_string = "+" + str(amount) + " Happiness"
            else:
                log_string = str(amount) + " Happiness"

            if add_to_log and amount != 0:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                mc.log_event(display_name + ": " + log_string, "float_text_yellow")

        def change_love(self, amount, add_to_log = True):
            amount = __builtin__.int(amount)
            self.love += amount
            if self.love < -100:
                self.love = -100
            elif self.love > 100:
                self.love = 100

            log_string = ""
            if amount > 0:
                log_string = "+" + str(amount) + " Love"
            else:
                log_string = str(amount) + " Love"

            if add_to_log and amount != 0:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                mc.log_event(display_name + ": " + log_string, "float_text_pink")

        def change_slut_temp(self,amount, add_to_log = True): #Adds the amount to our slut value. If over our max, add only to the max instead (but don't lower). If subtracting, don't go lower than 0.
            return_report = "" #This is the string that is returned that will report what the final value of the change was.
            if amount > 0:
                self.sluttiness += amount
                return_report = "+" + str(amount) + " Sluttiness"

                # We're experimenting with uncapping the sluttiness and having sluttiness in excess of your suggestability cap bleed off quickly and inefficently.
                # if self.sluttiness > self.core_sluttiness + self.suggestibility + 10:
                #     self.sluttiness = self.core_sluttiness + self.suggestibility + 10 #Set it to our max.
                #     return_report = "Sluttiness Cap Reached." #If we hit the cap, let them know that instead of the numeric amount.
                #     if self.suggestibility == 0:
                #         return_report += "\nUse Serum to Increase Cap."

            elif amount < 0:
                self.sluttiness += amount
                return_report = str(amount) + " Sluttiness"
                # if self.sluttiness < 0: #TODO: confirm that letting temp sluttiness drop below 0 does not cause any problems.
                #     self.sluttiness = 0

            else: #It is exactly 0
                return_report = "No Effect on Sluttiness"

            if add_to_log:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                mc.log_event(display_name + ": " + return_report, "float_text_pink")

            # return return_report #Return this so we can display the effective change or cap message. #Depreciated as of phone log approach


        def change_slut_core(self,amount, add_to_log = True, fire_event = True): #Adds set amount to core slut.
            self.core_sluttiness += amount
            # if self.core_sluttiness < 0: #TODO: Confirm that letting core sluttiness drop below 0 does not cause any problems.
            #     self.core_sluttiness = 0
            if fire_event:
                mc.listener_system.fire_event("core_slut_change", the_person = self, amount = amount)
            log_string = ""
            if amount > 0:
                log_string = "+" + str(amount) + " Core Sluttiness"
            else:
                log_string = str(amount) + " Core Sluttiness"

            if add_to_log and amount != 0:
                display_name = self.create_formatted_title("???")
                if self.title:
                    display_name = self.title
                mc.log_event(display_name + ": " + log_string, "float_text_pink")

        def add_situational_slut(self, source, amount, description = ""):
            #Adds a conditional, temporary sluttiness amount. This is added now and removed when clear_situational is called, or when another add_situational is called with the same source.
            if source in self.situational_sluttiness:
                difference = amount - self.situational_sluttiness[source][0]
                self.change_slut_core(difference, add_to_log = False)
                self.change_slut_temp(difference, add_to_log = False)

            else:
                self.change_slut_core(amount, add_to_log = False)
                self.change_slut_temp(amount, add_to_log = False)

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


        def bleed_slut(self): #Reduce temp slut in order to increase core slut at a ratio determined by the suggest score.
            if self.sluttiness > self.core_sluttiness: #We need to bleed away sluttiness.
                if self.suggestibility == 0 and self.title: #TODO: think about how much we need this now.
                    mc.business.add_normal_message(self.title + " has a sluttiness higher then her core sluttiness. Raising her suggestibility with serum will slowly increase her core sluttiness!")

                if self.sluttiness > self.core_sluttiness + self.suggestibility:
                    #We need to bleed a lot because our suggestibility dropped.
                    difference = self.sluttiness - (self.core_sluttiness + self.suggestibility)
                    if difference > 5:
                        difference = 5

                    if renpy.random.randint(1,5) <= difference: #ie. there's a 20% chance per point over to increase it by a point.
                        self.change_slut_core(1, add_to_log = False) #We're experimenting with sluttiness above your suggestability amount converting inefficently (instead of not at all)
                    self.change_slut_temp(-difference, add_to_log = False)

                # self.change_slut_temp(-3, add_to_log = False) #We're experimenting with only lowering the temporary sluttiness when the core sluttiness goes up.
                elif renpy.random.randint(0,100) < self.suggestibility: # If we're not over our suggestability amount we turn it into core slut effectively.
                    self.change_slut_core(3, add_to_log = False)
                    self.change_slut_temp(-3, add_to_log = False)

            if self.sluttiness < self.core_sluttiness: #If we're lower than core we quickly return to it.
                difference = self.core_sluttiness - self.sluttiness
                if difference > 5:
                    difference = 5
                self.change_slut_temp(difference, add_to_log = False)


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

        def change_cha(self,amount, add_to_log = True):
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

        def change_int(self,amount, add_to_log = True):
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

        def change_focus(self,amount, add_to_log = True): #See charisma for full comments
            self.focus += self.int_debt
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

        def review_outfit(self):
            if self.should_wear_uniform():
                self.wear_uniform()#Reset uniform
#                self.call_uniform_review() #TODO: actually impliment this call, but only when her outfit significantly differs from the real uniform.

            elif self.outfit.slut_requirement > self.sluttiness:
                self.outfit = self.planned_outfit.get_copy()
                self.call_dialogue("clothing_review")

        def judge_outfit(self,outfit,temp_sluttiness_boost = 0): #Judge an outfit and determine if it's too slutty or not. Can be used to judge other people's outfits to determine if she thinks they look like a slut.
            # temp_sluttiness can be used in situations (mainly crises) where an outfit is allowed to be temporarily more slutty than a girl is comfortable wearing all the time.
            #Returns true if the outfit is wearable, false otherwise
            if outfit.slut_requirement > (self.effective_sluttiness() + temp_sluttiness_boost): #Arousal is important for judging potential changes to her outfit while being stripped down during sex.
                return False
            else:
                return True

        def should_wear_uniform(self):
            #Check to see if we are: 1) Employed by the PC. 2) At work right now. 3) there is a uniform set for our department.
            employment_title = mc.business.get_employee_title(self)
            if employment_title != "None":
                if mc.business.is_open_for_business(): #We should be at work right now, so if there is a uniform we should wear it.
                    if mc.business.get_uniform_wardrobe(employment_title).get_count() > 0: #Check to see if there's anything stored in the uniform section.
                        return True

            return False #If we fail to meet any of the above conditions we should return false.

        def wear_uniform(self): #Puts the girl into her uniform, if it exists.
            if self.planned_uniform is None:
                self.set_uniform(mc.business.get_uniform_wardrobe(mc.business.get_employee_title(self)).decide_on_uniform(self),False) #If we don't have a uniform planned for today get one.

            if self.planned_uniform is not None: #If our planned uniform is STILL None it means we are unable to construct a valid uniform. Only assign it as our outfit if we have managed to construct a uniform.
                self.outfit = self.planned_uniform.get_copy() #Set our current outfit to a copy of our planned uniform.

        def get_job_happiness_score(self):
            happy_points = self.happiness - 100 #Happiness over 100 gives a bonus to staying, happiness less than 100 gives a penalty
            happy_points += self.obedience - 95 #A more obedient character is more likely to stay, even if they're unhappy. Default characters can be a little disobedeint without any problems.
            happy_points += self.salary - self.calculate_base_salary() #A real salary greater than her base is a bonus, less is a penalty. TODO: Make this dependent on salary fraction, not abosolute pay.

            if (day - self.event_triggers_dict.get("employed_since",0)) < 14:
                happy_points += 14 - (day - self.event_triggers_dict.get("employed_since",0)) #Employees are much less likely to quit over the first two weeks.
            return happy_points

        def change_arousal(self,amount, add_to_log = True):
            self.arousal += __builtin__.round(amount) #Round it to an integer if it isn't one already.
            if self.arousal < 0:
                self.arousal = 0

            log_string = ""
            if amount > 0:
                log_string = self.title + ": +" + str(amount) + " Arousal"
            else:
                log_string = self.title + ": " + str(amount) + " Arousal"

            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_red")

        def reset_arousal(self):
            self.arousal = 0

        def has_large_tits(self): #Returns true if the girl has large breasts. "D" cups and up are considered large enough for titfucking, swinging, etc.
            if self.tits == "D" or self.tits == "DD" or self.tits == "DDD" or self.tits == "E" or self.tits == "F" or self.tits == "FF":
                return True
            else:
                return False

        def effective_sluttiness(self): #Used in sex scenes where the girl will be more aroused, making it easier for her to be seduced.
            return __builtin__.int(self.sluttiness + (self.arousal/4))

        def cum_in_mouth(self): #Add the appropriate stuff to their current outfit, and peform any personal checks if rquired.
            mc.listener_system.fire_event("sex_cum_mouth", the_person = self)
            if self.outfit.can_add_accessory(mouth_cum):
                the_cumshot = mouth_cum.get_copy()
                the_cumshot.layer = 0 #TODO: make sure this doesn't break things by being on layer 0
                self.outfit.add_accessory(the_cumshot)

            self.change_slut_temp(5*self.get_opinion_score("drinking cum"))
            self.change_happiness(5*self.get_opinion_score("drinking_cum"))
            self.discover_opinion("drinking cum")

        def cum_in_vagina(self):
            mc.listener_system.fire_event("sex_cum_vagina", the_person = self)
            #TODO: Add in vaginal cumshot clothing item once we have rendering support for it
            self.change_slut_temp(5*self.get_opinion_score("creampies"))
            self.change_happiness(5*self.get_opinion_score("creampies"))
            self.discover_opinion("creampies")

        def cum_on_tits(self):
            if self.outfit.can_add_accessory(tits_cum):
                the_cumshot = tits_cum.get_copy()
                if self.outfit.get_upper_visible():
                    top_layer = self.outfit.get_upper_visible()[0].layer #Get the top most pice of clothing and get it's layer.
                else:
                    top_layer = -1
                the_cumshot.layer = top_layer+1 #The cumshot lives on a layer it hit, above the one it hit. Accessories are drawn first in the hirearchy, so they have to be on a level higehr than what they hit.
                self.outfit.add_accessory(the_cumshot)

            self.change_slut_temp(5*self.get_opinion_score("being covered in cum"))
            self.change_happiness(5*self.get_opinion_score("being covered in cum"))
            self.discover_opinion("being covered in cum")



        def cum_on_stomach(self):
            if self.outfit.can_add_accessory(stomach_cum):
                the_cumshot = stomach_cum.get_copy()
                if self.outfit.get_upper_visible():
                    top_layer = self.outfit.get_upper_visible()[0].layer #Get the top most pice of clothing and get it's layer.
                else:
                    top_layer = -1
                the_cumshot.layer = top_layer+1 #The cumshot lives on a layer it hit, above the one it hit. Accessories are drawn first in the hirearchy, so they have to be on a level higehr than what they hit.
                self.outfit.add_accessory(the_cumshot)

            self.change_slut_temp(5*self.get_opinion_score("being covered in cum"))
            self.change_happiness(5*self.get_opinion_score("being covered in cum"))
            self.discover_opinion("being covered in cum")


        def cum_on_face(self):
            #TODO: Add this once we get a render for it
            if self.outfit.can_add_accessory(face_cum):
                the_cumshot = face_cum.get_copy()
                the_cumshot.layer = 0
                self.outfit.add_accessory(the_cumshot)

            self.change_slut_temp(5*self.get_opinion_score("cum facials"))
            self.change_happiness(5*self.get_opinion_score("cum facials"))
            self.discover_opinion("cum facials")

            self.change_slut_temp(5*self.get_opinion_score("being covered in cum"))
            self.change_happiness(5*self.get_opinion_score("being covered in cum"))
            self.discover_opinion("being covered in cum")

        def cum_on_ass(self):
            if self.outfit.can_add_accessory(ass_cum):
                the_cumshot = ass_cum.get_copy()
                if self.outfit.get_lower_visible():
                    top_layer = self.outfit.get_lower_visible()[0].layer #Get the top most pice of clothing and get it's layer.
                else:
                    top_layer = -1
                the_cumshot.layer = top_layer+1 #The cumshot lives on a layer it hit, above the one it hit. Accessories are drawn first in the hirearchy, so they have to be on a level higehr than what they hit.
                self.outfit.add_accessory(the_cumshot)

            self.change_slut_temp(5*self.get_opinion_score("being covered in cum"))
            self.change_happiness(5*self.get_opinion_score("being covered in cum"))
            self.discover_opinion("being covered in cum")

        def change_salary(self, amount, add_to_log = True):
            amount = __builtin__.round(amount)
            self.salary += amount
            if self.salary < 0:
                self.salary = 0

            log_string = ""
            if amount > 0:
                log_string = self.title + ": +$" + str(amount) + "/Day"
            else:
                log_string = self.title + ": -$" + str(-amount) + "/Day"

            if add_to_log and amount != 0:
                mc.log_event(log_string, "float_text_green")

        def calculate_base_salary(self): #returns the default value this person should be worth on a per day basis.
            return (self.int + self.focus + self.charisma)*2 + (self.hr_skill + self.market_skill + self.research_skill + self.production_skill + self.supply_skill)

        def set_work(self, work_times, the_location): #Sets the person's schedule so they visit their location at those times.
            if work_times is None or the_location is None:
                for time_chunk in self.schedule:
                    if self.schedule[time_chunk] == self.work:
                        self.schedule[time_chunk] = None #For all of the times we were scheudled to be at work, set it to None.
                return #Finished, only do the other stuff if we're dealing with non-None inputs.

            for time_chunk in work_times:
                self.schedule[time_chunk] = the_location
            self.work = the_location

        def person_meets_requirements(self, slut_required = 0, core_slut_required = 0, obedience_required = 0, obedience_max = 2000, love_required = -200):
            if self.sluttiness >= slut_required and self.core_sluttiness >= core_slut_required and self.obedience >= obedience_required and self.obedience <= obedience_max and self.love >= love_required:
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

        def get_role_reference_by_name(self, the_role):
            for role in self.special_role:
                if role.role_name == the_role:
                    return role
            return None

    class Personality(renpy.store.object): #How the character responds to various actions
        def __init__(self, personality_type_prefix, default_prefix = "relaxed",
            common_likes = None, common_dislikes = None, common_sexy_likes = None, common_sexy_dislikes = None,
            titles_function = None, possessive_titles_function = None, player_titles_function = None):


            self.personality_type_prefix = personality_type_prefix
            self.default_prefix = default_prefix

            self.titles_function = titles_function
            self.possessive_titles_function = possessive_titles_function
            self.player_titles_function = player_titles_function

            #These are the labels we will be trying to get our dialogue. If the labels do not exist we will get their defaults instead. A default should _always_ exist, if it does not our debug check will produce an error.
            self.response_label_ending = ["greetings", "sex_responses", "climax_responses", "clothing_accept", "clothing_reject", "clothing_review", "strip_reject", "sex_accept", "sex_obedience_accept", "sex_gentle_reject", "sex_angry_reject",
            "seduction_response", "seduction_accept_crowded", "seduction_accept_alone", "seduction_refuse", "flirt_response", "cum_face", "cum_mouth", "suprised_exclaim", "talk_busy",
            "improved_serum_unlock", "sex_strip", "sex_watch", "being_watched", "work_enter_greeting", "date_seduction", "sex_end_early", "sex_take_control", "sex_beg_finish", "introduction"]

            self.response_dict = {}
            for ending in self.response_label_ending:
                if renpy.has_label(self.personality_type_prefix + "_" + ending):
                    self.response_dict[ending] = self.personality_type_prefix + "_" + ending
                else:
                    self.response_dict[ending] = self.default_prefix + "_" + ending



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
                return the_person.name


    def make_person(): #This will generate a person, using a pregen body some of the time if they are available.
        split_proportion = 20 #1/5 characters generated will be a premade character.
        return_character = None
        if renpy.random.randint(1,100) < split_proportion:
            return_character = get_premade_character()

        if return_character is None: #Either we aren't getting a premade, or we are out of them.
            return_character = create_random_person()
        return return_character

    # create_random_person is used to generate a Person object from a list of random or provided stats. use "make_a_person" to properly get premade characters mixed with randoms.
    def create_random_person(name = None, last_name = None, age = None, body_type = None, face_style = None, tits = None, height = None, hair_colour = None, hair_style = None, skin = None, eyes = None, job = None,
        personality = None, custom_font = None, name_color = None, dial_color = None, starting_wardrobe = None, stat_array = None, skill_array = None, sex_array = None,
        start_sluttiness = None, start_obedience = None, start_happiness = None, start_love = None, start_home = None,
        title = None, possessive_title = None, mc_title = None, relationship = None, kids = None, SO_name = None):
        if name is None:
            name = get_random_name()
        if last_name is None:
            last_name = get_random_last_name()
        if age is None:
            age = renpy.random.randint(18,50)
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

        # if hair_colour == "blond": #TODO: add random variation in hair colour, to add variety between people.
        #     hair_style.colour = [0.84,0.75,0.47,1]
        # elif hair_colour == "brown":
        #     hair_style.colour = [0.73,0.43,0.24,1]
        # elif hair_colour == "red":
        #     hair_style.colour = [0.3,0.05,0.05,1]
        # else: #black
        #     hair_style.colour = [0.1,0.09,0.08,1]

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
        if personality is None:
            personality = get_random_personality()

        if custom_font is None:
            #Get a font
            my_custom_font = get_random_font()

        if name_color is None:
            # Get a color
            name_color = get_random_readable_color()

        if dial_color is None:
            # Use name_color
            dial_color = copy.copy(name_color) #Take a copy

        skill_cap = 5
        stat_cap = 5

        if recruitment_skill_improvement_policy.is_owned():
            skill_cap += 2

        if recruitment_stat_improvement_policy.is_owned():
            stat_cap += 2

        if skill_array is None:
            skill_array = [renpy.random.randint(1,skill_cap),renpy.random.randint(1,skill_cap),renpy.random.randint(1,skill_cap),renpy.random.randint(1,skill_cap),renpy.random.randint(1,skill_cap)]

        if stat_array is None:
            stat_array = [renpy.random.randint(1,stat_cap),renpy.random.randint(1,stat_cap),renpy.random.randint(1,stat_cap)]

        if sex_array is None:
            sex_array = [renpy.random.randint(0,5),renpy.random.randint(0,5),renpy.random.randint(0,5),renpy.random.randint(0,5)]

        if start_love is None:
            start_love = 0

        if start_happiness is None:
            start_happiness = 100 + renpy.random.randint(-10,10)

        start_suggest = 0

        if start_obedience is None:
            start_obedience = renpy.random.randint(-10,10)

        if recruitment_obedience_improvement_policy.is_owned():
            start_obedience += 10

        if start_sluttiness is None:
            start_sluttiness = renpy.random.randint(0,10)

        if recruitment_slut_improvement_policy.is_owned():
            start_sluttiness += 20

        if starting_wardrobe is None:
            starting_wardrobe = default_wardrobe.get_random_selection(40)

        if start_home is None:
            start_home = Room(name+"'s home", name+"'s home", [], apartment_background, [],[],[],False,[0.5,0.5], visible = False, hide_in_known_house_map = False)
            start_home.link_locations_two_way(downtown)
            start_home.add_object(make_wall())
            start_home.add_object(make_floor())
            start_home.add_object(make_bed())
            start_home.add_object(make_window())
            list_of_places.append(start_home)

            #start_home = downtown

        if relationship is None:
            relationship = get_random_from_weighted_list([["Single",100-age],["Girlfriend",50],["Fiancée",120-age*2],["Married",20+age*4]]) #Age plays a major factor.

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

        if SO_name is None and relationship != "Single":
            SO_name = get_random_male_name()

        return Person(name,last_name,age,body_type,tits,height,body_images,emotion_images,hair_colour,hair_style,skin,eyes,job,starting_wardrobe,personality,
            stat_array,skill_array,sex_list=sex_array,sluttiness=start_sluttiness,obedience=start_obedience,suggest=start_suggest, love=start_love, happiness=start_happiness, home = start_home,
            font = my_custom_font, name_color = name_color , dialogue_color = dial_color,
            face_style = face_style,
            title = title, possessive_title = possessive_title, mc_title = mc_title,
            relationship = relationship, kids = kids, SO_name = SO_name)

    def height_to_string(the_height): #Height is a value between 0.9 and 1.0 which corisponds to 5' 0" and 5' 10"
        rounded_height = __builtin__.round(the_height,2) #Round height to 2 decimal points.
        if rounded_height >= 1.00:
            return "5' 10\""
        elif rounded_height == 0.99:
            return "5' 9\""
        elif rounded_height == 0.98:
            return "5' 8\""
        elif rounded_height == 0.97:
            return "5' 7\""
        elif rounded_height == 0.96:
            return "5' 6\""
        elif rounded_height == 0.95:
            return "5' 5\""
        elif rounded_height == 0.94:
            return "5' 4\""
        elif rounded_height == 0.93:
            return "5' 3\""
        elif rounded_height == 0.92:
            return "5' 2\""
        elif rounded_height == 0.91:
            return "5' 1\""
        elif rounded_height <= 0.90:
            return "5' 0\""
        else:
            return "Problem, height not found in chart."

    class Expression(renpy.store.object):
        def __init__(self,name,skin_colour,facial_style):
            self.name = name
            self.skin_colour = skin_colour
            self.facial_style = facial_style #The style of face the person has, currently creatively named "Face_1", "Face_2", "Face_3", etc..
            self.emotion_set = ["default","happy","sad","angry","orgasm"]
            self.positions_set = ["stand2","stand3","stand4","stand5","walking_away","kissing","missionary","blowjob","against_wall","back_peek","sitting","standing_doggy","cowgirl"] #The set of images we are going to draw emotions for. These are positions that look towards the camera
            self.special_modifiers = {"blowjob":["blowjob"],"kissing":["kissing"]} #Special modifiers that are sometimes applied to expressions, but not always. ie. for blowjobs that may be either in normal crouching mode or blowjob mode.
            self.ignore_position_set = ["doggy","walking_away","standing_doggy"] #The set of positions that we are not goign to draw emotions for. These look away from the camera TODO: This should reference the Position class somehow.
            self.position_dict = {}
            for position in self.positions_set+self.ignore_position_set:
                self.position_dict[position] = {}

            for position in self.positions_set:
                for emotion in self.emotion_set:
                    self.position_dict[position][emotion] = emotion + "_" + facial_style + "_" + position + "_" + skin_colour + ".png"

            for position in self.ignore_position_set: #Positions that ignore emotions always use the "default" emotion for the back of the head.
                for emotion in self.emotion_set:
                    self.position_dict[position][emotion] = "default" + "_" + facial_style + "_" + position + "_" + skin_colour + ".png" ##An empty image to be drawn when we don't want to draw any emotion, because the character's face is turned away.

            for position, modifiers in self.special_modifiers.iteritems(): #Position is the key of our special modifers dict, get all the positions with a special modifier assigned.
                for modifier in modifiers: #If that position has multiple special modifers we want to add them all.
                    for emotion in self.emotion_set:
                        modified_emotion = emotion + "_" + modifier
                        self.position_dict[position][modified_emotion] = modified_emotion + "_" + facial_style + "_" + position + "_" + skin_colour + ".png"#Add a new emotion titled "<emotion>_<modifier>", for example "sad_blowjob".


        def generate_emotion_displayable(self,position,emotion, special_modifier = None):
            if not position in self.positions_set+self.ignore_position_set:
                position = "stand3"
            if not emotion in self.emotion_set:
                emotion = "default" #Get our default emotion to show if we get an incorrect one.
            elif special_modifier is not None and special_modifier in self.special_modifiers:
                emotion = emotion + "_" + special_modifier

            return Image("character_images/"+ self.position_dict[position][emotion])
            # renpy.show(self.name+position+emotion+self.facial_style,at_list=[right,scale_person(height)],layer="Active",what=self.position_dict[position][emotion],tag=self.name+position+emotion)

    class Room(renpy.store.object): #Contains people and objects.
        def __init__(self,name,formalName,connections,background_image,objects,people,actions,public,map_pos, tutorial_label = None, visible = True, hide_in_known_house_map = True):
            self.name = name
            self.formalName = formalName
            self.connections = connections
            self.background_image = background_image
            self.objects = objects
            self.objects.append(Object("stand",["Stand"], sluttiness_modifier = 0, obedience_modifier = -5)) #Add a standing position that you can always use.
            self.people = people
            self.actions = actions #A list of Action objects
            self.public = public #If True, random people can wander here. TODO: Update rooms to include this value.
            self.map_pos = map_pos #A tuple of two int values giving the hex co-ords, starting in the top left. Using this guarantees locations will always tessalate.
            self.visible = visible #If true this location is shown on the map. If false it is not on the main map and will need some other way to access it.
            self.hide_in_known_house_map = hide_in_known_house_map #If true this location is hidden in the house map, usually because their house is shown on the main map.

            self.tutorial_label = tutorial_label #When the MC first enters the room the tutorial will trigger.
            self.trigger_tutorial = True #Flipped to false once the tutorial has been done once
            self.accessable = True #If true you can move to this room. If false it is disabled

            #TODO: add an "appropriateness" or something trait that decides how approrpaite it would be to have sex, be seduced, etc. in this location.

        def link_locations(self,other): #This is a one way connection!
            self.connections.append(other)

        def link_locations_two_way(self,other): #Link it both ways. Great for adding locations after the fact, when you don't want to modify existing locations.
            self.link_locations(other)
            other.link_locations(self)

        def add_object(self,the_object):
            self.objects.append(the_object)

        def add_person(self,the_person):
            self.people.append(the_person)
            #TODO: add situational modifiers for the location

        def remove_person(self,the_person):
            self.people.remove(the_person)

        def move_person(self,the_person,the_destination):
            if not the_person in the_destination.people: # Don't bother moving people who are already there.
                self.remove_person(the_person)
                the_destination.add_person(the_person)
                #TODO: add situational modifiers for the location

        def has_person(self,the_person):
            if the_person in self.people:
                return True
            else:
                return False

        def get_person_count(self):
            return len(self.people)

        def objects_with_trait(self,the_trait):
            return_list = []
            for object in self.objects:
                if object.has_trait(the_trait):
                    return_list.append(object)
            return return_list

        def has_object_with_trait(self,the_trait):
            if the_trait == "None":
                return True
            for object in self.objects:
                if object.has_trait(the_trait):
                    return True
            return False

        def get_object_with_name(self,name): #Use this to get objects from a room when you know what they should be named but don't have an object reference yet (ik
            for obj in self.objects:
                if obj.name == name:
                    return obj
            return None

        def valid_actions(self):
            count = 0
            for act in self.actions:
                if act.is_action_enabled() or act.is_disabled_slug_shown(): #We should also check if a non-action disabled slug would be available so that the player can check what the requirement would be.
                    count += 1
            return count

        def get_valid_actions(self):
            return_list = []
            for act in self.actions:
                if act.is_action_enabled() or act.is_disabled_slug_shown():
                    return_list.append(act)
            return return_list



    class Action(renpy.store.object): #Contains the information about actions that can be taken in a room. Dispayed when you are asked what you want to do somewhere.
        # Also used for crises, those are not related to any partiular room and are not displayed in a list. They are forced upon the player when their requirement is met.
        def __init__(self,name,requirement,effect,args = None, requirement_args = None, menu_tooltip = None):
            self.name = name

            # A requirement returns False if the action should be hidden, a string if the action should be disabled but visible (the string is the reason it is not enabled), and True if the action is enabled
            self.requirement = requirement #Requirement is a function that is called when the action is checked.


            self.effect = effect #effect is a string for a renpy label that is called when the action is taken.
            if not args:
                self.args = [] #stores any arguments that we want passed to the action or requirement when the action is created. Should be a list of variables.
            elif type(args) is not list:
                self.args = [args] #Make sure our list of arguments is a list.
            else:
                self.args = args


            if not requirement_args:
                self.requirement_args = [] #A list of arguments handed to the requirement but not the actual event.
            elif not isinstance(requirement_args, list):
                self.requirement_args = [requirement_args]
            else:
                self.requirement_args = requirement_args

            self.menu_tooltip = menu_tooltip # Added to any menu item where this action is displayed

        def __cmp__(self,other): ##This and __hash__ are defined so that I can use "if Action in List" and have it find identical actions that are different instances.
            if isinstance(other, Action):
                if self.name == other.name and self.requirement == other.requirement and self.effect == other.effect and self.args == other.args:
                    return 0
                else:
                    if self.__hash__() < other.__hash__(): #Use hash values to break ties.
                        return -1
                    else:
                        return 1
            else:
                if other is None:
                    return -1
                elif self.__hash__() < other.__hash__(): #Use hash values to break ties.
                    return -1
                else:
                    return 1

        def __hash__(self):
            return hash((self.name,self.requirement,self.effect))

        def check_requirement(self, extra_args = None): #Calls the requirement function associated with this action.
        # Effectively private. Use "is_action_enabled" and "is_disabled_slug_shown" to figure out if there are important actions to display or take.
            if not extra_args: #We need to make sure we package all potential extra args as a list and hand them over.
                extra_args = []
            elif not isinstance(extra_args, list):
                extra_args = [extra_args]
            extra_args = extra_args + self.requirement_args
            return self.requirement(*extra_args)

        def is_action_enabled(self, extra_args = None):
            requirement_return = self.check_requirement(extra_args)
            if isinstance(requirement_return, basestring):
                # Any string returned means the action is not enabled
                return False
            else:
                # If it's not a string it must be a bool
                return requirement_return

        def is_disabled_slug_shown(self, extra_args = None): # Returns true if this action is not enabled but should show something when it is disabled.
            requirement_return = self.check_requirement(extra_args)
            if isinstance(requirement_return, basestring):
                return True
            else:
                return False

        def get_disabled_slug_name(self, extra_args = None): #Returns a formated name for when the
            requirement_return = self.check_requirement(extra_args)
            return self.name + "\n{size=16}{color=#ff0000}" + requirement_return + "{/color}{/size} (disabled)"

        def call_action(self, extra_args = None): #Can only use global variables. args is a list of elements you want to include as arguments. None is default
            if not extra_args:
                extra_args = []
            elif not isinstance(extra_args, list):
                extra_args = [extra_args]

            renpy.call(self.effect,*(self.args+extra_args))
            renpy.return_statement()

    class Role(renpy.store.object): #Roles are assigned to special people. They have a list of actions that can be taken when you talk to the person and acts as a flag for special dialogue options.
        def __init__(self, role_name, actions, hidden = False):
            self.role_name = role_name
            self.actions = actions # A list of actions that can be taken. These actions are shown when you talk to a person with this role if their requirement is met.
            self.hidden = hidden #A hidden role is not shown on the "Roles" list

    class Listener_Management_System(renpy.store.object): #Used to manage listeners in objects. Contains functiosn for enrolling and removing triggers as well as firing notices to those triggers.
        def __init__(self):
            self.event_dict = {} #THis dictionary uses strings as keys (the trigger that is called) and each key holds a list of goals. When an event is triggered each listener enrolled to the key recieves a notice (the on_trigger_funciton is called)

        def enroll_goal(self, trigger_name, the_goal):
            if trigger_name in self.event_dict:
                self.event_dict[trigger_name].append(the_goal) #Add the goal to the list.

            else: #The trigger_name is not in our dict, we need to add it then add the goal to it.
                self.event_dict[trigger_name] = [the_goal]

        def fire_event(self, trigger_name, **kwargs):
            if trigger_name in self.event_dict: #Make sure we have the key first before we go grabbing lists.
                completed_goals = [] #We store completed goals in a seperate list to let us flag things for removal without
                for goal in self.event_dict[trigger_name]:
                    if goal.call_trigger(**kwargs): #on_trigger returns true if the goal is finished and we can stop letting it know.
                        completed_goals.append(goal)
                for goal in completed_goals:
                    goal.complete_goal()
                    self.event_dict[trigger_name].remove(goal) #Remove all completed goals, they are no longer important.



    class Goal(renpy.store.object):
        def __init__(self, goal_name, goal_description, event_name, listener_type, valid_goal_function, on_trigger_function, arg_dict = None, difficulty_scale_function = None, report_function = None, progress_fraction_function = None, mandatory = False):
            self.name = goal_name #Short form name to be displayed to the player, generally on a progress bar of some sort.
            self.description = goal_description #A long form fluff description of the goal purpose.
            self.event_name = event_name #The event (aka a string to give to a listnener manager) that this goal listens to.
            self.listener_type = listener_type #Either "MC" or "Business", decides which object the goal will grab as their listener manager when you ask it to enroll.
            self.valid_goal_function = valid_goal_function #A function called to check to see if the goal is a valid/reasonable one to give to the player.
            self.on_trigger_function = on_trigger_function #A function called by an event listener that that this goal is hooked up to.
            if arg_dict: #A dict to hold arguments you want to be used by the on_trigger function without having to get specific about what they are here.
                self.arg_dict = arg_dict
            else:
                self.arg_dict = {}

            self.completed = False #A flag set to true when the goal is finished, so the player can complete the objective and claim their bonus point.

            self.difficulty_scale_function = difficulty_scale_function #A function called when the goal is activated (aka when it is copied from the default goal) to scale the paramaters to the current difficulty.
            self.report_function = report_function
            self.progress_fraction_function = progress_fraction_function
            self.mandatory = mandatory

        def __cmp__(self,other):
            if self.name == other.name:
                if self.description == other.description:
                    if self.valid_goal_function == other.valid_goal_function:
                        if self.on_trigger_function == other.on_trigger_function:
                            if self.arg_dict == other.arg_dict:
                                return 0
            if self.__hash__() > other.__hash__():
                return 1
            else:
                return -1


        def __hash__(self):
            return hash((self.name, self.description, self.valid_goal_function, self.on_trigger_function))

        def activate_goal(self, difficulty):
            if self.listener_type == "MC": #Figure out what listener we should be listening to
                listener = mc.listener_system
            else: #== "Business"
                listener = mc.business.listener_system

            if self.difficulty_scale_function:
                self.difficulty_scale_function(self, difficulty) #If we have a function for changing difficulty hand it ourselves and the difficulty we were activated at.

            listener.enroll_goal(self.event_name, self) #Enroll us to the proper listener and hand it us so it will call our trigger when we need it to.

        def get_reported_progress(self): #Returns a string corisponding to the current progress of the goal. Generally something like "5 of 10" or "3/20".
            if self.completed:
                return "Completed"
            elif self.report_function:
                return self.report_function(self)
            else:
                return "In Progress"

        def get_progress_fraction(self):
            if self.progress_fraction_function:
                return self.progress_fraction_function(self)
            else:
                return 0.0

        def call_trigger(self, **kwargs):
            return self.on_trigger_function(self, **kwargs)

        def complete_goal(self):
            self.completed = True




    class Policy(renpy.store.object): # An upgrade that can be purchased by the character for their business.
        def __init__(self,name,desc,requirement,cost, on_buy_function = None, on_buy_arguments = None):
            self.name = name #A short name for the policy.
            self.desc = desc #A text description of the policy.
            self.requirement = requirement #a function that is run to see if the PC can purchase this policy.
            self.cost = cost #Cost in dollars.
            self.on_buy_function = on_buy_function #A function to be called when purchased
            self.on_buy_arguments = on_buy_arguments #A dictionary of values to be given to the function.

        def __cmp__(self,other): #
            if isinstance(other, Policy):
                if self.name == other.name and self.desc == other.desc and self.cost == other.cost:
                    return 0
                else:
                    if self.__hash__() < other.__hash__(): #Use hash values to break ties.
                        return -1
                    else:
                        return 1

            else:
                if self.__hash__() < other.__hash__(): #Use hash values to break ties.
                    return -1
                else:
                    return 1

        def __hash__(self):
            return hash((self.name,self.desc,self.cost))

        def buy_policy(self):
            mc.business.funds -= self.cost
            if self.on_buy_function is not None:
                self.on_buy_function(**self.on_buy_arguments)

        def is_owned(self):
            if self in mc.business.policy_list:
                return True
            else:
                return False

    class Object(renpy.store.object): #Contains a list of traits for the object which decides how it can be used.
        def __init__(self,name,traits,sluttiness_modifier = 0, obedience_modifier = 0):
            self.traits = traits
            self.name = name
            self.sluttiness_modifier = sluttiness_modifier #Changes a girls sluttiness when this object is used in a sex scene
            self.obedience_modifier = obedience_modifier #Changes a girls obedience when this object is used in a sex scene.

        def has_trait(self,the_trait):
            for trait in self.traits:
                if trait == the_trait:
                    return True
            return False

        def get_formatted_name(self):
            if not (self.sluttiness_modifier == 0 and self.obedience_modifier == 0):
                the_string = self.name + "\n{size=22}"
                if self.sluttiness_modifier < 0:
                    the_string += str(self.sluttiness_modifier) + " Sluttiness"
                    if not self.obedience_modifier == 0:
                        the_string += ", "
                if self.sluttiness_modifier > 0:
                    the_string += "+" + str(self.sluttiness_modifier) + " Sluttiness"
                    if not self.obedience_modifier == 0:
                        the_string += ", "

                if self.obedience_modifier < 0:
                    the_string += str(self.obedience_modifier) + " Obedience"

                if self.obedience_modifier >0:
                    the_string += "+" + str(self.obedience_modifier) + " Obedience"

                the_string += "{/size} (tooltip)The object you have sex on influences how enthusiastic and obedient a girl will be."
                return the_string
            else:
                return self.name

    class Clothing(renpy.store.object):
        #Slots are

        ##Feet##
        #Layer 1: Socks
        #Layer 2: Shoes

        ##Lower Body##
        #Layer 1: Panties
        #Layer 2: Pantyhose
        #Layer 3: Pants/Skirt

        ##Upper Body##
        #Layer 1: Bra
        #Layer 2: Shirt
        #Layer 3: Jacket

        ##Accessories##
        #Layer 1: Skin level
        #Layer 2: Over underwear
        #Layer 3: Over shirts
        #Layer 4: Over everything

        def __init__(self, name, layer, hide_below, anchor_below, proper_name, draws_breasts, underwear, slut_value, has_extension = None, is_extension = False, colour = None, tucked = False, body_dependant = True,
        opacity_adjustment = 1, whiteness_adjustment = 0.0, contrast_adjustment = 1.0, supported_patterns = None, pattern = None, colour_pattern = None):
            self.name = name
            self.proper_name = proper_name #The true name used in the file system
            self.hide_below = hide_below #If true, it hides the clothing beneath so you can't tell what's on.
            self.anchor_below = anchor_below #If true, you must take this off before you can take off anything of a lower layer.
            self.layer = layer #A list of the slots above that this should take up or otherwise prevent ffrom being filled. Slots are a list of the slot and the layer.

            self.position_sets = {} #A list of position set names. When the clothing is created it will make a dict containing these names and image sets for them.
            self.pattern_sets = {} #A list of patterns for this piece of clothing that are valid. Keys are in the form "position_patternName"
            self.supported_positions = ["stand2","stand3","stand4","stand5","walking_away","kissing","doggy","missionary","blowjob","against_wall","back_peek","sitting","standing_doggy","cowgirl"]
            self.supported_patterns = supported_patterns
            if not supported_patterns:
                self.supported_patterns = {"Default":None}
            self.supported_patterns["Default"] = None

            for set in self.supported_positions:
                self.position_sets[set] = Clothing_Images(proper_name,set,draws_breasts, body_dependant = body_dependant)
                if supported_patterns:
                    for the_pattern in supported_patterns:
                        pattern_name = supported_patterns[the_pattern]
                        if pattern_name:
                            self.pattern_sets[set + "_" + pattern_name] = Clothing_Images(proper_name+"_"+pattern_name, set, draws_breasts, body_dependant = body_dependant)


            self.draws_breasts = draws_breasts
            self.underwear = underwear #True if the item of clothing satisfies the desire for underwear for upper or lower (bra or panties), false if it can pass as outerwear. Underwear on outside of outfit gives higher slut requirement.
            self.slut_value = slut_value #The amount of sluttiness that this piece of clothing adds to an outfit.
            self.has_extension = has_extension #If the item of clothing spans two zones (say, lower and feet or upper and lower body) has_extension points towards the placeholder item that fills the other part.
            self.is_extension = is_extension #If this is true the clothing item exists only as a placeholder. It will draw nothing and not be removed unless the main piece is removed.
            if not colour:
                self.colour = [1,1,1,1]
            else:
                self.colour = colour
            self.tucked = tucked #Items of clothign that are tucked are drawn a "half level", aka we cycle thorugh all layer 2's and do untucked items, then do all tucked items.

            self.body_dependant = body_dependant #Items that are not body dependant are always draw as if they are on a standard body, ideal for facial accessories that do not vary with emotion like earings.

            self.whiteness_adjustment = whiteness_adjustment #A modifier applied to the greyscale version of a piece of clothing to bring it closer to a white piece of clothing instead of grey. Default is 0, ranges from -1 to 1.
            self.contrast_adjustment = contrast_adjustment #Changes the contrast, good for getting proper whites and blacks after changing whiteness. Default is 1.0, 0.0 is min contrast, >1 is increasing contrast
            self.opacity_adjustment = opacity_adjustment #An opacity modifier applied to the piece of clothing before any other modifiers are considered (including colour). A value >1 makes slightly transparent clothing opaque, perfect for fixing imperfect renders.

            self.pattern = pattern #If not none this should be a string that will let us find the proper pattern mask.
            if not colour_pattern:
                self.colour_pattern = [1,1,1,1]
            else:
                self.colour_pattern = colour_pattern #If there is a pattern assigned this is the colour used for the masked section.
        def __cmp__(self,other):
            if isinstance(self, type(other)):
                if self.name == other.name and self.hide_below == other.hide_below and self.layer == other.layer and self.is_extension == other.is_extension:
                    return 0

            if self.__hash__() < other.__hash__():
                return -1
            else:
                return 1

        def __hash__(self):
            return hash((self.name,self.hide_below,self.anchor_below,self.layer,self.draws_breasts,self.underwear,self.slut_value))

        def get_copy(self): #Returns a copy of the piece of clothing with the correct underlying references.
            return copy.copy(self)

        def get_layer(self,body_type,tit_size):
            return self.layer

        def generate_item_displayable(self,body_type, tit_size, position):
            if not self.is_extension: #We don't draw extension items, because the image is taken care of in the main object.
                if not self.body_dependant:
                    body_type = "standard_body"

                image_set = self.position_sets.get(position) # The image set we are using should corrispond to the set named "positon".
                if image_set == None: # If no image set is found with that name in the dict, use the default standing one instead. Standing should always exist.
                    image_set = self.position_sets.get("stand3") #Position names are always lowercase.

                if self.draws_breasts:
                    the_image = image_set.get_image(body_type, tit_size)
                else:
                    the_image = image_set.get_image(body_type, "AA")


                converted_mask_image = None
                inverted_mask_image = None
                if self.pattern is not None:
                    if self.draws_breasts:
                        mask_image = self.pattern_sets.get(position+"_"+self.pattern).get_image(body_type, tit_size)
                    else:
                        mask_image = self.pattern_sets.get(position+"_"+self.pattern).get_image(body_type, "AA")

                    if mask_image is None:
                        self.pattern = None
                    else:
                        inverted_mask_image = im.MatrixColor(mask_image, [1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,-1,1]) #Generate the masks that will be used to determine what is colour A and B
                        mask_image = im.MatrixColor(mask_image, [1,0,0,0,0, 0,1,0,0,0, 0,0,1,0,0, 0,0,0,1,0])



                brightness_matrix = im.matrix.brightness(self.whiteness_adjustment)
                contrast_matrix = im.matrix.contrast(self.contrast_adjustment)
                opacity_matrix = im.matrix.opacity(self.opacity_adjustment) #Sets the clothing to the correct colour and opacity.

                #This is the base greyscale image we have
                greyscale_image = im.MatrixColor(the_image, opacity_matrix * brightness_matrix * contrast_matrix) #Set the image, which will crush all modifiers to 1 (so that future modifiers are applied to a flat image correctly with no unusually large images


                colour_matrix = im.matrix.tint(self.colour[0], self.colour[1], self.colour[2])
                alpha_matrix = im.matrix.opacity(self.colour[3])
                shader_image = im.MatrixColor(greyscale_image, alpha_matrix * colour_matrix) #Now colour the final greyscale image


                if self.pattern is not None:
                    colour_pattern_matrix = im.matrix.tint(self.colour_pattern[0], self.colour_pattern[1], self.colour_pattern[2])
                    pattern_alpha_matrix = im.matrix.opacity(self.colour_pattern[3] * self.colour[3]) #The opacity of the pattern is relative to the opacity of the entire piece of clothing.
                    shader_pattern_image = im.MatrixColor(greyscale_image, pattern_alpha_matrix * colour_pattern_matrix)

                    final_image = AlphaBlend(mask_image, shader_image, shader_pattern_image, alpha=False)


                if self.pattern: #If we have been able to generate a pattern we present the composited single displayable item.
                    return final_image
                else: #Otherwise it was either a no-pattern piece of clothing OR we failed to produce the correct pattern.
                    return shader_image


    class Facial_Accessory(Clothing): #This class inherits from Clothing and is used for special accessories that require extra information
        def __init__(self, name, layer, hide_below, anchor_below, proper_name, draws_breasts, underwear, slut_value, has_extension = None, is_extension = False, colour = None, tucked = False,
            opacity_adjustment = 1, whiteness_adjustment = 0.0, contrast_adjustment = 1.0):

            self.name = name
            self.proper_name = proper_name
            self.hide_below = hide_below #If true, it hides the clothing beneath so you can't tell what's on.
            self.anchor_below = anchor_below #If true, you must take this off before you can take off anything of a lower layer.f
            self.layer = layer #A list of the slots above that this should take up or otherwise prevent from being filled. Slots are a list of the slot and the layer.

            self.position_sets = {} #A list of position set names. When the clothing is created it will make a dict containing these names and image sets for them.
            self.supported_positions = ["stand2","stand3","stand4","stand5","walking_away","kissing","doggy","missionary","blowjob","against_wall","back_peek","sitting","standing_doggy","cowgirl"]


            for set in self.supported_positions:
                self.position_sets[set] = Facial_Accessory_Images(proper_name,set)

            self.draws_breasts = draws_breasts
            self.underwear = underwear #True if the item of clothing satisfies the desire for underwear for upper or lower (bra or panties), false if it can pass as outerwear. Underwear on outside of outfit gives higher slut requirement.
            self.slut_value = slut_value #The amount of sluttiness that this piece of clothing adds to an outfit.
            self.has_extension = has_extension #If the item of clothing spans two zones (say, lower and feet or upper and lower body) has_extension points towards the placeholder item that fills the other part.
            self.is_extension = is_extension #If this is true the clothing item exists only as a placeholder. It will draw nothing and not be removed unless the main piece is removed.
            if not colour:
                self.colour = [1,1,1,1]
            else:
                self.colour = colour
            self.tucked = tucked #Items of clothing that are tucked are drawn a "half level", aka we cycle thorugh all layer 2's and do untucked items, then do all tucked items.

            self.opacity_adjustment = opacity_adjustment
            self.whiteness_adjustment = whiteness_adjustment
            self.contrast_adjustment = contrast_adjustment

        def generate_item_displayable(self, position, face_type, emotion, special_modifiers = None):
            if not self.is_extension:

                image_set = self.position_sets.get(position)
                if image_set is None:
                    image_set = self.position_sets.get("stand3") #Get a default image set if we are looking at a position we do not have.

                the_image = image_set.get_image(face_type, emotion, special_modifiers)
                if not the_image:
                    the_image = image_set.get_image(face_type, emotion) # If we weren't able to get something with the special modifier just use a default to prevent a crash.

                brightness_matrix = im.matrix.brightness(self.whiteness_adjustment)
                contrast_matrix = im.matrix.contrast(self.contrast_adjustment)
                opacity_matrix = im.matrix.opacity(self.opacity_adjustment) #Sets the clothing to the correct colour and opacity.

                greyscale_image = im.MatrixColor(the_image, opacity_matrix * brightness_matrix * contrast_matrix) #Set the image, which will crush all modifiers to 1 (so that future modifiers are applied to a flat image correctly with no unusually large images

                colour_matrix = im.matrix.tint(self.colour[0], self.colour[1], self.colour[2])
                alpha_matrix = im.matrix.opacity(self.colour[3])
                shader_image = im.MatrixColor(greyscale_image, alpha_matrix * colour_matrix) #Now colour the final greyscale image

                #shader_image = im.Recolor(the_image.filename,int(self.colour[0]*255),int(self.colour[1]*255),int(self.colour[2]*255),int(self.colour[3]*255))
                # shader_image = ShaderDisplayable(shader.MODE_2D, the_image.filename, shader.VS_2D,PS_COLOUR_SUB_LR2,{},uniforms={"colour_levels":self.colour})
                return shader_image


    class Facial_Accessory_Images(renpy.store.object):
        def __init__(self,accessory_name,position):
            self.images = {}
            self.supported_faces = ["Face_1","Face_2","Face_3","Face_4","Face_5","Face_6"]
            self.supported_emotions = ["default","sad","happy","angry","orgasm"]
            self.special_modifiers = {"blowjob":"blowjob","kissing":"kissing"}

            for face in self.supported_faces:
                for emotion in self.supported_emotions:
                    #Add the image string to the dict. We do not use Image obects directly because it greatly slows down the game (character objects become huge.)
                    #self.images[face + "_" + emotion] = "character_images/" + accessory_name + "_" + position + "_" + face + "_" + emotion + ".png" # Save the file string so we can generate a proper image from it easily later.

                    self.images[face + "_" + emotion] = accessory_name + "_" + position + "_" + face + "_" + emotion + ".png" # Save the file string so we can generate a proper image from it easily later.

                    if position in self.special_modifiers:
                        #self.images[face + "_" + emotion + "_" + self.special_modifiers[position]] = "character_images/" + accessory_name + "_" + position + "_" + face + "_" + emotion + "_" + self.special_modifiers[position] + ".png"

                        self.images[face + "_" + emotion + "_" + self.special_modifiers[position]] = accessory_name + "_" + position + "_" + face + "_" + emotion + "_" + self.special_modifiers[position] + ".png"
                        #There is a special modifier, we need to add that version as well.

        def get_image(self, face, emotion, special_modifier = None):
            index_string = face + "_" + emotion
            if not special_modifier is None:
                if renpy.loadable("character_images/" + self.images[index_string + "_" + special_modifier]):
                    index_string += "_" + special_modifier #We only want to try and load special modifier images if they exist. Otherwise we use the unmodified image to avoid a crash. This lets us omit images we do not plan on actually using, such as glasses not needing blowjob poses.

            return Image("character_images/" + self.images[index_string])
            #return Image(self.images[index_string]) #We have made an index string, use it to get the full filepath for the image used in this position.

    class Clothing_Images(renpy.store.object): # Stores a set of images for a single piece of cloting in a single position. The position is stored when it is put into the clothing object dict.
        def __init__(self,clothing_name,position_name,is_top, body_dependant = True):

            self.images = {}
            if body_dependant:
                self.body_types = ["standard_body","thin_body","curvy_body"]
            else:
                self.body_types = ["standard_body"]

            self.breast_sizes = ["AA","A","B","C","D","DD","DDD","E","F","FF"]

            for body in self.body_types:
                if is_top:
                    for breast in self.breast_sizes:
                        self.images [body + "_" + breast] = clothing_name+"_"+position_name+"_"+body+"_"+breast+".png"
                else:
                    self.images[body + "_AA"] = clothing_name+"_"+position_name+"_"+body+"_AA.png"

        def get_image(self, body_type, breast_size = "AA" ): #Generates a proper Image object from the file path strings we have stored previously. Prevents object bloat by storing large objects repeatedly for everyone.
            index_string = body_type + "_" + breast_size
            return Image("character_images/" + self.images[index_string])
            #return Image(self.images[index_string])


    class Outfit(renpy.store.object): #A bunch of clothing added together, without slot conflicts.
        def __init__(self,name):
            self.name = name
            self.upper_body = []
            self.lower_body = []
            self.feet = []
            self.accessories = [] #Extra stuff that doesn't fit anywhere else. Hats, glasses, ect.
            self.slut_requirement = 0 #The slut score requirement for this outfit.
            self.update_slut_requirement()

        def get_copy(self):
            copy_outfit = Outfit(self.name)

            for feet in self.feet:
                copy_outfit.feet.append(feet.get_copy())

            for lower in self.lower_body:
                copy_outfit.lower_body.append(lower.get_copy())

            for upper in self.upper_body:
                copy_outfit.upper_body.append(upper.get_copy())

            for accessory in self.accessories:
                copy_outfit.accessories.append(accessory.get_copy())
            copy_outfit.update_slut_requirement() #Make sure to properly set sluttiness because we haven't used the correct functions to add otherwise.

            return copy_outfit

        def generate_draw_list(self, the_person, position, emotion = "default", special_modifiers = None): #Generates a sorted list of displayables that when drawn display the outfit correctly.
            if the_person is None:
                body_type = "standard_body"
                tit_size = "D"
                face_style = "Face_1"

            else:
                body_type = the_person.body_type
                tit_size = the_person.tits
                face_style = the_person.face_style

            all_items = self.generate_clothing_list(body_type, tit_size, position) #First generate a list of the clothing objects
            ordered_displayables = []

            for item in all_items:
                if isinstance(item, Facial_Accessory):
                    ordered_displayables.append(item.generate_item_displayable(position, face_style, emotion, special_modifiers))
                else:
                    if not item.is_extension:
                        ordered_displayables.append(item.generate_item_displayable(body_type, tit_size, position))
            return ordered_displayables

        def generate_split_draw_list(self, split_on_clothing, the_person, position, emotion = "default", special_modifiers = None): #Mirrors generate draw list but returns only the clothing above and below the given item as two lists with the item in between (in a tuple)
            if the_person is None:
                body_type = "standard_body"
                tit_size = "D"
                face_style = "Face_1"

            else:
                body_type = the_person.body_type
                tit_size = the_person.tits
                face_style = the_person.face_style

            on_bottom = True #Checks to see if we are adding things to the top or bottom list, flips when it sees the split_on_clothing item
            bottom_items = [] #Things drawn below the middle item
            middle_item = None #The displayable for the middle item
            top_items = [] #Things drawn on top of the middle item
            all_items = self.generate_clothing_list(body_type, tit_size, position)

            for item in all_items:
                if isinstance(item, Facial_Accessory):
                    item_check = item.generate_item_displayable(position, face_style, emotion, special_modifiers)
                else:
                    if not item.is_extension:
                        item_check = item.generate_item_displayable(body_type, tit_size, position)

                if not item.is_extension:
                    if item == split_on_clothing:
                        middle_item = item_check
                        on_bottom = False
                    else:
                        if on_bottom:
                            bottom_items.append(item_check)
                        else:
                            top_items.append(item_check)
            return (bottom_items,middle_item,top_items)

        def generate_clothing_list(self, body_type, tit_size, position): #Returns a properly ordered list of clothing. If used to draw them they would be displayed correctly.
            items_to_draw = self.accessories + self.feet + self.lower_body + self.upper_body #Throw all of our items in a list.
            items_to_draw.sort(key= lambda clothing: clothing.tucked, reverse = True)
            items_to_draw.sort(key= lambda clothing: clothing.layer) #First, sort by clothing layer.
             #Next, modify things that are tucked into eachother.
            return items_to_draw

        def can_add_dress(self, new_clothing):
            return self.can_add_upper(new_clothing)

        def add_dress(self, new_clothing, re_colour = None, pattern = None, colour_pattern = None):
            self.add_upper(new_clothing, re_colour = None, pattern = None, colour_pattern = None)

        def can_add_upper(self, new_clothing):
            allowed = True
            for cloth in self.upper_body:
                if cloth.layer == new_clothing.layer:
                    allowed = False

            if new_clothing.has_extension: #It's a dress with a top and a bottom, make sure we can add them both!
                for cloth in self.lower_body:
                    if cloth.layer == new_clothing.has_extension.layer:
                        allowed = False

            return allowed

        def add_upper(self, new_clothing, re_colour = None, pattern = None, colour_pattern = None):
            if re_colour is not None:
                new_clothing.colour = re_colour

            if pattern is not None:
                new_clothing.pattern = pattern
                if colour_pattern is not None:
                    new_clothing.colour_pattern = colour_pattern
                else:
                    new_clothing.colour_pattern = new_clothing.colour

            if self.can_add_upper(new_clothing): ##Always check to make sure the clothing is valid before you add it.
                self.upper_body.append(new_clothing)
                if new_clothing.has_extension:
                    self.lower_body.append(new_clothing.has_extension)
                self.update_slut_requirement()

        def can_add_lower(self,new_clothing):
            allowed = True
            for cloth in self.lower_body:
                if cloth.layer == new_clothing.layer:
                    allowed = False
            return allowed

        def add_lower(self, new_clothing, re_colour = None, pattern = None, colour_pattern = None):
            if re_colour is not None:
                new_clothing.colour = re_colour
            if pattern is not None:
                new_clothing.pattern = pattern
                if colour_pattern is not None:
                    new_clothing.colour_pattern = colour_pattern
                else:
                    new_clothing.colour_pattern = new_clothing.colour

            if self.can_add_lower(new_clothing):
                self.lower_body.append(new_clothing)
                self.update_slut_requirement()

        def can_add_feet(self, new_clothing):
            allowed = True
            for cloth in self.feet:
                if cloth.layer == new_clothing.layer:
                    allowed = False
            return allowed

        def add_feet(self, new_clothing, re_colour = None, pattern = None, colour_pattern = None):
            if re_colour is not None:
                new_clothing.colour = re_colour

            if pattern is not None:
                new_clothing.pattern = pattern
                if colour_pattern is not None:
                    new_clothing.colour_pattern = colour_pattern
                else:
                    new_clothing.colour_pattern = new_clothing.colour

            if self.can_add_feet(new_clothing):
                self.feet.append(new_clothing)
                self.update_slut_requirement()

        def can_add_accessory(self, new_clothing):
            allowed = True #For now all we do not filter what accessories we let people apply. All we require is that this exact type of accessory is not already part of the outfit.
            for accessory in self.accessories:
                if accessory == new_clothing:
                    allowed = False
            return allowed

        def add_accessory(self,new_clothing, re_colour = None, pattern = None, colour_pattern = None):
            if re_colour is not None:
                new_clothing.colour = re_colour
            if pattern is not None:
                new_clothing.pattern = None
                if colour_pattern is not None:
                    new_clothing.colour_pattern = colour_pattern
                else:
                    new_clothing.colour_pattern = new_clothing.colour

            if self.can_add_accessory(new_clothing):
                self.accessories.append(new_clothing)
                self.update_slut_requirement()

        def has_clothing(self, the_clothing): #Returns True if this outfit includes the given clothing item, false otherwise. Checks only for exact match (ie. down to exact colour, opacity, etc.)
            if the_clothing in self.upper_body:
                return True
            elif the_clothing in self.lower_body:
                return True
            elif the_clothing in self.feet:
                return True
            elif the_clothing in self.accessories:
                return True
            return False

        def remove_clothing(self, old_clothing):
            #TODO: make sure this works with dresses when you remove the bottom (ie. extension) first.
            if old_clothing.has_extension:
                self.remove_clothing(old_clothing.has_extension)

            if old_clothing in self.upper_body:
                self.upper_body.remove(old_clothing)
            elif old_clothing in self.lower_body:
                self.lower_body.remove(old_clothing)
            elif old_clothing in self.feet:
                self.feet.remove(old_clothing)
            elif old_clothing in self.accessories:
                self.accessories.remove(old_clothing)

            self.update_slut_requirement()

        def get_upper_ordered(self): #Returns a list of pieces from bottom to top, on the upper body. Other functions do similar things, but to lower and feet.
            return sorted(self.upper_body, key=lambda clothing: clothing.layer)

        def get_lower_ordered(self):
            return sorted(self.lower_body, key=lambda clothing: clothing.layer)

        def get_upper_top_layer(self):
            if self.get_upper_ordered():
                return self.get_upper_ordered()[-1]
            return None

        def get_lower_top_layer(self):
            if self.get_lower_ordered():
                return self.get_lower_ordered()[-1]
            return None

        def get_feet_ordered(self):
            return sorted(self.feet, key=lambda clothing: clothing.layer)

        def get_upper_visible(self):
            return get_visible_list(self.upper_body)

        def get_lower_visible(self):
            return get_visible_list(self.lower_body)

        def get_feet_visible(self):
            return get_visible_list(self.feet)

        def remove_random_any(self, top_layer_first = False, exclude_upper = False, exclude_lower = False, exclude_feet = False, do_not_remove = False):
            #Picks a random upper, lower, or feet object to remove. Is guaranteed to remove something if possible, or return None if nothing on the person is removable (They're probably naked).
            functs_to_try = []
            if not exclude_upper:
                functs_to_try.append(self.remove_random_upper)
            if not exclude_lower:
                functs_to_try.append(self.remove_random_lower)
            if not exclude_feet:
                functs_to_try.append(self.remove_random_feet)
            renpy.random.shuffle(functs_to_try) #Shuffle the functions so they appear in a random order.
            for remover in functs_to_try: #Try removing each of an upper, lower, and feet. If any succeed break there and return what we removed. Otherwise keep trying. If we run out of things to try we could not remove anything.
                success = remover(top_layer_first, do_not_remove)
                if success:
                    return success
            return None

        def remove_random_upper(self, top_layer_first = False, do_not_remove = False):
            #if top_layer_first only the upper most layer is removed, otherwise anything unanchored is a valid target.
            #if do_not_remove is set to True we only use this to find something valid to remove and return that clothing item. this lets us use this function to find thigns to remove with an animation.
            #Returns None if there is nothing to be removed.
            to_remove = None
            if top_layer_first:
                #Just remove the very top layer
                if self.get_upper_unanchored():
                    to_remove = self.get_upper_unanchored()[0]
                else:
                    return None
            else:
                to_remove = get_random_from_list(self.get_upper_unanchored())

            if to_remove and not do_not_remove:
                self.remove_clothing(to_remove)
            return to_remove

        def remove_random_lower(self, top_layer_first = False, do_not_remove = False):
            to_remove = None
            if top_layer_first:
                #Just remove the very top layer
                if self.get_lower_unanchored():
                    to_remove = self.get_lower_unanchored()[0]
                else:
                    return None
            else:
                to_remove = get_random_from_list(self.get_lower_unanchored())

            if to_remove and not do_not_remove:
                self.remove_clothing(to_remove)
            return to_remove

        def remove_random_feet(self, top_layer_first = False, do_not_remove = False):
            to_remove = None
            if top_layer_first:
                #Just remove the very top layer
                if self.get_foot_unanchored():
                    to_remove = self.get_foot_unanchored()[0]
                else:
                    return None
            else:
                to_remove = get_random_from_list(self.get_foot_unanchored())

            if to_remove and not do_not_remove:
                self.remove_clothing(to_remove)
            return to_remove

        def get_unanchored(self): #Returns a list of the pieces of clothing that can be removed.
            #Question: should be be able to remove accessories like this? We would need a way to flag some things like makeup as unremovable.
            return_list = []
            return_list.extend(self.get_upper_unanchored())
            return_list.extend(self.get_lower_unanchored())
            return_list.extend(self.get_foot_unanchored())

            return return_list

        def is_item_unanchored(self, the_clothing): #Returns true if the clothing item passed is unanchored, ie. could be logically taken off.
            if the_clothing in self.upper_body:
                if the_clothing in self.get_upper_unanchored():
                    return True
                else:
                    return False

            elif the_clothing in self.lower_body:
                if the_clothing in self.get_lower_unanchored():
                    return True
                else:
                    return False

            elif the_clothing in self.feet:
                if the_clothing in self.get_foot_unanchored():
                    return True
                else:
                    return False

            else:
                return True

        def get_upper_unanchored(self):
            return_list = []
            for top in reversed(sorted(self.upper_body, key=lambda clothing: clothing.layer)):
                if top.has_extension is None:
                    return_list.append(top)
                elif self.is_item_unanchored(top.has_extension):
                    return_list.append(top)


                if top.anchor_below:
                    break #Search the list, starting at the outermost item, until you find something that anchors the stuff below it.
            return return_list

        def get_lower_unanchored(self):
            return_list = []
            for bottom in reversed(sorted(self.lower_body, key=lambda clothing: clothing.layer)):
                if bottom.has_extension is None or self.is_item_unanchored(bottom.has_extension):
                    return_list.append(bottom)

                if bottom.anchor_below:
                    break
            return return_list

        def get_foot_unanchored(self):
            return_list = []
            for foot in reversed(sorted(self.feet, key=lambda clothing: clothing.layer)):
                if foot.has_extension is None or self.is_item_unanchored(foot.has_extension):
                    return_list.append(foot)

                if foot.anchor_below:
                    break
            return return_list


        def vagina_available(self): ## Doubles for asshole for anal.
            reachable = True
            for cloth in self.lower_body:
                if cloth.anchor_below:
                    reachable = False
            return reachable

        def vagina_visible(self):
            visible = True
            for cloth in self.lower_body:
                if cloth.hide_below:
                    visible = False
            return visible

        def tits_available(self):
            reachable = True
            for cloth in self.upper_body:
                if cloth.anchor_below:
                    reachable = False
            return reachable

        def tits_visible(self):
            visible = True
            for cloth in self.upper_body:
                if cloth.hide_below:
                    visible = False
            return visible

        def wearing_bra(self):
            if self.get_upper_ordered():
                if self.get_upper_ordered()[0].underwear:
                    return True
            return False

        def get_bra(self): #returns our bra object if one exists, None otherwise
            if self.get_upper_ordered():
                if self.get_upper_ordered()[0].underwear:
                    return self.get_upper_ordered()[0]
            return None

        def wearing_panties(self):
            if self.get_lower_ordered():
                if self.get_lower_ordered()[0].underwear:
                    return True
            return False

        def get_panties(self):
            if self.get_lower_ordered():
                if self.get_lower_ordered()[0].underwear:
                    return self.get_lower_ordered()[0]
            return None

        def bra_covered(self):
            if self.get_upper_ordered():
                if not self.get_upper_ordered()[-1].underwear:
                    return True
            return False

        def panties_covered(self):
            if self.get_lower_ordered():
                if not self.get_lower_ordered()[-1].underwear:
                    return True
            return False

        def is_suitable_underwear_set(self): #Returns true if the outfit could qualify as an underwear set ie. Only layer 1 clothing.
            for cloth in self.accessories + self.upper_body + self.lower_body + self.feet:
                if cloth.layer > 1:
                    return False
            return True

        def is_suitable_overwear_set(self): #Returns true if the outfit could qualify as an overwear set ie. contains no layer 1 clothing.
            for cloth in self.accessories + self.upper_body + self.lower_body + self.feet:
                if cloth.layer < 2:
                    return False
            return True

        def get_total_slut_modifiers(self): #Calculates the sluttiness boost purely do to the different pieces of clothing and not what is hidden/revealed.
            new_score = 0
            for cloth in self.accessories + self.upper_body + self.lower_body + self.feet: #Add the extra sluttiness values of any of the pieces of clothign we're wearing.
                new_score += cloth.slut_value
            return new_score

        def get_underwear_slut_score(self): #Calculates the sluttiness of this outfit assuming it's an underwear set. We assume a modest overwear set is used (ie. one that covers visibility).
            new_score = 0
            if self.tits_available():
                new_score += 20

            if self.vagina_available():
                new_score += 20

            new_score += self.get_total_slut_modifiers()

            return new_score


        def get_overwear_slut_score(self): #Calculates the sluttiness of this outfit assuming it's an overwear set. That means we assume a modest underwear set is used (ie. one that denies access).
            new_score = 0
            if self.tits_visible():
                new_score += 20

            if self.vagina_visible():
                new_score += 20

            new_score += self.get_total_slut_modifiers()

            return new_score


        def get_full_outfit_slut_score(self): #Calculates the sluttiness of this outfit assuming it's a full outfit. Full penalties and such apply.
            new_score = 0

            if self.tits_available(): # You can reach your tits easily for a titfuck.
                new_score += 20
            if self.tits_visible(): # Everyone can see your tits clearly.
                new_score += 20
            else:
                if self.wearing_bra(): #We're wearing a bra, is it covered though?
                    if not self.bra_covered(): #You're wearing a bra but no top over it, in between nude and clothed in terms of sluttiness.
                        new_score += 20

                else: #We aren't wearing a bra but it would have helped.
                    new_score += 10

            if self.vagina_available(): # You can reach your tits easily for a titfuck.
                new_score += 20
            if self.vagina_visible(): # Everyone can see your tits clearly.
                new_score += 20
            else:
                if self.wearing_panties():
                    if not self.panties_covered():
                        new_score += 20
                else:
                    new_score += 10

            new_score += self.get_total_slut_modifiers()

            return new_score

        def update_slut_requirement(self): # Recalculates the slut requirement of the outfit. Should be called after each new addition.
            self.slut_requirement = self.get_full_outfit_slut_score()

        def get_slut_requirement(self): #A getter function for slut_requriement to be used for functional programming stuff.
            return self.slut_requirement

    def get_visible_list(list):
        temp_list = sorted(list, key=lambda clothing: clothing.layer) #Get a sorted list
        return_list = []
        visible = True #top layer is always visisble
        for cloth in reversed(temp_list): #Starting at the top layer (ie. 3, jackets and such)
            if visible == True: #If it's visible, add it to the list
                return_list.append(cloth)
                if cloth.hide_below: #If it hides everything below, do stop it from being visible. Nothing else will be added to the retrn list now.
                    visible = False
        return return_list


    class Wardrobe(renpy.store.object): #A bunch of outfits!
        def __init__(self,name,outfits = None, underwear_sets = None, overwear_sets = None): #Outfits is a list of Outfit objects, or empty if the wardrobe starts empty
            self.name = name
            self.outfits = outfits #Outfits is now used to hold full outfits.
            self.underwear_sets = underwear_sets #Limited to layer 1 clothing items.
            self.overwear_sets = overwear_sets #Limited to layer 2 and 3 clothing items.
            if outfits is None:
                self.outfits = []
            if underwear_sets is None:
                self.underwear_sets = []
            if overwear_sets is None:
                self.overwear_sets = []

        def __copy__(self):
            #TODO: see if adding a .copy() here has A) Fixed any potential bugs and B) not had a major performance impact.
            outfit_copy_list = []
            for outfit in self.outfits:
                outfit_copy_list.append(outfit.get_copy())

            under_copy_list = []
            for underwear in self.underwear_sets:
                under_copy_list.append(underwear.get_copy())

            over_copy_list = []
            for overwear in self.overwear_sets:
                over_copy_list.append(overwear.get_copy())

            return Wardrobe(self.name,outfit_copy_list,under_copy_list,over_copy_list)

        def merge_wardrobes(self, other_wardrobe): #Returns a copy of this wardrobe merged with the other one.
            base_wardrobe = self.__copy__() #This already redefines it's copy meth, so we should be fine.
            for outfit in other_wardrobe.outfits:
                base_wardrobe.add_outfit(outfit.get_copy())

            for underwear in other_wardrobe.underwear_sets:
                base_wardrobe.add_underwear_set(underwear.get_copy())

            for overwear in other_wardrobe.overwear_sets:
                base_wardrobe.add_overwear_set(overwear.get_copy())

            base_wardrobe.name = base_wardrobe.name + " + " + other_wardrobe.name
            return base_wardrobe

        def get_random_selection(self, chance_to_pick): #Returns a wardrobe made of a random assortment of clothing from this one.
            base_wardrobe = Wardrobe(self.name)
            for outfit in self.outfits:
                is_picked = renpy.random.randint(0,100)
                if is_picked < chance_to_pick:
                    base_wardrobe.add_outfit(outfit.get_copy())

            for underwear in self.underwear_sets:
                is_picked = renpy.random.randint(0,100)
                if is_picked < chance_to_pick:
                    base_wardrobe.add_underwear_set(underwear.get_copy())

            for overwear in self.overwear_sets:
                is_picked = renpy.random.randint(0,100)
                if is_picked < chance_to_pick:
                    base_wardrobe.add_overwear_set(overwear.get_copy())

            return base_wardrobe

        def add_outfit(self, new_outfit):
            self.outfits.append(new_outfit)

        def add_underwear_set(self, the_outfit):
            self.underwear_sets.append(the_outfit)

        def add_overwear_set(self, the_outfit):
            self.overwear_sets.append(the_outfit)

        def remove_outfit(self, old_outfit):
            if old_outfit in self.outfits:
                self.outfits.remove(old_outfit)
            elif old_outfit in self.underwear_sets:
                self.underwear_sets.remove(old_outfit)
            elif old_outfit in self.overwear_sets:
                self.overwear_sets.remove(old_outfit)

        def pick_random_outfit(self):
            return get_random_from_list(self.outfits).get_copy() # Get a copy of _any_ full outfit in this character's wardrobe.

        def get_random_appropriate_underwear(self, sluttiness_limit, sluttiness_min = 0): #Get an underwear outfit that is considered appropriate (based on underwear sluttiness, not full outfit sluttiness)
            valid_underwear = []
            for underwear in self.underwear_sets:
                if underwear.get_underwear_slut_score() <= sluttiness_limit and underwear.get_underwear_slut_score() >= sluttiness_min:
                    valid_underwear.append(underwear)

            if valid_underwear:
                return get_random_from_list(valid_underwear).get_copy()
            else:
                return None

        def get_random_appropriate_outfit(self, sluttiness_limit, sluttiness_min = 0): # Get a copy of a full outfit that the character is at or below the sluttiness limit.
            valid_outfits = []
            for outfit in self.outfits:
                if outfit.slut_requirement >= sluttiness_min and outfit.slut_requirement <= sluttiness_limit:
                    valid_outfits.append(outfit)

            the_underwear = get_random_from_list(valid_outfits)
            if the_underwear:
                return the_underwear.get_copy()
            else:
                return None

        def build_appropriate_outfit(self, sluttiness_limit, sluttiness_min = 0): # Let's assume characters have a limited number of overwear sets but a larger set of underwear. Get an overwear set, then a decent underwear set.
            valid_overwear = []
            for overwear in self.overwear_sets:
                if overwear.get_overwear_slut_score() >= sluttiness_min and overwear.get_overwear_slut_score() <= sluttiness_limit:
                    valid_overwear.append(overwear)

            if len(valid_overwear) == 0:
                return default_outfit.get_copy() #If we don't have any overwear stuff we should return the default outfit to prevent a crash.

            picked_overwear = get_random_from_list(valid_overwear) #We use a reference here, we will take a full copy of the underwear and build the outfit up based on that.
            remaining_sluttiness_limit = sluttiness_limit - picked_overwear.get_overwear_slut_score()
            remaining_sluttiness_min = sluttiness_min - picked_overwear.get_overwear_slut_score()

            picked_underwear = self.get_random_appropriate_underwear(remaining_sluttiness_limit, remaining_sluttiness_min)
            # valid_underwear = []
            # for underwear in self.underwear_sets:
            #     if underwear.get_underwear_slut_score() >= remaining_sluttiness_min and underwear.get_underwear_slut_score() <= remaining_sluttiness_limit:
            #         valid_underwear.append(underwear)

            #picked_underwear = get_random_from_list(valid_underwear)

            if picked_underwear is None:
                return default_outfit.get_copy() #If we weren't able to find any underwear we can't make an outfit with our selection. Return the default outfit to make sure we don't crash.

            for upper in picked_overwear.upper_body:
                picked_underwear.upper_body.append(upper.get_copy())

            for lower in picked_overwear.lower_body:
                picked_underwear.lower_body.append(lower.get_copy())

            for feet_wear in picked_overwear.feet:
                picked_underwear.feet.append(feet_wear.get_copy())

            for acc in picked_overwear.accessories:
                picked_underwear.accessories.append(acc.get_copy())

            picked_underwear.update_slut_requirement()
            if picked_underwear.slut_requirement < remaining_sluttiness_min or picked_underwear.slut_requirement > sluttiness_limit: #BUG: we sometimes have no valid outfits and hit our recursion limit.
                return self.build_appropriate_outfit(sluttiness_limit+1, sluttiness_min) #If for some reason our outfit violates our limits retry but with a slightly more slutty tolerance. Better to fail in favour of sluttiness then not have an outfit.

            else:
                picked_underwear.name = picked_underwear.name + " + " + picked_overwear.name #The outfit name is the hybrid of the two sets we made it out of.

            return picked_underwear


        def decide_on_outfit(self, sluttiness_limit, sluttiness_min = 0): #Has a chance to draw from full random sets if they are present or to create a completely new outfit by combinding sets.

            outfit_choice = renpy.random.randint(0,100)
            chance_to_use_full = 50 #For now we will make 50% of outfit choices use full outfits if possible.
            if outfit_choice < chance_to_use_full:
                valid_full_outfits = []
                for full_outfit in self.outfits:
                    if full_outfit.slut_requirement >= sluttiness_min and full_outfit.slut_requirement <= sluttiness_limit:
                        valid_full_outfits.append(full_outfit)

                if valid_full_outfits:
                    return get_random_from_list(valid_full_outfits).get_copy()
                else:
                    return self.build_appropriate_outfit(sluttiness_limit, sluttiness_min)
            else:
                return self.build_appropriate_outfit(sluttiness_limit, sluttiness_min)

        def decide_on_uniform(self, the_person): # Creates a uniform out of the clothing items from this wardrobe. Unlike a picked outfit sluttiness has no factor here. A girls personal underwear sets will be used for constructed uniforms.
            if len(self.outfits) > 0:
                #We have some full body outfits we mgiht use. 50/50 to use that or a constructed outfit.
                outfit_choice = renpy.random.randint(0,100)
                chance_to_use_full = 50 #Like normal outfits a uniform hasa 50/50 chance of being a full outfit or aa assembled outfit if both are possible.

                if outfit_choice < chance_to_use_full and len(self.underwear_sets + self.overwear_sets) > 0: #If we roll an assmelbed outfit and we have some parts to make it out of do that.
                    pass

                else: #Otherwise use one of the full outfits.
                    return get_random_from_list(self.outfits).get_copy()

            else:
                if len(self.underwear_sets + self.overwear_sets) == 0:
                    #We have nothing else to make a uniform out of. Return None and let the pick uniform function handle that.
                    return None

                else:
                    pass
                    #We have something to make an outfit out of. Go with that.

            #If we get to here we are assembling an outfit out of underwear or overwear.
            uniform_over = get_random_from_list(self.overwear_sets)
            if uniform_over:
                #We got a top, now get a bottom.
                uniform_under = get_random_from_list(self.underwear_sets)
                if not uniform_under:
                    #We need to get a bottom from her personal wardrobe. We also want to make sure it's something she would personally wear.
                    slut_limit_remaining = the_person.sluttiness - uniform_over.get_overwear_slut_score()
                    if slut_limit_remaining < 0:
                        slut_limit_remaining = 0 #If the outfit is so slutty we're not comfortable in it we'll try and wear the most conservative underwear we can.

                    possible_unders = []
                    for under in the_person.wardrobe.underwear_sets:
                        if under.get_underwear_slut_score() <= slut_limit_remaining:
                            possible_unders.append(under)

                    uniform_under = get_random_from_list(possible_unders)


            else:
                #There are no tops, so we're going to try and get a bottom and use one of the persons tops.
                uniform_under = get_random_from_list(self.underwear_sets) # We know we will always get something here, otherwise we would have returned None a while ago.
                slut_limit_remaining = the_person.sluttiness - uniform_under.get_underwear_slut_score()
                if slut_limit_remaining < 0:
                    slut_limit_remaining = 0 #If the outfit is so slutty we're not comfortable in it we'll try and wear the most conservative underwear we can.

                possible_overs = []
                for over in the_person.wardrobe.overwear_sets:
                    if over.get_overwear_slut_score() <= slut_limit_remaining:
                        possible_overs.append(over)

                uniform_over = get_random_from_list(possible_overs)

            #At this point we have our under and over, if at all possible.
            if not uniform_over or not uniform_under:
                return None #Something's gone wrong and we don't have one of our sets. return None and let the uniform gods sort it out.

            assembled_uniform = uniform_under.get_copy()
            assembled_uniform.name = uniform_under.name + " + " + uniform_over.name
            for upper in uniform_over.upper_body:
                assembled_uniform.upper_body.append(upper.get_copy())

            for lower in uniform_over.lower_body:
                assembled_uniform.lower_body.append(lower.get_copy())

            for feet_wear in uniform_over.feet:
                assembled_uniform.feet.append(feet_wear.get_copy())

            for acc in uniform_over.accessories:
                assembled_uniform.accessories.append(acc.get_copy())

            assembled_uniform.update_slut_requirement()
            return assembled_uniform


        def get_count(self):
            return len(self.outfits + self.underwear_sets + self.overwear_sets)

        def get_outfit_list(self):
            return self.outfits

        def get_underwear_sets_list(self):
            return self.underwear_sets

        def get_overwear_sets_list(self):
            return self.overwear_sets

        def has_outfit_with_name(self, the_name):
            has_name = False
            for checked_outfit in self.outfits + self.underwear_sets + self.overwear_sets:
                if checked_outfit.name == the_name:
                    has_name = True
            return has_name

        def get_outfit_with_name(self, the_name):
            for outfit in self.outfits + self.underwear_sets + self.overwear_sets:
                if outfit.name == the_name:
                    return outfit.get_copy()
            return None

    def make_wall(): #Helper functions for creating instances of commonly used objects.
        the_wall = Object("wall",["Lean"], sluttiness_modifier = 0, obedience_modifier = 5)
        return the_wall

    def make_window():
        the_window = Object("window",["Lean"], sluttiness_modifier = -5, obedience_modifier = 5)
        return the_window

    def make_chair():
        the_chair = Object("chair",["Sit","Low"], sluttiness_modifier = 0, obedience_modifier = 0)
        return the_chair

    def make_desk():
        the_desk = Object("desk",["Sit","Lay","Low"], sluttiness_modifier = 0, obedience_modifier = 0)
        return the_desk

    def make_table():
        the_table = Object("table",["Sit","Lay","Low"], sluttiness_modifier = 0, obedience_modifier = 0)
        return the_table

    def make_bed():
        the_bed = Object("bed",["Sit","Lay","Low"], sluttiness_modifier = 10, obedience_modifier = 10)
        return the_bed

    def make_couch():
        the_couch = Object("couch",["Sit","Lay","Low"], sluttiness_modifier = 5, obedience_modifier = -5)
        return the_couch

    def make_floor():
        the_floor = Object("floor",["Lay","Kneel"], sluttiness_modifier = -10, obedience_modifier = -10)
        return the_floor

    def make_grass():
        the_grass = Object("grass",["Lay","Kneel"], sluttiness_modifier = -5, obedience_modifier = -10)
        return the_grass



    class Position(renpy.store.object):
        def __init__(self,name,slut_requirement,slut_cap,position_tag,requires_location,requires_clothing,skill_tag,girl_arousal,guy_arousal,connections,intro,scenes,outro,transition_default,
        strip_description, strip_ask_description, orgasm_description,
        verb = "fuck" , opinion_tags = None):
            self.name = name
            self.slut_requirement = slut_requirement #The required slut score of the girl. Obedience will help fill the gap if possible, at a happiness penalty. Value from 0 (almost always possible) to ~100
            self.slut_cap = slut_cap #The maximum sluttiness that this position will have an effect on.
            self.position_tag = position_tag # The tag used to get the correct position image set
            self.requires_location = requires_location #
            self.requires_clothing = requires_clothing
            self.skill_tag = skill_tag #The skill that will provide a bonus to this position.
            self.opinion_tags = opinion_tags #The opinion that will be checked each round.
            self.girl_arousal = girl_arousal # The base arousal the girl recieves from this position.
            self.guy_arousal = guy_arousal # The base arousal the guy recieves from this position.
            self.connections = connections
            self.intro = intro
            self.scenes = scenes
            self.outro = outro
            self.transition_default = transition_default #TODO: add transitions that go between related positions but with different objects. Things like standing sex into fucking her against a window.
            self.transitions = []
            self.strip_description = strip_description
            self.strip_ask_description = strip_ask_description
            self.orgasm_description = orgasm_description
            self.verb = verb #A verb used to describe the position. "Fuck" is default, and mostly used for sex positions or blowjobs etc. Kiss, Fool around, etc. are also possibilities.

            self.current_modifier = None #We will update this if the posisiion has a special modifier that shoudl be applied, like blowjob.

        def link_positions(self,other,transition_label): #This is a one way link!
            self.connections.append(other)
            self.transitions.append([other,transition_label])

        def link_positions_two_way(self,other,transition_label_1,transition_label_2): #Link it both ways. Great for adding a modded position without modifying other positions.
            self.link_positions(other,transition_label_1)
            other.link_positions(self,transition_label_2)

        def call_intro(self, the_person, the_location, the_object, round):
            renpy.call(self.intro,the_person, the_location, the_object, round)

        def call_scene(self, the_person, the_location, the_object, round):
            random_scene = renpy.random.randint(0,len(self.scenes)-1)
            renpy.call(self.scenes[random_scene],the_person, the_location, the_object, round)

        def call_outro(self, the_person, the_location, the_object, round):
            renpy.call(self.outro,the_person, the_location, the_object, round)

        def call_transition(self,the_position, the_person, the_location, the_object, round):
            transition_scene = the_position.transition_default
            for position_tuple in self.transitions:
                if position_tuple[0] == the_position: ##Does the position match the one we are looking for?
                    transition_scene = position_tuple[1] ##If so, set it's label as the one we are going to change to.
            renpy.call(transition_scene, the_person, the_location, the_object, round)

        def call_strip(self, the_clothing, the_person, the_location, the_object, round):
            renpy.call(self.strip_description, the_clothing, the_person, the_location, the_object, round)

        def call_strip_ask(self, the_clothing, the_person, the_location, the_object, round):
            renpy.call(self.strip_ask_description, the_clothing, the_person, the_location, the_object, round)

        def call_orgasm(self, the_person, the_location, the_object, round):
            renpy.call(self.orgasm_description, the_person, the_location, the_object, round)

        def check_clothing(self, the_person):
            if self.requires_clothing == "Vagina":
                return the_person.outfit.vagina_available()
            elif self.requires_clothing == "Tits":
                return the_person.outfit.tits_available()
            else:
                return True ##If you don't have one of the requirements listed above just let it happen.

        def redraw_scene(self, the_person, emotion = None): #redraws the scene, call this when something is modified.
            the_person.draw_person(self.position_tag, emotion = emotion, special_modifier = self.current_modifier)

        def build_position_willingness_string(self, the_person): #Generates a string for this position that includes a tooltip and coloured willingness for the person given.
            willingness_string = ""
            tooltip_string = ""
            if the_person.sluttiness >= self.slut_cap:
                if the_person.arousal >= self.slut_cap:
                    willingness_string = "{color=#6b6b6b}Boring{/color}" #No sluttiness gain AND half arousal gain
                    tooltip_string = " (tooltip)This position is too boring to interest her when she is this horny. No sluttiness increase and her arousal gain is halved."
                else:
                    willingness_string = "{color=#3C3CFF}Comfortable{/color}" #No sluttiness
                    tooltip_string = " (tooltip)This position is too tame for her tastes. No sluttiness increase, but it may still be a good way to get warmed up and ready for other positions."
            elif the_person.sluttiness >= self.slut_requirement:
                willingness_string = "{color=#3DFF3D}Exciting{/color}" #Normal sluttiness gain
                tooltip_string = " (tooltip)This position pushes the boundry of what she is comfortable with. Increases temporary sluttiness, which may become permanent over time or with serum application."
            elif the_person.sluttiness + the_person.obedience-100 >= self.slut_requirement:
                willingness_string = "{color=#FFFF3D}Willing if Commanded{/color}"
                tooltip_string = " (tooltip)This position is beyond what she would normally consider. She is obedient enough to do it if she is commanded, at the cost of some happiness."
            else:
                willingness_string = "{color=#FF3D3D}Too Slutty{/color}"
                tooltip_string = " (tooltip)This position is so far beyond what she considers appropriate that she would never dream of it."

            if self.check_clothing(the_person):
                return self.name + "\n{size=22}" + willingness_string + "{/size}" + tooltip_string
            else:
                return self.name + "\n{size=22}"+ willingness_string + "\nObstructed by Clothing{/size} (disabled)"


    ##Initialization of requirement functions go down here. Can also be moved to init -1 eventually##

    def sleep_action_requirement():
        if time_of_day != 4:
            return "Too early to sleep."
        else:
            return True

    def faq_action_requirement():
        return True

    def hr_work_action_requirement():
        if time_of_day >= 4:
            return "Too late to work."
        else:
            return True

    def research_work_action_requirement():
        if time_of_day >= 4:
            return "Too late to work."
        elif mc.business.active_research_design == None:
            return "No research project set."
        else:
            return True

    def supplies_work_action_requirement():
        if time_of_day >= 4:
            return "Too late to work."
        else:
            return True

    def market_work_action_requirement():
        if time_of_day >= 4:
            return "Too late to work."
        else:
            return True

    def production_work_action_requirement():
        if time_of_day >= 4:
            return "Too late to work."
        elif len(mc.business.serum_production_array) == 0:
            return "No serum design set."
        else:
            return True

    def interview_action_requirement():
        if time_of_day >= 4:
            return "Too late to work."
        elif mc.business.get_employee_count() >= mc.business.max_employee_count:
            return "At employee limit."
        else:
            return True

    def serum_design_action_requirement():
        if time_of_day >= 4:
            return "Too late to work."
        else:
            return True

    def research_select_action_requirement():
        return True

    def production_select_action_requirement():
        return True

    def trade_serum_action_requirement():
        return True

    def sell_serum_action_requirement():
        return True

    def pick_supply_goal_action_requirement():
        return True

    def policy_purchase_requirement():
        return True

    def head_researcher_select_requirement():
        if  mc.business.head_researcher is not None:
            return False
        else:
            return True

    def set_uniform_requirement():
        return strict_uniform_policy.is_owned()

    def set_serum_requirement():
        return daily_serum_dosage_policy.is_owned()

    def review_designs_action_requirement():
        return True
    ##Creator Defined Displayables, used in custom menues throughout the game##

    class Vren_Line(renpy.Displayable): # Caused large amounts of lag when used! No longer in use.
        def __init__(self, start, end, thickness, color, **kwargs):
            super(Vren_Line,self).__init__(**kwargs)
            ##Base attributes
            self.start = start ## tuple of x,y coords
            self.end = end ## tuple of x,y coords
            self.thickness = thickness
            self.color = color

            ##Store normal values for drawing anti-aliased lines
            self.normal_temp = [self.end[0]-self.start[0],self.end[1]-self.start[1]]
            self.normal = [0,0]
            self.normal[0] = -self.normal_temp[1]
            self.normal[1] = self.normal_temp[0]
            self.mag = math.sqrt(math.pow(self.normal[0],2) + math.pow(self.normal[1],2))
            self.normal = [(self.normal[0]*self.thickness)/self.mag,(self.normal[1]*self.thickness)/self.mag]

            ##Store point list so we don't have to calculate it each time
            self.start_right = [self.start[0]+self.normal[0],self.start[1]+self.normal[1]]
            self.start_left = [self.start[0]-self.normal[0],self.start[1]-self.normal[1]]
            self.end_left = [self.end[0]+self.normal[0],self.end[1]+self.normal[1]]
            self.end_right = [self.end[0]-self.normal[0],self.end[1]-self.normal[1]]

            self.point_list = [self.start_left,self.start_right,self.end_left,self.end_right]

        def render(self, the_width, the_height, st, at):

            render = renpy.Render(the_width,the_height)
            canvas = render.canvas()

            canvas.polygon(self.color,self.point_list) ##Draw the polygon. It will have jagged edges so we...
            canvas.aalines(self.color,False,self.point_list) ##Also draw a set of antialiased lines around the edge so it doesn't look jagged any more.
            return render

        def __eq__(self,other): ## Used to see if two Vren_Line objects are equivelent and thus don't need to be redrawn each time any of the variables is changed.
            if not type(other) is Vren_Line:
                return False

            if not (self.start == other.start and self.end == other.end and self.thickness == other.thickness and self.color == other.color): ##ie not the same
                return False
            else:
                return True

        def per_interact(self):
            renpy.redraw(self,0)

init -1:
    python:
        list_of_positions = [] # These are sex positions that the PC can make happen while having sex.
        list_of_girl_positions = [] # These are sex positiosn that the girl can make happen while having sex.

        day_names = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"] #Arrays that hold the names of the days of the week and times of day. Arrays start at 0.
        time_names = ["Early Morning","Morning","Afternoon","Evening","Night"]

transform scale_person(scale_factor = 1):
    zoom scale_factor

transform character_right():
    yalign 1.0
    yanchor 1.0
    xalign 1.0
    xanchor 1.0

transform clothing_fade():
    linear 0.5 alpha 0.0

transform breathe_animation():
    subpixel True
    ease 3.0 yzoom 0.995
    ease 3.0 yzoom 1.0
    repeat

init -2 style textbutton_style: ##The generic style used for text button backgrounds. TODO: Replace this with a pretty background image instead of a flat colour.
    padding [5,5]
    margin [5,5]
    background "#000080"
    insensitive_background "#222222"
    hover_background "#aaaaaa"

init -2 style textbutton_text_style: ##The generic style used for the text within buttons
    size 20
    italic True
    bold True
    color "#dddddd"
    outlines [(2,"#222222",0,0)]
    text_align 0.5

init -2 style menu_text_style:
    size 18
    italic True
    bold True
    color "#dddddd"
    outlines [(2,"#222222",0,0)]
    text_align 0.5

init -2 style outfit_style: ##The text style used for text inside of the outfit manager.
    size 16
    italic True
    color "#dddddd"
    outlines [(1,"#666666",0,0)]
    insensitive_color "#222222"
    hover_color "#ffffff"

init -2:
    default name = "Input Your First Name"
    default l_name = "Input Your Last Name"
    default b_name = "Input Your Business Name"

    python:
        def name_func(new_name):
            store.name = new_name

        def b_name_func(new_name):
            store.b_name = new_name

        def l_name_func(new_name):
            store.l_name = new_name

screen character_create_screen():

    default cha = 0
    default int = 0
    default foc = 0

    default h_skill = 0
    default m_skill = 0
    default r_skill = 0
    default p_skill = 0
    default s_skill = 0

    default F_skill = 0
    default O_skill = 0
    default V_skill = 0
    default A_skill = 0


    default name_select = 0

    default character_points = 20
    default stat_max = 4
    default work_skill_max = 4
    default sex_skill_max = 4

    imagebutton auto "/gui/Text_Entry_Bar_%s.png" action [SetScreenVariable("name_select",1),  SetVariable("name","")] pos (320,800) xanchor 0.5 yanchor 0.5
    imagebutton auto "/gui/Text_Entry_Bar_%s.png" action [SetScreenVariable("name_select",3),SetVariable("l_name","")]  pos (320,880) xanchor 0.5 yanchor 0.5
    imagebutton auto "/gui/Text_Entry_Bar_%s.png" action [SetScreenVariable("name_select",2),SetVariable("b_name","")]  pos (320,960) xanchor 0.5 yanchor 0.5
    imagebutton auto "/gui/button/choice_%s_background.png" action Return([[cha,int,foc],[h_skill,m_skill,r_skill,p_skill,s_skill],[F_skill,O_skill,V_skill,A_skill]]) pos (1560,900) xanchor 0.5 yanchor 0.5 sensitive character_points == 0


    if name_select == 1: #Name
        input default name pos(320,800) changed name_func xanchor 0.5 yanchor 0.5 style "menu_text_style" length 25
    else:
        text name  pos(320,800) xanchor 0.5 yanchor 0.5 style "menu_text_style"

    if name_select == 3: #Last Name
        input default l_name  pos(320,880) changed l_name_func xanchor 0.5 yanchor 0.5 style "menu_text_style" length 25
    else:
        text l_name pos(320,880) xanchor 0.5 yanchor 0.5 style "menu_text_style"

    if name_select == 2: #Business Name
        input default b_name pos(320,960) changed b_name_func xanchor 0.5 yanchor 0.5 style "menu_text_style" length 25
    else:
        text b_name pos(320,960) xanchor 0.5 yanchor 0.5 style "menu_text_style"




    if character_points > 0:
        text "Spend All Character Points to Proceed" style "menu_text_style" anchor(0.5,0.5) pos(1560,900)
    else:
        text "Finish Character Creation" style "menu_text_style" anchor(0.5,0.5) pos(1560,900)

    text "Character Points Remaining: [character_points]" style "menu_text_style" xalign 0.5 yalign 0.1 size 30
    hbox: #Main Stats Section
        yalign 0.7
        xalign 0.5
        xanchor 0.5
        frame:
            background "#1a45a1aa"
            vbox:
                xsize 550
                text "Main Stats (3 points/level)" style "menu_text_style" size 25
                null height 40
                hbox:
                    text "Charisma: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("cha",cha-1), SetScreenVariable("character_points", character_points+3)] sensitive cha>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(cha) + "/[stat_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("cha",cha+1), SetScreenVariable("character_points", character_points-3)] sensitive character_points>2 and cha<stat_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your visual appearance and force of personality. Charisma is the key attribute for selling serums and managing your business." style "menu_text_style"
                null height 30
                hbox:
                    text "Intelligence: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("int",int-1), SetScreenVariable("character_points", character_points+3)] sensitive int>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(int) + "/[stat_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("int",int+1), SetScreenVariable("character_points", character_points-3)] sensitive character_points>2 and int<stat_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your raw knowledge and ability to think quickly. Intelligence is the key attribute for research and development of serums." style "menu_text_style"
                null height 30
                hbox:
                    text "Focus: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("foc",foc-1), SetScreenVariable("character_points", character_points+3)] sensitive foc>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(foc) + "/[stat_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("foc",foc+1), SetScreenVariable("character_points", character_points-3)] sensitive character_points>2 and foc<stat_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your mental endurance and precision. Focus is the key attribute for production and supply procurement." style "menu_text_style"

        null width 40
        frame:
            background "#1a45a1aa"
            vbox:
                xsize 550
                text "Work Skills (1 point/level)" style "menu_text_style" size 25
                null height 40
                hbox:
                    text "Human Resources: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("h_skill",h_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive h_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(h_skill)+"/[work_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("h_skill",h_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and h_skill<work_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at human resources. Crutial for maintaining an efficent business." style "menu_text_style"
                null height 30
                hbox:
                    text "Marketing: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("m_skill",m_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive m_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(m_skill)+"/[work_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("m_skill",m_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and m_skill<work_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at marketing. Higher skill will allow you to ship more doses of serum per day." style "menu_text_style"
                null height 30
                hbox:
                    text "Research and Development: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("r_skill",r_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive r_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(r_skill)+"/[work_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("r_skill",r_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and r_skill<work_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at researching new serum traits and designs. Critical for improving your serum inventory." style "menu_text_style"
                null height 30
                hbox:
                    text "Production: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("p_skill",p_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive p_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(p_skill)+"/[work_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("p_skill",p_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and p_skill<work_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at producing serum in the production lab. Produced serums can then be sold for profit or kept for personal use." style "menu_text_style"
                null height 30
                hbox:
                    text "Supply Procurement: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("s_skill",s_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive s_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(s_skill)+"/[work_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("s_skill",s_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and s_skill<work_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at obtaining raw supplies for your production division. Without supply, nothing can be created in the lab." style "menu_text_style"
                null height 30
        null width 40
        frame:
            background "#1a45a1aa"
            vbox:
                xsize 550
                text "Sex Skills (1 point/level)" style "menu_text_style" size 25
                null height 40
                hbox:
                    text "Foreplay: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("F_skill",F_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive F_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(F_skill)+"/[sex_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("F_skill",F_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and F_skill<sex_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at foreplay, including fingering, kissing, and groping." style "menu_text_style"
                null height 30
                hbox:
                    text "Oral: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("O_skill",O_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive O_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(O_skill)+"/[sex_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("O_skill",O_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and O_skill<sex_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at giving oral to women, as well as being a pleasant recipiant." style "menu_text_style"
                null height 30
                hbox:
                    text "Vaginal: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("V_skill",V_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive V_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(V_skill)+"/[sex_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("V_skill",V_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and V_skill<sex_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at vaginal sex in any position." style "menu_text_style"
                null height 30
                hbox:
                    text "Anal: " style "menu_text_style"
                    textbutton "<" action [SetScreenVariable("A_skill",A_skill-1), SetScreenVariable("character_points", character_points+1)] sensitive A_skill>0 style "textbutton_style" text_style "textbutton_text_style"
                    text str(A_skill)+"/[sex_skill_max]" style "textbutton_text_style"
                    textbutton ">" action [SetScreenVariable("A_skill",A_skill+1), SetScreenVariable("character_points", character_points-1)] sensitive character_points>0 and A_skill<sex_skill_max style "textbutton_style" text_style "textbutton_text_style"
                text "     Your skill at anal sex in any position. (NOTE: No content included in this version)." style "menu_text_style"
                null height 30

screen main_ui(): #The UI that shows most of the important information to the screen.
    frame:
        background "Info_Frame_1.png"
        xsize 600
        ysize 400
        yalign 0.0
        vbox:
            spacing -5
            text day_names[day%7] + " - " + time_names[time_of_day] + " (day [day])" style "menu_text_style" size 18
            textbutton "Outfit Manager" action Call("outfit_master_manager",from_current=True) style "textbutton_style" text_style "textbutton_text_style" xsize 220 tooltip "Design outfits to set as uniforms or give to suggest to women."
            textbutton "Check Inventory" action ui.callsinnewcontext("check_inventory_loop") style "textbutton_style" text_style "textbutton_text_style" xsize 220 tooltip "Check what serums you are currently carrying."
            if mc.stat_goal.completed or mc.work_goal.completed or mc.sex_goal.completed:
                textbutton "Character Sheet" action Show("mc_character_sheet") style "textbutton_style" text_style "textbutton_text_style" xsize 220 background "#44BB44" insensitive_background "#222222" hover_background "#aaaaaa" tooltip "Check your stats, skills, and goals."
            else:
                textbutton "Character Sheet" action Show("mc_character_sheet") style "textbutton_style" text_style "textbutton_text_style" xsize 220 tooltip "Check your stats, skills, and goals."

            # Removed as of v0.19.0, replaced by generic "wait here" button in general purpose menuself.
            # if time_of_day == 4: #TODO: check what time is night time
            #     textbutton "Go to Sleep" action [Function(mc.change_location,bedroom), Call("advance_time",from_current=True)] style "textbutton_style" text_style "textbutton_text_style" xsize 220 sensitive mc.can_skip_time tooltip "Go home and go to sleep." #NOTE: may cause problems if we add more things into the sleep section of the game.
            # else:
            #     textbutton "Wait Here" action Call("advance_time",from_current=True) style "textbutton_style" text_style "textbutton_text_style" xsize 220 sensitive mc.can_skip_time tooltip "Spend some time doing nothing in particular."

            textbutton "Arousal: [mc.arousal]%":
                ysize 28
                text_style "menu_text_style"
                tooltip "Your personal arousal. When it reaches 100% or more you're forced to climax, ending your current sexual encounter."
                action NullAction()
                sensitive True

            textbutton "Stamina: [mc.current_stamina]/[mc.max_stamina]":
                ysize 28
                text_style "menu_text_style"
                tooltip "Seducing women and having sex requires stamina. Your stamina will recover to its max value at the start of each day."
                action NullAction()
                sensitive True


screen tooltip_screen():
    zorder 50
    default hovered_enough_time = False
    $ tooltip = GetTooltip()
    if tooltip and len(tooltip) > 0:
        timer 0.7 action SetScreenVariable("hovered_enough_time",True)
        if hovered_enough_time:
            $ mouse_xy = renpy.get_mouse_pos()
            frame:
                if mouse_xy[1] > 1080/2:
                    background "#888888DD" xsize 450 xpos mouse_xy[0] ypos mouse_xy[1] yanchor 1.0
                else:
                    background "#888888DD" xsize 450 xpos mouse_xy[0] ypos mouse_xy[1]
                text "[tooltip]" style "menu_text_style"
    else:
        timer 0.1 action SetScreenVariable("hovered_enough_time",False)


screen goal_hud_ui():
    frame:
        background "Goal_Frame_1.png"
        yalign 0.5
        xsize 260
        ysize 250
        vbox:
            textbutton "Goal Information" action Show("mc_character_sheet") style "textbutton_style" text_style "textbutton_text_style" xsize 245 text_align 0.5 tooltip "Complete goals to earn experience, and spend experience to improve your stats and skills."
            for goal in [mc.stat_goal,mc.work_goal,mc.sex_goal]:
                if goal:
                    frame:
                        ysize 60
                        background None
                        bar value goal.get_progress_fraction() range 1 xalign 0.5
                        textbutton goal.name + "\n" + goal.get_reported_progress() text_style "menu_text_style" xalign 0.5 yanchor 0.5 yalign 0.5 text_size 16 text_text_align 0.5 action NullAction() sensitive True tooltip goal.description

transform phone_slide(start_yalign, goal_yalign, duration = 0.4):
    yalign start_yalign
    linear duration yalign goal_yalign

transform background_fade(max_time, time_used):
    alpha (max_time-time_used)/max_time
    linear max_time - time_used alpha 0

screen phone_hud_ui():
    default phone_up = False
    default start_phone_pos = 1.4
    default end_phone_pos = 1.4
    default start = True
    frame:
        background "#1a45a1aa"
        xsize 340
        ysize 400
        xanchor 1.0
        xalign 0.99
        at phone_slide(start_phone_pos, end_phone_pos)
        vbox:
            spacing 0
            if phone_up:
                textbutton "" style "textbutton_style":
                    text_style "textbutton_text_style" xsize 320 ysize 20 action [SetScreenVariable("phone_up",False), SetScreenVariable("end_phone_pos",1.4), SetScreenVariable("start_phone_pos",1.0)]
            else:
                textbutton "" style "textbutton_style":
                    text_style "textbutton_text_style" xsize 320 ysize 20 action [SetScreenVariable("phone_up",True), SetScreenVariable("end_phone_pos",1.0), SetScreenVariable("start_phone_pos",1.4)]

            null height 5

            for log_item in mc.log_items:
                $ fade_time = 5
                $ time_diff = time.time() - log_item[2]
                if time_diff > fade_time:
                    $ time_diff = fade_time
                    # background None
                    # xsize 320
                    # yfill False
                frame:
                    background "#33333388"
                    xsize 320
                    padding (0,0)
                    text log_item[0] style log_item[1] size 18 xsize 320 first_indent 20
                frame:
                    background "#ff0000aa"
                    xsize 320
                    ysize 8
                    yanchor 1.0
                    yalign 0.95
                    xpadding 0
                    ypadding 0
                    at background_fade(5, time_diff)
                null height 4
                    # frame:
                    #     background "#ff0000"
                    #     xsize 320
                    #     ymaximum 10
                    #     yanchor 1.0
                    #     yalign 0.9
                    #     xpadding 0
                    #     ypadding 0
                    #
                    #     text log_item[0] style log_item[1] size 18 xsize 320 first_indent 20 color "#ffffff00" #This is a dummy to make sure the spacing of our frames is correct!
                    # frame:






screen business_ui(): #Shows some information about your business.
    frame:
        background im.Flip("Info_Frame_1.png",vertical=True)
        xsize 600
        ysize 400
        yalign 1.0
        vbox:
            yanchor 1.0
            yalign 1.0
            spacing 5
            text "[mc.business.name]" style "menu_text_style" size 18 xalign 0.2
            textbutton "Employee Count: " + str(mc.business.get_employee_count()) + "/" + str(mc.business.max_employee_count):
                ysize 28
                text_style "menu_text_style"
                tooltip "Your current and maximum number of employees. Purchase new business policies from your main office to increase the number of employees you can have."
                action NullAction()
                sensitive True
            # text "Employee Count: " + str(mc.business.get_employee_count()) + "/" + str(mc.business.max_employee_count) style "menu_text_style"
            if mc.business.funds < 0:
                textbutton "Company Funds: $[mc.business.funds]":
                    ysize 28
                    text_style "menu_text_style"
                    text_color "#DD0000"
                    tooltip "The amount of money in your business account. If you are in the negatives for more than three days your loan defaults and the game is over!"
                    action NullAction()
                    sensitive True
            else:
                textbutton "Company Funds: $[mc.business.funds]":
                    ysize 28
                    text_style "menu_text_style"
                    tooltip "The amount of money in your business account. If you are in the negatives for more than three days your loan defaults and the game is over!"
                    action NullAction()
                    sensitive True

            textbutton "Daily Salary Cost: $"+ str(mc.business.calculate_salary_cost()):
                ysize 28
                text_style "menu_text_style"
                tooltip "The amount of money spent daily to pay your employees. Employees are not paid on weekends."
                action NullAction()
                sensitive True
            #text "Daily Salary Cost: $"+ str(mc.business.calculate_salary_cost()) style "menu_text_style"
            textbutton "Company Efficency: [mc.business.team_effectiveness]%":
                ysize 28
                text_style "menu_text_style"
                tooltip "The more employees you have the faster your company will become inefficent. Perform HR work at your office or hire someone to do it for you to raise your company efficency. All productivity is modified by company efficency."
                action NullAction()
                sensitive True
            #text "Company Efficency: [mc.business.team_effectiveness]%" style "menu_text_style"
#            text "Company Marketability: [mc.business.marketability]" style "menu_text_style"

            textbutton "Current Raw Supplys: " + str(int(mc.business.supply_count)) +"/[mc.business.supply_goal]":
                ysize 28
                text_style "menu_text_style"
                tooltip "Your current and goal amounts of serum supply. Manufacturing serum requires supplies, spend time ordering supplies from your office or hire someone to do it for you. Raise your supply goal from your office if you want to keep more supply stockpiled."
                action NullAction()
                sensitive True
            #text "Current Raw Supplys: [mc.business.supply_count]/[mc.business.supply_goal]" style "menu_text_style"
            if not mc.business.active_research_design == None:

                text "  Current Research: " style "menu_text_style"
                textbutton "    [mc.business.active_research_design.name] (" + str(__builtin__.int(mc.business.active_research_design.current_research))+"/[mc.business.active_research_design.research_needed])":
                    ysize 28
                    text_style "menu_text_style"
                    tooltip "The current research task of your R&D division. Visit them to set a new goal or to assemble a new serum design."
                    action NullAction()
                    sensitive True
                #text "    [mc.business.active_research_design.name] (" + str(__builtin__.int(mc.business.active_research_design.current_research))+"/[mc.business.active_research_design.research_needed])" style "menu_text_style"
            else:
                textbutton "Current Research: None!":
                    ysize 28
                    text_style "menu_text_style"
                    text_color "#DD0000"
                    tooltip "The current research task of your R&D division. Visit them to set a new goal or to assemble a new serum design."
                    action NullAction()
                    sensitive True
                #text "Current Research: None!" style "menu_text_style" color "#DD0000"

            textbutton "Review Staff" action Show("employee_overview") style "textbutton_style" text_style "textbutton_text_style" xsize 220 tooltip "Review all of your current employees."
            textbutton "Check Stock" action ui.callsinnewcontext("check_business_inventory_loop") style "textbutton_style" text_style "textbutton_text_style" xsize 220 tooltip "Check the doses of serum currently waiting to be sold or sitting in your production area."


screen end_of_day_update():
    add "Paper_Background.png"
    zorder 100
    text mc.business.name:
        style "textbutton_text_style"
        xanchor 0.5
        xalign 0.5
        yalign 0.07
        size 40

    frame:
        background "#1a45a1aa"
        xalign 0.1
        yalign 0.22
        xanchor 0.0
        vbox:
            xsize 1500
            ysize 200
            text "Daily Statistics:" style "textbutton_text_style" size 20
            text "     " + "Current Efficency Modifier: " + str(mc.business.team_effectiveness) + "%" style "textbutton_text_style"
            text "     " + "Production Potential: " + str(mc.business.production_potential) style "textbutton_text_style"
            text "     " + "Supplies Procured: " + str(mc.business.supplies_purchased) + " Units" style "textbutton_text_style"
            text "     " + "Production Used: " + str(mc.business.production_used) style "textbutton_text_style"
            text "     " + "Research Produced: " + str(mc.business.research_produced) style "textbutton_text_style"
            text "     " + "Sales Made: $" + str(mc.business.sales_made) style "textbutton_text_style"
            text "     " + "Daily Salary Paid: $" + str(mc.business.calculate_salary_cost()) style "textbutton_text_style"
            text "     " + "Serums Sold Today: " + str(mc.business.serums_sold) style "textbutton_text_style"
            text "     " + "Serums Ready for Sale: " + str(mc.business.sale_inventory.get_any_serum_count()) style "textbutton_text_style"

    frame:
        background "#1a45a1aa"
        xalign 0.1
        yalign 0.48
        xanchor 0.0
        yanchor 0.0

        viewport:
            mousewheel True
            scrollbars "vertical"
            xsize 1500
            ysize 350
            vbox:
                text "Highlights:" style "textbutton_text_style" size 20
                for item in mc.business.message_list:
                    text "     " + item style "textbutton_text_style" text_align 0.0

                for item in mc.business.counted_message_list:
                    text "     " + item + " x " + str(int(mc.business.counted_message_list[item])) style "textbutton_text_style" text_align 0.0

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.9]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return()
        textbutton "End Day" align [0.5,0.5] style "button_text" text_style "textbutton_text_style"

screen employee_overview(white_list = None, black_list = None, person_select = False): #If select is True it returns the person's name who you click on. If it is false it is a normal overview menu that lets you bring up their detailed info.
    modal True
    zorder 100
    add "Paper_Background.png"
    default division_select = "none"
    default division_name = "All"
    python:
        if not white_list: #If a white list is passed we will only display people that are on the list
            white_list = []
        if not black_list:
            black_list = [] #IF a black list is passed we will not include anyone on the blacklist. Blacklist takes priority

    $ showing_team = []
    $ display_list = []
    $ valid_person_count = 0

    python:
        if division_select == "none":
            showing_team = [] + mc.business.research_team + mc.business.production_team + mc.business.supply_team + mc.business.market_team + mc.business.hr_team
            division_name = "Everyone"
        elif division_select == "r":
            showing_team = mc.business.research_team #ie. take a shallow copy, so we can modify the team without everything exploding.
            division_name = "Research"
        elif division_select == "p":
            showing_team = mc.business.production_team
            division_name = "Production"
        elif division_select == "s":
            showing_team = mc.business.supply_team
            division_name = "Supply Procurement"
        elif division_select == "m":
            showing_team = mc.business.market_team
            division_name = "Marketing"
        elif division_select == "h":
            showing_team = mc.business.hr_team
            division_name = "Human Resources"

        display_list = [person for person in showing_team if (not white_list or person in white_list) and (not black_list or person not in black_list)] #Create our actual display list using people who are either on the white list or not on the black list


    vbox:
        xalign 0.5
        xanchor 0.5
        yalign 0.05
        yanchor 0.0
        spacing 20
        frame:
            background "#1a45a1aa"
            xsize 1800
            ysize 100
            if person_select:
                text "Staff Selection" xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5 size 36 style "menu_text_style"
            else:
                text "Staff Review" xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5 size 36 style "menu_text_style"
        frame:
            background "#1a45a1aa" xsize 1800
            hbox:
                xalign 0.5
                xanchor 0.5
                spacing 40
                $ button_mappings = [["All","none"],["Research","r"],["Production","p"],["Supply","s"],["Marketing","m"],["Human Resources","h"]]
                for button_map in button_mappings:
                    frame:
                        ysize 80
                        if division_select == button_map[1]:
                            background "#4f7ad6"
                        else:
                            background "#1a45a1"
                        button:
                            action SetScreenVariable("division_select", button_map[1])
                            xsize 200
                            ysize 60
                            text button_map[0] xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5 style "textbutton_text_style"




        # text "Position: " + division_name style "menu_text_style" size 24 yalign 0.18 xalign 0.02 xanchor 0.0
        frame:
            yanchor 0.0
            background "#1a45a1aa"
            xsize 1800
            $ grid_count = 15
            if person_select:
                $ grid_count += 1
            grid grid_count len(display_list)+1:
                text "Name" style "menu_text_style" xsize 120
                if person_select:
                    text "" style "menu_text_style" xsize 120
                text "Salary" style "menu_text_style" xsize 120
                text "Happiness" style "menu_text_style" xsize 120
                text "Obedience" style "menu_text_style" xsize 120
                text "Love" style "menu_text_style" xsize 120
                text "Sluttiness" style "menu_text_style" xsize 120
                text "Suggest" style "menu_text_style" xsize 120
                text "Charisma" style "menu_text_style" xsize 120
                text "Int" style "menu_text_style" xsize 120
                text "Focus" style "menu_text_style" xsize 120
                text "Research" style "menu_text_style" xsize 120
                text "Production " style "menu_text_style" xsize 120
                text "Supply" style "menu_text_style" xsize 120
                text "Marketing " style "menu_text_style" xsize 120
                text "HR" style "menu_text_style" xsize 120


                for person in display_list:
                    textbutton person.name + "\n" + person.last_name style "textbutton_style" text_style "menu_text_style" action Show("person_info_detailed",None,person) xmaximum 120 xfill True
                    if person_select:
                        textbutton "Select" style "textbutton_style" text_style "menu_text_style" action Return(person) xsize 120 yalign 0.5
                    text "$" + str(person.salary) + "/day" style "menu_text_style" xsize 120 yalign 0.5
                    text str(int(person.happiness)) style "menu_text_style" xsize 120 yalign 0.5
                    text str(int(person.obedience)) style "menu_text_style" xsize 120 yalign 0.5
                    text str(int(person.love)) style "menu_text_style" xsize 120 yalign 0.5
                    text str(int(person.sluttiness)) style "menu_text_style" xsize 120 yalign 0.5
                    text str(int(person.suggestibility)) style "menu_text_style" xsize 120 yalign 0.5
                    text str(int(person.charisma)) style "menu_text_style" xsize 120 yalign 0.5
                    text str(int(person.int)) style "menu_text_style" xsize 120 yalign 0.5
                    text str(int(person.focus)) style "menu_text_style" xsize 120 yalign 0.5
                    text str(int(person.research_skill)) style "menu_text_style" xsize 120 yalign 0.5
                    text str(int(person.production_skill)) style "menu_text_style" xsize 120 yalign 0.5
                    text str(int(person.supply_skill)) style "menu_text_style" xsize 120 yalign 0.5
                    text str(int(person.market_skill)) style "menu_text_style" xsize 120 yalign 0.5
                    text str(int(person.hr_skill)) style "menu_text_style" xsize 120 yalign 0.5


    if not person_select:
        frame:
            background None
            anchor [0.5,0.5]
            align [0.5,0.88]
            xysize [500,125]
            imagebutton:
                align [0.5,0.5]
                auto "gui/button/choice_%s_background.png"
                focus_mask "gui/button/choice_idle_background.png"
                action Hide("employee_overview")
            textbutton "Return" align [0.5,0.5] style "return_button_style"


screen person_info_ui(the_person): #Used to display stats for a person while you're talking to them.
    layer "Active" #By making this layer active it is cleared whenever we draw a person or clear them off the screen.
    $ formatted_tooltip = ""
    $ formatted_obedience_tooltip = ""
    python:
        positive_effects = ""
        negative_effects = ""
        for situation in the_person.situational_sluttiness:
            if the_person.situational_sluttiness[situation][0] > 0: #We purposefully ignore 0 so we don't show null sluttiness modifiers.
                positive_effects += get_coloured_arrow(1)+get_red_heart(the_person.situational_sluttiness[situation][0])+" - " + the_person.situational_sluttiness[situation][1] + "\n"
            elif the_person.situational_sluttiness[situation][0] < 0:
                negative_effects += get_coloured_arrow(-1)+get_red_heart(-the_person.situational_sluttiness[situation][0])+" - " + the_person.situational_sluttiness[situation][1] + "\n"
        formatted_tooltip += positive_effects + negative_effects
        formatted_tooltip += "The higher a girls sluttiness the more slutty actions she will consider acceptable and normal. Temporary sluttiness (" + get_red_heart(20) + ") is easier to raise but drops slowly over time. Core sluttiness (" + get_gold_heart(20) + ") is permanent, but only increases slowly unless a girl is suggestable."

        positive_effects = ""
        negative_effects = ""
        for situation in the_person.situational_obedience:
            if the_person.situational_obedience[situation][0] > 0:
                positive_effects += get_coloured_arrow(1)+"+"+__builtin__.str(the_person.situational_obedience[situation][0])+ " Obedience - " + the_person.situational_obedience[situation][1] + "\n"
            elif the_person.situational_obedience[situation][0] < 0:
                negative_effects += get_coloured_arrow(1)+""+__builtin__.str(the_person.situational_obedience[situation][0])+ " Obedience - " + the_person.situational_obedience[situation][1] + "\n"
        formatted_obedience_tooltip += positive_effects + negative_effects
        formatted_obedience_tooltip += "Girls with high obedience will listen to commands even when they would prefer not to and are willing to work for less pay. Girls who are told to do things they do not like will lose happiness, and low obedience girls are likely to refuse altogether."

    frame:
        background "gui/topbox.png"
        xsize 1100
        ysize 200
        yalign 0.0
        xalign 0.5
        xanchor 0.5
        hbox:
            xanchor 0.5
            xalign 0.5
            yalign 0.3
            spacing 100
            vbox:
                if the_person.title:
                    text the_person.title style "menu_text_style" size 40
                else:
                    text "???" style "menu_text_style" font the_person.char.what_args["font"] color the_person.char.what_args["color"] size 40

                if mc.business.get_employee_title(the_person) == "None":
                    text "     Job: Not employed." style "menu_text_style"
                else:
                    text "     Job: " + mc.business.get_employee_title(the_person) style "menu_text_style"

                for role in the_person.special_role:
                    if not role.hidden:
                        text "       - " + role.role_name style "menu_text_style" size 14

            vbox:
                if the_person.arousal > 0:
                    textbutton "Arousal: [the_person.arousal]% (+" + get_red_heart(__builtin__.int(the_person.arousal/4)) + ")":
                        ysize 28
                        text_style "menu_text_style"
                        tooltip "When a girl is brought to 100% arousal she will start to climax. Climaxing will instantly turn temporary sluttiness into core sluttiness, as well as make the girl happy. The more aroused you make a girl the more sex positions she is willing to consider."
                        action NullAction()
                        sensitive True
                else:
                    textbutton "Arousal: 0%":
                        ysize 28
                        text_style "menu_text_style"
                        tooltip "When a girl is brought to 100% arousal she will start to climax. Climaxing will instantly turn temporary sluttiness into core sluttiness, as well as make the girl happy. The more aroused you make a girl the more sex positions she is willing to consider."
                        action NullAction()
                        sensitive True

                textbutton "Happiness: [the_person.happiness]":
                    ysize 28
                    text_style "menu_text_style"
                    tooltip "The happier a girl the more tolerant she will be of low pay and unpleasant interactions. High or low happiness will return to it's default value over time."
                    action NullAction()
                    sensitive True

                textbutton "Suggestibility: [the_person.suggestibility]%":
                    ysize 28
                    text_style "menu_text_style"
                    tooltip "How likely this character is to increase her core sluttiness. Every time chunk there is a chance to change 1 point of temporary sluttiness (" + get_red_heart(5) + ") into core sluttiness (" + get_gold_heart(5) + ") as long as temporary sluttiness is higher."
                    action NullAction()
                    sensitive True

                textbutton "Sluttiness: " + get_heart_image_list(the_person):
                    ysize 28
                    text_style "menu_text_style"
                    tooltip formatted_tooltip
                    action NullAction()
                    sensitive True

                textbutton "Love: [the_person.love]":
                    ysize 28
                    text_style "menu_text_style"
                    tooltip "Girls who love you will be more willing to have sex when you're in private (as long as they aren't family) and be more devoted to you. Girls who hate you will have a lower effective sluttiness regardless of the situation."
                    action NullAction()
                    sensitive True

                textbutton "Obedience: [the_person.obedience] - " + get_obedience_plaintext(the_person.obedience):
                    ysize 28
                    text_style "menu_text_style"
                    tooltip formatted_obedience_tooltip
                    action NullAction()
                    sensitive True

            vbox:
                textbutton "Detailed Information" action Show("person_info_detailed",the_person=the_person) style "textbutton_style" text_style "textbutton_text_style"



screen person_info_detailed(the_person):
    add "Paper_Background.png"
    modal True
    zorder 100
    default hr_base = the_person.charisma*3 + the_person.hr_skill*2 + the_person.int + 10
    default market_base = the_person.charisma*3 + the_person.market_skill*2 + the_person.focus + 10
    default research_base = the_person.int*3 + the_person.research_skill*2 + the_person.focus + 10
    default prod_base = the_person.focus*3 + the_person.production_skill*2 + the_person.int + 10
    default supply_base = the_person.focus*3 + the_person.supply_skill*2 + the_person.charisma + 10
    vbox:
        spacing 25
        xalign 0.5
        xanchor 0.5
        yalign 0.2
        frame:
            xsize 1750
            ysize 120
            xalign 0.5
            background "#1a45a1aa"
            vbox:
                xalign 0.5 xanchor 0.5
                text "[the_person.name] [the_person.last_name]" style "menu_text_style" size 30 xalign 0.5 yalign 0.5 yanchor 0.5 color the_person.char.who_args["color"] font the_person.char.what_args["font"]
                if not mc.business.get_employee_title(the_person) == "None":
                    text "Position: " + mc.business.get_employee_title(the_person) + " ($[the_person.salary]/day)" style "menu_text_style" xalign 0.5 yalign 0.5 yanchor 0.5

                $ visible_roles = []
                $ role_string = "Special Roles: "
                python:
                    for role in the_person.special_role:
                        if not role.hidden:
                            visible_roles.append(role.role_name)

                    if visible_roles:
                        role_string += visible_roles[0]
                        for role in visible_roles[1::]: #Slicing off the first manually let's us use commas correctly.
                            role_string += ", " + role
                if visible_roles:
                    text role_string style "menu_text_style" xalign 0.5 yalign 0.5 yanchor 0.5

        hbox:
            xsize 1750
            xalign 0.5
            xanchor 0.5
            spacing 30
            frame:
                background "#1a45a1aa"
                xsize 325
                ysize 450
                vbox:
                    text "Status and Info" style "menu_text_style" size 22
                    text "Happiness: [the_person.happiness]" style "menu_text_style"
                    text "Suggestibility: [the_person.suggestibility]" style "menu_text_style"
                    text "Sluttiness: [the_person.sluttiness]" style "menu_text_style"
                    text "Love: [the_person.love]" style "menu_text_style"
                    text "Obedience: [the_person.obedience] - " + get_obedience_plaintext(the_person.obedience) style "menu_text_style"

                    text "Age: [the_person.age]" style "menu_text_style"
                    text "Relationship:  [the_person.relationship]" style "menu_text_style"
                    if the_person.relationship != "Single":
                        text "Significant Other: [the_person.SO_name]" style "menu_text_style"
                    text "Kids: [the_person.kids]" style "menu_text_style"

            frame:
                background "#1a45a1aa"
                xsize 325
                ysize 450
                vbox:
                    text "Characteristics" style "menu_text_style" size 22
                    text "Charisma: [the_person.charisma]" style "menu_text_style"
                    text "Intelligence: [the_person.int]" style "menu_text_style"
                    text "Focus: [the_person.focus]" style "menu_text_style"
            frame:
                background "#1a45a1aa"
                xsize 325
                ysize 450
                vbox:
                    text "Work Skills" style "menu_text_style" size 22
                    text "HR Skill: [the_person.hr_skill]" style "menu_text_style"
                    text "Marketing Skill: [the_person.market_skill]" style "menu_text_style"
                    text "Researching Skill: [the_person.research_skill]" style "menu_text_style"
                    text "Production Skill: [the_person.production_skill]" style "menu_text_style"
                    text "Supply Skill: [the_person.supply_skill]" style "menu_text_style"

            frame:
                background "#1a45a1aa"
                xsize 325
                ysize 450
                vbox:
                    text "Sex Skills" style "menu_text_style" size 22
                    text "Foreplay Skill: " + str(the_person.sex_skills["Foreplay"]) style "menu_text_style"
                    text "Oral Skill: " + str(the_person.sex_skills["Oral"]) style "menu_text_style"
                    text "Vaginal Skill: " + str(the_person.sex_skills["Vaginal"]) style "menu_text_style"
                    text "Anal: " + str(the_person.sex_skills["Anal"]) style "menu_text_style"

            frame:
                background "#1a45a1aa"
                xsize 325
                ysize 450
                vbox:
                    text "Currently Affected By:" style "menu_text_style" size 22
                    if not the_person.serum_effects:
                        text "No active serums." style "menu_text_style"

                    for serum in the_person.serum_effects:
                        text serum.name + " : " + str(serum.duration - serum.duration_counter) + " Turns Left" style "menu_text_style"
                    null height 20


        hbox:
            xsize 1750
            spacing 30
            $ master_opinion_dict = dict(the_person.opinions, **the_person.sexy_opinions)
            frame:
                background "#1a45a1aa"
                xsize 415
                ysize 200
                vbox:
                    text "Loves" style "menu_text_style" size 22
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == 2:
                            if master_opinion_dict[opinion][1]:
                                text "   " + opinion style "menu_text_style"
                            else:
                                text "   ????" style "menu_text_style"

            frame:
                background "#1a45a1aa"
                xsize 415
                ysize 200
                vbox:
                    text "Likes" style "menu_text_style" size 22
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == 1:
                            if master_opinion_dict[opinion][1]:
                                text "   " + opinion style "menu_text_style"
                            else:
                                text "   ????" style "menu_text_style"

            frame:
                background "#1a45a1aa"
                xsize 415
                ysize 200
                vbox:
                    text "Dislikes" style "menu_text_style" size 22
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == -1:
                            if master_opinion_dict[opinion][1]:
                                text "   " + opinion style "menu_text_style"
                            else:
                                text "   ????" style "menu_text_style"

            frame:
                background "#1a45a1aa"
                xsize 415
                ysize 200
                vbox:
                    text "Hates" style "menu_text_style" size 22
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == -2:
                            if master_opinion_dict[opinion][1]:
                                text "   " + opinion style "menu_text_style"
                            else:
                                text "   ????" style "menu_text_style"

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Hide("person_info_detailed")
        textbutton "Return" align [0.5,0.5] style "return_button_style"


screen mc_character_sheet():
    add "Paper_Background.png"
    modal True
    zorder 100
    vbox:
        xanchor 0.5
        xalign 0.5
        yalign 0.2
        frame:
            background "#1a45a1aa"
            vbox:
                xsize 1620
                text mc.name + " " + mc.last_name style "menu_text_style" size 40 xanchor 0.5 xalign 0.5
                text "Owner of: " + mc.business.name style "menu_text_style" size 30 xanchor 0.5 xalign 0.5
        null height 60
        hbox:
            xanchor 0.5
            xalign 0.5
            yalign 0.4
            spacing 40
            frame:
                background "#1a45a1aa"
                xalign 0.5
                xanchor 0.5
                vbox:
                    xsize 500
                    text "Main Stats" style "menu_text_style" size 32 xalign 0.5
                    text "Unspent Points: " + str(mc.free_stat_points) style "menu_text_style" xalign 0.5
                    hbox:
                        xalign 0.5
                        text "Charisma: " + str(mc.charisma) + "/" + str(mc.max_stats) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_stat, "cha") sensitive mc.free_stat_points > 0 and mc.charisma<mc.max_stats yanchor 0.5 yalign 0.5

                    hbox:
                        xalign 0.5
                        text "Intelligence: " + str(mc.int) + "/" + str(mc.max_stats) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_stat, "int") sensitive mc.free_stat_points > 0 and mc.int<mc.max_stats yanchor 0.5 yalign 0.5

                    hbox:
                        xalign 0.5
                        text "Focus: " + str(mc.focus) + "/" + str(mc.max_stats) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_stat, "foc") sensitive mc.free_stat_points > 0 and mc.focus<mc.max_stats yanchor 0.5 yalign 0.5


                    null height 40
                    frame:
                        background "#888888"
                        xsize 500
                        vbox:
                            xalign 0.5
                            if mc.stat_goal:
                                text "Goal: " + mc.stat_goal.name style "menu_text_style" xalign 0.5 size 24
                                text "    " + mc.stat_goal.description style "menu_text_style" xalign 0.5
                                frame:
                                    ysize 60
                                    background None
                                    bar value mc.stat_goal.get_progress_fraction() range 1 xalign 0.5
                                    text mc.stat_goal.get_reported_progress() style "menu_text_style" xalign 0.5 yanchor 0.5 yalign 0.5
                                if mc.stat_goal.completed:
                                    textbutton "Collect Reward" xalign 0.5 action Function(mc.complete_goal,mc.stat_goal) style "textbutton_style" text_style "textbutton_text_style"
                                else:
                                    textbutton "Replace Goal (1/day)" xalign 0.5 action Function(mc.scrap_goal,mc.stat_goal) style "textbutton_style" text_style "textbutton_text_style" sensitive mc.scrap_goal_available and not mc.stat_goal.mandatory
                            else:
                                text "Goal: No goals available!" style "menu_text_style" xalign 0.5

            frame:
                background "#1a45a1aa"
                xalign 0.5
                xanchor 0.5
                vbox:
                    xsize 500
                    text "Work Skills" style "menu_text_style" size 32 xalign 0.5
                    text "Unspent Points: " + str(mc.free_work_points) style "menu_text_style" xalign 0.5
                    hbox:
                        xalign 0.5
                        text "Human Resources: " + str(mc.hr_skill) + "/" + str(mc.max_work_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_work_skill, "hr") sensitive mc.free_work_points > 0 and mc.hr_skill < mc.max_work_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Marketing: " + str(mc.market_skill) + "/" + str(mc.max_work_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_work_skill, "market") sensitive mc.free_work_points > 0 and mc.market_skill < mc.max_work_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Research and Development: " + str(mc.research_skill) + "/" + str(mc.max_work_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_work_skill, "research") sensitive mc.free_work_points > 0 and mc.research_skill < mc.max_work_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Production: " + str(mc.production_skill) + "/" + str(mc.max_work_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_work_skill, "production") sensitive mc.free_work_points > 0 and mc.production_skill < mc.max_work_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Supply Procurement: " + str(mc.supply_skill) + "/" + str(mc.max_work_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_work_skill, "supply") sensitive mc.free_work_points > 0 and mc.supply_skill < mc.max_work_skills yanchor 0.5 yalign 0.5

                    null height 40
                    frame:
                        background "#888888"
                        xsize 500
                        vbox:
                            xalign 0.5
                            if mc.work_goal:
                                text "Goal: " + mc.work_goal.name style "menu_text_style" xalign 0.5 size 24
                                text "    " + mc.work_goal.description style "menu_text_style" xalign 0.5
                                frame:
                                    ysize 60
                                    background None
                                    bar value mc.work_goal.get_progress_fraction() range 1 xalign 0.5
                                    text mc.work_goal.get_reported_progress() style "menu_text_style" xalign 0.5 yanchor 0.5 yalign 0.5
                                if mc.work_goal.completed:
                                    textbutton "Collect Reward" xalign 0.5 action Function(mc.complete_goal,mc.work_goal) style "textbutton_style" text_style "textbutton_text_style"
                                else:
                                    textbutton "Replace Goal (1/day)" xalign 0.5 action Function(mc.scrap_goal,mc.work_goal) style "textbutton_style" text_style "textbutton_text_style" sensitive mc.scrap_goal_available and not mc.work_goal.mandatory
                            else:
                                text "Goal: No goals available!" style "menu_text_style" xalign 0.5

            frame:
                background "#1a45a1aa"
                xalign 0.5
                xanchor 0.5
                vbox:
                    xsize 500
                    text "Sex Skills" style "menu_text_style" size 32 xalign 0.5
                    text "Unspent Points: " + str(mc.free_sex_points) style "menu_text_style" xalign 0.5
                    hbox:
                        xalign 0.5
                        text "Stamina: " + str(mc.max_stamina) + "/" + str(mc.max_sex_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_sex_skill, "stam") sensitive mc.free_sex_points > 0 and mc.max_stamina<mc.max_sex_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Foreplay: " + str(mc.sex_skills["Foreplay"]) + "/" + str(mc.max_sex_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_sex_skill, "Foreplay") sensitive mc.free_sex_points > 0 and mc.sex_skills["Foreplay"]<mc.max_sex_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Oral: " + str(mc.sex_skills["Oral"]) + "/" + str(mc.max_sex_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_sex_skill, "Oral") sensitive mc.free_sex_points > 0 and mc.sex_skills["Oral"]<mc.max_sex_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Vaginal: " + str(mc.sex_skills["Vaginal"]) + "/" + str(mc.max_sex_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_sex_skill, "Vaginal") sensitive mc.free_sex_points > 0 and mc.sex_skills["Vaginal"]<mc.max_sex_skills yanchor 0.5 yalign 0.5
                    hbox:
                        xalign 0.5
                        text "Anal: " + str(mc.sex_skills["Anal"]) + "/" + str(mc.max_sex_skills) style "menu_text_style" xalign 0.5 yalign 0.5
                        textbutton "+1" style "textbutton_style" text_style "textbutton_text_style" xalign 0.5 action Function(mc.improve_sex_skill, "Anal") sensitive mc.free_sex_points > 0 and mc.sex_skills["Anal"]<mc.max_sex_skills yanchor 0.5 yalign 0.5

                    null height 40
                    frame:
                        background "#888888"
                        xsize 500
                        vbox:
                            xalign 0.5
                            if mc.sex_goal:
                                text "Goal: " + mc.sex_goal.name style "menu_text_style" xalign 0.5 size 24
                                text "    " + mc.sex_goal.description style "menu_text_style" xalign 0.5
                                frame:
                                    ysize 60
                                    background None
                                    bar value mc.sex_goal.get_progress_fraction() range 1 xalign 0.5
                                    text mc.sex_goal.get_reported_progress() style "menu_text_style" xalign 0.5 yanchor 0.5 yalign 0.5
                                if mc.sex_goal.completed:
                                    textbutton "Collect Reward" xalign 0.5 action Function(mc.complete_goal,mc.sex_goal) style "textbutton_style" text_style "textbutton_text_style"
                                else:
                                    textbutton "Replace Goal (1/day)" xalign 0.5 action Function(mc.scrap_goal,mc.sex_goal) style "textbutton_style" text_style "textbutton_text_style" sensitive mc.scrap_goal_available and not mc.sex_goal.mandatory
                            else:
                                text "Goal: No goals available!" style "menu_text_style" xalign 0.5

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Hide("mc_character_sheet")
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"





screen interview_ui(the_candidates,count):
    default current_selection = 0
    default the_candidate = the_candidates[current_selection]
    vbox:
        yalign 0.2
        xalign 0.4
        xanchor 0.5
        spacing 30
        frame:
            background "#1a45a1aa"
            ysize 80
            xsize 1320
            xalign 0.5
            xanchor 0.5
            text "[the_candidate.name] [the_candidate.last_name]" style "menu_text_style" size 50 xanchor 0.5 xalign 0.5 color the_candidate.char.who_args["color"] font the_candidate.char.what_args["font"]

        hbox:
            xsize 1320
            spacing 30
            frame:
                background "#1a45a1aa"
                xsize 420
                ysize 550
                vbox:
                    text "Personal Information" style "menu_text_style" size 26 xalign 0.5 xanchor 0.5 #Info about the person: age, height, happiness, obedience, etc.
                    text "Age: [the_candidate.age]" style "menu_text_style" size 16
                    text "Required Salary: $[the_candidate.salary]/day" style "menu_text_style" size 16


            frame:
                background "#1a45a1aa"
                xsize 420
                ysize 550
                vbox:
                    text "Stats and Skills" style "menu_text_style" size 26 xalign 0.5 xanchor 0.5 #Info about the persons raw stats, work skills, and sex skills
                    text "Stats" style "menu_text_style" size 20
                    text "    Charisma: [the_candidate.charisma]" style "menu_text_style" size 16
                    text "    Intelligence: [the_candidate.int]" style "menu_text_style" size 16
                    text "    Focus: [the_candidate.focus]" style "menu_text_style" size 16
                    text "Work Skills" style "menu_text_style" size 20
                    text "    HR: [the_candidate.hr_skill]" style "menu_text_style" size 16
                    text "    Marketing: [the_candidate.market_skill]" style "menu_text_style" size 16
                    text "    Research: [the_candidate.research_skill]" style "menu_text_style" size 16
                    text "    Production: [the_candidate.production_skill]" style "menu_text_style" size 16
                    text "    Supply: [the_candidate.supply_skill]" style "menu_text_style" size 16
                    if recruitment_knowledge_four_policy.is_owned():
                        text "Sex Skills" style "menu_text_style" size 20
                        text "    Foreplay: " + str(the_candidate.sex_skills["Foreplay"]) style "menu_text_style" size 16
                        text "    Oral: " + str(the_candidate.sex_skills["Oral"]) style "menu_text_style" size 16
                        text "    Vaginal: " + str(the_candidate.sex_skills["Vaginal"]) style "menu_text_style" size 16
                        text "    Anal: " + str(the_candidate.sex_skills["Anal"]) style "menu_text_style" size 16

            frame:
                $ master_opinion_dict = dict(the_candidate.opinions, **the_candidate.sexy_opinions)
                background "#1a45a1aa"
                xsize 420
                ysize 550
                vbox:
                    text "Opinions" style "menu_text_style" size 26 xalign 0.5 xanchor 0.5 #Info about the persons loves, likes, dislikes, and hates
                    text "Loves" style "menu_text_style" size 20
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == 2:
                            if master_opinion_dict[opinion][1]:
                                text "    " + opinion style "menu_text_style" size 16
                            else:
                                text "    ????" style "menu_text_style" size 16

                    text "Likes" style "menu_text_style" size 20
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == 1:
                            if master_opinion_dict[opinion][1]:
                                text "    " + opinion style "menu_text_style" size 16
                            else:
                                text "    ????" style "menu_text_style"

                    text "Dislikes" style "menu_text_style" size 20
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == -1:
                            if master_opinion_dict[opinion][1]:
                                text "    " + opinion style "menu_text_style" size 16
                            else:
                                text "    ????" style "menu_text_style" size 16


                    text "Hates" style "menu_text_style" size 20
                    for opinion in master_opinion_dict:
                        if master_opinion_dict[opinion][0] == -2:
                            if master_opinion_dict[opinion][1]:
                                text "    " + opinion style "menu_text_style" size 16
                            else:
                                text "    ????" style "menu_text_style" size 16

        frame:
            background "#1a45a1aa"
            xsize 1320
            ysize 200
            vbox:
                text "Expected Production" style "menu_text_style" size 30
                text "    Human Resources: +" + str(the_candidate.hr_skill*2 + the_candidate.charisma*3 + the_candidate.int + 10) + "% Company efficency per time chunk." style "menu_text_style" size 16
                text "    Marketing: " + str(the_candidate.market_skill*2 + the_candidate.charisma*3 + the_candidate.focus + 10) + " Units of serum sold per time chunk." style "menu_text_style" size 16
                text "    Research and Development: " + str(the_candidate.research_skill*2 + the_candidate.int*3 + the_candidate.focus + 10) + " Research points per time chunk." style "menu_text_style" size 16
                text "    Production: " + str(the_candidate.production_skill*2 + the_candidate.focus*3 + the_candidate.int + 10) + " Production points per time chunk." style "menu_text_style" size 16
                text "    Supply Procurement: " + str(the_candidate.supply_skill*2 + the_candidate.focus*3 + the_candidate.charisma + 10) + " Units of supply per time chunk." style "menu_text_style" size 16

        frame:
            background "#1a45a1aa"
            xsize 1320
            ysize 100
            hbox:
                yalign 0.5
                yanchor 0.5
                xalign 0.5
                xanchor 0.5
                textbutton "Previous Candidate" action [SetScreenVariable("current_selection",current_selection-1),
                    SetScreenVariable("the_candidate",the_candidates[current_selection-1]),
                    Function(show_candidate,the_candidates[current_selection-1])] sensitive current_selection > 0 selected False style "textbutton_style" text_style "textbutton_text_style" xanchor 0.5 xalign 0.5 yalign 0.5 yanchor 0.5

                null width 300
                textbutton "Hire Nobody" action Return("None") style "textbutton_style" text_style "textbutton_text_style" xanchor 0.5 xalign 0.5 yalign 0.5 yanchor 0.5

                textbutton "Hire " action Return(the_candidate) style "textbutton_style" text_style "textbutton_text_style" xanchor 0.5 xalign 0.5 yalign 0.5 yanchor 0.5
                null width 300
                textbutton "Next Candidate" action [SetScreenVariable("current_selection",current_selection+1),
                    SetScreenVariable("the_candidate",the_candidates[current_selection+1]),
                    Function(show_candidate,the_candidates[current_selection+1])] sensitive current_selection < count-1 selected False style "textbutton_style" text_style "textbutton_text_style"  xanchor 0.5 xalign 0.5 yalign 0.5 yanchor 0.5


    imagebutton:
        auto "/tutorial_images/restart_tutorial_%s.png"
        xsize 54
        ysize 54
        yanchor 1.0
        xanchor 1.0
        xalign 1.0
        yalign 1.0
        action Function(mc.business.reset_tutorial,"hiring_tutorial")


    $ hiring_tutorial_length = 5 #The number of  tutorial screens we have.
    if mc.business.event_triggers_dict["hiring_tutorial"] > 0 and mc.business.event_triggers_dict["hiring_tutorial"] <= hiring_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/hiring_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["hiring_tutorial"])+".png"
            hover "/tutorial_images/hiring_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["hiring_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"hiring_tutorial")



init -2 python: # Some functions used only within screens for modifying variables
    def show_candidate(the_candidate):
        renpy.scene("Active")
        the_candidate.draw_person(show_person_info = False)


screen show_serum_inventory(the_inventory, extra_inventories = [],inventory_names = []): #You can now pass extra inventories, as well as names for all of the inventories you are passing. Returns nothing, but is used to view inventories.
    add "Science_Menu_Background.png"
    hbox:
        $ count = 0
        xalign 0.05
        yalign 0.05
        spacing 40
        for an_inventory in [the_inventory] + extra_inventories:
            frame:
                background "#888888"
                xsize 400
                vbox:
                    xalign 0.02
                    yalign 0.02
                    if len(inventory_names) > 0 and count < len(inventory_names):
                        text inventory_names[count] style "menu_text_style" size 25
                    else:
                        text "Serums in Inventory" style "menu_text_style" size 25

                    for design in an_inventory.serums_held:
                        textbutton design[0].name + ": " + str(design[1]) + " Doses" style "textbutton_style" text_style "textbutton_text_style" action NullAction() sensitive True hovered Show("serum_tooltip",None,design[0]) unhovered Hide("serum_tooltip")
                $ count += 1

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return()
        textbutton "Return" align [0.5,0.5] style "return_button_style"



screen serum_design_ui(starting_serum,current_traits):
    add "Science_Menu_Background.png"
    python:
        effective_traits = 0
        for trait_count in starting_serum.traits:
            if not "Production" in trait_count.exclude_tags:
                effective_traits += 1
    hbox:
        yalign 0.15
        xanchor 0.5
        xalign 0.5
        xsize 1080
        spacing 40
        frame:
            background "#888888"
            ysize 800
            vbox:
                xsize 550
                #text "Add a trait" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5
                viewport:
                    xsize 550
                    ysize 480
                    scrollbars "vertical"
                    mousewheel True
                    frame:
                        xsize 550
                        background None
                        vbox:
                            xsize 530
                            text "Pick Production Type" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5 xsize 530
                            for trait in sorted(sorted(list_of_traits, key = lambda trait: trait.exclude_tags, reverse = True), key=lambda trait: trait.tier, reverse = True): # Sort traits by exclude tags (So all production traits are grouped, for example), then by tier (so the highest tier production tag ends up at the top
                                if trait not in starting_serum.traits and trait.researched and "Production" in trait.exclude_tags:
                                    $ trait_tags = ""
                                    if trait.exclude_tags:
                                        $ trait_tags = " - "
                                        for a_tag in trait.exclude_tags:
                                            $ trait_tags += "[[" + a_tag + "]"
                                    $ trait_allowed = True
                                    python: # Check to see if the trait is excluded by any of the traits currently in the serum. A long looped segment only to deal with lists of tags, which are unlikely.
                                        for checking_trait in starting_serum.traits:
                                            for tag in trait.exclude_tags:
                                                for checking_tag in checking_trait.exclude_tags:
                                                    if tag == checking_tag:
                                                        trait_allowed = False
                                    $ trait_side_effects = "\nMastery Level: " + str(trait.mastery_level) + " | Side Effect Chance: %" + str(trait.get_effective_side_effect_chance())
                                    textbutton trait.name + trait_tags + trait_side_effects action [Hide("trait_tooltip"),Function(starting_serum.add_trait,trait)] sensitive trait_allowed style "textbutton_style" text_style "textbutton_text_style" hovered Show("trait_tooltip",None,trait,0.315,0.57) unhovered Hide("trait_tooltip") xsize 520

                            null height 30
                            text "Add Serum Traits" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5 xsize 530
                            for trait in sorted(sorted(list_of_traits, key = lambda trait: trait.exclude_tags, reverse = True), key=lambda trait: trait.tier, reverse = True): # Sort traits by exclude tags (So all production traits are grouped, for example), then by tier (so the highest tier production tag ends up at the top
                                if trait not in starting_serum.traits and trait.researched and "Production" not in trait.exclude_tags:
                                    $ trait_tags = ""
                                    if trait.exclude_tags:
                                        $ trait_tags = " - "
                                        for a_tag in trait.exclude_tags:
                                            $ trait_tags += "[[" + a_tag + "]"
                                    $ trait_allowed = True
                                    python: # Check to see if the trait is excluded by any of the traits currently in the serum. A long looped segment only to deal with lists of tags, which are unlikely.
                                        for checking_trait in starting_serum.traits:
                                            for tag in trait.exclude_tags:
                                                for checking_tag in checking_trait.exclude_tags:
                                                    if tag == checking_tag:
                                                        trait_allowed = False
                                    $ trait_side_effects = "\nMastery Level: " + str(trait.mastery_level) + " | Side Effect Chance: %" + str(trait.get_effective_side_effect_chance())
                                    textbutton trait.name + trait_tags + trait_side_effects action [Hide("trait_tooltip"),Function(starting_serum.add_trait,trait)] sensitive trait_allowed style "textbutton_style" text_style "textbutton_text_style" hovered Show("trait_tooltip",None,trait,0.315,0.57) unhovered Hide("trait_tooltip") xsize 530

        frame:
            background "#888888"
            ysize 800
            vbox:
                xsize 550
                text "Remove a trait" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5
                viewport:
                    xsize 550
                    ysize 480
                    scrollbars "vertical"
                    mousewheel True
                    frame:
                        xsize 550
                        background None
                        vbox:
                            for trait in starting_serum.traits:
                                $ trait_tags = ""
                                if trait.exclude_tags:
                                    $ trait_tags = " - "
                                    for a_tag in trait.exclude_tags:
                                        $ trait_tags += "[[" + a_tag + "]"
                                $ trait_side_effects = "\nMastery Level: " + str(trait.mastery_level) + " | Side Effect Chance: %" + str(trait.get_effective_side_effect_chance())
                                textbutton trait.name + trait_tags + trait_side_effects action[Hide("trait_tooltip"), Function(starting_serum.remove_trait,trait)] style "textbutton_style" text_style "textbutton_text_style" hovered Show("trait_tooltip",None,trait,0.635,0.57) unhovered Hide("trait_tooltip") xsize 550

        frame:
            background "#888888"
            ysize 800
            vbox:
                xsize 550
                text "Current Serum Statistics:" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5
                if effective_traits > starting_serum.slots:
                    text "Trait Slots: " + str(effective_traits) +"/[starting_serum.slots]" style "menu_text_style" color "#DD0000" xanchor 0.5 xalign 0.5
                else:
                    text "Trait Slots: " + str(effective_traits) +"/[starting_serum.slots]" style "menu_text_style" xanchor 0.5 xalign 0.5
                hbox:
                    xanchor 0.5
                    xalign 0.5
                    spacing 10
                    xsize 550
                    for num in __builtin__.range(__builtin__.max(starting_serum.slots,effective_traits)):
                        if num < effective_traits and num < starting_serum.slots:
                            add "Serum_Slot_Full.png" xanchor 0.5 xalign 0.5
                        elif num < effective_traits and num >= starting_serum.slots:
                            add "Serum_Slot_Incorrect.png" xanchor 0.5 xalign 0.5
                        else:
                            add "Serum_Slot_Empty.png" xanchor 0.5 xalign 0.5
                grid 2 3 xanchor 0.5 xalign 0.5:
                    spacing 10
                    text "Research Required: [starting_serum.research_needed]" style "menu_text_style"
                    text "Production Cost: [starting_serum.production_cost]" style "menu_text_style"
                    text "Value: $[starting_serum.value]" style "menu_text_style"
                    $ calculated_profit = (starting_serum.value*mc.business.batch_size)-starting_serum.production_cost
                    if calculated_profit > 0:
                        text "Expected Profit:{color=#98fb98} $[calculated_profit]{/color}" style "menu_text_style"
                    else:
                        $ calculated_profit = 0 - calculated_profit
                        text "Expected Profit:{color=#ff0000} -$[calculated_profit]{/color}" style "menu_text_style"
                    text "Duration: [starting_serum.duration] Turns" style "menu_text_style"
                    null #Placeholder to keep the grid aligned

                text "Serum Effects:" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5

                viewport:
                    xsize 550
                    scrollbars "vertical"
                    mousewheel True
                    frame:
                        xsize 550
                        background None
                        vbox:
                            for trait in starting_serum.traits:
                                text trait.name style "menu_text_style"
                                text "    "  + trait.positive_slug style "menu_text_style" color "#98fb98"
                                text "    "  + trait.build_negative_slug() style "menu_text_style" color "#ff0000"

    frame:
        background "#888888"
        xsize 250
        xanchor 0.5
        xalign 0.5
        yalign 0.9
        vbox:
            xanchor 0.5
            xalign 0.5
            textbutton "Create Design":
                action Return(starting_serum) sensitive (starting_serum.slots >= effective_traits and len(starting_serum.traits) and starting_serum.has_tag("Production")) > 0
                style "textbutton_style"
                text_style "textbutton_text_style"
                xanchor 0.5
                xalign 0.5
                xsize 230

            textbutton "Reject Design" action Return("None") style "textbutton_style" text_style "textbutton_text_style" xanchor 0.5 xalign 0.5 xsize 230

    imagebutton:
        auto "/tutorial_images/restart_tutorial_%s.png"
        xsize 54
        ysize 54
        yanchor 1.0
        xalign 0.0
        yalign 1.0
        action Function(mc.business.reset_tutorial,"design_tutorial")

    $ design_tutorial_length = 5 #The number of  tutorial screens we have.
    if mc.business.event_triggers_dict["design_tutorial"] > 0 and mc.business.event_triggers_dict["design_tutorial"] <= design_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/design_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["design_tutorial"])+".png"
            hover "/tutorial_images/design_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["design_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"design_tutorial")


screen review_designs_screen():
    add "Science_Menu_Background.png"
    vbox:
        text "Serum Designs:" style "menu_text_style" size 30
        grid 2 len(mc.business.serum_designs):
            for serum_design in mc.business.serum_designs:
                if serum_design.researched:
                    textbutton serum_design.name + " - Research Finished":
                        action NullAction() hovered Show("serum_tooltip",None,serum_design) unhovered Hide("serum_tooltip") style "textbutton_style" text_style "textbutton_text_style"
                else:
                    textbutton serum_design.name + " - " + str(serum_design.current_research) + "/" + str(serum_design.research_needed) + " Research Required":
                        action NullAction() hovered Show("serum_tooltip",None,serum_design) unhovered Hide("serum_tooltip") style "textbutton_style" text_style "textbutton_text_style"

                textbutton "Scrap Design" action Function(mc.business.remove_serum_design,serum_design) style "textbutton_style" text_style "textbutton_text_style"

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return()
        textbutton "Return" align [0.5,0.5] style "return_button_style"


screen serum_tooltip(the_serum, set_x_align = 0.9, set_y_align = 0.1):
    frame:
        background "#888888"
        xalign set_x_align
        yalign set_y_align
        yanchor 0.0
        vbox:
            text "[the_serum.name]" style "menu_text_style" xanchor 0.5 xalign 0.5 size 26
            grid 2 3 xanchor 0.5 xalign 0.5:
                spacing 10
                text "Research Required: [the_serum.research_needed]" style "menu_text_style"
                text "Production Cost: [the_serum.production_cost]" style "menu_text_style"
                text "Value: $[the_serum.value]" style "menu_text_style"
                $ calculated_profit = (the_serum.value*mc.business.batch_size)-the_serum.production_cost
                if calculated_profit > 0:
                    text "Expected Profit:{color=#98fb98} $[calculated_profit]{/color}" style "menu_text_style"
                else:
                    $ calculated_profit = 0 - calculated_profit
                    text "Expected Profit:{color=#ff0000} -$[calculated_profit]{/color}" style "menu_text_style"

                text "Duration: [the_serum.duration] Turns" style "menu_text_style"
                null

            for trait in the_serum.traits:
                text trait.name style "menu_text_style"
                text "    "  + trait.positive_slug style "menu_text_style" color "#98fb98"
                text "    "  + trait.negative_slug style "menu_text_style" color "#ff0000"
            if the_serum.side_effects:
                for side_effect in the_serum.side_effects:
                    text side_effect.name style "menu_text_style"
                    text "    "  + side_effect.negative_slug style "menu_text_style" color "#ff0000"


screen trait_tooltip(the_trait,given_xalign=0.9,given_yalign=0.1):
    frame:
        background "#888888"

        xalign given_xalign
        yalign given_yalign
        xanchor 1.0
        yanchor 0.0
        vbox:
            xsize 500
            text the_trait.name style "menu_text_style" xalign 0.5 xanchor 0.5
            text the_trait.positive_slug style "menu_text_style" size 14 color "#98fb98" xalign 0.5 xanchor 0.5
            text the_trait.build_negative_slug() style "menu_text_style" size 14 color "#ff0000" xalign 0.5 xanchor 0.5
            text the_trait.desc style "menu_text_style" xalign 0.5 xanchor 0.5

screen trait_list_tooltip(the_traits):
    hbox:
        spacing 50
        xalign 0.5
        yalign 0.1
        xanchor 0.0
        for trait in the_traits:
            frame: #TODO: Functionally identical to trait Figure out how to put this into a separate screen or displayable.
                background "#888888"
                xalign 0.0
                yalign 0.0
                xanchor 1.0
                yanchor 0.0
                vbox:
                    xsize 500
                    text trait.name style "menu_text_style" xalign 0.5 xanchor 0.5
                    text trait.positive_slug style "menu_text_style" size 14 color "#98fb98" xalign 0.5 xanchor 0.5
                    text trait.build_negative_slug() style "menu_text_style" size 14 color "#ff0000" xalign 0.5 xanchor 0.5
                    text trait.desc style "menu_text_style" xalign 0.5 xanchor 0.5


screen serum_trade_ui(inventory_1,inventory_2,name_1="Player",name_2="Business"): #Lets you trade serums back and forth between two different inventories. Inventory 1 is assumed to be the players.
    modal True
    add "Science_Menu_Background.png"
    frame:
        background "#888888"
        xalign 0.3
        xanchor 0.5
        yalign 0.1

        vbox:
            xsize 590
            ysize 800
            yalign 0.0
            text "Trade Serums Between Inventories." style "menu_text_style" size 25 xalign 0.5 xanchor 0.5
            for serum in set(inventory_1.get_serum_type_list()) | set(inventory_2.get_serum_type_list()): #Gets a unique entry for each serum design that shows up in either list. Doesn't duplicate if it's in both.
                # has a few things. 1) name of serum design. 2) count of first inventory, 3) arrows for transfering, 4) count of second inventory.
                frame:
                    background "#777777"
                    xalign 0.5
                    xanchor 0.5
                    yalign 0.0
                    vbox:
                        xalign 0.5
                        xanchor 0.5
                        hbox:
                            textbutton serum.name + ": " style "textbutton_style" text_style "menu_text_style" action NullAction() hovered Show("serum_tooltip",None,serum) unhovered Hide("serum_tooltip") #displays the name of this particular serum
                            null width 40
                            text name_1 + " has: " + str(inventory_1.get_serum_count(serum)) style "menu_text_style"#The players current inventory count. 0 if there is nothing in their inventory
                            textbutton "#<#" action [Function(inventory_1.change_serum,serum,1),Function(inventory_2.change_serum,serum,-1)] sensitive (inventory_2.get_serum_count(serum) > 0) style "textbutton_style" text_style "textbutton_text_style"
                            #When pressed, moves 1 serum from the business inventory to the player. Not active if the business has nothing in it.
                            null width 40
                            textbutton "#>#" action [Function(inventory_2.change_serum,serum,1),Function(inventory_1.change_serum,serum,-1)] sensitive (inventory_1.get_serum_count(serum) > 0) style "textbutton_style" text_style "textbutton_text_style"
                            text name_2 + " has: " + str(inventory_2.get_serum_count(serum)) style "menu_text_style"


    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return()
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"


screen serum_select_ui: #How you select serum and trait research
    add "Science_Menu_Background.png"
    vbox:
        xalign 0.1
        yalign 0.4
        frame:
            background "#888888"
            xsize 1000
            if not mc.business.active_research_design == None:
                text "Current Research: [mc.business.active_research_design.name] ([mc.business.active_research_design.current_research]/[mc.business.active_research_design.research_needed])" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5
            else:
                text "Current Research: None!" style "menu_text_style" size 25 xanchor 0.5 xalign 0.5

        null height 20

        frame:
            background "#888888"
            xsize 1000
            ysize 900
            hbox:
                viewport:
                    xsize 320
                    ysize 800
                    scrollbars "vertical"
                    mousewheel True
                    vbox:
                        xsize 320
                        text "Research New Traits" style "menu_text_style" size 20 xanchor 0.5 xalign 0.5
                        for trait in sorted(sorted(list_of_traits, key = lambda trait: trait.exclude_tags, reverse = True), key=lambda trait: trait.tier, reverse = True):
                            if not trait.researched and trait.has_required():
                                $ trait_tags = ""
                                if trait.exclude_tags:
                                    $ trait_tags = "\nExcludes Other: "
                                    for a_tag in trait.exclude_tags:
                                        $ trait_tags += "[[" + a_tag + "]"
                                $ trait_title = trait.name + " " + "(" +str(trait.current_research)+"/"+ str(trait.research_needed) + ")" + trait_tags
                                textbutton trait_title:
                                    text_xalign 0.5
                                    text_text_align 0.5
                                    text_size 14
                                    action [Hide("trait_tooltip"),Return(trait)] style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    hovered Show("trait_tooltip",None,trait)
                                    unhovered Hide("trait_tooltip")
                                    xsize 320

                viewport:
                    xsize 320
                    ysize 800
                    scrollbars "vertical"
                    mousewheel True
                    vbox:
                        xsize 320
                        text "Master Existing Traits:" style "menu_text_style" size 20 xanchor 0.5 xalign 0.5

                        for trait in sorted(sorted(list_of_traits, key = lambda trait: trait.exclude_tags, reverse = True), key=lambda trait: trait.tier, reverse = True):
                            if trait.researched:
                                $ trait_tags = ""
                                if trait.exclude_tags:
                                    $ trait_tags = "\nExcludes Other: "
                                    for a_tag in trait.exclude_tags:
                                        $ trait_tags += "[[" + a_tag + "]"
                                $ trait_title = trait.name + " " + "(" +str(trait.current_research)+"/"+ str(trait.research_needed) + ")" + trait_tags + "\nMastery Level: " + str(trait.mastery_level) + "\nSide Effect Chance: %" + str(trait.get_effective_side_effect_chance())
                                textbutton trait_title:
                                    text_xalign 0.5
                                    text_text_align 0.5
                                    text_size 14
                                    action [Hide("trait_tooltip"),Return(trait)] style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    hovered Show("trait_tooltip",None,trait)
                                    unhovered Hide("trait_tooltip")
                                    xsize 320


                viewport:
                    xsize 320
                    ysize 800
                    scrollbars "vertical"
                    mousewheel True
                    vbox:
                        xsize 320
                        text "Research New Designs:" style "menu_text_style" size 20 xanchor 0.5 xalign 0.5
                        for serum in mc.business.serum_designs:
                            if not serum.researched:
                                textbutton "[serum.name] ([serum.current_research]/[serum.research_needed])":
                                    text_xalign 0.5
                                    text_text_align 0.5
                                    text_size 14
                                    action [Hide("serum_tooltip"),Return(serum)] style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    hovered Show("serum_tooltip",None,serum)
                                    unhovered Hide("serum_tooltip")
                                    xsize 320

            textbutton "Do not change research." action Return("None") style "textbutton_style" text_style "textbutton_text_style" yalign 0.995 xanchor 0.5 xalign 0.5

    imagebutton:
        auto "/tutorial_images/restart_tutorial_%s.png"
        xsize 54
        ysize 54
        yanchor 1.0
        xalign 0.0
        yalign 1.0
        action Function(mc.business.reset_tutorial,"research_tutorial")

    $ research_tutorial_length = 5 #The number of  tutorial screens we have.
    if mc.business.event_triggers_dict["research_tutorial"] > 0 and mc.business.event_triggers_dict["research_tutorial"] <= research_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/research_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["research_tutorial"])+".png"
            hover "/tutorial_images/research_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["research_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"research_tutorial")

screen serum_production_select_ui:
    add "Science_Menu_Background.png"
    default line_selected = None
    default production_remaining = 100
    python:
        production_remaining = 100
        for key in mc.business.serum_production_array:
            production_remaining -= mc.business.serum_production_array[key][1] # How much of the 100% capability are we using?

    vbox:
        xalign 0.04
        yalign 0.04
        xsize 600
        yanchor 0.0
        frame:
            background "#999999"
            xsize 510
            text "Production Lines" style "menu_text_style" size 30 xalign 0.5
        frame:
            background "#999999"
            xsize 510
            text "Capacity Remaining: [production_remaining]%" style "menu_text_style"
        spacing 20
        for count in range(1,mc.business.production_lines+1): #For the non-programmers we index our lines to 1 through production_lines.
            frame:
                background "#999999"
                vbox:
                    $ name_string = ""
                    if count in mc.business.serum_production_array:
                        $ name_string = "Production Line " + str(count) + "\nCurrently Producing: " + mc.business.serum_production_array[count][0].name
                    else:
                        $ name_string = "Production Line " + str(count) + "\nCurrently Producing: Nothing"

                    $ button_background = "#000080"
                    if line_selected == count:
                        $ button_background = "#666666"

                    if count in mc.business.serum_production_array:
                        $ the_serum = mc.business.serum_production_array[count][0]
                        textbutton name_string action [SetScreenVariable("line_selected",count),Hide("serum_tooltip")] style "textbutton_style" text_style "textbutton_text_style" hovered Show("serum_tooltip",None,the_serum,0.94,0.072) unhovered Hide("serum_tooltip") background button_background xsize 500
                    else:
                        textbutton name_string action SetScreenVariable("line_selected",count) style "textbutton_style" text_style "textbutton_text_style" background button_background xsize 500

                    null height 20
                    hbox:
                        ysize 40
                        xsize 500
                        text "Production Weight: " style "menu_text_style" xalign 0.0
                        if count in mc.business.serum_production_array:
                            textbutton "-10%" action Function(mc.business.change_line_weight,count,-10) style "textbutton_style" text_style "textbutton_text_style" yanchor 0.25 tooltip "Work done by production employees will be split between active lines based on production weight."
                            text str(mc.business.serum_production_array[count][1]) + "%" style "menu_text_style"
                            textbutton "+10%" action Function(mc.business.change_line_weight,count,10) style "textbutton_style" text_style "textbutton_text_style" yanchor 0.25 tooltip "Work done by production employees will be split between active lines based on production weight."
                        else:
                            textbutton "-10%" action NullAction style "textbutton_style" text_style "textbutton_text_style" sensitive False yanchor 0.25 tooltip "Work done by production employees will be split between active lines based on production weight."
                            text "0%" style "menu_text_style"
                            textbutton "+10%" action NullAction style "textbutton_style" text_style "textbutton_text_style" sensitive False yanchor 0.25 tooltip "Work done by production employees will be split between active lines based on production weight."

                    hbox:
                        ysize 40
                        xsize 500
                        text "Auto-sell Threshold: " style "menu_text_style"
                        if count in mc.business.serum_production_array:
                            textbutton "-1" action Function(mc.business.change_line_autosell,count,-1) style "textbutton_style" text_style "textbutton_text_style" yanchor 0.25 tooltip "Doses of serum above the auto-sell threshold will automatically be flagged for sale and moved to the marketing department."
                            if mc.business.serum_production_array[count][3] < 0:
                                text "None" style "menu_text_style"
                            else:
                                text str(mc.business.serum_production_array[count][3]) style "menu_text_style"
                            textbutton "+1" action Function(mc.business.change_line_autosell,count,1) style "textbutton_style" text_style "textbutton_text_style"  yanchor 0.25 tooltip "Doses of serum above the auto-sell threshold will automatically be flagged for sale and moved to the marketing department."
                        else:
                            textbutton "-1" action NullAction style "textbutton_style" text_style "textbutton_text_style" sensitive False yanchor 0.25 tooltip "Doses of serum above the auto-sell threshold will automatically be flagged for sale and moved to the marketing department."
                            text "None" style "menu_text_style"
                            textbutton "+1" action NullAction style "textbutton_style" text_style "textbutton_text_style" sensitive False yanchor 0.25 tooltip "Doses of serum above the auto-sell threshold will automatically be flagged for sale and moved to the marketing department."

    if line_selected:
        frame:
            yanchor 0.0
            background "#999999"
            xalign 0.5
            yalign 0.04
            xsize 600
            vbox:
                text "Choose Production for Line [line_selected]" style "menu_text_style" size 30
                if len(mc.business.serum_designs) == 0:
                    frame:
                        xfill True
                        background "#000080"
                        text "No designs researched! Create and research a design in the R&D department first!" style "textbutton_text_style"
                else:
                    for a_serum in mc.business.serum_designs:
                        if a_serum.researched:
                            textbutton a_serum.name action [Hide("serum_tooltip"), Function(mc.business.change_production,a_serum,line_selected), SetScreenVariable("line_selected",None)] hovered Show("serum_tooltip",None,a_serum,0.94,0.072) unhovered Hide("serum_tooltip") style "textbutton_style" text_style "textbutton_text_style"

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return()
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

    imagebutton:
        auto "/tutorial_images/restart_tutorial_%s.png"
        xsize 54
        ysize 54
        yanchor 1.0
        xalign 0.0
        yalign 1.0
        action Function(mc.business.reset_tutorial,"production_tutorial")


    $ production_tutorial_length = 5 #The number of  tutorial screens we have.
    if mc.business.event_triggers_dict["production_tutorial"] > 0 and mc.business.event_triggers_dict["production_tutorial"] <= production_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/production_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["production_tutorial"])+".png"
            hover "/tutorial_images/production_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["production_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"production_tutorial")

screen serum_inventory_select_ui(the_inventory): #Used to let the player select a serum from an inventory.
    add "Science_Menu_Background.png"
    frame:
        background "#888888"
        xsize 400
        ysize 1000
        xalign 0.05
        yalign 0.05
        anchor (0.0,0.0)
        vbox:
            text "Serum Available" size 22 style "menu_text_style"
            for serum in the_inventory.serums_held:
                button:
                    background "#1a45a1aa"
                    xsize 380
                    ysize 80
                    action [Hide("serum_tooltip"),Return(serum[0])]
                    hovered Show("serum_tooltip",None,serum[0])
                    unhovered Hide("serum_tooltip")
                    text serum[0].name + " - " + str(serum[1]) + " Doses" style "menu_text_style" size 18 xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return("None")
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

#LIKELY NOT NEEDED
init -2 python:
    def colour_changed_r(new_value):
        if not new_value:
            new_value = 0

        try:
            new_value = float(new_value)
        except ValueError:
            new_value = 0

        if float(new_value) < 0:
            new_value = 0
        elif float(new_value) > 1:
            new_value = 1.0
        cs = renpy.current_screen()

        cs.scope["current_r"] = __builtin__.round(float(new_value),2)
        renpy.restart_interaction()

    def colour_changed_g(new_value):
        if not new_value:
            new_value = 0

        try:
            new_value = float(new_value)
        except ValueError:
            new_value = 0

        if float(new_value) < 0:
            new_value = 0
        elif float(new_value) > 1:
            new_value = 1.0
        cs = renpy.current_screen()

        cs.scope["current_g"] = __builtin__.round(float(new_value),2)
        renpy.restart_interaction()

    def colour_changed_b(new_value):
        if not new_value:
            new_value = 0

        try:
            new_value = float(new_value)
        except ValueError:
            new_value = 0

        if float(new_value) < 0:
            new_value = 0
        elif float(new_value) > 1:
            new_value = 1.0

        cs = renpy.current_screen()

        cs.scope["current_b"] = __builtin__.round(float(new_value),2)
        renpy.restart_interaction()

    def update_colour_palette(palette_index, new_r,new_g,new_b,new_a):
        persistent.colour_palette[palette_index] = [new_r,new_g,new_b,new_a]
        renpy.save_persistent()


screen outfit_creator(starting_outfit, outfit_type = "full"): ##Pass a completely blank outfit instance for a new outfit, or an already existing instance to load an old one.\
    add "Paper_Background.png"
    modal True
    zorder 100
    default catagory_selected = "Panties"

    default demo_outfit = starting_outfit.get_copy()

    if outfit_type == "under":
        $ valid_layers = [0,1]
    elif outfit_type == "over":
        $ valid_layers = [2,3]
    else:
        $ valid_layers = [0,1,2,3]

    $ valid_catagories = ["Panties", "Bras", "Pants", "Skirts", "Dresses", "Shirts", "Socks", "Shoes", "Facial", "Rings", "Bracelets", "Neckwear"] #Holds the valid list of catagories strings to be shown at the top.

    $ catagories_mapping = {
        "Panties": [panties_list, Outfit.can_add_lower, Outfit.add_lower],  #Maps each catagory to the function it should use to determine if it is valid and how it should be added to the outfit.
        "Bras": [bra_list, Outfit.can_add_upper, Outfit.add_upper],
        "Pants": [pants_list, Outfit.can_add_lower, Outfit.add_lower],
        "Skirts": [skirts_list, Outfit.can_add_lower, Outfit.add_lower],
        "Dresses": [dress_list, Outfit.can_add_dress, Outfit.add_dress],
        "Shirts": [shirts_list, Outfit.can_add_upper, Outfit.add_upper],
        "Socks": [socks_list, Outfit.can_add_feet, Outfit.add_feet],
        "Shoes": [shoes_list, Outfit.can_add_feet, Outfit.add_feet],
        "Facial": [earings_list, Outfit.can_add_accessory, Outfit.add_accessory],
        "Rings": [rings_list, Outfit.can_add_accessory, Outfit.add_accessory],
        "Bracelets": [bracelet_list, Outfit.can_add_accessory, Outfit.add_accessory],
        "Neckwear": [neckwear_list, Outfit.can_add_accessory, Outfit.add_accessory]}

    default bar_select = 0 # 0 is nothing selected, 1 is red, 2 is green, 3 is blue, and 4 is alpha

    default selected_colour = "colour" #If secondary we are alterning the patern colour. When changed it updates the colour of the clothing item. Current values are "colour" and "colour_pattern"
    default current_r = 1.0
    default current_g = 1.0
    default current_b = 1.0
    default current_a = 1.0

    default selected_clothing = None
    # $ current_colour = [1.0,1.0,1.0,1.0] #This is the colour we will apply to all of the clothing

    #Each catagory below has a click to enable button. If it's false, we don't show anything for it.
    #TODO: refactor this outfit creator to remove as much duplication as possible.

    hbox: #The main divider between the new item adder and the current outfit view.
        xpos 15
        yalign 0.5
        yanchor 0.5
        spacing 15
        frame:
            background "#aaaaaa"
            padding (20,20)
            xysize (880, 1015)
            hbox:
                spacing 15
                vbox: #Catagories select on far left
                    spacing 15
                    for catagory in valid_catagories:
                        textbutton catagory:
                            style "textbutton_style"
                            text_style "textbutton_text_style"
                            if catagory == catagory_selected:
                                background "#4f7ad6"
                                hover_background "#4f7ad6"
                            else:
                                background "#1a45a1"
                                hover_background "#3a65c1"
                            text_align(0.5,0.5)
                            text_anchor(0.5,0.5)
                            xysize (220, 60)
                            action [SetScreenVariable("catagory_selected",catagory), SetScreenVariable("selected_clothing", None), SetScreenVariable("selected_colour", "colour")] #Set the clothing to None when you change catagories to avoid breaking the clothing add function assignments
                vbox:
                    spacing 15
                    viewport:
                        ysize 480
                        xminimum 605
                        scrollbars "vertical"
                        mousewheel True
                        frame:
                            xsize 620
                            yminimum 480
                            background "#888888"
                            vbox:
                                #THIS IS WHERE ITEM CHOICES ARE SHOWN
                                if catagory_selected in catagories_mapping:
                                    $ valid_check = catagories_mapping[catagory_selected][1]
                                    $ apply_method = catagories_mapping[catagory_selected][2]
                                    $ cloth_list_length = len(catagories_mapping[catagory_selected][0])
                                    for cloth in catagories_mapping[catagory_selected][0]:
                                        textbutton cloth.name:
                                            style "textbutton_style"
                                            text_style "textbutton_text_style"
                                            if valid_check(starting_outfit, cloth):
                                                background "#1a45a1"
                                                hover_background "#3a65c1"
                                            else:
                                                background "#444444"
                                                hover_background "#444444"
                                            insensitive_background "#444444"
                                            xfill True
                                            sensitive valid_check(starting_outfit, cloth) and cloth.layer in valid_layers
                                            action [SetScreenVariable("selected_clothing", cloth), SetScreenVariable("selected_colour", "colour")]
                                            hovered Function(apply_method, demo_outfit, cloth)
                                            unhovered Function(demo_outfit.remove_clothing, cloth)

                    frame:
                        #THIS IS WHERE SELECTED ITEM OPTIONS ARE SHOWN
                        xysize (605, 480)
                        background "#888888"
                        vbox:
                            spacing 10
                            if selected_clothing is not None:
                                text selected_clothing.name + ", +" + __builtin__.str(selected_clothing.slut_value) + " Slut Requirement" style "textbutton_text_style"
                                if __builtin__.type(selected_clothing) is Clothing: #Only clothing items have patterns, facial accessories do not (currently).
                                    hbox:
                                        spacing 5
                                        for pattern in selected_clothing.supported_patterns:
                                            textbutton pattern:
                                                style "textbutton_style"
                                                text_style "textbutton_text_style"
                                                if selected_clothing.pattern == selected_clothing.supported_patterns[pattern]:
                                                    background "#4f7ad6"
                                                    hover_background "#4f7ad6"
                                                else:
                                                    background "#1a45a1"
                                                    hover_background "#3a65c1"
                                                xfill False
                                                xsize 120
                                                text_xalign 0.5
                                                text_xanchor 0.5
                                                text_size 12
                                                sensitive True
                                                action SetField(selected_clothing,"pattern",selected_clothing.supported_patterns[pattern])

                                hbox:
                                    spacing -5 #We will manually handle spacing so we can have our colour predictor frames
                                    textbutton "Primary Colour":
                                        style "textbutton_style"
                                        text_style "textbutton_text_style"
                                        text_size 12
                                        xsize 120
                                        if selected_colour == "colour":
                                            background "#4f7ad6"
                                            hover_background "#4f7ad6"
                                        else:
                                            background "#1a45a1"
                                            hover_background "#3a65c1"
                                        sensitive True
                                        if selected_colour == "colour_pattern":
                                            action [SetField(selected_clothing,"colour_pattern",[current_r,current_g,current_b,current_a]), SetScreenVariable("selected_colour","colour"), SetScreenVariable("current_r",selected_clothing.colour[0]), SetScreenVariable("current_g",selected_clothing.colour[1]), SetScreenVariable("current_b",selected_clothing.colour[2]), SetScreenVariable("current_a",selected_clothing.colour[3])]
                                        else:
                                            action NullAction()

                                    frame:
                                        if selected_colour == "colour":
                                            background Color(rgb=(current_r,current_g,current_b,current_a))
                                        else:
                                            background Color(rgb=(selected_clothing.colour[0], selected_clothing.colour[1], selected_clothing.colour[2]))
                                        xysize (45,45)
                                        yanchor 0.5
                                        yalign 0.5

                                    if __builtin__.type(selected_clothing) is Clothing and selected_clothing.pattern is not None:
                                        null width 15
                                        textbutton "Pattern Colour":
                                            style "textbutton_style"
                                            text_style "textbutton_text_style"
                                            text_size 12
                                            xsize 120
                                            if selected_colour == "colour_pattern":
                                                background "#4f7ad6"
                                                hover_background "#4f7ad6"
                                            else:
                                                background "#1a45a1"
                                                hover_background "#3a65c1"
                                            sensitive True
                                            if selected_colour == "colour":
                                                action [SetField(selected_clothing,"colour",[current_r,current_g,current_b,current_a]), SetScreenVariable("selected_colour","colour_pattern"), SetScreenVariable("current_r",selected_clothing.colour_pattern[0]), SetScreenVariable("current_g",selected_clothing.colour_pattern[1]), SetScreenVariable("current_b",selected_clothing.colour_pattern[2]), SetScreenVariable("current_a",selected_clothing.colour_pattern[3])]
                                            else:
                                                action NullAction()
                                        frame:
                                            if selected_colour == "colour_pattern":
                                                background Color(rgb=(current_r,current_g,current_b,current_a))
                                            else:
                                                background Color(rgb=(selected_clothing.colour_pattern[0], selected_clothing.colour_pattern[1], selected_clothing.colour_pattern[2]))
                                            xysize (45,45)
                                            yanchor 0.5
                                            yalign 0.5

                                hbox:
                                    spacing 10
                                    vbox:
                                        text "Red" style "textbutton_text_style"
                                        hbox:
                                            if bar_select == 1:
                                                frame:
                                                    input default current_r length 4 changed colour_changed_r allow ".0123456789" style "menu_text_style"
                                                    xsize 70
                                                    ysize 50
                                            else:
                                                button:
                                                    background "#888888"
                                                    action SetScreenVariable("bar_select",1)
                                                    text "%.2f" % current_r style "menu_text_style"
                                                    xsize 70
                                                    ysize 50

                                            bar value ScreenVariableValue("current_r", 1.0) xsize 120 ysize 45 style style.slider unhovered SetScreenVariable("current_r",__builtin__.round(current_r,2))
                                    vbox:
                                        text "Green" style "textbutton_text_style"
                                        hbox:
                                            if bar_select == 2:
                                                frame:
                                                    input default current_g length 4 changed colour_changed_g allow ".0123456789" style "menu_text_style"
                                                    xsize 70
                                                    ysize 50
                                            else:
                                                button:
                                                    background "#888888"
                                                    action SetScreenVariable("bar_select",2)
                                                    text "%.2f" % current_g style "menu_text_style"
                                                    xsize 70
                                                    ysize 50

                                            bar value ScreenVariableValue("current_g", 1.0) xsize 120 ysize 45 style style.slider unhovered SetScreenVariable("current_g",__builtin__.round(current_g,2))
                                    vbox:
                                        text "Blue" style "textbutton_text_style"
                                        hbox:
                                            if bar_select == 3:
                                                frame:
                                                    input default current_b length 4 changed colour_changed_b allow ".0123456789" style "menu_text_style"
                                                    xsize 70
                                                    ysize 50
                                            else:
                                                button:
                                                    background "#888888"
                                                    action SetScreenVariable("bar_select",3)
                                                    text "%.2f" % current_b style "menu_text_style"
                                                    xsize 70
                                                    ysize 50

                                            bar value ScreenVariableValue("current_b", 1.0) xsize 120 ysize 45 style style.slider unhovered SetScreenVariable("current_b",__builtin__.round(current_b,2))

                                text "Transparency: " style "menu_text_style"
                                hbox:
                                    spacing 20
                                    button:
                                        if current_a == 1.0:
                                            background "#4f7ad6"
                                        else:
                                            background "#1a45a1"
                                        text "Normal" style "menu_text_style" xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5
                                        xysize (120, 40)
                                        action SetScreenVariable("current_a", 1.0)

                                    button:
                                        if current_a == 0.95:
                                            background "#4f7ad6"
                                        else:
                                            background "#1a45a1"
                                        text "Sheer" style "menu_text_style" xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5
                                        xysize (120, 40)
                                        action SetScreenVariable("current_a", 0.95)

                                    button:
                                        if current_a == 0.8:
                                            background "#4f7ad6"
                                        else:
                                            background "#1a45a1"
                                        text "Translucent" style "menu_text_style" xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5
                                        xysize (120, 40)
                                        action SetScreenVariable("current_a", 0.8)

                                                        #[SetField(cloth,"colour",[current_r,current_g,current_b,current_a]), Function(apply_method, demo_outfit, cloth)]

                                hbox:
                                    spacing 5
                                    xalign 0.5
                                    xanchor 0.5
                                    for count, a_colour in __builtin__.enumerate(persistent.colour_palette):
                                        frame:
                                            background "#aaaaaa"
                                            button:
                                                background Color(rgb=(a_colour[0], a_colour[1], a_colour[2]))
                                                xysize (40,40)
                                                sensitive True
                                                action [SetScreenVariable("current_r", a_colour[0]), SetScreenVariable("current_g", a_colour[1]), SetScreenVariable("current_b", a_colour[2]), SetScreenVariable("current_a", a_colour[3])]
                                                alternate Function(update_colour_palette, count, current_r, current_g, current_b, current_a)



                        #TODO: Change this "Add" butotn to "Remove" when you're selecting something that is arleady part of the outfit.
                        if selected_clothing:
                            textbutton "Add to Outfit":
                                style "textbutton_style"
                                text_style "textbutton_text_style"
                                background "#1a45a1"
                                hover_background "#3a65c1"
                                xalign 0.5
                                yalign 1.0
                                xanchor 0.5
                                yanchor 1.0
                                sensitive valid_check(starting_outfit, selected_clothing)
                                action [SetField(selected_clothing, selected_colour,[current_r,current_g,current_b,current_a]), Function(apply_method, starting_outfit, selected_clothing)]
                                hovered [SetField(selected_clothing, selected_colour,[current_r,current_g,current_b,current_a]), Function(apply_method, demo_outfit, selected_clothing)]
                                unhovered Function(demo_outfit.remove_clothing, selected_clothing)




            # vbox: #Items selector
            #     #W/ item customixing window at bottom
            #
        vbox:
            spacing 15
            frame:
                xysize (440, 500)
                background "#aaaaaa"
                padding (20,20)
                vbox:
                    spacing 15
                    text "Current Items" style "textbutton_text_style"
                    frame:
                        xfill True
                        yfill True
                        background "#888888"
                        vbox:
                            spacing 5 #TODO: Add a viewport here too.
                            for cloth in starting_outfit.upper_body + starting_outfit.lower_body + starting_outfit.feet + starting_outfit.accessories:
                                if not cloth.is_extension: #Don't list extensions for removal.
                                    button:
                                        background Color(rgb = (cloth.colour[0], cloth.colour[1], cloth.colour[2]))
                                        xysize (380, 40)
                                        action [Function(starting_outfit.remove_clothing, cloth),Function(demo_outfit.remove_clothing, cloth)]
                                        xalign 0.5
                                        yalign 0.0
                                        text cloth.name xalign 0.5 xanchor 0.5 yalign 0.5 yanchor 0.5 style "outfit_style"

            frame:
                background "#aaaaaa"
                xysize (440, 500)
                padding (20,20)
                vbox:
                    yalign 0.0
                    text "Outfit Stats" style "menu_text_style" size 20
                    text "Sluttiness (Full Outfit) : " + str(demo_outfit.slut_requirement) style "menu_text_style"
                    if demo_outfit.is_suitable_underwear_set():
                        text "Sluttiness (Underwear): " + str(demo_outfit.get_underwear_slut_score()) style "menu_text_style"
                    else:
                        text "Sluttiness (Underwear): Invalid" style "menu_text_style"

                    if demo_outfit.is_suitable_overwear_set():
                        text "Sluttiness (Overwear): " + str(demo_outfit.get_overwear_slut_score()) style "menu_text_style"
                    else:
                        text "Sluttiness (Overwear): Invalid" style "menu_text_style"
                    text "Tits Visible: " + str(demo_outfit.tits_visible()) style "menu_text_style"
                    text "Tits Usable: " + str(demo_outfit.tits_available()) style "menu_text_style"
                    text "Wearing a Bra: " + str(demo_outfit.wearing_bra()) style "menu_text_style"
                    text "Bra Covered: " + str(demo_outfit.bra_covered()) style "menu_text_style"
                    text "Pussy Visible: " + str(demo_outfit.vagina_visible()) style "menu_text_style"
                    text "Pussy Usable: " + str(demo_outfit.vagina_available()) style "menu_text_style"
                    text "Wearing Panties: " + str(demo_outfit.wearing_panties()) style "menu_text_style"
                    text "Panties Covered: " + str(demo_outfit.panties_covered()) style "menu_text_style"

                    hbox:
                        yalign 1.0
                        xalign 0.5
                        xanchor 0.5
                        spacing 50
                        textbutton "Save Outfit" action Return(starting_outfit.get_copy()) style "textbutton_style" text_style "textbutton_text_style" text_text_align 0.5 text_xalign 0.5 xysize (155,80)
                        textbutton "Abandon Design" action Return("Not_New") style "textbutton_style" text_style "textbutton_text_style" text_text_align 0.5 text_xalign 0.5 xysize (185,80)

    fixed: #TODO: Move this to it's own screen so it can be shown anywhere
        pos (1450,0)

        add mannequin_average
        for cloth in demo_outfit.generate_draw_list(None,"stand3"):
            add cloth

    imagebutton:
        auto "/tutorial_images/restart_tutorial_%s.png"
        xsize 54
        ysize 54
        yanchor 1.0
        xanchor 1.0
        xalign 1.0
        yalign 1.0
        action Function(mc.business.reset_tutorial,"outfit_tutorial")


    $ outfit_tutorial_length = 8 #The number of  tutorial screens we have.
    if mc.business.event_triggers_dict["outfit_tutorial"] > 0 and mc.business.event_triggers_dict["outfit_tutorial"] <= outfit_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/outfit_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["outfit_tutorial"])+".png"
            hover "/tutorial_images/outfit_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["outfit_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"outfit_tutorial")

style outfit_description_style is textbutton_text_style:
    size 14

screen outfit_delete_manager(the_wardrobe): ##Allows removal of outfits from players saved outfits.
    add "Paper_Background.png"
    modal True
    zorder 100
    default preview_outfit = None
    hbox:
        spacing 20
        xalign 0.1
        yalign 0.1
        frame:
            background "#888888"
            xsize 450
            ysize 750
            viewport:
                scrollbars "vertical"
                xsize 450
                ysize 750
                mousewheel True
                vbox:
                    text "Full Outfits" style "menu_text_style" size 30
                    for outfit in the_wardrobe.get_outfit_list():
                        textbutton "Delete "+outfit.name+ "\n(Sluttiness " +str(outfit.slut_requirement) +")" action Function(the_wardrobe.remove_outfit,outfit) hovered SetScreenVariable("preview_outfit", outfit.get_copy()) unhovered SetScreenVariable("preview_outfit", None) style "textbutton_style" text_style "outfit_description_style" xsize 210

        frame:
            background "#888888"
            xsize 450
            ysize 750
            viewport:
                scrollbars "vertical"
                xsize 450
                ysize 750
                mousewheel True
                vbox:
                    text "Overwear Sets" style "menu_text_style" size 30
                    for outfit in the_wardrobe.get_overwear_sets_list():
                        textbutton "Delete "+outfit.name+ "\n(Sluttiness " +str(outfit.get_overwear_slut_score()) +")" action Function(the_wardrobe.remove_outfit,outfit) hovered SetScreenVariable("preview_outfit", outfit.get_copy()) unhovered SetScreenVariable("preview_outfit", None) style "textbutton_style" text_style "outfit_description_style" xsize 210

        frame:
            background "#888888"
            xsize 450
            ysize 750
            viewport:
                scrollbars "vertical"
                xsize 450
                ysize 750
                mousewheel True
                vbox:
                    text "Underwear Sets" style "menu_text_style" size 30
                    for outfit in the_wardrobe.get_underwear_sets_list():
                        textbutton "Delete "+outfit.name+ "\n(Sluttiness " +str(outfit.get_underwear_slut_score()) +")" action Function(the_wardrobe.remove_outfit,outfit) hovered SetScreenVariable("preview_outfit", outfit.get_copy()) unhovered SetScreenVariable("preview_outfit", None) style "textbutton_style" text_style "outfit_description_style" xsize 210


    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return("No Return")
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

    fixed:
        pos (1450,0)
        add mannequin_average
        if preview_outfit:
            for cloth in preview_outfit.generate_draw_list(None,"stand3"):
                add cloth

screen outfit_select_manager(slut_limit = 999, show_outfits = True, show_overwear = True, show_underwear = True, main_selectable = True, show_make_new = False, show_export = False, show_modify = False, show_duplicate = False, show_delete = False):
    #If sluttiness_limit is passed, you cannot exit the creator until the proposed outfit has a sluttiness below it (or you create nothing).
    add "Paper_Background.png"
    modal True
    zorder 100
    default preview_outfit = None

    $ outfit_info_array = []
    ## ["Catagory name", is_catagory_enabled, "return value when new is made", slut score calculation field/function, "export field type", add_outfit_to_wardrobe_function] ##
    $ outfit_info_array.append([show_outfits, "Full Outfit", "new_full", Outfit.get_slut_requirement , "FullSets", Wardrobe.add_outfit, Wardrobe.get_outfit_list])
    $ outfit_info_array.append([show_overwear, "Overwear Set", "new_over", Outfit.get_overwear_slut_score, "OverwearSets",  Wardrobe.add_overwear_set, Wardrobe.get_overwear_sets_list])
    $ outfit_info_array.append([show_underwear, "Underwear Set", "new_under", Outfit.get_underwear_slut_score, "UnderwearSets", Wardrobe.add_underwear_set, Wardrobe.get_underwear_sets_list])

    hbox:
        spacing 20
        xalign 0.1
        yalign 0.1
        for catagory_info in outfit_info_array:
            if catagory_info[0]:
                frame:
                    background "#888888"
                    xsize 450
                    ysize 850
                    viewport:
                        scrollbars "vertical"
                        xsize 450
                        ysize 850
                        mousewheel True
                        vbox:
                            spacing -10
                            text catagory_info[1] + "s" style "menu_text_style" size 30 #Add an s to make it plural so we can reuse the field in the new button. Yep, I'm that clever-lazy.
                            null height 10
                            if show_make_new:
                                textbutton "Create New " + catagory_info[1]:
                                    action Return(catagory_info[2])
                                    sensitive True
                                    style "textbutton_style"
                                    text_style "outfit_description_style"
                                    xsize 450

                                null height 35

                            for outfit in catagory_info[6](mc.designed_wardrobe):
                                textbutton outfit.name + " (Sluttiness " +str(catagory_info[3](outfit)) +")":
                                    action Return(outfit.get_copy())
                                    sensitive (catagory_info[3](outfit) <= slut_limit) and main_selectable
                                    hovered SetScreenVariable("preview_outfit", outfit.get_copy())
                                    unhovered SetScreenVariable("preview_outfit", None)
                                    style "textbutton_style"
                                    text_style "outfit_description_style"
                                    tooltip "Pick this outfit."
                                    xsize 450

                                if show_export or show_modify or show_duplicate or show_delete:
                                    hbox:
                                        spacing 0
                                        xsize 450
                                        if show_export:
                                            default exported = []
                                            textbutton "Export":
                                                action [Function(exported.append,outfit), Function(log_outfit, outfit, outfit_class = catagory_info[4], wardrobe_name = "Exported_Wardrobe"), Function(renpy.notify, "Outfit exported to Exported_Wardrobe.xml")]
                                                sensitive outfit not in exported
                                                hovered SetScreenVariable("preview_outfit", outfit.get_copy())
                                                unhovered SetScreenVariable("preview_outfit", None)
                                                style "textbutton_style"
                                                text_style "outfit_description_style"
                                                tooltip "Export this outfit. The export will be added as an xml section in game/wardrobes/Exported_Wardrobe.xml."
                                                xsize 100

                                        if show_modify:
                                            textbutton "Modify":
                                                action Return(outfit) #If we are modifying an outfit just return it. outfit management loop will find which catagory it is in.
                                                sensitive (catagory_info[3](outfit) <= slut_limit)
                                                hovered SetScreenVariable("preview_outfit", outfit.get_copy())
                                                unhovered SetScreenVariable("preview_outfit", None)
                                                style "textbutton_style"
                                                text_style "outfit_description_style"
                                                tooltip "Modify this outfit."
                                                xsize 100

                                        if show_duplicate:
                                            $ the_copied_outfit = outfit.get_copy() #We make a copy to add to the wardrobe if this is selected. Otherwise continues same as "Modify"
                                            textbutton "Duplicate":
                                                action [Function(catagory_info[5], mc.designed_wardrobe, the_copied_outfit), Return(the_copied_outfit)]
                                                sensitive (catagory_info[3](outfit) <= slut_limit)
                                                hovered SetScreenVariable("preview_outfit", outfit.get_copy())
                                                unhovered SetScreenVariable("preview_outfit", None)
                                                style "textbutton_style"
                                                text_style "outfit_description_style"
                                                tooltip "Duplicate this outfit and edit the copy, leaving the original as it is."
                                                xsize 100

                                        if show_delete:
                                            textbutton "Delete":
                                                action Function(mc.designed_wardrobe.remove_outfit, outfit)
                                                sensitive (catagory_info[3](outfit) <= slut_limit)
                                                hovered SetScreenVariable("preview_outfit", outfit.get_copy())
                                                unhovered SetScreenVariable("preview_outfit", None)
                                                style "textbutton_style"
                                                text_style "outfit_description_style"
                                                tooltip "Remove this outfit from your wardrobe. This cannot be undone!"
                                                xsize 100

                                    null height 20

                                null height 25

    frame:
        background None
        anchor [0.5,0.5]
        align [0.39,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return("No Return")
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

    fixed:
        pos (1450,0)
        add mannequin_average
        if preview_outfit:
            for cloth in preview_outfit.generate_draw_list(None,"stand3"):
                add cloth

screen girl_outfit_select_manager(the_wardrobe, show_sets = False): ##Brings up a list of outfits currently in a girls wardrobe.
    add "Paper_Background.png"
    modal True
    zorder 100
    default preview_outfit = None

    hbox:
        xalign 0.1
        yalign 0.1
        spacing 20
        frame:
            background "#888888"
            xsize 450
            ysize 750
            viewport:
                scrollbars "vertical"
                xsize 450
                ysize 750
                mousewheel True
                vbox:
                    text "Full Outfits" style "menu_text_style" size 30
                    for outfit in the_wardrobe.get_outfit_list():
                        textbutton "Select "+outfit.name+ "\n(Sluttiness " +str(outfit.slut_requirement) +")" action Return(outfit) hovered SetScreenVariable("preview_outfit", outfit.get_copy()) unhovered SetScreenVariable("preview_outfit", None) style "textbutton_style" text_style "outfit_description_style" xsize 210

        if show_sets:
            frame:
                background "#888888"
                xsize 450
                ysize 750
                viewport:
                    scrollbars "vertical"
                    xsize 450
                    ysize 750
                    mousewheel True
                    vbox:
                        text "Overwear Sets" style "menu_text_style" size 30
                        for outfit in the_wardrobe.get_overwear_sets_list():
                            textbutton "Select "+outfit.name+ "\n(Sluttiness " +str(outfit.get_overwear_slut_score()) +")" action Return(outfit) hovered SetScreenVariable("preview_outfit", outfit.get_copy()) unhovered SetScreenVariable("preview_outfit", None) style "textbutton_style" text_style "outfit_description_style" xsize 210

            frame:
                background "#888888"
                xsize 450
                ysize 750
                viewport:
                    scrollbars "vertical"
                    xsize 450
                    ysize 750
                    mousewheel True
                    vbox:
                        text "Underwear Sets" style "menu_text_style" size 30
                        for outfit in the_wardrobe.get_underwear_sets_list():
                            textbutton "Select "+outfit.name+ "\n(Sluttiness " +str(outfit.get_underwear_slut_score()) +")" action Return(outfit) hovered SetScreenVariable("preview_outfit", outfit.get_copy()) unhovered SetScreenVariable("preview_outfit", None) style "textbutton_style" text_style "outfit_description_style" xsize 210

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return("None")
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

    fixed:
        pos (1450,0)
        add mannequin_average
        if preview_outfit:
            for cloth in preview_outfit.generate_draw_list(None,"stand3"):
                add cloth

screen map_manager():
    add "Paper_Background.png"
    modal True
    zorder 100

    $ x_size_percent = 0.07
    $ y_size_percent = 0.145

    for place in list_of_places: #Draw the text buttons over the background
        if place.visible:
            $ hex_x = x_size_percent * place.map_pos[0]
            $ hex_y = y_size_percent * place.map_pos[1]
            if place.map_pos[0] % 2 == 1:
                $ hex_y += y_size_percent/2
            if not place == mc.location:
                frame:
                    background None
                    xysize [171,150]
                    anchor [0.0,0.0]
                    align (hex_x,hex_y)
                    imagebutton:
                        anchor [0.5,0.5]
                        auto "gui/LR2_Hex_Button_%s.png"
                        focus_mask "gui/LR2_Hex_Button_idle.png"
                        action Function(mc.change_location,place)
                        sensitive place.accessable #TODO: replace once we want limited travel again with: place in mc.location.connections
                    text place.formalName + "\n(" + str(len(place.people)) + ")" anchor [0.5,0.5] style "map_text_style"

            else:
                frame:
                    background None
                    xysize [171,150]
                    anchor [0.0,0.0]
                    align (hex_x,hex_y)
                    imagebutton:
                        anchor [0.5,0.5]
                        idle "gui/LR2_Hex_Button_Alt_idle.png"
                        focus_mask "gui/LR2_Hex_Button_Alt_idle.png"
                        action Function(mc.change_location,place)
                        sensitive False
                    text place.formalName + "\n(" + str(len(place.people)) + ")" anchor [0.5,0.5] style "map_text_style"

        ##TODO: add a sub map to housing_map_manager() so we can go to people's homes

    $ xy_pos = [7,4]
    $ hex_x = x_size_percent * xy_pos[0]
    $ hex_y = y_size_percent * xy_pos[1]
    if xy_pos[0] % 2 == 1:
        $ hex_y += y_size_percent/2

    if mc.location in mc.known_home_locations:
        frame:
            background None
            xysize [171,150]
            anchor [0.0,0.0]
            align (hex_x,hex_y)
            imagebutton:
                anchor [0.5,0.5]
                idle "gui/LR2_Hex_Button_Alt_idle.png"
                focus_mask "gui/LR2_Hex_Button_Alt_idle.png"
                action Show("housing_map_manager")
                sensitive len(mc.known_home_locations) > 0
            text "Visit Someone..." anchor [0.5,0.5] style "map_text_style"
    else:
        frame:
            background None
            xysize [171,150]
            anchor [0.0,0.0]
            align (hex_x, hex_y)
            imagebutton:
                anchor [0.5,0.5]
                auto "gui/LR2_Hex_Button_%s.png"
                focus_mask "gui/LR2_Hex_Button_idle.png"
                action Show("housing_map_manager")
                sensitive len(mc.known_home_locations) > 0
            text "Visit Someone..." anchor [0.5,0.5] style "map_text_style"

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return(mc.location)
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

screen housing_map_manager():
    modal True
    zorder 101
    add "Paper_Background.png"
    # $ num_of_places = __builtin__.len(mc.known_home_locations) Should be irrelevant, removed 16/5/19
    $ places_so_far = 0
    $ x_offset_per_place = 0.1
    for place in mc.known_home_locations:
        if not place == mc.location and not place.hide_in_known_house_map:
            frame:
                background None
                xysize [171,150]
                anchor [0.0,0.0]
                align [0.1+(x_offset_per_place*places_so_far),0.5]
                #align place.map_pos #TODO arange this properly
                imagebutton:
                    anchor [0.5,0.5]
                    auto "gui/LR2_Hex_Button_%s.png"
                    focus_mask "gui/LR2_Hex_Button_idle.png"
                    action Function(mc.change_location,place)
                    sensitive place.accessable
                text place.formalName + "\n(" + str(len(place.people)) + ")" anchor [0.5,0.5] style "map_text_style"

        else:
            frame:
                background None
                xysize [171,150]
                anchor [0.0,0.0]
                align [0.1+(x_offset_per_place*places_so_far),0.5]
                imagebutton:
                    anchor [0.5,0.5]
                    idle "gui/LR2_Hex_Button_Alt_idle.png"
                    focus_mask "gui/LR2_Hex_Button_Alt_idle.png"
                    action Function(mc.change_location,place)
                    sensitive False
                text place.formalName + "\n(" + str(len(place.people)) + ")" anchor [0.5,0.5] style "map_text_style"
        $ places_so_far += 1

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action [Hide("housing_map_manager"), Return(mc.location)]
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"


init -2 python:
    def purchase_policy(the_policy):
        the_policy.buy_policy()
        mc.business.policy_list.append(the_policy)

init -2 screen policy_selection_screen():
    add "Paper_Background.png"
    modal True
    zorder 100
    $ tooltip = GetTooltip()
    $ catagories = [["Uniform Policies",uniform_policies_list], ["Recruitment Policies",recruitment_policies_list], ["Serum Policies",serum_policies_list], ["Organisation Policies",organisation_policies_list]]
    default selected_catagory = catagories[0] #Default to the first in our catagories list
    vbox:
        xalign 0.5
        yalign 0.15
        spacing 30
        frame: #Top frame holding the policy catagories that we have.
            xsize 1320
            ysize 140
            background "#1a45a1aa"
            vbox:
                text "Policy Catagories" style "menu_text_style" size 26 yalign 0.5 yanchor 0.5 xalign 0.5 xanchor 0.5
                hbox:
                    spacing 35
                    xalign 0.5
                    xanchor 0.5
                    for catagory in catagories:
                        textbutton catagory[0]:
                            xsize 300
                            ysize 80
                            action SetScreenVariable("selected_catagory", catagory)
                            sensitive selected_catagory != catagory
                            style "textbutton_style"
                            text_style "textbutton_text_style"

        frame: #Holds the list of business policies. Needs to be scrollable.
            xsize 1320
            ysize 650
            background "#1a45a1aa"
            viewport:
                mousewheel True
                scrollbars "vertical"
                xsize 800
                ysize 650
                vbox:
                    spacing 10
                    for policy in selected_catagory[1]:
                        if policy.is_owned():
                            textbutton "$" + str(policy.cost) + " - " + policy.name:
                                tooltip policy.desc
                                action NullAction()
                                style "textbutton_style"
                                text_style "textbutton_text_style"
                                background "#59853f"
                                hover_background "#78b156"
                                sensitive True
                                xsize 800
                                ysize 100
                        else:
                            if policy.requirement() and (policy.cost < mc.business.funds or policy.cost == mc.business.funds):
                                textbutton "$" + str(policy.cost) + " - " + policy.name:
                                    tooltip policy.desc
                                    style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    action Function(purchase_policy,policy)
                                    sensitive policy.requirement() and (policy.cost < mc.business.funds or policy.cost == mc.business.funds)
                                    xsize 800
                                    ysize 100
                            else:
                                textbutton "$" + str(policy.cost) + " - " + policy.name:
                                    tooltip policy.desc
                                    style "textbutton_style"
                                    text_style "textbutton_text_style"
                                    background "#666666"
                                    action NullAction()
                                    sensitive True
                                    xsize 800
                                    ysize 100


    if tooltip:
        frame:
            background "#1a45a1aa"
            anchor [1.0,0.0]
            align [0.84,0.2]
            xsize 500
            text tooltip style "menu_text_style"

    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return()
        textbutton "Return" align [0.5,0.5] text_style "return_button_style"

    imagebutton:
        auto "/tutorial_images/restart_tutorial_%s.png"
        xsize 54
        ysize 54
        yanchor 1.0
        xalign 0.0
        yalign 1.0
        action Function(mc.business.reset_tutorial,"policy_tutorial")

    $ policy_tutorial_length = 4 #The number of  tutorial screens we have.
    if mc.business.event_triggers_dict["policy_tutorial"] > 0 and mc.business.event_triggers_dict["policy_tutorial"] <= policy_tutorial_length: #We use negative numbers to symbolize the tutorial not being enabled
        imagebutton:
            auto
            sensitive True
            xsize 1920
            ysize 1080
            idle "/tutorial_images/policy_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["policy_tutorial"])+".png"
            hover "/tutorial_images/policy_tutorial_"+__builtin__.str(mc.business.event_triggers_dict["policy_tutorial"])+".png"
            action Function(mc.business.advance_tutorial,"policy_tutorial")


init -2 style return_button_style:
    text_align 0.5
    size 30
    italic True
    bold True
    color "#dddddd"
    outlines [(2,"#222222",0,0)]

init -2 style map_text_style:
    text_align 0.5
    size 14
    italic True
    bold True
    color "#dddddd"
    outlines [(2,"#222222",0,0)]

init -2 style map_frame_style:
    background "#094691"

init -2 style map_frame_blue_style:
    background "#5fa7ff"

init -2 style map_frame_grey_style:
    background "#222222"

transform float_up:
    subpixel True #Experimental, might have performance impact.
    xalign 0.92
    yalign 1.0
    alpha 1.0
    ease 1.0 yalign 0.4
    easeout 2.0 alpha 0.0

style float_text:
    size 30
    italic True
    bold True
    outlines [(2,"#222222",0,0)]

style float_text_pink is float_text:
    color "#FFB6C1"

style float_text_red is float_text:
    color "B22222"

style float_text_grey is float_text:
    color "696969"

style float_text_green is float_text:
    color "228B22"

style float_text_yellow is float_text:
    color "D2691E"

style float_text_blue is float_text:
    color "483D8B"

# screen float_up_screen (text_array, style_array): #text_array is a list of the text to be displayed on each line, style_array is the list of corisponding styles to be used for that text.
#     vbox at float_up:
#         xanchor 0.5
#         for index, update_text in enumerate(text_array):
#             text update_text style style_array[index]
#     timer 3.0 action Hide("float_up_screen") #Hide this screen after 3 seconds, so it can be called again by something else.

label start:
    scene bg paper_menu_background with fade
    "Lab Rats 2 contains adult content. If you are not over 18 or your contries equivalent age you should not view this content."
    menu:
        "I am over 18.":
            "Excellent, let's continue then."

        "I am not over 18.":
            $renpy.full_restart()

    "Vren" "v0.18.2 represents an early iteration of Lab Rats 2. Expect to run into limited content, unexplained features, and unbalanced game mechanics."
    "Vren" "Would you like to view the FAQ?"
    menu:
        "View the FAQ.":
            call faq_loop from _call_faq_loop
        "Get on with the game!":
            "You can access the FAQ from your bedroom at any time."

    $ renpy.block_rollback()
    call screen character_create_screen()
    $ return_arrays = _return #These are the stat, skill, and sex arrays returned from the character creator.
    call create_test_variables(store.name,store.b_name,store.l_name,return_arrays[0],return_arrays[1],return_arrays[2]) from _call_create_test_variables ##Moving some of this to an init block (init 1specifically) would let this play better with updates in the future.
    $ renpy.block_rollback()
    menu:
        "Play introduction and tutorial.":
            call tutorial_start from _call_tutorial_start

        "Skip introduction and tutorial.":
            $ mc.business.event_triggers_dict["Tutorial_Section"] = False
    jump normal_start

label tutorial_start:
    menu:
        "I have played Lab Rats 1 Before.":
            "It has been a year since the end of your summer job at the university lab."



        "I am new to Lab Rats.":
            "A year ago you were a chemical engineering student, getting ready to graduate soon and looking for something to do over the summer."
            "You ended up with a summer job on campus as a lab assistant working with a two person team."
            "Your lab director, Nora, and her long time lab assistant Stephanie were investigating the properties of a new lab created molecule."
            "It didn't take long before you discovered it could be used to deliver mind altering agents. You spent the summer creating doses of \"serum\" in secret."
            "It has been a year since the end of your summer job at the university lab."

    "Your experimentation with the inhibition removing serum was fun, but in the end the effects were temporary."
    "The end of the summer also meant the end of your access to the serum making supplies."
    "Little by litle the women slid back into into their previous lives."

    scene
    $ renpy.show(bedroom.name,what=bedroom.background_image) #Start our story at home.

    "Four months ago you graduated from university with a degree in chemical engineering."
    "Since then you have been living at home and sending out resumes. You have had several interviews, but no job offers yet."
    "Today you have have an interview with a small pharmacutical company. You've gotten up early and dressed in your finest suit."
    $renpy.show(hall.name, what=hall.background_image)
    "You head for the front door, eager to get to your interview early."
    mom.title "[mom.mc_title], are you leaving already?"
    "[mom.possessive_title]'s voice comes from the kitchen, along with the smell of breakfast."
    mc.name "Yeah, I want make sure I make it on time."
    mom.title "You haven't had any breakfast yet. You should eat, I'll drive you if you're running late."
    "The smell of cooked toast and frying eggs wins you over and you head to the kitchen."
    $ renpy.show(kitchen.name, what=kitchen.background_image)
    $ mom.draw_person(emotion = "happy", position = "back_peek")
    "[mom.possessive_title] is at the stove and looks back at you when you come into the room."
    mom.title "The food's almost ready. Just take a seat and I'll make you a plate."
    mc.name "Thanks Mom, I didn't realize how hungry I was. Nerves, I guess."
    mom.title "Don't worry, I'm sure they'll love you."
    "She turns back and focuses her attention on her cooking. A few minutes later she presents you with a plate."
    $ mom.draw_person(emotion = "happy")
    mom.title "Here you go sweetheart. You look very sharp in your suit, by the way. My little boy is all grown up."
    "You eat quickly, keeping a sharp eye on the time. When you're done you stand up and move to the front door again."
    mc.name "Okay, I've got to go if I'm going to catch my bus. I'll talk to you later and let you know how it goes."
    mom.title "Wait."
    "Mom follows you to the front door. She straightens your tie and brushes some lint off of your shoulder."
    mom.title "Oh, I should have ironed this for you."
    mc.name "It's fine, Mom. Really."
    mom.title "I know, I know, I'll stop fussing. Good luck sweety."
    "She wraps her arms around you and gives you a tight hug. You hug her back then hurry out the door."
    $ renpy.scene("Active")
    $ renpy.show(downtown.name,what=downtown.background_image)
    "It takes an hour on public transit then a short walk to find the building. It's a small single level office attached to a slightly larger warehouse style building."
    "You pull on the door handle. It thunks loudly - locked. You try the other one and get the same result."
    mc.name "Hello?"
    "You pull on the locked door again, then take a step back and look around for another enterance you might have missed. You don't see any."
    "You get your phone out and call the contact number you were given a few days earlier. It goes immediately to a generic voice mail system."
    "With nothing left to do you give up and turn around. Suddenly there's a click and the front door to the office swings open."
    "Janitor" "Hey, who's making all that noise?"
    "A middle aged man is standing at the door wearing grey-brown overalls. He's holding a stack of papers in one hand and a tape gun in the other."
    mc.name "That was me. I'm suppose to be here for a job interview, do you know where I should be going?"
    "Janitor" "Well I think you're shit out of luck then. They went belly up yesterday. This place belongs to the bank now."
    mc.name "What? That can't be right, I was talking to them less than a week ago."
    "Janitor" "Here, take a look for yourself."
    "The man, who you assume is a janitor of some sort, hands you one of the sheets of paper he's holding."
    "It features a picture of the building along with an address matching the one you were given and a large \"FORECLOSED\" lable along the top."
    "The janitor turns around and holds a page up to the front door, then sticks it in place with tape around all four edges."
    "Janitor" "They must have been neck deep in dept, if that makes you feel better about not working for 'em."
    "Janitor" "They left all their science stuff behind; must've been worth less than the debt they're ditching."
    mc.name "So everything's still in there?"
    "Janitor" "Seems like it. Bank doesn't know where to sell it and didn't want me to warehouse it, so it goes with the property."
    "You look back at the foreclosure notice and read until you see the listing price."
    "The rent on the unit is expensive, but an order of magnitude less than what you would have expected a fully stocked lab to be worth."
    mc.name "Would you mind if I take a quick look around? I promise I won't be long."
    "The janitor gives you a stern look, judging your character, then nods and opens the door."
    "Janitor" "I'm just about done tidying this place up so the bank can sell it. If you can be in and out in five minutes you can look around."
    mc.name "Thank you, I'll be quick."
    "You step inside the building and take a walk around."
    "The main office building contains a small lab, much like the one you worked at while you were in university, suitable for research and development tasks."
    "The connected warehouse space has a basic chemical production line installed. The machines are all off-brand but seem functional."
    "At the back of the building is a loading dock for shipping and recieving materials."
    "While you're exploring you hear the janitor yell from across the building."
    "Janitor" "I need to be heading off. Are ya done in there?"
    mc.name "Yeah, I'm done. Thanks again."
    "The janitor locks the door when you leave. You get on a bus heading home and do some research on the way."
    "You look up the price of some of the pieces of equipment you saw and confirm your suspicion. The bank has no idea how valuable the property really is."
    scene
    $ renpy.with_statement(fade)
    $ renpy.show(kitchen.name,what=kitchen.background_image)
    "Three days later..."
    $ mom.draw_person(position = "sitting")
    "Mom looks over the paperwork you've laid out. Property cost, equipment value, and potential earnings are all listed."
    mom.title "And you've checked all the numbers?"
    mc.name "Three times."
    mom.title "It's just... this is a lot of money [mom.mc_title]. I would need to take a second morgage out on the house."
    mc.name "And I'll be able to pay for that. This is the chance of a life time Mom."
    mom.title "What was it you said you were going to make again?"
    mc.name "When I was working at the lab last summer we developed some prototype chemical carriers. I think they have huge commercial potential."
    mc.name "And there's no regulation around them yet, because they're so new. I can start production and be selling them tomorrow."
    "[mom.possessive_title] leans back in her chair and pinches the brow of her nose."
    mom.title "Okay, you've convinced me. I'll get in touch with the bank and put a loan on the house."
    "You jump up and throw your arms around [mom.possessive_title]. She laughs and hugs you back."

    lily.title "What's going on?"
    $ lily.draw_person()
    "[lily.possessive_title] steps into the doorway and looks at you both."
    $ mom.draw_person(position = "sitting")
    mom.title "Your brother is starting a business. I'm his first investor."
    $ lily.draw_person(emotion = "happy")
    lily.title "Is that what you've been excited about the last couple days? What're you actually making?"
    mc.name "I'll have to tell you more about it later Lily, I've got some calls to make. Thanks Mom, you're the best!"
    $ renpy.scene("Active")
    "You leave [mom.possessive_title] and sister in the kitchen to talk retreat to your room for some privacy."

    $ renpy.show(bedroom.name, what=bedroom.background_image)
    "You can manage the machinery of the lab, but you're going to need help refining the serum design from last year."
    "You pick up your phone and call [stephanie.title]."
    stephanie.title "Hello?"
    mc.name "Stephanie, this is [mc.name]."
    stephanie.title "[stephanie.mc_title]! Good to hear from you, what's up?"
    mc.name "I'd like to talk to you about a business offer. Any chance we could meet somewhere?"
    stephanie.title "Ooh, a business offer. How mysterious. I'm almost done here at the lab, if you buy me a drink you've got a deal."
    mc.name "Done. Where's convenient for you?"
    "Stephanie sends you the address of a bar close to the university."
    scene
    $ renpy.show(bedroom.name,what=bar_background)
    "It takes you an hour to get your pitch prepared and to get over to the bar."
    "When you arrive [stephanie.title] is sitting at the bar with a drink already. She smiles and raises her glass."
    $ stephanie.draw_person(position = "sitting", emotion = "happy")
    stephanie.title "Hey [stephanie.mc_title], it's great to see you!"
    "She she stands and gives you a hug."
    stephanie.title "That was a crazy summer we had together. It seems like such a blur now, but I had a lot of fun."
    mc.name "Me too, that's actually part of what I want to talk to you about."
    "You order a drink for yourself and sit down."
    "You lay out your idea to [stephanie.title]: the commercial production and distribution of the experimental serum."
    stephanie.title "Well that's... Fuck, it's bold, I'll say that. And you need me to handle the R&D side of the business."
    mc.name "Right. Production processes are my bread and butter, but I need your help to figure out what we're actually making."
    "Stephanie finishes off her drink and flags down the bartender for another."
    stephanie.title "I would need to quit my job at the lab, and there's no guarantee that this even goes anywhere."
    mc.name "Correct."
    stephanie.title "Do have any clients?"
    mc.name "Not yet. It's hard to have clients without a product."
    "Stephanie gets her drink and sips it thoughtfully."
    mc.name "The pay won't be great either, but I can promise..."
    stephanie.title "I'm in."
    mc.name "I... what?"
    stephanie.title "I'm in. The old lab just doesn't feel the same since you left. I've been looking for something new in my life, something to shake things up."
    stephanie.title "I think this is it."
    "She raises her drink and smiles a huge smile."
    stephanie.title "A toast: To us, and stupid risks!"
    mc.name "To us!"
    "You clink glasses together and drink."
    stephanie.title "Ah... Okay, so I've got some thoughts already..."
    "Stephanie grabs a napkin and starts doodling on it. You spend the rest of the night with her, drinking and talking until you have to say goodbye."
    $ renpy.scene("Active")
    "A week later [mom.possessive_title] has a new morgage on the house and purchases the lab in your name."
    "You are the sole shareholder of your own company and [stephanie.title] is first, and so far only, employee. She takes her position as your head researcher."
    $ mc.business.event_triggers_dict["Tutorial_Section"] = True
    #$ mc.can_skip_time = False
    python: #To begin the tutorial we limit where people can travel!
        for place in list_of_places:
            place.accessable = False
    $ lobby.accessable = True
    return

label normal_start:
    ## For now, this ensures reloadin the game doesn't reset any of the variables.
    $ renpy.scene()
    show screen tooltip_screen
    show screen phone_hud_ui
    show screen business_ui
    show screen goal_hud_ui
    show screen main_ui
    $ renpy.show(bedroom.name,what=bedroom.background_image) #show the bedroom background as our starting point.
    "It's Monday, and the first day of operation for your new business!"
    "[stephanie.title] said she would meet you at your new office for a tour."

    #Add Stepyhanie to our business and flag her with a special role.
    $ mc.business.add_employee_research(stephanie)
    $ mc.business.r_div.add_person(stephanie) #Lets make sure we actually put her somewhere
    $ mc.business.r_div.move_person(stephanie,lobby)
    $ stephanie.set_work([1,2,3],mc.business.r_div)
    $ mc.business.head_researcher = stephanie
    $ stephanie.special_role = [steph_role, employee_role, head_researcher]

    call examine_room(mc.location) from _call_examine_room
    #TODO: movement overlay tutorial thing.
    jump game_loop

label faq_loop:
    menu:
        "Gameplay Basics.":
            menu:
                "Making Serum.":
                    "Vren" "Making serum in your lab is the most important task for success in Lab Rats 2. You begin the game with a fully equipt lab."
                    "Vren" "The first step to make a serum is to design it in your lab. The most basic serum design can be made without any additions, but most will be made by adding serum traits."
                    "Vren" "Serum traits modify the effects of a serum. The effects can be simple - increasing duration or Suggestion increase - or it may be much more complicated."
                    "Vren" "Each serum design has a limited number of trait slots. The number of slots can be increased by using more advanced serum production techniques."
                    "Vren" "Once you have decided on the traits you wish to include in your serum you will have to spend time in the lab researching it. Place it in the research queue and spend a few hours working in the lab."
                    "Vren" "More complicated serums will take more time to research. Once the serum is completely researched it can be produced by your production division. Move over their and slot it into the current production queue."
                    "Vren" "Before you can produce the serum you will need raw supplies. One unit of supply is needed for every production point the serum requires. You can order supply from your main office."
                    "Vren" "Once you have supplies you can spend time in your production lab. Doses of serum are made in batches - unlocking the ability to make larger batches will let you make more serum with the same amount of supply."
                    "Vren" "You can either take this serum for your own personal use, or you can head to the main office and mark it for sale. Once a serum is marked for sale you can spend time in your marketing division to find a buyer."
                    "Vren" "Your research and development lab can also spend time researching new traits for serum instead of producing new serum designs. You slot these into your research queue in the same way you do a new serum design."

                "Hiring Staff.":
                    "Vren" "While you can do all the necessary tasks for your company yourself, that isn't how you're going to make it big. Hiring employees will let you spend you grow your business and pull in more and more money."
                    "Vren" "To hire someone, head over to your main office. From there you can request a trio of resumes to choose from, for a small cost. The stats of the three candidates will be chosen, and you can choose who to hire."
                    "Vren" "The three primary stats - Charisma, Intelligence, and Focus - are the most important traits for a character. Each affects the jobs in your company differently."
                    "Vren" "Charisma is the primary stat for marketing and human resources, as well as being a secondary stat for purchasing supplies."
                    "Vren" "Intelligence is the primary stat for research, as well as a secondary stat for human resources and production."
                    "Vren" "Focus is the primary stat for supply procurement and production, as well as a secondary stat for research."
                    "Vren" "Each character will also have an expected salary, to be paid each day. Higher stats will result in a more expensive employee, so consider hiring specialists rather than generalists."
                    "Vren" "Your staff will come into work each morning and perform their appropriate tasks, freeing up your time for other pursuits..."

                "Corrupting People.":
                    "Vren" "You may be wondering what you can do with all this serum you produce. The main use of serum is to increase the Suggestibility statistic of another character."
                    "Vren" "While a character has a Suggestibility value of 0 nothing you do will have a long lasting effect on their personality. Suggestibility above 0 will allow you to slowly corrupt them."
                    "Vren" "Each girl has a Core Sluttiness value. This is the level of sluttiness they think is appropriate without any external influence. Core sluttiness looks like this: {image=gui/heart/gold_heart.png}"
                    "Vren" "They also have a Temporary Sluttiness value, which fluctuates up and down based on recent events. Temporary sluttiness looks like this: {image=gui/heart/red_heart.png}"
                    "Vren" "A girls Temporary Sluttiness will decrease if it is higher than her Core Sluttiness. If Suggestibility is higher than 0 there is a chance for the Temporary sluttiness to turn into Core sluttiness."
                    "Vren" "Suggesibility has another use. It will increase the cap for Temporary sluttiness. Temporary sluttiness looks like this: {image=gui/heart/grey_heart.png}"
                    "Vren" "Interacting with a girl is the most direct way to change their Obedience or Sluttiness. There may also be random events that change their scores."
                    "Vren" "Most actions have a minimum Temporary sluttiness rquirement before they can be attempted and a maximum Temporary sluttiness they will have an effect on."
                    "Vren" "Having sex with a girl is nessesary to increase her sluttiness to the highest levels. Higher arousal will make a girl more willing to strip down or have sex."
                    "Vren" "If you are able to make a girl cum she will immediately start to turn Temporary sluttiness into core sluttiness."
                    "Vren" "As a girls Sluttiness increases she will be more willing to wear revealing clothing or have sex with you."
                    "Vren" "As her Obedience increase she will be more deferential. She may be willing to have sex simply because you ask, even if she is not normally slutty enough."

                "Leveling Up.":
                    "Vren" "There are three main catagories of experience: Stats, Work Skills, and Sex Skills."
                    "Vren" "For each of these catagories you will have a goal assigned. When that goal is completed you will recieve one point to spend on any of the scores in that catagory."
                    "Vren" "Once per day you may also scrap a goal that is overly difficult or not possible to complete yet."
                    "Vren" "When you complete a goal future goals in that catagory will increase in difficulty. Spend your early points wisely!"
                    "Vren" "Some goals are only checked at the end of the day or end of a turn, so if you have a goal that should be completed but is not giving you the option try advancing time."

        "Development Questions.":
            menu:
                "Will there be more character poses?":
                    "Vren" "Absolutely! The current standing poses proved that the rendering workflow for the game is valid, which means I will be able to introduce character poses for different sex positions."
                    "Vren" "Most sex positions have character poses associated with them and new poses will be rendered with each update."

                "Will there be animation?":
                    "Vren" "No, there will not be full animation in the game. There may be small sprite based animations added later, but this will require more experimentation by me before I can commit to it."

                "Why are their holes in some pieces of clothing?":
                    "Vren" "Some character positions cause portions of the character model to poke out of their clothing when I am rendering them."
                    "Vren" "I will be adjusting my render settings and rerendering any clothing items that need it as we go forward."

        "Done.":
            return
    call faq_loop from _call_faq_loop_1
    return

label check_inventory_loop:
    call screen show_serum_inventory(mc.inventory)
    return

label check_business_inventory_loop:
    call screen show_serum_inventory(mc.business.inventory,[mc.business.sale_inventory],["Production Inventory","Waiting to Ship"])
    return

init -2 python:
    def indent(elem, level=0):
        i = "\n" + level*"    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "    "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def log_outfit(the_outfit, outfit_class = "FullSets", wardrobe_name = "Exported_Wardrobe"):
        file_path = os.path.abspath(os.path.join(config.basedir, "game"))
        file_path = os.path.join(file_path,"wardrobes")
        file_name = os.path.join(file_path, wardrobe_name + ".xml")

        if not os.path.isfile(file_name): #We assume if the file exists that it is well formed. Otherwise we will create it and guarantee it is well formed.
            #Note: if the file is changed (by inserting extra outfits, for example) exporting outfits may crash due to malformed xml, but we do not overwrite the file.
            missing_file = open(file_name,"w+")
            starting_element = ET.Element("Wardrobe",{"name":wardrobe_name})
            starting_tree = ET.ElementTree(starting_element)
            ET.SubElement(starting_element,"FullSets")
            ET.SubElement(starting_element,"UnderwearSets")
            ET.SubElement(starting_element,"OverwearSets")

            indent(starting_element)
            starting_tree.write(file_name,encoding="UTF-8")


        wardrobe_tree = ET.parse(file_name)
        tree_root = wardrobe_tree.getroot()
        outfit_root = tree_root.find(outfit_class)

        outfit_element = ET.SubElement(outfit_root,"Outfit",{"name":the_outfit.name})
        upper_element = ET.SubElement(outfit_element, "UpperBody")
        lower_element = ET.SubElement(outfit_element, "LowerBody")
        feet_element = ET.SubElement(outfit_element, "Feet")
        accessory_element = ET.SubElement(outfit_element, "Accessories")


        for cloth in the_outfit.upper_body:
            item_dict = build_item_dict(cloth)
            if not cloth.is_extension:
                ET.SubElement(upper_element,"Item", item_dict)
        for cloth in the_outfit.lower_body:
            item_dict = build_item_dict(cloth)
            if not cloth.is_extension:
                ET.SubElement(lower_element,"Item", item_dict)
        for cloth in the_outfit.feet:
            item_dict = build_item_dict(cloth)
            if not cloth.is_extension:
                ET.SubElement(feet_element,"Item", item_dict)
        for cloth in the_outfit.accessories:
            item_dict = build_item_dict(cloth)
            if not cloth.is_extension:
                ET.SubElement(accessory_element,"Item", item_dict)


        indent(tree_root)
        wardrobe_tree.write(file_name,encoding="UTF-8")

    def build_item_dict(cloth):
        item_dict = {"name":cloth.proper_name,"red":str(cloth.colour[0]),"green":str(cloth.colour[1]),"blue":str(cloth.colour[2]),"alpha":str(cloth.colour[3])}
        if __builtin__.type(cloth) is Clothing and cloth.pattern is not None:
            item_dict.update({"pattern":cloth.pattern, "pred":str(cloth.colour_pattern[0]), "pgreen":str(cloth.colour_pattern[1]), "pblue":str(cloth.colour_pattern[2]), "palpha":str(cloth.colour_pattern[3])})
        return item_dict

    def log_wardrobe(the_wardrobe, file_name):

        for outfit in the_wardrobe.outfits:
            log_outfit(outfit, outfit_class = "FullSets", wardrobe_name = file_name)

        for outfit in the_wardrobe.underwear_sets:
            log_outfit(outfit, outfit_class = "UnderwearSets", wardrobe_name = file_name)

        for outfit in the_wardrobe.overwear_sets:
            log_outfit(outfit, outfit_class = "OverwearSets", wardrobe_name = file_name)


label outfit_master_manager(): #WIP new outfit manager that centralizes exporting, modifying, duplicating, and deleting.

    call screen outfit_select_manager(main_selectable = False, show_make_new = True, show_export = True, show_modify = True, show_duplicate = True, show_delete = True)

    if _return == "No Return":
        return #We're done and want to leave.

    $ outfit_type = None
    if _return == "new_full":
        $ outfit_type = "full"
        call screen outfit_creator(Outfit("New Outfit"), outfit_type = outfit_type)

    elif _return == "new_over":
        $ outfit_type = "over"
        call screen outfit_creator(Outfit("New Overwear Set"), outfit_type = outfit_type)

    elif _return == "new_under":
        $ outfit_type = "under"
        call screen outfit_creator(Outfit("New Underwear Set"), outfit_type = outfit_type)

    elif isinstance(_return, Outfit):
        #If we are returning an outfit we should be in one of the three sets (if not: panic!)
        if _return in mc.designed_wardrobe.outfits:
            $ outfit_type = "full"

        elif _return in mc.designed_wardrobe.overwear_sets:
            $ outfit_type = "over"

        elif _return in mc.designed_wardrobe.underwear_sets:
            $ outfit_type = "under"

        else:
            "We couldn't find it anywhere! PANIC!"

        $ mc.designed_wardrobe.remove_outfit(_return) # Remove it so we can re-add it later. Note that "dupicate" has already copied an outfit and added it so we can re-use this code.

        call screen outfit_creator(_return, outfit_type = outfit_type)

    $ new_outfit = _return #This is the oufit the player has created.
    if not new_outfit == "Not_New":
        $ new_outfit_name = renpy.input("Please name this outfit.", default = new_outfit.name)
        while new_outfit_name == "":
            $ new_outfit_name = renpy.input("Please enter a non-empty name.", default = new_outfit.name)


        $ mc.save_design(new_outfit, new_outfit_name, outfit_type)

    call outfit_master_manager() from _call_outfit_master_manager #Loop around until the player decides they want to leave.
    return



label game_loop: ##THIS IS THE IMPORTANT SECTION WHERE YOU DECIDE WHAT ACTIONS YOU TAKE
    # $ mc.can_skip_time = True

    python:
        predicted_displayables = []
        for person in mc.location.people:
            predicted_displayables.append(person.build_person_displayable())
        renpy.start_predict(*predicted_displayables)


    $ people_list = ["Talk to Someone"]
    $ people_list.extend(mc.location.people)

    $ actions_list = ["Do Something"]
    if time_of_day == 4:
        if sleep_action not in mc.location.actions: #If they're in a location they can sleep we shouldn't show this because they can just sleep here.
            $ actions_list.append(["Go home and sleep.{image=gui/heart/Time_Advance.png} (tooltip)It's late. Go home and sleep.", "Wait"])
    else:
        $ actions_list.append(["Wait here. (tooltip)Kill some time and wait around.", "Wait"])
    $ actions_list.append(["Go somewhere else.", "Travel"])
    $ actions_list.extend(mc.location.get_valid_actions())

    call screen main_choice_display([people_list,actions_list])

    $ picked_option = _return
    if isinstance(picked_option, Person):
        # mc.can_skip_time = False
        if picked_option == "Back":
            $ renpy.jump("game_loop")
        else:
            $ picked_option.draw_person()
            $ enabled_talk_events = []
            python:
                for possible_talk_event in picked_option.on_talk_event_list:
                    if possible_talk_event.is_action_enabled(picked_option):
                        enabled_talk_events.append(possible_talk_event)
            if enabled_talk_events:
                #If there are any events we want to trigger it happens instead of talking to the person. If we want it to lead into talk_person we can call that separately. Only one event per interaction.
                $ talk_action = get_random_from_list(enabled_talk_events)
                $ talk_action.call_action(picked_option)
                $ picked_option.on_talk_event_list.remove(talk_action)


            else:
                if picked_option.title is None:
                    "You decide to approach the stranger and introduce yourself."
                else:
                    "You approach [picked_option.title] and chat for a little bit."
                    $ picked_option.call_dialogue("greetings")

                call talk_person(picked_option) from _call_talk_person

    elif isinstance(picked_option, Action):
        $ picked_option.call_action()


    elif picked_option == "Travel":
        call screen map_manager
        $ new_location = _return
        call change_location(new_location) from _call_change_location #_return is the location returned from the map manager.
        if new_location.people: #There are people in the room, let's see if there are any room events
            $ enabled_room_events = []
            python: #Scan through all the people and...
                for a_person in new_location.people:
                    for possible_room_event in a_person.on_room_enter_event_list:
                        if possible_room_event.is_action_enabled(a_person): #See what events the are enabled...
                            enabled_room_events.append([a_person, possible_room_event]) #Then keep track of the person so we know who to remove it from if it triggers.

            if enabled_room_events: #If there are room events to take care of run those right now.
                $ picked_event = get_random_from_list(enabled_room_events)
                $ picked_event[0].on_room_enter_event_list.remove(picked_event[1]) #Remove the event from their list since we will be running it.
                $ picked_event[1].call_action(picked_event[0]) #Run the action with the person as an extra argument.

            elif new_location in [mc.business.m_div, mc.business.p_div, mc.business.r_div, mc.business.s_div, mc.business.h_div]: #There are no room events, so generate a quick room greeting from an employee if one is around.
                $ possible_greetings = []
                python:
                    for a_person in new_location.people:
                        if mc.business.get_employee_title(a_person) != "None":
                            possible_greetings.append(a_person)
                $ the_greeter = get_random_from_list(possible_greetings)
                if the_greeter:
                    $ the_greeter.draw_person()
                    $ the_greeter.call_dialogue("work_enter_greeting")
                    $ renpy.scene("Active")

    elif picked_option == "Wait":
        if time_of_day == 4:
            $ mc.change_location(bedroom)
        call advance_time from _call_advance_time_15

    jump game_loop



label change_location(the_place):
    $ renpy.scene()
    $ renpy.show(the_place.name,what=the_place.background_image)
    if the_place.trigger_tutorial and the_place.tutorial_label is not None and mc.business.event_triggers_dict["Tutorial_Section"] == True:
        $ the_place.trigger_tutorial = False
        $ renpy.call(the_place.tutorial_label)

    return

label talk_person(the_person):
    $the_person.draw_person()
    if the_person.title is None:
        call person_introduction(the_person) from _call_person_introduction #If their title is none we assume it is because we have never met them before. We have a special introduction scene for new people.
        #Once that's done we continue to talk to the person.
    elif the_person.event_triggers_dict.get("wants_titlechange",False):
        if renpy.random.randint(0,1) == 0: #50% of the time she wants a new title, otherwise she wants to give you a new title.
            call person_new_title(the_person) from _call_person_new_title
        else:
            call person_new_mc_title(the_person) from _call_person_new_mc_title
        $ the_person.event_triggers_dict["wants_titlechange"] = False

    # BUGFIX: moved actions to init section (prevents memory leak on action objects)
    #         set parameters in python code for the displayed actions

    python:
        change_titles_action.args = [the_person]
        change_titles_action.requirement_args = [the_person]
        small_talk_action.args = [the_person]
        small_talk_action.requirement_args = [the_person]
        compliment_action.args = [the_person]
        compliment_action.requirement_args = [the_person]
        flirt_action.args = [the_person]
        flirt_action.requirement_args = [the_person]
        date_action.args = [the_person]
        date_action.requirement_args = [the_person]

        wardrobe_change_action.args = [the_person]
        wardrobe_change_action.requirement_args = [the_person]
        serum_give_action.args = [the_person]
        serum_give_action.requirement_args = [the_person]
        seduce_action.args = [the_person]
        seduce_action.requirement_args = [the_person]

        special_role_actions = ["Special Actions"]
        roles_that_need_people_args = []
        for role in the_person.special_role:
            for act in role.actions:
                special_role_actions.append([act,the_person]) #They're a list of actions and their extra arg so that gets passed through properly.
                roles_that_need_people_args.append(act) #All role actions need to be passed the specific person, so we keep a list of these actions here and check it below.


    call screen main_choice_display([
        ["Chat with her", change_titles_action, small_talk_action, compliment_action, flirt_action, date_action],
        ["Do something specific", "Say goodbye.", wardrobe_change_action, serum_give_action, seduce_action], 
        special_role_actions])

    if isinstance(_return, Action):
        $ starting_time_of_day = time_of_day
        if _return in roles_that_need_people_args:
            $ _return.call_action(the_person)
        else:
            $ _return.call_action()

        if the_person in mc.location.people and time_of_day == starting_time_of_day:
            call talk_person(the_person) from _call_talk_person_1 #If we're in the same place and time hasn't advanced keep talking to them until we stop talking on purpose.

    python:
        # Release objects
        special_role_actions = None
        roles_that_need_people_args = None

    $ renpy.scene("Active")
    return


label fuck_person(the_person, private=True, start_position = None, start_object = None, skip_intro = False, girl_in_charge = False, hide_leave = False):
    #Use a situational modifier to change sluttiness before having sex.
    $ use_love = True
    if any(relationship in [sister_role,mother_role,aunt_role,cousin_role] for relationship in the_person.special_role): #Check if any of the roles the person has belong to the list of family roles.
        $ the_person.add_situational_slut("taboo_sex", -20, "We're related, we shouldn't be doing this.")
        $ use_love = False

    $ the_person.discover_opinion("cheating on men")
    if the_person.relationship == "Girlfriend":
        if the_person.get_opinion_score("cheating on men") > 0:
            $ the_person.add_situational_slut("cheating", the_person.get_opinion_score("cheating on men") * 5, "I'm cheating on my boyfriend!")
        else:
            $ the_person.add_situational_slut("cheating", -5 + (the_person.get_opinion_score("cheating on men") * -10), "I can't cheat on my boyfriend!")
    elif the_person.relationship == "Fiancée":
        if the_person.get_opinion_score("cheating on men") > 0:
            $ the_person.add_situational_slut("cheating", the_person.get_opinion_score("cheating on men") * 8, "I'm cheating on my fiancé!")
        else:
            $ the_person.add_situational_slut("cheating", -15 + (the_person.get_opinion_score("cheating on men") * -15), "I could never cheat on my fiancé!")
    elif the_person.relationship == "Married":
        if the_person.get_opinion_score("cheating on men") > 0:
            $ the_person.add_situational_slut("cheating", the_person.get_opinion_score("cheating on men") * 10, "I'm cheating on my husband!")
        else:
            $ the_person.add_situational_slut("cheating", -20 + (the_person.get_opinion_score("cheating on men") * -20), "I could never cheat on my husband!")

    if not private:
        $ use_love = False
        if the_person.sluttiness < 50:
            $ the_person.add_situational_slut("public_sex", -10 + the_person.get_opinion_score("public sex") * 5, "There are people watching...")
        else:
            $ the_person.add_situational_slut("public_sex", the_person.get_opinion_score("public sex") * 5, "There are people watching!")

    if use_love or the_person.love < 0:
        if the_person.love > 0:
            $ the_person.add_situational_slut("love_modifier", the_person.love, "I love you and want you close to me!")
        else:
            $ the_person.add_situational_slut("love_modifier", the_person.love, "I hate you, get away from me!")


    python:
        tuple_list = []
        if start_position and (start_position in list_of_positions or start_position in list_of_girl_positions):
            position_choice = start_position
        else:
            if girl_in_charge:
                for position in list_of_girl_positions:
                    if mc.location.has_object_with_trait(position.requires_location):
                        if position.check_clothing(the_person):
                            if position.slut_requirement <= the_person.effective_sluttiness():
                                tuple_list.append(position)
                position_choice = get_random_from_list(tuple_list)
                if not position_choice:
                    position_choice = "Girl Leave"


            else:
                for position in list_of_positions:
                    if mc.location.has_object_with_trait(position.requires_location):
                        #Note: clothing checks are done in the build_position_willingness_string() check, where it markes them as obstructed and (disabled).
                        tuple_list.append([position.build_position_willingness_string(the_person), position])

                if not hide_leave: #Some events don't let you leave.
                    tuple_list.append(["Leave","Leave"]) #Stop having sex, since cumming is now a locked in thing.
                position_choice = renpy.display_menu(tuple_list,True,"Choice")

    if position_choice == "Leave":
        if the_person.effective_sluttiness() > 60:
            if renpy.random.randint(0,the_person.arousal) + 50 < the_person.obedience:
                $ the_person.call_dialogue("sex_take_control")
                $ the_person.change_obedience(-3)
                call fuck_person(the_person, private, start_position, start_object, skip_intro = True, girl_in_charge = True) from _call_fuck_person_18

            elif the_person.arousal > 80:
                # They're close to their orgasm and beg you to help them finish.
                $ the_person.call_dialogue("sex_beg_finish")
                menu:
                    "Keep going.":
                        $ the_person.change_obedience(2)
                        call fuck_person(the_person, private, start_position, start_object, skip_intro = True, hide_leave = True) from _call_fuck_person_19 #Redo all of this but don't let them leave. Start position and start_object will normally be None

                    "Leave.":
                        $ the_person.call_dialogue("sex_end_early")

            else: #They're slutty but they just say they're sad to end.
                $ the_person.call_dialogue("sex_end_early")
        else:
            $ the_person.call_dialogue("sex_end_early")

    elif position_choice == "Girl Leave":
        "[the_person.title] can't think of anything more to do with you."

    else: #It is neither of the leave options, so it is a position and we can continue
        python:
            tuple_list = []
            if start_object and start_object in mc.location.objects:
                object_choice = start_object
            elif girl_in_charge:
                for object in mc.location.objects:
                    if object.has_trait(position_choice.requires_location):
                        tuple_list.append(object)

                tuple_list.sort(key = lambda obj: obj.sluttiness_modifier, reverse = True)
                object_choice = tuple_list[0] #We know there was a valid object or the position couldn't have been selected. Get the most slutty object possible.

            else:
                renpy.say("","Where do you do it?")

                for object in mc.location.objects:
                    if object.has_trait(position_choice.requires_location):
                        tuple_list.append([object.get_formatted_name(),object]) #Displays a lsit of objects in the room related to that position and their appropriate bonuses/penalties

                object_choice = renpy.display_menu(tuple_list,True,"Choice")
            the_person.add_situational_slut("sex_object",object_choice.sluttiness_modifier,"using a " + object_choice.name)
            the_person.add_situational_obedience("sex_object",object_choice.obedience_modifier, "using a " + object_choice.name)
        $ start_round = 0
        if skip_intro:
            $ start_round = 1
        call sex_description(the_person, position_choice, object_choice, start_round, private=private, girl_in_charge = girl_in_charge) from _call_sex_description


    $ the_person.clear_situational_slut("love_modifier")
    $ the_person.clear_situational_slut("cheating")
    $ the_person.clear_situational_slut("taboo_sex")
    $ the_person.clear_situational_slut("sex_object")
    $ the_person.clear_situational_obedience("sex_object")
    $ mc.condom = False
    return

label sex_description(the_person, the_position, the_object, round, private = True, girl_in_charge = False):
    #NOTE: the private variable decides if you are in private or not relative to the location you are in. If True other people in the room do not get a chance to interact.

    ##Describe the current round

    ## FIRST ROUND EXCLUSIVE STUFF ##
    if round == 0: ##First round means you just started, so do intro stuff before we get on with it. Also where we check to see if they are into having this type of sex.
        if the_person.effective_sluttiness() >= the_position.slut_requirement: #The person is slutty enough to want to have sex like this.
            $ the_person.call_dialogue("sex_accept")
            if the_position.skill_tag == "Vaginal": #She may demand you put on a condom.
                call condom_ask(the_person) from _call_condom_ask
                if not _return:
                    call fuck_person(the_person, private = private, girl_in_charge = girl_in_charge) from _call_fuck_person_20
                    return

            $ the_position.call_intro(the_person, mc.location, the_object, round)
            $ the_position.redraw_scene(the_person)

        else: #The person isn't slutty enough for this. First, try and use obedience. If you still fail, but by a little, she rebukes you but you keep seducing her. Otherwise, the entire thing ends.
            if the_person.effective_sluttiness() + (the_person.obedience-100) >= the_position.slut_requirement:
                #You can use obedience to do it.
                $ the_person.call_dialogue("sex_obedience_accept")
                if the_position.skill_tag == "Vaginal": #She may demand you put on a condom.
                    call condom_ask(the_person) from _call_condom_ask_1
                    if not _return:
                        call fuck_person(the_person, private = private, girl_in_charge = girl_in_charge) from _call_fuck_person_21
                        return
                $ the_position.redraw_scene(the_person)
                $ change_amount = the_position.slut_requirement - the_person.sluttiness
                $ the_person.change_happiness(-change_amount) #She looses happiness equal to the difference between her sluttiness and the requirement. ie the amount obedience covered.
                $ the_position.call_intro(the_person, mc.location, the_object, round)
                $ the_position.redraw_scene(the_person)
            else:
                #No amount of obedience will help here. How badly did you screw up?
                if the_person.effective_sluttiness() < the_position.slut_requirement/2: #Badly, not even half way to what you needed
                    $ the_position.redraw_scene(the_person,emotion="angry")
                    $ the_person.change_happiness(-5) #She's pissed you would even try that
                    $ the_person.call_dialogue("sex_angry_reject")
                    return #Don't do anything else, just return.
                else:
                    $ the_person.call_dialogue("sex_gentle_reject")
                    call fuck_person(the_person, private = private, girl_in_charge = girl_in_charge) from _call_fuck_person_1 #Gives you a chance to fuck them some other way, but this path is ended by the return right after you finish having sex like that.
                    return

    ## ONCE WE HAVE DONE FIRST ROUND CHECKS WE GO HERE ##
    $ the_position.redraw_scene(the_person)
    $ the_position.call_scene(the_person, mc.location, the_object, round) #HERE IS WHERE THE SCENE SCRIPT IS CALLED
    $ mc.listener_system.fire_event("sex_event", the_person = the_person, the_position = the_position, the_object = the_object)

    $ change_amount = the_position.girl_arousal + (the_position.girl_arousal * mc.sex_skills[the_position.skill_tag] * 0.1) #How much we increase her arousal.
    if the_position.skill_tag == "Vaginal":
        $ the_person.discover_opinion("bareback sex")
        if mc.condom:
            $ change_amount += -2 * the_person.get_opinion_score("bareback sex")
        else:
            $ change_amount += 2 * the_person.get_opinion_score("bareback sex")

    if the_position.opinion_tags:
        python:
            for opinion_tag in the_position.opinion_tags:
                change_amount += the_person.get_opinion_score(opinion_tag) #Add a bonus or penalty if she likes or dislikes the position.
                the_person.discover_opinion(opinion_tag)

    if the_person.sluttiness + 1 > the_position.slut_cap:
        $ slut_report = "Position Max Reached."
    else:
        $ slut_report = the_person.change_slut_temp(1)

    if the_person.arousal > the_position.slut_cap: #She might be too turned on to be impressed by this position any more.
        if the_person.sluttiness > the_position.slut_cap: #She's too slutty to find this interesting.
            $ mc.log_event(the_person.title + ": Bored by position. Arousal gain halved.", "float_text_red")
            $ change_amount = change_amount/2 #Low sluttiness girls can be made to cum by kissing, higher sluttiness girls require more intense positions.
            #TODO: add a "sex_bored" dialogue option that can be called, asking for a more intense position.


    $ the_person.change_arousal(change_amount) #The girls arousal gain is the base gain + 10% per the characters skill in that category.
    $ mc.change_arousal(the_position.guy_arousal + (the_position.guy_arousal * the_person.sex_skills[the_position.skill_tag] * 0.1)) # The same calculation but for the guy

    ## POST ROUND CALCULATION AND DECISIONS PAST HERE ##

    if the_person.arousal >= 100:
        $ mc.listener_system.fire_event("girl_climax", the_person = the_person, the_position = the_position, the_object = the_object)
        $ the_position.call_orgasm(the_person,mc.location, the_object, round)
        $ the_position.current_modifier = None
        if the_person.sluttiness > the_person.core_sluttiness and the_person.core_sluttiness < the_position.slut_cap:
            $ the_person.change_slut_core(1)
            $ the_person.change_slut_temp(-1)
        $the_person.change_happiness(2) #Orgasms are good, right?
    else:
        $the_person.call_dialogue("sex_responses")

    ## IF OTHER PEOPLE ARE AROUND SEE WHAT THEY THINK ##
    if not private:
        $ other_people = [person for person in mc.location.people if person is not the_person] #Build a list with all the _other_ people in the room other than the one we're fucking.
        $ watcher = get_random_from_list(other_people) #Get a random person from the people in the area, if there are any.
        if watcher:
            # NOTE: the dialogue here often draws the person talking with various emotions or positions, so we redraw the scene after we call them.
            $ watcher.call_dialogue("sex_watch", the_sex_person = the_person, the_position = the_position) #Get the watcher's reaction to the people having sex. This might include dialogue calls from other personalities as well!
            $ the_position.redraw_scene(the_person)
            $ the_person.call_dialogue("being_watched", the_watcher = watcher, the_position = the_position) #Call her response to the person watching her.
            $ the_person.change_arousal(the_person.get_opinion_score("public sex"))
            $ the_person.discover_opinion("public sex")

    $ strip_chance = the_person.effective_sluttiness() - the_person.outfit.slut_requirement
    $ the_clothing = the_person.outfit.remove_random_any(exclude_feet = True, do_not_remove = True)
    if renpy.random.randint(0,100) < strip_chance and the_clothing:
        $ ask_chance = renpy.random.randint(0,100)
        if ask_chance < the_person.obedience - the_person.arousal:
            $ the_position.call_strip_ask(the_person, the_clothing, mc.location, the_object, round)
        else:
            $ the_position.call_strip(the_person, the_clothing, mc.location, the_object, round) #If a girl's outfit is less slutty than she is currently feeling (with arousal factored in) she will want to strip stuff off.

    #TODO: This is where we check to see if a girl seizes initative during an encounter.
    #TODO: This is where a girl might request a different position (and be happy if you follow through)

    ##Ask how you want to keep fucking her or find out how she keeps fucking you##
    $ position_choice = "Keep Going" #Default value just to make sure scope is correct.
    python:
        if (mc.arousal >= 100):
            "You're past your limit, you have no choice but to cum!"
            position_choice = "Finish"
        else:
            if girl_in_charge:
                renpy.say("",the_person.title +  " is taking the lead. She keeps " + the_position.verb + "ing you.")
                position_choice = the_position
                #TODO: this is where we perform any changes for the girl.
            else:
                tuple_list = []
                tuple_list.append(["Keep going.",the_position])
                tuple_list.append(["Back off and change positions.","Pull Out"])
                if (mc.arousal > 80): #Only let you finish if you've got a high enough arousal score. #TODO: Add stat that controls how much control you have over this.
                    tuple_list.append(["Cum!","Finish"])
                tuple_list.append(["Strip her down.","Strip"])
                for position in the_position.connections:
                    if the_object.has_trait(position.requires_location):
                        appended_name = "Change to " + position.build_position_willingness_string(the_person) #Note: clothing check is now done in build_position_willingness_string() call and marks them as (disabled)
                        tuple_list.append([appended_name,position])
                position_choice = renpy.display_menu(tuple_list,True,"Choice")

    if position_choice == "Finish":
        $ the_position.current_modifier = None
        $ the_position.call_outro(the_person, mc.location, the_object, round)
        $ mc.reset_arousal()
        # TODO: have you finishing bump her arousal up so you might both cum at once.

    elif position_choice == "Strip":
        call strip_menu(the_person) from _call_strip_menu
        $ the_position.redraw_scene(the_person)
        call sex_description(the_person, the_position, the_object, round+1, private = private) from _call_sex_description_1

    elif position_choice == "Pull Out": #Also how you leave if you don't want to fuck till you cum.
        $ the_position.current_modifier = None
        $ mc.condom = False
        call fuck_person(the_person, private = private, girl_in_charge = girl_in_charge) from _call_fuck_person_2

    # elif position_choice == "Girl Leave":
    #     $ the_position.current_modifier = None
    #     $ mc.condom = False
    #     "[the_person.title] can't think of anything else she wants to do with you and leaves."

    else:
        if not position_choice == the_position: #We are changing to a new position.
            $ the_position.current_modifier = None
            if the_person.effective_sluttiness() >= position_choice.slut_requirement: #The person is slutty enough to want to have sex like this. Higher arousal can get you up to a +50 slutiness boost.
                $ the_person.call_dialogue("sex_accept")
                $ the_position.call_transition(position_choice, the_person, mc.location, the_object, round)
            else: #The person isn't slutty enough for this. First, try and use obedience. If you still fail, but by a little, she rebukes you but you keep seducing her. Otherwise, the entire thing ends.
                if the_person.effective_sluttiness() + (the_person.obedience-100) >= position_choice.slut_requirement:
                    #You can use obedience to do it.
                    $ change_amount = the_person.effective_sluttiness() - the_person.sluttiness
                    $ the_position.redraw_scene(the_person,emotion = "sad")
                    $ the_person.change_happiness(-change_amount) #She looses happiness equal to the difference between her sluttiness and the requirement. ie the amount obedience covered.
                    $ the_person.call_dialogue("sex_obedience_accept")
                    $ the_position.call_transition(position_choice, the_person, mc.location, the_object, round)
                else:
                    #No amount of obedience will help here. How badly did you screw up?
                    if (the_person.effective_sluttiness() < (position_choice.slut_requirement/2)): #Badly, not even half way to what you needed
                        $ the_person.change_happiness(-5) #She's pissed you would even try that
                        $ the_person.change_love(-1)
                        $ the_person.call_dialogue("sex_angry_reject")
                        return #Don't do anything else, just return.
                    else:
                        $ the_position.call_transition(position_choice, the_person, mc.location, the_object, round)
                        $ the_person.call_dialogue("sex_gentle_reject")
                        $ position_choice.call_transition(the_position, the_person, mc.location, the_object, round)
                        $ position_choice = the_position

        call sex_description(the_person, position_choice, the_object, round+1, private = private, girl_in_charge = girl_in_charge) from _call_sex_description_2

    return

label condom_ask(the_person):
    $ condom_threshold = 70 + (the_person.get_opinion_score("bareback sex") * -10)
    if any(relationship in [sister_role,mother_role,aunt_role,cousin_role] for relationship in the_person.special_role):
        $ condom_threshold += 10

    if the_person.effective_sluttiness() < condom_threshold:
        # they demand you put on a condom.
        if the_person.get_opinion_score("bareback sex") > 0 or the_person.get_opinion_score("creampies"):
            the_person.char "I hate do say it, but I need you to put a condom on for me."
        else:
            the_person.char "Do you have a condom? You're going to have to put one on."

        menu:
            "Put on a condom.":
                $ mc.condom = True
                "You pull out a condom from your wallet and rip open the package. [the_person.title] watches while you slide it on."

            "Refuse and do something else.":
                "[the_person.title] doesn't seem like she's going to change her mind."
                mc.name "If it's that important to you let's just do something else."
                return False

    elif the_person.get_opinion_score("bareback sex") < 0 or the_person.effective_sluttiness() < condom_threshold + 20:
        # They suggest you put on a condom.
        if the_person.get_opinion_score("creampies") > 0:
            $ the_person.discover_opinion("creampies")
            the_person.char "I think you should put on a condom. If you do you won't have to pull out when you cum."
        else:
            the_person.char "Do you think you should put a condom on? Maybe it's a good idea."
        menu:
            "Put on a condom.":
                $ mc.condom = True
                mc.name "I think you're right. One second."
                "[the_person.title] watches eagerly while you pull a condom out of your wallet, tear open the package, and unroll it down your dick."

            "Fuck her raw.":
                mc.name "No way. I want to feel you wrapped around me."
                the_person.char "Just make sure to pull out if you're going to cum, okay?"

    else:
        # They ask you _not_ to put on a condom.
        if the_person.get_opinion_score("creampies") > 0:
            $ the_person.discover_opinion("creampies")
            the_person.char "Don't put on a condom, I want to feel you when you cum inside me."
        else:
            the_person.char "You don't need a condom, I want to feel every single thing you do to me."
        menu:
            "Put on a condom.":
                $ mc.condom = True
                mc.name "Sorry, but I still think a condom is a good idea."
                the_person.char "Fine, just make it quick please!"
                "[the_person.title] watches impatiently while you pull a condom out of your wallet, tear open the package, and unroll it down your dick."

            "Fuck her raw.":
                pass



    return True #If we make it to the end of the scene everything is fine and sex can continue. If we returned false we should go back to the position select, as if we asked for something to extreme.

label strip_menu(the_person):
    python:
        second_tuple_list = []
        for clothing in the_person.outfit.get_unanchored():
            if not clothing.is_extension: #Extension clothing is placeholder for multi-slot items like dresses.
                second_tuple_list.append(["Take off " + clothing.name + ".",clothing])
        second_tuple_list.append(["Go back to fucking her.","Finish"])
        strip_choice = renpy.display_menu(second_tuple_list,True,"Choice")

    if not strip_choice == "Finish":
        $ test_outfit = the_person.outfit.get_copy()
        $ test_outfit.remove_clothing(strip_choice)
        if the_person.judge_outfit(test_outfit):
            $ the_person.draw_animated_removal(strip_choice)
            $ renpy.say("", "You pull her " + strip_choice.name + " off, dropping it to the ground.")
            $ renpy.call("strip_menu", the_person) #TODO: Girl sometimes interupts you to get you to keep going. Have to strip them down in segments.
        else:
            $ renpy.say("", "You start to pull off " + the_person.title + "'s " + strip_choice.name + " when she grabs your hand and stops you.")
            $ the_person.call_dialogue("strip_reject")
            $ renpy.call("strip_menu", the_person) #TODO: Girl sometimes interupts you to get you to keep going. Have to strip them down in segments.
    return

label examine_room(the_room):
    python:
        renpy.say("","You are at [the_room.name].") #Where are we right now?

        people_here = the_room.people #Format the names of people in the room with you so it looks nice.
        if len(people_here) == 0:
            room_names = "There's nobody else in the room with you."
        elif len(people_here) == 1:
            room_names = "The only other person in the room with you is "
            room_names += people_here[0].name
            room_names += "."
        elif len(people_here) == 2:
            room_names = "Inside the room you see "
            room_names += people_here[0].name
            room_names += " and "
            room_names += people_here[1].name
            room_names += "."
        elif len(people_here) >2 and len(people_here) < 6:
            room_names = "Inside the room you see "
            for person in people_here[0:len(people_here)-2]:
                room_names += person.name
                room_names += ", "
            last_person = people_here[len(people_here)-1].name
            room_names += "and "
            room_names += last_person
            room_names += " among other people."
        else:
            room_names = "The room is filled with people."

        renpy.say("",room_names) ##This is the actual print statement!!

        connections_here = the_room.connections # Now we format the output for the connections so that it is readable.
        if len(connections_here) == 0:
            connect_names = "There are no exits from here. You're trapped!" #Shouldn't ever happen, hopefully."
        elif len(connections_here) == 1:
            connect_names = "From here your only option is to head to "
            connect_names += connections_here[0].name
            connect_names += "."
        elif len(connections_here) == 2:
            connect_names = "From here you can head to either "
            connect_names += connections_here[0].name
            connect_names += " or "
            connect_names += connections_here[1].name
            connect_names += "."
        else:
            connect_names = "From here you can go to "
            for place in connections_here[0:len(connections_here)-1]:
                connect_names += place.name
                connect_names += ", "
            last_place = connections_here[len(connections_here)-1].name
            connect_names += "and "
            connect_names += last_place
            connect_names += "."
        renpy.say("",connect_names) ##This is the actual print statement!!

    "That's all there is to see nearby."

    return

label examine_person(the_person):
    #Take a close look and figure out their physical attributes (tit size, ass size?, hair colour, hair style)

    python:
        string = "She has " + the_person.skin + " coloured skin, along with " + the_person.hair_colour[0] + " coloured hair and pretty " + the_person.eyes + " coloured eyes. She stands " + height_to_string(the_person.height) + " tall."
        renpy.say("",string)

        outfit_top = the_person.outfit.get_upper_visible()
        outfit_bottom = the_person.outfit.get_lower_visible()
        string = ""

        if len(outfit_top) == 0: ##ie. is naked
            string += "She's wearing nothing at all on top, with her nice " + the_person.tits + " sized tits on display for you."
        elif len(outfit_top) == 1:
            string += "She's wearing a " + outfit_top[0].name + " with her nice " + the_person.tits + " sized tits underneath."
        elif len(outfit_top) == 2:
            string += "She's wearing a " + outfit_top[1].name + " with a " + outfit_top[0].name + " underneath. Her tits look like they're " + the_person.tits + "'s."
        elif len(outfit_top) == 3:
            string += "She's wearing a " + outfit_top[2].name + " with a " + outfit_top[1].name + " and " + outfit_top[0].name + " underneath. Her tits look like they're " + the_person.tits + "'s."
        renpy.say("",string)

        string = ""
        if len(outfit_bottom) == 0: #naked
            string += "Her legs are completely bare, and you have a clear view of her pussy."
        elif len(outfit_bottom) == 1:
            string += "She's also wearing " + outfit_bottom[0].name + " below."
            if not outfit_bottom[0].hide_below:
                string += " You can see her pussy underneath."
        elif len(outfit_bottom) == 2:
            string += "She's also wearing " + outfit_bottom[0].name + " below, with " + outfit_bottom[1].name +  " visible below."
            if not outfit_bottom[1].hide_below:
                string += " You can see her pussy underneath."
        renpy.say("",string)
        title = mc.business.get_employee_title(the_person)
        if title == "Researcher":
            renpy.say("", the_person.title + " currently works in your research department.")
        elif title == "Marketing":
            renpy.say("", the_person.title + " currently works in your marketing department.")
        elif title == "Supply":
            renpy.say("", the_person.title + " currently works in your supply procurement department.")
        elif title == "Production":
            renpy.say("", the_person.title + " currently works in your production department.")
        elif title == "Human Resources":
            renpy.say("", the_person.title + " currently works in your human resources department.")
        else:
            renpy.say("", the_person.title + " does not currently work for you.")

    return

label give_serum(the_person):
    call screen serum_inventory_select_ui(mc.inventory)
    if not _return == "None":
        $ the_serum = _return
        "You decide to give [the_person.title] a dose of [the_serum.name]."
        $ mc.inventory.change_serum(the_serum,-1)
        $ the_person.give_serum(copy.copy(the_serum)) #use a copy rather than the main class, so we can modify and delete the effects without changing anything else.
        return True
    else:
        "You decide not to give [the_person.title] anything."
        return False

label sleep_action_description: #REMEMBER TO UPDATE THE SLEEP QUICK BUTTON ON THE MAIN UI, IT DOES NOT TOUCH THIS FUNCTION IN ANY WAY!
    "You go to bed after a hard days work."
    call advance_time from _call_advance_time
    return

label faq_action_description:
    call faq_loop from _call_faq_loop_2
    return

label hr_work_action_description:
    $ mc.business.player_hr()
    call advance_time from _call_advance_time_1
    return

label research_work_action_description:
    $ mc.business.player_research()
    call advance_time from _call_advance_time_2
    return

label supplies_work_action_description:
    $ mc.business.player_buy_supplies()
    call advance_time from _call_advance_time_3
    return

label market_work_action_description:
    $ mc.business.player_market()
    call advance_time from _call_advance_time_4

    return

label production_work_action_description:
    $ mc.business.player_production()
    call advance_time from _call_advance_time_5
    return

label interview_action_description:
    $ count = 3 #Num of people to generate, by default is 3. Changed with some policies
    if recruitment_batch_three_policy.is_owned():
        $ count = 10
    elif recruitment_batch_two_policy.is_owned():
        $ count = 6
    elif recruitment_batch_one_policy.is_owned():
        $ count = 4

    $ interview_cost = 50
    "Bringing in [count] people for an interview will cost $[interview_cost]. Do you want to spend time interviewing potential employees?"
    menu:
        "Yes, I'll pay the cost. -$[interview_cost]":
            $ mc.business.funds += -interview_cost
            $ renpy.scene("Active")
            hide screen main_ui #NOTE: We have to hide all of these screens because we are using a fake (aka. non-screen) background for this. We're doing that so we can use the normal draw_person call for them.
            hide screen phone_hud_ui
            hide screen business_ui
            hide screen goal_hud_ui
            python:
                candidates = []

                for x in range(0,count+1): #NOTE: count is given +1 because the screen tries to pre-calculate the result of button presses. This leads to index out-of-bounds, unless we pad it with an extra character (who will not be reached).
                    candidates.append(make_person())

                reveal_count = 0
                reveal_sex = False
                if recruitment_knowledge_one_policy.is_owned():
                    reveal_count += 2
                if recruitment_knowledge_two_policy.is_owned():
                    reveal_count += 2
                if recruitment_knowledge_three_policy.is_owned():
                    reveal_count += 1
                    reveal_sex = True
                if recruitment_knowledge_four_policy.is_owned():
                    reveal_count += 1


                for a_candidate in candidates:
                    for x in __builtin__.range(0,reveal_count): #Reveal all of their opinions based on our policies.
                        a_candidate.discover_opinion(a_candidate.get_random_opinion(include_known = False, include_sexy = reveal_sex),add_to_log = False) #Get a random opinion and reveal it.

                show_candidate(candidates[0]) #Show the first candidate, updates are taken care of by actions within the screen.

            show bg paper_menu_background #Show a paper background for this scene.
            call screen interview_ui(candidates,count)
            $ renpy.scene()
            show screen phone_hud_ui
            show screen business_ui
            show screen goal_hud_ui
            show screen main_ui
            $ renpy.scene("Active")
            $ renpy.show(mc.location.name,what=mc.location.background_image)
            if not _return == "None":
                $ new_person = _return
                $ new_person.event_triggers_dict["employed_since"] = day
                $ mc.business.listener_system.fire_event("new_hire", the_person = new_person)
                $ new_person.special_role.append(employee_role)
                "You complete the nessesary paperwork and hire [_return.name]. What division do you assign them to?"
                menu:
                    "Research and Development.":
                        $ mc.business.add_employee_research(new_person)
                        $ mc.business.r_div.add_person(new_person)
                        $ new_person.set_work([1,2,3], mc.business.r_div)

                    "Production.":
                        $ mc.business.add_employee_production(new_person)
                        $ mc.business.p_div.add_person(new_person)
                        $ new_person.set_work([1,2,3], mc.business.p_div)

                    "Supply Procurement.":
                        $ mc.business.add_employee_supply(new_person)
                        $ mc.business.s_div.add_person(new_person)
                        $ new_person.set_work([1,2,3], mc.business.s_div)

                    "Marketing.":
                        $ mc.business.add_employee_marketing(new_person)
                        $ mc.business.m_div.add_person(new_person)
                        $ new_person.set_work([1,2,3], mc.business.m_div)

                    "Human Resources.":
                        $ mc.business.add_employee_hr(new_person)
                        $ mc.business.h_div.add_person(new_person)
                        $ new_person.set_work([1,2,3], mc.business.h_div)

                python: #Establish their titles. TODO: Have this kind of stuff handled in an interview scene.
                    new_person.set_title(get_random_title(new_person))
                    new_person.set_possessive_title(get_random_possessive_title(new_person))
                    new_person.set_mc_title(get_random_player_title(new_person))

            else:
                "You decide against hiring anyone new for now."

            $ candidates = None # Release variables
            call advance_time from _call_advance_time_6
        "Nevermind.":
            $ temp = 0 #NOTE: just here so that this isn't technically an empty block.
    return

label serum_design_action_description:
    $counter = len(list_of_traits)
    hide screen main_ui
    hide screen phone_hud_ui
    hide screen business_ui
    call screen serum_design_ui(SerumDesign(),[]) #This will return the final serum design, or None if the player backs out.
    $ my_return_serum = _return

    show screen phone_hud_ui
    show screen business_ui
    show screen main_ui
    if not my_return_serum == "None":
        $ name = renpy.input("Please give this serum design a name.")
        $ my_return_serum.name = name
        $ mc.business.add_serum_design(my_return_serum)
        $ mc.business.listener_system.fire_event("new_serum", the_serum = my_return_serum)
        call advance_time from _call_advance_time_7
    else:
        "You decide not to spend any time designing a new serum type."
    return

label research_select_action_description:
    hide screen main_ui
    hide screen phone_hud_ui
    hide screen business_ui
    call screen serum_select_ui
    show screen phone_hud_ui
    show screen business_ui
    show screen main_ui
    if not _return == "None":
        $mc.business.set_serum_research(_return)
        "You change your research to [_return.name]."
    else:
        "You decide to leave your labs current research topic as it is."
    return

label production_select_action_description: #TODO: Change this to allow you to select which line of serum you are changing!
    hide screen main_ui
    hide screen phone_hud_ui
    hide screen business_ui
    call screen serum_production_select_ui
    show screen phone_hud_ui
    show screen business_ui
    show screen main_ui
    return

label trade_serum_action_description:
    "You step into the stock room to check what you currently have produced."
    hide screen main_ui
    hide screen phone_hud_ui
    hide screen business_ui
    $ renpy.block_rollback()
    call screen serum_trade_ui(mc.inventory,mc.business.inventory)
    $ renpy.block_rollback()
    show screen phone_hud_ui
    show screen business_ui
    show screen main_ui
    return

label sell_serum_action_description:
    "You look through your stock of serum, marking some to be sold by your marketing team."
    hide screen main_ui
    hide screen phone_hud_ui
    hide screen business_ui
    $ renpy.block_rollback()
    call screen serum_trade_ui(mc.business.inventory,mc.business.sale_inventory,"Production Stockpile","Sales Stockpile")
    $ renpy.block_rollback()

    show screen phone_hud_ui
    show screen business_ui
    show screen main_ui
    return

label review_designs_action_description:
    hide screen main_ui
    hide screen phone_hud_ui
    hide screen business_ui
    $ renpy.block_rollback() #Block rollback to prevent any strange issues with references being lost.
    call screen review_designs_screen()
    $ renpy.block_rollback()

    show screen phone_hud_ui
    show screen business_ui
    show screen main_ui
    return


label pick_supply_goal_action_description:
    $ amount = renpy.input("How many units of serum supply would you like your supply procurement team to keep stocked?")
    $ amount = amount.strip()

    while not amount.isdigit():
        $ amount = renpy.input("Please put in an integer value.")

    $ amount = int(amount)
    $ mc.business.supply_goal = amount
    if amount <= 0:
        "You tell your team to keep [amount] units of serum supply stocked. They question your sanity, but otherwise continue with their work. Perhaps you should use a positive number."
    else:
        "You tell your team to keep [amount] units of serum supply stocked."

    return

label policy_purchase_description:
    call screen policy_selection_screen()
    return

label head_researcher_select_description:
    call screen employee_overview(white_list = mc.business.research_team, person_select = True)
    $ new_head = _return
    $ mc.business.head_researcher = new_head
    $ new_head.special_role.append(head_researcher)
    return

label set_uniform_description:
    #First, establish the maximums the uniform can reach.
    if maximal_arousal_uniform_policy.is_owned():
        $slut_limit = 999 #ie. no limit at all.
        $underwear_limit = 999
        $limited_to_top = False
    elif corporate_enforced_nudity_policy.is_owned():
        $slut_limit = 80
        $underwear_limit = 999
        $limited_to_top = False
    elif minimal_coverage_uniform_policy.is_owned():
        $slut_limit = 60
        $underwear_limit = 15
        $limited_to_top = False
    elif reduced_coverage_uniform_policy.is_owned():
        $slut_limit = 40
        $underwear_limit = 10
        $limited_to_top = False
    elif casual_uniform_policy.is_owned():
        $slut_limit = 25
        $underwear_limit = 0
        $limited_to_top = True
    elif relaxed_uniform_policy.is_owned():
        $slut_limit = 15
        $underwear_limit = 0
        $limited_to_top = True
    elif strict_uniform_policy.is_owned():
        $slut_limit = 5
        $underwear_limit = 0
        $limited_to_top = True
    else:
        $slut_limit = 0
        $underwear_limit = 0
        $limited_to_top = True

    #Some quick holding variables to store the options picked.
    $ selected_div = None
    $ uniform_mode = None
    $ uniform_type = None
    menu:
        "Add a complete outfit." if not limited_to_top:
            $ uniform_mode = "full"

        "Add a complete outfit.\n{size=22}Requires: Casual Uniform Policy{/size} (disabled)" if limited_to_top:
            pass

        "Add an overwear set.":
            $ uniform_mode = "over"

        "Add an underwear set." if not limited_to_top:
            $ uniform_mode = "under"

        "Add an underwear set.\n{size=22}Rquires: Casual Uniform Policy{/size} (disabled)" if limited_to_top:
            pass

        "Remove a uniform or set.":
            $ uniform_mode = "delete"


    menu:
        "Company Wide Uniforms.\n{size=22}Can be worn by everyone.{/size}": #Get the wardrobe we are going to be modifying.
            $ selected_div = mc.business.all_uniform

        "R&D Uniforms.":
            $ selected_div = mc.business.r_uniform

        "Production Uniforms.":
            $ selected_div = mc.business.p_uniform

        "Supply Procurement Uniforms.":
            $ selected_div = mc.business.s_uniform

        "Marketing Uniforms.":
            $ selected_div = mc.business.m_uniform

        "Human Resources Uniforms.":
            $ selected_div = mc.business.h_uniform

    if uniform_mode == "delete":
        call screen outfit_delete_manager(selected_div) #Calls the wardrobe screen and lets teh player delete whatever they want.

    else:
        if uniform_mode == "full":
            call screen outfit_select_manager(slut_limit = slut_limit)
            $ new_outfit = _return
            if new_outfit == "No Return":
                return


            $ mc.business.listener_system.fire_event("add_uniform", the_outfit = new_outfit, the_type = "full")
            $ selected_div.add_outfit(new_outfit.get_copy())

        elif uniform_mode == "under":
            call screen outfit_select_manager(slut_limit = underwear_limit, show_outfits = False, show_underwear = True, show_overwear = False)
            $ new_outfit = _return
            if new_outfit == "No Return":
                return

            $ mc.business.listener_system.fire_event("add_uniform", the_outfit = new_outfit, the_type = "under")
            $ selected_div.add_underwear_set(new_outfit.get_copy())

        else: #uniform_mode == "over":
            call screen outfit_select_manager(slut_limit = slut_limit, show_outfits = False, show_underwear = False, show_overwear = True)
            $ new_outfit = _return
            if new_outfit == "No Return":
                return

            $ mc.business.listener_system.fire_event("add_uniform", the_outfit = new_outfit, the_type = "over")
            $ selected_div.add_overwear_set(new_outfit.get_copy())


    return

label set_serum_description: #TODO: Add a special screen for all of this instead of doing it through menus
    "Which divisions would you like to set a daily serum for?"
    $ selected_div = None
    $ selected_serum = None

    menu:
        "All.":
            $ selected_div = "All"

        "Research and Development.":
            $ selected_div = "R"

        "Production.":
            $ selected_div = "P"

        "Supply Procurement.":
            $ selected_div = "S"

        "Marketing.":
            $ selected_div = "M"

        "Human Resources.":
            $ selected_div = "H"

    menu:
        "Pick a new serum.":
            call screen serum_inventory_select_ui(mc.business.inventory)
            $ selected_serum = _return

        "Clear existing serum.":
            $ selected_serum = None

    if selected_serum == "None": #IF we didn't select an actual serum, just return and don't chagne anything.
        return

    if selected_div == "All":
        $ mc.business.m_serum = selected_serum
        $ mc.business.p_serum = selected_serum
        $ mc.business.r_serum = selected_serum
        $ mc.business.s_serum = selected_serum
        $ mc.business.h_serum = selected_serum

    elif selected_div == "R":
        $ mc.business.r_serum = selected_serum

    elif selected_div == "P":
        $ mc.business.p_serum = selected_serum

    elif selected_div == "S":
        $ mc.business.s_serum = selected_serum

    elif selected_div == "M":
        $ mc.business.m_serum = selected_serum

    elif selected_div == "H":
        $ mc.business.h_serum = selected_serum

    return

label advance_time:
    # 1) Turns are processed _before_ the time is advanced.
    # 1a) crises are processed if they are triggered.
    # 2) Time is advanced, day is advanced if required.
    # 3) People go to their next intended location.
    # Note: This will require breaking people's turns into movement and actions.
    # Then: Add research crisis when serum is finished, requiring additional input from the player and giving the chance to test a serum on the R&D staff.

    #$mc.can_skip_time = False #Ensure the player cannot skip time during crises.

    python:
        people_to_process = [] #This is a master list of turns of need to process, stored as tuples [character,location]. Used to avoid modifying a list while we iterate over it, and to avoid repeat movements.
        for place in list_of_places:
            for people in place.people:
                people_to_process.append([people,place])

    python:
        for (people,place) in people_to_process: #Run the results of people spending their turn in their current location.
            people.run_turn()
        mc.business.run_turn()
        mc.run_turn()


    #We make sure that all mandatory crises are run here. Mandatory crises always trigger as soon as they are able, possibly with multiple crises triggering in a single turn.
    $ count = 0
    $ max = len(mc.business.mandatory_crises_list)
    $ clear_list = []
    while count < max: #We need to keep this in a renpy loop, because a return call will always return to the end of an entire python block.
        $crisis = mc.business.mandatory_crises_list[count]
        if crisis.is_action_enabled():
            $ crisis.call_action()
            $ renpy.scene("Active")
            $ clear_list.append(crisis)
        $ count += 1
    $ renpy.show(mc.location.name,what=mc.location.background_image) #Make sure we're showing the correct background for our location, which might have been temporarily changed by a crisis.
    python: #Needs to be a different python block, otherwise the rest of the block is not called when the action returns.
        for crisis in clear_list:
            mc.business.mandatory_crises_list.remove(crisis) #Clean up the list.


    #Once mandatory crises are managed we may or may not run a random crisis to keep things interesting.
    if renpy.random.randint(0,100) < 10: #ie. run a crisis 10% of the time.
        python:
            possible_crisis_list = []
            for crisis in crisis_list:
                if crisis[0].is_action_enabled(): #Get the first element of the weighted tuple, the action.
                    possible_crisis_list.append(crisis) #Build a list of valid crises from ones that pass their requirement.

        $ the_crisis = get_random_from_weighted_list(possible_crisis_list)
        if the_crisis:
            $ the_crisis.call_action()

    $ renpy.scene("Active")
    $ renpy.scene()
    $ renpy.show(mc.location.name,what=mc.location.background_image) #Make sure we're showing the correct background for our location, which might have been temporarily changed by a crisis.
    show screen business_ui

    if time_of_day == 4: ##First, determine if we're going into the next chunk of time. If we are, advance the day and run all of the end of day code.
        python:
            for (people,place) in people_to_process:
                people.run_day()

        $ mc.run_day()
        $ mc.business.run_day()

        $ time_of_day = 0
        $ day += 1

        if mc.business.funds < 0:
            $ mc.business.bankrupt_days += 1
            if mc.business.bankrupt_days == mc.business.max_bankrupt_days:
                $ renpy.say("","With no funds to pay your creditors you are forced to close your business and auction off all of your materials at a fraction of their value. Your story ends here.")
                $ renpy.full_restart()
            else:
                $ days_remaining = mc.business.max_bankrupt_days-mc.business.bankrupt_days
                $ renpy.say("","Warning! Your company is losing money and unable to pay salaries or purchase necessary supplies! You have [days_remaining] days to restore yourself to positive funds or you will be foreclosed upon!")
        else:
            $ mc.business.bankrupt_days = 0

        call screen end_of_day_update() # We have to keep this outside of a python block, because the renpy.call_screen function does not properly fade out the text bar.
        $ mc.business.clear_messages()

        #Now we run mandatory morning crises. Nearly identical to normal crises, but these always trigger at the start of the day (ie when you wake up and before you have control of your character.)
        $ count = 0
        $ max = len(mc.business.mandatory_morning_crises_list)
        $ clear_list = []
        while count < max: #We need to keep this in a renpy loop, because a return call will always return to the end of an entire python block.
            $crisis = mc.business.mandatory_morning_crises_list[count]
            if crisis.is_action_enabled():
                $ crisis.call_action()
                $ renpy.scene("Active")
                $ clear_list.append(crisis)
            $ count += 1
        $ renpy.show(mc.location.name,what=mc.location.background_image) #Make sure we're showing the correct background for our location, which might have been temporarily changed by a crisis.
        python: #Needs to be a different python block, otherwise the rest of the block is not called when the action returns.
            for crisis in clear_list:
                mc.business.mandatory_morning_crises_list.remove(crisis) #Clean up the list.


        if renpy.random.randint(0,100) < 5: # We run morning crises 5% of all mornings
            python:
                possible_morning_crises = []
                for crisis in morning_crisis_list:
                    if crisis[0].is_action_enabled(): #Get the first element of the weighted tuple, the action.
                        possible_morning_crises.append(crisis) #Build a list of valid crises from ones that pass their requirement.
            $ the_morning_crisis = get_random_from_weighted_list(possible_morning_crises)
            if the_morning_crisis:
                $ the_morning_crisis.call_action()

    else:
        $ time_of_day += 1 ##Otherwise, just run the end of day code.

    if time_of_day == 1 and daily_serum_dosage_policy.is_owned(): #It is the start of the work day, give everyone their daily dose of serum
        $ mc.business.give_daily_serum()

    python:
        for (people,place) in people_to_process: #Now move everyone to where the should be in the next time chunk. That may be home, work, etc.
            people.run_move(place)

    #$mc.can_skip_time = True #Now give the player the ability to skip time again, because they should be back in control.
    return

init -1 python:
    ##Actions##
    hr_work_action = Action("Spend time orgainizing your business. {image=gui/heart/Time_Advance.png}",hr_work_action_requirement,"hr_work_action_description",
        menu_tooltip = "Raises business efficency, which drops over time based on how many employees the business has.\n+3*Charisma + 2*Skill + 1*Intelligence + 5 Efficency.")
    research_work_action = Action("Spend time researching in the lab. {image=gui/heart/Time_Advance.png}",research_work_action_requirement,"research_work_action_description",
        menu_tooltip = "Contributes research points towards the currently selected project.\n+3*Intelligence + 2*Skill + 1*Focus + 10 Research Points.")
    supplies_work_action = Action("Spend time ordering supplies. {image=gui/heart/Time_Advance.png}",supplies_work_action_requirement,"supplies_work_action_description",
        menu_tooltip = "Purchase serum supply at the cost of $1 per unit of supplies. When producing serum every production point requires one unit of serum.\n+3*Focus + 2*Skill + 1*Charisma + 10 Serum Supply.")
    market_work_action = Action("Spend time shipping doses of serum marked for sale. {image=gui/heart/Time_Advance.png}",market_work_action_requirement,"market_work_action_description",
        menu_tooltip = "Sells serum that has been marked for sale. Mark serum manually from the office or set an autosell threshold in production.\n3*Charisma + 2*Skill + 1*Focus + 5 Serum Doses Sold.")
    production_work_action = Action("Spend time producing serum in the lab. {image=gui/heart/Time_Advance.png}",production_work_action_requirement,"production_work_action_description",
        menu_tooltip = "Produces serum from raw materials. Each production point of serum requires one unit if supply, which can be purchased from your office.\n+3*Focus + 2*Skill + 1*Intelligence + 10 Production Points.")

    interview_action = Action("Hire someone new. {image=gui/heart/Time_Advance.png}", interview_action_requirement,"interview_action_description",
        menu_tooltip = "Look through the resumes of several candidates. More information about a candidate can be revealed by purchasing new business policies.")
    design_serum_action = Action("Create a new serum design. {image=gui/heart/Time_Advance.png}", serum_design_action_requirement,"serum_design_action_description",
        menu_tooltip = "Combine serum traits to create a new design. Once a design has been created it must be researched before it can be put into production.")
    pick_research_action = Action("Assign Research Project.", research_select_action_requirement,"research_select_action_description",
        menu_tooltip = "Pick the next research topic for your R&D division. Serum designs must be researched before they can be put into production.")
    pick_production_action = Action("Set production settings.", production_select_action_requirement,"production_select_action_description",
        menu_tooltip = "Decide what serum designs are being produced. Production is divided between multiple factory lines, and auto sell thresholds can be set to automatically flag serum for sale.")
    pick_supply_goal_action = Action("Set the amount of supply you would like to maintain.", pick_supply_goal_action_requirement,"pick_supply_goal_action_description",
        menu_tooltip = "Set a maximum amount of serum you and your staff will attempt to purchase.")
    policy_purhase_action = Action("Purchase new business policies.", policy_purchase_requirement,"policy_purchase_description",
        menu_tooltip = "New business policies changes the way your company runs and expands your control over it. Once purchased business policies are always active.")
    set_head_researcher_action = Action("Select a Head Researcher.", head_researcher_select_requirement, "head_researcher_select_description",
        menu_tooltip = "Pick a member of your R&D staff to be your head researcher. A head resercher with a high intelligence score will increase the amount of research produced by the entire division.")

    trade_serum_action = Action("Access the serum production stockpile.", trade_serum_action_requirement, "trade_serum_action_description",
        menu_tooltip = "Move serum to and from your personal inventory. You can only use serum you are carrying with you.")
    sell_serum_action = Action("Mark serum to be sold.", sell_serum_action_requirement, "sell_serum_action_description",
        menu_tooltip = "Decide what serum should be available for sale. It can then be sold from the marketing division. Setting an autosell threshold in the production department can do this automatically.")
    review_designs_action = Action("Review serum designs.", review_designs_action_requirement, "review_designs_action_description",
        menu_tooltip = "Shows all existing serum designs and allows you to delete any you no longer desire.")

    sleep_action = Action("Go to sleep for the night. {image=gui/heart/Time_Advance.png}",sleep_action_requirement,"sleep_action_description",
        menu_tooltip = "Go to sleep and advance time to the next day. Night time counts as three time chunks when calculating serum durations.")
    faq_action = Action("Check the FAQ.",faq_action_requirement,"faq_action_description",
        menu_tooltip = "Answers to frequently asked questions about Lab Rats 2.")

    change_titles_action = Action("Talk about what you call each other.", requirement = change_titles_requirement, effect = "change_titles_person", 
        menu_tooltip = "Manage how you refer to this girl and tell her how she should refer to you. Differnet combinations of stats, roles, and personalityes unlock different titles.")
    small_talk_action = Action("Make small talk. {image=gui/heart/Time_Advance.png}", requirement = small_talk_requirement, effect = "small_talk_person", 
        menu_tooltip = "A pleasant chat about your likes and dislikes. A good way to get to know someone and the first step to building a lasting relationship. Provides a chance to study the effects of active serum traits and raise their mastery level.")
    compliment_action = Action("Compliment her. {image=gui/heart/Time_Advance.png}", requirement = compliment_requirement, effect = "compliment_person",
        menu_tooltip = "Lay the charm on thick and heavy. A great way to build a relationship, and every girl is happy to recieve a compliment! Provides a chance to study the effects of active serum traits and raise their mastery level.")
    flirt_action = Action("Flirt with her. {image=gui/heart/Time_Advance.png}", requirement = flirt_requirement, effect = "flirt_person",
        menu_tooltip = "A conversation filled with innuendo and double entendre. Both improves your relationship with a girl and helps make her a little bit sluttier. Provides a chance to study the effects of active serum traits and raise their mastery level.")
    date_action = Action("Ask her on a date.", requirement = date_requirement, effect = "date_person",
        menu_tooltip = "Ask her out on a date. The more you impress her the closer you'll grow. If you play your cards right you might end up back at her place.")

    wardrobe_change_action = Action("Ask to change her wardrobe.", requirement = wardrobe_change_requirment, effect = "wardrobe_change_label",
        menu_tooltip = "Add and remove outfits from her wardrobe, or ask her to put on a specific outfit.")
    serum_give_action = Action("Try to give her a dose of serum.", requirement = serum_give_requirement, effect = "serum_give_label",
        menu_tooltip = "Demand she take a dose, ask her politely, or just try and slip it into something she'll drink. Failure may result in her trusting you less or being immediately unhappy.")
    seduce_action = Action("Try to seduce her.", requirement = seduce_requirement, effect = "seduce_label",
        menu_tooltip = "Try and seduce her right here and now. Love, sluttiness, obedience, and your own charisma all play a factor in how likely she is to be seduced.")

    ##Actions unlocked by policies##
    set_uniform_action = Action("Manage Employee Uniforms.",set_uniform_requirement,"set_uniform_description")
    set_serum_action = Action("Set Daily Serum Doses.",set_serum_requirement,"set_serum_description")

    ## Misc Actions
    dinner_action = Action("Dinner date", dinner_date_requirement, "dinner_date") #it happens on a friday, so day%7 == 4
    mom_weekly_pay_action = Action("mom weekly pay", mom_weekly_pay_requirement, "mom_weekly_pay_label")

    test_action = Action("This is a test.", faq_action_requirement, "faq_action_description")

label create_test_variables(character_name,business_name,last_name,stat_array,skill_array,_sex_array,max_num_of_random=4): #Gets all of the variables ready. TODO: Move some of this stuff to an init block?
    $ list_of_traits = [] #List of serum traits that can be used. Established here so they play nice with rollback, saving, etc.
    $ list_of_side_effects = [] #List of special serum traits that are reserved for bad results.
    $ list_of_places = [] #By having this in an init block it may be set to null each time the game is reloaded, because the initialization stuff below is only called once.

    call instantiate_serum_traits() from _call_instantiate_serum_traits #Creates all of the default LR2 serum traits. TODO: Create a mod loading list that has lables that can be externally added and called here.
    call instantiate_side_effect_traits() from _call_instantiate_side_effect_traits

    python:
        ##PC's Home##
        hall = Room("main hall","Home",[],house_background,[],[],[],False,[3,3])
        bedroom = Room("your bedroom", "Your Bedroom",[],bedroom_background,[],[],[sleep_action,faq_action],False,[3,2])
        lily_bedroom = Room("Lily's bedroom", "Lily's Bedroom",[],bedroom_background,[],[],[],False,[2,3])
        mom_bedroom = Room("your mom's bedroom", "Mom's Bedroom",[], bedroom_background,[],[],[],False,[2,4])
        kitchen = Room("kitchen", "Kitchen",[],kitchen_background,[],[],[],False,[3,4])


        ##PC's Work##
        lobby = Room(business_name + " lobby",business_name + " Lobby",[],office_background,[],[],[],False,[11,3], tutorial_label = "lobby_tutorial_intro")
        office = Room("main office","Main Office",[],office_background,[],[],[policy_purhase_action,hr_work_action,supplies_work_action,interview_action,sell_serum_action,pick_supply_goal_action,set_uniform_action,set_serum_action],False,[11,2], tutorial_label = "office_tutorial_intro")
        m_division = Room("marketing division","Marketing Division",[],office_background,[],[],[market_work_action],False,[12,3], tutorial_label = "marketing_tutorial_intro")
        rd_division = Room("R&D division","R&D Division",[],lab_background,[],[],[research_work_action,design_serum_action,pick_research_action,review_designs_action,set_head_researcher_action],False,[12,4], tutorial_label = "research_tutorial_intro")
        p_division = Room("Production division", "Production Division",[],office_background,[],[],[production_work_action,pick_production_action,trade_serum_action],False,[11,4], tutorial_label = "production_tutorial_intro")


        ##Connects all Locations##
        downtown = Room("downtown","Downtown",[],outside_background,[],[],[],True,[6,4])

        ##A mall, for buying things##
        mall = Room("mall","Mall",[],mall_background,[],[],[],True,[8,2])
        gym = Room("gym","Gym",[],mall_background,[],[],[],True,[7,1])
        home_store = Room("home improvement store","Home Improvement Store",[],mall_background,[],[],[],True,[8,1])
        sex_store = Room("sex store","Sex Store",[],mall_background,[],[],[],True,[9,2])
        clothing_store = Room("clothing store","Clothing Store",[],mall_background,[],[],[],True,[8,3])
        office_store = Room("office supply store","Office Supply Store",[],mall_background,[],[],[],True,[9,1])


        ##Other Locations##
        aunt_apartment = Room("Rebecca's Apartment", "Rebecca's Apartment", [], house_background, [], [], [], False, [4, 2], None, False)
        aunt_bedroom = Room("Rebecca's bedroom", "Rebecca's Bedroom", [], bedroom_background, [], [], [], False, [3, 1], None, False)
        cousin_bedroom = Room("Gabrielle's bedroom", "Gabrielle's Bedroom", [], bedroom_background, [], [], [], False, [4,1], None, False)

        university = Room("university Campus", "University Campus", [], campus_background, [], [], [], False, [9,5], None, False)

        ##PC starts in his bedroom##
        main_business = Business(business_name, m_division, p_division, rd_division, office, office)
        mc = MainCharacter(bedroom,character_name,last_name,main_business,stat_array,skill_array,_sex_array)
        mc.generate_goals()

        generate_premade_list() # Creates the list with all the premade characters for the game in it. Without this we both break the policies call in create_random_person, and regenerate the premade list on each restart.

        ##Keep a list of all the places##
        list_of_places.append(bedroom)
        list_of_places.append(lily_bedroom)
        list_of_places.append(mom_bedroom)
        list_of_places.append(kitchen)
        list_of_places.append(hall)

        list_of_places.append(lobby)
        list_of_places.append(office)
        list_of_places.append(rd_division)
        list_of_places.append(p_division)
        list_of_places.append(m_division)

        list_of_places.append(downtown)

        list_of_places.append(office_store)
        list_of_places.append(clothing_store)
        list_of_places.append(sex_store)
        list_of_places.append(home_store)
        list_of_places.append(gym)
        list_of_places.append(mall)

        list_of_places.append(aunt_apartment)
        list_of_places.append(aunt_bedroom)
        list_of_places.append(cousin_bedroom)
        list_of_places.append(university)

        hall.link_locations_two_way(bedroom)
        hall.link_locations_two_way(kitchen)
        hall.link_locations_two_way(lily_bedroom)
        hall.link_locations_two_way(mom_bedroom)

        downtown.link_locations_two_way(hall)
        downtown.link_locations_two_way(lobby)
        downtown.link_locations_two_way(mall)
        downtown.link_locations_two_way(aunt_apartment)
        downtown.link_locations_two_way(university)

        aunt_apartment.link_locations_two_way(aunt_bedroom)
        aunt_apartment.link_locations_two_way(cousin_bedroom)

        lobby.link_locations_two_way(office)
        lobby.link_locations_two_way(rd_division)
        lobby.link_locations_two_way(m_division)
        lobby.link_locations_two_way(p_division)

        mall.link_locations_two_way(office_store)
        mall.link_locations_two_way(clothing_store)
        mall.link_locations_two_way(sex_store)
        mall.link_locations_two_way(home_store)
        mall.link_locations_two_way(gym)

        for room in [bedroom, lily_bedroom, mom_bedroom, aunt_bedroom, cousin_bedroom]:
            room.add_object(make_wall())
            room.add_object(make_floor())
            room.add_object(make_bed())
            room.add_object(make_window())

        kitchen.add_object(make_wall())
        kitchen.add_object(make_floor())
        kitchen.add_object(make_chair())
        kitchen.add_object(make_table())

        hall.add_object(make_wall())
        hall.add_object(make_floor())

        lobby.add_object(make_wall())
        lobby.add_object(make_floor())
        lobby.add_object(make_chair())
        lobby.add_object(make_desk())
        lobby.add_object(make_window())

        office.add_object(make_wall())
        office.add_object(make_floor())
        office.add_object(make_chair())
        office.add_object(make_desk())
        office.add_object(make_window())

        rd_division.add_object(make_wall())
        rd_division.add_object(make_floor())
        rd_division.add_object(make_chair())
        rd_division.add_object(make_desk())

        m_division.add_object(make_wall())
        m_division.add_object(make_floor())
        m_division.add_object(make_chair())
        m_division.add_object(make_desk())

        p_division.add_object(make_wall())
        p_division.add_object(make_floor())
        p_division.add_object(make_chair())
        p_division.add_object(make_desk())

        downtown.add_object(make_floor())

        university.add_object(make_grass())

        office_store.add_object(make_wall())
        office_store.add_object(make_floor())
        office_store.add_object(make_chair())

        clothing_store.add_object(make_wall())
        clothing_store.add_object(make_floor())

        sex_store.add_object(make_wall())
        sex_store.add_object(make_floor())

        home_store.add_object(make_wall())
        home_store.add_object(make_floor())
        home_store.add_object(make_chair())

        mall.add_object(make_wall())
        mall.add_object(make_floor())

        gym.add_object(make_wall())
        gym.add_object(make_floor())

        aunt_apartment.add_object(make_wall())
        aunt_apartment.add_object(make_floor())
        aunt_apartment.add_object(make_couch())
        aunt_apartment.add_object(make_table())
        aunt_apartment.add_object(make_chair())

        for place in list_of_places:
            if place.public:
                if not max_num_of_random == 0:
                    random_count = renpy.random.randint(1,max_num_of_random)
                else:
                    random_count = 0;
                for x in range(0,random_count):
                    place.add_person(create_random_person()) #We are using create_random_person instead of make_person because we want premade character bodies to be hirable instead of being eaten up by towns-folk.

        ##Global Variable Initialization##
        day = 0 ## Game starts on day 0.
        time_of_day = 0 ## 0 = Early morning, 1 = Morning, 2 = Afternoon, 3 = Evening, 4 = Night

    return
