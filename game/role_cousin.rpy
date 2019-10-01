#Cousin Role Action Requirements
init -2 python:
    def cousin_intro_phase_one_requirement(day_trigger):
        if day >= day_trigger and time_of_day == 4:
            return True
        return False

    def cousin_house_phase_one_requirement(day_trigger):
        if day >= day_trigger:
            return True
        return False

    def cousin_house_phase_two_requirement(the_person):
        if the_person in hall.people: #Note: this breaks if we eventually let you move people around. By bringing her to your place you could leave and come back early.
            return True
        return False

    def cousin_house_phase_three_requirement(day_trigger):
        if day>= day_trigger:
            return True
        return False

    def cousin_blackmail_intro_requirement(the_person):
        if the_person in lily_bedroom.people and time_of_day == 2 and __builtin__.len(lily_bedroom.people) == 1: #Only triggers when she's in there alone (and after the event has been added to the trigger list)
            return True
        return False

    def cousin_blackmail_requirement(the_person):
        if the_person.event_triggers_dict.get("blackmail_level", -1) < 1:
            return False
        elif day < the_person.event_triggers_dict.get("last_blackmailed",-5) + 5:
            return "Blackmailed too recently."
        elif __builtin__.len(mc.location.people) > 1:
            return "Must be in private."
        else:
            return True

    def stripclub_show_requirement():
        if time_of_day in [0,1,2]:
            return "Too early for the performance to start."
        else:
            return True

    def blackmail_hint_requirement(the_person, min_day):
        if day < min_day:
            return False
        elif time_of_day != 4:
            return False
        elif the_person.sluttiness < 25:
            return False
        elif the_person.event_triggers_dict.get("blackmail_level",-1) != 1:
            return False
        else:
            return True

    def cousin_room_search_requirement(the_person):
        if the_person.event_triggers_dict.get("blackmail_level",-1) != 1:
            return False
        elif the_person.event_triggers_dict.get("found_stripping_clue", False):
            return False
        elif time_of_day == 4:
            return "Too late to search thoroughly."
        elif the_person in mc.location.people:
            return the_person.title + " is in the room."
        else:
            return True

    def blackmail_2_confront_requirement(the_person):
        if the_person.event_triggers_dict.get("blackmail_level", -1) != 1:
            return False
        else:
            return True

###COUSIN ACTION LABELS###
label cousin_intro_phase_one_label():
    #Your cousin bursts into your room at the end of the day frustrated with Lily and how little personal space she has.
    $ cousin.draw_person(emotion = "angry")
    "Without warning your bedroom door is opened and [cousin.possessive_title] walks in. She closes the door behind her and looks awkwardly at you."
    mc.name "Hey..."
    cousin.char "Hey. I'm just going to be here for a few minutes. You don't need to say anything."
    mc.name "Is everything okay?"
    cousin.char "Your sister just keeps talking. She won't shut up. I just need some silence."
    menu:
        "Offer to talk to [lily.title].":
            pass

        "Let [cousin.title] stay as long as she wants.":
            pass

        "Tell [cousin.title] to leave you alone.":
            pass

    mc.name "Right. How about..."
    "[cousin.possessive_title] glares at you."
    cousin.char "I want silence, [cousin.mc_title]. It means not talking."
    $ cousin.draw_person()
    "She sits down and leans back against your door, staring at her phone."
    menu:
        "Say nothing.":
            "You decide to just stay quiet and go back to what you were doing. [cousin.title] reads on her phone for half an hour before standing back up."
            $ cousin.change_happiness(5)
            $ cousin.change_love(1)
            cousin.char "Thanks."
            "With that she opens your door and leaves."

        "Kick her out.":
            mc.name "Listen [cousin.title], this is my room and I want some privacy. Get out."
            "[cousin.possessive_title] rolls her eyes and sighs dramatically."
            cousin.char "If you're just going to keep talking at me, gladly."
            $ cousin.change_love(-2)
            "She stands back up and leaves your room. She slams your door on the way out."

    $ renpy.scene("Active")
    return

label cousin_house_phase_one_label(the_person):
    #Changes her schedule to be at your house
    $ the_person.schedule[2] = hall
    $ cousin_house_phase_two_action = Action("Cousin visits house", cousin_house_phase_two_requirement, "cousin_house_phase_two_label")
    $ cousin.on_room_enter_event_list.append(cousin_house_phase_two_action) #When you see her next in your house this event triggers and she explains why she's there.
    return

