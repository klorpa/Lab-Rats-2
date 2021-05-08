init -1 python:
    def sleeping_walk_in_requirement(the_person):
        if not (the_person.has_role(sister_role) or the_person.has_role(mother_role)): #If it was LTE based we could avoid this. Basically any global reference should be by role.
            return False
        elif not (time_of_day == 0 or time_of_day == 4): #ie. early morning (sleeping in) or late at night (early bed time)
            return False
        elif the_person is mom and time_of_day == 0 and day%7 == 5:
            return False #Don't want to trigger at the same time as the morning offer.
        elif not the_person.home.has_person(the_person):
            return False
        elif the_person.home.get_person_count() > 1: #Nobody else in the room.
            return False
        return True

    sleeping_walk_in = Action("Sleeping walk in", sleeping_walk_in_requirement, "sleeping_walk_in_label", event_duration = 1)
    limited_time_event_pool.append([sleeping_walk_in,8,"on_enter"])

label sleeping_walk_in_label(the_person): #TODO: This event is currently for Mom or Lily, but we could add more generic paths and have it useable for everyone.
    $ old_location = mc.location #Record these so we can have it dark, but restore it to normal later.
    $ old_lighting = old_location.lighting_conditions
    $ mc.location.lighting_conditions = dark_lighting #ie. she's got hte lights off and the blinds drawn.

    "You open the door to [the_person.possessive_title]'s room."
    if time_of_day == 0: #Morning.
        "For a moment you think it's empty, until you see [the_person.title] lying in bed, still sound asleep."
    else: #Evening
        "For a moment you think the room is empty. Then you notice [the_person.title], already in bed and asleep."

    $ the_person.apply_outfit(the_person.wardrobe.get_random_appropriate_underwear(the_person.effective_sluttiness(), guarantee_output = True)) #She's sleeping in her underwear.
    $ the_person.draw_person(position = "missionary")
    menu:
        "Go inside.":
            "You close the door behind you slowly, careful not to wake [the_person.possessive_title] up."

            menu:
                "Wake her up.": #Wakes her up, starts a conversation. If she thinks her outfit is too slutty she'll get changed first.
                    mc.name "[the_person.title] are you awake?"
                    "You speak quietly, coaxing her back to consciousness."
                    $ the_person.change_happiness(-5)
                    if the_person == mom:
                        "She rolls over and rubs her eyes."
                        the_person "Hmm? Is everything okay [the_person.mc_title]?"
                        mc.name "Everything's fine, I just wanted to talk, if you have a moment."
                        if the_person.judge_outfit(the_person.outfit) and not the_person.has_taboo("underwear_nudity"): # No problem, get up and chat.
                            the_person "I'm always here for you [the_person.mc_title], of course we can talk."
                            $ the_person.draw_person(position = "sitting")
                            "She sits up and yawns, stretching her arms."

                        else: # She needs to get changed.
                            the_person "Of course, but..."
                            "She pulls the bed sheets up to cover her chest."
                            the_person "I'm not decent. Could you just look away for a moment while I get dressed?"
                            mc.name "Okay [the_person.title]."
                            "You avert your eyes. You can hear moving around [the_person.possessive_title] as she gets dressed."
                            $ clear_scene()
                            menu:
                                "Peek":
                                    "You reposition on the bed, sliding to the side so you can \"accidentally\" catch [the_person.title]'s reflection in her bedroom mirror."
                                    $ the_person.apply_outfit(Outfit("Nude"))
                                    $ the_person.draw_person(position = "walking_away")
                                    "You see her naked, quickly digging through her closet for something to put on."
                                    $ the_person.draw_person(position = "standing_doggy")
                                    $ mc.change_locked_clarity(10)
                                    "After searching for a moment she bends over, grabbing something from lower down."
                                    $ clear_scene()
                                    "You look away when she starts to turn around again."

                                "Wait for her to get dressed.":
                                    "You wait patiently until she's finished."
                            $ the_person.apply_outfit()
                            the_person "All done, thank you for waiting [the_person.mc_title]."
                            $ the_person.draw_person()
                            the_person "Now, what did you want to talk about?"
                    else: #Lily
                        "She rolls over and groans unhappily."
                        the_person "What? Ah... what do you want?"
                        mc.name "I wanted to talk, do you have a moment?"
                        if the_person.judge_outfit(the_person.outfit) and not the_person.has_taboo("underwear_nudity"):
                            the_person "Right now? Well, I'm already awake I guess..."
                            $ the_person.draw_person(position = "sitting")
                            "She swings her legs over the side of her bed and sit up, yawning dramatically."
                        else:
                            the_person "Right now? I'm not even dressed... Hey!"
                            "She grabs her pillow and swings at you half-heartedly."
                            the_person "Get out, I need to get dressed!"
                            mc.name "Relax! Just get dressed already, it's no big deal."
                            the_person "Just look away and let me put some clothes on."
                            mc.name "Fine. I promise I won't peek."
                            $ clear_scene()
                            "You look away, and [the_person.title] get's out of bed and starts to get dressed."
                            menu:
                                "Peek":
                                    "You reposition on the bed, sliding to the side so you can \"accidentally\" catch [the_person.title]'s reflection in her bedroom mirror."
                                    $ the_person.apply_outfit(Outfit("Nude"))
                                    $ the_person.draw_person(position = "walking_away")
                                    "You see her naked, quickly digging through her drawers for something to put on."
                                    $ the_person.draw_person(position = "standing_doggy")
                                    $ mc.change_locked_clarity(10)
                                    "After searching for a moment she bends over, grabbing something from lower down."
                                    $ clear_scene()
                                    "You look away when she starts to turn around again."

                                "Wait for her to get dressed.":
                                    "You wait patiently until she's finished."
                            $ the_person.apply_outfit()
                            the_person "Okay, you can look again."
                            $ the_person.draw_person()
                            the_person "Now what was so important you needed to wake me up?"


                    $ old_location.lighting_conditions = old_lighting
                    call talk_person(the_person) from _call_talk_person_20

                "Sleep in her bed.{image=gui/heart/Time_Advance.png}{image=gui/heart/Time_Advance.png}" if time_of_day == 4: #Only at night #TODO: Break the "sleep with" events out for more detail
                    "You move quietly to the side of [the_person.possessive_title]'s bed, lift the covers, and lie down next to her."
                    if the_person == mom:
                        "She stirs, rolling over to face you."
                        the_person "[the_person.mc_title]? Is everything alright?"
                        mc.name "Yeah, I just can't sleep [the_person.title]. Can I stay with you tonight?"
                        if the_person.love < 15:
                            the_person "You're a little old to have to be sleeping with your Mom."
                            "She gives you a gentle kiss on the forehead."
                            the_person "Go get yourself a glass of warm milk, add a little honey, and then try falling asleep again."
                            the_person "I'm sure that'll do it. Okay?"
                            mc.name "Okay, thanks for the help [the_person.title]."
                            "She smiles sleepily at you, and seems to be asleep by the time you make it to the door."
                            $ the_person.on_room_enter_event_list.append(Limited_Time_Action(sleeping_walk_in, sleeping_walk_in.event_duration)) #re-add the LTE since she's still asleep. Note that we can't have stat effects for this, otherwise it's infinitely farmable
                            $ mc.change_location(hall)
                        else:
                            $ the_person.change_love(2)
                            the_person "You still come right to your mommy when you can't sleep. That's so sweet."
                            "She gives you a gentle kiss on the forehead."
                            the_person "Of course you can stay. Let's get some rest."
                            #TODO: Break some of this out to a "sleep with Mom" event
                            $ old_location.lighting_conditions = old_lighting
                            call advance_time() from _call_advance_time_31

                    else: # Lily
                        "She groans and rolls over to face you."
                        the_person "[the_person.mc_title]? What... What are you doing here?"
                        mc.name "I can't sleep, can I stay here for a bit?"
                        if the_person.love < 25:
                            the_person "We're too old for this, I really just want to get some sleep."
                            the_person "Go bug [mom.title], maybe she'll let you stay with her."
                            mc.name "Fine, I'll leave you alone."
                            the_person "Thank... you..."
                            "You get out of bed, and [the_person.title] is asleep again by the time you make it to the door."
                            $ the_person.on_room_enter_event_list.append(Limited_Time_Action(sleeping_walk_in, sleeping_walk_in.event_duration)) #readd the LTE since she's still asleep. Note that we can't have stat effects for this, otherwise it's infinitely farmable
                            $ mc.change_location(hall)
                        else:
                            the_person "You really need your little sister, huh?"
                            $ the_person.change_love(2)
                            "She smiles and laughs sleepily."
                            the_person "You did let me sleep with you when we were younger, so sure."
                            the_person "Just stay on your side, and don't hog the blankets."
                            #TODO: Break some of this out into a "sleep with Lily" event
                            $ old_location.lighting_conditions = old_lighting
                            call advance_time() from _call_advance_time_32 #TODO: Double check advancing like this doesn't break anything.
                    #TODO: Let you try and cuddle-fuck her.
                    #TODO: Write cuddle fuck as a sex position. (Include transition from/to missionary and from/to doggy style)


                "Get a better look at her.":
                    "You wait a moment to make sure [the_person.title] is completely asleep, then creep closer to her bed."
                    "You reach out and gently pull the bed sheets down to her thighs."
                    the_person "Hmm? Mmm..." #TODO: We need an "asleep emotion" (ie. eyes closed, mouth neutral)
                    "She murmurs to herself, still asleep, and rolls onto her back."
                    call nightime_grope(the_person) from _call_nightime_grope #Break this out into a seperate function so we can loop easily. Returns True if our action woke her up
                    $ awake = _return
                    $ clear_scene()
                    if not awake:
                        $ the_person.on_room_enter_event_list.append(Limited_Time_Action(sleeping_walk_in, sleeping_walk_in.event_duration)) #Readd LTE.
                    $ mc.change_location(hall)



        "Let her sleep.":
            "You back out of the room and close door slowly, careful not to wake [the_person.possessive_title]."
            $ the_person.on_room_enter_event_list.append(Limited_Time_Action(sleeping_walk_in, sleeping_walk_in.event_duration)) # Re-add this LTE so it keeps triggering when you go back.
            $ mc.change_location(hall) #Make sure to change our location so we aren't immediately inside again.

    $ old_location.lighting_conditions = old_lighting
    $ clear_scene()
    return

