import numpy
from skimage.io import imread, imsave
from skimage.filters import threshold_multiotsu
from skimage.color import label2rgb
from src.morphology import get_connected_components, get_border_components, get_small_components
import os
import sys

inputs_dir = os.path.join(os.getcwd(), 'inputs')
out_dir = os.path.join(os.getcwd(), 'outputs')

if __name__ == '__main__':

    for file in sys.argv[1:]:

        image_matrix = imread(os.path.join(inputs_dir, file), as_gray=True)

        # Calculating the threshold
        _, _, higher_thresh = threshold_multiotsu(image_matrix, classes=4)
        
        # Applying the treshold on the image, resulting in a binary image
        binary_img = image_matrix > higher_thresh

        # Identifiyng the connected components of the image
        label_matrix, labels = get_connected_components(binary_img)

        # Identifying and removing border components
        border_labels = get_border_components(label_matrix, labels=labels)
        for label in border_labels:
            binary_img = (binary_img & ~(label_matrix == label))
        
        # Identifying and removing small components
        small_labels = get_small_components(label_matrix, min_size=1850)
        for label in small_labels:
            binary_img = (binary_img & ~(label_matrix == label))
        
        # Calculating the central point of the image
        centroid = numpy.around(numpy.mean(numpy.nonzero(binary_img), axis=1))
        print(f'--- {os.path.splitext(file)[0]} ---')
        print(f'Centroid X: {centroid[0]}')
        print(f'Centroid Y: {centroid[1]}')