label cousin_house_phase_two_label(the_person):
    "When you come in the front door you see [the_person.title] sitting on your couch watching TV."
    $ the_person.draw_person(position = "sitting")
    mc.name "Uh... Hey."
    the_person.char "Hey."
    "She glances up from the TV for the breifest moment then goes back to ignoring you."
    mc.name "What's up? Why are you over here?"
    the_person.char "Your mom said I could come over whenever I wanted. My mom won't stop bothering me and our crappy apartment is tiny."
    "[the_person.possessive_title] shrugs and turns her full attention to her TV show."
    $ cousin_at_house_phase_three_action = Action("Cousin changes schedule", cousin_house_phase_three_requirement, "cousin_house_phase_three_label", args = cousin, requirement_args = day+renpy.random.randint(2,5))
    $ mc.business.mandatory_crises_list.append(cousin_at_house_phase_three_action) #In a couple of days change her schedule so she starts stealing from Lily.
    return

label cousin_house_phase_three_label(the_person):
    $ the_person.schedule[2] = lily_bedroom #Set her to be in Lily's room AND for an event to trigger when you walk in on her.
    $ cousin_blackmail_intro_action = Action("Cousin caught stealing", cousin_blackmail_intro_requirement, "cousin_blackmail_intro_label")
    $ the_person.on_room_enter_event_list.append(cousin_blackmail_intro_action)
    return

label cousin_blackmail_intro_label(the_person):
    #You find your cousin in Lily's room, looking for cash. Event triggers as soon as you come in. Begins blackmailing storyline.
    $ the_person.draw_person(position = "walking_away")
    "[the_person.possessive_title] is standing in front of [lily.possessive_title]'s bedstand. She turns suddenly when you open the door."
    $ the_person.draw_person()
    the_person.char "Uh... Hey."
    mc.name "What are you doing in here?"
    "[the_person.title] crosses her arms and looks away from you."
    the_person.char "Nothing. I was just... looking around."
    mc.name "Uh huh. So I can tell [lily.title] about this and you won't mind?"
    "She glares at you."
    the_person.char "Sure. It's not even a big deal."
    "You shrug and get your phone out. You pull up [lily.possessive_title]'s contact information."
    the_person.char "Wait! It's really not a big deal [the_person.mc_title]. You don't need to tell her."
    mc.name "What were you doing in here [the_person.title]?"
    "[the_person.possessive_title] groans before breaking."
    $ the_person.change_happiness(-10)
    the_person.char "Fine. I was... I was looking for some money. My dad cut me off and my mom doesn't have any."
    the_person.char "[lily.possessive_title] is so scatterbrained she would never notice anything was missing."
    "[the_person.title] takes a few panicked steps towards you."
    the_person.char "You can't tell my mom. She would never let me leave the house."
    #TODO: add a "blackmail level" event variable that is increased by this.
    menu:
        "Blackmail her.":
            mc.name "Fine, I'll stay quiet. If you do something for me."
            $ the_person.change_happiness(5)
            $ the_person.change_obedience(5)
            $ the_person.change_love(-1)
            "[the_person.title] seems relieved. She nods."
            the_person.char "Fine. What do you want?"
            call cousin_blackmail_list(the_person) from _call_cousin_blackmail_list


        "Promise to stay quiet.":
            mc.name "I'll keep this between you and me."
            "[the_person.title] gives you a suspicious look."
            the_person.char "Just like that?"
            "You shrug."
            mc.name "You're right, [lily.title] wouldn't notice anything missing and you need it more."
            $ the_person.change_happiness(8)
            $ the_person.change_love(2)
            the_person.char "Okay. I better not find out you told someone."
            mc.name "Your secret's safe with me."

    $ the_person.event_triggers_dict["blackmail_level"] = 1

    $ blackmail_2_event = Action("Blackmail hint", blackmail_hint_requirement, "aunt_cousin_hint_label", args = [aunt, the_person], requirement_args = [the_person, day + renpy.random.randint(2,4)])
    $ mc.business.mandatory_crises_list.append(blackmail_2_event)
    $ renpy.scene("Active")
    return

label cousin_blackmail_label(the_person):
    #The dialogue intro for the blackmail list when you talk to her again.
    #TODO: Have this refer to the different blackmail stuff once it's been written
    #TODO: Write a variant for when you promised to "keep quiet' then come back to blackmail her.
    mc.name "So, I was thinking about going to your mom and having a talk. About you."
    "[the_person.title] lets out a resigned sigh."
    the_person.char "Fine. What do you want?"
    call cousin_blackmail_list(the_person) from _call_cousin_blackmail_list_1

    return

