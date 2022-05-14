#Contains all the stuff about instantiating duties.

#TODO: Define basic duties for all staff.
# ie basic produciton/research/supply procurement/marketing/HR work.
# Rework some existing special roles into duties.
# -> Rule of thumb: if you can only have one thing it's a Job, if you can have this thing plus other things they're duties.
# -> Modeling should be a duty.
# -> Head researcher should be a Job (w/ a special duty?)
# Rework existing business policies into duties (Research -> Clarity, Serum policies)
# Add new duties (weekend/overtime work, some cross-department duties (reduce HR costs, expand market reach with R&D, make raw cash with marketers, etc.)

init -2 python:
    #Basic work duty functions#
    ## Supply ##
    def get_duty_supply_cost_modifier(the_person):
        cost_modifier = 1.0
        if the_person.has_duty(greymarket_deals_duty):
            cost_modifier = 0.75
        if the_person.has_duty(alternative_payment_duty):
            if the_person.effective_sluttiness() >= 25:
                cost_modifier += -0.05*the_person.sex_skills["Foreplay"]
            if the_person.effective_sluttiness() >= 50:
                cost_modifier += -0.05*the_person.sex_skills["Oral"]
        return cost_modifier

    def supply_work_duty_on_turn(the_person):
        cost_modifier = get_duty_supply_cost_modifier(the_person)

        mc.business.supply_purchase(the_person.focus, the_person.charisma, the_person.supply_skill, the_person.calculate_job_efficency(), cost_modifier)

    def heavy_supply_work_duty_on_turn(the_person):
        cost_modifier = get_duty_supply_cost_modifier(the_person)

        mc.business.supply_purchase(the_person.focus, the_person.charisma, the_person.supply_skill, the_person.calculate_job_efficency() * 0.5, cost_modifier)
        the_person.change_happiness(-2, add_to_log = False)

    def greymarket_deals_duty_on_turn(the_person):
        mc.business.attention += 1

    def alternative_payment_duty_requirement(the_person):
        if not male_focused_marketing_policy.is_active():
            return False
        elif the_person.effective_sluttiness() < 25:
            return "Requires 25 Sluttiness"
        else:
            return True

    ## Research ##
    def research_clarity_production_check(the_person, research_amount): #Helper function to check a researcher and generate the correct amount of associated Clarity.
        clarity_produced = 0
        if the_person.has_duty(theoretical_research_duty):
            clarity_produced += research_amount * 0.2

        if the_person.has_duty(research_journal_subscription_duty):
            clarity_produced += research_amount * 0.2

        if the_person.has_duty(practical_experimentation_duty):
            if mc.business.supply_count >= 5:
                mc.business.supply_count += -5
                clarity_produced += research_amount * 0.2

        mc.business.partial_clarity += clarity_produced
        if mc.business.partial_clarity >= 1.0:
            int_clarity = __builtin__.int(mc.business.partial_clarity)
            mc.business.partial_clarity += -int_clarity
            mc.add_clarity(int_clarity, add_to_log = False)
            mc.business.add_counted_message("Idle R&D team produced Clarity")


    def research_work_duty_on_turn(the_person):
        research_amount = mc.business.research_progress(the_person.int, the_person.focus, the_person.supply_skill, the_person.calculate_job_efficency())
        research_clarity_production_check(the_person ,research_amount)

    def heavy_research_work_duty_on_turn(the_person):
        research_amount = mc.business.research_progress(the_person.int, the_person.focus, the_person.supply_skill, the_person.calculate_job_efficency() * 0.5)
        research_clarity_production_check(the_person, research_amount)
        the_person.change_happiness(-2, add_to_log = False)

    def research_journal_on_apply(the_person): #Done on_apply and on_remove so the ocsts will display as ongoing oepration costs.
        mc.business.operating_costs += 10

    def research_journal_on_remove(the_person):
        mc.business.operating_costs += -10

    ## Production
    def production_work_duty_on_turn(the_person):
        mc.business.production_progress(the_person.focus, the_person.int, the_person.production_skill, the_person.calculate_job_efficency())

    def heavy_production_work_duty_on_turn(the_person):
        mc.business.production_progress(the_person.focus, the_person.int, the_person.production_skill, the_person.calculate_job_efficency()*0.5)
        the_person.change_happiness(-2, add_to_log = False)

    def bend_safety_rules_on_turn(the_person):
        mc.business.production_progress(the_person.focus, the_person.int, the_person.production_skill, the_person.calculate_job_efficency()*0.25)
        if renpy.random.randint(0, 100) < 5:
            the_person.give_serum(mc.business.get_random_weighed_production_serum())
            the_person.change_happiness(-10)

    ## Marketing ##
    def market_work_duty_on_turn(the_person):
        work_skill = the_person.market_skill
        if the_person.has_duty(work_for_tips_duty):
            if the_person.effective_sluttiness() < 25:
                pass #Not slutty enough for a bonus.
            elif the_person.effective_sluttiness() < 50:
                work_skill += the_person.sex_skills["Foreplay"]
            else:
                work_skill += the_person.sex_skills["Oral"]

        mc.business.sale_progress(the_person.charisma, the_person.focus, work_skill, the_person.calculate_job_efficency())

    def heavy_market_work_duty_on_turn(the_person):
        work_skill = the_person.market_skill
        if the_person.has_duty(work_for_tips_duty):
            if the_person.effective_sluttiness() < 25:
                pass #Not slutty enough for a bonus.
            elif the_person.effective_sluttiness() < 50:
                work_skill += the_person.sex_skills["Foreplay"]
            else:
                work_skill += the_person.sex_skills["Oral"]
        mc.business.sale_progress(the_person.charisma, the_person.focus, work_skill, the_person.calculate_job_efficency()*0.5)
        the_person.change_happiness(-2, add_to_log = False)

    def client_demonstration_duty_requirement(the_person):
        if mandatory_unpaid_serum_testing_policy.is_active():
            return True
        else:
            return False

    def client_demonstration_duty_on_turn(the_person):
        mc.business.sale_progress(0, 0, the_person.sex_skills["Foreplay"], the_person.calculate_job_efficency())
        if renpy.random.randint(0, 100) < 5:
            the_person.give_serum(mc.business.get_random_weighed_production_serum())
            the_person.change_happiness(-10)

    def work_for_tips_duty_requirement(the_person):
        if not male_focused_marketing_policy.is_active():
            return False
        if the_person.effective_sluttiness() < 25:
            return "Requires 25 Sluttiness"
        else:
            return True

    ## HR ##
    def hr_work_duty_on_turn(the_person):
        mc.business.hr_progress(the_person.charisma, the_person.int, the_person.hr_skill, the_person.calculate_job_efficency())

    def heavy_hr_work_duty_on_turn(the_person):
        mc.business.hr_progress(the_person.charisma, the_person.int, the_person.hr_skill, the_person.calculate_job_efficency()*0.5)
        the_person.change_happiness(-2, add_to_log = False)

    def encourage_loyalty_duty_on_turn(the_person):
        coworker = get_random_from_list(mc.business.get_requirement_employee_list(exclude_list = [the_person], obedience_max = the_person.obedience - 1))
        if coworker is None:
            return
        coworker.change_obedience(1, add_to_log = False)

    def internal_propaganda_duty_on_turn(the_person):
        coworker = get_random_from_list(mc.business.get_requirement_employee_list(exclude_list = [the_person], love_max = the_person.love - 1))
        if coworker is None:
            return
        coworker.change_love(1, add_to_log = False)

    def corrupt_work_chat_duty_on_turn(the_person):
        coworker = get_random_from_list(mc.business.get_requirement_employee_list(exclude_list = [the_person], slut_max = the_person.effective_sluttiness() - 1))
        if coworker is None:
            return
        coworker.change_slut(1, add_to_log = False)

    ## GENERAL DUTY FUNCTIONS ##

    def mandatory_breaks_duty_on_turn(the_person):
        the_person.change_happiness(1, add_to_log = False)

    def paid_serum_testing_duty_requirement(the_person):
        if not mandatory_paid_serum_testing_policy.is_owned():
            return False
        else:
            return True

    def employee_paid_serum_test_requirement(the_person):
        if not mc.business.has_funds(100):
            return "Requires: $100"
        else:
            return True

    def unpaid_serum_testing_duty_requirement(the_person):
        if not mandatory_unpaid_serum_testing_policy.is_owned():
            return False
        else:
            return True

    def employee_unpaid_serum_test_requirement(the_person):
        return True #TODO: maybve limit this to once/day?

    def daily_serum_dosage_duty_requirement(the_person):
        if not daily_serum_dosage_policy.is_owned():
            return False
        else:
            return True

    def daily_serum_dosage_duty_on_move(the_person):
        if the_person.event_triggers_dict.get("daily_serum_distributed", False):
            return #Give it to them first thing in the morning, but only once

        elif not the_person.job.job_location.has_person(the_person):
            return #Don't give it to them if they aren't at work.

        the_serum = None
        if the_person in mc.business.research_team:
            the_serum = mc.business.r_serum
        elif the_person in mc.business.market_team:
            the_serum = mc.business.m_serum
        elif the_person in mc.business.production_team:
            the_serum = mc.business.p_serum
        elif the_person in mc.business.supply_team:
            the_serum = mc.business.s_serum
        elif the_person in mc.business.hr_team:
            the_serum = mc.business.h_serum

        if the_serum is not None:
            the_person.event_triggers_dict["daily_serum_distributed"] = True
            should_give_serum = True
            for active_serum in the_person.serum_effects:
                if the_serum.is_same_design(active_serum):
                    if active_serum.duration - active_serum.duration_counter >= 3:
                        should_give_serum = False #Don't double-dose girls if they have the serum running and it will last the work day already
                        break

            if should_give_serum:
                if mc.business.inventory.get_serum_count(the_serum) > 0:
                    mc.business.inventory.change_serum(the_serum,-1)
                    the_person.give_serum(the_serum, add_to_log = False)
                else:
                    the_message = "Stockpile out of " + the_serum.name + " to give to staff."
                    mc.business.add_counted_message(the_message)

    def daily_serum_dosage_duty_on_day(the_person):
        the_person.event_triggers_dict["daily_serum_distributed"] = False

    def bureaucratic_nightmare_duty_requirement(the_person):
        if bureaucratic_nightmare.is_active():
            return True
        return False

    def employee_generate_infraction_requirement(the_person):
        return True

    def social_media_advertising_duty_requirement(the_person):
        if not (the_person.event_triggers_dict.get("insta_known", False) or the_person.event_triggers_dict.get("dikdok_known", False) or the_person.event_triggers_dict.get("onlyfans_known", False)):
            return "No Known Social Media Account"
        else:
            return True

    def social_media_advertising_duty_on_turn(the_person):
        effect = 0
        work_skill = the_person.market_skill
        if the_person.effective_sluttiness() >= 25:
            work_skill += the_person.sex_skills["Foreplay"]
        if the_person.event_triggers_dict.get("insta_known", False):
            effect += 0.1
        if the_person.event_triggers_dict.get("dikdok_known", False):
            effect += 0.1
        if the_person.event_triggers_dict.get("onlyfans_known", False):
            effect += 0.1
        mc.business.hr_progress(the_person.charisma, the_person.int, work_skill, the_person.calculate_job_efficency()*effect)



    def auto_milk_tits(the_person, max_doses, extra_doses = 0):
        if the_person.has_role(lactating_serum_role):
            if the_person.event_triggers_dict.get("serum_in_breasts", 0) >= 1:
                available_doses = __builtin__.int(the_person.event_triggers_dict.get("serum_in_breasts",0))
                if available_doses > max_doses:
                    available_doses = max_doses
                the_person.event_triggers_dict["serum_in_breasts"] = the_person.event_triggers_dict.get("serum_in_breasts",0) - available_doses
                milk_serum = get_girl_milky_serum(the_person)
                mc.business.inventory.change_serum(milk_serum, available_doses + extra_doses)

            else:
                pass #Not enough in their tits, nothing to milk this turn.

        elif the_person.lactation_sources > 0:
            available_doses = __builtin__.int(the_person.event_triggers_dict.get("milk_in_breasts",0))
            if available_doses > max_doses:
                available_doses = max_doses
            if available_doses >= 1:
                the_person.event_triggers_dict["milk_in_breasts"] = the_person.event_triggers_dict.get("milk_in_breasts", 0) - available_doses
                milk_serum = SerumDesign()
                milk_serum.name = the_person.title + "'s Breast Milk"
                milk_serum.add_trait(the_person.get_milk_trait())
                mc.business.inventory.change_serum(milk_serum, available_doses + extra_doses)

        else:
            pass #not lactating any more, nothing to do.

    def breast_milking_space_duty_requirement(the_person):
        if not breast_milking_space_policy.is_active():
            return False
        elif the_person.lactation_sources <= 0:
            return "Not lactating"
        else:
            return True

    def breast_milking_space_on_turn(the_person):
        auto_milk_tits(the_person, 1)

    def breast_pump_2_duty_requirement(the_person):
        if not auto_pumping_stations_policy.is_active():
            return False
        elif the_person.lactation_sources <= 0:
            return "Not lactating"
        else:
            return True

    def breast_pump_2_duty_on_turn(the_person):
        auto_milk_tits(the_person, 3)

    def breast_pump_3_duty_requirement(the_person):
        if not high_suction_pumping_machinery_policy.is_active():
            return False
        elif the_person.lactation_sources <= 0:
            return "Not lactating"
        elif not the_person.has_large_tits():
            return "Breasts too small for machine"
        else:
            return True

    def breast_pump_3_duty_on_turn(the_person):
        auto_milk_tits(the_person, 99, 1)


    ## R&D DUTY FUNCTIONS ##
    def theoretical_research_duty_requirement(the_person):
        if not theoretical_research.is_active():
            return False
        else:
            return True

    def research_journal_subscription_duty_requirement(the_person):
        if not research_journal_subscription.is_active():
            return False
        else:
            return True

    def practical_experimentation_duty_requirement(the_person):
        if not practical_experimentation.is_active():
            return False
        else:
            return True

    ## HR DUTY FUNCTIONS ##
    def find_infractions_duty_requirement(the_person):
        if not office_punishment.is_active():
            return False
        else:
            return True

    def random_infraction_generation(the_target):
        potential_infractions = []
        potential_infractions.append(Infraction.bureaucratic_mistake_factory())
        potential_infractions.append(Infraction.careless_accident_factory())
        potential_infractions.append(Infraction.underperformance_factory())
        potential_infractions.append(Infraction.office_disturbance_factory())
        if the_person.is_wearing_uniform():
            potential_infractions.append(Infraction.out_of_uniform_factory())
        if the_person.obedience < 100:
            potential_infractions.append(Infraction.disobedience_factory())
        if the_person.effective_sluttiness() > 25:
            potential_infractions.append(Infraction.inappropriate_behaviour_factory())
        return get_random_from_list(potential_infractions)


    def find_infractions_duty_on_turn(the_person):
        if renpy.random.randint(0,100) < 10: #NOTE: This is different from 5% so we can have low obedience/rival employss show up more often.
            # There's a chance we've discovered an infraction
            the_target = get_random_from_list(mc.business.get_employee_list())
            if the_target is None:
                return #Nobody to generate infractions for.

            if the_person == the_target: #NOTE: Doesn't have any probabilyt correction, buecause you always 100% know when you've commited an infraction
                if the_person.obedience >= 140 or the_person.get_opinion_score("being submissive") > 0:
                    the_target.add_infraction(random_infraction_generation(the_target), add_to_log = False) # TODO: Generate an infraction for yourself. Those are the rules!
                else:
                    return #Whoops! We're just... going to ignore that.

            else:
                real_infraction_chance = 150 - the_target.obedience
                if town_relationships.get_relationship(the_person, the_target) == "Rival":
                    real_infraction_chance += 20
                elif town_relationships.get_relationship(the_person, the_target) == "Nemisis":
                    real_infraction_chance += 40
                elif town_relationships.get_relationship(the_person, the_target) == "Friend":
                    real_infraction_chance += -20
                elif town_relationships.get_relationship(the_person, the_target) in ["Best Friend","Daughter", "Mother", "Aunt", "Niece", "Cousin", "Grandmother", "Granddaughter"]:
                    real_infraction_chance += -40
                if renpy.random.randint(0,100) < real_infraction_chance:
                    the_target.add_infraction(random_infraction_generation(the_target)) #TODO:

