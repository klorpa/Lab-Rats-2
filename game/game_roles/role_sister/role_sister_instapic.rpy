# Contains all of the role events and actions related to Lily's InstaPic storyline.

#TODO: add a punish line for Lilys instathot storyline

init -2 python:
    def instathot_intro_requirement(the_person): #This action sits in her room
        if the_person.sluttiness < 20:
            return False
        elif the_person.event_triggers_dict.get("insta_intro_finished", False):
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
        if not lily_bedroom.has_person(the_person):
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
        elif mom in mc.location.people:
            return False #Don't talk to her in front of her face.
        elif not mc_at_home():
            return False #Don't talk about it outside of the house.
        else:
            return True

    def sister_boobjob_give_serum_requirement(the_person):
        if not the_person.event_triggers_dict.get("sister_boobjob_serum_enabled", False):
            return False
        elif the_person.event_triggers_dict.get("sister_boobjob_serum_count", 0) >= 3:
            return False
        elif the_person.event_triggers_dict.get("sister_boobjob_serum_last_day", -1) >= day:
            return "Already taken a dose today."
        else:
            return True

    def sister_serum_new_boobs_check_requirement(the_person, start_size, end_day):
        if the_person.rank_tits(the_person.tits) - the_person.rank_tits(start_size) >= 2:
            return True #Her boobs grew, she'll trigger her brag event
        elif day >= end_day:
            return True #It's been too long, she'll trigger the fail/timeout event.
        else:
            return False #Don't trigger until one of those conditions is met.

    def sister_got_boobjob_requirement(start_day):
        if day < start_day:
            return False
        return True

    def sister_get_boobjob_talk_requirment(the_person):
        if the_person.event_triggers_dict.get("sister_boobjob_ask_enabled", False):
            return True
        return False

    def sister_boobjob_brag_requirement(the_person):
        return True

    def sister_serum_boobjob_fail_requirement(the_person):
        return True

label sister_instathot_intro_label(the_person):
    # Your sister needs you to take pictures for her.
    # She's got an InstaPic (genius, they'll never guess!) account and wants to be an "influencer"
    # Triggers at some point when you go into your sisters room. You catch her taking pictures for InstaPic, but she doesn't mind and explains what she's doing.
    # Adds a random event where Lily posts InstaPics, similar to your mom sending you selfies.


    # Actually, let's have her start with a relatively tame outfit and grow into really sexy ones.
    "You open the door to [the_person.possessive_title]'s room."
    $ the_person.draw_person(position = "kneeling1")
    $ mc.change_locked_clarity(10)
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
            $ mc.change_locked_clarity(10)
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

    call setup_sister_insta(the_person)
    $ clear_scene()
    return

label setup_sister_insta(the_person):
    if not the_person.has_role(instapic_role):
        $ the_person.special_role.append(instapic_role)
    $ the_person.event_triggers_dict["insta_known"] = True
    $ the_person.event_triggers_dict["insta_intro_finished"] = True # Other events may set this is you discover her instapic career some other way
    $ sister_instathot_action = Action("Help her take Insta-pics.{image=gui/heart/Time_Advance.png}",instathot_requirement, "sister_instathot_label", menu_tooltip = "Help your sister grow her InstaPic account by taking some pictures of her.")
    $ sister_role.actions.append(sister_instathot_action)
    return

label sister_instathot_label(the_person):
    #Help your sister take slutty pictures for the internet. Get a share of the cash she's earning on them.
    #Requires you to be in Lily's bedroom with her, so we can assume that's true.
    mc.name "I've got some spare time, do you want some help taking pictures for InstaPic?"
    if the_person.event_triggers_dict.get("sister_kissing_quest_active", False):
        $ the_person.event_triggers_dict["sister_kissing_quest_progress"] = the_person.event_triggers_dict.get("sister_kissing_quest_progress",0) + 1

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

    $ skip_change = False
    if the_person.has_taboo(["bare_tits", "bare_pussy"]):
        "She looks at you expectantly."
        the_person "Can, you give me a moment? I'm not going to get undressed in front of you."
        menu:
            "Ask to watch.":
                mc.name "Let me watch, it'll be fun."
                if the_person.get_opinion_score(["showing her tits", "showing her ass", "not wearing anything"]) > 0:
                    "[the_person.possessive_title] rolls her eyes and shrugs."
                    the_person "You aren't going to be weird about this, are you?"
                    mc.name "Of course not [the_person.title]. We don't want [mom.title] wondering why I'm standing in the hall, right?"
                    the_person "Good point. Alright, you can stay."
                    $ the_person.break_taboo("bare_tits")
                    $ the_person.break_taboo("bare_pussy")

                elif the_person.effective_sluttiness() >= 30:
                    the_person "Fun for you, maybe. WHat am I getting out of it?"
                    mc.name "I'm helping you out already, aren't I? Come on [the_person.title], it's not a big deal."
                    "She thinks for a moment, but finally shrugs her acceptance."
                    $ the_person.change_love(-1)
                    the_person "You're weird, you know that? You need a girlfriend."
                    $ the_person.break_taboo("bare_tits")
                    $ the_person.break_taboo("bare_pussy")

                else:
                    the_person "Ew, that's fun for you? I'm your sister [the_person.mc_title]!"
                    mc.name "So?"
                    "She scoffs and shakes her head."
                    the_person "Yeah, that's not happening. Come on, we need to do this quick before [mom.title] gets curious."
                    $ clear_scene()
                    "You get the sense that she's not going to change her mind, so you step out into the hallway."
                    $ skip_change = True

            "Let her change.":
                $ skip_change = True
                mc.name "Right, sure."
                $ clear_scene()
                "You step out into the hallway so [the_person.possessive_title] can get changed."


    if skip_change:
        "You consider risking a peek, but the soft click of her door lock cuts that thought short."
        $ the_person.draw_person()
        "After a short wait there's another click and she opens the door."
        the_person "Come back in!"
        if the_person.event_triggers_dict.get("insta_special_request_outfit", False):
            $ insta_outfit = the_person.event_triggers_dict.get("insta_special_request_outfit")
            $ the_person.apply_outfit(insta_outfit, update_taboo = True)
            $ mc.change_locked_clarity(10)
            the_person "A fan said I should wear this. Isn't it cute?"
            $ the_person.draw_person()

        else:
            $ the_person.apply_outfit(insta_outfit, update_taboo = True)
            $ the_person.draw_person()
            the_person "It's cute, right?"

    else:
        $ strip_list = the_person.outfit.get_full_strip_list()
        $ generalised_strip_description(the_person, strip_list)
        $ the_person.update_outfit_taboos()
        $ the_person.draw_person(position = "doggy")
        $ mc.change_locked_clarity(20)
        "She gets onto her knees and pulls a shopping bag from the mall out from under her bed."
        the_person "I keep my stuff here so Mom doesn't find it. Okay, let's put this on!"
        $ the_person.draw_person(emotion = "happy")
        "[the_person.title] gets dressed in her new outfit and turns to you, smiling."

        if the_person.event_triggers_dict.get("insta_special_request_outfit", False):
            $ insta_outfit = the_person.event_triggers_dict.get("insta_special_request_outfit")
            $ the_person.apply_outfit(insta_outfit, update_taboo = True)
            $ mc.change_locked_clarity(10)
            the_person "A fan said I should wear this. Isn't it cute?"

        else:
            $ the_person.apply_outfit(insta_outfit, update_taboo = True)
            $ the_person.draw_person(emotion = "happy")
            the_person "Well, do you think they'll like it?"
            menu:
                "Of course!":
                    mc.name "Of course, you look hot!"
                    $ the_person.change_slut(1, 30)
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
    $ mc.change_locked_clarity(10)
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
                    $ the_person.event_triggers_dict["insta_special_request_asap"] = True #Flags you to receive a response as soon as possible, ignoring random chance.

            "Don't help":
                mc.name "That's going a little far. Let's end here, okay?"
                "She pouts, but nods."
                the_person "Fine..."

    else:
        "Finally she's happy with what she's got and takes her phone back."
        $ the_person.draw_person(emotion = "happy")
        the_person "Thanks so much [the_person.mc_title], these look amazing!"
        $ the_person.change_slut(1, 40)
    the_person "I guess I should pay you, huh? Since you're doing all this work for me."
    $ money_amount = 100 + 50*(Person.rank_tits(the_person.tits)-4)
    if money_amount < 50:
        $ money_amount = 50
    menu:
        "Take the money. +$[money_amount]":
            mc.name "I'm not going to say no."
            "She rolls her eyes and direct transfers you some cash."
            $ mc.business.change_funds(money_amount)
            the_person "No, I didn't think you would Mr.\"I own a business\"."

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
                            $ the_person.event_triggers_dict["insta_special_request_asap"] = True #Flags you to receive a response as soon as possible, ignoring random chance.

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
                            $ the_person.event_triggers_dict["insta_special_request_asap"] = True #Flags you to receive a response as soon as possible, ignoring random chance.


                    "Not right now.":
                        mc.name "I've got something else to get to. Sorry [the_person.title]."
                        the_person "Oh, that's fine. I'll just go take it in the bathroom mirror I guess."

        else:
            call sister_instathot_special_intro(the_person, is_topless_shoot) from _call_sister_instathot_special_intro

    if the_person.event_triggers_dict.get("sister_instathot_pic_count", 0) == 0:
        $ the_person.event_triggers_dict["sister_instathot_pic_count"] = 1
    else:
        $ the_person.event_triggers_dict["sister_instathot_pic_count"] += 1
    $ the_person.apply_outfit() #She gets redressed in something decent.
    return

