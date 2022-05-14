## All story stuff related to Mom getting her own Instapic account.

##TODO: Add requiremetn stuff
init -2 python:
    pass #TODO: Requirement stuff goes here.
    def mom_instapic_setup_intro_requirement(the_person, start_day):
        if the_person.has_role(instapic_role):
            return False
        elif day < start_day:
            return False
        return True

    def mom_instapic_setup_help_requirement(the_person):
        if the_person.has_role(instapic_role):
            return False
        elif the_person.event_triggers_dict.get("mom_instapic_intro_done", False):
            return False
        elif time_of_day >= 4:
            return "Not enough time."
        return True

    def mom_instapic_alt_intro_requirement(the_person, start_day):
        if the_person.event_triggers_dict.get("mom_instapic_help_enabled", False):
            return True #NOTE: When triggered this automatically returns, clearing the event from the internal list.

        if not the_person.has_role(instapic_role):
            return False
        elif day < start_day:
            return False
        elif not the_person.event_triggers_dict.get("mom_instapic_intro_done", False):
            return False
        return True

    def mom_instapic_ban_requirement(the_person, start_day):
        if not the_person.has_role(instapic_role):
            return False
        elif day < start_day:
            return False
        elif mc.location.get_person_count() > 1:
            return False
        return True

    def mom_onlyfans_help_requirement(the_person):
        if not the_person.has_role(onlyfans_role):
            return False
        elif (mom_bedroom.get_person_count() > 0 and not mom_bedroom.has_person(the_person)) or mom_bedroom.get_person_count() > 1:
            return "Not with people around..."
        elif the_person.event_triggers_dict.get("onlyfans_help_today", False):
            return "Already helped today."
        elif time_of_day >= 4:
            return "Not enough time."
        else:
            return True

    def sister_instapic_jealous_requirement(the_person, start_day):
        if mc.location.has_person(mom):
            return False
        elif day < start_day:
            return False
        else:
            return True

label mom_instapic_setup_intro(the_person): # Tells you that the instapic thing was "really fun" and she wants to set up her own account.
    $ the_person.draw_person()
    "[the_person.possessive_title] is staring at her cellphone, muttering frustrated curses under her breath."
    "When she notices you she breathes a sigh of relief and hurries over."
    the_person "Oh, just the man I was hoping for! Can you help me?"
    "She doesn't wait for a response and hurries over, pressing her phone into your hands."
    mc.name "Sure [the_person.title], what's the problem?"
    the_person "Well, I wanted to see some of those pictures that we took with [lily.title]."
    the_person "I went to that Insta-thing site, but it won't let me see them!"
    "You look at her phone and see the problem immediately; without an account she's stuck on [lily.possessive_title]'s public page."
    mc.name "It looks like you'll need to set up your own account before you can see them."
    the_person "Really? Why do I have to do that?"
    mc.name "I... You just do [the_person.title]."
    "[the_person.possessive_title] frowns, but seems to accept your expertise on the matter."
    the_person "Fine. How do I do that?"
    menu:
        "Help her set up an account.{image=gui/heart/Time_Advance.png}" if time_of_day < 4:
            mc.name "Here, I'll show you. Do you have a few minutes?"
            "She nods and stands beside you to watch what you're doing on the small screen."
            call mom_instapic_setup(the_person, intro_finished = True)

        "Help her set up an account.{image=gui/heart/Time_Advance.png}\nNot enough time (disabled)" if time_of_day >= 4:
            pass

        "Help her later.":
            "Watching [the_person.title] struggle with her phone convinces you this will take more time than you have right now."
            mc.name "I'm busy right now, but I can walk you through it later if you'd like."
            "She smiles happily."
            the_person "You don't mind?"
            mc.name "No, no, not at all. I'll find you when I've got a few minutes, okay?"
            the_person "Okay, sounds good. Thank you sweetheart!"
            $ mc.change_locked_clarity(5)
            "[the_person.possessive_title] gives you a kiss on the cheek."
            $ mom_instapic_setup_event = Action("Set up her InstaPic account.{image=gui/heart/Time_Advance.png}", mom_instapic_setup_help_requirement, "mom_instapic_setup", is_fast = False)
            $ mom.get_role_reference(mother_role).actions.append(mom_instapic_setup_event)



    return

