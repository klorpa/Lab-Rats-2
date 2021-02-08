# Contains all of the code related to the punishment events, used when an employee has broken a rule of some sort.

init -1 python:
    list_of_punishments = [] #Establish a central holder for punishments. Mods can add additional punishments to this list.

# Each punishment is an Action.
# The requirements should return the required severity if they would otherwise be unlocked, otherwise they are hidden.
# Note: Some punishments take place over a duration of time. We need to implement those in some way; maybe a Role.

#TODO: Modify the crisis system so roles generate crises seperately from normal stuff.
#TODO: Add an event so a rival snitches on a coworker and generates an infraction.


#5 levels of punishment. Each one will have 3 different options: 1 always available, 1 made available with corporal punishment, and 1 made available with another policy.
#TODO: Some punishments should leave open the possiblity that _resisting_ the punishment can increase the severity.

# Level 1 (Trivial infraction; Arrived slightly late, minor work mistake)
# A) Verbal scolding
# B) Wrist Slap (hand)
# C) Free Serum Testing (Rec: Paid serum testing)

# Level 2 (Minor infraction; uniform non-compliance, under performing work)
# A) Office busy work (ie. coffee girl, personal secretary)
# B) Spanking (Clothed, maybe skirt up)
# C) Office underwear (Req: Some uniform policy)

# Level 3 (Moderate infraction; out of uniform, direct disobedience)
# A) Pay cut
# B) Strip and Spank
# C) Office nudity (Req: Some uniform policy)

# Level 4 (Major infraction; )
# A) Humiliating office work (ie. scrubbing floors, cleaning bathrooms)
# B) Orgasm denial
# C) Forced punishment outfit (Req: Some uniform policy)

# Level 5 (Tremendous infraction; corporate espionage, intentional sabotage)
# A) Unpaid intern
# B) Office Free Use
# C) Dildo gag (Req: Some uniform policy) #TODO: Allow a multitude of gag options: panties, traditional, ball

#TODO Girls who like being submissive will willingly ask for harder punishments, increasing the effective severity of an infraction.

# LEVEL 1 #
init -1 python:
    def punishment_verbal_scolding_requirement(the_person, the_infraction):
        if the_infraction.severity < 1: #In theory not possible, but future events may reduce the effective severity of infractions and it keeps everyting looking similar
            return "Severity 1"
        else:
            return True

    def punishment_wrist_slap_requirement(the_person, the_infraction):
        if not corporal_punishment.is_active():
            return "Requires Policy: Corporal Punishment"
        elif the_infraction.severity < 1:
            return "Severity 1"
        else:
            return True

    def punishment_serum_test_requirement(the_person, the_infraction):
        if not mandatory_paid_serum_testing_policy.is_active():
            return "Requires Policy: Mandatory Paid Serum Testing"
        elif the_infraction.severity < 1:
            return "Severity 1"
        elif mc.inventory.get_any_serum_count() == 0:
            return "Requires: Serum in inventory"
        else:
            return True

    punishement_verbal_scolding_action = Action("Verbal scolding", punishment_verbal_scolding_requirement, "punishment_verbal_scolding")
    punishment_wrist_slap_action = Action("Wrist slaps", punishment_wrist_slap_requirement, "punishment_wrist_slap")
    punishment_serum_test_action = Action("Test serum", punishment_serum_test_requirement, "punishment_serum_test")

    list_of_punishments.append(punishement_verbal_scolding_action)
    list_of_punishments.append(punishment_wrist_slap_action)
    list_of_punishments.append(punishment_serum_test_action)


label punishment_verbal_scolding(the_person, the_infraction): #Note: Pass the infraction so we can reference it if we want.
    "You stare down [the_person.title] and shake your head."
    mc.name "What makes you think this was acceptable?"
    if the_person.obedience < (110 - (15*the_person.get_opinion_score("being submissive"))):
        the_person "I..."
        "You hold up your hand."
        mc.name "Stop. I don't want to hear excuses or half baked reasons."
    else:
        "[the_person.possessive_title] looks meekly at the floor."
        mc.name "Look at me."
        $ the_person.draw_person(emotion = "sad")
        "She raies her head slowly and looks you in the eye."
    mc.name "I need you get it through your head that what I want are results."
    $ the_person.change_obedience(1 + the_person.get_opinion_score("being submissive"))
    $ the_person.change_happiness(-2 + the_person.get_opinion_score("being submissive"))
    $ the_person.discover_opinion("being submissive")
    menu:
        "Keep going.":
            # Insult her work ethic. More obedience, lowers happiness
            mc.name "I expect results because I'm paying you for those results. If you can't deliver I'll have to cut your pay, or cut you loose."
            mc.name "You need to get yourself together and improve, because right now you're letting everyone down."
            if the_person.obedience < (100 - (15*the_person.get_opinion_score("being submissive"))):
                "She opens her mouth to respond, but stops herself at the last moment."
                $ the_person.draw_person(emotion = "angry")
                "Instead she simply glares at you and nods."
            else:
                "[the_person.title] listens and nods apologetically, remaining silent the whole time."
            $ the_person.change_obedience(2 + the_person.get_opinion_score("being submissive"))
            $ the_person.change_happiness(-5 + (2*the_person.get_opinion_score("being submissive")))
            menu:
                "Insult her.":
                    mc.name "Frankly, I'm not sure you really even deserve to be here."
                    mc.name "There were plenty of eager applicants who could have had your job, and I'm sure they could have followed simple instructions."
                    if the_person.obedience < (90 - (15*the_person.get_opinion_score("being submissive"))):
                        "She clenches her fists and grits her teeth, but finally she can take no more."
                        the_person "Do I deserve to be here? I... I can't believe you!"
                        the_person "I come in every day and work my hardest, and this is the thanks I get?"
                        $ the_person.draw_person(position = "walking_away")
                        "She scoffs and turns around to walk away."
                        mc.name "I haven't dismissed you yet, if you leave there will be further disciplinary actions."
                        the_person "Discipline this!"
                        $ the_person.change_happiness(-10)
                        $ the_person.change_love(-4)
                        $ the_person.change_obedience(-2)
                        "[the_person.title] puts up one hand and gives you the finger over her shoulder, storming out of the room."
                        $ the_person.add_infraction(Infraction.disobedience_factory())
                        return

                    else:
                        $ the_person.draw_person(emotion = "sad")
                        "[the_person.title] seems disheartened and docile, waiting in silence until you finish."
                        "You wait a moment to let your words sink in."
                        mc.name "I'm glad you understand. Now, get back to work and stop wasting my time."
                        $ the_person.change_happiness(-10)
                        $ the_person.change_love(-2)
                        $ the_person.change_obedience(2 + the_person.get_opinion_score("being submissive"))

                    # More obedience, lowers happiness and Love
                    # Low obedience girls or girls who dislike being submissive may mouth back at you, generating a more severe infraction (at the cost of stats to get there though.)

                "Let her go.":
                    mc.name "Do you understand me?"
                    the_person "Yes [the_person.mc_title], I understand."
                    mc.name "Good. Now get back to work, you're wasting everyone's time."


        "Let her go.":
            mc.name "Do you understand me?"
            the_person "Yes, [the_person.mc_title]."
            mc.name "Good. Now get back to work, you've wasted enough time already."

    $ clear_scene()
    return

