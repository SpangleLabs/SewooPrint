from PIL import Image
import math

musicImage = "/home/dr-spangle/music_image.png"

f = open("/dev/usb/lp1", "wb")

if(True):
    def loadBigImageFile(fileName):
        image = Image.open(fileName).convert('RGBA')
        width,height = image.size
        newwidth = 400
        print(width)
        print(height)
        print(newwidth)
        print(str(width) + "/" + str(newwidth))
        scalefactor = width/(newwidth+0.0)
        print(scalefactor)
        newheight = height//scalefactor
        endwidth = math.ceil(newwidth/8)*8
        endheight = math.ceil(newheight/8)*8
        image = image.resize((endwidth,endheight),Image.ANTIALIAS)
        
        numSegments = endheight//400
        print(numSegments)
        image_string = b''
        for segmentNum in range(numSegments):
            offset = segmentNum*400
            segHeight = min(400,endheight)

            image_string = b'\x1d\x2a'
            image_string += bytes([endwidth//8,segHeight//8])
            pixnum = 0
            pixval = 0
            for x in range(endwidth):
                for y in range(segHeight):
                    r,g,b,a = image.getpixel((x,y+offset))
                    if(r*g*b<100*100*100 and a>50):
                        pixval += 2**(7-pixnum)
                    if(pixnum==7):
                        image_string += bytes([pixval])
                        pixnum = 0
                        pixval = 0
                    else:
                        pixnum += 1
            image_string += b'\x1d\x2f\x00'
            f.write(image_string)
        return image_string

image_string = b""
loadBigImageFile(musicImage)
image_string += b'\n\n\n\n\n\n\x1d\x56\x01\n'


f.write(image_string)
#print(image_string)

