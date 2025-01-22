import numpy as np
import cv2

image = cv2.imread('sodapic2.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    # grayscale
output = image.copy()


# detect circles
circleslist = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
if circleslist is not None:
	# make coords into integers
	circles = np.round(circleslist[0, :]).astype('int')
	# look for 1st circle in array
	try:
		x, y, r  = circles[0]
	except:
		print('no circles found')
	# draw circle and center point
	cv2.circle(output, (x, y), r, (0, 255, 0), 4)
	cv2.circle(output, (x, y), 3, (255, 0, 0), 5)

	# display output
	cv2.imshow('circle', output)
	cv2.waitKey(0)
