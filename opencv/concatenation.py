import cv2
import numpy as np

# Read the images
image1 = cv2.imread('sample.jpg')
image2 = cv2.imread('sample2.png')

# Resize image to the same height and width to better alignment
height = min(image1.shape[0], image2.shape[0])
width = min(image1.shape[1], image2.shape[1])
image1_resized = cv2.resize(image1, (width, height))
image2_resized = cv2.resize(image2, (width, height))

# Horizontal concatenation (side by side)
side_by_side = cv2.hconcat([image1_resized, image2_resized])
cv2.imshow("Size by side", side_by_side)
cv2.waitKey(0)

# Vertical concatenation (top to bottom)
top_to_bottom = cv2.vconcat([image1_resized, image2_resized])
cv2.imshow("Size by side", top_to_bottom)
cv2.waitKey(0)