label sister_instathot_special_intro(the_person, is_topless_shoot = True):
    #Your sister lets you know that someone on insta is asking for "special" pictures. She's unsure if she should do it, but it's a lot of money.
    #Triggered when she's asked for a topless or nude shot
    $ the_person.event_triggers_dict["sister_insta_special_intro"] = True
    the_person "Wait, before you go I wanted to ask you something..."
    mc.name "What is it?"
    the_person "Ever since I started my insta-posts I've had guys sending me creepy messages, usually asking me to show my... you know."
    "She shrugs and laughs nervously."
    $ mc.change_locked_clarity(10)
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
            the_person "Yeah, you're probably right. I would die of embarrassment if [mom.title] found them."
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
    $ mc.change_locked_clarity(10)

    if the_person.outfit.tits_visible() or the_person.outfit.vagina_visible():
        the_person "Hmm, I guess I should actually put on some underwear. One second!"
        "[the_person.possessive_title] turns and starts to look through her wardrobe."
        $ the_person.apply_outfit(the_person.wardrobe.get_random_appropriate_underwear(the_person.sluttiness))
        if the_person.outfit.tits_visible() or the_person.outfit.vagina_visible():
            the_person "Hmm... Well, this will have to do I guess. They'll get a little more than they paid for I suppose!"
        "She gets changed quickly, then turns back to you."

    $ the_person.draw_person()
    the_person "Okay, let's get started then!"
    if the_person.effective_sluttiness() < 40:
        the_person "I just need one or two good pics to send this guy."
    else:
        the_person "Let's make sure we get something sexy for this guy, okay?"

    $ the_person.draw_person(position = "back_peek")
    $ mc.change_locked_clarity(10)
    "You take some shots for [the_person.possessive_title] while she poses in her underwear."
    the_person "Okay, there should be something good there. Let me take a look!"
    "She hurries over to you and holds onto your arm as you flick through the pictures you just took."
    the_person "Ooh, that one looks good. I'll send him that one, and maybe that one..."
    $ the_person.change_slut(1, 50)
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
                strip_list = the_person.outfit.get_half_off_to_tits_list()
            generalised_strip_description(the_person, strip_list, half_off_instead = half_off_instead)
        else:
            strip_list = the_person.outfit.get_full_strip_list()
            generalised_strip_description(the_person, strip_list)
    $ mc.change_locked_clarity(20)

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
        $ mc.change_locked_clarity(10)
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
                    $ mc.change_locked_clarity(5)
                    the_person "Oh, something like... Ah... I'm totally cumming."
                    mc.name "Come on, I'm serious. The pictures will look better if you act it out and really pretend."
                    mc.name "Think about what makes you cum, imagine you're right at the edge and it's all you want."
                    the_person "Fine, I'll try..."
                    $ the_person.draw_person(position = "kneeling1", emotion = "orgasm")
                "She wiggles her shoulders and takes a few deep, sensual breaths."
                $ mc.change_locked_clarity(10)
                the_person "Oh my god, I'm going to cum! I'm going to cum so fucking hard!"
                the_person "Fuck, I'm cuming! I'm cumming [the_person.mc_title]! Mmm!"
                $ mc.change_locked_clarity(10)
                "She rolls her eyes up towards the ceiling as she pretends to orgasm. You get a few more shots and push her for more."
                mc.name "That's it, keep going. What's making you cum [the_person.title]? Tell me!" #TODO: If we ever add more opinion information we can tie that in here.
                $ mc.change_locked_clarity(10)
                the_person "Your big cock is making me cum! I'm such a dirty little slut, cumming on your huge dick!"
                "[the_person.possessive_title] is panting loudly now as she continues to give a very convincing performance."
                "...At least you're pretty sure it's a performance."
                "You try to ignore the throbbing erection you have now and get a few more shots of [the_person.title]."
                the_person "Cuuuumming! Aaaah! Ah... Ah...."
                $ mc.change_locked_clarity(10)
                "[the_person.title] rolls her eyes up as far as she can, sticks her tongue out, and squeels happily for the camera."
                "You get the last shot - definitely the best of the lot - nod to [the_person.possessive_title]."
                "She takes a moment to recover from her theatrics, then hops off her bed and hurries over to you."

        $ the_person.draw_person(emotion = "happy")
        the_person "That felt so silly, but I bet they'll like it! Come on, show me how they turned out!"
        "[the_person.title] holds onto your arm as you flip through all of the shots you just took together."
        if not the_person.has_large_tits() and not the_person.event_triggers_dict.get("sister_boobjob_in_progress", False): #NOTE: She may end up with bigger tits due to normal serum use, so this event shouldn't be _manditory_
            the_person "Those look great! It's just..."
            $ the_person.draw_person(emotion = "sad")
            mc.name "What? What's wrong?"
            the_person "Oh, nothing. Sometimes I just wish my boobs were a little larger."
            the_person "Look at [mom.title], she's got huge boobs! These are..."
            "She grabs her chest and squeezes her tits in her hands."
            the_person "...A little small. All the really popular girls on InstaPic have big boobs."
            menu:
                "Get bigger tits":
                    mc.name "Then you should do something about it. You know you can just get fake boobs, right?"
                    the_person "Obviously. I've looked into it and it's super expensive."
                    if the_person.event_triggers_dict.get("sister_instathot_mom_enabled", False): #Mom already knows about her "hobby"
                        the_person "And what would I tell [mom.title]?"
                        mc.name "You thought she would be angry about your InstaPic account, and she turned out to love it."
                        mc.name "Maybe she would be fine with this too."
                        the_person "Maybe... I don't know, I don't think it's a good idea."
                        menu:
                            "I'll convince her for you.":
                                $ the_person.event_triggers_dict["sister_boobjob_in_progress"] = True
                                $ the_person.event_triggers_dict["sister_boobjob_convince_mom_enabled"] = True #Enables a branch in the InstaPic event.
                                mc.name "What if I convince her for you?"
                                "[the_person.possessive_title] laughs and shakes her head in disbelief."
                                the_person "Sure, good luck with that. Just don't tell her I'm taking these \"special\" pictures, alright?"
                                mc.name "Of course, I won't tell her anything. I'll just mention it next time you're taking some InstaPic's together."
                                the_person "That's going to be so embarrassing! But if you think it will actually work, I guess you can try it."

                            "Use serum instead.":
                                $ the_person.event_triggers_dict["sister_boobjob_in_progress"] = True
                                $ the_person.event_triggers_dict["sister_boobjob_serum_enabled"] = True
                                $ the_person.event_triggers_dict["sister_boobjob_serum_count"] = 0
                                mc.name "I might have another way which wouldn't require any surgery, and nothing for [mom.title] to be upset about."
                                the_person "Really? What would that be?"
                                mc.name "My lab is developing a breast enhancement drug. It's experimental, but I think it has a good chance of working for you."
                                mc.name "[mom.title] won't care if she thinks your boobs are just developing naturally."
                                "[the_person.possessive_title] cocks her head, curious."
                                the_person "That.. could work. Do you really have something that can do that?"
                                mc.name "Of course I do, I wouldn't lie to you."
                                $ sister_boobjob_serum_check_action = Action("sister_serum_boobjob_check", sister_serum_new_boobs_check_requirement, "sister_serum_new_boobs_check", args = [the_person, the_person.tits], requirement_args = [the_person, the_person.tits, day + 10])
                                $ mc.business.mandatory_crises_list.append(sister_boobjob_serum_check_action) #Check every turn to see if her boobs have grown.
                                menu:
                                    "Give her some serum right now.":
                                        call give_serum(the_person)
                                        if _return == False:
                                            mc.name "I'll need to pick some up from the lab first."
                                            the_person "Okay, bring it to me when you have it then."
                                            the_person "Oh, and thank you for helping me [the_person.mc_title]!"
                                        else:
                                            $ the_person.event_triggers_dict["sister_boobjob_serum_count"] += 1
                                            $ the_person.event_triggers_dict["sister_boobjob_serum_last_day"] = day
                                            mc.name "Here, drink this."
                                            "[the_person.possessive_title] takes the vial and looks at it."
                                            the_person "You just walk around with boob growing stuff in your pocket?"
                                            mc.name "It was a prototype, I was working on it when I left the lab last."
                                            "She shrugs and drinks the contents of the vial."
                                            the_person "Ah... So, now what?"
                                            mc.name "It might take some time, and it might take a few doses."
                                            the_person "Alright, I guess I'll just let you know if I see any changes then."

                                    "Bring her some serum later.":
                                        mc.name "I'll need to pick up some from the lab first."
                                        the_person "Okay, bring it to me when you have it then."
                                        the_person "Oh, and thank you for helping me [the_person.mc_title]!"

                                $ mc.change_locked_clarity(5)
                                "[the_person.title] gives you a quick hug."


                        the_person "Well, thanks for the help with the pics. That was fun."


                    else: #Mom doesn't know
                        the_person "And what would I tell [mom.title]? I would have to tell her about my InstaPic account, and she would make me take it down."
                        mc.name "I think you might be surprised."
                        the_person "Maybe, but I don't want to take that risk. I'm just happy with how things are going now."

                "They're fine.":
                    mc.name "You're worrying too much [the_person.title]. Your tits look great."
                    "She shrugs."
                    the_person "Yeah, you're probably right. Hey, thanks for the help!"
        else:
            $ the_person.change_happiness(5 + the_person.get_opinion_score("showing her tits"))
            the_person "Those look great! Look at my tits, don't they look fantastic? I'm so glad they're bigger now!"
            "She scoops up her tits and jiggles them playfully."
            the_person "This guy is going to cum just looking at them!"
    else:
        the_person "Yay! Let me see how they turned out!"
        $ the_person.draw_person(emotion = "happy")
        $ mc.change_locked_clarity(10)
        if is_topless_shoot:
            "[the_person.title] hops off of the bed and hurries to your side. She holds onto your arm as you flick through her topless shots."
        else:
            "[the_person.title] hops off of the bed and hurries to your side. She holds onto your arm as you flick through her new nudes."
        the_person "... Oh, that one's cute. I think I'll send him that one. Thank you so much [the_person.mc_title]!"
    $ the_person.change_slut(1, 30)
    "She gives you a hug and takes her phone back."
    if the_person.event_triggers_dict.get("sister_insta_special_count", 0) == 0:
        $ the_person.event_triggers_dict["sister_insta_special_count"] = 1
    else:
        $ the_person.event_triggers_dict["sister_insta_special_count"] += 1

    $ the_person.event_triggers_dict["sister_instathot_special_pictures_recent"] = True # Triggers an event for Mom to ask where Lily is getting this money.
    return

