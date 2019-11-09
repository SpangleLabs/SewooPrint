from image import GreyScaleImage, SilhouetteImage
from printer_repo import PrinterRepo
from document import TextDocument


# noinspection PyMethodMayBeStatic
class Input(object):
    """
    Stores a bunch of different raw inputs to be used.
    """

    TYPE_TEXT = "text"
    TYPE_ASCII = "ascii"
    TYPE_IMAGE = "image"
    TYPE_STREAM = "stream"

    mPrinter = None

    def __init__(self):
        """
        Start input choice.
        """
        self.mPrinter = PrinterRepo().default_printer()
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
            oath_document = self.tech_support_oath()
            self.mPrinter.print_document(oath_document)
            print("Printing complete")
            return
        if user_input_clean in ['not my business', 'notmybusiness']:
            poem_document = self.not_my_business()
            self.mPrinter.print_document(poem_document)
            print("Printing complete")
            return
        if user_input_clean in ['hal9000 warning', 'hal warning', 'hal', 'hal9000']:
            warn_document = self.hal_warning()
            self.mPrinter.print_document(warn_document)
            print("Printing complete")
            return
        print("I don't know that one.")

    def tech_support_oath(self):
        """
        Recites the tech support oath.
        Parody of the Night's Watch oath.
        """
        output = """\
User issues gather, and now my watch begins.
It shall not end until my death.
I shall take no wife (that I will ever see except on weekends),
hold no lands (because I don't make nearly enough),
father no children (because I will never be home anyway).
I shall receive no thanks and win no glory.
I shall live and die at my desk.
I am the antivirus in the darkness.
I am the coder on the walls.
I am the password reset that guards the logins of men.
I pledge my life and honor to the Help Desk's Watch,
for this night and all the nights to come."""
        document = TextDocument().add_title("Tech support oath")
        document.add_line_wrapped_text(output)
        return document

    def not_my_business(self):
        """
        Outputs Niyi Osundere's "Not my business"
        """
        poem = """ \
They picked Akanni up one morning
Beat him soft like clay
And stuffed him down the belly
Of a waiting jeep.
What business of mine is it
So long they don't take the yam
From my savouring mouth?
        
They came one night
Booted the whole house awake
And dragged Danladi out,
Then off to a lengthy absence.
What business of mine is it
So long they don't take the yam
From my savouring mouth?

Chinwe went to work one day
Only to find her job was gone:
No query, no warning, no probe -
Just one neat sack for a stainless record.
What business of mine is it
So long they don't take the yam
From my savouring mouth?

And then one evening
As I sat down to eat my yam
A knock on the door froze my hungry hand.
The jeep was waiting on my bewildered lawn
Waiting, waiting in its usual silence."""
        document = TextDocument().add_title("Not My Business")
        document.add_title("by Niyi Osundere")
        document.add_line_wrapped_text(poem)
        return document

    def hal_warning(self):
        """
        Outputs HAL9000's warning from the end of 2010:Odyssey Two
        """
        document = TextDocument()\
            .add_bold_centered_text("ALL THESE WORLDS ARE YOURS-EXCEPT EUROPA").nl()\
            .add_bold_centered_text("ATTEMPT NO LANDING THERE")
        return document

    @staticmethod
    def load_image_file(file_name):
        document = GreyScaleImage(file_name)
        return document.encoded

    @staticmethod
    def load_image_silhouette_file(file_name):
        document = SilhouetteImage(file_name)
        return document.encoded


if __name__ == "__main__":
    Input()
