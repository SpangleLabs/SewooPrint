from document_image import GreyScaleImage, SilhouetteImage
from document_web import ChoresBoardDocument
from printer_repo import PrinterRepo
from requests import TechSupportOathRequest, NotMyBusinessRequest, HAL9000WarningRequest, RawTextRequest, \
    ChoresBoardRequest


# noinspection PyMethodMayBeStatic
class Input(object):
    """
    Stores a bunch of different raw inputs to be used.
    """

    TYPE_TEXT = "text"
    TYPE_ASCII = "ascii"
    TYPE_IMAGE = "image"
    TYPE_STREAM = "stream"
    TYPE_WEB = "web"

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
            requests = [TechSupportOathRequest(), NotMyBusinessRequest(), HAL9000WarningRequest(), RawTextRequest()]
            self.choose_input(requests)
            return
        if input_type == self.TYPE_ASCII:
            print("Ascii art input type selected.")
            # TODO: Handle ascii art type input.
            return
        if input_type == self.TYPE_IMAGE:
            print("Image input type selected.")
            # Handle image type input.
            self.choose_image_input()
            return
        if input_type == self.TYPE_STREAM:
            print("Stream input type selected.")
            # TODO: Handle stream type input.
            return
        if input_type == self.TYPE_WEB:
            print("Web input type selected.")
            requests = [ChoresBoardRequest()]
            self.choose_input(requests)
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
        if user_input_clean in ['web']:
            return self.TYPE_WEB
        return None

    def choose_input(self, requests):
        """chooses a text input"""
        print("Available inputs: " + ", ".join(x.name for x in requests))
        user_input = input("Please select: ")
        user_input_clean = user_input.lower().strip()
        for request in requests:
            if request.matches_input(user_input_clean):
                print("Printing " + request.name)
                request.print(self.mPrinter)
                return
        print("I don't know that one.")

    def choose_image_input(self):
        """chooses an image input"""
        print("Available image input types: greyscale, silhouette.")
        user_input = input("Please select: ")
        user_input_clean = user_input.lower().strip()
        if user_input_clean in ["greyscale", "grayscale", "grey", "gray"]:
            filename = input("Please enter filename: ")
            image_document = self.load_image_file(filename)
            self.mPrinter.print_document(image_document)
            print("Printing complete")
            return
        if user_input_clean in ["silhouette"]:
            filename = input("Please enter filename: ")
            image_document = self.load_image_silhouette_file(filename)
            self.mPrinter.print_document(image_document)
            print("Printing complete")
            return
        print("I don't know that one.")

    @staticmethod
    def load_image_file(file_name):
        document = GreyScaleImage(file_name)
        return document

    @staticmethod
    def load_image_silhouette_file(file_name):
        document = SilhouetteImage(file_name)
        return document


if __name__ == "__main__":
    Input()
