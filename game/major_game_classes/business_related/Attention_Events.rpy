
init -2 python:
    def attention_event_requirement():
        if mc.business.is_work_day() and time_of_day == 1:
            return True
        return False

    def attention_fine_requirement(the_person):
        return True

    def attention_seize_inventory_requirement(the_person):
        if mc.business.inventory.get_any_serum_count() >= 10:
            return True
        return False

    def attention_seize_supplies_requirement(the_person):
        if mc.business.supply_count >= 200:
            return True
        return False

    def attention_seize_research_requirement(the_person):
        for design in mc.business.serum_designs:
            if design.researched:
                return True
        return False

    def attention_illegal_serum_requirement(the_person):
        for design in mc.business.serum_designs:
            if design.researched:
                return True
        return False

label attention_event():

    $ city_rep.event_triggers_dict["currently_interogating"] = True #Set to False so we can use Role actions without them appearing when you meet her somewhere else.
    $ city_rep.event_triggers_dict["bribe_attempts"] = [] #Reset our list so we can avoid letting you repeatedly bribe her
    $ city_rep.event_triggers_dict["bribe_successful"] = None #Store the most recently used bribe option so we can have some specific dialogues


    if city_rep.event_triggers_dict.get("city_rep_forced_uniform", False):
        $ city_rep.apply_outfit(city_rep.event_triggers_dict.get("city_rep_forced_uniform", Outfit("Nude")))
    else:
        $ city_rep.apply_outfit(city_rep.wardrobe.build_appropriate_outfit(city_rep.sluttiness))

    if mc.is_at_work():
        call attention_already_in(city_rep)
    else:
        call attention_call_to_work(city_rep)

    call attention_visit(city_rep)

    #TODO: Have an option to have your girls "distract" the enforcers so they find nothing.

    python:
        attention_fine_action = Action("attention_fine", attention_fine_requirement, "attention_pay_fine")
        attention_seize_inventory_action = Action("attention_seize_inventory", attention_seize_inventory_requirement, "attention_seize_inventory")
        attention_seize_supplies_action = Action("attention_seize_supplies", attention_seize_supplies_requirement, "attention_seize_supplies")
        attention_seize_research_action = Action("attention_seize_research", attention_seize_research_requirement, "attention_seize_research")
        attention_illegal_serum_action = Action("attention_illegal_serum", attention_illegal_serum_requirement, "attention_illegal_serum")

        attention_events = [attention_fine_action, attention_seize_inventory_action, attention_seize_supplies_action, attention_seize_research_action, attention_illegal_serum_action]
        valid_events = []
        for an_attention_event in attention_events:
            if an_attention_event.is_action_enabled(city_rep):
                valid_events.append(an_attention_event)


    $ picked_event = get_random_from_list(valid_events)

    $ city_rep.draw_person()

    $ bribe_result = city_rep.event_triggers_dict.get("bribe_successful", None)
    if bribe_result == "cash":
        "[city_rep.title]'s enforcers come back. Before they can report anything she orders them outside."
        city_rep "I've levied a fine and taken care of the paperwork. [city_rep.mc_title] was very cooperative."

    elif bribe_result == "order":
        "[city_rep.title]'s enforcers come back. Before they can report anything she orders them outside."
        city_rep "We're done here."
        "The two bruisers look at each other, a little confused. [city_rep.title] snaps at them."

    elif bribe_result == "orgasm":
        "[city_rep.title]'s enforcers come back. Before they can report anything she orders them outside."
        city_rep "I've had a long talk with [city_rep.mc_title], and we've come to a..."
        "Her eyes dart down to your crotch for a moment, then she gets herself under control."
        city_rep "...satisfying agreement."

    else:
        $ picked_event.call_action(city_rep)

    city_rep "I think we're done here men. Thank you for your cooperation [city_rep.mc_title]."
    "She leaves the building with her city toughs following behind her."


    $ mc.business.event_triggers_dict["attention_event_pending"] = False
    $ mc.business.attention = int(mc.business.attention/2)

    $ times_visited = mc.business.event_triggers_dict["attention_times_visited"] = mc.business.event_triggers_dict.get("attention_times_visited", 0) + 1
    $ city_rep.event_triggers_dict["currently_interogating"] = True #Set to False so we can use Role actions without them appearing when you meet her somewhere else.
    $ city_rep.event_triggers_dict["bribe_attempts"] = [] #Reset our list so we won't accidentally trigger something outside of this event.
    $ clear_scene()
    "You're glad to finally left alone, but the encounter has eaten up most of the day."
    return "Advance Time"

