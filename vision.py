import matplotlib.pyplot as plt
import numpy as np
import os
import meshlib.mrmeshpy as mr

from skimage import *
import skimage.io as io
from skimage.filters import threshold_otsu
from skimage import data, filters


def main():
    # Load an example image
    # filename = 'img.tif'
    # img = io.imread(filename)

    img_dir = os.path.join(os.getcwd(), 'images')
    all_files = os.listdir(img_dir)

    files_unsorted = [str(file[:-4]) for file in all_files if file.endswith('.tif')]

    tif_files = sorted(files_unsorted)
    print(tif_files)

    print('Finished flagging files')
    count = 0

    for file in tif_files:
        file_name = "{0}.tif".format(file)
        curr_file = os.path.join(img_dir, file_name)
        curr_img = io.imread(curr_file)

        print('processing file', "img_{count}")
        process_img(file, curr_img)
        count += 1
    
    print('Processing Images')




    # Create a 3D stl file
    settings = mr.LoadingTiffSettings()

    # load images from specified directory
    img_dir = os.path.join(os.getcwd(), 'new_images')
    settings.dir = img_dir

    # specifiy size of 3D image element
    settings.voxelSize = mr.Vector3f(1, 1, 1)

    #create voxel object from the series of images
    volume = mr.loadTiffDir(settings)

    #define ISO value to build surface
    iso=10

    #convert voxel object to mesh
    mesh=mr.gridToMesh(volume, iso)

    #save mesh to .stl file
    res_dir = os.path.join(os.getcwd(), 'out.stl')
    mr.saveMesh(mesh, res_dir)


    print('Finished 3D Model')

    





    

def process_img(name, img):
    # Contrast stretching
    p2, p98 = np.percentile(img, (2, 98))
    img_str =  img_as_ubyte(exposure.rescale_intensity(img, in_range=(p2, p98)))

    thresh = threshold_otsu(img_str)
    binary = img_str > thresh

    # edges = filters.sobel(img_str)

    # low = 0.1
    # high = 0.35

    # lowt = (edges > low).astype(int)
    # hight = (edges > high).astype(int)
    # hyst = filters.apply_hysteresis_threshold(edges, low, high)


    save_img = binary

    io.imsave("new_images/{0}.tif".format(name), save_img)

    return img_str



if __name__ == '__main__':
    main()
