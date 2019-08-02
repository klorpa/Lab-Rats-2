##########################################
# This file holds all of the role requirements and labels for the Alexia role.
##########################################

init -2 python:
    def alexia_intro_phase_zero_requirement(day_trigger):
        if day >= day_trigger:
            return True
        return False

    def alexia_intro_phase_one_requirement(the_person):
        if alexia in downtown.people:
            return True
        return False

    def alexia_intro_phase_two_requirement(the_person): #BUG: Alexia's title appears correctly in the action name but incorrectly in the disabled slug. May be due to some argument list references that are by reference instead of value.
        if mc.business.is_weekend():
            return "[alexia.title] only works on week days."
        elif time_of_day == 0:
            return "It's too early to visit [alexia.title]."
        elif time_of_day >= 4:
            return "It's too late to visit [alexia.title]."
        else:
            return True

    def alexia_hire_requirement(the_person):
        if not mc.business.get_employee_title(the_person) == "None":
            return False
        elif the_person.love <= 10:
            return "Requires: 10 Love"
        elif mc.business.get_employee_count() >= mc.business.max_employee_count:
            return "At employee limit."
        else:
            return True

    def camera_arrive_requirement(the_day):
        if day > the_day and mc.business.is_open_for_business():
            return True
        return False

    def alexia_ad_suggest_requirement(the_person, the_day):
        if not day > the_day:
            return False
        elif not mc.is_at_work():
            return False
        elif not mc.business.is_open_for_business():
            return False
        elif mc.business.get_employee_workstation(the_person) is None:
            return False
        else:
            return True

    def alexia_ad_suggest_reintro_requirement(the_person):
        if the_person.event_triggers_dict.get("camera_purchased", False):
            return False
        elif mc.location != mc.business.m_div:
            return False
        elif not mc.business.is_open_for_business():
            return False
        elif mc.business.get_employee_workstation(the_person) is None:
            return False
        elif mc.business.funds < 500:
            return "Insufficient funds."
        else:
            return True

    def alexia_photography_intro_requirement(the_person):
        if not mc.business.event_triggers_dict.get("has_expensive_camera",False):
            return False
        elif the_person.event_triggers_dict.get("ad_photography_enabled",False):
            return False #Don't trigger if we've already enabled the other event.
        elif mc.location != mc.business.m_div:
            return False
        elif not mc.business.is_open_for_business():
            return False
        elif mc.business.get_employee_workstation(the_person) is None:
            return False
        elif time_of_day >= 4:
            return "Too late to start taking pictures."
        else:
            return True

    def alexia_photography_list_requirement(the_person):
        if not mc.business.event_triggers_dict.get("has_expensive_camera",False):
            return False
        elif not the_person.event_triggers_dict.get("ad_photography_enabled",False):
            return False
        elif mc.location != mc.business.m_div:
            return False
        elif not mc.business.is_open_for_business():
            return False
        elif mc.business.get_employee_workstation(the_person) is None:
            return False
        elif time_of_day >= 4:
            return "Too late to start taking pictures."
        elif mc.business.event_triggers_dict.get("Last Ad Shot Day", -7) + 7 > day:
            return "An ad is already running."
        else:
            return True

    def ad_expire_requirement(the_day):
        if day > the_day:
            return True
        return False

label alexia_phase_zero_label():
    #Sets Alexia's schedule so she is downtown during time periods 1,2,3.
    python:
        alexia.schedule[1] = downtown
        alexia.schedule[2] = downtown
        alexia.schedule[3] = downtown
    return

label alexia_intro_phase_one_label(the_person):
    the_person.char "[the_person.mc_title]? [the_person.mc_title] is that you?"
    "You hear your name behind you and turn around to see a familiar face."
    $ the_person.draw_person(emotion = "happy")
    mc.name "[the_person.title]?"
    the_person.char "Yeah, it's me! I didn't know you were still in town, I thought you might have moved away."
    mc.name "I was just passing through, but yeah I'm still around. How about you?"
    if time_of_day == 1:
        the_person.char "Me too, I was just heading to work actually."

    elif time_of_day == 2:
        the_person.char "Me too, I'm actually just on my lunch break and wanted to take a walk."

    else: #time_of_day == 3:
        the_person.char "Me too, I was just heading home from work actually."

    mc.name "Well I guess I got lucky running into you! Where are you working? Making use of that biology degree?"
    "[the_person.title] sighs and shrugs."
    the_person.char "Not really, but that's a long story. I've got a part time job at a coffee shop right now."
    mc.name "That's still an important job; lots of people like coffee and someone's got to serve it."
    "She laughs and touches your arm."
    the_person.char "Do you? Like coffee I mean. I've got to run but I'd love to catch up with you. If you come by at the end of my shift I'll buy you a drink."
    menu:
        "I'd love to.":
            mc.name "That sounds like a great idea. I'll make sure to come by as soon as I can."
            $ the_person.change_happiness(2)
            $ the_person.change_love(1)
            the_person.char "It's a date then!"

        "I don't think I'll have time.":
            mc.name "I've been really busy lately, so I'm not sure I'll have time."
            $ the_person.change_happiness(-2)
            the_person.char "I understand. The offer stands, if your schedule ever changes."

    "[the_person.title] gives you the address of her coffee shop."
    $ the_person.draw_person(position = "walking_away")
    the_person.char "I've got to run, but I hope I'll see you around!"
    "You wave goodbye to [the_person.possessive_title] as she walks away."

    python:
        alexia_intro_phase_two_action = Action("Visit " + the_person.title + " at work", alexia_intro_phase_two_requirement, "alexia_intro_phase_two_label", args = the_person, requirement_args = the_person)
        downtown.actions.append(alexia_intro_phase_two_action)
        downtown.move_person(the_person, the_person.home) #Change her schedule again so you don't see her anymore unless you visit her explicitly.
        alexia.schedule[1] = alexia.home
        alexia.schedule[2] = alexia.home
        alexia.schedule[3] = alexia.home
    $ renpy.scene("Active")
    return