label cousin_blackmail_list(the_person):
    menu:
        "Demand to know where she has been going at night." if the_person.event_triggers_dict.get("stripping", False) and the_person.event_triggers_dict.get("blackmail_level",-1) == 1:
            call cousin_blackmail_ask_label(the_person) from _call_cousin_blackmail_ask_label
            if not _return: #If she didn't tell you anything she tells you to pick something else.
                call cousin_blackmail_list(the_person) from _call_cousin_blackmail_list_4
            else:
                $ the_person.event_triggers_dict["last_blackmailed"] = day
                $ the_person.change_love(-1)

        "Cash.":
            #Always succeeds. Get some extra cash from her.
            if the_person.event_triggers_dict.get("blackmail_level",-1) >= 2:
                mc.name "I assume your little stripping gig has still been paying well. I want my cut."
                the_person.char "Fine."
                if not the_person.outfit.tits_visible():
                    "[the_person.title] reaches into her shirt and pulls out a roll of cash."
                else:
                    "[the_person.title] pulls out a roll of cash."
                    "She leafs out a bunch of $100 bills and hand them over to you. You take the money and slip it into your wallet."

            else:
                mc.name "If you're taking cash from my sister I want half."
                $ the_person.change_obedience(1)
                if not the_person.outfit.tits_visible():
                    "[the_person.title] reaches into her shirt and pulls out a small wad of bills."
                else:
                    "[the_person.title] pulls out a small wad of bills."
                the_person.char "Fine."
                $ mc.business.funds += 100
                "She pulls out a $100 bill and hands it over to you. You take the money and slip it into your wallet."
            $ the_person.change_love(-1)
            $ the_person.change_obedience(3)
            $ the_person.event_triggers_dict["last_blackmailed"] = day



        "Test this serum.":
            #Always succeeds. She takes a dose of serum for you.
            mc.name "I've got stuff from work that needs testing. If you test it I'll stay quiet."
            the_person.char "Fine."
            "She rolls her eyes and waits for you give her a vial of serum."
            call give_serum(the_person) from _call_give_serum_12
            if _return:
                "You hand over the vial. [the_person.possessive_title] drinks it down without any comment or complaint."
                the_person.char "There. Now just keep up your end of the bargain and keep quiet."
                $ the_person.event_triggers_dict["last_blackmailed"] = day
                $ the_person.change_love(-1)
                $ the_person.change_obedience(3)

            else:
                mc.name "Actually, I don't have anything with me right now."
                "[the_person.title] rolls her eyes."
                the_person.char "Whatever, what else do I need to do to keep you quiet?"
                call cousin_blackmail_list(the_person) from _call_cousin_blackmail_list_2

        "Strip for me.":
            #Requires min sluttiness. She'll strip down her outfit until a certain point for you.
            mc.name "I want to see you strip for me."
            if the_person.sluttiness >= 15:
                "[the_person.possessive_title] doesn't say anything for a second."
                the_person.char "Fine. Sit down and pay attention. I'm only doing this once."
                if the_person.sluttiness <= 20:
                    #She only wants to show you her underwear.
                    if the_person.outfit.wearing_bra(): #If she's wearing a bra strip down to it.
                        while the_person.outfit.bra_covered():
                            $ the_item = the_person.outfit.remove_random_upper(top_layer_first = True, do_not_remove = True)
                            $ the_person.draw_animated_removal(the_item) #Strip down to her underwear.
                            "[the_person.possessive_title] takes off her [the_item.name]."
                    else: #She's not wearing a bra and doesn't want you to see her tits.
                        "[the_person.title] seems nervous and plays with her shirt." #TODO: Check that she is wearing a shirt
                        mc.name "What's wrong?"
                        the_person.char "I don't have a bra on... I can't take this off."
                        mc.name "Come on, you know the deal."
                        the_person.char "Nope. Not doing it. Be happy with what you're getting."

                    if the_person.outfit.wearing_panties():
                        while the_person.outfit.panties_covered():
                            $ the_item = the_person.outfit.remove_random_lower(top_layer_first = True, do_not_remove = True)
                            $ the_person.draw_animated_removal(the_item)
                            "[the_person.possessive_title] takes off her [the_item.name]."
                    else: #TODO: make sure she's actually wearing a dress or skirt or something
                        the_person.char "So, I'm not wearing any panties right now. That means I can't take this off."
                        mc.name "Come on, that's not what the deal is."
                        the_person.char "Sad you don't get to see my tight, wet pussy [the_person.mc_title]?"
                        the_person.char "Deal with it, go cry to mommy if it matters that much to you."

                    if the_person.outfit.wearing_panties() and the_person.outfit.wearing_bra():
                        "Once [the_person.possessive_title] has stripped down to her underwear she turns around to let you look at her ass."
                    else:
                        "Once [the_person.possessive_title] has stripped down as far as she's willing she turns around to let you look at her ass."
                    $ the_person.draw_person(position = "back_peek")
                    the_person.char "Finished yet? I bet you're about to cream your fucking pants looking at this."
                    "You take a second to enjoy the view."
                    mc.name "Alright, that'll do."
                    the_person.char "Finally..."
                    "[the_person.possessive_title] gets dressed again."
                    $ the_person.outfit = the_person.planned_outfit.get_copy()
                    $ the_person.draw_person()
                    $ the_person.change_slut_temp(5)

                elif the_person.sluttiness <= 40:
                    #She'll show you her tits.
                    while not the_person.outfit.tits_visible():
                        $ the_item = the_person.outfit.remove_random_upper(top_layer_first = True, do_not_remove = True)
                        $ the_person.draw_animated_removal(the_item) #Strip down to her underwear.
                        if the_person.outfit.tits_visible():
                            "[the_person.possessive_title] takes off her [the_item.name] slowly, teasing you as she frees her tits."
                        else:
                            "[the_person.possessive_title] takes off her [the_item.name]."

                    if the_person.outfit.wearing_panties():
                        while the_person.outfit.panties_covered():
                            $ the_item = the_person.outfit.remove_random_lower(top_layer_first = True, do_not_remove = True)
                            $ the_person.draw_animated_removal(the_item)
                            "[the_person.possessive_title] takes off her [the_item.name]."
                    else: #TODO: make sure she's actually wearing a dress or skirt or something
                        the_person.char "So, I'm not wearing any panties right now. That means I can't take this off."
                        mc.name "Come on, that's not what the deal is."
                        the_person.char "Sad you don't get to see my tight, wet pussy [the_person.mc_title]?"
                        the_person.char "Deal with it, go cry to mommy if it matters that much to you."

                    "Once [the_person.possessive_title] has stripped down she turns around to let you get a look at her ass."
                    $ the_person.draw_person(position  = "back_peek")
                    the_person.char "Look all you want... I bet you're creaming your pants thinking about touching me."
                    "She wiggles her butt in your direction. Her tits swing back and forth with the same movement."
                    the_person.char "Well keep dreaming. I'm not that fucking desparate."
                    "Once you've gotten your fill [the_person.title] gets dressed again."
                    $ the_person.outfit = the_person.planned_outfit.get_copy()
                    $ the_person.draw_person()
                    $ the_person.change_slut_temp(5)

                else:
                    #She'll get completely naked.
                    while not the_person.outfit.tits_visible():
                        $ the_item = the_person.outfit.remove_random_upper(top_layer_first = True, do_not_remove = True)
                        $ the_person.draw_animated_removal(the_item) #Strip down to her underwear.
                        if the_person.outfit.tits_visible():
                            "[the_person.possessive_title] takes off her [the_item.name] slowly, teasing you as she frees her tits."
                        else:
                            "[the_person.possessive_title] takes off her [the_item.name]."

                    while not the_person.outfit.vagina_visible():
                        $ the_item = the_person.outfit.remove_random_lower(top_layer_first = True, do_not_remove = True)
                        $ the_person.draw_animated_removal(the_item)
                        if the_person.outfit.vagina_visible():
                            "[the_person.possessive_title] peels off her [the_item.name], slowly revealing her cute little pussy."
                        else:
                            "[the_person.possessive_title] takes off her [the_item.name]."

                    the_person.char "There, are you satisfied?"
                    $ the_person.draw_person(position = "back_peek")
                    "She spins on the spot, letting you get a look at her ass."
                    #TODO: keep a record of how many times you've (fucked, been sucked by, etc.) the person so she can comment on that.
                    mc.name "I'm not sure this is enough [the_person.title]. I think you need to convince me."
                    "[the_person.possessive_title] sighs dramatically."
                    $ the_person.draw_person()
                    the_person.char "Please [the_person.mc_title], please don't tell my mom what a bad girl I've been."
                    the_person.char "I'm here, with my big fucking tits and my tight fucking cunt out just for you. Please don't say anything."
                    "She gives you an overly dramatic pout."
                    mc.name "Fine, that'll do."
                    the_person.char "Fucking finally..."
                    $ the_person.outfit = the_person.planned_outfit.get_copy()
                    $ the_person.draw_person()
                    $ the_person.change_slut_temp(5)

                $ the_person.event_triggers_dict["last_blackmailed"] = day
                $ the_person.change_love(-1)
                $ the_person.change_obedience(3)
                $ the_person.review_outfit()

            else:
                "[the_person.title] stares at you for a moment."
                the_person.char "Really? You want me to strip? For you?"
                the_person.char "You want me to get naked. To show you my nice... big... tits?"
                "She squeezes her breasts together and leans forward."
                the_person.char "Keep dreaming. Seriously, what do you want?"
                call cousin_blackmail_list(the_person) from _call_cousin_blackmail_list_3


        "Kiss me." if the_person.event_triggers_dict.get("blackmail_level", -1) >= 2:
            #Requires min sluttiness and more blackmail (Or high sluttiness). Either is a special kissing scene OR we add functionality to lock people into a sex position.
            mc.name "I want you to kiss me."
            "She sneers."
            the_person.char "Ugh. Disgusting."
            "She leans forward and gives you the brief kiss on the cheek."
            the_person.char "There, are we done now?"
            mc.name "You know we aren't. Come here."
            $ the_person.add_situational_obedience("blackmail", 30, "This will keep him quiet.")

            call fuck_person(the_person, start_position = kissing, start_object = mc.location.objects_with_trait("Stand"), position_locked = True) from _call_fuck_person_24
            if the_person.arousal >= 100:
                "[the_person.title] is left flush and panting when you're finished making out."
                mc.name "Did you enjoy yourself? You're pretty good at that."
                $ the_person.change_slut_temp(2)
                $ the_person.change_obedience(4)
                the_person.char "Shut up, I'm just glad that's over..."
            else:
                the_person.char "Finally. I'm glad that's over."
                $ the_person.change_obedience(3)

            $ the_person.reset_arousal()
            $ the_person.clear_situational_obedience("blackmail")
            $ the_person.review_outfit()
            $ the_person.event_triggers_dict["last_blackmailed"] = day

        "Fuck me." if the_person.event_triggers_dict.get("blackmail_level", -1) >= 2:
            #Requires min sluttiness and more blackmail (Or high sluttiness). Generic fuck_person call with a large obedience boost so she'll do things you tell her to do.
            mc.name "I want your body, all of it."
            if the_person.sluttiness >= 30:
                the_person.char "Ugh, really?"
                "She sighs and rolls her eyes dramatically."
                the_person.char "Fine. Just make it quick, and I swear to god you better never tell anyone about this."
                $ the_person.add_situational_obedience("blackmail", 30, "This will keep him quiet.")

                call fuck_person(the_person) from _call_fuck_person_25
                if the_person.arousal >= 100:
                    "[the_person.possessive_title] closes her eyes tries to catch her breath."
                    the_person.char "Fuck... God fucking damn it..."
                    mc.name "Something wrong?"
                    the_person.char "God damn it, you shouldn't be able to do that to me. Fuck."

                else:
                    the_person.char "Are we done here? I feel like I need a shower after that."
                    mc.name "Cheer up, you'll be enjoying it soon enough."
                    the_person.char "God I hope not. Even if I was you'll never get the satisfaction of knowing about it."


                $ the_person.reset_arousal()
                $ the_person.clear_situational_obedience("blackmail")
                $ the_person.review_outfit()
                $ the_person.event_triggers_dict["last_blackmailed"] = day

            else:
                the_person.char "Really? You want to touch me?"
                "She bites her lip and runs her hands over her hips."
                the_person.char "Grab my tits? Fuck my tight pussy? Make me cum with your with your huge cock?"
                the_person.char "Ha! Dream on you fucking perv. I'm a stripper not a whore."
                call cousin_blackmail_list(the_person) from _call_cousin_blackmail_list_5

        "Nothing.":
            mc.name "Nothing right now, but I'll come up with something."
            the_person.char "Ugh."

    return