label nightime_grope(the_person, masturbating = False):
    # A couple outcomes are possible:
    # 1) You do some stuff, and then get out
    # 2) You do some stuff and get caught. Large Love hit, maybe future reprecusions event. Useful way to break taboos early at the cost of Love.
    # 3) You do some stuff, get caught, but she's into it. Enter sex system.
    # Goal is to have this be relatively person agnostic, so we can use it with anyone.
    # Options to feel up/strip girl may be their own path?
    $ awake = False
    $ bra_item = the_person.outfit.get_bra()
    $ panties_item = the_person.outfit.get_panties()

    # Establish the Sluttiness requirement tokes ahead of time so we can reference them inline.
    $ grope_tits_slut_requirement = 10
    $ grope_tits_slut_token = get_red_heart(grope_tits_slut_requirement)

    $ grope_pussy_slut_requirement = 15
    $ grope_pussy_slut_token = get_red_heart(grope_pussy_slut_requirement)

    $ jerk_off_slut_requirement = 10
    $ jerk_off_slut_token = get_red_heart(jerk_off_slut_requirement)

    $ titfuck_slut_requirement = 30
    $ titfuck_slut_token = get_red_heart(titfuck_slut_requirement)

    $ facefuck_slut_requirement = 40
    $ facefuck_slut_token = get_red_heart(facefuck_slut_requirement)

    $ fuck_slut_requirement = 50
    $ fuck_slut_token = get_red_heart(fuck_slut_requirement)

    if masturbating: #TODO: Add a few variations of this since we might loop through here a few times
        "You stroke your cock, thinking about what you want to do with [the_person.possessive_title]."

    #TODO: We may want to replace this with an Action based menu at some point to more conveniently format all of the options
    menu:
        "Grope her tits. -5{image=gui/extra_images/energy_token.png}" if mc.energy >= 5 and the_person.effective_sluttiness() >= grope_tits_slut_requirement:
            $ mc.change_energy(-5)
            if the_person.outfit.tits_available():
                "You reach out and gently place your hand on one of [the_person.possessive_title]'s tits."
                $ the_person.draw_person(position = "missionary", the_animation = tit_bob, animation_effect_strength = 0.5)
                if the_person.has_large_tits():
                    "Her breast is large, warm, and soft under your hand. [the_person.title] sighs softly when you squeeze it."
                    "You grab her other boob too and start to massage both of them. They bounce and jiggle easily with each motion."
                else:
                    "You're able to cup her entire soft breast with one hand. [the_person.title] sighs softly when you squeeze it."
                    "You plant a hand on her other boob too and massage both of them. After a moment of teasing you feel her nipples harden."
                $ the_person.change_arousal(4 + mc.sex_skills.get("Foreplay", 0))
                $ mc.change_locked_clarity(10)

            else:
                "You reach out and gently place your hand on one of [the_person.possessive_title]'s tits, seperated only by her [bra_item.display_name]."
                if the_person.has_large_tits():
                    "Her tits are large, barely contained by her [bra_item.display_name] and begging to be set free."
                    "You grab her other boob and massage both at once. She sighs softly in her sleep."
                else:
                    "Even with it hidden away you can enjoy her perky tit."
                    "You grab her other boob, and start to massage both of them at once through her [bra_item.display_name]."

                $ the_person.change_arousal(1 + mc.sex_skills.get("Foreplay", 0))
                $ mc.change_locked_clarity(5)

            the_person "Ah..."


            if renpy.random.randint(0,100) < 15:
                $ awake = True
                if masturbating:
                    "Her eyes flutter lightly. You pull your hands back and stuff your cock hastily back in your pants as she lazily opens her eyes."
                else:
                    "Her eyes flutter lightly. You pull your hands back as she lazily opens her eyes."
                the_person "[the_person.mc_title]? Is that you?"
                mc.name "Hey [the_person.title], I was just checking in on you."
                $ the_person.change_happiness(-5)
                $ the_person.change_slut_temp(1 + the_person.get_opinion_score("being submissive"))
                "She rubs her eyes."
                the_person "I'm fine, do you need anything?"
                mc.name "No, I was just going... Sorry for waking you up."
                "[the_person.possessive_title] seems slightly confused as you back quickly out of the room."
                return True
            else:
                "She murmurs softly in her sleep, unaware of you feeling up her chest."

            if not awake and bra_item is not None and the_person.outfit.is_item_unanchored(bra_item, half_off_instead = True) and not bra_item.half_off:
                menu:
                    "Move her [bra_item.display_name].":
                        "You move slowly, hooking a finger underneath her [bra_item.display_name] and lifting it up and away."
                        $ the_person.draw_animated_removal(bra_item, position = "missionary", half_off_instead = True) #TODO: Decide if we need some special position info here
                        if the_person.has_large_tits():
                            "[the_person.possessive_title]'s tits spill free, jiggling for a couple of seconds before finally coming to a stop."
                        else:
                            pass #No extra dialogue needed
                        $ mc.change_locked_clarity(10)

                        if renpy.random.randint(0,100) < 15 - 2*the_person.get_opinion_score("not wearing underwear"):
                            the_person "Hmmm?"
                            if masturbating:
                                "[the_person.title]'s eyes flutter open. You jump back, stuffing your cock back into your pants as quickly as possible."
                            else:
                                "[the_person.title]'s eyes flutter open. You jump back, doing your best to look innocent."
                            mc.name "Sorry [the_person.title], I thought I had heard you say something and was checking in. I didn't mean to wake you up."
                            "[the_person.possessive_title] rubs her eyes and sits up, then notices her [bra_item.display_name] isn't covering her."
                            if the_person.judge_outfit(the_person.outfit):
                                the_person "I must have been having a dream and tossing in my sleep... I'm okay, thank you [the_person.mc_title]."
                            else:
                                "She yanks it back into place, then pulls the bed covers up around herself."
                                $ the_person.outfit.restore_all_clothing()
                                $ the_person.draw_person(position = "missionary") #TODO: Check if we need special position stuff here
                                the_person "I'm fine [the_person.mc_title], I must have just been having a bad dream."
                                $ the_person.change_happiness(-5)
                                $ the_person.change_love(-1)
                                $ the_person.change_slut_temp(1 + the_person.get_opinion_score("showing her tits"))
                                "She doesn't sound entirely convinced of her own explanation, but seems willing to let it go."


                            mc.name "That makes sense, sorry again!"
                            "You beat a hasty retreat from [the_person.possessive_title]'s bedroom."
                            return True
                        else:
                            the_person "Mmm..."
                            "[the_person.title] shifts in bed, but doesn't wake up."


                    "Leave it alone.":
                        "Your head wins out over your dick, and you decide not to risk it."
                        "You keep pawing at her tits through her [bra_item.display_name] instead."

            call nightime_grope(the_person, masturbating) from _call_nightime_grope_1
            return _return

        "Grope her tits. -5{image=gui/extra_images/energy_token.png} (disabled)" if mc.energy < 5 and the_person.effective_sluttiness() >= grope_tits_slut_requirement:
            pass

        "Grope her tits. -5{image=gui/extra_images/energy_token.png}\n{color=#ff0000}Requires:[grope_tits_slut_token]{/color} (disabled)" if the_person.effective_sluttiness() < grope_tits_slut_requirement:
            pass

        "Grope her pussy. -5{image=gui/extra_images/energy_token.png}" if mc.energy >= 5 and the_person.effective_sluttiness() >= grope_pussy_slut_requirement:
            "You reach a hand between [the_person.title]'s warm thighs."
            $ mc.change_energy(-5)
            $ the_person.draw_person(position = "missionary", the_animation = ass_bob, animation_effect_strength = 0.5)
            if the_person.outfit.vagina_available():
                "You gently pet her pussy, feeling her soft folds."
                "[the_person.possessive_title] shifts and moans again when you brush agaisnt the small nub of her clit."
                $ the_person.change_arousal(6 + mc.sex_skills.get("Foreplay", 0))
                $ mc.change_locked_clarity(10)
            else:
                "You massage her pussy through her [panties_item.display_name]."
                "Through the fabric you're able to make out the faint bump of her clit. She moans when you brush it."
                $ the_person.change_arousal(10 + mc.sex_skills.get("Foreplay", 0))
                $ mc.change_locked_clarity(5)
            the_person "Mmph..."

            if renpy.random.randint(0,100) < 20 - 3*the_person.get_opinion_score("being fingered"):
                "[the_person.title] shifts in bed, then groans and starts to sit up."
                if masturbating:
                    "You yank your hand back and stuff your cock back in your pants as her eyes flutter open."
                else:
                    "You yank your hand back and step away from the bed as her eyes flicker open."

                the_person "[the_person.mc_title], is that you? What... What's going on?"
                mc.name "Oh, nothing [the_person.title]. I thought I heard you say something, so I was just checking in..."
                $ the_person.change_slut_temp(1 + the_person.get_opinion_score("being submissive"))
                the_person "Oh... I must have been talking in my sleep. I was having a dream, that's all."
                mc.name "Right, that makes sense. Sorry for waking you up."
                "You beat a hastiy retreat, leaving [the_person.possessive_title] slightly confused."
                return True
            else:
                "She sighs and spreads her legs for you, instinct driving her even when asleep."
                $ mc.change_locked_clarity(10)

            if not awake and panties_item is not None and the_person.outfit.is_item_unanchored(panties_item, half_off_instead = True) and not panties_item.half_off:
                menu:
                    "Move her [panties_item.display_name].":
                        "You hook a finger under her [panties_item.display_name] and slowly slide them away."
                        $ the_person.draw_animated_removal(panties_item, position = "missionary", half_off_instead = True) #TODO: Decide if we need position info here
                        $ mc.change_locked_clarity(10)
                        if renpy.random.randint(0,100) < 25 - the_person.get_opinion_score("not wearing underwear"):
                            "[the_person.title] groans and rolls over, grabbing her [panties_item.display_name] forcing you to pull your hand away."
                            if masturbating:
                                "You stuff your cock back into your pants as quickly as you can manage when her eyes start to flutter open."
                            else:
                                "You take a step back as her eyes flutter open and she starts to sit up."
                            the_person "Ugh... Is someone there? [the_person.mc_title]?"
                            mc.name "Yeah, it's me [the_person.title]. I thought you had said something, but you must have just been talking in your sleep."
                            if the_person.judge_outfit(the_person.outfit):
                                the_person "Mmm... I was having a dream. What did I say?"
                                mc.name "I'm not sure, I just thought I should check on you. It looks like you're though."
                                "You back out of her room, leaving her confused but unaware of what you had been up to."
                            else:
                                the_person "Mmm... I was having a dream and..."
                                "She glances down and realises how exposed she is. She gathers up the blankets and pulls them up to cover herself."
                                $ the_person.outfit.restore_all_clothing()
                                $ the_person.draw_person(position = "missionary") #TODO: Check if we need special position stuff here
                                $ the_person.change_happiness(-5)
                                $ the_person.change_love(-1)
                                $ the_person.change_slut_temp(1 + the_person.get_opinion_score("showing her ass"))
                                the_person "I'm fine though, really. Thanks for checking in..."
                                mc.name "Right, good to hear. Forget I was even here..."
                                "You beat a hasty retreat, unsure if [the_person.title] really believed your excuse."
                            return True
                        else:
                            "[the_person.title] murmurs something, but sleeps on peacefully."


                    "Leave it alone.":
                        "Your head wins out over your dick, and you decide not to risk it."
                        "You continue to stroke her pussy through her [panties_item.display_name] instead."

            call nightime_grope(the_person, masturbating) from _call_nightime_grope_2
            return _return

        "Grope her pussy. -5{image=gui/extra_images/energy_token.png} (disabled)" if mc.energy < 5 and the_person.effective_sluttiness() >= grope_pussy_slut_requirement:
            pass

        "Grope her pussy. -5{image=gui/extra_images/energy_token.png}\n{color=#ff0000}Requires:[grope_pussy_slut_token]{/color} (disabled)" if the_person.effective_sluttiness() < grope_pussy_slut_requirement:
            pass

        "Jerk off." if not masturbating and the_person.effective_sluttiness() >= jerk_off_slut_requirement:
            if the_person.outfit.tits_visible():
                "Seeing [the_person.possessive_title] exposed in front of you, tits out, is enough to make you rock hard."

            elif the_person.outfit.vagina_visible():
                "Seeing [the_person.possessive_title] exposed in front of you, pussy out and waiting, is enough to make you rock hard."

            else:
                "Looking at [the_person.possessive_title] laid out in front of you half naked is enough to make you rock hard."

            "You pull your pants down and grab your cock, stroking it to the sight."
            $ mc.change_locked_clarity(10)

            if renpy.random.randint(0,100) < 5:
                "[the_person.title] shifts in her sleep, mumbles something, then sits up in bed."
                "You hurry and stuff your cock back into your pants as she opens her eyes and looks at you."
                the_person "[the_person.mc_title], what are you... Doing here?"
                mc.name "I thought... I heard you talking in your sleep. That's all."
                if the_person.effective_sluttiness() > 30 and not (the_person.has_taboo("touching_penis") and the_person.has_taboo("sucking_cock")): #High slut, doesn't care. TODO: Add a taboo break variant
                    $ the_person.update_outfit_taboos()
                    the_person "Uh huh? Then why is your cock hard?"
                    mc.name "I... Was... Uh..."
                    "You try and invent a quick excuse, but [the_person.possessive_title] just giggles and waves her hand."
                    the_person "Do you want some help with that? It seems like it's really distracting you..."
                    menu:
                        "Let her \"help\".":
                            mc.name "Sure, come take care of this for me."
                            if (the_person.effective_sluttiness() + 10*the_person.get_opinion_score("giving blowjobs")) > 50 and not the_person.has_taboo("sucking_cock"):
                                "She nods and sits up, then slides out of bed and gets onto her knees in front of you."
                                $ the_person.draw_person(position = "blowjob")
                                the_person "Mmm, I want to suck on that cock..."
                                $ mc.change_locked_clarity(10)
                                "[the_person.possessive_title] kisses the tip of your dick, then opens her lips and slides you into her mouth."
                                "She looks up at you from her knees, maintaining eye contact as she begins to bob her head up and down your shaft."
                                call fuck_person(the_person, start_position = blowjob, position_locked = True, girl_in_charge = True) from _call_fuck_person_94 #Standing position should be selected by default
                                $ the_report = _return
                                call sex_report_helper(the_person, the_report) from _call_sex_report_helper

                            else:
                                $ the_person.draw_person()
                                the_person "Oh my god, look at this..."
                                "She wraps one hand gently around your shaft and strokes it experimentally."
                                the_person "Just relax, I'm going to take care of this for you [the_person.mc_title]."
                                "[the_person.possessive_title] holds you close as she begins to jerk you off."
                                call fuck_person(the_person, start_position = handjob, position_locked = True, girl_in_charge = True) from _call_fuck_person_95
                                $ the_report = _return
                                call sex_report_helper(the_person, the_report) from _call_sex_report_helper_1




                        "Just leave.":
                            mc.name "I'm fine, I can take care of it. Sorry for waking you up."
                            "[the_person.title] almost seems disappointed as you back out of her room and close the door."


                else:
                    the_person "Uh huh... Maybe you should go and take care of... That."
                    $ the_person.change_happiness(-10)
                    $ the_person.change_love(-2)
                    $ the_person.change_slut_temp(1 + the_person.get_opinion_score("being submissive"))
                    "She nods at your pants, and the obvious crotch bulge."
                    "You try and re-adjust your pants to hide it as you back out of the room."
                return True
            else:
                "[the_person.title] sleeps peacefully, unaware of your thick cock being stroked only inches away."
            call nightime_grope(the_person, True) from _call_nightime_grope_3
            return _return

        "Jerk off.\n{color=#ff0000}Requires:[jerk_off_slut_token]{/color} (disabled)" if not masturbating and the_person.effective_sluttiness() < jerk_off_slut_requirement:
            pass

        "Get ready to cum." if masturbating:
            "You speed up your strokes, aware of the limited amount of time you might have before [the_person.possessive_title] wakes up."
            "With her exposed body as motivation it doesn't take long to push yourself to the edge."

            call sleep_climax_manager(the_person, face_allowed = True, tits_allowed = True)
            $ awake = _return
            # $ climax_options = []
            # $ climax_options.append(["Cum in your hand.","air"])
            # if the_person.effective_sluttiness() >= cum_face_slut_requirement:
            #     $ climax_options.append(["Cum on her face.","face"])
            # else:
            #     $ climax_options.append(["Cum on her face.\n{color=#ff0000}Requires:[cum_face_slut_token]{/color} (disabled)","face"])
            #
            # if the_person.effective_sluttiness() >= cum_tits_slut_requirement:
            #     $ climax_options.append(["Cum on her tits.","tits"])
            # else:
            #     $ climax_options.append(["Cum on her tits.\n{color=#ff0000}Requires:[cum_tits_slut_token]{/color} (disabled)","tits"])
            # $ climax_controller = ClimaxController(*climax_options)
            # $ the_choice = climax_controller.show_climax_menu()
            # "You take a deep breath and pass the point of no return."
            # if the_choice == "Cum in your hand.":
            #     call sleep_cum_hand(the_person)
            #
            # elif the_choice == "Cum on her face.":
            #     call sleep_cum_face(the_person)
            #     $ awake = _return
            #
            # elif the_choice == "Cum on her tits.":
            #     call sleep_cum_tits(the_person)
            #     $ awake = _return

        "Tit fuck her." if the_person.has_large_tits() and the_person.outfit.tits_available() and masturbating and the_person.effective_sluttiness() >= titfuck_slut_requirement:
            "You climb onto [the_person.possessive_title]'s bed and swing one leg over her, straddling her chest."
            "You lower yourself down and settle your cock between her tits. You grab one with each hand and squeeze them gently around your shaft."
            $ the_person.draw_person(position = "missionary", the_animation = tit_bob, animation_effect_strength = 0.7)
            "You start to fuck her tits, moving as slowly as you can bear while wrapped in her warm soft mammaries."
            $ mc.change_locked_clarity(20)
            if renpy.random.randint(0,100) < 50 - 5*the_person.get_opinion_score("giving tit fucks"):
                the_person "Mmm... Mmmph... Hmm?"
                "[the_person.possessive_title] moans softly, then lifts her head up and opens her eyes."
                the_person "[the_person.mc_title]?"
                if the_person.effective_sluttiness("touching_body") + 5*(the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("giving tit fucks")) >= 45 and not the_person.has_taboo("touching body"):
                    "She looks you up and down, her eyes eventually settling on your hard cock sandwiched between her tits."
                    the_person "Mmm... You don't have to stop, I was having the most amazing dream."
                    "She reaches down and puts her own hands over yours, squeezing her breasts together even harder."
                    $ mc.change_locked_clarity(20)
                    "You breathe a sigh of relief and start to pump your hips again."
                    the_person "How about you stand up and let me take care of you properly, hmm?"
                    menu:
                        "Let her tit fuck you.":
                            mc.name "That sounds fantastic [the_person.title]."
                            the_person "I thought you would be interested... Stand up."
                            $ the_person.draw_person(position = "blowjob")
                            "You do as you're told, standing up again. [the_person.possessive_title] gets off of her bed and onto her knees in front of you."
                            "She takes her tits up in her hands and lifts them up, pressing them on either size of your shaft."
                            if rank_tits(the_girl.tits) >= 7: #E sized or larger
                                "They're warm, soft, and feel like they melt around your sensitive dick. Her breasts are so large the tip of your cock doesn't even make it to the top of her cleavage."
                            else:
                                "They're warm, soft, and feel like they melt around your sensitive dick. The tip of your cock just barely pops out of the top of her cleavage."
                            call fuck_person(the_person, start_position = tit_fuck, position_locked = True, girl_in_charge = True) from _call_fuck_person_96
                            $ the_report = _return
                            call sex_report_helper(the_person, the_report) from _call_sex_report_helper_2

                        "Just leave.":
                            mc.name "That sounds like a good time, but maybe some other time..."
                            "You pull your cock out from between her breasts and stand up. [the_person.title] seems disappointed."
                            the_person "Feeling shy now that I'm awake? I'm sorry [the_person.mc_title], I didn't mean to scare you off..."
                            "You stuff your cock back in your pants and hurry out of the room, leaving [the_person.possessive_title] awake and confused."

                else:
                    "She seems momentarily stunned seeing you straddling her, cock held between her tits."
                    mc.name "Hey [the_person.title], I was just..."
                    "She gasps and pushes on your thighs, trying to move you off of her."
                    $ the_person.change_happiness(-10)
                    $ the_person.change_love(-5 + (2*the_person.get_opinion_score("being submissive")))
                    $ the_person.change_slut_temp(1 + the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("giving tit fucks"))
                    the_person "[the_person.mc_title]! Oh my god, what are you doing?"
                    "You shuffle backwards, then swing a leg over her and stand back up beside her bed. Her eyes are fixed on your rock hard dick."
                    the_person "You shouldn't... You can't do this [the_person.mc_title]!"
                    mc.name "It's not what it looks like, I was just..."
                    "She tears her eyes away from you and shakes her head."
                    the_person "No, just go. I don't want to talk about it. Ever."
                    "You stuff your erection back in your pants and hurry out of her room."

                return True
            else:
                "Despite the unavoidable bouncing of the mattress and your cock jammed between her breasts, [the_person.possessive_title] continues to sleep soundly."
                "You squeeze down on her tits as much as you dare, and soon your precum has turned her cleavage into a warm, slippery, fuck channel."
                $ mc.change_locked_clarity(20)
                "You enjoy [the_person.possessive_title]'s body for a few minutes, each stroke between her breasts pulling you closer to your orgasm."
                "Soon you're right at the edge, with nothing left to do but decide where to finish."
                call sleep_climax_manager(the_person, face_allowed = True, tits_allowed = True)
                $ awake = _return

        "Tit fuck her.\n{color=#ff0000}Requires:[titfuck_slut_token]{/color} (disabled)" if the_person.has_large_tits() and the_person.outfit.tits_available() and masturbating and the_person.effective_sluttiness() < titfuck_slut_requirement:
            pass

        "Face fuck her." if masturbating and the_person.effective_sluttiness() >= facefuck_slut_requirement:
            "You step closer to [the_person.possessive_title]'s bed, putting your cock right next to her face."
            "You put a finger on her chin and encourage her to turn her head to the side."
            "After a moment of resistance she sleepily rolls her head towards you, and you can feel her warm breath on the tip of your dick."
            "You take a deep breath, then move your hips and press the tip of your cock against her lips."
            $ mc.change_locked_clarity(10)
            the_person "Hmmm? Mmph..."
            $ the_person.draw_person(position = "missionary", special_modifier = "blowjob", the_animation = blowjob_bob, animation_effect_strength = 0.7)
            "[the_person.title] mumbles something, and you seize the moment to slide yourself past her lips."
            "Her tongue licks experimentally at your tip, exploring its visitor."
            "You place a hand on the back of her head and hold it steady as you move even deeper into her warm, wet, mouth."
            the_person "Mmph... Umph..."
            $ mc.change_locked_clarity(20)
            if renpy.random.randint(0,100) < 70 - 5*the_person.get_opinion_score("giving blowjobs"):
                "You're starting to think you actually get away with this when [the_person.possessive_title]'s eyes start to flutter."
                if the_person.effective_sluttiness("sucking_cock") + 5*(the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("giving blowjobs")) >= 50 and not the_person.has_taboo("sucking_cock"):
                    "Before you can react her eyes drift open."
                    "[the_person.title] blinks twice, as if surprised to find your cock in her mouth, and then starts to bob her head and suck you off."
                    $ mc.change_locked_clarity(20)
                    mc.name "Oh fuck..."
                    $ the_person.draw_person(position = "blowjob")
                    "She gives you few playful bobs of her head, then pulls off with a satisfying pop."
                    the_person "Hey, did you need something? You could have woken me up and I would have been happy to help with this..."
                    "She kisses the tip of your cock for emphasis."
                    the_person "Do you want me to take care of it for you?"
                    menu:
                        "Let her blow you.":
                            mc.name "Sure, come take care of this for me."
                            "She nods and sits up, then slides out of bed and gets onto her knees in front of you."
                            $ the_person.draw_person(position = "blowjob")
                            the_person "Mmm, I want to suck on that cock..."
                            "[the_person.possessive_title] kisses the tip of your dick, then opens her lips and slides you into her mouth."
                            "She looks up at you from her knees, maintaining eye contact as she begins to bob her head up and down your shaft."
                            call fuck_person(the_person, start_position = blowjob, position_locked = True, girl_in_charge = True) from _call_fuck_person_97 #Standing position should be selected by default
                            $ the_report = _return
                            call sex_report_helper(the_person, the_report) from _call_sex_report_helper_3

                        "Just leave.":
                            mc.name "I'm fine, I can take care of it. Sorry for waking you up."
                            "[the_person.title] almost seems disappointed as you back out of her room and close the door."


                else: #TODO: Use gagged text modifier when we have it ready
                    "Before you can react her eyes snap open."
                    the_person "Mmmph!"
                    $ the_person.draw_person(position = "missionary")
                    "She yanks her head back, pulling your cock suddenly out of her mouth."
                    the_person "[the_person.mc_title]! Oh my god, where you just..."
                    "She touches her lips, eyes suddenly locked on your throbbing cock in front of her."
                    mc.name "Oh, hey [the_person.title]. I, uh... Was just checking in on you."
                    $ the_person.change_happiness(-10)
                    $ the_person.change_love(-5 + (2*the_person.get_opinion_score("being submissive")))
                    $ the_person.change_slut_temp(1 + the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("giving blowjobs"))
                    the_person "You should... You should go, alright?"
                    "You stuff your wet dick back into your pants and back up towards her bedroom door."
                    mc.name "Hey, I..."
                    the_person "Just go. I don't want to talk about it."
                    "You leave the room and close her bedroom door behind her."

                return True
            else:
                "You're half-expecting her to snap awake at any time, but [the_person.title] seems to adjust well to having a cock down her throat."
                "Emboldened by your success, you start to thrust in and out. Soon you're happily fucking [the_person.possessive_title]'s mouth."
                $ mc.change_locked_clarity(20)
                "Each stroke of your cock in and out of [the_person.title]'s mouth feels better than the last, and the added thrill of being caught only hightens the experience."
                "It doesn't take long before you're at the edge and ready to cum."
                call sleep_climax_manager(the_person, face_allowed = True, tits_allowed = True, throat_allowed = True, straddle = True)
                $ awake = _return

        "Face fuck her.\n{color=#ff0000}Requires:[facefuck_slut_token]{/color} (disabled)" if masturbating and the_person.effective_sluttiness() < facefuck_slut_requirement:
            pass

        "Fuck her." if the_person.outfit.vagina_available() and masturbating and the_person.effective_sluttiness() >= fuck_slut_requirement: #TODO: Sluttiness requirements
            "You climb onto [the_person.possessive_title]'s bed and position yourself on top of her."
            "After a moment of resistance she unconciously spreads her legs to make room for you."
            $ mc.change_locked_clarity(20)
            "You grab your cock and tap the tip of it against her slit. She mumbles something in her sleep in response."
            menu:
                "Put on a condom.":
                    "You pause before pushing yourself into [the_person.title]'s pussy."
                    "You pull a condom out of your pocket, rip open the package, and roll it over your cock."
                    $ mc.condom = True
                    "When you're protected you lie back down on top of [the_person.possessive_title] and tease her cunt with the tip of your cock."

                "Fuck her raw.":
                    "There's no way you're about to stop now and fumble with a condom. She probably won't care, right?"

            "You push your hips forward and sink your cock into [the_person.title]. She mumbles softly in her sleep."
            if the_person.get_opinion_score("vaginal sex") > 0:
                the_person "... Fill me up... Mmph..."
                $ mc.change_locked_clarity(10)
                "She rolls her hips against yours, naturally encouraging you to push your full length into her."
                $ the_person.discover_opinion("vagianl sex")

            else:
                pass #No extra dialogue needed.
            "[the_person.possessive_title]'s pussy is warm, wet, and tight around your hard cock. You pause as you bottom out inside of her, enjoying the feeling."
            $ the_person.draw_person(position = "missionary", the_animation = missionary_bob, animation_effect_strength = 0.7)
            $ mc.change_locked_clarity(20)
            "You can't hold still for long. You start to move your hips, fucking [the_person.title] while trying to avoid any other movements that might wake her up."
            if renpy.random.randint(0,100) < 50 - 5*the_person.get_opinion_score("vaginal sex"):
                "You're so lost in the feeling of fucking [the_person.possessive_title] that you almost don't notice when her eyes flutter open."
                the_person "... Hmm... Ah... [the_person.mc_title]?"
                if the_person.effective_sluttiness("vaginal_sex") + 5*(the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("vaginal sex")) >= 60 and not the_person.has_taboo("vaginal_sex"):
                    "She takes a moment to comprehend what's happening, then rests her head back on her pillow and moans."
                    the_person "Is this a dream? Ah... Mmmm..."
                    mc.name "Hey [the_person.title], I hoep you don't mind. I just really needed to take..."
                    "You thrust hard into her, emphasising each word."
                    $ mc.change_locked_clarity(10)
                    mc.name "Care... Of..."
                    "Thrust, moan. Thrust, moan."
                    $ mc.change_locked_clarity(10)
                    mc.name "This!"
                    $ mc.change_locked_clarity(10)
                    if the_person.effective_sluttiness() >= the_person.get_no_condom_threshold():
                        the_person "Oh my god... Ah... Yes!"
                    else:
                        the_person "Yes! Ah... Are you... wearing a condom?"
                        if mc.condom:
                            mc.name "Of course I am. We have to be safe, right?"
                            the_person "Good... Keep fucking me [the_person.mc_title], I want you to keep fucking me!"
                        else:
                            mc.name "I couldn't wait, I just needed to get inside of you."
                            if the_person.break_taboo("condomless_sex"):
                                the_person "Oh no, you can't... We shouldn't... What if you..."
                                "She moans as you fuck her, despite her hesitations."
                                mc.name "It's a little late for that now, isn't it?"
                                if the_person.on_birth_control:
                                    the_person "Ah... Just... Be careful!"
                                else:
                                    the_person "Ah... Okay, just be careful! I'm not on the pill, we can't have any mistakes!"
                                    $ the_person.update_birth_control_knowledge()
                                    "She moans happily and relaxes underneath you, her last worry dismissed."
                            else:

                                "She moans happily as you fuck her."
                                the_person "It's fine, just... Ah... Be sure to pull out..."

                    call fuck_person(the_person, start_position = missionary, start_object = mc.location.get_object_with_name("bed"), skip_intro = True, skip_condom = True) from _call_fuck_person_98
                    $ the_report = _return
                    call sex_report_helper(the_person, the_report) from _call_sex_report_helper_4

                else:
                    "She takes a moment to comprehend what's happening, then she gasps and shakes her head."
                    the_person "Oh my god, what are we... what are you doing! Pull out!"
                    $ the_person.change_happiness(-15)
                    $ the_person.change_love(-7 + (2*the_person.get_opinion_score("being submissive")))
                    $ the_person.change_slut_temp(2 + the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("vaginal sex"))
                    $ the_person.draw_person(position = "missionary")
                    "[the_person.title] pushes on your hips. You pull out of her warm pussy reluctantly."
                    mc.name "Hey, I was just... Checking in on you."
                    the_person "And you ended up fucking me? Oh my god [the_person.mc_title]..."
                    "You roll off of [the_person.possessive_title] and stand up. She pulls the covers up around herself and looks away."
                    the_person "You should go, okay? We don't... need to talk about this."
                    "You think about responding, but decide it's better to get out while you can. You stuff your hard cock back into your pants and back out of the room."
                return True

            else:
                "You expect [the_person.possessive_title] to open her eyes at any moment, but she seems to be sleeping soundly despite being filled up by your cock."
                $ mc.change_locked_clarity(40)
                "You're feeling more confident and speed up, thrusting in and out of her tight pussy. Soon she's dripping wet and moaning in her sleep."
                if the_person.get_opinion_score("vaginal sex"):
                    $ mc.change_locked_clarity(20)
                    the_person "... Yes... Cock... More..."
                    "She murmurs, still unconcious"
                else:
                    pass #No extra dialogue needed.

                $ mc.change_locked_clarity(30)
                "Each stroke into her warm, wet slit draws you closer and closer to your climax. The risk of being caught only makes the experience more exciting."
                "It doesn't take long before you're at the very edge, just barely holding back from cumming."
                call sleep_climax_manager(the_person, stomach_allowed = True, inside_allowed = True)
                $ awake = _return

            $ mc.condom = False #Make sure to take the condom off at the end of the encounter

        "Fuck her.\n{color=#ff0000}Requires:[fuck_slut_token]{/color} (disabled)" if the_person.outfit.vagina_available() and masturbating and the_person.effective_sluttiness() < fuck_slut_requirement:
            pass

        "Leave.":
            if masturbating:
                if the_person.outfit.tits_visible() and mc.focus <= 2:
                    "You move to put your cock back in your pants, but the sight of [the_person.possessive_title]'s naked tits are too much for you to say no to."
                    "You keep stroking off, unable to leave until you've finished what you've started."
                    call nightime_grope(the_person, masturbating) from _call_nightime_grope_4
                    $ awake = _return
                elif the_person.outfit.vagina_visible() and mc.focus <= 2:
                    "You move to put your cock back in your pants, but the sight of [the_person.possessive_title]'s naked pussy distracts you."
                    "You keep stroking off, unable to leave until you've finished what you've started."
                    call nightime_grope(the_person, masturbating) from _call_nightime_grope_5
                    $ awake = _return

                else:
                    if the_person.outfit.tits_visible() or the_person.outfit.vagina_visible():
                        "You give your cock a few more strokes, then force yourself to put your hard cock back into your pants."
                        "It takes a significant amount of willpower to tear yourself away from [the_person.possessive_title]'s hot body."
                    else:
                        "You give your cock a few more strokes, then reluctantly stuff it back into your underwear and zip up your pants."
                    "You back slowly out of the room, leaving [the_person.possessive_title] asleep and unaware of your visit."

    return awake