label sister_instathot_mom_discover(the_person):
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
            $ the_person.change_slut(2, 60)
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
            $ mc.change_locked_clarity(20)
            the_mom "[the_sister.title], I want the whole experience! These outfits will get you more view on your insta... view... pic thing, right?"
            the_mom "Come on, show me what you picked out for me. I'm sure I can squeeze into it with a little bit of work."
        else:
            the_sister "First I need to pick an outfit and get changed."
            the_sister "You don't have to change anything though, I'll just..."
            $ the_group.draw_person(the_mom)
            "[the_mom.title] shakes her head and interrupts."
            $ mc.change_locked_clarity(20)
            the_mom "[the_sister.title], I want the whole experience! Don't you want more views on your insta... view... pic thing?"
            the_mom "Come on, show me what you have. I'm sure you have something I can squeeze into."
        $ the_group.draw_person(the_sister)
        "[the_sister.possessive_title] smiles and nods. She waves [the_mom.possessive_title] over to the pile of clothes she has laid out on her bed."
        the_sister "Really? Alright! Well, I've got this a few days ago that's really cute and..."
        "You lean against a wall and pass some time on your phone while [the_sister.possessive_title] and [the_mom.title] pick out outfits."
        the_sister "Right, I think these are going to drive them wild. Come on, let's see how they look!"

        $ mom_start_instapic_event = Action("mom start instapic", mom_instapic_setup_intro_requirement, "mom_instapic_setup_intro", requirement_args = day + renpy.random.randint(3,5))
        $ the_mom.on_room_enter_event_list.append(mom_start_instapic_event) #She'll want to start her own Instapic account in a few days (assuming she doesn't already have one)

        $ mom_start_instapic_alternative_event = Action("mom alt start instapic", mom_instapic_alt_intro_requirement, "mom_instapic_alt_intro", requirement_args = day + renpy.random.randint(3,5))
        $ the_mom.on_room_enter_event_list.append(mom_start_instapic_alternative_event) #If she ends up with an Instapic account in some other way (or already has one) this intros the help options.


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
    $ mc.change_locked_clarity(30)
    "[stripper.title] finishes stripping naked and starts to put on her outfit. [not_stripper.title] is naked now too, and is doing the same."

    $ stripper = None #Clear the reference.
    $ not_stripper = None

    $ insta_outfit_mom = insta_wardrobe.pick_random_outfit()
    $ insta_outfit_sister = insta_wardrobe.pick_random_outfit()


    if insta_outfit_mom.name == insta_outfit_sister.name:
        $ the_group.draw_person(the_sister)
        $ mc.change_locked_clarity(10)
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
    $ mc.change_locked_clarity(20)
    "[the_mom.possessive_title] gets onto the bed with [the_sister.possessive_title]."
    mc.name "That's looking good you two, now look at me and smile."
    "You take a few pictures of them, moving around the bed to get a few different angles."
    menu:
        "Get a little friendlier." if not first_time:
            mc.name "Squeeze together you two, I need to get you both in the shot."
            "[the_mom.title] slides closer to [the_sister.title] on the bed."
            the_mom "Like this?"
            mc.name "A little more. Try putting your arms around her."
            $ mc.change_locked_clarity(20)
            "[the_mom.possessive_title] slips behind [the_sister.possessive_title] and pulls her into a hug"
            the_mom "I haven't played with you like this since you were a kid [the_sister.title]!"
            $ the_group.draw_person(the_sister, position = "kneeling1", emotion = "happy")
            the_sister "Oh my god, you're so embarrassing [the_mom.title]!"
            $ the_group.draw_person(the_mom, position = "kneeling1", emotion = "happy")
            $ mc.change_locked_clarity(20)
            the_mom "[the_mom.mc_title], make sure to get some shots of me embarrassing your sister."
            "She leans over [the_sister.title]'s shoulder and kisses her on the side of the cheek."
            $ the_mom.change_happiness(10)
            $ the_mom.change_slut(2, 40)
            $ the_sister.change_happiness(5)
            "You get some great pictures of [the_mom.title] and [the_sister.title] playing around on the bed together."

            #TODO:
            menu:
                "Take your tits out.":
                    mc.name "This is really good stuff, but I want just a little bit more."
                    mc.name "How about you take your shirts off now girls."
                    if the_mom.has_taboo("bare_tits"):
                        $ the_mom.change_obedience(-1)
                        $ the_group.draw_person(the_mom)
                        "[the_mom.possessive_title] scoffs and shakes her head."
                        the_mom "Don't even joke about that [the_mom.mc_title]! It's obviously wrong for your mother and sister to have their shirts off in front of you."
                        $ the_group.draw_person(the_sister)
                        the_sister "Aww, come on..."
                        $ the_group.draw_person(the_mom)
                        "[the_mom.title] interrupts her sharply."
                        the_mom "I said no, now that's the end of it!"
                        $ the_group.draw_person(the_sister)
                        "[the_sister.possessive_title] glances at you and shrugs."

                    elif the_sister.event_triggers_dict.get("mom_sister_instapic_shirtless_count", 0) == 0:
                        $ the_group.draw_person(the_mom)
                        the_mom "[the_mom.mc_title], don't joke like that in front of your sister."
                        $ the_group.draw_person(the_sister)
                        the_sister "Aww come on [the_mom.title], let's do it! It's just a little bit of fun, and I know [the_sister.mc_title] doesn't care."
                        $ the_group.draw_person(the_mom)
                        the_mom "I thought you said InstaPic doesn't let you post nude pictures? Won't they kick you off the site?"
                        $ the_group.draw_person(the_sister)
                        the_sister "Well they don't, but... Uh... [the_sister.mc_title], what do you think?"
                        "She looks at you, hopeful that you have a way to convince her."

                        $ tease_requirement = 50 - 10*the_mom.get_opinion_score(["showing her tits", "incest"])
                        $ tease_token = get_red_heart(tease_requirement)
                        menu:
                            "It's just for fun!" if the_mom.get_known_opinion_score("showing her tits") > 0:
                                $ the_group.draw_person(the_mom)
                                mc.name "It's just for the fun of it, really."
                                mc.name "You're up for a little fun, right [the_mom.title]? Unless you're not confident about your tits."
                                the_mom "Oh, I'm plenty confident in them, and it does sound like fun..."
                                "[the_mom.possessive_title] thinks for a moment."
                                the_mom "Screw it, they won't look like this forever so we might as well have some fun with them while we can!"
                                the_mom "Now you two aren't going to be doing any with these shots, right? They'll be deleted after?"
                                $ the_group.draw_person(the_sister)
                                the_sister "Yeah, of course [the_mom.title]. Of course..."
                                call sister_instathot_label_mom_shirtless(the_sister, the_mom, the_group)

                            "It's just for fun!\nRequires: [the_mom.title] likes showing her tits (disabled)" if the_mom.get_known_opinion_score("showing her tits") <= 0:
                                pass

                            "We're just going to tease them." if the_mom.effective_sluttiness() >= tease_requirement:
                                $ the_group.draw_person(the_mom)
                                mc.name "Don't worry [the_mom.title], we're just going to take some teasing shots."
                                mc.name "You cover up [the_sister.title] and she covers you up. Nothing that breaks the rules, but it still gets a lot of views."
                                $ the_group.draw_person(the_sister)
                                "[the_sister.possessive_title] nods encouragingly."
                                the_sister "Yeah, that's it. You'll do ti for me, right [the_mom.title]?"
                                call sister_instathot_label_mom_shirtless(the_sister, the_mom, the_group)

                            "We're just going to tease them.\nRequires: [the_mom.title] [tease_token] (disabled)" if the_mom.effective_sluttiness() < tease_requirement:
                                pass

                            "Just do it [the_mom.title]." if the_mom.obedience >= 140:
                                $ the_group.draw_person(the_mom)
                                mc.name "Why do you have to make this complicated [the_mom.title]? Just do it."
                                $ the_group.draw_person(the_sister)
                                "[the_sister.possessive_title]'s jaw goes slack as you talk to her mother like that. She starts to stammer an apology."
                                the_sister "He doesn't mean that..."
                                $ the_group.draw_person(the_mom)
                                the_mom "It's okay [the_sister.title]. Sorry [the_mom.mc_title], I didn't mean to argue."
                                $ the_group.draw_person(the_sister)
                                "[the_sister.title] glances at you, confused."
                                the_sister "Right then..."
                                call sister_instathot_label_mom_shirtless(the_sister, the_mom, the_group)

                            "Just do it [the_mom.title]\nRequires: [the_mom.title] 140 Obedience. (disabled)" if the_mom.obedience < 140:
                                pass

                            #TODO: have an onlyfans option if they both have an account.

                            "Uh...":
                                mc.name "Uh... Up to you guys?"

                                the_mom "I don't want to get your account banned [the_sister.title]. Let's just get a few more shots like this and call it a day."
                                the_sister "Alright [the_mom.title], you're probably right."
                                "[the_sister.possessive_title] rolls her eyes."


                    else: #You've already convinced her, so she'll just do it.
                        $ the_group.draw_person(the_sister)
                        the_sister "What do you say [the_mom.title]? Up for it?"
                        $ the_group.draw_person(the_mom)
                        the_mom "I'm not here to cramp your style. Let's do it!"
                        call sister_instathot_label_mom_shirtless(the_sister, the_mom, the_group)

                # "Get some OnlyFanatics content." if the_mom.event_triggers_dict.get("onlyfans_known", False) and the_sister.event_triggers_dict.get("onlyfans_known", False):
                #     if first_time:
                #         pass
                #     else:
                #         pass
                #     #TODO: Lead into some lesbian action with the two of them.
                #     #TODO: Leave some obvious places for threesome action.

                "All done.":
                    pass

        "Bring up [the_sister.title]'s boobs." if the_sister.event_triggers_dict.get("sister_boobjob_convince_mom_enabled", False):
            call sister_convince_mom_boobjob(the_mom, the_sister)

        # TODO: Add some extra variations for this as sluttiness and Obedience rises.
        "All done.":
            pass

    mc.name "Alright, I think we've got all the shots we need."
    $ the_group.draw_person(the_mom, emotion = "happy")
    "[the_mom.possessive_title] hops off of the bed."
    the_mom "That was really fun, thanks for inviting me you two."
    $ the_group.draw_person(the_sister, emotion = "happy")
    the_sister "It was! Oh, I should give [the_sister.mc_title] his cut for being our photographer."
    $ money_amount = 100 + 50*(Person.rank_tits(the_sister.tits)-4) + 50*(Person.rank_tits(the_mom.tits)-4)
    if money_amount < 50:
        $ money_amount = 50
    menu:
        "Take the money. +$[money_amount]":
            $ the_group.draw_person(the_mom)
            the_mom "It's so nice to see you two working well together."
            $ mc.business.change_funds(money_amount)

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

