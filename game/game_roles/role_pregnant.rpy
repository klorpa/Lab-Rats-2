# Contains all of the information related to characters being pregnant.

init -1 python:
    def preg_announce_requirement(the_person, start_day):
        if day >= start_day:
            return True

    def preg_transform_requirement(the_person):
        if day >= the_person.event_triggers_dict.get("preg_transform_day", 0):
            return True
        return False

    def preg_tits_requirement(the_person):
        if day >= the_person.event_triggers_dict.get("preg_tits_date", 0):
            return True

        return False

    def pregnant_tits_annouce_requirement(the_person):
        return True

    def become_pregnant(the_person): # Called when a girl is knocked up. Establishes all of the nessesary bits of info.
        the_person.event_triggers_dict["immaculate_conception"] = the_person.has_taboo("vaginal_sex") #TODO: Add this, and a path where she doesn't think it's yours: and (the_person.relationship = "Single" and (the_person.effective_sluttiness() < 40 or the_person.love > 40)) or the_person.love > 80: #Doesn't even know how it happend!
        the_person.event_triggers_dict["preg_accident"] = the_person.on_birth_control # If a girl is on birth control the pregnancy is an accident.
        the_person.event_triggers_dict["preg_start_date"] = day
        the_person.event_triggers_dict["preg_tits_date"] = day + 21 + renpy.random.randint(0,7)
        the_person.event_triggers_dict["preg_transform_day"] = day + 90 + renpy.random.randint(0,15)
        the_person.event_triggers_dict["preg_finish_announce_day"] = day + 260 + renpy.random.randint(0,15)
        the_person.event_triggers_dict["pre_preg_tits"] = the_person.tits

        preg_announce_action = Action("Pregnancy Announcement", preg_announce_requirement, "pregnant_announce", requirement_args = day + renpy.random.randint(12,18))
        the_person.on_room_enter_event_list.append(preg_announce_action)

        preg_tits_action = Action("Pregnancy Tits Grow", preg_tits_requirement, "pregnant_tits_start", args = the_person, requirement_args = the_person)
        mc.business.mandatory_morning_crises_list.append(preg_tits_action)

        preg_transform_action = Action("Pregnancy Transform", preg_transform_requirement, "pregnant_transform", args = the_person, requirement_args = the_person)
        mc.business.mandatory_morning_crises_list.append(preg_transform_action) #This event adds an announcement event the next time you enter the same room as the girl.

        the_person.add_role(pregnant_role)

    def preg_transform_announce_requirement(the_person):
        return True

    def preg_finish_announcement_requirement(the_person):
        if day >= the_person.event_triggers_dict.get("preg_finish_announce_day", 0):
            return True
        return False

    def preg_finish_requirement(the_person, trigger_day):
        if day >= trigger_day:
            return True
        return False

    def tit_shrink_requirement(the_person, trigger_day):
        if day >= trigger_day:
            return True
        return False