#Helper funcitons for all the sleep stuff where you cum on her. Returns True if she wakes up.
label sex_report_helper(the_person, the_report): #TODO: We use this in enough places that we should have some her orgasm versions
    if the_report.get("guy orgasms", 0) > 0 and the_report.get("girl orgasms", 0) >0:
        the_person "Wow, you weren't the only one who needed that, apparently."
        "You both take a moment, panting softly as you recover from your orgasms."
        mc.name "Well I'm feeling much better now [the_person.title]."
        the_person "Me too. Come by again if you need some more help, okay"
        mc.name "I'm not going to say no to that."
    elif the_report.get("guy orgasms", 0) > 0:
        the_person "There, all taken care of. Hope that helps [the_person.mc_title]."
        mc.name "I'm feeling much better. Thanks [the_person.title]."
        the_person "For you, any time."
        "You stuff your cock back in your pants and leave [the_person.possessive_title]'s bedroom."
    elif the_report.get("girl orgasms", 0) > 0:
        the_person "Wow, I guess I needed that even more than you did."
        $ the_person.change_obedience(-(2 + the_person.get_opinion_score("being in control")))
        the_person "Sorry [the_person.mc_title], I'll make sure to finish you off next time, okay?"
        mc.name "Next time, huh? I can get behind that."
    else:
        the_person "I'm sorry [the_person.mc_title]. I guess I need a little more practice."
        the_person "Maybe we can do this again later and I can make it up to you, okay?"
        mc.name "Sure, I'm not going to say no to that."
    "You stuff your cock back in your pants and leave [the_person.possessive_title]'s bedroom."
    return

