init 0 python:
    def bedroom_masturbate_requirement():
        if time_of_day >= 4:
            return "Not enough time."
        elif mc.location.get_person_count() > 0:
            return "Not with someone around."
        elif mc.business.event_triggers_dict["Tutorial_Section"]:
            return "Not enough time."
        else:
            return True

    def cheat_menu_requirement():
        return True

label faq_loop:
    menu:
        "Gameplay Basics.":
            menu:
                "Making Serum.":
                    "Vren" "Making serum in your lab is the most important task for success in Lab Rats 2. You begin the game with a fully equipt lab."
                    "Vren" "A serum design is made up of a number of serum traits. You decide what traits you want to include when you create a design."
                    "Vren" "Serum traits modify the effects of a serum. The effects can be simple - increasing duration or Suggestion increase - or may be more complicated."
                    "Vren" "Each serum design has a limited number of trait slots. The number of slots can be increased by using more advanced serum production techniques."
                    "Vren" "Once you have decided on the traits you wish to include in your serum you will have to spend time in the lab researching it."
                    "Vren" "Place the design in the research queue and spend a some time working in the lab."
                    "Vren" "More complicated serums will take more time to research. Once the serum is completely researched it can be produced by your production division."
                    "Vren" "Move to your production division and slot the new design into the current production queue."
                    "Vren" "Before you can produce the serum you will need raw supplies."
                    "Vren" "One unit of supply is needed for every production point the serum requires. You can order supply from your main office."
                    "Vren" "Once you have supplies you can spend time in your production lab. Serum is made in batches - unlocking larger batches will let you make more serum with the same amount of supply."
                    "Vren" "You can kepp this serum for personal use or you can head to the main office and mark it for sale."
                    "Vren" "Once a serum is marked for sale you can spend time in your marketing division to find a buyer."
                    "Vren" "Your research and development lab can also spend time researching new traits for serum instead of producing new serum designs."

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
                    "Vren" "Having sex with a girl is necessaryto increase her sluttiness to the highest levels. Higher arousal will make a girl more willing to strip down or have sex."
                    "Vren" "If you are able to make a girl cum she will immediately start to turn Temporary sluttiness into core sluttiness."
                    "Vren" "As a girls Sluttiness increases she will be more willing to wear revealing clothing or have sex with you."
                    "Vren" "As her Obedience increase she will be more deferential. She may be willing to have sex simply because you ask, even if she is not normally slutty enough."

                "Leveling Up.":
                    "Vren" "There are three main catagories of experience: Stats, Work Skills, and Sex Skills."
                    "Vren" "For each of these catagories you will have a goal assigned. When that goal is completed you will receive one point to spend on any of the scores in that catagory."
                    "Vren" "Once per day you may also scrap a goal that is overly difficult or not possible to complete yet."
                    "Vren" "When you complete a goal future goals in that catagory will increase in difficulty. Spend your early points wisely!"
                    "Vren" "Some goals are only checked at the end of the day or end of a turn, so if you have a goal that should be completed but is not giving you the option try advancing time."

        "Development Questions.":
            menu:
                "Will there be more character poses?":
                    "Vren" "Absolutely! The current standing poses proved that the rendering workflow for the game is valid, which means I will be able to introduce character poses for different sex positions."
                    "Vren" "Most sex positions have character poses associated with them and new poses will be rendered with each update."

                "Why are their holes in some pieces of clothing?":
                    "Vren" "Some character positions cause portions of the character model to poke out of their clothing when I am rendering them."
                    "Vren" "I will be adjusting my render settings and rerendering any clothing items that need it as we go forward."

        "Done.":
            return
    call faq_loop
    return