label pregnant_announce(the_person):
    $ the_person.event_triggers_dict["preg_knows"] = True #Set here and in the larger tits, represents the person knowing they're pregnant so they don't ask for condoms ect.
    $ was_immaculate = the_person.event_triggers_dict.get("immaculate_conception", False) # In case you manage to get someone pregnant without even fucking them!
    $ was_accident = the_person.event_triggers_dict.get("preg_accident", False)
    $ the_person.draw_person()
    "[the_person.title] walks over to you as soon as she sees you."
    if mc.location.get_person_count() > 1:
        the_person "Could I talk to you for a second [the_person.mc_title]? It's important."
        "You nod and find a quiet spot to speak to [the_person.title]."

    if day - the_person.event_triggers_dict.get("preg_start_date", 0) > 30:
        return # If you don't ever check in with her for 30 days you probably don't care and we don't need to show this event.

    if was_immaculate:
        the_person "So, I have some news. This is really surprising, even to me..."
        mc.name "What's up? Is everything alright?"
    elif was_accident:
        the_person "So I have some news. This might be a little suprising."
        mc.name "What's up? Is everything okay?"
    else:
        the_person "I have some big news."
        mc.name "Okay, what's up?"


    if girlfriend_role in the_person.special_role:
        if was_immaculate:
            the_person "I know this might sound crazy but... I'm pregnant!"
            the_person "I don't know when it happened, or how, since we haven't even had sex, but I definitely am."
            the_person "Maybe some of your cum dripped between my legs? Or it was on my hands when I touched myself? It doesn't really matter."
        elif was_accident:
            the_person "Well, you know that we haven't exactly been careful with condoms lately, since I'm on birth control..."
            the_person "I'm not sure exactly when it happened, but it looks like you... managed to get me pregnant anyways."
        else:
            the_person "Obviously you know we haven't been using any protection lately when we've been having sex and..."
            the_person "Well, you finally fucked a baby into me!"
        "She takes your hands and smiles."
        the_person "Isn't that exciting?! I wanted to tell you as soon as I found out, but I thought you should hear it in person!"
        mc.name "That's fantastic news!"
        "You hug [the_person.title], and she squeezes you back. After a long moment she breaks the hug."
        the_person "That's all for now, I don't need you to do anything. I'm just so happy to be able to share this with you!"

    elif affair_role in the_person.special_role: #Note: Requires her to be in a relationship, so there's no "immaculate conception" chance. She'll just think it's his.
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if was_immaculate:
            the_person "So I know this is going to sound crazy, but I'm pregnant."
            the_person "I don't think it's [so_title]'s, the dates just don't line up."
            the_person "Maybe I got some of your cum on my hand and touched myself, or maybe it dripped down between my legs."
            the_person "Either way, I'm knocked up and I think it's yours."
        elif was_accident:
            the_person "Well... We haven't been using condoms since I'm taking birth control, but..."
            the_person "It looks like you managed to knock me up anyways."
        else:
            the_person "I'm not on any sort of birth control, and we haven't been using condoms..."
            the_person "It looks like one of those creampies stuck and you knocked me up."
        "She bites her lip and shrugs."
        the_person "What do you want me to tell my [so_title]? I could tell him it's his, but I don't know if he'll believe it."
        the_person "It's been a long time since I let him have sex with me."
        menu: #TODO: We should add disabled slugs. Might need to make these into actions in that case.
            "Leave your [so_title]." if the_person.love + 10 > leave_SO_love_calculation(the_person):
                mc.name "I think it's time you left him so we can be together. There's no point in hiding this any longer."
                "[the_person.title] seems nervous, but after thinking about it for a moment she nods."
                the_person "You're right. This has gone on long enough. I'll... I'll tell him later today."
                call transform_affair(the_person) from _call_transform_affair_4

            "Tell him it's his.":
                mc.name "Just tell him it's his. If he doesn't believe it we can deal with that later."
                "[the_person.title] nods nervously."
                the_person "Okay, that's what I'll do."
                #TODO: Have an event based on this, more likely to spawn the higher her Love (as a inverse substitute for her Love for him)

            "Let him fuck you." if the_person.effective_sluttiness() >= 50 or the_person.obedience >= 140 or the_person.get_opinion_score("creampies") > 0:
                #She won't fuck her SO unless she's slutty or obeident enough to do it despite her love for you (or if she just loves getting creampied)
                mc.name "I want you to let him fuck you, just once. Then in a week you can tell him it's his."
                the_person "Okay, I guess that would stop him from being suspicious. I'll do it, if that's what you want."

        "She gives you a quick hug and a kiss."
        the_person "That's all, I suppose. I'll keep you updated on how things are going."

    elif the_person.is_family(): #TODO: Expand this into full events for each family member. This is a placeholder until then
        if was_immaculate:
            the_person "There's no easy way to explain this, so I'll just say it. I'm pregnant."
            the_person "I don't know how it could have even happened. I haven't had sex in so long!"
            the_person "It's not important now though, what is important is that I'm going to have a baby!"
        elif was_accident:
            the_person "I... Well, I'm pregnant, [the_person.mc_title]."
            the_person "I don't know how it happened. I've been very careful with my birth control since we've been having sex."
        else:
            the_person "We've been being pretty risky, since I'm not on my birth control and you like cumming inside me so much."
            the_person "I took a test and it looks like you finally knocked me up. I'm going to have your baby."

        the_person "You don't need to do anything special, I'm going to take care of everything for us. I just wanted you to know."
        mc.name "Okay, I love you [the_person.title]."
        the_person "I love you too [the_person.mc_title]."
        "[the_person.possessive_title] gives you a tight hug."

    elif the_person.relationship != "Single": # You aren't having a formal affair, but she's in a relationship. More of a "one night stand" kind of thing.
        $ so_title = SO_relationship_to_title(the_person.relationship)
        if was_immaculate:
            the_person "Well I wanted you to know that... I'm pregnant. It's probably not yours, since we've never had sex."
            the_person "You don't think your cum might have ended up in my by... accident, do you?"
            mc.name "Nothing's impossible, I suppose."
            the_person "I was worried you'd say that... What do you think I should do?"

        elif was_accident:
            the_person "Well... I know I said I was on birth control when we fooled around, but it looks like something went wrong."
            the_person "I took a test, and I'm pregnant. You got me pregnant."
            the_person "I never meant for this to be so serious. I don't know how to tell my [so_title] that I let another man get me pregnant."
        else:
            the_person "I wasn't on any sort of birth control when we fooled around and you came inside me."
            the_person "It must have been the right time of the month, because I'm pregnant."
            the_person "I never meant for this to be so serious. I don't know how to tell my [so_title] that I let another man get me pregnant."
        menu:
            "Leave him for me." if the_person.love > leave_SO_love_calculation(the_person):
                mc.name "Just leave him. I'll take responsability for what happened, I'm ready to commit to a relationship with you [the_person.title]."
                the_person "Are you really? I..."
                "She thinks for a long moment, then she takes your hand and nods."
                the_person "Okay, if you promise to be there for me I think he deserves to tell the truth. I'll have to break it to him later today."
                call transform_affair(the_person) from _call_transform_affair_5 # She doesn't have the affair role, but it is effectively the same here and the functionality works.

            "Start having an affair." if ask_girlfriend_requirement(the_person):
                mc.name "Just tell him it's his, and we can start seeing each other more so I can help you in this difficult time."
                $ the_person.add_role(affair_role)

            "Tell him it's his.":
                mc.name "Just tell him it's his. I'm sure he'll be ecstatic to hear the good news."
                "She seems nervous and unsure, but nods her head."
                the_person "I guess that's what I'll have to do. Anyways, you don't need to do anything. I just thought you should know."

    else: #She's single, a true one night stand kind of encounter.
        if was_immaculate:
            the_person "I know this is going to come out of the blue, but... I'm pregnant."
            the_person "I know we haven't had sex, but I can't even think of anyone else I've been close to other than you."
            the_person "Maybe... I got some of your cum inside me by accident? Like it dripped between my legs? I don't know."
            the_person "What I do know is that I'm pregannt, and I think it's yours."
        elif was_accident:
            the_person "Well... I know I said I was on birth control when we fooled around, but it looks like something went wrong."
            the_person "I took a test, and I'm pregnant. You got me pregnant."
        else:
            the_person "I wasn't on any sort of birth control when we fooled around. It felt so good when you came inside me, but..."
            "She sighs and shrugs."
            the_person "It must have been the right time of the month, because I'm pregnant."
        the_person "You don't need to do anything, I knew the risks when we had sex. I just thought you should know."
        menu:
            "Take responsability." if ask_girlfriend_requirement(the_person):
                mc.name "I knew the risks too, and I think it's important we're both together for this. If you'd have me, I want to be your partner for this."
                "She blinks away a few tears and nods."
                $ the_person.change_happiness(10)
                the_person "I'm sorry, I guess the hormones are already getting to me. I'd like that."
                $ the_person.add_role(girlfriend_role)
                "You hug [the_person.possessive_title], and she hugs you back."
                the_person "That's all for now, I'll keep you informed as things progress."

            "Thanks for telling me.":
                mc.name "Thank you for telling me. Let me know how things are progressing."
                the_person "Okay, I will."
    $ clear_scene()
    return

