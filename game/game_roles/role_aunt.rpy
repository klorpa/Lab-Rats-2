#Aunt Role Action Requirements
init -2 python:
    def aunt_intro_requirement(day_trigger):
        if day >= day_trigger and time_of_day == 4:
            return True
        return False

    def aunt_intro_phase_two_requirement(): #Always triggers the day after the initial intro event
        return True

    def aunt_intro_phase_three_requirement(day_trigger):
        if day >= day_trigger:
            return True
        return False

    def aunt_intro_moving_apartment_requirement(the_person):
        if aunt.event_triggers_dict.get("moving_apartment",-1) >= 0:
            if aunt.event_triggers_dict.get("moving_apartment") >= 4:
                return "Everything has already been moved."

            elif time_of_day == 0:
                return "Too early in the day to start moving."

            elif time_of_day == 4:
                return "Too late in the day to start moving."

            elif aunt.event_triggers_dict.get("day_of_last_move",-1) == day:
                return "Too tired to move anything more today."

            else:
                return True
        return False

    def aunt_intro_phase_five_requirement(day_trigger):
        if day >= day_trigger:
            return True
        return False


    def aunt_drink_intro_requirement(the_person):
        if the_person in aunt_apartment.people:
            return True
        else:
            return False

    def aunt_share_drinks_requirement(the_person):
        if not the_person.event_triggers_dict.get("invited_for_drinks", False):
            return False
        elif the_person not in aunt_apartment.people:
            return False
        elif time_of_day < 3:
            return "Too early for drinks."
        elif time_of_day > 3:
            return "Too late for drinks."
        else:
            return True

    def family_games_night_intro_requirement(the_person):
        if not the_person.event_triggers_dict.get("invited_for_drinks", False):
            return False
        elif the_person not in aunt_apartment.people:
            return False
        elif time_of_day != 3:
            return False
        elif the_person.love < 20 or mom.love < 20:
            return False
        else:
            return True

    def family_games_night_setup_requirement():
        if day%7 != 2: #Triggers Wednesday
            return False
        elif time_of_day != 3: #Only on the end of the 3rd time tick, which makes it active at the end of the day.
            return False
        else:
            return True

    def family_games_night_requirement(the_mom, the_aunt):
        if not the_mom in hall.people or not the_aunt in hall.people:
            return False
        elif time_of_day != 4:
            return False
        elif day%7 != 2:
            return False
        else:
            return True




###AUNT ACTION LABELS###
label aunt_intro_label():
    #NOTE: Doesn't technically countain the aunt, but intoduces the concept of her when she appears the next day
    $ bedroom.show_background()
    mom "Hey [mom.mc_title], do you have a moment?"
    $ mom.draw_person()
    "[mom.possessive_title] cracks your door open and leans in."
    mc.name "Sure [mom.title], what's up?"
    mom "You remember your aunt [aunt.title], right? Well, she's been having a rough time with her husband lately and they're separating."
    "You nod and listen. [aunt.possessive_title] never spent much time visiting when you were a kid and it's been years since you've seen her at all."
    mom "It seems like he's going to be keeping the house, so she's going to be staying with us for a few days while she finds a new place to live."
    mom "She'll be bringing your cousin [cousin.title], too. You two haven't seen each other since you were kids, have you?"
    mc.name "No, it's been a long time."
    mom "I know it's going to be a little tight here while we sort this out, but she's family and I need to be there for her."
    mc.name "I understand [mom.title]. I'll help out however I can."
    $ mom.change_happiness(5)
    mom "That's so nice to hear [mom.mc_title], thank you. [cousin.possessive_title] will be sharing [lily.title]'s room with her and [aunt.title] will be on the couch in the living room."
    mom "They're going to be here in the morning. If you have a few minutes, could you help me pull out some sheets and get their beds made?"
    menu:
        "Help [mom.possessive_title] set up.":
            mc.name "Sure, let's go get it done."
            $ mom.change_happiness(3)
            $ mom.change_love(2)
            "You and [mom.possessive_title] go to the laundry room and gather up extra pillows, sheets, and towels for your house guests."
            "You fold out the couch in the living room and dress it up as a temporary bed for your aunt."
            "Next, you drag an air mattress into [lily.title]'s room and start inflating it."
            $ lily.draw_person()
            lily "Mom, I don't even know [cousin.title]. Can't she have [lily.mc_title]'s room and he can sleep somewhere else?"
            $ mom.draw_person()
            mom "Your brother has to worry about his work. It's just for a couple of days. I'm sure you and [cousin.title] will get along just fine."
            "[lily.possessive_title] pouts but stops complaining. You and [mom.possessive_title] finish setting up the air mattress."
            mom "Alright, I think that's everything. Thank you so much for the help [mom.mc_title]. I know it's late and you probably want to get to bed."
            "[mom.possessive_title] gives you a hug and kiss on the forehead. You head off to your room and go to sleep."



        "Make [lily.possessive_title] do it.":
            mc.name "Sorry [mom.title], I've got an early morning tomorrow and really need to get to bed. I think [lily.title]'s free though."
            $ lily.change_obedience(2)
            $ lily.change_love(-1)
            mom "Of course, [mom.mc_title]. I'm sure your sister won't mind helping. You get a good night's sleep."
            "[mom.possessive_title] gives you one last smile as she closes your door. You hear her talking to your sister outside while you get ready for bed."

    $ clear_scene()
    $ aunt_intro_phase_two = Action("Aunt introduction phase two", aunt_intro_phase_two_requirement, "aunt_intro_phase_two_label")
    $ mc.business.mandatory_morning_crises_list.append(aunt_intro_phase_two) #Aunt and cousin will be visiting tomorrow in the morning
    return

label aunt_intro_phase_two_label():
    #They show up at your house in the morning. Quick introductions with everyone.
    "In the morning [mom.possessive_title] wakes you up early with a knock on your door."
    $ the_group = GroupDisplayManager([mom], mom)
    $ the_group.draw_person(mom)
    mom "[mom.mc_title], I just got a call, your aunt and cousin are on their way over. Get ready so you can help move their stuff inside."
    $ kitchen.show_background()
    "You get up, get dressed, and head to the kitchen to have some breakfast. [mom.possessive_title] paces around the house nervously, looking for things to tidy."
    $ hall.show_background()
    $ the_group.add_person(lily)
    $ the_group.draw_group()
    "Finally the doorbell rings and she rushes to the door. You and [lily.title] join her in the front hall as she greets your guests."
    mom "[aunt.name], I'm so glad you made it!"
    $ the_group.add_person(aunt)
    $ the_group.add_person(cousin)
    $ the_group.set_primary(aunt)
    aunt "[mom.name]!"
    $ the_group.draw_group()
    "[aunt.title] lets out an excited, high pitched yell and rushes forward to hug [mom.possessive_title]."
    aunt "Thank you so much for taking us in. It means the world to me and [cousin.title]."
    $ the_group.draw_person(mom)
    "[mom.possessive_title] breaks the hug. Your cousin, [cousin.title], sits outside the door on a suitcase, idly scrolling through her phone."
    mom "How are you doing [cousin.title]? Holding up okay?"
    $ the_group.draw_person(cousin)
    "She shrugs and doesn't take her eyes off her phone."
    cousin "Eh. Fine..."
    $ the_group.draw_person(aunt)
    aunt "She's thrilled, really. Now who are these two little rascals I see?"
    "[aunt.possessive_title] steps into the house and throws her arms wide, pulling you and your sister in to a hug."
    aunt "I mean, it must be [mc.name] and [lily.title], but you're both so much bigger than I remember!"
    "She hugs you both tight and then lets go. [aunt.title] looks at you in particular and laughs."
    aunt "I remember when you were just a little baby, and now you're a full grown man. Oh no, I'm showing my age, aren't I. Hahaha."
    "She laughs and turns back to grab her things. [cousin.title] sighs loudly outside and rolls her eyes."
    aunt "Now [mom.name], where should I bring my things?"
    $ the_group.draw_person(mom)
    mom "Just follow me, I'll show you around. We got everything set up as soon as we heard the news."
    $ the_group.remove_person(mom)
    $ the_group.remove_person(aunt)
    $ the_group.set_primary(lily)
    $ the_group.redraw_group()
    "[mom.possessive_title] leads [aunt.possessive_title] into the house. When they're gone [lily.possessive_title] takes a step towards [cousin.title]."
    lily "Hi [cousin.title], it's nice to see you again. I don't think we've talked since we were little kids."
    $ the_group.draw_person(cousin)
    cousin "Yep..."
    "There's a long period of awkward silence."
    $ the_group.draw_person(lily)
    lily "... Right. Well I'm sure we'll get along while you're staying with me."
    "[aunt.possessive_title] calls from further inside the house."

    aunt "[cousin.name], sweetheart, you should come see your room! I'm sure [lily.name] and [mc.name] will help bring your stuff in."
    $ the_group.draw_person(cousin)
    "[cousin.possessive_title] gets up from her suitcase seat, picks up her smallest bag, and walks inside."
    cousin "Thanks for the help."
    $ the_group.remove_person(cousin)
    $ the_group.set_primary(lily)
    $ the_group.redraw_group()
    "[lily.title] glances at you and rolls her eyes dramatically. The two of you grab more luggage and start hauling it inside."
    "After a few minutes all of the suitcases have been moved to where they need to go."
    $ the_group.add_person(aunt, make_primary = True)
    $ the_group.redraw_group()
    aunt "Thank you two so much, you're such sweethearts. Here's something for all your hard work."
    $ aunt.change_love(2)
    $ mc.business.funds += 20
    "[aunt.possessive_title] finds her purse, pulls out her wallet, and hands you and [lily.possessive_title] $20."
    aunt "Now I think your mother wanted to talk with me. I'm sure you both have busy days, so don't let me keep you!"
    #Their temporary homes are at your place. Later we will restore them to their normal homes.
    python:
        aunt.home.move_person(aunt, hall)
        aunt.home = hall
        cousin.home.move_person(cousin,lily_bedroom)
        cousin.home = lily_bedroom

        aunt.set_schedule(aunt.home, times = [0,1,2,3,4]) #Hide them in their bedroom off the map until they're ready.
        cousin.set_schedule(cousin.home, times = [0,1,2,3,4])

        #Your aunt is a homebody, but your cousin goes wandering during the day (Eventually to be repalced with going to class sometimes.)
        cousin.set_schedule(None, times = [1,2,3])

    $ aunt_intro_phase_three = Action("aunt_intro_phase_three", aunt_intro_phase_three_requirement, "aunt_intro_phase_three_label", requirement_args = day + renpy.random.randint(6,10))
    $ mc.business.mandatory_morning_crises_list.append(aunt_intro_phase_three)

    $ cousin_intro_phase_one = Action("cousin_intro_phase_one", cousin_intro_phase_one_requirement, "cousin_intro_phase_one_label", requirement_args = day + renpy.random.randint(2,5))
    $ mc.business.mandatory_crises_list.append(cousin_intro_phase_one)
    $ clear_scene()
    return

label aunt_intro_phase_three_label():
    #Your aunt lets you know that she has an apartment lined up, and if you have free time would appreciate some help moving in.
    "There's a quick knock at your door."
    aunt "[aunt.mc_title], I hope you're decent because I'm coming in!"
    $ aunt.draw_person(emotion = "happy")
    "[aunt.possessive_title] throws your bedroom door open and steps in before you have a chance to answer."
    mc.name "Morning [aunt.title], uh... What's up?"
    aunt "Earlier today I got a call with some fantastic news. My realtor found this beautiful little apartment downtown for me and [cousin.title]!"
    aunt "That means in a few days we'll be out of your hair and your house can go back to normal."
    mc.name "It was nice having you around [aunt.title], but I'm happy you're getting back on your feet. Things will be back to normal for you soon, too."
    aunt "I hope so. I actually had one {i}tiny{/i} little favour to ask while I was here..."
    mc.name "What is it?"
    aunt "Well now that it's just me and [cousin.title], we don't have anyone to help us with the heavy lifting when we move in."
    aunt "We'll be moving our things starting tomorrow. If you have any free time to help us, it would mean the world to me."
    mc.name "I'll see if I have some spare time in my schedule and come to you if I do."
    $ aunt.draw_person(position = "sitting", emotion = "happy")
    $ aunt.change_happiness(8)
    "[aunt.possessive_title] sits on the side of your bed, puts a hand on your leg, and squeezes it gently."
    aunt "I'm so lucky to have such a wonderful nephew, you know that? If only I had married a man like you instead of..."
    aunt "Well, never mind that. Thank you."
    "She leans in, gives you a warm, familial hug, and then leaves you to get on with your day."
    $ clear_scene()
    $ aunt.event_triggers_dict["moving_apartment"] = 0 #If it's a number it's the number of times you've helped her move. If it doesn't exist or is negative the event isn't enabled

    $ moving_finished_action = Action("Moving finished", aunt_intro_phase_five_requirement, "aunt_intro_phase_final_label", requirement_args = day + 7)
    $ mc.business.mandatory_morning_crises_list.append(moving_finished_action)

    return

