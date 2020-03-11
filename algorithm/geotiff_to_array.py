import rasterio
import numpy as np

directory = 'C:/Users/joris/Desktop/Universiteit/Master - Applied Mathematics/Scalable Computing/data/world_population_5.tif'

with rasterio.open(directory) as src:
    array = src.read(1) + 1
    array[array == (src.nodata + 1)] = 0
    array = np.log10(array+1)
    array = (array - np.min(array))/(np.max(array)-np.min(array))
    array[array==0] = np.nan

x_max = src.width
y_max = src.height
n_y = 100
start_y = 3000
while start_y <= y_max:
    n_x = 100
    start_x = 0
    while start_x <= x_max:
        empty_array = np.zeros((n_x*n_y,3))
        for i in range(start_x, start_x + n_x):
            for j in range(start_y, start_y + n_y):
                xy = src.transform * (i,j)
                empty_array[j - start_y + (n_y)*(i - start_x)][0] = xy[0]
                empty_array[j - start_y + (n_y)*(i - start_x)][1] = xy[1]
                empty_array[j - start_y + (n_y)*(i - start_x)][2] = array[i,j]
        values = [row[2] for row in empty_array]
        if np.all(np.isnan(values)):
            average_location_value = empty_array.mean(axis=0)
        else:
            average_location_value = np.nanmean(empty_array, axis=0) 
        print(average_location_value)
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

print('hello')