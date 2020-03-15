import os
import findspark
findspark.init()

# Defining the python version to use on the workers
os.environ['PYSPARK_PYTHON'] = '/usr/bin/python'

import pyspark
from pyspark import SparkContext
sc = SparkContext("spark://my-spark-master:7077", "Pi Leibniz")
iteration=10000
partition=4
data = range(0,iteration)
distIn = sc.parallelize(data,partition)
result=distIn.map(lambda n:(1 if n%2==0 else -1)/float(2*n+1)).reduce(lambda a,b: a+b)
print("Pi is %f" % (result*4))