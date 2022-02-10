init -1 python:
    def stripper_private_dance_requirement(the_person):
        if not strip_club.has_person(the_person):
            return False
        elif not mc.business.has_funds(100):
            return "Not enough cash."
        else:
            return True

label stripper_private_dance_label(the_person):
    if the_person.has_role(cousin_role):
        mc.name "So, do you do private dances?"
        "[the_person.possessive_title] glares at you and rolls her eyes."
        the_person "Screw off."
        mc.name "Is that how you talk to all of your clients? You aren't very good at this."
        the_person "Haha, very funny. Now screw off, you're costing me money."
        "You pull out your wallet and shake a collection of bills in front of her. Her eyes follow them hungrily."
        the_person "God damn it... Fine, come with me."
        $ the_person.draw_person(position = "walking_away")
        "She snatches your wrist and half-drags you across the main room towards a series of curtain_obscured booths."
        "[the_person.possessive_title] shoves you towards the padded bench and snaps the curtain closed behind both of you."
        $ the_person.draw_person()
        the_person "Money. Now."
        menu:
            "Pay her. -$100":
                mc.name "Alright, alright. Calm down, I'm a man of my word."


            "Tits first. -$100" if not the_person.outfit.tits_visible():
                mc.name "How do I know you aren't just going to take the money and leave?"
                the_person "This is my fucking job, [the_person.mc_title], alright? I'm not going to screw you."
                mc.name "I don't know if I can trust you... Show me your tits first."
                $ the_person.change_happiness(-5)
                $ the_person.change_love(-1)
                $ the_person.change_obedience(1)
                "She glares at you, but finally relents."
                $ strip_list = the_person.outfit.get_tit_strip_list()
                $ generalised_strip_description(the_person, strip_list)
                the_person "Satisfied?"
                mc.name "Not yet, but we'll see how the evening plays out."
                the_person "Ugh, pig. Now pay up before I call get the bouncer to kick your ass."

        $ mc.business.change_funds(-100)
        "You hold up the bills and she snatches them almost immediately."
        "Then [the_person.possessive_title] flicks a switch, pumping the club music into the small booth."
        the_person "Now just stay still and let me get through my routine."
        "She starts to dance, swaying her hips and shaking her tits as you watch."
        call strip_tease(the_person, for_pay = True, skip_intro = True, start_girl_state = strip_dancing)
        the_person "Happy? Satisfied? Good."
        $ the_person.apply_outfit()
        "[the_person.possessive_title] gets dressed and pulls the curtain back, hurrying out into the main showroom without waiting for you."
        "You follow after her a few moments later."
    else:
        mc.name "Do you do private dances?"
        "[the_person.possessive_title] looks you up and down and smiles."
        the_person "For you, handsome? I think one can be arranged."
        the_person "But my boss won't be happy if I do it for free..."
        mc.name "That won't be a problem."
        the_person "Well then follow me."
        $ the_person.draw_person(position = "walking_away")
        "She brushes her fingers over your upper arm, then turns around and leads you towards a serious of curtain-obscured booths."
        $ mc.change_locked_clarity(10)
        "She rocks her hips as she walks in front of you, jiggling her ass with each step."
        "She pulls the curtain to the side of one booth and motions for you to enter."
        $ the_person.draw_person(position = "walking_away")
        "You take a seat on a padded bench, and [the_person.title] stands in front of you."
        the_person "Now before we go any further, do you have something for me..."
        $ mc.change_locked_clarity(10)
        "She places her hands on the bench behind you, nearly pressing her breasts into your face."
        $ the_item = the_person.outfit.get_upper_top_layer()
        menu:
            "Hand her the cash. -$100":
                "You pull out your wallet and retrieve [the_person.title]'s money."
                $ mc.business.change_funds(-100)
                "You press it into her hand, and she flips through it quickly. Satisfied, she tucks it away and smiles at you."

            "Stuff the cash into her cleavage. -$100" if the_item:
                "You pull out your wallet and retrieve [the_person.title]'s money."
                $ mc.business.change_funds(-100)
                "She waits patiently as you tuck the bills under the edge of her [the_item.display_name]."
                "She doesn't count it, but she seems satisfied with the number of bills you've stuffed between her tits."

        the_person "Now you just sit back, relax, and let me take care of you..."
        "She flicks on a speaker, pumping the club music into the small booth, and starts to dance."
        call strip_tease(the_person, for_pay = True, skip_intro = True, start_girl_state = strip_dancing)
        $ the_person.apply_outfit()
        "[the_person.possessive_title] gets tidied up, then slides the curtain open and walks out into the main showroom again."
        "You take a minute to compose yourself, then stand up and walk out yourself."
    return

