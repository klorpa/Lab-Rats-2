init 0 python:
    #### SERUM TESTING POLICY SECTION ####
    serum_policies_list = []

    mandatory_paid_serum_testing_policy = Policy(name = "Mandatory Paid Serum Testing",
        desc = "Employees will be required to take doses of serum when requested for \"testing purposes\". They will be entitled to compensation equal to five days wages.",
        cost = 500,
        toggleable = True)
    serum_policies_list.append(mandatory_paid_serum_testing_policy)

    mandatory_unpaid_serum_testing_policy = Policy(name = "Mandatory Unpaid Serum Testing",
        desc = "Updates to your employe contracts will remove the requirement for compensation when they are asked to test serums.",
        cost = 2000,
        toggleable = True,
        own_requirement = mandatory_paid_serum_testing_policy,
        dependant_policies = mandatory_paid_serum_testing_policy)
    serum_policies_list.append(mandatory_unpaid_serum_testing_policy)

    daily_serum_dosage_policy = Policy(name = "Daily Serum Dosage",
        desc = "Mandatory serum testing is expanded into a full scale daily dosage program. Each employee will receive a dose of the selected serum for their department, if one is currently in the stockpile.",
        cost = 5000,
        toggleable = True,
        own_requirement = mandatory_unpaid_serum_testing_policy,
        dependant_policies = mandatory_unpaid_serum_testing_policy)
    serum_policies_list.append(daily_serum_dosage_policy)

    def batch_size_increase(increase_amount = 0):
        mc.business.batch_size += increase_amount

    serum_size_1_policy = Policy(name = "Batch Size Improvement 1",
        desc = "Updating the equipment throughout the lab allows for increased batch sizes of serum as well as improved supply efficiency. Increases serum batch size by 1.",
        cost = 500,
        toggleable = True,
        on_buy_function = batch_size_increase,
        extra_arguments = {"increase_amount":1})
    serum_policies_list.append(serum_size_1_policy)


    serum_size_2_policy = Policy(name = "Batch Size Improvement 2",
        desc = "Improved recycling of waste materials allows for a boost in production efficiency. Increases serum batch size by 2.",
        cost = 2500,
        toggleable = True,
        own_requirement = serum_size_1_policy,
        on_buy_function = batch_size_increase,
        extra_arguments = {"increase_amount":2},
        dependant_policies = serum_size_1_policy)
    serum_policies_list.append(serum_size_2_policy)

    serum_size_3_policy = Policy(name = "Batch Size Improvement 3",
        desc = "Another improvement to the lab equipment allows for even more impressive boosts in production efficiency and speed. Increases serum batch size by 2.",
        cost = 10000,
        toggleable = True,
        own_requirement = serum_size_2_policy,
        on_buy_function = batch_size_increase,
        extra_arguments = {"increase_amount":2},
        dependant_policies = serum_size_2_policy)
    serum_policies_list.append(serum_size_3_policy)

    def serum_production_improvement(increase_amount = 1, operating_cost_increase = 0):
        mc.business.max_serum_tier += increase_amount
        mc.business.operating_costs += operating_cost_increase

    serum_production_1_policy = Policy(name = "Tier 1 Serum Production",
        desc = "You will need more complex machinery to produce advanced serum designs, but those machines aren't cheap, and they add significant overhead to your business. Allows you to produce tier 1 serum designs, but costs an additional $50 per day in oprating costs.",
        cost = 750,
        toggleable = False,
        on_buy_function = serum_production_improvement,
        extra_arguments = {"operating_cost_increase":50})
    serum_policies_list.append(serum_production_1_policy)

    serum_production_2_policy = Policy(name = "Tier 2 Serum Production",
        desc = "Equipping your production lines with state-of-the-art machinery is necessary to produce tier 2 serum designs. Maintenence and licensing fees will cost an additional $200 per work day.",
        cost = 5000,
        toggleable = False,
        own_requirement = serum_production_1_policy,
        on_buy_function = serum_production_improvement,
        extra_arguments = {"operating_cost_increase":200})
    serum_policies_list.append(serum_production_2_policy)

    serum_production_3_policy = Policy(name = "Tier 3 Serum Production",
        desc = "Installing protoype machinery in your production lines will allow you to produce tier 3 serum designs. Maintenence and licensing fees will cost an additional $500 per work day.",
        cost = 10000,
        toggleable = False,
        own_requirement = serum_production_2_policy,
        on_buy_function = serum_production_improvement,
        extra_arguments = {"operating_cost_increase":500})
    serum_policies_list.append(serum_production_3_policy)

    def production_line_addition_1_requirement():
        return True

    def add_production_lines(amount):
        for x in range(0,amount):
            mc.business.production_lines.append(ProductionLine(mc.business.inventory))

    production_line_addition_1_policy = Policy(name = "Production Line Expansion 1",
        desc = "Adding a new serum processing area will allow for the production of three serums at once.",
        cost = 800,
        on_buy_function = add_production_lines,
        extra_arguments = {"amount":1})
    serum_policies_list.append(production_line_addition_1_policy)

    production_line_addition_2_policy = Policy(name = "Production Line Expansion 2",
        desc = "Another serum assembly line will allow for the simultaneous production of four different serum designs at once.",
        cost = 3000,
        own_requirement = production_line_addition_1_policy,
        on_buy_function = add_production_lines,
        extra_arguments = {"amount":1},
        dependant_policies = production_line_addition_1_policy)
    serum_policies_list.append(production_line_addition_2_policy)