label aunt_intro_moving_apartment_label(the_person):
    #You help her move in, with different focuses each time you do it.
    $ aunt.draw_person()
    mc.name "[aunt.title], I've got a few free hours. Would you like some help moving your things?"
    aunt "Oh [aunt.mc_title], your help would be amazing. Here, let's go look at what we have to move."
    if aunt.event_triggers_dict.get("moving_apartment") == 0:
        #You help them and get a brief overview of what they're bringing in the future
        "You follow [aunt.possessive_title] to the stack of boxes, luggage, and furniture that are being stored in the garage."
        aunt "With your help I think we can manage this in four trips. Today we'll rent a truck and move all of the big stuff in."
        aunt "Once that's done we can move all of my things into my room, then we move [cousin.title]'s stuff."
        aunt "Last, we move in the kitchen things and get the place all tidied up. Sound good?"
        mc.name "Yeah, let's get started I guess."
        $ aunt.change_happiness(5)
        $ aunt.change_love(2)
        aunt "Thank you so much! I'll go rent that truck, you just stay here and I'll be back in a little bit."
        $ clear_scene()
        "[aunt.title] gets in her car and drives off. You organize the boxes so they'll be easier to load when she gets back."
        cousin "What're you doing out here?"
        "You're startled by [cousin.possessive_title]'s voice. You spin around and find her leaning against the house door frame."
        $ cousin.draw_person()
        mc.name "Your mom's going to rent a truck. I'm helping you guys move your stuff over to your new place."
        cousin "Why?"
        menu:
            "Because it's a nice thing to do.":
                mc.name "Because it's a nice thing to do, that's all."

            "Because I want to impress her.":
                mc.name "Because I want to make a good impression. I want her to like me."

            "Because I'm hoping she'll pay me.":
                mc.name "Because I'm hoping when we're done she'll pay me for the help."

        cousin "That's dumb, but whatever."
        mc.name "Yeah, whatever. [aunt.title] will be back soon. Do you want to give me a hand?"
        cousin "Not really. Be careful with my stuff."
        $ cousin.draw_person(position = "walking_away")
        "With that she turns around and goes back inside."
        $ clear_scene()
        mc.name "You're welcome..."
        "A few minutes later [aunt.title] pulls up in a rented pickup truck. You load up the back with furniture and boxes, then get in the passenger seat."
        $ aunt.draw_person(position = "sitting")
        aunt "Okay, let's get going! I don't know what I'd do without a big strong man like you to lift things for me. I'd be helpless!"
        $ aunt.change_love(1)
        $ downtown.show_background()
        "It doesn't take long to drive to [aunt.title]'s new apartment. She parks out front and you grab a box to bring up with you."
        $ aunt.draw_person()
        $ aunt_apartment.show_background()
        "The apartment is small but tidy, with two bedrooms and a combined living area and kitchen. [aunt.title] gestures to one of the bedrooms."
        aunt "My room will be in there, and the other one will be [cousin.title]'s room. You can put that box down and go get another, I'll start unpacking."
        "The next couple of hours are spent unloading the truck and bringing everything up to [aunt.possessive_title]."
        "When you're done [aunt.title] returns the truck and drives you both home. When you get out of the car she gives you a tight hug."
        $ aunt.change_love(3)
        $ aunt.change_happiness(5)
        $ aunt.draw_person(emotion = "happy")
        aunt "You're my hero [aunt.mc_title]. Come see me if you have any more spare time and we can move the rest of this over."
        "She breaks the hug and smiles."
        aunt "Now I'm going to go see if I can use your mothers shower!"
        $ clear_scene()



    elif aunt.event_triggers_dict.get("moving_apartment") == 1:
        #You help move your aunt's wardrobe and get a chance to dig through her underwear
        "You and [aunt.title] head to the garage and look over the stuff that still needs to be moved."
        aunt "I think we can move my things over today. If I need something I can always borrow it from your mother."
        aunt "She always hated when I borrowed her clothes when we were younger. She said I stretched out her tops."
        aunt "I think she was just jealous I got the nice tits."
        "[aunt.possessive_title] laughs and blushes."
        $ aunt.change_slut_temp(1)
        aunt "Sorry, I shouldn't be talking about your mom's chest like that. It's different when you're sisters, you know?"
        mc.name "Oh yeah, I know what you mean."
        aunt "Anyway, we have work to get done. I think we can fit all of my clothes in the back of my car, so we don't need a truck today."
        aunt "Let's load it up and we can bring it all over."
        "You and [aunt.title] load up her hatchback with boxes filled with clothes. Once the car is loaded to capacity, you get in and drive to her new apartment."
        $ aunt_apartment.show_background()
        "When you arrive, you start to shuttle boxes up to [aunt.possessive_title]'s bedroom. [aunt.title] is kept busy unpacking the boxes and putting everything away."
        $ aunt.draw_person(position = "sitting")
        "After some hard work the car is empty and the last box is in [aunt.title]'s room."
        aunt "Thank you for all the help [aunt.mc_title]. It'll just take me a few minutes to get the rest of this put away."
        $ aunt.change_happiness(5)
        $ aunt.change_love(1)
        menu:
            "Offer to help.":
                mc.name "Here, let me help with that. Just tell me where to put things."
                $ aunt.change_love(1)
                aunt "My sister raised such a perfect gentleman! Here, this goes in the top drawer over there."
                "You clear out a couple of boxes, putting away shirts, skirts, and pants for [aunt.title]. [aunt.possessive_title] reaches for the last box, marked \"Private,\" then hesitates."
                aunt "I can go through this one myself. It's all my underwear and that's probably the last thing you want to be digging through."
                mc.name "We're both adults, it's no big deal."
                "[aunt.possessive_title] shrugs, opens the box, and starts to sort through it. She hands you a pile of colourful panties."
                aunt "Okay, put these in that drawer on the left..."
                "You slide the garments into their drawer. Next [aunt.title] hands you a stack of lacey bras and small thongs."
                aunt "This goes to the side... and then... Oh my."
                "She closes the box and looks away, blushing."
                aunt "This is so embarrassing [aunt.mc_title]. I'll just finish this up myself later."
                mc.name "Come on, we're almost done."
                $ aunt.change_slut_temp(1)
                aunt "Don't tell my sister about this."
                "[aunt.title] pulls out the last few pieces of underwear from the box: a collection of g-strings and nippleless bras."
                mc.name "Is that all? I thought you had something to be embarrassed about."
                "You pick the tiniest g-string and hold it up against your waist. [aunt.title] laughs and snatches it from your hands."
                aunt "Stop that! I bought those for my husband, not that he ever cared what I wore. He was more interested what his secretary {i}wasn't{/i} wearing."
                "She throws the underwear back at you."
                $ aunt.change_slut_temp(1)
                aunt "You know what, keep all this stuff near the front. Maybe I'll get a chance to wear it for someone who'll appreciate it."
                "You put away [aunt.title]'s sexy underwear and finish your work for the day."

            "Take a break.":
                mc.name "Alright, I'm going to go get a glass of water and catch my breath."
                aunt "Go ahead, you've certainly earned it!"
                $ aunt.change_obedience(1)
                $ clear_scene()
                "You get a glass of water and sit down on the new sofa in the living room."
                "After half an hour [aunt.possessive_title] comes out and dusts off her hands."


        aunt "Alright, that's everything for today [aunt.mc_title]. Let's get you home."
        $ clear_scene()

    elif aunt.event_triggers_dict.get("moving_apartment") == 2:
        #You help move your cousin's wardrobe and get a chance to dig through her underwear. She catches you and taunts you "You little perv, you'll never get to see me wear something like that." kind of stuff.
        "You head to the garage and look at the dwindling pile of boxes that need to be moved."
        aunt "I think we can move [cousin.title]'s things today. I'll go get her."
        $ clear_scene()
        $ the_group = GroupDisplayManager([aunt, cousin], primary_speaker = aunt)
        $ the_group.draw_group()
        "[aunt.possessive_title] is gone for a few minutes before coming back with [cousin.title] in tow."
        aunt "Let's get this show on the road! I know [cousin.title] is excited to have a room to herself again, aren't you sweetheart."
        $ the_group.draw_person(cousin)
        cousin "I'm not your sweetheart Mom. Let's just get this over with."
        $ the_group.draw_person(cousin, position = "sitting")
        "She sulks over to [aunt.title]'s car and gets in the passenger seat."
        $ the_group.draw_person(aunt)
        aunt "Sorry about that [aunt.mc_title]. She doesn't always play nice with others and this whole move has been tough on her. Could you help me load up the car?"
        mc.name "Sure. Just tell me where to put things."
        $ the_group.draw_person(aunt, position = "sitting")
        "You fill up [aunt.title]'s hatchback and get in the back seat with the last box sitting on your lap. [cousin.title] puts on headphones and ignores both of you."
        $ cousin_bedroom.show_background()
        $ the_group.draw_group()
        "When you arrive, you start to shuttle everything up to [cousin.possessive_title]'s room."
        $ cousin.draw_person(position = "sitting")
        "[cousin.title] sits down on her bed and gets her phone out. She looks up occasionally to tell you where to put boxes down."
        mc.name "You could help, you know."
        cousin "I could, but I don't want to. You're doing fine."
        $ the_group.draw_person(aunt)
        "[aunt.possessive_title] pokes her head into the room."
        aunt "[cousin.title], sweety, we should go downstairs and get an extra key for you."
        $ the_group.draw_person(cousin, position = "back_peek")
        "[cousin.title] rolls her eyes dramatically, then gets up and follows her mother. She stops just before leaving and looks back at you."
        cousin "Don't touch my stuff."
        $ clear_scene()
        menu:
            "Touch her stuff.":
                "She's not the boss of you. You wait a couple of minutes then start snooping around."
                "Most of the boxes are clearly labeled, but you find one that just says \"Keep Out!\" on the side."
                "You open the box and find it filled with all of [cousin.title]'s underwear, all black, purple, or blue."
                "You dig deeper, past the large cupped bras she needs for her big tits. She has a handful of g-strings, fishnet stockings, and a garter belt near the bottom."
                "You think you feel something rigid at the bottom, but your search is interrupted by the front door lock clicking open."
                "You rush to get [cousin.possessive_title]'s underwear back in order. You slam the box shut and sit down on her bed, trying to look nonchalant."
                $ cousin.draw_person()
                cousin "You didn't paw through my things, did you?"
                mc.name "Of course not, you told me not to."
                "She glares at you, then at her box of underwear, then at you again. She shakes her head."
                $ cousin.change_obedience(-3)
                cousin "Pervert."
                mc.name "Fine, I was curious. I didn't know what was in there."
                $ cousin.change_slut_temp(2)
                cousin "Whatever. It's not like you'll ever get to see me in it. I bet you'd like to though. I bet you're weird like that."
                "[cousin.title] gives you a strange, mischievous smile."
                cousin "Do you want to see me try some of it on? I won't tell anyone."
                menu:
                    "Yes.":
                        "You nod your head. [cousin.title] laughs."
                        $ cousin.change_happiness(10)
                        $ cousin.change_slut_temp(1)
                        cousin "Ha! You wish you pervert. Now get out of here before I tell my mom."

                    "No.":
                        mc.name "What? No, you're being weird now."
                        "She shrugs."
                        cousin "Your loss. You'll just have to imagine it now. Now get out of here before I tell my mom you're digging through my things."

                "You get up off of [cousin.title]'s bed and leave."


            "Don't touch her stuff.":
                "Not wanting to bring down [cousin.title]'s wrath, you focus on bringing up the rest of the boxes from the car."
                "Twenty minutes later, [aunt.title] and [cousin.title] come back just after you're done moving the last box."
                $ cousin.draw_person()
                cousin "You didn't paw through my things, did you?"
                mc.name "Of course not, you told me not to."
                $ cousin.change_obedience(-3)
                $ cousin.change_happiness(2)
                cousin "Good."

        "With your work done for the day, the three of you drive back home. [aunt.title] gives you a big hug when you get out of the car."
        $ aunt.change_love(1)
        aunt "Thank you again for all the help."



    elif aunt.event_triggers_dict.get("moving_apartment") == 3:
        #You help them move their kitcehn stuff in. Your aunt gets dirty/sweaty and wants to chance now that her clothes are here. She asks you to wait around whlie hse takes a shower, then
        #the landlord shows up and needs some documents from her, so you have to come into her bathroom and get a chance to see her naked/just in her underwear or something.
        #mc.name "Okay, I'm going to get a drink and catch my breath."
        #$ clear_scene()
        #"She smiles at you and nods. You sit down on her new couch in the living room and relax for a bit."
        #"A minute later [aunt.title]'s phone rings. You catch half of the conversation from the living room."
        #aunt "Hello? Yes, that's me. I'm actually in the building right now, I can come to the office right away. Okay. See you soon."
        #"[aunt.possessive_title] comes out and heads for the door."
        #6aunt "I just need to dip down to the

        "You head to the garage and look at the small pile of boxes left."
        aunt "I think it's just the kitchen stuff left. Let's get this packed in the car and we'll have everything moved over!"
        "You fill up [aunt.possessive_title]'s hatchback and head for her apartment."
        $ aunt_apartment.show_background()
        "You and [aunt.possessive_title] get to work shifting boxes upstairs."
        "After the first couple of boxes are upstairs, she starts to unpack them while you keep unloading the car."
        "It takes a couple of hours to get everything moved and unpacked. You and [aunt.title] are happy when the last box is emptied and you're finished with the move."
        $ aunt.change_happiness(5)
        aunt "[aunt.mc_title], I think that's everything! I think we should order a pizza and celebrate a little, what do you say?"
        mc.name "That sounds good to me. I'm starving."
        $ aunt.change_love(1)
        aunt "I'm sure you are, you've been doing all the heavy lifting for me! You're my big strong man, coming in to rescue me."
        "She gives you a hug, then grabs her phone and finds a local pizza place that delivers. She places your order."
        aunt "They said it may take a little while. All this hard work got me all sweaty. I'm going to go take a shower. Back in a bit!"
        $ clear_scene()
        "[aunt.possessive_title] heads off to the bathroom and you hear the shower start."
        "You're killing time on your phone when there's a knock on the door. It's the pizza guy."
        "Pizza Guy" "Hey, this is for you. One large."
        "He hands it over, then waits for you to pay."
        menu:
            "Pay for the pizza.\n-$25" if mc.business.funds >= 25:
                mc.name "Thanks, here you go."
                $ mc.business.funds += -25
                "Pizza Guy" "Thanks man, enjoy."
                "You take the pizza into the kitchen. A couple of minutes later [aunt.title] comes out of the bathroom."
                aunt "Oh, is that here already? I'm sorry [aunt.mc_title], I was going to pay for that."
                mc.name "Don't worry about it, it's no big deal."
                $ aunt.change_love(1)
                aunt "Well thank you. Give me a slice of that, I'm starving now too!"

            "Pay for the pizza.\n-$25 (disabled)" if mc.business.funds < 25:
                pass

            "Get the money from [aunt.title].":
                mc.name "Thanks, I just have to get the money. One sec."
                "The pizza guy nods and hangs out in the doorway while you head to the bathroom door and knock."
                aunt "Hmm? What is it?"
                mc.name "The pizza guy's here."
                aunt "Oh! I didn't think he would be here so soon! Just, uh... just come in and get it, it's in my purse."
                "You open the door to the bathroom. [aunt.possessive_title]'s shower has a clear glass door that doesn't hide anything. She turns away as you come in."
                $ aunt.apply_outfit(Outfit("Nude"))
                #$ aunt.outfit = default_wardrobe.get_outfit_with_name("Nude 1") changed v0.24.1
                $ aunt.draw_person(position = "back_peek")
                $ aunt.change_slut_temp(2)
                aunt "It's right over there. Just grab it and go."
                "She nods her head towards her purse. You hurry inside, grab it, then retreat. You pull the cash out of her wallet and give it to the pizza guy."
                $ clear_scene()
                "Pizza Guy" "Thanks man, enjoy."
                $ aunt.apply_outfit()
                $ aunt.draw_person()
                "You take the pizza into the kitchen. A couple of minutes later [aunt.title] comes out of the bathroom."
                aunt "I'm so sorry about that. I know it must be embarrassing to see your aunt naked."
                mc.name "It's fine. We're family, right? We're supposed to be comfortable with each other."
                aunt "I guess you're right. Anyway, let me have some of that pizza. I'm starving now too!"

        "You enjoy your lunch together then get in [aunt.title]'s car and head home. With all of their stuff moved, [aunt.title] and [cousin.title] should be ready to move out."

    $ aunt.event_triggers_dict["moving_apartment"] += 1
    $ aunt.event_triggers_dict["day_of_last_move"] = day
    call advance_time() from _call_advance_time_16
    return