label mom_instapic_setup(the_person, intro_finished = False): # Sets up her InstaPic role and gives you the opportunity to push some buttons.
    $ the_person.event_triggers_dict["mom_instapic_intro_done"] = True
    if not intro_finished:
        mc.name "Do you have some time to get your Instapic account set up?"
        "[the_person.possessive_title] nods and pulls out her phone. She hands it to you and clings to your side, watching what you're doing."

    mc.name "Okay, let's see here... First thing we need is your username."
    the_person "Can I just use my name?"
    mc.name "Uh, it doesn't really work like that."
    $ mom_username = ""
    menu:
        "Let her pick one.":
            mc.name "Give it some thought, you must have some sort of idea."
            "She purses her lips and thinks for a moment."
            if mom.has_taboo("vaginal_sex"):
                $ mom_username = "VeryNaughtyMommy"
                $ mc.change_locked_clarity(10)
                the_person "How about \"Very naughty mommy\"?"
                mc.name "Wow, where'd that come from?"
                "She blushes and shrugs innocently."
                the_person "Nowhere, it's just something I've... Uh... Used before on some sites."
                mc.name "Well, that'll do. Alright, let's see what's next!"
            else:
                $ mom_username = "DedicatedMommy"
                the_person "How about \"Dedicated mom\"? I hope that sounds like me."
                mc.name "That'll do! Next!"

        "Pick her username." if the_person.obedience >= 120:
            $ mom_username = renpy.input("Pick her username.")
            mc.name "How about..."
            the_person "Hmm, do you think that's good?"
            mc.name "Yeah, that should suit you just fine. Next!"

        "Pich her username.\nRequires: 120 Obedience (disabled)" if the_person.obedience < 120:
            pass

    "You submit the name and move onto the next screen. It asks you for a collection of personal details."
    mc.name "It wants some personal details, like your job and sort of hobbies you like."
    the_person "Oh, I never know what to put for things like that. Can you fill it out for me?"
    menu:
        "Fill it with garbage info.":
            "You fill up her profile page with garbage info, typing in a random number for her age and selecting random hobbies."

        "Fill it with slutty info.":
            mc.name "No problem [the_person.title], no problem..."
            $ mc.change_locked_clarity(10)
            "You start to fill her profile with as much overtly slutty info as you think you can get away with."
            if the_person.has_role(employee_role) or the_person.has_job(mom_associate_job) or the_person.has_job(mom_secretary_job):
                "Job: \"Office Bimbo\"" (what_style = "text_message_style")
            else:
                "Job: \"Stay-at-home MILF\"" (what_style = "text_message_style")

            "Hobbies: \"Looking Sexy, Teasing Cocks!\"" (what_style = "text_message_style")
            "Other Info: \"[the_person.tits] Cup Tits!\"" (what_style = "text_message_style")

    the_person "What're they asking for now?"
    "There's an optional section for other details: full name, address, favourite hangouts."
    mc.name "Just some more details about you. Do you care what I put here?"
    if the_person.get_opinion_score(["showing her tits", "showing her ass"]) >= 2:
        the_person "Oh just put down the truth. I'm an open book!"
    else:
        the_person "I don't know about giving out that sort of stuff on the internet; people might figure out who I am!"
        mc.name "That's fine, 'll just leave it blank then."
        the_person "Thank you [the_person.mc_title], I'd be so lost without you!"

    menu:
        "Skip the section.":
            "You leave all of the fields that might identify [the_person.title] empty."

        "Fill it with her real details.":
            "You fill her profile up with all of her real details, including her name and where she works."
            #TODO: Trigger future events where people know who she is.

    "You submit the details and move on. The last step is to put up [the_person.title]'s first post!"
    mc.name "Right, now we just need to make your first post and we'll be all done."
    "She's excited, but clearly has no clue how the platform works."
    the_person "Okay! What does that mean?"
    menu:
        "Use a random picture.":
            mc.name "It just needs to be some sort of picture. It doesn't even matter what it is."
            "You open up her phone's gallery and pick a random picture of a nearby park."


        "Take a picture of her.":
            mc.name "We just need to take a picture of you. Here, smile!"
            if the_person.get_opinion_score(["showing her tits", "showing her ass"]) >= 2:
                "You open up her camera app and point the phone at her. She smiles and waves her hand for the picture."
            else:
                #TODO: Have this trigger future events where people know who she is on sight.
                "You open up her camera app and point the phone at her. She holds her hand in front of her face."
                the_person "I don't know if I want people on the internet to know what I look like!"
                mc.name "You've already been in [lily.title]'s pictures, what's there to hide?"
                the_person "Well... Okay, just make sure I don't look silly."
                "She lowers her hand and smiles meekly for the camera."

    "You take the shot and submit it. Her phone chimes happily as you complete the account creation."
    mc.name "There we go, that's it! Now I'll subscribe you to [lily.title]'s account and you can see all of your pictures together."
    mc.name "If you want you can event start posting your own pictures too."
    the_person "I don't know if I'm brave enough for that, but I'll think about it!"
    $ mc.change_locked_clarity(5)
    "You hand her phone back. She tucks it away and gives you a tight hug."
    the_person "Thank you [the_person.mc_title], I'd never have figured all of that out!"
    the_person "I'm so lucky to have a son like you!"


    $ the_person.add_role(instapic_role)
    $ the_person.event_triggers_dict["insta_known"] = True
    $ the_person.event_triggers_dict["mom_instapic_help_enabled"] = True
    $ clear_scene()
    call advance_time()
    return


