### All of the event stuff specific to getting Jennifer to be your girlfriend.

init -2 python:
    def mom_girlfriend_ask_blessing_requirement(the_person):
        if the_person.event_triggers_dict.get("mom_girlfriend_ask_blessing", False):
            return True
        else:
            return False

    def mom_girlfriend_return_requirement(the_person):
        if the_person.event_triggers_dict.get("mom_girlfriend_sister_blessing_given", None) is None:
            return False
        elif the_person.event_triggers_dict.get("mom_girlfriend_waiting_for_blessing", False) and lily.event_triggers_dict.get("mom_girlfriend_ask_blessing", False):
            return "Talk to [lily.title] first."
        else:
            return True

label mom_girlfriend_intro(the_person):
    $ first_time = not the_person.event_triggers_dict.get("mom_girlfriend_asked_before", False)
    $ the_person.draw_person(emotion = "happy")
    mc.name "There's something important I need to talk you about [the_person.title]. Do you have a moment?"
    the_person "Of course, what do you want to talk about?"
    if first_time:
        $ the_person.event_triggers_dict["mom_girlfriend_asked_before"] = True
        mc.name "You've always been the most important woman in my life..."
        the_person "Aww..."
        mc.name "...and I feel like our relationship has evolved. I feel like you're more than just my mother now, and I want to be more than just your son."
        mc.name "I want to be your boyfriend."
        "[the_person.possessive_title] doesn't say anything for a long moment. At long last she sighs and smiles weakly."
        $ the_person.draw_person(emotion = "happy")
        the_person "[the_person.mc_title], thats so sweet of you to say, but that's really not something we can do."
    else:
        mc.name "I still want to make you my girlfriend. I don't care about anyone the way I care about you."
        $ the_person.draw_person(emotion = "happy")
        the_person "That really is sweet [the_person.mc_title], but I haven't changed my mind."

    the_person "It's natural for us to feel a connection, but you're young and the world is full of wonderful girls your own age to meet."
    the_person "Why would you want to be with someone old like me?"

    $ convinced = False
    $ was_preg = False
    if the_person.event_triggers_dict.get("preg_your_kids_known",0) > 0:
        $ was_preg = True

    menu:
        "I can provide for us!":
            if not the_person.event_triggers_dict.get("mom_girlfriend_provided_cash", False):
                mc.name "Because we make an amazing team, and I want to contribute even more."
                mc.name "You've worked your whole life to take care of me and [lily.title]. When we're together I can help take care of both of you."
                "[the_person.possessive_title] seems unconvinced, but doesn't immediately turn you down."
                mc.name "Come on [the_person.title], let me prove it. Are there any bills we need to pay?"
                the_person "I suppose there is one thing that I certainly don't have the money for right now... but it's expensive!"
                the_person "The car has been giving me trouble every morning. I took it to a shop to have it looked at and repairs are going to cost five thousand dollars!"
                menu:
                    "Pay for the repairs. -$5000" if mc.business.funds >= 5000:
                        "You pull out your phone and open up your banking app."
                        mc.name "No problem at all. Just one moment..."
                        the_person "[the_person.mc_title], you really don't have to do this! I'm sure I could have taken care of it eventually..."
                        mc.name "You shouldn't have to take care of it all by yourself. I want to be your partner in all of this!"
                        $ mc.business.funds += -5000
                        "You send [the_person.possessive_title] the money she needs and put your phone away again."
                        mc.name "There. The money should be in your account next time you check."
                        "She smiles and her eyes soften. She seems almost on the verge of tears."
                        the_person "[the_person.mc_title]... I don't know what to say..."
                        the_person "Okay, you've made your point. It would be nice to have someone to support me when I need it."


                        $ convinced = True
                        $ the_person.event_triggers_dict["mom_girlfriend_provided_cash"] = True

                    "Pay for the repairs.\nRequires: $5000 (disabled)" if mc.business.funds < 5000:
                        pass

                    "Start saving up.":
                        mc.name "Five grand? Whew, that's going to take me a little bit of time..."
                        the_person "It's fine, really. I'm sure I'll be able to pay for it eventually."
                        mc.name "Don't worry [the_person.title], I'm going to get the money together real soon."
                        the_person "If you do I promise I'll think about your... proposal. Deal?"
                        mc.name "Deal."
                        "She smiles warmly at you."
                        the_person "I must be the only mother in the world who has trouble with her son loving her {i}too much!{/i}"

            else:
                $ convinced = True
                mc.name "Because I want to take care of you, just like you always took care of me."
                mc.name "Remember the car? It's fixed because you treated me like your partner, not just your son."
                the_person "That's true, I wouldn't have been able to do it without you."
                the_person "And it would be nice to be with someone I can trust..."
                "She smiles and her eyes soften."
                the_person "Okay, you've made your point."


        "Order her to agree." if the_person.obedience >= 200:
            "You step closer to [the_person.title] and put your hand on the back of her neck. Her breath catches in her throat as whe waits for you to speak."
            mc.name "Because I don't want to share you with anyone else. I want you to be mine, and only mine. Do you understand?"
            "She nods obediently, eyes wide and fixed on yours. She trembles slightly under your touch."
            the_person "Yes [the_person.mc_title], I understand. I'll be whatever you want me to be."
            $ convinced = True

        "Order her to agree.\nRequires: 200 Obedience (disabled)" if the_person.obedience < 200:
            pass

        "Think of the baby!" if was_preg and persistent.pregnancy_pref > 0:
            mc.name "We need to think our baby [the_person.title]. This isn't just about the two of us any more."
            if the_person.event_triggers_dict.get("preg_knows", False):
                "[the_person.possessive_title] puts a hand on her stomach and sighs happily before returning her attention to you."

            else: #Pregnant before and already had the kid.
                pass

            the_person "I told you that I would take full responsibility for what happend. It was a happy little accident."
            mc.name "I want it to be more than an accident. I want this to be an experience we can share together."
            "She thinks for a long moment, then nods and smiles."
            the_person "You're right. I want to share this with you too."
            $ convinced = True

        "Think of the baby!\nRequires: Get her pregnant! (disabled)" if not was_preg and persistent.pregnancy_pref > 0:
            pass

        "Let it go.":
            mc.name "You're being too hard on yourself [the_person.title]. Maybe you're right though, I should try dating someone else first."
            the_person "Of course I am. A mother is {i}always{/i} right when she's giving advice to her child."
            the_person "Don't worry [the_person.mc_title], I'll always be here when you need me."

    if not convinced:
        return

    the_person "We still need to be practical. A mother dating her own son, it's not something most people would agree with."
    the_person "I could even lose my job if my boss found out!"
    $ convinced = False
    menu:
        "We shouldn't care what other people think!" if the_person.get_known_opinion_score("incest") > 0:
            $ convinced = True
            mc.name "We shouldn't hide our love just because some people may not agree with it."
            mc.name "You aren't ashamed of me, are you [the_person.title]?"
            the_person "What!? Of course not, you're the most important thing in the world to me! It's just... I..."
            "[the_person.possessive_title] stumbles over her words, then sighs in defeat."
            the_person "You're right, of course. We shouldn't hide anything. I'm just a little scared."
            mc.name "It's okay, I'll be with you the whole way through."

        "We shouldn't care what other people think!\nRequires: Positive incest opinion (disabled)" if the_person.get_known_opinion_score("incest") <= 0:
            pass

        "We'll hide it from everyone." if mc.charisma >= 4 and the_person.charisma >= 4:
            $ convinced = True
            mc.name "You're right, we'll have to be very careful. When other people are around we'll just pretend to be a normal family."
            the_person "I'll even have to lie to my sister..."
            mc.name "I think that's true. Do you think you can do that?"
            "She thinks for a moment, then nods confidently."
            the_person "She was never very good at telling when I'm lying."

        "We'll hide it from everyone.\nRequires: Both 4+ Charisma (disabled)" if mc.charisma <4 or the_person.charisma < 4:
            pass

        #"You can stay at home all day. #TODO: Add support for this in a future update

        "You can stay at home all day.\nRequires: [mom.title] isn't working (disabled)":
            pass

        "Let it go.":
            mc.name "You're right, this could go really badly if we aren't prepared. We shouldn't rush things."
            the_person "I think that's a wise decision. Maybe it'll be easier for us one day. Or maybe you'll even meet another cute girl you like more than me."

    if not convinced:
        return

    the_person "I can't believe we might actually be doing this! What are we going to tell [lily.title]?"
    the_person "I couldn't do this if she doesn't approve. I won't make her life difficult just for my own happiness."
    $ convinced = False
    menu:
        "I'll talk to her and explain everything.":
            $ convinced = False #NOTE: this isn't a direct success, but it does enable other events
            mc.name "I'll talk to [lily.title] and explain everything. I'm sure when she hears it all laid out she'll be happy for us."
            the_person "Well... if you think that will work, okay. I hope you're as convincing with her as you were with me."
            $ lily.event_triggers_dict["mom_girlfriend_ask_blessing"] = True
            $ the_person.event_triggers_dict["mom_girlfriend_waiting_for_blessing"] = True

        "Don't worry, I'm dating her too." if lily.has_role(sister_girlfriend_role):
            $ convinced = True
            $ already_knows = the_person.event_triggers_dict.get("sister_girlfriend_mom_knows", False)
            mc.name "If she had any problems she probably wouldn't be dating me too."
            if already_knows:
                the_person "I hadn't thought about that..."
            else:
                $ the_person.event_triggers_dict["sister_girlfriend_mom_knows"] = True
                the_person "You're dating [lily.title]? Oh my god, for how long?"
                mc.name "A while, but that's not important now. She doesn't mean nearly as much to me as you do."
            "Vren" "The harem varient of this relationship is still under construction. It will be added in a future update!"
            "Vren" "Until then enjoy having both girls as your girlfriend!"
            the_person "Well, I suppose if she's willing to date you she won't have any problems with me doing it too."
            the_person "I'm not worried, there's no replacement for a mothers love."

        "Don't worry, I'm dating her too.\nRequires: Dating [lily.title] (disabled)" if not lily.has_role(sister_girlfriend_role):
            pass

        "She's too dumb to notice." if lily.int < 2:
            $ convinced = True
            mc.name "I don't think we'll have any issues with her. [lily.title]'s... well, she's not terribly hard to trick."
            mc.name "As long as she doesn't catch us fucking I doubt she'll notice anything has changed."
            the_person "[the_person.mc_title], do you really have to be so crude?"
            the_person "...But you do have a point. Just a little discretion on our part and we won't have to bother her at all."



        "She's too dumb to notice.\nRequires: [lily.title] 1 Int (disabled)" if lily.int >= 2:
            pass

        "Let it go.":
            mc.name "I don't think she'll take it well."
            the_person "Then we should wait. Maybe you'll even find a nice girl in the mean time."

    if convinced:
        "She takes a deep breath and nods her final approval."
        the_person "Okay then, I'll be your girlfriend [the_person.mc_title]!"
        call mom_girlfriend_setup(the_person, lily_knows = False)

    return

