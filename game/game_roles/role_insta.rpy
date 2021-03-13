# Contains all of the information/events for girls who are on instapic.
# Girls are given this role if they have an account.


init -2 python:
    def insta_on_turn(the_person):
        rand_chance = renpy.random.randint(0,100)
        if rand_chance < 20 + 5*the_person.get_opinion_score("skimpy outfits") + 5*the_person.get_opinion_score("showing her tits") + 5*the_person.get_opinion_score("showing her ass"):
            the_person.event_triggers_dict["insta_generate_pic"] = True # Generates a new post when you view her profile.
        return

    def insta_on_day(the_person):
        #TODO: Chance every day that she will make an DikDok or Onlyfans account.
        return


    def insta_would_ban(the_outfit): #Helper function for Insta related stuff. Returns True if an outfit would get you banned from InstaPic.
        if the_outfit.tits_visible() or the_outfit.vagina_visible():
            return True
        else:
            return False

    def comment_action_requirement(the_person):
        if the_person.event_triggers_dict.get("insta_commented_day",-1) >= day:
            return "Already commented today."
        else:
            return True

    def dm_action_requirement(the_person):
        if the_person.event_triggers_dict.get("insta_special_request_pending", False):
            return "Waiting for her reply."
        return True

    def dm_option_specific_outfit_requirement(the_person):
        return True

    def dm_option_underwear_requirement(the_person):
        return True

    def dm_option_topless_requirement(the_person):
        return True

    def dm_option_nude_requirement(the_person):
        return True

    def dm_response_requirement(the_person):
        if renpy.random.randint(0,100) < 60 and not the_person.event_triggers_dict.get("insta_special_request_asap", False): #Respond at a random time, not as soon as possible.
            return False
        elif person_at_work(the_person) and the_person.obedience >= 110: #Obedient girls don't try and take pics at work.
            return False
        elif mc.location.has_person(the_person) and mc.location.public:
            return False #If she's in the same location as us and we are in public she doesn't take the picture.
        elif the_person.home.has_person(the_person) and mc.location == the_person.home: #Doesn't do it if she's at home and you're in the room with her (mainly for Lily/Mom)
            return False
        return True

    def insta_dm_cleanup(the_person): #Resets all the appropriate flags that should be reset after a response has been given.
        the_person.event_triggers_dict["insta_special_request_pending"] = False
        if the_person.event_triggers_dict.get("insta_special_request_sis", None) is not None:
            the_person.event_triggers_dict["insta_special_request_sis"] = None
        return

label check_insta():
    # TODO: Check if anyone you know has posted pictures on InstaPic
    # TODO: Ability to find new Insta girls who are posting revealing pics.
    $ insta_list = ["Accounts You Know"]
    python:
        for a_person in mc.phone.get_person_list():
            if a_person.has_role(instapic_role) and a_person.event_triggers_dict.get("insta_known", False): #We may add a flag to have some girls (ie. Lily) hide their profile under a different name.
                insta_list.append(a_person) #TODO: Have a flag that notes girls who have a new picture. (Flag is set at the beginning of each day in the on_day action)

    $ other_options_list = ["Other Options", "Back"]
    call screen main_choice_display([insta_list, other_options_list], draw_hearts_for_people = False)
    $ picked_option = _return
    if isinstance(picked_option, Person):
        call view_insta(picked_option) from _call_view_insta
    elif picked_option == "Back":
        return
    return

