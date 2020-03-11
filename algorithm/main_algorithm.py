import rasterio
import numpy as np
from matplotlib import pyplot as plt
import glob
import os

# input files folder path (from which we get all the smaller geotiff files)
dirpath = 'C:/Users/joris/Desktop/Universiteit/Master - Applied Mathematics/Scalable Computing/data/'
# output file path
out_fp = 'C:/Users/joris/Desktop/Universiteit/Master - Applied Mathematics/Scalable Computing/data/'
out_file_name = 'world_population_normalized_'

# search for all the .tif files that start with the letter 'w'
# and save the paths in dem_fps
search_criteria = "w*.tif"
q = os.path.join(dirpath, search_criteria)
dem_fps = glob.glob(q)

# create an empty list for the datafiles that will be part of the mosaic
# and fill it with the geotiff files from dem_fps
src_files = []
for fp in dem_fps:
   src = rasterio.open(fp)
   src_files.append(src)

for i in range(0,(len(dem_fps)-1)):
    print(i)
    with rasterio.open(dem_fps[i]) as src:
        profile = src.profile.copy()
    
        array = src.read(1) + 1
        array[array == (src.nodata + 1)] = 0
        array = np.log10(array+1)
        array = (array - np.min(array))/(np.max(array)-np.min(array))
        array[array==0] = np.nan

        print(out_fp + out_file_name + str(i) + '.tif')

        with rasterio.open(out_fp + out_file_name + str(i) + '.tif', 'w', **profile) as dst:
            dst.write_band(1, array)

