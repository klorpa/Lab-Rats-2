init -1 python: #You can add your own trainables to these lists after init -1
    stat_trainables = []
    skill_trainables = []
    opinion_trainables = []
    special_trainables = [] #Trainables put in this list are universal, and also displayed in the same list as Role specific trainables.

    # Trainable definitions are defined here, the labels and requirements are seperated off into their own file.
    # STAT TRAINABLES #
    sluttiness_trainable = Trainable("slut_train", "train_slut_label", "Increase Sluttiness", base_cost = 200)
    stat_trainables.append(sluttiness_trainable)

    obedience_trainable = Trainable("train_obedience", "train_obedience_label", "Increase Obedience", base_cost = 200)
    stat_trainables.append(obedience_trainable)

    love_trainable = Trainable("train_love", "train_love_label", "Increase Love", base_cost = 200)
    stat_trainables.append(love_trainable)

    suggest_trainable = Trainable("train_suggest", "train_suggest_label", "Increase Suggestibility", base_cost = 400)
    stat_trainables.append(suggest_trainable)

    charisma_trainable = Trainable("train_charisma", "train_charisma_label", "Increase Charisma", base_cost = 600)
    stat_trainables.append(charisma_trainable)

    intelligence_trainable = Trainable("train_intelligence", "train_intelligence_label", "Increase Intelligence", base_cost = 600)
    stat_trainables.append(intelligence_trainable)

    focus_trainable = Trainable("train_focus", "train_focus_label", "Increase Focus", base_cost = 600)
    stat_trainables.append(focus_trainable)

    # WORK SKILL TRAINABLES #
    hr_trainable = Trainable("hr_train", "train_hr_label", "Increase HR Skill", unlocked_function = train_work_requirement)
    skill_trainables.append(hr_trainable)

    market_trainable = Trainable("market_train", "train_market_label", "Increase Marketing Skill", unlocked_function = train_work_requirement)
    skill_trainables.append(market_trainable)

    research_trainable = Trainable("research_train", "train_research_label", "Increase R&D Skill", unlocked_function = train_work_requirement)
    skill_trainables.append(research_trainable)

    production_trainable = Trainable("production_train", "train_production_label", "Increase Production Skill", unlocked_function = train_work_requirement)
    skill_trainables.append(production_trainable)

    supply_trainable = Trainable("supply_train", "train_supply_label", "Increase Supply Skill", unlocked_function = train_work_requirement)
    skill_trainables.append(supply_trainable)

    # SEX SKILL TRAINABLES #
    foreplay_trainable = Trainable("foreplay_train", "train_foreplay_label", "Increase Foreplay Skill", unlocked_function = train_foreplay_requirement)
    skill_trainables.append(foreplay_trainable)

    oral_trainable = Trainable("oral_train", "train_oral_label", "Increase Oral Skill", base_cost = 200, unlocked_function = train_oral_requirement )
    skill_trainables.append(oral_trainable)

    vaginal_trainable = Trainable("vaginal_train", "train_vaginal_label", "Increase Vaginal Skill", base_cost = 300, unlocked_function = train_vaginal_requirement)
    skill_trainables.append(vaginal_trainable)

    anal_trainable = Trainable("anal_train", "train_anal_label", "Increase Anal Skill", base_cost = 400, unlocked_function = train_anal_requirement)
    skill_trainables.append(anal_trainable)

    # OPINION SKILL TRAINABLES #
    learn_opinion_trainable = Trainable("learn_opinion_train", "train_learn_opinion_label", "Reveal a New Opinion", unlocked_function = train_learn_opinion_requirement)
    opinion_trainables.append(learn_opinion_trainable)

    strengthen_opinion_trainable = Trainable("strengthen_opinion_train", "train_strengthen_opinion_label", "Strengthen an Opinion", base_cost = 200, unlocked_function = train_strengthen_opinion_requirement, training_tag = "change_opinion")
    opinion_trainables.append(strengthen_opinion_trainable)

    weaken_opinion_trainable = Trainable("weaken_opinion_train", "train_weaken_opinion_label", "Weaken an Opinion", unlocked_function = train_weaken_opinion_requirement, training_tag = "change_opinion")
    opinion_trainables.append(weaken_opinion_trainable)

    new_normal_opinion_trainable = Trainable("new_normal_opinion_train", "train_new_opinion_label", "Inspire a New Normal Opinion", training_tag = "new_opinion")
    opinion_trainables.append(new_normal_opinion_trainable)

    new_sexy_opinion_trainable = Trainable("new_sexy_opinion_train", "train_new_opinion_label", "Inspire a New Sex Opinion", base_cost = 200, extra_args = True, training_tag = "new_opinion")
    opinion_trainables.append(new_sexy_opinion_trainable)

    # SPECIAL TRAINABLES #
    breeder_trainable = Trainable("breeder_train", "train_breeder_label", "Breeding Fascination", base_cost = 1500, unlocked_function = train_breeder_requirement)
    special_trainables.append(breeder_trainable)

    hypno_orgasm_trainable = Trainable("hypno_orgasm_train", "train_hypnotic_orgasm", "Trigger Word Orgasms", base_cost = 1000, unlocked_function = train_hypnotic_orgasm_requirement)
    special_trainables.append(hypno_orgasm_trainable)

    online_attention_whore_trainable = Trainable("online_attention_whore", "train_online_attention_whore", "Online Attention Whore", base_cost = 800, unlocked_function = train_online_attention_whore_requirement)
    special_trainables.append(online_attention_whore_trainable) #RIght now this ensures she has all possible social media accounts. TODO: In the future we should expand on this some more, make this the intro to a longer storyline.