label alexia_intro_phase_two_label(the_person):
    # Have a coffee together. She talk about what she's been doing, introduce her boyfriend.

    #TODO: Add a new background for the coffee shop (and other events that take place here?)
    "You find the coffee shop [the_person.title] works at. It's a small corner unit, with a patio outside full of patrons."
    #TODO: Add a waitress outfit for her
    $ the_person.draw_person()
    "You step inside you see [the_person.possessive_title] behind the front counter. She smiles when she sees you and waves you over."
    the_person.char "Hey, I'm glad you were able to make it! I'm just finishing up my shift, grab a seat and I'll be over in a minute."
    $ renpy.scene("Active")
    "She heads into the back room of the shop. You sit down at a small table for two by a window and wait."
    "A couple of minutes later [the_person.title] comes over with a paper cup in either hand. She puts one on the table and sits down opposite you."
    $ the_person.draw_person(position = "sitting")
    the_person.char "I think I remembered how you like your coffee. Do you remember all the afternoons we spent together, just hanging out and having coffee together?"
    mc.name "Of course, they're some of my best memories. I just wish we had stayed in touch, what happened to you?"
    "She looks out the window and swirles her coffee cup with one hand."
    the_person.char "Something about that summer was just confusing. I didn't know what I wanted to do, but biology wasn't it any more."
    the_person.char "So I didn't come back for my last year. I did some traveling, a lot of thinking, and now I'm back here."
    "You sip at your coffee and listen to [the_person.possessive_title] talk."
    the_person.char "I'm sorry we never talked again. You must have thought I fell off the face of the Earth."
    menu:
        "I forgive you.":
            mc.name "It's okay [the_person.title], I think I understand what you were going through. I'm glad we're able to reconnect now."
            $ the_person.change_happiness(5)
            $ the_person.change_love(1)
            "She sighs and smiles."
            the_person.char "That means the world to me to hear. Thank you [the_person.mc_title]."

        "I missed you.":
            mc.name "When you disappeared it hurt, and I've missed you all this time. It's really strange having you pop back into my life again."
            $ the_person.change_happiness(-5)
            $ the_person.change_obedience(3)
            "She reaches across the table for your hand and holds it in hers."
            the_person.char "I promise I will never hurt you like that again. We've got a second chance, to get to know each other as friends again."

    the_person.char "But enough about me, what have you been doing? Are you done your degree?"
    menu:
        "Brag.":
            mc.name "More than that. You're looking at the proud owner of [mc.business.name], an independent pharmaceutical company."

        "Be Humble.":
            mc.name "I am. I work for a small pharmaceutical company now."
            the_person.char "That's great! What do you do there?"
            mc.name "A bunch of things, really. I manage the day to day operations, oversee production, R&D, sales..."
            the_person.char "It sounds like you practically run the place."
            mc.name "I suppose I do, since I own it."

    the_person.char "What? Come on, be serious."
    mc.name "I am! After I graduated I bought this little lab on the edge of town. We make small batch, limited run pharmaceuticals."
    the_person.char "That's amazing! Tell me more."
    "She leans forward in her chair and listens to you talk about your business. When you've both finished your coffee she checks the time."
    the_person.char "Your work sounds fascinating. I'm don't think I could ever do the science that it sounds like you do, but if you ever need someone to sell coffee for you give me a call!"
    $ the_person.draw_person()
    "[the_person.title] laughs and stands up."
    the_person.char "It's time for me to head home though, my ride should be here soon. Oh, do you want to come out and meet him?"
    "You stand up and walk out with [the_person.possessive_title]."
    mc.name "Uh, sure. Who is he?"
    "When you get outside [the_person.title] looks around for a moment, then waves to a car as it pulls over."
    the_person.char "Right on time! [the_person.SO_name], we met while I was traveling and we've been dating ever since."
    "A man steps out of the car. [the_person.title] hurries over and gives him a hug, then turns around to face you with her arm wrapped around his waist."
    the_person.char "Sweety, this is [the_person.mc_title]. He's an old friend of mine from university. [the_person.mc_title], this is [the_person.SO_name]."
    the_person.SO_name "Hey, it's nice to meet you."
    "He holds out his hand to shake yours."
    menu:
        "Be polite.":
            "You take his hand and shake it."
            mc.name "It's nice to meet you too. I hope we'll have time to talk more in the future."
            $ the_person.change_happiness(3)
            the_person.char "That would be great, the three of us should meet up and have dinner or see a movie or something."

        "Be rude.":
            "You don't shake his hand."
            mc.name "Oh, [the_person.title] didn't even mention she was seeing anyone until now."
            $ the_person.change_love(-1)
            $ the_person.change_obedience(1)
            the_person.char "Sorry sweety, we got talking about [the_person.mc_title]'s work and it never came up."
            "She glares at you for a moment, but [the_person.SO_name] doesn't seem to notice."
            the_person.SO_name "Well we'll have to fix that. If you two are friends we should have dinner together, so you can catch up."

    $ renpy.scene("Active")
    "[the_person.title] gets into the passenger side of her boyfriend's car. She says goodbye from inside and they drive off."
    python:
        downtown.actions.remove(alexia_intro_phase_two_action) #Clear the action from her actions list.
        alexia.schedule[1] = downtown #She spends her time downtown "working".
        alexia.schedule[2] = downtown
        alexia.schedule[3] = downtown

        alexia_hire_action = Action("Hire " + alexia.title + " to work in sales.", alexia_hire_requirement, "alexia_hire_label")
        the_person.get_role_reference_by_name("Alexia").actions.append(alexia_hire_action)
    call advance_time from _call_advance_time_18
    return



label alexia_hire_label(the_person):
    #Hire her onto your marketing team.
    mc.name "[the_person.title], do you like your job at that coffee shop?"
    the_person.char "Do I like it? Not really, but it pays the bills. Why?"
    mc.name "[mc.business.name] is expanding and I need competent people. You're pretty good at selling coffee, I think you'd be perfect for my marketing team."
    the_person.char "You're being serious? Oh man, I don't know what to say [the_person.mc_title]."
    mc.name "How about \"I'll do it\"? I promise I pay better than your coffee place does."
    $ the_person.change_happiness(5)
    $ the_person.change_love(2)
    the_person.char "Okay, I'll do it! Thank you [the_person.mc_title]! Or should I call you boss now?"
    menu:
        "[the_person.mc_title] is fine.":
            mc.name "No need to be too formal. I want you around because you're a friend and we make a good team."
            $ the_person.change_love(1)

        "Boss sounds good.":
            $ the_person.set_mc_title("Boss")
            mc.name "I guess I am your boss now, aren't I. I like the way that sounds."
            $ the_person.change_obedience(2)
            the_person.char "Okay then [the_person.mc_title], you got it!"

    $ the_person.draw_person(emotion = "happy") #TODO: When we have a hugging position draw them as happy.
    the_person.char "So, when can I start?"
    "You give [the_person.title] all of the details about her new job. She phones the coffee shop and quits on the spot."
    python:
        the_person.event_triggers_dict["employed_since"] = day
        mc.business.listener_system.fire_event("new_hire", the_person = the_person)
        the_person.special_role.append(employee_role)
        mc.business.add_employee_marketing(the_person)
        the_person.set_work([1,2,3], mc.business.m_div)

        the_person.get_role_reference_by_name("Alexia").actions.remove(alexia_hire_action) #Remove the hire action because this story event has played itself out.

        ad_suggest_event = Action("Ad Suggestion", alexia_ad_suggest_requirement, "alexia_ad_suggest_label", args = the_person, requirement_args = [the_person, day + renpy.random.randint(7,12)])
        mc.business.mandatory_crises_list.append(ad_suggest_event)
    return