label punishment_wrist_slap(the_person, the_infraction):
    mc.name "Let's get this over with. Put your hands out, palms down."
    if the_person.obedience < (110 - (15*the_person.get_opinion_score("being submissive"))):
        "[the_person.title] hesitates for a split second before moving her hands out."
    else:
        "[the_person.title] nods and moves her hands."

    "You take her left hand in yours to hold it steady., holding it steady, and give it a fast slap."
    if the_person.obedience < (120 - (15*the_person.get_opinion_score("being submissive"))):
        "[the_person.possessive_title] gasps and instinctively tries to pull her hand away."
        the_person "Ow, that stings..."
    else:
        "[the_person.possessive_title] closes her eyes briefly, but bears her punishment without comment."

    "You switch hands and repeat the process, smacking the back of [the_person.title]'s right hand."
    if the_person.obedience < (120 - (15*the_person.get_opinion_score("being submissive"))):
        the_person "Ouch..."
    elif the_person.get_opinion_score("being submissive") > 0:
        the_person "Ah..."
    else:
        "[the_person.title] doesn't react beyond a short catch in her breath."

    $ the_person.change_obedience(2 + the_person.get_opinion_score("being submissive"))
    $ the_person.change_love(-1 + the_person.get_opinion_score("being submissive"))

    the_person "I'm sorry [the_person.mc_title], it won't happen again."
    menu:
        "Keep going.":
            mc.name "I hope not, or I'll have to find some way to actually get through to you."
            "She tries to gently pull her hand back, but you keep your grip on it."
            "You give it another hard slap across the back, and this time she jumps slightly."
            if the_person.obedience < (120 - (15*the_person.get_opinion_score("being submissive"))):
                the_person "Ach... How many times do you need to do this, exactly?"
                mc.name "Until I think you've learned your lesson."
            else:
                the_person "Oh..."

            "You continue, alternating between hands. After a few strikes the backs of [the_person.title]'s hands are starting to turn red."
            $ the_person.change_obedience(2 + the_person.get_opinion_score("being submissive"))
            $ the_person.change_love(-2 + the_person.get_opinion_score("being submissive"))
            "When you're satisfied you let go of her hands. She holds them, rubbing their backs gingerly."
            mc.name "Have you learned your lesson?"
            the_person "Yes [the_person.mc_title], I have."
            mc.name "Good. I don't enjoy this, but I'll continue to do what is nessesary to maintain good disipline in my staff."
            "She nods obediently."


        "Let her go.":
            "You let go of her hands. She holds them, rubbing their backs gingerly."
            mc.name "It better not, or I won't be so gentle with you."
            $ the_person.change_love(1 + the_person.get_opinion_score("being submissive"))
            if the_person.get_opinion_score("being submissive") > 0:
                the_person "If you need to be rough with me I understand. Sometimes I deserve it."
                the_person "Thank you [the_person.mc_title]."
            else:
                the_person "I understand."

    mc.name "Now get back to work."
    $ clear_scene()
    return

label punishment_serum_test(the_person, the_infraction):
    mc.name "To make up for your disappointing actions, you're going to help the company further it's research goals."
    mc.name "I have a dose of serum here. You're going to take it, so we can observe the effects."
    "[the_person.possessive_title] nods."
    the_person "Alright, hand it over."
    call give_serum(the_person) from _call_give_serum_31
    if _return:
        $ the_person.change_obedience(1)
        "You hand [the_person.title] the small vial. She looks at it for a moment, then removes the stopper at the top and drinks the contents down."
        the_person "Is that all?"
        menu:
            "Make her pay for it." if mandatory_unpaid_serum_testing_policy.is_active():
                mc.name "Not quite. You're going to have to pay for that dose."
                if the_person.obedience >= 130:
                    the_person "Right, of course."
                else:
                    the_person "What? But this was your idea, why do I need to pay?"
                    mc.name "It's already company policy that I can have you test serum whenever I need you to."
                    mc.name "As this is a punishment, you have forfit the right to any special company access. You need to pay for it just like anyone else."
                    "She sighs."
                    the_person "This should be illegal. Fine."
                    $ the_person.change_obedience(1)
                    $ the_person.change_love(-1)
                "[the_person.title] hands over the market value of the dose you gave her."
                $ mc.business.funds += _return.value

            "Make her pay for it.\nRequires Policy: Mandatory Unpaid Serum Testing (disabled)" if not mandatory_unpaid_serum_testing_policy.is_active():
                pass

            "Let her go.":
                pass

        mc.name "That's all for now. I may need to speak with you to record the effects of that dose."
        "She seems slightly nervous, but nods."


    else:
        mc.name "Your punishment will have to wait until later. I don't have the material I need at the moment."
        "She seems slightly apprehensive, but nods."
        $ the_person.add_infraction(the_infraction, add_to_log = False) #The infraction is about to be cleared, we re-add it so the end result is as if this never happened.

    $ clear_scene()
    return

# LEVEL 2 #

init -1 python:
    def punishment_office_busywork_requirement(the_person, the_infraction):
        if the_infraction.severity < 2:
            return "Severity 2"
        elif employee_busywork_role in the_person.special_role:
            return "Already performing office busywork"
        elif employee_humiliating_work_role in the_person.special_role:
            return "Already performing humiliating work"
        else:
            return True

    def punishment_spank_requirement(the_person, the_infraction):
        if not corporal_punishment.is_active():
            return "Requires Policy: Corporal Punishment"
        elif the_infraction.severity < 2:
            return "Severity 2"
        else:
            return True


    def punishment_underwear_only_requirement(the_person, the_infraction):
        if not relaxed_uniform_policy.is_active():
            return "Requires: Relaxed Corporate Uniforms Policy"
        elif the_infraction.severity < 2:
            return "Severity 2"
        elif the_person.event_triggers_dict.get("forced_uniform", False):
            return "Already has a forced uniform" #TODO: Forced uniforms as a concept need some attention in the future.
        elif the_person.outfit.vagina_visible() and the_person.outfit.tits_visible():
            return "Already naked"
        elif the_person.outfit.wearing_panties() and (not the_person.outfit.panties_covered()) and the_person.outfit.wearing_bra() and (not the_person.outfit.bra_covered()):
            return "Already in her underwear"
        else:
            return True

    punishment_office_busywork_action = Action("Office Busywork", punishment_office_busywork_requirement, "punishment_office_busywork")
    punishment_spank_action = Action("Spanking", punishment_spank_requirement, "punishment_spank")
    punishment_underwear_only_action = Action("Underwear only", punishment_underwear_only_requirement, "punishment_underwear_only") #Note: Actually level 2, move it

    list_of_punishments.append(punishment_office_busywork_action)
    list_of_punishments.append(punishment_spank_action)
    list_of_punishments.append(punishment_underwear_only_action)

