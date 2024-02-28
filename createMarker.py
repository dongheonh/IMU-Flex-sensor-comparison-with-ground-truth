import cv2
import numpy as np
import matplotlib.pyplot as plt

# Create a predefined dictionary object for ArUco markers
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

# Specify marker ID and size
marker_id = 12
marker_size = 200

# Generate an ArUco marker image
marker_image = cv2.aruco.generateImageMarker(dictionary, marker_id, marker_size)

# Display the marker using matplotlib
plt.imshow(marker_image, cmap='gray')
plt.axis('off')
plt.show()
