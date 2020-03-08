import os

# Make sure you call it before importing pyspark
import findspark
findspark.init() # no parameter means it should use SPARK_HOME
# if doesn't work, try setting to /opt/spark-xxxxxxxx

# Defining the python version to use on the workers
os.environ['PYSPARK_PYTHON'] = '/usr/bin/python'

# Pyspark imports
import pyspark
from pyspark.sql import SparkSession

# For pi test
import random

spark = SparkSession.builder.master('spark://my-spark-master:7077').appName('spark-cluster').getOrCreate()

NUM_SAMPLES = 10

def inside(p):
    x, y = random.random(), random.random()
    return x*x + y*y < 1

count = spark.sparkContext.parallelize(range(0, NUM_SAMPLES)) \
             .filter(inside).count()

print('Pi is roughly {}'.format(4.0 * count / NUM_SAMPLES))

# Pi is roughly 4.0
