import rasterio
from shapely import geometry
from rasterio.mask import mask

################
### FUNCTIONS ##
################
# Takes a Rasterio dataset and splits it into squares of dimensions squareDim * squareDim
def splitImageIntoCells(img, filename, squareDim):
    numberOfCellsWide = img.shape[1] // squareDim
    numberOfCellsHigh = img.shape[0] // squareDim
    print(numberOfCellsHigh)
    print(numberOfCellsWide)
    x, y = 0, 0
    count = 0
    for hc in range(numberOfCellsHigh):
        y = hc * squareDim
        print(hc)
        for wc in range(numberOfCellsWide):
            x = wc * squareDim
            geom = getTileGeom(img.transform, x, y, squareDim)
            getCellFromGeom(img, geom, filename, count)
            count = count + 1
    return

# Generate a bounding box from the pixel-wise coordinates using the original datasets transform property
def getTileGeom(transform, x, y, squareDim):
    corner1 = transform * (x, y)
    corner2 = transform * (x + squareDim, y + squareDim)
    return geometry.box(corner1[0], corner1[1],
                        corner2[0], corner2[1])

# Crop the dataset using the generated box and write it out as a GeoTIFF
def getCellFromGeom(img, geom, filename, count):
    crop, cropTransform = mask(img, [geom], crop=True)
    writeImageAsGeoTIFF(crop,
                        cropTransform,
                        img.meta,
                        img.crs,
                        filename+"_"+str(count))

# Write the passed in dataset as a GeoTIFF
def writeImageAsGeoTIFF(img, transform, metadata, crs, filename):
    metadata.update({"driver":"GTiff",
                     "height":img.shape[1],
                     "width":img.shape[2],
                     "transform": transform,
                     "crs": crs})
    with rasterio.open(filename+".tif", "w", **metadata) as dest:
        dest.write(img)

##########################
### SPLIT GEOTIFF FILE ###
##########################
# Open the large geotiff file
directory = 'C:/Users/joris/Desktop/Universiteit/Master - Applied Mathematics/Scalable Computing/test_folder/'
world_population_full = 'ppp_2020_1km_Aggregated.tif'
dataset = rasterio.open(directory + world_population_full)

# Split the large geotiff file into smaller files of dimension dim by dim
dim = 9000 # Splits the world map into 8 small geotiff files
splitImageIntoCells(dataset, "world_population", dim)