label mom_instapic_alt_intro(the_person): #Triggers if she's ended up with an InstaPic account some other way.
    if the_person.event_triggers_dict.get("mom_instapic_help_enabled", False):
        return #We've already triggered this, we're just cleaning up the event.

    $ the_person.draw_person()
    the_person "[the_person.mc_title], I was wondering if I could ask a little favour from you..."
    mc.name "Of course [the_person.title], what do you need?"
    the_person "I had so much taking those pictures with you and [lily.title], I want to post some stuff like that to my own InstaPic page."
    if the_person.event_triggers_dict.get("insta_known", False):
        pass
    else:
        mc.name "You have an InstaPic account?"
        the_person "Oh, didn't I tell you? Here..."
        "She pulls out her phone and texts you her username."
        the_person "You don't have to follow me if you don't want to, I just post the occasional selfie. I know that's probably lame to hear from your mother."
        mc.name "I'd love to see what you post [the_person.title]. Now what did you need help with?"
        $ the_person.event_triggers_dict["insta_known"] = True

    the_person "I want to start taking better pictures; ones where I'm not doing it all in a mirror or holding my phone out."
    the_person "Some people use tripods and other gizmos, but I since you're around and you have all this experience helping [lily.title]..."
    "She trails off with a smile."
    mc.name "I get it. You need me to be your camera man."
    the_person "Only when you have the time, and it would mean a lot to me!"
    mc.name "Alright, I can't promise anything but I'll let you know if I have the time."
    $ mc.change_locked_clarity(5)
    $ the_person.change_happiness(5)
    "She pulls you into a warm hug."
    the_person "Thank you [the_person.title], you're such a good son."
    $ the_person.event_triggers_dict["mom_instapic_help_enabled"] = True
    $ clear_scene()
    return

# TODO: Add a "help Mom with her Instapic" option similar to Lily? Probably not super interesting at the level of corruption that you'd have reached at that point.

label mom_instapic_ban(the_person):

    $ the_person.event_triggers_dict["mom_instapic_banned"] = True
    $ the_person.draw_person()
    the_person "[the_person.mc_title], I need your help!"
    "[the_person.possessive_title] hurries over and thrusts her phone in your direction as soon as she sees you. She's clearly frustrated by something."
    mc.name "Okay, okay, just tell me what's wrong."
    the_person "I don't know! I tried to make a post on InstaPic and it's not letting me for some reason!"
    "You nod and open the app on her phone to investigate for yourself."
    "InstaPic" "One of your recent posts seems to violate our content policy! Please review our rules before posting. Ban time: 24 hours." (what_style = "text_message_style")
    mc.name "It says something you posted recently was against their rules. Any idea what that might be?"
    "She frowns and shakes her head. You open her recent postings and browse through them."

    $ old_outfit = the_person.outfit.get_copy()
    $ the_person.apply_outfit(lingerie_wardrobe.pick_random_outfit()) #TODO: See if we want to have any specific outfit stuff here.
    $ the_person.outfit.strip_to_tits()
    $ the_person.draw_person("kneeling1")
    $ mc.change_locked_clarity(15)
    "It doesn't take long to find the problem: A topless picture [the_person.possessive_title] tried to post yesterday."
    mc.name "Yeah, I think this is the issue."
    "She holds onto your arm and peers at her phone."
    the_person "I don't get it, what's the problem?"
    mc.name "InstaPic doesn't allow nudity."
    the_person "What? They're just boobs; I could walk around downtown without a shirt and wouldn't get in any trouble."
    the_person "And what about all the shirtless guys? Why aren't they banned?"
    $ the_person.apply_outfit()
    $ the_person.draw_person()
    "She takes her phone back and frowns."
    mc.name "I know it's not fair, but they get to make the rules."
    the_person "Well that's just silly. I'm going to send them a letter and complain."
    menu:
        "Tell her about OnlyFanatics." if not the_person.event_triggers_dict.get("onlyfans_known", False):
            mc.name "There is a different site that wouldn't care..."
            if the_person.has_role(onlyfans_role):
                the_person "Oh, I know I could post it on my OnlyFanatics, but I shouldn't have to!"
                mc.name "I... Your what?"
                the_person "My OnlyFanatics page? Didn't I tell you about it?"
                $ mc.change_locked_clarity(10)
                mc.name "No, I think I would remember my own mother having an OnlyFanatics page!"
                the_person "Don't be mad, I wasn't trying to hide it from you! I just thought you knew already."
                "She texts you a link to her account."
                the_person "There, you can check it out any time you want. Maybe you could even hold the camera?"
                mc.name "Sure thing [the_person.title], I'd be happy to."
                the_person "Great! Let me know when you have the time."
                $ the_person.event_triggers_dict["onlyfans_known"] = True

            else:
                the_person "Oh? Well that's good, I don't want to support InstaPic if they have such an archaic view of women and their bodies!"
                "She hands you her phone again."
                the_person "Show me!"
                "You download the OnlyFanatics app for her and open it up."
                mc.name "Now this might be a little strange, but don't overreact..."
                "She takes her phone back and blushes a little. The landing page is littered with half-naked previews of all the most popular girls."
                the_person "Is this... A porn site?"
                mc.name "No, no... Well, sort of. It's a way for women to take control of their sexuality and make a little money from it."
                mc.name "Think of it more like InstaPic with no posting rules and a tip jar for people who like what you're doing."
                "[the_person.possessive_title] seems convinced by this. She thinks about it for a long time before making a decision."
                $ the_person.change_slut(2)
                the_person "That's very forward thinking, I think I'll make an account."
                "She glances at her cell, then gives you a meek smile."
                the_person "Could you help me with it? I really don't know what I'm doing."
                mc.name "Sure [the_person.title]. It shouldn't take very long."
                "You take [the_person.possessive_title]'s phone again and go through the new account process."
                "After a few minutes you've filled out all of the basic information. You use the same username as her InstaPic account to make things simple for her."
                mc.name "Alright, the last step is to take a verification photo so they know the person posting the pictures is you."
                the_person "How does that work?"
                mc.name "You send them a picture of yourself holding some paper with your account name on it. Here..."
                "You get some paper, scribble down her username, and hand it to her."
                the_person "And that's it?"
                menu:
                    "Yep, that's it.":
                        mc.name "Yep, it's that simple."
                        "She holds the paper up and poses while you take the picture."
                        mc.name "Alright, that should be it. They say your account will be activated in a couple of hours."
                        the_person "I know I've said it already, but thank you!"

                    "And you need to be topless...":
                        mc.name "One last thing: you need to be topless."
                        if the_person.outfit.tits_visible():
                            the_person "Already done then!"
                        else:
                            the_person "What? Why would I need to do that?"
                            mc.name "It's, uh... It makes sure other people can't use an old picture of you hold up any piece of paper and photoshop it."
                            "She thinks about that for a moment before noding."
                            the_person "I didn't even think about that! That's very smart of them."
                            $ strip_list = the_person.outfit.get_tit_strip_list()
                            $ generalised_strip_description(the_person, strip_list)
                            $ the_person.break_taboo("tits_visible")
                            $ mc.change_locked_clarity(15)
                            "Now naked from the waist up, [the_person.possessive_title] holds up the paper and smiles while you take the picture."


                        mc.name "Alright, that should be it. They say your account will be activated in a couple of hours."
                        "She hurries over to your side, pressing her bare breasts into your shoulder to look at the pic you took."
                        the_person "It looks great. I know I've said it already, but thank you!"

                mc.name "Always happy to help [the_person.title]."
                the_person "Good, so if I need someone to hold my phone for some extra pictures..."
                mc.name "I'll let you know when I have time."
                the_person "You're the best son in the world!"
                "She takes her phone back and starts exploring the OnlyFanatics site."
                $ the_person.add_role(onlyfans_role)
                $ the_person.event_triggers_dict["onlyfans_known"] = True
                $ the_person.apply_outfit()


            $ mom_onlyfans_help_action = Action("Help her with OnlyFanatics.{image=gui/heart/Time_Advance.png}", mom_onlyfans_help_requirement, "mom_onlyfans_help", is_fast = False)
            $ the_person.get_role_reference(mother_role).actions.append(mom_onlyfans_help_action)

        "Wish her luck.":
            mc.name "Right, good luck with that."
            "She nods with determination."
            the_person "Thank you for trying to help out."
            #TODO: Add some way of restarting this if she gains the Onlyfans role some other way.

    $ clear_scene()
    return

