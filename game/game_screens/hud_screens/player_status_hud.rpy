label check_inventory_loop:
    call screen show_serum_inventory(mc.inventory)
    return

screen main_ui(): #The UI that shows most of the important information to the screen.
    frame:
        background "Info_Frame_1.png"
        xsize 600
        ysize 400
        yalign 0.0
        vbox:
            $ month_count = int(day/30)
            $ day_count = day%30
            spacing -5

            text day_names[day%7] + " - " + time_names[time_of_day] + " (month " + str(month_count) + " day " + str(day_count) + ")" style "menu_text_style" size 18
            textbutton "Outfit Manager" action Call("outfit_master_manager",from_current=True) style "textbutton_style" text_style "textbutton_text_style" xsize 220 tooltip "Design outfits to set as uniforms or give to suggest to women."
            textbutton "Check Inventory" action ui.callsinnewcontext("check_inventory_loop") style "textbutton_style" text_style "textbutton_text_style" xsize 220 tooltip "Check what serums you are currently carrying."
            if mc.stat_goal.completed or mc.work_goal.completed or mc.sex_goal.completed:
                textbutton "Character Sheet" action Show("mc_character_sheet") style "textbutton_style" text_style "textbutton_text_style" xsize 220 background "#44BB44" insensitive_background "#222222" hover_background "#aaaaaa" tooltip "Check your stats, skills, and goals."
            else:
                textbutton "Character Sheet" action Show("mc_character_sheet") style "textbutton_style" text_style "textbutton_text_style" xsize 220 tooltip "Check your stats, skills, and goals."

            $ disp_arousal = int(mc.arousal)
            $ disp_max_arousal = int(mc.max_arousal)
            textbutton "Arousal: " + str(disp_arousal) + "/" + str(disp_max_arousal) + " {image=gui/extra_images/arousal_token.png}":
                ysize 28
                text_style "menu_text_style"
                tooltip "Your personal arousal. When you reach your limit you will may cum, releasing Locked Clarity and allowing you to spend it."
                action NullAction()
                sensitive True

            $ disp_energy = int(mc.energy)
            $ disp_max_energy = int(mc.max_energy)
            textbutton "Energy: " + str(disp_energy) + "/" + str(disp_max_energy) + " {image=gui/extra_images/energy_token.png}":
                ysize 28
                text_style "menu_text_style"
                tooltip "Many actions require energy to perform, sex especially. Energy comes back slowly throughout the day, and most of it is recovered after a good nights sleep."
                action NullAction()
                sensitive True

            $ disp_free_clarity = int(mc.free_clarity)
            $ disp_locked_clarity = int(mc.locked_clarity)
            textbutton "Clarity: " + str(disp_free_clarity) + " (" + str(disp_locked_clarity) + " Locked)": #TODO: Add a clarity token
                ysize 28
                text_style "menu_text_style"
                tooltip "Clarity is generated any time you are aroused, but must be released by climaxing before it can be spent. It can be used to unlock new serum traits for research or to create new serum designs."
                action NullAction()
                sensitive True
