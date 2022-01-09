screen contract_select_button(the_contract):
    frame:
        background "#444444"
        xsize 800
        hbox:
            ysize 140
            vbox:
                xsize 580
                $ contract_name = the_contract.name
                if the_contract.contract_started:
                    $ contract_name += " (" + str(the_contract.get_current_serum_count()) + "/"+str(the_contract.amount_desired) + ") Doses"
                else:
                    $ contract_name += " (" + str(the_contract.amount_desired) + " doses requested"
                text the_contract.name:
                    style "textbutton_text_style"
                    size 20

                use contract_aspect_grid(the_contract)

                text the_contract.description style "textbutton_text_style" size 12 text_align 0.0


            vbox:
                yfill False
                xanchor 1.00
                xalign 0.95
                xsize 195
                transclude #Place things on the right side of this entry for things like accessing the inventory.
