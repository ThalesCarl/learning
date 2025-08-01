import cv2

# Read a image
image = cv2.imread('sample.jpg')

# Show the image
cv2.imshow("original image", image)
cv2.waitKey(0)

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("grayscale image", gray_image)
cv2.waitKey(0)

# Save the image
cv2.imwrite("gray_image.jpg", gray_image)

# Resize the image
resized_image = cv2.resize(image, (200, 200))
cv2.imshow("resized image", resized_image)
cv2.waitKey(0)

# Crop the image
cropped_image = image[200:300, 100:200] # height, width
cv2.imshow("cropped image", cropped_image)
cv2.waitKey(0)

# Rotate the image
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
rotation_matrix = cv2.getRotationMatrix2D(center, 45, 1.0) # Last value is a scaling factor that is not used in this matrix
rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h))
cv2.imshow("rotated image", rotated_image)
cv2.waitKey(0)

# Scale a image
scaled_image = cv2.resize(image, None, fx=1.5, fy=0.5)
cv2.imshow("scaled image", scaled_image)
cv2.waitKey(0)

# Finish example
cv2.destroyAllWindows()
