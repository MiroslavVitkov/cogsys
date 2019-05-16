#!/usr/bin/env python3


import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from io import BytesIO
from os.path import isfile
from PIL import Image
import requests
import urllib
from visual_genome import api as vgr
from visual_genome import local as vgl
from zipfile import ZipFile


DATA_DIR = './data/'
PREDICATES = ['on top of']


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


def get_next_remote(ids=None):
    if ids is None:
        ids = vgr.get_all_image_ids()  # ids start from 1

    for id in ids:
        image = vgr.get_image_data(id)
        regions = vgr.get_region_descriptions_of_image(id)
        graph = vgr.get_scene_graph(id)
        yield image, regions, graph


def get_next_local(ids=None):
    images = vgl.get_all_image_data(DATA_DIR)
    all_regions = vgl.get_all_region_descriptions(DATA_DIR)  # slow
    if ids is None:
        ids = [i for i in range(1, len(images))]

    for id in ids:
        image = images[id-1]
        regions = all_regions[id-1]
        graph = vgl.get_scene_graph(id
                                   ,images=DATA_DIR
                                   ,image_data_dir=DATA_DIR+'/by-id/'
                                   ,synset_file=DATA_DIR+'/synsets.json')
        yield image, regions, graph


def download_zip(path, url):
    with urllib.request.urlopen(url) as response:
        stream = BytesIO(response.read())
        zip = ZipFile(stream)
        zip.extractall(path)


def download_dataset(path=DATA_DIR):
    if not isfile(path+'/image_data.json'):
        download_zip(path, 'http://visualgenome.org/static/data/dataset/image_data.json.zip')
    if not isfile(path+'/region_descriptions.json'):
        download_zip(path, 'http://visualgenome.org/static/data/dataset/region_descriptions.json.zip')
    if not isfile(path+'/scene_graphs.json'):
        download_zip(path, 'http://visualgenome.org/static/data/dataset/scene_graphs.json.zip')
        vgl.save_scene_graphs_by_id(data_dir='data/', image_data_dir='data/by-id/')
    if not isfile(path+'/synsets.json'):
        download_zip(path, 'http://visualgenome.org/static/data/dataset/synsets.json.zip')


def is_relation_spatial(relation):
    if relation.predicate in (PREDICATES):
        return True
    else:
        return False


def main():
    for image, regions, graph in get_next_local(ids=range(1, 1000)):
        print('Processing image with id', image.id)
        for r in graph.relationships:
            if is_relation_spatial(r):
                print('SUBJ:', r.subject, 'PRED:', r.predicate, 'OBJ:', r.object, 'SYNSET:', r.synset)
                if not r.subject.y > r.object.y + r.object.height:
                    print('VIOLATION')
                    # Draw subject and object bounding boxes for verification by a human operator.
                    for reg in regions:
                        if reg.id == r.subject.id:
                            print('CONFIRMED')
                            visualize_regions(image, regions[:8])


if __name__ == '__main__':
    main()
