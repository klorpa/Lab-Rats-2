##########################################
# This file holds all of the role requirements and labels for the sister role.
##########################################

#TODO: add a punish line for Lilys instathot storyline
#TODO: Purposeful teasing ebents

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
            if the_person.sluttiness >= 30 and mc.business.event_triggers_dict.get("sister_serum_test_count",0) >= 4:
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
        elif time_of_day == 1:
            return "Too early to take pictures."
        else:
            return True

    def sister_instapic_discover_requirement(the_person):
        if lily not in lily_bedroom.people:
            return False #She's not at home, probably because of some other event
        elif not mc_at_home():
            return False #We're not at home, same deal.
        elif not mc_asleep():
            return False
        elif mc.location.get_person_count() > 0:
            return False #There's someone in our room, so she'll wait for another day
        elif the_person.event_triggers_dict.get("sister_instathot_mom_enabled", False):
            return False #She already knows, maybe this event got added twice somehow
        else:
            return True

    def sister_instathot_mom_report_requirement(the_person, start_day):
        if day <= start_day:
            return False #Wait at least a day
        if mom in mc.location.people:
            return False #Don't talk to her in front of her face.
        elif not mc_at_home():
            return False #Don't talk about it outside of the house.
        else:
            return True


#SISTER ACTION LABELS#

label sister_intro_crisis_label(the_person):
    #This is a mantatory crisis, so we assume that our requirements are tight enough to always trigger correctly. If you want to do crisis requirement checks here you need to re-add the crisis to the mandatory list!
    $ bedroom.show_background()
    "There's a knock at your bedroom door."
    mc.name "Come in."
    $ the_person.draw_person()
    the_person "Hey [the_person.mc_title], do you have a moment?"
    mc.name "Sure, what's up?"
    "[the_person.possessive_title] steps into your room and closes the door behind her."
    the_person "I wanted to say I'm really impressed with how your business is going. It must be really exciting to be your own boss now."
    mc.name "It's certainly been challanging, that's for sure."
    the_person "And... Well, I've been so busy with school that I haven't had a chance to get a job like Mom's been wanting..."
    mc.name "Oh no, I can see where this is going."
    the_person "If you could just give me a {i}tiny{/i} bit of cash I could show Mom I can take care of myself."
    mc.name "But you can't, apparantly."
    the_person "Please? Please please please, [the_person.mc_title]? Maybe there's some extra work I could do? I could..."
    "She gives up and shrugs."
    the_person "Help you science all that science stuff?"
    mc.name "I don't think that's really where I need help. But..."
    menu:
        "Ask [the_person.title] to test serum for you.":
            the_person "But...? Come on [the_person.mc_title], I really need your help."
            mc.name "Well, at the lab we've been running some experiements, but we need some test subjects."
            mc.name "I can bring home some of the stuff we're working on and if you let me test it on you I can pay you for it."
            the_person "It's not going to turn me into a lizard or something, right?"
            mc.name "Obviously not. It's just a liquid that you'd need to drink, then I'll watch to see how it affects you over the next few hours."
            the_person "What is it going to do?"
            mc.name "That's what we're trying to find out."
            $ the_person.draw_person(emotion = "happy")
            "[the_person.possessive_title] thinks about it for a moment, then nods."
            the_person "Okay, but I want $50 each time."
            mc.name "You drive a hard bargin sis. You've got a deal."
            "You shake on it."
            $ the_person.change_obedience(5)
            the_person "Thank you so much [the_person.mc_title]. Uh, if Mom asks just say I got a part time job."
            mc.name "Sure thing. I'll come see you when I have something for you to test."
            "[the_person.title] gives you one last smile then leaves your room, shutting the door behind her."
            $ mc.business.event_triggers_dict["sister_serum_test"] = True

        "Ask [the_person.title] to leave you alone.":
            the_person "But...?"
            mc.name "But I was just about to head to bed, so if you could let me get some sleep that would be a huge help."
            $ the_person.draw_person(emotion = "sad")
            $ the_person.change_happiness(-5)
            "[the_person.title] pouts and crosses her arms. She leaves your room in a huff."
            $ mc.business.event_triggers_dict["sister_needs_reintro"] = True

    $ clear_scene()
    return

label sister_reintro_label(the_person):
    #If you turn your sister away the first time you can approach her and ask to have her test serums anyways.
    mc.name "So [the_person.title], are you still looking for some work to do?"
    $ the_person.draw_person(emotion = "happy")
    the_person "Oh my god yes! Do you have something for me to do?"
    mc.name "Well, at the lab we've been running some experiements, but we need some test subjects."
    mc.name "I can bring home some of the stuff we're working on and if you let me test it on you I can pay you for it."
    the_person "It's not going to turn me into a lizard or something, right?"
    mc.name "Obviously not. It's just a liquid that you'd need to drink, then I'll watch to see how it affects you over the next few hours."
    the_person "What is it going to do?"
    mc.name "That's what we're trying to find out."
    $ the_person.draw_person(emotion = "happy")
    "[the_person.possessive_title] thinks about it for a moment, then nods."
    the_person "Okay, but I want $50 each time."
    mc.name "You drive a hard bargin sis. You've got a deal."
    "You shake on it."
    $ the_person.change_obedience(5)
    the_person "Thank you so much [the_person.mc_title]. Uh, if Mom asks just say I got a part time job."
    mc.name "Sure thing. I'll let you know when I have something for you to test."
    $ mc.business.event_triggers_dict["sister_needs_reintro"] = False
    $ mc.business.event_triggers_dict["sister_serum_test"] = True
    return

label sister_serum_test_label(the_person):
    #Give your sister some serum to test for cash.
    mc.name "Hey [the_person.title], I have something for you to test out for me."
    the_person "Alright, $50 and I'll try it."
    call give_serum(the_person) from _call_give_serum_7
    if _return:
        $ mc.business.funds += -50
        "You give [the_person.possessive_title] the cash and the serum. She puts the money away then drinks the serum, handing back the empty vial."
        $ the_person.change_obedience(1)
        the_person "Easiest fifty bucks I've ever earned. I guess you can hang around and keep an eye on me if it's important for your research."
        if mc.business.event_triggers_dict.get("sister_serum_test_count"):
            $ mc.business.event_triggers_dict["sister_serum_test_count"] += 1
        else:
            $ mc.business.event_triggers_dict["sister_serum_test_count"] = 1

    else:
        mc.name "Sorry [the_person.title], I guess I don't actually have anything for you to test."
        the_person "Ugh, come on [the_person.mc_title], you know I need the money!"
        mc.name "I'll find something for you to test, promise."
    return

