import cv2
import numpy as np
from matplotlib import pyplot as plt



def draw_lines(image, hough_lines):
    for line in hough_lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return image


def roi(image, vertices):
    mask = np.zeros_like(image)
    mask_color = 255
    vertices = vertices.reshape((-1, 1, 2))  # Ensure it's a 2D array with shape (n, 1, 2)
    cv2.fillPoly(mask, [vertices], mask_color)  # Pass vertices as a list of arrays
    cropped_img = cv2.bitwise_and(image, mask)
    return cropped_img
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

def process(img):
    height = img.shape[0]
    width = img.shape[1]

    # Define the ROI vertices based on your specifications
    roi_vertices = np.array([
        [int(width * 0.38), int(height * 0.5)],  # Top-left
        [int(width * 0.6), int(height * 0.5)],  # Top-right
        [int(width * 0.93), int(height * 0.98)], # Bottom-right
        [int(width * 0.15), int(height * 0.98)]  # Bottom-left
    ], dtype=np.int32)

    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.dilate(gray_img, kernel=np.ones((3, 3), np.uint8))

    # Perform Canny edge detection
    canny = cv2.Canny(gray_img, 130, 220)

    # Apply ROI to the Canny edge image
    roi_img = roi(canny, roi_vertices)

    # Debug: Check if ROI mask is working (Show the mask itself)
    cv2.imshow("ROI Mask", roi_img)

    # Draw the ROI polygon on the original image
    cv2.polylines(img, [roi_vertices], isClosed=True, color=(255, 0, 0), thickness=3)

    # Detect lines using Hough Line Transform
    lines = cv2.HoughLinesP(roi_img, 1, np.pi / 180, threshold=10, minLineLength=15, maxLineGap=2)

    # Debug: Check the lines detected
    if lines is not None:
        print(f"Detected {len(lines)} lines.")
    else:
        print("No lines detected.")

    # Draw the detected lines on the original image
    final_img = draw_lines(img, lines)

    return final_img

cap = cv2.VideoCapture("test2 (1).mp4")
arrow = cv2.imread('pink arrow.png', cv2.IMREAD_UNCHANGED)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    try:
        picture = process(frame)
        picture = overlay_arrow(frame, arrow)


        # Show the frame
        cv2.imshow("Frame", picture)

        # Wait for key press (1ms delay to update window)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:
        print(f"Error processing frame: {e}")
        break

cap.release()
cv2.destroyAllWindows()
