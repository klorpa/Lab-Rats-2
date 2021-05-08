init -1 python:
    def mom_room_search_requirement():
        if mom_bedroom.has_person(mom):
            return "Not with " + mom.title + " around."
        elif mc.energy < 15:
            return "Not enough {image=gui/extra_images/energy_token.png}"
        else:
            return True

label mom_room_search_description():
    $ mc.change_energy(-15)
    $ the_person = mom
    "You take a look around [the_person.possessive_title]'s bedroom."
    menu:
        "Investigate her bedstand.":
            #TODO: First thing you find are her BC pills if she's taking them.
            "[the_person.title] keeps her bedstand neat and tidy, just a lamp, an old clock radio, and a charging cable for her phone."
            if the_person.on_birth_control and persistent.pregnancy_pref != 0:
                "There is also has a blister pack of small blue pills. They must be her birth control pills."
                $ the_person.update_birth_control_knowledge()
                if the_person.event_triggers_dict.get("BC_nightstand_hide_day",-7) < day:
                    menu:
                        "Hide her birth control.":
                            $ the_person.event_triggers_dict["BC_nightstand_hide_day"] = day #Can't rehide it today, because she never stops until tomorrow anyways.
                            "You take the small pack and drop it down the crack between [the_person.possessive_title]'s bed and the bedstand."
                            "She'll probably find it if she takes the time to look, and even if she doesn't she doesn't she could pick some more up at the pharmacy any time."
                            "It would be so irresponsible for her to be unprotected just because it's slightly inconvenient to get more pills..."
                            if renpy.random.randint(0,100) < 5 + 5*the_person.get_opinion_score("bareback sex"): #She doesn't bother getting more. Just asking for trouble!
                                call manage_bc(start = True, update_knowledge = False) #Don't get BC info, because you don't know if she found it or not.

                        "Leave them alone.":
                            pass
                #TODO: Way to fuck with her BC, because evil is fun.

            "You slide open the single drawer to have a peek inside."
            if the_person.core_sluttiness < 10: # V. low sluttiness
                "The inside is as neat as the top, with a murder mystery novel sitting at the front of the otherwise empty drawer."
                "Disappointed, you slide hthe drawer closed again."
            elif the_person.core_sluttiness < 30: # Low sluttiness.
                "The inside is as neat as the top. The only thing inside is a well read, probably second hand novel."
                "The cover features a shirtless cowboy looking out over wide open plains and a herd of cattle."
                "The title reads \"A Fist Full of Bodices\", and [the_person.possessive_title] has dog-earred a bunch of pages."
                "You aren't terribly interested in reading through her cheap romance novel, so you slide the drawer closed again."
                pass
            elif the_person.core_sluttiness < 50: # Mid sluttiness.
                "The inside is as neat as the top, except for a cheap looking paper back novel."
                "The cover features a shirtless cowboy looking out over wide open plains and a herd of cattle."
                "The title reads \"A Fist Full of Bodices\", and [the_person.possessive_title] has dog-earred a bunch of pages."
                "You notice something tucked behind the romance novel. You push it to the side, revealing a small black piece of plastic about the size of tube of lipstick."
                "It's tapered at one end, flat on the other. It takes a moment for you to realise it must be a small vibrator."
                $ mc.change_locked_clarity(10)
                "You enjoy a moment imagining [the_person.possessive_title] on her bed, vibrator planted against her clit."
                "With nothing else to do you make sure everything is back in place and close the drawer again."

            elif the_person.core_sluttiness < 75: # High sluttiness. A larger rabbit vibrator, plus a small container of lube."
                $ mc.change_locked_clarity(10)
                "The inside isn't as prim and proper as the top is. The first thing you see as you open the drawer is a plum coloured dildo."
                "Coming off the base is a small forked section, the perfect length to rub against her clit while she plays with herself."
                "Laying down beside the toy is a travel sized bottle of lube, currently half empty."
                "You check around, but there's nothing else inside of the drawer. You make sure everything is where you found it, then close it up."

            else: # V. high sluttiness.
                "The moment you open the bedstand you find a large, white, wand style vibrator jammed kitty-corner inside."
                "Beside the wand is a slightly smaller plum dildo and a half-empty bottle of lube. The two toys are surrounded by loose batteries, either spares or already used up."
                $ mag_name = get_appropriate_mag_name(the_person, discover_opinion = True)
                "At the bottom of the of the drawer is a magazine, titled \"[mag_name]\"."
                $ mc.change_locked_clarity(10)
                "You take a moment and enjoy the thought of [the_person.possessive_title] naked and moaning happily with her toys between her legs."
                "When you're finished imagining you double check nothing is out of position and slide the drawer shut again."


        "Check her computer.":
            "[the_person.title] doesn't use her computer very often, but keeps it around in case she has to do some office work from home."
            "You turn the computer on and wait for it to boot up."
            if the_person.event_triggers_dict.get("known_computer_password", False): #If you don't know the password yet, try and guess it.
                "After a short wait the login screen comes up. You enter her password."
            else:
                "After a short wait the login screen comes up."
                "COMPUTER" "INPUT PASSWORD" (what_style = "text_message_style")
                $ password_attempt = renpy.input("")
                $ success = False
                if password_attempt.lower() == mc.name.lower():
                    $ the_person.event_triggers_dict["known_computer_password"] = True
                    $ success = True
                else:
                    "COMPUTER" "INCORRECT PASSWORD" (what_style = "text_message_style")

                while not success:
                    menu:
                        "Try again.":
                            "COMPUTER" "INPUT PASSWORD" (what_style = "text_message_style")
                            $ password_attempt = renpy.input("HINT: The oldest")
                            if password_attempt.lower() == mc.name.lower():
                                $ the_person.event_triggers_dict["known_computer_password"] = True
                                $ success = True
                            else:
                                "COMPUTER" "INCORRECT PASSWORD" (what_style = "text_message_style")

                        "Give up.":
                            "You give up and power down [the_person.possessive_title]'s computer."

            if the_person.event_triggers_dict.get("known_computer_password", False): #If you know the password at this point, no problem logging in."
                "COMPUTER" "WELCOME [the_person.title]!" (what_style = "text_message_style")
                if the_person.core_sluttiness < 15: # Nothing interesting to find
                    "[the_person.possessive_title] doesn't keep much on her computer, but you spend a few minutes poking through files anyways."
                    "You don't find anything other than reports from work and the family budget for the month."
                    "She's cleared her search history as well. Nothing interesting to find."
                elif the_person.core_sluttiness < 30:
                    "[the_person.possessive_title] doesn't keep much on her computer, but you spend a few minutes poking around anyways."
                    "All you find are work reports and the family budget. Next, you open up her browser."
                    "COMPUTER" "RESTORE BROWSING SESSION?" (what_style = "text_message_style")
                    "You hit \"Yes\", and her browser immediately takes you to \"A_Mothers_Advice.net\"."
                    "It seems to be an advice forum for mothers, and [the_person.title] was already looking at a post when she logged off last."
                    "Anon3342" "{b}(Advice Wanted) My Sex Drive is Back!?{/b}" (what_style = "text_message_style")
                    "Anon3342" "I'm the lucky single mother of two wonderful children. Both are growing up so fast, and are starting to leave the nest" (what_style = "text_message_style")
                    "Anon3342" "Raising them has always been my top priority, but lately something feels different. My libido has sky rocketed!" (what_style = "text_message_style")
                    "Anon3342" "I thought I was going to be in mother-mode for the rest of my life, but I feel like I'm a horny teenager again!" (what_style = "text_message_style")
                    "Anon3342" "Now I don't know what to do! Should I ignore this to make sure I'm around for my children 100%%?" (what_style = "text_message_style")
                    "Anon3342" "Looking for advice, signed: a horny Mom!" (what_style = "text_message_style")
                    "Did [the_person.title] write this? You scroll down to see the responses."
                    "Anon1449" "Don't feel guilty Horny Mom, you've spent your whole life caring for them. Now it's time to enjoy yourself!" (what_style = "text_message_style")
                    "MTeresa" "You aren't going to be young forever Horny Mom. Get out and meet a new man while you still can." (what_style = "text_message_style")
                    "Jocasta1" "There's at least one way to satisfy your needs without ignoring your family. Do you have a son?" (what_style = "text_message_style")
                    "Anon3342" "I do have a son Jocasta1. I also have a daughter." (what_style = "text_message_style")
                    "Jocasta1" "Well then let him take care of your sex drive! He's probably filled with hormones, and you'll be so much closer!" (what_style = "text_message_style")
                    "Anon3342 doesn't respond. You wonder if that really is [the_person.possessive_title], and what she thought about the idea."
                    $ mc.change_locked_clarity(5)
                    "Either way [the_person.title] was at least reading this. Maybe it gave her some ideas..."

                elif the_person.core_sluttiness < 50:
                    "[the_person.possessive_title] doesn't keep much on her computer, but she might not have cleared her browser history lately."
                    "You check and see that the last site visited was \"AphroditeNightly.com/The_Poolboy\". You bring up the site again to see what she was looking at."
                    "It's an online sex store, and [the_person.title] was looking at one of their product pages. The page features a picture of a small, discrete black vibrator."
                    "You scroll down and read through the description."
                    "\"Mr.Right not taking care of your needs? Busy mother on the go with no time for Me Time?\""
                    "\"Then The Poolboy is the toy for you. Small enough to bring with you wherever you go, powerful enough to blow your socks off.\""
                    "\"So invite the poolboy in, and let him pet your neglected kitty.\""
                    "You wonder if [the_person.title] actually ordered this, or if she was just window shopping."
                    $ mc.change_locked_clarity(10)
                    "You enjoy a moment thinking about the vibe pressed tight against [the_person.possessive_title]'s clit, then close down the browser."
                else:
                    "[the_person.possessive_title] doesn't keep much on her computer, but you spend a few minutes poking around anyways."
                    "All you find are work reports and the family budget. Next, you open up her browser."
                    "COMPUTER" "RESTORE BROWSING SESSION?" (what_style = "text_message_style")
                    "You hit \"Yes\", and her browser immediately restores a half dozen tabs, all from \"MILFSDaily.xxx\"."
                    $ mc.change_locked_clarity(10)
                    "Each one has a video loaded, and each video features an older busty woman getting fucked in a variety of interesting ways."
                    "You flick through the tabs, noting which videos are starting half way through."
                    if the_person.discover_opinion(the_person.get_random_opinion(only_positive = True, include_known = False, include_sexy = True, include_normal = False)):
                        "Seeing [the_person.title]'s prefernece in porn has given you some insight into her."
                    else:
                        "Even you're surprised at how hard core some of the videos are. You have a hard time imagining [the_person.possessive_title] sitting down and watching them."
                        $ mc.change_locked_clarity(10)
                        "... But you do imagine it though."
                    "You don't notice anything else interesting, so you close down the browser."
                #TODO: This could also use some sort of blowout top end event.

                "You log off of [the_person.possessive_title]'s computer and power it down."



            #TODO:Different levels based on sluttiness.

        "Look in her dresser.":
            "You slide open the drawers of [the_person.possessive_title]'s dresser."
            "You find her collection of socks, carefully folded shirts, and stash of makeup in the top drawer."
            $ mc.change_locked_clarity(5)
            "The second drawer has something much more interesting: Her underwear."
            "[the_person.title]'s panties are folded neatly along one edge, with styles ranging from practical to scandalous."
            "Even if she doesn't wear them she clearly likes having the choice."
            "The rest of the drawer is filled with [the_person.possessive_title]'s bras, stacked so that the large cups fit together neatly."
            "There are so many pieces of underwear in here, [the_person.title] probably wouldn't notice if one of them went missing."
            "It would certainly give you something more interesting to jerk off into than some tissue."
            menu:
                "Steal a bra.":
                    "You grab one of [the_person.possessive_title]'s softer, fancier bras from the back of her underwear drawer."
                    "They don't look like one she would be brave enough to wear, so she won't miss them. You tuck it behind your back and hurry to your room to stash it away."
                    $ mc.steal_underwear(the_person, bra.get_copy()) #TODO: Draw this from an actual outfit
                    $ mc.change_masturbation_novelty(5)
                    if the_person.event_triggers_dict.get("mom_stolen_panties",0) > 0:
                        $ the_person.event_triggers_dict["mom_stolen_bras"] += 1
                    else:
                        $ the_person.event_triggers_dict["mom_stolen_bras"] = 1

                    #TODO: Chance based on number of items stolen that she'll notice something's missing and ask you about it.
                    $ mc.change_location(bedroom)
                    $ mc.location.show_background()



                "Steal a pair of panties.":
                    "You grab one of [the_person.possessive_title]'s sexier set of panties from the back of her underwear drawer."
                    "They don't like a pair she would be brave enough to wear, so you doubt she'll miss them. You tuck them behind your back and hurry to your room to stash them away."
                    $ mc.steal_underwear(the_person, panties.get_copy()) #TODO: Draw this from an actual outfit
                    $ mc.change_masturbation_novelty(5)
                    if the_person.event_triggers_dict.get("mom_stolen_panties",0) > 0:
                        $ the_person.event_triggers_dict["mom_stolen_bras"] += 1
                    else:
                        $ the_person.event_triggers_dict["mom_stolen_bras"] = 1

                    #TODO: Chance based on number of items stolen that she'll notice something's missing and ask you about it.

                    $ mc.change_location(bedroom)
                    $ mc.location.show_background()

                "Leave everything alone.":
                    "You decide to leave all of [the_person.possessive_title]'s underwear where it is. It wouldn't be good if she noticed any of it missing."
                    "You make sure nothing has been moved around, then slide the drawer shut."

            # TODO: Decide if we wnat to have extra options here for peeking at wardrobe stuff.

    return
#TODO: Lily mirror of this event, or maybe you hack into her phone instead. Maybe learn about her Instapic account that way, instead of knowing about it for free?