label sister_instathot_label_mom_shirtless(the_sister, the_mom, the_group): #Called when you convince them to take some shirtless pics.
    #TODO: Have extra options if htey have Onlyfans accounts.
    $ the_sister.event_triggers_dict["mom_sister_instapic_shirtless_count"] = the_sister.event_triggers_dict.get("mom_sister_instapic_shirtless_count", 0) + 1
    $ the_item = the_sister.outfit.get_upper_top_layer()
    "[the_sister.possessive_title] starts to strip off her [the_item.display_name], and [the_mom.possessive_title] follows her lead."
    $ generalised_strip_description(the_sister, the_sister.outfit.get_tit_strip_list(), group_display = the_group, other_people = [(the_mom, the_mom.outfit.get_tit_strip_list())])
    $ mc.change_locked_clarity(20)

    $ the_group.draw_person(the_mom)
    if the_mom.has_large_tits():
        "With her tits out [the_mom.title] cups them with her hands. They're more than a handful, but she does succeed in hiding her nipples away from the camera."
    else:
        "With her tits out [the_mom.title] cups them with her hands. She manages to cover most of herself up, while still looking hot for the camera."
    the_mom "Come on [the_sister.title], hold them like this so we aren't showing too much for the camera."
    $ the_group.draw_person(the_sister)
    the_sister "Let's see, like this?"
    $ mc.change_locked_clarity(10)
    "She does the same, grabbing her breasts and holding them tight to her chest with her hand bra."
    the_sister "How do we look [the_sister.mc_title]?"
    mc.name "Fantastic, let me get a few pictures..."

    if the_sister.event_triggers_dict.get("sister_instathot_mom_shirtless_covered_count", 0) > 0:

        $ cover_other_requirement = 45
        $ red_heart_token = get_red_heart(cover_other_requirement)

        menu:
            #TODO: Enable this if they both have an onlyfans account.
            "Cover each other's tits." if (the_mom.effective_sluttiness() >= 50 or the_mom.get_known_opinion_score("incest") > 0) and (the_sister.effective_sluttiness() >= 50 or the_sister.get_known_opinion_score("incest") > 0):
                mc.name "Let's try a few different poses now. [the_mom.title], sit behind [the_sister.title] and hold onto her boobs for her."
                mc.name "[the_sister.title], all you have to do is make sure your body is in the way of [the_mom.title]'s tits. Can you do that?"
                the_sister "Yeah, I can do that [the_sister.mc_title]."
                #TODO: Have some sort of taboo style system for Mom and Lily.
                $ the_group.draw_person(the_mom)
                the_mom "Are you okay with this [the_sister.title]?"
                $ the_group.draw_person(the_sister)
                the_sister "Of course [the_mom.title]! Come on, here..."
                $ mc.change_locked_clarity(10)
                "She wraps [the_mom.possessive_title]'s arms around her and presses her hands against her tits."
                the_sister "There, no big deal!"
                $ the_group.draw_person(the_mom)
                the_mom "Oh! Well... [the_mom.mc_title], take the pictures!"
                "[the_sister.title] leans back, squishing herself up against [the_mom.title]'s tits. You get a few hot shots that might just survive on InstaPic."
                mc.name "What do [the_sister.title]'s tits feel like [the_mom.title]?"
                "[the_mom.possessive_title] jiggles her daughter's tits experimentally, without really thinking about it."
                the_mom "They're so perky! Oh, the benefits of youth!"

                if the_sister.event_triggers_dict.get("sister_instathot_mom_shirtless_uncovered_count", 0) > 0:
                    $ show_them_requirement = 50
                    $ red_heart_token = get_red_heart(show_them_requirement)

                    menu:
                        "Now show them to the camera." if (the_mom.effective_sluttiness() >= show_them_requirement or the_mom.get_known_opinion_score("incest") > 0) and (the_sister.effective_sluttiness() >= show_them_requirement or the_sister.get_known_opinion_score("incest") > 0):
                            mc.name "That's great, now [the_sister.title], just lean to the side so we can see [the_mom.title]'s tits."
                            if first_time:
                                $ the_group.draw_person(the_mom)
                                the_mom "Oh, I don't know..."
                                "[the_sister.title] doesn't hesitate. She shuffles to the side on her bed, and [the_mom.possessive_title] pulls her hands back suddenly to cover herself."
                                "Of course, this means she's not covering up her daughter any more."
                                $ the_group.draw_person(the_sister)
                                the_sister "Well I don't care. How do I look [the_sister.mc_title]?"
                                if the_sister.has_large_tits():
                                    "[the_sister.possessive_title] shakes her shoulders, jiggling her big for the camera."
                                else:
                                    "[the_sister.possessive_title] shakes her shoulders, jiggling her little tits for the camera."
                                the_sister "Come on [the_mom.title], just show them off a little!"
                                $ the_group.draw_person(the_mom)
                                the_mom "Well... Just a little can't hurt..."
                                "She lowers her hands tenatively from her chest, letting her boobs spill free from. They take a few seconds to stop jiggling."

                            else:
                                $ the_group.draw_person(the_sister)
                                the_sister "Right away boss!"
                                "She shuffles to the side on her bed, leaving [the_mom.title]'s tits uncovered."
                                $ the_group.draw_person(the_mom)
                                the_mom "Oh you two... Alright, just a few shots..."
                                "She takes her hands off of [the_sister.title]'s breasts and puts them on the bed."

                            mc.name "Perfect. Shake 'em around a little bit. Give me something to work with..."
                            $ mc.change_locked_clarity(10)
                            "The girls shake their shoulders, working their tits around for you."
                            $ the_group.draw_person(the_mom)
                            the_mom "Like this? I'm not sure if I'm doing this right..."
                            mc.name "That's great... Really just great..."
                            #TODO: Here's where you can get them to start touching each other.
                            #TODO: Do that in the future.

                        "Now show them to the camera.\nRequires: both [red_heart_token] or likes incest (disabled)" if the_mom.effective_sluttiness < 55:
                            pass

                else:
                    "[the_sister.title] laughs, and [the_mom.possessive_title] seems to realise exactly what she's doing."
                    the_mom "Oh my god... I'm sorry [the_sister.title]!"
                    $ the_group.draw_person(the_sister)
                    the_sister "It's fine [the_mom.title], it's fun!"
                    $ the_group.draw_person(the_mom)
                    "[the_mom.title] pulls her hands back and wraps them around her own chest."
                    the_mom "I... I still think that's enough for today."
                    "[the_sister.possessive_title] shrugs, apparently unworried about showing off her own tits."

                $ the_sister.event_triggers_dict["sister_instathot_mom_shirtless_uncovered_count"] = the_sister.event_triggers_dict.get("sister_instathot_mom_shirtless_uncovered_count", 0) + 1

            "Cover each other's tits.\nRequires: both [red_heart_token] or likes incest (disabled)" if the_mom.effective_sluttiness() < cover_other_requirement or the_sister.effective_sluttiness() < cover_other_requirement:
                pass

            "All done.":
                pass

        if not the_mom.event_triggers_dict.get("mom_instapic_banned", False): #TOD: Check if we've already triggerded this for Mom
            $ mom_insta_ban_event = Action("Mom InstaPic Ban", mom_instapic_ban_requirement, "mom_instapic_ban", requirement_args = day + renpy.random.randint(3,5))
            $ the_mom.on_room_enter_event_list.append(mom_insta_ban_event)

    else:
        "You take some great shots of them with their shirts off."

    $ the_sister.event_triggers_dict["sister_instathot_mom_shirtless_covered_count"] = the_sister.event_triggers_dict.get("sister_instathot_mom_shirtless_covered_count", 0) + 1
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

