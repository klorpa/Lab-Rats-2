init -2 python:
    class VrenZipImage(renpy.display.im.ImageBase): #TODO: Move this to a more obvious file. Probably something to do along with a bunch of other refactoring.
        def __init__(self, position, filename, mtime=0, **properties):
            super(VrenZipImage, self).__init__(position, filename, mtime, **properties)
            self.position = position
            self.filename = filename

        def load(self):
            tries = 0
            max_tries = 5
            while tries < max_tries:
                global mobile_zip_dict
                try:
                    data = mobile_zip_dict[self.position].read(self.filename)
                    sio = io.BytesIO(data)
                    the_image = renpy.display.pgrender.load_image(sio, self.filename)
                    return the_image

                except (zipfile.BadZipfile, RuntimeError): #Not my fault! See: https://github.com/pfnet/pfio/issues/104
                    e = sys.exc_info()[1]
                    log_message("ERR " + str(tries) + ": "  + str(e))
                    tries += 1
                    if tries >= max_tries:
                        renpy.notify("Unsuccessful Recovery: " + self.position + ", Item: " + self.filename)
                        return renpy.display.pgrender.surface((2, 2), True)

                    else:
                        file_name = mobile_zip_dict[self.position].filename
                        mobile_zip_dict[self.position].close()
                        mobile_zip_dict[self.position] = zipfile.ZipFile(file_name, "a") #May have to convert to a renpy_file first, but I dthink Zipfile will have alreayd done that
