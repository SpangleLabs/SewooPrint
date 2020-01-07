import math
from abc import abstractmethod, ABC
from typing import Tuple, Union

import qrcode
from PIL import Image

from document import Document, TextDocument, ConcatDocument


class ImageDocument(Document, ABC):

    def __init__(self, image):
        super().__init__()
        # Load, then resize image
        self.image = image
        self.width, self.height = self.image.size
        self._resize_image()

        # Encode image
        self.encoded = b'\x1d\x2a'
        self.encoded += bytes([self.width // 8, self.height // 8])
        pix_num = 0
        pix_val = 0
        for x in range(self.width):
            for y in range(self.height):
                pixel = self.image.getpixel((x, y))
                if self.is_pixel_dark(pixel):
                    pix_val += 2 ** (7 - pix_num)
                if pix_num == 7:
                    self.encoded += bytes([pix_val])
                    pix_num = 0
                    pix_val = 0
                else:
                    pix_num += 1
        self.encoded += b'\x1d\x2f\x00'

    def _resize_image(self):
        new_width = 400
        scale_factor = self.width / new_width
        new_height = self.height // scale_factor
        end_width = math.ceil(new_width / 8) * 8
        end_height = math.ceil(new_height / 8) * 8
        self.image = self.image.resize((end_width, end_height), Image.ANTIALIAS)
        self.width = end_width
        self.height = end_height

    @abstractmethod
    def is_pixel_dark(self, pixel: Union[int, Tuple[int, int, int], Tuple[int, int, int, int]]):
        pass


class GreyScaleImage(ImageDocument):
    def is_pixel_dark(self, pixel):
        if isinstance(pixel, int):
            return pixel < 100
        if len(pixel) == 4:
            r, g, b, a = pixel
            return r * g * b < 100 * 100 * 100 and a > 50
        if len(pixel) == 3:
            r, g, b = pixel
            return r * g * b < 100 * 100 * 100


class SilhouetteImage(ImageDocument):
    def is_pixel_dark(self, pixel):
        if isinstance(pixel, Tuple) and len(pixel) == 4:
            _, _, _, a = pixel
            return a > 10
        return True


class QRCodeImage(GreyScaleImage):

    def __init__(self, qr_data):
        self.qr_data = qr_data
        image = qrcode.make(qr_data)
        super().__init__(image)


class WifiQRCode(Document):

    def __init__(self, ssid, password, auth_type="WPA"):
        super().__init__()
        text = f"WIFI:T:{auth_type};S:{ssid};P:{password};;"
        self.qr_image_doc = QRCodeImage(text)
        self.title_doc = TextDocument().add_title(ssid).nl()
        self.pass_doc = TextDocument().add_bold_text("Password: ").add_text(password)
        self.encoded = ConcatDocument([self.title_doc, self.qr_image_doc, self.pass_doc]).encoded
