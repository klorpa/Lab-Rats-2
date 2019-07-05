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
        if the_person not in aunt_apartment.people:
            return False
        elif time_of_day < 3:
            return "Too early for drinks."
        elif time_of_day > 3:
            return "Too late for drinks."
        else:
            return True


###AUNT ACTION LABELS###
label aunt_intro_label():
    #NOTE: Doesn't technically countain the aunt, but intoduces the concept of her when she appears the next day
    $ renpy.show(bedroom.name,what=bedroom.background_image)
    mom.char "Hey [mom.mc_title], do you have a moment?"
    $ mom.draw_person()
    "[mom.possessive_title] cracks your door open and leans in."
    mc.name "Sure [mom.title], what's up?"
    mom.char "You remember your aunt [aunt.title], right? Well, she's been having a rough time with her husband lately and they're separating."
    "You nod and listen. [aunt.possessive_title] never spent much time visiting when you were a kid and it's been years since you've seen her at all."
    mom.char "It seems like he's going to be keeping the house, so she's going to be staying with us for a few days while she finds a new place to live."
    mom.char "She'll be bringing your cousin [cousin.title] too. You two haven't seen each other since you were kids, have you?"
    mc.name "No, it's been a long time."
    mom.char "I know it's going to be a little tight here while we sort this out, but she's family and I need to be there for her."
    mc.name "I understand [mom.title], I'll help out however I can."
    $ mom.change_happiness(5)
    mom.char "That's so nice to hear [mom.mc_title], thank you. [cousin.possessive_title] will be sharing [lily.title]'s room with her and [aunt.title] will be on the couch in the living room."
    mom.char "They're going to be here in the morning. If you have a few minutes could you help me pull out some sheets and get their beds made?"
    menu:
        "Help [mom.possessive_title] set up.":
            mc.name "Sure, let's go get it done."
            $ mom.change_happiness(3)
            $ mom.change_love(2)
            "You and [mom.possessive_title] go to the laundry room and gather up extra pillows, sheets, and towels for your house guests."
            "You fold out the couch in the living room and dress it up as a temporary bed for your aunt."
            "Next, you drag an air mattress into [lily.title]'s room and start inflating it."
            $ lily.draw_person()
            lily.char "Mom, I don't even know [cousin.title]. Can't she have [lily.mc_title]'s room and he can sleep somewhere else?"
            $ mom.draw_person()
            mom.char "Your brother has to worry about his work. It's just for a couple of days, I'm sure you and [cousin.title] will get along just fine."
            "[lily.possessive_title] pouts but stops complaining. You and [mom.possessive_title] finish setting up the air mattress."
            mom.char "Alright, I think that's everything. Thank you so much for the help [mom.mc_title], I know it's late and you probably want to get to bed."
            "[mom.possessive_title] gives you a hug and kiss on the forehead. You head off to your room and go to sleep."



        "Make [lily.possessive_title] do it.":
            mc.name "Sorry [mom.title], I've got an early morning tomorrow and really need to get to bed. I think [lily.title]'s free though."
            $ lily.change_obedience(2)
            $ lily.change_love(-1)
            mom.char "Of course [mom.mc_title], I'm sure your sister won't mind helping. You get a good nights sleep."
            "[mom.possessive_title] gives you one last smile as she closes your door. You hear her talking to your sister outside while you get ready for bed."

    $ renpy.scene("Active")
    $ aunt_intro_phase_two = Action("Aunt introduction phase two", aunt_intro_phase_two_requirement, "aunt_intro_phase_two_label")
    $ mc.business.mandatory_morning_crises_list.append(aunt_intro_phase_two) #Aunt and cousin will be visiting tomorrow in the morning
    return

label aunt_intro_phase_two_label():
    #They show up at your house in the morning. Quick introductions with everyone.
    "In the morning [mom.possessive_title] wakes you up early with a knock on your door."
    mom.char "[mom.mc_title], I just got a call, your aunt and cousin are on their way over. Get ready so you can help move their stuff inside."
    $ renpy.show(kitchen.name,what=kitchen.background_image)
    "You get up, get dressed, and head to the kitchen to have some breakfast. [mom.possessive_title] paces around the house nervously, looking for things to tidy."
    $ renpy.show(hall.name,what=hall.background_image)
    "Finally the doorbell rings and she rushes to the door. You and [lily.title] join her in the front hall as she greets your guests."
    $ mom.draw_person()
    mom.char "[aunt.name], I'm so glad you made it!"
    $ aunt.draw_person()
    aunt.char "[mom.name]!"
    "[aunt.title] lets out an excited, high pitched yell and rushes forward to hug [mom.possessive_title]."
    aunt.char "Thank you so much for taking us in. It means the world to me and [cousin.title]."
    $ cousin.draw_person()
    "[mom.possessive_title] breaks the hug and out the door. Your cousin, [cousin.title], is sitting on a suitcase and idly scrolling through her phone."
    mom.char "How are you doing [cousin.title]? Holding up okay?"
    "She shrugs and doesn't take her eyes off her phone."
    cousin.char "Eh. Fine..."
    $ aunt.draw_person()
    aunt.char "She's thrilled, really. Now who are these two little rascals I see?"
    "[aunt.possessive_title] steps into the house and throws her arms wide, pulling you and your sister in to a hug."
    aunt.char "I mean, it must be [mc.name] and [lily.title], but you're both so much bigger than I remember!"
    "She hugs you both tight then lets go. [aunt.title] looks at you in particular and laughs."
    aunt.char "I remember when you were just a little baby, and now you're a full grown man. Oh no, I'm showing my age, aren't I. Hahaha."
    "She laughs and turns back to grab her things. [cousin.title] sighs loudly outside and rolls her eyes."
    aunt.char "Now [mom.name], where should I bring my things?"
    $ mom.draw_person()
    mom.char "Just follow me, I'll show you around. We got everything set up as soon as we heard the news."
    "[mom.possessive_title] leads [aunt.possessive_title] into the house. When they're gone [lily.possessive_title] takes a step towards [cousin.title]."
    $ lily.draw_person()
    lily.char "Hi [cousin.title], it's nice to see you again. I don't think we've talked since we were little kids."
    $ cousin.draw_person()
    cousin.char "Yep..."
    "There's a long period of awkward silence."
    $ lily.draw_person()
    lily.char "... Right. Well I'm sure we'll get along while you're staying with me."
    "[aunt.possessive_title] calls from further inside the house."
    aunt.char "[cousin.name], sweetheart, you should come see your room! I'm sure [lily.name] and [mc.name] will help bring your stuff in."
    $ cousin.draw_person()
    "[cousin.possessive_title] gets up from her suitcase seat, picks up her smallest bag, and walks inside."
    cousin.char "Thanks for the help."
    $ lily.draw_person()
    "[lily.title] glances at you and rolls her eyes dramatically. The two of you grab more luggage and start hauling it inside."
    "After a few minutes all of the suitcases have been moved to where they need to go."
    $ aunt.draw_person()
    aunt.char "Thank you two so much, you're such sweethearts. Here's something for all your hard work."
    $ aunt.change_love(2)
    $ mc.business.funds += 20
    "[aunt.possessive_title] finds her purse, pulls out her wallet, and hands you and [lily.possessive_title] $20."
    aunt.char "Now I think your mother wanted to talk with me. I'm sure you both have busy days, so don't let me keep you!"
    #Their temporary homes are at your place. Later we will restore them to their normal homes.
    python:
        aunt.home.move_person(aunt, hall)
        aunt.home = hall
        cousin.home.move_person(cousin,lily_bedroom)
        cousin.home = lily_bedroom
        for i in range(0,5):
            aunt.schedule[i] = aunt.home #Hide them in their bedroom off the map until they're ready.
            cousin.schedule[i] = cousin.home

        #Your aunt is a homebody, but your cousin goes wandering during the day (Eventually to be repalced with going to class sometimes.)
        cousin.schedule[1] = None
        cousin.schedule[2] = None
        cousin.schedule[3] = None

    $ aunt_intro_phase_three = Action("aunt_intro_phase_three", aunt_intro_phase_three_requirement, "aunt_intro_phase_three_label", requirement_args = day + renpy.random.randint(6,10))
    $ mc.business.mandatory_morning_crises_list.append(aunt_intro_phase_three)

    $ cousin_intro_phase_one = Action("cousin_intro_phase_one", cousin_intro_phase_one_requirement, "cousin_intro_phase_one_label", requirement_args = day + renpy.random.randint(2,5))
    $ mc.business.mandatory_crises_list.append(cousin_intro_phase_one)
    $ renpy.scene("Active")
    return

