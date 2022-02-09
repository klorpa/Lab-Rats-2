init -3 python: #Init -3 is used for all project wide imports of external resources
    import os
    import copy
    import math
    import __builtin__
    import xml.etree.ElementTree as ET
    import time
    import zipfile
    import io
    from collections import defaultdict
    from collections import OrderedDict
    import unittest
    import unicodedata
    import sys
    from functools import partial
    import re
    import string
    from operator import attrgetter


#Init -2 establishes all game clases
#Init -1 is then used by all game content that will use those game classes (ie. instantiates different Crises that could be generated)
#Init 0 establishes Renpy settings, including callbacks for display code.

init -1: # Establish some platform specific stuff.
    # if renpy.macintosh:
    #     #default persistent.vren_animation = True
    #     $ persistent.vren_mac_scale = 1.0 #2.0 # Changes to the way the surface size is calculated has made a mac specific setting like this oboslete. This section is only here until I can confirm everything is working properly.
    #
    # else:
    #     default persistent.vren_animation = True
    #     $ persistent.vren_mac_scale = 1.0

    default persistent.vren_animation = True #By default animation is enabled if possible. If it's not possible because it's on mobile toggling it just does nothing for now.
    default persistent.pregnancy_pref = 0 # 0 = no content, 1 = predictable, 2 = realistic
    default persistent.vren_display_pref = "Float" # "Float" = no BG, "Frame" = Frame with coloured BG for most interactions.

    python:
        list_of_instantiation_labels = [] #Strings added to this list will be called at the start of the game. Use to initialize things which need their game state saved.
        # label should take no parameters.

        list_of_positions = [] # These are sex positions that the PC can make happen while having sex.
        list_of_girl_positions = [] # These are sex positiosn that the girl can make happen while having sex.
        list_of_strip_positions = [] # These are positiosn a girl can take while putting on a stirp tease for you.


        day_names = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"] #Arrays that hold the names of the days of the week and times of day. Arrays start at 0.
        time_names = ["Early Morning","Morning","Afternoon","Evening","Night"]

init 0 python:
    global mobile_zip_dict
    mobile_zip_dict = {}
    for position in ["stand2", "stand3", "stand4", "stand5", "walking_away", "back_peek", "sitting", "kissing", "doggy", "missionary", "blowjob", "against_wall", "standing_doggy", "kneeling1", "cowgirl"]:
        file_path = "images/character_images/" + position + ".zip"
        renpy_file = renpy.file(file_path)
        mobile_zip_dict[position] = zipfile.ZipFile(renpy_file, "a") #Cache all of the zip files so we have a single static pointer to them.

    #config.use_cpickle = False #Set to True for more useful save failure info

    #config.interact_callbacks.append(take_animation_screenshot)
    config.history_callbacks.append(text_message_history_callback) #Ensures conversations had via text are recorded properly
    # config.say_arguments_callback = text_message_say_callback #Recolours and re-fonts say statements made while having a text conversation #NOTE: NOt needed now that we properly store messages into the phone and display them from a custom screen.

    config.gl2 = True  #Required to enable the model based renderer and use shaders.

    config.predict_screen_statements = True
    config.predict_statements = 50
    config.predict_screens = True

    config.cache_surfaces = True
    config_image_cache_size = 8

    config.has_autosave = False
    config.autosave_frequency = None
    config.has_quicksave = True


    config.rollback_enabled = True #Disabled for the moment because there might be unexpected side effects of such a small rollback length.
    config.rollback_length = 32

    if persistent.colour_palette is None or len(persistent.colour_palette) < 20:
        persistent.colour_palette = []
        for x in range(0,20):
            persistent.colour_palette.append([1,1,1,1])

    config.autoreload = False

    #config.debug_text_overflow = True
    config.debug_text_overflow = False #If enabled finds locations with text overflow. Turns out I have a lot, kind of blows up when enabled and generates a large text file. A problem for another day.

    config.debug_image_cache = False
    config.debug = True

    # THIS IS WHAT PREVENTS IT FROM INDEXING IMAGES
    # SEE 00images.rpy for where this is created
    config.images_directory = None
    preferences.gl_tearing = True ## Prevents juttery animation with text while using advanced shaders to display images #TODO: Double check if this actually does anything anymore.

    _preferences.show_empty_window = False #Prevents Ren'py from incorrectly showing the text window in complex menu sitations (which was a new bug/behaviour in Ren'py v7.2)

    global draw_layers
    draw_layers = []

    add_draw_layer("front_1") # Layer used for extra characters. For example, drawing a preview while still showing a group in the back
    add_draw_layer("solo") # Add the main default draw layer, used for all single character displays

    build.classify("game/images/character_images/**stand2**.png", None) # unarchived images for the different positiosn are not needed, they are all included in .zip files.
    build.classify("game/images/character_images/**stand3**.png", None)
    build.classify("game/images/character_images/**stand4**.png", None)
    build.classify("game/images/character_images/**stand5**.png", None)
    build.classify("game/images/character_images/**walking_away**.png", None)
    build.classify("game/images/character_images/**back_peek**.png", None)
    build.classify("game/images/character_images/**sitting**.png", None)
    build.classify("game/images/character_images/**kissing**.png", None)
    build.classify("game/images/character_images/**doggy**.png", None)
    build.classify("game/images/character_images/**missionary**.png", None)
    build.classify("game/images/character_images/**blowjob**.png", None)
    build.classify("game/images/character_images/**against_wall**.png", None)
    build.classify("game/images/character_images/**standing_doggy**.png", None)
    build.classify("game/images/character_images/**kneeling1**.png", None)
    build.classify("game/images/character_images/**cowgirl**.png", None)

    build.classify("game/images/character_images/**.zip", "all")

