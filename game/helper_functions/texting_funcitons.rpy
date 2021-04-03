init -1 python:
    def text_message_history_callback(history_entry): #Manages taking the history entry and slotting it into the appropriate list
        if hasattr(store,"mc"): #Make sure the main character has been instantiated
            if mc.having_text_conversation: #This is set to a Person when talking via text, to allow us to log the interation correctly.
                if history_entry.who is not None and not mc.text_conversation_paused: #Record the dialogue, we'll figure out in the history display section if it's messages from us or a Person.
                    mc.phone.add_message(mc.having_text_conversation, history_entry)
                else:
                    pass #Nothing to do. We don't record narration.

    def text_message_say_callback(who, *args, **kwargs): #Manually sets the style of anything sent as part of a text conversation #NOTE: No longer used or hooked up once the proper phone UI was added
        if hasattr(store,"mc"):
            if mc.having_text_conversation:
                kwargs["what_color"] = "#19e9f7" #We need to define these explicitly so they are not overridden by the characters defaults.
                kwargs["what_font"] = "fonts/Autobusbold-1ynL.ttf"
        return args, kwargs