label sister_convince_mom_boobjob(the_mom, the_sister):
    if the_sister.event_triggers_dict.get("mom_boobjob_convince_first_try", True):
        $ the_sister.event_triggers_dict["mom_boobjob_convince_first_try"] = False
        mc.name "That's a good start. [the_mom.title], try and puff your chest out a little more for me."
        $ mc.change_locked_clarity(10)
        "[the_mom.possessive_title] rolls her shoulders back, emphasising her large breasts for the camera."
        the_mom "Umm, like this? Sorry, I'm not very good at this."
        mc.name "Don't worry about that, you've got such large boobs that it's easy to make them look good."
        "You get a few pictures of [the_mom.title] with [the_sister.possessive_title] beside her."
        mc.name "Good thing too, big tits are the number one thing that gets you views on InstaPic."
        the_mom "Don't be so crude [the_mom.mc_title], I'm sure that's not true. Right [the_sister.title]?"
        $ the_group.draw_person(the_sister, position = "kneeling1")
        "[the_sister.possessive_title] shrugs."
        the_sister "No, he's right about that. All of the top influencers have big boobs. Bigger than me, at least."
        mc.name "It can be real hard for flat chested girls like [the_sister.title] to make an impact."
        $ the_group.draw_person(the_mom, position = "kneeling1")
        the_mom "[the_sister.title] isn't flat chested, they're just a bit little smaller than mine. I think they're the perfect size sweetheart."
        mc.name "I like them too, but that little bit makes all the difference to the InstaPic algorithm."
        mc.name "I've heard that a lot of girls have gone and gotten fake breasts to help get ahead."
        "[the_mom.possessive_title] turns and looks at [the_sister.possessive_title], who nods in agreement."
        $ the_group.draw_person(the_sister, position = "kneeling1")
        the_sister "You're lucky [the_mom.title], I wish my boobs had grown in to be as big as yours."
        the_sister "This would be so much easier, and I could make more money to help you with all of our bills..."
        $ the_group.draw_person(the_mom, position = "kneeling1")
        the_mom "Oh sweetheart, don't think about it like that. Go on [the_mom.mc_title], tell your sister that she's perfect just the way she is!"
        menu:
            "She would be perfect with bigger tits!":
                $ mc.change_locked_clarity(10)
                mc.name "[the_sister.title]'s beautiful, obviously, but I think she would be stunning with bigger boobs."
                mc.name "Bigger is always better, right?"


            "Of course! But if she could earn more money...":
                mc.name "Of course she is, but there are practical things to think about [the_mom.title]."
                $ mc.change_locked_clarity(10)
                mc.name "[the_sister.title] would be just as perfect with slightly bigger boobs."
                mc.name "And the extra money she could earn from InstaPic would be so helpful for the household."

        $ the_group.draw_person(the_sister, position = "kneeling1", emotion = "happy")
        "[the_sister.possessive_title] smiles at you and nods her head."
        the_sister "I think [the_sister.mc_title] is right [the_mom.title]. Maybe I should do it..."

    else:
        mc.name "That's a good start. [the_mom.title], puff out your chest for the camera."
        $ mc.change_locked_clarity(10)
        "[the_mom.possessive_title] rolls her shoulders back, emphasising her large breasts for the camera."
        mc.name "That's great, just like that."
        "You get a few pictures of [the_mom.title] with [the_sister.possessive_title] beside her."
        mc.name "These shots would be even better if [the_sister.title] had tits as big as yours."
        the_mom "[the_mom.mc_title], You know how I feel about her getting implants..."
        mc.name "I just think you need to consider it a bit more. It's what she wants, right [the_sister.title]?"
        $ the_group.draw_person(the_sister, position = "kneeling1", emotion = "happy")
        "[the_sister.possessive_title] nods her head eagerly."
        the_sister "I think it's a good idea [the_mom.title]. Please?"


    $ the_group.draw_person(the_mom, position = "kneeling1")
    the_mom "That's a very big change to make in your life just for your internet work [the_sister.title]."
    the_mom "I don't think I'd be a very good mother if I let you do it."
    "[the_mom.possessive_title] seems hesitant. You'll need some way to convince her."
    $ boobjob_allowed = False
    $ sluttiness_required = 40 - the_mom.get_opinion_score("showing her tits") * 5
    $ sluttiness_token = get_red_heart(sluttiness_required)
    menu:
        "[the_sister.title] would look so hot!" if the_mom.effective_sluttiness() >= sluttiness_required:
            mc.name "Think about how hot [the_sister.title] would be with bigger boobs though."
            mc.name "On her slender frame they're going to look even bigger!"
            $ the_group.draw_person(the_sister, position = "kneeling1")
            $ mc.change_locked_clarity(20)
            the_sister "Please [the_mom.title]? I just want to have big boobs like I've always wanted. Boobs like yours."
            "[the_sister.possessive_title] pouts and flutters her eyes at [the_mom.possessive_title]."
            "She thinks for a long moment, then sighs and nods."
            $ the_group.draw_person(the_mom, position = "kneeling1", emotion = "happy")
            the_mom "I can't say no to you. You can do it."
            $ boobjob_allowed = True

        "[the_sister.title] would look so hot!\nRequires: Mom, [sluttiness_token] (disabled)" if the_mom.effective_sluttiness() < sluttiness_required:
            pass

        "Order [the_sister.title] to do it anyways." if the_sister.obedience >= 140:
            mc.name "I knew she wouldn't go for it. I don't think she likes this job you've found."
            the_mom "I didn't say that! But surgery is a very serious thing to consider!"
            mc.name "Well I think you should do it anyways [the_sister.title]. You're an adult, [the_mom.title] can't stop you."
            $ the_group.draw_person(the_sister, position = "kneeling1")
            "[the_sister.possessive_title] stutters for a moment, clearly unsure of what to say. She looks to you for direction."
            the_sister "I... Are you sure I should [the_sister.mc_title]?"
            mc.name "I am. I'll help you, I promise."
            "[the_sister.title] finds her nerve and turns to face [the_mom.title]."
            the_sister "Okay, then I'm going to do it! I'm sorry [the_mom.title], but it's important to me!"
            $ the_group.draw_person(the_mom, position = "kneeling1")
            the_mom "You're sure about this?"
            "[the_sister.possessive_title] nods. [the_mom.possessive_title] sighs and shrugs."
            the_mom "If I can't change your mind, then I want to make sure you're being safe."
            $ boobjob_allowed = True

        "Order [the_sister.title] to do it anyways.\nRequires: 140 Obedience (disabled)" if the_sister.obedience < 140:
            pass

        "Order [the_mom.title] to allow it." if the_mom.obedience >= 140:
            mc.name "[the_sister.title]'s an adult [the_mom.title], you can't tell her what to do for the rest of her life."
            mc.name "She wants to do this. You need to be a good mother and support her."
            $ the_group.draw_person(the_mom, position = "kneeling1")
            the_mom "[the_sister.title], you're sure about this?"
            "[the_sister.possessive_title] nods. [the_mom.possessive_title] sighs and shrugs."
            the_mom "[the_mom.mc_title] is right, this is your decision to make."
            the_mom "If you want to get implants, I'll support you."
            $ boobjob_allowed = True

        "Order [the_mom.title] to allow it.\nRequires: 140 Obedience (disabled)" if the_mom.obedience < 140:
            pass

        "You got yourself implants already." if the_mom.event_triggers_dict.get("boobjob_count", 0) > 0:
            mc.name "Don't be a hypocrite [the_mom.title]. You were fine with getting implants for yourself."
            mc.name "If you can do it, why can't [the_sister.title]?"
            $ the_group.draw_person(the_mom, position = "kneeling1")
            the_mom "I suppose you have a point... Maybe I'm over reacting a little bit. My little girl is growing up."
            the_mom "As long as you're sure [the_sister.title], you have my permission."
            $ boobjob_allowed = True

        "Try to convince her later.":
            "You can't think of anything to say that would convince [the_mom.title]."
            mc.name "Give it some thought, maybe you'll change your mind."
            "You take a few more pictures of [the_mom.possessive_title] and [the_sister.possessive_title] posing together."



    if boobjob_allowed:
        "[the_sister.title] squeals happily and hugs [the_mom.possessive_title]."
        $ the_group.draw_person(the_sister, position = "kneeling1", emotion = "happy")
        the_sister "Thank you, thank you! They're going to look great, I just know it!"
        $ the_group.draw_person(the_mom, position = "kneeling1")
        the_mom "I hope they do. Do you have a plan for how you're going to pay for this?"
        the_mom "Surgery like that isn't cheap."
        $ the_group.draw_person(the_sister, position = "kneeling1", emotion = "happy")
        the_sister "I have some money saved up, and my InstaPic fans will probably send me some donations."
        the_sister "I don't know if it will be enough, but it's a start!"
        menu:
            "[the_mom.title], you should help." if mom.love >= 40:
                mc.name "[the_mom.title], we must have something saved we could help [the_sister.title] with."
                $ the_group.draw_person(the_mom, position = "kneeling1")
                the_mom "Hmm... I do have some money saved for her tuition next year. I could take a little bit out of that..."
                $ the_group.draw_person(the_sister, position = "kneeling1", emotion = "happy")
                the_sister "That's a great idea! I'll earn it all back and more on InstaPic, I promise!"
                $ the_sister.event_triggers_dict["getting boobjob"] = True #Avoids potential problem where she gets another boobjob from a different source.
                $ got_boobjob_action = Action("Sister got boobjob", sister_got_boobjob_requirement, "sister_got_boobjob_label", args = the_sister, requirement_args = day + renpy.random.randint(3,6))
                $ mc.business.mandatory_crises_list.append(got_boobjob_action)

            "[the_mom.title], you should help\nRequires: Mom, 40 Love (disabled)" if mom.love < 40:
                pass

            "I can help with the rest.":
                mc.name "I can help you with the rest of it [the_sister.title]."
                $ the_sister.change_love(3)
                the_sister "Oh my god, really? That's such a huge help!"
                $ the_group.draw_person(the_mom, position = "kneeling1")
                $ the_mom.change_love(2)
                the_mom "You're lucky to have such a generous brother [the_sister.title]."
                $ the_group.draw_person(the_sister, position = "kneeling1", emotion = "happy")
                the_sister "I know [the_mom.title]. [the_sister.mc_title], talk to me later and we can sort out the details."
                $ the_sister.event_triggers_dict["sister_boobjob_ask_enabled"] = True

        mc.name "Glad to have that sorted out. Now smile for the camera."
        $ the_group.draw_group(position = "kneeling1", emotion = "happy")
        "The two of them smile and pose happily for you."

    else:
        pass

    return

