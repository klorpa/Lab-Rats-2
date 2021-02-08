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
        elif the_person.love < 10:
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
        if public_advertising_license_policy.is_owned():
            return False
        elif not day > the_day:
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
        if public_advertising_license_policy.is_owned():
            return False
        elif not the_person.event_triggers_dict.get("camera_reintro_enabled", False):
            return False
        elif the_person.event_triggers_dict.get("camera_purchased", True):
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
        if public_advertising_license_policy.is_owned():
            return False
        elif not mc.business.event_triggers_dict.get("has_expensive_camera",False):
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

    def ad_expire_requirement(the_day):
        if day > the_day:
            return True
        return False

label alexia_phase_zero_label():
    #Sets Alexia's schedule so she is downtown during time periods 1,2,3.
    $alexia.set_schedule(downtown, times = [1,2,3])
    return

label alexia_intro_phase_one_label(the_person):
    the_person "[the_person.mc_title]? [the_person.mc_title] is that you?"
    "You hear your name behind you and turn around to see a familiar face."
    $ the_person.draw_person(emotion = "happy")
    mc.name "[the_person.title]?"
    the_person "Yeah, it's me! I didn't know you were still in town, I thought you might have moved away."
    mc.name "I was just passing through, but yeah I'm still around. How about you?"
    if time_of_day == 1:
        the_person "Me too. I was just heading to work actually."

    elif time_of_day == 2:
        the_person "Me too. I'm on my lunch break and wanted to take a walk."

    else: #time_of_day == 3:
        the_person "Me too. I was just heading home from work actually."

    mc.name "Well I guess I got lucky running into you! Where are you working? Making use of that biology degree?"
    "[the_person.title] sighs and shrugs."
    the_person "Not really, but that's a long story. I've got a part time job at a coffee shop right now."
    mc.name "That's still an important job! Lots of people like coffee and someone's got to serve it."
    "She laughs and touches your arm."
    the_person "Do you? Like coffee, I mean. I've got to run, but I'd love to catch up with you. If you come by at the end of my shift I'll buy you a drink."
    menu:
        "I'd love to.":
            mc.name "That sounds like a great idea. I'll make sure to come by as soon as I can."
            $ the_person.change_happiness(2)
            $ the_person.change_love(1)
            the_person "It's a date then!"

        "I don't think I'll have time.":
            mc.name "I've been really busy lately, so I'm not sure I'll have time."
            $ the_person.change_happiness(-2)
            the_person "I understand. The offer stands, if your schedule ever changes."

    "[the_person.title] gives you the address of her coffee shop."
    $ the_person.draw_person(position = "walking_away")
    the_person "I've got to run, but I hope I'll see you around!"
    "You wave goodbye to [the_person.possessive_title] as she walks away."

    python:
        alexia_intro_phase_two_action = Action("Visit " + the_person.title + " at work", alexia_intro_phase_two_requirement, "alexia_intro_phase_two_label", args = the_person, requirement_args = the_person)
        downtown.actions.append(alexia_intro_phase_two_action)
        downtown.move_person(the_person, the_person.home) #Change her schedule again so you don't see her anymore unless you visit her explicitly.
        alexia.set_schedule(alexia.home, times = [1,2,3])
    $ clear_scene()
    return