label view_insta(the_person):
    # TODO: If she has a dikdok or onlyfan she may plug that along with a slutty pic.
    # TODO: Add support for girls doing colab posts or bringing their friends in. ie. Mom and Lily should appear in some shoots together.
    $ posted_today = False
    if the_person.event_triggers_dict.get("insta_generate_pic", False):
        "It looks like [the_person.title] has posted a new picture today, along with a comment overlaid at the bottom."
        $ posted_today = True
        if the_person.event_triggers_dict.get("insta_special_request_outfit", None) is not None:
            $ the_person.apply_outfit(the_person.event_triggers_dict.get("insta_special_request_outfit"))
            $ rand_num = renpy.random.randint(0,3)
            if rand_num == 0:
                $ the_person.draw_person(the_animation = None)
            elif rand_num == 1:
                $ the_person.draw_person(position = "kneeling1", the_animation = None)
            elif rand_num == 2:
                $ the_person.draw_person(position = "back_peek", the_animation = None)
            the_person "Wearing something special today: a design sent in by a fan!" (what_style = "text_message_style")


        elif the_person.effective_sluttiness() + the_person.get_opinion_score("showing her ass")*5 + the_person.get_opinion_score("showing her tits")*5 > 20: #TODO: Decide what slut_requirement should be.
            $ skimpy_outfit = insta_wardrobe.pick_random_outfit()
            $ the_person.apply_outfit(skimpy_outfit)
            $ rand_num = renpy.random.randint(0,3)
            if rand_num == 0:
                $ the_person.draw_person(position = "stand3", the_animation = None)
                the_person "Thought this outfit looked sexy. What do you think?" (what_style = "text_message_style")
            elif rand_num == 1:
                $ the_person.draw_person(position = "kneeling1", the_animation = None)
                the_person "Hey everyone, what do you think of this pose? I think it makes my tits look great!" (what_style = "text_message_style")
            elif rand_num == 2:
                $ the_person.draw_person(position = "back_peek", the_animation = None)
                the_person "Ass was looking great, just had to take a pic!" (what_style = "text_message_style")
            elif rand_num == 3:
                $ the_person.draw_person(position = "kneeling1", the_animation = None)
                the_person "Do I look good down on my knees?" (what_style = "text_message_style")

            if the_person.has_role(dikdok_role) and the_person.event_triggers_dict.get("dikdok_generate_video", False):
                the_person "If you liked that, come see me getting into trouble on DikDok! Hurry, I might get banned soon!" (what_style = "text_message_style")
                $ the_person.event_triggers_dict["dikdok_known"] = True

            elif the_person.has_role(onlyfans_role) and the_person.event_triggers_dict.get("instafans_generate_content", False):
                the_person "If you like that, subscribe to my OnlyFanatics and see so, sooo much more!" (what_style = "text_message_style")
                $ the_person.event_triggers_dict["onlyfans_known"] = True

            $ the_person.apply_outfit() # Reset them to their normal daily wear.
        elif the_person.is_wearing_uniform() and not (the_person.outfit.vagina_visible() or the_person.outfit.tits_visible()):
            $ rand_num = renpy.random.randint(0,1)
            if rand_num == 0:
                $ the_person.draw_person(the_animation = None)
                the_person "Getting dressed for work. I make this uniform work!" (what_style = "text_message_style")

            elif rand_num == 1:
                $ the_person.draw_person(position = "back_peek", the_animation = None)
                the_person "I think my boss makes me wear this just because it makes my butt look good. At least he's right!" (what_style = "text_message_style")

        else:
            $ rand_num = renpy.random.randint(0,1)
            if rand_num == 0:
                $ the_person.draw_person(the_animation = None)
                the_person "Good morning everyone!"

            elif rand_num == 1:
                $ the_person.draw_person(position = "back_peek", the_animation = None)
                the_person "About to head out the door. I've got a full day ahead of me!"



    else:
        #TODO: Include a chance for something flavourful like "It's just pictures of food. Pages and pages of food!"
        "You scan [the_person.title]'s profile. Nothing new today."

    call instapic_comment_loop(the_person, posted_today) from _call_instapic_comment_loop
    $ clear_scene()
    $ the_person.event_triggers_dict["insta_generate_pic"] = False
    return

