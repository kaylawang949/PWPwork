import cv2
import numpy as np

man_pic = cv2.imread('photos/manface.jpg', cv2.IMREAD_GRAYSCALE)
crowd = cv2.imread('photos/crowd.jpg', cv2.IMREAD_GRAYSCALE)


#sharpen
kernel = np.array([[0, -1, 0], [-1, 5, -], [0, -1, 0]])

#gaussian blur
crowd = cv2.filter2D(crowd, -1, kernel)
crowd = cv2.GaussianBlur(crowd, (7, 7), 0)

#canny edge detection on man face 
man_pic = cv2.GaussianBlur(man_pic, (7, 7), 0)
man_edges = cv2.Canny(man_pic, 30, 100)

#initialize haar cascades 
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#scanning faces in crowd 
faces = face_cascade.detectMultiScale(crowd, scaleFactor=1.12, minNeighbors=3)

#rectangles around detected faces 
for (x, y, w, h) in faces:
    cv2.rectangle(crowd, (x, y), (x + w, y + h), (0, 255, 0), 2)

contours_target, _ = cv2.findContours(man_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
target_contour = max(contours_target, key=cv2.contourArea)

min_similarity = 1
best_coords = None

for (x, y, w, h) in faces:
    face_in_crowd = crowd[y:y + h, x:x + w]

    face_in_crowd_edges = cv2.Canny(face_in_crowd, 30, 100)

    # face_in_crowd_edges = cv2.resize(face_in_crowd_edges, (400, 400))
    # man_edges = cv2.resize(man_edges, (400, 400))

    contours_crowd, _ = cv2.findContours(face_in_crowd_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours_crowd: 
        similarity = cv2.matchShapes(target_contour, contour, cv2.CONTOURS_MATCH_I3, 0.0)
        print(similarity)

        if similarity < min_similarity:
            min_similarity = similarity
            best_coords = (x, y, w, h)

if best_coords is not None:
    x, y, w, h = best_coords
    cv2.rectangle(crowd, (x, y), (x + w, y + h), (0, 0, 0), 2)  

cv2.imshow('Sharpened Image', man_edges)
cv2.imshow('Crowd image', crowd)
cv2.waitKey(0)
cv2.destroyAllWindows()