label aunt_cousin_hint_label(the_aunt, the_cousin):
    #Your aunt calls at night to ask if you know where Gabrielle is. Hints that she's up to something late at night.
    "You get a call on your phone. It's [the_aunt.possessive_title]."
    mc.name "Hey [the_aunt.title], is everything alright?"
    the_aunt.char "Hi [the_aunt.mc_title], everything is okay. Do you have a moment?"
    mc.name "Sure, what's up?"
    the_aunt.char "It's about [the_cousin.title]. For the last few nights she's been staying out late and she won't tell me where she is."
    the_aunt.char "I'm worried that she's getting up to trouble. Do you have any clue what she's doing?"
    menu:
        "Offer to find out.":
            mc.name "No, but I can try and find out if you'd like."
            $ the_aunt.change_happiness(3)
            $ the_aunt.change_love(1)
            the_aunt.char "That would be great, thank you. I'm sure I'm just overreacting, but it would help me sleep better at night knowing she's okay."
            mc.name "I'll let you know if I learn anything."

        "No clue.":
            mc.name "Nope, no idea. Sorry."
            the_aunt.char "That's okay, she's always been very private so I'm not surprised."
            the_aunt.char "Well if you hear anything just let me know, okay? I'm sure I'm overreacting, but it would help me sleep if I knew she was okay."
            mc.name "Okay [the_aunt.title], if I hear anything I'll let you know."


    the_aunt.title "Thank you. I won't keep you any longer then, I'm sure you're busy!"

    $ stripclub_strippers.append(the_cousin)
    $ the_cousin.set_schedule([4], strip_club)

    $ the_cousin.event_triggers_dict["stripping"] = True #Used to flag the blackmail event.
    $ cousin_room_search_action = Action("Search her room. {image=gui/heart/Time_Advance.png}", cousin_room_search_requirement, "cousin_search_room_label",requirement_args = [the_cousin], args = [the_cousin, the_aunt])
    $ cousin_bedroom.actions.append(cousin_room_search_action) #Lets you search her room for a clue about where to go to find her.

    return