label aunt_intro_phase_final_label():
    #You have finished moving all of their stuff over so your aunt and cousin can move out of your house.

    "When you get up for breakfast you find [aunt.title] and [mom.title] in the kitchen, both awake earlier than normal."
    $ the_group = GroupDisplayManager([mom, aunt], aunt)
    $ the_group.draw_group(position = "sitting")
    aunt "Good morning [aunt.mc_title]."
    "She smiles at you warmly and sips coffee from a mug. [mom.possessive_title] is drinking a cup of tea across the table from her."
    mc.name "Morning. You two are up early."
    aunt "All the paperwork for my new apartment has been finished, so [cousin.title] and I will be moving out today."
    $ the_group.draw_person(mom, position = "sitting")
    mom "We're just finishing our drinks, then they'll be heading out."
    $ the_group.draw_person(aunt, position = "sitting")
    if aunt.event_triggers_dict.get("moving_apartment", 0) == 0:
        #Did nothing
        aunt "I was going to wake you up before I left, of course. You've been so busy, I barely got a chance to see you."
        $ the_group.draw_person(mom, position = "sitting")
        mom "You're welcome to come over and visit any time [aunt.title]. I'll make sure [mom.mc_title] takes a break to come visit his family."

    elif aunt.event_triggers_dict.get("moving_apartment") in [1,2,3]:
        #Did some stuff
        aunt "I was going to wake you up before I left, of course. I want to say thank you again for helping us move our things over."
        $ the_group.draw_person(mom, position = "sitting", emotion = "happy")
        $ mom.change_love(2)
        $ mom.change_happiness(5)
        mom "I'm glad you were able to find some time to help them out [mom.mc_title]. I'm proud of you."

    else:
        #Did everything
        aunt "I was going to wake you up before I left, of course. I needed to say thank you again for the huge amount of help you gave us."
        $ the_group.draw_person(mom, position = "sitting", emotion = "happy")
        $ mom.change_love(3)
        $ mom.change_happiness(8)
        mom "[aunt.title] has been telling me all morning how helpful you've been. I'm so proud of you [mom.mc_title].:"
        $ the_group.draw_person(aunt, position = "sitting", emotion = "happy")
        aunt "He was a godsend, he really was."

    $ the_group.draw_person(aunt, position = "sitting", emotion = "happy")
    aunt "Come on [aunt.mc_title], sit down and join us for a few minutes."
    "You join [aunt.possessive_title] and [mom.possessive_title] while they finish their drinks and chat with each other."
    "[aunt.title] certainly seems happier now than she did a week ago when she arrived."
    $ clear_scene()
    $ the_group = GroupDisplayManager([mom, lily, aunt, cousin], aunt)
    $ the_group.draw_group()
    "When her drink is done [aunt.title] collects [cousin.possessive_title] and heads to the door. [lily.title] joins you as you say goodbye."
    $ the_group.draw_person(aunt, emotion = "happy")
    aunt "Thank you all for giving us a place to go. You're welcome to visit us any time. Just drop by."
    "[cousin.title] looks at you and shakes her head from behind her mother."
    $ the_group.draw_person(mom, emotion = "happy")
    mom "And you two are always welcome here. Call if you need anything."
    $ the_group.draw_person(aunt)
    aunt "I will. Thanks sis."
    "[mom.possessive_title] and [aunt.possessive_title] hug each other and don't let go for a long while."
    $ clear_scene()
    $ lily.draw_person()
    "When the moment has passed [mom.title] walks them out to the driveway, leaving you alone with [lily.possessive_title]."
    lily "I'm going to miss them. I think [cousin.title] and I were really getting along."
    mc.name "Really?"
    lily "Yeah! She may not talk much but she's a great listener. I hope she stays in touch."
    "You shrug and head back to your room to get ready for the day."

    python:
        aunt.event_triggers_dict["moving_apartment"] = -1 #Disables the event in their action list so you can't help them move out once they're already moved out.
        aunt.home = aunt_bedroom # Set their homes to the new locations
        cousin.home = cousin_bedroom

        aunt_bedroom.visible = True
        aunt_apartment.visible = True
        cousin_bedroom.visible = True

        aunt.set_schedule(aunt.home, times = [0,1,2,3,4]) #Hide them in their bedroom off the map until they're ready.
        cousin.set_schedule(cousin.home, times = [0,1,2,3,4])

        #Your aunt is a homebody, but your cousin goes wandering during the day (Eventually to be repalced with going to class sometimes.)
        aunt.set_schedule(aunt_apartment, times = [2,3])

        cousin.set_schedule(None, times = [1,2,3])

        cousin_at_house_phase_one_action = Action("Cousin changes schedule", cousin_house_phase_one_requirement, "cousin_house_phase_one_label", args = cousin, requirement_args = day+renpy.random.randint(2,5))
        mc.business.mandatory_crises_list.append(cousin_at_house_phase_one_action) #This event changes the cousin's schedule so she shows up at your house.

        cousin_at_house_phase_two_action = Action("Cousin at house", cousin_house_phase_two_requirement, "cousin_house_phase_two_label")
        cousin.on_room_enter_event_list.append(cousin_at_house_phase_two_action)

        aunt_share_drink_intro = Action("Aunt drink intro", aunt_drink_intro_requirement, "aunt_share_drink_intro_label")
        aunt.on_talk_event_list.append(aunt_share_drink_intro)
    return


label aunt_share_drink_intro_label(the_person):
    # On talk trigger after she has moved out and you visit her
    # She invites you over to share some drinks. You can come by in the afternoon and share a drink with her.
    the_person "[the_person.mc_title], I'm so happy to see you! Come here, give me a hug."
    "[the_person.possessive_title] gives you a tight hug."
    mc.name "It's good to see you too [the_person.title]."
    the_person "We really should get together more often. I miss seeing my cute little nephew!"
    the_person "Come by in the afternoon some time, you can join me for a glass of wine and we can chat."
    "She gives you a kiss on the cheek and smiles at you."
    $ the_person.change_happiness(1)
    the_person "Anyway, I'm sure you have other stuff you wanted to talk about!"
    $ the_person.event_triggers_dict["invited_for_drinks"] = True
    call talk_person(the_person) from _call_talk_person_6
    return