label pregnant_tits_start(the_person):
    python:
        the_person.event_triggers_dict["preg_knows"] = True
        the_person.tits = get_larger_tits(the_person.tits) #Her tits start to swell.
        the_person.personal_region_modifiers["breasts"] = the_person.personal_region_modifiers["breasts"] + 0.1 #As her tits get larger they also become softer, unlike large fake tits. (Although even huge fake tits get softer)

        pregnant_tits_announce_action = Action("Announce Pregnant Tits", pregnant_tits_annouce_requirement, "pregnant_tits_announce", args = day)
        the_person.on_talk_event_list.append(pregnant_tits_announce_action)
    return

label pregnant_tits_announce(start_day, the_person):
    if day - start_day >= 7:
        return #If it's been a week she doesn't comment on it.

    if the_person.effective_sluttiness() + (the_person.get_opinion_score("showing her tits")*10) > 50: #She's happy to show off her new tits
        the_person "Hey [the_person.mc_title]. I was looking in the mirror this morning and I noticed something."
        "She cups her tits and jiggles them."
        if the_person.get_opinion_score("creampies") > 0 and the_person.get_opinion_score("being submissive") > 0:
            the_person "My tits are starting to swell. It feels like my body is tranforming into a sluttier version of me."
            the_person "Soon everyone is going to know that I was a desperate cumslut who got bred. Ah..."
            "She closes her eyes and sighs happily, clearly lost in her own little fantasy."

        else:
            the_person "My tits are starting to swell up. I wonder how long it's going to be until people figure out I'm pregnant."
            mc.name "I think you've got a little longer before it's obvious. For now you can just let all the other girls be jealous of your big tits."
            "She smiles and lets her tits drop out of her hands. They bounce a few times before coming to a stop."

    else: #She's a little embarrassed about it
        the_person "Hey [the_person.mc_title], I have a question."
        mc.name "Okay, what is it?"
        the_person "Can you tell that my boobs are bigger? They're starting to swell up and I'm nervous people are going to figure out I'm pregnant."
        "She moves her arms and gives you a clear look at her chest. Her tits do look bigger than they were before."
        mc.name "They're definitely larger, but I don't think you need to worry about it. I'm sure all the other girls will be jealous of your great rack."
        the_person "That's good to hear. Thanks [the_person.mc_title]."

    call talk_person(the_person) from _call_talk_person_11
    return