label alexia_intro_phase_two_label(the_person):
    # Have a coffee together. She talk about what she's been doing, introduce her boyfriend.

    #TODO: Add a new background for the coffee shop (and other events that take place here?)
    "You find the coffee shop [the_person.title] works at. It's a small corner unit, with a patio outside full of patrons."
    #TODO: Add a waitress outfit for her
    $ the_person.draw_person()
    "You step inside and see [the_person.possessive_title] behind the front counter. She smiles when she sees you and waves you over."
    the_person "Hey, I'm glad you were able to make it! I'm just finishing up my shift. Grab a seat and I'll be over in a minute."
    $ clear_scene()
    "She heads into the back room of the shop. You sit down at a small table for two by a window and wait."
    "A couple of minutes later [the_person.title] comes over with a paper cup in each hand. She puts one on the table and sits down opposite you."
    $ the_person.draw_person(position = "sitting")
    the_person "I think I remembered how you like your coffee. Do you remember all the afternoons we spent together, just hanging out and having coffee together?"
    mc.name "Of course, they're some of my best memories. I just wish we had stayed in touch. What happened to you?"
    "She looks out the window and swirls her coffee cup with one hand."
    the_person "Something about that summer was just confusing. I didn't know what I wanted to do, but biology wasn't it anymore."
    the_person "So I didn't come back for my last year. I did some traveling, a lot of thinking, and now I'm back here."
    "You sip at your coffee and listen to [the_person.possessive_title] talk."
    the_person "I'm sorry we never talked again. You must have thought I fell off the face of the Earth."
    menu:
        "I forgive you.":
            mc.name "It's okay [the_person.title], I think I understand what you were going through. I'm glad we're able to reconnect now."
            $ the_person.change_happiness(5)
            $ the_person.change_love(1)
            "She sighs and smiles."
            the_person "That means the world to me to hear. Thank you [the_person.mc_title]."

        "I missed you.":
            mc.name "When you disappeared it hurt, and I've missed you all this time. It's really strange having you pop back into my life again."
            $ the_person.change_happiness(-5)
            $ the_person.change_obedience(3)
            "She reaches across the table for your hand and holds it in hers."
            the_person "I promise I will never hurt you like that again. We've got a second chance to get to know each other as friends again."

    the_person "But enough about me, what have you been doing? Are you done with your degree?"
    menu:
        "Brag.":
            mc.name "More than that. You're looking at the proud owner of [mc.business.name], an independent pharmaceutical company."

        "Be Humble.":
            mc.name "I am. I work for a small pharmaceutical company now."
            the_person "That's great! What do you do there?"
            mc.name "A bunch of things, really. I manage the day to day operations, oversee production, R&D, sales..."
            the_person "It sounds like you practically run the place."
            mc.name "I suppose I do, since I own it."

    the_person "What? Come on, be serious."
    mc.name "I am! After I graduated I bought this little lab on the edge of town. We make small batch, limited run pharmaceuticals."
    the_person "That's amazing! Tell me more."
    "She leans forward in her chair and listens to you talk about your business. When you've both finished your coffee she checks the time."
    the_person "Your work sounds fascinating. I'm don't think I could ever do the science that it sounds like you do, but if you ever need someone to sell coffee for you, give me a call!"
    $ the_person.draw_person()
    "[the_person.title] laughs and stands up."
    the_person "It's time for me to head home. My ride should be here soon. Oh, do you want to come out and meet him?"
    "You stand up and walk out with [the_person.possessive_title]."
    mc.name "Uh, sure. Who is he?"
    "When you get outside [the_person.title] looks around for a moment, then waves to a car as it pulls over."
    the_person "Right on time! [the_person.SO_name], we met while I was traveling and we've been dating ever since."
    "A man steps out of the car. [the_person.title] hurries over and gives him a hug, then turns around to face you with her arm wrapped around his waist."
    the_person "Sweety, this is [the_person.mc_title]. He's an old friend of mine from university. [the_person.mc_title], this is [the_person.SO_name]."
    the_person.SO_name "Hey, it's nice to meet you."
    "He holds out his hand to shake yours."
    menu:
        "Be polite.":
            "You take his hand and shake it."
            mc.name "It's nice to meet you, too. I hope we'll have time to talk more in the future."
            $ the_person.change_happiness(3)
            the_person "That would be great, the three of us should meet up and have dinner, or see a movie, or something."

        "Be rude.":
            "You don't shake his hand."
            mc.name "Oh, [the_person.title] didn't even mention she was seeing anyone until now."
            $ the_person.change_love(-1)
            $ the_person.change_obedience(1)
            the_person "Sorry sweety, we got talking about [the_person.mc_title]'s work and it never came up."
            "She glares at you for a moment, but [the_person.SO_name] doesn't seem to notice."
            the_person.SO_name "Well, we'll have to fix that. If you two are friends we should have dinner together, so you can catch up."

    $ clear_scene()
    "[the_person.title] gets into the passenger side of her boyfriend's car. She says goodbye from inside and they drive off."
    python:
        downtown.actions.remove(alexia_intro_phase_two_action) #Clear the action from her actions list.
        alexia.set_schedule(downtown, times = [1,2,3]) #She spends her time downtown "working".

        alexia_hire_action = Action("Hire " + alexia.title + " to work in sales.", alexia_hire_requirement, "alexia_hire_label")
        the_person.get_role_reference_by_name("Alexia").actions.append(alexia_hire_action)
    call advance_time from _call_advance_time_18
    return