label aunt_share_drinks_label(the_person):
    # An action that is only enabled in the evening (maybe only friday nights? Only ad)
    # Aunt shares drinks with you and chats. At higher sluttiness she does things like model for you, talk about her sexual preferences, etc.
    mc.name "Do you feel like having a glass of wine and chatting? I'm sure we have a lot to catch up on."
    "[the_person.title] claps her hands together excitedly!"
    the_person "Yes! You go sit on the couch and I'll pour us both a glass."
    "You sit down in [the_person.possessive_title]'s tiny living room and wait. She shuffles around in the kitchen, then comes out with two glasses of red wine."
    the_person "There you go. Now you have to make sure that I just have one glass of this. I love it, but wine goes straight to my head."
    $ the_person.draw_person(position = "sitting")
    "She hands you a glass, sits down, and tilts her glass toward you. You clink them together."
    mc.name "Cheers!"
    the_person "Cheers!"
    "[the_person.possessive_title] takes a sip, then leans back on the couch. She crosses her legs and turns to you."
    the_person "So what's been going on with your life? It's been so long!"
    menu:
        "Talk about work.":
            mc.name "Well, work's been keeping me busy lately..."
            "You talk to [the_person.possessive_title] about your work. She nods politely but doesn't understand most of it."
            $ the_person.change_obedience(1)
            the_person "It sounds like you're a very important person, doing some very important work. I'm proud of you [the_person.mc_title]"

        "Talk about girls.":
            mc.name "Well, I've been trying to meet someone lately..."
            "You talk to [the_person.possessive_title] about your love life. She listens intently."
            $ the_person.change_slut_temp(1)
            the_person "I've always thought it's important to be adventurous. You might connect with someone you wouldn't expect."

        "Talk about her.":
            mc.name "Oh, it's been pretty quiet lately. What about you? I know you've been through a lot."
            "You get [the_person.possessive_title] talking about herself. She tells you about her failed marriage."
            $ the_person.change_love(1)
            the_person "... and when I told him I knew he was plowing his secretary everyday, he kicked us out."
            "She takes another sip from her wine."
            the_person "Whew. That felt good to talk about actually."

    "[the_person.title] finishes off the last of her wine."
    the_person "Well that was a lovely chat [the_person.mc_title]. I won't keep you here any longer."
    menu:
        "Convince her to have another glass.":
            mc.name "It's really no trouble. I can go pour you another glass, if you'd like."
            if the_person.love >= 20: #Can be convinced
                the_person "Oh, I really shouldn't. It's getting a little late, you probably have important places to be..."
                mc.name "It's not late, and I don't have anywhere important to be. Come on, just relax and give me your glass."
                the_person "Okay, okay, you've twisted my arm. I'm not to blame for any of my actions beyond this point though!"
                "She hands you her glass and you head to the kitchen to uncork her bottle of wine."
                menu:
                    "Add a dose of serum to her wine.":
                        call give_serum(the_person) from _call_give_serum_13

                    "Leave her drink alone.":
                        pass
                "You top up your own drink while you're in the kitchen and head back to [the_person.title]. You hand over her new drink and sit down."
                the_person "Now, where were we..."
                "You and [the_person.possessive_title] keep talking. After her first glass she seems more relaxed, and the second one is already having its effect."
                $ the_person.add_situational_slut("Drunk", 20, "More than a little tipsy.")
                $ decision_score = the_person.sluttiness + renpy.random.randint(0,25) #Her choice in this check is up to 25 points more slutty than she is.
                if decision_score <= 35:
                    # She talks about her ex and then falls asleep.
                    "As [the_person.title] gets deeper into her drink she starts to rant about her now ex-husband."
                    the_person "I don't even know what he saw in that little skank... You've never seen her, but she was this flat chested little thing."
                    "She scoffs and takes another drink while you listen patiently."
                    $ the_person.change_slut_temp(2)
                    the_person "And youth isn't everything it's cracked up to be. It takes practice to get good at some things. I hope he enjoys shitty blowjobs. HA!"
                    "[the_person.possessive_title] puts her feet up on the couch and yawns."
                    the_person "Oh, this wine really has just knocked me out. I'm just going to... rest my eyes while we talk, okay?"
                    "She closes her eyes and leans her head back on the arm rest. She manages a few minutes of mumbled conversation before falling asleep completely."
                    menu:
                        "Get her a blanket.":
                            "You go to [the_person.title]'s room and take the blanket off her bed."
                            "You lay the blanket over [the_person.possessive_title]. She grabs onto it and rolls over, mumbling something you can't understand."
                            $ the_person.change_love(2)
                            "You take your wine glasses to the kitchen and leave them in the sink, then see yourself out."

                        "Grope her tits.":
                            "Seizing the opportunity, you kneel down in front of [the_person.possessive_title]."
                            if the_person.outfit.tits_available():
                                "Her nicely shaped breasts are already there for the taking. You move slowly and cup them in your hands."
                            else:
                                $ the_clothing = the_person.outfit.get_upper_top_layer()
                                "You move slowly and cup her nicely shaped breasts, feeling them through her [the_clothing.name]."
                            the_person "Mmm..."
                            "[the_person.possessive_title] moans softly and tilts her head to the side."
                            $ the_person.change_slut_temp(2)
                            "You fondle her big tits until she seems like she's starting to wake up. You sit back down on the couch and pretend like nothing happened."
                            the_person "... Hmm? Oh, did I nod off there? I'm sorry [the_person.mc_title], I think I need to have a little nap."
                            mc.name "No problem, I'll clean up our glasses and head out."
                            "She rolls over on the couch and is asleep again before you're out the door."

                        "Grope her pussy.":
                            "Seizing the opportunity, you kneel down in front of [the_person.possessive_title]."
                            if the_person.outfit.vagina_available():
                                "Her pussy is out on display for you, there for the taking. You move slowly and slide your hand along her inner thigh, working upward."
                            else:
                                $ the_clothing = the_person.outfit.get_lower_top_layer()
                                "You move slowly, sliding your hand along her inner thigh and working upward."
                                "When you reach her waist, you slide your hand inside of her [the_clothing.name]."

                            if mc.sex_skills["Foreplay"] >= 3:
                                the_person "Mmm..."
                                "She moans softly when your fingers make first contact with her pussy. Her hips press up gently against your hand."
                                $ the_person.change_slut_temp(3)
                                "You run your index finger gently over her clit, gently caressing it while you listen to her moan."
                                "When it starts to seem like she's waking up, you retreat to your seat on the couch."

                            else:
                                "She moans softly when you make first contact with her pussy. You start to move your hand around, feeling for her clit."
                                $ the_person.change_slut_temp(1)
                                "You're inexperienced and perhaps a little overeager. [the_person.title] starts to wake up and you make a hasty retreat to your spot on the couch."

                            the_person "... Hmm? Oh, did I nod off there? I'm sorry [the_person.mc_title], I think I need to have a little nap."
                            mc.name "No problem, I'll clean up our glasses and head out."
                            "She rolls over on the couch and is asleep again before you're out the door."

                elif decision_score <= 45:
                    # She talks to you about stuff she finds sexy. Reveal a sex opinion
                    "[the_person.title] talks more about herself, and it seems like being a little drunk seems to have removed any inhibitions she might have had."
                    $ her_opinion = the_person.get_random_opinion(include_known = False, include_sexy = True, include_normal = False)
                    if her_opinion:
                        $ the_person.discover_opinion(her_opinion)
                        $ opinion_string = opinion_score_to_string(the_person.get_opinion_score(her_opinion))
                        "Through her surprisingly erotic ramblings you discover that she [opinion_string] [her_opinion]."
                    else:
                        #We know everything.
                        "You don't learn anything new, but hearing [the_person.possessive_title] talk this way is certainly eye opening."

                    "She finally blushes and looks away from you."
                    $ the_person.change_slut_temp(2)
                    the_person "Oh my god, what have I even been saying? It's this wine [the_person.mc_title], I told you it makes me do crazy things."
                    the_person "Just... don't tell my sister that I told you any of that. You can keep a secret, right?"
                    mc.name "Of course, it's just between us."
                    the_person "That's a good boy. Now I think I should stop drinking this wine while I still can. It was nice talking, come by any time and we can do it again."
                    "She walks you to the door and you say goodbye."

                elif decision_score <= 55:
                    # She wants your opinion on some outfits
                    the_person "So [the_person.mc_title], now that I'm back on the market I think I need your help with something."
                    mc.name "With what?"
                    the_person "I need to update my wardrobe. You know, make it a little more modern. You're a hip young guy, I'm sure you can tell me what men like to see."
                    the_person "Would you help me? It'll just take a few minutes."
                    mc.name "Of course. Come on, show me what you've got."
                    "She smiles, drinks the last of her wine, and leads you into her bedroom."
                    call change_location(aunt_bedroom) from _call_change_location_1 #Changbe our location so that the background is correct,
                    the_person "Okay, so here's what I have to work with. Tell me what you think."
                    "She opens her wardrobe and stands back, giving you room to look around."
                    call outfit_master_manager() from _call_outfit_master_manager_10
                    #call screen outfit_creator(Outfit("New Outfit"))
                    if _return:
                        $ created_outfit = _return
                        "You pull out a few pieces of clothing and lay them out on [the_person.possessive_title]'s bed."
                        "She looks at the outfit you've laid out for her and seems to think for a second."
                        if created_outfit.slut_requirement <= the_person.sluttiness: #She likes it enough to try it on.
                            if created_outfit.vagina_visible():
                                the_person "Oh, wow. My pussy would just be out there, for everyone to see..."
                                "She sounds more excited than worried."
                            elif created_outfit.tits_visible():
                                the_person "Oh, wow. If I wore that my tits would just be out there, for everyone to see..."
                                "She sounds more excited than worried."
                            elif not created_outfit.wearing_panties():
                                the_person "Oh wow, you don't think I should wear any panties with it? I guess that's what girls are doing these days..."
                            elif not created_outfit.wearing_bra():
                                the_person "You don't think I'd need a bra? I don't want my girls bouncing around all the time. Or do I?"
                            else:
                                the_person "Oh, that looks so cute!"
                            $ the_person.update_outfit_taboos()

                            the_person "If I try it on will you tell me what you think?"
                            mc.name "Go for it. I want to see what it looks like on you."
                            "[the_person.possessive_title] starts to get undressed in front of you. She pauses after a second."
                            the_person "I'll just be naked for a second. You don't mind, right?"
                            mc.name "Of course not."
                            $ the_person.change_slut_temp(2)
                            the_person "I didn't think so. Just don't tell my sister."
                            $ strip_list = the_person.outfit.get_full_strip_list()
                            $ generalised_strip_description(the_person, strip_list)

                            "Once she's stripped out of her clothing, [the_person.possessive_title] puts on the outfit you've made for her."
                            $ the_person.apply_outfit(created_outfit, update_taboo = True)
                            #$ the_person.outfit = created_outfit.get_copy() changed v0.24.1
                            $ the_person.draw_person()

                            if created_outfit.slut_requirement <= the_person.sluttiness-20:
                                #She would like it normally and doesn't find it slutty.
                                the_person "Well, this is cute, but I don't know if I'm going to be wowing any men in it."
                                $ the_person.draw_person(position = "back_peek")
                                the_person "I think it needs to be a little... more. Or less, if you know what I mean."

                            else:
                                #She only likes it because she's drunk.
                                the_person "Well, it's certainly a lot bolder than I would normally wear. Is this the sort of thing men like?"
                                $ the_person.draw_person(position = "back_peek")
                                $ the_person.change_slut_temp(2)
                                the_person "What about my ass? Does it look good?"

                            menu:
                                "Add it to her wardrobe.":
                                    mc.name "It looks really good on you. You should wear it more often."
                                    the_person "You really think so? Okay then, that's why I wanted your opinion in the first place!"
                                    $ the_person.change_obedience(2)
                                    $ the_person.draw_person()
                                    $ the_person.wardrobe.add_outfit(created_outfit)
                                "Don't add it to her wardrobe.":
                                    mc.name "Now that I'm seeing it, I don't think it really suits you."
                                    the_person "That's a shame. Well, that's why I wanted your opinion in the first place!"
                                    $ the_person.change_obedience(1)
                                    "[the_person.title] starts to get naked again to put on her old outfit."

                                    $ strip_list = the_person.outfit.get_full_strip_list()
                                    $ generalised_strip_description(the_person, strip_list)
                                    $ the_person.apply_outfit(the_person.planned_outfit)
                                    #$ the_person.outfit = the_person.planned_outfit.get_copy() changed v0.24.1
                                    $ the_person.draw_person()
                            the_person "This was really fun [the_person.mc_title], but I think that extra glass of wine is starting to get to me."
                            "She yawns dramatically and lies down on her bed."
                            $ the_person.change_happiness(2)
                            the_person "I'm going to have a little nap, but we should do this again some time. You're so nice to have around."
                            mc.name "I'll make sure to come by again. I'll see myself out."



                        else: #It's too slutty even for her drunk state. She's bashful but doesn't try it on.

                            the_person "Oh my god [the_person.mc_title], do you really think I could wear that?"
                            $ the_person.change_slut_temp(2)
                            if created_outfit.vagina_visible():
                                the_person "My... pussy would just be out there for everyone to see!"
                            elif created_outfit.tits_visible():
                                the_person "I would just have my tits out for everyone!"
                            elif not created_outfit.wearing_panties():
                                the_person "It doesn't even have any panties for me!"
                            elif not created_outfit.wearing_bra():
                                the_person "It doesn't even have a bra for me!"
                            mc.name "I think it would be a good look for you. You should try it on."
                            "[the_person.possessive_title] blushes and shakes her head."
                            the_person "I don't think I can... Maybe that extra glass of wine wasn't such a good idea [the_person.mc_title], its gone straight to my head."
                            "She sits down on her bed and sighs."
                            the_person "I think I just need to have a rest. You can help me out with this some other day, okay?"
                            "[the_person.title] lies down and seems to be drifting off to sleep almost instantly. You say goodbye and head to the door."


                    else:
                        mc.name "Sorry [the_person.title], I don't have any ideas right now."
                        $ the_person.change_happiness(-2)
                        $ the_person.draw_person(emotion="sad")
                        "[the_person.possessive_title] sighs dramatically and collapses onto her bed."
                        the_person "Am I really that out of touch? I'll have to go shopping and update everything then."
                        the_person "Maybe I just need to lie down, this wine is really getting to me."
                        "[the_person.title] seems to be drifting off to sleep already. You say goodbye and head to the door."
                    $ clear_scene()
                    call change_location(aunt_apartment) from _call_change_location_3

                elif decision_score <= 65:
                    # She wants your opinion about some underwear
                    the_person "So [the_person.mc_title], since you're here I could use some help with something. It's a little... delicate."
                    mc.name "What do you need?"
                    the_person "Well, I want to put myself out there and meet someone, but I haven't done that since [cousin.title] was born."
                    the_person "I've got plenty of lingerie, but I need to know what looks good on me. Can I trust you to give me an honest opinion?"
                    mc.name "Of course, I'll tell you exactly what I think."
                    "She smiles, drinks the last of her wine, and leads you into her bedroom."
                    call change_location(aunt_bedroom) from _call_change_location_2 #Changbe our location so that the background is correct,
                    the_person "Okay, so I have a few things I want your opinion on. You just tell me what looks good and what I should keep around."
                    "She starts to strip down, then pauses and looks at you."
                    the_person "Don't tell my sister I'm doing this with you. We're both adults, but I don't think she'd understand."
                    "She rolls her eyes and keeps going."
                    $ the_person.change_slut_temp(1)

                    $ strip_list = the_person.outfit.get_full_strip_list()
                    $ generalised_strip_description(the_person, strip_list)

                    the_person "Okay, first one."
                    $ lingerie = default_wardrobe.get_random_appropriate_underwear(the_person.sluttiness, the_person.sluttiness-30, guarantee_output = True)
                    $ the_person.apply_outfit(lingerie, update_taboo = True)
                    #$ the_person.outfit = lingerie.get_copy() changed v0.24.1
                    $ the_person.draw_person()
                    "She slips on her new set of underwear."
                    the_person "Okay, what do you think? Keep or toss?"
                    $ the_person.draw_person(position="back_peek")
                    menu:
                        "Add it to her wardrobe.":
                            mc.name "Keep, definitely."
                            $ the_person.draw_person()
                            the_person "Okay, keep it is! Let's see what's up next..."
                            $ the_person.wardrobe.add_underwear_set(lingerie)
                        "Don't add it to her wardrobe.":
                            mc.name "Toss, I think you can do better."
                            $ the_person.draw_person()
                            the_person "I think so too. Let's see what's up next..."

                    $ the_person.change_slut_temp(1)

                    $ strip_list = the_person.outfit.get_full_strip_list()
                    $ generalised_strip_description(the_person, strip_list)

                    $ lingerie = default_wardrobe.get_random_appropriate_underwear(the_person.sluttiness, the_person.sluttiness-25, guarantee_output = True)
                    $ the_person.apply_outfit(lingerie, update_taboo = True)
                    #$ the_person.outfit = lingerie.get_copy() changed v0.24.1
                    $ the_person.draw_person()
                    "She slips on the next set of lingerie."
                    the_person "What about this one? Keep or toss?"
                    $ the_person.draw_person(position="back_peek")
                    menu:
                        "Add it to her wardrobe.":
                            mc.name "Keep."
                            $ the_person.draw_person()
                            the_person "We've got a winner! Okay, one more..."
                            $ the_person.wardrobe.add_underwear_set(lingerie)
                        "Don't add it to her wardrobe.":
                            mc.name "Toss."
                            $ the_person.draw_person()
                            the_person "Tough customer. Okay, one more..."

                    $ the_person.change_slut_temp(1)

                    $ strip_list = the_person.outfit.get_full_strip_list()
                    $ generalised_strip_description(the_person, strip_list)

                    $ lingerie = default_wardrobe.get_random_appropriate_underwear(the_person.sluttiness, the_person.sluttiness-20, guarantee_output = True)
                    $ the_person.apply_outfit(lingerie, update_taboo = True)
                    #$ the_person.outfit = lingerie.get_copy() changed v0.24.1
                    $ the_person.draw_person()
                    "She slips on the last set of underwear she has to show you."
                    $ the_person.draw_person(position="back_peek")
                    the_person "Well?"
                    menu:
                        "Add it to her wardrobe.":
                            mc.name "Keep it."
                            $ the_person.draw_person()
                            the_person "I thought you'd like this one. Okay, I'll hold onto it!"
                            $ the_person.wardrobe.add_underwear_set(lingerie)
                        "Don't add it to her wardrobe.":
                            mc.name "Toss it, you've got nice stuff you could wear."
                            $ the_person.draw_person()
                            the_person "Yeah, I think you're right. Let's get this off then!"
                            $ strip_list = the_person.outfit.get_full_strip_list()
                            $ generalised_strip_description(the_person, strip_list)

                    $ the_person.change_love(2)
                    $ the_person.change_slut_temp(2)
                    the_person "Thank you for helping me [the_person.mc_title]. Now I think I need to lie down, because that wine is going right to my head."
                    "She yawns dramatically and falls back onto her bed, arms spread wide."
                    the_person "Stop by again sometime soon though, we can do this again."
                    mc.name "Sure thing [the_person.title], I'll be by again soon."


                    $ clear_scene()
                    call change_location(aunt_apartment) from _call_change_location_4
                    # Same as above but she strips down and asks you for underwear sets.
                elif decision_score <= 75:
                    # She wants to strip for you.
                    the_person "[the_person.mc_title], does it feel warm in here or is it just me?"
                    "[the_person.title] takes a sip from her glass of wine and stands up."
                    if the_person.outfit.remove_random_any(exclude_feet = True, do_not_remove = True):
                        the_person "You don't mind if I get a little more comfortable, do you?"
                        $ strip_choice = the_person.outfit.remove_random_upper(top_layer_first = True, do_not_remove = True)
                        $ the_person.draw_animated_removal(strip_choice)
                        "Before you can answer she peels off her [strip_choice.name] and drops it onto the couch."
                        mc.name "No, go right ahead."
                        if the_person.outfit.remove_random_lower(do_not_remove = True):
                            $ strip_choice = the_person.outfit.remove_random_lower(top_layer_first = True, do_not_remove = True)
                            $ the_person.draw_animated_removal(strip_choice)
                            "She takes off her [strip_choice.name] next and throws it onto the couch too."
                    the_person "[the_person.mc_title], can I ask you a question? Do you think I'm still attractive?"
                    $ the_person.draw_person(position = "back_peek")
                    "She spins around in front of you, showing you her butt."
                    the_person "I mean, would you be attracted to me if I wasn't your aunt?"
                    menu:
                        "Encourage her." if the_person.outfit.remove_random_any(exclude_feet = True, do_not_remove = True):
                            mc.name "Keep taking your clothes off and maybe I'll tell you."
                            $ the_person.change_slut_temp(2)
                            $ the_person.change_obedience(1)
                            the_person "Oh? Okay then, I'll play your game, you dirty boy."
                            $ strip_choice = the_person.outfit.remove_random_any(exclude_feet = True, do_not_remove = True)
                            $ the_person.draw_animated_removal(strip_choice, position = "back_peek")
                            "She keeps her back to you and takes off her [strip_choice.name]."
                            the_person "Do you like watching me strip down for you? Do you think I'm hot?"
                            mc.name "Yeah, I think you're hot."
                            the_person "Oh [the_person.mc_title], that's so nice to hear. I just want to be wanted. Even if it's only by you..."
                            $ the_person.draw_person()
                            the_person "We should keep this our little secret, okay?"

                        "Compliment her.":
                            mc.name "Of course you're attractive [the_person.title], look at you! You've got a hot ass and a killer rack."
                            the_person "Oh [the_person.mc_title], you know just what I wanted to hear..."
                            "She wiggles her ass just for you."
                            the_person "You don't think I'm too old? I feel like I'm past my prime."
                            mc.name "You're beautiful, you have an amazing body, and you have the experience to know what to do with it."
                            $ the_person.change_happiness(5)
                            $ the_person.change_slut_temp(2)
                            $ the_person.change_love(1)
                            $ the_person.draw_person()
                            if the_person.outfit.tits_available():
                                "She turns back around and leans over to give you a hug on the couch. Her tits dangle down in front of you, tempting you."
                            else:
                                "She turns back around and leans over to give you a hug on the couch."
                            the_person "It's been so long since I felt wanted... I think I just needed to feel like I was, even if it's only by you..."

                        "Insult her.":
                            mc.name "Attractive? Sure, but you've got to accept you're past your prime."
                            $ the_person.change_happiness(-5)
                            the_person "What?"
                            mc.name "You're getting older [the_person.title], you just can't compete with all the younger women out there."
                            $ the_person.draw_person(emotion="angry")
                            "She turns back and crosses her arms."
                            the_person "You're telling me these aren't some nice tits?"
                            mc.name "Maybe, but you have to do more than just tease. If you want to impress someone get them wrapped around their cock."
                            mc.name "You've got experience, but you need to put it to work."
                            $ the_person.change_obedience(2)
                            $ the_person.change_slut_temp(3)
                            "She seems to think long and hard about this for a few seconds."
                            the_person "I guess I understand. Thank you for being honest with me."

                    $ the_person.draw_person(position="sitting")
                    "She sits down on the couch again and sighs."
                    the_person "I'm sorry but that extra glass of wine is just knocking me out. I think I'm going to lie down for a bit."
                    the_person "Do you want to come by another day and do this again?"
                    mc.name "I'd love to."
                    "You take your wine glasses to the kitchen for [the_person.title] and say goodbye."

                else:
                    "[the_person.possessive_title] slides closer to you on the couch and places her hand on your thigh while you chat."
                    "Inch by inch it moves up your leg until it brushes against the tip of your soft cock. She rubs it gently through your pants, coaxing it to life."
                    the_person "I... I know we shouldn't, but nobody needs to know. Right?"
                    if the_person.has_taboo("vaginal_sex") or the_person.has_taboo("anal_sex"):
                        the_person "We won't take it too far, I just really need this..."
                    menu:
                        "Fool around.":
                            call fuck_person(the_person) from _call_fuck_person_22
                            $ the_report = _return
                            "[the_person.possessive_title] lies down on the couch when you're finished."
                            if the_report.get("girl orgasms",0) > 0 and the_report.get("guy orgasms", 0) > 0:
                                the_person "That was great [the_person.mc_title], I feel like I'm floating."
                                "She looks up at you and giggles."
                                $ the_person.change_happiness(5)
                                the_person "And making you cum felt so good, I've still got it! I'm not too old yet! Haha..."
                                "She puts her head down and sighs happily."

                            elif the_report.get("girl orgasms",0) > 0:
                                the_person "Oh wow, you really know what you're doing [the_person.mc_title], I feel like I'm floating."
                                "She looks up at you and giggles."
                                the_person "Next time I'm going to make you cum too, I want to show you that I've still got it!"
                                mc.name "So there's going to be a next time?"
                                the_person "I hope so! That was everything I needed."
                                "She puts her head down and sighs happily."

                            elif the_report.get("guy orgasms", 0) > 0:
                                $ the_person.change_happiness(5)
                                the_person "Ah... It's good to know I can still make a young man cum his brains out."
                                "She looks up at you and giggles."
                                the_person "Maybe next time I can give you some pointers on what girls like. Teach you something to impress a girlfriend."
                                mc.name "So there's going to be a next time?"
                                the_person "If you want there to be. I have years of experience I need to pass on to the next generation."
                                "She puts her head down and sighs happily."


                            else:
                                the_person "We should, uh... It's probably a good idea we stop. I think I've had too much wine, I'm not thinking straight."
                                "She looks up at you and smiles."
                                the_person "But that was all very flattering. I'm sorry if I made you uncomfortable..."
                                mc.name "No, I was having a good time too."
                                the_person "It's kind of nice, still being wanted like that... Even if we shouldn't be doing this..."
                                "She puts her head back down and sighs."
                            "You move to the bathroom to get yourself cleaned up, and when you come back [the_person.title] is fast asleep."


                        "Turn her down.":
                            mc.name "I don't think that's a good idea right now [the_person.title]. You're in no state to make that kind of decision."
                            "You gently take her hand off you. She seems to snap to her senses and looks away."
                            the_person "Right, of course. I didn't mean... I didn't mean anything, okay?"
                            $ the_person.change_love(1)
                            $ the_person.change_obedience(1)
                            the_person "Maybe you should go, I'm clearly not thinking straight with all this wine."
                            mc.name "That may be for the best. Maybe we can do this again some other time though."
                            "You take the glasses of wine to the kitchen for [the_person.possessive_title] and say goodbye."


                $ the_person.clear_situational_slut("Drunk")

            else:
                the_person "Oh, I really shouldn't. Too much wine makes me go silly."
                $ the_person.draw_person()
                "[the_person.title] waits until you've finished your glass of wine, then escorts you to the door."
                mc.name "See you soon [the_person.title]."
                the_person "I hope so! See you around."
        "Say goodbye.":
            "[the_person.title] waits until you've finished your glass of wine, then escorts you to the door."
            mc.name "See you soon [the_person.title]."
            the_person "I hope so! See you around."

    call advance_time() from _call_advance_time_17 #Drinking advances time
    return

