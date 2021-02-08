##########################################
# This file holds all of the role requirements and labels for the head researcher role.
##########################################


init -2 python:
    #HEAD RESEARCHER ACTION REQUIREMENTS#
    def improved_serum_unlock_requirement(the_person): #If the person is with their R&D head in the research division during work hours and they meet the sluttiness requirements you can
        if mc.location != mc.business.r_div:
            return False
        elif not mc.business.is_open_for_business():
            return False
        elif mc.business.research_tier != 0:
            return False
        elif the_person.obedience < 110 or the_person.int < 3:
            return "Requires: 110 Obedience, 3 Intelligence"
        else:
            return True

    def advanced_serum_stage_1_requirement(the_person):
        if mc.business.event_triggers_dict.get("advanced_serum_stage_1",False):
            return False
        elif mc.location != mc.business.r_div:
            return False
        elif not mc.business.is_open_for_business():
            return False
        elif mc.business.research_tier != 1:
            return False
        elif the_person.obedience < 120 or the_person.core_sluttiness < 25 or the_person.int < 4:
            return "Requires: 120 Obedience, 4 Intelligence, " + get_gold_heart(25)
        else:
            return True

    def advanced_serum_stage_2_requirement(the_person,earliest_trigger_day):
        if mc.business.is_open_for_business():
            if day >= earliest_trigger_day:
                return True
        return False

    def advanced_serum_stage_3_requirement(the_person):
        if not mc.business.event_triggers_dict.get("advanced_serum_stage_3",False):
            return False
        elif mc.location != mc.business.r_div:
            return False
        elif not mc.business.is_open_for_business():
            return False
        elif mc.business.research_tier != 1:
            return False
        elif the_person.obedience < 120 or the_person.int < 4:
            return "Requires: 120 Obedience, 4 Intelligence"
        else:
            return True

    def futuristic_serum_stage_1_requirement(the_person):
        if mc.business.event_triggers_dict.get("futuristic_serum_stage_1",False):
            return False
        elif mc.location != mc.business.r_div:
            return False
        elif not mc.business.is_open_for_business():
            return False
        elif mc.business.research_tier != 2:
            return False
        elif the_person.obedience < 140 or the_person.core_sluttiness < 50 or the_person.int < 5:
            return "Requires: 140 obedience, 5 Intelligence, " + get_gold_heart(50)
        else:
            return True

    def futuristic_serum_stage_2_requirement(the_person):
        if not mc.business.event_triggers_dict.get("futuristic_serum_stage_1",False):
            return False
        elif mc.location != mc.business.r_div:
            return False
        elif not mc.business.is_open_for_business():
            return False
        elif mc.business.research_tier != 2:
            return False
        elif the_person.obedience < 140 or the_person.core_sluttiness < 50 or the_person.int < 5:
            return "Requires: 140 obedience, 5 Intelligence, " + get_gold_heart(50)
        else:
            return True

    def fire_head_researcher_requirement(the_person): #Remove the person as your head researcher.
        return True

    def visit_nora_intro_requirement(the_person):
        if steph_role not in the_person.special_role: #Only Stephanie gets to have this event trigger while she is head researcher.
            return False
        elif not mc.business.event_triggers_dict.get("intro_nora", False):
            return False
        elif mc.location != mc.business.r_div:
            return False
        elif not mc.business.is_open_for_business():
            return False
        elif mc.business.research_tier != 1: #This event is used to get to tier 2, so if you're already past that it doesn't matter.
            return False
        elif the_person.love < 15:
            return "Requires: 15 Love"
        else:
            return True


#####HEAD RESEARCHER ACTION LABELS#####

label fire_head_researcher(the_person):
    mc.name "[the_person.title], I need to talk to you about your role as my head researcher."
    the_person "Yes?"
    mc.name "I've decided that the role would be better filled by someone else. I hope you understand."
    if the_person.int > 2:
        $ the_person.change_happiness(-5)
        $ the_person.change_obedience(-1)
        $ the_person.draw_person(emotion="sad")
        the_person "I... I'm sorry I couldn't do a better job. Good luck filling the position, sir."
    else:
        $ the_person.draw_person(emotion="happy")
        the_person "Whew, I found all that science stuff super confusing to be honest. I hope whoever replaces me can do a better job at it!"
    $ the_person.remove_role(head_researcher)
    $ mc.business.head_researcher = None
    return

