import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np
import matplotlib.pyplot as plt

directory = 'C:/Users/joris/Desktop/Universiteit/Master - Applied Mathematics/Scalable Computing/data/world_population_complete_normalized.tif'
file_is_normalized = True

with rasterio.open(directory) as src:
    if file_is_normalized:
        array = src.read(1)
    else:
        array = src.read(1) + 1
        array[array == (src.nodata + 1)] = 0
        array = np.log10(array+1)
        array = (array - np.min(array))/(np.max(array)-np.min(array))
        array[array==0] = np.nan
    print('data is imported and pre-processed')

plt.imshow(array, cmap='Greys')
plt.show()

x_max = src.width
y_max = src.height
n_x_start = 100
n_y_start = 100

# initialize empty array
size = np.ceil(x_max/n_x_start)*np.ceil(y_max/n_y_start)
average_location_values = np.array(np.zeros((np.int(size),3)))

n_y = n_y_start
start_y = 0
i = 0
while start_y <= y_max:
    n_x = n_x_start
    start_x = 0
    while start_x <= x_max:
        average_xy = (np.array(src.transform * (start_x,start_y)) + np.array(src.transform * (start_x + n_x,start_y + n_y))) / 2.0
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

plt.scatter(-y, -x, c=z, s=5)
plt.colorbar()
plt.show()