label punishment_office_busywork(the_person, the_infraction):
    # The employee gains +1 Obedience every work day, but the company loses an extra company efficency.

    mc.name "As punishment, for the next week you are expected to carry out all of the basic busywork of the office."
    mc.name "If the printer needs paper, you fill it. If someone needs coffee, you get it for them."
    "[the_person.title] nods their understanding."
    mc.name "If I don't hear a glowing review from your coworkers by the end of the week there will be further disciplinary action."
    mc.name "Your punishment does not, of course, absolve you of your normal duties."

    $ the_person.add_role(employee_busywork_role)
    $ clear_action = Action("Clear employee busywork", employee_busywork_remove_requirement, "employee_busywork_remove_label", args = the_person, requirement_args = [the_person, day + 7])
    $ mc.business.mandatory_crises_list.append(clear_action)
    return

label punishment_spank(the_person, the_infraction):
    mc.name "I have no choice but to punish you for your infraction. Turn around and put your hands on the desk."
    if the_person.obedience + 10*the_person.get_opinion_score("being submissive") < 120: #She complains
        the_person "What are you going to do?"
        mc.name "You're going to put your hands on the desk, bend forward, and I'm going to spank you."
        the_person "Really? I don't think that's..."
        mc.name "Company policy is clear as day. Would you prefer to see what the punishment is for disobedience?"
        "She hesitates, then sighs and turns around and plants her hands flat on the desk."
        the_person "Fine..."

    else: #She follows instructions rightaway
        "[the_person.title] follows your instructions without any hesitation."
    $ the_person.draw_person(position = "standing_doggy")


    "You stand to the side of [the_person.possessive_title] and place one hand on her hip, ready to spank her with the other."
    #If she has a skirt on, option to pull it up.
    $ top_clothing = the_person.outfit.get_lower_top_layer()
    if top_clothing and top_clothing.can_be_half_off and top_clothing.half_off_gives_access and top_clothing.hide_below and not top_clothing.anchor_below and not top_clothing.underwear:
        menu:
            "Pull up her [top_clothing.display_name] first.":
                if the_person.obedience + 10*the_person.get_opinion_score("being submissive") < 120 and the_person.effective_sluttiness("underwear_nudity") < 30:
                    "You grab the hem of [the_person.title]'s [top_clothing.display_name]."
                    the_person "Hey! what are you doing?"
                    mc.name "Making sure your [top_clothing.display_name] doesn't get in the way of your punishment."
                    the_person "Are... Are you allowed to do that?"
                    if reduced_coverage_uniform_policy.is_active():
                        mc.name "Of course, I have authority over everything you wear."
                    else:
                        mc.name "No clothing is being removed, so yes I can."
                    "You pull her [top_clothing.display_name] up and leave it bunched around her waist."
                else:
                    "You grab the hem of [the_person.title]'s [top_clothing.display_name] and pull it up around her waist."

                $ the_person.draw_animated_removal(top_clothing, position = "standing_doggy", half_off_instead = True)
                if not the_person.outfit.wearing_panties():
                    mc.name "No panties today, I see."

                $ the_person.update_outfit_taboos()

            "Leave her [top_clothing.display_name] in place.":
                pass

    call spank_description(the_person, the_infraction) from _call_spank_description
    $ clear_scene()
    return

label spank_description(the_person, the_infraction):
    "You rub her butt briefly, then slap it hard."
    $ not_cushioned = the_person.outfit.vagina_available() or (the_person.outfit.wearing_panties() and not the_person.outfit.panties_covered())
    if not_cushioned: #ouch!
        "Your hand makes a satisfying smack as it makes contact with her ass cheek. Her ass jiggles for a few moments before settling down."
        the_person "Ah... That really stings..."
    else: #Not too bad.
        "Her clothing absorbs some of the blow, but you still make good contact and set her ass jiggling for a moment."
        the_person "Ah..."

    menu:
        "Go easy on her.":
            "You give her butt a few more smacks, alternating between her left and right cheek, and then step back."
            if the_person.get_opinion_score("being submissive") > 0:
                the_person "Is that all? I thought this would go on longer..."
                $ the_person.outfit.restore_all_clothing()
                $ the_person.draw_person()
                "She seems disappointed as she stands up straight."
            else:
                the_person "Are we done?"
                $ the_person.outfit.restore_all_clothing()
                $ the_person.draw_person()
                "She stands up straight, massaging her butt."
            mc.name "We're done. Get back to work."

            $ the_person.change_obedience(2)
            the_person "Right away."

        "Teach her a lesson.":
            "You keep smacking her butt, putting more force behind your blow each time."
            if not_cushioned: #Ass gets red, she gets sore.
                "Her exposed ass jiggles with each hit, and quickly starts to turn red."
                the_person "Ah... Am I almost done [the_person.mc_title]?"

                if the_person.get_opinion_score("being submissive") > 0: #She likes it and is getting turned on.
                    "You spank her again, and she moans."
                    $ the_person.discover_opinion("being submissive")
                    $ the_person.change_arousal(5*the_person.get_opinion_score("being submissive"))
                    the_person "I... Don't know if I can take much more of this! Mmph..."

                else:
                    "You spank her again, making her gasp."
                    the_person "I... Don't know how much more of this I can take!"

                mc.name "You'll take it until I think you have learned your lesson. Do you understand?"
                "Another smack, another ass jiggle."
                if the_person.get_opinion_score("being submissive") > 0:
                    the_person "Yes [the_person.mc_title]! I understand! Ah!"
                else:
                    "She lowers her head and grits her teeth."

                    the_person "Yes [the_person.mc_title]. Ah..."

                mc.name "Do you have anything to say for your actions?"
                if the_person.get_opinion_score("being submissive") > 0:
                    the_person "It won't happen again [the_person.mc_title], I..."
                    "You interupt her with a slap on the ass. She pauses, then continues."
                    the_person "I'm sorry to let you down, and I see just how wrong I was now! Ah!"

                else:
                    the_person "Ow... It won't happen again [the_person.mc_title], I... Ow!"
                    "You interupt her with a slap on the ass. She takes a moment to collect herself before continuing."
                    the_person "I promise it won't happen again!"

                "You give her one last hit on her now red butt and then step back, letting her stand up."
                $ the_person.outfit.restore_all_clothing()
                $ the_person.draw_person()
                if the_person.get_opinion_score("being submissive") > 0:
                    $ the_person.change_arousal(5*the_person.get_opinion_score("being submissive"))
                    $ the_person.change_obedience(the_person.get_opinion_score("being submissive"))
                    the_person "Thank you [the_person.mc_title]. I promise I'll do better."
                else:
                    $ the_person.change_obedience(3)
                    $ the_person.change_love(-2 + the_person.get_opinion_score("being submissive"))
                    the_person "Finally. Ow..."
                mc.name "I expect you've learned your lesson. Now get back to work, you've wasted enough time already."

            else: #Doesn't particularly mind."
                "[the_person.title] jerks forward with each strike, but her [top_clothing.display_name] seems to be saving her from the worst of it."
                the_person "Ah... Ow..."
                "After a few more strikes it's clear you aren't having the effect on [the_person.possessive_title] that you were hoping for."
                "You give her one last slap on the ass and step back."
                mc.name "Stand up, we're done here."
                $ the_person.outfit.restore_all_clothing()
                $ the_person.draw_person()
                "She turns around, rubbing her butt."
                the_person "I'll get back to work..."
                $ the_person.change_love(-1)
                $ the_person.change_obedience(2)
    return

