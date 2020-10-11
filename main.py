import cv2
import imutils
import numpy as np
import imutils.contours

def areaRatio(cnt, image):
    return cv2.contourArea(cnt) / (image.shape[0] * image.shape[1])

# Load input image
image = cv2.imread('input.jpg')

# Convert image to grayscale and blure it 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 3)

# Perform Canny Edge Detection and dialate image
edged = cv2.Canny(gray, 20, 30)
edged = cv2.dilate(edged, None, iterations=1)

# Get Image Contours
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# Select contours with areaRatio > 0.001
cnts = [*filter(lambda c: areaRatio(c, image) > 1e-3, cnts)]

# Sort contours in left-to-right order
(cnts, boxes) = imutils.contours.sort_contours(cnts)

# Calculate Pixels Per Centimiter for width and Height
ppcW = boxes[0][2] / 1.0
ppcH = boxes[0][3] / 1.0

# Draw bounding boxes and object sizes
res_img = image.copy()
for (x, y, w, h) in boxes:

    cv2.rectangle(res_img, (x, y), (x + w, y + h), (0, 255, 0), 10)

    cv2.putText(res_img, f'{w / ppcW:.1f}x{h / ppcH:.1f} cm',
                (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 10)

# Save Image to File
cv2.imwrite('output.jpg', res_img)

cv2.destroyAllWindows()
