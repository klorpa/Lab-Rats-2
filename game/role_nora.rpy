# All of the role specific actions for Nora
# Nora acts as an alternate way of unlocking serum research progress and allows the player to unlock special serum traits.

# Nora needs the player to help her cut through beurocratic red tape and test serum traits that she can't.
# She gives the player (temporary) access to a serum trait with a very high side effect chance, strange/extreme effects, and minimal sale value.
# The player needs to raise the mastery value of the trait to a certain level, after which they can "turn in" the request for a reward.
# Initially this reward will be acces to higher serum tech tiers or unlocks of other serum traits without having to research them.
# Later it may let you unlock unique serum traits.



#Pre starting Nora's events you talk to Steph for your lvl 2 serum advance. She says you'll either need a lot of cash OR you can talk to Nora.
#TODO: Add a lab submap and make the submap system more robust.
#You go to her lab and talk to her there,

init -2 python:
    def nora_research_up_requirement():
        if mc.business.research_tier != 1:
            return False
        elif time_of_day== 0:
            return "Too early to visit [nora.title]."
        elif time_of_day == 4:
            return "Too late to visit [nora.title]."
        elif round(nora_suggest_up.mastery_level) < 2:
            return "Trait Mastery Level of [nora_suggest_up.name] must be 2 or higher."
        else:
            return True



label nora_intro_label(the_steph):
    $ the_nora = nora
    $ mc.business.event_triggers_dict["intro_nora"] = False #We've already intro'd her, so we don't have to do this again.
    mc.name "[the_steph.title], have you talked to [the_nora.title] yet?"
    "She nods."
    the_steph.char "I did, she said we would be welcome by any time."
    mc.name "Excellent, I want to pay her a visit and want you to come along."
    the_steph.char "Sure thing. It's going to be strange being back there, but I'm looking forward to it!"
    "The two of you head to the university. Being on campus again triggers a wave of nostalgia that you hadn't expected."

    # TODO: Change location (add background)
    "You navigate to the old lab and knock on the door. You hear the click of high heels approaching from the other side."
    "Your old lab director opens the door and smiles at you and [the_steph.title]. Inside the room is bustling with activity."
    $ the_nora.draw_person(emotion = "happy")
    the_nora.char "[the_nora.mc_title], [the_steph.title], I'm glad you stopped by."
    mc.name "It's nice to see you [the_nora.title]."
    $ the_steph.draw_person(emotion = "happy")
    the_steph.char "Hey [the_nora.title]. Good to be back."
    $ the_nora.draw_person(emotion = "happy")
    "[the_nora.possessive_title] steps out into the hallway and closes the lab door behind her."
    the_nora.char "I'm sorry I can't invite you in; the lab is a high security space now."
    the_nora.char "The university has gotten very protective of my work since you left."
    "She sounds frustrated with the situation."
    the_nora.char "Anyway, I know you aren't here for an earful about academic politics. You had a problem you needed help with?"
    mc.name "We did, but it might take a while to explain. How about I buy us a round of coffees and we talk about it upstairs."
    the_nora.char "The two of you have piqued my interest, lead the way."

    #TODO: Change the background
    "The three of you return to ground level and go to a coffee shop near the center of campus."
    $ the_nora.draw_person(position = "sitting")
    "When you get there [the_steph.title] pulls out a folder containing a synopsis of your research and slides it over to [the_nora.title]."
    "[the_nora.possessive_title] looks through the notes, sipping thoughtfully at her coffee."
    the_nora.char "Hmm... Yes... Ah, I see what's going on. I ran into this same roadblock."
    $ the_steph.draw_person(position = "sitting")
    the_steph.char "Excellent, so you know where to go from here?"
    "[the_nora.title] looks up from her notes."
    $ the_nora.draw_person(position = "sitting")
    the_nora.char "Do I know? Of course! I haven't just been twiddling my thumbs since you two left!"
    the_nora.char "The problem is that all of my research is suppose to be kept within the university now. No sharing with outside organisations."
    the_nora.char "I wish I could help, but it's my job at risk."
    mc.name "Come on [the_nora.title], we're counting on you here."
    $ the_steph.draw_person(position = "sitting")
    the_steph.char "Think of the science, we shouldn't let bureaucrats get in the way of progress! That's what you always taught me, at least."
    "She leans forward in her chair, thinking intensely. You and [the_steph.title] wait while she comes to a decision."
    $ the_nora.draw_person(position = "sitting")
    the_nora.char "Okay, I'll help. But I'll need something in return."
    "You breath a sigh of relief."
    mc.name "Name it, I'll do what I can."
    the_nora.char "I have some effects that might be achievable, but I'm running into nothing but red tape getting them approved for human testing."
    the_nora.char "I will provide you with some of my research. I need you to develop it into a complete package, test it, and return the results to me."
    the_nora.char "Once I have your results back I'll give you my old notes, which should be enough to keep you moving forward."
    $ the_steph.draw_person(position = "sitting", emotion = "happy")
    the_steph.char "That's perfect, that's all I need."
    mc.name "We'll make it happen [the_nora.title]. Send the plans for the trait you need researched and we'll get started right away."
    $ the_nora.draw_person()
    "[the_nora.title] stands up and pushes her chair in."
    the_nora.char "I hope to hear from you soon. Good luck."
    "She hugs [the_steph.title] goodbye, and you go your separate ways."

    #TODO: Change your location back to the lab.
    $ list_of_traits.append(nora_suggest_up)
    $ nora_suggest_up.researched = True


    #TODO: Assign a nora serum trait
    "When you get back to the office [the_steph.title] has a new file detailing an untested serum trait."
    the_steph.char "Without [the_nora.title]'s research notes all we'll be able to do is put this trait into a serum and manufacture it."
    the_steph.char "You'll need to test a serum containing this trait on someone to raise it's mastery level."
    the_steph.char "We should bring it up to at least mastery level 2 before we go back to [the_nora.title]."

    mc.name "Understood. I'll be back once the testing is done."

    $ university_research_action = Action("Present your research to [nora.title].", nora_research_up_requirement, "nora_research_up_label", args = nora, menu_tooltip = "Deliver your field research to [nora.title] in exchange for her theoretical research notes.")
    $ mc.business.event_triggers_dict["nora_research_up"] = university_research_action
    $ university.actions.append(university_research_action)
    $ university.visible = True

    return