label cousin_blackmail_ask_label(the_person):
    #This is an option made available when blackmailing her
    #With a high enough love or obedience she tells you what she's been doing, otherwise she just tells you to fuck off.
    $ talked_before = the_person.event_triggers_dict.get("blackmail_2_asked", False)
    $ the_person.event_triggers_dict["blackmail_2_asked"] = True # For future events we have slightly different dialogue.

    $ told = False
    if not talked_before:
        mc.name "Your mom told me you've been staying out late but you won't tell her why. I'm want to know what you're up to."
    else:
        mc.name "So [the_person.title], are you ready to tell me what you've been staying out late for?"

    if the_person.love >= 60:
        if not talked_before:
            the_person.char "You heard about that? Ugh, of course she's been asking everyone."
        else:
            the_person.char "Are you still thinking about that? Ugh..."
        mc.name "You know you can trust me. What have you been doing?"
        "She hesitates, torn between her love of you and her desire for privacy. She finally breaks down."
        the_person.char "I have a new job."
        the_person.char "At a strip club."
        mc.name "What?"
        the_person.char "I got a job at a strip club. I didn't tell my mom because she would flip out."
        the_person.char "I didn't tell you because you're my cousin, and I didn't want you to think I was a freak."
        the_person.char "Can you please just not tell her? I make a lot of money, I could give you a cut to stay quiet."
        mc.name "I would really hate to let your mom down though..."
        "She sighs and nods her head."
        the_person.char "Yeah, yeah, I know what else you want. I'll let you touch me sometimes, if you promise to keep your mouth shut."
        mc.name "I think that might be enough."
        $ the_person.event_triggers_dict["blackmail_level"] = 2
        $ told = True

    elif the_person.obedience >= 130:
        "She rolls her eyes."
        if not talked_before:
            the_person.char "Ugh, of course she's been asking everyone. I'm not telling her for a reason."
        else:
            the_person.char "Ugh, are you still thinking about that. I haven't told my mom for a reason, you know."
        mc.name "Well I want to know. What have you been doing?"
        "She hesitates, fighting against her own obedience to you, then breaks down."
        the_person.char "I have a new job."
        the_person.char "At a strip club."
        mc.name "What?"
        the_person.char "I got a job at a strip club, and I don't want my mom to know, okay?"
        the_person.char "She would freak out, and I make a lot of money doing it. Just don't tell her."
        mc.name "Why not? What do I get out of it?"
        "She sighs dramatically."
        the_person.char "Yeah, yeah, I see where this is going. I'll give you a cut."
        mc.name "And?"
        the_person.char "And... I'll let you touch me sometimes, if you promise to stay quiet."
        mc.name "I think that might be enough."
        $ the_person.event_triggers_dict["blackmail_level"] = 2
        $ told = True

    else:
        "She rolls her eyes."
        if not talked_before:
            the_person.char "And you think I'd tell you instead? Dream on."
            mc.name "But you {i}are{/i} doing something?"
            the_person.char "Wouldn't you like to know. Come one, what do you really want?"
        else:
            the_person.char "Why would I tell you anything? If you're so curious you should figure it out yourself."
            the_person.char "Come on, tell me what you really want so I can get this over with."

        "[the_person.possessive_title] doesn't seem like she's about to crack."
        "Maybe if she liked you more or was more obedient she would tell you, or maybe there's another way to figure out what she's been doing."

    return told