label punishment_underwear_only(the_person, the_infraction):
    mc.name "You've let me down [the_person.title], and more importantly you've let down the entire company."
    mc.name "Strip down to your underwear."
    if the_person.should_wear_uniform():
        mc.name "You don't deserve to wear your uniform, so for the rest of today you won't."
    else:
        mc.name "You can consider that your official uniform for the day."

    if not (the_person.outfit.wearing_bra() and the_person.outfit.wearing_panties()): # Whoops, not wearing underwear today! Tough luck.
        the_person "I... I can't do that [the_person.mc_title]."
        mc.name "What do you mean you can't? These are the rules you agreed with to work here, if you..."
        "She shakes her head and interupts you."
        $ slut_continue_requirement = 40
        if not (the_person.outfit.wearing_bra() or the_person.outfit.wearing_panties()):
            the_person "No, I mean I can't strip down to my underwear because... I'm not wearing any."
            $ slut_continue_requirement = 60
            $ slut_continue_requirement += -(5*the_person.get_opinion_score("not wearing anything"))

        elif not the_person.outfit.wearing_bra():
            the_person "No, I mean I can't strip down to my underwear because... I'm not wearing a bra."
            the_person "My... breasts would be out."
            $ slut_continue_requirement += -(5*the_person.get_opinion_score("showing her tits"))

        else: #not wearing panties
            the_person "No, I mean I can't strip down to my underwear because... I'm not wearing any panties."
            $ slut_continue_requirement += -(5*the_person.get_opinion_score("showing her ass"))

        "You consider this for a moment, then shrug."
        mc.name "That's unfortunate, but your inability to wear a decent outfit doesn't absolve you of your punishment."
        the_person "So you still want me to..."
        mc.name "Strip. Now."

        if the_person.effective_sluttiness() < slut_continue_requirement:
            # She's not slutty enough to do it, she'll defy you and accept a disobedience infraction instead.
            "[the_person.possessive_title] shuffles nervously."
            the_person "I don't think I can do it. I'm sorry [the_person.mc_title]."
            mc.name "If you're refusing the only choice I have is to write you up for disobedience, which will carry an even heavier penalty."
            $ the_person.change_happiness(-5)
            $ the_person.change_obedience(-1)
            the_person "I'm sorry, but I just can't do it. I'll accept a worse punishment if I have to."
            $ the_person.add_infraction(Infraction.disobedience_factory())
            mc.name "Fine, we'll do it your way."
            $ clear_scene()
            return
        else:
            $ the_person.change_happiness(-5)
            $ the_person.change_obedience(2 + the_person.get_opinion_score("being submissive"))
            "Your words seem to shock her into action."

    elif the_person.obedience < (130 - (10*the_person.get_opinion_score("being submissive"))): # She's not very obedient
        if the_person.effective_sluttiness("underwear_nudity") < 40:
            $ the_person.draw_person(emotion = "angry")
            the_person "You... You can't make me do that!"
            if reduced_coverage_uniform_policy.is_active():
                mc.name "Of course I can, it's company policy. I could even tell you what underwear to wear if I wanted, but I'm keeping this simple."
            else:
                mc.name "Of course I can. It's company policy that I set the uniform you have to wear, and I'm telling you that it's nothing over your underwear."
                mc.name "You have the freedom to wear any style of underwear you like, or none at all, under your uniform. I hope you've dressed appropriately today."

            mc.name "You lost any right to complain when you failed to follow company policy in the first place."
            the_person "But... It's not..."
            mc.name "Strip. Now."
            "[the_person.possessive_title] glares at you, and for a moment you think she is going to refuse."
            the_person "Fine."
            $ the_person.change_obedience(1 + the_person.get_opinion_score("being submissive"))
        else: #Not obedient, but slutty enough to not care
            "[the_person.title] seems to relax a little."
            the_person "Okay, I understand."
    else:
        if the_person.effective_sluttiness("underwear_nudity") < 40:
            # Obedient but very shy about it
            "She blushes and looks away."
            the_person "Are you sure [the_person.mc_title]? I'm not use to... being undressed in front of people."
            mc.name "Of course I'm sure. Now strip."
            "She nods meekly."
            the_person "Okay, if you say I have to..."

        else:
            # Obedient and slutty, the perfect combination
            "[the_person.title] nods obediently."
            the_person "Yes [the_person.mc_title], I'll go change into my new uniform."
            mc.name "You'll change right here. Now strip."
            the_person "Of course. Right away."

    $ generalised_strip_description(the_person, the_person.outfit.get_underwear_strip_list())
    if the_person.update_outfit_taboos() or the_person.effective_sluttiness() < 40:
        "[the_person.possessive_title] blushes and tries to cover her body."
        the_person "This is so embarrassing..."
    $ slut_change = 0
    if the_person.outfit.tits_visible():
        $ slut_change += the_person.get_opinion_score("showing her tits")
    if the_person.outfit.vagina_visible():
        $ slut_change += the_person.get_opinion_score("showing her ass")
    if the_person.outfit.tits_visible() and the_person.outfit.vagina_visible():
        $ slut_change += the_person.get_opinion_score("not wearing anything")
    $ the_person.change_slut_temp(slut_change)

    mc.name "I expect you to stay in your new uniform for the rest of the week. Any deviation from it and there will be further punishments."
    mc.name "Understood?"
    the_person "Yes, [the_person.mc_title]."
    mc.name "Good. We're done here."
    $ the_person.event_triggers_dict["forced_uniform"] = the_person.outfit.get_copy()
    $ clear_scene()
    return

# LEVEL 3 #

init -1 python:
    def punishment_pay_cut_requirement(the_person, the_infraction):
        if the_infraction.severity < 3:
            return "Severity 3"
        elif the_person.salary <= 0:
            return "Requires: Paid Position"
        else:
            return True

    def punishment_strip_and_spank_requirement(the_person, the_infraction):
        if the_infraction.severity < 3:
            return "Severity 3"
        elif not corporal_punishment.is_active():
            return "Requires Policy: Corporal Punishment"
        else:
            return True

    def punishment_office_nudity_requirement(the_person, the_infraction):
        if the_infraction.severity < 3:
            return "Severity 3"
        elif not reduced_coverage_uniform_policy.is_active():
            return "Requires Policy: Reduced Coverage Corporate Uniforms"
        elif the_person.event_triggers_dict.get("forced_uniform", False):
            return "Already has a forced uniform" #TODO: Forced uniforms as a concept need some attention in the future.
        else:
            return True


    punishment_pay_cut_action = Action("Pay cut", punishment_pay_cut_requirement, "punishment_pay_cut")
    punishment_strip_and_spank_action = Action("Strip and Spank", punishment_strip_and_spank_requirement, "punishment_strip_and_spank")
    punishment_office_nudity_action = Action("Mandatory Nudity", punishment_office_nudity_requirement, "punishment_office_nudity")

    list_of_punishments.append(punishment_pay_cut_action)
    list_of_punishments.append(punishment_strip_and_spank_action)
    list_of_punishments.append(punishment_office_nudity_action)


