#!/usr/bin/env python3


'''
This module investigates colour detection over Visual Genome image regions.

Firstly, attributes are extracted from region graphs.
Then a naive word search is performed to detect colours.
The associated images are fetched and relevant regions - cropped.
Cropped regions are randomly split into a training and test sets.
A multi-label classifier is trained and evaluated.
Prevision and accuracy are reported,
along with some of the true positives and false positives.
'''


from PIL import Image


# Crop and rescale images into this size.
PATCH_SIZE = (224, 224)


def main():
    print('putka')
    img = Image.open('/home/vorac/2019-05-08-190834_1920x1080_scrot.png')
    print('kur')
    img = resize(img, 224, 224)
    img.show()

if __name__ == '__main__':
    main()

