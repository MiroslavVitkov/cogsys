#!/usr/bin/env python3


'''
This module investigates colour detection over Visual Genome image regions.

Firstly, attributes are extracted from region graphs.
Then a naive word search is performed to detect colours.
The associated images are fetched and relevant regions - cropped.
Cropped regions are randomly split into a training and test sets.
A multi-label classifier is trained and evaluated.
Precision and accuracy are reported,
along with some of the true positives and false positives.
'''


from io import BytesIO
from iter import Local
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from PIL import Image
import requests


# Crop and rescale images into this size.
PATCH_SIZE = (224, 224)

# RGB(24bit) descriptions of many colours. Source:
# https://simple.wikipedia.org/wiki/List_of_colors
COLOURS = {'amber': (255, 192, 0)
          ,'amethist': (153, 102, 204)
          ,'apricot': (251, 206, 177)
          ,'aquamarine': (127, 255, 212)
          ,'azure': (0, 127, 255)
          ,'baby blue': (137, 207, 240)
          ,'beige': (245, 245, 220)
          ,'black': (0, 0, 0)
          ,'blue': (0, 0, 255)
          ,'blue-green': (0, 149, 182)
          ,'blue-violet': (138, 43, 226)
          ,'blush': (222, 93, 131)
          ,'bronze': (205, 127, 50)
          ,'brown': (150, 75, 0)
          ,'burgundy': (128, 0, 32)
          ,'byzantium': (112, 41, 99)
          ,'carmine': (150, 0, 24)
          ,'cerise': (222, 49, 99)
          ,'cerulean': (0, 123, 167)
          ,'champagne': (247, 231, 206)
          ,'chartreuse green': (127, 255, 0)
          ,'chocolate': (123, 63, 0)
          ,'cobalt blue': (0, 71, 171)
          ,'coffee': (111, 78, 55)
          ,'copper': (184, 115, 51)
          ,'coral': (255, 127, 80)
          ,'crimson': (220, 20, 60)
          ,'cyan': (0, 255, 255)
          ,'desert sand': (237, 201, 175)
          ,'electric blue': (125, 249, 255)
          ,'emerald': (80, 200, 120)
          ,'erin': (0, 255, 63)
          ,'gold': (255, 215, 0)
          ,'gray': (128, 128, 128)
          ,'green': (0, 256, 0)
          ,'harlequin': (63, 255, 0)
          ,'indigo': (75, 0, 130)
          ,'ivory': (255, 255, 240)
          ,'jade': (0, 168, 107)
          ,'jungle green': (41, 171, 135)
          ,'lavander': (181, 126, 220)
          ,'lemon': (255, 247, 0)
          ,'lilac': (200, 162, 200)
          ,'lime': (191, 255, 0)
          ,'magneta': (255, 0, 255)
          ,'magneta rose': (255, 0, 175)
          ,'maroon': (128, 0, 0)
          ,'mauve': (224, 176, 255)
          ,'navy blue': (0, 0, 128)
          ,'ochre': (204, 119, 34)
          ,'olive': (128, 128, 0)
          ,'orange': (255, 102, 0)
          ,'orange-red': (255, 69, 0)
          ,'orchid': (218, 112, 214)
          ,'peach': (255, 229, 180)
          ,'pear': (209, 226, 49)
          ,'periwinkle': (204, 204, 255)
          ,'persian blue': (28, 57, 187)
          ,'pink': (253, 108, 158)
          ,'plum': (142, 69, 133)
          ,'prussian blue': (0, 49, 83)
          ,'pauce': (204, 136, 153)
          ,'purple': (128, 0, 128)
          ,'raspberry': (227, 11, 92)
          ,'red': (255, 0, 0)
          ,'red-violet': (199, 21, 133)
          ,'rose': (255, 0, 127)
          ,'ruby': (224, 17, 95)
          ,'salmon': (250, 128, 114)
          ,'sangria': (146, 0, 10)
          ,'sapphire': (15, 82, 186)
          ,'scarlet': (255, 36, 0)
          ,'silver': (192, 192, 192)
          ,'slate gray': (112, 128, 144)
          ,'spring bud': (167, 252, 0)
          ,'spring green': (0, 255, 127)
          ,'tan': (210, 180, 140)
          ,'taupe': (72, 60, 50)
          ,'teal': (0, 128, 128)
          ,'turquoise': (64, 224, 208)
          ,'ultramarine': (63, 0, 255)
          ,'violet': (127, 0, 255)
          ,'viridian': (64, 130, 109)
          ,'white': (255, 255, 255)
          ,'yellow': (255, 255, 0)
          }


def visualize_regions(image, regions):
    response = requests.get(image.url)
    file = BytesIO(response.content)
    img = Image.open(file)
    plt.imshow(img)

    ax = plt.gca()
    for region in regions:
        ax.add_patch(Rectangle((region.x, region.y)
                              ,region.width
                              ,region.height
                              ,fill=False
                              ,edgecolor='red'
                              ,linewidth=1))
        ax.text(region.x
               ,region.y
               ,region.phrase
               ,style='italic'
               ,bbox={'facecolor':'white', 'alpha':0.4, 'pad':10})
    fig = plt.gcf()
    plt.tick_params(labelbottom='off', labelleft='off')
    plt.show()


def from_desc():
    it = Local([1,2,3])
    for image, regions, n in it:
        interesting = []
        for r in regions:
            for word in r.phrase.split():
                if word in COLOURS:
                    interesting.append(r)
                    continue
        if len(interesting):
            visualize_regions(image, interesting)


def from_pixels():
    it = Local([1,2,3])
    for image, regions, n in it:
        response = requests.get(image.url)
        file = BytesIO(response.content)
        img = Image.open(file)
        for r in regions:
            cropped = img.crop((r.x, r.y, r.x+r.width, r.y+r.height))
            print(dir(cropped))


def main():
#    from_desc()
    from_pixels()

    #img = Image.open('/home/vorac/2019-05-08-190834_1920x1080_scrot.png')
    #img = img.resize((224, 224))
    #img.show()


if __name__ == '__main__':
    main()


# arm if the chair is grey