label punishment_pay_cut(the_person, the_infraction): #There is a similar option in the performance review, but this doens't have a chance for her to quit and has reduced happiness penalties.
    mc.name "As punishment for your rules infraction I will be cutting your pay."
    the_person "By how much?"
    python:
        minor_amount = int(0.05 * the_person.salary)
        mod_amount = int(0.15 * the_person.salary)
        maj_amount = int(0.25 * the_person.salary)
        if minor_amount <= 1:
            minor_amount = 1
        if mod_amount <= 3:
            mod_amount = 3
        if maj_amount <= 5:
            maj_amount = 5
        # Cap the reduction so we can't end up with a negative salary (Although this would be an interesting extra punishment!
        if minor_amount >= the_person.salary:
            minor_amount = the_person.salary
        if mod_amount >= the_person.salary:
            mod_amount = the_person.salary
        if maj_amount >= the_person.salary:
            maj_amount = the_person.salary

    menu:
        "Minor cut (-$[minor_amount]/day)":
            mc.name "I'm going to be generous. Your pay will only be cut by $[minor_amount] per day."
            $ the_person.change_salary(-minor_amount)
            $ the_person.change_happiness(-2)
            $ the_person.change_obedience(1)
            $ the_person.draw_person(emotion = "sad")
            "[the_person.possessive_title] seems upset by the news, but she nods her understanding."
            mc.name "Good. Now get back to work."

        "Moderate cut (-$[mod_amount]/day)":
            mc.name "You will see a $[mod_amount] reduction in your daily pay, effective immediately."
            $ the_person.change_salary(-mod_amount)
            $ the_person.change_happiness(-5)
            $ the_person.change_obedience(2)
            $ the_person.draw_person(emotion = "sad")
            if the_person.obedience + 10*the_person.get_opinion_score("being submissive") < 125:
                "[the_person.possessive_title] seems upset by the news, but she nods obediently."
                the_person "Of course. Thank you [the_person.mc_title], for being so understanding."
            else:
                the_person "I... Is there anything else I can do to make it up? That's a big cut."
                mc.name "If you impress me with your performance maybe you'll earn a raise."
                "She seems uncertain, but nods."
            mc.name "Good, now get back to work before I have to write you up again."


        "Major cut (-$[maj_amount]/day)":
            mc.name "There will be a $[maj_amount] cut to your daily pay, effective immediately."
            $ the_person.change_salary(-maj_amount)
            $ the_person.change_happiness(-10)
            $ the_person.change_obedience(3)
            $ the_person.draw_person(emotion = "sad")
            if the_person.obedience + 10*the_person.get_opinion_score("being submissive") < 125:
                "[the_person.possessive_title] seems shocked for a moment, but finally nods obediently."
                the_person "I... I understand. I'm sorry for letting you down like this [the_person.mc_title]..."
                mc.name "Don't let it happen again. Now get back to work."
                the_person "Right away."
            else:
                "[the_person.possessive_title] seems shocked for a moment before responding."
                the_person "Are you sure? That seems like a very big change."
                mc.name "Well, I need to make sure you've learned your lesson."
                mc.name "If you are unhappy with your pay you're welcome to quit."
                "She shakes her head."
                the_person "No, I don't want to do that. I... I understand."
                mc.name "Good, now don't let it happen again. Now get back to work."
                the_person "Right away, [the_person.mc_title]."

    $ clear_scene()
    return

label punishment_strip_and_spank(the_person, the_infraction):
    mc.name "It's time for your disciplinary punishment [the_person.title]."
    the_person "What are you going to do?"
    mc.name "I'm going to bend you over and spank you, until you've learned your lesson."

    if not (the_person.outfit.vagina_available() or the_person.outfit.tits_available() or the_person.outfit.vagina_visible() or the_person.outfit.tits_visible()): #She's wearing something, let's strip her down.
        mc.name "But first we need to ensure there's nothing that will get in my way. Strip naked."
        call strip_naked_command_helper(the_person, the_infraction) from _call_strip_naked_command_helper
        $ remove_shoes = _return
        $ strip_list = the_person.outfit.get_full_strip_list(strip_feet = remove_shoes)
        $ generalised_strip_description(the_person, strip_list)
        if the_person.update_outfit_taboos(): #Being nude has broken a taboo
            "[the_person.title] stands meekly in front of you, completely nude. She tries to cover herself up with her hands."
            mc.name "Hands down, there's no point hiding anything from me now."
            "She frowns, but follows your instructions. She lowers her hands to her sides, letting you get a good view of her body."
        mc.name "Good girl. Now put your hands on the desk, bend over, and stick your ass out for your punishment."

    else: #Already basically nude.
        mc.name "You're already dressed for the occasion, so let's get right to it."
        mc.name "Hands on the desk, bend over, and stick your ass out for your punishment."

    $ the_person.draw_person(position = "standing_doggy")
    call spank_description(the_person, the_infraction) from _call_spank_description_1
    $ clear_scene()
    return

label punishment_office_nudity(the_person, the_infraction):
    mc.name "I have decided on a suitable punishment for your violation of company rules."
    mc.name "You're going to spend the rest of the week working while nude."
    if not (the_person.outfit.tits_available() and the_person.outfit.vagina_available() and the_person.outfit.tits_visible() and the_person.outfit.vagina_available()): #Something to strip
        mc.name "Let's start by having you strip down."
        call strip_naked_command_helper(the_person, the_infraction) from _call_strip_naked_command_helper_1
        $ remove_shoes = _return
        $ strip_list = the_person.outfit.get_full_strip_list(strip_feet = remove_shoes)
        $ generalised_strip_description(the_person, strip_list)

        if the_person.update_outfit_taboos(): # Broke a taboo
            "[the_person.title] stands meekly in front of you, completely nude. She tries to cover herself up with her hands."
            mc.name "Hands down, there's no point hiding anything from me now."
            "She frowns, but follows your instructions. She lowers her hands to her sides, letting you get a good view of her body."

        mc.name "Good. Now I want you to consider this your uniform for the rest of the week."

    else:
        mc.name "You're already un-dressed for the occasion, consider this your uniform for the rest of the week."

    $ the_person.event_triggers_dict["forced_uniform"] = the_person.outfit.get_copy()
    $ slut_change = 0
    if the_person.outfit.tits_visible():
        $ slut_change += the_person.get_opinion_score("showing her tits")
    if the_person.outfit.vagina_visible():
        $ slut_change += the_person.get_opinion_score("showing her ass")
    if the_person.outfit.tits_visible() and the_person.outfit.vagina_visible():
        $ slut_change += the_person.get_opinion_score("not wearing anything")
    $ the_person.change_slut_temp(slut_change)
    mc.name "If I find you attempting to wear anything else there will have to be further punishments."
    mc.name "Understood?"
    the_person "Yes [the_person.mc_title], I understand."
    mc.name "Good, now get back to work."
    return