label sleep_climax_manager(the_person, straddle = False, stomach_allowed = False, face_allowed = False, tits_allowed = False, throat_allowed = False, inside_allowed = False): #Helper that collects all of the orgasm checks
    $ cum_tits_slut_requirement = 30
    $ cum_tits_slut_token = get_red_heart(cum_tits_slut_requirement)

    $ cum_face_slut_requirement = 40
    $ cum_face_slut_token = get_red_heart(cum_face_slut_requirement)

    $ cum_throat_slut_requirement = 55
    $ cum_throat_slut_token = get_red_heart(cum_throat_slut_requirement)

    $ cum_inside_slut_requirement = 65
    $ cum_inside_slut_token = get_red_heart(cum_inside_slut_requirement)

    $ climax_options = []
    $ climax_options.append(["Cum in your hand.","air"])

    if stomach_allowed:
        $ climax_options.append(["Cum on her stomach.","body"])

    if face_allowed:
        if the_person.effective_sluttiness() >= cum_face_slut_requirement:
            $ climax_options.append(["Cum on her face.","face"])
        else:
            $ climax_options.append(["Cum on her face.\n{color=#ff0000}Requires:[cum_face_slut_token]{/color} (disabled)","face"])

    if tits_allowed:
        if the_person.effective_sluttiness() >= cum_tits_slut_requirement:
            $ climax_options.append(["Cum on her tits.","tits"])
        else:
            $ climax_options.append(["Cum on her tits.\n{color=#ff0000}Requires:[cum_tits_slut_token]{/color} (disabled)","tits"])

    if throat_allowed:
        if the_person.effective_sluttiness() >= cum_throat_slut_requirement:
            $ climax_option.append(["Cum down her throat.","throat"])
        else:
            $ climax_option.append(["Cum down her throat.\n{color=#ff0000}Requires:[cum_throat_slut_token]{/color} (disabled)"])

    if inside_allowed:
        if the_person.effective_sluttiness() >= cum_inside_slut_requirement or mc.condom:
            $ climax_option.append(["Cum inside her.","pussy"])
        else:
            $ climax_option.append(["Cum inside her.\n{color=#ff0000}Requires:[fuck_slut_token]{/color} (disabled)","pussy"])

    $ climax_controller = ClimaxController(*climax_options)
    $ the_choice = climax_controller.show_climax_menu()
    "You take a deep breath and pass the point of no return."
    if the_choice == "Cum in your hand.":
        call sleep_cum_hand(the_person, climax_controller)
        return _return

    elif the_choice == "Cum on her stomach.":
        call sleep_cum_stomach(the_person, climax_controller)
        return _return

    elif the_choice == "Cum on her face.":
        call sleep_cum_face(the_person, climax_controller, straddle = straddle)
        return _return

    elif the_choice == "Cum on her tits.":
        call sleep_cum_tits(the_person, climax_controller, straddle = straddle)
        return _return

    elif the_choice == "Cum down her throat.":
        call sleep_cum_throat(the_person, climax_controller)
        return _return

    elif the_choice == "Cum inside her.":
        call sleep_cum_vagina(the_person, climax_controller)
        return _return

    return False

