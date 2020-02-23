## Create and enable python virtual environment

`python3 -m venv ./venv`

`. ./bin/venv/activate`

## Install GDAL libraries

From https://github.com/domlysz/BlenderGIS/wiki/How-to-install-GDAL

`sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable`

`sudo apt-get install gdal-bin`

`sudo apt-get install python3-gdal`

`sudo apt-get install python3-numpy`

## Install python packages

`pip3 install rasterio`
`pip3 install shapely`

## Split GEOTiff

Example of how to split a GEOTiff file.

```python
import rasterio
import split_geotiff

dataset = rasterio.open('path/to/file.tif')

split_geotiff.splitImageIntoCells(dataset, "some_file_name", 10)
```

This will create `n = ceil(dataset.width / 10) * ceil(dataset.height / 10)` images, named `some_file_name_0`...`some_file_name_n`.

## Using the data

_The source for this part can be found [here](https://rasterio.readthedocs.io/en/latest/quickstart.html) (quickstart)_

use `dataset = rasterio.open()` to open a file and get a dataset object. 

The dataset object contains metadata such as the coordinate reference system (CRS), amount of data (`width` and `height`) and the transformation used. 

The transformation is especially important, as it translates row/column indices to coordinates within the CRS. However, the dataset also has a method to do this translation, `dataset.xy(col, row)`.

The data in GEOTiff image is organized in bands. These bands each represent a certain datatype. In an RGB image, there would be three bands, one for red, one for green and one for blue. Each band then consists of a `height` * `width` 2-D array of intensity values.

Our data consists of a a single band, approximately 20000 * 40000 pixels of 1km * 1km.

Example to print the population density per 1km * 1km square:

```python
import rasterio

dataset = rasterio.open("path/to/file.tif")

values = dataset.read()

for row in range(dataset.height):
  for col in range(dataset.width):
    coords = dataset.xy(col, row)
    pop_dens = values[row][col]
    print("The population density at {} is {}".format(coords, pop_dens))
```

## Using the Docker container

To build the container (while the current working directory is the directory containing the Dockerfile) run `./build.sh`.

To run the container and start a shell in the container run `./shell`.
