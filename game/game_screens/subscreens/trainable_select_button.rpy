screen trainable_select_button(the_trainable, the_person):
    #TODO: Include the ability to show disabled slugs so the player knows how to unlock certain options.
    textbutton the_trainable.get_full_name(the_person):
        style "textbutton_style"
        xfill True
        text_style "textbutton_text_style"
        text_text_align 0.0
        text_size 16
        sensitive the_trainable.is_unlocked(the_person)
        action Return(the_trainable)
