screen serum_sell_ui():
    add "Science_Menu_Background.png"
    #use serum_tooltip
    modal True
    hbox:
        spacing 40
        xalign 0.05
        yalign 0.05
        frame:
            background "#888888"
            xsize 700 ysize 800
            vbox:
                hbox:
                    xsize 700
                    text "Serum In Stock" style "menu_text_style" size 20 xalign 0.0
                    text "Sell Serum" style "menu_text_style" size 20 xalign 0.9 xanchor 1.0
                viewport:
                    mousewheel True
                    scrollbars "vertical"
                    vbox:
                        for serum_stock in mc.business.inventory.serums_held:
                            $ the_serum = serum_stock[0]
                            $ serum_amount = serum_stock[1]
                            hbox:
                                $ serum_dose_value = mc.business.get_serum_base_value(the_serum, round_value = True)
                                use serum_design_menu_item(the_serum, given_y_size = 60, name_addition = ": " + str(serum_amount) + " Doses, $" + str(serum_dose_value) + "/Dose")
                                textbutton "-1":
                                    ysize 60
                                    xsize 80
                                    text_yalign 0.5
                                    text_yanchor 0.5
                                    action Function(mc.business.sell_serum, the_serum)
                                    style "textbutton_style" text_style "textbutton_text_style"
                                    sensitive serum_amount >= 1
                                textbutton "-10":
                                    ysize 60
                                    xsize 80
                                    text_yalign 0.5
                                    text_yanchor 0.5
                                    action Function(mc.business.sell_serum, the_serum, serum_count = 10)
                                    style "textbutton_style" text_style "textbutton_text_style"
                                    sensitive serum_amount >= 10


            #TODO: This holds the current serem selections


        vbox:
            spacing 40
            frame:
                background "#888888"
                xsize 800 ysize 200
                #TODO: Holds current information about aspect price, attention, market reach
                vbox:
                    hbox:
                        textbutton "Market Reach:":
                            action VrenNullAction style "textbutton_style" text_style "textbutton_text_style"
                            tooltip "How many people have heard about your business. The larger your market reach the more each serum aspect point is worth."

                        text str(mc.business.market_reach) + " People" style "textbutton_text_style" yanchor -0.5

                        null width 50

                        text "Current Funds: {color=#98fb98}$" + str(mc.business.funds) + "{/color}" style "textbutton_text_style" yanchor -0.5

                    hbox:
                        textbutton "Attention:":
                             action VrenNullAction style "textbutton_style" text_style "textbutton_text_style"
                             tooltip "How much attention your business has drawn. If this gets too they will act, outlawing a serum design, leveling a fine, or seizing your inventory."


                        text str(mc.business.attention) + "/" + str(mc.business.max_attention) + " (-" + str(mc.business.attention_bleed) + "/Day)" style "textbutton_text_style" yanchor -0.5

                    text "Aspect Data" style "menu_text_style"
                    grid 6 3:
                        null

                        text "Mental" style "menu_text_style" color "#0049d8"
                        text "Physical" style "menu_text_style" color "#00AA00"
                        text "Sexual" style "menu_text_style" color "#FFC0CB"
                        text "Medical" style "menu_text_style" color "#FFFFFF"
                        text "Flaws" style "menu_text_style" color "#BBBBBB"

                        text ("Aspect Values") style "menu_text_style"
                        text "$" + str("%.2f" % mc.business.get_aspect_price("Mental")) style "menu_text_style"
                        text "$" + str("%.2f" % mc.business.get_aspect_price("Physical")) style "menu_text_style"
                        text "$" + str("%.2f" % mc.business.get_aspect_price("Sexual")) style "menu_text_style"
                        text "$" + str("%.2f" % mc.business.get_aspect_price("Medical")) style "menu_text_style"
                        text "-$" + str("%.2f" % -mc.business.get_aspect_price("Flaw")) style "menu_text_style"

                        text ("Aspect Desire") style "menu_text_style"
                        text str("%.0f" % (200*mc.business.get_aspect_percent("Mental"))) + "%" style "menu_text_style"
                        text str("%.0f" % (200*mc.business.get_aspect_percent("Physical"))) + "%" style "menu_text_style"
                        text str("%.0f" % (200*mc.business.get_aspect_percent("Sexual"))) + "%" style "menu_text_style"
                        text str("%.0f" % (200*mc.business.get_aspect_percent("Medical"))) + "%" style "menu_text_style"
                        text str("-%.0f" % (200*mc.business.get_aspect_percent("Flaw"))) + "%" style "menu_text_style"

            frame:
                background "#888888"
                xsize 800 ysize 500
                vbox:
                    ysize 400
                    text "Active Contracts (" + str(len(mc.business.active_contracts)) + "/" + str(mc.business.max_active_contracts) + " Max)" style "menu_text_style"
                    viewport:
                        mousewheel True
                        scrollbars "vertical"
                        vbox:
                            spacing 20
                            xsize 800
                            for contract in mc.business.active_contracts:
                                use contract_select_button(contract):
                                    textbutton "Add Serum":
                                        xanchor 1.0
                                        xalign 0.90
                                        style "textbutton_style"
                                        text_style "textbutton_text_style"
                                        action Show("serum_trade_ui", None, mc.business.inventory, contract.inventory, name_1 = "Stockpile", name_2 = contract.name, trade_requirement = contract.check_serum, hide_instead = True, inventory_2_max = contract.amount_desired)

                                    textbutton "Abandon": #TODO: This should probably require a double click or something.
                                        xanchor 1.0
                                        xalign 0.90
                                        style "textbutton_style"
                                        text_style "textbutton_text_style"
                                        action Function(mc.business.abandon_contract, contract)

                                    textbutton "Complete":
                                        xanchor 1.0
                                        xalign 0.90
                                        style "textbutton_style"
                                        text_style "textbutton_text_style"
                                        action Function(mc.business.complete_contract, contract)
                                        sensitive contract.can_finish_contract()


                textbutton "New Contracts: " + str(len(mc.business.offered_contracts)) + " Available":
                    style "textbutton_style"
                    text_style "textbutton_text_style"
                    yanchor 1.0
                    yalign 1.0
                    xalign 0.5
                    ysize 40
                    action Show("contract_select")


                #TODO: Holds information about current contracts and lets you transfer serum into and out of them


    frame:
        background None
        anchor [0.5,0.5]
        align [0.5,0.88]
        xysize [500,125]
        imagebutton:
            align [0.5,0.5]
            auto "gui/button/choice_%s_background.png"
            focus_mask "gui/button/choice_idle_background.png"
            action Return()
        textbutton "Return" align [0.5,0.5] style "return_button_style" text_style "return_button_style"
