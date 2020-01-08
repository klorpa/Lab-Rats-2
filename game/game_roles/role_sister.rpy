##########################################
# This file holds all of the role requirements and labels for the sister role.
##########################################

init -2 python:
    #SISTER ACTION REQUIREMENTS#
    def sister_intro_crisis_requirements(the_person, day_trigger):
        if time_of_day == 4 and mc.location == bedroom and day >= day_trigger: #We use time == 4 because we want it to trigger during our night/day transition (ie. when you're guaranteed to be at home)
            return True
        return False

    def sister_reintro_action_requirement(the_person):
        if mc.business.event_triggers_dict.get("sister_needs_reintro"):
            return True
        return False

    def sister_serum_test_requirement(the_person):
        if not mc.business.event_triggers_dict.get("sister_serum_test", False):
            return False
        elif mc.business.funds < 50:
            return "Requires: $50"
        else:
            return True

    def sister_strip_intro_requirement(the_person): #Note that this only ever triggers once, so we don't need to worry if it will retrigger at any point.
        if time_of_day == 4 and mc.location == bedroom:
            if the_person.sluttiness >= 30 and mc.business.event_triggers_dict.get("sister_serum_test_count") and mc.business.event_triggers_dict.get("sister_serum_test_count") >= 4:
                return True
        return False

    def sister_strip_reintro_requirement(the_person):
        if not mc.business.event_triggers_dict.get("sister_strip_reintro",False):
            return False
        elif mc.location != lily_bedroom:
            return False
        elif len(lily_bedroom.people) > 1:
            return False
        elif the_person.sluttiness < 30:
            return "Requires: " + get_red_heart(30)
        else:
            return True

    def sister_strip_requirement(the_person): #She'll only strip if you're in her bedroom and alone.
        if not mc.business.event_triggers_dict.get("sister_strip",False):
            return False
        elif mc.location != lily_bedroom:
            return False
        elif len(lily_bedroom.people) > 1:
            return False
        elif the_person.sluttiness < 30 or mc.business.funds < 100:
            return "Requires: $100, " + get_red_heart(30)
        else:
            return True

    def instathot_intro_requirement(the_person): #This action sits in her room
        if the_person.sluttiness < 20:
            return False
        elif the_person not in lily_bedroom.people:
            return False
        elif __builtin__.len(lily_bedroom.people) > 1:
            return False
        else:
            return True


    def instathot_requirement(the_person):
        if lily not in lily_bedroom.people:
            return False
        elif __builtin__.len(lily_bedroom.people) > 1:
            return False
        elif time_of_day == 4:
            return "Too late to take pictures."
        else:
            return True


#SISTER ACTION LABELS#

label sister_intro_crisis_label(the_person):
    #This is a mantatory crisis, so we assume that our requirements are tight enough to always trigger correctly. If you want to do crisis requirement checks here you need to re-add the crisis to the mandatory list!
    $ bedroom.show_background()
    "There's a knock at your bedroom door."
    mc.name "Come in."
    $ the_person.draw_person()
    the_person.char "Hey [the_person.mc_title], do you have a moment?"
    mc.name "Sure, what's up?"
    "[the_person.possessive_title] steps into your room and closes the door behind her."
    the_person.char "I wanted to say I'm really impressed with how your business is going. It must be really exciting to be your own boss now."
    mc.name "It's certainly been challanging, that's for sure."
    the_person.char "And... Well, I've been so busy with school that I haven't had a chance to get a job like Mom's been wanting..."
    mc.name "Oh no, I can see where this is going."
    the_person.char "If you could just give me a {i}tiny{/i} bit of cash I could show Mom I can take care of myself."
    mc.name "But you can't, apparantly."
    the_person.char "Please? Please please please, [the_person.mc_title]? Maybe there's some extra work I could do? I could..."
    "She gives up and shrugs."
    the_person.char "Help you science all that science stuff?"
    mc.name "I don't think that's really where I need help. But..."
    menu:
        "Ask [the_person.title] to test serum for you.":
            the_person.char "But...? Come on [the_person.mc_title], I really need your help."
            mc.name "Well, at the lab we've been running some experiements, but we need some test subjects."
            mc.name "I can bring home some of the stuff we're working on and if you let me test it on you I can pay you for it."
            the_person.char "It's not going to turn me into a lizard or something, right?"
            mc.name "Obviously not. It's just a liquid that you'd need to drink, then I'll watch to see how it affects you over the next few hours."
            the_person.char "What is it going to do?"
            mc.name "That's what we're trying to find out."
            $ the_person.draw_person(emotion = "happy")
            "[the_person.possessive_title] thinks about it for a moment, then nods."
            the_person.char "Okay, but I want $50 each time."
            mc.name "You drive a hard bargin sis. You've got a deal."
            "You shake on it."
            $ the_person.change_obedience(5)
            the_person.char "Thank you so much [the_person.mc_title]. Uh, if Mom asks just say I got a part time job."
            mc.name "Sure thing. I'll come see you when I have something for you to test."
            "[the_person.title] gives you one last smile then leaves your room, shutting the door behind her."
            $ mc.business.event_triggers_dict["sister_serum_test"] = True

        "Ask [the_person.title] to leave you alone.":
            the_person.char "But...?"
            mc.name "But I was just about to head to bed, so if you could let me get some sleep that would be a huge help."
            $ the_person.draw_person(emotion = "sad")
            $ the_person.change_happiness(-5)
            "[the_person.title] pouts and crosses her arms. She leaves your room in a huff."
            $ mc.business.event_triggers_dict["sister_needs_reintro"] = True

    $ renpy.scene("Active")
    return

