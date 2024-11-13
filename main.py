import cv2
import numpy as np
import cv2 from skimage.metrics
import mean_squared_error,peak_signal_noise_ratio,structural_similarity
import matplotlib.pyplot as plt


manpic = cv2.imread("photos/manface.jpg", cv2.IMREAD_GRAYSCALE)

kernel = np.array([[0, -1, 0],
[-1, 5, -1],
[0, -1, 0]])
sharpened = cv2.filter2D(manpic, -1, kernel)

# cv2.imshow("Original Image", manpic)
# cv2.imshow("Sharpened Image", sharpened)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



#Reading the image
image = cv2.imread(sharpened)
(H, W) = image.shape[:2]
# convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# blur the image
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# Perform the canny operator
canny = cv2.Canny(blurred, 30, 150)

fig,ax =  plt.subplots(1,2,figsize=(18, 18))
ax[0].imshow(gray,cmap='gray')
ax[1].imshow(canny,cmap='gray')
ax[0].axis('off')
ax[1].axis('off')