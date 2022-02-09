init -2 python:
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

            self.m_div = m_div #The physical locations of all of the teams, so you can move to different offices in the future.
            self.p_div = p_div
            self.r_div = r_div
            self.s_div = s_div
            self.h_div = h_div

            # These wardrobes handle the department specific uniform stuff. A list of UniformOutfits is used to populate the uniform manager screen.
            #self.all_uniform = Wardrobe(self.name + " All Wardrobe")
            self.m_uniform = Wardrobe(self.name + " Marketing Wardrobe")
            self.p_uniform = Wardrobe(self.name + " Production Wardrobe")
            self.r_uniform = Wardrobe(self.name + " Research Wardrobe")
            self.s_uniform = Wardrobe(self.name + " Supply Wardrobe")
            self.h_uniform = Wardrobe(self.name + " HR Wardrobe")

            self.business_uniforms = [] #A list of UniformOutfits
            #self.all_uniform = Wardrobe(self.name + " Shared Uniform Wardrobe")

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
            self.company_model = None #A reference to the currnet company model. May be used for some events.

            self.max_employee_count = 5

            self.supply_count = 0
            self.supply_goal = 250
            self.auto_sell_threshold = None
            self.marketability = 0
            #self.production_points = 0 Use to be used to store partial progress on serum. is now stored in the assembly line array
            self.team_effectiveness = 100 #Ranges from 50 (Chaotic, everyone functions at 50% speed) to 200 (masterfully organized). Normal levels are 100, special traits needed to raise it higher.
            self.effectiveness_cap = 100 #Max cap, can be raised.

            self.research_tier = 0 #The tier of research the main charcter has unlocked with storyline events. 0 is starting, 3 is max.
            self.max_serum_tier = 0 #The tier of serum you can produce in your lab. Mirrors reasearch tiers.

            self.blueprinted_traits = [] #List of traits that we have built from trait blueprints.

            self.serum_designs = [] #Holds serum designs that you have researched.
            self.active_research_design = None #The current research (serum design or serum trait) the business is working on

            self.batch_size = 5 #How many serums are produced in each production batch

            self.recruitment_cost = 50


            self.inventory = SerumInventory()
            # Produciton lines now have their own class.
            self.production_lines = [] #Holds instances of Production Line. Default is 2, buying more production lines let's you produce serum designs in parallel (but no more than your default amount).
            self.production_lines.append(ProductionLine(self.inventory))
            self.production_lines.append(ProductionLine(self.inventory))

            self.max_active_contracts = 2
            self.active_contracts = []

            self.max_offered_contracts = 2
            self.offered_contracts = []


            self.policy_list = [] #This is a list of Policy objects.
            self.active_policy_list = [] #This is a list of currently active policies (vs just owned ones)

            self.message_list = [] #This list of strings is shown at the end of each day on the business update screen. Cleared each day.
            self.counted_message_list = {} #This is a dict holding the count of each message stored in it. Used when you want to have a message that is counted and the total shown at the end of the day.
            self.production_potential = 0 #How many production points the team was capable of
            self.supplies_purchased = 0
            self.production_used = 0 #How many production points were actually used to make something.
            self.research_produced = 0 #How much research the team produced today.
            self.sales_made = 0
            self.serums_sold = 0

            self.partial_clarity = 0.0 #Float used to store partial clarity produced by research until it can be given out as a full integer.

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

            self.market_reach = 100 #"market_reach" can be thought of as your total customr base.
            self.mental_aspect_sold = 0 #Customers only have so much need for serum, so as you sell aspects the price per aspect goes down. You need to increase your market reach to get that price back up.
            self.physical_aspect_sold = 0
            self.sexual_aspect_sold = 0
            self.medical_aspect_sold = 0

            self.default_aspect_price = 10 # THis is the starting price that most aspects are "worth".
            self.aspect_price_max_variance = 8 # This is the todal amount each aspect can be worht (ie no aspect is ever worth base more than 18 or less than 2).
            self.aspect_price_daily_variance = 2 #This is the +- amount the price of each apsect can fluctuate.


            self.mental_aspect_price = self.default_aspect_price #These are the actual current values of each aspect, which will vary from day to day
            self.physical_aspect_price = self.default_aspect_price
            self.sexual_aspect_price = self.default_aspect_price
            self.medical_aspect_price = self.default_aspect_price

            self.flaws_aspect_cost = -10 #NOTE: Flaws are a flat -10 each, _not_ reduced by amount sold.

            self.attention = 0 #Current attention.
            self.max_attention = 100 #If you end the day over this much attention you trigger a high attention event.
            self.attention_bleed = 10 #How much attention is burned each day,

            self.operating_costs = 0 #How much money is spent every work day just owning yoru lab.

            self.listener_system = ListenerManagementSystem()

            self.renew_contracts()

        def run_turn(self): #Run each time the time segment changes. Most changes are done here.
            if time_of_day == 1 and daily_serum_dosage_policy.is_active() and self.is_work_day(): #Not done on run_day because we want it to apply at the _start_ of the day.
                self.give_daily_serum()

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

            for person in self.market_team:
                if person in self.m_div.people:
                    if person.should_wear_uniform():
                        self.sale_progress(person.charisma,person.focus, person.market_skill, slut_modifier = person.outfit.slut_requirement) #If there is a uniform pass it's sluttiness along.
                    else:
                        self.sale_progress(person.charisma, person.focus, person.market_skill) #Otherwise their standard outfit provides no bonuses.
                    person.change_happiness(person.get_opinion_score("working")+person.get_opinion_score("marketing work"), add_to_log = False)

            self.do_autosale() #Mark extra serums to be sold by marketing.

            for policy in self.active_policy_list:
                policy.on_turn()

            #Compute efficiency drop
            for person in self.supply_team + self.research_team + self.production_team + self.market_team:
                if person in self.s_div.people + self.r_div.people + self.p_div.people + self.m_div.people: #Only people in the office lower effectiveness, no loss on weekends, not in for the day, etc.
                    self.change_team_effectiveness(-1)

            #Compute effiency rise from HR
            for person in self.hr_team:
                if person in self.h_div.people:
                    self.hr_progress(person.charisma,person.int,person.hr_skill)
                    person.change_happiness(person.get_opinion_score("working")+person.get_opinion_score("HR work"), add_to_log = False)

        def run_move(self):
            for policy in self.active_policy_list:
                policy.on_move()

        def run_day(self): #Run at the end of the day.
            self.attention += -self.attention_bleed
            if self.attention < 0:
                self.attention = 0

            if mc.business.is_work_day():
                cost = self.calculate_salary_cost() + self.operating_costs
                self.change_funds(-cost)

                if self.attention >= self.max_attention and not self.event_triggers_dict.get("attention_event_pending", False):
                    self.event_triggers_dict["attention_event_pending"] = True
                    self.mandatory_crises_list.append(Action("attention_event", attention_event_requirement, "attention_event"))

                for policy in self.active_policy_list:
                    policy.on_day()

                remove_list = []
                for contract in self.active_contracts:
                    remove_list = []
                    if contract.run_day():
                        remove_list.append(contract)
                        if contract.can_finish_contract():
                            contract.finish_contract()
                            self.add_normal_message("Contract " + contract.name + " was going to expire with product in inventory, completed automatically.")
                        else:
                            contract.abandon_contract()
                            self.add_normal_message("Contract " + contract.name + " has expired unfilled.")

                for removal in remove_list:
                    self.active_contracts.remove(removal)

            if day%7 == 6: #ie is Monday
                self.renew_contracts()
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

        def get_uniform_wardrobe(self,title): #Takes a title and returns the correct uniform for that division, if one exists. If it is None, returns false. TODO: get this working.
            if title == "Marketing":
                return self.m_uniform
            elif title == "Researcher":
                return self.r_uniform
            elif title == "Production":
                return self.p_uniform
            elif title == "Supply":
                return self.s_uniform
            elif title == "Human Resources":
                return self.h_uniform
            else:
                return None

        def get_uniform_wardrobe_for_person(self, the_person):
            return self.get_uniform_wardrobe(self.get_employee_title(the_person))

        def get_uniform_limits(self): #Returns three values: the max sluttiness of a full outfit, max sluttiness of an underwear set, and if only overwear sets are allowed or notself.
            slut_limit = 0
            underwear_limit = 0
            limited_to_top = True
            if maximal_arousal_uniform_policy.is_active():
                slut_limit = 999 #ie. no limit at all.
                underwear_limit = 999
                limited_to_top = False
            elif corporate_enforced_nudity_policy.is_active():
                slut_limit = 80
                underwear_limit = 999
                limited_to_top = False
            elif minimal_coverage_uniform_policy.is_active():
                slut_limit = 60
                underwear_limit = 15
                limited_to_top = False
            elif reduced_coverage_uniform_policy.is_active():
                slut_limit = 40
                underwear_limit = 10
                limited_to_top = False
            elif casual_uniform_policy.is_active():
                slut_limit = 25
                underwear_limit = 0
                limited_to_top = True
            elif relaxed_uniform_policy.is_active():
                slut_limit = 15
                underwear_limit = 0
                limited_to_top = True
            elif strict_uniform_policy.is_active():
                slut_limit = 5
                underwear_limit = 0
                limited_to_top = True
            else:
                slut_limit = 0
                underwear_limit = 0
                limited_to_top = True
            return slut_limit, underwear_limit, limited_to_top

        def update_uniform_wardrobes(self): #Rebuilds all uniforms in the wardrobe based on current uniform settings.
            #NOTE: This is inefficent, because we will often be adding then clearing the same uniform every time we change the list.
            # But it's only done once on exit from the screen, and is likely fast enough. Optimize by only manipulating changes if it's a problem.
            self.m_uniform.clear_wardrobe()
            self.p_uniform.clear_wardrobe()
            self.r_uniform.clear_wardrobe()
            self.s_uniform.clear_wardrobe()
            self.h_uniform.clear_wardrobe()

            for a_uniform in self.business_uniforms:
                if a_uniform.hr_flag:
                    self.update_department_uniform(self.h_uniform, a_uniform)
                if a_uniform.research_flag:
                    self.update_department_uniform(self.r_uniform, a_uniform)
                if a_uniform.production_flag:
                    self.update_department_uniform(self.p_uniform, a_uniform)
                if a_uniform.supply_flag:
                    self.update_department_uniform(self.s_uniform, a_uniform)
                if a_uniform.marketing_flag:
                    self.update_department_uniform(self.m_uniform, a_uniform)


        def update_department_uniform(self, the_wardrobe, the_uniform):
            if the_uniform.full_outfit_flag:
                the_wardrobe.add_outfit(the_uniform.outfit)
            if the_uniform.overwear_flag:
                the_wardrobe.add_overwear_set(the_uniform.outfit)
            if the_uniform.underwear_flag:
                the_wardrobe.add_underwear_set(the_uniform.outfit)

        def clear_messages(self): #clear all messages for the day.
            self.message_list = []
            self.counted_message_list = {}
            self.production_potential = 0
            self.supplies_purchased = 0
            self.production_used = 0
            self.research_produced = 0
            self.sales_made = 0
            self.serums_sold = 0

        def add_counted_message(self,message,new_count = 1):
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
            for line in self.production_lines:
                 if line.selected_design == the_serum:
                     line.set_product(None)

        def remove_trait(self, the_trait):
            self.blueprinted_traits.remove(the_trait)
            if the_trait is self.active_research_design:
                self.active_research_design = None

        def set_serum_research(self,new_research):
            if callable(new_research):
                new_research = new_research() #Used by serumtrait.unlock_function's, particularly SerumTraitBlueprints to properly set the new trait.
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
                clarity_produced = 0
                if theoretical_research.is_active():
                    clarity_produced += research_amount * 0.05

                if research_journal_subscription.is_active():
                    clarity_produced += research_amount * 0.05

                if independent_experimentation.is_active():
                    if mc.business.supply_count >= 5:
                        mc.business.supply_count += -5
                        clarity_produced += research_amount * 0.05

                self.partial_clarity += clarity_produced
                if self.partial_clarity >= 1.0:
                    int_clarity = __builtin__.int(self.partial_clarity)
                    self.partial_clarity += -int_clarity
                    mc.add_clarity(int_clarity, add_to_log = False)
                    self.add_counted_message("Idle R&D team produced Clarity")




                #research_amount = 0 #We didn't actually research anything because there is nothing to research!

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
            max_supply = __builtin__.int(max_supply)
            if max_supply + self.supply_count > self.supply_goal:
                max_supply = self.supply_goal - self.supply_count
                if max_supply <= 0:
                    return 0

            self.change_funds(-max_supply)
            self.supply_count += max_supply
            self.supplies_purchased += max_supply #Used for end of day reporting
            max_supply = int(max_supply)
            return max_supply

        def accept_contract(self, the_contract):
            self.active_contracts.append(the_contract)
            if the_contract in self.offered_contracts:
                self.offered_contracts.remove(the_contract)

            the_contract.start_contract()

        def abandon_contract(self, the_contract):
            if the_contract in self.active_contracts:
                self.active_contracts.remove(the_contract)

            the_contract.abandon_contract()

        def complete_contract(self, the_contract):
            if the_contract in self.active_contracts:
                self.active_contracts.remove(the_contract)

            the_contract.finish_contract()

        def renew_contracts(self):
            self.offered_contracts = []
            for x in range(0, self.max_offered_contracts):
                self.offered_contracts.append(generate_contract(self.max_serum_tier))

        def player_market(self):
            amount_increased = self.sale_progress(mc.charisma,mc.focus,mc.market_skill)
            #  #TODO: Replace the old goal here with the new one.
            self.listener_system.fire_event("general_work")
            # renpy.say("","You spend time making phone calls to clients and shipping out orders. You sell " + str(amount_sold) + " doses of serum.")
            renpy.say("","You spend time making cold calls to potential clients. You increase your market reach by " + str(amount_increased) + ".")
            return amount_increased

        def sale_progress(self,cha,focus,skill, slut_modifier = 0): #TODO: Decide what effects should directly affect price, and which ones should increase market reach gain.
            amount_increased = ((3*cha) + (focus) + (2*skill)) * ((self.team_effectiveness*0.01)) * (1.0+(slut_modifier)) * 5.0
            amount_increased = __builtin__.round(amount_increased)
            self.market_reach += amount_increased
            return amount_increased

        def sell_serum(self, the_serum, serum_count = 1, slut_modifier = 0, fixed_price = -1, external_serum_source = False): #TODO: Set this up. Takes each serum, check's it's value on todays' market, and sells it.
            #NOTE: Each serum immediately decreases the value of the one sold after it. (ie selling one serum at a time is no more or less efficent than bulk selling to the open market.
            sales_value = 0

            if self.inventory.get_serum_count(the_serum) < serum_count and not external_serum_source:
                serum_count = self.inventory.get_serum_count(the_serum)

            for x in range(0, serum_count):
                if fixed_price >= 0:
                    serum_base_value = fixed_price
                else:
                    serum_base_value = self.get_serum_base_value(the_serum)
                sales_value += serum_base_value

                self.mental_aspect_sold += the_serum.mental_aspect
                self.physical_aspect_sold += the_serum.physical_aspect
                self.sexual_aspect_sold += the_serum.sexual_aspect
                self.medical_aspect_sold += the_serum.medical_aspect

                attention_gain = the_serum.attention
                if attention_floor_increase_1_policy.is_active():
                    attention_gain += - 1
                if attention_floor_increase_2_policy.is_active():
                    attention_gain += - 1
                if attention_gain < 0:
                    attention_gain = 0
                self.attention += attention_gain

            sales_value = int(__builtin__.round(sales_value))

            if not external_serum_source:
                self.inventory.change_serum(the_serum, -serum_count)
            self.change_funds(sales_value)
            self.sales_made += sales_value
            self.listener_system.fire_event("player_serums_sold_count", amount = serum_count)
            self.listener_system.fire_event("serums_sold_value", amount = sales_value)

        def get_serum_base_value(self, the_serum, round_value = False):
            serum_value = 0
            serum_value += the_serum.mental_aspect * self.get_aspect_price("mental")
            serum_value += the_serum.physical_aspect * self.get_aspect_price("physical")
            serum_value += the_serum.sexual_aspect * self.get_aspect_price("sexual")
            serum_value += the_serum.medical_aspect * self.get_aspect_price("medical")

            if round_value:
                serum_value = int(__builtin__.round(serum_value))

            return serum_value

        def get_aspect_price(self, the_aspect): #If we want to be really proper we could have this check _per aspect_, but I think that's excessive.
            the_aspect = the_aspect.lower()
            if the_aspect == "mental":
                return self.mental_aspect_price * self.get_aspect_percent("mental")

            elif the_aspect == "physical":
                return self.physical_aspect_price * self.get_aspect_percent("physical")

            elif the_aspect == "sexual":
                return self.sexual_aspect_price * self.get_aspect_percent("sexual")

            elif the_aspect == "medical":
                return self.medical_aspect_price * self.get_aspect_percent("medical")

            elif the_aspect == "flaw":
                return self.flaws_aspect_cost * self.get_aspect_percent("flaw")

        def get_aspect_percent(self, the_aspect):
            the_aspect = the_aspect.lower()
            if the_aspect == "mental":
                return 1.0/(1+((self.mental_aspect_sold*1.0)/(self.market_reach*1.0)))

            elif the_aspect == "physical":
                return 1.0/(1+((self.physical_aspect_sold*1.0)/(self.market_reach*1.0)))

            elif the_aspect == "sexual":
                return 1.0/(1+((self.sexual_aspect_sold*1.0)/(self.market_reach*1.0)))

            elif the_aspect == "medical":
                return 1.0/(1+((self.medical_aspect_sold*1.0)/(self.market_reach*1.0)))

            elif the_aspect == "flaw":
                return 1.0

        def has_funds(self, money_amount):
            if self.funds >= money_amount:
                return True
            else:
                return False

        def change_funds(self, change_amount):
            change = int(change_amount)
            self.funds += change_amount

        def production_progress(self,focus,int,skill):
            #First, figure out how many production points we can produce total. Subtract that much supply and mark that much production down for the end of day report.
            production_amount = __builtin__.round(((3*focus) + (int) + (2*skill) + 10) * (self.team_effectiveness))/100
            self.production_potential += production_amount

            if production_amount > self.supply_count:
                production_amount = self.supply_count #Figure out our total available production, before we split it up between tasks (which might not have 100% usage!)

            for line in self.production_lines:
                supply_used = line.add_production(production_amount) #NOTE: this is modified by the weighted use of the Line in particular. This allows for greater than 100% efficency.
                self.supply_count += - supply_used
                self.production_used += supply_used

            return production_amount

        # Use to be def clear_production(self)
        def clear_all_production(self): #Clears all current produciton lines.
            for line in self.production_lines:
                line.set_product(None)

        def get_used_line_weight(self):
            used_production = 0
            for line in self.production_lines:
                used_production += line.production_weight #Tally how much weight we are using so far.
            return used_production

        def do_autosale(self):
            for line in self.production_lines:
                if line.autosell and line.selected_design:
                    extra_doses = self.inventory.get_serum_count(line.selected_design) - line.autosell_amount
                    if extra_doses > 0:
                        self.sell_serum(line.selected_design, extra_doses)

        def get_random_weighed_production_serum(self): #Return the serum design of one of our activly produced serums, relative probability by weight.
            used_production = self.get_used_line_weight()
            random_serum_number = renpy.random.randint(0,used_production)

            for line in self.production_lines:
                if random_serum_number < line.production_weight and line.selected_design:
                    return line.selected_design
                else:
                    random_serum_number -= line.production_weight #Subtract the probability of this one from our number to make progress in our search.

            return None


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
            renpy.say("","You settle in and spend a few hours filling out paperwork, raising company efficiency by " + str(eff_amount )+ "%%.")
            return eff_amount

        def hr_progress(self,cha,int,skill): #Don't compute efficiency cap here so that player HR effort will be applied against any efficiency drop even though it's run before the rest of the end of the turn.
            restore_amount = (3*cha) + (int) + (2*skill) + 5
            self.change_team_effectiveness(restore_amount)
            return restore_amount

        def change_team_effectiveness(self, the_amount):
            self.team_effectiveness += the_amount
            if self.team_effectiveness > self.effectiveness_cap:
                self.team_effectiveness = self.effectiveness_cap
            elif self.team_effectiveness < 50:
                self.team_effectiveness = 50

        def undesignate_person(self, the_person): #Removes the_person from all of the work lists so they can be moved around without them working in two departments.
            if the_person in self.research_team:
                self.research_team.remove(the_person)
            if the_person in self.production_team:
                self.production_team.remove(the_person)
            if the_person in self.supply_team:
                self.supply_team.remove(the_person)
            if the_person in self.market_team:
                self.market_team.remove(the_person)
            if the_person in self.hr_team:
                self.hr_team.remove(the_person)

        def evict_person(self, the_person): #Removes a person from a location in the building and moves them to their home.
            self.move_person(the_person, the_person.home)

        def move_person(self, the_person, the_destination):
            if rd_division.has_person(the_person):
                rd_division.move_person(the_person, the_destination)
            if p_division.has_person(the_person):
                p_division.move_person(the_person, the_destination)
            if office.has_person(the_person):
                office.move_person(the_person, the_destination)
            if m_division.has_person(the_person):
                m_division.move_person(the_person, the_destination)

        def add_employee_research(self, new_person):
            self.undesignate_person(new_person)
            self.research_team.append(new_person)
            new_person.add_job(rd_job, job_known = True)

        def add_employee_production(self, new_person):
            self.undesignate_person(new_person)
            self.production_team.append(new_person)
            new_person.add_job(production_job, job_known = True)

        def add_employee_supply(self, new_person):
            self.undesignate_person(new_person)
            self.supply_team.append(new_person)
            new_person.add_job(supply_job, job_known = True)


        def add_employee_marketing(self, new_person):
            self.undesignate_person(new_person)
            self.market_team.append(new_person)
            new_person.add_job(market_job, job_known = True)

        def add_employee_hr(self, new_person):
            self.undesignate_person(new_person)
            self.hr_team.append(new_person)
            new_person.add_job(hr_job, job_known = True)

        def remove_employee(self, the_person): #As of v0.49 this should be used exclusively for firing people. When changing jobs you can just assign them a new one, they should keep the correct roles.
            self.undesignate_person(the_person)
            self.evict_person(the_person)

            the_person.add_job(unemployed_job, job_known = True)

            #Roles can have an on_remove function, but these have special events that we want to make sure are triggered properly.
            if the_person == self.head_researcher:
                renpy.call("fire_head_researcher", the_person) #Call the label we use for firing the person as a role action. This should trigger it any time you fire or move your head researcher.

            if the_person == self.company_model:
                renpy.call("fire_model_label", the_person)

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
            for person in self.get_employee_list():
                self.give_department_serum(person)

        def give_department_serum(self, the_person):
            the_serum = None
            if the_person in self.research_team:
                the_serum = self.r_serum
            elif the_person in self.market_team:
                the_serum = self.m_serum
            elif the_person in self.production_team:
                the_serum = self.p_serum
            elif the_person in self.supply_team:
                the_serum = self.s_serum
            elif the_person in self.hr_team:
                the_serum = self.h_serum

            if the_serum is not None:
                should_give_serum = True
                for active_serum in the_person.serum_effects:
                    if the_serum.is_same_design(active_serum):
                        if active_serum.duration - active_serum.duration_counter >= 3:
                            should_give_serum = False #Don't double-dose girls if they have the serum running and it will last the work day already
                            break

                if should_give_serum:
                    if self.inventory.get_serum_count(the_serum) > 0:
                        self.inventory.change_serum(the_serum,-1)
                        the_person.give_serum(copy.copy(the_serum), add_to_log = False)
                    else:
                        the_message = "Stockpile out of " + the_serum.name + " to give to staff."
                        self.add_counted_message(the_message)

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

        def generate_candidate_requirements(self): #Checks current business policies and generates a dict of keywords for create_random_person to set the correct values to company requirements.
            # In cases where a range is allowed it generates a random value in that range, so call this one per person being created.
            candidate_dict = {} # This will hold keywords and arguments for create_random_person to create a person with specific modifies

            if recruitment_skill_improvement_policy.is_active():
                skill_cap = 7
                candidate_dict["age_ceiling"] = candidate_dict.get("age_ceiling", 50) - 10
                candidate_dict["skill_array"] = [renpy.random.randint(1,skill_cap),renpy.random.randint(1,skill_cap),renpy.random.randint(1,skill_cap),renpy.random.randint(1,skill_cap),renpy.random.randint(1,skill_cap)]

            if recruitment_stat_improvement_policy.is_active():
                stat_cap = 7
                candidate_dict["age_floor"] = candidate_dict.get("age_floor", 18) + 10
                candidate_dict["stat_array"] = [renpy.random.randint(1,stat_cap),renpy.random.randint(1,stat_cap),renpy.random.randint(1,stat_cap)]

            if recruitment_sex_improvement_policy.is_active():
                stat_cap = 7
                candidate_dict["sex_array"] = [renpy.random.randint(1,stat_cap),renpy.random.randint(1,stat_cap),renpy.random.randint(1,stat_cap)]

            if recruitment_suggest_improvment_policy.is_active():
                candidate_dict["age_ceiling"] = candidate_dict.get("age_ceiling", 50) - 10
                candidate_dict["bonus_suggest"] = 2

            if recruitment_obedience_improvement_policy.is_active():
                candidate_dict["bonus_obedience"] = 10

            if recruitment_slut_improvement_policy.is_active():
                candidate_dict["age_ceiling"] = candidate_dict.get("age_ceiling", 50) - 10
                candidate_dict["bonus_sluttiness"] = 20

            if candidate_dict.get("age_ceiling", 50) < candidate_dict.get("age_floor", 18):
                candidate_dict["age_ceiling"] = candidate_dict.get("age_floor",18) + 1


            if recruitment_mothers_policy.is_active():
                candidate_dict["bonus_kids"] = candidate_dict.get("bonus_kids", 0) + 1
            elif recruitment_childless_policy.is_active():
                candidate_dict["kids"] = 0

            if recruitment_big_tits_policy.is_active():
                candidate_dict["tits"] = get_random_big_tit()
            elif recruitment_huge_tits_policy.is_active():
                candidate_dict["tits"] = get_random_huge_tit()
            elif recruitment_small_tits_policy.is_active():
                candidate_dict["tits"] = get_random_small_tit()
            elif recruitment_tiny_tits_policy.is_active():
                candidate_dict["tits"] = "AA"

            if recruitment_short_policy.is_active():
                candidate_dict["height"] = 0.9 + (renpy.random.random()/30)
            elif recruitment_tall_policy.is_active():
                candidate_dict["height"] = 0.96 + (renpy.random.random()/30)


            if recruitment_single_policy.is_active():
                candidate_dict["relationship"] = "Single"
            elif recruitment_married_policy.is_active():
                candidate_dict["relationship"] = "Married"


            if recruitment_old_policy.is_active():
                candidate_dict["age_floor"] = 40
            elif recruitment_teen_policy.is_active():
                candidate_dict["age_ceiling"] = 19

            if candidate_dict.get("age_ceiling", 50) > 60: #TODO: Introduce postmenapause women.
                candidate_dict["age_ceiling"] = 60
            if candidate_dict.get("age_floor", 18) < 18: #No FBI needed here!
                candidate_dict["age_floor"] = 18

            return candidate_dict