label instantiate_duties():
    python:
        ## BASIC WORK DUTIES ##
        supply_work_duty = Duty("Order Supplies",
            "Contact bulk chemical providers, place orders, arrange for deliveries, and ensure the production team has all of the materials they need. Orders 3xFocus + 2xSupply Skill + 1xCharisma Supply, at a cost of $1 per Supply.",
            on_turn_function = supply_work_duty_on_turn)
        heavy_supply_work_duty = Duty("Heavy Workload",
            "Enough work to fill up the day, and then some. Produces an extra 25% of normal production, but lowers Happiness by -2 per turn.",
            on_turn_function = heavy_supply_work_duty_on_turn)

        research_work_duty = Duty("Research and Development",
            "Experiment with chemical formulations, refine synthesis techniques, and prepare models for stability and long term effectiveness of new serum traits and designs. Produces 3xIntelligence + 2xResearch Skill + 1xFocus Research Points per turn.",
            on_turn_function = research_work_duty_on_turn)
        heavy_research_work_duty = Duty("Heavy Workload",
            "Enough work to fill up the day, and then some. Produces an extra 25% of normal production, but lowers Happiness by -2 per turn.",
            on_turn_function = heavy_research_work_duty_on_turn)

        production_work_duty = Duty("Prodution Line Work",
            "Operate the machinery nessesary to turn chemical precursors into serum doses at an industrial scale and at economical costs. Produces 3xFocus + 2xProduction Skill + 1xIntelligence  Production Points per turn, at the cost of 1 unit of Supply.",
            on_turn_function = production_work_duty_on_turn)
        heavy_production_work_duty = Duty("Heavy Workload",
            "Enough work to fill up the day, and then some. Produces an extra 25% of normal production, but lowers Happiness by -2 per turn.",
            on_turn_function = heavy_production_work_duty_on_turn)

        market_work_duty = Duty("Find Clients",
            "Cold-call potential clients and inform them about new products, respond to business inquiries, and increase general awareness about your product. Increases Market Reach by 15xCharisma + 10xMarket Skill + 5xFocus per turn. Producing 1 Market Reach per 1 of each Serum Aspect sold is enough to keep price at 100%. Higher Market Reach increases Aspect value, while lower Market Reach decreases it.",
            on_turn_function = market_work_duty_on_turn)
        heavy_market_work_duty = Duty("Heavy Workload",
            "Enough work to fill up the day, and then some. Produces an extra 25% of normal production, but lowers Happiness by -2 per turn.",
            on_turn_function = heavy_market_work_duty_on_turn)

        #TODO: Make sure HR work results in effiency increasing properly and not bouncing around strangely.
        hr_work_duty = Duty("Office Paperwork",
            "Manage payroll, distribute internal reports, recieve official complaints, and otherwise handle administrative work as it arises. Raises Business Efficiency by 3xFocus + 2xHR Skill + 1xCharisma per turn. Efficiency directly affects the production of all other duties.",
            on_turn_function = hr_work_duty_on_turn) #We could do this on_move?
        heavy_hr_work_duty = Duty("Heavy Workload",
            "Enough work to fill up the day, and then some. Produces an extra 25% of normal production, but lowers Happiness by -2 per turn.",
            on_turn_function = heavy_hr_work_duty_on_turn)

        ## GENERAL DUTIES ## - Duties that should be available to everyone at the company.
        mandatory_breaks_duty = Duty("Mandatory Breaks",
            "Ample time throughout the day to take a break, get some coffee, and strech your legs. Doesn't achieve anything, but makes the work slightly more pleasant. Increases Happiness by 1/turn.",
            on_turn_function = mandatory_breaks_duty_on_turn)

        employee_paid_serum_test = Action("Test serum (paid) -$100.", employee_paid_serum_test_requirement, "employee_paid_serum_test_label",
            menu_tooltip = "Pay her to willingly take a dose of serum, per company policy.")
        mandatory_paid_serum_testing_duty = Duty("Mandatory Paid Serum Testing",
            "Test serum provided by management, per company policy. Compensation is five days pay for every dose of serum tested this way.",
            requirement_function = paid_serum_testing_duty_requirement,
            actions = [employee_paid_serum_test])

        extra_paperwork_duty = Duty("Extra Paperwork", #NOTE: Effect is calculated by Business so it can ignore extra effectiveness costs from other things
            "Complete all of your own paperwork, reducing the amount of administrative work that needs to be done. This employee will not lower Business Efficiency every turn.")

        employee_unpaid_serum_test = Action("Test serum (unpaid).", employee_unpaid_serum_test_requirement, "employee_unpaid_serum_test_label",
            menu_tooltip = "Give her a dose of serum to test on herself, per company policy.")
        unpaid_serum_testing_duty = Duty("Mandatory Unpaid Serum Testing",
            "Test serum provided by management on demand. No compensation is provided for this.",
            requirement_function = unpaid_serum_testing_duty_requirement,
            actions = [employee_unpaid_serum_test])

        daily_serum_dosage_duty = Duty("Daily Serum Dose",
            "Recieve a dose of serum from management at the start of every work day, unless a previous dose will last the work day. Serum type can be varried by department and set from the main office.",
            requirement_function = daily_serum_dosage_duty_requirement,
            on_move_function = daily_serum_dosage_duty_on_move, #NOTE: A flag makes sure this is only triggered once per day.
            on_day_function = daily_serum_dosage_duty_on_day)

        employee_generate_infraction = Action("Invent an infraction. -5 Efficency", employee_generate_infraction_requirement, "employee_generate_infraction_label",
            menu_tooltip = "Company policy is so complicated it's nearly impossible to go a day without violating some minor rule. If you were paranoid, you might think it was written that way on purpose...")
        bureaucratic_nightmare_duty = Duty("Bureaucratic nightmare",
            "Forms, records, reports, and even more forms, all in triplicate. So many rules that it's impossible not to make a mistake somewhere! Management can generate an infraction at will, at the cost of 5% business efficency.",
            requirement_function = bureaucratic_nightmare_duty_requirement,
            actions = [employee_generate_infraction])

        social_media_advertising_duty = Duty("Social Media Advertising",
            "Post company approved adds on your personal social media accounts. Produces 10% of normal Marketing production for each InstaPic, DikDok, and OnlyFanatics account the employee has. If Sluttiness is 25 or higher, also adds Foreplay to Marketing Skill for this bonus production .",
            requirement_function = social_media_advertising_duty_requirement,
            on_turn_function = social_media_advertising_duty_on_turn)


        breast_milk_pump_1_duty = Duty("Provide Breast Milk Samples",
            "Make use of company provide milk pumping equipment to provide management with breast milk samples for health and safety purposes. Produces doses of breast milk serum, limited to a maximum 1 dose per turn. Smaller breasts or a low number of lactation sources may result in doses only being created every two or three turns.",
            requirement_function = breast_milking_space_duty_requirement,
            on_turn_function = breast_milking_space_on_turn)

        breast_milk_pump_2_duty = Duty("Mandatory Breast Pumping",
            "Use electronic breast pump stations at regular intervals to prevent interuptions to normal business operations. Produces up to 3 doses of breast milk serum per turn. Large breasts and/or multiple lactation sources will be required to reach maximum output.",
            requirement_function = breast_pump_2_duty_requirement,
            on_turn_function = breast_pump_2_duty_on_turn)

        breast_milk_pump_3_duty = Duty("Industrial Breast Suction",
            "Spend part of the day with your breasts attached to repurposed dairy hardware. The high efficiency hardware will ensure every possible drop of breast milk is extracted in a timely manner. Breast milk production is limited only by breast size and number of lacation sources, and an additional dose is created whenever any milk is produced. Requires at least D-cup breast to properly interface with the machinery.",
            requirement_function = breast_pump_3_duty_requirement,
            on_turn_function = breast_pump_3_duty_on_turn)

        #TODO: Company Informant. Occasionally will generate an infraction for other girls, particularly ones she is friends with.
        #TODO: Turn the +Sluttiness effects into individual duties.
        #TODO: Milking duties, unlocked by having the milk serum production thing unlocked.

        #TODO: Figure out how to work this into our scheduling code. Probably not worth it.
        #TODO: Extra Hours. Employee will stay 1 time chunk later.
        #TODO: Work Weekends. Employee will show up on the weekend. (and needs to be paid for those days)
         #-> Adjust the pay code for that.


        ## Supply Specific Duties ##
        # TODO: THis
        greymarket_deals_duty = Duty("Arrange Greymarket Deals",
            "Contact various less-than-reputable suppliers and arrange deals. Lowers cost of all supplies by purchased by this character by 25%, but increases Attention by 1 per turn.",
            on_turn_function = greymarket_deals_duty_on_turn)

        alternative_payment_duty = Duty("Alternative Payment Methods",
            "Convince vendors to provide Serum Supplies, using methods other than money to convince them. Reduces supply cost by 5% per Foreplay skill level. If Sluttiness is higher than 50, also add Oral skill.",
            requirement_function = alternative_payment_duty_requirement)

        ## R&D Specific Duties ##
        theoretical_research_duty = Duty("Theoretical Research",
            "Read cutting edge research papers and propose novel ideas to management. Generate 1 Clarity for every 5 Research Points generated.",
            requirement_function = theoretical_research_duty_requirement)

        research_journal_subscription_duty = Duty("Journal Studies",
            "Read academic journals, a critical task to keep abreast of the most recent developments in the field. Generates 1 Clarity for every 5 Research Points generated. Costs $10 per day in journal subscription fees.",
            requirement_function = research_journal_subscription_duty_requirement,
            on_apply_function = research_journal_on_apply,
            on_remove_function = research_journal_on_remove)

        practical_experimentation_duty = Duty("Practical Experimentation",
            "Formulate novel hypotheses, test them, and produce research reports. Generates 1 Clarity for every 5 Research Points generated, at the cost of 5 Serum Supply per turn.",
            requirement_function = practical_experimentation_duty_requirement)
        #TODO: Self-testing duty. Employee will sometimes randomly be dosed with random serums.

        head_researcher_duty = Duty("Provide Research Expertise", #NOTE: Doesnt' actually do anything, but exists so it can appear in the head researcher's mandatory duty list.
            "Direct research efforts and provide high level assistance to all members of the R&D team. Provides a 5% bonus to Research Points produced per point of Int above 2. Int below 2 instead produces a penalty of 5% per missing point.")

        ## Production work duties ##
        bend_safety_rules_duty = Duty("Bend Safety Rules",
            "Safety equipment that gets in the way of productivity should be ignored. This employee will produce an additional 25% productivity, but may ocassionally dose themselves with a serum being produced.",
            on_turn_function = bend_safety_rules_on_turn)
        # TODO: Some more production specific duties

        ## Market Specific Duties ##
        # TODO: turn modeling into a duty.
        client_demonstration_duty = Duty("Client Demonstrations",
            "Provide practical demonstrations of serum effects to clients on demand. Increases Market reach by 2*Foreplay skill, with a small chance each turn to be given a dose of serum currently in production.",
            requirement_function = client_demonstration_duty_requirement,
            on_turn_function = client_demonstration_duty_on_turn)

        work_for_tips_duty = Duty("Arouse Potential Clients",
            "Take advantage of the male dominated market by teasing and arousing potential clients when possible. Adds Foreplay skill to Marketing skill. If Sluttiness is higher than 50, also adds Oral skill.",
            requirement_function = work_for_tips_duty_requirement)

        # TODO: Seductive Deal Making. Increases serum value based on Foreplay skill. Requires some level of Sluttiness
        # TODO: Management Eye Candy. Strip tease for managemnt on demand. Requires some level of Sluttiness or Opinions
        # TODO: Secretive Marketing. Actively lowers attention by a small amount.
        # TODOx2: Some way of using your girls as a bribe to lower attention even more at high Sluttiness.


        ## HR Specific Duties##
        # TODO: Personal secretary specific duties.
        find_infractions_duty = Duty("Find Infractions",
            "Verify reports, check uniforms, and apply company regulations wherever possible. Base 5% chance to discover an infraction every turn. Less likely to generate infractions for high Obedience employees and friends, more likely for lower Obedience and rival employees.",
            requirement_function = find_infractions_duty_requirement,
            on_turn_function = find_infractions_duty_on_turn)

        encourage_loyalty_duty = Duty("Encourage Staff Loyalty",
            "Talk to other staff, reminding them of the importance of loyalty and obedience around the office. Picks an employee with Obedience lower than this employee each turn and raises Obedience by 1.",
            on_turn_function = encourage_loyalty_duty_on_turn)

        internal_propaganda_duty = Duty("Distribute Internal Propaganda",
            "Spread stories among the staff, highlighting the positive and likeable features of management. Picks an employee with Love lower than this employee each turn and raises Love by 1.",
            on_turn_function = internal_propaganda_duty_on_turn)

        corrupt_work_chat_duty = Duty("Corrupt Work Chat Groups",
            "Share scandelous stories and links to porn while encouraging others within the company to do the same. Picks an employee with Sluttiness lower than this employee each turn and raises Sluttiness by 1.",
            on_turn_function = corrupt_work_chat_duty_on_turn)


        # V have these key off of the recruitment elements.
        # TODO: Add "Internal Propaganda" duty. Raises Love of someone within the company by 1 per day, up to this character's Love.
        # TODO: Add "Disciplinary Meetings" duty. Raises Obedience of someone within the company by 1 per day, up to this character's Obedience
        # TODO: Management Stress Relief. Requires some level of sluttiness, which determines what she'll do for you.


        # -> Stuff like "On Demand Stress Relief" to fuck them whenever, blowjobs at yoru desk, etc.
        # -> Also options to have them manage punishments (just consumes infractions and produces Obedience).

        general_duties_list = []
        general_duties_list.append(mandatory_breaks_duty)
        general_duties_list.append(extra_paperwork_duty)
        general_duties_list.append(mandatory_paid_serum_testing_duty)
        general_duties_list.append(unpaid_serum_testing_duty)
        general_duties_list.append(daily_serum_dosage_duty)
        general_duties_list.append(bureaucratic_nightmare_duty)
        general_duties_list.append(social_media_advertising_duty)
        general_duties_list.append(breast_milk_pump_1_duty)
        general_duties_list.append(breast_milk_pump_2_duty)
        general_duties_list.append(breast_milk_pump_3_duty)

        general_rd_duties = []
        general_rd_duties.append(heavy_research_work_duty)
        general_rd_duties.append(theoretical_research_duty)
        general_rd_duties.append(research_journal_subscription_duty)
        general_rd_duties.append(practical_experimentation_duty)

        general_market_duties = []
        general_market_duties.append(market_work_duty)
        general_market_duties.append(heavy_market_work_duty)
        general_market_duties.append(client_demonstration_duty)
        general_market_duties.append(work_for_tips_duty)

        general_supply_duties = []
        general_supply_duties.append(supply_work_duty)
        general_supply_duties.append(heavy_supply_work_duty)
        general_supply_duties.append(greymarket_deals_duty)
        general_supply_duties.append(alternative_payment_duty)

        general_production_duties = []
        general_production_duties.append(production_work_duty)
        general_production_duties.append(heavy_production_work_duty)
        general_production_duties.append(bend_safety_rules_duty)

        general_hr_duties = []
        general_hr_duties.append(hr_work_duty)
        general_hr_duties.append(heavy_hr_work_duty)
        general_hr_duties.append(find_infractions_duty)
        general_hr_duties.append(encourage_loyalty_duty)
        general_hr_duties.append(internal_propaganda_duty)
        general_hr_duties.append(corrupt_work_chat_duty)
        #TODO: Dudies to raise Obedience, Love, Sluttiness

    return
