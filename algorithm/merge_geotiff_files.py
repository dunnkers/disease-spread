import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import glob
import os

# input files folder path (from which we get all the smaller geotiff files)
dirpath = 'C:/Users/joris/Desktop/Universiteit/Master - Applied Mathematics/Scalable Computing/data/'
# output file path
out_fp = 'C:/Users/joris/Desktop/Universiteit/Master - Applied Mathematics/Scalable Computing/data/merged_world_population.tif'

# search for all the .tif files that start with the letter 'w'
# and save the paths in dem_fps
search_criteria = "w*.tif"
q = os.path.join(dirpath, search_criteria)
dem_fps = glob.glob(q)

# create an empty list for the datafiles that will be part of the mosaic
# and fill it with the geotiff files from dem_fps
src_files_to_mosaic = []
for fp in dem_fps:
   src = rasterio.open(fp)
   src_files_to_mosaic.append(src)

# create the mosaic
mosaic, out_trans = merge(src_files_to_mosaic)

# plot the outcome
# show(mosaic, cmap='terrain')

# write the new file to out_fp
out_meta = src.meta.copy()
out_meta.update({"driver": "GTiff",
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": out_trans,
    "crs": "+proj=utm +zone=35 +ellps=GRS80 +units=m +no_defs "
    }
)
with rasterio.open(out_fp, "w", **out_meta) as dest:
   dest.write(mosaic)