#!/usr/bin/env python3


import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
import requests
from io import BytesIO
from visual_genome import api as vg


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


def get_next():
    #ids = vg.get_all_image_ids()
    ids = [1,2,3,4,5]
    for id in ids:
        image = vg.get_image_data(id)
        regions = vg.get_region_descriptions_of_image(id)
        yield image, regions


for image, regions in get_next():
    print('Processing image with id ', image.id)
    for region in regions:
        print(region.phrase)
    #visualize_regions(image, regions[:8])

