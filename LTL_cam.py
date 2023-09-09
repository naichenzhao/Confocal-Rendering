import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


img = cv.imread('img.tif')



# Using a 2D filter
kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

kernel2 = np.array([[-1, -1, -1],
                    [-1, 5, -1],
                    [-1, -1, -1]])


img_2df = cv.filter2D(img, -1, kernel)

# adding gaussian blur
blur = cv.GaussianBlur(img, (3, 3), 0)
blur_2df = cv.filter2D(blur, -1, kernel)


df_thresh = cv.threshold(img_2df, 20, 255, cv.THRESH_BINARY)[1]
blur_thresh = cv.threshold(blur_2df, 20, 255, cv.THRESH_BINARY)[1]

Hori = np.concatenate((img, df_thresh, blur_thresh), axis=1)


cv.imshow('Image', Hori)
cv.waitKey(0)
cv.destroyAllWindows()


plt.hist(blur_2df.ravel(), 256, alpha=0.5, label='filtered')
plt.hist(img_2df.ravel(), 256, alpha=0.5, label='2df')
plt.hist(img.ravel(), 256, alpha=0.5, label='original')
plt.legend(loc='upper right')
plt.show()





















# Hori = np.concatenate((edges, edges2), axis = 1)


# # cv.imshow('Image', Hori)
# # cv.waitKey(0)
# # cv.destroyAllWindows()

# # try and highlight lines
# rho = 1  # distance resolution in pixels of the Hough grid
# theta = np.pi / 180  # angular resolution in radians of the Hough grid
# threshold = 15  # minimum number of votes (intersections in Hough grid cell)
# min_line_length = 50  # minimum number of pixels making up a line
# max_line_gap = 20  # maximum gap in pixels between connectable line segments
# line_image = np.copy(img) * 0  # creating a blank to draw lines on

# # # Run Hough on edge detected image
# # # Output "lines" is an array containing endpoints of detected line segments
# # lines = cv.HoughLinesP(edges, rho, theta, threshold, np.array([]),
# #                         min_line_length, max_line_gap)

# # for line in lines:
# #     for x1, y1, x2, y2 in line:
# #         cv.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 1)

# # lines_edges = cv.addWeighted(img, 0.1, line_image, 1, 0)


# # # concatenate image Horizontally
# # Hori = np.concatenate((cv.cvtColor(edges, cv.COLOR_GRAY2RGB), lines_edges), axis=1)

# # cv.imshow('Image', Hori)
# # cv.waitKey(0)
# # cv.destroyAllWindows()

# # # Load the image
# # img = cv.imread('img.tif')
# # gs_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


# # edges = cv.Canny(2 * gs_img, 10, 30)

# # # Apply the binary filter
# # thresh = 16
# # maxValue = 255
# # bn_img = cv.threshold(img, thresh, maxValue, cv.THRESH_BINARY)[1]

# # # automatic thresholding
# # # bn_img = cv.threshold(gs_img, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)[1]

# # # Save the binary image
# # cv.imshow('Image', bn_img)
# # cv.waitKey(0)

# # cv.destroyAllWindows()




# # plt.subplot(1, 2, 1)

# # img_hist = img.ravel()
# # plt.hist(img_hist[img_hist > 4], 256)

# # plt.subplot(1, 2, 2)
# # plt.hist(bn_img.ravel(), 256)

# # # plt.show()