label bedroom_masturbation(location_description = "home", edging_available = True, should_advance_time = True): #Baseline efficiency for masturbating. Advances time, consumes energy, and releases Clarity inefficently.
    if location_description == "home":
        "You sit down in front of your computer and start to look around for some porn to jerk off to."

    if mc.masturbation_novelty >= 95:
        "You have the entire internet's worth of porn at your fingertips, so it's not long before you're stroking your cock to some new porn."
    elif mc.masturbation_novelty >= 75:
        "You browse the internet for something hot to watch. After a few minutes you've found enough to entertain you and start to stroke your cock."
    elif mc.masturbation_novelty >= 60:
        "You browse the internet, but it's getting hard to find good porn you haven't seen before."
        "Soon you're searching one handed as you bounce from site to site, stroking yourself to keep hard until you find that perfect video to finish to."
    else:
        "You browse the internet, but it feels as if you've seen it all before."
        "Nothing new interests you, so you pull up some old favourites and jerk off to those instead."

    menu:
        "Jerk off and cum.":
            "You enjoy stroking yourself off for a long while."
            $ mc.change_locked_clarity(10)
            "Eventually you can feel the edge of your orgasm and push yourself towards it."
            $ climax_controller = ClimaxController(["Cum!", "masturbation"])
            $ climax_controller.show_climax_menu()
            $ climax_controller.do_clarity_release()
            "You grab desperately at some tissue as you start to cum, smothering your tip to avoid making a mess."

            "You take a few deep breaths as your climax passes, then wad up the spent tissues and chuck them into the trash."

        "Try and edge yourself." if edging_available:
            "You enjoy stroking yourself off for a long while."
            $ mc.change_locked_clarity(10)
            if renpy.random.randint(0,100) < 15*mc.focus + 10:
                # You manage to avoid climaxing
                "For a long while you edge yourself, pushing yourself to the edge of your orgasm and then slowing down."
                $ mc.change_locked_clarity(10)
                "It takes focus and willpower, but you're able to avoid making yourself cum. You feel like a dam ready to burst now."
                "You put your cock away, excited about the release you'll experience next time you climax."
            else:
                "For a long while you edge yourself, pushing yourself right to the edge of your climax before slowing down."
                "It only takes a momentary lapse of willpower for it all to fall apart. An unexpectly jiggle set of internet tits and you're suddenly past the point of no return."
                $ climax_controller = ClimaxController(["Cum!", "masturbation"])
                $ climax_controller.show_climax_menu()
                "You grab desperately at some tissue as you start to cum, smothering your tip to avoid making a mess."
                $ climax_controller.do_clarity_release()
                "You take a few deep breaths as your climax passes, then wad up the spent tissues and chuck them into the trash."

    if should_advance_time:
        call advance_time()
    return

label cheat_menu():
    #TODO; Check to see if it's a patron account. Of course for the patron release I'm _sure_ only patrons end up with this copy, so no need to worry about it now!
    menu:
        "+$10,000.":
            $ mc.business.change_funds(10000)
        "+5000 Clarity.":
            $ mc.add_clarity(5000)
        "Unlock all Clarity.":
            $ mc.convert_locked_clarity(with_novelty = 100)
        "+1 Stat Point.":
            $ mc.buy_point("stat")
        "+1 Work Skill Point.":
            $ mc.buy_point("work")
        "+1 Sex Skill Point.":
            $ mc.buy_point("sex")
        "+25 Family Sluttiness.":
            $ mom.change_slut(25)
            $ lily.change_slut(25)
            $ cousin.change_slut(25)
            $ aunt.change_slut(25)
        "+25 Family Obedience.":
            $ mom.change_obedience(25)
            $ lily.change_obedience(25)
            $ cousin.change_obedience(25)
            $ aunt.change_obedience(25)
        "+25 Family Love.":
            $ mom.change_love(25)
            $ lily.change_love(25)
            $ cousin.change_love(25)
            $ aunt.change_love(25)
        "+1 research tier.":
            $ mc.business.research_tier += 1
        "Research all serum traits.":
            python:
                for a_trait in list_of_traits:
                    if not isinstance(a_trait, SerumTraitBlueprints): #Don't research trait blueprints; they have special rules.
                        a_trait.unlock_trait(pay_clarity = False)
                        a_trait.researched = True
            "All base serum traits researched."
    return
