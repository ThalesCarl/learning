import cv2
import numpy as np

# Create blank image
image = np.zeros((500, 500, 3), dtype=np.uint8)

# Add text - (text, position, font, font_scale, color, thickness, linetype)
cv2.putText(image, "Wake up, Neo!", (10, 30), cv2.FONT_SCRIPT_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

cv2.imshow("White rabbit", image)
cv2.waitKey(0)

# Finish example
cv2.destroyAllWindows()