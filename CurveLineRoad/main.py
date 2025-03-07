import cv2
import numpy as np

# filter out flat lines
SLOPE_THRESHOLD = 0.5  # adjustable

# function for roi
def draw_roi(frame, roi_points):
    cv2.polylines(frame, [roi_points], isClosed=True, color=(0, 0, 0), thickness=1)
    return frame

def process_frame(frame, arrow, frame_count):
    height, width = frame.shape[:2]

    # define adjustable roi
    roi_points = np.array([
        [0.3 * width, height * 0.8],  # bottom left
        [0.4 * width, 0.5 * height],  # left midpoint
        [0.6 * width, 0.5 * height],  # right midpoint
        [0.9 * width, height * 0.8]  # bottom right
    ], np.int32)

    # draw roi
    frame = draw_roi(frame, roi_points)

    # make roi mask
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, [roi_points], (255, 255, 255))

    # apply mask
    roi_frame = cv2.bitwise_and(frame, mask)

    # convert to grayscale
    gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

    # apply gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # apply canny edge
    edges = cv2.Canny(blurred, 50, 150)

    # apply hough lines
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=100, maxLineGap=50)

    if lines is not None:

        left_lines = []
        right_lines = []

        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1) if x2 != x1 else float('inf')

            # filter based on slope threshold
            if abs(slope) > SLOPE_THRESHOLD:
                if slope < 0:  # left lines (negative slope)
                    left_lines.append(line[0])
                else:  # right lines (positive slope)
                    right_lines.append(line[0])

        # extend the left and right lines
        y_bottom = int(height * 0.9)
        y_top = int(height * 0.55)

        # extend the lines for left and right lanes
        def extend_line(line, y1, y2):
            x1, y1_, x2, y2_ = line
            if x1 == x2:
                return [(x1, y1), (x1, y2)]
            else:
                slope = (y2_ - y1_) / (x2 - x1)
                intercept = y1_ - slope * x1
                if slope != 0:
                    x1_new = int((y1 - intercept) / slope)
                    x2_new = int((y2 - intercept) / slope)
                    return [(x1_new, y1), (x2_new, y2)]
                else:
                    return [(x1, y1), (x2, y2)]

        left_extended = [extend_line(line, y_top, y_bottom) for line in left_lines]
        right_extended = [extend_line(line, y_top, y_bottom) for line in right_lines]

        # average line endpoints
        def average_lines(lines):
            if len(lines) == 0:
                return None
            x1_avg = int(np.mean([line[0][0] for line in lines]))
            x2_avg = int(np.mean([line[1][0] for line in lines]))
            return [(x1_avg, y_top), (x2_avg, y_bottom)]

        left_lane = average_lines(left_extended)
        right_lane = average_lines(right_extended)

        # draw lanes
        if left_lane is not None:
            cv2.line(frame, left_lane[0], left_lane[1], (0, 255, 0), 5)
        if right_lane is not None:
            cv2.line(frame, right_lane[0], right_lane[1], (0, 255, 0), 5)

    # overlay arrow
    frame = overlay_arrow(frame, arrow, frame_count)

    return frame

def rotate_arrow(arrow, angle):
    height, width = arrow.shape[:2]
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_arrow = cv2.warpAffine(arrow, rotation_matrix, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    return rotated_arrow

def overlay_arrow(frame, arrow, frame_count):
    arrow_height, arrow_width, _ = arrow.shape
    arrow_height = int(arrow_height * 0.2)
    arrow_width = int(arrow_width * 0.2)
    arrow = cv2.resize(arrow, (arrow_width, arrow_height))
    
    if 500 <= frame_count < 650:  # 20s to 25s
        arrow = rotate_arrow(arrow, -90)
    elif 1450 <= frame_count < 1600:  # 60s to 65s
        arrow = rotate_arrow(arrow, 90)

    arrow_bgr = arrow[:, :, :3]
    arrow_alpha = arrow[:, :, 3]

    roi = frame[10:10 + arrow_height, -arrow_width - 10:-10]
    mask = arrow_alpha.astype(float) / 255.0

    for x in range(3):
        roi[:, :, x] = (mask * arrow_bgr[:, :, x] + (1 - mask) * roi[:, :, x])

    return frame

cap = cv2.VideoCapture('My Movie 7.MOV')
arrow = cv2.imread("pink arrow.png", cv2.IMREAD_UNCHANGED)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame = process_frame(frame, arrow, frame_count)

    cv2.imshow('Lane Detection', processed_frame)

    frame_count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