label instapic_comment_loop(the_person, posted_today = False):
    $ display_list = []

    if posted_today:
        $ nice_comment_action = Action("Leave a nice comment.", comment_action_requirement, "comment_description", requirement_args = the_person, args = ["nice"])
        $ mean_comment_action = Action("Leave a mean comment.", comment_action_requirement, "comment_description", requirement_args = the_person, args = ["mean"])
        $ sexy_comment_action = Action("Leave a sexual comment.", comment_action_requirement, "comment_description", requirement_args = the_person, args = ["sexy"])

        $ comment_list = ["Comment", nice_comment_action, mean_comment_action, sexy_comment_action]
        $ display_list.append(comment_list)

    $ dm_request_action = Action("Ask for something special.", dm_action_requirement, "dm_description", requirement_args = the_person)
    $ dm_list = ["Direct message her", dm_request_action]
    $ display_list.append(dm_list)

    $ other_list = ["Other Options"]
    $ other_list.append("Back")
    $ display_list.append(other_list)

    call screen main_choice_display(display_list)
    $ the_choice = _return
    if isinstance(the_choice, Action):
        $ the_choice.call_action(the_person)

    return

label comment_description(type, the_person):
    $ the_person.event_triggers_dict["insta_commented_day"] = day
    if type == "nice":
        mc.name "Looking good!" (what_style = "text_message_style")
        $ the_person.change_happiness(2, add_to_log = False)
    elif type == "mean":
        mc.name "You should wear something else. That outfit looks terrible!" (what_style = "text_message_style")
        $ the_person.change_happiness(-2, add_to_log = False)
    elif type == "sexy":
        mc.name "Stunning! Wish I could see you naked!" (what_style = "text_message_style")
        $ her_slut = the_person.effective_sluttiness() + 5*(the_person.get_opinion_score("showing her tits") + the_person.get_opinion_score("showing her ass"))
        if her_slut < 20: #Dislikes it
            $ the_person.change_happiness(-5 + the_person.get_opinion_score("showing her tits") + the_person.get_opinion_score("showing her ass"), add_to_log = False)
        elif her_slut < 40: #Doesn't mind, is made slightly sluttier by it
            $ the_person.change_happiness(-2 + the_person.get_opinion_score("showing her tits") + the_person.get_opinion_score("showing her ass"), add_to_log = False)
            $ the_person.change_slut_temp(1 + the_person.get_opinion_score("showing her tits") + the_person.get_opinion_score("showing her ass"), add_to_log = False)
        else: #Likes it, gets sluttier if her opinions line up with that
            $ the_person.change_happiness(5 + the_person.get_opinion_score("showing her tits") + the_person.get_opinion_score("showing her ass"), add_to_log = False)
            $ the_person.change_slut_temp(0 + the_person.get_opinion_score("showing her tits") + the_person.get_opinion_score("showing her ass"), add_to_log = False)
    call instapic_comment_loop(the_person, posted_today = False) from _call_instapic_comment_loop_1
    return

label dm_description(the_person):
    $ dm_option_specific_outfit_action = Action("Wear a specific outfit. -$20", dm_option_specific_outfit_requirement, "dm_option_specific_outfit", requirement_args = the_person)
    $ dm_option_underwear_action = Action("Show me your underwear. -$50", dm_option_underwear_requirement, "dm_option_underwear", requirement_args = the_person)
    $ dm_option_topless_action = Action("Show me your tits. -$100", dm_option_topless_requirement, "dm_option_topless", requirement_args = the_person)
    $ dm_option_nude_action = Action("Send me some nudes. -$200", dm_option_nude_requirement, "dm_option_nude", requirement_args = the_person)
    $ dm_options = ["Make a request", dm_option_specific_outfit_action, dm_option_underwear_action, dm_option_topless_action, dm_option_nude_action]

    $ other_list = ["Other Options"]
    $ other_list.append("Back")
    call screen main_choice_display([dm_options], [other_list])
    $ the_choice = _return
    if isinstance(the_choice, Action):
        $ the_choice.call_action(the_person)
        if _return:
            $ the_person.event_triggers_dict["insta_special_request_pending"] = True
            "You hit send. You'll have to wait for her to get back to you with a response."
        else:
            "You hesitate before hitting send, then decide against messaging her at all and delete it."

    return