label strip_naked_command_helper(the_person, the_infraction): #Helper function for events that need a girl to strip naked.
    $ remove_shoes = False
    if the_person.obedience + 10*the_person.get_opinion_score("being submissive") < 125 and the_person.effective_sluttiness(["bare_tits", "bare_pussy"]) < 60:
        # not obedient or slutty enough to do it without comment.
        "[the_person.title] hesitates and looks away."
        the_person "Isn't there something else I could do? Do you really need me to be naked?"
        mc.name "I've made my decision. Get naked, or your punishment will only be worse."
        "She sighs and nods."
        the_person "Yes [the_person.mc_title]."

        $ feet_ordered = the_person.outfit.get_feet_ordered()
        if feet_ordered:
            $ top_feet = feet_ordered[-1]
            the_person "Can I keep my [top_feet.display_name] on?"
            menu:
                "Strip it all off.":
                    mc.name "Take it all off, I don't want you to be wearing anything."
                    $ remove_shoes = True

                "Leave them on.":
                    mc.name "Fine, you can leave them on."

    else: # No big deal, she just gets right to it
        "She nods and starts to strip immediately."
        $ feet_ordered = the_person.outfit.get_feet_ordered()
        if feet_ordered:
            $ top_feet = feet_ordered[-1]
            the_person "Would you like me to take off my [top_feet.display_name] too?"
            menu:
                "Strip it all off.":
                    mc.name "Take it all off, I want you naked."
                    $ remove_shoes = True

                "Leave them on.":
                    mc.name "Fine, you can leave them on."

    return remove_shoes

# LEVEL 4 #
init -1 python:
    def punishment_office_humiliating_work_requirement(the_person, the_infraction):
        if the_infraction.severity < 4:
            return "Severity 4"
        elif employee_busywork_role in the_person.special_role:
            return "Already performing office busywork"
        elif employee_humiliating_work_role in the_person.special_role:
            return "Already performing humiliating work"
        else:
            return True

    def punishment_orgasm_denial_requirement(the_person, the_infraction):
        if the_infraction.severity < 4:
            return "Severity 4"
        elif not corporal_punishment.is_active():
            return "Requires Policy: Corporal Punishment"
        else:
            return True

    def punishment_forced_punishment_outfit_requirement(the_person, the_infraction):
        if the_infraction.severity < 4:
            return "Severity 4"
        elif not reduced_coverage_uniform_policy.is_active():
            return "Requires Policy: Reduced Coverage Corporate Uniforms"
        elif the_person.event_triggers_dict.get("forced_uniform", False):
            return "Already has a forced uniform" #TODO: Forced uniforms as a concept need some attention in the future.
        else:
            return True

    punishment_office_humiliating_work_action = Action("Humiliating Office Work", punishment_office_humiliating_work_requirement, "punishment_office_humiliating_work")
    punishment_orgasm_denial_action = Action("Orgasm Denial", punishment_orgasm_denial_requirement, "punishment_orgasm_denial")
    punishment_forced_punishment_outfit_action = Action("Punishment Outfit", punishment_forced_punishment_outfit_requirement, "punishment_forced_punishment_outfit")

    list_of_punishments.append(punishment_office_humiliating_work_action)
    list_of_punishments.append(punishment_orgasm_denial_action)
    list_of_punishments.append(punishment_forced_punishment_outfit_action)

label punishment_office_humiliating_work(the_person, the_infraction):
    mc.name "As punishment for your flagrant disregard of company policy you responsible for the cleaning of this office for the next week."
    mc.name "Contact the cleaning agency for the building and inform them they will not be needed."
    if the_person.int >= 3 and the_person.obedience + 10*the_person.get_opinion_score("being submissive") < 120: #She went to university, she doesn't want to scrub toilets!
        the_person "You... expect me to clean up after everyone in here?"
        mc.name "I do. I expect you to be scrubbing scrubbing toilets, washing floors, and taking out the garbage."
        the_person "I have a degree! This is just a complete waste of my time!"
        mc.name "I hope you'll learn some humility during your punishment. Of course, I also expect you to keep up with your normal work."
        the_person "I don't know how you can expect that [the_person.mc_title], there aren't enough hours in the day!"
        mc.name "You better figure it out, or there will be further punishments when you're done."
        mc.name "Maybe you'll think about this next time you think about ignoring company rules."
        "[the_person.title] is about to respond, but you wave your hand and cut her off."
        mc.name "There's nothing to discuss here, I've made my decision. Call the cleaning company and get back to work."
        the_person "I... Fine. Right away, [the_person.mc_title]."
    else:
        mc.name "I expect you to be scrubbing scrubbing toilets, washing floors, and taking out the garbage."
        the_person "Understood [the_person.mc_title]."
        mc.name "Of course, I expect you to keep up with your normal responsibilities as well."
        the_person "I'll do my best, [the_person.mc_title]."
        mc.name "Good. If I find there have been performance issues there will have to be further disciplinary action."
        "She nods her understanding."
        mc.name "We're done here, you can get back to work."
        the_person "Right away, [the_person.mc_title]."

    $ the_person.add_role(employee_humiliating_work_role)
    $ clear_action = Action("Clear employee busywork", employee_humiliating_work_role, "employee_humiliating_work_remove_requirement", args = the_person, requirement_args = [the_person, day + 7])
    $ mc.business.mandatory_crises_list.append(clear_action)
    return

