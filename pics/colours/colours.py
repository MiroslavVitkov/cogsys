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
COLOURS = ('white silver grey black navy blue cerulean sky blue turquoise '
           'blue-green azure teal cyan green lime chartreuse olive yellow '
           'gold amber orange brown orange-red red maroon rose red-violet '
           'pink magenta purple blue-violet indigo violet peach apricot '
           'ochre plum').split()


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