label improved_serum_unlock_label(the_person):
    $ the_person.call_dialogue("improved_serum_unlock") #In which the player introduces the idea of advancing the lab's research and the head researcher offers to test serum on themselves.
    menu:
        "Assist [the_person.title]":
            mc.name "I think you're right, this is the only way forward. What do you need me to do?"
            "[the_person.title] opens the door to one of the small offices attached to the reserach lab. The two of you step inside and she closes the door."
            the_person "First, we're going to need a test dose of serum."
            call give_serum(the_person) from _call_give_serum_6
            if not _return:
                mc.name "I don't have any with me right now. I'll stop by the production division and pick some up."
                the_person "Come see me when you do. I'll be waiting."
            else:
                "You pull out the vial of serum and present it to [the_person.title]. She takes the vial and holds it up to the light, then opens it up and drinks the content."
                the_person "No going back now. I'm going to need you to take notes for me - about me I suppose."
                "There's a pad of paper and a pen on the desk already. You pick it up, click the pen, and turn to a fresh page."
                mc.name "Let's start with the basics. How did it taste?"
                the_person "Hmm, a little sweet, then bitter towards the end."
                mc.name "Was it an overpowering taste?"
                the_person "Not particularly, no."
                "You scribble down [the_person.possessive_title]'s name at the top of your notes page then add some bullet points listing her responses."
                mc.name "My old research suggested that these serums could make people more suggestable. Do you feel like you are more suggestable than normal?"
                "[the_person.title] thinks for a moment before responding."
                the_person "Maybe? No? God, that's hard question to answer objectively, isn't it?"
                if mc.charisma > 4:
                    "You take a keen look at [the_person.title]. She might not be able to tell but you certainly can. You mark her down as \"Highly Suggestible\"."
                else:
                    "You can't tell any better than [the_person.title]. You put down \"Suggestability Uncertain\" on your notepad."
                mc.name "That's fine, you're doing great."
                mc.name "Next question: Early research has suggested that our serums might deliver performance enhancing effects. What do you think about this?"
                the_person "Well, I think I need to know more about it. I suppose that's why I'm doing this - to learn more."
                mc.name "I think we should take advantage of these effects. You agree with me, correct?"
                the_person "I... Yes, I agree with you sir."
                "[the_person.title]'s eyes are fixed firmly on yours. This seems like a good chance to impress upon her your goals for the company."
                menu:
                    "Stress the importance of obedience. (tooltip)Likely to raise her obedience.":
                        mc.name "A highly organised workplace is important, especially in a lab setting. I need employees who are able to listen to my instructions and follow them."
                        "[the_person.possessive_title] nods in agreement."
                        mc.name "As the leader of the research team I need you to be especially loyal. Do you understand?"
                        $ the_person.change_obedience(10)
                        the_person "Yes, absolutely. I'll do everything I can to make sure this business is successful."

                    "Stress the importance of appearance. (tooltip)Likely to raise her sluttiness.":
                        mc.name "Impressions are key in this line of business, and I need my employees dressed to impress."
                        "[the_person.possessive_title] nods in agreement."
                        mc.name "As the leader of the research team I need you to be especially aware of your appearance. You represent everything our technology can achieve. Do you understand?"
                        $ the_person.change_slut_temp(5)
                        $ the_person.change_slut_core(5)
                        the_person "Yes, absolutely. I'll make sure I always leave a positive impression."

                    "Stress the importance of satisfaction. (tooltip)Likely to dramatically raise her happiness.":
                        mc.name "It can be easy to burn yourself out in this line of business. Pay might not always be great and the hours might be long, but a good attitude is key."
                        "[the_person.possessive_title] nods in agreement."
                        mc.name "Your attitude is going to affect the rest of the research team. I need you to be as positive as possible, do you understand?"
                        $ the_person.change_happiness(10)
                        the_person "Yes sir, I understand completely. I'll try and be as chipper as possible."

                    "Stress the importance of your relationship. (tooltip)Likely to raise her love for you.":
                        mc.name "Through everything we're going to do together I want you to know that your friendship means the world to me."
                        mc.name "I need you to stick by my side throught it all."
                        $ the_person.change_love(5)
                        "[the_person.possessive_title] nods in agreement."
                        the_person "Yes, absolutely. Our friendship means everything to me too."

                mc.name "Good to hear it."
                "You ask [the_person.title] a few more questions, recording her observations and noting down a few of your own. Half an hour passes before you're finished."
                the_person "Thank you for your help [the_person.mc_title], that was an... interesting experience. It might take some work, but I think I know where we should focus our research efforts."
                $ mc.business.research_tier = 1
                $ mc.log_event("Tier 1 Research Unlocked", "float_text_grey")
                "[the_person.title] takes your notes and returns to the R&D department."
                call advance_time from _call_advance_time_8

        "Do not allow the test.":
            mc.name "I'll think about it, but I would like to avoid self experimentation if possible."
            the_person "If you change your mind let me know. Until then I will do my best with what little knowledge we have available."

    return

