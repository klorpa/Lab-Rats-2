init 0 python:
    recruitment_policies_list = []

    #### RECRUITMENT IMPROVEMENT POLICIES ####

    def recruitment_batch_one_requirement():
        return True

    recruitment_batch_one_policy = Policy(name = "Recruitment Batch Size Improvement One",
        desc = "More efficent hiring software will allow you to interview up to review up to four resumes in a single recruitment batch.",
        cost = 200,
        toggleable = True,
        requirement = recruitment_batch_one_requirement)

    recruitment_policies_list.append(recruitment_batch_one_policy)

    def recruitment_batch_two_requirement():
        if recruitment_batch_one_policy.is_owned():
            return True
        else:
            return False

    recruitment_batch_two_policy = Policy(name = "Recruitment Batch Size Improvement Two",
        desc = "Further improvements in hiring software and protocols allows you to review up to six resumes in a single recruitment batch.",
        cost = 600,
        toggleable = True,
        requirement = recruitment_batch_two_requirement,
        dependant_policies = recruitment_batch_one_policy)

    recruitment_policies_list.append(recruitment_batch_two_policy)

    def recruitment_batch_three_requirement():
        if recruitment_batch_two_policy.is_owned():
            return True
        else:
            return False

    recruitment_batch_three_policy = Policy(name = "Recruitment Batch Size Improvement Three",
        desc = "A complete suite of recruitment software lets you maximize the use of your time while reviewing resumes. Allows you to review ten resumes in a single recruitment batch.",
        cost = 1200,
        toggleable = True,
        requirement = recruitment_batch_three_requirement,
        dependant_policies = recruitment_batch_two_policy)

    recruitment_policies_list.append(recruitment_batch_three_policy)

    def recruitment_knowledge_one_requirement():
        return True

    recruitment_knowledge_one_policy = Policy(name = "Applicant Questionnaire",
        desc = "A simple questionnaire required from each applicant reveals some of their likes and dislikes, helpying to determine if they would a good fit for your company culture. Reveals two opinions on an applicants resume.",
        cost = 400,
        toggleable = True,
        requirement = recruitment_knowledge_one_requirement)
    recruitment_policies_list.append(recruitment_knowledge_one_policy)

    def recruitment_knowledge_two_requirement():
        if recruitment_knowledge_one_policy.is_owned():
            return True
        else:
            return False

    recruitment_knowledge_two_policy = Policy(name = "Applicant Background Checks",
        desc = "An automated background check produces a detailed history for each applicant. This can reveal a great deal of information about a potential employee before they even step in the door. Reveals two more opinions on an applicants resume.",
        cost = 800,
        toggleable = True,
        requirement = recruitment_knowledge_two_requirement,
        dependant_policies = recruitment_knowledge_one_policy)
    recruitment_policies_list.append(recruitment_knowledge_two_policy)

    def recruitment_knowledge_three_requirement():
        if recruitment_knowledge_two_policy.is_owned():
            return True
        else:
            return False

    recruitment_knowledge_three_policy = Policy(name = "Applicant History Deep Dive",
        desc = "Scrapping the web for any and all information about an applicant can reveal a startling amount of information. Reveals one more opinion on an applicants resume, and revealed opinions may be about sex.",
        cost = 1500,
        toggleable = True,
        requirement = recruitment_knowledge_three_requirement,
        dependant_policies = recruitment_knowledge_two_policy)
    recruitment_policies_list.append(recruitment_knowledge_three_policy)

    def recruitment_knowledge_four_requirement():
        if recruitment_knowledge_three_policy.is_owned():
            return True
        else:
            return False

    recruitment_knowledge_four_policy = Policy(name = "Applicant Sexual History Survey",
        desc = "A detailed questionnaire focused on sex, fetishes, and kinks produces even more information about an applicants sexaul preferences. It can also be used as a surprisingly accurate predictor of sexual experience. Reveals one more opinion, and sex skills are now displayed on an applicants resume.",
        cost = 2500,
        toggleable = True,
        requirement = recruitment_knowledge_four_requirement,
        dependant_policies = recruitment_knowledge_three_policy)
    recruitment_policies_list.append(recruitment_knowledge_four_policy)

    def recruitment_skill_improvement_requirement():
        return True

    recruitment_skill_improvement_policy = Policy(name = "Recruitment Skill Improvement",
        desc = "Restricting your recruitment search to university and college graduates improves their skill across all disiplines. Raises all skill caps when hiring new employees by two.",
        cost = 800,
        toggleable = True,
        requirement = recruitment_skill_improvement_requirement)

    recruitment_policies_list.append(recruitment_skill_improvement_policy)

    def recruitment_stat_improvement_requirement():
        if recruitment_skill_improvement_policy.is_owned():
            return True
        else:
            return False

    recruitment_stat_improvement_policy = Policy(name = "Recruitment Stat Improvment",
        desc = "A wide range of networking connections can put you in touch with the best and brightest in the industry. Raises all statistic caps when hiring new employees by two.",
        cost = 1500,
        toggleable = True,
        requirement = recruitment_stat_improvement_requirement,
        dependant_policies = recruitment_skill_improvement_policy)

    recruitment_policies_list.append(recruitment_stat_improvement_policy)

    # def recruitment_high_suggest_requirement(): #TODO: Figure out what this means with suggestibility. What the hell do we even want suggestability to do right now?
    #     return True
    #
    # recruitment_suggest_improvment_policy = Policy(name = "High Suggestibility Recruits",
    #     desc = "You change your focus to hiring younger, more impressionable employees. New employees will all have a starting suggestibility of 10.",
    #     cost = 600,
    #     requirement = recruitment_high_suggest_requirement)
    #
    # recruitment_policies_list.append(recruitment_suggest_improvment_policy)

    def recruitment_obedience_improvement_requirement():
        return True

    recruitment_obedience_improvement_policy = Policy(name = "High Obedience Recruits",
        desc = "A highly regimented business appeals to some people. By improving your corporate image and stressing company stability new recruits will have a starting obedience 10 points higher than normal.",
        cost = 600,
        toggleable = True,
        requirement = recruitment_obedience_improvement_requirement)

    recruitment_policies_list.append(recruitment_obedience_improvement_policy)

    def recruitment_slut_improvement_requirement():
        if recruitment_obedience_improvement_policy.is_owned():
            return True
        else:
            return False

    recruitment_slut_improvement_policy = Policy(name = "High Sluttiness Recruites",
        desc = "Narrowing your resume search parameters to include previous experience at strip clubs, bars, and modeling agencies produces a batch of potential employees with a much higher initial slutiness value. Increases starting sluttiness by 20.",
        cost = 1200,
        toggleable = True,
        requirement = recruitment_slut_improvement_requirement)

    recruitment_policies_list.append(recruitment_slut_improvement_policy)

    #TODO: Add a policy that improves the sex skills of your recruits.