label sister_reintro_label(the_person):
    #If you turn your sister away the first time you can approach her and ask to have her test serums anyways.
    mc.name "So [the_person.title], are you still looking for some work to do?"
    $ the_person.draw_person(emotion = "happy")
    the_person.char "Oh my god yes! Do you have something for me to do?"
    mc.name "Well, at the lab we've been running some experiements, but we need some test subjects."
    mc.name "I can bring home some of the stuff we're working on and if you let me test it on you I can pay you for it."
    the_person.char "It's not going to turn me into a lizard or something, right?"
    mc.name "Obviously not. It's just a liquid that you'd need to drink, then I'll watch to see how it affects you over the next few hours."
    the_person.char "What is it going to do?"
    mc.name "That's what we're trying to find out."
    $ the_person.draw_person(emotion = "happy")
    "[the_person.possessive_title] thinks about it for a moment, then nods."
    the_person.char "Okay, but I want $50 each time."
    mc.name "You drive a hard bargin sis. You've got a deal."
    "You shake on it."
    $ the_person.change_obedience(5)
    the_person.char "Thank you so much [the_person.mc_title]. Uh, if Mom asks just say I got a part time job."
    mc.name "Sure thing. I'll let you know when I have something for you to test."
    $ mc.business.event_triggers_dict["sister_needs_reintro"] = False
    $ mc.business.event_triggers_dict["sister_serum_test"] = True
    return

label sister_serum_test_label(the_person):
    #Give your sister some serum to test for cash.
    mc.name "Hey [the_person.title], I have something for you to test out for me."
    the_person.char "Alright, $50 and I'll try it."
    call give_serum(the_person) from _call_give_serum_7
    if _return:
        $ mc.business.funds += -50
        "You give [the_person.possessive_title] the cash and the serum. She puts the money away then drinks the serum, handing back the empty vial."
        $ the_person.change_obedience(1)
        the_person.char "Easiest fifty bucks I've ever earned. I guess you can hang around and keep an eye on me if it's important for your research."
        if mc.business.event_triggers_dict.get("sister_serum_test_count"):
            $ mc.business.event_triggers_dict["sister_serum_test_count"] += 1
        else:
            $ mc.business.event_triggers_dict["sister_serum_test_count"] = 1

    else:
        mc.name "Sorry [the_person.title], I guess I don't actually have anything for you to test."
        the_person.char "Ugh, come on [the_person.mc_title], you know I need the money!"
        mc.name "I'll find something for you to test, promise."
    return

label sister_strip_intro_label(the_person):
    #Give your sister some cash in exchange for her stripping. Higher sluttiness means she'll strip more (for less).
    $ bedroom.show_background()
    "There's a knock at your bedroom door."
    mc.name "Come in."
    $ the_person.draw_person()
    the_person.char "Hey [the_person.mc_title], can I talk to you about something?"
    "[the_person.possessive_title] comes into your room and shuts the door behind her. She seems nervous, avoiding eye contact as she comes closer."
    mc.name "Any time, what's up?"
    the_person.char "You know how I've been testing some of that lab stuff you make? For money?"
    mc.name "Yeah."
    the_person.char "Well I've been out shopping, and Mom would {i}kill{/i} me if she knew how much I was spending, so I was hoping you could pay me some more."
    mc.name "Sorry [the_person.title], I don't have anything for you to test right now."
    $ the_person.draw_person(emotion = "sad")
    the_person.char "Oh come on [the_person.mc_title], don't you have anything I could do? I really need the money now."
    "[the_person.possessive_title] puts her arms behind her back and pouts at you."
    menu:
        "Pay her to strip for you.":
            call strip_explanation(the_person) from _call_strip_explanation


        "Tell her to leave.":
            mc.name "I just don't have anything to give you [the_person.title]. I promise if I think of anything I'll come to you right away."
            the_person.char "Ugh... fine."
            "She turns and leaves your room, disappointed."
            $ the_person.change_happiness(-5)
            $ mc.business.event_triggers_dict["sister_strip_reintro"] = True

    $ renpy.scene("Active")
    return

