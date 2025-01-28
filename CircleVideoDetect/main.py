import numpy as np
import cv2


def circledetect(frame):
	output = frame.copy()
	gra = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)  # grayscale
	gray = cv2.GaussianBlur(gra, (15, 15), sigmaX=0)  # gaussian blur
	circleslist = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.4, 100, param1=30, param2=130)
	if circleslist is not None:
		# make coords into integers
		circles = np.round(circleslist[0, :]).astype('int')
		# look for 1st circle in array
		try:
			x, y, r = circles[0]
		except:
			print('no circles found')
		# draw circle and center point
		cv2.circle(output, (x, y), r, (0, 255, 0), 6)
		cv2.circle(output, (x, y), 3, (255, 0, 0), 5)
	return output


# opening camera
cam = cv2.VideoCapture('tube2.mov')

while True:
    ret, frame = cam.read()
    if ret:
        frame = cv2.flip(frame, 1)
        picture = circledetect(frame)

        # show frames
        cv2.imshow('circle', picture)

    # exit from pressing q
    if cv2.waitKey(1) == ord('q'):
        break

# release
cam.release()
cv2.destroyAllWindows()