label sleep_cum_hand(the_person, climax_controller):
    $ climax_controller.do_clarity_release(the_person)
    "You grunt softly as you climax, doing your best to cum into your hand instead of all over [the_person.title]."
    "When your orgasm has passed you take a moment to catch your breath, then back carefully out of her room."
    return False

label sleep_cum_face(the_person, climax_controller, straddle = False):
    $ awake = False
    $ the_person.cum_on_face()
    $ the_person.draw_person(position = "missionary") #Redraw whatever position we were in previously
    "You grunt softly as you climax, spraying your hot load in an arc onto [the_person.possessive_title]'s unsuspecting face."
    $ climax_controller.do_clarity_release(the_person)
    if the_person.get_opinion_score("drinking cum") > 0:
        "When the first splash of cum hits her face [the_person.title] opens her mouth."
        $ mc.change_locked_clarity(10)
        "You watch as she begins to unconciously lick up your sperm, even as you pulse more out onto her"
        $ the_person.discover_opinion("drinking cum")
    else:
        "[the_person.title] twitches in her sleep as pulse after pulse of cum splashes across her face."


    if renpy.random.randint(0,100) < 60 - 5*the_person.get_opinion_score("being covered in cum"): #TODO: Adjust chance based on opinion
        "A moment later she opens one eye - the one not welded shut by your cum - and locks eyes with you."
        if the_person.effective_sluttiness() + 5*(the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("being covered in cum")) >= 60: #TODO: Cum based taboo stuff
            #She's surprised, but fine with it
            the_person "Oh my... [the_person.mc_title]? Ah..."
            mc.name "Sorry [the_person.title], I just needed some relief and you were..."
            "She wipes a puddle of cum away from her eye and blinks."
            $ mc.change_locked_clarity(5)
            the_person "Oh, it's fine. You obviously really needed it."
            if straddle:
                "You climb off of [the_person.title] and stand up beside her bed, stuffing your cock back in your pants."
            else:
                "You stuff your cock back in your pants, feeling relieved."

            if the_person.get_opinion_score("drinking cum") > 0:
                "[the_person.possessive_title] starts to tidy herself up as you leave, scooping your sperm up with a finger and then licking it clean."
            else:
                "[the_person.possessive_title] starts to clean herself up as you leave, wiping off your sperm with her bed sheets."



        else: #Not okay with it
            the_person "Oh my... [the_person.mc_title]? What did you just..."
            "She reaches up and brushes a hand over her face, feeling the warm puddles of cum you've put there."
            mc.name "Sorry [the_person.title], I just got a little carried away and..."
            the_person "And you finished on my face? I... I don't know what to say [the_person.mc_title]..."
            "Her eyes are locked on your cock, still hard despite the recent orgasm."
            mc.name "I didn't mean to, it just sort of... happened."
            $ the_person.change_happiness(-10)
            $ the_person.change_love(-3 + the_person.get_opinion_score("being covered in cum"))
            $ the_person.change_slut_temp(2 + the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("being covered in cum"))
            the_person "I... You should go. This isn't right, you shouldn't be here..."
            if straddle:
                "You think about what to say, but realise the first thing to do is probably to get your cock out of her face."
                "You climb off of [the_person.title]'s bed and stuff your cock back into your pants."
            else:
                "You hurry to stuff your cock back in your pants."
            mc.name "Let's just pretend this never happened, okay? Just a mistake, no big deal."
            "She nods, but seems unconvinced. You hurry out of the room, leaving her to clean up."

        $ awake = True
    else:
        "Her eyes flutter briefly, despite being solidly welded closed by your cum."
        "She murmurs something, then rolls over. You breathe a sigh of relief and stuff your cock back in your pants."
        $ mc.change_locked_clarity(30)
        "You back out of the room slowly. You wonder how she'll react to waking up with a face full of mystery cum." #TODO: Add some events related to this. Maybe just an additional comment as an on-talk.
        $ the_person.change_slut_temp(2 + the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("being covered in cum"))
    return awake

