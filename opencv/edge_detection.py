import cv2
import numpy as np
image = cv2.imread('sample.jpg')

# Sobel Edge Detection
sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
sobel_edges = cv2.magnitude(sobel_x, sobel_y)
cv2.imshow("Sobel", np.uint8(sobel_edges))
cv2.waitKey(0)

# Canny Edge Detection
canny_edges = cv2.Canny(
    image,
    100, # min_value
    200, # max_value
)
cv2.imshow("Canny", np.uint8(canny_edges))
cv2.waitKey(0)