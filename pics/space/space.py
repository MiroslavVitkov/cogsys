#!/usr/bin/env python3


import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from io import BytesIO
from os.path import isfile
from PIL import Image
import requests
import urllib
from visual_genome import api as vg
from visual_genome import local as vgl
from zipfile import ZipFile


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


def get_next(ids=None):
    if ids is None:
        ids = vg.get_all_image_ids()
    for id in ids:
        image = vg.get_image_data(id)
        regions = vg.get_region_descriptions_of_image(id)
        graph = vg.get_scene_graph_of_image(id)
        yield image, regions, graph


def download_zip(path, url):
    with urllib.request.urlopen(url) as response:
        stream = BytesIO(response.read())
        zip = ZipFile(stream)
        zip.extractall(path)


def download_dataset(path='data/'):
    if not isfile(path+'/image_data.json'):
        download_zip(path, 'http://visualgenome.org/static/data/dataset/image_data.json.zip')
    if not isfile(path+'/region_descriptions.json'):
        download_zip(path, 'http://visualgenome.org/static/data/dataset/region_descriptions.json.zip')
    if not isfile(path+'/scene_graphs.json'):
        download_zip(path, 'http://visualgenome.org/static/data/dataset/scene_graphs.json.zip')
        vgl.save_scene_graphs_by_id(data_dir='data/', image_data_dir='data/by-id/')
    if not isfile(path+'/synsets.json'):
        download_zip(path, 'http://visualgenome.org/static/data/dataset/synsets.json.zip')


download_dataset()

#scene_graphs = vgl.get_scene_graphs(start_index=0, end_index=-1, min_rels=1,
#                                    data_dir='data/', image_data_dir='data/by-id/')

#_, _, graph = get_next(ids=[1])
#r = graph.relationships[0]
#print(r, 'OBJ', r.object, 'PRED', r.predicate, 'SUBJ', r.subject, 'SYNSET', r.synset)


#for image, regions in get_next([1]):
#    print('Processing image with id', image.id)
#    for region in regions:
#        print(region.phrase)
#    #visualize_regions(image, regions[:8])