label punishment_orgasm_denial(the_person, the_infraction):
    mc.name "It's time for your punishment [the_person.title]."
    the_person "What are you going to do?"
    mc.name "We'll get to that. First, I need you to strip down."
    call strip_naked_command_helper(the_person, the_infraction) from _call_strip_naked_command_helper_2
    $ remove_shoes = _return
    $ strip_list = the_person.outfit.get_full_strip_list(strip_feet = remove_shoes)
    $ generalised_strip_description(the_person, strip_list)

    if the_person.update_outfit_taboos(): # Broke a taboo
        "[the_person.title] stands meekly in front of you, completely nude. She tries to cover herself up with her hands."
        mc.name "Hands down, there's no point hiding anything from me now."
        "She frowns, but follows your instructions. She lowers her hands to her sides, letting you get a good view of her body."

    mc.name "Good, now we can get started."
    "You step close to [the_person.possessive_title] and cup one of her breasts, squeezing it softly."
    mc.name "You've really disappointed me [the_person.title], so in return..."
    "You place your other hand on her hip."
    mc.name "...I'm going to disappoint you. I'm going to bring you right to the edge of cumming and leave you there."
    if the_person.effective_sluttiness() < 40:
        the_person "You can't... You aren't allowed to do that, are you?"
        "You slide your hand from her hip down to her inner thigh."
        mc.name "Of course I can, punishments are all listed in the employee manual. Of course, if you'd prefer to quit I can walk you to the door."
        if reduced_coverage_uniform_policy.is_active():
            mc.name "Your clothing is company property though, so you'd be walking out of that door naked."
        "She stands frozen in place as you caress her body. She finally mutters out her answer."
        the_person "I'll take my punishment, [the_person.mc_title]... I doubt you'll even get me close."
        mc.name "Good girl. I won't make you wait any longer..."
    elif the_person.effective_sluttiness() < 80:
        the_person "Okay [the_person.mc_title], I'll take my punishment."
        "You slide your hand from her hip down to her inner thigh."
        mc.name "Good girl."
    else:

        the_person "You wouldn't be that cruel, would you [the_person.mc_title]?"
        the_person "Come on, wouldn't it be better if we both enjoyed ourselves?"
        mc.name "I fully intend to enjoy myself with you, but you aren't going to get to cum."
        "[the_person.possessive_title] pouts while you slide your hand from her hip down to her inner thigh."
        mc.name "So be a good girl and take your punishment."

    "You move behind [the_person.possessive_title], keeping one hand between her legs and the other massaging a tit."
    $ the_person.break_taboo("touching_body")
    $ the_person.add_situational_obedience("punishment", 20, "I'm being punished, I don't have any right to refuse.")
    call fuck_person(the_person, private = False, start_position = standing_grope, start_object = mc.location.objects_with_trait("Stand")[0], skip_intro = True, affair_ask_after = False) from _call_fuck_person_92
    $ report = _return
    $ the_person.clear_situational_obedience("punishment")

    if report.get("girl orgasms", 0) == 0: #Successfully didn't let her orgasm.
        if report.get("end arousal", 0) >= 95 : # Got her very close
            the_person "No [the_person.mc_title], you can't... You can't leave me like this!"
            "She moans desperately."
            if the_person.wants_creampie():
                the_person "Please, just fuck me and make me cum! You can cum inside of me, I don't care!"
                the_person "I need it!"
                $ the_person.add_situational_slut("orgasm denial", 20, "I was so close! I need to cum, I need to!")
                menu:
                    "Fuck her.":
                        mc.name "Beg for it."
                        the_person "Please, I... I want you to fuck me! Fuck me and cum inside me, I want it!"
                        the_person "Put that cock in me before I go crazy!"
                        call fuck_person(the_person, private = False, affair_ask_after = False) from _call_fuck_person_93
                        $ report = _return
                        if report.get("girl orgasms", 0) > 0:
                            mc.name "I hope that satisfied you."
                            the_person "It was everything I needed it to be. Ah..."
                            $ the_person.change_slut_temp(2)
                            $ the_person.change_obedience(1)
                            mc.name "Good, now get back to work."
                            the_person "Yes [the_person.mc_title], right away."
                        else:
                            the_person "No, no, no, you can't... Not again!"
                            mc.name "Sorry [the_person.title], but you need to learn your lesson."
                            the_person "Fuck... I'm so horny, I can't think straight!"
                            mc.name "If I catch you trying to pleasure yourself, or having someone else do it for you, there will be further punishments."
                            mc.name "Do you understand?"
                            $ the_person.change_happiness(-5)
                            $ the_person.change_obedience(4)
                            the_person "I understand [the_person.mc_title]..."
                            mc.name "Good, now get back to work."

                    "Ignore her pleas.":
                        mc.name "Need it or not, this is your punishment."
                        mc.name "If I catch you trying to pleasure yourself, or having someone else do it for you, there will be further punishments."
                        mc.name "Do you understand me?"
                        the_person "I... Oh fuck, fine. I understand."
                        $ the_person.change_happiness(-5)
                        $ the_person.change_obedience(4)
                        mc.name "Good, now get back to work."
                        the_person "Yes [the_person.mc_title]."

            else:
                mc.name "I can, and I am. If I catch you trying to pleasure yourself, or having someone else do it for you, there will be further punishments."
                mc.name "Do you understand?"
                the_person "I understand [the_person.mc_title]..."
                mc.name "Good. Now get back to work, you've wasted enough of our time."
                the_person "Yes [the_person.mc_title]."


        elif report.get("end arousal", 0) >= 80: # Reasonably high
            the_person "God, I was getting close... Fuck."
            "She groans unhappily."
            mc.name "Good, that's the point. If I catch you trying to pleasure yourself, or having someone else do it for you, there will be further punishments."
            the_person "I understand... God this is going to be hard!"
            $ the_person.change_happiness(-5)
            $ the_person.change_obedience(3)
            mc.name "Get back to work, It'll take your mind off of it."
            the_person "Yes [the_person.mc_title]."


        elif report.get("end arousal", 0) >= 50: # At least you tried
            the_person "Ah... Ah..."
            mc.name "If I catch you trying to pleasure yourself, or having someone else do it for you, there will be further punishments."
            the_person "Right, I understand [the_person.mc_title]."
            $ the_person.change_happiness(-5)
            $ the_person.change_obedience(2)
            mc.name "Good, now get back to work."
            the_person "Yes [the_person.mc_title]."

        else: #You didn't even try
            the_person "So, are we done?"
            mc.name "We are, and if I catch you trying to pleasure yourself, or having someone else do it for you, there will be further punishments."
            the_person "I understand, but I think I'll be able to manage."
            $ the_person.change_obedience(1)
            mc.name "Get back to work, you've wasted enough time already."
            the_person "Yes [the_person.mc_title]."

    else: #You let her cum. Woops.
        the_person "Ah, that was nice..."
        mc.name "It wasn't suppose to be nice, it was suppose to be a punishment."
        the_person "Do you want to punish me some more?"
        $ the_person.change_slut_temp(3)
        $ the_person.change_obedience(-3)
        "You sigh and give up."
        mc.name "Get back to work, or I'll come up with something more unpleasant."
        the_person "Yes [the_person.mc_title]."

    $ clear_scene()
    return

label punishment_forced_punishment_outfit(the_person, the_infraction):
    #TODO: In the future some clothing items should only be possible through this (and other) special events
    mc.name "I've decided on a suitable punishment for your violation of company rules."
    if not (the_person.outfit.tits_available() and the_person.outfit.vagina_available() and the_person.outfit.tits_visible() and the_person.outfit.vagina_available()): #Something to strip
        mc.name "Let's start by having you strip down."

        call strip_naked_command_helper(the_person, the_infraction) from _call_strip_naked_command_helper_3
        $ remove_shoes = _return
        $ strip_list = the_person.outfit.get_full_strip_list(strip_feet = remove_shoes)
        $ generalised_strip_description(the_person, strip_list)

        if the_person.update_outfit_taboos(): # Broke a taboo
            "[the_person.title] stands meekly in front of you, completely nude. She tries to cover herself up with her hands."
            mc.name "Hands down, there's no point hiding anything from me now."
            "She frowns, but follows your instructions. She lowers her hands to her sides, letting you get a good view of her body."
        the_person "What now, [the_person.mc_title]?"
    else:
        the_person "What is it going to be, [the_person.mc_title]?"

    mc.name "I've put together a special outfit for you. It will be your outfit for the rest of the week."
    call outfit_master_manager() from _call_outfit_master_manager_9
    $ the_outfit = _return
    if the_outfit is None:
        "You consider what to dress [the_person.possessive_title] for a moment, then shrug."
        mc.name "On second thought, I think wearing nothing at all suits a disobedient slut like you."
        mc.name "Consider this your uniform for the rest of the week. Do you understand?"
        $ the_person.set_uniform(the_person.outfit, wear_now = True)

    else:
        "You collect the clothing from a stash in your office and hand it over to [the_person.title]."
        mc.name "Get changed."
        "She nods obediently."
        $ the_person.set_uniform(the_outfit, wear_now = True)
        $ the_person.draw_person()
        "You watch as she gets changed. When [the_person.possessive_title] is finished she stands in front of you."

        if the_person.effective_sluttiness() < the_person.outfit.slut_requirement:
            the_person "Is this it? This is so embarassing..."

    $ the_person.event_triggers_dict["forced_uniform"] = the_person.outfit.get_copy()
    $ slut_change = 0
    if the_person.outfit.tits_visible():
        $ slut_change += the_person.get_opinion_score("showing her tits")
    if the_person.outfit.vagina_visible():
        $ slut_change += the_person.get_opinion_score("showing her ass")
    if the_person.outfit.tits_visible() and the_person.outfit.vagina_visible():
        $ slut_change += the_person.get_opinion_score("not wearing anything")
    $ the_person.change_slut_temp(slut_change)
    mc.name "If I find you attempting to wear anything else there will have to be further punishments."
    mc.name "Understood?"
    the_person "Yes [the_person.mc_title], I understand."
    mc.name "Good, now get back to work."

    $ clear_scene()
    return