label sister_strip_intro_label(the_person):
    #Give your sister some cash in exchange for her stripping. Higher sluttiness means she'll strip more (for less).
    $ bedroom.show_background()
    "There's a knock at your bedroom door."
    mc.name "Come in."
    $ the_person.draw_person()
    the_person "Hey [the_person.mc_title], can I talk to you about something?"
    "[the_person.possessive_title] comes into your room and shuts the door behind her. She seems nervous, avoiding eye contact as she comes closer."
    mc.name "Any time, what's up?"
    the_person "You know how I've been testing some of that lab stuff you make? For money?"
    mc.name "Yeah."
    the_person "Well I've been out shopping, and Mom would {i}kill{/i} me if she knew how much I was spending, so I was hoping you could pay me some more."
    mc.name "Sorry [the_person.title], I don't have anything for you to test right now."
    $ the_person.draw_person(emotion = "sad")
    the_person "Oh come on [the_person.mc_title], don't you have anything I could do? I really need the money now."
    "[the_person.possessive_title] puts her arms behind her back and pouts at you."
    menu:
        "Pay her to strip for you.":
            call strip_explanation(the_person) from _call_strip_explanation


        "Tell her to leave.":
            mc.name "I just don't have anything to give you [the_person.title]. I promise if I think of anything I'll come to you right away."
            the_person "Ugh... fine."
            "She turns and leaves your room, disappointed."
            $ the_person.change_happiness(-5)
            $ mc.business.event_triggers_dict["sister_strip_reintro"] = True

    $ clear_scene()
    return

label sister_strip_reintro_label(the_person):
    mc.name "I've been thinking about some stuff you could do for me [the_person.title]. Are you still interested in earning some more money?"
    $ the_person.draw_person(emotion = "happy")
    the_person "Yes! What do you want me to do?"

    call strip_explanation(the_person) from _call_strip_explanation_1

    $ mc.business.event_triggers_dict["sister_strip_reintro"] = False
    return

label strip_explanation(the_person):
    #Pulls out the explanation part of the strip intro so it's not duplicated
    mc.name "I've been busy getting my business running and earning all of this money I'm going to be paying you, so I haven't had a chance to meet many people."
    mc.name "It's been a while since I was able to just appreciate the looks of a hot woman."
    the_person "What are... what are you suggesting?"
    mc.name "I'll pay you if you just stand around and let me look at you. Maybe take some of your clothing off, if you're comfortable with it."
    the_person "So you want me to give you a strip show?"
    "You nod."
    "[the_person.possessive_title] seems surprised, but not particularly offended by the idea. She takes a long moment to consider it."
    the_person "Okay, I'll do it. I want $100 up front, plus a little extra if you want me to take anything off."
    mc.name "I think that's reasonable."
    $ the_person.change_obedience(5)
    $ mc.business.event_triggers_dict["sister_strip"] = True
    the_person "And obviously you can't touch me. Or yourself. And you can {i}never{/i} tell Mom about it."
    mc.name "Don't worry [the_person.title], I promise I won't make it weird."
    "[the_person.title] nods. There's a long silence before she speaks again."
    the_person "So... do you want me to do it for you now?"
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
            the_person "Okay. Thanks for helping me out [the_person.mc_title], you're a life saver."
            "[the_person.title] leaves your room and closes the door behind her."
    return


label sister_strip_label(the_person):
    #A short intro so that we can reuse the pay_strip_scene with other characters if we want.
    mc.name "So [the_person.title], are you interested in earning a hundred dollars?"
    if the_person.effective_sluttiness("underwear_nudity") < 50:
        the_person "Oh, do you want me to... show off for you?"
    else:
        the_person "You want me to strip down for you?"
    $ mc.business.funds += -100
    "You nod and sit down on [the_person.possessive_title]'s bed. She holds her hand out and you hand over her money."
    "She tucks the money away and gets ready in front of you."
    call pay_strip_scene(the_person) from _call_pay_strip_scene_1
    return

label sister_instathot_intro_label(the_person):
    # Your sister needs you to take pictures for her.
    # She's got an InstaPic (genius, they'll never guess!) account and wants to be an "influencer"
    # Triggers at some point when you go into your sisters room. You catch her taking pictures for InstaPic, but she doesn't mind and explains what she's doing.
    # Adds a random event where Lily posts InstaPics, similar to your mom sending you selfies.


    # Actually, let's have her start with a relatively tame outfit and grow into really sexy ones.
    if not the_person.has_role(instapic_role):
        $ the_person.special_role.append(instapic_role)
    $ the_person.event_triggers_dict["insta_known"] = True


    "You open the door to [the_person.possessive_title]'s room."
    $ the_person.draw_person(position = "kneeling1")
    "She's posed on her bed, holding her phone high up in one hand to take a selfie. She startles when you come in, standing up quickly before calming down."
    $ the_person.draw_person()
    the_person "Oh... It's just you. Come in and close the door, please."
    "You step inside and close the door behind you."
    the_person "You scared me, I thought you were [mom.title] for a second."
    mc.name "Why would you be worried about her? What are you up to?"
    the_person "Nothing, she just wouldn't understand and I don't want to make it a big thing."
    "She holds up her phone and smiles."
    the_person "But if you have to know, I made an account on InstaPic and I'm putting up some pictures for my fans."
    mc.name "InstaPic?"
    the_person "Oh my god, how old are you again? It's a social media thing, people post pictures and follow other people."
    the_person "If you're popular some companies will even pay for you to wear their clothes or show off their stuff."
    mc.name "So how popular are you?"
    the_person "Well... Not very, yet, but I just started posting! I'm still figuring out what people want to see."
    "Looking at her outfit it seems like she has the right idea."
    the_person "Since you're here, could you use my phone and take some pictures? It's hard doing it all myself."
    menu:
        "Help her.":
            mc.name "Fine, give it here."
            $ the_person.change_happiness(5)
            the_person "Yay, thank you [the_person.mc_title]!"
            "She hands you her phone and strikes a pose."
            $ the_person.draw_person(emotion = "happy")
            the_person "Got it? Okay. Now get one like I just noticed you."
            $ the_person.draw_person(emotion = "happy", position = "walking_away")
            "It seems like no shot is ever perfect, but eventually she's satisfied and takes her phone back with a smile."
            $ the_person.draw_person()
            $ the_person.change_love(2)
            the_person "Thank you so much, you're the best!"
            "She gives you a quick kiss on the cheek."
            the_person "It's so nice to have you helping me with this. I could never get any of these shots myself, and it's not like I could ask Mom for help."
            the_person "If you ever have some spare time and want to be the greatest brother we could do this again. If my shots end up being popular I could even split some of the cash with you."
            mc.name "Alright, I'll keep that in mind. Glad to help."
            $ the_person.event_triggers_dict["insta_generate_pic"] = True


        "Refuse and leave.":
            mc.name "I'm busy right now, I was just stopping by to say hi."
            $ the_person.change_happiness(-5)
            $ the_person.draw_person(emotion = "sad")
            the_person "Oh... Alright. If you ever have some spare time I could use a hand though. There are a ton of angles I can't get by myself."

    "You make a mental note to check out her profile on instapic at some point."



    $ sister_instathot_action = Action("Help her take Insta-pics.{image=gui/heart/Time_Advance.png}",instathot_requirement, "sister_instathot_label", menu_tooltip = "Help your sister grow her InstaPic account by taking some pictures of her.")
    $ sister_role.actions.append(sister_instathot_action)
    $ clear_scene()
    return