label sister_strip_reintro_label(the_person):
    mc.name "I've been thinking about some stuff you could do for me [the_person.title]. Are you still interested in earning some more money?"
    $ the_person.draw_person(emotion = "happy")
    the_person.char "Yes! What do you want me to do?"

    call strip_explanation(the_person) from _call_strip_explanation_1

    $ mc.business.event_triggers_dict["sister_strip_reintro"] = False
    return

label strip_explanation(the_person):
    #Pulls out the explanation part of the strip intro so it's not duplicated
    mc.name "I've been busy getting my business running and earning all of this money I'm going to be paying you, so I haven't had a chance to meet many people."
    mc.name "It's been a while since I was able to just appreciate the looks of a hot woman."
    the_person.char "What are... what are you suggesting?"
    mc.name "I'll pay you if you just stand around and let me look at you. Maybe take some of your clothing off, if you're comfortable with it."
    the_person.char "So you want me to give you a strip show?"
    "You nod."
    "[the_person.possessive_title] seems surprised, but not particularly offended by the idea. She takes a long moment to consider it."
    the_person.char "Okay, I'll do it. I want $100 up front, plus a little extra if you want me to take anything off."
    mc.name "I think that's reasonable."
    $ the_person.change_obedience(5)
    $ mc.business.event_triggers_dict["sister_strip"] = True
    the_person.char "And obviously you can't touch me. Or yourself. And you can {i}never{/i} tell Mom about it."
    mc.name "Don't worry [the_person.title], I promise I won't make it weird."
    "[the_person.title] nods. There's a long silence before she speaks again."
    the_person.char "So... do you want me to do it for you now?"
    menu:
        "Ask her to strip for you." if mc.business.funds >= 100:
            mc.name "I don't see why not."
            $ mc.business.funds += -100
            "You pull a hundred dollars out of your wallet and hand it over to [the_person.possessive_title]. She tucks it away and gets ready."
            call pay_strip_scene(the_person) from _call_pay_strip_scene

        "Ask her to strip for you.\n{size=22}Requires: $100{/size} (disabled)" if mc.business.funds < 100:
            pass

        "Not right now.":
            mc.name "Not right now. I'll come find you if I'm interested, okay?"
            the_person.char "Okay. Thanks for helping me out [the_person.mc_title], you're a life saver."
            "[the_person.title] leaves your room and closes the door behind her."
    return


label sister_strip_label(the_person):
    #A short intro so that we can reuse the pay_strip_scene with other characters if we want.
    mc.name "So [the_person.title], are you interested in earning a hundred dollars?"
    if the_person.sluttiness < 50:
        the_person.char "Oh, do you want me to... show off for you?"
    else:
        the_person.char "You want me to strip down for you?"
    $ mc.business.funds += -100
    "You nod and sit down on [the_person.possessive_title]'s bed. She holds her hand out and you hand over her money."
    "She tucks the money away and gets ready in front of you."
    call pay_strip_scene(the_person) from _call_pay_strip_scene_1
    return

