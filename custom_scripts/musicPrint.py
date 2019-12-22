from PIL import Image
import math

music_image = "/home/dr-spangle/music_image.png"

f = open("/dev/usb/lp1", "wb")


def load_big_image_file(file_name):
    image = Image.open(file_name).convert('RGBA')
    width, height = image.size
    new_width = 400
    print(width)
    print(height)
    print(new_width)
    print(str(width) + "/" + str(new_width))
    scale_factor = width / (new_width + 0.0)
    print(scale_factor)
    new_height = height // scale_factor
    end_width = math.ceil(new_width / 8) * 8
    end_height = math.ceil(new_height / 8) * 8
    image = image.resize((end_width, end_height), Image.ANTIALIAS)

    num_segments = end_height // 400
    print(num_segments)
    output = b''
    for segmentNum in range(num_segments):
        offset = segmentNum * 400
        seg_height = min(400, end_height)

        output = b'\x1d\x2a'
        output += bytes([end_width // 8, seg_height // 8])
        pix_num = 0
        pix_val = 0
        for x in range(end_width):
            for y in range(seg_height):
                r, g, b, a = image.getpixel((x, y + offset))
                if r * g * b < 100 * 100 * 100 and a > 50:
                    pix_val += 2 ** (7 - pix_num)
                if pix_num == 7:
                    output += bytes([pix_val])
                    pix_num = 0
                    pix_val = 0
                else:
                    pix_num += 1
        output += b'\x1d\x2f\x00'
        f.write(output)
    return output


image_string = load_big_image_file(music_image)
image_string += b'\n\n\n\n\n\n\x1d\x56\x01\n'

f.write(image_string)
# print(image_string)
