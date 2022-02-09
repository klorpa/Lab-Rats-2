## Holds all of the information required for the city rep who visits your company when Attention gets too high.

#TODO: write our requiprements. Remember to check if "currently_interogating" is True if it's explicitly for a bribe, if not we've met her somewhere else!
init -1 python:
    def city_rep_negotiate_requirement(the_person):
        if attention_floor_increase_2_policy.is_owned():
            return False
        elif not the_person.event_triggers_dict.get("currently_interogating", False):
            return False
        return True

    def city_rep_bribe_requirement(the_person):
        if not the_person.event_triggers_dict.get("currently_interogating", False):
            return False
        elif "cash_bribe" in the_person.event_triggers_dict.get("bribe_attempts", []):
            return False
        return True

    def city_rep_seduce_requirement(the_person):
        if not the_person.event_triggers_dict.get("currently_interogating", False):
            return False
        elif "seduction_attempted" in the_person.event_triggers_dict.get("bribe_attempts", []):
            return False
        return True

    def city_rep_order_requirement(the_person):
        if not the_person.event_triggers_dict.get("currently_interogating", False):
            return False
        elif "order_attempted" in the_person.event_triggers_dict.get("bribe_attempts", []):
            return False
        return True


label city_rep_negotiate(the_person):
    mc.name "This is a waste of everyone's time. I'm sure you have better things to be doing today."
    the_person "I go where the city sends me. That's all."
    mc.name "Couldn't we come to some sort of agreement so this isn't necessary? What does the city need to stay out of my hair."
    $ obedience_requirement = 130 - 10*the_person.get_opinion_score("being submissive")
    if the_person.love < 0:
        the_person "They need you to stop peddling unregulated, unethical pharmaceuticals. Do you think you can do that for me?"
        mc.name "That's my whole business..."
        the_person "Then I suppose we'll be seeing a lot of each other."
    elif the_person.love < 25:
        the_person "It would help if you stopped selling unregulated pharmaceuticals, but I don't think you can really do that."
        the_person "If you could get a restricted goods business license there would be far fewer questions, but those are particularly hard to obtain."
        mc.name "How would I get one?"
        the_person "You? Oh, you don't. You would need someone to vouch for the importance of this business. Someone like me."
        the_person "And frankly, I don't think you deserve one. You're a nice enough man [the_person.mc_title], but I take my work very seriously."
        mc.name "So if I change your mind you could get me one of those licenses?"
        "She shrugs non-committally."
    else:
        the_person "Assuming you want to stay in business? What you really need is a restricted goods business license."
        mc.name "And how would I get one of those?"
        the_person "Well... The first step would be having someone vouch for the importance of this business to the welfare of the city."
        the_person "Someone like me."
        mc.name "Would you do that for me?"
        "She thinks for a moment."
        the_person "It would be a big risk for me. This isn't the most savoury business, and if one of my higher-ups reviews my work there could be trouble."
        menu:
            "Pay her. -$2500" if mc.business.has_funds(2500):
                mc.name "I can pay you for it. I'm sure there are application fees, extra taxes, and so on..."
                the_person "[the_person.mc_title], are you trying to bribe me?"
                mc.name "Of course not! But if you're taking a risk, you deserve to be compensated. Consider it insurance in case something does go wrong."
                "A longer pause this time."
                the_person "Okay, I'll arrange for the paperwork to be put through."
                mc.name "And I'll be sending you your funds. thank you for your help [the_person.title]."
                the_person "Don't make me regret this."
                $ mc.business.change_funds(-2500)
                $ attention_floor_increase_2_policy.buy_policy(ignore_cost = True)

            "Pay her. -$1000 (disabled)" if not mc.business.has_funds(-1000):
                pass

            "Order her." if the_person.obedience >= obedience_requirement:
                mc.name "That's a risk you're going to have to take. Get me that license."
                $ the_person.change_love(-5 + 2*the_person.get_opinion_score("being submissive"))
                $ attention_floor_increase_2_policy.buy_policy(ignore_cost = True)
                "[the_person.title] seems unhappy with being ordered around, but she nods obediently anyways."
                the_person "Fine, I'll sort out the paperwork for you."

            "Order her.\nRequires: [obedience_requirement] Obedience" if the_person.obedience < obedience_requirement:
                pass

            "Never mind.":
                mc.name "I wouldn't want you to put your career in danger. I'm sure I can figure something else out."
                the_person "You've proven to be quite ingenious to date, so I don't doubt it."
    return