label alexia_ad_suggest_label(the_person):
    $ the_person.draw_person()
    the_person.char "Knock knock. Hey [the_person.mc_title], do you have a second?"
    "[the_person.title] is at your office door."
    mc.name "For you, always. What's up?"
    the_person.char "So I was getting some boxes ready for shipping and I had a thought."
    the_person.char "I know this might be silly, but back at the coffee shop when we had to-go orders we would add a little flier."
    "You nod and listen, noticing now that she has a business card sized piece of paper."
    the_person.char "I put together this mockup, super rough, to show you. I think it would really help boost sales."
    "She hands over her example business card. It has [mc.business.name] written in bold across the top and [the_person.title] posing with a vial of serum."
    the_person.char "What do you think? I put myself in as a place holder, so we would just need to hire a model to be eye candy."
    "You look it over and think for a minute."
    mc.name "I think this is a great idea and you've done great work here."
    $ the_person.change_happiness(5)
    $ the_person.draw_person(emotion = "happy")
    mc.name "I also don't think we would need to hire a model."
    the_person.char "What do you mean?"
    menu:
        "You're all the eye candy we need.":
            mc.name "You're all the eye candy we need. We can take a few high quality pictures of you and we're good to go."
            $ the_person.change_slut_temp(2)
            $ the_person.change_love(1)
            "[the_person.title] blushes waves her hand at you dismissively."
            the_person.char "Oh come on, you know we could find someone better for it. But I guess if I did it we would save some money."
            the_person.char "If it's just a few quick shots I suppose I wouldn't mind."

        "We would save money if you were the model.":
            mc.name "You look perfect for the role in this mockup already. We can take a few high quality pictures and these would be ready for production."
            $ the_person.change_obedience(2)
            $ the_person.change_happiness(1)
            "[the_person.title] seems relieved."
            the_person.char "Right, of course that's what you mean. I guess if it's just a few quick shots I wouldn't mind."

    mc.name "Good to hear. What will you need to get this going?"
    the_person.char "We should probably get a proper camera instead of just my phone, and we'll need to pay to have the cards printed professionally."
    menu:
        "Pay for equipment. -$500" if mc.business.funds >= 500:
            mc.name "That sounds reasonable. Buy whatever you think is reasonable and I will cover the expense."
            $ mc.business.funds += -500
            the_person.char "You got it! I'll order it A.S.A.P and let you know when it arrives."
            mc.name "Great work [the_person.title], you're a credit to the team."
            $ camera_arrive_action = Action("Camera Arrive", camera_arrive_requirement, "alexia_ad_camera_label", args = the_person, requirement_args = day + renpy.random.randint(3,7))
            $ mc.business.mandatory_crises_list.append(camera_arrive_action)
            $ the_person.event_triggers_dict["camera_purchased"] = True

        "Pay for equipment. -$500 (disabled)" if mc.business.funds < 500:
            pass

        "Talk to her later.":
            mc.name "Okay, I'll come talk to you soon and we can sort out these details. Great work [the_person.title], you're a credit to the team."

    the_person.char "Thanks [the_person.mc_title], I'm just happy to have a chance to contribute!"



    return

label alexia_ad_suggest_reintro_label(the_person):
    mc.name "[the_person.title], I want you to order in whatever camera equipment you think is best for your ad photoshoot."
    the_person.char "Okay. I'll get right on that and order it A.S.A.P!"
    mc.name "Send me any receipts and I'll cover the cost."
    $ mc.business.funds += -500
    $ camera_arrive_action = Action("Camera Arrive", camera_arrive_requirement, "alexia_ad_camera_label", args = the_person, requirement_args = day + renpy.random.randint(3,7))
    $ mc.business.mandatory_crises_list.append(camera_arrive_action)
    $ the_person.event_triggers_dict["camera_purchased"] = True
    return

label alexia_ad_camera_label(the_person):
    if mc.business.get_employee_workstation(the_person): #ie is an employee, otherwise this is None.
        "You get a text from [the_person.title]."
        the_person.char "Hey [the_person.mc_title], the camera for that ad idea I had just arrived."
        the_person.char "Come see me when you want to do something with it."
    else: #In case you've fired them or something. Future proofing mostly.
        "A package is delivered during the day. It's the camera [the_person.title] ordered while she was still working for you."
    $ mc.business.event_triggers_dict["has_expensive_camera"] = True
    return

label alexia_photography_intro_label(the_person):
    # You shoot your business cards. Results in a minor (%1) boost in sales values and gives you an opportunity to tell Alexia to pose for you.
    mc.name "Are you ready for our photoshoot?"
    the_person.char "As ready as I'll ever be I suppose. I found a good spot in the storage room, plenty of light and a blank wall."
    mc.name "Excellent. Let's go."
    # TODO: Change location? Just change background art?
    "You and [the_person.possessive_title] go to the stoarge room. Once you get there she hands you the new camera."

    the_person.char "Here you go [the_person.mc_title]. How do you want to do this?"
    mc.name "Let's start with some basic shots of you. Just act natural and look into the camera."
    $ the_person.draw_person(position = "stand4")
    "You frame up [the_person.title] and take a few pictures."
    the_person.char "How's that?"
    mc.name "Good. Try another pose."
    $ the_person.draw_person(position = "stand5")
    mc.name "Perfect. Now try turning around."
    $ the_person.draw_person(position = "back_peek")
    "You snap pictures as she changes pose."
    menu:
        "Focus on her ass.":
            mc.name "Bend forward just a little bit for me. Let's show off your butt."
            the_person.char "Really? Do you think that's important?"
            mc.name "Sex sells. It may not be what we go with, but I want to have options."
            $ the_person.change_slut_temp(2)
            $ the_person.change_obedience(1)
            "She rolls her eyes and bends forward, perking up her ass and showing it off to the camera. You take a couple more pictures."

        "Focus on her smile.":
            mc.name "That's good, now give me one of your beautiful smiles. That's what the camera wants to see."
            $ the_person.draw_person(position = "back_peek", emotion = "happy")
            $ the_person.change_happiness(4)
            $ the_person.change_love(2)
            "She rolls her eyes dramatically, but her smile is genuine and lights up the room."

    "For an hour you try different poses and camera settings until you're satisfied with the results."
    the_person.char "I think that's everything I need to get this business card designed. I'll order them and have them ready for the next shipment out."
    $ mc.business.add_sales_multiplier("Business Cards", 1.01)
    mc.name "Good work [the_person.title], I've been very impressed."
    the_person.char "Thanks, this was fun! If you think this advertising thing is working out we could try putting ads in magazines and stuff."
    mc.name "I think that's another good idea, as long as you want to do the modeling for it."
    $ the_person.change_obedience(1)
    the_person.char "Yeah, I can do that! I don't know why but I thought it was really exciting to be in front of that camera."
    mc.name "I'll let you get back to work then. See you around [the_person.title]."
    $ the_person.event_triggers_dict["ad_photography_enabled"] = True
    call advance_time from _call_advance_time_19
    return

