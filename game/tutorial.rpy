label tutorial_start:
    menu:
        "I have played Lab Rats 1 Before.":
            "It has been a year since the end of your summer job at the university lab."



        "I am new to Lab Rats.":
            "A year ago you were a chemical engineering student, getting ready to graduate soon and looking for something to do over the summer."
            "You ended up with a summer job on campus as a lab assistant working with a two person team."
            "Your lab director, Nora, and her long time lab assistant Stephanie were investigating the properties of a new lab created molecule."
            "It didn't take long before you discovered it could be used to deliver mind altering agents. You spent the summer creating doses of \"serum\" in secret."
            "It has been a year since the end of your summer job at the university lab."

    "Your experimentation with the inhibition removing serum was fun, but in the end the effects were temporary."
    "The end of the summer also meant the end of your access to the serum making supplies."
    "Little by little the women slid back into their previous lives."

    scene
    $ bedroom.show_background()

    "Four months ago you graduated from university with a degree in chemical engineering."
    "Since then you have been living at home and sending out resumes. You have had several interviews, but no job offers yet."
    "Today you have an interview with a small pharmacutical company. You've gotten up early and dressed in your finest suit."
    $ hall.show_background()
    "You head for the front door, eager to get to your interview early."
    mom "[mom.mc_title], are you leaving already?"
    "[mom.possessive_title]'s voice comes from the kitchen, along with the smell of breakfast."
    mc.name "Yeah, I want to make sure I make it on time."
    mom "You haven't had any breakfast yet. You should eat, I'll drive you if you're running late."
    "The smell of cooked toast and frying eggs wins you over and you head to the kitchen."
    $ kitchen.show_background()
    $ mom.draw_person(emotion = "happy", position = "back_peek")
    "[mom.possessive_title] is at the stove and looks back at you when you come into the room."
    mom "The food's almost ready. Just take a seat and I'll make you a plate."
    mc.name "Thanks Mom, I didn't realize how hungry I was. Nerves, I guess."
    mom "Don't worry, I'm sure they'll love you."
    "She turns back and focuses her attention on her cooking. A few minutes later she presents you with a plate."
    $ mom.draw_person(emotion = "happy")
    mom "Here you go sweetheart. You look very sharp in your suit, by the way. My little boy is all grown up."
    "You eat quickly, keeping a sharp eye on the time. When you're done you stand up and move to the front door again."
    mc.name "Okay, I've got to go if I'm going to catch my bus. I'll talk to you later and let you know how it goes."
    mom "Wait."
    "Mom follows you to the front door. She straightens your tie and brushes some lint off of your shoulder."
    mom "Oh, I should have ironed this for you."
    mc.name "It's fine, Mom. Really."
    mom "I know, I know, I'll stop fussing. Good luck sweety."
    "She wraps her arms around you and gives you a tight hug. You hug her back then hurry out the door."
    $ clear_scene()
    $ downtown.show_background()
    "It takes an hour on public transit then a short walk to find the building. It's a small single level office attached to a slightly larger warehouse style building."
    "You pull on the door handle. It thunks loudly - locked. You try the other one and get the same result."
    mc.name "Hello?"
    "You pull on the locked door again, then take a step back and look around for another entrance you might have missed. You don't see any."
    "You get your phone out and call the contact number you were given a few days earlier. It goes immediately to a generic voice mail system."
    "With nothing left to do you give up and turn around. Suddenly there's a click and the front door to the office swings open."
    "Janitor" "Hey, who's making all that noise?"
    "A middle aged man is standing at the door wearing grey-brown overalls. He's holding a stack of papers in one hand and a tape gun in the other."
    mc.name "That was me. I'm supposed to be here for a job interview, do you know where I should be going?"
    "Janitor" "Well I think you're shit out of luck then. They went belly up yesterday. This place belongs to the bank now."
    mc.name "What? That can't be right, I was talking to them less than a week ago."
    "Janitor" "Here, take a look for yourself."
    "The man, who you assume is a janitor of some sort, hands you one of the sheets of paper he's holding."
    "It features a picture of the building along with an address matching the one you were given and a large \"FORECLOSED\" label along the top."
    "The janitor turns around and holds a page up to the front door, then sticks it in place with tape around all four edges."
    "Janitor" "They must have been neck deep in debt, if that makes you feel better about not working for 'em."
    "Janitor" "They left all their science stuff behind; must've been worth less than the debt they're ditching."
    mc.name "So everything's still in there?"
    "Janitor" "Seems like it. Bank doesn't know where to sell it and didn't want me to warehouse it, so it goes with the property."
    "You look back at the foreclosure notice and read until you see the listing price."
    "The rent on the unit is expensive, but an order of magnitude less than what you would have expected a fully stocked lab to be worth."
    mc.name "Would you mind if I take a quick look around? I promise I won't be long."
    "The janitor gives you a stern look, judging your character, then nods and opens the door."
    "Janitor" "I'm just about done tidying this place up so the bank can sell it. If you can be in and out in five minutes you can look around."
    mc.name "Thank you, I'll be quick."
    "You step inside the building and take a walk around."
    "The main office building contains a small lab, much like the one you worked at while you were in university, suitable for research and development tasks."
    "The connected warehouse space has a basic chemical production line installed. The machines are all off-brand but seem functional."
    "At the back of the building is a loading dock for shipping and receiving materials."
    "While you're exploring you hear the janitor yell from across the building."
    "Janitor" "I need to be heading off. Are ya done in there?"
    mc.name "Yeah, I'm done. Thanks again."
    "The janitor locks the door when you leave. You get on a bus heading home and do some research on the way."
    "You look up the price of some of the pieces of equipment you saw and confirm your suspicion. The bank has no idea how valuable the property really is."
    scene
    $ renpy.with_statement(fade)
    $ kitchen.show_background()
    "Three days later..."
    $ mom.draw_person(position = "sitting")
    "[mom.title] looks over the paperwork you've laid out. Property cost, equipment value, and potential earnings are all listed."
    mom "And you've checked all the numbers?"
    mc.name "Three times."
    mom "It's just... this is a lot of money [mom.mc_title]. I would need to take a second mortgage out on the house."
    mc.name "And I'll be able to pay for that. This is the chance of a life time Mom."
    mom "What was it you said you were going to make again?"
    mc.name "When I was working at the lab last summer we developed some prototype chemical carriers. I think they have huge commercial potential."
    mc.name "And there's no regulation around them yet, because they're so new. I can start production and be selling them tomorrow."
    "[mom.possessive_title] leans back in her chair and pinches the brow of her nose."
    mom "Okay, you've convinced me. I'll get in touch with the bank and put a loan on the house."
    "You jump up and throw your arms around [mom.possessive_title]. She laughs and hugs you back."

    lily "What's going on?"
    $ lily.draw_person()
    "[lily.possessive_title] steps into the doorway and looks at you both."
    $ mom.draw_person(position = "sitting")
    mom "Your brother is starting a business. I'm his first investor."
    $ lily.draw_person(emotion = "happy")
    lily "Is that what you've been excited about the last couple days? What're you actually making?"
    mc.name "I'll have to tell you more about it later Lily, I've got some calls to make. Thanks Mom, you're the best!"
    $ clear_scene()
    "You leave [mom.possessive_title] and sister in the kitchen to talk. You retreat to your room for some privacy."

    $ bedroom.show_background()
    "You can manage the machinery of the lab, but you're going to need help refining the serum design from last year."
    "You pick up your phone and call [stephanie.title]."
    stephanie "Hello?"
    mc.name "Stephanie, this is [mc.name]."
    stephanie "[stephanie.mc_title]! Good to hear from you, what's up?"
    mc.name "I'd like to talk to you about a business offer. Any chance we could meet somewhere?"
    stephanie "Ooh, a business offer. How mysterious. I'm almost done here at the lab, if you buy me a drink you've got a deal."
    mc.name "Done. Where's convenient for you?"
    "Stephanie sends you the address of a bar close to the university."
    scene
    $ bar_location.show_background()
    "It takes you an hour to get your pitch prepared and to get over to the bar."
    "When you arrive [stephanie.title] is sitting at the bar with a drink already. She smiles and raises her glass."
    $ stephanie.draw_person(position = "sitting", emotion = "happy")
    stephanie "Hey [stephanie.mc_title], it's great to see you!"
    $ mc.change_locked_clarity(5)
    "She stands and gives you a hug."
    stephanie "That was a crazy summer we had together. It seems like such a blur now, but I had a lot of fun."
    mc.name "Me too, that's actually part of what I want to talk to you about."
    "You order a drink for yourself and sit down."
    "You lay out your idea to [stephanie.title]: the commercial production and distribution of the experimental serum."
    stephanie "Well that's... Fuck, it's bold, I'll say that. And you need me to handle the R&D side of the business."
    mc.name "Right. Production processes are my bread and butter, but I need your help to figure out what we're actually making."
    "Stephanie finishes off her drink and flags down the bartender for another."
    stephanie "I would need to quit my job at the lab, and there's no guarantee that this even goes anywhere."
    mc.name "Correct."
    stephanie "Do you have any clients?"
    mc.name "Not yet. It's hard to have clients without a product."
    "Stephanie gets her drink and sips it thoughtfully."
    mc.name "The pay won't be great either, but I can promise..."
    stephanie "I'm in."
    mc.name "I... what?"
    stephanie "I'm in. The old lab just doesn't feel the same since you left. I've been looking for something new in my life, something to shake things up."
    stephanie "I think this is it."
    "She raises her drink and smiles a huge smile."
    stephanie "A toast: To us, and stupid risks!"
    mc.name "To us!"
    "You clink glasses together and drink."
    stephanie "Ah... Okay, so I've got some thoughts already..."
    "Stephanie grabs a napkin and starts doodling on it. You spend the rest of the night with her, drinking and talking until you have to say goodbye."
    $ clear_scene()
    "A week later [mom.possessive_title] has a new mortgage on the house and purchases the lab in your name."
    "You are the sole shareholder of your own company and [stephanie.title] is first, and so far only, employee. She takes her position as your head researcher."
    $ mc.business.event_triggers_dict["Tutorial_Section"] = True
    #$ mc.can_skip_time = False
    python: #To begin the tutorial we limit where people can travel!
        for place in list_of_places:
            place.accessable = False
    $ lobby.accessable = True
    return


