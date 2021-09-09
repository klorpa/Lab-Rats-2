### All of the event stuff specific to getting Lily to be your girlfriend.
init -2 python:
    def sister_girlfriend_ask_blessing_requirement(the_person): #This is an action that Mom has
        if the_person.event_triggers_dict.get("sister_girlfriend_ask_blessing", False):
            return True
        else:
            return False

    def sister_girlfriend_return_requirement(the_person): #This is an action Lily has, enabled when you've talked to Mom
        if the_person.event_triggers_dict.get("sister_girlfriend_mom_blessing_given", None) is None:
            return False
        elif the_person.event_triggers_dict.get("sister_girlfriend_waiting_for_blessing", False) and the_person.event_triggers_dict.get("sister_girlfriend_ask_blessing", False):
            return "Talk to [mom.title] first."
        else:
            return True

label sister_girlfriend_intro(the_person):
    mc.name "[the_person.title], I want to ask you something important."
    "[the_person.possessive_title] nods and listens attentively."

    $ first_time = not the_person.event_triggers_dict.get("sister_girlfrind_asked_before", False)
    $ the_person.draw_person(emotion = "happy")
    if first_time:
        $ the_person.event_triggers_dict["sister_girlfrind_asked_before"] = True
        mc.name "I've been thinking about this - and you - for a while. We've grown really close, closer than I could imagine being with anyone else."
        mc.name "I want you to be my girlfriend. What do you say?"
    else:
        mc.name "I haven't stopped thinking about you. I still can't imagine being with anyone other than you."
        mc.name "I still want you to be my girlfriend. What do you say?"
    $ the_person.draw_person(emotion = "happy")
    "[the_person.title] smiles, but she seems conflicted."
    the_person "I love you, but I love you like a brother."
    the_person "I don't know if I could see you as anything {i}other{/i} than family."

    $ convinced = False
    $ most_done = None
    $ most_phrase = "do nothing"

    $ was_preg = False
    if the_person.event_triggers_dict.get("preg_your_kids_known",0) > 0:
        $ was_preg = True

    if not the_person.has_taboo("vaginal_sex"):
        $ most_done = "vaginal"
        $ most_phrase = "fuck their brother"
    elif not the_person.has_taboo("anal_sex"):
        $ most_done = "anal"
        $ most_phrase = "get analed by their brother"
    elif not the_person.has_taboo("sucking_cock"):
        $ most_done = "suck"
        $ most_phrase = "suck their brother's cock"
    elif not the_person.has_taboo("kissing"):
        $ most_done = "kiss"
        $ most_phrase = "make out with their brother"

    menu:
        "Most sisters don't [most_phrase].":
            if most_done == "vaginal":
                $ convinced = True
                mc.name "Most sisters don't fuck their brother."
                if the_person.effective_sluttiness() < 40:
                    the_person "Oh god, I knew that was a mistake!"
                    the_person "[the_person.mc_title], we need to forget about that!"
                    if the_person.sex_record["Vaginal Sex"] > 1:
                        mc.name "Once might have been a mistake, but we're so far past that now."
                    else:
                        mc.name "I can't forget it [the_person.title], you were incredible! Now you're all I want!"
                else:
                    the_person "That was... I know we shouldn't have..."
                mc.name "We're so far past being \"just family\", we need to throw all of that out and decide what makes us happy."

            elif most_done == "anal":
                $ convinced  = True
                mc.name "Most sisters don't take their brother's cock in their ass."
                mc.name "I think we're a little more than \"just family\" at this point."
                if the_person.effective_sluttiness() < 40:
                    the_person "Oh god, I knew that was a mistake!"
                    the_person "[the_person.mc_title], we need to forget about that!"
                    if the_person.sex_record["Anal Sex"] > 1:
                        mc.name "Once might have been a mistake, but we're so far past that now."
                    else:
                        mc.name "I can't forget it [the_person.title], you were incredible! Now you're all I want!"
                else:
                    the_person "That was... I know we shouldn't have..."
                mc.name "Don't be scared. Just think about what makes you happy."

            elif most_done == "suck":
                mc.name "Most sisters don't take their brother's cock down their throat."
                mc.name "Aren't we a little more than \"just family\" at this point?"
                if the_person.sex_record["Blowjobs"] > 1:
                    the_person "It's not like we actually had sex or anything like that."
                    the_person "I just... need to get practice doing that sort of thing, and I trust you!"
                else:
                    the_person "That was just a one time thing, don't expect me to do that for you all the time!"

            elif most_done == "kiss":
                mc.name "Most sisters don't make out with their brother."
                mc.name "Doesn't that make us a little more than \"just family\"?"
                the_person "Oh, that? It was just a little kissing [the_person.mc_title]. It doesn't mean anything."
                the_person "I've heard so many stories at school of girls making out with their brothers."
                the_person "It happens all the time!"

            if convinced:
                the_person "You do make me happy..."
                "She stares deep into your eyes as you take her hands and hold them in yours."
                mc.name "Just be with me [the_person.title]. It's that simple."
                "[the_person.possessive_title] hesitates for a long moment. At long last she nods."
                the_person "Okay, you're right. We've gone this far already..."

            else:
                the_person "It's not like we've done anything serious like fuck each other."
                "[the_person.possessive_title] shakes her head."
                the_person "Let's not make this weird [the_person.mc_title], it's all just been casual fun."
                "You don't think you're going to change her mind without taking things further first."
                mc.name "You're right, I was reading too much into things."

        "Order her to agree." if the_person.obedience >= 200:
            $ convinced = True
            mc.name "Then I don't want you to think of me as family."
            "You put a hand on the back of her neck and make sure she's looking you directly in the eye."
            mc.name "Think of me as your master. I want you in my life, and I don't want to share."
            "[the_person.possessive_title]'s eyes are wide and fixed on yours. You can feel her trembling under your touch."
            mc.name "Do you understand?"
            the_person "Yes, I understand [the_person.mc_title]. Of course I'll do whatever you want me to do."

        "Order her to agree.\nRequires: 200 Obedience (disabled)" if the_person.obedience < 200:
            pass

        "Think of the baby!" if was_preg and persistent.pregnancy_pref > 0:
            $ convinced = True
            mc.name "Most sisters don't end up knocked up with their brothers baby."
            if the_person.event_triggers_dict.get("preg_knows", False): #She's pregnant right now
                "You put a hand on her stomach and look deeply into her eyes."
                mc.name "Think about the baby [the_person.title]. Don't you want me by your side for this?"
                "She places her hands over yours and sighs happily."

            else:
                "You take her hand and look deeply into her eyes."
                mc.name "Think about the baby [the_person.title]. Shouldn't we be together for this?"
                "She sighs happily and hold your gaze."
            the_person "You're right. Of course you're right!"
            "[the_person.possessive_title] hugs you tight, pressing her head against your chest."
            "After a long moment she steps back, looking happy but concerned."

        "Think of the baby!\nRequires: Get her pregnant! (disabled)" if not was_preg and persistent.pregnancy_pref > 0:
            pass

        "Let it go.":
            mc.name "You know what, you're right. I shouldn't ruin a good thing by trying to force it to be more than it is."
            "[the_person.possessive_title] sighs in relief."
            the_person "I'm glad you understand."

    if not convinced:
        return

    #Assuming she hasn't told you directly no yet:
    the_person "What do we tell other people? Someone's going to notice what's going on eventually."
    $ convinced = False
    menu:
        "Who cares what other people think?" if the_person.get_known_opinion_score("incest") > 0:
            $ convinced = True #Tell everyone that you're in a relationship, and you don't care what they think!
            mc.name "I think our love is more important than what other people think of us!"
            mc.name "We shouldn't have to hide how we really feel just to satisfy other people!"
            "[the_person.possessive_title] nods in agreement, gaining confidence with each moment."
            the_person "You're right! Love is the most important thing in the world, and I love you!"

        "Who cares what other people think?\nRequires: Positve incest opinion (disabled)" if the_person.get_known_opinion_score("incest") <= 0:
            pass

        "We'll keep it a secret." if mc.focus >= 4 and the_person.focus >= 4:
            $ convinced = True #Don't tell anyone at all. Kind of like an affair but for fucking your sister. A perfect analogy.
            mc.name "We'll have to keep it a secret from everyone. It won't be easy, but if we're careful nobody needs to know but us."
            "[the_person.possessive_title] nods her understanding."
            the_person "I think I can do that. At least we can be together when we are here at home."

        "We'll keep it a secret\nRequires: Both 4+ Focus (disabled)" if mc.focus < 4 or the_person.focus < 4:
            pass

        "We'll pretend we aren't related." if mc.charisma >= 4 and the_person.charisma >= 4:
            $ convinced = True
            mc.name "Nobody needs to know that we're siblings. If we're careful and convincing enough nobody will know we aren't just a normal couple."
            the_person "What about all of my friends? They're going to recognise you if they see us together."
            mc.name "We'll avoid them when we are toegther. If they ask do your best to convince them I'm just a normal big brother."
            "[the_person.possessive_title] nods her understanding."
            the_person "I think I can do that. I can be pretty convincing when I need to be."

        "We'll pretend we aren't related.\nRequires: Both 4+ Charisma (disabled)" if mc.charisma < 4 or the_person.charisma < 4:
            pass

        "Let it go.":
            mc.name "You're right, there's no good way for us to do this even if we wanted to."
            "[the_person.possessive_title] sighs and shrugs."
            the_person "I'm sorry, but it's just not the right time. I don't know if it ever will be..."

    if not convinced:
        return


    the_person "Okay, but what about [mom.title]? I don't know how long we could hide this from her."
    the_person "I don't think she would be very happy with us being together..."

    $ convinced = False
    menu:
        "I'll get [mom.title]'s blessing.":
            $ convinced = False #Note that this _isn't_ a success, but opens up the path to a success later.
            mc.name "I'll talk to [mom.title]. I'm sure I can convince her that love is more important than anything."
            the_person "I hope you're right [the_person.mc_title]. Just try not to get us in trouble, okay?"
            "She gives you a hopeful smile."
            $ mom.event_triggers_dict["sister_girlfriend_ask_blessing"] = True #This flags an action for Mom to be enabled.
            $ the_person.event_triggers_dict["sister_girlfriend_waiting_for_blessing"] = True #STops you from asking her to be your girlfriend until you come back with an answer.

        "Don't worry, I'm dating her too." if mom.has_role(mom_girlfriend_role): #TODO: Requires: you're also already in a relationship with Mom.
            $ convinced = True
            $ already_knows = the_person.event_triggers_dict.get("mom_girlfriend_sister_knows", False)
            mc.name "If she had any problems she probably wouldn't be dating me too."
            if already_knows:
                the_person "Oh yeah, huh..."
            else:
                $ the_person.event_triggers_dict["mom_girlfriend_sister_knows"] = True # She knows now!
                the_person "Oh my god, you are? I should have known!"
                "[the_person.possessive_title] slaps you playfully on the arm."
                the_person "That's my mom you're fucking, you know!"

            "Vren" "The harem variant of this relationship is still under construction. It will be added in a future update!"
            "Vren" "Until then enjoy having both girls as your girlfriend!"

            the_person "She can't be angry about us dating if she's already dating you, so fine!"
            the_person "She's old anyways, I'll show you that you want someone younger to be with you."
            "She takes a deep breath and nods her final approval."
            the_person "Okay then, I'll be your girlfriend [the_person.mc_title]!"

        "Don't worry, I'm dating her too.\nRequires: Dating [mom.title] (disabled)" if not mom.has_role(mom_girlfriend_role): #TODO: Fill in with inverse requirement once we have the forward one.
            pass

        "She's too dumb to notice." if mom.int < 2:
            $ convinced = True
            mc.name "Have you noticed how distracted she's been lately? She's so focused on work that she'll never notice anything is different."
            the_person "She has seemed... different lately. Do you really think we can hide it from her?"
            mc.name "As long as we aren't fucking on the kitchen table in front of her I think we can get away with it."
            "[the_person.possessive_title] considers this, then nods in agreement."
            the_person "Alright then, you've convinced me! I can't believe this is really happening!"
            "She smiles happily and hugs you tight."
            the_person "[the_person.mc_title], my... boyfriend!"

        "She's too dumb to notice.\nRequires: [mom.title] 1 Int (disabled)" if mom.int >= 2:
            pass

        "Let it go.":
            mc.name "I... didn't think about that."
            "[the_person.possessive_title] sighs and shrugs."
            the_person "I'm sorry, but it's just not the right time. I don't know if it ever will be..."

    if convinced:
        call sister_girlfriend_setup(the_person, mom_knows = False)
    return

