# All of the role specific actions for Nora
# Nora acts as an alternate way of unlocking serum research progress and allows the player to unlock special serum traits.

# Nora needs the player to help her cut through beurocratic red tape and test serum traits that she can't.
# She gives the player (temporary) access to a serum trait with a very high side effect chance, strange/extreme effects, and minimal sale value.
# The player needs to raise the mastery value of the trait to a certain level, after which they can "turn in" the request for a reward.
# Initially this reward will be acces to higher serum tech tiers or unlocks of other serum traits without having to research them.
# Later it may let you unlock unique serum traits.

init -2 python:
    def nora_research_up_requirement():
        if mc.business.research_tier != 1:
            return False
        elif mc.business.event_triggers_dict.get("nora_trait_researched",None) is None:
            return False
        elif time_of_day== 0:
            return "Too early to visit [nora.title]."
        elif time_of_day == 4:
            return "Too late to visit [nora.title]."
        elif round(mc.business.event_triggers_dict.get("nora_trait_researched").mastery_level) < 2:
            trait_name = mc.business.event_triggers_dict.get("nora_trait_researched").name
            return "Trait Mastery Level of " + trait_name + " must be 2 or higher."
        else:
            return True

    def nora_research_cash_intro_requirement(the_person, min_day):
        if day < min_day:
            return False
        elif not mc.business.is_open_for_business():
            return False
        elif time_of_day not in [2,3]:
            return False
        else:
            return True

    def visit_lab_intro_requirement(the_person):
        if mc.business.research_tier == 1:
            return False
        elif mc.business.event_triggers_dict.get("nora_trait_researched", None) is None and not mc.business.event_triggers_dict.get("nora_cash_research_trigger", False):
            return False
        elif mc.business.is_weekend():
            return "[nora.title] does not work on the weekend."
        elif time_of_day == 0:
            return "Too early to talk to [nora.title] about business."
        elif time_of_day == 4:
            return "Too late to talk to [nora.title] about business."
        else:
            return True

    def nora_research_cash_requirement(the_person):
        if mc.business.event_triggers_dict.get("nora_cash_research_trait", None) is None:
            return False
        elif time_of_day == 0:
            return "Too early to visit [nora.title]."
        elif time_of_day == 4:
            return "Too late to visit [nora.title]."
        elif round(mc.business.event_triggers_dict.get("nora_cash_research_trait").mastery_level) < 2:
            trait_name = mc.business.event_triggers_dict.get("nora_cash_research_trait").name
            return "Trait Mastery Level of " + trait_name + " must be 2 or higher."
        else:
            return True

    def special_research_requirement(the_person):
        if mc.business.event_triggers_dict.get("nora_research_subject", None) is None:
            return "No new research to turn in."
        elif mc.business.is_weekend():
            return "[nora.title] does not work on the weekend."
        elif time_of_day == 0:
            return "Too early to visit [nora.title]."
        elif time_of_day == 4:
            return "Too late to visit [nora.title]."
        else:
            return True


    def study_person_requirement(the_person):
        if time_of_day == 4:
            return "Not enough time."
        return True