label aunt_intro_phase_three_label():
    #Your aunt lets you know that she has an apartment lined up, and if you have free time would appreciate some help moving in.
    "There's a quick knock at your door."
    aunt.char "[aunt.mc_title], I hope you're decent because I'm coming in!"
    $ aunt.draw_person(emotion = "happy")
    "[aunt.possessive_title] throws your bedroom door open and steps in before you have a chance to answer."
    mc.name "Morning [aunt.title], uh... What's up?"
    aunt.char "Earlier today I got a call with some fantastic news. My realtor found this beautiful little apartment downtown for me and [cousin.title]!"
    aunt.char "That means in a few days we'll be out of your hair and your house can go back to normal."
    mc.name "It was nice having you around [aunt.title], but I'm happy you're getting back on your feet. Things will be back to normal for you soon too."
    aunt.char "I hope so. I actually had one {i}tiny{/i} little favour to ask while I was here..."
    mc.name "What is it?"
    aunt.char "Well now that it's just me and [cousin.title], we don't have anyone to help us with the heavy lifting when we move in."
    aunt.char "We'll be moving our things starting tomorrow, if you had any free time to help us it would mean the world to me."
    mc.name "I'll see if I have some spare time in my schedule and come to you if I do."
    $ aunt.draw_person(position = "sitting", emotion = "happy")
    $ aunt.change_happiness(8)
    "[aunt.possessive_title] sits on the side of your bed, puts a hand on your leg, and squeezes it gently."
    aunt.char "I'm so lucky to have such a wonderful nephew, you know that? If only I had married a man like you instead of..."
    aunt.char "Well, never mind that. Thank you."
    $ aunt.change_love(3)
    "She leans in, gives you a warm, familial hug, and then leaves you to get on with your day."
    $ renpy.scene("Active")
    $ aunt.event_triggers_dict["moving_apartment"] = 0 #If it's a number it's the number of times you've helped her move. If it doesn't exist or is negative the event isn't enabled

    $ moving_finished_action = Action("Moving finished", aunt_intro_phase_five_requirement, "aunt_intro_phase_final_label", requirement_args = day + 7)
    $ mc.business.mandatory_morning_crises_list.append(moving_finished_action)

    return

