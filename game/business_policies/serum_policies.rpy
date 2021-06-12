init 0 python:
    #### SERUM TESTING POLICY SECTION ####
    serum_policies_list = []

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
        desc = "Mandatory serum testing is expanded into a full scale daily dosage program. Each employee will receive a dose of the selected serum for their department, if one is currently in the stockpile.",
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
        desc = "Improved recycling of waste materials allows for a boost in production efficiency. Increases serum batch size by 2.",
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
        desc = "Another improvement to the lab equipment allows for even more impressive boosts in production efficiency and speed. Increases serum batch size by 2.",
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
