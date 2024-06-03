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
            
    return label_matrix, labels


def get_border_components(label_matrix=None, labels=None, img_matrix=None, max_border_pixels=1):

    """
        Identifies and returns border components

        args:
            label_matrix: Numpy array with same shape of the image containing component labels
            img_matrix: Numpy array representing a binary image
            max_border_pixels: Maximum amount of border pixels allowed per component. If a component exceeds
            the maximum amount of border pixels, it's considered a border_component
        
        returns:
            A numpy array containing the labels of border components  
    """

    if img_matrix is None and label_matrix is None:
        raise Exception('Either an image matrix or a label_matrix of need to be provided')

    if img_matrix is not None and label_matrix is None:
        label_matrix, labels = get_connected_components(img_matrix)

    if label_matrix is not None and labels is None:
        labels = numpy.unique(label_matrix)

    temp = numpy.zeros(shape=(label_matrix.shape[0] - 2, label_matrix.shape[1] - 2), dtype=int)
    border_mask = numpy.pad(temp, pad_width=1, constant_values=1)

    def filter_border(label):
        label_mask = label_matrix == label
        return numpy.count_nonzero(label_mask & border_mask) > max_border_pixels

    return list(filter(filter_border, labels))
        

def get_small_components(label_matrix=None, img_matrix=None, labels=None, min_size=None):
    
    """
        Identifies and returns small componenents

        args:
            label_matrix: Numpy array with same shape of the image containing component labels
            img_matrix: Numpy array representing a binary image
            min_size: The minimum size that a component should have to not be considered small

        returns:
            A numpy array containing the indices of small objects
    """

    if min_size is None:
        raise Exception('An minimum size must be provided')
    
    if img_matrix is None and label_matrix is None:
        raise Exception('Either an image matrix or a label_matrix must be provided')
    
    if img_matrix is not None and label_matrix is None:
        label_matrix, labels = get_connected_components(img_matrix)

    if label_matrix is not None and labels is None:
        labels = numpy.unique(label_matrix)

    return list(filter(lambda label: numpy.count_nonzero(label_matrix == label) < min_size, labels))