label pregnant_transform(the_person): #Changes the person to their pregnant body and stores what their pre-pregnancy body and tits were
    python:
        the_person.event_triggers_dict["pre_preg_body"] = the_person.body_type
        the_person.body_type = "standard_preg_body"
        the_person.tits = get_larger_tits(the_person.tits) # Her tits get even larger
        the_person.personal_region_modifiers["breasts"] = the_person.personal_region_modifiers["breasts"] + 0.1 #As her tits get larger they also become softer, unlike large fake tits. (Although even huge fake tits get softer)
        the_person.lactation_sources += 1

        preg_transform_announce_action = Action("Pregnancy Transform Announcement", preg_transform_announce_requirement, "pregnant_transform_announce", args = day)
        the_person.on_room_enter_event_list.append(preg_transform_announce_action)

        preg_finish_announce_action = Action("Pregnancy Finish Announcement", preg_finish_announcement_requirement, "pregnant_finish_announce", args = the_person, requirement_args = the_person)
        mc.business.mandatory_crises_list.append(preg_finish_announce_action)
    return

label pregnant_transform_announce(start_day, the_person):
    if day - start_day > 21: #If you haven't noticed in 3 weeks you probably just don't care. Skip the event.
        return

    $ the_person.draw_person()
    "[the_person.possessive_title] notices you and comes over to talk."


    if the_person.event_triggers_dict.get("preg_start_date", day) - day <= 75:
        # Unusually short pregnancy.
        the_person "Hey [the_person.mc_title]. I know this might be a little suprising, but obviously things..."
        "She runs her hand over her belly, accentuating the new and prominent curves that have formed."
        the_person "... are moving pretty fast. My doctor tells me everything is fine, I'm just ahead of the curve."

    else:
        # Normal length pregnancy
        the_person "Hey [the_person.mc_title]. So, I'm past the point of just having a little baby bump..."
        "She turns and runs a hand over her belly, accentuating the new and prominent curves that have formed there."

    the_person "My boobs are starting to swell with milk too. It's a little embarrassing but..."
    the_person "Now when I get aroused they leak just a little bit."
    mc.name "You look fantastic. You really are glowing."
    $ the_person.change_happiness(10)
    "[the_person.possessive_title] smiles and holds your hand for a moment."
    the_person "Well don't let me distract you any more, I'm sure you were doing something important."
    return