label advanced_serum_stage_1_label(the_person):
    $ the_person.draw_person()
    mc.name "[the_person.title], the research department has been doing an incredible job lately. I wanted to say thank you."
    $ the_person.draw_person(emotion = "happy")
    the_person "Thank you sir, it's been my pleasure. It's my job after all."
    mc.name "On the topic of research: I was wondering if there was anything you needed here to push your discoveries even further."
    "[the_person.possessive_title] thinks for a moment."
    the_person "We have everything we need for our basic research, but our theoretical work has hit a wall."
    mc.name "Tell me what you need and I'll do what I can."
    the_person "Well, I've seen a few papers floating around that make it seem like other groups are working with the same basic techniques as us."
    the_person "I'd like to reach out to them and see about securing a prototype of some sort, to see if we can learn anything from its effects."
    the_person "These academic types can get very defensive about their research, so I don't think we'll get anything for free."
    if steph_role in the_person.special_role and not mc.business.event_triggers_dict.get("intro_nora", False):
        the_person "I suppose there's one person we could ask..."
        mc.name "Do you mean [nora.title]?"
        "[the_person.title] nods."
        the_person "When I left the university was cracking down on her research and trying to keep it private. I know she hated that."
        the_person "Getting her help could save us a lot of money, and it would be nice to see her again."
    menu:
        "Try and secure a prototype serum.\n{size=22}Costs $2000{/size}" if mc.business.funds >= 2000:
            $ mc.business.funds += -2000
            mc.name "That sounds like a good lead. I'll make sure the funds are allocated, let me know when you have something to show me."
            the_person "Absolutely sir, you'll know as soon as I know something."
            $ random_day = day + renpy.random.randint(2,4)
            $ mc.business.event_triggers_dict["advanced_serum_stage_1"] = True
            $ advanced_serum_unlock_stage_2 = Action("Advanced serum unlock stage 2",advanced_serum_stage_2_requirement,"advanced_serum_stage_2_label", args = the_person, requirement_args = [the_person, random_day])
            $ mc.business.mandatory_crises_list.append(advanced_serum_unlock_stage_2) #Append it to the mandatory crisis list so that it will be run eventually. We will list the person and the random day that the event will finish.

        "Try and secure a prototype serum.\n{size=22}Costs $2000{/size} (disabled)" if mc.business.funds < 2000:
            pass

        "Contact Nora."if steph_role in the_person.special_role and not mc.business.event_triggers_dict.get("intro_nora", False) and mc.business.event_triggers_dict.get("nora_trait_researched",None) is None:
            $ mc.business.event_triggers_dict["intro_nora"] = True
            mc.name "I think [nora.title] is the right choice."
            the_person "I'll call and see when she's available. Come back and talk to me when you want to go visit her."

        "Wait until later.":
            mc.name "Funds are tight right now. I'll try and secure them for you, but until do what you can with the resources you have."
            the_person "Understood. Come by and visit any time."

    return

