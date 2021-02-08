### All of the events related to the employee freeuse role, made available by some punishment options,.
init -2 python:
    def employee_freeuse_remove_requirement(the_person, trigger_day):
        if day >= trigger_day:
            return True
        return False

    def freeuse_fuck_requirement(the_person):
        if not mc.is_at_work():
            return False
        elif not mc.business.is_open_for_business():
            return False
        return True

    def employee_freeuse_report_requirement(the_person):
        if not mc.business.is_open_for_business():
            return False
        elif not mc.is_at_work():
            return False
        return True

label employee_freeuse_remove_label(the_person):
    python:
        the_person.remove_role(employee_freeuse_role)
        if the_person.has_role(employee_role):
            freeuse_report_action = Action("Freeuse report crisis", employee_freeuse_report_requirement, "employee_freeuse_report_label", args = the_person, requirement_args = the_person)
            mc.business.mandatory_crises_list.append(freeuse_report_action)
    return

label employee_freeuse_report_label(the_person):
    $ the_person.draw_person()
    "[the_person.title] catches your attention while you are working."
    the_person "Do you have a moment [the_person.mc_title]?"
    mc.name "Sure, what do you need?"
    the_person "I wanted to let you know that I've finished my week of punishment."
    mc.name "Good, I hope you've learned your lesson."
    if the_person.effective_sluttiness() > 80 and the_person.get_opinion_score("being submissive") + the_person.event_triggers_dict.get("freeuse orgasms", 0) > 3: #You have to make her cum, more is better depending on her opinion.
        the_person "I have, and I know what I want now [the_person.mc_title]..."
        "She bites her lip and looks at the floor, avoiding your eye contact while she speaks softly."
        the_person "I don't want my punishment to end."
        mc.name "Sorry? I don't think I quite heard you."
        "[the_person.possessive_title] looks up at you, a sudden hunger in her eyes."
        the_person "I don't want you to stop fucking me! I like it, no, I love it!"
        the_person "When you just grab me and take me, like I'm just a fuck toy!"
        "She closes her eyes and moans."
        the_person "It makes me so wet, and I always cum so hard on your dick!"
        the_person "So don't stop my punishment, or I'll just have to keep breaking rules until you do this to me again."
        the_person "Please, [the_person.mc_title], can you keep punishing me?"
        menu:
            "Extend her punishment indefinitely.":
                $ the_person.event_triggers_dict["willing_freeuse"] = True
                $ the_person.add_role(employee_freeuse_role)
                "[the_person.title] waits impatiently as you consider her request."
                mc.name "I suppose I don't have any choice if I want to avoid future disciplinary problems."
                mc.name "Fine, consider your punishment extended indefinitely. You're my office slut now, I hope you're happy."
                $ the_person.change_happiness(10)
                $ the_person.change_obedience(5)
                "She nods eagerly."
                the_person "I am, oh god I'm so happy [the_person.mc_title]!"
                the_person "Do you want to fuck, right now?"
                menu:
                    "Use her right now.":
                        call employee_freeuse_fuck(the_person) from _call_employee_freeuse_fuck
                        mc.name "I think this arrangement is going to work out well for both of us."
                        the_person "Ah... Thank you [the_person.mc_title]!"
                        mc.name "You've had enough fun, get back to work."

                    "Send her away.":
                        mc.name "Not right now. Get out of here."


            "Refuse her request.":
                mc.name "This was never about what you want, or what you enjoy. Your punishment is over."
                mc.name "I don't want to listen to you complain, understood."
                the_person "Yes [the_person.mc_title], I'm sorry..."
                mc.name "Good. Get out of here."
    "She nods and steps away."
    $ clear_scene()
    return

label employee_freeuse_fuck(the_person):
    #Special action to fuck her on the spot. No option to be private about it (that's the whole point!)
    if the_person.event_triggers_dict.get("willing_freeuse", False):
        # She's happy to have you use her
        mc.name "Come here, I'm horny."
        "[the_person.possessive_title] nods eagerly."
        the_person "Yes [the_person.mc_title], right away!"
        $ the_person.add_situational_obedience("freeuse", 60, "This is what I wanted. I want him to tell me what to do, even if I don't want to do it.")
    else:
        mc.name "Come here, I'm horny."
        "[the_person.possessive_title] nods obediently."
        $ the_person.add_situational_obedience("freeuse", 60, "This is part of my punishment, I agreed to this and I can't say no.")

    if the_person.get_opinion_score("being submissive") > 0:
        $ the_person.add_situational_slut("freeuse", 5*the_person.get_opinion_score("being submissive"), "Someone using me, just like a toy... It's making me so wet!")
    elif the_person.get_opinion_score("being submissive") < 0:
        $ the_person.add_situational_slut("freeuse", 5*the_person.get_opinion_score("being submissive"), "I'm being used like a toy, it feels so heartless!")
    call fuck_person(the_person, private = False) from _call_fuck_person_6
    $ the_person.clear_situational_obedience("freeuse")
    $ the_person.clear_situational_slut("freeuse")
    $ the_report = _return
    if the_person.event_triggers_dict.get("freeuse orgasms", 0) > 0:
        $ the_person.event_triggers_dict["freeuse orgasms"] += the_report.get("girl orgasms", 0)
    else:
        $ the_person.event_triggers_dict["freeuse orgasms"] = the_report.get("girl orgasms", 0)
    return