label start:
    scene bg paper_menu_background with fade
    "Lab Rats 2 contains adult content. If you are not over 18 or your country's equivalent age you should not view this content."
    menu:
        "I am over 18.":
            "Excellent, let's continue then."

        "I am not over 18.":
            $renpy.full_restart()

    "Vren" "[config.version] represents an early iteration of Lab Rats 2. Expect to run into limited content, unexplained features, and unbalanced game mechanics."
    "Vren" "Would you like to view the FAQ?"
    menu:
        "View the FAQ.":
            call faq_loop
        "Get on with the game!":
            "You can access the FAQ from your bedroom at any time."

    "Vren" "Lab Rats 2 contains content related to impregnation and pregnancy. These settings may be changed in the menu at any time."
    menu:
        "No pregnancy content.\n{size=16}Girls never become pregnant. Most pregnancy content hidden.{/size}":
            $ persistent.pregnancy_pref = 0

        "Predictable pregnancy content.\n{size=16}Birth control is 100%% effective. Girls always default to taking birth control.{/size}":
            $ persistent.pregnancy_pref = 1

        "Realistic pregnancy content.\n{size=16}Birth control is not 100%% effective. Girls may not be taking birth control.{/size}":
            $ persistent.pregnancy_pref = 2

    $ renpy.block_rollback()
    call screen character_create_screen()
    $ return_arrays = _return #These are the stat, skill, and sex arrays returned from the character creator.
    call initialize_game_state(store.name,store.b_name,store.l_name,return_arrays[0],return_arrays[1],return_arrays[2])
    $ renpy.block_rollback()
    menu:
        "Play introduction and tutorial.":
            call tutorial_start

        "Skip introduction and tutorial.":
            $ mc.business.event_triggers_dict["Tutorial_Section"] = False
    jump normal_start

label normal_start:
    ## For now, this ensures reloading the game doesn't reset any of the variables.
    $ renpy.scene()
    show screen tooltip_screen
    show screen phone_hud_ui
    show screen business_ui
    show screen goal_hud_ui
    show screen main_ui
    $ bedroom.show_background()
    "It's Monday, and the first day of operation for your new business!"
    "[stephanie.title] said she would meet you at your new office for a tour."
    #TODO: Have an on_enter event for Steph if you see her the first day. Minor interaction stuff.

    #Add Stepyhanie to our business and flag her with a special role.

    $ mc.business.add_employee_research(stephanie)
    $ mc.business.r_div.add_person(stephanie) #Lets make sure we actually put her somewhere
    $ mc.business.r_div.move_person(stephanie,lobby)
    $ setup_employee_stats(stephanie)
    $ stephanie.add_role(head_researcher)
    $ mc.business.head_researcher = stephanie

    #TODO: movement overlay tutorial thing.
    jump game_loop

