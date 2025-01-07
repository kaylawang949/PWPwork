import numpy as np
import cv2
import math



def mainfilter(frame):
    mask = np.zeros(frame.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (600, 200), (1400, 900), (255, 0, 0), -1)
    masked = cv2.bitwise_and(frame, frame, mask=mask)

    gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)  # converts to grayscale
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # applies gaussian blur
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)  # detect edges

    mask_border = cv2.rectangle(
        np.zeros_like(mask), (610, 210), (1390, 890), 255, -1)  # shrink mask by 10px
    edges = cv2.bitwise_and(edges, edges, mask=mask_border)

    dilation = cv2.dilate(edges, np.array([5, 5]), iterations=20)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, np.array([9, 9]))  #
    erosion = cv2.erode(closing, np.array([5, 5]), iterations=10)  # erodes boundaries

    return erosion



def houghstuff(frame, original):
    lines = cv2.HoughLinesP(frame, rho=1, theta=np.pi / 180, threshold=50, minLineLength=200, maxLineGap=500)

    line1lst = []
    line2lst = []

    #following code from group github
    if lines is not None:  # checks to see if there are lines to iterate through
        x1, y1, x2, y2 = lines[0][0]
        slope = (y2 - y1) / (x2 - x1) if x2 != x1 else 999  # slope calculation
        tanbase = math.atan(slope)
        baseangle = tanbase * 180 / math.pi
        line1lst.append([(x1, y1), (x2, y2)])
        for line in lines[1:]:
            x1, y1, x2, y2 = line[0]

            slope = (y2 - y1) / (x2 - x1) if x2 != x1 else 999  # slope calculation
            tan = math.atan(slope)
            angle = tan * 180 / math.pi

            if abs(int(baseangle - angle)) > 10:
                line1lst.append([(x1, y1), (x2, y2)])
            else:
                line2lst.append([(x1, y1), (x2, y2)])

        try:
            cv2.line(original, line1lst[0][0], line1lst[0][1], (0, 255, 0), 8)
            cv2.line(original, line1lst[1][0], line1lst[1][1], (0, 255, 0), 8)
        except:
            pass

    list1midpoint = midpoints(line1lst)
    list2midpoint = midpoints(line2lst)

    actualmidpoint = ((list1midpoint[0] + list2midpoint[0]) // 2, (list1midpoint[1] + list2midpoint[1]) // 2)
    cv2.circle(original, actualmidpoint, 7, (0, 0, 255), -1)

    # perp bisector stuff below
    x1, y1 = list1midpoint[0], list1midpoint[1]
    x2, y2 = list2midpoint[0], list2midpoint[1]

    midpoint = ((x1 + x2) // 2, (y1 + y2) // 2)

    dx = x2 - x1
    dy = y2 - y1

    try:
        perp_slope = -dx / dy  # slope of perp line
    except ZeroDivisionError:
        perp_slope = -999


    line_length = 300

    dx_perp = line_length * np.cos(np.arctan(perp_slope))
    dy_perp = line_length * np.sin(np.arctan(perp_slope))

    # points used
    x3, y3 = int(midpoint[0] - dx_perp), int(midpoint[1] - dy_perp)
    x4, y4 = int(midpoint[0] + dx_perp), int(midpoint[1] + dy_perp)

    # midline and mask rect
    cv2.line(original, (x3, y3), (x4, y4), (255, 0, 0), 7)
    cv2.rectangle(original, (610, 210), (1390, 890), (0, 0, 0), 1)

    return original



def midpoints(line1lst):
    line1mdarray = []

    for i in line1lst:
        [(x1, y1), (x2, y2)] = i
        midpoint = [(x1 + x2) / 2, (y1 + y2) / 2]
        line1mdarray.append(midpoint)

    total_x, total_y = 0, 0
    num_points = len(line1mdarray)

    for midpoint in line1mdarray:
        total_x += midpoint[0]
        total_y += midpoint[1]

    # no zero division
    if num_points > 0:
        avg_x = total_x / num_points
        avg_y = total_y / num_points
    else:
        avg_x, avg_y = 0, 0

    return (int(avg_x), int(avg_y))


# following code from: https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/

# Open the default camera
cam = cv2.VideoCapture('IMG_5708.MOV')

while True:
    ret, frame = cam.read()
    if ret:
        picture = mainfilter(frame)
        picture2 = houghstuff(picture, frame)

        # Display the captured frame
        cv2.imshow('og', picture)
        cv2.imshow('pic', picture2)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and writer objects
cam.release()
cv2.destroyAllWindows()



