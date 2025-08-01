import cv2
import numpy as np
image1 = cv2.imread('sample.jpg')
image2 = cv2.imread('sample2.png')

# Resize image to the same height and width to better alignment
height = min(image1.shape[0], image2.shape[0])
width = min(image1.shape[1], image2.shape[1])
image1_resized = cv2.resize(image1, (width, height))
image2_resized = cv2.resize(image2, (width, height))

# Add images
added_image = cv2.add(image1_resized, image2_resized)
# Subtract images
subtracted_image = cv2.subtract(image1_resized, image2_resized)
# Multiply images
multiplied_image = cv2.multiply(image1_resized, image2_resized)

cv2.imshow("Add", added_image)
cv2.waitKey(0)
cv2.imshow("Subtract", subtracted_image)
cv2.waitKey(0)
cv2.imshow("Multiply", multiplied_image)
cv2.waitKey(0)
