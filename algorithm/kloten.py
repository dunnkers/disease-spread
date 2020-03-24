import rasterio
from rasterio.windows import Window
import numpy as np

src = rasterio.open('D:/Files/Downloads/Geotiffs world population/ppp_2020_1km_Aggregated.tif')

windows = [window for ij, window in src.block_windows()]

window = windows[4000]
data = src.read(1, window=window)

x = np.linspace(0, 256,np.sqrt(16)+1)[0:int(np.sqrt(16))]
grid = np.array(np.meshgrid(x, x))
combinations = grid.T.reshape(-1, 2)
print(combinations)

window1 = Window(window.col_off+128, window.row_off+128, 128, 128)
data1 = src.read(1, window=window1)
print('hellow')