label aunt_intro_moving_apartment_label(the_person):
    #You help her move in, with different focuses each time you do it.
    $ aunt.draw_person()
    mc.name "[aunt.title], I've got a few free hours. Would you like some help moving your things?"
    aunt.char "Oh [aunt.mc_title], your help would be amazing. Here, let's go look at what we have to move."
    if aunt.event_triggers_dict.get("moving_apartment") == 0:
        #You help them and get a brief overview of what they're bringing in the future
        "You follow [aunt.possessive_title] to the stack of boxes, luggage, and furnature that are being stored in the garage."
        aunt.char "With your help I think we can manage this in four trips. Today we'll rent a truck and move all of the big stuff in."
        aunt.char "Once that's done we can move all of my things into my room, then we move [cousin.title]'s stuff."
        aunt.char "And then last we move in the kitchen things and get the place all tidied up. Sound good?"
        mc.name "Yeah, let's get started I guess."
        $ aunt.change_happiness(5)
        $ aunt.change_love(2)
        aunt.char "Thank you so much! I'll go rent that truck, you just stay here and I'll be back in a little bit."
        $ renpy.scene("Active")
        "[aunt.title] gets in her car and drives off. You organize the boxes so they'll be easier to load when she gets back."
        cousin.char "What're you doing out here?"
        "You're startled by [cousin.possessive_title]'s voice. You spin around and find her leaning against the house door frame."
        $ cousin.draw_person()
        mc.name "Your mom's going to rent a truck. I'm helping you guys move your stuff over to your new place."
        cousin.char "Why?"
        menu:
            "Because it's a nice thing to do.":
                mc.name "Because it's a nice thing to do, that's all."

            "Because I want to impress her.":
                mc.name "Because I want to make a good impression. I want her to like me."

            "Because I'm hoping she'll pay me.":
                mc.name "Because I'm hoping when we're done she'll pay me for the help."

        cousin.char "That's dumb, but whatever."
        mc.name "Yeah, whatever. [aunt.title] will be back soon, do you want to give me a hand?"
        cousin.char "Not really. Be careful with my stuff."
        $ cousin.draw_person(position = "walking_away")
        "With that she turns around and goes back inside."
        $ renpy.scene("Active")
        mc.name "You're welcome..."
        "A few minutes later [aunt.title] pulls up in a rented pickup truck. You load up the back with furniture and boxes, then get in the passenger seat."
        aunt.char "Okay, let's get going! I don't know what I'd do without a big strong man like you to lift things for me. I'd be helpless!"
        $ aunt.change_love(1)
        $ renpy.show(downtown.name,what=downtown.background_image)
        "It doesn't take long to drive to [aunt.title]'s new apartment. She parks out front and you grab a box to bring up with you."
        $ renpy.show(aunt_apartment.name, what=aunt_apartment.background_image)
        "The apartment is small but tidy, with two bedrooms and a combined living area and kitchen. [aunt.title] gestures to one of the bedrooms."
        aunt.char "My room will be in there, and the other one will be [cousin.title]'s room. You can put that box down and go get another, I'll start unpacking."
        "The next couple of hours are spent unloading the truck and bringing everything up to [aunt.possessive_title]."
        "When you're done [aunt.title] returns the truck and drives you both home. When you get out of the car she gives you a tight hug."
        $ aunt.change_love(3)
        $ aunt.change_happiness(5)
        aunt.char "You're my hero [aunt.mc_title]. Come see me if you have any more spare time and we can move the rest of this over."
        "She breaks the hug and smiles."
        aunt.char "Now I'm going to go see if I can use your mothers shower!"
        $ renpy.scene("Active")



    elif aunt.event_triggers_dict.get("moving_apartment") == 1:
        #You help move your aunt's wardrobe and get a chance to dig through her underwear
        "You and [aunt.title] head to the garage and look over the stuff that still needs to be moved."
        aunt.char "I think we can my things over today. If I need something I can always borrow it from your mother."
        aunt.char "She always hated when I borrowed her clothes when we were younger. She said I stretched out her tops."
        aunt.char "I think she was just jelious I got the nice tits."
        "[aunt.possessive_title] laughs and blushes."
        $ aunt.change_slut_temp(1)
        aunt.char "Sorry, I shouldn't be talking about your mom's chest like that. It's different when you're sisters, you know?"
        mc.name "Oh yeah, I know what you mean."
        aunt.char "Anyways, we have work to get done. I think we can fit all of my clothes in the back of my car, so we don't need a truck today."
        aunt.char "Let's load it up and we can bring it all over."
        "You and [aunt.title] load up her hatchback with boxes filled with clothes. Once the car is loaded to capacity you get in and drive to her new apartment."
        $ renpy.show(aunt_apartment.name, what=aunt_apartment.background_image)
        "When you arrive you start to shuttle boxes up to [aunt.possessive_title]'s bedroom. [aunt.title] is kept busy unpacking the boxes and putting everything away."
        $ aunt.draw_person(position = "sitting")
        "After some hard work the car is empty and the last box is in [aunt.title]'s room."
        aunt.char "Thank you for all the help [aunt.mc_title], It'll just take me a few minutes to get the rest of this put away."
        $ aunt.change_happiness(5)
        $ aunt.change_love(1)
        menu:
            "Offer to help.":
                mc.name "Here, let me help with that. Just tell me where to put things."
                $ aunt.change_love(1)
                aunt.char "My sister raised such a perfect gentleman! Here, this goes in the top drawer over there."
                "You clear out a couple of boxes, putting away shirts, skirts, and pants for [aunt.title]. [aunt.possessive_title] reaches for the last box, marked \"Private\" then hesitates."
                aunt.char "I can go through this one myself, it's all my underwear and that's probably the last thing you want to be digging through."
                mc.name "We're both adults, it's no big deal."
                "[aunt.possessive_title] shrugs and opens the box and starts to sort through it. She hands you a pile of colourful panties."
                aunt.char "Okay, put these in that drawer on the left..."
                "You slide the garments into their drawer. Next [aunt.title] hands you a stack of lacey bras and small thongs."
                aunt.char "This goes to the side... and then... Oh my."
                "She closes the box and looks away, blushing."
                aunt.char "This is so embarrassing [aunt.mc_title], I'll just finish this up myself later."
                mc.name "Come on, we're almost done."
                $ aunt.change_slut_temp(1)
                aunt.char "Don't tell my sister about this."
                "[aunt.title] pulls out the last few pieces of underwear from the box: a collection of g-strings and nippleless bras."
                mc.name "Is that all? I thought you had something to be embarrassed about."
                "You pick the tiniest g-string and hold it up against your waist. [aunt.title] laughs and snatches it from your hands."
                aunt.char "Stop that! I bought those for my husband, not that he ever cared what I wore. He was more interested what his secretary {i}wasn't{/i} wearing."
                "She throws the underwear back at you."
                $ aunt.change_slut_temp(1)
                aunt.char "You know what, keep all this stuff near the front. Maybe I'll get a chance to wear it for someone that'll appreciate it."
                "You put away [aunt.title]'s sexy underwear and finish your work for the day."

            "Take a break.":
                mc.name "Alright, I'm going to go get a glass of water and catch my breath."
                aunt.char "Go ahead, you've certainly earned it!"
                $ aunt.change_obedience(1)
                $ renpy.scene("Active")
                "You get a glass of water and sit down on the new sofa in the living room."
                "After half an hour [aunt.possessive_title] comes out and dusts off her hands."


        aunt.char "Alright, that's everything for today [aunt.mc_title]. Let's get you home."
        $ renpy.scene("Active")

    elif aunt.event_triggers_dict.get("moving_apartment") == 2:
        #You help move your cousin's wardrobe and get a chance to dig through her underwear. She catches you and taunts you "You little perv, you'll never get to see me wear something like that." kind of stuff.
        "You head to the garage and look at the dwindling pile of boxes that need to be moved."
        aunt.char "I think we can move [cousin.title]'s things today. I'll go get her."
        $ renpy.scene("Active")
        "[aunt.possessive_title] is gone for a few minutes before coming back with [cousin.title] in tow."
        $ aunt.draw_person()
        aunt.char "Let's get this show on the road! I know [cousin.title] is excited to a room to herself again, aren't you sweetheart."
        $ cousin.draw_person()
        cousin.char "I'm not your sweetheart Mom. Let's just get this over with."
        "She sulks over to [aunt.title]'s car and gets in the passanger seat."
        $ aunt.draw_person()
        aunt.char "Sorry about that [aunt.mc_title], she doesn't always play nice with others and this whole move has been tough on her. Could you help me load up the car?"
        mc.name "Sure. Just tell me where to put things."
        "You fill up [aunt.title]'s hatchback and get in the back seat with the last box sitting on your lap. [cousin.title] puts on headphones and ignores both of you."
        $ renpy.show(cousin_bedroom.name, what=cousin_bedroom.background_image)
        "When you arrive you start to shuttle everything up to [cousin.possessive_title]'s room."
        $ cousin.draw_person(position = "sitting")
        "[cousin.title] sits down on her bed and gets her phone out. She looks up occasionally to tell you where to put boxes down."
        mc.name "You could help, you know."
        cousin.char "I could, but I don't want to. You're doing fine."
        "[aunt.possessive_title] pokes her head into the room."
        aunt.char "[cousin.title], sweety, we should go downstairs and get an extra key for you."
        "[cousin.title] rolls her eyes dramatically, then gets up and follows her mother. She stops just before leaving and looks back at you."
        cousin.char "Don't touch my stuff."
        $ renpy.scene("Active")
        menu:
            "Touch her stuff.":
                "She's not the boss of you. You wait a couple of minutes then start snooping around."
                "Most of the boxes are clearly labeled, but you find one that just says \"Keep Out!\" on the side."
                "You open the box and find it filled with all of [cousin.title]'s underwear, all black, purple, or blue."
                "You dig deeper, past the large cupped bras she needs for her big tits. She has a handful of g-strings, fishnet stockings, and a garter belt near the bottom."
                "You think you feel something rigid at the bottom, but your search is interrupted by the front door lock clicking open."
                "You rush to get [cousin.possessive_title]'s underwear back in order. You slam the box shut and sit down on her bed, trying to look nonchalant."
                $ cousin.draw_person()
                cousin.char "You didn't paw through my things, did you?"
                mc.name "Of course not, you told me not to."
                "She glares at you, then at her box of underwear, then at you again. She shakes her head."
                $ cousin.change_obedience(-3)
                cousin.char "Pervert."
                mc.name "Fine, I was curious. I didn't know what was in there."
                $ cousin.change_slut_temp(2)
                cousin.char "Whatever. It's not like you'll ever get to see me in it. I bet you'd like to though. I bet you're weird like that."
                "[cousin.title] gives you a strange, mischievous smile."
                cousin.char "Do you want to see me try some of it on? I won't tell anyone."
                menu:
                    "Yes.":
                        "You nod your head. [cousin.title] laughs."
                        $ cousin.change_happiness(10)
                        $ cousin.change_slut_temp(1)
                        cousin.char "Ha! You wish you pervert. Now get out of here before I tell my mom."

                    "No.":
                        mc.name "What? No, you're being weird now."
                        "She shrugs."
                        cousin.char "Your loss. You'll just have to imagine it now. Now get out of here before I tell my mom you're digging through my things."

                "You get up off of [cousin.title]'s bed and leave."


            "Don't touch her stuff.":
                "Not wanting to bring down [cousin.title]'s wrath, you focus on bringing up the rest of the boxes from the car."
                "Twenty minutes later, [aunt.title] and [cousin.title] come back just after you're done moving the last box."
                $ cousin.draw_person()
                cousin.char "You didn't paw through my things, did you?"
                mc.name "Of course not, you told me not to."
                $ cousin.change_obedience(-3)
                $ cousin.change_happiness(2)
                cousin.char "Good."

        "With your work for the day done the three of you drive back home. [aunt.title] gives you a big hug when you get out of the car."
        $ aunt.change_love(1)
        aunt.char "Thank you again for all the help."



    elif aunt.event_triggers_dict.get("moving_apartment") == 3:
        #You help them move their kitcehn stuff in. Your aunt gets dirty/sweaty and wants to chance now that her clothes are here. She asks you to wait around whlie hse takes a shower, then
        #the landlord shows up and needs some documents from her, so you have to come into her bathroom and get a chance to see her naked/just in her underwear or something.
        #mc.name "Okay, I'm going to get a drink and catch my breath."
        #$ renpy.scene("Active")
        #"She smiles at you and nods. You sit down on her new couch in her living room and relax for a bit."
        #"A minute later [aunt.title]'s phone rings. You catch half of the conversation from the living room."
        #aunt.char "Hello? Yes, that's me. I'm actually in the building right now, I can come to the office right away. Okay. See you soon."
        #"[aunt.possessive_title] comes out and heads for the door."
        #6aunt.char "I just need to dip down to the

        "You head to the garage and look at the small pile of boxes left."
        aunt.char "I think it's just the kitchen stuff left. Let's get this packed in the car and we'll have everything moved over!"
        "You fill up [aunt.possessive_title]'s hatchback and head for her apartment."
        $ renpy.show(aunt_apartment.name, what=aunt_apartment.background_image)
        "You and [aunt.possessive_title] get to work shifting boxes upstairs."
        "After the first couple boxes are upstairs she starts to unpack them while you keep unloading the car."
        "It takes a couple of hours to get everything moved and unpacked. You and [aunt.title] are happy when the last box is emptied and you're finished with the move."
        $ aunt.change_happiness(5)
        aunt.char "[aunt.mc_title], I think that's everything! I think we should order a pizza and celebrate a little, what do you say?"
        mc.name "That sounds good to me. I'm starving."
        $ aunt.change_love(1)
        aunt.char "I'm sure you are, you've been doing all the heavy lifting for me! You're my big strong man, coming in to rescue me."
        "She gives you a hug, then grabs her phone and finds a local pizza place that delivers. She places your order."
        aunt.char "They said it may take a little while. All this hard work got me all sweaty, I'm going to go take a shower. Back in a bit!"
        $ renpy.scene("Active")
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
                aunt.char "Oh, is that here already? I'm sorry [aunt.mc_title], I was going to pay for that."
                mc.name "Don't worry about it, it's no big deal."
                $ aunt.change_love(1)
                aunt.char "Well thank you. Get me a slice of that, I'm starving now too!"

            "Pay for the pizza.\n-$25 (disabled)" if mc.business.funds < 25:
                pass

            "Get the money from [aunt.title].":
                mc.name "Thanks, I just have to get the money. One sec."
                "The pizza guy nods and hangs out in the doorway while you head to the bathroom door and knock."
                aunt.char "Hmm? What is it?"
                mc.name "The pizza guy's here."
                aunt.char "Oh! I didn't think he would be here so soon! Just, uh... just come in and get it, it's in my purse."
                "You open the door to the bathroom. [aunt.possessive_title]'s shower has a clear glass door, not hiding anything. She turns away as you come in."
                $ aunt.outfit = default_wardrobe.get_outfit_with_name("Nude 1")
                $ aunt.draw_person(position = "back_peek")
                $ aunt.change_slut_temp(2)
                aunt.char "It's right over there, just grab it and go."
                "She nods her head towards her purse. You hurry inside, grab it, then retreat. You pull the cash out of her wallet and give it to the pizza guy."
                "Pizza Guy" "Thanks man, enjoy."
                "You take the pizza into the kitchen. A couple of minutes later [aunt.title] comes out of the bathroom."
                aunt.char "I'm so sorry about that, I know must be embarrassing to see your aunt naked."
                mc.name "It's fine. We're family, right? We're suppose to be comfortable with each other."
                aunt.char "I guess you're right. Anyways, let me have some of that pizza, I'm starving now too!"

        "You enjoy your lunch together then get in [aunt.title]'s car and head home. With all of their stuff moved [aunt.title] and [cousin.title] should be all ready to move out."

    $ aunt.event_triggers_dict["moving_apartment"] += 1
    $ aunt.event_triggers_dict["day_of_last_move"] = day
    call advance_time() from _call_advance_time_16
    return