label sister_instathot_intro_label(the_person):
    # Your sister needs you to take pictures for her.
    # She's got an insta-pic (genius, they'll never guess!) account and wants to be an "influencer"
    # Triggers at some point when you go into your sisters room. You catch her taking pictures for insta-pic, but she doesn't mind and explains what she's doing.
    # Adds a random event where Lily posts insta-pics, similar to your mom sending you selfies.


    # Actually, let's have her start with a relatively tame outfit and grow into really sexy ones.
    "You open the door to [the_person.possessive_title]'s room."
    $ the_person.draw_person(position = "kneeling1")
    "She's posed on her bed, holding her phone high up in one hand to take a selfie. She startles when you come in, standing up quickly before calming down."
    $ the_person.draw_person()
    the_person.char "Oh... It's just you. Come in and close the door, please."
    "You step inside and close the door behind you."
    the_person.char "You scared me, I thought you were [mom.title] for a second."
    mc.name "Why would you be worried about her? What are you up to?"
    the_person.char "Nothing, she just wouldn't understand and I don't want to make it a big thing."
    "She holds up her phone and smiles."
    the_person.char "But if you have to know, I made an account on insta-pic and I'm putting up some pictures for my fans."
    mc.name "Insta-pic?"
    the_person.char "Oh my god, how old are you again? It's a social media thing, people post pictures and follow other people."
    the_person.char "If you're popular some companies will even pay for you to wear their clothes or show off their stuff."
    mc.name "So how popular are you?"
    the_person.char "Well... Not very, yet, but I just started posting! I'm still figuring out what people want to see."
    "Looking at her outfit it seems like she has the right idea."
    the_person.char "Since you're here, could you use my phone and take some pictures? It's hard doing it all myself."
    menu:
        "Help her.":
            mc.name "Fine, give it here."
            $ the_person.change_happiness(5)
            the_person.char "Yay, thank you [the_person.mc_title]!"
            "She hands you her phone and strikes a pose."
            $ the_person.draw_person(emotion = "happy")
            the_person.char "Got it? Okay. Now get one like I just noticed you."
            $ the_person.draw_person(emotion = "happy", position = "walking_away")
            "It seems like no shot is ever perfect, but eventually she's satisfied and takes her phone back with a smile."
            $ the_person.draw_person()
            $ the_person.change_love(2)
            the_person.char "Thank you so much, you're the best!"
            "She gives you a quick kiss on the cheek."
            the_person.char "It's so nice to have you helping me with this. I could never get any of these shots myself, and it's not like I could ask Mom for help."
            the_person.char "If you ever have some spare time and want to be the greatest brother we could do this again. If my shots end up being popular I could even split some of the cash with you."
            mc.name "Alright, I'll keep that in mind. Glad to help."


        "Refuse and leave.":
            mc.name "I'm busy right now, I was just stopping by to say hi."
            $ the_person.change_happiness(-5)
            $ the_person.draw_person(emotion = "sad")
            the_person.char "Oh... Alright. If you ever have some spare time I could use a hand though. There are a ton of angles I can't get by myself."

    #TODO: Add the "help take pictures" action to her role, either by addint a static action and a flag or adding it here.

    $ sister_instathot_action = Action("Help her take Insta-pics.{image=gui/heart/Time_Advance.png}",instathot_requirement, "sister_instathot_label", menu_tooltip = "Help your sister grow her Insta-pic account by taking some pictures of her.")
    $ sister_role.actions.append(sister_instathot_action)
    $ renpy.scene("Active")
    return

