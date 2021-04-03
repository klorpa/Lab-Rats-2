init 1299:
    python:
        list_of_personalities = []

        def get_random_personality():
            return get_random_from_list(list_of_personalities)


#Prior to v0.26.0 this file contained all personality definitions. It now only defines the master list of personalites and holds a few helper functions related to personalities.
    #These are the different personality specific responses/dialogue options called through the game. These must all be defined for general personalites.

    # @_greetings - short convo used when you start a convo with someome.
    # @_sex_responses_[foreplay, oral, vaginal, anal] - exclamation used while having sex, generally vaginal.
    # @_climax_responses_[foreplay, oral, vaginal, anal] - exclamation used when a girl climaxes, with a different type for each type of sex
    # @_clothing_accept - dialogue used when you add an outfit to a girls wardrobe and she accepts it.
    # @_clothing_reject - dialogue used when you offer an outfit to a girl but she refuses it because it's too slutty.
    # @_clothing_review - dialogue used after sex when a girl checks her outfit and realises she needs to get redressed.
    # @_strip_reject - dialogue used when you try and strip a piece of clothing off of a girl but she wants it in place.
    # @_sex_accept - dialogue when you offer a sex position to a girl and she agrees because she's slutty. (Not just when you seduce them, that's below!)
    # @_sex_obedience_accept - dialogue used when you offer a sex position to a girl but she only agrees because she's obedient
    # @_sex_gentle_reject - dialouge used when you try and offer a sex position to a girl but she refuse without being angry
    # @_sex_angry_reject - dialogue used when you try and offer a sex position to a girl with a psotiion she finds ridiculously inappropriate.
    # @_seduction_response - dialogue used when you seduce a girl and she accepts
    # @_flirt_response - dialogue when you "chat with" and "flirt" with a girl.
    # @_cum_face - dialogue when you cum on a girls face.
    # @_cum_mouth - dialogue when you cum in a girls mouth
    # @_surprised_exclaim - List of random exclimations used when a character is surprised.
    # @_talk_busy - dialogue used when you've used "chat with" option too many times
    # @_improved_serum_unlock - dialogue used for the serum unlock head researcher event.
    # @_sex_strip - dialogue used when a girl strips for you (but she's not asking permission).
    # @_sex_watch - dialogue used when you're having sex in front of this girl.
    # @_being_watched - dialogue when you're having sex with the girl and being watched by another person
    # @_work_enter_greeting - dialogue used when you walk into a room at work with an employee in it.
    # @_date_seduction - dialogue used after a date when the person had a good time and wants to go back to have sex/make out/whatever.

    ### TABOO DIALOGUE ###
    #Sex Taboos
    # @_kissing_taboo_break - dialogue used the first time you go to kiss the girl
    # @_touching_body_taboo_break - dialogue used the first time you touch to body/breasts of the girl
    # @_touching_penis_taboo_break - dialogue used the first time you convince the girl to touch your penis.
    # @_touching_vagina_taboo_break - dialogue used the first time you touch a girls vagina.
    # @_sucking_cock_taboo_break - dialogue used the first time you convince a girl to suck your cock.
    # @_licking_pussy_taboo_break - dialogue used the first time you lick a girls pussy.
    # @_vaginal_sex_taboo_break - dialogue used the first time you fuck a girl.
    # @_anal_sex_taboo_break - dilogue used the first time you anal a girl.
    # @_condomless_sex_taboo_break - dialogue used the first time you convince a girl to have sex without a condom.

    #Nudity Taboos
    # @_underwear_nudity_taboo_break - dialogue used the first time you see a girl in her underwear
    # @_bare_tits_taboo_break - dialogue used when you first see a girls tits
    # @_bare_pussy_taboo_break - dialogue used when you first see a girls pussy

    #Cum Taboos
    # @_facial_cum_taboo_break - dialogue used when you first cum on a girls face
    # @_mouth_cum_taboo_break - dialogue used when you first cum in a girls mouth
    # @_body_cum_taboo_break - dialogue used when you first cum on a girls body (tits included)
    # @_creampie_taboo_break - dialogue used when you first creampie a girl
    # @_anal_creampie_taboo_break - dialogue used when you first anal creampie a girl