label attention_pay_fine(the_person):
    $ fine_amount = round(mc.business.calculate_salary_cost()*0.01)*1000 #ie. costs 10x a days staff cost, rounded to the nearest $100
    if fine_amount < 100:
        $ fine_amount = 100

    if the_person.event_triggers_dict.get("city_rep_reduced_penalties_trained", False):
        $ fine_amount = fine_amount/2

    "[the_person.title]'s enforcers come back. One shakes his head, and she nods some secret understanding."
    the_person "I think we're all done here."
    "She pulls another piece of paper out of her purse and hands it over."

    the_person "Here is your receipt for your fine."
    the_person "Funds should have already been seized from your accounts, so you don't have anything else to worry about."
    mc.name "How convenient."
    if the_person.event_triggers_dict.get("city_rep_reduced_penalties_trained", False):
        "She pauses."
        the_person "On second thought, let me take a look at that..."
        "She takes back the receipt and produces a pen."
        the_person "This fee seems a touch excessive. I think it would be fair to lower it a touch..."
        "[the_person.title] alters the document and hands it back to you."
        the_person "There, that should be more reasonable."
    else:
        "She ignores your sarcasm and moves on."
    $ mc.business.change_funds(-fine_amount)
    $ mc.log_event("$" + str(fine_amount) + " seized!", "float_text_red")
    return

label attention_seize_inventory(the_person):
    python:
        inventories = [mc.business.inventory]
        for contract in mc.business.active_contracts:
            inventories.append(contract.inventory)

        highest_attention_design = None
        for inventory in inventories:
            for design in inventory.get_serum_type_list():
                if highest_attention_design is None or design.attention > highest_attention_design.attention:
                    highest_attention_design = design

    if highest_attention_design:
        $ doses_seized = 0
        python:
            inventories = [mc.business.inventory]
            for contract in mc.business.active_contracts:
                inventories.append(contract.inventory)

            for inventory in inventories:
                design_list = inventory.get_serum_type_list()
                for design in design_list:
                    if design.attention == highest_attention_design.attention:
                        if the_person.event_triggers_dict.get("city_rep_reduced_penalties_trained", False):
                            doses_seized += inventory.get_serum_count(design)/2
                            inventory.change_serum(design, -inventory.get_serum_count(design)/2)
                        else:
                            doses_seized += inventory.get_serum_count(design)
                            inventory.change_serum(design, -inventory.get_serum_count(design))

    "[the_person.title]'s enforcers return. One is holding one of the cardboard boxes you use to store ready-to-ship serum."
    "Enforcer" "Found it Ma'am, right where you said it would be."
    the_person "Good. Let me take a look..."
    "[the_person.possessive_title] flips open one of the boxes and pulls out the plastic vial inside."
    $ highest_attention_design_name = highest_attention_design.name
    the_person "Hmmm, [highest_attention_design_name]. How... descriptive."
    "She slips it back into it's box and turns back to you."
    if the_person.event_triggers_dict.get("city_rep_reduced_penalties_trained", False):
        the_person "We'll be taking..."
        "She pauses. You can see the trance-planted obedience taking hold."
        the_person "... Some of this with us. You, go put half of that back."
        "Enforcer" "Ma'am? Are you sure?"
        the_person "Of course I'm sure! Now hurry up, before I have to report you when we get back."
        "Enforcer" "Sorry Ma'am. Right away Ma'am."
    else:
        the_person "We'll be taking this with us for further investigation."
        mc.name "Will I be getting them back?"
        "She shakes her head politely."
        the_person "No. You won't."
    $ mc.log_event(str(doses_seized) + " of serum seized!", "float_text_red")
    return