label sister_instathot_label(the_person):
    #Help your sister take slutty pictures for the internet. Get a share of the cash she's earning on them.
    #Requires you to be in Lily's bedroom with her, so we can assume that's true.
    mc.name "I've got some spare time, do you want some help taking pictures for Insta-pic?"
    "[the_person.possessive_title] smiles and nodes excitedly."
    the_person.char "Yes! I've got a cute new outfit I want to show off, this is going to be great."
    $ insta_ouftit = insta_wardrobe.pick_random_outfit()
    "She hands you her phone and starts stripping down."
    the_person.char "Just give me a moment to get changed. It'll just be a sec!"
    $ next_item = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
    while next_item:
        $ the_person.draw_animated_removal(next_item)
        "..."
        $ next_item = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)

    $ the_person.draw_person(position = "doggy")
    "She gets onto her knees and pulls a shopping bag from the mall out from under her bed."
    the_person.char "I keep my stuff here so Mom doesn't find it. Okay, let's put this on!"
    $ the_person.draw_person(emotion = "happy")
    "[the_person.title] gets dressed in her new outfit and turns to you, smiling."
    $ the_person.apply_outfit(insta_ouftit)
    #$ the_person.outfit = insta_ouftit changed v0.24.1
    $ the_person.draw_person(emotion = "happy")
    the_person.char "Well, do you think they'll like it?"
    menu:
        "Of course!":
            mc.name "Of course, you look hot!"
            $ the_person.change_slut_temp(1)
            $ the_person.change_happiness(3)

        "I don't think so.":
            mc.name "I'm not so sure. They might be looking for something... More."
            if the_person.sluttiness >= 30:
                the_person.char "Yeah, I think so too. Too bad Insta-pic is run by a bunch of prudes. I wish there was somewhere I could show more..."
            else:
                $ the_person.change_happiness(-2)
                the_person.char "Really? Well, this is as much as I'm allowed to show, so I guess it doesn't matter either way."
            "She shrugs."
            the_person.char "Come on, let's take some pics!"

        "I've got another idea...":
            mc.name "It's nice, but I think I know an outfit they might like even more."
            the_person.char "Uh huh? Let me see it!"
            call screen outfit_select_manager()
            $ the_suggested_outfit = _return
            if the_suggested_outfit == "No Return":
                mc.name "On second thought, I don't think I have anything better than what you're wearing."
                the_person.char "Well, let's get started with this then!"

            elif the_suggested_outfit.vagina_visible():
                the_person.char "Come on [the_person.mc_title], I can't have my... You know, just hanging out like that."
                the_person.char "I'd get kicked off of Insta-pic so fast! Let's just take some pictures with what I'm wearing."

            elif the_suggested_outfit.tits_visible():
                the_person.char "I couldn't get away with that, they would ban me for showing my boobs."
                the_person.char "It's so unfair that guys can take pictures shirtless and post them but girls can't."
                the_person.char "Oh well, let's just take some pictures with the outfit I'm wearing."

            elif the_person.judge_outfit(the_suggested_outfit, -30):
                the_person.char "I mean, I guess it would be nice, but it isn't very... revealing, you know?"
                the_person.char "Guys on the site like it when you show some skin. A little cleavage, maybe some underwear."
                the_person.char "As long as it's not full on tits or pussy, it's fair game. Let's just go with what I'm wearing right now, okay?"

            elif not the_person.judge_outfit(the_suggested_outfit, 20):
                #It's so slutty she can't be convinced to try it.
                the_person.char "Oh wow... I guess it technically covers everything that needs to be covered but..."
                the_person.char "I don't think I could wear that [the_person.mc_title]. I wish I had that kind of confidence, but what if Mom saw these pictures?"
                the_person.char "Let's stick with what I had picked out, okay?"

            else:
                the_person.char "Oh, that would look really cute! Okay, I'll try it on!"
                $ next_item = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
                while next_item:
                    $ the_person.draw_animated_removal(next_item)
                    "..."
                    $ next_item = the_person.outfit.remove_random_any(top_layer_first = True, do_not_remove = True)
                "Once she's stripped down she puts on the outfit you've suggested."
                $ the_person.apply_outfit(the_suggested_outfit)
                #$ the_person.outfit = the_suggested_outfit.get_copy() #Getting a copy of it so we can assign the proper one to her wardrobe if we want. changed v0.24.1
                $ the_person.draw_person()
                $ the_person.change_love(1)
                $ the_person.change_obedience(2)
                if the_person.judge_outfit(the_suggested_outfit):
                    the_person.char "Alright, there we go! This is actually a really nice blend of cute and sexy."
                    the_person.char "You've got a really good eye for fashion, I might even wear this later I like it so much! Now let's take some pics!"
                    $ the_person.wardrobe.add_outfit(the_suggested_outfit)
                else:
                    the_person.char "Alright, there we go! It's perfect, just the right amount of sexy! Let's take some pics now!"

    $ the_person.draw_person(emotion = "happy", position = "kneeling1")
    "She jumps up onto her bed and gives the camera her sluttiest pout."
    "For the next hour you help [the_person.title] take pictures for her Insta-pic account. She looks over each one, deciding if it's worth keeping or not."
    "Finally she's happy with what she's got and takes her phone back."
    $ the_person.draw_person(emotion = "happy")
    the_person.char "Thank you so much [the_person.mc_title], these look amazing!"
    $ the_person.change_slut_temp(3)
    the_person.char "I guess I should pay you, huh? Since you're doing all this work for me."
    menu:
        "Take the money. +$100":
            mc.name "I'm not going to say no."
            "She rolls her eyes and direct transfers you some cash."
            $ mc.business.funds += 100
            the_person.char "No, I didn't think you would mr.\"I own a business\"."


        "Let her keep it.":
            mc.name "Don't worry about it, I'm just happy to see you doing something cool."
            $ the_person.change_love(1)
            the_person.char "Aww, you're the best!"
            "She gives you a hug and a quick kiss on the cheek."

    #TODO: SHe may keep the outfit.
    #TODO: She lets you suggest an outfit
    $ renpy.scene("Active")
    call advance_time() from _call_advance_time_30
    return




label sister_cam_girl_intro_label(the_person):
    # Your sister comes to you asking for _more_ money, this time to buy a better computer.
    # "I have an idea to make money, right here at home. I just need to buy some equipment."
    # "I need a new computer. And a microphone. And a webcam."
    # "It's none of your business!"
    # Threaten to tell your Mom, she tells you that she's going to make some videos for her "premium instapic followers".
    # Offer to buy her the equipment in exchange for a cut.
    return

label sister_cam_girl_online_view_label(the_person):
    # Tune into one of your sisters shows. Give her cash to do things as an anonymous doner.
    return

label sister_cam_girl_in_person_view_label(the_person):
    # Crash your sister's room and watch/join in on the show. At very high sluttiness she has you pose as her "boyfriend" for various things.
    return