label stripper_offer_hire(the_person):
    if the_person.has_role(cousin_role): #NOTE: This is only possible if you get her up to 20 Love, otherwise, you hire her through her blackmail event.
        mc.name "Have you ever thought about a different career?"
        mc.name "I might have a position at my company, and I'm always happy to help out family."
    else:
        mc.name "Have you ever thought about a different career?"
        mc.name "My company could really use talented people like you."
    if strip_club.has_person(the_person):
        the_person "I really can't talk about stuff like that when I'm at work [the_person.mc_title]."
        the_person "We can talk when I'm not at the club, okay?"
        mc.name "Right, sure."
    else:
        the_person "Really? Why would you possibly need a stripper?"
        the_person "I mean, I'll do corporate parties, if that's what you need me for."
        mc.name "No, I mean a normal job."
        if the_person.get_opinion_score(["showing her ass", "showing her tits"]) < 0: #Happy to get out of here
            the_person "Really? God, I do hate working here... It feels so degrading, having men leer at me all day."
            "She thinks about it for a long moment."
            the_person "Fine, yeah. What would this job be?"
            call stripper_hire_accept(the_person)
        else: #Needs to be convinced, because stirpping money is good.
            the_person "That's a kind offer [the_person.mc_title], but I make really good money dancing."
            if the_person.get_opinion_score(["showing her ass", "showing her tits"]) > 0:
                the_person "And it's pretty fun, honestly. There's nothing quite like being up on stage and being the center of attention."

            the_person "It would take a lot to convince me to quit."
            menu:
                "Quit for me." if the_person.has_role(girlfriend_role) or the_person.has_role(affair_role):
                    if the_person.has_role(affair_role):
                        mc.name "If you worked for me we would have so much more time together. Think of all the fun we could have."
                        the_person "Oh I see you've already thought about my duties..."
                    else:
                        mc.name "Do it for me, then, not the job. I don't want you dancing for other men when you could be spending time with me."
                        the_person "Aww, are you feeling jealous? Well..."
                    "She bites her lip and thinks about it for a long moment."
                    the_person "Fine, I'll consider it. Where would I be working?"
                    call stripper_hire_accept(the_person)


                "Quit for me.\nRequires: Girlfriend or Paramour (disabled)" if not (the_person.has_role(girlfriend_role) or the_person.has_role(affair_role)):
                    pass

                "Pay her double normal wages.":
                    mc.name "You're a valuable woman, I understand that. Let's see if I can pay you what you deserve..."
                    $ the_person.salary_modifier = 2.0
                    call stripper_hire_accept(the_person)

                "Let it go.":
                    mc.name "I understand. Let me know if you change your mind."

    return


label stripper_hire_accept(the_person):
    call stranger_hire_result(the_person)
    if _return:
        mc.name "It's settled then. I'll see you at work."
        the_person "And I'll go call my boss and let him know I'm finished."
        the_person "I don't think he's going to be very happy to hear it..."
    else:
        mc.name "On second thought... I think I'm going to have to wait a little before I can take you on."
        the_person "I can't just wait around doing nothing. Tell me when you actually have a position for me, then I'll quit."
    return