label sister_girlfriend_return(the_person):
    $ convinced_mom = the_person.event_triggers_dict.get("sister_girlfriend_mom_blessing_given", False)
    mc.name "I talked to [mom.title]..."
    the_person "And? What did she say? Was she angry?"
    if convinced_mom:
        mc.name "A little, at first, but I talked it out with her and she agrees wtih us."
        mc.name "She gave us her blessing, she won't give us any trouble."
        call sister_girlfriend_setup(the_person, mom_knows = True)

    else:
        mc.name "I tried, but she was a lot more resistant than I was expecting."
        "[the_person.possessive_title] frowns."
        the_person "So that's it then..."
        mc.name "I don't know. Maybe I'll think of something else."
        the_person "I'll be here if you do. Come talk to me any time."
        "She gives you a quick kiss on the cheek."

    $ the_person.event_triggers_dict["sister_girlfriend_mom_blessing_given"] = None
    $ the_person.event_triggers_dict["sister_girlfriend_waiting_for_blessing"] = False
    return

label sister_girlfriend_mom_blessing(the_person):
    #Action available once you've convinced lily to be your girlfriend, but she wants Mom's blessing.
    $ convinced = False
    $ first_time = not the_person.event_triggers_dict.get("sister_girlfriend_asked_blessing_before", False)
    $ the_person.event_triggers_dict["sister_girlfriend_asked_blessing_before"] = True
    "[the_person.title], I have something important to tell you about me and [lily.title]."
    the_person "Oh? What is it?"
    mc.name "Me and [lily.title] are in love, and we are going to be spending more time together. As a couple."
    if not first_time:
        mc.name "I'm not joking this time, I really mean it."


    #TODO: Have some measure of how surprised they are by this. ie. if they've caught you fucking before.
    "[the_person.possessive_title] doesn't say anything for a long moment."
    the_person "... Could you run that by me again? You love your sister... romantically?"
    mc.name "That's right."
    "You give her another moment to process this. As it sinks in she starts to shake her head."
    the_person "No, no, you can't be doing, well, anything with your sister!"
    the_person "I don't know how the two of you got this silly idea in your heads, but it stops now."

    menu:
        "Isn't love more important?" if the_person.get_known_opinion_score("incest") > 0:
            $ convinced = True
            mc.name "[the_person.title], isn't our love more important than how other people tell us to feel?"
            the_person "Of course, but you need to be practical [the_person.mc_title]. This could make life hard for both of you."
            mc.name "We know, and we don't care! This is how we feel!"
            the_person "Oh, to be young and in love."
            "[the_person.possessive_title] expression softens."
            the_person "If this is what you both want and you understand the challenges, then I won't stop you."
            mc.name "Thank you [the_person.title], I knew we could trust you."
            "[the_person.possessive_title] smiles and opens her arms up for a hug."
            $ the_person.change_happiness(10)
            the_person "Come here, give me a hug. I'll always be here for both of you."
            "You let [the_person.title] pull you into her arms. After a long moment she lets you go."
            the_person "Well, you should go tell your sister the good news, I suppose."

        "Isn't love more important?!\n Requires: Positive incest opinion (disabled)" if the_person.get_known_opinion_score("incest") <= 0:
            pass

        "Demand she allows it." if the_person.obedience >= 200:
            $ convinced = True
            "You step close to [the_person.title] and put your hand on the back of her head."
            "You hold her by the hair and turn her to look directly at you. She holds her breath in anticipation."
            mc.name "I never needed your permission, I just need you to not cause trouble."
            mc.name "Me and [lily.title] are together now, and you need to accept that."
            "You feel [the_person.possessive_title] try and nod, but you don't let her head move. Her eyes are wide, still fixed on yours."
            the_person "Of course. You can do what ever you want."
            mc.name "Thank you, I'm glad you understand. If [lily.title] asks how you feel, what are you going to tell her?"
            the_person "... That your happiness is the most important thing in the world. If she makes you happy, that's all that matters."
            "You let go of her hair. She lets out a deep breath, but doesn't immediately relax."
            mc.name "I'm going to go tell her the good news then."

        "Demand she allows it.\nRequires: [the_person.title] 200 Obedience (disabled)" if the_person.obedience < 200:
            pass

        "I'm just joking!":
            "You can't think of anything that would convince [the_person.possessive_title] to change her mind, so you shift to damage control."
            mc.name "Hahah, oh man [the_person.title], you should have seen your face!"
            the_person "I... excuse me?"
            if first_time:
                mc.name "I was just joking, obviously. Me and [lily.title] were curious how you would react."
            else:
                mc.name "I'm joking again, obviously! Me and [lily.title] wondered if you'd fall for it twice!"
            $ the_person.change_happiness(-10)
            $ the_person.change_love(-1)
            the_person "I don't think that's a very funny joke [the_person.mc_title]."
            "[the_person.title] scowls at you. You fake a laugh and hold you your hands in innocence"
            mc.name "I'm sorry, maybe it was funnier in our heads."
            "[the_person.possessive_title] lets the subject drop for now."

    if convinced:
        $ lily.event_triggers_dict["sister_girlfriend_mom_blessing_given"] = True
    else:
        $ lily.event_triggers_dict["sister_girlfriend_mom_blessing_given"] = False
    $ the_person.event_triggers_dict["sister_girlfriend_ask_blessing"] = False #Disables this event.


    return

label sister_girlfriend_setup(the_person, mom_knows = False): #Sets up the actual role assignment
    $ the_person.change_happiness(15)
    $ the_person.change_love(5)
    $ the_person.event_triggers_dict["sister_girlfriend_mom_knows"] = mom_knows
    $ the_person.add_role(sister_girlfriend_role)
    return