label pregnant_finish_announce(the_person): #TODO: have more varients for girlfriend_role, affair_role, etc.
    # The girl tells you she'll need a few days to have the kid and recover, and she'll be back in a few days.
    "You get a call from [the_person.possessive_title]. You answer it."
    mc.name "Hey [the_person.title], what's up?"

    if employee_role in the_person.special_role:
        the_person "Hi [the_person.mc_title]. I wanted to let you to know that I won't be at work for a few days."
    else:
        the_person "Hi [the_person.mc_title], I have some exciting news."

    the_person "I saw my doctor yesterday and he tells me I'm going to pop any day now."

    if the_person.event_triggers_dict.get("preg_start_date", day) - day <= 230: #It's unusually short
        the_person "It's earlier than I expected, but he tells me everything looks like it's perfectly normal."

    mc.name "That's amazing news. Do you need me to do anything?"
    the_person "No, I know you're very busy. You just focus on work and I'll focus on this. I know you'll be there for me in spirit."
    mc.name "Okay, I'll talk to you soon then."
    the_person "I'll let you know as soon as things are finished. Bye!"

    python:
        the_person.event_triggers_dict["preg_old_schedule"] = the_person.schedule.copy() #Take a shallow copy so we can change their current schedule to nothing
        the_person.set_schedule(the_person.home, times = [0,1,2,3,4])

        preg_finish_action = Action("Pregnancy Finish", preg_finish_requirement, "pregnant_finish", args = the_person, requirement_args = [the_person, day + renpy.random.randint(4,7)])
        mc.business.mandatory_morning_crises_list.append(preg_finish_action)
    return

