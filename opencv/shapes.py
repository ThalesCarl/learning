import cv2
import numpy as np

# Create blank image
image = np.zeros((500, 500, 3), dtype=np.uint8)

# Draw a rectangle
cv2.rectangle(image, (50, 50), (400, 400), (0, 255, 0), 3) # (start_point, end_point, color, tickness)

# Draw a circle
cv2.circle(image, (250, 250), 100, (255, 0, 0), 5) # (center, radius, color, thickness)

# Draw a line
cv2.line(image, (0, 0), (500, 500), (0, 0, 255), 2) # (start_point, end_point, color, thickness)

cv2.imshow("Image with shapes", image)
cv2.waitKey(0)

# Finish example
cv2.destroyAllWindows()