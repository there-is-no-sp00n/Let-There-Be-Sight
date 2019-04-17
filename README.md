# Let-There-Be-Sight

Requirements:

Intel RealSense D400 series cameras.
Nvidia GPU.
YOLO v2.



Brief Explanation:

This program, using the Intel RealSense D430 camera, scans the environment to look for pertinent objects that are specified.

The pertinent objects are recognized using a neural network framework called YOLO v2.

Once the object is identified, the depth sensor on the Intel RealSense will be utilized to retrieve the distance.

The depth sensor is used to get A) the distance to the object and B) the XYZ coordinates of the object in the real world.

All distance calculations for distance and XYZ coordinates are in reference to where the Intel RealSense is located.