label advanced_serum_stage_2_label(the_person):
    #TODO: Add a special section where the head researcher aknowledges the work of her predecesor if the person who is handed over here is not the head researcher any more.
    if mc.location != mc.business.r_div:
        "Your phone buzzes, alerting you to a work email."
        the_person "I have news about the prototype serum you asked me to retrieve. Meet me in the R&D department when you have a moment."
        "You finish up what you were working on and head over to meet [the_person.title]."
        $ mc.change_location(mc.business.r_div)
        $ mc.business.r_div.show_background()
        $ the_person.draw_person()
        mc.name "What's the news [the_person.title]?"

    else:
        $ mc.business.r_div.show_background()
        the_person "Excuse me, [the_person.mc_title]?"
        $ the_person.draw_person()
        the_person "I have some news about that prototype serum you asked me to retrieve. Can I have a moment?"
        mc.name "Of course."
    "[the_person.title] nods towards one of the small offices attached to the lab. You follow her inside and shut the door after yourself."
    the_person "I was able to get in touch with a small research team that was doing some work paralleling our own, and after some sweet talking I got my hands on this..."
    if the_person.outfit.get_lower_ordered(): #Use this as a proxy to see if she is wearing something on her lower body.
        "She reaches into a pocket and pulls out small brown tinted vial, corked with a rubber stopper."
    else:
        "She grabs a small brown tinted vial off of the table and shows it to you. It's corked with a rubber stopper."
    mc.name "Excellent work [the_person.title]. Reverse engineering it is our next step then, correct?"
    the_person "I've set aside enough for a thorough chemical analysis, but I doubt that will give us a complete picture."
    mc.name "What do you suggest we do then?"
    the_person "With your permission I'd like to test it on myself. We can record the results, and I'll look over them after. With some luck I should learn enough to push our research forward."
    #TODO: Give you the option to test on someone else in your R&D division.
    mc.name "I agree, this seems like our most likely way forward."
    the_person "I'm glad you agree. Okay, I don't know what effect this will have on me so I want to record it."
    "[the_person.title] leaves the room for a moment, then returns with a small tripod. She mounts her phone on it and sets it up on the table facing both of you."
    "When she turns back she hands a second vial of liquid over to you. This one is in the familiar labware you use every day."
    the_person "I prepared this just in case, it counteracts any effects of the prototype serum. Use it if something is going wrong, but remember this might be the only chance we get to try this."
    "You take the second vial of serum and tuck it in your back pocket."
    mc.name "Are you ready?"
    "[the_person.possessive_title] nods. She starts her phone recording and looks into the lens."
    the_person "I'm [the_person.title], head researcher at [mc.business.name]. The following are the effects of the prototype serum we have secured."
    "She takes the rubber stopper off of the vial and swirls the content. After a steadying breath and glance at you she drinks it all down."
    the_person "Bleh... The taste isn't anything to write home about."
    "[the_person.title] puts the container on the table and waits for a few seconds while the serum takes full effect. You watch carefully, studying her reaction."
    $ old_int = the_person.int
    "As you watch her pupils dilate, her breathing slows and becomes more regular, and her gaze settles dead ahead."
    mc.name "How are you feeling [the_person.title]?"
    the_person "Fine. A little warm maybe."
    $ the_person.draw_person(emotion="happy")
    "She looks at you and smiles, then laughs self consciously."
    $ the_person.change_happiness(15)
    the_person "I don't know why I was so worried about this, I feel silly getting you so involved. This feels fine."
    $ the_person.change_slut_core(5)
    $ slut_report = the_person.change_slut_temp(10)
    the_person "I mean, not that I mind the help of such a good looking man."
    "She giggles and looks you up and down."
    mc.name "Try and focus [the_person.title], do you notice any unusual with yourself right now?"
    the_person "With me? Why would... Oh right, because of the test! Sorry, you're just so... distracting."
    $ the_person.change_int(-1)
    $ the_person.change_slut_core(10)
    $ slut_report = the_person.change_slut_temp(20)
    "She bites her lip and takes a step closer. You notice her cheeks are flush and her breathing is getting a little heavier."
    the_person "Ugh, [the_person.mc_title] do we really have to do this right now? Couldn't we be doing something more fun? I can think of a ton of fun things we could do together."
    $ the_person.change_int(-1)
    $ the_person.change_slut_core(10)
    $ slut_report = the_person.change_slut_temp(20)
    $ old_personality = the_person.personality
    $ the_person.personality = bimbo_personality
    $ mc.log_event("[the_person.title]: Personality changed. Now: Bimbo", "float_text_pink")
    "[the_person.title] reaches her hand down to your waist and runs her fingers along your cock through your pants."
    menu:
        "Have sex with [the_person.title].":
            "You smile back at [the_person.title]. She lets out a happy giggle when you wrap your arms around her waist."
            $ the_person.change_int(-1)
            call fuck_person(the_person) from _call_fuck_person_8
            $ the_report = _return
            if the_report.get("girl orgasms", 0) > 0:
                $ the_person.change_obedience(10)
                the_person "Oh... my... god... [the_person.mc_title] that felt so good! If you could make me feel like that all the time I swear I would do anything for you. Anything at all."
            else:
                "[the_person.possessive_title] giggles softly."
                the_person "Ahh, that was a lot of fun [the_person.mc_title]. I really want to give that another try, maybe once you've had a chance to recharge."

            "It's been a few minutes since [the_person.title] took the dose of prototype serum. Besides the obvious spike in arousal she seems more carefree and eager to please you."
            "Even her tone of voice has changed; She's practically bubbling over with excitement right now. She certainly doesn't seem like the intelligent research head you've come to rely on though."

            menu:
                "Give [the_person.title] the reversal serum.":
                    $ had_sex = True
                    pass #This falls through to the previous section.

                "Leave [the_person.title] the way she is.":
                    "You think about giving [the_person.title] the reversal serum but decide against it. You aren't sure if the serum effects will wear off, but she seems happy enough as she is."
                    "[the_person.title] certainly doesn't seem like she's in any state to run your research department. It would be a good idea to pick a successor to continue [the_person.title]'s work."
                    mc.name "Okay [the_person.title], we're all done here."
                    "Her eyebrows knit together, like a child's attempt to concentrate."
                    the_person "I... wasn't there something I was suppose to do first? Or have done? Uh... I'm sorry [the_person.mc_title], I'm having a real hard time thinking right."
                    "She sticks out her tounge, then giggles and shrugs."
                    the_person "Oh well, how important can it be, right? Glad I could help you with your science. And all that fun other stuff."
                    mc.name "And thank you for all that help."
                    "[the_person.possessive_title] gives you a wink and leaves the room. "
                    $ clear_scene()
                    "You take [the_person.title]'s phone off of it's tripod and make a copy of the footage it took. Maybe your next head researcher can make use of this to figure out how to press forward."
                    $ mc.business.event_triggers_dict["advanced_serum_stage_3"] = True #Flag the next event to be enabled.
                    $ mc.business.event_triggers_dict["research_bimbo"] = the_person
                    return

        "Give [the_person.title] the reversal serum.":
            $ had_sex = False
            pass

    #Undo the effects of the serum, we will use a special exit if we leave her as she is.
    mc.name "Okay [the_person.title], I think we should wrap this little experiment up. I need you to drink this for me."
    "You grab the reversal serum from your back pocket and hand it over. [the_person.title] pouts and looks at you."
    $ the_person.draw_person(emotion="sad")
    the_person "Aww, do I have to? I really like the way I feel right now."
    mc.name "Drink up."
    "She frowns but does as she's told. She drinks the content of the vial."
    $ int_to_add = old_int - the_person.int #Calculate what we need to add back, almost certainly 3 but wierd things might happen.
    $ the_person.change_int(int_to_add)
    $ the_person.change_slut_core(-25)
    $ the_person.change_slut_temp(-50)
    $ the_person.change_happiness(-15)
    # $ the_person.remove_status_effects([bliss,ditzy])
    $ the_person.personality = old_personality
    $ mc.log_event("[the_person.title]: Suggestability removed.", "float_text_blue")
    $ mc.log_event("[the_person.title]: - Ditzy", "float_text_blue")
    $ mc.log_event("[the_person.title]: - Blissful", "float_text_blue")
    $ mc.log_event("[the_person.title]: Personality Restored", "float_text_blue")
    "After another moment [the_person.title] shakes her head and looks at you. She seems suddenly more alert, more aware."
    the_person "Ugh, that's given me a serious headache. I'm not sure if I should blame their stuff or mine."
    mc.name "Glad to have you back. Are you feeling like yourself again?"
    the_person "Yeah, I think so. I mean, it's a little hard to say I guess."
    "[the_person.title] grabs her phone and unclips it from the short tripod it was on."
    if had_sex:
        the_person "Well I guess we have plenty of evidence that the prototype affects inhibition and arousal."
        mc.name "Sorry about that, I just..."
        $ slut_report = the_person.change_slut_temp(5)
        the_person "No, I was literally throwing myself at you, I understand. It was fun, honestly."
        "She looks at her phone for a moment, then back up at you."
        the_person "And you managed to keep it all in frame. That should help me break down the effects piece by piece."

    else:
        the_person "About what I said before, while I was... you know. Thank you for not taking advantage of it."
        $ the_person.change_obedience(5)
        $ the_person.change_happiness(5)
        $ the_person.change_love(5)
        mc.name "Of course, I understand that you weren't yourself. I'm glad to have you're back to normal."
        "She looks at her phone for a moment, then back up at you."
        the_person "I'll have to go over the footage in more detail, but I think I'll be able to break the effects down piece by piece from this."
    the_person "Obviously I can't make any promises, but between this and the chemical analysis I think we have a good shot at recreating the basic creation techniques used."
    the_person "I'm going to go take a break, but stop by later if you want me to change our research focus and look into this more."
    $ mc.log_event("Tier 2 Research Unlocked","float_text_grey")
    $ mc.business.research_tier = 2
    return

