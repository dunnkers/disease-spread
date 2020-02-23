import rasterio
import time

dataset = rasterio.open("./resources/full_pop_data.tif")

print("reading {} rows and {} columns".format(dataset.height, dataset.width))

values = dataset.read()

print("begin processing...")
count = 0
progress_at = 100000
total_cells = dataset.width * dataset.height

t1 = time.time()
for row in range(dataset.height):
  for col in range(dataset.width):
    coords = dataset.xy(col, row)
    pop_dens = max(values[0][row][col], 0)
    if (pop_dens > 0):
      print("The population density at {} is {}".format(coords, pop_dens))
    count += 1
    if count == progress_at:
      t2 = time.time()
      print("processed {} ({}%) cells in {} seconds. {}% finished".format(progress_at, (count / total_cells) * 100, t2 - t1, ((col + row * col) / total_cells) * 100))
      count = 0
      t1 = time.time()
