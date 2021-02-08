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
    the_person "These are my first ideas, you should pick something for me to work on right now. If you change your mind you can always come back here and pick a new topic."
    $ clear_scene()
    call research_select_action_description from _call_research_select_action_description
    $ stephanie.draw_person(emotion = "happy")
    stephanie "Good, I'll work on that later. Can we take a look at the production lab now?"
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