label mom_girlfriend_return(the_person):
    $ convinced_lily = the_person.event_triggers_dict.get("mom_girlfriend_sister_blessing_given", False)
    mc.name "I had a chat with [lily.title]..."
    the_person "Oh? What did she say?"
    if convinced_lily:
        mc.name "She was a little confused at first, of course, but she's come around."
        mc.name "She said she's happy for us, and wants us to give this a try."
        "[the_person.possessive_title] smiles and presses her hands to her heart."
        the_person "Oh, oh that's such good news! This is really it then, we're a couple!"
        call mom_girlfriend_setup(the_person, lily_knows = True)
    else:
        mc.name "She was a little more upset than I expected her to be."
        $ the_person.draw_person(emotion = "sad")
        the_person "I thought that might be what happens. I'm sorry [the_person.mc_title], but I have to think about her too, not just us."
        "She places a hand on your arm and rubs it gently."
        the_person "Maybe things will change. We can always hope."

    $ the_person.event_triggers_dict["mom_girlfriend_sister_blessing_given"] = None
    $ the_person.event_triggers_dict["mom_girlfriend_waiting_for_blessing"] = False


    return

label mom_girlfriend_sister_blessing(the_person):
    $ convinced = False
    $ first_time = not the_person.event_triggers_dict.get("mom_girlfriend_asked_blessing_before", False)
    $ the_person.event_triggers_dict["mom_girlfriend_asked_blessing_before"] = True

    mc.name "[the_person.title], I need to tell you something. It's about me and [mom.title]."
    the_person "You and [mom.title]? What could you two possibly have going on?"
    mc.name "Well we had a talk and we've decided to start dating."
    "[the_person.possessive_title] stares at you for a moment, blinking slowly in confusion."
    the_person "Uh... Like a mother-son bonding thing, right?"
    mc.name "No, I mean romantically. She wants your approval before we go any further though."
    "The reality of the situation finally sets in and [the_person.title] starts to shake her head."
    if the_person.get_opinion_score("incest") > 0:
        the_person "Oh my god, can you do that? What am I saying, of course you shouldn't do that!"
    else:
        the_person "Oh my god, ew! Of course not, you two can't do that! It's... I... Ew!"
    menu:
        #TODO: Figure out hat our convince conditions are
        "Isn't our love important?" if the_person.get_known_opinion_score("incest") > 0:
            $ convinced = True
            mc.name "Don't be like that [the_person.title], isn't love more important than what other people tell us is right?"
            "She seems unconvinced, but doesn't immediately respond. You keep pressing your point."
            mc.name "This is going to make [mom.title] happy. You want her to be happy, right?"
            the_person "Obviously, but... Is this really what she wants?"
            "You nod and [the_person.possessive_title] takes a long time to think."
            "At last she sighs and shrugs."
            the_person "Why do you have to be so weird [the_person.mc_title]! Fine, if this will make her happy I won't get in your way."
            mc.name "Thank you [the_person.title] I'm going to go tell [mom.title] the good news!"

        "Isn't our love important?\nRequires: Positive incest opinion (disabled)" if the_person.get_known_opinion_score("incest") <= 0:
            pass

        "I'll pay you.":
            mc.name "I really need you to go along with this. How much money would it take to convince you?"
            the_person "You really think I'll pimp out my own mother for a little bit of cash?"
            mc.name "Not a little bit of cash, no. A lot of cash."
            "[the_person.possessive_title] eyes you suspiciously."
            mc.name "Come on [the_person.title], it's not like she's hooking up with some stranger! It's me!"
            the_person "That's what makes it so weird! Fine, if you give me... ten thousand dollars I'll let you do it."
            menu:
                "Pay her. -$10,000" if mc.business.funds >= 10000:
                    $ convinced = True
                    mc.name "Fine."
                    the_person "Wait, really? You're crazy [the_person.mc_title]!"
                    "You pull out your phone and start to send the cash over."
                    mc.name "I told you I was serious about this. Now I expect you not to cause any trouble for us."
                    $ mc.business.funds += -10000
                    "Her phone buzzes as you finish the transaction. She pulls it out and looks at the notification in disbelief."
                    the_person "Wow, you really did it... Whatever, just don't make things too weird, okay?"
                    mc.name "Sure. I'm going to go give [mom.title] the good news."

                "Pay her.\nRequires: $10,000" if mc.business.funds < 10000:
                    pass

                "Negotiate.":
                    mc.name "Try and take this seriously. How much do you really want?"
                    the_person "I {i}am{/i} being serious! You want to... you know... with our mom!"
                    mc.name "Pick a more reasonable number and we can talk about it."
                    $ the_person.change_love(-1)
                    the_person "Fine. Five thousand, and that's as low as I'll go."
                    menu:
                        "Pay her. -$5000" if mc.business.funds >= 5000:
                            $ convinced = True
                            mc.name "Fine, if that's what it cost."
                            "You pull out your phone and start to send the cash over."
                            the_person "I can't believe you're doing this, it's crazy!"
                            mc.name "I told you I was being serious. Now..."
                            $ mc.business.funds += -5000
                            "Her phone buzzes as you finish the transaction. She pulls it out and looks at the notification in disbelief."
                            mc.name "...I don't want you to cause any trouble for the two of us."
                            the_person "Wow, you really did it... Whatever, just don't make things too weird, okay?"
                            mc.name "Sure. I'm going to go give [mom.title] the good news."

                        "Pay her.\nRequires: $5000 (disabled)" if mc.business.funds < 5000:
                            pass

                        "Refuse.":
                            mc.name "That's still ridiculous, I'm not giving you that much."
                            "She shrugs."
                            the_person "Well then you can tell [mom.title] that I don't agree to any of this!"


                "Refuse.":
                    mc.name "That's ridiculous, I'm not giving you that much."
                    "She shrugs."
                    the_person "Well then you can tell [mom.title] that I don't agree to any of this!"

        "Demand she allows it." if the_person.obedience >= 200:
            $ convinced = True
            mc.name "I'm not asking your permission, I'm telling you to not cause us any problems."
            "You lock your gaze on [the_person.possessive_title] until she nods obediently. It's a well practiced gesture."
            the_person "Right, of course I won't say anything to [mom.title]. You can... do whatever you want to her."
            mc.name "Good to hear. I'll go and tell her the good news."

        "Demand she allows it.\nRequires: 200 Obedience (disabled)" if the_person.obedience < 200:
            pass

        "I'm just joking!":
            "You can't think of anything that would convince [the_person.possessive_title] to change her mind, so you switch to damage control."
            mc.name "Wow, you actually believed me? I'm just joking [the_person.title]."
            $ the_person.change_love(-1)
            "You fake a laugh while [the_person.possessive_title] glares at you."
            the_person "You're so weird [the_person.mc_title], I could actually see you trying something like that!"

        # TODO:At some point blackmail stuff to enable this

    if convinced:
        $ mom.event_triggers_dict["mom_girlfriend_sister_blessing_given"] = True
    else:
        $ mom.event_triggers_dict["mom_girlfriend_sister_blessing_given"] = False
    $ the_person.event_triggers_dict["mom_girlfriend_ask_blessing"] = False
    return


label mom_girlfriend_setup(the_person, lily_knows = False): #Sets up the actual role assignment
    $ the_person.change_happiness(15)
    $ the_person.change_love(5)
    $ the_person.event_triggers_dict["mom_girlfriend_sister_knows"] = lily_knows
    $ the_person.add_role(mom_girlfriend_role)



    return
