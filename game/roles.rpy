# This file holds the initialization information and general storyline info for all of the roles in the game. Individual roles and individual files.
init -1 python:
    def prostitute_requirement(the_person):
        if mc.business.funds < 200:
            "Not enough cash"
        elif mc.current_stamina < 1:
            "Requires: 1 Stamina"
        elif the_person.sexed_count >= 1:
            "She's worn out. Maybe later."
        else:
            return True

label instantiate_roles(): #This section instantiates all of the key roles in the game. It is placed here to ensure it is properly created, saved, ect. by Renpy.
    #All of the role labels and requirements are defined in their own file, but their Action representitions are stored here for saving purposes.
    python:
        #EMPLOYEE ACTIONS#
        move_employee_action = Action("Move her to a new division", move_employee_requirement, "move_employee_label",
            menu_tooltip = "Move her to a new division, where her skills might be put to better use.")
        employee_complement_action = Action("Compliment her work.", employee_complement_requirement, "employee_complement_work",
            menu_tooltip = "Offer a few kind words about her performance at work. Increases happiness and love, dependent on your charisma.")
        employee_insult_action = Action("Insult her work.", employee_insult_requirement, "insult_recent_work",
            menu_tooltip = "Offer a few choice words about her performance at work. Lowers love and happiness, but is good for instilling obedience.")
        employee_pay_cash_action = Action("Pay her a cash bonus.", employee_pay_cash_requirement, "employee_pay_cash_bonus",
            menu_tooltip = "A bonus in cold hard cash is good for obedience and happiness. The larger the reward the greater the effect.")
        employee_performance_review = Action("Start a performance review. {image=gui/heart/Time_Advance.png}", employee_performance_review_requirement , "employee_performance_review",
            menu_tooltip = "Bring her to your office for a performance review. Get her opinion about her job, reward, punish, or fire her as you see fit. Can only be performed once every seven days.")

        employee_role = Role("Employee", [employee_complement_action, employee_insult_action, employee_pay_cash_action, employee_performance_review, move_employee_action])

        #HEAD RESEARCHER ACTIONS#
        improved_serum_unlock = Action("Ask about advancing your research.", improved_serum_unlock_requirement, "improved_serum_unlock_label",
            menu_tooltip = "Your basic initial research can only take you so far. You will need a breakthrough to discover new serum traits.")

        visit_nora_intro = Action("Visit Nora to try and advance your research.", visit_nora_intro_requirement, "nora_intro_label",
            menu_tooltip = "Have your head researcher reach out to your old mentor to see if she can help advance your research.")

        advanced_serum_unlock_stage_1 = Action("Ask about advancing your research.", advanced_serum_stage_1_requirement, "advanced_serum_stage_1_label",
            menu_tooltip = "Another breakthrough will unlock new serum traits.")

        advanced_serum_unlock_stage_3 = Action("Present with recording of prototype serum test.", advanced_serum_stage_3_requirement, "advanced_serum_stage_3_label",
            menu_tooltip = "Your new head researcher will have to take over now, and this recording should help them.")

        futuristic_serum_unlock_stage_1 = Action("Ask about advancing your research.", futuristic_serum_stage_1_requirement, "futuristic_serum_stage_1_label",
            menu_tooltip = "You will need another breakthrough to unlock new serum traits.") #First time you ask about it

        futuristic_serum_unlock_stage_2 = Action("Talk about the test subjects.", futuristic_serum_stage_2_requirement, "futuristic_serum_stage_2_label",
            menu_tooltip = "Your head researcher needs willing, dedicated test subjects to advance your research any further.") #Talk to her to either select test subjects or get a refresher on what you need.


        fire_head_researcher_action = Action("Remove her as head reseracher.", fire_head_researcher_requirement, "fire_head_researcher",
            menu_tooltip = "Remove her as your head researcher so you can select another. Without a head researcher your R&D department will be less efficent.")

        head_researcher = Role("Head Researcher", [fire_head_researcher_action,improved_serum_unlock,advanced_serum_unlock_stage_1, visit_nora_intro, advanced_serum_unlock_stage_3,futuristic_serum_unlock_stage_1, futuristic_serum_unlock_stage_2])


        #MODEL ACTIONS#

        model_ad_photo_list = Action("Shoot pictures for an advertisement. {image=gui/heart/Time_Advance.png}", model_photography_list_requirement, "model_photography_list_label")

        fire_model_action = Action("Remove her as your company model.", fire_model_requirment, "fire_model_label",
            menu_tooltip = "Remove her as your company model so you can give the position to someone else. Effects from existing ad campaigns will continue until they expire.")

        company_model_role = Role("Model", [model_ad_photo_list])


        #STEPH ACTIONS#

        steph_role = Role("Stephanie", [], hidden = True) #Used to hold any Stephanie specific actions not tied to another role, and to guarantee this is Steph even if she undergoes a personality change.

        #NORA ROLE#

        nora_role = Role("Nora", [], hidden = True)

        #ALEXIA ACTIONS#
        alexia_ad_reintro = Action("Have her order photography equipment. -$500", alexia_ad_suggest_reintro_requirement, "alexia_ad_suggest_reintro_label")

        alexia_ad_photo_intro = Action("Shoot pictures for your business cards. {image=gui/heart/Time_Advance.png}", alexia_photography_intro_requirement, "alexia_photography_intro_label") #This vent leads to Alexia being given the model role.

        alexia_role = Role("Alexia", [alexia_ad_reintro, alexia_ad_photo_intro], hidden = True) #Hide her role because we don't want to display it.

        #SISTER ACTIONS#
        sister_reintro_action = Action("Ask if she needs extra work.", sister_reintro_action_requirement, "sister_reintro_label",
            menu_tooltip = "She was eager to make some money before, maybe she still is.")

        sister_serum_test_action = Action("Ask her to test serum.", sister_serum_test_requirement, "sister_serum_test_label",
            menu_tooltip = "Have your sister test serum for you. Over time she will become more comfortable following your orders and making deals with you.")


        sister_strip_reintro_action = Action("Ask if she would strip for pay.", sister_strip_reintro_requirement, "sister_strip_reintro_label",
            menu_tooltip = "She was eager to make some money, maybe she will be willing to strip for you if you pay her.")

        sister_strip_action = Action("Ask her to strip for you.", sister_strip_requirement, "sister_strip_label",
            menu_tooltip = "Have your sister strip for you, in exchange for some money.")

        sister_role = Role("Sister", [sister_reintro_action, sister_serum_test_action, sister_strip_reintro_action, sister_strip_action])


        #MOTHER ACTIONS#
        mother_offer_make_dinner = Action("Offer to make dinner. {image=gui/heart/Time_Advance.png}", mom_offer_make_dinner_requirement, "mom_offer_make_dinner_label",
            menu_tooltip = "Earn some good will by making dinner for your mother and sister.")

        mother_role = Role("Mother", [mother_offer_make_dinner])


        #AUNT ACTIONS#
        aunt_help_move = Action("Help her move into her apartment. {image=gui/heart/Time_Advance.png}", aunt_intro_moving_apartment_requirement, "aunt_intro_moving_apartment_label",
            menu_tooltip = "Help your aunt and your cousin move their stuff from your house to their new apartment. They're sure to be grateful, and it would give you a chance to snoop around.")

        aunt_share_drinks_action = Action("Share a glass of wine. {image=gui/heart/Time_Advance.png}", aunt_share_drinks_requirement, "aunt_share_drinks_label",
            menu_tooltip = "Sit down with your aunt and share a glass or two of wine. Maybe a little bit of alcohol will loosen her up a bit.")

        aunt_role = Role("Aunt", [aunt_help_move,aunt_share_drinks_action])


        #COUSIN ACTIONS#
        cousin_blackmail_action = Action("Blackmail her.", cousin_blackmail_requirement, "cousin_blackmail_label",
            menu_tooltip = "Threaten to tell her mother about what she's been doing and see what you can get out of her.")

        cousin_role = Role("Cousin", [cousin_blackmail_action])



        ####################
        #RELATIONSHIP ROLES# TODO TODO TODO
        ####################

        #GIRLFRIEND ACTIONS#
        # Give her gifts (bonus happiness + Love)
        # She tests serum for you for free.
        # Go on dates (Remove this option from the normal chat menu?)
        # If she has (of age) kids, meet them (and, amazingly, they're hot young women!)

        #Other things to add#
        # Enables new girlfriend specific crises.
        # Adds more love to seduction attempts (reduce love from other sources)
        # Fallout if your girlfriend catches you with someone else.


        girlfrind_role = Role("Girlfriend", []) #Your girlfriend, and she's not in a relationship with anyone else
        #Getting married is some kind of victory for the game?


        #AFFAIRE ACTIONS
        # Sneaky versions of all of the normal girlfriend stuff
        # Have her get money from her (b/f/h) and give it to you.
        # Convince her to leave her (boyfriend/fiance/husband) for you. Changes to her being your girlfriend.
        # Start to blackmail her for money or sex.

        affaire_role = Role("Affaire", []) #A women who, if she were single, would be your girlfriend but is in a relationship.


        ###################
        ### OTHER ROLES ###
        ###################

        prostitute_action = Action("Pay her for sex. -$200", prostitute_requirement, "prostitute_label",
            menu_tooltip = "You know she's a prostitute, pay her to have sex with you.")

        prostitute_role = Role("Prostitute", [prostitute_action])
    return




