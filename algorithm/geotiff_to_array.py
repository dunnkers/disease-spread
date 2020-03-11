import rasterio
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

# local directory from where we import the geotiff file
directory = 'C:/Users/joris/Desktop/Universiteit/Master - Mathematics/Scalable Computing/data/world_population_normalized_m.tif'
file_is_normalized = True

with rasterio.open(directory) as src:
    # if the file is normalized the values are already scaled, normalized, etc.
    if file_is_normalized:
        array = src.read(1)
    else:
        # datapoints values run from 0 to ~70000, nodata points have value -10^38
        array = src.read(1) + 1  # translate the datapoints by 1
        array[array == (src.nodata + 1)] = 0 # set nodata points to 0
        array = np.log10(array+1) # rescale all points to log10
        array = (array - np.min(array))/(np.max(array)-np.min(array)) # normalize all points
        # Note that now the data points are larger than 0 and the nodata points are equal to 0
        array[array==0] = np.nan  # set nodata points back to nan (so they won't be plotted)
    print('data is imported and pre-processed')

# There are too many data points, so we compress the large matrix into smaller blocks
# And take the average longitude and latitude and population value per block
x_max = array.shape[0] # length of matrix in x-direction
y_max = array.shape[1] # length of matrix in y-direction
n_x_start = 50 # size of blocks in x-direction
n_y_start = 50 # size of blocks in y-direction

# initialize empty array
size = np.ceil(x_max/n_x_start)*np.ceil(y_max/n_y_start)
average_location_values = np.array(np.zeros((np.int(size),3)))

# Loop over the map until the blocks have reached the end
# the result is a 2d array where each element is of the form (x,y,z)
# x is the longitude, y is the latitude, z is the population value
n_y = n_y_start
start_y = 0 
i = 0
while start_y <= y_max:
    n_x = n_x_start
    start_x = 0
    while start_x <= x_max:
        average_xy = (np.array(src.transform * (start_y,start_x)) + np.array(src.transform * (start_y + n_y,start_x + n_x))) / 2.0
        values_matrix = array[start_x:(start_x+n_x), start_y:(start_y+n_y)]
        if np.all(np.isnan(values_matrix)):
            average_z = np.nan
        else:
            average_z = np.nanmean(values_matrix)
        average_location_values[i][0] = average_xy[0]
        average_location_values[i][1] = average_xy[1]
        average_location_values[i][2] = average_z
        i = i + 1
        start_x = start_x + n_x
        if(start_x + n_x > x_max - 1):
            n_x = x_max - start_x - 1
        if(start_x == x_max - 1): 
            start_x = x_max + 1
    start_y = start_y + n_y
    if(start_y + n_y > y_max - 1):
        n_y = y_max - start_y - 1
    if(start_y == y_max - 1): 
        break


x = np.array([row[0] for row in average_location_values])
y = np.array([row[1] for row in average_location_values])
z = np.array([row[2] for row in average_location_values])
z = (z - np.nanmin(z)) / (np.nanmax(z) - np.nanmin(z))

plt.scatter(x, y, c=z, s=5, cmap='Reds')
plt.colorbar()
plt.show()