label advanced_serum_stage_3_label(the_person):
    #This event can only come up when the player has chosen to keep their head researcher a bimbo. It makes sure they can still reach the second tier of research.
    mc.name "[the_person.title], I have some experimental footage I need you to look at."
    the_person "Hmm? What is it about?"
    $ old_researcher = mc.business.event_triggers_dict["research_bimbo"] #Get the old researcher so we can call her name.
    if mc.business.get_employee_workstation(old_researcher):
        mc.name "I'm sure you've seen [old_researcher.name] around the office? She use to be my head of research and insisted she try a prototype serum she had located."
        the_person "She use to lead the R&D team?"
        mc.name "Just look at this, it will all make sense."
    else:
        mc.name "A previous head of research insisted she try a prototype serum she had located. These were the test results."
    "You hand [the_person.title] a thumb drive containing the footage of your test session with [old_researcher.name]. She plugs the drive into her computer and opens up the footage."
    $ slut_report = the_person.change_slut_temp(5)
    the_person "Oh my god... it's like something flipped a switch inside of her."
    "[the_person.title] watches as [old_researcher.name] steps close to you and reaches down to grab your crotch."
    mc.name "As far as I can tell the effects are permanent. It's unfortunate, but I know she wouldn't want us to let all of her research go to waste."
    the_person "I... I understand sir. I'll pull apart what I can and list out some preliminary theories."
    $ mc.business.research_tier = 2
    $ mc.log_event("Tier 2 Research Unlocked", "float_text_grey")

    return

