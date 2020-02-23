## create and enable python virtual environment

`python3 -m venv ./venv`

`. ./bin/venv/activate`

## install GDAL libraries

From https://github.com/domlysz/BlenderGIS/wiki/How-to-install-GDAL

`sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable`

`sudo apt-get install gdal-bin`

`sudo apt-get install python3-gdal`

`sudo apt-get install python3-numpy`

## install python packages

`pip3 install rasterio`
`pip3 install shapely`

## split GEOTiff

see `example_split.py` to see how to split a GEOTiff file