label family_games_night_intro(the_person): # Triggered as an on-talk event in her apartment. #TODO: Hook this up.
    #Aunt introduces the family games night. she's already talked to your mother and it's planned for [some evening].
    # you're not required to go, but you're always welcome!
    $ the_person.draw_person()
    "You knock on the door of [the_person.possessive_title]'s apartment. After a brief pause she opens the door while talking to someone on her cell phone."
    the_person "... Well speak of the devil, he's just come by for a visit."
    "She gives you a smile and waves you into the living room, closing the door behind you."
    the_person "Oh no, he's no trouble... No, I don't mind at all... Don't worry, he's a wonderful kid."
    "You sit down on the couch and relax while she finishes her phonecall."
    the_person "Yeah... I'll tell him. Talk to you soon. Love you sis."
    "[the_person.title] dramatic kissing noise before hanging up and turning her attention to you."
    the_person "Hi [the_person.mc_title], I'm glad you've stopped by."
    $ the_person.draw_person(position = "sitting")
    "She gives you a kiss on the forehead and sits down on the couch next to you."
    mc.name "It's good to see you [the_person.title]. Did you need to tell me something?"
    the_person "That was your mom. We want to spend more time together as a family, so she invited me to spend wednesday evenings with her."
    the_person "We'll probably have some drinks, chat about what we've been doing, maybe play some cards."
    the_person "If you don't have anything better to do than hang out with a couple of old women you're welcome to join us."
    menu:
        "Promise to join.":
            mc.name "I'd love to spend time with both of you. I'll do my best to make it."
            the_person "I'm looking forward to it even more now!"

        "You'll think about it.":
            mc.name "It sounds like fun, but I'm not sure if I'll be free."
            the_person "I understand, you're a busy boy."

    $ init_family_games_night()
    $ clear_scene()
    return

label family_games_night_setup(the_mom, the_aunt): # Triggered as a mandatory crisis right before the
    python:
        if the_mom.get_desination(specified_time = 4) in [the_mom.home, None, hall] and the_aunt.get_desination(specified_time = 4) in [the_aunt.home, None, hall]: #Change their schedule if they aren't explicitly suppose to be somewhere else.
            the_mom.set_schedule(hall, [2], [4]) #She is in the hall on wednesdays in the evening.
            the_aunt.set_schedule(hall, [2], [4]) #She is in the hall on wednesdays in the evening.

        elif the_mom.get_desination(specified_time = 4) == hall: #She's in the hall but her sister can't make it.
            the_mom.set_schedule(the_mom.home, [2], [4])

        elif the_aunt.get_desination(specified_time = 4) == hall: #She's in the hall but her sister can't make it.
            the_aunt.set_schedule(the_aunt.home, [2], [4])


        if not mc.business.event_triggers_dict.get("family_games_setup_complete", False):
            mc.business.event_triggers_dict["family_games_drink"] = 0
            mc.business.event_triggers_dict["family_games_cards"] = 0
            mc.business.event_triggers_dict["family_games_fun"] = 0
            mc.business.event_triggers_dict["family_games_cash"] = 0
            mc.business.event_triggers_dict["family_games_strip"] = 0
            mc.business.event_triggers_dict["family_games_setup_complete"] = True

        init_family_games_night() #Re-add the event for next week.
    return

init -1 python:
    def init_family_games_night():
        family_games_night_setup_action = Action("Family games night setup", family_games_night_setup_requirement, "family_games_night_setup", args = [mom, aunt])
        mc.business.mandatory_crises_list.append(family_games_night_setup_action)

        family_games_night_action = Action("Family games night", family_games_night_requirement, "family_games_night_start", args = [aunt], requirement_args = [aunt])
        family_games_night_LTE = Limited_Time_Action(family_games_night_action, 2)
        mom.on_room_enter_event_list.append(family_games_night_LTE)