label alexia_photography_list_label(the_person):
    #TODO: Add a chance for her to drink some serum before this happens for maximum manipulation potential.
    mc.name "I want you to put together a new company ad. We'll need some promotional pictures to go with it."
    the_person.char "Sounds like a good idea to me. I've got the camera right here."
    "[the_person.title] grabs the camera from her desk and hands it to you."

    if the_person.planned_uniform is not None: #Check to see if she should have a uniform on.
        if the_person.outfit.slut_requirement> the_person.sluttiness + (the_person.get_opinion_score("skimpy uniforms")*5):
            the_person.char "Do I get to change into something more reasonable, or do you want me in my uniform?"
        else:
            the_person.char "Is my uniform fine for the shoot, or should I put something else on?"
    else:
        the_person.char "How do I look? Do you think I should wear something else for this?"
        $ the_person.draw_person(position = "back_peek")
        "She gives you a quick spin."
        the_person.char "I want to make sure I show my best side for the business."

    menu:
        "Your outfit is fine.":
            mc.name "You look great already, I don't think you need to change a thing."
            $ the_person.discover_opinion("skimpy uniforms")
            $ the_person.change_slut_temp(the_person.get_opinion_score("skimpy uniforms"))
            the_person.char "Okay, I think I'm ready to go then!"

        "Put something else on for me.":
            mc.name "I think you could use something with a little more pop."
            if the_person.sluttiness < 20 and the_person.relationship != "Single":
                the_person.char "Nothing too crazy though, okay? I don't want my boyfriend to freak out when he hears about this."
            else:
                the_person.char "Sex sells, right, so it should be something skimpy. Did you have somethign in mind?"
                "She seems excited to see what you have in mind."


            call screen outfit_select_manager(slut_limit = the_person.sluttiness, show_overwear = False, show_underwear = False)
            if not _return == "No Return":
                if the_person.sluttiness >= _return.slut_requirement:
                    the_person.char "Yeah, I think that would look good. I'll go put that on."

                $ renpy.scene("Active")
                "[the_person.possessive_title] leaves to get changed and is back in a moment."
                $ the_person.outfit = _return #A copy is already what is returned, so we don't have to copy it here.
                $ the_person.draw_person()

            else:
                mc.name "On second thought, I think you look perfect in that."

    "You lead [the_person.possessive_title] to a supply room. She stands against a blank wall while you get the camera ready."
    mc.name "Okay, strike a pose for me."
    $ the_person.draw_person(position = "stand4", emotion = "happy")
    "She smiles at the camera and poses for you."
    the_person.char "Tell me what you want me to do."

    #Outfit checks that let us be sure a girl isn't already naked before asking her to strip.
    $ outfit_state = 0 #0 = relatively normal outfit. 1 = just underwear, can't be stripped down further without being naked. 2 = already naked.
    if the_person.outfit.wearing_bra() and the_person.outfit.wearing_panties() and the_person.outfit.bra_covered() and the_person.outfit.panties_covered(): #She has underwear on and something over both.
        $ outfit_state = 0 #She's wearing enough we can have a "strip to your underwear" scene.
    elif (the_person.outfit.wearing_bra() and not the_person.outfit.bra_covered()) or (the_person.outfit.wearing_panties() and not the_person.outfit.panties_covered()) or (not the_person.outfit.tits_visible() and not the_person.outfit.vagina_visible()):
        $ outfit_state = 1 #She's wearing enough that we can have a strip scene.
    else:
        $ outfit_state = 2 #She's practically naked with no clothing on.

    $ slut_willingness = the_person.sluttiness
    if the_person.obedience > 100:
        $ slut_willingness += the_person.obedience - 100

    # These are "checkpoint" options for future passes through this event.
    menu:
        "Be playful.":
            call photo_be_playful(the_person) from _call_photo_be_playful

        "Be flirty." if the_person.event_triggers_dict.get("camera_flirt", False) and slut_willingness+(5*the_person.get_opinion_score("skimpy uniforms")) >= 15:
            mc.name "Be flirty for me. You're young and sexy, I want you to show that to the camera."
            call photo_be_sexy(the_person) from _call_photo_be_sexy

        "Strip to your underwear." if the_person.event_triggers_dict.get("camera_flash", False) and outfit_state == 0 and slut_willingness+(5*the_person.get_opinion_score("skimpy uniforms")) >= 30:
            mc.name "I want to take some sexy, bold photos of you in your underwear. I want you to strip down for the camera."
            call photo_flash(the_person) from _call_photo_flash

        "Get naked." if the_person.event_triggers_dict.get("camera_naked", False) and outfit_state in [0,1] and slut_willingness+(5*the_person.get_opinion_score("not wearing anything")) >= 50:
            mc.name "Strip everything off for me, I want to get some nude shots."
            call photo_naked(the_person) from _call_photo_naked

        "Touch yourself." if the_person.event_triggers_dict.get("camera_masterbate", False) and slut_willingness+(5*the_person.get_opinion_score("masturbating")) >= 60:
            if not outfit_state == 2:
                mc.name "Get naked and lean against that wall. I want to get some shots of you touching yourself."
                "[the_person.title] nods and starts to strip naked."
                call photo_strip_naked(the_person) from _call_photo_strip_naked
            else:
                mc.name "Lean up against that wall, I want to get some shots of you touching yourself."
            call photo_touch(the_person) from _call_photo_touch

        "Suck my dick." if the_person.event_triggers_dict.get("camera_suck", False) and slut_willingness+(5*the_person.get_opinion_score("giving blowjobs")) >= 70:
            if not outfit_state == 2:
                mc.name "Get naked and on your knees. I want to get some close ups of you sucking my cock."
                "[the_person.title] nods and starts to strip naked."
                call photo_strip_naked(the_person) from _call_photo_strip_naked_1
            else:
                mc.name "Come and kneel down in front of me. I want to get some close ups of you sucking my cock."
            call photo_blowjob(the_person) from _call_photo_blowjob

        "Get fucked on camera." if the_person.event_triggers_dict.get("camera_fuck", False) and slut_willingness+(5*the_person.get_opinion_score("vaginal sex")) >= 80:
            if not outfit_state == 2:
                mc.name "Get naked first, then I'm going to lay you down and get some pictures of you getting fucked."
            else:
                mc.name "I want you to come over here and lay down so I can take some pictures of you getting fucked."
            call photo_sex(the_person) from _call_photo_sex

    $ sexy_score = _return # Each scene returns the sexiness it produced (mainly based on her outfit).
    "You hand the camera over to [the_person.title] and go back to her desk. She pulls out the memory card and puts into the computer."
    $ the_person.draw_person(position = "sitting")
    "You go through the pictures you got, discarding the poor ones and finally settling on best ones to use."
    if the_person.relationship != "Single" and sexy_score > 30 :
        $ SO_title = SO_relationship_to_title(the_person.relationship)
        "You wonder what her [SO_title] would think about [the_person.title] showing so much skin for this ad."


    $ ad_multiplier = 1
    if sexy_score <= 10:
        "The photos you took of [the_person.title] are perfect for an ad placed at the back of a small medical journal."
        "Putting an ad here will boost serum value sales by {b}%%5{/b} for the next week."
        $ ad_multiplier = 1.05
    elif sexy_score <= 30:
        "The photos you took of [the_person.title] are perfect for an ad placed in a lifestyle magazine."
        "Putting an ad here will boost serum value sales by {b}%%10{/b} for the next week."
        $ ad_multiplier = 1.1
    elif sexy_score <= 50:
        "The photos you took of [the_person.title] are perfect for a sexy ad in a local tabloid."
        "Putting an ad here will boost serum value sales by {b}%%20{/b} for the next week."
        $ ad_multiplier = 1.2
    elif sexy_score <= 100:
        "The photos you took of [the_person.title] are perfect for a sexy ad in a soft core porn magazine."
        "Putting an ad here will boost serum value sales by {b}%%40{/b} for the next week."
        $ ad_multiplier = 1.4
    else:
        "The photos you took of [the_person.title] are perfect for a sexy ad in a hard core porn magazine."
        "Putting an ad here will boost serum value sales by {b}%%80{/b} for the next week."
        $ ad_multiplier = 1.8

    the_person.char "What do you think [the_person.mc_title]? Should I get this ad made up and sent out?"
    menu:
        "Pay for the ad space. -$300" if mc.business.funds >=300:
            mc.name "The picutres look good, get to work and get that pushed out as soon as possible."
            the_person.char "You got it!"
            $ mc.business.funds += -300
            $ mc.business.add_sales_multiplier("Ad Campaign", ad_multiplier)
            $ ad_expire_trigger = Action("Ad Expire", ad_expire_requirement, "ad_expire", args = ad_multiplier, requirement_args = day+7)
            $ mc.business.mandatory_crises_list.append(ad_expire_trigger) #It'll expire in 7 days.
            $ mc.business.event_triggers_dict["Last Ad Shot Day"] = day


        "Pay for the ad space. -$300 (disabled)" if mc.business.funds < 300:
            pass

        "Scrap the plan.":
            mc.name "I think our budget is better spent somewhere else. Sorry to put you through all that work."
            the_person.char "I understand. Maybe if we start selling more it'll be worth it."

    call advance_time from _call_advance_time_20
    return