label mom_onlyfans_help(the_person):
    $ the_person.event_triggers_dict["onlyfans_help_today"] = True

    mc.name "Did you still want help with your OnlyFanatics [the_person.title]."
    if not mom_bedroom.has_person(the_person):
        the_person "Yes, if you have the time. Come with me."
        "You follow [the_person.possessive_title] to her bedroom."
        $ mc.location.move_person(the_person, mom_bedroom) # Make sure she's in her bedroom so we can have the proper sex props
    the_person "Close the door, please."
    "You shut her bedroom door while she pulls her phone out of her purse and hands it over to you."
    the_person "You get that camera ready while I get changed..."
    $ lingerie = lingerie_wardrobe.pick_random_outfit()
    $ generalised_strip_description(the_person, the_person.outfit.get_full_strip_list())
    $ mc.change_locked_clarity(10)
    "You enjoy the show as [the_person.possessive_title] gets naked, then starts to pull on a skimpy lingerie set."
    $ the_person.apply_outfit(lingerie)
    $ the_person.draw_person()
    "Once she's dressed she turns to you and strikes a flirty pose."
    the_person "How do I look?"
    mc.name "Perfect, [the_person.title]."
    the_person "You're just saying that to make me feel good. This is really fun though, I acted like this when I was younger."
    the_person "It's nice to know some people still think I'm sexy. Anyways, you aren't hear to listen to me ramble on. Let's get started!"
    "[the_person.possessive_title] strikes a few poses around the room, leaning playfully over her bed or against the walls."
    $ the_item = the_person.outfit.get_upper_top_layer()
    if not the_person.outfit.tits_visible() and the_item is not None:
        the_person "What do you think [the_person.mc_title], should I stop teasing them?"
        if the_person.has_large_tits():
            $ mc.change_locked_clarity(5)
            "She cups her breasts and jiggles them inside of her [the_item.display_name]."
        else:
            $ mc.change_locked_clarity(5)
            "She presses her hands against her breasts and plays with them through her [the_item.display_name]."

        mc.name "Yeah, I think you should. Take that thing off."
        $ generalised_strip_description(the_person, the_person.outfit.get_tit_strip_list())
        $ mc.change_locked_clarity(5)

    "You get close to [the_person.title] and get some good pictures of her tits. She blushes a little and glances away from the camera."
    the_person "Well thank you [the_person.mc_title], I think that will do for today!"
    $ slut_requirement = 50 - the_person.get_opinion_score(["showing her tits", "showing her ass"]) * 5
    if the_person.has_taboo("bare_pussy"):
        $ slut_requirement += 10
    $ slut_token = get_red_heart(slut_requirement)
    menu:
        "Convince her to keep going." if the_person.effective_sluttiness() >= slut_requirement:
            mc.name "Don't stop now, you're doing great!"
            $ the_item = the_person.outfit.get_lower_top_layer()
            if not the_person.outfit.vagina_visible() and the_item is not None:
                mc.name "Lie down and take off your [the_item.display_name] and show off your ass. They'll go crazy for that..."
                the_person "Well... Okay, just a few more pictures."
                $ generalised_strip_description(the_person, the_person.outfit.get_vagina_strip_list())
                $ mc.change_locked_clarity(10)
            else:
                mc.name "Lie down and show off your ass. They'll go crazy for that."
            $ the_person.draw_person(position = "doggy")
            "[the_person.possessive_title] hops onto her bed and points her butt in your direction."
            mc.name "Okay, now shake it for me [the_person.title]!"
            "You switch her phone into video mode and start recording."
            if the_person.get_opinion_score("showing her ass") > 0:
                "She doesn't need any convincing. [the_person.possessive_title] shakes her hips aggressively, twerking her ass for the camera."
            else:
                the_person "Uh, like this?"
                "She tries her best, wiggling her hips in a poor attempt at twerking. Luckily her \"natural talent\" makes up for her lack of experience."
            menu:
                "Smack her ass.":
                    "You hold her phone in one hand and give her butt cheek a hard open-palmed slap."
                    $ mc.change_locked_clarity(10)
                    "There's a satisfying, sharp smack as you connect and send her ass jiggling even more."
                    the_person "Ah! Hey..."
                    mc.name "Sorry, but it looks really good on camera."
                    if the_person.get_opinion_score("showing her ass") > 0:
                        the_person "It does? Well then... Do it again!"
                        $ mc.change_locked_clarity(10)
                        "She lowers her shoulders into the bed and stifles her own soft yelps as you spank her butt a few more times."
                    else:
                        the_person "Well it hurts too!"
                        mc.name "The pains we go through for art, huh?"
                        "You give her butt a lighter slap. She grumbles, but doesn't complain any more."

                "Show off her pussy.":
                    "You crouch down to make sure the camera gets a good look of her pussy too."
                    the_person "Ah... This is hard work!"
                    mc.name "Just keep going, you're doing great!"

            "[the_person.possessive_title] slows down, then stops shaking her hips entirely. She's a little out of breath after all that effort."
            the_person "That... should do it. Oh wow, that's a good workout!"
            #TODO: Have an option to get your cock out (/have her notice?) and lead into the option to record her giving you a handjob/blowjob/fucking you.
            $ slut_requirement = 60 - the_person.get_opinion_score("incest") * 10
            $ slut_token = get_red_heart(slut_requirement)
            menu:
                "Get your cock out." if the_person.effective_sluttiness() >= slut_requirement:
                    "You've been hard since [the_person.possessive_title] got undressed, and you can't ignore it any longer."
                    "You keep the phone steady in one hand and unzip your pants with the other, letting your cock spring free."
                    the_person "Now, let's see what those picutres look li..."
                    $ the_person.draw_person(position = "sitting")
                    "[the_person.title] spins around to sit on the edge of her bed, halting when she sees your hard dick in her face."
                    the_person "[the_person.mc_title], what are you doing?"
                    mc.name "I'm not made of stone, that was hot."
                    "You hold your shaft with your free hand and stroke it slowly."
                    mc.name "Come on, let's make an extra fun video for everyone."
                    $ mc.change_locked_clarity(10)
                    if the_person.get_opinion_score("incest") <= 0:
                        "She reaches out uncertainly, brushing her fingers over the tip as she thinks."
                        the_person "It would be mean of me to leave you like this, so worked up..."
                        "[the_person.possessive_title] wraps her fingers around your cock and starts to stroke it for you."
                    else:
                        "She bites her lip playfully and reaches out, wrapping her fingers around your cock."
                        the_person "It would be mean of me to leave you worked up like this..."

                    $ blowjob_requirement = 60 - the_person.get_opinion_score("giving blowjobs") * 5
                    if the_person.has_taboo("sucking_cock"):
                        $ blowjob_requirement += 10
                    $ blowjob_token = get_red_heart(blowjob_requirement)

                    $ sex_requirement = 80 - the_person.get_opinion_score("vaginal sex") * 5
                    if the_person.has_taboo("vaginal_sex"):
                        $ sex_requirement += 10
                    $ sex_token = get_red_heart(sex_requirement)

                    $ anal_requirement = 70 - the_person.get_opinion_score("anal sex") * 5
                    if the_person.has_taboo("anal_sex"):
                        $ anal_requirement += 10
                    $ anal_token = get_red_heart(anal_requirement)

                    menu:
                        "Enjoy the handjob.":
                            "You sigh happily and let her stroke you off for a few moments."
                            the_person "Do you like that? You just let me take care of this big, hard cock for you."
                            mc.name "Thanks [the_person.title], that feels amazing."
                            "You try to focus on keeping her centered in the video, but her soft hands are making it very hard to concentrate."
                            call fuck_person(the_person, private = True, start_position = handjob, skip_intro = True, girl_in_charge = True)


                        "Tell her to suck it." if the_person.effective_sluttiness() >= blowjob_requirement:
                            mc.name "Fuck, I want you to suck it [the_person.title]."
                            "You try and focus on keeping her centered on the camera, but her soft hands are making it very hard to concentrate."
                            "She looks up at you and smiles playfully."
                            the_person "Really? Do you need it that badly?"
                            "[the_person.possessive_title] leans forward and kisses the tip a couple of times. Your cock twitches in response."
                            the_person "I can't say no to you when you're like this. Here, let me take care of you..."
                            $ the_person.draw_person(position = "kneeling1")
                            "She slides off the bed and onto her knees in front of you. With one hand holding your shaft steady she starts to slip your cock into her mouth."
                            mc.name "Fuck that's good. Don't forget to look up at the camera."
                            "[the_person.title] does her best, tilting her head up to try and maintain eye contact with the audience while she sucks on your dick."
                            call fuck_person(the_person, private = True, start_position = blowjob, skip_intro = True, girl_in_charge = True)

                        "Tell her to suck it.\nRequires: [blowjob_token] (disabled)" if the_person.effective_sluttiness() < blowjob_requirement:
                            pass

                        "Fuck her." if the_person.effective_sluttiness() >= sex_requirement:
                            mc.name "Fuck, I need to be inside you [the_person.title]."
                            "You try and focus on keeping her centered on the camera, but her soft hands are making it very hard to concentrate."
                            "She looks up at you and smiles playfully."
                            the_person "Do you really need it that badly? Well then, I'll just have to take care of you sweetheart..."
                            $ the_person.draw_person(position = "doggy")
                            "She climbs onto her bed and shakes her butt in your direction."
                            call condom_ask(the_person)
                            if not _return:
                                the_person "Well if you won't wear a condom you'll just have to be satisfied with my mouth. Okay?"
                                "[the_person.possessive_title] doesn't wait for a response. She gets onto her knees in front of you and slides the tip of your cock into her mouth."
                                call fuck_person(the_person, private = True, start_position = handjob, skip_intro = True, girl_in_charge = True, skip_condom = True)
                            else:
                                "You hop up behind her, tap your cock experimentally on her butt cheeks a few times, then lower it to rub tip along her went cunt."
                                "You grab her ass and pull it to the side, giving the camera a view of her pussy lips spreading open as you push into her."
                                the_person "Oooooh."
                                "She lowers her head into a pillow and moans as you slide home."
                                call fuck_person(the_person, private = True, start_position = doggy, start_object = mc.location.get_object_with_name("bed"))

                        "Fuck, her.\nRequires: [sex_token] (disabled)" if the_person.effective_sluttiness() < sex_requirement:
                            pass

                        "Anal her." if the_person.effective_sluttiness() >= anal_requirement:
                            mc.name "Fuck, I need you so badly [the_person.title]. Come on, let me fuck you."
                            if the_person.has_taboo("vaginal_sex") and not the_person.has_taboo("anal_sex"):
                                the_person "Do you really need me so badly? well..."
                                $ the_person.draw_person(position = "doggy")
                                "She climbs up onto the bed and shakes her ass in your direction."
                                the_person "You know you can't use my pussy, so you'll just have to fuck my butt, okay?"
                            elif not the_person.has_taboo("vaginal_sex"):
                                "She climbs up onto the bed and shakes her ass in your direction."
                                the_person "Well then come and fuck me. My pussy's wet and waiting for you."
                                "You tap your cock on her ass a few times, then press the tip against her tight butthole. You do the best to capture everything on camera."
                                mc.name "I was thinking of something else..."
                                if the_person.has_taboo("anal_sex"):
                                    the_person "Really? I don't know, is that something you want?"
                                    "You press forward a little, teasing her hole."
                                    mc.name "Yeah. Ready?"
                                    "She seems unsure, but eventually nods her concent."
                                else:
                                    the_person "Then do it. You know it's all yours."
                            else:
                                "She climbs up onto the bed and shakes her ass in your direction."
                                the_person "Come on then, pick a hole and fuck me!"

                            "You hold onto her hips with one hand and her phone with the other."
                            "You capture in wonderful detail the way the head of your cock spreads open her ass as you push yourself into her."
                            call fuck_person(the_person, private = True, start_position = doggy_anal, start_object = mc.location.get_object_with_name("bed"))

                        "Anal her.\nRequires [anal_token] (disabled)" if the_person.effective_sluttiness() < anal_requirement:
                            pass

                    $ the_report = _return
                    if the_report.get("creampies", 0) > 0:
                        "You grab [the_person.possessive_title]'s legs and spread them open."
                        "You bring the camera close to her pussy and make sure to capture the moment your cum starts to drip out of it."
                        if not the_person.event_triggers_dict.get("preg_knows", False): #Don't trigger it if she's pregnant
                            menu:
                                "Interview her.":
                                    mc.name "Well [the_person.title], what do you think just happened?"
                                    "You use your thumb to spread open her cunt, sending a gush of sperm onto the bed sheets."
                                    if the_person.on_birth_control:
                                        $ the_person.update_birth_control_knowledge()
                                        "She raises her head and smiles weakly at the camera."
                                        the_person "Probably nothing, I take an amazing little pill that lets me get creampied as much as I want."

                                    else:

                                        if the_person.has_role(breeder_role) or the_person.get_opinion_score(["bareback sex", "creampies"]) > 0: #Highly enthusiastic.
                                            $ the_person.update_birth_control_knowledge()
                                            the_person "I think I just got fucked and knocked up!"
                                            "She arches her back and sighs happily."
                                            the_person "I hope I'm right, I really wanted to get bred today."

                                        elif the_person.get_opinion_score("creampies") < 0: #Unhappy with you.
                                            the_person "Cut it out [the_person.mc_title], this isn't funny. Ugh..."
                                            "She reaches a hand between her legs and groans unhappily when she feels your semen dripping out of her."
                                            the_person "What a mess..."

                                        else: #Neutral
                                            the_person "Cut it out [the_person.mc_title], this is serious!"
                                            $ the_person.update_birth_control_knowledge()
                                            the_person "What if I get pregant? It won't be funny then!"
                                            mc.name "Then it's a good thing we caught this special moment on film. These are special family memories."
                                            "She sighs dramatically, her anger mostly for show, and sinks back into the pillows on the bed."

                                "Finish up.":
                                    "With the moment imortalized you end the video and chuck her phone onto the pillow beside her."
                    elif the_report.get("facials", 0) > 0:
                        "You bring the camera close to [the_person.possessive_title]'s face, capturing it in all it's cum-covered glory."
                        if the_person.get_opinion_score("cum facials") > 0:
                            "She runs a finger through the cum puddles, dragging it around her face sensually."
                            the_person "Oh look at this, I'm absolutely covered in his cum!"
                        elif the_person.get_opinion_score("cum facials") < 0:
                            "She reaches a hand out and tries to push the camera away, frowning unhappily."
                            the_person "Cut it out, now I have to go get all of this cleaned up. Ugh."
                        else:
                            "She holds a hand up and tries to shield herself from the camera."
                            the_person "[the_person.mc_title], cut it out. You're embarrassing me!"
                            mc.name "Relax, you look great like that."

                    elif the_report.get("body_cum", 0) > 0:
                        "You bring the camera close to [the_person.possessive_title]'s body, giving it a good look at your cum splattered all over her."
                        #TODO: Add some opinion based variants
                    elif the_report.get("girl orgasms",0) > 0:
                        "You bring the camera up to [the_person.possessive_title]'s face, giving it a good look at her post climax face."
                        #TODO: Add some opion based variants
                    elif the_report.get("guy orgasms", 0) > 0:
                        pass #TODO: Talk about how you're exhausted; must have climaxed in some sort of boring way or in a condom
                    else:
                        pass #TODO: Boring outro, you didn't actually do much.


                    "Happy with the results, you end the video and lie down next to [the_person.possessive_title] to catch your breath."
                    the_person "Do you think they'll like it? The OnlyFanatics people, I mean."
                    mc.name "Yeah, I think they will. Did you have fun?"
                    $ the_person.change_slut(1)
                    $ the_person.draw_person(position = "sitting")
                    "She nods happily and lifts herself up onto one arm to look at you."

                    the_person "It was a good time. Now, can you help me post all of this? I really am helpless..."
                    "You grab her phone and post the video to her Onlyfanastics page."






                "Get your cock out.\nRequires:[slut_token] (disabled)" if the_person.effective_sluttiness() < slut_requirement:
                    pass

                "Stop for today.":
                    mc.name "Alright, well I think you've got some really good options for posting here."
                    $ the_person.draw_person()
                    "You hand her phone back. She scrolls through them and nods approvingly."
                    the_person "Yeah, these look great! You're a wizard [the_person.mc_title], I don't know how you do it."
                    mc.name "It's not hard when you're working with such a talented model."
                    "She puts her arms around you and squeezes you tight, pressing her bare boobs against you in the process."
                    $ the_person.change_slut(1, 60)
                    $ the_person.change_love(1)
                    the_person "Really. Thank you. Now, can you help me post these? I really am helpless..."
                    "You help her post all of her new pictures to her OnlyFanatics page."


        "Convince her to keep going.\nRequires: [slut_token] (disabled)" if the_person.effective_sluttiness() < slut_requirement:
            pass

        "Stop for today.":
            mc.name "Alright, well I think you've got some really good options for posting here."
            "You hand her phone back. She scrolls through them and nods approvingly."
            the_person "Yeah, these look great! You're a wizard [the_person.mc_title], I don't know how you do it."
            mc.name "It's not hard when you're working with such a talented model."
            "She puts her arms around you and squeezes you tight, pressing her bare boobs against you in the process."
            $ the_person.change_slut(1, 50)
            $ the_person.change_love(1)
            the_person "Really. Thank you. Now, can you help me post these? I really am helpless..."
            "You help her post all of her new pictures to her OnlyFanatics page."

    if not the_person.event_triggers_dict.get("onlyfans_sister_jealous", False):
        $ the_person.event_triggers_dict["onlyfans_sister_jealous"] = True
        $ sister_instapic_jealous_event = Action("Lily instapic jealous", sister_instapic_jealous_requirement, "sister_instapic_jealous", requirement_args = day + renpy.random.randint(3,5))
        $ lily.on_talk_event_list.append(sister_instapic_jealous_event)

    $ the_person.event_triggers_dict["onlyfans_help_count"] = the_person.event_triggers_dict.get("onlyfans_help_count", 0) + 1

    $ the_person.apply_outfit()
    $ clear_scene()
    call advance_time()
    return

