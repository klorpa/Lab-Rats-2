## This file holds the upgrades for your business, known as "policies".
## Policies have a:
## 1) Name, used when displaying the button for them/
## 2) A description, a text description of the effects the policy will have on your business.
## 3) A cost, a value in $$$ that purchasing the policy will cost.
## 4) A requirement, a function that is evaluated when checking to see if the player can purchase this policy.

init 1300 python:
    policies_list = [] #The master list of policies that can be displayed for purchase.

    uniform_policies_list = []
    recruitment_policies_list = []
    serum_policies_list = []
    organisation_policies_list = []


    #### UNIFORM POLICY SECTION ####
    def reset_invalid_uniforms(uniform_disobedience_priority): #Called by all uniform policies to clear newly inappropriate planned uniforms.
        slut_limit, underwear_limit, limited_to_top = mc.business.get_uniform_limits()
        for employee in mc.business.get_employee_list():
            if employee.planned_uniform:
                if employee.planned_uniform.slut_requirement > slut_limit and employee.planned_uniform.slut_requirement > employee.effective_sluttiness():
                    employee.planned_uniform = None
                    employee.apply_outfit()
        return

    def strict_uniform_policy_requirement(): #
        return True

    strict_uniform_policy = Policy(name = "Strict Corporate Uniforms",
        desc = "Requiring certain styles of attire in the business world is nothing new. Allows you to designate overwear sets of sluttiness 5 or less as part of your business uniform.",
        cost = 500,
        toggleable = True,
        requirement = strict_uniform_policy_requirement,
        on_remove_function = reset_invalid_uniforms,
        on_move_function = uniform_disobedience_on_move,
        extra_arguments = {"uniform_disobedience_priority":0}) #Uniform disobedience is only run once, regardless of how many policies are running. The highest priority uniform function is run.


    uniform_policies_list.append(strict_uniform_policy)

    def relaxed_uniform_policy_requirement():
        if strict_uniform_policy.is_owned():
            return True
        else:
            return False

    relaxed_uniform_policy = Policy(name = "Relaxed Corporate Uniforms",
        desc = "Corporate dress code is broadened to include more casual apparel. You can designate overwear sets up to sluttiness 15 as part of your business uniform.",
        cost = 1000,
        toggleable = True,
        requirement = relaxed_uniform_policy_requirement,
        on_remove_function = reset_invalid_uniforms,
        on_move_function = uniform_disobedience_on_move,
        dependant_policies = strict_uniform_policy,
        extra_arguments = {"uniform_disobedience_priority":1})

    uniform_policies_list.append(relaxed_uniform_policy)

    def casual_uniform_policy_requirement():
        if relaxed_uniform_policy.is_owned():
            return True
        else:
            return False

    casual_uniform_policy = Policy(name = "Casual Corporate Uniforms",
        desc = "Corporate dress code is broadened even further. Overwear sets up to 25 sluttiness are now valid uniforms.",
        cost = 2000,
        toggleable = True,
        requirement = casual_uniform_policy_requirement,
        on_remove_function = reset_invalid_uniforms,
        on_move_function = uniform_disobedience_on_move,
        dependant_policies = relaxed_uniform_policy,
        extra_arguments = {"uniform_disobedience_priority":2})

    uniform_policies_list.append(casual_uniform_policy)

    def reduced_coverage_uniform_policy_requirment():
        if casual_uniform_policy.is_owned():
            return True
        else:
            return False

    reduced_coverage_uniform_policy = Policy(name = "Reduced Coverage Corporate Uniforms",
        desc = "The term \"appropriate coverage\" in the employee manual is redefined and subject to employer approval. You can now use full outfits or underwear sets as part of your corporate uniform. Underwear sets must have a sluttiness score of 10 or less, outfits to 40 or less.",
        cost = 5000,
        toggleable = True,
        requirement = reduced_coverage_uniform_policy_requirment,
        on_remove_function = reset_invalid_uniforms,
        on_move_function = uniform_disobedience_on_move,
        dependant_policies = casual_uniform_policy,
        extra_arguments = {"uniform_disobedience_priority":3})

    uniform_policies_list.append(reduced_coverage_uniform_policy)

    def minimal_coverage_uniform_policy_requirement():
        if reduced_coverage_uniform_policy.is_owned():
            return True
        else:
            return False

    minimal_coverage_uniform_policy = Policy(name = "Minimal Coverage Corporate Uniforms",
        desc = "Corporate dress code is broadened further. Uniforms must now only meet a \"minumum coverage\" requirement, generally nothing more than a set of bra and panties. Full uniforms can have a sluttiness score of 60, underwear sets can go up to 15.",
        cost = 10000,
        toggleable = True,
        requirement = minimal_coverage_uniform_policy_requirement,
        on_remove_function = reset_invalid_uniforms,
        on_move_function = uniform_disobedience_on_move,
        dependant_policies = reduced_coverage_uniform_policy,
        extra_arguments = {"uniform_disobedience_priority":4})

    uniform_policies_list.append(minimal_coverage_uniform_policy)

    def corporate_enforced_nudity_requirement():
        if minimal_coverage_uniform_policy.is_owned():
            return True
        else:
            return False

    corporate_enforced_nudity_policy = Policy(name = "Corporate Enforced Nudity",
        desc = "Corporate dress code is removed in favour of a \"need to wear\" system. All clothing items that are deemed non-essential are subject to employer approval. Conveniently, all clothing is deemed non-essential. Full outfit sluttiness is limited to 80 or less, underwear sets have no limit.",
        cost = 25000,
        toggleable = True,
        requirement = corporate_enforced_nudity_requirement,
        on_remove_function = reset_invalid_uniforms,
        on_move_function = uniform_disobedience_on_move,
        dependant_policies = minimal_coverage_uniform_policy,
        extra_arguments = {"uniform_disobedience_priority":5})

    uniform_policies_list.append(corporate_enforced_nudity_policy)

    def maximal_arousal_uniform_policy_requirement():
        if corporate_enforced_nudity_policy.is_owned():
            return True
        else:
            return False

    maximal_arousal_uniform_policy = Policy(name = "Maximal Arousal Uniform Policy",
        desc = "Visually stimulating uniforms are deemed essential to the workplace. Any and all clothing items and accessories are allowed, uniform sluttiness is uncapped.",
        cost = 50000,
        toggleable = True,
        requirement = maximal_arousal_uniform_policy_requirement,
        on_remove_function = reset_invalid_uniforms,
        on_move_function = uniform_disobedience_on_move,
        dependant_policies = corporate_enforced_nudity_policy,
        extra_arguments = {"uniform_disobedience_priority":6})

    uniform_policies_list.append(maximal_arousal_uniform_policy)

    def male_focused_marketing_requirement():
        if strict_uniform_policy.is_owned():
            return True
        else:
            return False

    male_focused_marketing_policy = Policy(name = "Male Focused Modeling",
        desc = "The adage \"Sex Sells\" is especially true when selling your serum to men. Serum will sell for %1 per point of sluttiness of your marketing uniform.",
        cost = 500,
        toggleable = True,
        requirement = male_focused_marketing_requirement,
        dependant_policies = strict_uniform_policy)

    uniform_policies_list.append(male_focused_marketing_policy)


    #### SERUM TESTING POLICY SECTION ####

    def mandatory_paid_serum_testing_policy_requirement():
        return True

    mandatory_paid_serum_testing_policy = Policy(name = "Mandatory Paid Serum Testing",
        desc = "Employees will be required to take doses of serum when requested for \"testing purposes\". They will be entitled to compensation equal to five days wages.",
        cost = 500,
        toggleable = True,
        requirement = mandatory_paid_serum_testing_policy_requirement)

    serum_policies_list.append(mandatory_paid_serum_testing_policy)

    def mandatory_unpaid_serum_testing_policy_requirement():
        if mandatory_paid_serum_testing_policy.is_owned():
            return True
        else:
            return False

    mandatory_unpaid_serum_testing_policy = Policy(name = "Mandatory Unpaid Serum Testing",
        desc = "Updates to your employe contracts will remove the requirement for compensation when they are asked to test serums.",
        cost = 2000,
        toggleable = True,
        requirement = mandatory_unpaid_serum_testing_policy_requirement,
        dependant_policies = mandatory_paid_serum_testing_policy)

    serum_policies_list.append(mandatory_unpaid_serum_testing_policy)

    def daily_serum_dosage_policy_requirement():
        if mandatory_unpaid_serum_testing_policy.is_owned():
            return True
        else:
            return False

    daily_serum_dosage_policy = Policy(name = "Daily Serum Dosage",
        desc = "Mandatory serum testing is expanded into a full scale daily dosage program. Each employee will recieve a dose of the selected serum for their department, if one is currently in the stockpile.",
        cost = 5000,
        toggleable = True,
        requirement = daily_serum_dosage_policy_requirement,
        dependant_policies = mandatory_unpaid_serum_testing_policy)

    serum_policies_list.append(daily_serum_dosage_policy)

    def batch_size_increase(increase_amount = 0):
        mc.business.batch_size += increase_amount

    def batch_size_1_requirement():
        return True

    serum_size_1_policy = Policy(name = "Batch Size Improvement 1",
        desc = "Updating the equipment throughout the lab allows for increased batch sizes of serum as well as improved supply efficiency. Increases serum batch size by 1.",
        cost = 500,
        toggleable = True,
        requirement = batch_size_1_requirement,
        on_buy_function = batch_size_increase,
        extra_arguments = {"increase_amount":1})
    serum_policies_list.append(serum_size_1_policy)

    def batch_size_2_requirement():
        if serum_size_1_policy.is_owned():
            return True
        else:
            return False

    serum_size_2_policy = Policy(name = "Batch Size Improvement 2",
        desc = "Improved recycling of waste materials allows for a boost in production efficency. Increases serum batch size by 2.",
        cost = 2500,
        toggleable = True,
        requirement = batch_size_2_requirement,
        on_buy_function = batch_size_increase,
        extra_arguments = {"increase_amount":2},
        dependant_policies = serum_size_1_policy)
    serum_policies_list.append(serum_size_2_policy)

    def batch_size_3_requirement():
        if serum_size_2_policy.is_owned():
            return True
        else:
            return False

    serum_size_3_policy = Policy(name = "Batch Size Improvement 3",
        desc = "Another improvement to the lab equipment allows for even more impressive boosts in production efficency and speed. Increases serum batch size by 2.",
        cost = 10000,
        toggleable = True,
        requirement = batch_size_3_requirement,
        on_buy_function = batch_size_increase,
        extra_arguments = {"increase_amount":2},
        dependant_policies = serum_size_2_policy)
    serum_policies_list.append(serum_size_3_policy)

    def production_line_addition_1_requirement():
        return True

    def add_production_lines(amount):
        mc.business.production_lines += amount

    production_line_addition_1_policy = Policy(name = "Production Line Expansion 1",
        desc = "Adding a new serum processing area will allow for the production of three serums at once.",
        cost = 800,
        requirement = production_line_addition_1_requirement,
        on_buy_function = add_production_lines,
        extra_arguments = {"amount":1})
    serum_policies_list.append(production_line_addition_1_policy)

    def production_line_addition_2_requirement():
        if production_line_addition_1_policy.is_owned():
            return True
        else:
            return False

    production_line_addition_2_policy = Policy(name = "Production Line Expansion 2",
        desc = "Another serum assembly line will allow for the simultaneous production of four different serum designs at once.",
        cost = 3000,
        requirement = production_line_addition_2_requirement,
        on_buy_function = add_production_lines,
        extra_arguments = {"amount":1},
        dependant_policies = production_line_addition_1_policy)
    serum_policies_list.append(production_line_addition_2_policy)


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
        desc = "A detailed questionnaire focused on sex, fetishes, and kinks produces even more information about an applicants sexaul preferences. It can also be used as a suprisingly accurate predictor of sexual experience. Reveals one more opinion, and sex skills are now displayed on an applicants resume.",
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

    # def recruitment_high_suggest_requirement(): #TODO: Figure out what this means with suggestability. What the hell do we even want suggestability to do right now?
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


    ## Organisation Policies ##
    def increase_max_employee_size(amount):
        mc.business.max_employee_count += amount

    def business_size_1_requirement():
        return True

    business_size_1_policy = Policy(name = "Employee Count Improvement One",
        desc = "Some basic employee management and tracking software will let you hire more employees. Increases max employee count by 2.",
        cost = 500,
        toggleable = False,
        requirement = business_size_1_requirement,
        on_buy_function = increase_max_employee_size,
        extra_arguments = {"amount":2})
    organisation_policies_list.append(business_size_1_policy)

    def business_size_2_requirement():
        if business_size_1_policy.is_owned():
            return True
        else:
            return False

    business_size_2_policy = Policy(name = "Employee Count Improvement Two",
        desc = "Improved employee management software yet again increases the number of employees you can comfortably keep around. Increases max employee count by 3.",
        cost = 2000,
        toggleable = False,
        requirement = business_size_2_requirement,
        on_buy_function = increase_max_employee_size,
        extra_arguments = {"amount":3})
    organisation_policies_list.append(business_size_2_policy)

    def business_size_3_requirement():
        if business_size_2_policy.is_owned():
            return True
        else:
            return False

    business_size_3_policy = Policy(name = "Employee Count Improvement Three",
        desc = "Distributed management roles lets you nearly double the employee count of your business. Increases max employee count by 8.",
        cost = 5000,
        toggleable = False,
        requirement = business_size_3_requirement,
        on_buy_function = increase_max_employee_size,
        extra_arguments = {"amount":8})
    organisation_policies_list.append(business_size_3_policy)

    def business_size_4_requirement():
        if business_size_3_policy.is_owned():
            return True
        else:
            return False

    business_size_4_policy = Policy(name = "Employee Count Improvement Four",
        desc = "Fully automated payroll calculations, benefit management, and productivity tracking allows for a final, massive jump in maximum business size. Increases max employee count by 20.",
        cost = 10000,
        toggleable = False,
        requirement = business_size_4_requirement,
        on_buy_function = increase_max_employee_size,
        extra_arguments = {"amount":20})
    organisation_policies_list.append(business_size_4_policy)

    def public_advertising_license_requirement():
        return True

    public_advertising_license_policy = Policy(name = "Public Advertising License",
        desc = "After filling out the proper paperwork and familiarizing yourself with publishing regultions you will be ready to advertise your product in print publications. Allows you to pick a girl as your company model and launch ad campaigns.",
        cost = 2500,
        toggleable = False,
        requirement = public_advertising_license_requirement)

    organisation_policies_list.append(public_advertising_license_policy)

    def office_punishment_policy_requirement():
        return True

    office_punishment = Policy(name = "Office Punishment",
        desc = "Establish a formal set of punishments for business policy violations. Allows you to punish employees for infractions they have committed. More severe infractions enable more severe punishments.",
        cost = 700,
        toggleable = False,
        requirement = office_punishment_policy_requirement)
    organisation_policies_list.append(office_punishment)

    def corporal_punishment_policy_requirement():
        if office_punishment.is_owned():
            return True
        else:
            return False

    corporal_punishment = Policy(name = "Corporal Punishment",
        desc = "Updates to the company punishment guidelines allow for punishments involving physical contact. Research into the topic has shown sexual punishment to be extremely effective in cases of severe disobedience.",
        cost = 2000,
        toggleable = False,
        requirement = corporal_punishment_policy_requirement)
    organisation_policies_list.append(corporal_punishment)

    def strict_enforcement_policy_requirment():
        if office_punishment.is_owned():
            return True
        else:
            return False

    def strict_enforcement_on_day():
        mc.business.change_team_effectiveness(-1*mc.business.get_employee_count())

    strict_enforcement = Policy(name = "Strict Enforcement",
        desc = "By strictly applying the letter, rather than spirit, of the company punishment guidelines you are able to treat infractions as more severe than they initially seem. All infraction severities are increased by one while this policy is active, but the increased administrative work lowers business efficency by one per employee every day.",
        cost = 2500,
        toggleable = True,
        requirement = strict_enforcement_policy_requirment,
        on_day_function = strict_enforcement_on_day)
    organisation_policies_list.append(strict_enforcement)

    def draconian_enforcement_policy_requirement():
        if strict_enforcement.is_owned():
            return True
        else:
            return False

    def draconian_enforcement_on_day():
        for employee in mc.business.get_employee_list():
            employee.change_happiness(-5)

    draconian_enforcement = Policy(name = "Draconian Enforcement",
        desc = "Each policy infraction is to be punished to the utmost tolerable. All infraction severities are increased by one, but the restrictive office environment affects company morale, lowering all empolyee happiness by -5 per day.",
        cost = 5000,
        toggleable = True,
        requirement = draconian_enforcement_policy_requirement,
        on_day_function = draconian_enforcement_on_day,
        dependant_policies = strict_enforcement)
    organisation_policies_list.append(draconian_enforcement)

    def bureaucratic_nightmare_policy_requirement():
        if office_punishment.is_owned():
            return True
        else:
            return False

    def bureaucratic_nightmare_on_day():
        mc.business.change_team_effectiveness(-1*mc.business.get_employee_count())

    bureaucratic_nightmare = Policy(name = "Bureaucratic Nightmare",
        desc = "Rewriting all company policies to be intentionally vague and misleading creates a work environment where mistakes are practically unavoidable. Allows you to generate minor infractions at will, but the new labyrinthian rules result in business efficency dropping by an additional one per employee each day.",
        cost = 2500,
        toggleable = True,
        requirement = bureaucratic_nightmare_policy_requirement,
        on_day_function = bureaucratic_nightmare_on_day)
    organisation_policies_list.append(bureaucratic_nightmare)