label dm_option_specific_outfit(the_person):
    $ previous_request_level = the_person.event_triggers_dict.get("insta_special_request_level")
    if previous_request_level == 0:
        mc.name "I found your profile and thought that you look amazing! I was wondering if you took special requests." (what_style = "text_message_style")
        mc.name "I think you would look amazing wearing this outfit, and I'd pay you $20 if you made an InstaPic for it." (what_style = "text_message_style")

    else:# previous_request_level > 0:
        mc.name "I think you would look amazing in this outfit, you should wear it for your next InstaPic post." (what_style = "text_message_style")
        mc.name "If you do I'll send you $20, and I'm sure it'll be great for your brand!" (what_style = "text_message_style")

        call outfit_master_manager(show_overwear = False, show_underwear = False) from _call_outfit_master_manager_11
        $ the_outfit = _return
        if the_outfit is None:
            return False
        else:
            "You put together a list of links to stores she could buy everything from."
            $ response_action = Action("DM outfit response", dm_response_requirement, "dm_option_specific_outfit_response", args = [the_person,the_outfit], requirement_args = the_person)
            $ mc.business.mandatory_crises_list.append(response_action)
            return True

label dm_option_specific_outfit_response(the_person, the_outfit):
    "Your phone buzzes: it's a response from [the_person.title] on InstaPic."
    $ the_choice = False
    if the_person.effective_sluttiness() < 10:
        the_person "I don't take requests, I'm just doing this for fun. Sorry!" (what_style = "text_message_style")
    elif insta_would_ban(the_outfit):
        the_person "Thanks for the interest, but I couldn't wear that without getting banned!" (what_style = "text_message_style")
        if the_person.has_role(onlyfans_role):
            the_person "If you're interested in that sort of content you should check out my OnlyFanatics!" (what_style = "text_message_style")
            "She gives you her OnlyFanatics name."
    elif the_person.judge_outfit(the_outfit, temp_sluttiness_boost = -20) and the_outfit.slut_requirement < 40:
        the_person "It's nice, but I don't think it's the sort of thing my audience is interested in seeing." (what_style = "text_message_style")
        the_person "Thanks for the interest though!" (what_style = "text_message_style")
    elif the_person.judge_outfit(the_outfit):
        the_person "Thanks for the interest, that outfit is so cute! I could see myself wearing it every day!" (what_style = "text_message_style")
        the_person "Send me the money and check my Insta page in a day or two!" (what_style = "text_message_style")
        $ the_choice = True
    elif the_person.judge_outfit(the_outfit, temp_sluttiness_boost = 20):
        the_person "Thanks for the interest! That's not the kind of thing I would normally wear in one of my posts, but I'm willing to give it a try!" (what_style = "text_message_style")
        the_person "Send me the money and check my Insta page in a day or two! If the reactions are good maybe I'll wear more stuff like that!" (what_style = "text_message_style")
        $ the_choice = True

    if the_choice:
        $ the_person.event_triggers_dict["insta_special_request_outfit"] = the_outfit
        if the_person.event_triggers_dict.get("insta_special_request_level",0) < 1:
            $ the_person.event_triggers_dict["insta_special_request_level"] = 1
        $ mc.business.funds += -20
        "You wire her the cash you promised."

    $ insta_dm_cleanup(the_person)
    return

label dm_option_underwear(the_person):
    $ previous_request_level = the_person.event_triggers_dict.get("insta_special_request_level")
    if previous_request_level == 0:
        mc.name "I just found your profile, you look so amazing! I wish you could show more, but I know InstaPic would ban you if you did." (what_style = "text_message_style")
        mc.name "Do you take private pictures? I'd be glad to pay just for some shots of you in your underwear. How does $50 sound?" (what_style = "text_message_style")

    elif previous_request_level == 1:
        mc.name "You looked so good in that last outfit, I wish you could show more without InstaPic banning you." (what_style = "text_message_style")
        mc.name "How about some private pictures, just for me? I'll pay $50 for some shots of you in your underwear." (what_style = "text_message_style")

    else:# previous_request_level == 2:
        mc.name "Interested in making another fifty bucks? I'd like some more shots of you in your underwear." (what_style = "text_message_style")

    $ response_action = Action("DM underwear response", dm_response_requirement, "dm_option_underwear_response", args = the_person, requirement_args = the_person)
    $ mc.business.mandatory_crises_list.append(response_action)

    if the_person.has_role(sister_role):
        $ the_person.event_triggers_dict["insta_special_request_sis"] = "underwear"
    return True