label attention_seize_supplies(the_person):
    "[the_person.title]'s enforcers come back. One is carrying pile of cardboard boxes."
    "Enforcer" "All done Ma'am. Found their supply room."
    "[the_person.title] nods and turns to you."
    if the_person.event_triggers_dict.get("city_rep_reduced_penalties_trained", False):
        the_person "We'll be taking all of this..."
        "She glances at you, and the trance-planted obedience takes hold."
        the_person "...Half of it. We'll be taking half of it with us."
        "Enforcer" "Are you sure Ma'am?"
        the_person "Yes I'm sure! Now hurry up, I don't want to be here all day."
    else:
        the_person "We'll be taking this with us for further analysis."
    $ supply_seized = mc.business.supply_count
    if the_person.event_triggers_dict.get("city_rep_reduced_penalties_trained", False):
        $ supply_seized = supply_seized/2
    $ mc.business.supply_count += -supply_seized
    $ mc.log_event(str(supply_seized) + " serum supply seized!", "float_text_red")
    return

label attention_seize_research(the_person):
    $ highest_attention_design = None
    python:
        for design in mc.business.serum_designs:
            if design.researched:
                if highest_attention_design is None or design.attention > highest_attention_design.attention:
                    highest_attention_design = design

    if highest_attention_design:
        if the_person.event_triggers_dict.get("city_rep_reduced_penalties_trained", False):
            pass
        else:
            $ mc.business.remove_serum_design(highest_attention_design)
    else:
        "They are unable to find any of the research they were looking for."
        return

    "[the_person.title]'s enforcers return. One is holding a box of files. They look like they're from your lab."
    "Enforcer" "I think this is the right stuff, Ma'am. Not too sure, really"
    the_person "Let me take a look..."
    "[the_person.possessive_title] snatches the top file and flips through it."
    $ highest_attention_design_name = highest_attention_design.name
    the_person "\"Design and Manufacturing of [highest_attention_design_name]\". How very... descriptive."
    "She snaps the file closed again."
    if the_person.event_triggers_dict.get("city_rep_reduced_penalties_trained", False):
        the_person "This..."
        "[the_person.title] looks at you before making up her mind."
        the_person "Doesn't seem to be it."
        "Enforcer" "Are you sure? All of the reports say..."
        "She snaps at him, cutting him off mid sentence."
        the_person "I said it's not what we're looking for! Our reports must have been wrong."
    else:
        the_person "Yes, this is it. Take it all."
        $ mc.log_event(highest_attention_design_name + " design seized!", "float_text_red")

    return

label attention_illegal_serum(the_person):
    $ highest_attention_design = None
    python:
        for design in mc.business.serum_designs:
            if design.researched:
                if highest_attention_design is None or design.attention > highest_attention_design.attention:
                    highest_attention_design = design

    $ highest_attention_design_change = 2
    if highest_attention_design:
        if the_person.event_triggers_dict.get("city_rep_reduced_penalties_trained", False):
            $ highest_attention_design_change = 1
            # $ highest_attention_design.attention += 1

    if not highest_attention_design:
        "They can't find any serum research, and eventually stop searching."
        return #Just in case we've removed our highest design at some point so we don't crash out.
    "[the_person.title]'s enforcers return. One is holding one of the cardboard boxes of serum vials."
    "Enforcer" "Here you go Ma'am."
    the_person "You found them? Good."
    "[the_person.possessive_title] takes one of the vial and looks it over."
    $ highest_attention_design_name = highest_attention_design.name
    the_person "Yes, this what we're looking for."

    the_person "The city has signed a new law, banning the sale of substances like..."
    if the_person.event_triggers_dict.get("city_rep_reduced_penalties_trained", False):
        "She pauses to read the label, then glances at you. You can see the trance-planted obedience taking hold of her."
        the_person "[highest_attention_design_name]. It's a shame, if you ask me."
        mc.name "So, are you going to be taking it from me?"
        the_person "No, no. I will have to put in a report listing it as a substance of potential concern."
        the_person "But what you do with your current stock, well... That's none of my concern."
    else:
        "She pauses to read the label pasted onto the vial."
        the_person "[highest_attention_design_name]. Not soon enough, if you ask me."
        mc.name "So what, you're taking all of it?"
        the_person "Oh no, disposal is your responsibility. As long as we don't see any on the open market there are no issues."
        "She gives you a cold smile and hands the vial over to you."
        the_person "But if we do I'll have to come down for another visit. I don't think either of us want that."
    $ mc.log_event(highest_attention_design_name + " made illegal, +"+str(highest_attention_design_change)+" Attention!", "float_text_red")
    return