label futuristic_serum_stage_1_label(the_person):
    mc.name "[the_person.title], what do you think about the current state of our R&D? Is there anything we could be doing better?"
    the_person "We seem to be pressed right up against the boundry of knowledge for medical science. Before we can come up with anything new we need data, and there just isn't any."
    the_person "What I need right now are test subjects. Girls who have taken a few doses of serum and been affected by it. If we can do that I can build up some data and maybe discover something new."
    mc.name "It's probably best these girls come from inside the company. How many test subjects do you need?"
    the_person "Not including me: three. I'll need them to be obedient and open to... intimate testing procedures."
    "[the_person.title] requires three employees who satisfy the following requirements: Core Sluttiness 50+ and Obedience 130+."
    mc.name "Alright [the_person.title], I'll do what I can. I'll come back when I've got some girls who fit your requirements."
    $ mc.business.event_triggers_dict["futuristic_serum_stage_1"] = True
    return

label futuristic_serum_stage_2_label(the_person):
    if __builtin__.len(mc.business.get_requirement_employee_list(core_slut_required = 50, obedience_required = 130)) <= 3: # If you don't have enough people who meet the requirements just get an update.
        mc.name "I'm still working on getting your test subjects ready. Could you remind me what you need?"
        the_person "To learn anything useful I need at least three girls who have been seriously affected by our serums. I need them to be obedient and open to some intimate testing procedures."
        "[the_person.title] requires three employees who satisfy the following requirements: Core Sluttiness 50+ and Obedience 130+"
        $ satisfying_list = mc.business.get_requirement_employee_list(core_slut_required = 50, obedience_required = 130, exclude_list = [the_person])
        $ my_string = "The following people currently satisfy the requirements: "
        python:
            if satisfying_list:
                for person in satisfying_list:
                    my_string += person.name + " " + person.last_name + ", "
            else:
                my_string = "There is currently nobody in your company who meets these requirements."
        "[my_string]"
        the_person "Noted. I'll get back to you when I have your test subjects ready."
        return

    mc.name "[the_person.title], I have your group of test subjects ready."
    the_person "Excellent, let me know who to call down and I'll begin as soon as possible."
    $ possible_picks = mc.business.get_requirement_employee_list(core_slut_required = 50, obedience_required = 130, exclude_list = [the_person])
    call screen employee_overview(white_list = possible_picks, person_select = True)
    $ pick_1 = _return
    call screen employee_overview(white_list = possible_picks, black_list = [pick_1], person_select = True)
    $ pick_2 = _return
    call screen employee_overview(white_list = possible_picks, black_list = [pick_1,pick_2], person_select = True)
    $ pick_3 = _return
    "[the_person.title] looks over the files of the employees you suggested and nods approvingly."
    the_person "I think they will do. You're sure you want me to bring in [pick_1.name], [pick_2.name], and [pick_3.name] for testing?"
    menu:
        "Begin the testing.":
            pass

        "Reconsider.":
            mc.name "On second thought, I don't think I want them involved. I'll think about it and come back."
            the_person "I'll be here."
            return

    mc.name "Yes, you may begin."
    $ the_person.draw_person(emotion = "happy")
    the_person "Excellent!"
    "[the_person.title] gets her phone out and calls all three girls down to the lab. It doesn't take long for them all to assemble."
    $ go_first = pick_1
    if pick_2.obedience > go_first:
        $ go_first = pick_2
    if pick_3.obedience > go_first:
        $ go_first = pick_3
    $ the_group = GroupDisplayManager([the_person, pick_1, pick_2, pick_3], primary_speaker = the_person)
    $ clear_scene()
    $ the_group.draw_group()
    the_person "The testing might take some time sir, I'll get started right now and have all my findings recorded. Come by later and we can review any discoveries."
    "[the_person.title] turns to the other girls."
    the_person "Well then, we have some special testing to get through today! Who would like to go first?"
    "[go_first.name] raises her hand. [the_person.title] smiles and grabs her clipboard."
    the_person "Very good. Come with me, you two can wait here until we're done."
    "[the_person.title] leads [go_first.title] into a side office, and you decide to leave her to her work."
    #TODO: Expand this event for more sexy stuff.
    $ mc.business.research_tier = 3
    $ mc.log_event("Max Research Tier Unlocked", "float_text_grey")
    $ clear_scene()
    call advance_time from _call_advance_time_9
    return