label photo_be_playful(the_person):
    mc.name "Be playful. Give the camera a smile and just have fun with it."
    $ the_person.draw_person(position = "stand3", emotion = "happy")
    "She gives you a few more poses and seems to be enjoying herself."
    $ the_person.draw_person(position = "stand5", emotion = "happy")

    $ slut_willingness = the_person.sluttiness + (5*the_person.get_opinion_score("skimpy uniforms"))
    if the_person.obedience > 100:
        $ slut_willingness += the_person.obedience - 100
    menu:
        "Push her to be flirty." if slut_willingness >= 15:
            mc.name "That's great [the_person.title]. Give me a little more attitude now. You're sexy, you're young, let me feel it!"
            call photo_be_sexy(the_person) from _call_photo_be_sexy_1

        "Push her to be flirty.\n{color=#ff0000}Not slutty or obedient enough{/color} (disabled)" if slut_willingness < 15:
            pass

        "Finish the shoot.":
            "You take a few final pictures."
            mc.name "I think that's all we need. Good job [the_person.title], you look great."
            $ the_person.change_happiness(3)
            the_person.char "Glad to hear it, that was fun!"
            return the_person.outfit.slut_requirement
    return _return

label photo_be_sexy(the_person):
    $ the_person.event_triggers_dict["camera_flirt"] = True
    if the_person.sluttiness >= 15:
        #She's totally onboard with this idea.
        $ the_person.draw_person(position = "back_peek", emotion = "happy")
        "[the_person.possessive_title] spins around, peeking over her shoulder."
        the_person.char "Like this? Get a good shot of my butt, that's the kind of shot you probably want."
        "She wiggles her ass for the camera."

    else:
        #She's only doing it because you're commanding her.
        the_person.char "Oh my god, I feel so awkward trying to do this. This isn't me at all!"
        mc.name "Trust me, just give it a try. Turn around and shake your ass, that'll be sexy."
        $ the_person.draw_person(position = "back_peek", emotion = "happy")
        $ the_person.change_obedience(1)
        "She timidly wiggles her butt for the camera."

    $ slut_willingness = the_person.sluttiness
    if the_person.obedience > 100:
        $ slut_willingness += the_person.obedience - 100

    $ skimpy_uniform_bonus = (5*the_person.get_opinion_score("skimpy uniforms"))
    $ no_clothing_bonus = (5*the_person.get_opinion_score("not wearing anything"))
    $ masturbate_bonus = (5*the_person.get_opinion_score("masturbating"))

    $ outfit_state = 0 #0 = relatively normal outfit. 1 = just underwear, can't be stripped down further without being naked. 2 = already naked.
    if the_person.outfit.wearing_bra() and the_person.outfit.wearing_panties() and the_person.outfit.bra_covered() and the_person.outfit.panties_covered(): #She has underwear on and something over both.
        $ outfit_state = 0 #She's wearing enough we can have a "strip to your underwear" scene.
    elif (the_person.outfit.wearing_bra() and not the_person.outfit.bra_covered()) or (the_person.outfit.wearing_panties() and not the_person.outfit.panties_covered()) or (not the_person.outfit.tits_visible() and not the_person.outfit.vagina_visible()):
        $ outfit_state = 1 #She's wearing enough that we can have a strip scene.
    else:
        $ outfit_state = 2 #She's practically naked with no clothing on.
    menu:
        "Strip to your underwear." if slut_willingness+skimpy_uniform_bonus >= 30 and outfit_state == 0: #TODO: Also check to make sure she's got the right type of clothign TO strip down to her underwear
            #Into her flashing the camera.
            mc.name "These are looking great. Now let's trying something a little more bold. Get into your underwear for me [the_person.title]."
            call photo_flash(the_person) from _call_photo_flash_1

        "Strip to your underwear.\n{color=#ff0000}Not slutty or obedient enough{/color} (disabled)" if slut_willingness+skimpy_uniform_bonus < 30 and outfit_state == 0:
            pass

        "Get naked for the camera." if slut_willingness+no_clothing_bonus >= 50 and outfit_state == 1: #If that's the only possible next step based on her outfit.
            mc.name "Let's kick it up another notch. Get completely naked for these next shots."
            call photo_naked(the_person) from _call_photo_naked_1

        "Get naked for the camera.\n{color=#ff0000}Not slutty or obedient enough{/color} (disabled)" if slut_willingness+skimpy_uniform_bonus < 50 and outfit_state == 1:
            pass

        "Touch yourself." if slut_willingness+masturbate_bonus >= 60 and outfit_state == 2:
            mc.name "You're already undressed for the occasion, so lean against that wall and touch yourself for the camera. I want to see you really get into it."
            call photo_touch(the_person) from _call_photo_touch_1

        "Touch yourself.\n{color=#ff0000}Not slutty or obedient enough{/color} (disabled)" if slut_willingness+masturbate_bonus < 60 and outfit_state == 2:
            pass

        "Finish the shoot.":
            "You take a few final pictures."
            mc.name "I think I got everything we need. Good job [the_person.title], you look great."
            $ the_person.change_happiness(3)
            the_person.char "Glad to hear it, that was fun!"
            return the_person.outfit.slut_requirement
    return _return

