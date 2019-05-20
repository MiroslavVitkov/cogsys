#!/usr/bin/env python3


from PIL import Image


class Region:
    '''Recatangular region, top left is (0, 0).'''
    def __init__(me, x, y, w, h):
        assert x >=0 and y >=0 and w > 0 and h > 0
        me.x = x
        me.y = y
        me.w = w
        me.h = h


    @staticmethod
    def from_image(image):
        w, h = image.size()
        return Region(0, 0, w, h)


    def contains(me, region):
#        if me.x <= region.x and
#           me.y <= region.y and
#           me.x + me.w >= region.x + region.w and
#           me.y + me.h >= region.y + region.h:
#            return True
#        else:
#            return False
        pass


def crop(image, region):
    assert Region.from_image(image).contains(region)
    r = region
    box = (r.x, r.y, r.x+r.w, r.y+r.h)
    img = image.crop(box)
    return img


def main():
    print('putka')
    img = Image.open('/home/vorac/2019-05-08-190834_1920x1080_scrot.png')
    print('kur')
    img = resize(img, 224, 224)
    img.show()

if __name__ == '__main__':
    main()

