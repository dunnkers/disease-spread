import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

input_fp = 'C:/Users/joris/Desktop/Universiteit/Master - Applied Mathematics/Scalable Computing/data/world_population_normalized_2.tif'
output_fp = 'C:/Users/joris/Desktop/Universiteit/Master - Applied Mathematics/Scalable Computing/data/world_population_normalized_2_m.tif'

dst_crs = '+proj=latlong' # destination coordinate system

with rasterio.open(input_fp) as src:
    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds)
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height
    })

    with rasterio.open(output_fp, 'w', **kwargs) as dst:
        reproject(
            source=rasterio.band(src, 1),
            destination=rasterio.band(dst, 1),
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=transform,
            dst_crs=dst_crs,
            resampling=Resampling.nearest)