label nora_research_up_label(the_person):
    #TODO: Change background to lab
    "You knock on the door to [the_person.title]'s lab and wait until the door is opened."
    $ the_person.draw_person()
    the_person.char "[the_person.mc_title], it's good to see you again."
    "She steps out of the office and close the door behind her."
    mc.name "You too. I've got something for you."
    "You hold out the folder containing the details of your testing."
    the_person.char "Good, wait here."
    $ renpy.scene("Active")
    "She slips back into the room and is gone for a couple of minutes."
    $ the_person.draw_person()
    "When she comes back out she has two large binders tucked under her arm."
    the_person.char "Let's go get a coffee and chat."
    #TODO: Change background back.
    $ the_person.draw_person(position = "sitting")
    "A short walk later and you're sitting in a small coffee shop near the center of campus. You slide your folder to [the_person.title] and she opens it eagerly."
    the_person.char "Hmmm. Interesting... Ah..."
    the_person.char "This is exactly the kind of information I wanted. Well done [the_person.mc_title]."
    "She slides her binders of notes over to you."
    $ the_person.change_love(3)
    the_person.char "I always thought you were destined for great things."
    $ mc.business.research_tier = 2
    $ mc.log_event("Tier 2 Research Unlocked","float_text_grey")
    the_person.char "I may have more testing for you to do soon. I'll get in touch when I do."
    "You finish your coffees and say goodbye. The notes [the_person.title] has given you provide all of the details you need to pursue a number of new serum traits."
    #TODO: Add Nora to the university location schedule.
    $ university.actions.remove(mc.business.event_triggers_dict.get("nora_research_up"))
    $ list_of_traits.remove(nora_suggest_up)
    $ nora.set_work([1,2,3], university)
    $ renpy.scene ("Active")
    return