label aunt_intro_phase_final_label():
    #You have finished moving all of their stuff over so your aunt and cousin can move out of your house.

    "When you get up for breakfast you find [aunt.title] and [mom.title] in the kitchen, both awake earlier than normal."
    $ aunt.draw_person(position = "sitting")
    aunt.char "Good morning [aunt.mc_title]."
    "She smiles at you warmly and sips coffee from a mug. [mom.possessive_title] is drinking a cup of tea across the table from her."
    mc.name "Morning. You two are up early."
    aunt.char "All the paperwork for my new apartment has been finished, so me and [cousin.title] will be moving out today."
    $ mom.draw_person(position = "sitting")
    mom.char "We're just finishing our drinks then they'll be heading out."
    $ aunt.draw_person(position = "sitting")
    if aunt.event_triggers_dict.get("moving_apartment") == 0:
        #Did nothing
        aunt.char "I was going to wake you up before I left, of course. You've been so busy, I barely got a chance to see you."
        $ mom.draw_person(position = "sitting")
        mom.char "You're welcome to come over and visit any time [aunt.title]. I'll make sure [mom.mc_title] takes a break to come visit his family."

    elif aunt.event_triggers_dict.get("moving_apartment") in [1,2,3]:
        #Did some stuff
        aunt.char "I was going to wake you up before I left, of course. I want to say thank you again for helping us move our things over."
        $ mom.draw_person(position = "sitting", emotion = "happy")
        $ mom.change_love(2)
        $ mom.change_happiness(5)
        mom.char "I'm glad you were able to find some time to help them out [mom.mc_title]. I'm proud of you."

    else:
        #Did everything
        aunt.char "I was going to wake you up before I left, of course. I needed to say thank you again for the huge amount of help you gave us."
        $ mom.draw_person(position = "sitting", emotion = "happy")
        $ mom.change_love(3)
        $ mom.change_happiness(8)
        mom.char "[aunt.title] has been telling me all morning how helpful you've been. I'm so proud of you [mom.mc_title].:"
        $ aunt.draw_person(position = "sitting", emotion = "happy")
        aunt.char "He was a godsend, he really was."

    $ aunt.draw_person(position = "sitting", emotion = "happy")
    aunt.char "Come on [aunt.mc_title], sit down and join us for a few minutes."
    "You join [aunt.possessive_title] and [mom.possessive_title] while they finish their drinks and chat with each other."
    "[aunt.title] certainly seems happier now than she did a week ago when she arrived."
    "When her drink is done [aunt.title] collects [cousin.possessive_title] and heads to the door. [lily.title] joins you as you say goodbye."
    $ aunt.draw_person(emotion = "happy")
    aunt.char "Thank you all for giving us a place to go. You're welcome over to visit us any time. Just drop by."
    $ cousin.draw_person()
    "[cousin.title] looks at you and shakes her head from behind her mother."
    $ mom.draw_person()
    mom.char "And you two are always welcome here. Call if you need anything."
    $ aunt.draw_person()
    aunt.char "I will. Thanks sis."
    "[mom.possessive_title] and [aunt.possessive_title] hug each other and don't let go for a long while."
    "When the moment has passed [mom.title] walks them out to the driveway, leaving you alone with [lily.possessive_title]."
    $ lily.draw_person()
    lily.char "I'm going to miss them. I think me and [cousin.title] were really getting along."
    mc.name "Really?"
    lily.char "Yeah! She may not talk much but she's a great listener. I hope she stays in touch."
    "You shrug and head back to your room to get ready for the day."

    python:
        aunt.event_triggers_dict["moving_apartment"] = -1 #Disables the event in their action list so you can't help them move out once they're already moved out.
        aunt.home = aunt_bedroom # Set their homes to the new locations
        cousin.home = cousin_bedroom

        aunt_bedroom.visible = True
        aunt_apartment.visible = True
        cousin_bedroom.visible = True

        for i in range(0,5):
            aunt.schedule[i] = aunt.home #Change their home locations.
            cousin.schedule[i] = cousin.home
        #Your aunt is a homebody, but your cousin goes wandering during the day (Eventually to be repalced with going to class sometimes.)
        aunt.schedule[2] = aunt_apartment
        aunt.schedule[3] = aunt_apartment


        cousin.schedule[1] = None
        cousin.schedule[2] = None
        cousin.schedule[3] = None

        cousin_at_house_phase_one_action = Action("Cousin changes schedule", cousin_house_phase_one_requirement, "cousin_house_phase_one_label", args = cousin, requirement_args = day+renpy.random.randint(2,5))
        mc.business.mandatory_crises_list.append(cousin_at_house_phase_one_action) #This event changes the cousin's schedule so she shows up at your house.

        cousin_at_house_phase_two_action = Action("Cousin at house", cousin_house_phase_two_requirement, "cousin_house_phase_two_label")
        cousin.on_room_enter_event_list.append(cousin_at_house_phase_two_action)

        aunt_share_drink_intro = Action("Aunt drink intro", aunt_drink_intro_requirement, "aunt_share_drink_intro_label")
        aunt.on_talk_event_list.append(aunt_share_drink_intro)
    return


