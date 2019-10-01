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
            if the_person.sluttiness > 20 and mc.business.event_triggers_dict.get("sister_serum_test_count") and mc.business.event_triggers_dict.get("sister_serum_test_count") >= 4:
                return True
        return False

    def sister_strip_reintro_requirement(the_person):
        if not mc.business.event_triggers_dict.get("sister_strip_reintro",False):
            return False
        elif mc.location != lily_bedroom:
            return False
        elif len(lily_bedroom.people) > 1:
            return False
        elif the_person.sluttiness < 20:
            return "Requires: " + get_red_heart(20)
        else:
            return True

    def sister_strip_requirement(the_person): #She'll only strip if you're in her bedroom and alone.
        if not mc.business.event_triggers_dict.get("sister_strip",False):
            return False
        elif mc.location != lily_bedroom:
            return False
        elif len(lily_bedroom.people) > 1:
            return False
        elif the_person.sluttiness < 20 or mc.business.funds < 100:
            return "Requires: $100, " + get_red_heart(20)
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
