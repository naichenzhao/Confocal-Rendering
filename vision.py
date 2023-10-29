import matplotlib.pyplot as plt
import numpy as np
import scipy
import os
from tqdm import tqdm
import mcubes
import cv2 as cv
from aspose.threed.utilities import Vector3
from aspose.threed.entities import PolygonModifier, Box
from aspose.threed import Scene
from skimage.transform import probabilistic_hough_line
from skimage import filters

from skimage import *
import skimage.io as io
from skimage.filters import *
from skimage.morphology import binary_erosion
from skimage.morphology import (erosion, dilation, opening, closing,  # noqa
                                white_tophat)
from skimage.morphology import black_tophat, skeletonize, convex_hull_image  # noqa
from skimage import feature
from scipy.ndimage.filters import gaussian_filter

import pymesh
from multiprocessing import Pool



'''
Important constants to set:
    IMAGES_FOLDER: Folder we read images from, We will read all .tif foles from folder
    IMAGE_THRESHOLD: Intensity threshold. All images below will be ignored

    E_CONST: Value of kernal size for erosion


    SAVE_STL: Extra step of saving to STL file (File is very large!!!)

'''

# Set the constants below:
IMAGES_FOLDER = 'images'
IMAGE_THRESHOLD = 40

E_CONST = 6

SAVE_STL = False




def main():
    print('Reading Images')

    # Grab all .tif files from active folder
    img_dir = os.path.join(os.getcwd(), IMAGES_FOLDER)
    all_files = os.listdir(img_dir)
    files_unsorted = [str(file[:-4]) for file in all_files if file.endswith('.tif')]
    tif_files = sorted(files_unsorted)
    

    # Pre-process images before constructing 3D model
    length = len(tif_files)
    mat = np.zeros((512, 512, length+20))
    count = 0
    for file in tqdm(tif_files):
        # Read and import image
        file_name = "{0}.tif".format(file)
        curr_file = os.path.join(img_dir, file_name)
        curr_img = cv.cvtColor(cv.imread(curr_file), cv.COLOR_BGR2GRAY)

        # check if image meets minimum threshold
        if(np.max(curr_img) < IMAGE_THRESHOLD):
            continue

        # Process image and add it to the list
        mat[:, :, count+10] = process_img("zlevel_{0}".format(count), curr_img)
        count += 1


    print('Images Processed')
    print("{0} Images processed out of {1} total".format(count, length))


    print('\n----------\n')


    # We are just generating the smoothed mode, the standard one is ignored
        # Generate obj files of models
        #   We use marching cubes to obtain the surface mesh of these ellipsoids
    # print('Generating 3D model (this is gonna take a while...)')
    # vertices, triangles = mcubes.marching_cubes(mat, 0)
    # mcubes.export_obj(vertices, triangles, "output.obj")


    print('Generating Smoothed 3D model (this is gonna take a while...)')
    # Run marching cubes
    smoothed_mat = mcubes.smooth(mat, sigma = 1.5)
    vertices, triangles = mcubes.marching_cubes(smoothed_mat, 0)

    # # Scale Marching Cubes
    scale = count/int(np.max(vertices[:,0]) - np.min(vertices[:,0]))
    vertices[:,0] = vertices[:,0] * scale
    vertices[:,1] = vertices[:,1] * scale

    # Export obj file
    mcubes.export_obj(vertices, triangles, "output_sm.obj")

    
    print('\n----------\n')


    # Convert obj files to stl (Only does it if enabled)
    # if SAVE_STL:
    #     print('Converting Model to stl')
    #     scene = Scene.from_file("output.obj")
    #     scene.save("output.stl")

    #     print('Converting Smoothed Model to stl')
    #     scene = Scene.from_file("tmp/output_sm.obj")
    #     scene.save("output_sm.stl")


    print('Program Finished')





def process_img(name, img):
    # Use an otsu filter to remove background
    thresh =  threshold_yen(img)
    binary = img > thresh

    # Perform closing first
    footprint_close=np.ones((7,7))
    closed = closing(binary, footprint_close)

    # Erode image
    footprint = np.ones((E_CONST, E_CONST))
    eroded = dilation(skeletonize(closed == 1), footprint)
    
    # Apply a strobel edge detection
    # edge_sobel = img_as_ubyte(filters.sobel(eroded))
    
    # Save image and return
    cv.imwrite("new_images/{0}.tif".format(name), img_as_ubyte(eroded))
    return eroded



if __name__ == '__main__':

    # Run main at startup
    main()
