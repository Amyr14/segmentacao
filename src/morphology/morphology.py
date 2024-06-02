import numpy
from scipy.cluster.hierarchy import DisjointSet


def get_connected_components(img_matrix):

    """
        Returns the indices of connected components in C-Style Row Major (for indexing),
        a matrix containing the labeled connected components and a list of the labels
    """

    disjoint_sets = DisjointSet()

    # Adding zero padding in the matrix to deal with border values
    img_matrix = numpy.pad(img_matrix, pad_width=1, constant_values=0)
    
    # Matrix with zero padding that'll hold label values, will be returned later
    label_matrix = numpy.zeros(img_matrix.shape, dtype=numpy.int32)

    
    label_count = 1

    for i in range(1, img_matrix.shape[0] - 1):
        for j in range(1, img_matrix.shape[1] - 1):
            
            anchor = img_matrix[i][j]

            if not anchor:
                continue

            label_window = (label_matrix[i - 1: i + 2, j - 1: j + 2]).flatten()
            defined_region = numpy.sum(label_window) > 0
            labels = numpy.unique(label_window[label_window != 0])
            
            # Pixel is on with undefined label region
            if anchor and not defined_region:
                label_matrix[i][j] = label_count
                disjoint_sets.add(label_count)
                label_count += 1
            
            # Pixel is on with a defined label region
            elif anchor and defined_region:
                first_label = labels[0]
                for label in labels[1:]:
                    disjoint_sets.merge(first_label, label)
                
                label_matrix[i][j] = disjoint_sets[first_label]
                
                
    # Removing padding
    label_matrix = label_matrix[1:-1, 1:-1]

    # Merging labels in the matrix
    for label in range(1, label_count):
        root = disjoint_sets[label]
        label_matrix[label_matrix == label] = root

    # Recovering labels
    labels = numpy.unique(label_matrix[label_matrix != 0])
            
    # Recovering the indices of individual connected components
    # Talvez se essa parte do codigo for vetorizada, algum ganho de performance pode ser obtido
    indices_list = []
    for label in labels:
        indices_list.append(numpy.nonzero(label_matrix == label))

    return indices_list, label_matrix, labels


def get_border_components(img_matrix=None, image_shape=None, components=None, max_border_pixels=1):

    """
        Identifies and returns border components

        args:
            img_matrix: Numpy array representing a binary image
            image_size: Tuple containing the dimensions of the image
            components: Numpy array containing lists of component indices
            max_border_pixels: Maximum amount of border pixels permited per component. If a component exceeds
            the maximum amount of border pixels, it's considered a border_component
        
        returns:
            A numpy array containing the indices of border componenents  
    """

    if not img_matrix and not components:
        raise Exception('Either an image matrix or a list of component indices must be provided')
    
    if not img_matrix and not image_shape:
        raise Exception('image_shape must be provided in the absence of a image matrix')
    
    if img_matrix and not image_shape:
        image_shape = img_matrix.shape

    if img_matrix and not components:
        components = get_connected_components(img_matrix)

    temp = numpy.zeros(shape=(image_shape[0] - 1, image_shape[1] - 1), dtype=numpy.int8)
    border_mask = numpy.pad(temp, pad_width=1, constant_values=1)
    components_mask = numpy.zeros_like(border_mask)
    
    def filter_border(component):
        components_mask[component] = 1
        border_comp = numpy.count_nonzero(components_mask & border_mask) > max_border_pixels
        components_mask[:, :] = 0
        return border_comp

    return list(filter(filter_border, components))

def get_small_components(img_matrix=None, components=None, min_size=None):
    
    """
        Identifies and returns small componenents

        args:
            img_matrix: Numpy array representing a binary image
            components: Numpy array containing lists of component indices
            min_size: The minimum size that a component should have to not be considered small

        returns:
            A numpy array containing the indices of small objects
    """

    if not min_size:
        raise Exception('A minimum size must be provided')
    
    if not img_matrix and not components:
        raise Exception('Either a image matrix or a list of component indices must be provided')
    
    if img_matrix and not components:
        components = get_connected_components(img_matrix)

    return list(filter(lambda component: component[0].size < min_size, components))