label dm_option_underwear_response(the_person):
    "Your phone buzzes: it's a response from [the_person.title] on InstaPic."
    $ previous_request_level = the_person.event_triggers_dict.get("insta_special_request_level")
    $ the_choice = False

    if the_person.effective_sluttiness() < 10:
        the_person "I don't do private shoots, and definitely nothing like that!" (what_style = "text_message_style")
    elif the_person.effective_sluttiness() < 20:
        the_person "Thanks for the interest, but I don't do underwear shoots (yet!)" (what_style = "text_message_style")
    elif the_person.effective_sluttiness() < 40: #Moderately slutty, she'll do it
        $ the_choice = True
        if previous_request_level < 2: #First time
            the_person "This was a little out of my comfort zone, but I couldn't say no to a fan!" (what_style = "text_message_style")
        else: #Has done it before, or already done worse
            the_person "It's always nice to hear from you. I hope this shot is what you were thinking of!" (what_style = "text_message_style")

        $ the_person.apply_outfit(insta_wardrobe.pick_random_outfit()) #She starts from an Insta-specific design.
        $ strip_list = the_person.outfit.get_underwear_strip_list()
        $ the_person.outfit.strip_to_underwear(avoid_nudity = True)
        $ the_person.draw_person(the_animation = None)
        $ the_person.apply_outfit() #Redress
        "There's a short pause, then she sends an image."
        the_person "Enjoy, and remember to leave a nice comment on my profile!" (what_style = "text_message_style")

    else:
        $ the_choice = True
        the_person "I had a lot of fun taking these. Always happy to do something special for a fan!" (what_style = "text_message_style")

        $ the_person.apply_outfit(insta_wardrobe.pick_random_outfit()) #She starts from an Insta-specific design.
        $ the_person.outfit.strip_to_underwear()
        $ the_person.draw_person(the_animation = None)
        "There's a short pause, then she sends an image."
        $ the_person.draw_person(postiion = "back_peek", the_animation = None)
        "...Then another."
        $ the_person.draw_person(position = "kneeling1", the_animation = None)
        "...And another."
        if the_person.get_opinion_score("showing her tits") > 0 and not the_person.outfit.tits_visible():
            $ strip_list = the_person.outfit.strip_to_tits()
            if the_person.outfit.can_half_off_to_tits():
                $ strip_list = the_person.outfit.get_half_off_to_tits_list()
                $ the_person.outfit.remove_clothing_list(strip_list, half_off_instead = True)
            else:
                $ the_person.outfit.remove_clothing_list(strip_list)
            $ the_person.draw_person(position = "blowjob", the_animation = None)
            "...And one more. This time, with her tits out!"
            the_person "I got a little carried away, I'm sure you don't mind!" (what_style = "text_message_style")
            the_person "Have fun with those, and let me know if there's anything else I can do for you!" (what_style = "text_message_style")
        else:
            the_person "Enjoy, and get in touch if you have any other special requests I can help out with." (what_style = "text_message_style")
        $ the_person.apply_outfit() #Get redressed

    if the_choice:
        the_person "Oh, and if you liked that, check out my OnlyFanatics page. I'm sure you'll love it!" (what_style = "text_message_style")
        "She sends you a link."
        $ the_person.event_triggers_dict["onlyfans_known"] = True

        $ mc.business.funds += -50
        if the_person.event_triggers_dict.get("insta_special_request_level",0) < 2:
            $ the_person.event_triggers_dict["insta_special_request_level"] = 2
        "You wire her the cash you promised."

    $ insta_dm_cleanup(the_person)
    $ clear_scene()
    return


