import math
from abc import ABC, abstractmethod

from PIL import Image


class ImageDocument(ABC):

    def __init__(self, file_name):
        self.image = Image.open(file_name).convert('RGBA')
        self.width, self.height = self.image.size
        self._resize_image()

        self.encoded = b'\x1d\x2a'
        self.encoded += bytes([self.width // 8, self.height // 8])
        pix_num = 0
        pix_val = 0
        for x in range(self.width):
            for y in range(self.height):
                r, g, b, a = self.image.getpixel((x, y))
                if self.is_pixel_dark(r, g, b, a):
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
    def is_pixel_dark(self, r, g, b, a):
        pass


class GreyScaleImage(ImageDocument):
    def is_pixel_dark(self, r, g, b, a):
        return r * g * b < 100 * 100 * 100 and a > 50


class SilhouetteImage(ImageDocument):
    def is_pixel_dark(self, r, g, b, a):
        return a > 10
