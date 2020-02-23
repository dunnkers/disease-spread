import rasterio
import split_geotiff

raster = rasterio.open('./RGB.byte.tif')

split_geotiff.splitImageIntoCells(raster, "some_file", 100)