label sister_get_boobjob(the_person):
    mc.name "So, about those implants you wanted to get..."
    $ the_person.draw_person(emotion = "happy")
    the_person "Right! I've got some money saved up, but it's still going to be pretty expensive..."
    mc.name "How much does it cost total?"
    $ the_person.draw_person()
    the_person "... Seven thousand dollars."
    mc.name "Okay. And how much do you have saved?"
    the_person "Three thousand."
    "You sigh."
    mc.name "So I need to pay for over half of this, huh?"
    "She shrugs innocently."
    the_person "I'm putting in all I have!"
    menu:
        "Pay.\n-$4000" if mc.business.has_funds(4000):
            mc.name "Fine, I'll pay for the rest. You have to get everything organised though."
            $ the_person.draw_person(emotion = "happy")
            "[the_person.possessive_title] nods eagerly."
            the_person "I can do that! Thank you [the_person.mc_title]!"
            $ mc.change_locked_clarity(5)
            "She pulls you into a tight hug."
            the_person "I'll let you know when it's done, I guess. I'm so excited!"
            $ mc.business.change_funds(-4000)
            "You send [the_person.title] the money she needs."
            #BUG: If she's getting a second boobjob from some other event this could cause a rare collision. Probably not a problem worth worrying about.
            $ the_person.event_triggers_dict["getting boobjob"] = True #Avoids potential problem where she gets another boobjob from a different source.
            $ got_boobjob_action = Action("Sister got boobjob", sister_got_boobjob_requirement, "sister_got_boobjob_label", args = the_person, requirement_args = day + renpy.random.randint(3,6))
            $ mc.business.mandatory_crises_list.append(got_boobjob_action)
            $ the_person.event_triggers_dict["sister_boobjob_ask_enabled"] = False

        "Pay.\n{color=#FF0000}Requires: $4000{/color} (disabled)" if not mc.business.has_funds(4000):
            pass

        "Talk about it later.":
            mc.name "I'm going to need to pull together some money."
            mc.name "I'll let you know when I've got enough."
            "[the_person.possessive_title] nods."
            the_person "Okay. I hope it doesn't take you too long, I'm so excited!"
    return

