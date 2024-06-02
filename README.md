## Description
This project was developed during an image processing course. It's goal was to develop an algorithm that could read an image of a sutter, remove unwanted objects in a manner that only the sutter remained and finally calculate it's centroid coordinates.

## Solution
The proposed solution is as follows:
1. Threshold the image with the multiotsu method to remove noise
2. Identify and label connected components in the image
3. Remove objects that have connection with the border
4. Remove objects that have less than 1850 pixels
5. Retrieve the coordinates of active pixels and calculate the arithmetic mean for the X and Y coordinates

To achieve this pipeline, three functions were implemented. Their implementation can be verified in the morphology package. A brief descripttion of their behavior is given bellow.

## Implemented Functions