label dm_option_topless(the_person):
    $ previous_request_level = the_person.event_triggers_dict.get("insta_special_request_level")
    if previous_request_level == 0:
        mc.name "I just found your profile and it blew me away! You're gorgeous!" (what_style = "text_message_style")
        mc.name "Do you do topless shots? Your tits are driving me crazy, I'd pay to see them!" (what_style = "text_message_style")
        mc.name "How about $100? Would that be enough for some private pics?" (what_style = "text_message_style")
    elif previous_request_level == 1:
        mc.name "You looked so good in that last outfit, I wish you could show more without InstaPic banning you." (what_style = "text_message_style")
        mc.name "Would you consider taking some topless shots? Your tits are driving me crazy, I'd pay to see them!" (what_style = "text_message_style")
        mc.name "How about $100? Would that be enough for some private pics?" (what_style = "text_message_style")
    elif previous_request_level == 2:
        mc.name "Those last shots were so hot, I loved them!" (what_style = "text_message_style")
        mc.name "How about some topless shots? I'd pay more, of course." (what_style = "text_message_style")
    else:
        mc.name "I want some pictures of your tits, would $100 be enough?" (what_style = "text_message_style")
    $ response_action = Action("DM topless response", dm_response_requirement, "dm_option_topless_response", args = the_person, requirement_args = the_person)
    $ mc.business.mandatory_crises_list.append(response_action)

    if the_person.has_role(sister_role):
        $ the_person.event_triggers_dict["insta_special_request_sis"] = "topless"
    return True

label dm_option_topless_response(the_person):
    $ previous_request_level = the_person.event_triggers_dict.get("insta_special_request_level")
    $ the_choice = False
    "Your phone buzzes: it's a response from [the_person.title] on InstaPic."
    if the_person.effective_sluttiness() < 20:
        the_person "I don't do private shoots, and definitely nothing like that!" (what_style = "text_message_style")
    elif the_person.effective_sluttiness() < 30:
        the_person "Sorry, but I don't do any nude shots. I hope you still like the rest of my content though!" (what_style = "text_message_style")
    elif the_person.effective_sluttiness() < 50: #Does it, with a little bit of reservation
        $ the_choice = True
        if previous_request_level < 3: #First time
            the_person "I've never really done something like this, but I suppose I can give it a try!" (what_style = "text_message_style")
        else:
            the_person "I'm always happy to make a fan happy, so here are soem shots I took just for you!" (what_style = "text_message_style")


        $ the_person.apply_outfit(insta_wardrobe.pick_random_outfit()) #She starts from an Insta-specific design.
        $ strip_list = the_person.outfit.get_tit_strip_list()
        if the_person.outfit.can_half_off_to_tits():
            $ strip_list = the_person.outfit.get_half_off_to_tits_list()
            $ the_person.outfit.remove_clothing_list(strip_list, half_off_instead)
        else:
            $ the_person.outfit.remove_clothing_list(strip_list)
        $ the_person.draw_person(the_animation = None)
        $ the_person.apply_outfit()
        "There's a short pause, then she sends an image."
        the_person "Hope that's everything you hoped it would be! Leave a nice comment on my profile, it helps!" (what_style = "text_message_style")

    else: #Does it happily
        $ the_choice = True
        the_person "Of course I can get you some shots of my tits! I love doing this for special fans like you!" (what_style = "text_message_style")
        $ the_person.apply_outfit() #She starts from her normal outfit (assigned as normal)
        "There's a short pause, then she sends an image."
        $ the_person.draw_person(the_animation = None)
        if the_person.should_wear_uniform():
            the_person "Here's what my boss makes me wear..." (what_style = "text_message_style")
        else:
            the_person "Here's what everyone else sees..." (what_style = "text_message_style")
        $ strip_list = the_person.outfit.get_tit_strip_list()
        if the_person.outfit.can_half_off_to_tits():
            $ strip_list = the_person.outfit.get_half_off_to_tits_list()
            $ the_person.outfit.remove_clothing_list(strip_list, half_off_instead)
        else:
            $ the_person.outfit.remove_clothing_list(strip_list)
            $ the_person.draw_person(the_animation = None)
        "Another pause, then another picture."
        the_person "And here's what you get to see!" (what_style = "text_message_style")

        $ the_person.outfit.restore_all_clothing()
        $ the_person.outfit.strip_to_underwear()
        $ the_person.outfit.strip_to_tits() #Gets her into her underwear, then strips her bra off on top of that.
        $ the_person.draw_person(position = "kneeling1", the_animation = None)
        "Pause, then image."
        the_person "Do you think anyone IRL would guess that I'm a little slut for men on the internet?" (what_style = "text_message_style")
        $ the_person.draw_person(position = "missionary", the_animation = None)
        "One last picture, this time of her lying down."
        the_person "Just let me know if you want to see more, I love doing these special requests!" (what_style = "text_message_style")
        $ the_person.apply_outfit()

    if the_choice:
        if the_person.has_role(onlyfans_role) and not the_person.event_triggers_dict.get("onlyfans_known", False):
            the_person "Oh, and if you liked that, check out my OnlyFanatics page. I'm sure you'll love it!" (what_style = "text_message_style")
            "She sends you a link."
            $ the_person.event_triggers_dict["onlyfans_known"] = True


        $ mc.business.funds += -100
        if the_person.event_triggers_dict.get("insta_special_request_level",0) < 3:
            $ the_person.event_triggers_dict["insta_special_request_level"] = 3
        "You wire her the cash you promised."




    $ insta_dm_cleanup(the_person)
    $ clear_scene()
    return