label aunt_share_drink_intro_label(the_person):
    # On talk trigger after she has a certain love score (and she's moved out. Add this crisis to her lsit once she moves out)
    # She invites you over to share some drinks. You can come by in the afternoon and share a drink with her.
    the_person.char "[the_person.mc_title], I'm so happy to see you! Come here, give me a hug."
    "[the_person.possessive_title] gives you a tight hug."
    mc.name "It's good to see you too [the_person.title]."
    the_person.char "We really should get together more often, I miss seeing my cute little nephew!"
    the_person.char "Come by in the afternoon some time, you can join me for a glass of wine and we can chat."
    "She gives you a kiss on the cheek and smiles at you."
    $ the_person.change_happiness(1)
    the_person.char "Anyways, I'm sure you have other stuff you wanted to talk about!"
    $ the_person.event_triggers_dict["invited_for_drinks"] = True
    call talk_person(the_person) from _call_talk_person_6
    return

label aunt_share_drinks_label(the_person):
    # An action that is only enabled in the evening (maybe only friday nights? Only ad)
    # Aunt shares drinks with you and chats. At higher sluttiness she does things like model for you, talk about her sexual preferences, etc.
    mc.name "Do you feel like having a glass of wine and chatting? I'm sure we have a lot to catch up on."
    "[the_person.title] claps her hands together excitedly!"
    the_person.char "Yes! You go sit on the couch and I'll pour us both a glass."
    "You sit down in [the_person.possessive_title]'s tiny living room and wait. She shuffles around in the kitchen, then comes out with two glasses of red wine."
    the_person.char "There you go. Now you have to make sure that I just have one glass of this. I love it, but wine goes straight to my head."
    $ the_person.draw_person(position = "sitting")
    "She hands you a glass, sits down, and tilts her glass towards you. You clink them together."
    mc.name "Cheers!"
    the_person.char "Cheers!"
    "[the_person.possessive_title] takes a sip, then leans back on the couch. She crosses her legs and turns towards you."
    the_person.char "So what's been going on with your life? It's been so long!"
    menu:
        "Talk about work.":
            mc.name "Well, work's been keeping me busy lately..."
            "You talk to [the_person.possessive_title] about your work. She nods politely but doesn't understand most of it."
            $ the_person.change_obedience(1)
            the_person.char "It sounds like you're a very important person, doing some very important work. I'm proud of you [the_person.mc_title]"

        "Talk about girls.":
            mc.name "Well, I've been trying to meet soneone lately..."
            "You talk to [the_person.possessive_title] about your love life. She listens intently."
            $ the_person.change_slut_temp(1)
            the_person.char "I've always thought it's important to be adventurous. You might connect with someone who you wouldn't expect."

        "Talk about her.":
            mc.name "Oh, it's been pretty quiet lately actually. What about you? I know you've been through a lot."
            "You get [the_person.possessive_title] talking about herself. She tells you about her failed mariage."
            $ the_person.change_love(1)
            the_person.char "... and when I told him I knew he was plowing his secretary every day he kicked us out."
            "She takes another sip from her wine."
            the_person.char "Whew. That felt good to talk about actually."

    "[the_person.title] finishes off the last of her wine."
    the_person.char "Well that was a lovely chat [the_person.mc_title]. I won't keep you here any longer."
    menu:
        "Convince her to have another glass.":
            mc.name "It's really no trouble. I can go pour you another glass, if you'd like."
            if the_person.love >= 20: #Can be convinced
                the_person.char "Oh, I really shouldn't. It's getting a little late, you probably have important places to be..."
                mc.name "It's not late, and I don't have anywhere important to be. Come on, just relax and give me your glass."
                the_person.char "Okay, okay, you've twisted my arm. I'm not to blame for any of my actions beyond this point though!"
                "She hands you her glass and you head to the kitchen to uncork her bottle of wine."
                menu:
                    "Add a dose of serum to her wine.":
                        call give_serum(the_person) from _call_give_serum_13

                    "Leave her drink alone.":
                        pass
                "You top up your own drink while you're in the kitchen and head back to [the_person.title]. You hand over her new drink and sit down."
                the_person.char "Now, where were we..."
                "You and [the_person.possessive_title] keep talking. After her first glass she seems more relaxed, and the second one is already having it's effect."
                $ the_person.add_situational_slut("Drunk", 20, "More than a little tipsy.")
                $ decision_score = the_person.sluttiness + renpy.random.randint(0,25) #Her choice in this check is up to 25 points more slutty than she is.
                if decision_score <= 35:
                    # She talks about her ex and then falls asleep.
                    "As [the_person.title] gets deeper into her drink she starts to rant about her now ex husband."
                    the_person.char "I don't even know what he saw in that little skank... You've never seen her, but she was this flat chested little thing."
                    "She scoffs and takes another drink while you listen patiently."
                    $ the_person.change_slut_temp(2)
                    the_person.char "And youth isn't everything it's cracked up to be. It takes practice to get good at some things. I hope he enjoys shitty blowjobs. HA!"
                    "[the_person.possessive_title] puts her feet up on the couch and yawns."
                    the_person.char "Oh, this wine really has just knocked me out. I'm just going to... rest my eyes while we talk, okay?"
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
                            the_person.char "Mmm..."
                            "[the_person.possessive_title] moans softly and tilts her head to the side."
                            $ the_person.change_slut_temp(2)
                            "You fondle her big tits until she seems like she's starting to wake up. You sit back down on the couch and pretend like nothing happened."
                            the_person.char "... Hmm? Oh, did I nod off there? I'm sorry [the_person.mc_title], I think I need to have a little nap."
                            mc.name "No problem, I'll clean up our glasses and head out."
                            "She rolls over on the couch and is asleep again before you're out the door."

                        "Grope her pussy.":
                            "Seizing the opportunity, you kneel down in front of [the_person.possessive_title]."
                            if the_person.outfit.vagina_available():
                                "Her pussy out on display for you, there for the taking. You move slowly and slide your hand along her inner thigh, working upwards."
                            else:
                                $ the_clothing = the_person.outfit.get_lower_top_layer()
                                "You move slowly, sliding your hand along her inner thigh and working upwards."
                                "When you reach her waist you slide your hand inside of her [the_clothing.name]."

                            if mc.sex_skills["Foreplay"] >= 3:
                                the_person.char "Mmm..."
                                "She moans softly when your fingers make first contact with her pussy. Her hips press up gently against your hand."
                                $ the_person.change_slut_temp(3)
                                "You run your index finger gently over her clit, gently caressing it while you listen to her moan."
                                "When it starts to seem like she's waking up you retreat to your seat on the couch."

                            else:
                                "She moans sofly when you make first contact with her pussy. You start to move your hand around, feeling for her clit."
                                $ the_person.change_slut_temp(1)
                                "You're inexperienced and perhaps a little overeager. [the_person.title] starts to wake up and you make a hasty retreat to your spot on the couch."

                            the_person.char "... Hmm? Oh, did I nod off there? I'm sorry [the_person.mc_title], I think I need to have a little nap."
                            mc.name "No problem, I'll clean up our glasses and head out."
                            "She rolls over on the couch and is asleep again before you're out the door."

                elif decision_score <= 45:
                    # She talks to you about stuff she finds sexy. Reveal a sex opinion
                    "[the_person.title] talks more about herself, and it seems like being a little drunk seems to have removed any inhibitions she might have had."
                    $ her_opinion = the_person.get_random_opinion(include_known = False, include_sexy = True, include_normal = False)
                    if her_opinion:
                        $ the_person.discover_opinion(her_opinion)
                        $ opinion_string = opinion_score_to_string(her_opinion)
                        "Through her suprisingly erotic ramblings you discover that she [opinion_string] [her_opinion]."
                    else:
                        #We know everything.
                        "You don't learn anything new, but hearing [the_person.possessive_title] talk this way is certainly eye opening."

                    "She finally blushes and looks away from you."
                    $ the_person.change_slut_temp(2)
                    the_person.char "Oh my god, what have I even been saying? It's this wine [the_person.mc_title], I told you it makes me do crazy things."
                    the_person.char "Just... don't tell my sister that I told you any of that. You can keep a secret, right?"
                    mc.name "Of course, it's just between us."
                    the_person.char "That's a good boy. Now I think I should stop drinking this wine while I still can. It was nice talking, come by any time and we can do it again."
                    "She walks you to the door and you say goodbye."

                elif decision_score <= 55:
                    # She wants your opinion on some outfits
                    the_person.char "So [the_person.mc_title], now that I'm back on the market I think I need your help with something."
                    mc.name "With what?"
                    the_person.char "I need to update my wardrobe. You know, make it a little more modern. You're a hip young guy, I'm sure you can tell me what men like to see."
                    the_person.char "Would you help me? It'll just take a few minutes."
                    mc.name "Of course. Come on, show me what you've got."
                    "She smiles, drinks the last of her wine, and leads you into her bedroom."
                    call change_location(aunt_bedroom) from _call_change_location_1 #Changbe our location so that the background is correct,
                    the_person.char "Okay, so here's what I have to work with. Tell me what you think."
                    "She opens her wardrobe and stands back, giving you room to look around."
                    call screen outfit_creator(Outfit("New Outfit"))
                    if _return:
                        $ created_outfit = _return
                        "You pull out a few pieces of clothing and lay them out on [the_person.possessive_title]'s bed."
                        "She looks at the outfit you've laid out for her and seems to think for a second."
                        if created_outfit.slut_requirement <= the_person.sluttiness: #She likes it enough to try it on.
                            if created_outfit.vagina_visible():
                                the_person.char "Oh, wow. My pussy would just be out there, for everyone to see..."
                                "She sounds more excited than worried."
                            elif created_outfit.tits_visible():
                                the_person.char "Oh, wow. I wore that my tits would just be out there, for everyone to see..."
                                "She sounds more excited than worried."
                            elif not created_outfit.wearing_panties():
                                the_person.char "Oh wow, you don't think I should wear any panties with it? I guess that's what girls are doing these days..."
                            elif not created_outfit.wearing_bra():
                                the_person.char "You don't think I'd need a bra? I don't want my girls bouncing around all the time. Or do I?"
                            else:
                                the_person.char "Oh, that looks so cute!"

                            the_person.char "If I try it on will you tell me what you think?"
                            mc.name "Go for it. I want to see what it looks like on you."
                            "[the_person.possessive_title] starts to get undressed in front of you. She pauses after a second."
                            the_person.char "I'll just be naked for a second. You don't mind, right?"
                            mc.name "Of course not."
                            $ the_person.change_slut_temp(2)
                            the_person.char "I didn't think so. Just don't tell my sister."
                            $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
                            while strip_choice is not None:
                                $ the_person.draw_animated_removal(strip_choice)
                                "You watch as [the_person.possessive_title] take off her [strip_choice.name]."
                                $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)

                            "Once she's stripped out of her clothing [the_person.possessive_title] puts on the outfit you've made for her."
                            $ the_person.outfit = created_outfit.get_copy()
                            $ the_person.draw_person()

                            if created_outfit.slut_requirement <= the_person.sluttiness-20:
                                #She would like it normally and doesn't find it slutty.
                                the_person.char "Well? This is cute, but I don't know if I'm going to be wowing any men in it."
                                $ the_person.draw_person(position = "back_peek")
                                the_person.char "I think it needs to be a little... more. Or less, if you know what I mean."

                            else:
                                #She only likes it because she's drunk.
                                the_person.char "Well? It's certainly a lot bolder than I would normally wear. Is this the sort of thing men like?"
                                $ the_person.draw_person(position = "back_peek")
                                $ the_person.change_slut_temp(2)
                                the_person.char "What about my ass? Does it look good?"

                            menu:
                                "Add it to her wardrobe.":
                                    mc.name "It looks really good on you. You should wear it more often."
                                    the_person.char "You really think so? Okay then, that's why I wanted your opinion in the first place!"
                                    $ the_person.change_obedience(2)
                                    $ the_person.draw_person()
                                    $ the_person.wardrobe.add_outfit(created_outfit)
                                "Don't add it to her wardrobe.":
                                    mc.name "Now that I'm seeing it I don't think it really suits you."
                                    the_person.char "That's a shame. well, that's why I wanted your opinion in the first place!"
                                    $ the_person.change_obedience(1)
                                    "[the_person.title] starts to get naked again to put on her old outfit."
                                    $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
                                    while strip_choice is not None:
                                        $ the_person.draw_animated_removal(strip_choice)
                                        "You watch as [the_person.possessive_title] take off her [strip_choice.name]."
                                        $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
                                    $ the_person.outfit = the_person.planned_outfit.get_copy()
                                    $ the_person.draw_person()
                            the_person.char "This was really fun [the_person.mc_title], but I think that extra glass of wine is starting to get to me."
                            "She yawns dramatically and lies down on her bed."
                            $ the_person.change_happiness(2)
                            the_person.char "I'm going to have a little nap, but we should do this again some time. You're so nice to have around."
                            mc.name "I'll make sure to come by again. I'll see myself out."
                                    


                        else: #It's too slutty even for her drunk state. She's bashful but doesn't try it on.

                            the_person.char "Oh my god [the_person.mc_title], do you really think I could wear that?"
                            $ the_person.change_slut_temp(2)
                            if created_outfit.vagina_visible():
                                the_person.char "My... pussy would just be out there for everyone to see!"
                            elif created_outfit.tits_visible():
                                the_person.char "I would just have my tits out for everyone!"
                            elif not created_outfit.wearing_panties():
                                the_person.char "It doesn't even have any panties for me!"
                            elif not created_outfit.wearing_bra():
                                the_person.char "It doesn't even have a bra for me!"
                            mc.name "I think it would be a good look for you. You should try it on."
                            "[the_person.possessive_title] blushes and shakes her head."
                            the_person.char "I don't think I can... Maybe that extra glass of wine wasn't such a good idea [the_person.mc_title], it's gone straight to my head."
                            "She sits down on her bed and sighs."
                            the_person.char "I think I just need to have a rest. You can help me out with this some other day, okay?"
                            "[the_person.title] lies down and seems to be drifting off to sleep almost instantly. You say goodbye and head to the door."


                    else:
                        mc.name "Sorry [the_person.title], I don't have any ideas right now."
                        $ the_person.change_happiness(-2)
                        $ the_person.draw_person(emotion="sad")
                        "[the_person.possessive_title] sighs dramatically and collapses onto her bed."
                        the_person.char "Am I really that out of touch? I'll have to go shopping and update everything then."
                        the_person.char "Maybe I just need to lie down, this wine is really getting to me."
                        "[the_person.title] seems to be drifting off to sleep already. You say goodbye and head to the door."
                    $ renpy.scene("Active")
                    call change_location(aunt_apartment) from _call_change_location_4

                elif decision_score <= 65:
                    # She wants your opinion about some underwear
                    the_person.char "So [the_person.mc_title], since you're here I could use some help with something. It's a little... delicate."
                    mc.name "What do you need?"
                    the_person.char "Well, I want to put myself out there and meet someone, but I haven't done that since [cousin.title] was born."
                    the_person.char "I've got plenty of lingerie, but I need to know what looks good on me. Can I trust you to give me an honest opinion?"
                    mc.name "Of course, I'll tell you exactly what I think."
                    "She smiles, drinks the last of her wine, and leads you into her bedroom."
                    call change_location(aunt_bedroom) from _call_change_location_2 #Changbe our location so that the background is correct,
                    the_person.char "Okay, so I have a few things I want your opinion on. You just tell me what looks good and that I should keep around."
                    "She starts to strip down, then pauses and looks at you."
                    the_person.char "Don't tell my sister I'm doing this with you. We're both adults, but I don't think she'd understand."
                    "She rolls her eyes and keeps going."
                    $ the_person.change_slut_temp(1)
                    $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
                    while strip_choice is not None:
                        $ the_person.draw_animated_removal(strip_choice)
                        "You watch as [the_person.possessive_title] take off her [strip_choice.name]."
                        $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)

                    the_person.char "Okay, first one."
                    $ lingerie = default_wardrobe.get_random_appropriate_underwear(the_person.sluttiness, the_person.sluttiness-30)
                    $ the_person.outfit = lingerie.get_copy()
                    $ the_person.draw_person()
                    "She slips on her new set of underwear."
                    the_person.char "Okay, what do you think? Keep or toss?"
                    $ the_person.draw_person(position="back_peek")
                    menu:
                        "Add it to her wardrobe.":
                            mc.name "Keep, definitely."
                            $ the_person.draw_person()
                            the_person.char "Okay, keep it is! Let's see what's up next..."
                            $ the_person.wardrobe.add_underwear_set(lingerie)
                        "Don't add it to her wardrobe.":
                            mc.name "Toss, I think you can do better."
                            $ the_person.draw_person()
                            the_person.char "I think so too. Let's see what's up next..."

                    $ the_person.change_slut_temp(1)
                    $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
                    while strip_choice is not None:
                        $ the_person.draw_animated_removal(strip_choice)
                        "You watch as [the_person.possessive_title] take off her [strip_choice.name]."
                        $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)

                    $ lingerie = default_wardrobe.get_random_appropriate_underwear(the_person.sluttiness, the_person.sluttiness-25)
                    $ the_person.outfit = lingerie.get_copy()
                    $ the_person.draw_person()
                    "She slips on the next set of lingerie."
                    the_person.char "What about this one? Keep or toss?"
                    $ the_person.draw_person(position="back_peek")
                    menu:
                        "Add it to her wardrobe.":
                            mc.name "Keep."
                            $ the_person.draw_person()
                            the_person.char "We've got a winner! Okay, one more..."
                            $ the_person.wardrobe.add_underwear_set(lingerie)
                        "Don't add it to her wardrobe.":
                            mc.name "Toss."
                            $ the_person.draw_person()
                            the_person.char "Tough customer. Okay, one more..."

                    $ the_person.change_slut_temp(1)
                    $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
                    while strip_choice is not None:
                        $ the_person.draw_animated_removal(strip_choice)
                        "You watch as [the_person.possessive_title] take off her [strip_choice.name]."
                        $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)

                    $ lingerie = default_wardrobe.get_random_appropriate_underwear(the_person.sluttiness, the_person.sluttiness-20)
                    $ the_person.outfit = lingerie.get_copy()
                    $ the_person.draw_person()
                    "She slips on the last set of underwear she has to show you."
                    $ the_person.draw_person(position="back_peek")
                    the_person.char "Well?"
                    menu:
                        "Add it to her wardrobe.":
                            mc.name "Keep it."
                            $ the_person.draw_person()
                            the_person.char "I thought you'd like this one. Okay, I'll hold onto it!"
                            $ the_person.wardrobe.add_underwear_set(lingerie)
                        "Don't add it to her wardrobe.":
                            mc.name "Toss it, you've got nice stuff you could wear."
                            $ the_person.draw_person()
                            the_person.char "Yeah, I think you're right. Let's get this off then!"
                            $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
                            while strip_choice is not None:
                                $ the_person.draw_animated_removal(strip_choice)
                                "You watch as [the_person.possessive_title] take off her [strip_choice.name]."
                                $ strip_choice = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)

                    $ the_person.change_love(2)
                    $ the_person.change_slut_temp(2)
                    the_person.char "Thank you for helping me [the_person.mc_title]. Now I think I need to lie down, because that wine is going right to my head."
                    "She yawns dramatically and falls back onto her bed, arms spread wide."
                    the_person.char "Stop by again some time soon though, we can do this again."
                    mc.name "Sure thing [the_person.title], I'll be by again soon."


                    $ renpy.scene("Active")
                    call change_location(aunt_apartment) from _call_change_location_3
                    # Same as above but she strips down and asks you for underwear sets.
                elif decision_score <= 75:
                    # She wants to strip for you.
                    the_person.char "[the_person.mc_title], does it feel warm in here or is it just me?"
                    "[the_person.title] takes a sip from her glass of wine and stands up."
                    if the_person.outfit.remove_random_any(exclude_feet = True, do_not_remove = True):
                        the_person.char "You don't mind if I get a little more comfortable, do you?"
                        $ strip_choice = the_person.outfit.remove_random_upper(top_layer_first = True, do_not_remove = True)
                        $ the_person.draw_animated_removal(strip_choice)
                        "Before you can answer she peels off her [strip_choice.name] and drops it onto the couch."
                        mc.name "No, go right ahead."
                        if the_person.outfit.remove_random_lower(do_not_remove = True):
                            $ strip_choice = the_person.outfit.remove_random_lower(top_layer_first = True, do_not_remove = True)
                            $ the_person.draw_animated_removal(strip_choice)
                            "She takes off her [strip_choice.name] next and throws it onto the couch too."
                    the_person.char "[the_person.mc_title], can I ask you a question? Do you think I'm still attractive?"
                    $ the_person.draw_person(position = "back_peek")
                    "She spins around in front of you, showing you her butt."
                    the_person.char "I mean, would you be attracted to me if I wasn't your aunt?"
                    menu:
                        "Encourage her." if the_person.outfit.remove_random_any(exclude_feet = True, do_not_remove = True):
                            mc.name "Keep taking your clothes off and maybe I'll tell you."
                            $ the_person.change_slut_temp(2)
                            $ the_person.change_obedience(1)
                            the_person.char "Oh? Okay then, I'll play your game you dirty boy."
                            $ strip_choice = the_person.outfit.remove_random_any(exclude_feet = True, do_not_remove = True)
                            $ the_person.draw_animated_removal(strip_choice, position = "back_peek")
                            "She keeps her back to you and takes off her [strip_choice.name]."
                            the_person.char "Do you like watching me strip down for you? Do you think I'm hot?"
                            mc.name "Yeah, I think you're hot."
                            the_person.char "Oh [the_person.mc_title], that's so nice to hear. I just want to be wanted. Even if it's only by you..."
                            $ the_person.draw_person()
                            the_person.char "We should keep this our little secret, okay?"

                        "Compliment her.":
                            mc.name "Of course you're attractive [the_person.title], look at you! You've got a hot ass and a killer rack."
                            the_person.char "Oh [the_person.mc_title], you know just what I wanted to hear..."
                            "She wiggles her ass just for you."
                            the_person.char "You don't think I'm too old? I feel like I'm past my prime."
                            mc.name "You're beautiful, you have an amazing body, and you have the experience to know what to do with it."
                            $ the_person.change_happiness(5)
                            $ the_person.change_slut_temp(2)
                            $ the_person.change_love(1)
                            $ the_person.draw_person()
                            if the_person.outfit.tits_available():
                                "She turns back around and leans over to give you a hug on the couch. Her tits dangle down in front of you, tempting you."
                            else:
                                "She turns back around and leans over to give you a hug on the couch."
                            the_person.char "It's been so long since I felt wanted... I think I just needed to feel like I was, even if it's only by you..."

                        "Insult her.":
                            mc.name "Attractive? Sure, but you've got to accept you're past your prime."
                            $ the_person.change_happiness(-5)
                            the_person.char "What?"
                            mc.name "You're getting older [the_person.title], you just can't compete with all the younger women out there."
                            $ the_person.draw_person(emotion="angry")
                            "She turns back and crosses her arms."
                            the_person.char "You're telling me these aren't some nice tits?"
                            mc.name "Maybe, but you have to do more than just tease. If you want to impress someone get them wrapped around their cock."
                            mc.name "You've got experience, but you need to put it to work."
                            $ the_person.change_obedience(2)
                            $ the_person.change_slut_temp(3)
                            "She seems to think long and hard about this for a few seconds."
                            the_person.char "I guess I understand. Thank you for being honest with me."

                    $ the_person.draw_person(position="sitting")
                    "She sits down on the couch again and sighs."
                    the_person.char "I'm sorry but that extra glass of wine is just knocking me out. I think I'm going to lie down for a bit."
                    the_person.char "Do you want to come by another day and do this again?"
                    mc.name "I'd love to."
                    "You take your wine glasses to the kitchen for [the_person.title] and say goodbye."

                else:
                    "[the_person.possessive_title] slides closer to you on the couch and places her hand on your thigh while you chat."
                    "Inch by inch it moves up your leg until it brushes against the tip of your soft cock. She rubs it gently through your pants, coaxing it to life."
                    the_person.char "I... I know we shouldn't, but nobody needs to know. Right?"
                    menu:
                        "Fuck her." if mc.current_stamina > 0:
                            call fuck_person(the_person) from _call_fuck_person_22
                            "[the_person.possessive_title] is exhausted when you're finished fooling around. She lies back on the couch and quickly falls asleep."
                            "You get yourself tidied up, move the dirty glasses of wine to the kitchen, and get ready to leave."

                        "Fuck her. (disabled)" if mc.current_stamina == 0:
                            pass

                        "Turn her down.":
                            mc.name "I don't think that's a good idea right now [the_person.title]. You're in no state to make that kind of decision."
                            "You gently take her hand off you. She seems to snap to her senses and looks away."
                            the_person.char "Right, of course. I didn't mean... I didn't mean anything, okay?"
                            $ the_person.change_love(1)
                            $ the_person.change_obedience(1)
                            the_person.char "Maybe you should go, I'm clearly not thinking straight with all this wine."
                            mc.name "That may be for the best. Maybe we can do this again some other time though."
                            "You take the glasses of wine to the kitchen for [the_person.possessive_title] and say goodbye."


                $ the_person.clear_situational_slut("Drunk")

            else:
                the_person.char "Oh, I really shouldn't. You can ask your mom some time, wine makes me go silly."
                $ the_person.draw_person()
                "[the_person.title] waits until you've finished your glass of wine, then escorts you to the door."
                mc.name "See you soon [the_person.title]."
                the_person.char "I hope so! See you around."
        "Say goodbye.":
            "[the_person.title] waits until you've finished your glass of wine, then escorts you to the door."
            mc.name "See you soon [the_person.title]."
            the_person.char "I hope so! See you around."

    call advance_time() from _call_advance_time_17 #Drinking advances time
    return