label sleep_cum_throat(the_person, climax_controller): #Always assumes you're standing up
    $ awake = False
    $ the_person.cum_in_mouth()
    $ the_person.draw_person(position = "missionary", special_modifier = "blowjob") #Position specific stuff
    "You thrust forward, pushing yourself as deep down [the_person.possessive_title]'s throat as you dare."
    $ climax_controller.do_clarity_release(the_person)
    "With one last grunt you climax, sending a blash of hot cum to the back of her mouth."

    if the_person.get_opinion_score("drinking cum") > 0:
        $ the_person.discover_opinion("drinking cum")
        $ mc.change_locked_clarity(10)
        "[the_person.title] reacts instinctively, drinking down your sperm as fast as she can manage even as she sleeps."
    else:
        "[the_person.title] coughs and sputters as you pump a few more pulses down her throat."

    if renpy.random.randint(0,100) < 50 - 5*the_person.get_opinion_score("drinking cum"): #TODO: Adjust chance based on opinion
        $ awake = True
        "As your orgasm passes you relax, pulling your cock out of her mouth."
        "You think you've gotten away with it when her eyes flutter open."
        if the_person.effective_sluttiness() + 5*(the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("drinking cum")) >= 75 and not the_person.has_taboo("sucking_cock"): #Fine with it #TODO: Cum based taboo stuff
            if the_person.get_opinion_score("drinking cum") > 0:
                "[the_person.possessive_title] glances up at you, then swallows proudly. She rolls over and looks up at you from her back."
            else:
                "[the_person.possessive_title] glances up at you. She wipes her lips, clears her throat, then rolls over and looks up at you from her back."
            the_person "Whew... I'm feeling a little light headed... I do need to breath, you know."
            mc.name "You seemed to manage just fine. Sorry for waking you up, I came into check on you and..."
            "She waves her hand."
            the_person "It's fine, I know... Are you all better now?"
            "You nod, stuffing your satisfied cock back into your pants."
            the_person "Good. I think I'm going to need some time to recover, if that's okay."
            mc.name "Of course. Thanks for the help."
            "She smiles, and you back out of her room."

        else: #Not fine with it
            "Her eyes are locked on your dick for a moment, then she glances up at you wide-eyed."
            the_person "[the_person.mc_title]? I..."
            "She coughs, sputtering out the last mouthful of cum you had given her."
            mc.name "Hey [the_person.title]... I was just checking in on you..."
            "[the_person.possessive_title] sits up and bed, wiping her lips with the back of her hand."
            if the_person.has_taboo("sucking_cock"):
                the_person "Was I... giving you a blowjob in my sleep?"
                $ the_person.change_happiness(-15)
                $ the_person.change_love(-4 + the_person.get_opinion_score("drinking cum"))
                mc.name "Uh... Yeah, I guess you were."
                the_person "Oh my god... Nobody can know about this, okay [the_person.mc_title]? I thought it was a dream!"
                $ the_person.change_happiness(-15)
                $ the_person.change_love(-4 + the_person.get_opinion_score("drinking cum"))
                $ the_person.change_slut_temp(2 + the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("drinking cum"))
                mc.name "I thought you were acting a little strange."
                the_person "You... You should go. It was just a dream, okay? I wasn't... I didn't mean to do anything."
                "You stuff your cock back into your pants."
                mc.name "I didn't mind, though. You were pretty good at it."
                $ the_person.break_taboo("sucking_cock")
                the_person "Oh god... I can't believe it."



            else:
                $ the_person.change_happiness(-15)
                $ the_person.change_love(-4 + the_person.get_opinion_score("being covered in cum"))
                $ the_person.change_slut_temp(2 + the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("being covered in cum"))
                the_person "Did you just... Can you put that thing away?"
                "You stuff your cock back into your pants."
                mc.name "Oh, right... Maybe I'll just go, okay?"
                the_person "I... I think that's a good idea."
            "You take your chance and hurry out of [the_person.title]'s room."

    else:
        "As your orgasm passes you relax and pull your cock out of her mouth. It drags out a line of spit and cum as you pull back."
        $ the_person.change_slut_temp(2 + the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("being covered in cum"))
        if the_person.get_opinion_score("drinking cum") > 0:
            "She smiles happily and rolls over, swallowing down the last few drops of your sperm. It feels like she should be thanking you."
        else:
            "She mumbles something and rolls over, her sleep undisturbed by the whole ordeal. Somehow you've gotten away with it."
        $ mc.change_locked_clarity(30)
        "You back quietly out of the room, wondering what she'll think when she wakes up with her breath smelling of mystery cum."
    return awake