label nora_intro_label(the_steph):
    $ the_nora = nora
    $ mc.business.event_triggers_dict["intro_nora"] = False #We've already intro'd her, so we don't have to do this again.
    mc.name "[the_steph.title], have you talked to [the_nora.title] yet?"
    "She nods."
    the_steph "I did, she said we would be welcome by any time."
    mc.name "Excellent, I want to pay her a visit and want you to come along."
    the_steph "Sure thing. It's going to be strange being back there, but I'm looking forward to it!"
    "The two of you head to the university. Being on campus again triggers a wave of nostalgia that you hadn't expected."

    $ university.show_background()
    "You navigate to the old lab and knock on the door. You hear the click of high heels approaching from the other side."
    "Your old lab director opens the door and smiles at you and [the_steph.title]. Inside the room is bustling with activity."
    $ the_nora.draw_person(emotion = "happy")
    the_nora "[the_nora.mc_title], [the_steph.title], I'm glad you stopped by."
    mc.name "It's nice to see you [the_nora.title]."
    $ the_steph.draw_person(emotion = "happy")
    the_steph "Hey [the_nora.title]. Good to be back."
    $ the_nora.draw_person(emotion = "happy")
    "[the_nora.possessive_title] steps out into the hallway and closes the lab door behind her."
    the_nora "I'm sorry I can't invite you in; the lab is a high security space now."
    the_nora "The university has gotten very protective of my work since you left."
    "She sounds frustrated with the situation."
    the_nora "Anyway, I know you aren't here for an earful about academic politics. You had a problem you needed help with?"
    mc.name "We did, but it might take a while to explain. How about I buy us a round of coffees and we talk about it upstairs."
    the_nora "The two of you have piqued my interest, lead the way."

    "The three of you return to ground level and go to a coffee shop near the center of campus."
    $ the_nora.draw_person(position = "sitting")
    "When you get there [the_steph.title] pulls out a folder containing a synopsis of your research and slides it over to [the_nora.title]."
    "[the_nora.possessive_title] looks through the notes, sipping thoughtfully at her coffee."
    the_nora "Hmm... Yes... Ah, I see what's going on. I ran into this same roadblock."
    $ the_steph.draw_person(position = "sitting")
    the_steph "Excellent, so you know where to go from here?"
    "[the_nora.title] looks up from her notes."
    $ the_nora.draw_person(position = "sitting")
    the_nora "Do I know? Of course! I haven't just been twiddling my thumbs since you two left!"
    the_nora "The problem is that all of my research is suppose to be kept within the university now. No sharing with outside organisations."
    the_nora "I wish I could help, but it's my job at risk."
    mc.name "Come on [the_nora.title], we're counting on you here."
    $ the_steph.draw_person(position = "sitting")
    the_steph "Think of the science, we shouldn't let bureaucrats get in the way of progress! That's what you always taught me, at least."
    "She leans forward in her chair, thinking intensely. You and [the_steph.title] wait while she comes to a decision."
    $ the_nora.draw_person(position = "sitting")
    the_nora "Okay, I'll help. But I'll need something in return."
    "You breath a sigh of relief."
    mc.name "Name it, I'll do what I can."
    the_nora "I have some effects that might be achievable, but I'm running into nothing but red tape getting them approved for human testing."
    the_nora "I will provide you with some of my research. I need you to develop it into a complete package, test it, and return the results to me."
    the_nora "Once I have your results back I'll give you my old notes, which should be enough to keep you moving forward."
    $ the_steph.draw_person(position = "sitting", emotion = "happy")
    the_steph "That's perfect, that's all I need."
    mc.name "We'll make it happen [the_nora.title]. Send the plans for the trait you need researched and we'll get started right away."
    $ the_nora.draw_person()
    "[the_nora.title] stands up and pushes her chair in."
    the_nora "I hope to hear from you soon. Good luck."
    "She hugs [the_steph.title] goodbye, and you go your separate ways."

    $ randomly_selected_trait = get_random_from_list(list_of_nora_traits)
    $ mc.business.event_triggers_dict["nora_trait_researched"] = randomly_selected_trait

    $ list_of_traits.append(randomly_selected_trait)
    $ randomly_selected_trait.researched = True
    $ the_steph.draw_person()
    "When you get back to the office [the_steph.title] has a new file detailing an untested serum trait."
    the_steph "Without [the_nora.title]'s research notes all we'll be able to do is put this trait into a serum and manufacture it."
    the_steph "You'll need to test a serum containing this trait on someone to raise it's mastery level."
    the_steph "We should bring it up to at least mastery level 2 before we go back to [the_nora.title]."

    mc.name "Understood. I'll be back once the testing is done."
    $ clear_scene()

    $ university_research_action = Action("Present your research to [nora.title].", nora_research_up_requirement, "nora_research_up_label", args = nora, menu_tooltip = "Deliver your field research to [nora.title] in exchange for her theoretical research notes.")
    $ mc.business.event_triggers_dict["nora_research_up"] = university_research_action
    $ university.actions.append(university_research_action)
    $ university.visible = True

    $ nora_research_visit = Action("Vist Nora's lab.", visit_lab_intro_requirement, "nora_research_cash_first_time", args = the_nora, requirement_args = the_nora,
        menu_tooltip = "Visit your old lab and talk to Nora about serum research.")

    $ university.actions.append(nora_research_visit) #Prepare this so if we visit the university again under the proper conditions we can start studying traits for her for money.

    $ mc.location.show_background()
    return

