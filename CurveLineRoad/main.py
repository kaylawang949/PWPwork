import numpy as np
import cv2

def mainfilter(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    edges = cv2.Canny(blurred, 120, 80, apertureSize=3)

    kernel = np.ones((41, 41))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    return closed

def midpoints(line1, line2):
    midlist = [[(x1 + x2) // 2, (y1 + y2) // 2]
               for (x1, y1), (x2, y2) in zip((pt[0] for pt in line1), (pt[0] for pt in line2))]

    if len(line1) > 1 and len(line2) > 1:
        midlist.append([(line1[-1][0][0] + line2[-1][0][0]) // 2,
                        (line1[-1][0][1] + line2[-1][0][1]) // 2])

    return np.array(midlist)

def curvedetect(frame):
    mask = frame.copy()
    height, width, _ = mask.shape

    # Define upside-down, slightly narrower, much taller trapezoidal ROI
    roi_vertices = np.array([[(width // 2 - 850, height - 100),
                              (width // 2 + 1800, height - 100),
                              (width // 2 + 850, height - 800),
                              (width // 2 - 300, height - 800)]], dtype=np.int32)

    # Create mask for the trapezoid
    roi_mask = np.zeros_like(mask)
    cv2.fillPoly(roi_mask, roi_vertices, (255, 255, 255))

    masked = cv2.bitwise_and(mask, roi_mask)
    filtered = mainfilter(masked)

    contours, _ = cv2.findContours(filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea)

    if len(contours) >= 2:
        line1 = cv2.approxPolyDP(contours[-1], 6, True)
        line1 = line1[:int(len(line1) / 1.68)]
        cv2.polylines(masked, [line1], False, (0, 255, 0), 7, lineType=cv2.LINE_AA)

        line2 = cv2.approxPolyDP(contours[-2], 6, True)
        line2 = line2[:int(len(line2) / 1.68)]
        cv2.polylines(masked, [line2], False, (0, 255, 0), 7, lineType=cv2.LINE_AA)

        midlist2 = midpoints(line1, line2)

    cv2.polylines(mask, roi_vertices, isClosed=True, color=(0, 0, 255), thickness=2)

    return mask

def overlay_arrow(frame, arrow):
    arrow_height, arrow_width, _ = arrow.shape
    arrow_height = int(arrow_height * 0.2)
    arrow_width = int(arrow_width * 0.2)
    arrow = cv2.resize(arrow, (arrow_width, arrow_height))

    arrow_bgr = arrow[:, :, :3]
    arrow_alpha = arrow[:, :, 3]

    roi = frame[10:10 + arrow_height, -arrow_width - 10:-10]
    mask = arrow_alpha.astype(float) / 255.0

    for x in range(3):
        roi[:, :, x] = (mask * arrow_bgr[:, :, x] + (1 - mask) * roi[:, :, x])

    return frame

cam = cv2.VideoCapture('Screen Recording 2025-02-19 at 9.36.29 AM.mov')
arrow = cv2.imread('pink arrow.png', cv2.IMREAD_UNCHANGED)

while True:
    ret, frame = cam.read()
    if ret:
        picture = curvedetect(frame)
        picture = overlay_arrow(picture, arrow)

        cv2.imshow('lines', picture)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