label sleep_cum_tits(the_person, climax_controller, straddle = False):
    $ awake = False
    $ the_person.cum_on_tits()
    $ the_person.draw_person(position = "missionary")
    $ climax_controller.do_clarity_release(the_person)
    if the_person.outfit.tits_available():
        "You grunt softly as you climax, spraying your load all over her chest."
    else:
        "You grunt softly as you climax, spraying your load all over her chest and [bra_item.display_name]."

    if the_person.get_opinion_score("being covered in cum") > 0:
        "[the_person.possessive_title] moans as you cum all over her. She mutters quietly in her sleep."
        $ mc.change_locked_clarity(10)
        the_person "Yes daddy... Mmph... Cover me..."
        $ the_person.discover_opinion("being covered in cum")
    else:
        pass #No extra dialogue needed

    if renpy.random.randint(0,100) < 40 - 5*the_person.get_opinion_score("being covered in cum"):
        $ awake = True
        "She reaches up, brushing her chest and running her fingers through your cum."
        the_person "Hmm?"
        "Her eyes flutter open, and she takes a moment to absorb the situation."
        if the_person.effective_sluttiness() + 5*(the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("being covered in cum")) >= 50:
            the_person "Oh... Hello [the_person.mc_title]. What did I miss?"
            if the_person.get_opinion_score("drinking cum") > 0:
                "She idly runs a finger between her cleavage, covering it in cum. She looks at you and licks it clean while you talk."
            else:
                "She idly runs a finger between her cleavage, spreading your cum around."
            mc.name "Hey [the_person.title], I was just checking in on you and... Well, I just couldn't resist."
            "[the_person.possessive_title] shrugs."
            the_person "No harm in it, I suppose. I'm going to need to get cleaned up though."
            if straddle:
                mc.name "Oh, right..."
                "You climb off of [the_person.title] and stuff your cock back into your pants."
            else:
                "You stuff your cock back into your pants."
            mc.name "I'll leave you to it, then."
            the_person "Come by any time."
            "You back out of her room, leaving her to clean your cum off of her chest."
        else:
            if straddle:
                the_person "[the_person.mc_title]? What... What are you doing on top of me?"
                "Her eyes glance down to her chest, splattered with cum, then at your still-hard cock."
                "You hurry to climb off of her bed."
            else:
                the_person "[the_person.mc_title]? What... What did you do?"
                "Her eyes glance down to her chest, splattered with cum, then at your still-hard cock."
            mc.name "I was... Just checking in on you. When I saw you, I just couldn't resist..."
            $ the_person.change_happiness(-10)
            $ the_person.change_love(-3 + the_person.get_opinion_score("being covered in cum"))
            the_person "You... You should go, okay? We don't need to talk about this."
            mc.name "It's not what..."
            the_person "Just go. Please."
            "You take the hint and stuff your cock back into your pants, hurrying out of her bedroom."

    else:
        if the_person.get_opinion_score("being covered in cum") > 0:
            "She reaches up lazily and brushes her chest, spreading your semen around in her sleep."
            the_person "Thank you daddy..."
        else:
            "She murmurs something, then rolls over in bed."
            if straddle:
                "You breathe a sigh of relief, then carefully get off the bed and stuff your cock back into your pants."
            else:
                "You breathe a sigh of relief and stuff your cock back in your pants."
        $ mc.change_locked_clarity(30)
        "You back out of the room slowly. You wonder how she'll react to waking up with her tits covered in mystery cum." #TODO: Events. It doesn't take Sherlock to solve this one.
    return awake