label attention_already_in(the_person):
    $ times_visited = mc.business.event_triggers_dict.get("attention_times_visited", 0)

    if times_visited == 0:
        "There's a hard banging on the front door of the office."
        the_person "Hello? Is anyone in?"
        "You consider ignoring the noise, but another round of hard knocks demands attention."
        $ the_person.draw_person()
        "When you enter the lobby you can see a formally dressed woman on the other side of the main glass doors."
        "She is flanked by two burly looking men wearing poorly fitting suits."
        "The woman is typing something on her phone. She glances up at you as you approach the door and puts her phone away."
        menu:
            "Open the door.":
                "You unlock the door and open it wide enough to have a conversation."
                mc.name "Hello? Can I help you?"
                the_person "Hello. Are you [the_person.mc_title]?"
                mc.name "I am, who are you?"
                "The woman pulls a piece of ID out of her wallet and hands it over for you to look at."
                $ the_person.set_title("Ms." + the_person.last_name)
                $ the_person.set_possessive_title("Your annoyance")
                the_person "I'm [the_person.title]. I've been sent by the city to have a little chat with you."

            "Yell through the door.":
                "Suddenly feeling uneasy, you keep the door locked and shout so you can be heard on the other side."
                mc.name "Hello? Can I help you?"
                the_person "Hello. Are you [the_person.mc_title]?"
                mc.name "I am, who are you?"
                "The woman pulls a piece of ID out of her wallet and presses it against the door for you to look at."
                $ the_person.set_title("Ms." + the_person.last_name)
                $ the_person.set_possessive_title("Your annoyance")
                the_person "I'm [the_person.title]. I've been sent by the city to have a little chat with you."
                the_person "It's best you open up the doors. I have permission to enter by any means necessary."
                "The presence of the two enforcers makes a little more sense now."
                "You unlock the door and open it for your new \"guests\"."
                the_person "Thank you. Your cooperation will make all of this a lot easier for both of us."

        mc.name "What do we have to talk about?"

    elif times_visited == 1:
        "There's a hard banging on the front door of the office."
        the_person "Hello? [the_person.mc_title], are you here?"
        "You roll your eyes and get up from your desk."
        $ the_person.draw_person()
        "When you step into the lobby you see [the_person.title], flanked by two tough looking men in too-small suits."
        "You unlock the door and open it. [the_person.title] moves into the lobby right away."
        the_person "Hello again [the_person.mc_title]. I hope you weren't in the middle of anything."
        mc.name "Would it matter if I was?"
        the_person "No, it wouldn't. The city has sent me to have another chat with you."
        mc.name "And these two?"
        "The two men look at you, but neither says a word."
        the_person "Well, they've been told to have a little look around while we chat."

    else:
        "There's a loud, insistent knocking on the front door of the office."
        the_person "Hello [the_person.mc_title]. Can you let us in, please?"
        $ the_person.draw_person()
        "You step into the lobby and see [the_person.title], flanked by her usual enforcers."
        if the_person.event_triggers_dict.get("city_rep_forced_uniform", False):
            call city_rep_outfit_comment(the_person)
        "You know the routine. You unlock the door and let them in."

    return

