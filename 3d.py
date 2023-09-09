import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Define the 3D Gaussian function
def gaussian_3d(x, y, z, mu=0, sigma=1):
    return np.exp(-((x-mu)**2 + (y-mu)**2 + (z-mu)**2) / (2*sigma**2))


# Generate a 3D grid
x, y, z = np.meshgrid(np.linspace(-1, 1, 30),
                      np.linspace(-1, 1, 30),
                      np.linspace(-1, 1, 30))

# Apply the Gaussian function
data = gaussian_3d(x, y, z)


# Take a slice along the x-axis
slice = data[data.shape[0] // 2, :, :]


plt.imshow(slice, interpolation='nearest', cmap='viridis')
plt.colorbar()
plt.show()