label sister_give_boobjob_serum_label(the_person):
    #Should trigger max once/day.
    if the_person.event_triggers_dict.get("sister_boobjob_serum_count",0) == 0:
        mc.name "I've picked up what I needed from the lab."

    elif the_person.event_triggers_dict.get("sister_boobjob_serum_count",0) == 1:
        mc.name "I think it's time for another treatment."
        the_person "And soon I should see some sort of effect, right?"
        mc.name "Definitely. Any day now."

    else: #ie. third dose. She's getting sceptical.
        mc.name "It's time for another treatment."
        the_person "Okay, but it really needs to work this time."
        the_person "If it doesn't work we need to try something else."

    call give_serum(the_person)
    if _return == False:
        mc.name "My mistake, I must have forgotten to pick it up from the lab."

    else:
        "[the_person.possessive_title] takes the vial of serum and drinks it down."
        the_person "I'll let you know if I notice my boobs growing."
        $ the_person.event_triggers_dict["sister_boobjob_serum_count"] += 1
        $ the_person.event_triggers_dict["sister_boobjob_serum_last_day"] = day
    return

label sister_got_boobjob_label(the_person):
    call got_boobjob(the_person) #This does the actual breast increase
    $ sister_brag_action = Action("Sister_brag_boobjob", sister_boobjob_brag_requirement, "sister_new_boobs_brag_label", args = False)
    $ the_person.on_room_enter_event_list.append(sister_brag_action)
    return

