init -2 python:
    class Clothing_Images(renpy.store.object): # Stores a set of images for a single piece of clothing in a single position. The position is stored when it is put into the clothing object dict.
        def __init__(self,clothing_name,position_name,is_top, body_dependant = True):

            self.images = {}
            self.clothing_name = clothing_name #Used for some debugging, not needed for the actual game logic.
            self.position_name = position_name #Used so we can access the correct .zip file
            if body_dependant:
                self.body_types = ["standard_body","thin_body","curvy_body","standard_preg_body"]
            else:
                self.body_types = ["standard_body"]

            self.breast_sizes = ["AA","A","B","C","D","DD","DDD","E","F","FF"]

            for body in self.body_types:
                if is_top:
                    for breast in self.breast_sizes:
                        if clothing_name is None:
                            self.images [body + "_" + breast] = "empty_holder.png" #Placeholder for clothing items that exist but don't get drawn for some reason (or that don't have image sets yet).
                        else:
                            self.images [body + "_" + breast] = clothing_name+"_"+position_name+"_"+body+"_"+breast+".png"
                else:
                    if clothing_name is None:
                        self.images [body + "_AA"] = "empty_holder.png"
                    else:
                        self.images[body + "_AA"] = clothing_name+"_"+position_name+"_"+body+"_AA.png"

        def get_image(self, body_type, breast_size = "AA" ): #Generates a proper Image object from the file path strings we have stored previously. Prevents object bloat by storing large objects repeatedly for everyone.
            index_string = body_type + "_" + breast_size
            return_image = VrenZipImage(self.position_name, self.images[index_string])

            if return_image:
                return return_image
            else:
                return

        def get_image_name(self, body_type, breast_size = "AA" ): #Generates a proper Image object from the file path strings we have stored previously. Prevents object bloat by storing large objects repeatedly for everyone.
            index_string = body_type + "_" + breast_size
            return self.images[index_string]

    class Facial_Accessory_Images(renpy.store.object):
        def __init__(self,accessory_name,position):
            self.images = {}
            self.position_name = position
            self.supported_faces = ["Face_1","Face_2","Face_3","Face_4","Face_5","Face_6","Face_7","Face_8","Face_9","Face_11","Face_12","Face_13","Face_14"]
            self.supported_emotions = ["default","sad","happy","angry","orgasm"]
            self.special_modifiers = {self.position_name:"blowjob","kissing":"kissing"} #As of v0.35 all positions support the blowjob modifier so we can have good looking gags and a wider variety of facial expressions.

            for face in self.supported_faces:
                for emotion in self.supported_emotions:
                    #Add the image string to the dict. We do not use Image obects directly because it greatly slows down the game (character objects become huge.)
                    self.images[face + "_" + emotion] = accessory_name + "_" + position + "_" + face + "_" + emotion + ".png" # Save the file string so we can generate a proper image from it easily later.
                    if position in self.special_modifiers:
                        self.images[face + "_" + emotion + "_" + self.special_modifiers[position]] = accessory_name + "_" + position + "_" + face + "_" + emotion + "_" + self.special_modifiers[position] + ".png"
                        #There is a special modifier, we need to add that version as well.

        def get_image(self, face, emotion, special_modifier = None):
            index_string = face + "_" + emotion
            global mobile_zip_dict
            file = mobile_zip_dict[self.position_name]
            if special_modifier is not None:
                if index_string+"_"+special_modifier in file.namelist():
                    index_string += "_" + special_modifier #We only want to try and load special modifier images if they exist. Otherwise we use the unmodified image to avoid a crash. This lets us omit images we do not plan on actually using, such as glasses not needing blowjob poses.

            the_image = VrenZipImage(self.position_name, self.images[index_string])
            return the_image
        def get_image_name(self, face, emotion, special_modifier = None):
            index_string = face + "_" + emotion
            global mobile_zip_dict
            file = mobile_zip_dict[self.position_name]
            if special_modifier is not None:
                if index_string+"_"+special_modifier in file.namelist():
                    index_string += "_" + special_modifier #We only want to try and load special modifier images if they exist. Otherwise we use the unmodified image to avoid a crash. This lets us omit images we do not plan on actually using, such as glasses not needing blowjob poses.

            return self.images[index_string]
