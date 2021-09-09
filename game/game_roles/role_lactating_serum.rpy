#TODO: All the stuff for using a girl as a serum incubator.
init -2 python:
    def lactating_serum_on_turn(the_person):
        the_person.event_triggers_dict["max_serum_in_breasts"] = rank_tits(the_person.tits) * 2
        if not the_person.event_triggers_dict.get("serum_in_breasts", False):
            the_person.event_triggers_dict["serum_in_breasts"] = 0

        #TODO: Ability to have a girl pumping for you, so you can talk to her and just get a pile of serum.
        the_person.event_triggers_dict["serum_in_breasts"] += rank_tits(the_person.tits) * the_person.lactation_sources * 0.2
        if the_person.event_triggers_dict.get("serum_in_breasts", 0) > the_person.event_triggers_dict.get("max_serum_in_breasts", 0):
            the_person.event_triggers_dict["serum_in_breasts"] = the_person.event_triggers_dict.get("max_serum_in_breasts", 0)

        the_person.event_triggers_dict["recently_milked"] = False

    def lactation_serum_on_day(the_person):
        lactation_serum_on_turn(the_person)
        lactation_serum_on_turn(the_person)
        return

    def milk_for_serum_requirement(the_person):
        if the_person.lactation_sources <= 0:
            return "She's not lactating."
        elif the_person.event_triggers_dict.get("recently_milked", False):
            return "She's already been milked."
        elif mc.energy < 15:
            return "Not enough energy."
        else:
            return True


