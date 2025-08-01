import cv2

image = cv2.imread('sample.jpg', cv2.IMREAD_GRAYSCALE)

# Simple thresholding
_, simple_thresholded_image = cv2.threshold(
    image,
    127, # threshold value used to classify the pixels
    255, # value assigned to pixels exceding the threshold
    cv2.THRESH_BINARY
)
cv2.imshow("Simple Threshold", simple_thresholded_image)
cv2.waitKey(0)

# Adaptaptive
adapatative_thresholded_image = cv2.adaptiveThreshold(
    image,
    255, # value assign to pixels exceding the threshold
    cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY,
    11, # block size: 	Size of a pixel neighborhood that is used to calculate a threshold value
    2, # C: Constant subtracted from the mean or weighted mean
)
cv2.imshow("Adaptative Threshold", adapatative_thresholded_image)
cv2.waitKey(0)