label nora_research_up_label(the_person):

    "You knock on the door to [the_person.title]'s lab and wait until the door is opened."
    $ the_person.draw_person()
    the_person "[the_person.mc_title], it's good to see you again."
    "She steps out of the office and close the door behind her."
    mc.name "You too. I've got something for you."
    "You hold out the folder containing the details of your testing."
    the_person "Good, wait here."
    $ clear_scene()
    "She slips back into the room and is gone for a couple of minutes."
    $ the_person.draw_person()
    "When she comes back out she has two large binders tucked under her arm."
    the_person "Let's go get a coffee and chat."

    $ the_person.draw_person(position = "sitting")
    "A short walk later and you're sitting in a small coffee shop near the center of campus. You slide your folder to [the_person.title] and she opens it eagerly."
    the_person "Hmmm. Interesting... Ah..."
    the_person "This is exactly the kind of information I wanted. Well done [the_person.mc_title]."
    "She slides her binders of notes over to you."
    $ the_person.change_love(3)
    the_person "I always thought you were destined for great things."
    $ mc.business.research_tier = 2
    $ mc.log_event("Tier 2 Research Unlocked","float_text_grey")
    the_person "I may have more testing for you to do soon. I'll get in touch when I do."
    "You finish your coffees and say goodbye. The notes [the_person.title] has given you provide all of the details you need to pursue a number of new serum traits."
    $ university.actions.remove(mc.business.event_triggers_dict.get("nora_research_up"))
    $ the_trait = mc.business.event_triggers_dict.get("nora_trait_researched")
    $ mc.business.event_triggers_dict["nora_trait_researched"] = None
    $ list_of_traits.remove(the_trait)
    $ list_of_nora_traits.remove(the_trait)
    $ nora.set_schedule(university, times = [1,2,3])
    $ clear_scene()


    # Prepare the event that triggers the next phase
    $ nora_research_cash_intro_action = Action("Nora cash research intro", nora_research_cash_intro_requirement, "nora_research_cash_intro", args = the_person, requirement_args = [the_person, day + renpy.random.randint(3,6)])
    $ mc.business.mandatory_crises_list.append(nora_research_cash_intro_action)

    return

label nora_research_cash_intro(the_person):
    # Nora calls you and enables the rest of the quest line. Doesn't give you the first trait yet, for that you need to visit her.
    "You get a call from [the_person.title]."
    mc.name "[the_person.title], good to hear from you. How can I help you."
    the_person "Hello [the_person.mc_title], I have some good news for you."
    the_person "I presented the research findings from your field tests to my section head."
    the_person "They were very impressed with my findings and have given my lab a grant to accelerate our work."
    the_person "Obviously, I won't be able to keep up with the pace they expect without some help from you."
    mc.name "So you're saying you have some more work for me."
    the_person "I do. Come by the lab when you have the time and I can give you the details and discuss payment."
    mc.name "I'll see when I have time in my schedule. Talk to you soon [the_person.title]."

    $ mc.business.event_triggers_dict["nora_cash_research_trigger"] = True
    return