label dm_option_nude(the_person):
    $ previous_request_level = the_person.event_triggers_dict.get("insta_special_request_level")
    if previous_request_level == 0:
        mc.name "I just found your profile and it blew me away! You're gorgeous!" (what_style = "text_message_style")
        mc.name "Do you do nude shots? I'd pay so much to see you naked!" (what_style = "text_message_style")
        mc.name "How $200? Would that be enough for some private pics?" (what_style = "text_message_style")
    elif previous_request_level == 1:
        mc.name "Your posts are so hot, but I really think you'd look better naked." (what_style = "text_message_style")
        mc.name "Do you do nude shots? I'd pay so much to see you naked!" (what_style = "text_message_style")
        mc.name "How $200? Would that be enough for some private pics?" (what_style = "text_message_style")
    elif previous_request_level == 2 or previous_request_level == 3:
        mc.name "Fuck, you're so beautiful I just need to see more of you!" (what_style = "text_message_style")
        mc.name "I want some nudes, could you send them to me? I'll pay you $200 for them." (what_style = "text_message_style")
    else:
        mc.name "I'm looking for some more nudes, interested? I'll pay another $200 for them." (what_style = "text_message_style")
    $ response_action = Action("DM topless response", dm_response_requirement, "dm_option_nude_response", args = the_person, requirement_args = the_person)
    $ mc.business.mandatory_crises_list.append(response_action)

    if the_person.has_role(sister_role):
        $ the_person.event_triggers_dict["insta_special_request_sis"] = "nude"
    return True