label sister_instathot_label(the_person):
    #Help your sister take slutty pictures for the internet. Get a share of the cash she's earning on them.
    #Requires you to be in Lily's bedroom with her, so we can assume that's true.
    mc.name "I've got some spare time, do you want some help taking pictures for InstaPic?"
    if the_person.event_triggers_dict.get("sister_instathot_mom_enabled", False) and person_at_home(mom):
        if mom.event_triggers_dict.get("mom_instathot_pic_count",0) == 0: #It's your first time inviting her.
            "[the_person.possessive_title] smiles and nods excitedly."
            the_person "Yeah! Is [mom.title] around? She's been bugging me about wanting to take some pictures together."
            the_person "We might as well get those out of the way right now."
            mc.name "I'll go check."
            call sister_instathot_label_mom(the_person, mom) from _call_sister_instathot_label_mom

        else:
            "[the_person.possessive_title] smiles and nods excitedly."
            the_person "Yeah! Hey, do you think [mom.title] would want to join again? Our last shots together did really well."
            menu:
                "Ask [mom.title] to join.":
                    mc.name "I'll go check."
                    call sister_instathot_label_mom(the_person, mom) from _call_sister_instathot_label_mom_1
                "Just Lily.":
                    mc.name "I think she's busy right now."
                    "[the_person.title] shrugs."
                    the_person "Alright, maybe next time. Come on, I got a cute new outfit I want to show off!"
                    call sister_instathot_label_solo(the_person) from _call_sister_instathot_label_solo

    else:
        "[the_person.possessive_title] smiles and nods excitedly."
        the_person "Yes! I've got a cute new outfit I want to show off, this is going to be great."
        call sister_instathot_label_solo(the_person) from _call_sister_instathot_label_solo_1

    $ clear_scene()
    call advance_time() from _call_advance_time_23
    return