label nora_research_cash_first_time(the_person):
    # The event for your first visit to see her to talk about being paid for your research. Can also trigger if you have research level 2 but nora_trait_researched is present (ie. you started her quest but never finished).
    "You knock on the door to the lab. [the_person.title] answers and steps out into the hallway to talk to you."
    $ the_person.draw_person()
    the_person "[the_person.mc_title], I'm glad you were able to come by. Let's walk and talk."
    $ university.show_background()
    "You walk upstairs together to make sure none of [the_person.possessive_title]'s co-workers are around."
    if mc.business.event_triggers_dict.get("nora_trait_researched", None) is None: #You don't have her first trait hanging around, so you've finished that quest line
        mc.name "So you have a serum trait for me to test?"
        the_person "I do. I have the details prepared for you to manufacture, and a section of the grant money set aside to pay for your work."
        the_person "Once your research findings are returned I can pay you a bounty of $2000 and provide you another trait to study."
        the_person "Do you find this acceptable?"
        "You think the offer over. It's a good amount of money for the amount of work, as long as you have someone to test these serums on."
        mc.name "I can make that work."
        the_person "Good. I'll send you the manufacturing details that we have prepared right away. Come and see me when your report is complete."
        $ the_trait = get_random_from_list(list_of_nora_traits)
        $ the_trait.researched = True
        $ mc.business.event_triggers_dict["nora_cash_research_trait"] = the_trait
        $ list_of_traits.append(the_trait)


    else:
        the_person "Do you have your finished research for me?"
        mc.name "I don't. My lab went in another direction and we found the breakthrough we were looking for."
        the_person "I see. I'm proud of you [the_person.mc_title], you seem very capable of turning theoretical science into practical results."
        the_person "I suppose this means we need to come to some sort of new arrangement then. If I cannot buy your services with research material I hope cash payment will do."
        the_person "If you finish your field research on the trait I provided you I can pay a bounty of $2000. I may also be able to provide another trait for you to study."
        the_person "Do you find this acceptable?"
        "You think the offer over. It's a good amount of money for the amount of work, as long as you have someone to test these serums on."
        mc.name "I can make that work."
        the_person "Glad to hear it. Come see me again when your research is complete."

        $ mc.business.event_triggers_dict["nora_cash_research_trait"] = mc.business.event_triggers_dict.get("nora_trait_researched") #The old research trait is now the cash goal trait
        $ mc.business.event_triggers_dict["nora_trait_researched"] = None #Clear this so we can use it as a flag to not show future events related to the research up quest.

    $ mc.business.event_triggers_dict["nora_cash_research_trigger"] = False #Reset this trigger so the event is hidden properly again in the future (TODO: Just remove it from the list)


    $ nora_research_cash_action = Action("Turn in your finished research.", nora_research_cash_requirement, "nora_research_cash", args = the_person, requirement_args = the_person,
        menu_tooltip = "Turn in your completed trait research to Nora, in exchange for payment.")

    $ university.actions.append(nora_research_cash_action)
    $ clear_scene()
    return