label photo_flash(the_person):
    $ the_person.event_triggers_dict["camera_flash"] = True

    $ first_item = the_person.outfit.get_upper_top_layer()
    if the_person.sluttiness >= 30:
        # She's slutty enough to do it.
        "[the_person.title] nods and starts to take off her [first_item.name]."

    else:
        # She's doing it for obedience
        "[the_person.possessive_title] hesitates."
        the_person.char "This is really what you think we need to do for the ad?"
        mc.name "Come on [the_person.title], I'm counting on you."
        "She takes a deep breath, then presses on and starts to take off her [first_item.name]."

    $ the_person.draw_animated_removal(first_item)
    if not person.outfit.panties_covered():
        "When she drops it she's wearing only her underwear."
    else:
        $ covering_item = the_person.outfit.get_lower_top_layer()

        "She pulls it off and drops it to the ground, then starts to pull off her [covering_item.name]."
        $ the_person.draw_animated_removal(covering_item)
        "When that comes off she's left wearing only her underwear."

    if the_person.sluttiness >= the_person.outfit.slut_requirement:
        the_person.char "Time for you to get those shots [the_person.mc_title]!"
        $ the_person.draw_person(position = "stand3", emotion = "happy")
        "[the_person.title] gives you a few different poses in her underwear."
        $ the_person.draw_person(position = "stand4", emotion = "happy")

    else:
        the_person.char "Take those pictures before I have second thoughts..."
        $ the_person.draw_person(position = "stand3")
        "[the_person.title] switches quickly between a few different poses, obviously a little uncomfortable with her state of undress."
        $ the_person.draw_person(position = "stand4")

    $ slut_willingness = the_person.sluttiness + (5*the_person.get_opinion_score("not wearing anything"))
    if the_person.obedience > 100:
        $ slut_willingness += the_person.obedience - 100
    menu:
        "Strip naked." if slut_willingness >= 50:
            mc.name "That's great [the_person.title], this is great material. Next up I want to get some nude shots, so keep stripping for me."
            call photo_naked(the_person) from _call_photo_naked_2

        "Strip naked.\n{color=#ff0000}Not slutty or obedient enough{/color} (disabled)" if slut_willingness < 50:
            pass

        "Finish the shoot.":
            mc.name "I think I've got all the pictures we need, we can call it there."
            the_person.char "Yay, glad to help!"
            $ the_person.change_slut_temp(1)
            $ the_person.change_obedience(2)
            $ the_person.review_outfit()
            return the_person.outfit.slut_requirement

    return _return

label photo_naked(the_person):
    $ the_person.event_triggers_dict["camera_naked"] = True
    if the_person.sluttiness >= 50:
        the_person.char "You got it [the_person.mc_title], I'm up for a little taseful nudity."
        "You make sure to get some pictures as she strips off her underwear."
    else:
        the_person.char "Okay... I think I can do that..."
        "She takes a few deep breaths before she starts to take off her underwear. You make sure to get some pictures as she strips down."

    call photo_strip_naked(the_person) from _call_photo_strip_naked_2


    if the_person.outfit.slut_requirement > the_person.sluttiness + (5*the_person.get_opinion_score("not wearing anything")):
        "[the_person.title] seems unsure of what to do now that she's completely naked."
        the_person.char "Oh my god [the_person.mc_title], my heart is pounding... I feel so vulnerable like this."
        mc.name "You look great [the_person.title], just give me a little spin and relax. Let me do all the hard work, you just have to look pretty."
        $ the_person.draw_person(position = "back_peek")
        if the_person.relationship != "Single":
            $ SO_title = SO_relationship_to_title(the_person.relationship)
            the_person.char "Do.... do you think my [SO_title] would be okay with this?"
            $ the_person.draw_person()
            the_person.char "It's not like we're doing anything wrong, this is all just for work."
            menu:
                "Reassure her.":
                    mc.name "If he was a reasonable person he'd be fine with this."
                    mc.name "You're using your, uh, natural talents to perform your job as well as you can. That's an admirable thing to do."
                    $ the_person.change_happiness(2)
                    $ the_person.change_slut_temp(1)
                    "She smiles and nods."
                    the_person.char "Yeah, that's what I think too."

                "Make her worry.":
                    mc.name "I don't know [the_person.title]. Some men would be very jealous that you were showing off your body to anyone but them."
                    mc.name "Me and you both know it's for the good of the company, but he might not see it that way."
                    $ the_person.change_happiness(-5)
                    $ the_person.draw_person(emotion = "sad")
                    mc.name "But I wouldn't worry about it too much. We can keep it our little secret if you'd like."
                    $ the_person.change_obedience(3)
                    the_person.char "That... might be a good idea. Thanks [the_person.mc_title]."
                    mc.name "No problem. Now smile for the camera and let me get a good look at your tits for this next shot."

        else:
            the_person.char "She gives you a quick spin before turning back."
    else:
        "[the_person.title] drops her underwear to the side and turns to face you."
        the_person.char "There! How do I look? Good?"
        $ the_person.draw_person(position = "back_peek")
        "She winks at you and gives you a quick spin, showing off her ass."


    $ the_person.draw_person()
    the_person.char "Do you have all the shots you want, or did you have something more in mind?"

    menu:
        "Touch yourself." if slut_willingness >= 60:
            mc.name "I want to get some more sensual shots of you. Lean back against the wall and touch yourself."
            call photo_touch(the_person) from _call_photo_touch_2

        "Touch yourself.\n{color=#ff0000}Not slutty or obedient enough{/color} (disabled)" if slut_willingness < 60:
            pass

        "Finish the shoot.":
            mc.name "I think that's everything we need."
            $ the_person.change_obedience(2)
            $ the_person.change_slut_temp(2)
            $ the_person.review_outfit()
            "[the_person.title] collects her things and you finish up the photo shoot."
            return return the_person.outfit.slut_requirement
    return _return