# LEVEL 5 #
init -1 python:
    def punishment_unpaid_intern_requirement(the_person, the_infraction):
        if the_infraction.severity < 5:
            return "Severity 5"
        elif the_person.salary < 0:
            return "Requires: Paid Position"
        else:
            return True

    def punishment_freeuse_slut_requirement(the_person, the_infraction):
        if the_infraction.severity < 5:
            return "Severity 5"
        elif the_person.has_role(employee_freeuse_role):
            return "Already a freeuse slut"
        elif not corporal_punishment.is_active():
            return "Requires Policy: Corporal Punishment"
        else:
            return True

    punishment_unpaid_intern_action = Action("Unpaid Internship", punishment_unpaid_intern_requirement, "punishment_unpaid_intern")
    punishment_orgasm_denial_action = Action("Freeuse Office Slut", punishment_freeuse_slut_requirement, "punishment_office_freeuse_slut")

    list_of_punishments.append(punishment_unpaid_intern_action)
    list_of_punishments.append(punishment_orgasm_denial_action)


label punishment_unpaid_intern(the_person, the_infraction):
    mc.name "Because of your actions, I have no choice but to slash your salary."
    the_person "Slash how badly?"
    mc.name "Completely. Right down to zero. From now on you will be working as an unpaid intern."
    $ the_person.draw_person(emotion = "sad")
    if the_person.obedience < 150:
        $ the_person.change_happiness(-20)
        $ the_person.change_love(-5)
        the_person "You can't do that, how am I going to live?"
        mc.name "I can, and I am. I could fire you if I wanted to, but I want to give you the chance to redeem yourself."
        mc.name "You're welcome to quit, but with this on your record, well..."
        mc.name "You may have a hard time finding future employement without my reference."
        "[the_person.title] stands still for a moment, completely stunned."
        the_person "That's blackmail, there's no way this is legal."
        mc.name "You could hire a lawyer, but you should probably be a little more responable with your finances."
        mc.name "If you work hard enough maybe you'll earn yourself a promotion to a paying position again."
        $ the_person.change_obedience(5)
        "[the_person.possessive_title] seems speechless."
        mc.name "I'll give you some time to process all of this. Your updated employee contract will be in the mail."

    else:
        $ the_person.change_happiness(-10)
        $ the_person.change_obedience(1)
        "[the_person.title] looks devastated, but after a moment of shock she nods."
        the_person "Right, I understand. Do you need anything else?"
        mc.name "You're taking this well..."
        the_person "You've made your decision, that's all I need to know [the_person.mc_title]."
        mc.name "Good, I'm glad to hear such dedication from you. Keep it up and I'm sure you'll earn a promotion."
        the_person "Thank you [the_person.mc_title], I'll try."


    "You leave [the_person.title] to consider her new position in the company."
    $ the_person.change_salary(-the_person.salary) #You get nothing! Good day sir!
    $ clear_scene()
    return

label punishment_office_freeuse_slut(the_person, the_infraction):
    mc.name "It is time for your punishment to begin."
    the_person "What is it going to be, [the_person.mc_title]?"
    mc.name "Obviously, I could fire you, but I hope that your disobedience can be corrected instead."
    mc.name "This next week is going to be an exercise in obedience, because your body is going to be company property."
    mc.name "And I'm going to make sure you're well used by the end of your punishment."
    if the_person.effective_sluttiness() + (10*the_person.get_opinion_score("being submissive")) < 40: #Not very slutty, needs it explained
        if the_person.obedience < 140: # Not obedient enough to let it happen without complaining.
            the_person "I don't understand, what does that even mean? I already have to show up to work, what else can I do?"
            mc.name "That's cute. Let me demonstrate what I mean."
            if the_person.has_large_tits():
                "You reach out and grab one of [the_person.title]'s hefty breasts."
            else:
                "You reach out and grab at one of [the_person.title]'s tits."
            mc.name "These tits are what I'm interested in, along with the rest of you."
            the_person "[the_person.mc_title]! I can't... You don't really expect me to just take this, do you?"
            mc.name "I do. All of the punishments are laid out in the employee manual. I suggest you read through it at some point."
            mc.name "You're welcom to quit, but you might have a hard time finding future employment without a positive reference."
            "You play with her tits while she stands still, frozen by indecision."
            "She finally sighs and lowers her head."
            the_person "Just for a week... Fine."

        else: # Not slutty, but obedient enough to let it happen. Nun style answers
            the_person "I can show up for work earlier, if that's what you mean."
            mc.name "That's cute, but that's not what I mean. Let me demonstrate."
            if the_person.has_large_tits():
                "You reach out and grab one of [the_person.title]'s hefty breasts."
            else:
                "You reach out and grab at one of [the_person.title]'s tits."
            mc.name "These tits are what I'm interested in, along with the rest of you."
            the_person "Oh... I think I understand now."

    elif the_person.effective_sluttiness() + (10*the_person.get_opinion_score("being submissive")) < 80: #Moderately slutty, assumes you mean things like handjobs at first
        if the_person.obedience < 140:
            the_person "I think I can see where this is going. You want me to act all sexy around the office to keep you entertained."
            mc.name "That's cute, but not quite what I mean."
            if the_person.has_large_tits():
                "You reach out and grab one of [the_person.title]'s hefty breasts."
            else:
                "You reach out and grab at one of [the_person.title]'s tits."
            mc.name "You aren't going to just be teasing the office, you're going to have to put out."
        else: # Slightly shocked when you tell her she'll have to go "all the way", but that's all
            the_person "I understand [the_person.mc_title]. I will be yours to use, whenever you want me."
            mc.name "Good, I'm glad you've understood so quickly."

    else: #Very slutty, excited by the idea of being used.
        if the_person.obedience < 140: # Eager slut answer
            the_person "You're going to fuck me, [the_person.mc_title]? All week long?"
            "She doesn't seem very upset by the idea."
            the_person "I understand, if that's my punishment I accept it."
        else: # Obedient fuck slut answer
            the_person "Yes [the_person.mc_title]. My holes are yours to fuck whenever you want."
            the_person "I'll be your fuck slut to make up for my mistakes, and I promise to do better."

    mc.name "For the rest of the week you are to make yourself available to myself, all other employees, and visitors, during business hours."
    mc.name "Nothing is off limits, and it would be easier for everyone involved if you wore something with easy access."
    mc.name "Do you understand?"
    "She nods obediently."
    mc.name "Good."
    $ the_person.add_role(employee_freeuse_role)
    $ clear_action = Action("Clear employee freeuse", employee_freeuse_remove_requirement, "employee_freeuse_remove_label", args = the_person, requirement_args = [the_person, day + 7])
    $ mc.business.mandatory_crises_list.append(clear_action)
    return

label punishment_gag_her(the_person, the_infraction):
    #Gag her, but also have the option to strip her down.
    #TOOD: We need to get all of our gag mecahnics working before we can implement this.
    return
