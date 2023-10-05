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
from skimage.filters import threshold_otsu
from skimage import feature



def main():
    print('Reading Images')
    img_dir = os.path.join(os.getcwd(), 'images')
    all_files = os.listdir(img_dir)
    files_unsorted = [str(file[:-4]) for file in all_files if file.endswith('.tif')]
    tif_files = sorted(files_unsorted)
    


    length = len(tif_files)
    mat = np.zeros((512, 512, length+20))

    count = 0
    for file in tqdm(tif_files):
        file_name = "{0}.tif".format(file)
        curr_file = os.path.join(img_dir, file_name)
        curr_img = cv.cvtColor(cv.imread(curr_file), cv.COLOR_BGR2GRAY)

        mat[:, :, count+10] = process_img("zlevel_{0}".format(count), curr_img)
        count += 1
    print('Images Processed')

    print('\n----------\n')

    print('Generating 3D model (this is gonna take a while...)')
    # Use marching cubes to obtain the surface mesh of these ellipsoids
    vertices, triangles = mcubes.marching_cubes(mat, 0)
    mcubes.export_obj(vertices, triangles, "output.obj")

    # print('Converting Model to stl')
    # scene = Scene.from_file("output.obj")
    # scene.save("output.stl")


    print('Generating Smoothed 3D model (this is gonna also take a while...)')
    smoothed_mat = mcubes.smooth(mat, sigma = 1.5)
    vertices, triangles = mcubes.marching_cubes(smoothed_mat, 0)
    mcubes.export_obj(vertices, triangles, "output_sm.obj")

    # print('Converting Smoothed Model to stl')
    # scene = Scene.from_file("tmp/output_sm.obj")
    # scene.save("output_sm.stl")


    print('Program Finished')




    


    

def process_img(name, img):
    thresh = threshold_otsu(img)
    binary = img_as_ubyte(img > thresh)

    edge_sobel = img_as_ubyte(filters.sobel(binary))

    # # lines = probabilistic_hough_line(edge_sobel, threshold=10, line_length=5,
    #                              line_gap=3)
    
    # for line in lines:
    #     p0, p1 = line
    #     plt.plot((p0[0], p1[0]), (p0[1], p1[1]))
    # plt.imshow(edge_sobel)
    # plt.show()
    
    filled_img = img_as_ubyte(binary)
    io.imsave("new_images/{0}.tif".format(name), edge_sobel)

    return edge_sobel



if __name__ == '__main__':
    main()