label photo_touch(the_person):
    $ the_person.event_triggers_dict["camera_touch"] = True
    if the_person.sluttiness >= 60:
        "[the_person.title] doesn't hesistate at all. She takes a step back and leans against the wall, spreading her legs slightly."
    else:
        the_person.char "Touch myself? What do you... what do you mean [the_person.mc_title]? I couldn't... do that in front of you."
        "[the_person.title] looks nervous. She seems suddenly self conscious, turning side-on to the camera to limit how much it can see."
        mc.name "Just relax. It's not like you haven't done it before, right?"
        the_person.char "Well obviously not, but..."
        mc.name "And it's not like you're the first person to touch themselves in front of a camera."
        the_person.char "Yeah, I know but..."
        mc.name "And it's for the business. You want us to do well, right?"
        if the_person.relationship != "Single":
            $ SO_title = SO_relationship_to_title(the_person.relationship)
            the_person.char "But what do I tell my [SO_title]? What happens if he sees our ad and sees all of this?"
            mc.name "Tell him whatever you want, he doesn't control you. The only important question is if you want to do this."
            "She thinks about it for a long moment."
            the_person.char "Yeah, I do. For you. Uh, I mean, for your business."
            mc.name "Then he should respect what you want to do. If he doesn't, that's his problem."
            $ the_person.change_obedience(-1)
            $ the_person.change_slut_temp(1 + the_person.get_opinion_score("cheating on men"))
            $ the_person.discover_opinion("cheating on men")
            "[the_person.possessive_title] seems filled with a sudden resolve. She takes a deep breath and turns back towards the camera."
            the_person.char "You're right. Fuck him if he isn't happy about it."
            "She leans back against the wall and spreads her legs slightly."

        else:
            the_person.char "Yeah... Of course I do. You're right."
            "She takes a deep breath shakes her arms out, like an athlete about to perform. Her cute tits jiggle as she moves."
            the_person.char "You can do this. Just relax [the_person.title], you can do this."
            "She leans back against the wall and spreads her legs slightly."

    "[the_person.possessive_title] slowly runs her hand up her inner thigh. You can hear her breath catch in her throat as she comes closer to the top."
    "She stops just before she reaches her pussy and does it again, this time moving along the other thigh."
    "You take a few steps to the side to get a better angle of [the_person.title] as she sensually feels herself up."
    mc.name "That's great, now a little higher."
    "Her hand slides all the way up and her fingers glide gently over her slit."
    the_person.char "Ah..."
    "She hesitates for a second, then slips her middle finger into herself with a soft, throaty moan."
    "You take a few steps closer and take some more pictures."
    "[the_person.title]'s other hand comes up subconciously and cradles a breast as she starts to slowly finger herself."
    "Without any prompting she starts to speed up. Her breathing gets louder and she slides a second finger inside."

    $ slut_willingness = the_person.sluttiness
    if the_person.obedience > 100:
        $ slut_willingness += the_person.obedience - 100
    $ slut_willingness += the_person.get_opinion_score("giving blowjobs") * 5
    menu:
        "Suck my cock." if slut_willingness >= 70:
            mc.name "That's perfect [the_person.title]. Now just get onto your knees for me, we're going to get some hard core shots."
            call photo_blowjob(the_person) from _call_photo_blowjob_1

        "Suck my cock.\n{color=#ff0000}Not slutty or obedient enough{/color} (disabled)" if slut_willingness < 70:
            pass

        "Take photos as she climaxes.":
            the_person.char "Ah... Hah..."
            "[the_person.possessive_title] turns her head away from the camera and closes her eyes to focus on the task at hand."
            "She moves both hands down to her pussy, fingering herself with one and rubbing her clit with the other."
            the_person.char "Do... oh god, do you want me to go all the way?"
            mc.name "Yes, I do. We'll get some great photos out of this."
            "She moans louder and tilts her head back."
            the_person.char "I'm... going to cum! Fuck!"
            $ the_person.change_slut_temp(3)
            $ the_person.change_happiness(5)
            "She gasps and tenses up, both hands moving as fast as she can make them."
            "Then the tension melts away and she slumps a little against the wall. She sighs and opens her eyes."
            the_person.char "Did you get that?"
            mc.name "Yeah, I got it."
            the_person.char "Good, I don't think I could manage that again. Whew..."
            "[the_person.title] goes to get cleaned up and you finish up the shoot."
            $ the_person.review_outfit()
            return the_person.outfit.slut_requirement + (the_person.sex_skills["Foreplay"] * 5)
    return _return