label sister_instathot_label_solo(the_person):
    # Called when you're alone with Lily.
    $ the_person.event_triggers_dict["insta_generate_pic"] = True #If we take pics, generate a post for her for you to view next time you check her page.
    $ insta_outfit = insta_wardrobe.pick_random_outfit()
    "She hands you her phone and starts stripping down."
    the_person "Just give me a moment to get changed. It'll just be a sec!"


    $ special_request = the_person.event_triggers_dict.get("insta_special_request_sis", None) #Check if there are any special requests you sent. Should be "underwear", "topless", or "nude", or None.
    $ for_player = False
    if special_request is None: #Chance someone else will have sent her a request for you to help with.
        if renpy.random.randint(0,100) < 15: #Someone else has a special request
            $ special_request = get_random_from_weighted_list([["underwear",30],["topless",50],["nude",30]]) #Sometimes people send her special requests
            if special_request == "underwear" and the_person.effective_sluttiness() < 20:
                $ special_request = None
            elif special_request == "topless" and the_person.effective_sluttiness() < 30:
                $ special_request = None
            elif special_request == "nude" and the_person.effective_sluttiness() < 40:
                $ special_request = None
    else:
        $ for_player = True

    $ the_person.event_triggers_dict["insta_special_request_sis"] = None #And then clear any special requests. NOTE: outfit requests are handled seperately. This is for anything that produces a private pic.

    $ strip_list = the_person.outfit.get_full_strip_list()
    $ generalised_strip_description(the_person, strip_list)

    $ the_person.draw_person(position = "doggy")
    "She gets onto her knees and pulls a shopping bag from the mall out from under her bed."
    the_person "I keep my stuff here so Mom doesn't find it. Okay, let's put this on!"
    $ the_person.draw_person(emotion = "happy")
    "[the_person.title] gets dressed in her new outfit and turns to you, smiling."
    if the_person.event_triggers_dict.get("insta_special_request_outfit", False):
        $ insta_outfit = the_person.event_triggers_dict.get("insta_special_request_outfit")
        $ the_person.apply_outfit(insta_outfit, update_taboo = True)
        the_person "A fan said I should wear this. Isn't it cute?"

    else:
        $ the_person.apply_outfit(insta_outfit, update_taboo = True)
        $ the_person.draw_person(emotion = "happy")
        the_person "Well, do you think they'll like it?"
        menu:
            "Of course!":
                mc.name "Of course, you look hot!"
                $ the_person.change_slut_temp(1)
                $ the_person.change_happiness(3)

            "I don't think so.":
                mc.name "I'm not so sure. They might be looking for something... More."
                if the_person.effective_sluttiness() >= 30:
                    the_person "Yeah, I think so too. Too bad InstaPic is run by a bunch of prudes. I wish there was somewhere I could show more..."
                else:
                    $ the_person.change_happiness(-2)
                    the_person "Really? Well, this is as much as I'm allowed to show, so I guess it doesn't matter either way."
                "She shrugs."
                the_person "Come on, let's take some pics!"

            "I've got another idea...":
                mc.name "It's nice, but I think I know an outfit they might like even more."
                the_person "Uh huh? Let me see it!"
                call outfit_master_manager() from _call_outfit_master_manager_1
                $ the_suggested_outfit = _return
                if the_suggested_outfit is None:
                    mc.name "On second thought, I don't think I have anything better than what you're wearing."
                    the_person "Well, let's get started with this then!"

                elif the_suggested_outfit.vagina_visible():
                    the_person "Come on [the_person.mc_title], I can't have my... You know, just hanging out like that."
                    the_person "I'd get kicked off of InstaPic so fast! Let's just take some pictures with what I'm wearing."

                elif the_suggested_outfit.tits_visible():
                    the_person "I couldn't get away with that, they would ban me for showing my boobs."
                    the_person "It's so unfair that guys can take pictures shirtless and post them but girls can't."
                    the_person "Oh well, let's just take some pictures with the outfit I'm wearing."

                elif the_person.judge_outfit(the_suggested_outfit, -30):
                    the_person "I mean, I guess it would be nice, but it isn't very... revealing, you know?"
                    the_person "Guys on the site like it when you show some skin. A little cleavage, maybe some underwear."
                    the_person "As long as it's not full on tits or pussy, it's fair game. Let's just go with what I'm wearing right now, okay?"

                elif not the_person.judge_outfit(the_suggested_outfit, 20):
                    #It's so slutty she can't be convinced to try it.
                    the_person "Oh wow... I guess it technically covers everything that needs to be covered but..."
                    the_person "I don't think I could wear that [the_person.mc_title]. I wish I had that kind of confidence, but what if Mom saw these pictures?"
                    the_person "Let's stick with what I had picked out, okay?"

                else:
                    the_person "Oh, that would look really cute! Okay, I'll try it on!"

                    $ strip_list = the_person.outfit.get_full_strip_list()
                    $ generalised_strip_description(the_person, strip_list)

                    "Once she's stripped down she puts on the outfit you've suggested."
                    $ the_person.apply_outfit(the_suggested_outfit, update_taboo = True)
                    #$ the_person.outfit = the_suggested_outfit.get_copy() #Getting a copy of it so we can assign the proper one to her wardrobe if we want. changed v0.24.1
                    $ the_person.draw_person()
                    $ the_person.change_love(1)
                    $ the_person.change_obedience(2)
                    if the_person.judge_outfit(the_suggested_outfit):
                        the_person "Alright, there we go! This is actually a really nice blend of cute and sexy."
                        the_person "You've got a really good eye for fashion, I might even wear this later I like it so much! Now let's take some pics!"
                        $ the_person.wardrobe.add_outfit(the_suggested_outfit)
                    else:
                        the_person "Alright, there we go! It's perfect, just the right amount of sexy! Let's take some pics now!"
                        $ insta_wardrobe.add_outfit(the_suggested_outfit) #If she wouldn't wear it normally it's added to the list of insta-appropriate outfits instead

    $ the_person.draw_person(emotion = "happy", position = "kneeling1")
    "She jumps up onto her bed and gives the camera her sluttiest pout."
    "For the next hour you help [the_person.title] take pictures for her InstaPic account. She looks over each one, deciding if it's worth keeping or not."
    if special_request == "underwear" and not the_person.event_triggers_dict.get("sister_insta_special_ignore", False): #TODO: Set up this flag. For now it only triggers when you send her a request for it.
        if the_person.event_triggers_dict.get("sister_insta_underwear_count", 0) == 0:
            the_person "Oh, one more thing before you go! I need you to take some pictures of me in my, uh... underwear."
            mc.name "Wait, I thought you would be banned for posting pictures like that."
            the_person "It's kind of a grey zone. I mean, what counts as underwear and what's just slutty clothing?"
            the_person "I just need a few shots, please?"
            $ the_person.event_triggers_dict["sister_insta_underwear_count"] = 0
        else:
            the_person "Oh, one more thing before you go! I need some more underwear shots."
        menu:
            "Take the pictures":
                mc.name "Okay, let's do it."
                call sister_instathot_special_underwear(the_person) from _call_sister_instathot_special_underwear
                if for_player:
                    $ the_person.event_triggers_dict["insta_special_request_asap"] = True #Flags you to recieve a response as soon as possible, ignoring random chance.

            "Don't help":
                mc.name "That's going a little far. Let's end here, okay?"
                "She pouts, but nods."
                the_person "Fine..."

    else:
        "Finally she's happy with what she's got and takes her phone back."
        $ the_person.draw_person(emotion = "happy")
        the_person "Thanks so much [the_person.mc_title], these look amazing!"
        $ the_person.change_slut_temp(3)
    the_person "I guess I should pay you, huh? Since you're doing all this work for me."
    menu:
        "Take the money. +$100":
            mc.name "I'm not going to say no."
            "She rolls her eyes and direct transfers you some cash."
            $ mc.business.funds += 100
            the_person "No, I didn't think you would mr.\"I own a business\"."

        "Let her keep it.":
            mc.name "Don't worry about it, I'm just happy to see you doing something cool."
            $ the_person.change_love(1)
            the_person "Aww, you're the best!"
            "She gives you a hug and a quick kiss on the cheek."

    if (special_request == "topless" or special_request == "nude") and not the_person.event_triggers_dict.get("sister_insta_special_ignore", False): #One of her viewers has a special request.
        #TODO: This should set the chance of the girl responding to your Insta DM to 100% for the next valid time, if you had sent one.
        $ is_topless_shoot = special_request == "topless"
        if the_person.event_triggers_dict.get("sister_insta_special_intro", False): #
            if the_person.event_triggers_dict.get("sister_insta_special_count",0) == 0: #You told her no the first time.
                the_person "Before you go... I know you said it was a bad idea, but I got another big offer for a topless shot."
                the_person "Do you think I should reconsider? Maybe I can split the cash with [mom.title], that way I'm helping everyone!"
                menu:
                    "Take the pictures":
                        mc.name "Well... I guess if it's just a topless shot, and [mom.title] could definitely use the cash."
                        the_person "Come on [the_person.mc_title], it'll just take a moment!"
                        "She smiles eagerly and hands her phone back to you."
                        call sister_instathot_special_pictures(the_person, is_topless_shoot) from _call_sister_instathot_special_pictures
                        if for_player:
                            $ the_person.event_triggers_dict["insta_special_request_asap"] = True #Flags you to recieve a response as soon as possible, ignoring random chance.

                    "Ignore the offer.":
                        mc.name "I told you before, I don't think it's a good idea."
                        the_person "Right, sorry I even mentioned it. I'll just delete all those messages and won't bother you about it again."
                        $ the_person.event_triggers_dict["sister_insta_special_ignore"] = True #If you turn her down both times she stops asking. #TODO: Remember to keep this storyline non-critical since you can disable it.
            else:
                the_person "Before you go, can we take a few special shots? I another special request from a fan."
                the_person "It'll just take a moment!"
                menu:
                    "Take the picture":
                        mc.name "Sure, no problem."
                        "[the_person.possessive_title] smiles and hands her phone back over to you."
                        call sister_instathot_special_pictures(the_person, is_topless_shoot) from _call_sister_instathot_special_pictures_1
                        if for_player:
                            $ the_person.event_triggers_dict["insta_special_request_asap"] = True #Flags you to recieve a response as soon as possible, ignoring random chance.


                    "Not right now.":
                        mc.name "I've got something else to get to. Sorry [the_person.title]."
                        the_person "Oh, that's fine. I'll just go take it in the bathroom mirror I guess."

        else:
            call sister_instathot_special_intro(the_person, is_topless_shoot) from _call_sister_instathot_special_intro

    if the_person.event_triggers_dict.get("sister_instathot_pic_count", 0) == 0:
        $ the_person.event_triggers_dict["sister_instathot_pic_count"] = 1
    else:
        $ the_person.event_triggers_dict["sister_instathot_pic_count"] += 1
    return

