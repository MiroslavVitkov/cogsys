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
        ax.add_patch(Rectangle((region.x, region.y),
                               region.width,
                               region.height,
                               fill=False,
                               edgecolor='red',
                               linewidth=3))
        ax.text(region.x, region.y, region.phrase, style='italic', bbox={'facecolor':'white', 'alpha':0.7, 'pad':10})
    fig = plt.gcf()
    plt.tick_params(labelbottom='off', labelleft='off')
    plt.show()


fig = plt.gcf()
image = vg.get_image_data(id=61512)
regions = vg.get_region_descriptions_of_image(id=61512)
visualize_regions(image, regions[:8])