label sister_instapic_jealous(the_person): #Triggers 3-5 days after you've helped mom with her first Onlyfans shoot.
    $ the_person.draw_person()
    "[the_person.possessive_title] is staring at her phone when you approach her."
    mc.name "Hey [the_person.title]."
    the_person "Hi..."
    "She barely glances up from her phone."
    the_person "Have you looked at [mom.title]'s InstaPic account?"
    menu:
        "Yeah, I check it all the time.":
            mc.name "Yeah, I check it all the time. Why?"

        "No, not lately.":
            mc.name "Not lately, no. What's up?"

    the_person "Her follower count is huge! It took me months to get this many followers, her account has exploded since last week!"
    "She pouts and keeps scrolling through [mom.possessive_title]'s account."
    the_person "I just don't get how she's doing it! She isn't even showing off her tits very well!"
    menu:
        "Tell her about OnlyFanatics.":
            mc.name "Not on InstaPic she doesn't..."
            the_person "What do you mean?"
            mc.name "You know she has an OnlyFanatics page, right?"
            if the_person.has_role(onlyfans_role):
                the_person "She does? Why didn't she tell me about that?"
                "You shrug."
                mc.name "Want to see her account?"
                the_person "Duh! Does she have more subscribers than me there too?"
                "[the_person.title] stands close to you and brings up the OnlyFanatics app."
                "You give her [mom.title]'s account name and the two of you spend a few minutes browsing through it."
                the_person "Oh my god, I didn't know she was such a slut!"
                "[the_person.possessive_title] smiles mischievously."
                the_person "I'm never going to let her hear the end of this! Ha!"
            else:
                "[the_person.possessive_title] opens and closes her mouth a few times, unsure what to say."
                the_person "What? You're kidding, right?"
                mc.name "No, seriously. Want to see her account?"
                the_person "You perv, you've been watching her haven't you!"
                "You shrug. [the_person.title] shakes her head in disbelief, but pulls close to you so she can look at your phone."
                the_person "Fine, just show me."
                "You pull up the OnlyFanatics app and navitage to [mom.possessive_title]'s page."
                the_person "Oh my god she really does... Wait, is that why so many people have started following her on InstaPic?"
                mc.name "You're the expert in these things, you tell me."
                the_person "That slut! Everyone's following her because she's showing them her tits!"
                "[the_person.possessive_title] sounds more relieved rather than angry."
                the_person "Well if she's doing it then she can't complain about me. Thanks [the_person.mc_title]."
                mc.name "So you're going to start an OnlyFanatics too?"
                "She bites her lip playfully and nods."
                the_person "I'm going to get so many followers, it's going to be insane."
                menu:
                    "Offer to help.":
                        mc.name "Let me know if you need a hand with that, sounds like it'll be interesting."
                        the_person "You're so predictable. Yeah, I'll let you know."
                        the_person "Or maybe I should start making you pay to see my tits? Hmm, I'll have to think about that!"

                    "Wish her luck.":
                        mc.name "Good luck with that."
                        the_person "Oh, you don't want to help? You'll get to see my boobies, and you won't even have to pay for it."
                        mc.name "I don't know, I've already seen them plenty of times."
                        the_person "Oh shut up. Whatever, I'm sure you'll come running when I say I need help."
                $ the_person.event_triggers_dict["onlyfans_known"] = True
                $ the_person.add_role(onlyfans_role)

            #TODO: Add a flag and have this trigger special stuff in the normal instapic shared shoot to "make some stuff for your Onlyfans.

        "Don't tell her.":
            mc.name "I don't know [the_person.title]. Maybe people just appreciate an older woman."
            the_person "Maybe... Ugh, what do guys like about MILF's anyways? I have better tits, a nicer butt, and a cuter pussy!"
            the_person "Whatever! It's just a fad."

    "She puts her phone away and gives you her full attention."
    call talk_person(the_person)
return

label mom_sister_onlyfans_help(the_person):
    #TODO: Mom asks you to get Lily and have her help with some lingerie.
    #TODO: -> Maybe a matching set? Something like "It was buy-one get-one free, so I got one in her size".

    #TODO: FIrst time Lily is surprised, helps with some lingerie stuff.
    #TODO: After that do stuff similar to normal help, but with both of them.


    #TODO: Afterwards Lily asks you to help her set up an Onlyfans as well (Also: have a version where she already has one set up)
    return






#TODO: Mom starts doing onlyfans, asks _Lily_ to help her with some lingerie shoot.
#TODO; Lily is surprised her mom is doing this, doesn't want to be outdone, starts an Onlysfans account.
#TODO: Extra Instapic, Onlyfans, DikDok content.