label pregnant_finish(the_person):
    python:
        the_person.body_type = the_person.event_triggers_dict.get("pre_preg_body", "standard_body")
        the_person.schedule = the_person.event_triggers_dict.get("preg_old_schedule")

        the_person.event_triggers_dict["preg_knows"] = False #Otherwise she immediately knows the next time she's pregnant.
        the_person.kids += 1 #TODO: add a new role related to a girl being a mother of your kid?

        tit_shrink_one_day = day + renpy.random.randint(21,30)
        tit_shrink_one = Action("Tits Shrink One", tit_shrink_requirement, "tits_shrink", args = [the_person, True], requirement_args = [the_person, tit_shrink_one_day])
        tit_shrink_one_announcement_action = Action("Tits Shrink One Announcement", tit_shrink_requirement, "tits_shrink_announcement_one", args = tit_shrink_one_day, requirement_args = tit_shrink_one_day)

        tit_shrink_two_day = day + renpy.random.randint(40,60)
        tit_shrink_two = Action("Tits Shrink Two", tit_shrink_requirement, "tits_shrink", args = [the_person, False], requirement_args = [the_person, tit_shrink_two_day])
        tit_shrink_two_announcement_action = Action("Tits Shrink Two Announcement", tit_shrink_requirement, "tits_shrink_announcement_two", args = tit_shrink_two_day, requirement_args = tit_shrink_two_day)

        mc.business.mandatory_morning_crises_list.append(tit_shrink_one) #Events for her breasts to return to their normal size.
        mc.business.mandatory_morning_crises_list.append(tit_shrink_two)

        the_person.on_talk_event_list.append(tit_shrink_one_announcement_action) #And here is where she tells you about those changes
        the_person.on_talk_event_list.append(tit_shrink_two_announcement_action)

        while pregnant_role in the_person.special_role: #While loop just in case it's ended up in there multiple times. In theory this should only trigger once.
            the_person.remove_role(pregnant_role)

    "You get a call from [the_person.possessive_title] early in the morning. You answer it."
    the_person "Hey [the_person.mc_title], good news! Two days ago I had a beautiful, healthy baby girl! I'll be coming back to work today." #Obviously they're all girls for extra fun in 18 years.
    #TODO: Let you pick a name (or at low obedience she's already picked one)
    mc.name "That's amazing, but are you sure you don't need more rest?"
    if affair_role in the_person.special_role:
        $ so_title = SO_relationship_to_title(the_person.relationship)
        the_person "I'll be fine, I'll be leaving our girl with her \"father\" so I can come back and see you again."


    else:
        the_person "I'll be fine. I'm leaving her with my mother for a little while so I can get back to a normal life."

    the_person "I just wanted to let you know. I'll talk to you soon."
    "You say goodbye and [the_person.title] hangs up."
    return


label tits_shrink(the_person, reduce_lactation):
    $ the_person.lactation_sources += -1
    $ the_person.tits = get_smaller_tits(the_person.tits)
    $ the_person.personal_region_modifiers["breasts"] = the_person.personal_region_modifiers["breasts"] - 0.1
    return

label tits_shrink_announcement_one(day_shrunk, the_person):
    #She lets you know that her tits are getting back to normal (Base reaction based on opinion and sluttiness).
    if day - day_shrunk >= 7:
        return # If it's been a week sincei t's happened just move on and don't comment on it.

    the_person "Hey [the_person.mc_title]."
    "[the_person.possessive_title] sighs and looks down at her chest. She cups a boob and rubs it gently."
    the_person "It looks like my milk is starting to dry up. I'm going to miss having my tits that big..."
    if the_person.get_opinion_score("creampies") > 0 or the_person.get_opinion_score("bareback sex"):
        the_person "If you really wanted to keep them around you could always get me pregnant again."
        "She bites her lip and eyes your crotch, obviously fantasising."
        mc.name "What a good little slut, being so eager to get bred again just so I can have some bigger tits to play with."
        $ the_person.change_arousal(10)
        "She nods and sighs happily."
    else:
        the_person "I won't miss milk soaking through all my bras. That was a huge pain."
    call talk_person(the_person) from _call_talk_person_12
    return

label tits_shrink_announcement_two(day_shrunk, the_person):
    #She lets you know that her tits are getting back to normal (Base reaction based on opinion and sluttiness).
    if day - day_shrunk >= 7:
        return # If it's been a week sincei t's happened just move on and don't comment on it.

    the_person "Hey [the_person.mc_title]."
    "[the_person.possessive_title] sighs and looks down down at her chest. She cups one of her boobs and rubs it gently."
    the_person "My chest is back to it's old size. I had gotten so use to them when I was pregnant that these feel tiny now."
    mc.name "That's a pretty easy problem to solve. I'll just have to get you pregnant again."
    if the_person.get_opinion_score("creampies") > 0 or the_person.get_opinion_score("bareback sex"):
        $ the_person.change_arousal(10)
        "[the_person.title] moans and nods happily."
        the_person "Yes please, I want that so badly... Whenever you want to do it."
    else:
        the_person "That was a lot of work to go through just for some bigger tits. Maybe I'll get a boobjob though..."
    call talk_person(the_person) from _call_talk_person_13
    return
