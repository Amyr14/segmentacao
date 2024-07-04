## Description
This is an image processing course assignment on the topic of image segmentation. It was requested the development an algorithm that could read an image of a solder, remove unwanted objects in a manner that only the solder remained and finally calculate it's centroid coordinates. A more elaborate description of the solution can be found in the file "segmentacao.pdf", which is the portuguese-written assigment's report.

## Solution
The proposed solution is as follows:
1. Threshold the image with the multiotsu method to remove noise
2. Identify and label connected components in the image
3. Remove objects that have connection with the border
4. Remove objects that have less than 1850 pixels
5. Retrieve the coordinates of active pixels and calculate the arithmetic mean for the X and Y coordinates

To achieve this pipeline, three functions were implemented. Their implementation can be verified in the morphology module. A brief description of their behavior is given bellow.

![image](https://github.com/Amyr14/segmentation/assets/69065770/facc4008-2304-4275-b9aa-c57e1a218296)

*Labeled components in a solder's image*

## Implemented Functions
#### get_connected_components
Identifies and labels connected components of binary images. Given an binary image_matrix, it returns a matrix containing the labeled components and a list of labels. To identify the components, it uses a 3x3 sliding window with centered origin in conjunction with a disjoint set to keep track of label equivalences. As the window slides through the image, if the origin (anchor) is defined, it gives it and all other elements in the window the same label. When it finds more than one label in the same window, the disjoint set puts them in the same subset, keeping track of their equivalence. Finally, when the whole image is labeled, equivalent labels are recovered and joined together in the label matrix.

#### get_border_components
Identifies and returns the labels of border-connected components. Given a binary image / label matrix and a maximum number of border pixels (tolerance number), it uses a border mask to find non-empty intersections with components.

#### get_small_components
Identifies and returns small components. Given a binary image / label matrix and a minimum size (tolerance number), it simply uses mask operations to count the size of each componenent, returning a list of the ones that are smaller than the given minimum size.