label photo_blowjob(the_person):
    $ the_person.event_triggers_dict["camera_suck"] = True
    #TODO: boyfriend might call while she's "busy with work." Alternates between talking to him and sucking your cock on the phone.

    if the_person.sluttiness >= 70:
        "You step towards her and [the_person.title] kneels down."
        the_person.char "Make sure I'm in focus."
        "She reaches for your pants and unzips your fly."

    else:
        if the_person.relationship != "Single":
            $ SO_title = SO_relationship_to_title(the_person.relationship)
            the_person.char "Wait, wait, wait. This really crosses a line, don't you think?"
            mc.name "What do you mean?"
            the_person.char "I can justify doing some nude shots. I can understand wanting some sensual shots with me touching myself."
            the_person.char "But how could I ever tell my [SO_title] about giving someone else a blowjob?"
            "She crosses her arms and looks away."
            "You lower the camera and take a step closer to [the_person.possessive_title]. You reach out and touch her shoulder. She looks up at you."
            mc.name "Don't think about your [SO_title] right now. Think about me, and the business, and what you want to do."
            mc.name "We can make sure he never sees these ads. I need you, [the_person.title]."
            "Her expression softens. Finally she sighs and uncrosses her arms."
            the_person.char "I... I can't believe I'm going to do this. Make sure to get plenty of good shots, make this worth it."
            "She kneels down in front of you and unzips your fly for you."

        else:
            "She takes unsteady step forward, then pauses."
            the_person.char "I don't know [the_person.mc_title]..."
            mc.name "It's for the company [the_person.title], don't let me down now."
            "After a moment of hesitation she comes closer and kneels down. She reaches out and undoes your fly."


    $ the_person.draw_person(position = "blowjob")
    "You hold the camera in one hand, positioning it to the side as [the_person.possessive_title] pulls your pants down."
    the_person.char "Let's see what I'm working with down here."
    "Your hard cock springs free of your underwear as she yanks it down."
    if the_person.sluttiness >= 70 or the_person.get_opinion_score("giving blowjobs") > 0:
        the_person.char "Mmm, that's what I like to see."
    else:
        the_person.char "Sweet Jesus..."
    $ the_person.draw_person(position = "blowjob", special_modifier = "blowjob")
    "She licks at the tip a couple of times, then slips it into her mouth."
    "You feel [the_person.title]'s tounge lick at the bottom of your shaft as she starts to move her head, bobbing it back and forth."
    "You try to stay focused and snap a few more pictures as she sucks you off."


    $ slut_willingness = the_person.sluttiness
    if the_person.obedience > 100:
        $ slut_willingness += the_person.obedience - 100
    $ slut_willingness += the_person.get_opinion_score("vaginal sex") * 5
    menu:
        "Fuck her." if the_person.sluttiness >= 80:
            mc.name "We've come this far, there's only one more thing we can do. Lie down so I can fuck you."
            $ the_person.draw_person(position = "blowjob")
            call photo_sex(the_person) from _call_photo_sex_1

        "Take photos as you cum.":
            mc.name "I'm going to cum, get ready!"
            $ the_person.draw_person(position = "blowjob")
            "You pull your cock out of [the_person.possessive_title]'s mouth and stroke it off with your left hand, working the camera with your right."
            "She looks up at you as you cum, blowing your hot load over her face. You struggle to keep the camera pointed in the right direction."
            $ the_person.cum_on_face()
            $ the_person.draw_person(position = "blowjob")
            $ the_person.change_slut_temp(the_person.get_opinion_score("being covered in cum"))
            $ the_person.discover_opinion("being covered in cum")
            "It takes you a couple long seconds to recover from your orgasm."
            "When you're able to you recenter the camera and take a few pictures of [the_person.title]'s cum splattered face."
            the_person.char "How do I look?"
            mc.name "Beautiful. Smile for the camera!"
            "Once you've taken all the pictures you think you'll need you get cleaned up."
            $ the_person.review_outfit()
            return the_person.outfit.slut_requirement + 10 + (5* the_person.sex_skills["Oral"])
    return _return

label photo_sex(the_person):
    $ the_person.event_triggers_dict["camera_fuck"] = True
    #TODO: Add a crisis where her boyfriend recognizes her after this event has taken place.

    if the_person.sluttiness < 80:
        if the_person.relationship != "Single":
            $ SO_title = SO_relationship_to_title(the_person.relationship)
            the_person.char "I can't do that [the_person.mc_title], my [SO_title]..."
            mc.name "We've gone so far already, what's the difference? Just relax and do what feel natural."
            "Her resistance wavers, then melts away."
            #TODO: Make her break up with her boyfriend while you fuck her.
        else:
            the_person.char "I can't do that [the_person.mc_title]..."
            mc.name "We've gone so far already, what's the difference? Just relax and do what feel natural."
            "Her resistance wavers, then melts away."
    else:
        "[the_person.title] nods excitedly."

    $ the_person.draw_person(position = "missionary")
    "She lies down and you get on your knees. You pull her close to you, legs to either side with her pussy in line with your hard cock."
    $ mc.condom = False #Just in case we didn't maintain it properly or something
    call condom_ask(the_person) from _call_condom_ask_2
    "You pull on [the_person.title]'s hips and thrust forward. Her pussy is warm and wet, inviting you in."
    $ the_person.call_dialogue("sex_responses")
    "You thrust as best you can from a kneeling position, your hands busy with the camera."
    "You take pictures of [the_person.possessive_title]'s face as you fuck her and her cunt as you slide in and out."
    if the_person.relationship != "Single" and the_person.sluttiness > 65:
        "You hear [the_person.title] mumble to herself."
        the_person.char "I'm sorry sweetheart, but this feels so good..."

    "You lay into her, fucking her until you feel your orgasm approaching."
    $ the_person.change_slut_temp(5)
    $ came_inside_mod = 0
    menu:
        "Cum on [the_person.title].":
            $ the_person.change_slut_temp(the_person.get_opinion_score("being covered in cum"))
            $ the_person.discover_opinion("being covered in cum")
            if mc.condom:
                "You pull out of [the_person.title]'s tight pussy. You whip the condom off with your left hand, then start to stroke yourself to completion."

            else:
                "You pull out of [the_person.title]'s tight pussy and grab it with your left hand, stroking yourself to completion."

            "You fire your load out over her, struggling to keep the camera pointed in the right direction."
            $ the_person.cum_on_stomach()
            $ the_person.draw_person(position = "missionary")
            "She gasps softly as she is spattered with your hot cum. For a few seconds you're both quiet as you catch your breath."

        "Creampie her." if not mc.condom:
            $ the_person.change_slut_temp(the_person.get_opinion_score("creampies"))
            $ the_person.discover_opinion("creampies")
            "You pull on [the_person.title]'s hips one handed and thrust as deep as you can into her."
            $ the_person.cum_in_vagina()
            "You stay tight against her while you pump your hot load deep inside of her pussy. She closes her eyes and moans."
            "For a few seconds you're both quiet, panting for breath. You make sure to get some pictures as you pull out and your cum drips out of her cunt."
            if the_person.relationship != "Single":
                if the_person.sluttiness < 90:
                    the_person.char "I'm so sorry... I'm so sorry sweetheart."
                else:
                    $ SO_title = SO_relationship_to_title(the_person.relationship)
                    the_person.char "I hope my [SO_title] doesn't mind if I get pregnant. I'll just say it's his I guess."

            else:
                the_person.char "Fuck, that was intense."

            $ came_inside_mod = 10

        "Creampie her. (disabled)" if mc.condom:
            pass

    mc.name "I think I got all the pictures I'll need."
    the_person.char "I would hope so. Hell of a time to realise the lens cap was on."
    $ mc.condom = False
    $ the_person.review_outfit()
    return the_person.outfit.slut_requirement + 15 + (5* the_person.sex_skills["Vaginal"]) + came_inside_mod

label photo_strip_naked(the_person): #A helper label that strips a girl until her top and bottom are available for whatever you want to use them fore
    #Possible alternative: just strip until tits and vagina are usable.
    while the_person.outfit.get_upper_top_layer() is not None or the_person.outfit.get_lower_top_layer() is not None: #Strip until the top and bottom are empty, ie not None.
        $ the_item = the_person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True)
        $ the_person.draw_animated_removal(the_item)
        "" #Just so they can click through and see each thing removed.
    return

label ad_expire(the_amount):
    $ mc.business.remove_sales_multiplier("Ad Campaign", the_amount)
    return