label dm_option_nude_response(the_person):
    $ previous_request_level = the_person.event_triggers_dict.get("insta_special_request_level")
    if the_person.effective_sluttiness() < 20:
        the_person "I would never do that, for any amount of money!" (what_style = "text_message_style")
    #TODO: If she has an Onlyfans it can be plugged here instead of giving you anything.
    elif the_person.effective_sluttiness() < 40:
        the_person "Sorry, but I don't show full nudes for any price." (what_style = "text_message_style")
        the_person "I hope you still like the rest of my content though!" (what_style = "text_message_style")
    elif the_person.effective_sluttiness() < 60: #Willing, not excited.
        $ the_choice = True
        if previous_request_level < 4: #First time
            the_person "I wouldn't normally do something like this, but I suppose I can give it a try. Be nice!" (what_style = "text_message_style")

        else: #You've done this before
            the_person "It's always nice to hear from you, of course I can take some pics for you!" (what_style = "text_message_style")

        $ the_person.apply_outfit(insta_wardrobe.pick_random_outfit()) #She starts from an Insta-specific design.
        $ strip_list = the_person.outfit.get_full_strip_list()
        $ the_person.outfit.remove_clothing_list(strip_list)

        "There's a short pause, then she sends an image."
        $ the_person.draw_person(the_animation = None)
        the_person "From the front..." (what_style = "text_message_style")
        "Another pause, then another image."
        $ the_person.draw_person(position = "back_peek", the_animation = None)
        the_person "... and from the back!" (what_style = "text_message_style")
        the_person "Enjoy, and message me any time you have a special request." (what_style = "text_message_style")
        $ the_person.draw_person(the_animation = None)
        $ the_person.apply_outfit()

    else: #Willing and excited
        $ the_choice = True
        the_person "I love getting requests like this! Of course I can take some shots for you!" (what_style = "text_message_style")
        $ the_person.apply_outfit() #Starts in her normal outfit.
        "There's a short pause, then she sends an image."
        $ the_person.draw_person(the_animation = None)
        if the_person.should_wear_uniform():
            the_person "Here's what my boss makes me wear..." (what_style = "text_message_style")
        else:
            the_person "Here's what I should be wearing..." (what_style = "text_message_style")
        $ strip_list = the_person.outfit.get_full_strip_list()
        $ the_person.outfit.remove_clothing_list(strip_list)
        "Another pause, then another image."
        $ the_person.draw_person(the_animation = None)
        the_person "And here's what I'm wearing now, because of you!" (what_style = "text_message_style")
        "Another picture, this one from behind."
        $ the_person.draw_person(position = "back_peek", the_animation = None)
        the_person "How does my butt look? Here, let's get you a better view..."
        "Pause. Picture."
        $ the_person.draw_person(position = "doggy", the_animation = None)
        $ the_person.apply_outfit()
        the_person "I hope you have fun with those, I had fun taking them!"

    if the_choice:
        the_person "Oh, and if you liked that, check out my OnlyFanatics page. I'm sure you'll love it!" (what_style = "text_message_style")
        "She sends you a link."
        $ the_person.event_triggers_dict["onlyfans_known"] = True

        $ mc.business.funds += -200
        if the_person.event_triggers_dict.get("insta_special_request_level",0) < 4:
            $ the_person.event_triggers_dict["insta_special_request_level"] = 4
        "You wire her the cash you promised."

    $ insta_dm_cleanup(the_person)
    $ clear_scene()
    return

#TODO: Implement this at some point. For now it's more complexity than we need.
label insta_interupt_check(the_person): # Returns Something???  a callback label or None. The callback should be called after the event.
    if the_person.has_role(sister_role):
        if mc.location.has_person(the_person) and mc.location == the_person.home:
            $ the_person.draw_person()
            "[the_person.title] pulls out her phone, then looks at you."
            the_person "Hey [the_person.mc_title], I got another one of those requests on InstaPic."
            the_person "You know, to see my boobs."
            pass #We're in Lily's room.
        elif the_person.home.has_person(the_person) and mc_at_home():
            pass #We're somewhere in the house, probably our room.
    elif mc.location.has_person(the_person):
        if the_person.has_role(employee_role) and is_at_work(the_person):
            "You notice [the_person.title] look at her phone, then glances around the room as if checking to see if she's being watched."
            "She stands up and heads for the bathroom. You wonder briefly why she's being so secretive."
        else:
            "You notice [the_person.title] look at her phone, then glance up at you."
            $ the_person.draw_person()
            the_person "Back in a moment, just need to take care of this..."
            $ clear_scene()
            "She hurries away, leaving you to wonder what, exactly, she needs to take care of."

    #TODO: Check if the_person is in the same location as you, or if she would come find you (Lily specfically).
    #TODO: If at work you notice her slipping away,
    return