label family_games_night_start(the_aunt, the_mom): # Triggered as an on enter event
    # Girls ask if you want to have some drinks, and then play cards some cards.

    $ the_group = GroupDisplayManager([the_mom, the_aunt], the_mom)
    $ the_group.draw_group(position = "sitting", emotion = "happy")
    $ first_time = mc.business.event_triggers_dict.get("family_games_cards",0) == 0

    # Ensure neither of them have shown up with outfits too slutty for the other to consider appropriate.
    $ highest_slut = the_aunt.effective_sluttiness()
    if the_mom.effective_sluttiness() > highest_slut:
        $ highest_slut = the_mom.effective_sluttiness()
    $ the_aunt.apply_outfit(the_aunt.wardrobe.get_random_appropriate_outfit(sluttiness_limit = highest_slut, guarantee_output = True))
    $ the_mom.apply_outfit(the_mom.wardrobe.get_random_appropriate_outfit(sluttiness_limit = highest_slut, guarantee_output = True))

    "[the_mom.title] and [the_aunt.title] are sitting on the couch, chatting happily to each other when you enter the living room."
    if first_time:
        the_mom "Welcome home [the_mom.mc_title]. [the_aunt.title] is here to visit for the evening."
        $ the_group.draw_person(the_aunt, position = "sitting", emotion = "happy")
        the_aunt "Hi [the_aunt.mc_title]. We were just about to have some drinks, do you want to join us?"
    else:
        the_mom "Welcome home [the_mom.mc_title]. [the_aunt.title] is over to play some cards this evening."
        $ the_group.draw_person(the_aunt, position = "sitting", emotion = "happy")
        the_aunt "Hi [the_aunt.mc_title]. We're having some drinks first, do you want to join us?"

    menu:
        "Join them.":
            call family_games_night_drinks(the_mom, the_aunt) from _call_family_games_night_drinks
            $ mc.business.event_triggers_dict["family_games_drink"] += 1

        "Say you're busy.":
            mc.name "Sorry, but I'll have to take a rain check tonight. Maybe next time."
            $ the_group.redraw_person(the_mom)
            the_mom "Have a good evening sweetheart. We'll try not to make too much noise."
            $ the_group.redraw_person(the_aunt)
            the_aunt "No promises, my sister gets pretty rowdy once she has a couple of glasses of wine in her."
            $ the_group.redraw_person(the_mom)
            the_mom "Hey!"
            "She slaps her sister playfully on the shoulder."
            the_mom "Just for that you're going to have to go pour the drinks! Go on, get!"
            "You leave the girls in the living room as they drink and gossip."



    # Otherwise they just ask you to go get your sister, it's becoming a routine.
    # Opportunity to drop out early here if all you wanted to do was dose them.

    $ clear_scene()
    return

label family_games_night_drinks(the_mom, the_aunt): #Breakout function for the drink serving section to keep things organised.
    $ first_time = mc.business.event_triggers_dict.get("family_games_cards",0) == 0
    mc.name "I'd love to. What are you drinking?"
    the_aunt "I brought over a bottle of wine for us. It's in the kitchen, would you mind pouring us some?"
    $ the_group.redraw_person(the_mom)
    the_mom "I can take care of that [the_aunt.title], [the_mom.mc_title] is probably tired and just wants to relax."
    $ the_group.redraw_person(the_aunt)
    the_aunt "He's getting free drinks. He should be pampering us like the refined wine moms we are."
    menu: #TODO: Have an option for Aunt at high obedience where you command her to do it for you.
        "Pour the drinks yourself.":
            mc.name "Don't worry about it [the_mom.title], I'll be back with drinks in a moment."
            $ the_group.redraw_person(the_mom)
            the_mom "You're so sweet. Thank you."
            $ clear_scene()
            $ kitchen.show_background()
            "You find the bottle of wine easily in the kitchen and pour three glasses."
            menu:
                "Add a dose of serum to [the_mom.title]'s wine." if mc.inventory.get_any_serum_count() > 0:
                    call give_serum(the_mom) from _call_give_serum_29
                    if _return:
                        "You add a dose of serum into [the_mom.title]'s wine and swirl the glass, mixing it in thoroughly."
                    else:
                        "You reconsider, and decide not to add anything to [the_mom.title]'s drink."

                "Add a dose of serum to [the_mom.title]'s wine.\nRequires: Serum (disabled)" if mc.inventory.get_any_serum_count() == 0:
                    pass

                "Leave her drink alone.":
                    pass

            menu:
                "Add a dose of serum to [the_aunt.title]'s wine." if mc.inventory.get_any_serum_count() > 0:
                    call give_serum(the_aunt) from _call_give_serum_30
                    if _return:
                        "You add a dose of serum into [the_aunt.title]'s wine and swirl the glass, mixing it in thoroughly."
                    else:
                        "You reconsider, and decide not to add anything to [the_aunt.title]'s drink."

                "Add a dose of serum to [the_aunt.title]'s wine.\nRequires: Serum (disabled)" if mc.inventory.get_any_serum_count() == 0:
                    pass

                "Leave her drink alone.":
                    pass

            $ hall.show_background()
            $ the_group.redraw_group()
            "You return to the living room and hand [the_mom.possessive_title] and [the_aunt.possessive_title] their drinks and sit back down beside them."

        "Let [mom.title] pour the drinks.":
            mc.name "You're right [the_mom.title], I could really use a break."
            "[the_mom.possessive_title] stands up and motions to the couch as she walks towards the kitchen."
            $ the_group.draw_person(the_mom, emotion = "happy")
            the_mom "You sit down, I'll be back in a moment with drinks for everyone."
            $ the_mom.change_obedience(1)
            $ clear_scene()
            $ the_aunt.draw_person(position = "sitting", emotion = "happy")
            "As [the_mom.title] leaves her sister turns to you and shakes her head."
            the_aunt "Are you this popular with all of the ladies? You have my big sis falling over herself to serve you."
            mc.name "I try to be. I'm lucky to have such an amazing mother."
            the_aunt "You really are, and don't you forget it."
            $ clear_scene()
            $ the_group.set_primary(the_mom)
            $ the_group.redraw_group()
            "[the_mom.possessive_title] comes back into the living room, three glasses of wine balanced between both hands."
            $ the_group.draw_person(the_mom, position = "sitting", emotion = "happy")
            "She hands out the drinks, then sits back down beside her sister."

    $ the_mom.change_happiness(5)
    the_mom "This is nice, you two. I'm glad we're able to get together like this."
    "[the_mom.possessive_title] and [the_aunt.possessive_title] chat about their week, happily trading stories and opinions."
    "You sip at your own glass of wine, content to just listen."
    "After a half an hour of drinking and gossip [the_mom.title] puts her finished glass aside."
    if first_time:
        the_mom "Would you two like to play something while we drink? I have a pack of cards in the kitchen."
        $ the_group.redraw_person(the_aunt)
        the_aunt "Oh my god, we use to play cards every night after school. Do you play cards often [the_aunt.mc_title]?"
        mc.name "Not very often."
        the_aunt "Well I'm sure you'll catch on quickly. Do you want to try?"

    else:
        the_mom "We should decide now if we want to play any cards tonight. If I have another glass of wine I'll be hopeless."
        $ the_group.redraw_person(the_aunt)
        the_aunt "Cards sound like a lot of fun. What do you think [the_aunt.mc_title]?"

    menu:
        "Play cards.\n{image=gui/heart/Time_Advance.png}":
            if first_time:
                mc.name "Cards sound like like fun, but you'll have to teach me how to play."
                the_aunt "First we'll need a fourth player, so we can split up into teams."
                $ the_group.redraw_person(the_mom)
                the_mom "[the_mom.mc_title], go see if your sister wants to come and play. We'll set up in the kitchen."

            else:
                mc.name "I'm up for some cards. I'll go see if Lily wants to join."
                the_aunt "Okay, we'll go and set up in the kitchen."

            $ clear_scene()
            if lily in lily_bedroom.people:
                "You knock on [lily.possessive_title]'s bedroom door."
                lily "It's open!"
                $ lily.draw_person()
                lily "What's up [lily.mc_title]?"
                if first_time:
                    mc.name "[the_mom.title] and [the_aunt.title] want to play some cards, and we need a fourth player."
                    mc.name "Do you want to come and play?"
                    "She sighs and rolls her eyes."
                    lily "Cards? Like poker?"
                    mc.name "I don't think so. It's some game they played back when they were kids."
                    lily "We need to tell them that nobody plays with cards any more."
                    mc.name "They're having a good time together, let's just humour them, okay?"
                    lily "Fine, I wasn't doing anything tonight anyways."
                else:
                    mc.name "[the_mom.title] and [the_aunt.title] want to play cards again. Do you want to be our fourth player?"
                    lily "Sure, I guess I'm not doing anything else."
                    "She sighs."
                    lily "How sad is that? The most exciting thing I have to be doing is playing cards with my mom?"
                    mc.name "I'm sure we can figure out how to make it more exciting."
                    #TODO: This is where you can ask her to take a dive for you.

                call family_games_night_cards(the_mom, the_aunt, lily) from _call_family_games_night_cards
                $ mc.business.event_triggers_dict["family_games_cards"] += 1
                call advance_time() from _call_advance_time_30

            else:
                "You knock on [lily.possessive_title]'s bedroom door. After you get no response you open it and peek inside."
                $ kitchen.show_background()
                $ the_group.draw_group(emotion = "happy")
                "The room is empty. You head back to the kitchen, where [the_mom.possessive_title] and [the_aunt.possessive_title] are sorting a deck of cards."
                mc.name "Bad news. It looks like Lily is out for the night."
                $ the_mom.draw_person()
                the_mom "Oh, that's too bad."
                $ the_aunt.draw_person()
                the_aunt "I think I'll just have another glass of wine then, if you don't mind [the_mom.title]."
                the_aunt "We can play cards next time I'm over."
                $ the_mom.draw_person()
                the_mom "Pour me one as well, I think I'm going to join you."
                "The sisters return to the living room and relax on the couch together."
                #TODO: Add a mom and aunt event specifically if Lily is busy (or she doesn't want to play/you don't invite her.)


        "Call it a night.":
            mc.name "I'm going to have to pass this time, I have some business to attend to."
            $ the_group.redraw_person(the_aunt)
            the_aunt "Then the drinking will continue! Pour me another glass sis!"
            "You finish your own glass of wine and leave the girls in the living room to chat with each other."



    # Get Lily and bring her back, gather around the kitchen table to play.
    return

label family_games_night_cards(the_mom, the_aunt, the_sister): #Breakout function for the card game to keep things organised (and support adding new varients later)

    $ the_group = GroupDisplayManager([the_mom, the_aunt, the_sister], the_mom)
    $ the_group.draw_group()
    "You bring [lily.title] back to the kitchen, where you find [the_mom.possessive_title] and [the_aunt.possessive_title] sorting a deck of cards."
    the_mom "And now the gang's all together! Pull up a chair, we've got the deck sorted out."
    $ the_group.draw_group(position = "sitting")
    "You sit down around the table while [the_mom.possessive_title] shuffles the deck."
    $ partner = None

    $ first_time = mc.business.event_triggers_dict.get("family_games_cards",0) == 0
    if first_time:
        the_mom "Alright, so have either of you two ever played euchre?"
        "[the_sister.title] shakes her head."
        the_mom "It's a card game that was popular back when me any my sister were in school."
        the_mom "You play it with a partner, and the goal is to win as many hands as possible."
        the_mom "The trick is that you don't know what cards your partner has, so..."
        "You listen as [the_mom.possessive_title] explains the rules of the game."
        if mc.int <= 2:
            "You do your best to follow along, but you don't think you've fully grasped the concept."
        else:
            "When she's finished you think you have a solid understanding of how to play."

        the_mom "Now normally we would pick our partners first, but it wouldn't be very fair to put the two new players on the same team."
        the_mom "So let's split up. [the_sister.title], you can be my partner."
        $ the_group.redraw_person(the_aunt)
        the_aunt "And I'll team up with you, [the_aunt.mc_title]."
        $ partner = the_aunt

        $ the_group.redraw_person(the_mom)
        the_mom "Well, is everyone ready?"
        $ the_group.redraw_person(the_aunt)
        the_aunt "Wait, what are we playing for?"
        $ the_group.redraw_person(the_mom)
        the_mom "It's just suppose to be a friendly game. We don't need to play for anything."
        $ the_group.redraw_person(the_aunt)
        the_aunt "Come on, we use to play for cash all the time. Let's make it interesting."
        $ the_group.redraw_person(the_mom)
        the_mom "[the_mom.mc_title], [the_sister.title], what do you want to do?"
    else:
        the_mom "Okay then, we need to pick teams. [the_person.mc_title], you can pick first."
        call screen person_choice([the_mom, the_aunt, the_sister], person_prefix = "Pick", person_suffix = "as your partner.")
        $ partner = _return
        "You pick [partner.title] and move seats so you are sitting across from each other."
        $ the_group.redraw_person(partner)
        if partner == the_mom:
            partner "Good choice, we work so well together."
        elif partner == the_aunt:
            partner "Your son knows how to pick the winning team sis."
            "She gives you a friendly wink."
        else: # the_sister
            partner "Okay, let's give it our best shot I guess..."
            $ the_group.redraw_person(the_aunt)
            the_aunt "Age versus experience, let's see how well you two have learned!"
            $ the_group.redraw_person(the_mom)
            the_mom "Don't worry you two, we'll go easy on you."

        $ the_group.redraw_person(the_aunt)
        the_aunt "So, what are we playing for tonight? Any suggestions?"



    menu:
        "Play for fun.":
            # standard, always enabled
            $ first_time_fun = mc.business.event_triggers_dict.get("family_games_fun", 0) == 0
            if first_time_fun:
                mc.name "Let's just play for fun. I could use some more practice before I put anything more on the line."
            else:
                mc.name "Let's just play for fun, I don't want to put anything more on the line."
            $ the_group.redraw_person(the_mom)
            the_mom "That's a very reponsible decision [the_mom.mc_title]."
            call family_games_night_fun(the_mom, the_aunt, the_sister, partner) from _call_family_games_night_fun
            $ mc.business.event_triggers_dict["family_games_fun"] += 1

        "Play for cash." if the_mom.love >= 30 and the_aunt.love >= 30 and the_sister.love >= 30:
            $ first_time_cash = mc.business.event_triggers_dict.get("family_games_cash", 0) == 0
            if first_time_cash:
                mc.name "Let's make it interesting and play for a little bit of cash."
                $ the_group.redraw_person(the_aunt)
                the_aunt "Sounds like fun!"
            else:
                mc.name "Let's play for some cash again. It made the game a lot more interesting."
                "[the_aunt.title] smiles happily."

            call family_games_night_cash(the_mom, the_aunt, the_sister, partner) from _call_family_games_night_cash
            $ mc.business.event_triggers_dict["family_games_cash"] += 1

        "Play for cash.\nRequires: 30 Love, All (disabled)" if the_mom.love < 30 or the_aunt.love < 30 or the_sister.love < 30:
            pass


        "Play strip euchre." if the_mom.sluttiness >= 30 and the_sister.sluttiness >= 30 and the_aunt.sluttiness >= 30:
            $ first_time_strip = mc.business.event_triggers_dict.get("family_games_strip", 0) == 0
            if first_time_strip:
                mc.name "I know something that will make the game very interesting."
                mc.name "[the_mom.title], [the_aunt.title], have you two ever played strip poker?"
                $ the_group.redraw_person(the_mom)
                "[the_mom.possessive_title] gasps quietly and shakes her head."
                the_mom "[the_mom.mc_title], I would never..."
                "She's interupted by her sister."
                $ the_group.redraw_person(the_aunt)
                the_aunt "Yeah, I have."
                "[the_mom.title] turns to [the_aunt.possessive_title], looking suprised."
                $ the_group.redraw_person(the_mom)
                the_mom "You have? When?"
                "[the_aunt.title] giggles and shrugs."
                $ the_group.redraw_person(the_aunt)
                the_aunt "A bunch of times in university. It's a fun party game."
                $ the_group.redraw_person(the_mom)
                the_mom "I... Really? I can't believe my own little sister was getting into so much mischief and I never knew!"
                "[the_aunt.title] shrugs again."
                $ the_group.redraw_person(the_aunt)
                the_aunt "Come on, it sounds like it could be fun. Let's give it a try."
                $ the_group.redraw_person(the_mom)
                the_mom "No, I couldn't... I mean, I don't want to have to... strip in front of all of you."
                "You sit back, happy to let [the_aunt.possessive_title] do the convincing for you."
                $ the_group.redraw_person(the_aunt)
                the_aunt "That's why you try and win! Don't be such a stick in the mud, it'll be fun!"
                "[the_mom.possessive_title] considers it for a long moment, then sighs and srugs."
                $ the_group.redraw_person(the_mom)
                the_mom "Fine, but I don't want anyone taking this further than they're comfortable with. Okay?"
                $ the_group.redraw_person(the_aunt)
                the_aunt "Of course. Okay, let's play!"
            else:
                mc.name "Let's play strip euchre again, that was interesting last time."
                $ the_group.redraw_person(the_aunt)
                the_aunt "Alright, strip euchre it is. Let's play!"

            call family_games_night_strip(the_mom, the_aunt, the_sister, partner) from _call_family_games_night_strip
            $ mc.business.event_triggers_dict["family_games_strip"] += 1

        "Play strip euchre.\nRequires: 30 Sluttiness, All (disabled)" if the_mom.sluttiness < 30 or the_sister.sluttiness < 30 or the_aunt.sluttiness < 30:
            pass

        #TODO: Figure out if we want an even higher tier (Maybe not yet, since we've avoided most inter-family stuff.
        # |-> Maybe if a girl strips completely you can add an extra requirement.


    if mc.business.event_triggers_dict.get("family_games_cards", 0) == 0:
        the_mom "This was a lot of fun [the_aunt.title]. Should we do it again next week."
        $ the_group.redraw_person(the_aunt)
        the_aunt "That sounds great. I'll bring the wine again."
    else:
        the_mom "Okay, I'll walk you to the door. This was a lot of fun, as always."
        $ the_group.redraw_person(the_aunt)
        the_aunt "Same time next week?"
        $ the_group.redraw_person(the_mom)
        the_mom "As long as you bring the wine!"

    "[the_mom.possessive_title] walks [the_aunt.possessive_title] to the door while you and [the_sister.title] clean up the kitchen."
    "It's already late, so when you're finished you go back to your room and go to bed."
    return