label city_rep_bribe(the_person):
    $ the_person.event_triggers_dict["bribe_attempts"] = the_person.event_triggers_dict.get("bribe_attempts",[]).append("cash_bribe")
    mc.name "This is a waste of everyone's time. Isn't there some sort of fee I can pay you and we can all get back to doing real work?"
    if the_person.love < 0:
        the_person "I hope you aren't trying to bribe me [the_person.mc_title]."
        mc.name "Of course not, I was just trying to move this along a little more quickly."
        the_person "Unfortunately I do not believe that will be possible. You should get comfortable with the wait."
    else:
        the_person "That sounds an awful lot like you're trying to offer me a bribe [the_person.mc_title]."
        mc.name "Of course it's not a bribe, but I understand there's a cost to all of this administrative work you are doing."
        mc.name "So if you could just tell me what that cost is I could pay it, right now."
        $ bribe_cost = 1000
        if the_person.obedience < 80:
            $ bribe_cost = 2000

        elif the_person.obedience < 120:
            pass

        else:
            $ bribe_cost = 500

        "She considers this for a moment."
        the_person "That sounds quite reasonable. For a simple fee of, oh... $[bribe_cost] I think we can avoid any further punishments."
        menu:
            "Pay the bribe. -$[bribe_cost]" if mc.business.has_funds(bribe_cost):
                mc.name "That seems like a reasonable cost of doing business. I can send the money over right away."
                "She seems a little surprised that you've taken her up on her offer."
                the_person "Excellent. When my men come back I'll let them know that we've already settled your fine and that we're done here."
                $ the_person.change_obedience(2)
                $ mc.business.change_funds(-bribe_cost)
                $ the_person.event_triggers_dict["bribe_successful"] = "cash"


            "Pay the bribe. -$[bribe_cost] (disabled)" if not mc.business.has_funds(bribe_cost):
                pass

            "Refuse to pay.":
                mc.name "Well, maybe we should just wait until your thugs are back."
                the_person "They're perfectly respectable governmental employees, thank you very much."
    return

label city_rep_seduce(the_person): #TODO: Figure out if we can have something like this trigger automatically if you seduce her by groping her or something
    $ the_person.event_triggers_dict["bribe_attempts"] = the_person.event_triggers_dict.get("bribe_attempts",[]).append("seduction_attempted")
    mc.name "It seems like we have some time to spare [the_person.title]."
    "You step close to her and put your hand on the small of her back."
    mc.name "How about we head to my office and get to know each other better while your thugs are searching the place."
    call apply_sex_slut_modifier(the_person)
    $ should_fuck = False
    if the_person.effective_sluttiness() < 20: #Offended
        $ the_person.change_love(-1)
        "She slaps your hand away and glares at you."
        the_person "Please, let's keep this professional."
        "You hold your hands up innocently and wait a few minutes for her to cool off."
    elif the_person.effective_sluttiness() < 40: #Tempted, but not convinced
        "She tenses under your touch, but doesn't pull away."
        the_person "Tempting, but I don't think that would be a wise idea. It's important that I appear impartial."
        the_person "If anyone suspects we are involved with each other there might be serious repercussions."
        menu: #TODO: Think of some other ways to convince her. Opinion based?
            "Order her." if the_person.obedience >= 120:
                mc.name "I'm not going to stand around and let you rob me without getting something else in return."
                "You push on her back and have her start walking towards your office."
                the_person "You make it sound like I'm sort of prostitute."
                "After a few steps shes realises that this is happening one way or another and falls into line."
                mc.name "Maybe I can convince you to let me keep my stuff."
                mc.name "Then you'll just be a slut. Better?"
                the_person "Hardly."
                "You lead her into your office and close the door behind you."
                $ should_fuck = True

            "Order her.\nRequires: 120 Obedience (disabled)" if the_person.obedience < 120:
                pass

            "Let it go.":
                mc.name "You're probably right."
                "You wait a few minutes in silence."


    else: #Hell yeah (TODO: Have an option for her to proposition you when she shows up instead)
        "She leans into you, pressing her weight into your side."
        the_person "I thought you'd never ask. Your office is a good idea, I think we'd cause a bit of a scene if we stayed here..."
        "You lead her to your office and close the door behind you."
        $ should_fuck = True

    if should_fuck:
        call fuck_person(the_person, private = True)
        $ the_report = _return
        if the_report.get("girl orgasms", 0) > 0:
            $ the_person.event_triggers_dict["bribe_successful"] = "orgasm"
            mc.name "I trust I've given you sufficient reason to take your thugs and leave?"
            "[the_person.possessive_title] is still breathing heavy, recovering from her climax."
            the_person "What? Oh... Fine, I'll call off my men."
            $ the_person.change_obedience(2)
            the_person "But nobody can know about this, understood?"
            mc.name "Of course [the_person.title]. It will be our little secret."
        else:
            $ the_report = _return
            $ the_person.call_dialogue("sex_review", the_report = the_report)
        $ the_person.apply_outfit()

    call clear_sex_slut_modifiers(the_person)
    return

