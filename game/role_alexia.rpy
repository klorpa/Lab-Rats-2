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

#TODO: Visit her at the coffee shop again and ask her to work for you.

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
    return








#TODO: She wants to start a marketting campaign.