label family_games_night_fun(the_mom, the_aunt, the_sister, partner):
    # Describes a game where you're playing for fun.
    $ still_playing = True
    $ round_count = 1
    $ max_rounds = 5

    $ opponents = [the_mom, the_aunt, the_sister]
    $ opponents.remove(partner)
    $ opponent_a = opponents[0]
    $ opponent_b = opponents[1]

    $ the_group = GroupDisplayManager([the_mom, the_aunt, the_sister], partner)
    $ clear_scene()
    $ the_group.draw_group(position = "sitting")

    while still_playing:
        call card_round_description(the_mom, the_aunt, the_sister, partner, round_count) from _call_card_round_description
        if _return:
            # if partner == the_mom:
            #     pass #TODO
            # elif partner == the_aunt:
            #     pass #TODO: Unique dialogue
            # else: the_sister
            #     pass #Dialogue
            $ the_group.draw_person(partner, position = "sitting", emotion = "happy")
            $ partner.change_happiness(2)
            partner "Nice! Good play [partner.mc_title]."

            $ the_group.draw_person(opponent_a, position = "sitting")
            opponent_a "Gah, I thought we had that one..."


        else:

            # if partner == the_mom:
            #     pass #TODO
            # elif partner == the_aunt:
            #     pass #TODO: Unique dialogue
            # else: the_sister
            #     pass #Dialogue
            $ the_group.draw_person(opponent_b, position = "sitting", emotion = "happy")
            $ opponent_a.change_happiness(2)
            $ opponent_b.change_happiness(2)
            opponent_b "Ooh, tough break there."
            $ the_group.draw_person(opponent_a, position = "sitting")
            opponent_a "I'm sure you'll get us next time though."

        if round_count > max_rounds:
            $ still_playing = False
            $ the_group.redraw_person(the_aunt)
            "[the_aunt.possessive_title] pushes her cards towards the center of the table."
            the_aunt "Well, this has been a lot of fun but I should be heading home. It's getting late and I need to get a cab home."

        $ round_count += 1 #The only thing that stops us is if we're over our round count.

    return

label family_games_night_cash(the_mom, the_aunt, the_sister, partner):
    # Describes a game where you're playing for cash.
    $ still_playing = True
    $ round_count = 1
    $ max_rounds = 5

    $ opponents = [the_mom, the_aunt, the_sister]
    $ opponents.remove(partner)
    $ opponent_a = opponents[0]
    $ opponent_b = opponents[1]

    $ the_group = GroupDisplayManager([the_mom, the_aunt, the_sister], partner)
    $ clear_scene()
    $ the_group.draw_group(position = "sitting")
    while still_playing:
        call card_round_description(the_mom, the_aunt, the_sister, partner, round_count) from _call_card_round_description_1
        if _return:
            $ partner.change_happiness(5)
            $ opponent_a.change_happiness(-1)
            $ opponent_b.change_happiness(-1)
            # if partner == the_mom:
            #     pass #TODO
            # elif partner == the_aunt:
            #     pass #TODO: Unique dialogue
            # else: the_sister
            #     pass #Dialogue
            $ the_group.draw_person(partner, position = "sitting", emotion = "happy")
            partner "Yes!"
            mc.name "Ooh, tough break girls. Come on, pay up."
            "[opponent_a.possessive_title] and [opponent_b.possessive_title] sigh and pull out a twenty."
            "They slide the money over to you and [partner.possessive_title]."
            $ mc.business.funds += 20
        else:

            $ partner.change_happiness(-1)
            $ opponent_a.change_happiness(5)
            $ opponent_b.change_happiness(5)
            # if partner == the_mom:
            #     pass #TODO
            # elif partner == the_aunt:
            #     pass #TODO: Unique dialogue
            # else: the_sister
            #     pass #Dialogue
            # pass #TODO: Loss dialogue
            $ the_group.draw_person(opponent_a, position = "sitting", emotion = "happy")
            opponent_a "So sorry about this, but it looks we won."
            $ the_group.draw_person(opponent_b, position = "sitting", emotion = "happy")
            opponent_b "You know the rules."
            if mc.business.funds >= 20:
                $ mc.business.funds += -20
            else:
                "You pull out your wallet and realise there's no more cash in it."
                mc.name "Uh... it looks like you've cleared me out."
                $ opponent_a.change_happiness(-2)
                $ opponent_b.change_happiness(-2)
                "[opponent_b.possessive_title] looks disappointed, but [opponent_a.title] just smiles and shrugs."
                $ the_group.draw_person(opponent_a, position = "sitting")
                opponent_a "Looks like that's the end of the game then. We win!"
                $ the_group.redraw_person(the_aunt)
                the_aunt "It's getting late, so this is probably a good time for me to head out too."

        if round_count > max_rounds and still_playing:
            $ still_playing = False
            $ the_group.redraw_person(the_aunt)
            "[the_aunt.possessive_title] pushes her cards towards the center of the table."
            the_aunt "Well, this has been a lot of fun but I should be heading home. It's getting late and I need to get a cab home."


        $ round_count += 1 #The only thing that stops us is if we're over our round count.

    # Outro dialogue. Assumes you've already talked about why you're stopping.
    if first_time: #TODO: Hook this up
        the_mom "This was a lot of fun [the_aunt.title]. Should we do it again next week."
        $ the_group.redraw_person(the_aunt)
        the_aunt "That sounds great. I'll bring the wine again."
    else:
        the_mom "Okay, I'll walk you to the door. This was a lot of fun, as always."
        $ the_group.redraw_person(the_aunt)
        the_aunt "Same time next week?"
        $ the_group.redraw_person(the_mom)
        the_mom "As long as you bring the wine!"
    return

