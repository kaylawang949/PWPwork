import numpy as np    # IMPORT numpy library
import cv2    # IMPORT opencv library

def mainfilter(frame):    # DEFINE function mainfilter(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    # CONVERT frame to grayscale
    blurred = cv2.GaussianBlur(gray, (23, 23), 0)    # APPLY Gaussian blur to smooth image
    edges = cv2.Canny(blurred, 30, 80, apertureSize=3)    # DETECT edges using Canny edge detector

    kernel = np.ones((41, 41))    # CREATE kernel for morphological operations
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)    # APPLY morphological closing to edges

    return closed    # RETURN processed image 

def midpoints(line1, line2):    # DEFINE function midpoints(line1, line2)

    midlist = [[(x1 + x2) // 2, (y1 + y2) // 2]
                  for (x1, y1), (x2, y2) in zip((pt[0] for pt in line1), (pt[0] for pt in line2))]
                  # INITIALIZE list of midpoints by calculating the midpoint of each pair of points

    if len(line1) > 1 and len(line2) > 1:    # IF both lines have more than one point
        midlist.append([(line1[-1][0][0] + line2[-1][0][0]) // 2,
                           (line1[-1][0][1] + line2[-1][0][1]) // 2])
                           # CALCULATE and ADD midpoint of last points

    return np.array(midlist)    # RETURN midpoints as numpy array

def curvedetect(frame):    # DEFINE function curvedetect(frame)

    mask = frame.copy()    # COPY frame to mask
    height, width, _ = mask.shape    # EXTRACT height and width of frame
    masked = mask[100:height - 100, 350:width - 350]    # CROP ROI
    filtered = mainfilter(masked)    # APPLY mainfilter to ROI

    contours, _ = cv2.findContours(filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # FIND contours in filtered image
    contours = sorted(contours, key=cv2.contourArea)    # SORT contours by area

    if len(contours) >= 2:    # IF there are at least 2 contours

        line1 = cv2.approxPolyDP(contours[-1], 6, True)    # APPROXIMATE the largest contour
        line1 = line1[:int(len(line1) / 1.68)]    # EXTRACT portion of the contour
        cv2.polylines(masked, [line1], False, (0, 255, 0), 7, lineType=cv2.LINE_AA)
        # DRAW polyline on masked image

        line2 = cv2.approxPolyDP(contours[-2], 6, True)    # APPROXIMATE the second-largest contour
        line2 = line2[:int(len(line2) / 1.65)]    # EXTRACT portion of the contour
        cv2.polylines(masked, [line2], False, (0, 255, 0), 7, lineType=cv2.LINE_AA)
        # DRAW polyline on masked image

        midlist2 = midpoints(line1, line2)    # CALCULATE midpoints between the two contours

        if len(midlist2) > 0:    # IF midpoints exist
            cv2.polylines(masked, [midlist2], False, (255, 0, 0), 6, lineType=cv2.LINE_AA)
            # DRAW polyline connecting midpoints

    mask[100:height - 100, 350:width - 350] = masked    # REPLACE ROI in original mask
    cv2.rectangle(mask, (350, 100), (width - 350, height - 100), (0, 0, 0), 1)
    # DRAW rectangle around ROI

    return mask    # RETURN processed mask

cam = cv2.VideoCapture(0)    # INITIALIZE camera capture

while True:    # WHILE camera is active
    ret, frame = cam.read()    # CAPTURE frame
    if ret:    # IF frame is captured successfully
        picture = curvedetect(frame)    # PROCESS frame using curvedetect
        cv2.imshow('lines', picture)    # DISPLAY processed frame in window

    if cv2.waitKey(1) == ord('q'):    # IF q key is pressed
        break    # BREAK loop

cam.release()    # RELEASE camera
cv2.destroyAllWindows()    # CLOSE all windows
