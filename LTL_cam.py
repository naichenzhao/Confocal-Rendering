import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


# Load the image
img = cv.imread('img.tif')
gs_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


edges = cv.Canny(2 * gs_img, 10, 30)

# Apply the binary filter
thresh = 16
maxValue = 255
bn_img = cv.threshold(img, thresh, maxValue, cv.THRESH_BINARY)[1]

# automatic thresholding
# bn_img = cv.threshold(gs_img, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)[1]

# Save the binary image
cv.imshow('Image', bn_img)
cv.waitKey(0)

cv.destroyAllWindows()




plt.subplot(1, 2, 1)

img_hist = img.ravel()
plt.hist(img_hist[img_hist > 4], 256)

plt.subplot(1, 2, 2)
plt.hist(bn_img.ravel(), 256)

# plt.show()