label family_games_night_strip(the_mom, the_aunt, the_sister, partner):
    # Describes a game where you're playing to strip each other down.
    #TODO: All of this
    $ still_playing = True
    $ round_count = 1
    $ max_rounds = 5

    $ player_wins = 0 #AKA girl losses
    $ player_losses = 0

    $ opponents = [the_mom, the_aunt, the_sister]
    $ opponents.remove(partner)
    $ opponent_a = opponents[0]
    $ opponent_b = opponents[1]

    $ the_group = GroupDisplayManager([the_mom, the_aunt, the_sister], partner)
    $ clear_scene()
    $ the_group.draw_group(position = "sitting")
    while still_playing:
        $ still_playing = True
        call card_round_description(the_mom, the_aunt, the_sister, partner, round_count) from _call_card_round_description_2
        if _return:
            $ player_wins += 1
            # if partner == the_mom:
            #     pass #TODO
            # elif partner == the_aunt:
            #     pass #TODO: Unique dialogue
            # else: the_sister
            #     pass #Dialogue

            #TODO: We need to check if we've won already.
            $ something_to_strip = False
            python:
                for person in [opponent_a, opponent_b]:
                    the_item = person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True)
                    if the_item:
                        something_to_strip = True


            if something_to_strip:
                mc.name "Good try girls, but that round is ours."
                $ the_group.redraw_person(partner)
                partner "You know what that means!"
                $ partner.change_happiness(2)
                $ the_group.redraw_person(opponent_b)
                opponent_b "Yeah, we know. Come on, let's get this over with."
                $ something_removed = False
                python:
                    for person in [opponent_a, opponent_b]:
                        the_item = person.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True)
                        if the_item:
                            euchre_strip_description(person, the_item, the_group)
                            something_removed = True
                            person.change_slut_temp(1)
                    #TODO: Add some dialogue to describe what they strip down.
            else:
                "[opponent_a.title] sighs, and [opponent_b.title] pushes her cards into the center of the kitchen table."
                $ the_group.redraw_person(opponent_a)
                opponent_a "Okay, we're out of clothes. You two win."
                $ the_group.redraw_person(opponent_b)
                opponent_b "Well done. Can we get dressed now? It's a little chilly..."
                $ the_group.redraw_person(partner)
                partner "What do you think [partner.mc_title]? Should we let them off easy?"
                menu:
                    "Let them get dressed.":
                        mc.name "Good game everyone, now let's get dressed and get everything cleaned up."

                    "Give us a dance.": #TODO: Decide on any requirements. Maybe sluttiness or obedience for the two dancers
                        mc.name "I don't think so [partner.title]. I think we should get a little reward for winning."
                        $ the_group.redraw_person(opponent_a)
                        opponent_a "What do you want?"
                        mc.name "You've been able to hide behind the table all night, so I want a little dance now."
                        "[opponent_a.possessive_title] and [opponent_b.possessive_title] glance at each other."
                        opponent_a "What do you think?"
                        $ the_group.redraw_person(opponent_b)
                        opponent_b "I mean... It's just a silly game, right? It doesn't mean anything..."
                        $ the_group.redraw_person(opponent_a)
                        opponent_a "Okay, fine. Then we're getting dressed."
                        mc.name "Sounds fair to me."
                        $ the_group.draw_person(opponent_b, False)
                        $ the_group.draw_person(opponent_a)
                        "The girls slide their chairs back from the kitchen table and stand up next to each other."
                        opponent_a "Okay, so how do we do this?"
                        $ the_group.redraw_person(opponent_b)
                        opponent_b "Just move around a little. Here, like this..."
                        $ the_group.draw_person(opponent_b, the_animation = tit_bob, animation_effect_strength = 0.6)
                        "[opponent_b.title] takes the lead, swaying her hips and holding her hands high and out of the way."
                        $ the_group.draw_person(opponent_a, the_animation = tit_bob, animation_effect_strength = 0.6)
                        "After watching for a second [opponent_a.title] starts to follow along."
                        mc.name "Turn around ladies, let's get a full view of things."
                        opponent_a "Oh my god, this is so embarrassing..."
                        $ the_group.draw_person(opponent_a, position = "walking_away", the_animation = tit_bob, animation_effect_strength = 0.6)
                        $ the_group.draw_person(opponent_b, False, position = "walking_away", the_animation = tit_bob, animation_effect_strength = 0.6)
                        "Despite her complains she spins around, and [opponent_b.possessive_title] does the same."
                        "You turn to [partner.possessive_title], who is still sitting at the table next to you."
                        mc.name "Enjoying the show [partner.title]?"
                        $ the_group.redraw_person(partner)
                        partner "It could be better. I think we might need a better view..."
                        $ the_group.redraw_person(opponent_b)
                        opponent_b "Like this?"
                        $ the_group.draw_person(opponent_b, position = "standing_doggy", the_animation = ass_bob, animation_effect_strength = 0.6)
                        "[opponent_b.possessive_title] puts her hand on the kitchen counter and bends forward. She spreads her legs and twerks her ass for you."
                        $ the_group.redraw_person(opponent_a)
                        opponent_a "Oh my god, where did you learn to do that?"
                        "[opponent_b.title] just laughs and wiggles her butt a few more times before standing up."
                        $ the_group.draw_person(opponent_b)
                        opponent_b "Alright, I think they've seen enough."
                        $ the_group.draw_person(opponent_a)
                        opponent_a "Whew... Well I think we should get everything tidied up and then get dressed."
                        $ partner.change_slut_temp(2)
                        $ opponent_a.change_slut_temp(2)
                        $ opponent_b.change_slut_temp(2)
                        $ opponent_a.change_obedience(5)
                        $ opponent_b.change_obedience(5)



        else:
            $ player_losses += 1
            # if partner == the_mom:
            #     pass #TODO
            # elif partner == the_aunt:
            #     pass #TODO: Unique dialogue
            # else: the_sister
            #     pass #Dialogue

            $ partner_item = partner.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True)
            if partner_item:
                #TODO: Add in a check to see if a girl wants to quit after stripping.
                $ the_group.redraw_person(opponent_b)
                opponent_b "[opponent_a.title], I think we just won. What does that mean again?"
                $ the_group.redraw_person(opponent_a)
                opponent_a "I think it means [opponent_a.mc_title] and [partner.title] need to start stripping!"
                $ the_group.redraw_person(partner)
                partner "Come on, let's get this over with [partner.mc_title]."
                $ euchre_strip_description(partner, partner_item, the_group)

                "[partner.possessive_title] grabs her [partner_item.display_name] and pulls it off while [opponent_a.title] and [opponent_b.title] watch."
            else:
                if player_losses > 4:
                    # You're naked too, so you lose.
                    $ still_playing = False
                    "[opponent_a.title] and [opponent_b.title] cheer."
                    $ the_group.redraw_person(opponent_b)
                    opponent_b "It looks like you two are out of things to take off, which means we've won!"
                    $ the_group.redraw_person(opponent_a)
                    opponent_a "You gave it a good try though."

                else:
                    # She's naked but you aren't, so you keep playing.
                    "[partner.title] looks at you."
                    partner "Come on [partner.mc_title], you're keeping us in the game right now."
                pass #TODO: Game ends, she's naked

            if still_playing: # Shirt, pants, socks, underwear
                if player_losses == 1: #Take off your shirt.
                    "You grab the bottom of your shirt and pull it over your head in a single movement."
                    $ the_group.redraw_person(the_aunt)
                    the_aunt "Looking good [the_aunt.mc_title]. Have you been working out?"
                elif player_losses == 2: # Take off your pants
                    mc.name "I guess this is next..."
                    "You stand up and undo the zipper on your jeans."
                    $ the_group.redraw_person(the_mom)
                    if the_mom.effective_sluttiness() < 40:
                        the_mom "Oh lord, [the_mom.mc_title]..."
                        "[the_mom.title] blushes and looks away as you pull them down."
                    else:
                        the_mom "[the_mom.mc_title]..."
                        "[the_mom.title] blushes, but doesn't take her eyes off of you as you pull them down."
                    "You kick your pants clear of your ankles and sit back down, wearing nothing but your socks and a set of underwear that only highlights your bulge."

                elif player_losses == 3: #Take off your socks (totally cheating, but girls have more pieces of clothing on average!)
                    $ the_group.redraw_person(opponent_b)
                    opponent_b "Now this is getting interesting. Come on [opponent_b.mc_title]."
                    "You shrug and reach down to your feet, quickly pulling off your socks and throwing them to the side."
                    opponent_b "Oh, come on. Is that all?"
                    mc.name "What? Were you hoping to see something else?"
                    opponent_b "I... Never mind."
                    mc.name "Win another round and maybe you'll get what you want."

                elif player_losses == 4:
                    "All eyes are fixed on you as you stand up once again, with nothing else to remove but your tight boxers."
                    "The game already has you excited, and your cock is straining against the fabric."
                    $ the_group.redraw_person(the_mom)
                    if the_mom.effective_sluttiness() < 40:
                        the_mom "I think we've all had enough fun, right? You can stop [the_mom.mc_title]."
                        $ the_group.redraw_person(the_aunt)
                        the_aunt "Oh come on, don't be such a prude. This is the whole point of the game!"
                        $ the_group.redraw_person(the_mom)
                        "[the_mom.title] leans closer to her sister and half-whispers."
                        the_mom "[the_aunt.title], he's clearly... excited. Isn't this going a little too far?"
                        $ the_aunt.redraw_person(the_aunt)
                        the_aunt "You're worrying way too much. Go ahead [the_aunt.mc_title], take it off!"
                    else:
                        the_mom "No need to be embarrassed [the_mom.mc_title], we're all family here."
                        the_mom "It's just some good natured fun. Right [the_aunt.title]?"
                        $ the_group.redraw_person(the_aunt)
                        the_aunt "Yeah. Go ahead, take it off!"

                    "You slip a thumb under your underwear waistband and start to pull them down."
                    "All of the girls watch with keen attention as your hard cock finally slips free of your boxers."
                    #TODO: Maybe only have this dialogue trigger the first time.
                    the_aunt "You have a nice looking cock [the_aunt.mc_title]." #TODO: Add a way to keep track of how much the various family members know about _each others_ taboos.
                    $ the_group.redraw_person(the_mom)
                    the_mom "[the_aunt.title]!"
                    $ the_group.redraw_person(the_sister)
                    the_sister "Oh my god..."
                    "[the_sister.possessive_title] shrinks down in her chair, as if trying to hide from the conversation entirely."
                    $ the_group.redraw_person(the_aunt)
                    "[the_aunt.possessive_title] just shrugs."
                    the_aunt "What? It's true, and men just don't get complemented enough these days."
                    the_aunt "It's good for his mental health to hear stuff like this."
                    $ the_group.redraw_person(the_mom)
                    the_mom "You shouldn't be commenting on my son's... penis. Especially not in front of me!"
                    mc.name "What's wrong with my penis [the_mom.title]?"
                    the_mom "Oh! Nothing is wrong with it sweetheart, it's very attractive."
                    $ the_group.redraw_person(the_aunt)
                    the_aunt "And a great size."
                    $ the_group.redraw_person(the_mom)
                    the_mom "[the_aunt.title], please... It is a very impressive size [the_mom.mc_title]."
                    "Her gaze lingers on your cock for an extra second before clears her throat and looks away."
                    the_mom "Now... Can you please sit down so we can continue the game?"
                    mc.name "Yeah, of course."

                    $ partner.change_slut_temp(2)
                    $ opponent_a.change_slut_temp(2)
                    $ opponent_b.change_slut_temp(2)

                    "You sit down, leaning back to give [opponent_a.title] and [opponent_b.title] a good look at you if they want it."

                else: # You're already naked
                    mc.name "Good thing you dressed up today [partner.title], you're the only reason we're still in the game."
                    #TODO: Extra stuff for being hard in front of them.
                    pass




        if round_count > max_rounds and still_playing:
            $ still_playing = False
            $ the_group.redraw_person(the_aunt)
            the_aunt "I hate to be a stick in the mud, but I'm going to have to get ready to head home."
            the_aunt "It's getting late, and I have to catch a cab."


        $ round_count += 1
    return

label card_round_description(the_mom, the_aunt, the_sister, partner, round_count):
    # Describes a technical round of cards and picks a winner (returns True if player).
    $ opponents = [the_mom, the_aunt, the_sister]
    $ opponents.remove(partner)
    $ opponent_a = opponents[0]
    $ opponent_b = opponents[1]

    "The cards are dealt. You look at your hand and take a moment to formulate a plan."

    $ opponents_int = 0
    python:
        for opp in opponents:
            opponents_int += opp.int

    $ team_int = mc.int + partner.int
    $ win_chance = 50 + ((team_int - opponents_int))*10
    if win_chance > 90:
        $ win_chance = 90 #Cap this so there's always some chance of failing
    $ win_roll = renpy.random.randint(0,100)
    if win_roll < win_chance: #Player wins
        $ player_win = True
        if win_chance - win_roll >= 50: #Blowout win
            "You see a smooth line of play, and do your best to signal your plans to [partner.title]."
            "Card by card you lay down your hand, and, with the timely help of [partner.possessive_title], win the round."
        elif win_chance - win_roll <= 20: #Fair match
            "You think you see a good line of play, and do your best to signal your plans to [partner.title]."
            "It's a tough round, but with help from [partner.possessive_title] you're able to sweep up enough points to win."
        else: #Barely won
            "You have a poor hand, but [partner.title] is giving you signs that her hand is strong."
            "It's a struggle, but [partner.possessive_title] manages to grab the very last point and win you the round."
    else:
        $ player_win = False
        if win_roll - win_chance >= 50: # Blowout loss
            "Your cards are terrible, and when you glance at [partner.title] she doesn't seem much more confident."
            "From the first card it's clear that you're doomed. [opponent_a.possessive_title] and [opponent_b.possessive_title] wipe the floor with you this round."
        elif win_roll - win_chance >= 20: # Fair loss
            "Your hand is weak, and as the cards start to fall it's clear that [partner.possessive_title] has an even worse hand than you."
            "It doesn't take long for [opponent_a.possessive_title] and [opponent_b.possessive_title] to win the round."
        else:  #Barely lost
            "Your hand looks strong, but as the cards start to fall you see that [partner.possessive_title] has a much weaker set of cards."
            "It's a close round, but by working together [opponent_a.possessive_title] and [opponent_b.possessive_title] are beat you and secure the win."

    return player_win

label cards_winner_reward(the_mom, the_aunt, the_sister, partner):
    #TODO: If you win the game of cards what is your final reward (TODO: Decide if this is a bit we want to have).
    pass

init -1 python:
    def euchre_strip_description(person, the_item, the_group):
        test_outfit = person.outfit.get_copy()
        test_outfit.remove_clothing(the_item)
        if test_outfit.tits_visible() and not person.outfit.tits_visible():
            if person.has_taboo("bare_tits"):
                renpy.say("", person.title + " glances around the table nervously.")
                renpy.say(person, "Maybe we should call it here?")
                renpy.say(mc.name, "Relax " + person.title + ", it's just a game! Come on, get those tits out for us.")
                renpy.say("", person.possessive_title + " hesitates, and the other girls start to cheer her on.")
                renpy.say(person, "Okay, okay...")

            the_group.draw_animated_removal(person, make_primary = False, the_clothing = the_item)
            if person.has_large_tits(): #Bazongas
                renpy.say("", person.title + " pulls off her " + the_item.display_name + ". Her large breasts jiggle briefly as they're released.")
            else: #Peepers
                renpy.say("", person.title + " pulls off her " + the_item.display_name + ", setting her tits free.")

            if person.has_taboo("bare_tits"):
                renpy.say("", person.title + " tries to keep her breasts covered with her hands, cheeks red.")
                person.break_taboo("bare_tits")

        elif test_outfit.vagina_visible() and not person.outfit.vagina_visible():
            if person.has_taboo("bare_pussy"):
                renpy.say("", person.title + " starts to move her " + the_item.display_name + ", but hesitates.")
                renpy.say(person, "Maybe we've taken this far enough...")
                renpy.say(mc.name, "Come on " + person.title + ", you can't quit now. We're all family here, nobody cares.")
                renpy.say("", "The rest of the table cheers her on. She takes a deep breath and gathers up her courage.")
            the_group.draw_animated_removal(person, make_primary = False, the_clothing = the_item)
            renpy.say("", person.title + " pulls her " + the_item.display_name + " down, peeling them away from her pussy.") # We should probably check if they're actually underwear, but I'm happy enough with this.

            if person.has_taboo("bare_pussy"):
                renpy.say("", the_item.display_name + " off, " + person.title + " sits back down quickly, blushing a fierce red.")
                person.break_taboo("bare_pussy")

        elif person.has_taboo("underwear_nudity") and test_outfit.underwear_visible() and not person.outfit.underwear_visible():
            renpy.say("", person.title + " glances nervously around the table.")
            renpy.say(person, "You don't really want me to take off my " + the_item.display_name + ", do you? I'll just have my underwear on...")
            renpy.say(mc.name, "Come on " + person.title + ", that's the whole point of the game! Nobody cares about you just wearing your underwear.")
            renpy.say("","She bites her lip as she considers it, then takes a deep breath.")
            the_group.draw_animated_removal(person, make_primary = False, the_clothing = the_item)
            renpy.say("", person.title + " pulls off her " + the_item.display_name + " and drops it beside her chair.")
            renpy.say(person, "There, I did it.")
            person.break_taboo("underwear_nudity")

        else: #She's just stripping, and it's not really important
            the_group.draw_animated_removal(person, make_primary = False, the_clothing = the_item)
            renpy.say("", person.title + " takes her " + the_item.display_name + " off, putting it down beside her chair.")
            pass



        #TODO: See about streamlining that by rolling it all into a single strip based description thing (we're doing a lot of strip dialogue lately)

        person.update_outfit_taboos() #Make sure we update all taboos, in case two were broken at once.
        return #TODO: Have this return something special so we can tell if any of the girls should comment.