label attention_call_to_work(the_person):
    $ times_visited = mc.business.event_triggers_dict.get("attention_times_visited", 0)
    if times_visited == 0:
        "Your phone buzzes, a call from an unknown number."
        mc.name "Hello?"
        the_person "Hello, am I speaking to [the_person.mc_title]?"
        "The voice on the other end is feminine and authoritative."
        menu:
            "Yes, that's me.":
                mc.name "That's me. Who is this?"

            "Who's asking?":
                mc.name "That depends on who's asking."

        $ the_person.set_title("Ms." + the_person.last_name)
        $ the_person.set_possessive_title("Your annoyance")

        the_person "This is [the_person.title], speaking on behalf of the city."
        the_person "I'm standing outside of your business, would you be able to come and let us in?"
        menu:
            "I'll be right over.":
                mc.name "I'm just a few minutes away. I'll be there soon and we can talk about whatever business you have with me."
                the_person "Good. Thank you for your cooperation."

            "I don't think so.":
                mc.name "I don't think I'm going to do that."
                the_person "[the_person.mc_title], you may want to reconsider. I have official permission to enter the building."
                the_person "I'm trying to save you the trouble of buying a new front door."
                "She doesn't sound like she's lying."
                mc.name "Fine, I'll be over as quickly as I can."
                the_person "Good. Don't take too long, I'm not a patient woman."

    elif times_visited == 1:
        "Your phone buzzes. It's another call from [the_person.title]. You sigh and answer it."
        mc.name "Hello?"
        the_person "Hello [the_person.mc_title]. It looks like the city has taken some interest in your operations again."
        the_person "I'm going to need you to come meet me at your office as soon as you can."
        "You consider arguing, but it's probably best to be on your best behaviour right now."
        mc.name "I'll be over as soon as I can."
        the_person "Good. I'll be waiting."

    else:
        "Your phone buzzes. A call from [the_person.title]."
        mc.name "Hello [the_person.title]."
        the_person "Hello again [the_person.mc_title]. The city wants me to have another talk with you."
        mc.name "It's never just a talk though, is it."
        the_person "No, it's not. It's best you come to the office. Right now."
        "You sigh. Not much you can do to change things now."
        mc.name "Fine. I'm on my way."
        the_person "Good. I'll be waiting."

    $ mc.change_location(lobby)
    $ mc.location.show_background()
    "A few minutes later you arrive at the office."
    $ the_person.draw_person()
    "[the_person.title] is waiting at the front door, typing something on her phone."
    "She is flanked by two burly men in poorly fitting suits."
    if the_person.event_triggers_dict.get("city_rep_forced_uniform", False):
        call city_rep_outfit_comment(the_person)

    the_person "Ah, you're here. May we come in?"
    "It doesn't really sound like a question."
    "You unlock the door and take them into the lobby."

    return

label city_rep_outfit_comment(the_person):
    "You're happy to see your training has taken hold. [the_person.title] is happily wearing the uniform you picked out for her."
    if the_person.outfit.vagina_visible():
        pass #TODO

    elif the_person.outfit.tits_visible():
        pass #TODO:

    elif the_person.outfit.underwear_visible():
        pass #TODO:

    return