label game_loop(): ##THIS IS THE IMPORTANT SECTION WHERE YOU DECIDE WHAT ACTIONS YOU TAKE
    $ people_list = []
    $ people_list.extend(mc.location.people)
    $ actions_list = []

    $ actions_list.append(["Check your phone.", "Phone"])
    $ actions_list.extend(mc.location.get_valid_actions())

    $ people_list.sort(key = sort_display_list, reverse = True)
    $ actions_list.sort(key = sort_display_list, reverse = True)

    $ actions_list.insert(0,["Go somewhere else.", "Travel"])
    if time_of_day == 4:
        if sleep_action not in mc.location.actions: #If they're in a location they can sleep we shouldn't show this because they can just sleep here.
            $ actions_list.insert(0, ["Go home and sleep.{image=gui/heart/Time_Advance.png}{image=gui/heart/Time_Advance.png} (tooltip)It's late. Go home and sleep.", "Wait"])
    else:
        $ actions_list.insert(0, ["Wait here\n{image=gui/heart/Time_Advance.png}, +10 Extra {image=gui/extra_images/energy_token.png} (tooltip)Kill some time and wait around. Recovers more energy than working.", "Wait"])
    $ actions_list.insert(0,"Do Something")
    $ people_list.insert(0,"Talk to Someone")


    call screen main_choice_display([people_list,actions_list], person_preview_args = {"show_person_info":False})

    $ picked_option = _return
    if isinstance(picked_option, Person):
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
            if talk_action in picked_option.on_talk_event_list: #This shouldn't come up much, but it an event is double removed this helps us fail gracefully.
                $ picked_option.on_talk_event_list.remove(talk_action)


        else:
            if picked_option.title is None:
                "You decide to approach the stranger and introduce yourself."
            else:
                "You approach [picked_option.title] and chat for a little bit."
                $ picked_option.call_dialogue("greetings")

            if picked_option.has_taboo(["underwear_nudity","bare_tits", "bare_pussy"]) and picked_option.judge_outfit(picked_option.outfit, -30): #If she's in anything close to slutty she's self-conscious enough to coment on it.
                if picked_option.outfit.vagina_visible() and picked_option.has_taboo("bare_pussy") and picked_option.outfit.tits_visible() and picked_option.has_taboo("bare_tits"):
                    "[picked_option.title] doesn't say anything about it, but seems unconfortable being naked in front of you."
                    "As you talk she seems to become more comfortable with her own nudity, even if she isn't thrilled by it."

                if picked_option.outfit.vagina_visible() and picked_option.has_taboo("bare_pussy"):
                    "[picked_option.title] doesn't say anything about it, but angles her body to try and conceal her bare pussy from you."
                    "As you talk she seems to become more comfortable, even if she isn't thrilled about it."

                elif picked_option.outfit.tits_visible() and picked_option.has_taboo("bare_tits"):
                    "[picked_option.title] doesn't say anything about it, but brings her arms up to try and conceal her tits."
                    if picked_option.has_large_tits():
                        "Her large chest isn't easy to hide, and she quickly realises it's hopeless."
                    else:
                        "As you talk she seems to become more comfortable, and eventaully lets her arms drop again."

                elif ((picked_option.outfit.wearing_panties() and not picked_option.outfit.panties_covered()) or (picked_option.outfit.wearing_bra() and not picked_option.outfit.bra_covered())) and picked_option.has_taboo("underwear_nudity"):
                    "[picked_option.title] doesn't say anything about it, but she tries to cover up her underwear with her hands."
                    "As you talk she seems to become more comfortable, and eventually she lets her arms drop to her sides."

                $ picked_option.update_outfit_taboos()
            call talk_person(picked_option) from _call_talk_person

    elif isinstance(picked_option, Action):
        $ picked_option.call_action()


    elif picked_option == "Travel":
        call screen map_manager
        $ new_location = _return
        call change_location(new_location) from _call_change_location #_return is the location returned from the map manager.
        if new_location.people: #There are people in the room, let's see if there are any room events
            $ enabled_people_events = []
            $ enabled_room_events = []
            python: #Scan through all the people and...
                for a_person in new_location.people:
                    for possible_person_event in a_person.on_room_enter_event_list:
                        if possible_person_event.is_action_enabled(a_person): #See what events the are enabled...
                            enabled_people_events.append([a_person, possible_person_event]) #Then keep track of the person so we know who to remove it from if it triggers.

                for possible_room_event in new_location.on_room_enter_event_list:
                    if possible_room_event.is_action_enabled():
                        enabled_room_events.append(possible_room_event)

            if enabled_people_events: #If there are room events to take care of run those right now.
                $ picked_event = get_random_from_list(enabled_people_events)
                $ picked_event[0].on_room_enter_event_list.remove(picked_event[1]) #Remove the event from their list since we will be running it.
                $ picked_event[1].call_action(picked_event[0]) #Run the action with the person as an extra argument.

            elif enabled_room_events:
                $ picked_event = get_random_from_list(enabled_room_events)
                $ new_location.on_room_enter_event_list.remove(picked_event)
                $ picked_event.call_action()

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
                    $ clear_scene()

    elif picked_option == "Phone":
        call browse_internet() from _call_browse_internet

    elif picked_option == "Wait":
        if time_of_day == 4:
            $ mc.change_location(bedroom)
        else:
            $ mc.change_energy(10) #Extra 10 energy gain if you spend your time waiting around
        call advance_time from _call_advance_time_15
        $ mc.location.show_background() #Redraw the background in case it has changed due to the new time.

    jump game_loop


label change_location(the_place):
    $ renpy.scene()
    $ the_place.show_background()
    if the_place.trigger_tutorial and the_place.tutorial_label is not None and mc.business.event_triggers_dict.get("Tutorial_Section",False):
        $ the_place.trigger_tutorial = False
        $ renpy.call(the_place.tutorial_label)

    return

