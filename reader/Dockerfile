FROM osgeo/gdal:ubuntu-full-latest

RUN apt-get update && apt-get install -y python3-pip

RUN pip3 install rasterio shapely

ENTRYPOINT /bin/bash