label attention_visit(the_person):
    $ times_visited = mc.business.event_triggers_dict.get("attention_times_visited", 0)
    if times_visited == 0:
        "[the_person.title] pulls an official looking piece of paper out of her purse and hands it over."
        the_person "The city is very concerned with your business, and it's products."
        the_person "You see, we've had them show up in some... interesting places."
        mc.name "I'm not doing anything illegal."
        the_person "No, not as far as we can tell. At least not completely."
        the_person "Unfortunately for you, the city has so many bylaws and ordinances on the books that they'll always be able to find something you're doing wrong."
        the_person "What you're doing isn't illegal, but it has caused a stir, and they need to be seen taking action."
        mc.name "So what, you can just charge in here and do whatever you want?"
        "She shrugs and nods."
        the_person "You could hire a lawyer, but it's probably cheaper and easier to just let it happen."
        the_person "If you fight back the city might decide to make an example and throw the book at you."
        mc.name "So what now?"
        the_person "My two associates are going to take a look around. Me and you, we're just going to wait while they finish their work."

    elif times_visited == 1:
        "[the_person.title] hands you an official looking piece of paper."
        the_person "Looks like the city wants me to take another look around [the_person.mc_title]."
        "You look over the citation. It seems genuine."
        mc.name "So you're here to rob me again, huh?"
        "She shrugs, understanding but unapologetic."
        the_person "I sympathise with the feeling, but it's how things go."
        the_person "If you want my advice, you should try to make less of a splash. The less the city hears about you the better."
        the_person "But it's too late for that now. I have my instructions, and you'll only make it worse by arguing."
        "You want to argue, but you know she's right."

    else:
        the_person "I'm here for another look around [the_person.mc_title]. It seems like the city has a real interest in your operation."
        "She hands over an official work order. You glance at it, but it hardly matters what it says."
        mc.name "Clearly."
        the_person "I think you know the routine at this point. Let's just stay over here and let the men have a look around."

    "The two suited enforcers shoulder past you and start wandering around the lab."
    menu:
        "Chat with [the_person.title].":
            call talk_person(the_person, keep_talking = False)
            $ the_person.draw_person()
            "The two suited men show no signs of returning soon."
            if not _return: #IF you want to stop talking we stop right away.
                call talk_person(the_person, keep_talking = False)
                $ the_person.draw_person()
                "Her enforcers still haven't finished poking around your lab, so you have a little more time to chat."
                if not _return:
                    $ the_person.draw_person()
                    call talk_person(the_person, keep_talking = False)

        "Offer her a coffee.":
            call attention_coffee(the_person)
            if not _return:
                $ the_person.draw_person()
                call talk_person(the_person, keep_talking = False)
                "Her enforcers still haven't finished poking around your lab, so you have a little more time to chat."
                if not _return:
                        $ the_person.draw_person()
                        call talk_person(the_person, keep_talking = False)

        "Wait in silence.":
            "You stand in silence while [the_person.title]'s men search the lab."
    return


label attention_coffee(the_person):
    mc.name "Can I get you a coffee while we wait?"
    if the_person.love < 0:
        "[the_person.possessive_title] gives you an icy glare."
        the_person "No. Thank you."

    elif the_person.love < 15:
        the_person "I'm not suppose to accept anything from the subject of an investigation, but..."
        "[the_person.possessive_title] considers it for a moment, then gives you a polite nod."
        the_person "I doubt anyone is going to complain about a cup of coffee. Thank you."
        mc.name "Right, I'll just go get that and..."
        the_person "Oh, I'm sorry but I'm going to have to stay with you. To keep you under observation, you understand."
        mc.name "Of course..."
        "You and [the_person.title] walk together to the office break room. You make a cup of coffee for both of you."
        "You keep an eye out for an opportunity to slip a dose of serum into it, but she's watching you like a hawk."
        $ the_person.change_love(1)
        "She holds the paper cup in both hands and inhales, enjoying the smell."
        the_person "Ah... I think I would go insane without coffee. Some days it's the only breakfast I get."

    else:
        the_person "Some coffee sounds lovely. Thank you [the_person.mc_title]."
        mc.name "I'll be back in a second and..."
        the_person "Oh, I should really come with you. I'm suppose to keep you under observation at all times."
        mc.name "Is that necessary? I'll just be a moment, and I'm just going to the break room. You can see the door from here."
        "She considers it for a moment, then nods her approval."
        the_person "I'll just take a seat over here while I wait."
        mc.name "I'll be back before you know it."
        $ clear_scene()
        "You head to the break room and make a coffee for yourself and [the_person.title]."
        menu:
            "Add a dose of serum to her coffee." if mc.inventory.get_any_serum_count() > 0:
                call give_serum(the_person)
                if _return:
                    "You stir the serum into her coffee. The strong smell and taste should mask any hint of it easily."
                else:
                    "You reconsider at the last moment, and decide not to slip [the_person.title] anything."

            "Add a dose of serum to her coffee.\nRequires: Serum in Inventory (disabled)" if mc.inventory.get_any_serum_count() <= 0:
                pass

            "Leave her coffee alone.":
                pass

        $ the_person.draw_person()
        "You return to the lobby, coffee in hand. [the_person.possessive_title] gives a happy sigh as you hand her a cup."
        the_person "Ah... I think I would go insane without coffee. Some days it's the only breakfast I get."

    return