label sister_serum_new_boobs_check(the_person, starting_tits):
    if the_person.rank_tits(the_person.tits) - the_person.rank_tits(starting_tits) >= 2:
        $ sister_serum_brag_action = Action("Sister_brag_serum_boobjob", sister_boobjob_brag_requirement, "sister_new_boobs_brag_label", args = True)
        $ the_person.on_room_enter_event_list.append(sister_serum_brag_action)
    else: #Handles all the possible ways the serum checks could fail.
        $ sister_serum_fail_action = Action("Sister_serum_boobjob_fail", sister_serum_boobjob_fail_requirement, "sister_serum_partial_boobjob_label", args = starting_tits)
        $ the_person.on_room_enter_event_list.append(sister_serum_fail_action)
    return

label sister_new_boobs_brag_label(from_serum = False, the_person):
    $ the_person.draw_person(emotion = "happy")
    "[the_person.possessive_title] hurries over to you, smiling from ear to ear."
    the_person "Hey! So..."
    $ mc.change_locked_clarity(10)
    "She puffs out her chest, emphasising her breasts. They're noticeably larger than the last time you saw them."
    the_person "Notice anything different? Maybe something's a little bigger..."
    if from_serum:
        mc.name "Looks like your tits are filling out nicely."
    else:
        mc.name "Finally got your implants, huh?"
    "[the_person.title] nods eagerly."
    the_person "Uh huh! What do you think? Do they look good?"
    menu:
        "You look good.":
            mc.name "You look great with them [the_person.title]. This was a good idea."
            $ the_person.change_happiness(10)
            $ the_person.change_love(1)
            $ the_person.change_slut(1, 40)
            the_person "Thanks! I think they look great too!"

        "You look like a slut.":
            mc.name "They look huge on you. They make you look pretty slutty."
            if the_person.personality is bimbo_personality or the_person.effective_sluttiness() > 40:
                $ the_person.change_happiness(10)
                $ the_person.change_love(1)
                the_person "Thanks! I think they look great too!"
            else:
                if from_serum:
                    the_person "Really? You don't think it was too much, was it?"
                    the_person "Maybe I should have taken less of that drug thing you gave me..."
                else:
                    the_person "Really? You don't think it was too much, was it? I could have gone smaller..."
                mc.name "No, I think it suits you perfectly. It was a good idea."
                $ the_person.change_love(-1)
                $ the_person.change_slut(2, 60)

    the_person "I'm excited to show them off on InstaPic, I think I'm going to earn way more money now!"
    menu:
        "Show them to me." if not the_person.outfit.tits_visible() and mc.location.get_person_count() == 1:
            $ top_item = the_person.outfit.get_upper_top_layer()
            mc.name "Take your [top_item.display_name] off. I think I deserve a good look after all I've done to help you."
            if from_serum:
                the_person "I guess it was your drug thing that made them grow... Alright, just a quick look!"
            else:
                the_person "I guess you have done a lot for me... Alright, just a quick look!"
            if the_person.outfit.can_half_off_to_tits():
                $ strip_list = the_person.outfit.get_half_off_to_tits_list()
                $ generalised_strip_description(the_person, strip_list, half_off_instead = True)
            else:
                $ strip_list = the_person.outfit.get_tit_strip_list()
                $ generalised_strip_description(the_person, strip_list)
            $ mc.change_locked_clarity(20)
            $ the_person.update_outfit_taboos()
            the_person "They're great, right? I'm so happy with them!"
            if from_serum:
                "She jumps up and down in her excitement, jiggling her enlarged tits."
            else:
                "She jumps up and down in her excitement, jiggling her new fake tits."
            the_person "I can't wait to take some pictures for InstaPic, I'm going to make so much more money!"
            the_person "Can you come by and help me out later? I'd really appreciate it."
            mc.name "Sure, I'll stop by if I have the time."
            call talk_person(the_person)

        "Talk to her.":
            mc.name "I hope you do, because those weren't cheap."
            "[the_person.possessive_title] shrugs."
            the_person "They're worth it. Come help me take some pictures later, okay?"
            mc.name "Sure, I'll stop by if I have the time."
            call talk_person(the_person)
    #TODO: She brags to you about the new boobs she just got.
    #TODO: Maybe set up a "brag to Mom" style event, or have it trigger next time you take Instapics together.
    return

label sister_serum_partial_boobjob_label(starting_tits, the_person):
    $ the_person.draw_person()
    the_person "Hey, glad you're here, I wanted to talk to you."
    if the_person.event_triggers_dict.get("sister_boobjob_serum_count", 0) == 0:
        the_person "You said you were going to give me some of your research stuff to grow my boobs."
        the_person "Do you actually have any, or should we try convincing [mom.title] to let me get implants instead?"
        menu:
            "I'll get you some serum.":
                mc.name "Sorry [the_person.title], work at the lab got busy and I haven't had a chance to grab some."
                mc.name "Give me a little more time, I'll get you some."
                the_person "Okay, just don't take too long! I could be earning so much more on InstaPic already!"
                $ sister_boobjob_serum_check_action = Action("sister_serum_boobjob_check", sister_serum_new_boobs_check_requirement, "sister_serum_new_boobs_check", args = [the_person, the_person.tits], requirement_args = [the_person, the_person.tits, day + 10])
                $ mc.business.mandatory_crises_list.append(sister_boobjob_serum_check_action)
                pass

            "Let's convince [mom.title].":
                mc.name "You're right, we should try and convince [mom.title]."
                mc.name "I'll bring it up next time you're taking InstaPic's with her."
                the_person "Okay, I hope you're convincing!"
                $ the_person.event_triggers_dict["sister_boobjob_convince_mom_enabled"] = True

    else: #You gave her some, but they weren't effective.
        if the_person.rank_tits(the_person.tits) == the_person.rank_tits(starting_tits):
            the_person "So it's been a while, and I don't think your boob drug stuff is really working."
            "She gestures down at her chest and shrugs."
            the_person "I guess the only thing left is to get implants. That means we need to convince [mom.title]."
            mc.name "I'll bring it up next time you're taking InstaPic's with her."
            the_person "Okay, I hope you're convincing!"
        elif the_person.rank_tits(the_person.tits) < the_person.rank_tits(starting_tits):
            the_person "So it's been a while, and I really don't think your boob drug stuff is working."
            "She gestures down at her chest and shrugs."
            the_person "I think they've actually gotten smaller!"

        elif the_person.rank_tits(the_person.tits) - the_person.rank_tits(starting_tits) == 1:
            the_person "So it's been a while, and I don't think your boob drug stuff is really working."
            "She gestures down at her chest and shrugs."
            the_person "They're a little bit bigger, I guess, but I imagining a more dramatic change."

        the_person "The only thing left to do is to get implants. That means we need to convince [mom.title]."
        mc.name "I'll bring it up next time you're taking InstaPic's with her."
        the_person "Okay, I hope you're convincing!"
        $ the_person.event_triggers_dict["sister_boobjob_convince_mom_enabled"] = True

    call talk_person(the_person)
    return
