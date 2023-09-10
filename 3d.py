import meshlib.mrmeshpy as mr
import os
settings = mr.LoadingTiffSettings()

# load images from specified directory
img_dir = os.path.join(os.getcwd(), 'new_images')
settings.dir = img_dir

# specifiy size of 3D image element
settings.voxelSize = mr.Vector3f(0.1, 0.1, 0.5)

#create voxel object from the series of images
volume = mr.loadTiffDir(settings)

#define ISO value to build surface
iso=127

#convert voxel object to mesh
mesh=mr.gridToMesh(volume, iso)

#save mesh to .stl file
res_dir = os.path.join(os.getcwd(), 'out.stl')
mr.saveMesh(mesh, res_dir)