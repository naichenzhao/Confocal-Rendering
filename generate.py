import numpy as np
import os
import argparse
from tqdm import tqdm
import mcubes
import cv2 as cv

from skimage import *
import skimage.io as io
from skimage.filters import *
from skimage.morphology import *
from skimage.morphology import skeletonize
from skimage import feature

import pymesh
from multiprocessing import Pool



'''
Important constants to set:
    CLOSE_CONST: Value of kernal size for close function
    DIALATE_CONST: Value of kernal for dialation of skeleton

    
Structure Generation Pipeline:
    1) Image processing
        - Use Yen Thresholding to differentiate the structure from the background
        - Use close to get rid of any small disconnects
        - Skeletonize to get the basic features/shapes of the structure
        - Dialate the skeleton to give the stucture depth
        - Saves the data into a 3D numpy array
    
    2) Model generation
        - Use gaussian blur to smooth out the structure (helps make obj file smaller and makes it look nicer)
        - Use marching cubes to generate a .obj file and save it

'''

# Set the constants below:
CLOSE_CONST = 7
DIALATE_CONST = 6


# Main function
def main():

    # =========================================
    #   Interpret Arguments
    # =========================================

    # Parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('-in_folder', '-i', type=str, default='images', 
                        help= 'Input folder to read all .tif files from'
    )
    parser.add_argument('-out_folder', '-o', type=str, default='processed_images', 
                        help= 'Output folder to save post-processed images to'
    )
    parser.add_argument('-threshold', '-t', type=int, default=40, 
                        help= 'Image threshold. If max value from an image does not exceed this, the image is thrown out'
    )
    parser.add_argument('-filename', '-f', type=str, default='structure', 
                        help= 'Name for the .obj output file'
    )
    args = parser.parse_args()

    images_folder = args.in_folder
    output_folder = args.out_folder

    image_threshold = args.threshold
    output_name = args.filename


    # =========================================
    #   Run Loop
    # =========================================
    print('Reading Images')

    # Process images
    struct_matrix, length = process(images_folder, output_folder, image_threshold)

    print('\n----------\n')

    # Generate 3D model
    generate(struct_matrix, length, output_name)

    print('Program Finished')



# Function for generating a model from a 3D array
def generate(matrx, length, name):
    print('Generating 3D model (this is gonna take a while...)')

    # Smooth images
    print('   ... Smoothing model')
    smoothed_mat = mcubes.smooth(matrx, sigma = 1.5)

    # Run marching cubes
    print('   ... Running marching cubes')
    vertices, triangles = mcubes.marching_cubes(smoothed_mat, 0)

    # Scale Marching Cubes output to be square 
    print('   ... Scaling output model')
    scale = length/int(np.max(vertices[:,0]) - np.min(vertices[:,0]))
    vertices[:,0] = vertices[:,0] * scale
    vertices[:,1] = vertices[:,1] * scale

    # Export obj file
    print('   ... Saving structure')
    mcubes.export_obj(vertices, triangles, "{0}.obj".format(name))



# Process imaged from images folder
def process(in_folder, out_folder, threshold):
    print('   ... Grabbing images from input folder: {0}'.format(in_folder))

    # Grab all .tif files from active folder
    img_dir = os.path.join(os.getcwd(), in_folder)
    all_files = os.listdir(img_dir)
    files_unsorted = [str(file[:-4]) for file in all_files if file.endswith('.tif')]
    tif_files = sorted(files_unsorted) 

    # Empty the output folder. This useful for flushing the previous run's files
    print('   ... Emptying output folder: {0}'.format(out_folder))
    for f in os.listdir(out_folder):
        os.remove(str(out_folder) + "/" + f)

    # Pre-process images before constructing 3D model
    length = len(tif_files)
    mat = np.zeros((512, 512, length+20))

    # Process images from folder
    count = 0 # counter for number of images processed
    print('   ... Starting image processing loop')
    for file in tqdm(tif_files):
        # Read and import image
        file_name = "{0}.tif".format(file)
        curr_file = os.path.join(img_dir, file_name)
        curr_img = cv.cvtColor(cv.imread(curr_file), cv.COLOR_BGR2GRAY)

        # check if image meets minimum threshold. If it doesnt, we skip it
        if(np.max(curr_img) < threshold):
            continue

        # Process image and add it to the list
        processed_image = process_img(curr_img)
        mat[:, :, count+10] = processed_image

        # Write image into output file
        cv.imwrite("{0}/{1}.tif".format(out_folder, "zlevel_{0}".format(count)), processed_image)
        count += 1

    print('Images Processed')
    print("{0} Images processed out of {1} total".format(count, length))
    return mat, count



# Code from processing a simgular image
def process_img(img):
    # Use an yen filter to remove background 
    #   (Initially I tried otsu, yen seems better from what I tested)
    thresh =  threshold_yen(img)
    binary = img > thresh

    # Perform closing first
    footprint_close=np.ones((CLOSE_CONST, CLOSE_CONST))
    closed = closing(binary, footprint_close)

    # Erode image
    footprint = np.ones((DIALATE_CONST, DIALATE_CONST))
    eroded = dilation(skeletonize(closed == 1), footprint)
    
    # Return image
    return img_as_ubyte(eroded)


if __name__ == '__main__':

    # Run main at startup
    main()