label lobby_tutorial_intro():
    "You arrive at your newly purchased lab building. It's small, out of date, and run down, but it's yours!"
    "You can see [stephanie.title] through the glass front door as you walk up. She turns and waves when you come in."
    $ stephanie.draw_person(emotion = "happy")
    stephanie "Hey [stephanie.mc_title]. I can't believe you were able to find this place, this is a once in a lifetime opportunity."
    mc.name "I got lucky, that's all. Have you been here long?"
    stephanie "Just a few minutes. I figured we could take a walk through the place together and make sure we know what we're doing."
    mc.name "Sounds like a good idea."
    "[stephanie.title] motions to the room you're standing in. The only item of interest in the small room is a welcome desk covered in a thin layer of dust."
    stephanie "This is the lobby I guess. I doubt we'll be spending much time here."
    mc.name "There's a lab section down here that I thought would be ideal for your R&D work."
    stephanie "Sweet, let's go take a look."
    $ lobby.accessable = False
    $ rd_division.accessable = True
    $ clear_scene()
    return

label research_tutorial_intro():
    $ stephanie.draw_person(emotion = "happy")
    "The small room has a couple of lab benches with fume hoods, old but serviceable glassware, and a few more delicate instruments you don't recognise by sight."
    mc.name "Here we are, what do you think?"
    "[stephanie.title] starts to walk down the benches, checking cabinets and machinery."
    stephanie "I'll need some more time to check it all out, but it all looks like it works. Holy crap [stephanie.mc_title], I can't believe you're giving me my own lab."
    mc.name "I need you [stephanie.title]. You've got the expertise and talent to get this place off the ground."
    stephanie "I'll try not to let you down. So, let's talk about how this R&D is going to work."
    stephanie "I have a different ideas I can explore right now. With some time I should be able to figure out some new fundamental property."
    stephanie "When you want to produce an actual product we will need to create a new serum design."
    stephanie "It will take some more research work to figure out how we can actually produce the design."
    stephanie "Right now I think we'll struggle to get a single property to express itself properly in our serums, but with some experience we can combined a bunch."
    mc.name "Right, I think I understand."
    "[stephanie.title] pulls out a notebook and flips it open, handing it over to you."
    stephanie "These are my first ideas, you should pick something for me to work on right now. If you change your mind you can always come back here and pick a new topic."
    $ clear_scene()
    call research_select_action_description from _call_research_select_action_description
    "You read through the options she's laid out. \"Suggestion Drugs\", \"Inhibition Suppression\", and vague hints of even more {i}questionable{/i} developments down the line."
    $ mc.change_locked_clarity(10)
    "You weren't planning for this to be a repeat of last year, but [stephanie.title] seems happy to hand you all the tools you would need."
    "You're so distracted by your thoughts that [stephanie.possessive_title] needs to clear her throat to get your attention again."
    $ stephanie.draw_person()
    stephanie "Well? What do you think?"
    mc.name "It, uh... It all look good. Start wherever you want."
    stephanie "I'm going to need a little more direction than that [stephanie.mc_title]."
    stephanie "This isn't quite brain surgery, but you could throw a rock into their back yard. I need your input."
    "You try and take another look through her notes, but you can't focus your mind."
    "Your dick seems to be using more than its fair share of brain power to run some imaginative scenarios."
    menu:
        "Go jerk off.":
            "You can only think of one immediate solution to the problem."
            mc.name "I'll need a moment to think about this. Just wait here, I'm going to stretch my legs and take a walk around."
            stephanie "Sure, I'll come with..."
            mc.name "I think better alone, actually."
            stephanie "Oh, sure... Uh, I'll be here then..."
            $ clear_scene()
            "You find your personal office, or what will be once you get the old name plate removed, and step inside."
            "You close the door and sit down at the desk, pulling out your phone to find some porn to get you off."
            "You settle on an old favourite and start to jack off, determined to make it quick."
            "After a couple of minutes you notice something odd - you're barely paying attention to the bouncing tits on your tiny screen."
            "Instead you're remembering all the trouble you got up to last year, and all of the new opportunities you will have now."
            "Does [stephanie.title] really not care what you're making here, and what it can do? How could she not?"
            "Maybe she likes it? Maybe you really left an impression on her with your last serum-based mind control spree?"
            $ mc.change_locked_clarity(10)
            "... Maybe she wants to help this time?"
            "That thought pushes you over the edge!"
            $ climax_controller = ClimaxController(["Cum!", "masturbation"])
            $ climax_controller.show_climax_menu()
            $ climax_controller.do_clarity_release()
            "You snatch at some tissues and do your best to contain the mess as you cum."
            "A cold calm washes over you now that you're finished, and along with it the razor sharp focus you'll need to achieve your goals."
            "You double check that you're presentable and return to the research lab."
            $ stephanie.draw_person()
            stephanie "Well, any ideas?"
            "This time when you look at her notes they all make perfect sense. You see what will need to be studied, and how to turn that knowledge into a useful discovery."
            call research_select_action_description
            $ stephanie.draw_person(emotion = "happy")
            stephanie "That's a very clever thought [stephanie.mc_title], I'll start studying that right away."

        "Pick your research later.":
            mc.name "I'll need some time to look these options over. Make sure all of these machines are working at peak efficency until then."
            "[stephanie.title] seems disappointed by the slow start."
            stephanie "Fine, I'll run them all through a diagnostic cycle. Don't keep me waiting though, I don't want to just sit around and waste time."

    stephanie "Can we take a look at the production lab now?"
    $ rd_division.accessable = False
    $ p_division.accessable = True
    $ clear_scene()
    return

