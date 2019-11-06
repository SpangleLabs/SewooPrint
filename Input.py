from PIL import Image
import math
from Printer import Printer
from Formatter import Formatter


class Input(object):
    """
    Stores a bunch of different raw inputs to be used.
    """

    TYPE_TEXT = "text"
    TYPE_ASCII = "ascii"
    TYPE_IMAGE = "image"
    TYPE_STREAM = "stream"

    mPrinter = None
    mFormatter = None

    def __init__(self):
        """
        Start input choice.
        """
        self.mPrinter = Printer()
        self.mFormatter = Formatter()
        input_type = self.choose_input_type()
        if input_type is None:
            print("Invalid input type.")
            return
        if input_type == self.TYPE_TEXT:
            print("Text input type selected.")
            # Handle text type input.
            self.choose_text_input()
            return
        if input_type == self.TYPE_ASCII:
            print("Ascii art input type selected.")
            # TODO: Handle ascii art type input.
            return
        if input_type == self.TYPE_IMAGE:
            print("Image input type selected.")
            # TODO: Handle image type input.
            return
        if input_type == self.TYPE_STREAM:
            print("Stream input type selected.")
            # TODO: Handle stream type input.
            return
        print("Unknown input type.")
        return

    def choose_input_type(self):
        """
        Ask the user what type of input they want
        """
        print("Please select an input type.")
        print("Available input types: text, ascii art, image, stream")
        user_input = input("Enter type: ")
        user_input_clean = user_input.strip().lower()
        if user_input_clean in ['text']:
            return self.TYPE_TEXT
        if user_input_clean in ['ascii', 'ascii art', 'asciiart']:
            return self.TYPE_ASCII
        if user_input_clean in ['image', 'img', 'picture', 'pic']:
            return self.TYPE_IMAGE
        if user_input_clean in ['stream', 'feed', 'twitter']:
            return self.TYPE_STREAM
        return None

    def choose_text_input(self):
        """chooses a text input"""
        print("Available text inputs: tech support oath, not my business, HAL9000 warning, raw.")
        user_input = input("Please select: ")
        user_input_clean = user_input.lower().strip()
        if user_input_clean in ['tech support oath', 'techsupportoath', 'oath']:
            oath_output = self.tech_support_oath()
            self.mPrinter.print_raw(oath_output)
            print("Printing complete")
            return
        if user_input_clean in ['not my business', 'notmybusiness']:
            poem_output = self.not_my_business()
            self.mPrinter.print_raw(poem_output)
            print("Printing complete")
            return
        if user_input_clean in ['hal9000 warning', 'hal warning', 'hal']:
            warn_output = self.hal_warning()
            self.mPrinter.print_raw(warn_output)
            print("Printing complete")
            return

    def tech_support_oath(self):
        """
        Recites the tech support oath.
        Parody of the Night's Watch oath.
        """
        output = "User issues gather, and now my watch begins. "
        output += "It shall not end until my death. "
        output += "I shall take no wife (that I will ever see except on weekends), "
        output += "hold no lands (because I don't make nearly enough), "
        output += "father no children (because I will never be home anyway). "
        output += "I shall receive no thanks and win no glory. "
        output += "I shall live and die at my desk. "
        output += "I am the antivirus in the darkness. "
        output += "I am the coder on the walls. "
        output += "I am the password reset that guards the logins of men. "
        output += "I pledge my life and honor to the Help Desk's Watch, "
        output += "for this night and all the nights to come."
        print_output = self.mFormatter.title("Tech support oath")
        print_output += self.mFormatter.multiLine(output)
        return print_output

    def not_my_business(self):
        """
        Outputs Niyi Osundere's "Not my business"
        """
        output = self.mFormatter.title("Not My Business")
        output += self.mFormatter.title("by Niyi Osundere")
        output += b"They picked Akanni up one morning\n"
        output += b"Beat him soft like clay\n"
        output += b"And stuffed him down the belly\n"
        output += b"Of a waiting jeep.\n"
        output += b"What business of mine is it\n"
        output += b"So long they don't take the yam\n"
        output += b"From my savouring mouth?\n\n"
        output += b"They came one night\n"
        output += b"Booted the whole house awake\n"
        output += b"And dragged Danladi out,\n"
        output += b"Then off to a lengthy absence.\n"
        output += b"What business of mine is it\n"
        output += b"So long they don't take the yam\n"
        output += b"From my savouring mouth?\n\n"
        output += b"Chinwe went to work one day\n"
        output += b"Only to find her job was gone:\n"
        output += b"No query, no warning, no probe -\n"
        output += b"Just one neat sack for a stainless record.\n"
        output += b"What business of mine is it\n"
        output += b"So long they don't take the yam\n"
        output += b"From my savouring mouth?\n\n"
        output += b"And then one evening\n"
        output += b"As I sat down to eat my yam\n"
        output += b"A knock on the door froze my hungry hand.\n"
        output += b"The jeep was waiting on my bewildered lawn\n"
        output += b"Waiting, waiting in its usual silence."
        return output

    def hal_warning(self):
        """
        Outputs HAL9000's warning from the end of 2010:Odyssey Two
        """
        output = self.mFormatter.bold(
            self.mFormatter.centreText("ALL THESE WORLDS ARE YOURS-EXCEPT EUROPA"))
        output += b"\n"
        output += self.mFormatter.bold(self.mFormatter.centreText("ATTEMPT NO LANDING THERE"))
        return output

    @staticmethod
    def load_image_file(file_name):
        image = Image.open(file_name).convert('RGBA')
        width, height = image.size
        new_width = 400
        scale_factor = width / new_width
        new_height = height // scale_factor
        end_width = math.ceil(new_width / 8) * 8
        end_height = math.ceil(new_height / 8) * 8
        image = image.resize((end_width, end_height), Image.ANTIALIAS)

        image_string = b'\x1d\x2a'
        image_string += bytes([end_width // 8, end_height // 8])
        pix_num = 0
        pix_val = 0
        for x in range(end_width):
            for y in range(end_height):
                r, g, b, a = image.getpixel((x, y))
                if r * g * b < 100 * 100 * 100 and a > 50:
                    pix_val += 2 ** (7 - pix_num)
                if pix_num == 7:
                    image_string += bytes([pix_val])
                    pix_num = 0
                    pix_val = 0
                else:
                    pix_num += 1
        return image_string + b'\x1d\x2f\x00'

    @staticmethod
    def load_image_silhouette_file(file_name):
        image = Image.open(file_name).convert('RGBA')
        width, height = image.size
        new_width = 400
        scale_factor = width / new_width
        new_height = height // scale_factor
        end_width = math.ceil(new_width / 8) * 8
        end_height = math.ceil(new_height / 8) * 8
        image = image.resize((end_width, end_height), Image.ANTIALIAS)

        image_string = b'\x1d\x2a'
        image_string += bytes([end_width // 8, end_height // 8])
        pix_num = 0
        pix_val = 0
        for x in range(end_width):
            for y in range(end_height):
                _, _, _, a = image.getpixel((x, y))
                if a > 10:
                    pix_val += 2 ** (7 - pix_num)
                if pix_num == 7:
                    image_string += bytes([pix_val])
                    pix_num = 0
                    pix_val = 0
                else:
                    pix_num += 1
        image_string += b'\x1d\x2f\x00'
        return image_string


if __name__ == "__main__":
    Input()
