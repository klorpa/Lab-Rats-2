# Contains all of the events and related things to Christina's role (Emily's mother)

init -2 python:
    def student_mom_appologise_requirement(the_person):
        if time_of_day != 3:
            return False
        elif the_person not in the_person.home.people:
            return False
        else:
            return True


label study_check_up(the_student, the_mom):
    # TODO: Christina asks how things are going after a study session.
    # If her marks have improved enough, and if you haven't been already, Christina invites you to stay for dinner.

    $ clear_scene()
    $ the_group = GroupDisplayManager([the_student, the_mom], primary_speaker = the_mom)
    $ the_group.draw_group()
    "[the_student.title] opens the door to her room and leads you downstairs. [the_mom.title] is waiting at the front door."
    the_mom "All done for tonight? Tell me [the_mom.mc_title], how is my daughter doing?"
    $ current_marks = the_student.event_triggers_dict.get("current_marks",0)
    if current_marks < 20:
        mc.name "I'll be honest, there's still a lot of work to do. It's going to take a lot of hard work if she wants to succeed."
        the_mom "Do you hear that [the_person.title]? I expect you to keep working at this and to listen to everything [the_mom.mc_title] says."
        $ the_group.draw_person(the_student)
        $ the_student.change_happiness(-5)
        $ the_student.change_obedience(1)
        the_student "I promise I'm doing my best Mom."

    elif current_marks < 50:
        mc.name "I've watched her improve a little, but there's still a long way to go."
        mc.name "[the_student.title] has been giving it her all though. I think with more time and focus she'll be able to do it."
        the_mom "At least she's improving. [the_student.title], I expect you to listen to [the_mom.mc_title] and do everything he suggests."
        $ the_group.draw_person(the_student)
        $ the_student.change_happiness(-5)
        $ the_student.change_obedience(1)
        the_student "Okay Mom, I will."

    elif current_marks < 75:
        mc.name "[the_student.title] is really starting to improve. As long as she can keep this up she will do fine."
        the_mom "That's good to hear. I'm glad to hear you are working so well with [the_mom.mc_title]."
        $ the_group.draw_person(the_student)
        $ the_student.change_obedience(1)
        the_student "Thank you Mom. He's been such a big help."

    elif current_marks < 95:
        mc.name "[the_student.title] has turned things around. As long as she stays on top of her studies she shouldn't have any more problems."
        $ the_mom.change_love(1)
        the_mom "That's very good to hear. [the_student.title], I'm proud of you."
        $ the_group.draw_person(the_student)
        $ the_student.change_obedience(1)
        $ the_student.change_love(1)
        the_student "Thanks Mom, It was really [the_student.title], he's a very engaging teacher."


    else:
        mc.name "[the_student.title] has been a model student. She's put in the hard work, and her marks reflect that. I'm expecting her to be the top of her class."
        $ the_mom.change_love(1)
        the_mom "Well that's suprising to hear. [the_student.title] has never been very invested in her academics before."
        $ the_group.draw_person(the_student)
        $ the_student.change_obedience(1)
        $ the_student.change_love(2)
        the_student "I owe it all to [the_student.mc_title], he's the best teacher I've ever had. He really knows how to teach me a lesson."

    $ the_group.draw_person(the_mom)
    if the_student.event_triggers_dict.get("current_marks",0) >= 75:
        if the_mom.event_triggers_dict.get("offered_dinner", 0) == 0:
            $ the_mom.event_triggers_dict["stayed_for_dinner"] = 0
            $ the_mom.event_triggers_dict["offered_dinner"] = 1
            the_mom "Thank you for all your hard work [the_mom.mc_title]."
            the_mom "If you don't have any plans for the evening you're welcome to join us for dinner."#

        else:
            the_mom "Thank you for all of your hard work [the_mom.mc_title]. Would you like to join us for dinner tonight?"

        $ the_group.draw_person(the_student, emotion = "happy")
        "[the_student.possessive_title] holds onto your arm and smiles happily."
        the_student "You can stay a little longer, right [the_student.mc_title]?"

        menu:
            "Stay for dinner.":
                mc.name "I'd love to say for dinner. Thank you [the_mom.title]."
                $ the_group.draw_person(the_mom)
                if the_mom.event_triggers_dict["stayed_for_dinner"] == 0:
                    the_mom "Excellent! Mr.[the_mom.last_name] will be home soon, he has wanted to meet you for a long time."
                    the_mom "I will have dinner ready in a few minutes. [the_student.title], can you show [the_mom.mc_title] to the dining room and get the places set?"
                    call student_dinner(the_student, the_mom, first_time = True) from _call_student_dinner
                else:
                    the_mom "Excellent! I will have dinner ready in a few minutes."
                    the_mom "[the_student.title], can you show [the_mom.mc_title] to the dining room and get the places set?"
                    $ the_group.draw_person(the_student)
                    the_student "Right away Mom. Come with me."
                    call student_dinner(the_student, the_mom, first_time = False) from _call_student_dinner_1
                $ the_mom.event_triggers_dict["stayed_for_dinner"] += 1

            "Leave politely.":
                mc.name "I'm sorry, I made other plans for tonight."
                $ the_group.draw_person(the_mom)
                the_mom "That's a shame. Maybe next time you're over to tutor [the_student.title] then."
                mc.name "I'll do my best."


    else:
        the_mom "Thank you for your hard work [the_mom.mc_title]. I hope we see you again soon."

    return

