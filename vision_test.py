import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

from skimage import *
import plotly.express as px
import skimage.io
from skimage import data
from skimage.filters import threshold_otsu


matplotlib.rcParams['font.size'] = 8


def plot_img_and_hist(image, axes, bins=256):
    """Plot an image along with its histogram and cumulative histogram.

    """
    image = img_as_float(image)
    ax_img, ax_hist = axes
    ax_cdf = ax_hist.twinx()

    # Display image
    ax_img.imshow(image, cmap=plt.cm.gray)
    ax_img.set_axis_off()

    # Display histogram
    ax_hist.hist(image.ravel(), bins=bins, histtype='step', color='black')
    ax_hist.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    ax_hist.set_xlabel('Pixel intensity')
    ax_hist.set_xlim(0, 1)
    ax_hist.set_yticks([])

    # Display cumulative distribution
    img_cdf, bins = exposure.cumulative_distribution(image, bins)
    ax_cdf.plot(bins, img_cdf, 'r')
    ax_cdf.set_yticks([])

    return ax_img, ax_hist, ax_cdf


def otsu(image):
    thresh = threshold_otsu(image)
    binary = image > thresh

    fig, axes = plt.subplots(ncols=3, figsize=(8, 2.5))
    ax = axes.ravel()
    ax[0] = plt.subplot(1, 3, 1)
    ax[1] = plt.subplot(1, 3, 2)
    ax[2] = plt.subplot(1, 3, 3, sharex=ax[0], sharey=ax[0])

    ax[0].imshow(image, cmap=plt.cm.gray)
    ax[0].set_title('Original')
    ax[0].axis('off')

    ax[1].hist(image.ravel(), bins=256)
    ax[1].set_title('Histogram')
    ax[1].axvline(thresh, color='r')

    ax[2].imshow(binary, cmap=plt.cm.gray)
    ax[2].set_title('Thresholded')
    ax[2].axis('off')

    plt.show()


def local_otsu(image):
    global_thresh = threshold_otsu(image)

    binary_global = image > global_thresh

    block_size = 101
    local_thresh = threshold_local(image, block_size, offset=10)
    binary_local = image > local_thresh

    fig, axes = plt.subplots(nrows=3, figsize=(7, 8))
    ax = axes.ravel()
    plt.gray()

    ax[0].imshow(image)
    ax[0].set_title('Original')

    ax[1].imshow(binary_global)
    ax[1].set_title('Global thresholding')

    ax[2].imshow(binary_local)
    ax[2].set_title('Local thresholding')

    for a in ax:
        a.axis('off')

    plt.show()


def local_otsu_rank(img):
    radius = 15
    footprint = disk(radius)

    local_otsu = rank.otsu(img, footprint)
    threshold_global_otsu = threshold_otsu(img)
    global_otsu = img >= threshold_global_otsu

    fig, axes = plt.subplots(2, 2, figsize=(8, 5), sharex=True, sharey=True)
    ax = axes.ravel()
    plt.tight_layout()

    fig.colorbar(ax[0].imshow(img, cmap=plt.cm.gray),
                 ax=ax[0], orientation='horizontal')
    ax[0].set_title('Original')
    ax[0].axis('off')

    fig.colorbar(ax[1].imshow(local_otsu, cmap=plt.cm.gray),
                 ax=ax[1], orientation='horizontal')
    ax[1].set_title(f'Local Otsu (radius={radius})')
    ax[1].axis('off')

    ax[2].imshow(img >= local_otsu, cmap=plt.cm.gray)
    ax[2].set_title('Original >= Local Otsu')
    ax[2].axis('off')

    ax[3].imshow(global_otsu, cmap=plt.cm.gray)
    ax[3].set_title('Global Otsu (threshold = {threshold_global_otsu})')
    ax[3].axis('off')

    plt.show()


# Load an example image
filename = 'img.tif'
img = skimage.io.imread(filename)

# Contrast stretching
p2, p98 = np.percentile(img, (2, 98))
img_rescale = exposure.rescale_intensity(img, in_range=(p2, p98))

# Equalization
img_eq = exposure.equalize_hist(img)

# Adaptive Equalization
img_adapteq = exposure.equalize_adapthist(img, clip_limit=0.03)

# Display results
fig = plt.figure(figsize=(8, 5))
axes = np.zeros((2, 4), dtype=object)
axes[0, 0] = fig.add_subplot(2, 4, 1)
for i in range(1, 4):
    axes[0, i] = fig.add_subplot(
        2, 4, 1+i, sharex=axes[0, 0], sharey=axes[0, 0])
for i in range(0, 4):
    axes[1, i] = fig.add_subplot(2, 4, 5+i)

ax_img, ax_hist, ax_cdf = plot_img_and_hist(img, axes[:, 0])
ax_img.set_title('Low contrast image')

y_min, y_max = ax_hist.get_ylim()
ax_hist.set_ylabel('Number of pixels')
ax_hist.set_yticks(np.linspace(0, y_max, 5))

ax_img, ax_hist, ax_cdf = plot_img_and_hist(img_rescale, axes[:, 1])
ax_img.set_title('Contrast stretching')

ax_img, ax_hist, ax_cdf = plot_img_and_hist(img_eq, axes[:, 2])
ax_img.set_title('Histogram equalization')

ax_img, ax_hist, ax_cdf = plot_img_and_hist(img_adapteq, axes[:, 3])
ax_img.set_title('Adaptive equalization')

ax_cdf.set_ylabel('Fraction of total intensity')
ax_cdf.set_yticks(np.linspace(0, 1, 5))

# prevent overlap of y-axis labels
fig.tight_layout()
plt.show()