label pay_strip_scene(the_person):
    # TODO: Figure out where this scene should go, since this file should be a pure role-define section.
    #A loop where someone strips if you pay them. Not nessicarily limited to the Lily-MC relationship.
    #Concept: tell the girl what position to stand in and ask her to take things off for you. If her outfit is conservative she'll strip for free, when it starts to get slutty she'll want extra cash.
    #High obedience will sub in for sluttiness; an obedient girl will strip just because you ask.
    #Compliment, insult, etc. to change some of her stats.

    #Requirements: Person can be told to stand in a few different positions. Some are unlocked at higher sluttiness.
    #Requirements: Person can be asked to take off clothing.
    #Requirements: Some they will strip off on their own.
    #Requirements: Person will demand some amount of $$$ while stripping if they feel it's slutty.
    #Requirements: Person will have different descriptions of stripping/dancing depending on sluttiness.
    #Optional: Some way to ask the person to change into a different outfit.
    #Optional: Way to progress from strip tease to sex and/or mastribation.

    $ pose_list = [["Turn around","walking_away"],["Turn around and look back","back_peek"],["Hands down, ass up.","standing_doggy"],["Be flirty","stand2"],["Be casual","stand3"],["Strike a pose","stand4"],["Move your hands out of the way","stand5"]]

    $ picked_pose = the_person.idle_pose #She starts in her idle pose (which is a string)
    $ rand_strip_desc = renpy.random.randint(0,3) #Produce 4 different descriptions at each level to help keep this interesting.

    # strip_willingness is a measure of how into the whole strip process the girl is. The less dressed she get the more embarassed she'll get,
    # the more slutty the more she'll tease you, take clothing off willingly, etc.
    $ strip_willingness = the_person.sluttiness + (5*the_person.get_opinion_score("not wearing anything")) - the_person.outfit.slut_requirement
    #If there are other things that influence how willing a person is to strip they go here!

    $ keep_stripping = True #When set to false the loop ends and the strip show stops.

    while keep_stripping:
        $ the_person.draw_person(position = picked_pose)
        if strip_willingness < 0:
            if rand_strip_desc == 0:
                "[the_person.title] blushes intensely while you watch her."
            elif rand_strip_desc == 1:
                if the_person.has_large_tits():
                    "[the_person.title] instinctively tries to cover herself with her hands, but her large tits make it a difficult task."
                else:
                    "[the_person.title] instinctively tries to cover herself with her hands."
            elif rand_strip_desc == 2:
                the_person.char "Oh my god..."
                "[the_person.title] covers her eyes for a moment and looks away."
            else:
                "[the_person.title] shakes her head and mutters to herself."
                the_person.char "I can't believe I'm doing this..."

        elif strip_willingness < 20:
            if rand_strip_desc == 0:
                "[the_person.title] stands awkwardly in front of you and avoids making eye contact."
            elif rand_strip_desc == 1:
                if the_person.has_large_tits():
                    "[the_person.title] shifts her weight from side to side while you watch her. The small movements still make her big tits jiggle around."
                else:
                    "[the_person.title] shifts her weight from side to side while you watch her."
            elif rand_strip_desc == 2:
                "You get a good look at [the_person.title] while she stands in front of you."
            else:
                "[the_person.title] blushes and looks around the room to avoid making eye contact."

        elif strip_willingness < 60:
            $tease_clothing = the_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True) #She's slutty enough that she wants to tease you a little more
            if rand_strip_desc == 0:
                if tease_clothing is not None:
                    "[the_person.title] pulls at her [tease_clothing.name] seductively."
                    the_person.char "Mmm, I bet you want me to take this off, right?"
                else:
                    "[the_person.title] runs her hands down her body seductively."
                    the_person.char "Mmm, I bet you want to get your hands on me now, right?"

            elif rand_strip_desc == 1:
                if the_person.has_large_tits():
                    "[the_person.title] moves her body side to side for you, letting her large tits bounce and jiggle while you watch."
                else:
                    "[the_person.title] moves her body side to side for you while you watch."

            elif rand_strip_desc == 2:
                if tease_clothing is not None:
                    "[the_person.title] slips a hand under her [tease_clothing.name] and starts to pull it off."
                    the_person.char "Maybe I should just... slip this off. What do you think?"
                else:
                    if the_person.has_large_tits():
                        "[the_person.title]'s hands slide up and down her body. She cups one of her sizeable breast and squeezes it, pinching her own nipple while she does."
                    else:
                        "[the_person.title]'s hands slide up and down her body. She rubs her small breasts, paying special attention to their firm nipples."
            else:
                the_person.char "I hope you're enjoying the show [the_person.mc_title]."
                "She wiggles her hips for you and winks."

        else: #strip_willingness >= 60
            $tease_clothing = the_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True) #She's slutty enough that she wants to tease you a little more
            if rand_strip_desc == 0:
                if tease_clothing is not None:
                    "[the_person.title] pulls at her [tease_clothing.name]."
                    the_person.char "I'm going to have to get this out of the way before we can have any fun."
                else:
                    "[the_person.title] runs her hands over her own body."
                    the_person.char "Oh [the_person.mc_title], I think I'm going to need more than your eyes on me soon..."

            elif rand_strip_desc == 1:
                "[the_person.title] puts her hands up in the air and spins around. You get a great look at her body as she enjoys herself."

            elif rand_strip_desc == 2:
                if tease_clothing is not None:
                    the_person.char "Don't you just think all of this clothing is just useless? How about I take it all off for you... would you like that?"
                else:
                    "[the_person.title] takes a wider stances and slides her hands down her own thighs, all while maintaining eye contact with you."
                    the_person.char "You're looking so good today [the_person.mc_title], did you know that?"

            else:
                "[the_person.title] wiggles her hips side to side and bites her bottom lip, as if imagining some greater pleasure yet to come."

        $menu_list = [] #Tuple of menu things.
        # High obedience characters are more willing to be told to strip down (althoug they still expect to be paid for it)
        # Low obedience characters will strip off less when told but can be left to run the show on their own and will remove some.
        python:
            for item in the_person.outfit.get_unanchored():
                if not item.is_extension:
                    test_outfit = the_person.outfit.get_copy()
                    test_outfit.remove_clothing(item)
                    new_willingness = the_person.sluttiness + (5*the_person.get_opinion_score("not wearing anything")) - test_outfit.slut_requirement
                    if new_willingness + (the_person.obedience-100) >= 0:
                        #They're willing to strip it off.
                        price = 0 # Default value
                        if new_willingness >= 40:
                            price = 0 #They'll do it for free!

                        elif new_willingness >= 20:
                            price = (strip_willingness - new_willingness) * 3 #They feel pretty good about how they'll be dressed after, so the price is decent.

                        else:
                            price = (strip_willingness - new_willingness) * 10 #THey will feel pretty uncomfortable, so they expect to be paid well.

                        price = math.ceil((price/5.0))*5 #Round up to the next $5 increment

                        display_string = "Strip " + item.name + "\n{size=22}$" + str(price) + "{/size}"
                        if price > mc.business.funds:
                            display_string += " (disabled)"

                        menu_list.append([display_string, [item,price]])

                    else:
                        menu_list.append(["Strip " + item.name + "\n{size=22}Too Slutty{/size} (disabled)", [item,-1]])

            menu_list.append(["Just watch.","Watch"])
            menu_list.append(["Tell her to pose.","Pose"])
            menu_list.append(["Finish the show.","Finish"])

        $ strip_choice = renpy.display_menu(menu_list,True,"Choice")
        if strip_choice == "Watch":
            if renpy.random.randint(0,1) == 0:
                $ tease_item = the_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True) #The clothing item she's considering taking off
                $ free_spirit_threshold = 40 + (100 - the_person.obedience)
                if renpy.random.randint(0,100) < free_spirit_threshold: #She's independant enough to strip, change pose, etc. on her own.
                    if tease_item is not None and new_willingness >= (the_person.obedience-100): #A more obedient person is less willing to strip without being told to. A less obedient person will strip further on their own.
                        $ test_outfit = the_person.outfit.get_copy()
                        $ test_outfit.remove_clothing(tease_item)
                        $ new_willingness = the_person.sluttiness + (5*the_person.get_opinion_score("not wearing anything")) - test_outfit.slut_requirement
                        $ price = 0
                        if new_willingness >= 40: #She's slutty enough to do it for free!
                            $ price = 0
                        elif new_willingness >= 20:
                            $ price = (strip_willingness - new_willingness) * 3
                        else:
                            $ price = (strip_willingness - new_willingness) * 10

                        $ price = math.ceil((price/5.0))*5 #Round up to the next $5 increment
                        if price > 0:
                            "[the_person.title] steps a little closer to you and plays with the edge of her [tease_item.name]."
                            the_person.char "$[price] and I'll take this off for you..."
                            menu:
                                "Pay her $[price]." if price <= mc.business.funds:
                                    "You pull the cash out of your wallet and hand it over."
                                    $ mc.business.funds += -price
                                    $ the_person.change_obedience(-1)
                                    $ the_person.change_slut_temp(1)
                                    $ the_person.draw_animated_removal(tease_item, position = picked_pose)
                                    "[the_person.title] takes it, puts it to the side, and starts to slide her [tease_item.name] off."


                                "Pay her $[price]. (disabled)" if price > mc.business.funds:
                                    pass

                                "Don't pay her.":
                                    mc.name "I think you look good with it on."
                                    "[the_person.title] seems disappointed but shrugs and keeps going."

                        else:
                            $ the_person.draw_animated_removal(tease_item, position = picked_pose)
                            "You watch as [the_person.title] grabs their [tease_item.name] and pulls it off."
                    else:
                        #She has nothing to strip off or she's as slutty as she's willing to get
                        "[the_person.title] seems comfortable just the way she is."

                else: #She doesn't quite know what to do without you telling her.
                    "Without any direction [the_person.title] just keeps doing what she was doing."

            else:
                #She decides to change pose half the time.
                $ new_pose = get_random_from_list(pose_list)
                if not new_pose[1] == picked_pose:
                    $ picked_pose = new_pose[1]
                    "While you're watching [the_person.title] changes pose so you can see her from a different angle."
                else:
                    "[the_person.title] seems comfortable just the way she is."


        elif strip_choice == "Pose":
            #You ask her to change into a different pose
            mc.name "I want to see you from a different angle."
            $pose_menu_tuple = []
            python:
                for pose_tuple in pose_list:
                    if not pose_tuple[1] == picked_pose:
                        pose_menu_tuple.append(pose_tuple)
                pose_menu_tuple.append(["Nevermind.",None])

            $ pose_choice = renpy.display_menu(pose_menu_tuple,True,"Choice")
            if pose_choice is not None:
                $ picked_pose = pose_choice
                "[the_person.title] nods and moves for you."

            else:
                mc.name "Nevermind, you look perfect like this."

        elif strip_choice == "Finish":
            $ keep_stripping = False
            mc.name "That was fun [the_person.title], I think that's enough."
            if strip_willingness < 0:
                "[the_person.title] sighs happily."
                the_person.char "Oh my god, I thought I was going to die of embarrassment!"
            elif strip_willingness < 20:
                the_person.char "Oh, okay. That... wasn't as bad as I thought it was going to be, at least."
            else:
                the_person.char "Oh, is that all you wanted to see? I feel like we were just getting started!"

        else: #The only other result is an actual strip. Pay the cash, remove the piece and loop or end.
            $ mc.business.funds += -strip_choice[1]
            $ test_outfit = the_person.outfit.get_copy() #We use a temp copy so that we can get her reaction first.
            $ test_outfit.remove_clothing(strip_choice[0])
            $ the_clothing = strip_choice[0]
            # $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
            $ strip_willingness = the_person.sluttiness + (5*the_person.get_opinion_score("not wearing anything")) - test_outfit.slut_requirement
            if strip_choice[1] > 0:
                if strip_willingness < 0:
                    "You pull some cash from your wallet and offer it to [the_person.title]. She takes it and looks at it for a long second."
                    the_person.char "Oh my god... I shouldn't be doing this..."
                    $ the_person.change_obedience(2)
                    $ the_person.change_slut_temp(1)
                    "Nevertheless, she keeps the money and pulls off her [the_clothing.name]."
                    $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
                elif strip_willingness < 20:
                    "You pull some cash out from your wallet and hand it over to [the_person.title]. She puts it to the side and grabs her [the_clothing.name]."
                    the_person.char "Ready?"
                    $ the_person.change_obedience(1)
                    $ the_person.change_slut_temp(1)
                    $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
                    "You nod and [the_person.title] pulls off the piece of clothing, throwing it to the side."
                else:
                    "You're still pulling out cash as [the_person.title] strips off her [the_clothing.name] and chucks it to the side."
                    $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
                    the_person.char "Thank you!"
                    "She plucks the cash from your hand and quickly puts it away."

            else: #She'll only do it for free if she's becoming less slutty (ie taking off lingerie, bondage gear, etc.) or if she's very slutty anyways.
                the_person.char "Is that all? Well, I think that's easy."
                $ the_person.draw_animated_removal(strip_choice[0], position = picked_pose)
                "[the_person.title] strips off her [the_clothing.name] for free, leaving it on the ground at her feet."

    return


label prostitute_label(the_person):
    mc.name "[the_person.title], I'm looking for a friend to spend some time with. Are you available?"
    the_person.char "If you're paying I am."
    $ mc.business.funds += -200
    $ the_person.change_obedience(1)

    $ add_situational_obedience("prostitute", 40, "I'm being paid for this, I should do whatever he wants me to do.")
    call fuck_person(private = True) from _call_fuck_person_23
    $ the_person.clear_situational_obedience("prostitute")
    if the_person.arousal >= 100:
        "It takes [the_person.title] a few moments to catch her breath."
        the_person.char "Maybe I should be paying you... Whew!"
    $ the_person.reset_arousal()
    $ the_person.review_outfit()

    the_person.char "That was fun, I hope you had a good time [the_person.mc_title]."
    "She gives you a quick peck on the cheek."
    $ renpy.scene("Active")
    return