label production_tutorial_intro():
    $ stephanie.draw_person(emotion = "happy")
    "This lab room is larger than [stephanie.title]'s production lab and filled with bulkier and more familiar equipment."
    stephanie "When I'm finished creating a serum design you can take it here and tool up the production lines to make it on an industrial scale."
    mc.name "Right. I'll need some basic chemical supplies though, so I need to make sure to order them."
    stephanie "Or hire someone else to do that for you. If you want to turn this into a successful business we will probably need more than just the two of us."
    "You take a quick walk around the production lab."
    stephanie "I think the proper offices are down here, let's go take a look."

    $ p_division.accessable = False
    $ office.accessable = True
    $ clear_scene()
    return

label office_tutorial_intro():
    $ stephanie.draw_person(emotion = "happy")
    "The offices are divided into a few separate cubicles and a small private office."
    stephanie "This seems like a good place to do any of your supply ordering from, and you can use your office to interview anyone who you're thinking of hiring."
    mc.name "The more people we take on the more paperwork I'm going to have to do to keep everyone organised."
    stephanie "With enough people that would end up being a full time job all by itself. I don't envy you [stephanie.mc_title], I much prefer my cozy little lab."
    mc.name "That's all there is to see here. Last stop is the marketing room."
    stephanie "Lead on!"
    $ office.accessable = False
    $ m_division.accessable = True
    $ clear_scene()
    return

label marketing_tutorial_intro():
    $ stephanie.draw_person(emotion = "happy")
    "The marketing room is a combination of office and mail room. It comes with all the supplies you would need to mail out your product to your customers."
    mc.name "When we've got actual product to sell I'll be able to come here and mail it off."
    stephanie "I suppose we'll be relying on word of mouth for now, but we should see about advertising in the future."
    "You nod in agreement and wander around the room until you're satisfied there's nothing more of interest."
    mc.name "That's everything there is to see, so I guess it's time to get to work!"
    stephanie "I'll get back to the lab, come see me if you want to check in on my progress."
    python:
        for place in list_of_places:
            place.accessable = True
    $ clear_scene()
    call advance_time from _call_advance_time_11
    return
