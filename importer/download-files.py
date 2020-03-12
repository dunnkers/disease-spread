import shutil
import urllib.request as request
from contextlib import closing

year = 2020
with closing(request.urlopen('ftp://ftp.worldpop.org.uk/GIS/Population/Global_2000_2020/{}/0_Mosaicked/ppp_{}_1km_Aggregated.tif'.format(year, year))) as r:
    with open('{}_pop.tif'.format(year), 'wb') as f:
        shutil.copyfileobj(r, f)