label talk_person(the_person, keep_talking = True):
    $ mc.having_text_conversation = None #Just in case some event hasn't properly reset this.
    # $ the_person.draw_person() #Removed v0.28.1, this was often called when no character change was required. Character draw should be handled by events that lead into this label if required.
    if the_person.title is None:
        call person_introduction(the_person) from _call_person_introduction #If their title is none we assume it is because we have never met them before. We have a special introduction scene for new people.
        #Once that's done we continue to talk to the person.





    $ specific_actions_list = ["Say goodbye.", command_action, grope_action]

    python:
        chat_list = []
        specific_actions_list = ["Say goodbye"]
        special_role_actions = []

        for act in chat_actions:
            if keep_talking or act.is_fast:
                chat_list.append([act, the_person])

        for act in specific_actions:
            if keep_talking or act.is_fast:
                specific_actions_list.append([act, the_person])

        for role in the_person.special_role:
            for act in role.actions:
                if keep_talking or act.is_fast:
                    special_role_actions.append([act, the_person]) #They're a list of actions and their extra arg so that gets passed through properly.

        for act in mc.main_character_actions: #The main character has a "role" that lets us add special actions as well.
            if keep_talking or act.is_fast:
                special_role_actions.append([act,the_person])

        chat_list.sort(key = sort_display_list, reverse = True)
        chat_list.insert(0,"Chat with her")

        specific_actions_list.sort(key = sort_display_list, reverse = True)
        specific_actions_list.insert(0,"Do something specific")

        special_role_actions.sort(key = sort_display_list, reverse = True)
        special_role_actions.insert(0,"Special Actions")

    call screen main_choice_display([chat_list, specific_actions_list, special_role_actions])

    $ explicit_exit = True # Use to check if the player selected an explicit "stop talking" option
    if isinstance(_return, Action):
        $ starting_time_of_day = time_of_day
        $ _return.call_action(the_person)

        if the_person in mc.location.people and time_of_day == starting_time_of_day and keep_talking:
            call talk_person(the_person) from _call_talk_person_1 #If we're in the same place and time hasn't advanced keep talking to them until we stop talking on purpose.

        $ explicit_exit = False
    $ clear_scene()
    return explicit_exit

label advance_time:
    # 1) Turns are processed _before_ the time is advanced.
    # 1a) crises are processed if they are triggered.
    # 2) Time is advanced, day is advanced if required.
    # 3) People go to their next intended location.
    # Then: Add research crisis when serum is finished, requiring additional input from the player and giving the chance to test a serum on the R&D staff.

    $ mandatory_advance_time = False #If a crisis returns an "Advance Time" value once this turn is finished processing it will process ANOTHER turn, so a crisis can require a turn to pass.

    python:
        people_to_process = [] #This is a master list of turns of need to process, stored as tuples [character,location]. Used to avoid modifying a list while we iterate over it, and to avoid repeat movements.
        for place in list_of_places:
            for people in place.people:
                people_to_process.append([people,place])

    python:
        for (people,place) in people_to_process: #Run the results of people spending their turn in their current location.
            people.run_turn() #T

        mc.business.run_turn()
        mc.run_turn()


    #We make sure that all mandatory crises are run here. Mandatory crises always trigger as soon as they are able, possibly with multiple crises triggering in a single turn.
    $ count = 0
    $ max = len(mc.business.mandatory_crises_list)
    $ clear_list = []
    while count < max: #We need to keep this in a renpy loop, because a return call will always return to the end of an entire python block.
        $ crisis = mc.business.mandatory_crises_list[count]
        if crisis.is_action_enabled():
            $ crisis.call_action()
            if _return == "Advance Time":
                $ mandatory_advance_time = True
            $ clear_scene()
            $ clear_list.append(crisis)
        $ count += 1
    $ mc.location.show_background()
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
            if _return == "Advance Time":
                $ mandatory_advance_time = True

    $ clear_scene()
    $ renpy.scene()
    $ mc.location.show_background()
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
                $ renpy.say("","Warning! Your company is losing money and unable to pay salaries or purchase necessary supplies!")
                $ renpy.say("","You have [days_remaining] days to restore yourself to positive funds or the bank will reclaim the business!")
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
                if _return == "Advance Time":
                    $ mandatory_advance_time = True
                $ clear_scene()
                $ clear_list.append(crisis)
            $ count += 1
        $ mc.location.show_background()
        python: #Needs to be a different python block, otherwise the rest of the block is not called when the action returns.
            for crisis in clear_list:
                mc.business.mandatory_morning_crises_list.remove(crisis) #Clean up the list.


        if renpy.random.randint(0,100) < 15: # We run morning crises 5% of all mornings
            python:
                possible_morning_crises = []
                for crisis in morning_crisis_list:
                    if crisis[0].is_action_enabled(): #Get the first element of the weighted tuple, the action.
                        possible_morning_crises.append(crisis) #Build a list of valid crises from ones that pass their requirement.
            $ the_morning_crisis = get_random_from_weighted_list(possible_morning_crises)
            if the_morning_crisis:
                $ the_morning_crisis.call_action()
                if _return == "Advance Time":
                    $ mandatory_advance_time = True

        $ renpy.free_memory()

    else:
        $ time_of_day += 1 ##Otherwise, just run the end of day code.

    python:
        for (people,place) in people_to_process: #Now move everyone to where the should be in the next turn. That may be home, work, etc.
            people.run_move(place)

            if people.title is not None: #We don't assign events to people we haven't met.
                if renpy.random.randint(0,100) < 15: #Only assign one to 15% of people, to cut down on the number of people we're checking.
                    possible_crisis_list = []
                    for crisis in limited_time_event_pool:
                        if crisis[0].is_action_enabled(people): #Get the first element of the weighted tuple, the action.
                            possible_crisis_list.append(crisis) #Build a list of valid crises from ones that pass their requirement.

                    the_crisis = get_random_from_weighted_list(possible_crisis_list, return_everything = True)
                    if the_crisis is not None:
                        limited_time_event = Limited_Time_Action(the_crisis[0], the_crisis[0].event_duration) #Wraps the action so that we can have an instanced duration counter and add/remove it easily.\
                        #renpy.notify("Created event: " + the_crisis[0].name + " for " + people.name)
                        if the_crisis[2] == "on_talk":
                            people.on_talk_event_list.append(limited_time_event)

                        elif the_crisis[2] == "on_enter":
                            people.on_room_enter_event_list.append(limited_time_event)

    $ mc.business.run_move() # In each phase it runs people->MC->Business. Policy effects are run as part of the business, and so can overwrite/alter things an employee has done (like wear their uniform)


    $ mc.location.show_background()
    if mandatory_advance_time: #If a crisis has told us to advance time after it we do so.
        call advance_time from _call_advance_time_28

    $ people_to_process = [] #Clears the memory used here.
    return