label cousin_search_room_label(the_cousin, the_aunt):
    # You start to search her room to find anything you can. If her mom is home she'll ask you to stop, but with enough obedience you can tell her to let you do it.
    "You start to search through [the_cousin.title]'s room for any hints you can find about where she's been going at night."
    if the_aunt in aunt_apartment.people or the_aunt in aunt_bedroom.people:
        #Your aunt is around and asks you to stop.
        "You start with the most obvious places, digging through the papers on her desk and checking her closet."
        "While you're searching the bedroom door is opened."
        $ the_aunt.draw_person()
        if the_aunt.love < 10:
            the_aunt.char "[the_aunt.mc_title], what the hell are you doing?"
            mc.name "Uh... I'm looking for information about your daughter."
            $ the_person.draw_person(emotion = "angry")
            $ the_person.change_love(-3)
            the_aunt.char "And you think you can just come in here and dig through her stuff? Get out, I'll be telling your mother about this!"
            "She glares at you and ushers you out of the apartment and out of the building."
            $ mom.change_happiness(-5)
            $ mom.change_love(-1)
            $ mc.change_location(downtown)
            "You'll need [the_aunt.possessive_title] out of the apartment if you want to search [the_cousin.title]'s room undisturbed."
            return
        else:
            the_aunt.char "[the_aunt.mc_title], are you looking for something?"
            mc.name "I'm looking for clues about what your daughter has been up to."
            the_aunt.char "Oh. I'm not sure she would appreciate you searching through all of her things though."
            mc.name "I doubt she would, but we both want information, right?"
            if the_aunt.obedience < 130:
                the_aunt.char "I do, but not like this. You're going to have to stop."
                $ the_aunt.change_love(-1)
                "You're forced to abandon your search. [the_aunt.possessive_title] escorts you to the living room."
                $ mc.change_location(aunt_apartment)
                "If she was more obedient she might let you continue the search, or you could wait until she isn't in the apartment at all."
                return

            else:
                "She sighs and nods."
                the_aunt.char "You're right. If [the_cousin.title] asks I don't know anything about this, okay?"
                mc.name "I won't tell a soul."
                $ renpy.scene("Active")
                "[the_aunt.possessive_title] leaves you alone in her daughter's room to continue your search."



    else:
        "With nobody else around you're able to thoroughly search the room. You start with the most obvious places, digging through her desk and checking her closet."

    "Your initial sweep doesn't turn up anything interesting, so you start looking in more hidden places."
    "Under her mattress you discover a piece of paper hidden as deep as possible. You pull it out and read it."
    $ club_name = strip_club.name
    $ strip_club.visible = True
    "It's a pay stub from [club_name], covering the last two weeks for an impressive amount of pay."
    "It's possible that [the_cousin.title] is working there as a waitress, but you have your doubts."
    "If you can catch [the_cousin.title] while she's working there she won't be able to make any excuses and you'll have her in the palm of your hand."

    $ the_cousin.event_triggers_dict["found_stripping_clue"] = True
    call advance_time from _call_advance_time_25
    return