label milk_for_serum_label(the_person): #Note that thee serum types have already had the "Milk" component added to them and are unconnected copies of the origional.
    $ serum_produced = get_random_from_list(the_person.event_triggers_dict.get("lactating_serum_types", [])) #If there are multiple traits we only use a random one
    $ milk_serum = copy.copy(serum_produced)
    $ milk_serum.name = "Milky " + milk_serum.name
    $ milk_trait = the_person.get_milk_trait()
    $ milk_serum.add_trait(milk_trait)
    #TODO: Set recently_milked = True if you pull it off
    $ milking_allowed = False
    if not the_person.event_triggers_dict.get("been_milked_before", False):
        $ the_person.event_triggers_dict["been_milked_before"] = True
        mc.name "I've got a request that's a little personal. I hope you don't mind."
        "[the_person.possessive_title] cocks an eyebrow, but waits for you to continue."
        mc.name "It's hard to explain, but my research right now has a need for natural breast milk."
        mc.name "You're lactating, right?"
        if the_person.event_triggers_dict.get("preg_knows", False):
            if the_person.effective_sluttiness() + 10* the_person.get_opinion_score("showing her tits") > 40 and the_person.has_large_tits():
                "[the_person.title] jiggles her tits and laughs."
                the_person "They don't call them \"big mommy milkers\" for nothing!"
            else:
                the_person "That's part of being pregnant!"
        elif the_person.has_role(breeder_role):
            "She nods happily."
            the_person "My body is so ready to be pregnant it decided to start early!"
        else:
            the_person "How did you know? It's so strange, I don't know what's causing it!"
            mc.name "I've heard it's perfectly natural."

        the_person "So you want a sample of my breast milk?"
        mc.name "Yes. The more the better. Do you have some to spare for me?"

    else:
        mc.name "I need some breast milk for my research. Do you have some to spare?"

    if the_person.has_role(girlfriend_role) or the_person.has_role(affair_role) or the_person.has_role(breeder_role) or the_person.effective_sluttiness() + 5*the_person.get_opinion_score("showing her tits") > 50:
        the_person "For you, of course I do!"
        $ milking_allowed = True

    elif the_person.love > 30 or the_person.effective_sluttiness("bare_tits") > 30:
        the_person "I don't know..."
        "[the_person.possessive_title] is unsure, but you think you might be able to convince her."
        menu:
            "I just need a little bit...":
                mc.name "Even just a little bit would be fine. You could collect it all yourself."
                "She thinks about it for a long moment, and finally shrugs and nods."
                the_person "Fine, I just need something to store it in..."
                "You pull an empty serum vial out of your pocket and hand it over to her."
                the_person "I need some privacy for this. I'll be back in a moment."
                $ clear_scene()
                "[the_person.title] leaves for a few minutes."

                $ the_person.draw_person()
                if the_person.event_triggers_dict.get("serum_in_breasts", 0) < 1:
                    "When she comes back she is awkwardly holding the vial, still empty."
                    the_person "I tried, but I just don't have any stored up right now."
                elif the_person.event_triggers_dict.get("serum_in_breasts", 0) < 4:
                    "When she comes back she is awkwardly holding the vial, now filled with milk."
                    the_person "Here..."
                    $ mc.inventory.change_serum(milk_serum, 1)
                    $ mc.log_event("Recieved 1 dose of " + milk_serum.name, "float_text_blue")
                    "She hands you the vial and quickly tries to change the subject."

                else:
                    "When she comes back she is awkwardly holding the vial, now filled to the very top with milk."
                    the_person "I collected as much as I could in this, but I ran out of space..."
                    $ mc.inventory.change_serum(milk_serum, 2)
                    $ mc.log_event("Recieved 2 doses of " + milk_serum.name, "float_text_blue")
                    "She hands you the vial and quickly tries to change the subject."
                $ the_person.event_triggers_dict["recently_milked"] = True
                $ the_person.event_triggers_dict["serum_in_breasts"] += -__builtin__.int(the_person.event_triggers_dict.get("serum_in_breasts",0)) #She's just milked herself, potentially wasting a whole bunch of serum.

            "You didn't mind when I was a kid..." if the_person.has_role(mother_role):
                mc.name "Please [the_person.title]? You didn't have any issue giving me your milk when I was a kid."
                the_person "That was a long time ago, and very different!"
                "You give her your best set of puppy dog eyes."
                the_person "You're lucky you have such an understanding mother... Fine, I'll do it. Only because it's you though."
                mc.name "Thank you [mom.title]!"
                $ the_person.change_slut(1, 30)
                $ milking_allowed = True

            "Just bring your tits over here!" if the_person.obedience >= 130:
                if the_person.outfit.tits_available():
                    mc.name "Come on, I said I need your milk! Get your tits ready!"
                else:
                    mc.name "Come on, I said I need your milk! Get your tits out already!"
                "Your direct orders snap [the_person.title] out of her indecision and she nods."
                $ the_person.discover_opinion("being submissive")
                $ the_person.change_happiness(-5 + 5*the_person.get_opinion_score("being submissive"))
                the_person "Right, of course!"
                $ milking_allowed = True

            "Just bring your tits over here!\nRequires: 130 Obedience (disabled)" if the_person.obedience < 130:
                pass

            "I can pay you. -$200" if mc.business.funds >= 200:
                mc.name "I can pay you, even if you can't get me any. I just need you to try for me."
                "You pull out your wallet while you're talking, leafing through bills inside teasingly."
                "She thinks for a moment, then nods."
                the_person "Okay, we can try it."
                $ mc.business.funds += -200
                "You hand over some cash before she can reconsider."
                $ milking_allowed = True

            "I can pay you.\nRequires: $200 (disabled)" if mc.business.funds < 200:
                pass




    else:
        $ the_person.change_happiness(-5)
        $ the_person.change_love(-1)
        the_person "What? I'm not going to give you my breast milk!"
        "She shakes her head and laughs awkwardly."
        the_person "What a weird question!"


    if milking_allowed:
        if the_person.effective_sluttiness("bare_tits") + 10*the_person.get_opinion_score("showing her tits") < 30:
            the_person "We need to find somewhere private for me to do this first."
            "You shrug and follow her as you find a quiet spot. Eventually she's satisfied and you can continue."

        if the_person.has_taboo("bare_tits") or (the_person.effective_sluttiness() < 30 and the_person.love < 30 and not the_person.has_role(girlfriend_role) and not the_person.has_role(affair_role)):
            the_person "Okay, I'll just need a moment alone..."
            mc.name "Actually, I need to observe to make sure the sample is collected correctly."
            mc.name "There's no need to be nervous, this is a completely natural process."
            $ the_person.break_taboo("bare_tits")
            "She seems momentarily unsure, but nods and starts to undress."

        if the_person.outfit.can_half_off_to_tits(visible_enough = False):
            $ strip_list = the_person.outfit.get_half_off_to_tits_list(visible_enough = False)
            $ generalised_strip_description(the_person, strip_list, half_off_instead = True)
        else:
            $ strip_list = the_person.outfit.get_tit_strip_list(visible_enough = False)
            $ generalised_strip_description(the_person, strip_list)

        $ mc.change_locked_clarity(10)

        $ sluttiness_required = 40
        if the_person.has_taboo("touching_body"):
            $ sluttiness_required += 10
        $ sluttiness_token = get_red_heart(sluttiness_required)

        $ the_person.event_triggers_dict["recently_milked"] = True
        $ available_doses = __builtin__.int(the_person.event_triggers_dict.get("serum_in_breasts",0))
        $ the_person.event_triggers_dict["serum_in_breasts"] += -__builtin__.int(the_person.event_triggers_dict.get("serum_in_breasts",0))

        menu:
            "Milk her yourself." if the_person.effective_sluttiness() >= sluttiness_required or the_person.has_role(girlfriend_role) or the_person.has_role(affair_role) or the_person.has_role(breeder_role):
                mc.name "I'll need to gather the sample myself, to ensure it's collected correctly."
                if the_person.has_taboo("touching_body"):
                    the_person "I'm sure I can handle it, you can keep a close eye on me."
                    mc.name "I'm sorry, but it really is critical."
                    "You produce a water bottle sized container that you brought for just such a purpose and step close to [the_person.title]."
                    $ mc.change_locked_clarity(40)
                    if the_person.has_large_tits():
                        "You reach out and place a hand on one of her big, milk engourged tits. You can feel her quivering nervously under your touch."
                    else:
                        "You reach out and place a hand on one of her little tits. You can feel her quivering nervously under your touch."

                    mc.name "Just relax and trust me; I'm a professional."
                    $ the_person.break_taboo("touching_body")
                    "It must have sounded more sincere to her than it did to you, because she takes a deep breath and calms down noticeably."

                else:
                    the_person "Oh, okay..."
                    "You produce a water bottle sized container that you brought for just this purpose and step close to [the_person.title]."
                    if the_person.has_large_tits():
                        "You reach out and cup one of her big, jiggly tits. You wonder how much milk she could keep in these things."
                    else:
                        "You reach out and place a hand on one of her little tits. You wonder how much milk she could even fit in these tiny things."

                $ mc.change_locked_clarity(40)
                "You put the bottle up to one of her nipples and start to massage her breast, encouraging it to action."
                if available_doses == 0:
                    "After a few moments it's clear that [the_person.possessive_title] just doesn't have any milk to give you right now."
                    the_person "Sorry [the_person.mc_title], I guess I need some time to build some up."

                else:
                    if the_person.lactation_sources == 1:
                        "[the_person.possessive_title]'s tits start to trickle milk into the bottle, one small squirt at a time."
                        "It's slow progress, but you're a patient man. Having an excuse to play with her tits doesn't hurt either."
                        "Eventually you've milked her dry."
                    elif the_person.lactation_sources == 2:
                        "[the_person.possessive_title]'s tits start to squirt milk into the bottle, one pulse at a time."
                        "It takes a little bit of time, but playing with [the_person.title]'s tits keeps you entertained as you milk her dry."
                    elif the_person.lactation_sources == 3 or the_person.lactation_sources == 4:
                        "[the_person.possessive_title]'s tits jet milk at the lightest touch, making an audible splash with each massaged squirt."
                        "Her body seems eager to give up it's bounty, and you've milked her dry in a surprisingly short time."
                    else:
                        "[the_person.possessive_title]'s tits are dripping milk just being exposed, and they gush it into the bottle when she starts to massage them."
                        "You aren't sure how she avoid soaking through every single bra and shirt she puts on!"
                        if the_person.has_large_tits():
                            "Soon you've milked her her big tits empty, but they never quite stop dripping as her body makes new milk at a tremendous rate."
                        else:
                            "Her tiny tits are emptied in seconds, but they still never quite stop dripping as her body keeps making new milk at a tremendous rate."

                    menu:
                        "Finish up.":
                            pass

                        "Milk her {i}hard{/i}":
                            mc.name "Let's make sure we get every last drop..."
                            "You squeeze down hard on [the_person.possessive_title]'s breast. She gasps in a mixture of surprise and pain."
                            if the_person.has_role(breeder_role) or the_person.get_opinion_score("being in control") < 0:
                                the_person "Mmm, get it all [the_person.mc_title]..."
                                $ the_person.change_slut(1,50)
                                "She sounds a little too happy to be milked roughly."
                                "Her body is responding well though, squirting more milk into the bottle."
                                $ available_doses += 2

                            else:
                                the_person "Hey, I'm a little sensitive right now! Could you be a little more gentle?"
                                "You swap the bottle to her other tit and grab it, yanking on it hard."
                                mc.name "Sorry, but it's important I collect as much as I can."
                                $ the_person.change_obedience(1)
                                $ the_person.change_love(-1)
                                "[the_person.possessive_title] doesn't say anything more, other than a few supressed groans."
                                "She's a trooper, and when you're finished you're sure you've managed to collect an extra dose or two of milk."
                                $ available_doses += 1

                        "Give her a fresh sample.":
                            mc.name "Almost done. One last thing, I need you to taste test some."
                            the_person "Some of my own milk? Why?"
                            "You fabricate a quick story."
                            mc.name "Women are very sensitive to minor contaminants in their own breast milk. You can save us a lot of time in the lab this way."
                            if the_person.intelligence < 3:
                                "[the_person.title] doesn't even think about it, trusting you blindly."
                                the_person "Alright then, you're the expect here."
                            elif the_person.intelligence < 5:
                                the_person "I suppose that makes some amount of sense... Alright, just a little bit."
                            else:
                                "[the_person.title] thinks about this for a long time. You're getting worried she's about to call your bluff when she nods."
                                the_person "I think I remember reading that article too. The human body is such an amazing thing."
                                "You agree wholeheartedly as you squeeze drugged milk right out of her tits."

                            menu:
                                "Give her the bottle.":
                                    "You hand her the bottle. Her nipple continues to produce a steady drip of milk, unwilling to stop now that it's started."
                                    "She takes the container and takes a quick sip."
                                    $ available_doses += -1
                                    $ the_person.give_serum(copy.copy(milk_serum))
                                    mc.name "How does it taste?"
                                    the_person "Warm, but good."
                                    "You return the bottle to her nipple and keep massaging."
                                    mc.name "Good, good."

                                "Give her a tit." if the_person.has_large_tits() and available_doses > 1:
                                    mc.name "Alright, here you go..."
                                    "She seems confused when you put the bottle down, but quickly understands when you use that hand to pull her head down towards her chest."
                                    if the_person.effective_sluttiness() < 40:
                                        $ the_person.change_slut(1, 40)
                                        $ the_person.change_love(-1)
                                        "She opens her mouth, likely in surprise or to complain, and you fill it with her own boob."
                                        "When you start to massage it and squirt milk into her mouth she has little choice but to start drinking."
                                    else:
                                        "She opens her mouth and latches onto her own nipple when you bring it close enough."
                                        "She drinks down her own milk as you massage her boob and squirt it into her mouth."

                                    $ full_blast_amount = the_person.lactation_sources
                                    if full_blast_amount > available_doses:
                                        $ full_blast_amount = available_doses
                                    $ full_blast = False
                                    $ full_blast_string = str(full_blast_amount) + " simultaneous doses!"
                                    if full_blast_amount > 1:
                                        menu:
                                            "Just a taste...":
                                                pass

                                            "Full Blast!\n[full_blast_string]":
                                                $ full_blast = True

                                    if full_blast:
                                        $ available_doses += -full_blast_amount
                                        $ count = 0
                                        $ the_person.give_serum(copy.copy(milk_serum))
                                        "You hold [the_person.title]'s head in place and massage out as much milk as you can manage."
                                        $ mc.change_locked_clarity(10*full_blast_amount)
                                        if full_blast_amount == 2:
                                            $ the_person.give_serum(copy.copy(milk_serum))
                                            "You make sure she gets a mouth full and swallows it down before you let go of her head."
                                            "Her breast falls from her lips and bounces back to it's natural position. She seems a little overwhelmed, but maintains her composure."
                                            the_person "It tastes fine... You made sure I was very thorough!"
                                        elif full_blast_amount <= 4:
                                            $ the_person.give_serum(copy.copy(milk_serum))
                                            "[the_person.title] has to swallow multiple times to keep up with her own milk output."
                                            $ gulp_string = "Gulp!"
                                            while count+2 < full_blast_amount:
                                                $ the_person.give_serum(copy.copy(milk_serum))
                                                $ count+= 1
                                                "[gulp_string]"
                                                $ gulp_string += " Gulp!"

                                            "You let go of her head, and her breast jiggles back to it's natural position."
                                            "She seems a little shaken, but wipes her lips after a moment and answers:"
                                            the_person "Nothing strange to report..."


                                        else:
                                            $ the_person.give_serum(copy.copy(milk_serum))
                                            "[the_person.title] is practically drowning in her own milk as it comes torrenting out of her tit."
                                            "She sputters briefly, milk splattering around her lips and back onto her own breast."
                                            "Finally she gets into the rhythm and gulps it down as quickly as she makes it."
                                            $ gulp_string = "Gulp!"
                                            while count+2 < full_blast_amount:
                                                $ the_person.give_serum(copy.copy(milk_serum))
                                                $ count+= 1
                                                "[gulp_string]"
                                                $ gulp_string += " Gulp!"
                                            "When you let go of her head she unlatches, dribbling a mixture of milk and spit onto her own chest."
                                            "Meanwhile. her tit jiggle back down to it's natural position. A steady stream of milk continues to drip from her nipple, unwilling to stop once it's been started."
                                            mc.name "Well, how was it?"
                                            "[the_person.possessive_title] needs a moment to catch her breath before she can answer."
                                            the_person "Uh... it was fine, just fine..."


                                    else:
                                        $ available_doses += -1
                                        $ the_person.give_serum(copy.copy(milk_serum))
                                        "When you're sure [the_person.title] has had about a dose you let go of her head and boob."
                                        "She lets her bounce back to it's natural position."
                                        the_person "Uh... it tastes fine."

                    if available_doses <= 0:
                        "There would have been some milk to spare, but you've had [the_person.title] drink every last drop she produced!"
                    elif available_doses < 3:
                        "The bottle has a little bit of liquid at the bottom now. Not much, but enough for a dose or two of serum."
                    elif available_doses < 8:
                        "You check the bottle. There's a sizeable amount of liquid sloshing around inside - enough to rival a batch of traditionally made serum."
                    elif available_doses < 14:
                        "The bottle is so full you need to be careful not to spill any as you get a cap on it. Easily more than you would produce in the lab."
                    else:
                        "The bottle is so full that milk is overflowing and running down the sides. You slap a cap on it before you lose any more to spillage."
                        "[the_person.title] laughs, embarassed."
                        the_person "Maybe you should bring a second bottle next time."
                        "You seriously consider it as you store away the full bottle - easily a dozen doses or more."

                    if available_doses > 0:
                        $ mc.inventory.change_serum(milk_serum, available_doses)
                        $ mc.log_event("Recieved " + str(available_doses) + " dose of " + milk_serum.name, "float_text_blue")

                    "Job complete, you put the bottle away."


            "Milk her yourself.\nRequires: [sluttiness_token] (disabled)" if the_person.effective_sluttiness() < sluttiness_required:
                pass

            "Let her milk herself.":
                mc.name "Well, you better get to it."
                "You're well prepared: you hand [the_person.possessive_title] a water bottle sized container to try and fill."
                if the_person.has_large_tits():
                    "She takes the bottle and holds it up to the nipple of one of her heavy breasts, using her other hand to massage it."
                else:
                    "She holds the bottle up to the nipple of one of her cute little tits, using the other hand to massage it to action."
                    "You're unsure how much milk she could even store in those little things..."


                if available_doses == 0:
                    "She tries for a few moments, but it becomes clear that [the_person.title] just doesn't have any milk to give right now."
                    the_person "Sorry [the_person.mc_title], I guess I need some time to build some up."
                else:
                    $ mc.change_locked_clarity(10*the_person.lactation_sources)
                    if the_person.lactation_sources == 1:
                        "[the_person.possessive_title]'s tits start to trickle milk into the bottle, one small squirt at a time."
                        "It's slow progress, but you're patient as she alternates breasts and milks herself dry"
                    elif the_person.lactation_sources == 2:
                        "[the_person.possessive_title]'s tits start to squirt milk into the bottle, one pulse at a time."
                        "It takes a little bit of time, but you're patient as she alternates breasts and milks herself dry."
                    elif the_person.lactation_sources == 3 or the_person.lactation_sources == 4:
                        "[the_person.possessive_title]'s tits jet milk at the lightest touch, making an audible splash with each massaged squirt."
                        "It only takes a couple of moments for her to milk herself dry, alternating breasts as she goes."
                    else:
                        "[the_person.possessive_title]'s tits are dripping milk just being exposed, and they gush it into the bottle when she starts to massage them."
                        "You aren't sure how she avoid soaking through every single bra and shirt she puts on!"
                        if the_person.has_large_tits():
                            "In barely a moment she's milked her big tits empty, but they never quite stop dripping as her body makes new milk at a tremendous rate."
                        else:
                            "Her tiny tits are emptied in seconds, but they still never quite stop dripping as her body keeps making new milk at a tremendous rate."

                    the_person "Here you go, I hope this is enough."
                    if available_doses < 3:
                        "She hands over the bottle. There's not much liquid in it, but there should still be enough for a dose or two of serum."
                    elif available_doses < 8:
                        "She hands over the bottle. There's a sizeable amount of liquid sloshing around inside - enough to rival a batch of traditionally made serum."
                    elif available_doses < 14:
                        "She hands over the bottle, and it's so full you need to be careful not to spill any as you get a cap on it. Easily more than you would produce in the lab."
                    else:
                        "She hands over the bottle, so full that milk is overflowing and running down the sides. You slap a cap on it before you lose any more to spillage."
                        "[the_person.title] laughs, embarassed."
                        the_person "Maybe you should bring a second bottle next time."
                        "You seriously consider it as you store away the full bottle - easily a dozen doses or more."

                    $ mc.inventory.change_serum(milk_serum, available_doses)
                    $ mc.log_event("Recieved " + str(available_doses) + " dose of " + milk_serum.name, "float_text_blue")

        $ mc.change_energy(-15)
        mc.name "Alright, I think we're done here then."
        $ the_person.review_outfit()

    return
