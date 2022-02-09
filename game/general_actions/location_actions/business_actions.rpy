init 0 python:
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
        elif mc.business.get_used_line_weight() == 0:
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
        if mc.business.head_researcher is not None:
            return False
        elif __builtin__.len(mc.business.research_team) == 0:
            return "Nobody to pick."
        else:
            return True

    def pick_company_model_requirement():
        if mc.business.company_model is not None:
            return False
        elif not public_advertising_license_policy.is_active():
            return False
        elif mc.business.get_employee_count() == 0:
            return "Nobody to pick."
        else:
            return True

    def set_uniform_requirement():
        return strict_uniform_policy.is_active()

    def set_serum_requirement():
        if daily_serum_dosage_policy.is_owned() and not daily_serum_dosage_policy.is_active():
            return "Policy not active."
        else:
            return daily_serum_dosage_policy.is_active()

    def review_designs_action_requirement():
        return True

    def mc_breakthrough_requirement(new_level, clarity_cost):
        if mc.business.research_tier+1 != new_level:
            return False
        elif clarity_cost > mc.free_clarity:
            return "Not enough Clarity."
        elif time_of_day >= 4:
            return "Too late to work."
        else:
            return True

label sleep_action_description:
    "You go to bed after a hard days work."
    call advance_time from _call_advance_time
    return

label faq_action_description:
    call faq_loop
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
    if recruitment_batch_three_policy.is_active():
        $ count = 10
    elif recruitment_batch_two_policy.is_active():
        $ count = 6
    elif recruitment_batch_one_policy.is_active():
        $ count = 4

    $ interview_cost = mc.business.recruitment_cost
    "Bringing in [count] people for an interview will cost $[interview_cost]. Do you want to spend time interviewing potential employees?"
    menu:
        "Yes, I'll pay the cost. -$[interview_cost]":
            $ mc.business.change_funds(-interview_cost)
            $ clear_scene()
            $ renpy.free_memory() #Try and free available memory
            python: #Build our list of candidates with our proper recruitment requirements
                candidates = []

                for x in range(0,count+1): #NOTE: count is given +1 because the screen tries to pre-calculate the result of button presses. This leads to index out-of-bounds, unless we pad it with an extra character (who will not be reached).
                    candidates.append(make_person(mc.business.generate_candidate_requirements()))

                reveal_count = 0
                reveal_sex = False
                if recruitment_knowledge_one_policy.is_active():
                    reveal_count += 2
                if recruitment_knowledge_two_policy.is_active():
                    reveal_count += 2
                if recruitment_knowledge_three_policy.is_active():
                    reveal_count += 1
                    reveal_sex = True
                if recruitment_knowledge_four_policy.is_active():
                    reveal_count += 1
                for a_candidate in candidates:
                    for x in __builtin__.range(0,reveal_count): #Reveal all of their opinions based on our policies.
                        a_candidate.discover_opinion(a_candidate.get_random_opinion(include_known = False, include_sexy = reveal_sex),add_to_log = False) #Get a random opinion and reveal it.
            call hire_select_process(candidates) from _call_hire_select_process
            $ candidates = [] #Prevent it from using up extra memory
            $ renpy.free_memory() #Try and force a clean up of unused memory.

            if not _return == "None":
                $ new_person = _return
                $ new_person.generate_home() #Generate them a home location so they have somewhere to go at night.
                call hire_someone(new_person, add_to_location = True) from _call_hire_someone #
                $ new_person.set_title(get_random_title(new_person))
                $ new_person.set_possessive_title(get_random_possessive_title(new_person))
                $ new_person.set_mc_title(get_random_player_title(new_person))
            else:
                "You decide against hiring anyone new for now."
            call advance_time from _call_advance_time_6
        "Nevermind.":
            pass
    return

label hire_select_process(candidates):
    hide screen main_ui #NOTE: We have to hide all of these screens because we are using a fake (aka. non-screen) background for this. We're doing that so we can use the normal draw_person call for them.
    hide screen phone_hud_ui
    hide screen business_ui
    hide screen goal_hud_ui
    $ show_candidate(candidates[0]) #Show the first candidate, updates are taken care of by actions within the screen.
    show bg paper_menu_background #Show a paper background for this scene.
    $ count = __builtin__.len(candidates)-1
    call screen interview_ui(candidates,count)
    $ renpy.scene()
    show screen phone_hud_ui
    show screen business_ui
    show screen goal_hud_ui
    show screen main_ui
    $ clear_scene()
    $ mc.location.show_background()

    return _return


label hire_someone(new_person, add_to_location = False, research_allowed = True, production_allowed = True, supply_allowed = True, marketing_allowed = True, hr_allowed = True): # Breaks out some of the functionality of hiring someone into an independent lable.
    # python:
        # new_person.event_triggers_dict["employed_since"] = day
        # mc.business.listener_system.fire_event("new_hire", the_person = new_person)
        # for other_employee in mc.business.get_employee_list():
        #     town_relationships.begin_relationship(new_person, other_employee) #They are introduced to everyone at work, with a starting value of "Acquaintance"

    # $ setup_employee_stats(the_person) # Sets up relationships with everyone at work, the day they were hired, etc.

    "You complete the necessary paperwork and hire [_return.name]. What division do you assign her to?"
    menu:
        "Research and Development." if research_allowed:
            $ mc.business.add_employee_research(new_person)
            if add_to_location:
                $ mc.business.r_div.add_person(new_person)

        "Production." if production_allowed:
            $ mc.business.add_employee_production(new_person)
            if add_to_location:
                $ mc.business.p_div.add_person(new_person)

        "Supply Procurement." if supply_allowed:
            $ mc.business.add_employee_supply(new_person)
            if add_to_location:
                $ mc.business.s_div.add_person(new_person)

        "Marketing." if marketing_allowed:
            $ mc.business.add_employee_marketing(new_person)
            if add_to_location:
                $ mc.business.m_div.add_person(new_person)

        "Human Resources." if hr_allowed:
            $ mc.business.add_employee_hr(new_person)
            if add_to_location:
                $ mc.business.h_div.add_person(new_person)
    return