label cousin_blackmail_level_2_confront_label(the_person):
    # A talk action added once you have seen her stripping that results in higher blackmailing levels.
    $ club_name = strip_club.name
    mc.name "So I was at [club_name] and I saw something really interesting."
    "Her eyes go wide and lock with yours."
    the_person.char "Uh... What were you doing there? That's a weird place for you to be."
    mc.name "I was enjoying the talent. Imagine my suprise when I see you walk out."
    $ the_person.change_happiness(-5)
    the_person.char "... Fuck."
    mc.name "So this was what you were hiding, huh? I'm sure your mom is going to be thrilled when she hears about this."
    the_person.char "I swear to god I'll kill you if you do. You can't say a word about this to her."
    mc.name "Why not? What do I get out of it?"
    "She holds her forehead for a moment and sighs."
    $ the_person.change_love(-5)
    the_person.char "Yeah yeah, I see where this is going. Listen, I make really good money doing this."
    the_person.char "I'll give you a cut if you stay quiet."
    mc.name "And?"
    the_person.char "And? What \"and\"? could you want?"
    mc.name "That whole strip show is just a massive tease. I'm feeling a little unsatisfied."
    the_person.char "God, you fucking perv. Fine, if you can keep quiet I might also let you... touch me. Deal?"
    mc.name "I think that might be enough."
    $ the_person.event_triggers_dict["blackmail_level"] = 2
    return

