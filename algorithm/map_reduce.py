import rasterio
import numpy as np
import matplotlib.pyplot as plt
import functools 

directories = ['C:/Users/joris/Desktop/Universiteit/Master - Mathematics/Scalable Computing/data/world_population_normalized_0.tif',
'C:/Users/joris/Desktop/Universiteit/Master - Mathematics/Scalable Computing/data/world_population_normalized_1.tif',
'C:/Users/joris/Desktop/Universiteit/Master - Mathematics/Scalable Computing/data/world_population_normalized_2.tif',
'C:/Users/joris/Desktop/Universiteit/Master - Mathematics/Scalable Computing/data/world_population_normalized_3.tif',
'C:/Users/joris/Desktop/Universiteit/Master - Mathematics/Scalable Computing/data/world_population_normalized_4.tif',
'C:/Users/joris/Desktop/Universiteit/Master - Mathematics/Scalable Computing/data/world_population_normalized_5.tif',
'C:/Users/joris/Desktop/Universiteit/Master - Mathematics/Scalable Computing/data/world_population_normalized_6.tif',
'C:/Users/joris/Desktop/Universiteit/Master - Mathematics/Scalable Computing/data/world_population_normalized_7.tif']

# function that opens a geotiff file and returns the matrix with normalized value
def open_geotiff_file(fp, file_is_normalized=True):
    with rasterio.open(fp) as src:
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
    return array

# step 1
mapped = list(map(open_geotiff_file, directories))

#step 2:
#reduced = functools.reduce(reducer, mapped)