label alexia_hire_label(the_person):
    #Hire her onto your marketing team.
    mc.name "[the_person.title], do you like your job at that coffee shop?"
    the_person "Do I like it? Not really, but it pays the bills. Why?"
    mc.name "[mc.business.name] is expanding and I need competent people. You're pretty good at selling coffee - I think you'd be perfect for my marketing team."
    the_person "You're being serious? Oh man, I don't know what to say [the_person.mc_title]."
    mc.name "How about \"I'll do it\"? I promise I pay better than your coffee place does."
    $ the_person.change_happiness(5)
    $ the_person.change_love(2)
    the_person "Okay, I'll do it! Thank you [the_person.mc_title]! Or should I call you boss now?"
    menu:
        "[the_person.mc_title] is fine.":
            mc.name "No need to be too formal. I want you around because you're a friend and we make a good team."
            $ the_person.change_love(1)

        "Boss sounds good.":
            $ the_person.set_mc_title("Boss")
            mc.name "I guess I am your boss now, aren't I. I like the way that sounds."
            $ the_person.change_obedience(2)
            the_person "Okay then [the_person.mc_title], you got it!"

    $ the_person.draw_person(emotion = "happy") #TODO: When we have a hugging position draw them as happy.
    the_person "So, when can I start?"
    "You give [the_person.title] all of the details about her new job. She phones the coffee shop and quits on the spot."
    python: #TODO: Consider calling the "hire someone" label instead of having a special section for this.
        the_person.event_triggers_dict["employed_since"] = day
        mc.business.listener_system.fire_event("new_hire", the_person = the_person)
        the_person.add_role(employee_role)
        for other_employee in mc.business.get_employee_list():
            town_relationships.begin_relationship(the_person, other_employee) #She is introduced to everyone at work

        mc.business.add_employee_marketing(the_person)
        the_person.set_work(mc.business.m_div)
        the_person.get_role_reference_by_name("Alexia").actions.remove(alexia_hire_action) #Remove the hire action because this story event has played itself out.

        ad_suggest_event = Action("Ad Suggestion", alexia_ad_suggest_requirement, "alexia_ad_suggest_label", args = the_person, requirement_args = [the_person, day + renpy.random.randint(7,12)])
        mc.business.mandatory_crises_list.append(ad_suggest_event)
    return


label alexia_ad_suggest_label(the_person):
    $ the_person.draw_person()
    the_person "Knock, knock. Hey [the_person.mc_title], do you have a second?"
    "[the_person.title] is at your office door."
    mc.name "For you, always. What's up?"
    the_person "So I was getting some boxes ready for shipping and I had a thought."
    the_person "I know this might be silly, but back at the coffee shop when we had takeout orders we would add a little flier."
    "You nod and listen, noticing now that she has a business card sized piece of paper."
    the_person "I put together this mockup, super rough, to show you. I think it would really help boost sales."
    "She hands over her example business card. It has [mc.business.name] written in bold across the top and [the_person.title] posing with a vial of serum."
    the_person "What do you think? I put myself in as a place holder, so we would just need to hire a model to be eye candy."
    "You look it over and think for a minute."
    mc.name "I think this is a great idea and you've done great work here."
    $ the_person.change_happiness(5)
    $ the_person.draw_person(emotion = "happy")
    mc.name "I also don't think we would need to hire a model."
    the_person "What do you mean?"
    menu:
        "You're all the eye candy we need.":
            mc.name "You're all the eye candy we need. We can take a few high quality pictures of you and we're good to go."
            $ the_person.change_slut_temp(2)
            $ the_person.change_love(1)
            "[the_person.title] blushes and waves her hand at you dismissively."
            the_person "Oh come on, you know we could find someone better for it. But I guess if I did it we would save some money."
            the_person "If it's just a few quick shots, I suppose I wouldn't mind."

        "We would save money if you were the model.":
            mc.name "You look perfect for the role in this mockup already. We can take a few high quality pictures and these would be ready for production."
            $ the_person.change_obedience(2)
            $ the_person.change_happiness(1)
            "[the_person.title] seems relieved."
            the_person "Right, of course that's what you mean. I guess if it's just a few quick shots, I wouldn't mind."

    mc.name "Good to hear. What will you need to get this going?"
    the_person "We should probably get a proper camera instead of my phone, and we'll need to pay to have the cards printed professionally."
    menu:
        "Pay for equipment. -$500" if mc.business.funds >= 500:
            mc.name "That sounds reasonable. Buy whatever you think is reasonable and I will cover the expense."
            $ mc.business.funds += -500
            the_person "You got it! I'll order it A.S.A.P and let you know when it arrives."
            mc.name "Great work [the_person.title], you're a credit to the team."
            $ camera_arrive_action = Action("Camera Arrive", camera_arrive_requirement, "alexia_ad_camera_label", args = the_person, requirement_args = day + renpy.random.randint(3,7))
            $ mc.business.mandatory_crises_list.append(camera_arrive_action)
            $ the_person.event_triggers_dict["camera_purchased"] = True

        "Pay for equipment. -$500 (disabled)" if mc.business.funds < 500:
            pass

        "Talk to her later.":
            $ the_person.event_triggers_dict["camera_reintro_enabled"] = True
            mc.name "Okay, I'll come talk to you soon and we can sort out these details. Great work [the_person.title], you're a credit to the team."

    the_person "Thanks [the_person.mc_title], I'm just happy to have a chance to contribute!"



    return