label sister_instathot_special_intro(the_person, is_topless_shoot = True):
    #Your sister lets you know that someone on insta is asking for "special" pictures. She's unsure if she should do it, but it's a lot of money.
    #Triggered when she's asked for a topless or nude shot
    $ the_person.event_triggers_dict["sister_insta_special_intro"] = True
    the_person "Wait, before you go I wanted to ask you something..."
    mc.name "What is it?"
    the_person "Ever since I started my insta-posts I've had guys sending me creepy messages, usually asking me to show my... you know."
    "She shrugs and laughs nervously."
    the_person "I've just been ignoring them, but today a guy PM'd me and said he'd give me a lot of money for a topless shot."
    the_person "[mom.title] has been so worried about money, I feel kind of selfish saying no to something so easy."
    the_person "What do you think I should do?"
    menu:
        "Take the picture.":
            mc.name "I think the answer is pretty clear. We can take the shot right now, then you can give [mom.title] a cut, to help with the bills."
            mc.name "Give me your phone and we can take the shot right now."
            "She hesitates for a moment, then nods and hands her phone back to you."
            the_person "Yeah, you're right. Let's get a few pictures, I'll send him the best one."
            call sister_instathot_special_pictures(the_person, is_topless_shoot) from _call_sister_instathot_special_pictures_2

        "Ignore them.":
            mc.name "You know what they say [the_person.title]. Once it's on the internet it's there forever."
            mc.name "I think it would be a bad idea to be giving nudes to anyone, even if they're paying you a lot of money."
            "She seems a little disappointed, but nods anyways."
            the_person "Yeah, you're probably right. I would die of embarassement if [mom.title] found them."
    return

label sister_instathot_special_underwear(the_person): #She's been asked to do an underwear shoot.
    #TODO: We should do some underwear checks to make sure she's actually covered.
    if the_person.has_taboo("underwear_nudity"):
        the_person "You don't mind seeing me in my underwear, do you?"
        mc.name "No, not at all. There's nothing weird about that."
        the_person "Yeah, I don't think so either. You're my brother, I can trust you!"
        the_person "I'm so lucky to have you around [the_person.mc_title]."

    $ strip_list = the_person.outfit.get_underwear_strip_list(avoid_nudity = True)
    if strip_list:
        "[the_person.title] starts to pull her clothes off."
        $ generalised_strip_description(the_person, strip_list)

    if the_person.tits_visible() or the_person.vagina_visible():
        the_person "Hmm, I guess I should actually put on some underwear. One second!"
        "[the_person.possessive_title] turns and starts to look through her wardrobe."
        $ the_person.apply_outfit(the_person.wardrobe.get_random_appropriate_underwear(the_person.sluttiness))
        if the_person.tits_visible() or the_person.vagina_visible():
            the_person "Hmm... Well, this will have to do I guess. They'll get a little more than they paid for I suppose!"
        "She gets changed quickly, then turns back to you."

    $ the_person.draw_person()
    the_person "Okay, let's get started then!"
    if the_person.effective_sluttiness() < 40:
        the_person "I just need one or two good pics to send this guy."
    else:
        the_person "Let's make sure we get something sexy for this guy, okay?"

    $ the_person.draw_person(position = "back_peek")
    "You take some shots for [the_person.possessive_title] while she poses in her underwear."
    the_person "Okay, there should be something good there. Let me take a look!"
    "She hurries over to you and holds onto your arm as you flick through the pictures you just took."
    the_person "Ooh, that one looks good. I'll send him that one, and maybe that one..."
    $ the_person.change_slut_temp(2)
    "She gives you a hug and takes her phone back."
    the_person "Thanks for the help [the_person.mc_title], you're an awesome brother!"
    $ the_person.event_triggers_dict["sister_insta_underwear_count"] += 1
    return

