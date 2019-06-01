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

    def cousin_house_phase_two_requirement(day_trigger, the_person):
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
        "Cash.":
            #Always succeeds. Get some extra cash from her.
            mc.name "If you're taking cash from my sister I want half."
            $ the_person.change_obedience(1)
            if not the_person.outfit.tits_visible():
                "[the_person.title] reaches into her shirt and pulls out a small wad of bills."
            else:
                "[the_perosn.title] pulls out a small wad of bills."
            the_person.char "Fine."
            $ mc.business.funds += 100
            "She pulls out a $100 bill and hands it over to you. You take the money and slip it back into your pocket."
            $ the_person.event_triggers_dict["last_blackmailed"] = day
            $ the_person.change_love(-1)
            $ the_person.change_obedience(3)


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
                $ the_perosn.change
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

                    while not the_perosn.outfit.vagina_visisble():
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

            else:
                "[the_person.title] stares at you for a moment."
                the_person.char "Really? You want me to strip? For you?"
                the_person.char "You want me to get naked. To show you my nice... big... tits?"
                "She squeezes her breasts together and leans forward."
                the_person.char "Keep dreaming. Seriously, what do you want?"
                call cousin_blackmail_list(the_person) from _call_cousin_blackmail_list_3


        "Kiss me." if the_person.event_triggers_dict.get("blackmail_level", -1) >= 2:
            #Requires min sluttiness and more blackmail (Or high sluttiness). Either is a special kissing scene OR we add functionality to lock people into a sex position.
            $ the_person.event_triggers_dict["last_blackmailed"] = day
            pass #TODO once we have a level 2 blackmail event

        "Fuck me." if the_person.event_triggers_dict.get("blackmail_level", -1) >= 2:
            #Requires min sluttiness and more blackmail (Or high sluttiness). Generic fuck_person call with a large obedience boost so she'll do things you tell her to do.
            $ the_person.event_triggers_dict["last_blackmailed"] = day
            pass #TODO once we have a level 2 blackmail event.

        "Nothing.":
            mc.name "Nothing right now, but I'll come up with something."
            the_person.char "Ugh."

    return