label initialize_game_state(character_name,business_name,last_name,stat_array,skill_array,_sex_array,max_num_of_random=4): #Gets all of the variables ready. TODO: Move some of this stuff to an init block?

    ##Global Variable Initialization##
    $ day = 0 ## Game starts on day 0.
    $ time_of_day = 0 ## 0 = Early morning, 1 = Morning, 2 = Afternoon, 3 = Evening, 4 = Night

    $ list_of_traits = [] #List of serum traits that can be used. Established here so they play nice with rollback, saving, etc.
    $ list_of_nora_traits = []
    $ list_of_side_effects = [] #List of special serum traits that are reserved for bad results.

    #NOTE: These need to be established in a seperate label to ensure they are loaded/saved correctly
    call instantiate_serum_traits() #Creates all of the default LR2 serum traits. TODO: Create a mod loading list that has labels that can be externally added and called here.
    call instantiate_side_effect_traits()
    call instantiate_roles()
    call instantiate_business_policies()


    python:
        list_of_places = [] #By having this in an init block it may be set to null each time the game is reloaded, because the initialization stuff below is only called once.

        ##Work Actions##
        hr_work_action = Action("Organize your business.\n{image=gui/heart/Time_Advance.png}",hr_work_action_requirement,"hr_work_action_description",
            menu_tooltip = "Raise business efficiency, which drops over time based on how many employees the business has.\n+3*Charisma + 2*Skill + 1*Intelligence + 5 Efficiency.")
        research_work_action = Action("Research in the lab.\n{image=gui/heart/Time_Advance.png}",research_work_action_requirement,"research_work_action_description",
            menu_tooltip = "Contribute research points towards the currently selected project.\n+3*Intelligence + 2*Skill + 1*Focus + 10 Research Points.")
        supplies_work_action = Action("Order supplies.\n{image=gui/heart/Time_Advance.png}",supplies_work_action_requirement,"supplies_work_action_description",
            menu_tooltip = "Purchase serum supply at the cost of $1 per unit of supplies. When producing serum every production point requires one unit of serum.\n+3*Focus + 2*Skill + 1*Charisma + 10 Serum Supply.")
        market_work_action = Action("Find new clients.\n{image=gui/heart/Time_Advance.png}",market_work_action_requirement,"market_work_action_description",
            menu_tooltip = "Find new clients who may be interested in buying serum from you, increasing your Market reach. Important for maintaining good Aspect prices.\n+(3*Charisma + 2*Skill +1*Focus)*5 Market Reach.")
        production_work_action = Action("Produce serum.\n{image=gui/heart/Time_Advance.png}",production_work_action_requirement,"production_work_action_description",
            menu_tooltip = "Produce serum from raw materials. Each production point of serum requires one unit if supply, which can be purchased from your office.\n+3*Focus + 2*Skill + 1*Intelligence + 10 Production Points.")

        ##Breakthrough Actions##
        mc_breakthrough_1 = Action("Have a Breakthrough\n-500 Clarity, {image=gui/heart/Time_Advance.png}", mc_breakthrough_requirement, "mc_research_breakthrough", args = [1, 500], requirement_args = [1, 500],
            menu_tooltip = "Put your intelect to work and unlock a new tier of research! There may be other was to achieve this breakthrough as well", priority = 100)
        mc_breakthrough_2 = Action("Have a Breakthrough.\n-5000 Clarity, {image=gui/heart/Time_Advance.png}", mc_breakthrough_requirement, "mc_research_breakthrough", args = [2, 5000], requirement_args = [2, 5000],
            menu_tooltip = "Put your intelect to work and unlock a new tier of research! There may be other was to achieve this breakthrough as well", priority = 100)
        mc_breakthrough_3 = Action("Have a Breakthrough.\n-25000 Clarity, {image=gui/heart/Time_Advance.png}", mc_breakthrough_requirement, "mc_research_breakthrough", args = [3, 25000], requirement_args = [3, 25000],
            menu_tooltip = "Put your intelect to work and unlock a new tier of research! There may be other was to achieve this breakthrough as well", priority = 100)

        ##Complex Work Actions##
        interview_action = Action("Hire someone new.\n{image=gui/heart/Time_Advance.png}", interview_action_requirement,"interview_action_description",
            menu_tooltip = "Look through the resumes of several candidates. More information about a candidate can be revealed by purchasing new business policies.")
        design_serum_action = Action("Create a new serum design.\n{image=gui/heart/Time_Advance.png}", serum_design_action_requirement,"serum_design_action_description",
            menu_tooltip = "Combine serum traits to create a new design. Once a design has been created it must be researched before it can be put into production.")
        pick_research_action = Action("Assign Research Project.", research_select_action_requirement,"research_select_action_description",
            menu_tooltip = "Pick the next research topic for your R&D division. Serum designs must be researched before they can be put into production.")
        pick_production_action = Action("Set production settings.", production_select_action_requirement,"production_select_action_description",
            menu_tooltip = "Decide what serum designs are being produced. Production is divided between multiple factory lines, and auto sell thresholds can be set to automatically flag serum for sale.")
        pick_supply_goal_action = Action("Set the amount of supply you would like to maintain.", pick_supply_goal_action_requirement,"pick_supply_goal_action_description",
            menu_tooltip = "Set a maximum amount of serum you and your staff will attempt to purchase.")
        policy_purhase_action = Action("Manage business policies.", policy_purchase_requirement,"policy_purchase_description",
            menu_tooltip = "New business policies changes the way your company runs and expands your control over it. Once purchased business policies are always active.")
        set_head_researcher_action = Action("Select a Head Researcher.", head_researcher_select_requirement, "head_researcher_select_description",
            menu_tooltip = "Pick a member of your R&D staff to be your head researcher. A head resercher with a high intelligence score will increase the amount of research produced by the entire division.")
        trade_serum_action = Action("Access production stockpile.", trade_serum_action_requirement, "trade_serum_action_description",
            menu_tooltip = "Move serum to and from your personal inventory. You can only use serum you are carrying with you.")
        sell_serum_action = Action("Sell Serum.", sell_serum_action_requirement, "sell_serum_action_description",
            menu_tooltip = "Review your current stock of serum, accept and complete contracts, and check the current market prices.")
        review_designs_action = Action("Review serum designs.", review_designs_action_requirement, "review_designs_action_description",
            menu_tooltip = "Shows all existing serum designs and allows you to delete any you no longer desire.")
        set_company_model_action = Action("Pick a company model.", pick_company_model_requirement, "pick_company_model_description",
            menu_tooltip = "Pick one your employees to be your company model. You can run ad campaigns with your model, increasing the value of every dose of serum sold.")

        #PC Bedroom actions#
        sleep_action = Action("Go to sleep for the night.\n{image=gui/heart/Time_Advance.png}{image=gui/heart/Time_Advance.png}",sleep_action_requirement,"sleep_action_description",
            menu_tooltip = "Go to sleep and advance time to the next day. Overnight counts as three turns when calculating serum durations.", priority = 20)
        bedroom_masturbate_action = Action("Masturbate.\n{image=gui/heart/Time_Advance.png}", bedroom_masturbate_requirement, "bedroom_masturbation",
            menu_tooltip = "Jerk off. A useful way to release Clarity, but you'll grow bored of this eventually.")

        ##Mom Bedroom Actions##
        mom_room_search_action = Action("Search [mom.title]'s room. -15{image=gui/extra_images/energy_token.png}", mom_room_search_requirement, "mom_room_search_description",
            menu_tooltip = "Take a look around and see what you can find.")

        faq_action = Action("Check the FAQ.",faq_action_requirement,"faq_action_description",
            menu_tooltip = "Answers to frequently asked questions about Lab Rats 2.")


        downtown_search_action = Action("Wander the streets.\n{image=gui/heart/Time_Advance.png}", downtown_search_requirement, "downtown_search_label",
            menu_tooltip = "Spend time exploring the city and seeing what interesting locations it has to offer.")


        strip_club_show_action = Action("Watch a show. -$20", stripclub_show_requirement, "stripclub_dance",
            menu_tooltip = "Take a seat and wait for the next girl to come out on stage.")

        mom_office_person_request_action = Action("Approach the receptionist.", mom_office_person_request_requirement, "mom_office_person_request",
            menu_tooltip = "The receptionist might be able to help you, if you're looking for someone.")


        import_wardrobe_action = Action("Import a wardrobe file.", faq_action_requirement, "wardrobe_import",
            menu_tooltip = "Select and import a wardrobe file, adding all outfits to your current wardrobe.")

        ## Temp and Test Actions
        test_action = Action("Temp test action.", integration_test_dev_requirement, "debug_label")
        integration_test_action = Action("Run Integration Tests.", integration_test_dev_requirement, "run_integration_tests")



        ##Actions unlocked by policies##
        set_uniform_action = Action("Manage Employee Uniforms.",set_uniform_requirement,"uniform_manager_loop")
        set_serum_action = Action("Set Daily Serum Doses.",set_serum_requirement,"set_serum_description")


        ##PC's Home##
        hall = Room("main hall","Home", background_image = standard_house_backgrounds[:],
            map_pos = [3,3], lighting_conditions = standard_indoor_lighting)
        bedroom = Room("your bedroom", "Your Bedroom", background_image = standard_bedroom_backgrounds[:],
            actions = [sleep_action,bedroom_masturbate_action,faq_action,integration_test_action, test_action],
            map_pos = [3,2], lighting_conditions = standard_indoor_lighting)
        lily_bedroom = Room("Lily's bedroom", "Lily's Bedroom", background_image = standard_bedroom_backgrounds[:],
            map_pos = [2,3], lighting_conditions = standard_indoor_lighting)
        mom_bedroom = Room("your mom's bedroom", "Mom's Bedroom", background_image = standard_bedroom_backgrounds[:],
            actions = [mom_room_search_action],
            map_pos = [2,4], lighting_conditions = standard_indoor_lighting)
        kitchen = Room("kitchen", "Kitchen", background_image = standard_kitchen_backgrounds[:],
            map_pos = [3,4], lighting_conditions = standard_indoor_lighting)

        home_bathroom = Room("bathroom", "Bathroom", background_image = home_bathroom_background,
            map_pos = [0,0], visible = False) #Note: Only used by special events. Not connected to the main map


        ##PC's Work##
        lobby = Room(business_name + " lobby",business_name + " Lobby", background_image = standard_office_backgrounds[:],
            map_pos = [11,3], tutorial_label = "lobby_tutorial_intro", lighting_conditions = standard_indoor_lighting)
        office = Room("main office","Main Office", background_image = standard_office_backgrounds[:],
            actions = [policy_purhase_action,hr_work_action,supplies_work_action,interview_action,pick_supply_goal_action,set_uniform_action,set_serum_action],
            map_pos = [11,2], tutorial_label = "office_tutorial_intro", lighting_conditions = standard_indoor_lighting)
        m_division = Room("marketing division","Marketing Division", background_image = standard_office_backgrounds[:],
            actions = [sell_serum_action, market_work_action,set_company_model_action],
            map_pos = [12,3], tutorial_label = "marketing_tutorial_intro", lighting_conditions = standard_indoor_lighting)
        rd_division = Room("R&D division","R&D Division", background_image = lab_background,
            actions = [research_work_action,design_serum_action,pick_research_action,review_designs_action,set_head_researcher_action, mc_breakthrough_1, mc_breakthrough_2, mc_breakthrough_3],
            map_pos = [12,4], tutorial_label = "research_tutorial_intro", lighting_conditions = standard_indoor_lighting)
        p_division = Room("Production division", "Production Division",background_image = standard_office_backgrounds[:],
            actions = [production_work_action,pick_production_action,trade_serum_action],
            map_pos = [11,4], tutorial_label = "production_tutorial_intro", lighting_conditions = standard_indoor_lighting)


        ##Connects all Locations##
        downtown = Room("downtown","Downtown", background_image = standard_downtown_backgrounds[:],
            actions = [downtown_search_action],public = True,
            map_pos = [6,4], lighting_conditions = standard_outdoor_lighting)

        ##A mall, for buying things##
        mall = Room("mall","Mall", background_image = standard_mall_backgrounds[:], public = True,
            map_pos = [8,2], lighting_conditions = standard_indoor_lighting)
        gym = Room("gym","Gym", background_image = standard_mall_backgrounds[:], public = True,
            map_pos = [7,1], lighting_conditions = standard_indoor_lighting)
        home_store = Room("home improvement store","Home Improvement Store", background_image = standard_mall_backgrounds[:], public = True,
            map_pos = [8,1], lighting_conditions = standard_indoor_lighting)
        sex_store = Room("sex store","Sex Store", background_image = standard_mall_backgrounds[:], public = True,
            map_pos = [9,2], lighting_conditions = standard_indoor_lighting)
        clothing_store = Room("clothing store","Clothing Store", background_image = standard_mall_backgrounds[:],
            actions = [import_wardrobe_action], public = True,
            map_pos = [8,3], lighting_conditions = standard_indoor_lighting)
        office_store = Room("office supply store","Office Supply Store", background_image = standard_mall_backgrounds[:], public = True,
            map_pos = [9,1], lighting_conditions = standard_indoor_lighting)
        electronics_store = Room("electornics store", "Electronics Store", background_image = standard_mall_backgrounds[:], public = True,
            map_pos = [7,2], lighting_conditions = standard_indoor_lighting)


        ##Other Locations##
        aunt_apartment = Room("Rebecca's Apartment", "Rebecca's Apartment", background_image = standard_house_backgrounds[:],
            map_pos = [4,2], visible = False, lighting_conditions = standard_indoor_lighting)
        aunt_bedroom = Room("Rebecca's bedroom", "Rebecca's Bedroom", background_image = standard_bedroom_backgrounds[:],
            map_pos = [3,1],visible = False, lighting_conditions = standard_indoor_lighting)
        cousin_bedroom = Room("Gabrielle's bedroom", "Gabrielle's Bedroom", background_image = standard_bedroom_backgrounds[:],
            map_pos = [4,1], visible = False, lighting_conditions = standard_indoor_lighting)

        university = Room("university Campus", "University Campus", background_image = standard_campus_backgrounds[:],
            map_pos = [9,5], visible = False, lighting_conditions = standard_outdoor_lighting)

        strip_club_owner = get_random_male_name()
        strip_club = Room(strip_club_owner + "'s Gentlemen's Club", strip_club_owner + "'s Gentlemen's Club", background_image = stripclub_background,
            actions = [strip_club_show_action],
            map_pos = [6,5], visible = False, lighting_conditions = standard_club_lighting)

        mom_office_name = get_random_male_name() + " and " + get_random_male_name() + " Ltd."
        mom_office_lobby = Room(mom_office_name + " Lobby", mom_office_name + " Lobby", background_image = standard_office_backgrounds[:],
            actions = [mom_office_person_request_action],
            map_pos = [5,4], lighting_conditions = standard_indoor_lighting)
        mom_offices = Room(mom_office_name + " Offices", mom_office_name + " Offices", background_image = standard_office_backgrounds[:],
            map_pos = [5,5], visible = False, lighting_conditions = standard_indoor_lighting)


        bar_location = Room("Bar", "Bar", background_image = standard_bar_backgrounds[:],
            map_pos = [10,10], visible = False, lighting_conditions = standard_indoor_lighting)

        city_hall = Room("City Hall", "City Hall", background_image = standard_house_backgrounds[:],
            map_pos = [20,20], visible = False, lighting_conditions = standard_indoor_lighting)

        ##PC starts in his bedroom##
        main_business = Business(business_name, m_division, p_division, rd_division, office, office)
        mc = MainCharacter(bedroom,character_name,last_name,main_business,stat_array,skill_array,_sex_array)

        mc.change_locked_clarity(50, add_to_log = False) #PC starts with 50 locked clarity, which can be masturbated into the 25 Clarity needed to unlock the med trait.



        town_relationships = RelationshipArray() #Singleton class used to track relationships. Remvoes need for recursive character references (which messes with Ren'py's saving methods)
        mc.generate_goals()

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
        list_of_places.append(electronics_store)
        list_of_places.append(mall)

        list_of_places.append(aunt_apartment)
        list_of_places.append(aunt_bedroom)
        list_of_places.append(cousin_bedroom)
        list_of_places.append(university)
        list_of_places.append(strip_club)

        list_of_places.append(mom_office_lobby)
        list_of_places.append(mom_offices)

        list_of_places.append(city_hall)

        for room in [bedroom, lily_bedroom, mom_bedroom, aunt_bedroom, cousin_bedroom]:
            room.add_object(make_wall())
            room.add_object(make_floor())
            room.add_object(make_bed())
            room.add_object(make_window())

        home_bathroom.add_object(make_wall())
        home_bathroom.add_object(Object("shower door", ["Lean"]))#, sluttiness_modifier = 5, obedience_modifier = 5))
        home_bathroom.add_object(make_floor())

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

        mom_office_lobby.add_object(make_wall())
        mom_office_lobby.add_object(make_floor())
        mom_office_lobby.add_object(make_chair())
        mom_office_lobby.add_object(make_desk())
        mom_office_lobby.add_object(make_window())

        mom_offices.add_object(make_wall())
        mom_offices.add_object(make_floor())
        mom_offices.add_object(make_chair())
        mom_offices.add_object(make_desk())
        mom_offices.add_object(make_window())

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

        electronics_store.add_object(make_wall())
        electronics_store.add_object(make_floor())

        mall.add_object(make_wall())
        mall.add_object(make_floor())

        gym.add_object(make_wall())
        gym.add_object(make_floor())

        aunt_apartment.add_object(make_wall())
        aunt_apartment.add_object(make_floor())
        aunt_apartment.add_object(make_couch())
        aunt_apartment.add_object(make_table())
        aunt_apartment.add_object(make_chair())

        strip_club.add_object(make_wall())
        strip_club.add_object(make_floor())
        strip_club.add_object(make_table())
        strip_club.add_object(make_chair())
        strip_club.add_object(make_stage())

        city_hall.add_object(make_wall())
        city_hall.add_object(make_floor())
        city_hall.add_object(make_chair())
        city_hall.add_object(make_table())

    call instantiate_jobs() #We need locations to exist before we can set up jobs, so we do that here.
    $ c = 0
    while c < len(list_of_instantiation_labels):
        $ renpy.call(list_of_instantiation_labels[c])
        $ c += 1
    python:
        generate_premade_list() # Creates the list with all the premade characters for the game in it. Without this we both break the policies call in create_random_person, and regenerate the premade list on each restart.

        for place in list_of_places:
            if place.public:
                if not max_num_of_random == 0:
                    random_count = renpy.random.randint(1,max_num_of_random)
                else:
                    random_count = 0;
                for x in range(0,random_count):
                    the_person = create_random_person()
                    the_person.generate_home()
                    place.add_person(the_person) #We are using create_random_person instead of make_person because we want premade character bodies to be hirable instead of being eaten up by towns-folk.

        stripclub_strippers = []
        stripclub_wardrobe = wardrobe_from_xml("Stripper_Wardrobe")
        for i in __builtin__.range(0,4):
            a_girl = create_random_person(start_sluttiness = renpy.random.randint(15,30), job = stripper_job)
            a_girl.generate_home()
            strip_club.add_person(a_girl)

        business_wardrobe = wardrobe_from_xml("Business_Wardrobe") #Used in some of Mom's events when we need a business-ish outfit

    return