label sister_instathot_special_pictures(the_person, is_topless_shoot = True):
    if the_person.has_taboo("bare_tits"): #NOTE: I don't think this dialogue ever comes up,because you always see her nude when she's changing earlier.
        the_person "I guess that means you're going to have to see my tits... Are you okay with that?"
        mc.name "Yeah, it's no problem. I'm just glad you can trust me with this and not some sleezy photographer."
        "She smiles and nods."
        the_person "I'm so lucky to have you around [the_person.mc_title]."

    if is_topless_shoot:
        the_person "Okay, he just wants some pictures of my boobs."
    else: #Is a nude shoot
        the_person "Okay, he wants some full body nudes."
    "[the_person.title] starts to pull her clothes off."

    python:
        if is_topless_shoot:
            strip_list = the_person.outfit.get_tit_strip_list()
            half_off_instead = False
            if the_person.outfit.can_half_off_to_tits():
                half_off_instead = True
                strip_list = the_person.get_half_off_to_tits_list()
            generalised_strip_description(the_person, strip_list, half_off_instead = half_off_instead)
        else:
            strip_list = the_person.outfit.get_full_strip_list()
            generalised_strip_description(the_person, strip_list)

    $ the_person.update_outfit_taboos()
    "She gets onto her bed, onto her knees, and looks at you and the camera."
    $ the_person.draw_person(position = "kneeling1", emotion = "happy")
    the_person "Okay, ready?"
    "You square up the shot and nod. [the_person.possessive_title] smiles for the camera, tits on display."
    "You take a few pictures, trying a few different angles."
    mc.name "Alright, that should do it."
    if the_person.effective_sluttiness() >= 35:
        the_person "Wait, just a few more. Get a few where I roll my eyes up, like I'm cumming or something."
        $ the_person.draw_person(position = "kneeling1", emotion = "orgasm")
        "[the_person.possessive_title] sticks her tongue out and unfocuses her eyes. She trusts her chest forward and pants for added effect."
        menu:
            "Take the pictures.":
                "You take a few more pictures, capturing her tits along with her fake-orgasm face."
                "When you're done she giggles and hops off her bed and hurries over to you."


            "Encourage her.":
                mc.name "That's a good idea. Come on [the_person.title], act it out. Convince me!"
                if the_person.effective_sluttiness() <= 50:
                    $ the_person.draw_person(position = "kneeling1", emotion = "happy")
                    "She blushes and giggles, then responds jokingly."
                    the_person "Oh, something like... Ah... I'm totally cumming."
                    mc.name "Come on, I'm serious. The pictures will look better if you act it out and really pretend."
                    mc.name "Think about what makes you cum, imagine you're right at the edge and it's all you want."
                    the_person "Fine, I'll try..."
                    $ the_person.draw_person(position = "kneeling1", emotion = "orgasm")
                "She wiggles her shoulders and takes a few deep, sensual breaths."
                the_person "Oh my god, I'm going to cum! I'm going to cum so fucking hard!"
                the_person "Fuck, I'm cuming! I'm cumming [the_person.mc_title]! Mmm!"
                "She rolls her eyes up towards the ceiling as she pretends to orgasm. You get a few more shots and push her for more."
                mc.name "That's it, keep going. What's making you cum [the_person.title]? Tell me!" #TODO: If we ever add more opinion information we can tie that in here.
                the_person "Your big cock is making me cum! I'm such a dirty little slut, cumming on your huge dick!"
                "[the_person.possessive_title] is panting loudly now as she continues to give a very convincing performance."
                "...At least you're pretty sure it's a performance."
                "You try to ignore the throbbing erection you have now and get a few more shots of [the_person.title]."
                the_person "Cuuuumming! Aaaah! Ah... Ah...."
                "[the_person.title] rolls her eyes up as far as she can, sticks her tongue out, and squeels happily for the camera."
                "You get the last shot - definitely the best of the lot - nod to [the_person.possessive_title]."
                "She takes a moment to recover from her theatrics, then hops off her bed and hurries over to you."


        $ the_person.draw_person(emotion = "happy")
        the_person "That felt so silly, but I bet they'll like it! Come on, show me how they turned out!"
        "[the_person.title] holds onto your arm as you flip through all of the shots you just took together."
        if not the_person.has_large_tits():
            the_person "Those look great! It's just..."
            $ the_person.draw_person(emotion = "sad")
            mc.name "What? What's wrong?"
            the_person "Oh, nothing. Sometimes I just wish my boobs were a little larger."
            the_person "Look at [mom.title], she's got huge boobs! These are..."
            "She grabs her chest and squeezes her tits in her hands."
            the_person "...A little small. All the really popular girls on InstaPic have big boobs."
            menu:
                "Get bigger boobs":
                    mc.name "Then you should do something about it. You know you can just get fake boobs, right?"
                    the_person "Obviously. I've looked into it and it's super expensive."
                    if the_person.event_triggers_dict.get("sister_instathot_mom_enabled", False): #Mom already knows about her "hobby"
                        #TODO: Hook this up as an actual event that can start here (and maybe other places?)
                        the_person "And what would I tell [mom.title]?"
                        mc.name "You thought she would be angry about your InstaPic account, and she turned out to love it."
                        mc.name "Maybe she would be fine with this too."
                        the_person "Maybe... I don't know, I don't think it's a good idea."
                        mc.name "What if I convince her for you?"
                        "[the_person.possessive_title] laughs and shakes her head in disbelief."
                        the_person "Sure, good luck with that. Just don't tell her I'm taking these special pictures, alright?"
                        mc.name "Of course. I won't tell her anything."
                        the_person "Well, thanks for the help with the pics. That was fun."


                    else: #Mom doesn't know
                        the_person "And what would I tell [mom.title]? I would have to tell her about my InstaPic account, and she would make me take it down."
                        mc.name "I think you might be surprised."
                        the_person "Maybe, but I don't want to take that risk. I'm just happy with how things are going now."



                "They're fine.":
                    mc.name "You're worrying too much [the_person.title]. Your tits look great."
                    "She shrugs."
                    the_person "Yeah, you're probably right. Hey, thanks for the help!"
            #TODO: Add an event chain to get Lily some bigger tits!
        else:
            $ the_person.change_happiness(5 + the_person.get_opinion_score("showing her tits"))
            the_person "Those look great! Look at my tits, don't they look fantastic? I'm so glad they're bigger now!"
            "She scoops up her tits and jiggles them playfully."
            the_person "This guy is going to cum just looking at them!"
    else:
        the_person "Yay! Let me see how they turned out!"
        $ the_person.draw_person(emotion = "happy")
        if is_topless_shoot:
            "[the_person.title] hops off of the bed and hurries to your side. She holds onto your arm as you flick through her topless shots."
        else:
            "[the_person.title] hops off of the bed and hurries to your side. She holds onto your arm as you flick through her new nudes."
        the_person "... Oh, that one's cute. I think I'll send him that one. Thank you so much [the_person.mc_title]!"
    $ the_person.change_slut_temp(2)
    "She gives you a hug and takes her phone back."
    if the_person.event_triggers_dict.get("sister_insta_special_count", 0) == 0:
        $ the_person.event_triggers_dict["sister_insta_special_count"] = 1
    else:
        $ the_person.event_triggers_dict["sister_insta_special_count"] += 1

    $ the_person.event_triggers_dict["sister_instathot_special_pictures_recent"] = True # Triggers an event for Mom to ask where Lily is getting this money.
    return

label sister_instathot_mom_discover(the_person): # TODO: Hook this up as a night time crisis triggered if you tell Mom about Lily's Insta job
    $ the_person.change_happiness(-15, add_to_log = False)
    "You're getting ready for bed when your door is opened suddenly."
    $ the_person.draw_person(emotion = "angry")
    $ the_person.change_love(-2)
    "[the_person.title] hurries in and slams the door behind her. She seems angry"
    the_person "Did you really tell [mom.title] about my InstaPic profile?"
    mc.name "Yeah, I did. She seems proud of you."
    the_person "I... You didn't tell her about the private pictures I've been sending, did you?"
    mc.name "You mean your nudes?"
    the_person "Hey, it's just my tits..."
    mc.name "You can relax, I didn't tell her about that. I just told her that it's basically online modeling."
    mc.name "Has she said anything to you?"
    $ the_person.draw_person()
    "[the_person.possessive_title] rolls her eyes and shrugs."
    the_person "She said she was proud of me, and that I should have told her earlier."
    the_person "Now [mom.title] wants to see how it's done and take some pictures with me... Ugh..."
    mc.name "So do it, what's the big deal?"
    the_person "I don't want to take boring pictures with my Mom! My followers are going to hate it!"
    menu:
        "Dress [mom.title] up":
            mc.name "The pictures don't need to be boring. Dress [mom.title] up the same way you normally do."
            "[the_person.possessive_title] laughs and shakes her head."
            the_person "Oh my god, could you imagine? There's no way she would do it."
            mc.name "She wants a reason to spend time with you, I think she'd give it a try."
            the_person "You really think so? But she's still my mom, isn't that a little weird."
            mc.name "It's just to keep your followers hooked. I bet a a bunch of them would be into an older woman."
            the_person "Eww, gross. Still..."
            $ the_person.change_slut_temp(2)
            the_person "Alright, I'll think about it. At least I don't have to worry about her catching me anymore."
            $ the_person.event_triggers_dict["sister_instathot_mom_pics_slutty"] = True #A flag for the instathot event to have Lily suggest Mom wears something slutty like her.


        "Just do it once":
            mc.name "She just wants to be involved. Do one picture with her, then go back to normal."
            "Her shoulders slump and she sighs."
            the_person "I guess. At least I don't have to hide it now."
            $ the_person.change_love(1)

    the_person "And uh... Sorry about barging in."
    mc.name "Don't make a habit of it, alright?"
    "She nods and leaves, closing the door softly behind her."
    $ clear_scene()
    $ the_person.event_triggers_dict["sister_instathot_mom_enabled"] = True
    return