label nora_research_cash(the_person):
    # The event where you turn in a completed research report.
    if not emily.event_triggers_dict.get("tutor_introduced", False):
        $ emily.event_triggers_dict["tutor_introduced"] = True
        call student_intro_one(the_person, emily) from _call_student_intro_one

    else:
        "You knock on the door to the lab. [the_person.title] answers and steps out into the hallway to talk to you."
        $ the_person.draw_person()
        the_person "[the_person.mc_title], I'm glad you were able to come by. Let's walk and talk."
        $ university.show_background()
        "You walk upstairs together to make sure none of [the_person.possessive_title]'s co-workers are around."

    # TODO: The first intro bit returns here
    $ the_trait = mc.business.event_triggers_dict.get("nora_cash_research_trait") #We know won't be None from our initial event check.
    $ mc.business.event_triggers_dict["nora_cash_research_trait"] = None

    $ list_of_traits.remove(the_trait)
    $ list_of_nora_traits.remove(the_trait) #Clear it from Nora's list as well so it cannot be randomly obtained again.

    mc.name "I have your research report prepared. The effects of the trait you designed were... {i}interesting{/i}."
    "You hand her a folder you've put together containing the information you collected from your test subjects. She takes it and tuckes it under her arm."
    the_person "Thank you, I'll look through this later and send your payment if everything is in order."

    if list_of_nora_traits:
        #There are still items in the list, get one, give it to the player to study.
        the_person "I have another trait I would like studied, if you are still interested. I will send you the production details." #I'll mark the location of the setlement on your mp
        $ the_new_trait = get_random_from_list(list_of_nora_traits)
        $ mc.business.event_triggers_dict["nora_cash_research_trait"] = the_new_trait
        $ the_new_trait.researched = True
        $ list_of_traits.append(the_new_trait)
        mc.name "Okay, I'll see what I can do. Thank you for your business, [the_person.title]."
        "You say goodbye to [the_person.possessive_title] and split up. Your payment is sent soon after."

    else:
        #Unlock the boss trait phase
        the_person "I also have some good news. Thanks in part to your assistance I have been given a long term grant to continue my research."
        mc.name "Congratulations [the_person.title], after all your hard work you deserve it."
        the_person "Thank you. I had to pressure on my boss but I was able to... Well, I was able to convince him, let's leave it at that."
        the_person "This money relieves the pressure on me to produce results quickly, and means I will not need you to perform any more field tests."
        the_person "But I have an idea we may both benefit from."
        mc.name "Go on, you always have interesting ideas for me."
        the_person "In my studies I have found that people with extreme personalities, mindsets, backgrounds, or beliefs can offer insights into new serum traits."
        the_person "I will provide you with a detailed questionnaire. Have an intersting person fill it out, or interview them and fill it out yourself, and bring it back to me."
        the_person "If I find any hints pointing towards a trait I will share the research with you. I improve my research, and you may discover useful applications for your business."
        mc.name "That sounds like a good deal for both of us."
        the_person "My thoughts exactly, I'm glad you agree."
        "You say goodbye to [the_person.possessive_title] and split up. She sends your final payment and her research questionnaire soon after."

        $ study_person_action = Action("Study her for Nora. {image=gui/heart/Time_Advance.png}", study_person_requirement, "nora_profile_person",
            menu_tooltip = "Work through the research questionnaire provided to you by Nora. After you can give it to Nora to see if she notices any interesting properties.")
        $ mc.main_character_actions.append(study_person_action)

        $ turn_in_person_research_action = Action("Turn in a research questionnaire.", special_research_requirement, "nora_special_research", args = the_person, requirement_args = the_person,
            menu_tooltip = "Turn in the research questionnaire you had filled out. If the person is particularly unique or extreme she may be able to discover unqiue serum traits for you to research.")
        $ university.actions.append(turn_in_person_research_action)
    $ mc.business.funds += 2000
    $ clear_scene()
    return