label serum_design_action_description:
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
    call screen research_select_ui
    show screen phone_hud_ui
    show screen business_ui
    show screen main_ui
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
    hide screen main_ui
    hide screen phone_hud_ui
    hide screen business_ui
    $ renpy.block_rollback()
    # call screen serum_trade_ui(mc.business.inventory,mc.business.sale_inventory,"Production Stockpile","Sales Stockpile")
    call screen serum_sell_ui()
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
    $ new_head.add_role(head_researcher)
    return

label pick_company_model_description:
    call screen employee_overview(white_list = mc.business.market_team,person_select = True)
    $ new_model = _return
    if new_model is not None:
        $ mc.business.company_model = new_model
        $ new_model.add_role(company_model_role)
    return

label uniform_manager_loop():
    call screen uniform_manager()
    if _return == "Add":
        call outfit_master_manager() #TODO: Decide if we need to pass this the uniform peramiters, of if we do that purely in what's selectable.
        if isinstance(_return, Outfit):
            $ mc.business.business_uniforms.append(UniformOutfit(_return))
            $ mc.business.listener_system.fire_event("add_uniform", the_outfit = _return)
        call uniform_manager_loop()
    return

# label set_uniform_description:
#     #First, establish the maximums the uniform can reach.
#     $ slut_limit, underwear_limit, limited_to_top = mc.business.get_uniform_limits() #Function generates all uniform related limits to keep them consistent between events and active/deavtive policies.
#
#
#     #Some quick holding variables to store the options picked.
#     $ selected_div = None
#     $ uniform_mode = None
#     $ uniform_type = None
#     menu:
#         "Add a complete outfit." if not limited_to_top:
#             $ uniform_mode = "full"
#
#         "Add a complete outfit.\n{size=22}Requires: Reduced Coverage Corporate Uniforms{/size} (disabled)" if limited_to_top:
#             pass
#
#         "Add an overwear set.":
#             $ uniform_mode = "over"
#
#         "Add an underwear set." if not limited_to_top:
#             $ uniform_mode = "under"
#
#         "Add an underwear set.\n{size=22}Requires: Reduced Coverage Corporate Uniforms{/size} (disabled)" if limited_to_top:
#             pass
#
#         "Remove a uniform or set.":
#             $ uniform_mode = "delete"
#
#
#     menu:
#         "Company Wide Uniforms.\n{size=22}Can be worn by everyone.{/size}": #Get the wardrobe we are going to be modifying.
#             $ selected_div = mc.business.all_uniform
#
#         "R&D Uniforms.":
#             $ selected_div = mc.business.r_uniform
#
#         "Production Uniforms.":
#             $ selected_div = mc.business.p_uniform
#
#         "Supply Procurement Uniforms.":
#             $ selected_div = mc.business.s_uniform
#
#         "Marketing Uniforms.":
#             $ selected_div = mc.business.m_uniform
#
#         "Human Resources Uniforms.":
#             $ selected_div = mc.business.h_uniform
#
#     if uniform_mode == "delete":
#         call screen outfit_delete_manager(selected_div) #Calls the wardrobe screen and lets teh player delete whatever they want.
#
#     else:
#         if uniform_mode == "full":
#             call outfit_master_manager(slut_limit = slut_limit) from _call_outfit_master_manager_3
#             $ new_outfit = _return
#             if new_outfit is None:
#                 return
#
#
#             $ mc.business.listener_system.fire_event("add_uniform", the_outfit = new_outfit, the_type = "full")
#             $ selected_div.add_outfit(new_outfit.get_copy())
#
#         elif uniform_mode == "under":
#             call outfit_master_manager(slut_limit = underwear_limit, show_outfits = False, show_underwear = True, show_overwear = False) from _call_outfit_master_manager_4
#             $ new_outfit = _return
#             if new_outfit is None:
#                 return
#
#             $ mc.business.listener_system.fire_event("add_uniform", the_outfit = new_outfit, the_type = "under")
#             $ selected_div.add_underwear_set(new_outfit.get_copy())
#
#         else: #uniform_mode == "over":
#             call outfit_master_manager(slut_limit = slut_limit, show_outfits = False, show_underwear = False, show_overwear = True) from _call_outfit_master_manager_5
#             $ new_outfit = _return
#             if new_outfit is None:
#                 return
#
#             $ mc.business.listener_system.fire_event("add_uniform", the_outfit = new_outfit, the_type = "over")
#             $ selected_div.add_overwear_set(new_outfit.get_copy())
#
#
#     return

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

label mc_research_breakthrough(new_level, clarity_cost):
    "You feel an idea in the back of your head. You realise it's been there this whole time, but you've been too distracted to see it."
    "You snatch up the nearest notebook and get to work right away."
    "Within minutes your thoughts are flowing fast and clear. Everything makes sense, and your path forward is made crystal clear."
    $ mc.spend_clarity(clarity_cost)
    $ mc.business.research_tier = new_level
    if new_level == 1:
        $ mc.log_event("Tier 1 Research Unlocked", "float_text_grey")
    elif new_level == 2:
        $ mc.log_event("Tier 2 Research Unlocked", "float_text_grey")
    else:
        $ mc.log_event("Max Research Tier Unlocked", "float_text_grey")
    "You throw your pen down when you're finished. Your new theory is awash in possibilities!"
    "Now you just need to research them in the lab!"
    return