label sister_instathot_label_mom(the_sister, the_mom):
    $ clear_scene()
    "You leave [the_sister.title] in her room and go to find [the_mom.possessive_title]."
    $ first_time = the_mom.event_triggers_dict.get("mom_instathot_pic_count",0) == 0
    $ kitchen.show_background()
    $ the_mom.draw_person(position = "back_peek")
    "You find her in the kitchen, standing in front of the open fridge."
    the_mom "Oh, hi sweetheart. I'm just thinking about what to make for dinner. Do you need anything?"
    if first_time:
        mc.name "[the_sister.title] is getting ready to take some pictures for her InstaPic account."
        mc.name "She wanted to know if you wanted to join in."
        $ the_mom.draw_person(emotion = "happy")
        the_mom "Really? She's not just saying that to make me happy, is she?"
        mc.name "No, she really wants to spend time with you [the_mom.title]."
        the_mom "Okay then, I'll give it a try. Dinner can be a little late tonight."
    else:
        mc.name "[the_sister.title] is getting ready to take some more pictures for her InstaPic."
        mc.name "Do you want to join in?"
        $ the_mom.draw_person(emotion = "happy")
        the_mom "I really should be getting dinner started, but it was a lot of fun..."
        the_mom "Oh what the heck, dinner can be a little late tonight."

    "[the_mom.possessive_title] closes the fridge and follows you back to [the_sister.possessive_title]'s room."
    $ clear_scene()
    $ lily_bedroom.show_background()
    $ the_group = GroupDisplayManager([the_sister, the_mom], primary_speaker = the_sister)
    $ the_group.draw_group()

    if first_time:
        the_sister "Hey [the_mom.title], come on in."
        $ the_group.draw_person(the_mom)
        the_mom "Thank you for inviting me, I just hope I'm not going to get in your way."
        mc.name "You're going to do great [the_mom.title]."
        the_mom "Thank you sweetheart. You can run along then, me and your sister will..."
        $ the_group.draw_person(the_sister)
        the_sister "Wait [the_mom.title], we need him. He's going to take the pictures."
        $ the_group.draw_person(the_mom)
        the_mom "Oh! I was wondering how we were going to both be in the pictures. That makes sense."
        the_mom "What do we first then?"
        $ the_group.draw_person(the_sister)
        if the_sister.event_triggers_dict.get("sister_instathot_mom_pics_slutty", False):
            the_sister "I've got some outfits picked out for us. I had to guess at some of your sizes, so it might be a bit small."
            the_sister "You don't have to wear it if you don't want to though. I..."
            $ the_group.draw_person(the_mom)
            "[the_mom.title] shakes her head and interrupts."
            the_mom "[the_sister.title], I want the whole experience! These outfits will get you more view on your insta... view... pic thing, right?"
            the_mom "Come on, show me what you picked out for me. I'm sure I can squeeze into it with a little bit of work."
        else:
            the_sister "First I need to pick an outfit and get changed."
            the_sister "You don't have to change anything though, I'll just..."
            $ the_group.draw_person(the_mom)
            "[the_mom.title] shakes her head and interrupts."
            the_mom "[the_sister.title], I want the whole experience! Don't you want more views on your insta... view... pic thing?"
            the_mom "Come on, show me what you have. I'm sure you have something I can squeeze into."
        $ the_group.draw_person(the_sister)
        "[the_sister.possessive_title] smiles and nods. She waves [the_mom.possessive_title] over to the pile of clothes she has laid out on her bed."
        the_sister "Really? Alright! Well, I've got this a few days ago that's really cute and..."
        "You lean against a wall and pass some time on your phone while [the_sister.possessive_title] and [the_mom.title] pick out outfits."
        the_sister "Right, I think these are going to drive them wild. Come on, let's see how they look!"

    else:
        the_sister "Hey [the_mom.title], come on in!"
        $ the_group.draw_person(the_mom)
        the_mom "Hi sweety, thanks for having me back. So, do you have something for us to wear today?"
        $ the_group.draw_person(the_sister)
        the_sister "I've got some really cute outfits I think we'll look amazing in. Come on, let's get changed."

    if the_mom.has_taboo(["bare_tits", "bare_pussy"]): #She doesn't want to strip in front of you, let's break those taboos!
        $ the_group.draw_person(the_mom)
        the_mom "[the_mom.mc_title], you don't mind, do you? I can go back to my room if this..."
        mc.name "Don't worry [the_mom.title], I don't mind at all. Go ahead and get changed and we can take some pics."
        the_mom "Right, nothing to worry about then..."
        "She seems uncomfortable undressing in front of you, but get's over it quickly as [the_sister.title] starts stripping down without comment."
        $ the_mom.break_taboo("bare_tits")
        $ the_mom.break_taboo("bare_pussy")
    else: #No problems here, strip away!
        "[the_sister.title] starts to strip down, and [the_mom.possessive_title] hurries to keep up."

    $ stripper = the_sister # Pick which girl you want to make the primary for this event.
    menu:
        "Watch [the_sister.title] strip.":
            $ stripper = the_sister
            $ not_stripper = the_mom

        "Watch [the_mom.title] strip.":
            $ stripper = the_mom
            $ not_stripper = the_sister

    $ the_group.set_primary(stripper)
    $ the_group.draw_person(stripper)

    # Now loop through everyone

    $ generalised_strip_description(stripper, stripper.outfit.get_full_strip_list(), group_display = the_group, other_people = [(not_stripper, not_stripper.outfit.get_full_strip_list())])

    "[stripper.title] finishes stripping naked and starts to put on her outfit. [not_stripper.title] is naked now too, and is doing the same."

    $ stripper = None #Clear the reference.
    $ not_stripper = None

    $ insta_outfit_mom = insta_wardrobe.pick_random_outfit()
    $ insta_outfit_sister = insta_wardrobe.pick_random_outfit()


    if insta_outfit_mom.name == insta_outfit_sister.name:
        $ the_group.draw_person(the_sister)
        the_sister "I got us matching outfits, because I thought it would really show off the family resemblance."
        the_sister "It should make for a really cute shoot! Maybe [the_sister.mc_title] can tell us who wears it best."


    $ the_mom.apply_outfit(insta_outfit_mom)
    $ the_sister.apply_outfit(insta_outfit_sister)

    "The girls get dressed. [the_mom.title] turns to [the_sister.possessive_title], ready for her inspection."

    $ the_group.draw_person(the_mom)
    the_mom "Okay, am I wearing this right?"
    $ the_group.draw_person(the_sister)
    the_sister "You look great [mom.title], it's so cute on you!"
    $ the_group.draw_person(the_mom)
    if the_mom.judge_outfit(insta_outfit_mom):
        the_mom "Thank you! We need to go shopping together, I think I need more fashion advice from you."
    else:
        the_mom "Are you sure there isn't any more? A slip or a cover-up, maybe?"

    $ the_group.draw_person(the_sister)
    the_sister "Come on [mom.title], we've got to take some pictures now. Get up here."
    $ the_group.draw_person(the_sister, position = "kneeling1", emotion = "happy")
    "[the_sister.title] jumps onto her bed and gets onto her knees, looking towards you and her phone camera."
    $ the_group.draw_person(the_mom)
    the_mom "Okay, I think I can do that..."
    $ the_group.draw_person(the_mom, position = "kneeling1", emotion = "happy")
    "[the_mom.possessive_title] gets onto the bed with [the_sister.possessive_title]."
    mc.name "That's looking good you two, now look at me and smile."
    "You take a few pictures of them, moving around the bed to get a few different angles."
    menu:
        "Get a little friendlier." if not first_time:
            mc.name "Squeeze together you two, I need to get you both in the shot."
            "[the_mom.title] slides closer to [the_sister.title] on the bed."
            the_mom "Like this?"
            mc.name "A little more. Try putting your arms around her."
            "[the_mom.possessive_title] slips behind [the_sister.possessive_title] and pulls her into a hug"
            the_mom "I haven't played ith you like this since you were a kid [the_sister.title]!"
            $ the_group.draw_person(the_sister, position = "kneeling1", emotion = "happy")
            the_sister "Oh my god, you're so embarrassing [the_mom.title]!"
            $ the_group.draw_person(the_mom, position = "kneeling1", emotion = "happy")
            the_mom "[the_mom.mc_title], make sure to get some shots of me embarrassing your sister."
            "She leans over [the_sister.title]'s shoulder and kisses her on the side of the cheek."
            $ the_mom.change_happiness(10)
            $ the_mom.change_slut_temp(2)
            $ the_sister.change_happiness(5)
            "You get some great pictures of [the_mom.title] and [the_sister.title] playing around on the bed together."


        # TODO: Add some extra variations for this as sluttiness and Obedience rises.
        "All done.":
            pass

    mc.name "Alright, I think we've got all the shots we need."
    $ the_group.draw_person(the_mom, emotion = "happy")
    "[the_mom.possessive_title] hops off of the bed."
    the_mom "That was really fun, thanks for inviting me you two."
    $ the_group.draw_person(the_sister, emotion = "happy")
    the_sister "It was! Oh, I should give [the_sister.mc_title] his cut for being our photographer."

    menu:
        "Take the money. +$100":
            $ the_group.draw_person(the_mom)
            the_mom "It's so nice to see you two working well together."
            $ mc.business.funds += 100

        "Let her keep it.":
            mc.name "Don't worry about it, I'm just happy to see you doing something cool."
            $ the_sister.change_love(1)
            the_sister "Aww, you're the best!"
            "She gives you a hug and a quick kiss on the cheek."
            $ the_group.draw_person(the_mom)
            $ the_mom.change_love(1)
            the_mom "You're such a good brother [the_mom.mc_title]."

        "Let [the_mom.title] have it.":
            mc.name "[the_mom.title], you can have what [the_sister.title] normally gives me."
            mc.name "I hope that helps with the bills."
            $ the_group.draw_person(the_mom)
            the_mom "Oh sweetheart, you don't have to..."
            mc.name "Really [the_mom.title], I want you to have it."
            $ the_mom.change_love(2)
            the_mom "Thank you, it really does help."

    if the_mom.judge_outfit(insta_outfit_mom) and not the_mom.wardrobe.has_outfit_with_name(insta_outfit_mom.name):
        the_mom "Say [the_sister.title], do you need this outfit back?"
        $ the_group.draw_person(the_sister)
        the_sister "No, you can keep it if you want. It's obviously not my size, and I don't think they'll take returns."
        $ the_mom.wardrobe.add_outfit(insta_outfit_mom)
        $ the_mom.planned_outfit = insta_outfit_mom #She wears it for the rest of the day.
        the_mom "Thank you! It's so cute, it would be a shame for it to go to waste. Now I need to get back to making dinner!"
        "[the_mom.title] collects her clothing and hurries off to her room. You give [the_sister.title] her phone back and leave her to upload the pics."

    else:
        the_mom "Well, I need to go get changed and get back to making dinner."
        "[the_mom.title] collects her clothing and hurries off to her room. You give [the_sister.title] her phone back and leave her to upload the pics."


    if the_sister.judge_outfit(insta_outfit_sister) and not the_sister.wardrobe.has_outfit_with_name(insta_outfit_sister.name):
        $ the_sister.wardrobe.add_outfit(insta_outfit_sister)


    if the_mom.event_triggers_dict.get("mom_instathot_pic_count", 0) == 0:
        $ the_mom.event_triggers_dict["mom_instathot_pic_count"] = 1
        $ sister_instathot_mom_report_crisis = Action("Sister instathot mom report crisis", sister_instathot_mom_report_requirement, "sister_instathot_mom_report", requirement_args = day)
        $ the_sister.on_talk_event_list.append(sister_instathot_mom_report_crisis)
    else:
        $ the_mom.event_triggers_dict["mom_instathot_pic_count"] += 1

    if the_sister.event_triggers_dict.get("sister_instathot_pic_count", 0) == 0:
        $ the_sister.event_triggers_dict["sister_instathot_pic_count"] = 1
    else:
        $ the_sister.event_triggers_dict["sister_instathot_pic_count"] += 1

    return