label alexia_ad_suggest_reintro_label(the_person):
    mc.name "[the_person.title], I want you to order whatever camera equipment you think is best for your ad photoshoot."
    the_person "Okay. I'll get right on that and order it ASAP!"
    mc.name "Send me any receipts and I'll cover the cost."
    $ mc.business.funds += -500
    $ camera_arrive_action = Action("Camera Arrive", camera_arrive_requirement, "alexia_ad_camera_label", args = the_person, requirement_args = day + renpy.random.randint(3,7))
    $ mc.business.mandatory_crises_list.append(camera_arrive_action)
    $ the_person.event_triggers_dict["camera_purchased"] = True
    $ the_person.event_triggers_dict["camera_reintro_enabled"] = False
    return

label alexia_ad_camera_label(the_person):
    if mc.business.get_employee_workstation(the_person): #ie is an employee, otherwise this is None.
        "You get a text from [the_person.title]."
        the_person "Hey [the_person.mc_title], the camera for that ad idea I had just arrived."
        the_person "Come see me when you want to do something with it."
    else: #In case you've fired them or something. Future proofing mostly.
        "A package is delivered during the day. It's the camera [the_person.title] ordered while she was still working for you."
    $ mc.business.event_triggers_dict["has_expensive_camera"] = True
    return

label alexia_photography_intro_label(the_person):
    # You shoot your business cards. Results in a minor (%1) boost in sales values and gives you an opportunity to tell Alexia to pose for you.
    mc.name "Are you ready for our photoshoot?"
    the_person "As ready as I'll ever be, I suppose. I found a good spot in the storage room. It has plenty of light and a blank wall."
    mc.name "Excellent. Let's go."
    # TODO: Change location? Just change background art?
    "You and [the_person.possessive_title] go to the storage room. Once you get there she hands you the new camera."

    the_person "Here you go [the_person.mc_title]. How do you want to do this?"
    mc.name "Let's start with some basic shots of you. Just act natural and look into the camera."
    $ the_person.draw_person(position = "stand4")
    "You frame up [the_person.title] and take a few pictures."
    the_person "How's that?"
    mc.name "Good. Try another pose."
    $ the_person.draw_person(position = "stand5")
    mc.name "Perfect. Now try turning around."
    $ the_person.draw_person(position = "back_peek")
    "You snap pictures as she poses."
    menu:
        "Focus on her ass.":
            mc.name "Bend forward just a little bit for me. Let's show off your butt."
            the_person "Really? Do you think that's important?"
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
    the_person "I think that's everything I need to get this business card designed. I'll order them and have them ready for the next shipment out."
    $ mc.business.add_sales_multiplier("Business Cards", 1.01)
    mc.name "Good work [the_person.title]. I've been very impressed."
    the_person "Thanks, this was fun! If you think this advertising thing is working out we could try putting ads in magazines and stuff."
    mc.name "I think that's another good idea, as long as you want to do the modeling for it."
    $ the_person.change_obedience(1)
    the_person "Yeah, I can do that! I don't know why, but I thought it was really exciting to be in front of that camera."
    mc.name "I'll let you get back to work then. See you around [the_person.title]."
    if mc.business.company_model is not None:
        $ mc.business.company_model.remove_role(company_model_role) #If we somehow ended up with her here, fire her.
    $ mc.business.company_model = the_person
    $ the_person.add_role(company_model_role) #Now we just make Alexia a model instead of having this be specific to her role. You get there by either buying the policy or following her storyline here.

    $ public_advertising_license_policy.buy_policy(ignore_cost = True) # This special storyline "buys" the policy for free.
    call advance_time from _call_advance_time_19
    return