label stripclub_dance():
    #Watch a dance at the strip club.
    #-> You sit down and watch. A girl (generate a list of girls at the club) comes out wearing one of several special outfits.
    #-> She poses a few times. Each time you can tip her or just watch.
    #-> If you tip enough she strips off her bra and/or panties.
    #-> When she ends her dance, if you've paid enough she may ask if you want to come back for a private lap dance.
    #-> Lap dance scene may just turn into sex.
    $ pose_list = ["walking_away","back_peek","standing_doggy","stand2","stand3","stand4","stand5"] #A list to let us randomly get some poses so each dance is a little different.



    "You take a seat near to the edge of the stage and wait for the next performer."

    $ the_person = get_random_from_list(list(set(stripclub_strippers) & set(mc.location.people))) #Create a list of strippers who are present, then pick a random person.
    if the_person is None:
        $ the_person = get_random_from_list(stripclub_strippers) #If there is nobody around make sure to grab them and bring them here so we don't crash.
    $ the_person.outfit = stripclub_wardrobe.pick_random_outfit()
    $ performer_title = the_person.title
    $ the_person.draw_person()
    "A new song starts playing over the strip club speakers and a girl steps out onto the stage."
    if performer_title is not None:
        if cousin_role in the_person.special_role:
            if the_person.event_triggers_dict.get("blackmail_level",-1) < 2 and not the_person.event_triggers_dict.get("seen_cousin_stripping",False):
                python:
                    blackmail_2_confront_action = Action("Confront her about her stripping", blackmail_2_confront_requirement, "cousin_blackmail_level_2_confront_label",
                        menu_tooltip = "Tell her that you know about her job as a stripper and use it as further leverage.")
                    cousin_role.actions.append(blackmail_2_confront_action)
                    the_person.event_triggers_dict["seen_cousin_stripping"] = True

                "It takes you a moment to recognise your cousin, [the_person.title], as she struts out onto the stage."
                if not the_person.event_triggers_dict.get("found_stripping_clue", False):
                    "[the_person.possessive_title]'s late nights and secret keeping suddenly make a lot more sense."

                "With the glare of the stage lights it's likely she won't be able to see who you are, but you can talk to her later and use this as leverage to blackmail her."


            else:
                "You recognise your cousin almost as soon as she steps out onto the stage."

        elif sister_role in the_person.special_role:
            "You recognise your little sister almost as soon as she steps out onto the stage."

        elif aunt_role in the_person.special_role:
            "You recognise your aunt as she steps into the stage spotlights."

        elif mother_role in the_person.special_role:
            "You recognise your own mother up on the stage as soon as she comes into the light."

        elif employee_role in the_person.special_role:
            "You recognise [performer_title] as one of your employees."

        else:
            "You recognise her as [performer_title]."

        $ performer_title = the_person.possessive_title #Change to their possessive title, because that sounds better in the following dialogue

    else:
        $ performer_title = the_person.create_formatted_title("The stripper")
    "She poses for a moment and the crowd cheers around you. Then she starts to strut down the walkway."
    "She stops at the end of the stage peninsula, surrounded on three sides by eagerly watching men."
    "[performer_title] starts to dance to the music, swinging her hips and turning slowly to show herself off to all members of the crowd."
    call stripshow_strip(the_person) from _call_stripshow_strip
    $ the_person.draw_person(position = "back_peek")
    "She spins and poses for her audience, who respond with whoops and cheers."
    call stripshow_strip(the_person) from _call_stripshow_strip_1
    if the_person.has_large_tits():
        if the_person.outfit.tits_available():
            "As the music builds [performer_title]'s dance becomes more energetic. Her big tits bounce and jiggle in rhythm with her movements."
        else:
            "As the music builds [performer_title]'s dance becomes more energetic. Her big tits bounce and jiggle, looking almost desperate to escape."
    else:
        "As the music builds [performer_title]'s dance becomes more energetic. She runs her own hands over her tight body, accentuating her curves."
    call stripshow_strip(the_person) from _call_stripshow_strip_2
    $ the_person.draw_person(position = get_random_from_list(pose_list))
    "Her music hits its crescendo and her danacing does the same. [performer_title] holds onto the pole in the middle of the stage and spins herself around it."
    call stripshow_strip(the_person) from _call_stripshow_strip_3
    $ the_person.draw_person(position = "doggy")
    if the_person.outfit.vagina_visible():
        "As the song comes to an end the dancer lowers herself to all fours, showing off her ass and pussy to the crowd."
    else:
        "As the song comes to an end the dancer lowers herself to all fours. She spreads her legs and works her hips, jiggling her ass for the crowds amusement."

    $ the_person.draw_person()
    "She stands up and waves to her audience."
    the_person.char "Thank you everyone, you've been wonderful!"
    $ the_person.draw_person(position = "walking_away")
    "[performer_title] blows a kiss and struts off stage."

    $ renpy.scene("Active")
    return

label stripshow_strip(the_person):
    menu:
        "Throw some cash. -$20" if mc.business.funds >= 20:
            $ mc.business.funds += -20
            "You reach into your wallet and pull out a $20 bill. You wait until the dancer is looking in your direction, then throw it onto the stage."

            $ random_item = the_person.outfit.remove_random_any(top_layer_first = True, exclude_lower = True,  exclude_feet = True, do_not_remove = True) #Try and get a bra/top first if you can
            if random_item is None:
                $ random_item = the_person.outfit.remove_random_any(top_layer_first = True, exclude_lower = False,  exclude_feet = True, do_not_remove = True) #When that fails get her bottom/panties.

            if random_item:
                $ the_person.draw_animated_removal(random_item)
                "She smiles at you and starts to peel off her [random_item.name]."
            else:
                "She smiles wiggles her hips for you."

        "Throw some cash. -$20 (disabled)" if mc.business.funds < 20:
            pass

        "Just enjoy the show.":
            "You lean back in your seat and enjoy the dance."
            if renpy.random.randint(0,100) < 30:
                #Someone else throws cash onto the stage.
                "On the other side of the stage someone waves a bill at the dancer."
                $ random_item = the_person.outfit.remove_random_any(top_layer_first = True, exclude_lower = True,  exclude_feet = True, do_not_remove = True) #Try and get a bra/top first if you can
                if random_item is None:
                    $ random_item = the_person.outfit.remove_random_any(top_layer_first = True, exclude_lower = False,  exclude_feet = True, do_not_remove = True) #When that fails get her bottom/panties.

                if random_item:
                    "She takes the money and starts to slowly strip off her [random_item.name]."
                    $ the_person.draw_animated_removal(random_item)
                else:
                    "She takes the money and holds onto it while she continues to move her body to the music."
    return