label city_rep_order(the_person):
    $ the_person.event_triggers_dict["bribe_attempts"] = the_person.event_triggers_dict.get("bribe_attempts",[]).append("order_attempted")
    if the_person.obedience < 110:
        mc.name "[the_person.title], you're going to stop with this stupid charade. There isn't going to be any punishment today."
        "She smirks and glares at you."
        the_person "You really think that? You don't have any power here [the_person.mc_title]."
        the_person "Now take a breath and get yourself under control before you say something that makes things worse for you."

    elif the_person.obedience < 130:
        mc.name "[the_person.title], you need to make this go away for me."
        the_person "I can't just snap my fingers and make it go poof [the_person.mc_title]."
        the_person "There's paperwork, bosses to report to, a whole system."
        mc.name "But you can bypass all of that, right?"
        the_person "Only if I want to get fired! No, no, you're stuck with whatever punishment the rulebook lays out for you."

    else:
        mc.name "[the_person.title], you're going to make all of this go away for me. Change whatever paperwork you have to."
        if the_person.get_opinion_score("being submissive") >= 2:
            "[the_person.possessive_title] doesn't argue. She just nods her head obediently."
            the_person "Yes [the_person.mc_title], I'll make it happen."
            $ the_person.event_triggers_dict["bribe_successful"] = "order"
            mc.name "That's what I like to hear."
        else:
            the_person "I can't do that [the_person.mc_title], there would be so much trouble for me if someone found out."
            "Even as she protests she sounds unsure, as if uncertain about disobeying you."
            menu:
                "Do this and we're even. -5 Obedience.":
                    mc.name "Do it anyways. I won't ask you to do anything else if you can do this for me."
                    the_person "Well... If it's just this once I think I can manage it..."
                    $ the_person.event_triggers_dict["bribe_successful"] = "order"
                    $ the_person.change_obedience(-5)

                "Forget it.":
                    mc.name "Fine, forget about it then."
                    the_person "I'm sorry, if there was any way I could do it safely I would!"


    return

init -1 python:
    def city_rep_dressup_training_requirement(the_person):
        if the_person.get_known_opinion_score("skimpy uniforms") > 0:
            return True
        else:
            return "Likes Skimpy Uniforms"

    def city_rep_penalty_reduction_training_requirement(the_person):
        if the_person.event_triggers_dict.get("city_rep_reduced_penalties_trained", False):
            return False
        elif the_person.get_known_opinion_score("being submissive") < 1:
            return "Likes being submissive"
        else:
            return True

    def city_rep_internal_sabotage_training_requirement(the_person):
        if attention_bleed_increase_2_policy.is_owned():
            return False
        elif the_person.get_known_opinion_score("being submissive") < 2 or the_person.obedience < 120:
            return "Loves being submissive, 120+ Obedience"
        else:
            return True


