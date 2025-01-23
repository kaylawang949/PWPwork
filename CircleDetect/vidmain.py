import numpy as np
import cv2
import math



def mainfilter(frame):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # grayscale
	output = frame.copy()
	circleslist = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.4, 100, param1=100, param2=20)
	if circleslist is not None:
		# make coords into integers
		circles = np.round(circleslist[0, :]).astype('int')
		# look for 1st circle in array
		try:
			x, y, r = circles[0]
		except:
			print('no circles found')
		# draw circle and center point
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.circle(output, (x, y), 3, (255, 0, 0), 5)
		return output




# following code from: https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/

# Open the default camera
cam = cv2.VideoCapture('IMG_8970.mov')

while True:
    ret, frame = cam.read()
    if ret:
        frame = cv2.flip(frame, 1)
        picture = mainfilter(frame)

        # Display the captured frame
        cv2.imshow('og', picture)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and writer objects
cam.release()
cv2.destroyAllWindows()


