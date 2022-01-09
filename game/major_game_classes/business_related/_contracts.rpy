init -2 python:
    def generate_contract(contract_tier = 0): #TODO: Have a way to setting the contract tier.

        primary_aspect = renpy.random.choice(["mental","physical","sexual","medical"])

        secondary_list = ["mental","physical","sexual","medical"]
        secondary_list.remove(primary_aspect)
        secondary_aspect = renpy.random.choice(secondary_list)

        contract_name, contract_description = get_contract_description(primary_aspect, secondary_aspect, contract_tier)

        contract_length = 3 + (renpy.random.randint(0,3+contract_tier) * renpy.random.randint(0,3+contract_tier))

        amount_desired = 5*(contract_tier+renpy.random.randint(1,3))*(contract_tier+renpy.random.randint(1,3))

        # 1*2 = 2, 3*4 = 12, 5*6 = 30, 7*8 = 56
        primary_aspect_amount = ((contract_tier+1) * (contract_tier+2)) + renpy.random.randint(-(contract_tier+3), (contract_tier+2))
        secondary_aspect_amount = (primary_aspect_amount/2) + renpy.random.randint(-(contract_tier+1), (contract_tier))

        if primary_aspect_amount < 2:
            primary_aspect_amount = 1
        if secondary_aspect_amount < 1:
            secondary_aspect_amount = 1

        flaw_tolerance = renpy.random.randint(0, (contract_tier+1)*2)
        if flaw_tolerance < 0:
            flaw_tolerance = 0

        attention_tolerance = 1 + contract_tier + renpy.random.randint(-(contract_tier/2),contract_tier)
        if attention_tolerance < 0:
            attention_tolerance = 0

        # if contract_tier == 0 and attention_tolerance == 0:
        #     attention_tolerance = 1 #Raise the floor for tier 0, since we don't have 0 attention variants of some aspects.

        mental_requirement = 0
        physical_requirement = 0
        sexual_requirement = 0
        medical_requirement = 0

        if primary_aspect == "mental":
            mental_requirement = primary_aspect_amount
        elif primary_aspect == "physical":
            physical_requirement = primary_aspect_amount
        elif primary_aspect == "sexual":
            sexual_requirement = primary_aspect_amount
        else:
            medical_requirement = primary_aspect_amount

        if secondary_aspect == "mental":
            mental_requirement = secondary_aspect_amount
        elif secondary_aspect == "physical":
            physical_requirement = secondary_aspect_amount
        elif secondary_aspect == "sexual":
            sexual_requirement = secondary_aspect_amount
        else:
            medical_requirement = secondary_aspect_amount



        new_contract = Contract(contract_name, contract_description, contract_length,
            mental_requirement = mental_requirement, physical_requirement = physical_requirement, sexual_requirement = sexual_requirement, medical_requirement = medical_requirement,
            flaw_tolerance = flaw_tolerance, attention_tolerance = attention_tolerance, amount_desired = amount_desired)

        return new_contract

    def get_contract_description(primary_aspect, secondary_aspect, contract_tier):
        contract_name = ""
        contract_description = ""
        if primary_aspect == "mental":
            if secondary_aspect == "physical":
                contract_name = "Eltaro Co. Employee Boosters"
                contract_description = "Eltaro Co. is looking for a way to improve the general productivity of their employees by sharpening both body and mind."

            elif secondary_aspect == "sexual":
                contract_name = "Iris Cosmetics Makeup Additive"
                contract_description = "Having a beautiful mind is just as important as clear skin or perfect makeup. Iris cosmetics is looking for something to promote that feeling in their customers, and a little sex appeal always helps sell products."

            elif secondary_aspect == "medical":
                contract_name = "Tresmon Pharmaceuticals Neuotropics"
                contract_description = "Tresmon Pharmaceuticals has a number of clients interested in thought-boosting drugs, and they're willing to pay top dollar for you to fill those orders for them."

        elif primary_aspect == "physical":
            if secondary_aspect == "mental":
                contract_name = "Univerity Athletics Council Request"
                contract_description = "The university athletics council is looking for a way to improve the performance of their key athletes, on and off the field."

            elif secondary_aspect == "sexual":
                contract_name = "Univerity Cheerleading Council Request"
                contract_description = "Attendance at recent sporting events has been down, and many are blaming the new \"respectful\" cheerleading uniforms. Cheer leadership is looking for a new workout enhancer, ideally one that will reduce resistance to a return to the old uniform."

            elif secondary_aspect == "medical":
                contract_name = "Gary's Power Lifting Additive"
                contract_description = "Gary runs a local gym, and he's always on the look out for another performance enhancing drug to peddle to those looking for a quick path to fitness."

        elif primary_aspect == "sexual":
            if secondary_aspect == "mental":
                contract_name = "Personal Business Supplies"
                contract_description = "A C-suite executive of a nearby business has a secretary they want to turn into a, quote, \"Cock drunk bimbo-slut\", and they're willing to pay good money for a large stock of serum to make it happen."

            elif secondary_aspect == "physical":
                contract_name = strip_club.name
                contract_description = strip_club_owner + " is interested in anything that will give his girls more sex appeal while they're stripping on stage. Bigger tits, toned bodies, whatever you think they need to get more twenties on the stage."

            elif secondary_aspect == "medical":
                contract_name = "A Questionable Contact"
                contract_description = "An individual using an obviously fake name has requested \"Anything that gets 'em horny, wet, and ready to suck dick.\". Their name might be fake, but their cash definitely isn't."

        elif primary_aspect == "medical":
            if secondary_aspect == "mental":
                contract_name = "Tresmon Pharmaceuticals Research Materials"
                contract_description = "Tresmon Pharmaceuticals is intensely interested in our work on mind altering substances. They want a stock of their own to perform advanced R&D with."

            elif secondary_aspect == "physical":
                contract_name = "Military Research Study"
                contract_description = "The military is interested in potential \"super soldier\" applications, and they're willing to work with civilian sources to obtain research material."

            elif secondary_aspect == "sexual":
                contract_name = "Female Libedo Enhancements"
                contract_description = "Low libedo is a side effect for many different medications. Tresmon Pharmaceuticals is interested in an additive that might lessen or eliminate that problem from their existing drugs."

        return contract_name, contract_description
