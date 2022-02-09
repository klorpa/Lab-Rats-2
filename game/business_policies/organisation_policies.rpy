init 0 python:
    ## Organisation Policies ##

    organisation_policies_list = []

    def increase_max_employee_size(amount):
        mc.business.max_employee_count += amount

    business_size_1_policy = Policy(name = "Employee Count Improvement One",
        desc = "Some basic employee management and tracking software will let you hire more employees. Increases max employee count by 2.",
        cost = 500,
        toggleable = False,
        on_buy_function = increase_max_employee_size,
        extra_arguments = {"amount":2})
    organisation_policies_list.append(business_size_1_policy)
    
    business_size_2_policy = Policy(name = "Employee Count Improvement Two",
        desc = "Improved employee management software yet again increases the number of employees you can comfortably keep around. Increases max employee count by 3.",
        cost = 2000,
        toggleable = False,
        own_requirement = business_size_1_policy,
        on_buy_function = increase_max_employee_size,
        extra_arguments = {"amount":3})
    organisation_policies_list.append(business_size_2_policy)

    business_size_3_policy = Policy(name = "Employee Count Improvement Three",
        desc = "Distributed management roles lets you nearly double the employee count of your business. Increases max employee count by 8.",
        cost = 5000,
        toggleable = False,
        own_requirement = business_size_2_policy,
        on_buy_function = increase_max_employee_size,
        extra_arguments = {"amount":8})
    organisation_policies_list.append(business_size_3_policy)

    business_size_4_policy = Policy(name = "Employee Count Improvement Four",
        desc = "Fully automated payroll calculations, benefit management, and productivity tracking allows for a final, massive jump in maximum business size. Increases max employee count by 20.",
        cost = 10000,
        toggleable = False,
        own_requirement = business_size_3_policy,
        on_buy_function = increase_max_employee_size,
        extra_arguments = {"amount":20})
    organisation_policies_list.append(business_size_4_policy)

    def business_contract_increase(change_amount = 1):
        mc.business.max_active_contracts += change_amount

    def business_contract_offered_increase(change_amount = 1):
        mc.business.max_offered_contracts += change_amount

    def business_contract_increase_1_on_turn():
        mc.business.change_team_effectiveness(-len(mc.business.active_contracts))

    business_contract_increase_1_policy = Policy(name = "Streamlined Contract Processing.",
        desc = "Managing multiple contracts at once is difficult, but the extra payout offered makes the trouble worth it. Allows you to have one additional active contract at a time, but reduces business efficiency by 1 per turn per active contract.",
        cost = 500,
        toggleable = False,
        on_buy_function = business_contract_increase,
        on_turn_function = business_contract_increase_1_on_turn)
    organisation_policies_list.append(business_contract_increase_1_policy)

    business_contract_offer_increase_1_policy = Policy(name = "Favoured Business Partnerships",
        desc = "Forging strong relationships with repeat customers makes it more likely they'll turn to you when they have special requests. Increases the number of contracts offered every Monday by 1.",
        cost = 1000,
        toggleable = False,
        own_requirement = business_contract_increase_1_policy,
        on_buy_function = business_contract_offered_increase)
    organisation_policies_list.append(business_contract_offer_increase_1_policy)

    business_contract_increase_2_policy = Policy(name = "Multi-Contract Business Strategy.",
        desc = "Focus your business on managing multiple contract at once. Increases the maximum number of active contracts by 1, but reduces business efficiency by 1 per turn per active contract.",
        cost = 3000,
        toggleable = False,
        own_requirement = business_contract_offer_increase_1_policy,
        on_buy_function = business_contract_increase,
        on_turn_function = business_contract_increase_1_on_turn)
    organisation_policies_list.append(business_contract_increase_2_policy)

    business_contract_offer_increase_2_policy = Policy(name = "Public Relationship Management",
        desc = "Further reinforce your relationship with common business partners, encouraging them to present you with contracts first and often. Increases the number of contracts offered every Monday by 1.",
        cost = 5000,
        toggleable = False,
        own_requirement = business_contract_offer_increase_1_policy,
        on_buy_function = business_contract_offered_increase)
    organisation_policies_list.append(business_contract_offer_increase_2_policy)

    public_advertising_license_policy = Policy(name = "Public Advertising License",
        desc = "After filling out the proper paperwork and familiarizing yourself with publishing regultions you will be ready to advertise your product in print publications. Allows you to pick a girl as your company model and launch ad campaigns.",
        cost = 2500,
        toggleable = False)

    organisation_policies_list.append(public_advertising_license_policy)

    office_punishment = Policy(name = "Office Punishment",
        desc = "Establish a formal set of punishments for business policy violations. Allows you to punish employees for infractions they have committed. More severe infractions enable more severe punishments.",
        cost = 700,
        toggleable = False)
    organisation_policies_list.append(office_punishment)


    corporal_punishment = Policy(name = "Corporal Punishment",
        desc = "Updates to the company punishment guidelines allow for punishments involving physical contact. Research into the topic has shown sexual punishment to be extremely effective in cases of severe disobedience.",
        cost = 2000,
        toggleable = False,
        own_requirement = office_punishment)
    organisation_policies_list.append(corporal_punishment)

    def strict_enforcement_on_day():
        mc.business.change_team_effectiveness(-1*mc.business.get_employee_count())

    strict_enforcement = Policy(name = "Strict Enforcement",
        desc = "By strictly applying the letter, rather than spirit, of the company punishment guidelines you are able to treat infractions as more severe than they initially seem. All infraction severities are increased by one while this policy is active, but the increased administrative work lowers business efficiency by one per employee every day.",
        cost = 2500,
        toggleable = True,
        own_requirement = office_punishment,
        on_day_function = strict_enforcement_on_day)
    organisation_policies_list.append(strict_enforcement)

    def draconian_enforcement_on_day():
        for employee in mc.business.get_employee_list():
            employee.change_happiness(-5)

    draconian_enforcement = Policy(name = "Draconian Enforcement",
        desc = "Each policy infraction is to be punished to the utmost tolerable. All infraction severities are increased by one, but the restrictive office environment affects company morale, lowering all empolyee happiness by -5 per day.",
        cost = 5000,
        toggleable = True,
        own_requirement = strict_enforcement,
        on_day_function = draconian_enforcement_on_day,
        dependant_policies = strict_enforcement)
    organisation_policies_list.append(draconian_enforcement)

    def bureaucratic_nightmare_on_day():
        mc.business.change_team_effectiveness(-1*mc.business.get_employee_count())

    bureaucratic_nightmare = Policy(name = "Bureaucratic Nightmare",
        desc = "Rewriting all company policies to be intentionally vague and misleading creates a work environment where mistakes are practically unavoidable. Allows you to generate minor infractions at will, but the new labyrinthian rules result in business efficiency dropping by an additional one per employee each day.",
        cost = 2500,
        toggleable = True,
        own_requirement = office_punishment,
        on_day_function = bureaucratic_nightmare_on_day)
    organisation_policies_list.append(bureaucratic_nightmare)

    theoretical_research = Policy(name = "Theoretical Research",
        desc = "Establish a framework that will allow your R&D team to contribute to the discovery of completely novel serum traits. When not given a specific task your research team will convert 5% of their generated Research Points into Clarity.",
        cost = 300,
        toggleable = False)
    organisation_policies_list.append(theoretical_research)

    def research_journal_subscription_on_day():
        if mc.business.is_work_day():
            mc.business.change_funds(-30)

    research_journal_subscription = Policy(name = "Research Journal Subscription",
        desc = "Ensuring your research team has access to all of the latest research isn't cheap, but it is important if you want to push your own progress further and faster. Converts an additional 5% of idle Research Points into Clarity when your R&D team is idle. Costs $30 a day to maintain your subscription.",
        cost = 1000,
        toggleable = False,
        own_requirement = theoretical_research,
        on_day_function = research_journal_subscription_on_day)
    organisation_policies_list.append(research_journal_subscription)

    independent_experimentation = Policy(name = "Independent Experimentation",
        desc = "Make the lab available to your research staff and encourage them to pursue their own experiments when it would otherwise be idle. Requires 5 serum supply per researcher and converts an additional 5% of idle research production into Clarity.",
        cost = 500,
        toggleable = True,
        own_requirement = theoretical_research)
    organisation_policies_list.append(independent_experimentation)


    def office_conduct_guidelines_on_day():
        if mc.business.is_work_day():
            for an_employee in mc.business.get_employee_list():
                if an_employee.sluttiness < 20:
                    an_employee.change_slut(1, 20, add_to_log = False)
                    mc.business.change_team_effectiveness(-1)

    office_conduct_guidelines = Policy(name = "Office Conduct Guidelines",
        desc = "Set and distribute guidelines for staff behaviour. Daily emails will remind them to be \"pleasant, open, and receptive to all things.\". Increases all staff Sluttiness by 1 per day, to a maximum of 20. Reduces business effiency by 1 per employee affected.",
        cost = 700,
        toggleable = True,
        on_day_function = office_conduct_guidelines_on_day)
    organisation_policies_list.append(office_conduct_guidelines)

    def mandatory_staff_reading_on_day():
        if mc.business.is_work_day():
            for an_employee in mc.business.get_employee_list():
                if an_employee.sluttiness <= 20:
                    an_employee.change_happiness(-5, add_to_log = False)

                if an_employee.sluttiness < 40:
                    an_employee.change_slut(1, 40, add_to_log = False)
                    mc.business.change_team_effectiveness(-1)

    mandatory_staff_reading = Policy(name = "Mandatory Staff Reading",
        desc = "Distribute copies of \"Your Place in the Work Place\" - a guidebook for women, written in the 60's by a womanizing executive. Increases all staff Sluttiness by an additional 1 per day, to a maximum of 40. Reduces business efficiency by 1 per employee affected, and reduces happiness of women with Sluttiness 20 or lower by 5 per day.",
        cost = 1500,
        toggleable = True,
        active_requirement = office_conduct_guidelines,
        on_day_function = mandatory_staff_reading_on_day,
        dependant_policies = office_conduct_guidelines)
    organisation_policies_list.append(mandatory_staff_reading)

    def superliminal_office_messaging_on_day():
        if mc.business.is_work_day():
            for an_employee in mc.business.get_employee_list():
                if an_employee.sluttiness <= 20:
                    an_employee.change_happiness(-10)
                    mc.business.change_team_effectiveness(-3)
                elif an_employee.sluttiness < 60:
                    mc.business.change_team_effectiveness(-1)
                an_employee.change_slut(1, 60, add_to_log = False)

    superliminal_office_messaging = Policy(name = "Superliminal Messaging",
        desc = "Fill the office with overtly sexual content. Distribute pinup girl calendars, provide access to a company porn account, hang nude posters. Increases staff Sluttiness by 1 per day, to a maximum of 60. Reduces business efficiency by 1 per girl affected, or by 3 if her Sluttiness is 20 or lower. Reduces happiness of women with Sluttiness 20 or lower by 10 per day.",
        cost = 7500,
        toggleable = True,
        active_requirement = mandatory_staff_reading,
        on_day_function = superliminal_office_messaging_on_day,
        dependant_policies = mandatory_staff_reading)
    organisation_policies_list.append(superliminal_office_messaging)

    def max_attention_increase(amount = 100):
        mc.business.max_attention += amount


    max_attention_increase_1_policy = Policy(name = "National Sales",
        desc = "Begin working with clients all over the country. The local authorities are less likely to take an interest in you if your product doesn't always end up in their back yard. Increase the attention threshold by 100.",
        cost = 2000,
        toggleable = False,
        on_buy_function = max_attention_increase)
    organisation_policies_list.append(max_attention_increase_1_policy)

    def attention_bleed_increase(amount = 10):
        mc.business.attention_bleed += amount

    attention_bleed_increase_1_policy = Policy(name = "Public Charity Work",
        desc = "Sponsor a few local charities to improve the public perception of your business. Reduces pressure for authorities to tkae action against you, lowering Attention by an additional 10 per day.",
        cost = 2000,
        toggleable = False,
        on_buy_function = attention_bleed_increase)
    organisation_policies_list.append(attention_bleed_increase_1_policy)

    attention_bleed_increase_2_policy = Policy(name = "City Hall Internal Sabotage",
        desc = "Reports go missing, meetings are misscheduled, and evidence is misfiled. An inside agent down at city hall is making sure it's particularly hard to pin anything on your business. Lowers Attention by an additional 10 per day.",
        cost = 0,
        toggleable = False,
        on_buy_function = attention_bleed_increase) #Only accessable by corrupting the city rep.

    attention_floor_increase_1_policy = Policy(name = "Establish Cover Story",
        desc = "Establish a cover story for your business. This will reduce the amount of attention generated when selling a dose of serum by 1.",
        cost = 2000,
        toggleable = True)
    organisation_policies_list.append(attention_floor_increase_1_policy)

    attention_floor_increase_2_policy = Policy(name = "Business License",
        desc = "Having the proper licenses and paperwork makes it much easier to sell product without attracting undo attention. Reduces the amount of attention generated when selling a dose of serum by another 1.",
        cost = 2500,
        toggleable = False) #Only accessable by corrupting the city rep