label student_dinner(the_student, the_mom, first_time):
    #TODO Have a unique dining room background
    $ clear_scene()
    $ the_group = GroupDisplayManager([the_student], primary_speaker = the_student)
    $ the_group.draw_group()

    if first_time:
        "[the_student.possessive_title] leads you into a finely decorated dining room. She pulls out a chair and motions for you to sit down at the table."

    else:
        "[the_student.possessive_title] leads you into the dining room and pulls out a chair for you."
    the_student "You just have a seat, I'll get everything ready."
    $ the_group.draw_person(the_student, position = "sitting")
    "You sit down and wait while [the_student.title] sets out placemats and cutlery. When she's done she sits down in the seat next to you."
    $ the_group.add_person(the_mom, make_primary = True)
    $ the_group.redraw_person(the_student)
    $ the_group.draw_person(the_mom)
    "After waiting for a few minutes [the_mom.possessive_title] steps into the kitchen, carrying a tray of roast chicked and a bottle of wine under her arm."
    "She places the tray down, places the bottle of wine down, and sit down across from you and her daughter."
    $ the_group.draw_person(the_mom, position = "sitting")
    the_mom "Mr.[the_mom.last_name] should be home any minute now, he's probably just held up at the office."
    mc.name "No problem, we can wait a little..."
    $ the_group.draw_person(the_student, position = "sitting")
    $ the_group.draw_person(the_mom, make_primary = False, position = "walking_away")
    "You're interrupted by the phone ringing. [the_mom.title] apologies and moves into the kitchen."
    the_mom "Yes... Okay... [the_student.title]'s tutor is over for dinner... I'll tell him... We can talk when you get home..."
    $ the_group.draw_person(the_mom, position = "sitting")
    "[the_mom.possessive_title] comes back into the room and sits down. She has a tense smile as she reaches for the bottle of wine."
    if first_time:
        the_mom "My husband is going to be at the office for the rest of the night, so we should just get started."
        the_mom "He wanted me to tell you how happy he is with your work."
        "[the_student.title] sits, uncomfortably quiet, as her mother uncorks the bottle of wine and pours herself a generous amount."
    else:
        the_mom "My husband is going to be at the office later again. He told us to have dinner without him."
        "[the_student.title] sighs unhappily as her mother uncorks the bottle of wine. She pours herself a generous glass."

    the_mom "Let me pour you both a glass..."
    "You have dinner with [the_student.possessive_title] and [the_mom.title]."
    "[the_mom.possessive_title] seems tense at first, but after some food and two glasses of wine she is smiling and making pleasant conversation."
    $ the_group.draw_person(the_mom, position = "sitting", emotion = "happy")
    the_mom "[the_student.title], you made a very good choice when you asked [the_mom.mc_title] to tutor you. He's an absolute pleasure to have around."
    if the_student.love > 40 or the_student.effective_sluttiness() > 30:
        $ the_group.draw_person(the_student, position = "sitting")
        "[the_student.possessive_title] places her hand on your thigh and rubs it for emphasis."
        if the_student.effective_sluttiness() > 50:
            "She carries on the conversation with her mother, but her hand starts to drift higher up."
            "Soon [the_student.title] is rubbing your bulge under the table, massaging it through your pants."

    if the_mom.effective_sluttiness() > 20:
        $ the_group.draw_person(the_mom, position = "sitting")
        "While you are talking you feel a gentle touch on your leg. You glance under the table and see it is [the_mom.title]'s foot caressing your calf."
        "She turns to you and smiles, keeping up her conversation with her daughter while her foot moves up your leg."
        "Soon enough she is rubbing her soft foot against your inner thigh. The movement brings her dangerously close to brushing your cock."
        "After a few moments of teasing she draws her leg back and slips her foot back in her shoe."


    the_mom "Now, how about I get desert ready. [the_student.title], please clean the table. Leave my wine, I'll have the rest with desert."
    $ the_group.draw_person(the_student, position = "sitting")
    the_student "Okay Mom."
    $ the_group.draw_group(position = "walking_away")
    "Both women stand up. [the_mom.title] moves into the kitchen, while her daughter collects a stack of dirty dishes before following behind her."
    $ clear_scene()
    # You can already give Emily serum while she's studying, so this is just to corrupt her Mom.
    menu:
        "Add serum to [the_mom.title]'s wine." if mc.inventory.get_any_serum_count() > 0:
            call give_serum(the_mom) from _call_give_serum_28
            if _return:
                "You stand up and lean over the table, quickly emptying the contents of a small glass vial into [the_mom.title]'s half finished wine glass."
                "You give the glass a quick swirl, then sit back down and wait for [the_mom.title] and [the_student.title] to return."
            else:
                "You reconsider, and instead sit back in your chair and wait for [the_mom.title] and [the_student.title] to return."


        "Leave her drink alone.":
            "You lean back in your chair and relax while you wait for [the_mom.title] and [the_student.title] to return."


    "After another minute or two both of them come back from the kitchen, now carrying small bowls of ice cream."
    $ the_group.draw_person(the_mom)
    $ the_group.draw_person(the_student, position = "sitting")
    "[the_student.title] places one bowl down in front of you before sitting back in her chair beside you."
    $ the_group.draw_person(the_mom, position = "sitting")
    "[the_mom.possessive_title] sits down and takes a sip from her wine."
    the_mom "I'm glad you were able to join us for the evening [the_mom.mc_title]."
    the_mom "It seems like my husband is always at work, it's nice to have some company."
    menu:
        "Talk about [the_student.title].":
            mc.name "It's no trouble. It also gives us a perfect opportunity to talk about your daughters education."
            if the_mom.event_triggers_dict.get("student_mom_extra_obedience", False):
                the_mom "Yes, give me an update on how things are going."
                "You give [the_mom.title] a recap of your work educating [the_student.title], leaving out anything too explicit."
                $ the_mom.change_happiness(5)
                the_mom "It sounds like you have everything under control. Good work."

            else:
                the_mom "That's a very good idea. Is she giving you any problems?"
                "You glance at [the_student.possessive_title] at your side, then shake your head."
                mc.name "No, she is doing very well. There are some new study techniques that I would like to try though."
                the_mom "Is that so? Well you have my full permission. [the_student.title], I want you to do everything [the_mom.mc_title] tells you to do."
                the_mom "Please treat his instructions as if they were coming from me or your father."
                $ the_group.draw_person(the_student, position = "sitting")
                $ the_student.change_obedience(10)
                the_student "Yes Mom, I promise I will."
                $ the_mom.event_triggers_dict["student_mom_extra_obedience"] = True

        "Flirt with [the_mom.title].":
            mc.name "The pleasure is all mine. Your daughter is wonderful, I should have known she got it from her mother."
            "[the_mom.possessive_title] laughs and waves you off."
            the_mom "You're too kind."
            "You flirt with [the_mom.title] as much as you think you can get away with while her daughter is in the room."
            $ the_mom.change_slut_temp(1)
            $ the_mom.change_love(2, max_modified_to = 25)

        "Touch [the_student.title]." if the_student.effective_sluttiness("touching_body") > 35:
            mc.name "I'm glad to be here. I'm always happy to spend time with you and your daughter."
            $ the_group.draw_person(the_student, position = "sitting")
            "You move a hand to your side, then and onto [the_student.possessive_title]'s thigh, rubbing it gently."
            "You move your hand higher, up her thigh and to her crotch. You can feel her struggling to keep still in front of her mother."

            if the_student.effective_sluttiness() > 50:
                "In response [the_student.title] moves her hand onto your crotch, the movements hidden by the table."
                "She runs her hand along the bulge of your crotch, stroking you slowly through the fabric."
                the_student "He's been such a strong, firm presence in my life since I met him. I'm really learning a lot."
                $ the_student.change_slut_temp(1)
                "You and [the_student.possessive_title] fondle each other while you eat dinner, doing your best to keep [the_mom.title] from noticing everything."

            else:
                "You fondle [the_student.possessive_title] as you eat your desert, doing your best to keep [the_mom.title] from noticing."



            $ the_student.change_slut_temp(1 + the_student.get_opinion_score("public sex"))
            $ the_student.discover_opinion("public sex")
            "Eventually you finish your ice cream."
            $ the_group.draw_person(the_mom, position = "sitting")
            the_mom "[the_student.title], could you clean things up for us?"

    "[the_student.possessive_title] collects up the dishes again when you are finished desert and carries them to the kitchen."
    the_mom "It's been wonderful having you over [the_mom.mc_title], but I'm sure you're looking forward to getting home."
    mc.name "The dinner was fantastic. I'm lucky to have such a generous, beautiful host."
    "[the_mom.title] seems to blush, although it might just be wine taking effect."
    $ the_group.draw_group()
    "[the_mom.title] and [the_student.title] walk you to the door to say goodbye."
    the_student "Bye [the_student.mc_title], I hope you'll be by again soon!"

    if the_mom.effective_sluttiness("kissing") > 20 and not the_mom.event_triggers_dict.get("student_mom_door_kiss", 0) == 1: #TODO: Add a check that we haven't triggered the "I'm sorry" event.
        $ the_group.draw_person(the_mom)
        the_mom "[the_student.title], I need to have a private word with [the_mom.mc_title] before he goes."

        $ clear_scene()
        $ the_mom.draw_person()
        "[the_student.possessive_title] nods and goes upstairs to her room. [the_mom.title] waits until she is gone before turning back to you."
        if the_mom.event_triggers_dict.get("student_mom_door_kiss", 0) == 2: #TODO: Add a check that you've also triggered the "I'm sorry event
            # She wants to kiss you, and you've already done it before
            the_mom "I just wanted to say thank you again for coming over..."
            $ the_mom.draw_person(position = "kissing", emotion = "happy", special_modifier = "kissing")
            "She takes a half step closer and leans in. You close the rest of the gap and kiss her."
            "[the_mom.possessive_title] kisses you passionately at the door, rubbing her body against you for a moment."
            "After a long moment she pulls back and breaks the kiss, panting softly."
            $ the_mom.draw_person(position = "kissing", emotion = "happy")
            $ the_mom.break_taboo("kissing")
            the_mom "Come again soon, okay? I don't like being lonely..."
            mc.name "I won't be gone long."
            "She watches you from the front door as you leave."

        else:
            # It's the first time
            mc.name "Is something wrong?"
            the_mom "No, nothing is wrong. I wanted to say thank you for tutoring my daughter."
            "She takes a half step closer, putting one of her legs between yours."
            the_mom "And for spending the evening with me, when I would have otherwise been all alone..."
            "She leans close, barely an inch seperating you from her. You can smell the faint hint of wine on her breath."
            the_mom "With no one to comfort me..."
            $ the_mom.draw_person(position = "kissing", emotion = "happy", special_modifier = "kissing")
            "[the_mom.possessive_title] closes the gap and kisses you passionately, almost over-eagerly."
            "She presses her body against you and holds the back of your neck. After a long moment she pulls back, panting softly."
            $ the_mom.draw_person(position = "kissing", emotion = "happy")
            $ the_mom.change_slut_temp(1)
            $ the_mom.break_taboo("kissing")
            the_mom "Thank you for coming for dinner [the_mom.mc_title]. I hope I see you again soon..."
            "She steps back, trailing a hand along your chest."
            mc.name "I hope so too. Goodnight [the_mom.title]."
            "She watches you from the front door as you leave the house."
            $ student_mom_appologise_action = Action("Student_mom_appologise", student_mom_appologise_requirement, "student_mom_appologise_label")
            $ the_mom.on_room_enter_event_list.append(student_mom_appologise_action)
            $ the_mom.event_triggers_dict["student_mom_door_kiss"] = 1

    else:
        $ the_group.draw_person(the_mom)
        the_mom "You're welcome to come again for dinner any time [the_mom.mc_title]. Have a good evening."
        "They watch you from the porch as you leave."





    #TODO: Something like "It's nice to have some company at home..."
    #TODO: Branching options? Let the player select what they want to do?
    #TODO: Something should lead directly into her having the affair role.
    #TODO: Options like "Talk about her daughter.", "Flirt with Christina.".
    #TODO: If she's slutty enough (should be achievable with some minor corruption or serum use, 25-ish) she finds a way to kiss you. The next time you're over she appologises.



    # TODO: This event. YOu stay for dinner. Emily's father is "delayed at the office", so the three of you have dinner together.
    # Christina praises your work and gives you permission to "do whatever you need to do to help her daughter."
    # Mention that she should "get more involved" in her daughters schooling.
    # She also gets a little tipsy and a little hands-y with you when you go to leave.

    $ the_mom.event_triggers_dict["stayed_for_dinner"] += 1
    $ clear_scene()
    return

