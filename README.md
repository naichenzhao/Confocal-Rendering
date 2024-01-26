# Confocal Rendering Script

A script to generate a 3D model using 2D confocal image slices. Thie code is used to re-construct 2-Photon_Polymerization (2PP) structures from 2D slices before and after being put under compression tests. 

![unnamed](https://github.com/naichenzhao/Confocal-Rendering/assets/49353868/df1fbe0d-d7e9-425a-92e6-31c980c5237e)

---


# Running the code

The Confocal Rendering script is housed within the generate.py python file. To generate the 3D model, use the terminal to run:

```$ python3 generate.py```

All the 2D .tif images should be placed in the `images` directory The program essentially goes through the 'images' directlry and alphabetically reads through all of its .tif files, so only place the images you wish to process in there and ensure they are properly sorted. 

Processed images will be placed in the `processed_images` directory. 

The 3D model will be saced in the main directory into `structure.obj`.

## Arguments

- ``-in_folder`` specifies the input directory from which to read images from. It is set to `images` by default.
- ``-out_folder`` specifies the directory to write post-processed images to. It is set to `processed_images` by default.
-  ``-threshold`` specifies the image threshold. If the max intensity value from an image is less than this value, we will skip processing that image. Set to 40 by default.
-  ``-filename`` specifies the file name of the output .obj file. It is set to `structure` by default.
-  ``-skeletonize`` dicattes whether we want to dkeletonize and re-dialate the model. Can normalize line widths but doesnt always work. It is set to `False` by default.


---


# How the code works

The code is broken into two parts: **Image processing** and **3D model generation** The first pre-processes the images from th

## Image Processing
This part reads the input .tif images from the ``in_folder`` and runs pre-processing to determine where the structure is. It then outputs all of the post-processed images into the ``out_folder``. Do note: This will remove all files in the ``out_folder``, mainly to ensure we do not have collisions between the current iteration and any previous iterations.

The image processing uses the scikit-image machine vision library. The processing pipeline involves:

1. `threshold_yen()` to differentiate the structure from the background of the image. Initially I tried using Otsu thresholding, but in the end, it seemed Yen worked better.
2. `closing()` function to help join any small gaps left by the thresholding.
3. `skeletonize()` the image. Since this software is primarily built for testing wireframe structures and we are mainly focused on seeing how the shape changes, this helps isolate just the features of the image. This is only done if ``-skeletonize`` is set to True
4. `dilation()` the skeleton to make the image thicker. This helps to actually give depth to the image and lets different layers better mesh together. We also assume the beams of the structure are of similar withs, so this helps ensure consistency between the sizing of each of the sturcture's rods. This is only done if ``-skeletonize`` is set to True.

Then, the images are stacked into a 3D numpy array.

## Model Generation
To generate the 3D model, we run the marching [cubes algorithm](https://en.wikipedia.org/wiki/Marching_cubes) on the 3D point array. The code uses an library implementation of the marching cubes algorithm which can be found [here](https://github.com/pmneila/PyMCubes).

Generating the model involves:

1. Use a gaussian blur to smooth the image. This helps get rid of any artifatcs that can ocurr due to the layers not being fully aligned. Moreover, it also helps decrease the complexity of the mode, helping to reduce the file size of the final 3D model.
2. Run Marching Cubes to convert the 3D array to a surface mesh 3D model.
3. Scale the structure vertically to make it a cube. Since the height of the model is calculated based on the number of z-slices available, we potentially run into issues with the image being streched based on how fine the z-resolution is. Thus, we re-scale the height to be the same size as the length/width. For the sake of this part, we assume the initial model was a cube,


---


# Library Dependancies
The software was run and tested using `Python 3.11.5` though it should be backwards compatable with older versions. The required libraries are listed below, all of them can be downloaded through pip
- [os](https://docs.python.org/3/library/os.html) (for file access)
- [numpy](https://numpy.org/) (cause numpy)
- [argparse](https://docs.python.org/3/library/argparse.html) (for parsing command line arguments)
- [tqdm](https://tqdm.github.io/) (for the loading bar)
- [mcubes](https://github.com/pmneila/PyMCubes) (for the implementation of the marching cubes algorithm
- [skimage](https://scikit-image.org/) (for image processing)