label sister_instathot_mom_report(the_person): #Lily tells you that her shots with Mom were super popular and that you want to do more
    $ the_person.draw_person(emotion = "happy")
    the_person "Hey, so you know those pics we took with [mom.title]?"
    mc.name "Yeah? What about them?"
    the_person "I posted them to InstaPic and they've got viral! I already have thousands of new followers!"
    the_person "We need to get her to do more shoots with us, people are going crazy for it!"
    mc.name "Maybe we can even convince her to join in on your nudes."
    "[the_person.possessive_title] shakes her head and laughs."
    the_person "Oh my god, there is no way she would ever do that."
    mc.name "Why not? She had a lot of fun taking pictures with us, and she was already half-naked for that."
    the_person "This would be different. The guys who are asking for these pictures are using them to... you know."
    the_person "I don't think [mom.title] would be okay with that. Plus I would be so embarrassed if I had to tell her."
    mc.name "I think she might surprise you. Maybe I'll talk to her about it."
    the_person "[the_person.mc_title], you can't tell her!"
    mc.name "Relax, I won't tell her anything. I'll just try and see if it's something she'd even consider."
    the_person "Just... don't get me in trouble."
    call talk_person(the_person) from _call_talk_person_14
    return #TODO: Have this event unlock one for Mom asking her to take nudes with Lily. (Maybe as a morning favour?)

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

label sister_pregnant_report(the_person):
    #TODO: Special event called when your sister realises she's pregnant.
    return