#TODO: Hook this event up!
label student_mom_appologise_label(the_person): #TODO Provide a way to not activate this event right away? Or even just to turn it down when it triggers.
    if affair_role in the_person.special_role or the_person.effective_sluttiness() >= 60:
        $ the_person.event_triggers_dict["student_mom_door_kiss"] = 2
        return # There's nothing to worry about, she's either already fooling around with you or she's slutty enough she doesn't care.
    $ the_person.draw_person()
    the_person "[the_person.mc_title], it's nice to see you."
    "She avoids making eye contact with you, looking off to the side."
    the_person "Could I speak with you for a moment, privately?"
    "You nod and follow her to the sitting room."
    the_person "I wanted to appologise for my moment of indiscretion."
    the_person "I was angry, and lonely, and drunk, and I lost control. I'm sorry."
    mc.name "You mean when you kissed me?"
    "She nods meekly."
    mc.name "You don't need to be sorry, I liked it. It sounds like you really needed it, too."
    the_person "I don't know what you mean..."
    mc.name "It's pretty obviously. When's the last time your husband was home on time?"
    the_person "It's been a few weeks..."
    mc.name "When was the last time you had sex together?"
    if the_person.effective_sluttiness() < 35:
        the_person "[the_person.mc_title], that's a little personal!"
        mc.name "It's been a while though, right?"
        the_person "It... has been a while. You're right."
    else:
        the_person "It... certainly has been a long time. Sometimes he asks for a blowjob when he gets home, but he reciprocates."
        "She shakes her head in disbelief."
        the_person "I'm sorry, I shouldn't be telling you that."
    mc.name "You're a woman, and you have needs. [emily.title] is out of the house most of the day, your husband is working..."
    "You step close to [the_person.possessive_title] and put your arm around her waist."
    mc.name "It's natural for you to need some sort of physical contact. Isn't that what you want?"
    "She stutters out a few half answers."
    the_person "I don't... I mean, it would be nice, but I can't... I..."
    "You kiss her, and after a moment of hesitation she kisses you back."
    "When you break the kiss she looks deep into your eyes."
    the_person "Wow..."
    mc.name "I'm going to be here to tutor your daughter. I could also give you the physical contact you need."
    the_person "You mean, cheat on my..."
    "You nod. She sighs and closes her eyes, thinking it over. Your hand wanders down her back until you are cradling her ass."
    "Finally she opens her eyess and answers."
    the_person "Okay, but it's purely physical. There can any be anything real between us, and my daughter can never find out."
    mc.name "That sounds just fine to me."
    "You slap her ass hard, making her jump a little bit."
    mc.name "I'll be seeing you soon."
    "She nods meekly, cheeks flush."
    $ the_person.add_role(affair_role)
    return
