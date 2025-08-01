import cv2
image = cv2.imread('sample.jpg')

# Gaussian blur
gaussian_blur = cv2.GaussianBlur(
    image, 
    (15, 15), # Dimension
    0,
)

# Median blur
median_blur = cv2.medianBlur(
    image,
    15,
)

# Bilateral blur
bilateral_blur = cv2.bilateralFilter(
    image,
    9,
    25,
    25,
)

cv2.imshow("Gaussian Blur", gaussian_blur)
cv2.waitKey(0)
cv2.imshow("Median Blur", median_blur)
cv2.waitKey(0)
cv2.imshow("Bilateral Blur", bilateral_blur)
cv2.waitKey(0)