init 0 python:
    recruitment_policies_list = []

    #### RECRUITMENT IMPROVEMENT POLICIES ####

    recruitment_batch_one_policy = Policy(name = "Recruitment Batch Size Improvement One",
        desc = "More efficent hiring software will allow you to interview up to review up to four resumes in a single recruitment batch.",
        cost = 200,
        toggleable = True)

    recruitment_policies_list.append(recruitment_batch_one_policy)

    recruitment_batch_two_policy = Policy(name = "Recruitment Batch Size Improvement Two",
        desc = "Further improvements in hiring software and protocols allows you to review up to six resumes in a single recruitment batch.",
        cost = 600,
        toggleable = True,
        own_requirement = recruitment_batch_one_policy,
        dependant_policies = recruitment_batch_one_policy)

    recruitment_policies_list.append(recruitment_batch_two_policy)

    recruitment_batch_three_policy = Policy(name = "Recruitment Batch Size Improvement Three",
        desc = "A complete suite of recruitment software lets you maximize the use of your time while reviewing resumes. Allows you to review ten resumes in a single recruitment batch.",
        cost = 1200,
        toggleable = True,
        own_requirement = recruitment_batch_two_policy,
        dependant_policies = recruitment_batch_two_policy)

    recruitment_policies_list.append(recruitment_batch_three_policy)

    recruitment_knowledge_one_policy = Policy(name = "Applicant Questionnaire",
        desc = "A simple questionnaire required from each applicant reveals some of their likes and dislikes, helpying to determine if they would a good fit for your company culture. Reveals two opinions on an applicants resume.",
        cost = 400,
        toggleable = True)
    recruitment_policies_list.append(recruitment_knowledge_one_policy)

    recruitment_knowledge_two_policy = Policy(name = "Applicant Background Checks",
        desc = "An automated background check produces a detailed history for each applicant. This can reveal a great deal of information about a potential employee before they even step in the door. Reveals two more opinions on an applicants resume.",
        cost = 800,
        toggleable = True,
        own_requirement = recruitment_knowledge_one_policy,
        dependant_policies = recruitment_knowledge_one_policy)
    recruitment_policies_list.append(recruitment_knowledge_two_policy)

    recruitment_knowledge_three_policy = Policy(name = "Applicant History Deep Dive",
        desc = "Scrapping the web for any and all information about an applicant can reveal a startling amount of information. Reveals one more opinion on an applicants resume, and revealed opinions may be about sex.",
        cost = 1500,
        toggleable = True,
        own_requirement = recruitment_knowledge_two_policy,
        dependant_policies = recruitment_knowledge_two_policy)
    recruitment_policies_list.append(recruitment_knowledge_three_policy)

    recruitment_knowledge_four_policy = Policy(name = "Applicant Sexual History Survey",
        desc = "A detailed questionnaire focused on sex, fetishes, and kinks produces even more information about an applicants sexaul preferences. It can also be used as a surprisingly accurate predictor of sexual experience. Reveals one more opinion, and sex skills are now displayed on an applicants resume.",
        cost = 2500,
        toggleable = True,
        own_requirement = recruitment_knowledge_three_policy,
        dependant_policies = recruitment_knowledge_three_policy)
    recruitment_policies_list.append(recruitment_knowledge_four_policy)

    def recruitment_skill_improvement_requirement():
        return True

    recruitment_skill_improvement_policy = Policy(name = "Recruitment Skill Improvement",
        desc = "Restricting your recruitment search to university and college graduates improves their skill across all disiplines. Raises all skill caps when hiring new employees by two, lowers average age.",
        cost = 800,
        toggleable = True)
    recruitment_policies_list.append(recruitment_skill_improvement_policy)

    recruitment_stat_improvement_policy = Policy(name = "Recruitment Stat Improvment",
        desc = "A wide range of networking connections can put you in touch with the best and brightest in the industry. Raises all statistic caps when hiring new employees by two, raises average age.",
        cost = 1500,
        toggleable = True,
        own_requirement = recruitment_skill_improvement_policy,
        dependant_policies = recruitment_skill_improvement_policy)
    recruitment_policies_list.append(recruitment_stat_improvement_policy)

    recruitment_suggest_improvment_policy = Policy(name = "High Suggestibility Recruits",
        desc = "You change your focus to hiring younger, more impressionable employees. New employees will all have a starting suggestibility of 10. Lowers average age.",
        cost = 1000,
        toggleable = True,
        own_requirement = recruitment_knowledge_three_policy)
    recruitment_policies_list.append(recruitment_suggest_improvment_policy)

    recruitment_obedience_improvement_policy = Policy(name = "High Obedience Recruits",
        desc = "A highly regimented business appeals to some people. By improving your corporate image and stressing company stability new recruits will have a starting obedience 10 points higher than normal.",
        cost = 600,
        toggleable = True)
    recruitment_policies_list.append(recruitment_obedience_improvement_policy)

    recruitment_slut_improvement_policy = Policy(name = "High Sluttiness Recruits",
        desc = "Narrowing your resume search parameters to include previous experience at strip clubs, bars, and modeling agencies produces a batch of potential employees with a much higher initial slutiness value. Increases starting sluttiness by 20, lowers average age.",
        cost = 1200,
        toggleable = True,
        own_requirement = recruitment_obedience_improvement_policy)
    recruitment_policies_list.append(recruitment_slut_improvement_policy)

    recruitment_sex_improvement_policy = Policy (name = "Recruitment Sex Skill Improvement",
        desc = "Extending your recruitment advertising to several pornographic sites is likely to draw people with higher than average sex skills. Raises all sex skill caps by two.",
        cost = 1500,
        toggleable = True,
        active_requirement = [recruitment_slut_improvement_policy, recruitment_knowledge_two_policy])
    recruitment_policies_list.append(recruitment_sex_improvement_policy)

    def increase_interview_cost(amount):
        mc.business.recruitment_cost += amount

    def decrease_interview_cost(amount):
        mc.business.recruitment_cost -= amount

    recruitment_big_tits_policy = Policy(name = "Screening Criteria: Large Breasts",
        desc = "Only accept resumes from applicants with a D cup or larger. Raises the cost of screening applicants by $100 while active.",
        cost = 2000,
        toggleable = True,
        own_requirement = recruitment_knowledge_two_policy,
        on_apply_function = increase_interview_cost,
        on_remove_function = decrease_interview_cost,
        extra_arguments = {"amount":100},
        exclusive_tag = "breast_critera")
    recruitment_policies_list.append(recruitment_big_tits_policy)

    recruitment_huge_tits_policy = Policy(name = "Screening Criteria: Huge Breasts",
        desc = "All but the most big-breasted women have their resume automatically rejected, ensuring all applicants will have an E cup or larger. Raises the cost of screening applicants by $500 while active.",
        cost = 4500,
        toggleable = True,
        own_requirement = [recruitment_big_tits_policy, recruitment_knowledge_three_policy],
        on_apply_function = increase_interview_cost,
        on_remove_function = decrease_interview_cost,
        extra_arguments = {"amount":500},
        exclusive_tag = "breast_critera")
    recruitment_policies_list.append(recruitment_huge_tits_policy)

    recruitment_small_tits_policy = Policy(name = "Screening Criteria: Small Breasts",
        desc = "Eliminates resumes from applicants with a D cup or larger, leaving only small-chested women in the application pool. Raises the cost of screening applicatns by $100 while active.",
        cost = 2000,
        toggleable = True,
        own_requirement = recruitment_knowledge_two_policy,
        on_apply_function = increase_interview_cost,
        on_remove_function = decrease_interview_cost,
        extra_arguments = {"amount":100},
        exclusive_tag = "breast_critera")
    recruitment_policies_list.append(recruitment_small_tits_policy)

    recruitment_tiny_tits_policy = Policy(name = "Screening Criteria: Tiny Breasts",
        desc = "Automatically removes the resume of any woman applying with more than an AA cup. The smaller pool of talent raises the cost of screening applicants by $500 while active.",
        cost = 4500,
        toggleable = True,
        own_requirement = recruitment_small_tits_policy,
        on_apply_function = increase_interview_cost,
        on_remove_function = decrease_interview_cost,
        extra_arguments = {"amount":500},
        exclusive_tag = "breast_critera")
    recruitment_policies_list.append(recruitment_tiny_tits_policy)

    recruitment_short_policy = Policy(name = "Screening Criteria: Short",
        desc = "Only accept applications from women under 5',3\". Raises the cost of applicant screening by $50.",
        cost = 1500,
        toggleable = True,
        own_requirement = recruitment_knowledge_one_policy,
        on_apply_function = increase_interview_cost,
        on_remove_function = decrease_interview_cost,
        extra_arguments = {"amount":50},
        exclusive_tag = "height_critera")
    recruitment_policies_list.append(recruitment_short_policy)

    recruitment_tall_policy = Policy(name = "Screening Criteria: Tall",
        desc = "Only accept applications from women over 5',9\". Raises the cost of applicant screening by $50.",
        cost = 1500,
        toggleable = True,
        own_requirement = recruitment_knowledge_one_policy,
        on_apply_function = increase_interview_cost,
        on_remove_function = decrease_interview_cost,
        extra_arguments = {"amount":50},
        exclusive_tag = "height_critera")
    recruitment_policies_list.append(recruitment_tall_policy)

    recruitment_mothers_policy = Policy(name = "Screening Criteria: Mother",
        desc = "Only seek applications from women who are mothers. Raises the cost of applicant screening by $200.",
        cost = 2000,
        toggleable = True,
        own_requirement = recruitment_knowledge_three_policy,
        on_apply_function = increase_interview_cost,
        on_remove_function = decrease_interview_cost,
        extra_arguments = {"amount":200},
        exclusive_tag = "mother_critera")
    recruitment_policies_list.append(recruitment_mothers_policy)

    recruitment_childless_policy = Policy(name = "Screening Criteria: Childless",
        desc = "Only seek applications from women who are not parents. Raise the cost of applicant screening by $50.",
        cost = 1000,
        toggleable = True,
        own_requirement = recruitment_knowledge_three_policy,
        on_apply_function = increase_interview_cost,
        on_remove_function = decrease_interview_cost,
        extra_arguments = {"amount":50},
        exclusive_tag = "mother_critera")
    recruitment_policies_list.append(recruitment_childless_policy)

    recruitment_single_policy = Policy(name = "Screening Criteria: Single",
        desc = "Take applications only from women who are currently single. Raise the cost of applicant screening by $200.",
        cost = 2000,
        toggleable = True,
        own_requirement = recruitment_knowledge_two_policy,
        on_apply_function = increase_interview_cost,
        on_remove_function = decrease_interview_cost,
        extra_arguments = {"amount":200},
        exclusive_tag = "relationship_criteria")
    recruitment_policies_list.append(recruitment_single_policy)

    recruitment_married_policy = Policy(name = "Screening Criteria: Married",
        desc = "Take applications only from women who are married. Raise the cost of applicant screening by $200.",
        cost = 2000,
        toggleable = True,
        own_requirement = recruitment_knowledge_two_policy,
        on_apply_function = increase_interview_cost,
        on_remove_function = decrease_interview_cost,
        extra_arguments = {"amount":200},
        exclusive_tag = "relationship_criteria")
    recruitment_policies_list.append(recruitment_married_policy)

    recruitment_old_policy = Policy(name = "Screening Criteria: Old",
        desc = "Only accept applications from women 40 or older. Raise the cost of applicant sceening by $100.",
        cost = 2000,
        toggleable = True,
        own_requirement = recruitment_knowledge_one_policy,
        on_apply_function = increase_interview_cost,
        on_remove_function = decrease_interview_cost,
        extra_arguments = {"amount":100},
        exclusive_tag = "age_criteria")
    recruitment_policies_list.append(recruitment_old_policy)

    recruitment_teen_policy = Policy(name = "Screening Criteria: Teenager",
        desc = "Only accept applications from women ages 18 or 19. Raise the cost of applicant sceening by $400.",
        cost = 5000,
        toggleable = True,
        own_requirement = recruitment_knowledge_one_policy,
        on_apply_function = increase_interview_cost,
        on_remove_function = decrease_interview_cost,
        extra_arguments = {"amount":400},
        exclusive_tag = "age_criteria")
    recruitment_policies_list.append(recruitment_teen_policy)