label city_rep_dressup_training(the_person):
    mc.name "[the_person.title], I'm sure you get bored of these stuffy work uniforms you have to wear."
    the_person "... Sometimes I want to wear something more fun..."
    mc.name "Of course you do. Let's talk about that and give you something a lot more fun to wear next time..."
    "You describe your ideal uniform for her."
    call outfit_master_manager(slut_limit = the_person.sluttiness + 30, show_overwear = False, show_underwear = False)
    if _return:
        $ the_uniform = _return
        $ the_person.event_triggers_dict["city_rep_forced_uniform"] = the_uniform
        "She listens attentively. At one point she even starts taking notes."
        if the_uniform.vagina_visible():
            the_person "... But everyone at the office will be able to see my..."
            mc.name "Say it."
            the_person "They'll be able to see my pussy, [the_person.mc_title]."
            "She doesn't sound very worried about it, but that might just be the trance taking hold."
            the_person "Won't I get in trouble?"
            mc.name "I'm sure you can come up something. Maybe you need to start working from home."
            $ the_person.discover_opinion("showing her ass")
            $ the_person.change_slut(the_person.get_opinion_score("showing her ass"))
            the_person "But... I want to go to the office like this."
            mc.name "Then I hope your boss likes what he sees and decides to keep you around."
            "She nods obediently."
        elif the_uniform.tits_visible():
            the_person "But everyone at the office will see my..."
            mc.name "Say it."
            the_person "They'll be able to see my tits. I'll be showing my tits to everyone."
            "She doesn't sound very worried about it, but that might just be the trance taking hold."
            the_person "What if I get in trouble?"
            mc.name "I doubt anyone will complain much. Everyone likes to oggle a good set of tits."
            $ the_person.discover_opinion("showing her tits")
            $ the_person.change_slut(the_person.get_opinion_score("showing her tits"))
            "She bites her lips and nods obediently."
        elif the_uniform.underwear_visible():
            the_person "But I'll barely be covered..."
            mc.name "You're going to like it."
            "It's not a suggestion, it's a command. She nods."
            the_person "Okay. What if my boss comments on my outfit?"
            mc.name "Tell him he's welcome to look at much as he wants."
            mc.name "He probably has a boring job, he should be thanking me for giving him some eye candy."
            "She nods obediently."
        the_person "Okay, I'll go and buy everything I need tonight."
        mc.name "Good girl."
        return True
    return False


label city_rep_penalty_reduction_training(the_person):
    mc.name "[the_person.title], these penalties my business is being hit with are going to ruin me."
    mc.name "I need you to reduce them for me."
    "She shakes her head weakly."
    the_person "I can't... There are rules about this sort of thing..."
    mc.name "I'm sure they're more like guidelines. You're a smart girl, I'm certain you can figure something out."
    "The trance takes hold and she nods obediently."
    the_person "Okay, I'll figure something out."
    $ the_person.event_triggers_dict["city_rep_reduced_penalties_trained"] = True
    return


label city_rep_internal_sabotage_training(the_person):
    mc.name "[the_person.title], all of these visits are nice, but I'd like a little less attention from the city."
    mc.name "I want you to start destroying any evidence about me that crosses your desk."
    "She shakes her head weakly."
    the_person "I... I can't do that [the_person.mc_title]. It's not what I'm supposed to do."
    mc.name "It is now, because I'm telling you to do it."
    "She resists a moment longer, but she can only hold out so long while in a trance."
    the_person "Okay, I'll get rid of anything I can..."
    mc.name "Good girl."
    $ attention_bleed_increase_2_policy.buy_policy(ignore_cost = True)
    return

label city_rep_offer_hire(the_person):
    mc.name "Tell me [the_person.title], have you ever thought about finding work in the public sector?"
    mc.name "I'm sure you could make a lot more money at, random example, a friendly pharmaceutical company."
    "She shakes her head, dismissing the idea."
    the_person "I don't do this for the money, I do it for the people."
    the_person "It's not glamourous, but I know that I'm making a difference and keeping people safe."
    mc.name "Surely there's something I could offer you to change your mind."
    "She smiles politely and shakes her head again."
    the_person "Sorry [the_person.mc_title], I'm not for sale."
    return
