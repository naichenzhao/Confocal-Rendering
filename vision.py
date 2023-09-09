import mayavi.mlab as mlab
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

from skimage import *
import skimage.io as io
from skimage.util import *
from skimage.morphology import *

import mayavi.mlab as mlab


def main():
    # Load an example image
    # filename = 'img.tif'
    # img = io.imread(filename)

    img_dir = os.path.join(os.getcwd(), 'images')
    all_files = os.listdir(img_dir)
    tif_files = [file[:-4] for file in all_files if file.endswith('.tif')]

    print(tif_files)


    # for file in tif_files:
    #     file_name = "{0}.tif".format(file)
    #     curr_file = os.path.join(img_dir, file_name)
    #     curr_img = io.imread(curr_file)

    #     print('processing file', file_name)
    #     process_img(file, curr_img)


    # Create a 3D array
    array = np.random.rand(100, 100, 100)

    # Create a figure
    fig = mlab.figure()

    # Create a mesh object
    mesh = mlab.mesh(array)

    # Display the mesh
    mlab.show()
    





    

def process_img(name, img):
    # Contrast stretching
    p2, p98 = np.percentile(img, (2, 98))
    img_str = exposure.rescale_intensity(img, in_range=(p2, p98))

    io.imsave("new_images/{0}.tif".format(name), img_str)

    return img_str



if __name__ == '__main__':
    main()
