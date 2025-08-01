import cv2

# Load the pre-trained Haar Cascade classifier
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haardcascasde_frontalface_default.xml')

image = cv2.imread('sample.jpg')
image_gray = cv2.imread('sample.jpg', cv2.IMREAD_GRAYSCALE)

faces = face_cascade.detectMultiScale(
    image_gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30,30),
)

for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)


cv2.imshow("Faces", image)
cv2.waitKey(0)