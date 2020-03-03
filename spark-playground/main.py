import pyspark
sc = pyspark.SparkContext('local[*]')
import time

for i in range(100):
    print("heallo world")
    time.sleep(1)

# txt = sc.textFile('file:////usr/share/doc/python/copyright')
# print(txt.count())

# python_lines = txt.filter(lambda line: 'python' in line.lower())
# print(python_lines.count())