label sleep_cum_stomach(the_person, climax_controller): #Note: always assumes you're stradling her
    $ awake = False
    $ the_person.cum_on_stomach()
    $ the_person.draw_person(position = "missionary")

    $ climax_controller.do_clarity_release(the_person)
    "You grunt softly as you climax, splattering your load over [the_person.title]'s stomach."

    if the_person.get_opinion_score("being covered in cum") > 0:
        "[the_person.possessive_title] moans as you cum on her. She mutters quietly in her sleep."
        $ mc.change_locked_clarity(10)
        the_person "Yes daddy... Mmph... Cover me..."
        $ the_person.discover_opinion("being covered in cum")
    else:
        pass #No extra dialogue needed



    if renpy.random.randint(0,100) < 30 - 5*the_person.get_opinion_score("being covered in cum"):
        $ awake = True
        "She mumbles, and after a brief moment of suspense her eyes flutter open."
        if the_person.effective_sluttiness() + 5*(the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("being covered in cum")) >= 50:
            "[the_person.possessive_title] glances at you, then at the pool of cum on her stomach."
            the_person "Oh... I see."
            mc.name "[the_person.title], I was just checking in on you and..."
            the_person "No, no I think I understand. It's fine, really."
            if the_person.get_opinion_score("drinking cum") > 0:
                "She reaches down and runs a finger through your sperm, then brings the it to her lips and licks it clean."
                the_person "Mmm, I don't really mind. Do you need anything else, or can I get cleaned up?"
            else:
                the_person "Do you need anything else, or can I get cleaned up?"
            mc.name "You can get cleaned up, I'll leave you to it. Talk to you later."
            "You stuff your cock back into your pants and back out of the room as [the_person.possessive_title] sits up in bed."

        else:
            "[the_person.possessive_title] looks over at you. Her eyes go wide when she sees your throbbing cock, still in your hands."
            mc.name "Oh, hey [the_person.title], I..."
            the_person "Why is your... thing out? Is this..."
            "She notices the pool of warm cum on her stomach."
            $ the_person.change_happiness(-10)
            $ the_person.change_love(-3 + the_person.get_opinion_score("being covered in cum"))
            mc.name "I was just checking in on you and..."
            the_person "And you jerked off onto me? Oh my god [the_person.mc_title], this isn't right!"
            mc.name "I couldn't resist, you were looking so good."
            "She covers her face with her hands and sighs. You stuff your cock back into your pants and take a few steps towards the exit."
            the_person "You should go, okay? This never happened, understood?"
            mc.name "Yes [the_person.title]."
            "You take your chance and exit in a hurry, leaving [the_person.possessive_title] to figure out how to clean up your cum."
    else:
        if the_person.get_opinion_score("being covered in cum") > 0:
            "She reaches down and brushes her fingers over the puddles of cum, spreading it around in her sleep."
            the_person "... Thank you daddy..."
        else:
            "She mumbles something, but after a brief moment of suspense seems to still be asleep."
        "You breathe a sigh of relief and stuff your cock back in your pants."
        $ mc.change_locked_clarity(30)
        "As you back out of the room you wonder how she'll react to waking up covered in mystery cum."
    return awake

label sleep_cum_vagina(the_person, climax_controller):
    $ awake = False
    if not mc.condom:
        $ the_person.cum_in_vagina()
        $ the_person.draw_person(position = "missionary")

    $ climax_controller.do_clarity_release(the_person)

    $ wake_chance = 40
    if mc.condom:
        "You blow your load into [the_person.possessive_title]'s pussy, constrained only by a thin layer of latex."
        $ wake_chance += -10 #Less likely to wake up if you cum in a condom, although the same as if she loves creampies (the perfect dream!)
    else:
        $ mc.change_locked_clarity(30)
        "You grunt softly as you climax, blowing your load into [the_person.possessive_title]'s raw pussy."
        $ wake_chance += -5*the_person.get_opinion_score("creampies")



    if renpy.random.randint(0,100) < wake_chance - 5*the_person.get_opinion_score("creampies"):
        $ awake = True
        "She shift in bed, then blinks and opens one eye sleepily."
        the_person "[the_person.mc_title]? What are you doing here? I..."
        "[the_person.possessive_title] lifts her head and looks down, realising you're inside of her."
        if the_person.effective_sluttiness() + 5*(the_person.get_opinion_score("being submissive") + the_person.get_opinion_score("creampies")) > 70 and not the_person.has_taboo("vaginal_sex"):
            the_person "Oh... that's what I was dreaming about."
            "She puts her head back and sighs happily."
            the_person "Thank you [the_person.mc_title]. Mmm..."
            mc.name "It's my pleasure."
            the_person "Wait, are you... wearing a condom?"
            if mc.condom:
                mc.name "Of course I am."
                if the_person.has_taboo("condomless_sex"):
                    "She breathes a loud sigh of relief."
                    the_person "Okay, good. That's good."
                else:
                    the_person "That's probably a good idea. Good thinking."
            else:
                mc.name "I didn't have time, I just needed to fuck you so badly."
                if the_person.has_taboo("condomless_sex"):

                    if the_person.wants_creampie():
                        the_person "Oh, okay. I guess it's already done, so it doesn't matter."
                        the_person "You can't always cum inside me though, okay? What if I get pregnant?"
                    else:
                        if the_person.on_birth_control:
                            the_person "Oh no [the_person.mc_title], what if my birth control doesn't work?"
                            $ the_person.update_birth_control_knowledge()
                        else:
                            the_person "Oh [the_person.mc_title], what have you done? What if I get pregnant?"
                    mc.name "I'm sure it'll be fine, don't worry about it."
                    "She seems unconvinced, but let's the subject drop."
                    $ the_person.break_taboo("condomless_sex")

                else:
                    if the_person.wants_creampie():
                        "She moans softly."
                        the_person "I can feel it... It's so warm."
                    else:
                        "She sighs."
                        the_person "Oh [the_person.mc_title], you shouldn't be cumming in me. You know that."
                        mc.name "Well, it's a little late now."
                        the_person "Yeah, I guess it is."

            if mc.condom:
                "You pull out of [the_person.possessive_title]'s pussy, all of your cum trapped inside of the ballooned tip of your condom."
            else:
                "You pull out of [the_person.possessive_title]'s pussy. A small stream of cum follows, dripping down her inner thigh."

            the_person "So, are you feeling satisfied?"
            mc.name "Yeah, I think that was just what I needed."
            "You get up from [the_person.title]'s bed, stuffing your cock back into your pants."
            the_person "Good, that's what I like to hear. Talk to you later, okay?"
            "You back up towards the door, taking one last peak into the room before you close the door."
            if the_person.get_opinion_score("bareback sex") > 0 and the_person.get_opinion_score("creampies") > 0 and not mc.condom:
                "[the_person.possessive_title] lifts her knees up to her chest and holds them close, keeping all of your cum inside of her pussy."
                $ mc.change_locked_clarity(20)
                the_person "Mmmm, it's so deep..."
            else:
                "[the_person.possessive_title] sighs and rolls over, pulling her blankets back around her."

        else:
            the_person "You're... inside of me."
            mc.name "Hey [the_person.title]... I just couldn't resist."
            the_person "You can't... We can't have sex [the_person.mc_title], it's not right! Pull out, we can finish some other way."
            mc.name "Well, it's a little late for that..."
            "She gasps."
            the_person "You... already came? Please tell me you're wearing a condom!"
            if mc.condom:
                mc.name "Of course. You don't want to get knocked up, do you?"
                if the_person.get_opinion_score("bareback sex") > 0 and the_person.get_opinion_score("creampies") > 0:
                    the_person "Oh fuck, I do... But not by you!"
                else:
                    the_person "Of course not!"
                mc.name "Well you're fine then, okay?"
                $ the_person.break_taboo("vaginal_sex")
            else:
                mc.name "Well... I wasn't really thinking straight and may have forgot."
                the_person "You're kidding, right? What if you got me pregnant?"
                mc.name "Are you on the pill?"
                if the_person.on_birth_control:
                    the_person "I am, but what if it doesn't work?"
                else:
                    the_person "No! You came inside me without any protection!"
                $ the_person.update_birth_control_knowledge()
                mc.name "I'm sure it'll be fine. Try not to overreact, okay?"
                $ the_person.break_taboo("vaginal_sex")
                $ the_person.break_taboo("condomless_sex")

            if mc.condom:
                "You pull out of [the_person.possessive_title]'s pussy, all of your cum trapped inside of the ballooned tip of your condom."
            else:
                "You pull out of [the_person.possessive_title]'s pussy. A small stream of cum follows, dripping down her inner thigh."
            the_person "You... should go. You're finished, right?"
            mc.name "Yeah, I'm feeling pretty satisfied."
            "You stuff your cock back in your pants and retreat out of the room."

    else:
        if the_person.get_opinion_score("creampies") > 0 and not mc.condom:
            the_person "... So full..."
            $ mc.change_locked_clarity(20)
            "She sighs happily, enjoying a pussy full of cum even when she's asleep."
        else:
            "She moans and shifts underneath you, but doesn't wake up."

        "You pull out, trying to avoid any extra movements that might alert [the_person.title]."
        if not mc.condom:
            "A small stream of your cum follows after your cock as you clear her pussy, drippling down her inner thigh."

        "You back up off of her bed and stand up, stuffing your cock back in your pants before backing slowly out of the room."

        if not mc.condom:
            $ mc.change_locked_clarity(30)
            "You wonder when, or if, she'll notice she has a pussy full of mystery cum when she wakes up."

    return awake