label nora_special_research(the_person):
    # Bring a report about a special person to Nora and she generates a special serum trait for them.
    $ the_subject = mc.business.event_triggers_dict.get("nora_research_subject") #This is guaranteed to exist thanks to the pre action checks.

    mc.name "I have a research profile for you to take a look at [the_person.title]. Let me know if you can find anything interesting out."
    "You give [the_person.possessive_title] the report you have prepared on [the_subject.title]."
    the_person "Excellent. This shouldn't take too long to process, I just need to head to the lab and input the data."
    $ clear_scene()
    "[the_person.title] leaves for her lab. True to her word, she's back in less than half an hour with her findings in hand."
    $ the_person.draw_person()
    if mother_role in the_subject.special_role and the_subject.core_sluttiness > 75 and the_subject.love > 75 and nora_reward_mother_trait not in list_of_traits:
        the_person "This was certainly an interesting case, and I have a development for you."
        the_person "Your mother's responses indicate an intense level of devotion to you, to the point that she seems to derive almost sexual pleasure from your satisfaction."
        the_person "It may be possible to reverse the relationship in others, inspiring love in place of sexual attraction."
        "She hands you her research on the matter, unlocking a new serum trait for you to research."
        $ list_of_traits.append(nora_reward_mother_trait)

    elif sister_role in the_subject.special_role and the_subject.core_sluttiness > 75 and the_subject.obedience > 150 and nora_reward_sister_trait not in list_of_traits:
        the_person "This was certainly an interesting case, and I have a development for you."
        the_person "Your sister's responses seemed incredibly deferential, but she seemed to derive some sort of pleasure from the act."
        the_person "It may be possible to produce that association in others, with the effect increasing alongside their natural tendencies to obey."
        "She hands you her research on the matter, unlocking a new serum trait for you to research."
        $ list_of_traits.append(nora_reward_sister_trait)

    elif cousin_role in the_subject.special_role and the_subject.core_sluttiness > 75 and the_subject.love < -25 and nora_reward_cousin_trait not in list_of_traits:
        the_person "This was certainly an interesting case, and I have a development for you."
        the_person "This was your cousin, correct? I'm surprised to find such vitriol in such a close family member."
        the_person "Her hate of you brings her great pleasure, to the point that I believe she has a sexual link to it."
        the_person "I don't know how useful it would be, but I think this could be replicated in others with some research work."
        "She hands you her research on the matter, unlocking a new serum trait for you to research."
        $ list_of_traits.append(nora_reward_cousin_trait)

    elif aunt_role in the_subject.special_role and the_subject.core_sluttiness > 75 and nora_reward_aunt_trait not in list_of_traits:
        the_person "This was certainly an interesting case, and I have a development for you."
        the_person "Your aunt is a blank slate, ready for any sort of change. That would make her an ideal candidate to be affected by any number of other effects."
        the_person "If we could emulate that state of mind in others, you could safely add more serum traits to a single design."
        $ list_of_traits.append(nora_reward_aunt_trait)

    elif nora_role in the_subject.special_role and the_subject.core_sluttiness > 75 and nora_reward_nora_trait not in list_of_traits:
        the_person "Well I suppose your out-of-the-box thinking is why I appreciate your scientific input, [the_person.mc_title]."
        the_person "I ran your report on myself, and much to my suprise I think there may be something here for us both to study."
        the_person "My own sexual drive seems to be linked quite heavily to the intelligence of the person I am talking to."
        the_person "It may be possible to develop a serum that replicates this in another person, with the effect being more pronounced the larger the intelligence difference."
        "She hands you her research on the matter, unlocking a new serum trait for you to research."
        $ list_of_traits.append(nora_reward_nora_trait)

    elif pregnant_role in the_subject.special_role and the_subject.event_triggers_dict.get("preg_transform_day",day) < day and the_subject.core_sluttiness > 75 and nora_reward_hucow_trait not in list_of_traits:
        the_person "First off, congratulations [the_person.mc_title]. You're the father."
        the_person "Second, I have an interesting development and possible path forward."
        the_person "My testing has revealed a number of major differences between the test subject's hormonal balance and what is expected."
        the_person "I believe this is the bodies natural response to her noticeably intense desire for sexual satisfaction."
        the_person "If most women have a biological clock ticking, this one has a church bell."
        the_person "It may be possible to induce and amplify this hormonal response in others pre-impregnation."
        the_person "I would expect the results to be increased fertility, breast swelling, and very likely immediate lactation."
        the_person "Traditional birth control is also unlikely to affect this new hormonal balance, so it will be rendered ineffective."
        $ list_of_traits.append(nora_reward_hucow_trait)

    elif the_subject.love > 85 and nora_reward_high_love_trait not in list_of_traits:
        the_person "This was certainly an interesting case, and I have a development for you."
        the_person "The subject reported an intense love for you, to the exclusion of all others."
        the_person "Moral objections aside, this effect would have obvious appplications if you could find a way to apply it to others."
        "She hands you her research on the matter, unlocking a new serum trait for you to research."
        $ list_of_traits.append(nora_reward_high_love_trait)

    elif the_subject.love < -50 and nora_reward_low_love_trait not in list_of_traits:
        the_person "This was certainly an interesting case, and I have a development for you."
        the_person "I'm surprised you were able to convince the subject to produce any answers at all for you. She reported a burning, almost single minded hatred of you."
        the_person "I don't know how useful it will be, but with some further research work you may be able to replicate that level of absolute disgust in whomever you want."
        "She hands you her research on the matter, unlocking a new serum trait for you to research."
        $ list_of_traits.append(nora_reward_low_love_trait)

    elif the_subject.obedience > 180 and nora_reward_high_obedience_trait not in list_of_traits:
        the_person "This was certainly an interesting case, and I have a development for you."
        the_person "I'm not surprised you were able to extract such detailed information from the subject, her obedience to you seems to be almost complete."
        the_person "She seems content with her lack of independence, which you might be able to replicate and harness with some further research work."
        "She hands you her research on the matter, unlocking a new serum trait for you to research."
        $ list_of_traits.append(nora_reward_high_obedience_trait)

    elif the_subject.core_sluttiness > 100 and nora_reward_high_slut_trait not in list_of_traits:
        the_person "This was certainly an interesting case, and I have a development for you."
        the_person "Your subject was obviously very forthcoming with her sexual desires, but what I found interesting was how central to her personality they were."
        the_person "It may be possible to instill this same sexual confidence in others, if they have a budding tendency for it to start with."
        "She hands you her research on the matter, unlocking a new serum trait for you to research."
        $ list_of_traits.append(nora_reward_high_slut_trait)

    elif the_subject.int >= 7 and the_subjectisma >= 7 and the_subject.focus >= 7 and nora_reward_genius_trait not in list_of_traits:
        the_person "This was certainly an interesting case, and I have a development for you."
        the_person "Your subject was extremely competent, scoring near perfectly across the board on all intellectual tests."
        the_person "Replicating the capabilities of this amazing mind may be impossible with modern science, but it may be possible to approximate it for short periods of time."
        "She hands you her research on the matter, unlocking a new serum trait for you to research."
        $ list_of_traits.append(nora_reward_genius_trait)

    else:
        the_person "There doesn't seem to be anything of particular interest about your subject, unfortunately."

    $ mc.business.event_triggers_dict["nora_research_subject"] = None

    return

label nora_profile_person(the_person):
    if mc.business.event_triggers_dict.get("nora_research_subject", None) is not None:
        $ the_other_person = mc.business.event_triggers_dict.get("nora_research_subject")
        "Studying [the_person.title] will replace your information about [the_other_person.title]."
        menu:
            "Discard the report and continue.":
                pass

            "Keep the report on [the_other_person.title].":
                return


    if the_person.love < 0:
        "[the_person.title]'s obvious dislike of you makes it difficult to fill out the survey [nora.title] gave to you, but with a little guess work and some clever questions you fill it all in."
        "All that is left is to take it back to [nora.title] and to see if she finds anything interesting."

    else:
        mc.name "Do you have a few minutes, [the_person.title]? I have a few questions I was hoping you could answer for me."
        "You fill in all the information you already know about [the_person.possessive_title], then have her answer a few questions you were unsure about."
        "It takes some time, but soon you have completed [nora.title]'s research survey."
        "All that is left now is to take it back to her and see if she finds anything interesting."


    $ mc.business.event_triggers_dict["nora_research_subject"] = the_person
    $ clear_scene()
    call advance_time from _call_advance_time_24
    return
