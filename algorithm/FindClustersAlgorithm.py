# Spark dependencies
import pyspark

import pyspark.sql.functions as f
from pyspark import SparkContext
from pyspark.sql import SparkSession

from pyspark.sql.functions import lit, udf
from pyspark.sql.functions import log10
from pyspark.sql.functions import isnan, when, count, col

from pyspark.sql.types import ArrayType
from pyspark.sql.types import FloatType

from pyspark.ml import Pipeline

from pyspark.ml.clustering import KMeans

from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import MinMaxScaler
from pyspark.ml.feature import Normalizer

# Miscellaneous dependencies
import numpy as np
import os
from matplotlib import pyplot as plt
import json
import math

# user defined functions
def ith_(v, i):
    try:
        return float(v[i])
    except ValueError:
        return None

ith = udf(ith_, FloatType()) # unlist a vector
unlist = udf(lambda x: round(float(list(x)[0]),3), FloatType()) # converting column type from vector to double type
log10_udf = udf(lambda y: np.log10(y), FloatType()) # unlist a vector
take_first_udf = udf(lambda y: y[0], FloatType()) # take first element of a list
take_second_udf = udf(lambda y: y[1], FloatType()) # take second element of a list

password = os.getenv('MONGODB_ROOT_PASSWORD')
mongoUri = 'mongodb://root:{}@my-mongodb:27017'.format(password)

spark = SparkSession     .builder     .appName("PySparkPopulationAlgorithm")     .config("spark.mongodb.input.uri", mongoUri)     .config("spark.mongodb.output.uri", mongoUri)     .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.4.1')     .getOrCreate()
sc = spark.sparkContext

df = spark     .read     .format("com.mongodb.spark.sql.DefaultSource")     .option("database", "geotest-db")     .option("collection", "2020_pop_128_geojson")     .load()

# Put mongo data in dataframe
data = df.select("geometry.coordinates", "properties.pop", "properties.old_females")

# Transform the dataframe into three columns: x,y,z
df1 = data.select(       take_first_udf('coordinates').alias('lon'),       take_second_udf('coordinates').alias('lat'),       data.pop.cast(FloatType()).alias('pop'),       data.old_females.cast(FloatType()).alias('granny'))

# count number of null or na value in df1
#df1.select([count(when(isnan(c) | col(c).isNull(), c)).alias(c) for c in df1.columns]).show()

# replace all null or na value with 0
df1 = df1.na.fill(0)


# prepare dataframe for K means clustering
FEATURES_COL = ['lon', 'lat', 'pop', 'granny']
FEATURES_COL_pop = ['lon', 'lat', 'pop']
FEATURES_COL_granny = ['lon', 'lat', 'granny']
vecAssembler = VectorAssembler(inputCols=FEATURES_COL, outputCol="features")
vecAssembler_pop = VectorAssembler(inputCols=FEATURES_COL_pop, outputCol="features")
vecAssembler_granny = VectorAssembler(inputCols=FEATURES_COL_granny, outputCol="features")
df_kmeans = vecAssembler.transform(df1).select('features')
df_kmeans_pop = vecAssembler_pop.transform(df1).select('features')
df_kmeans_granny = vecAssembler_granny.transform(df1).select('features')

# K means clustering
k = 15
kmeans = KMeans().setK(k).setSeed(1).setFeaturesCol("features")
model = kmeans.fit(df_kmeans)
model_pop = kmeans.fit(df_kmeans_pop)
model_granny = kmeans.fit(df_kmeans_granny)
centers = model.clusterCenters()
centers_pop = model_pop.clusterCenters()
centers_granny = model_granny.clusterCenters()
df_tags = model.transform(df_kmeans)
df_tags_pop = model_pop.transform(df_kmeans_pop)
df_tags_granny = model_granny.transform(df_kmeans_granny)

# find the largest value in the centers array
center_sorted = sorted(centers, key=lambda x: x[2], reverse=True)
center_sorted_pop = sorted(centers_pop, key=lambda x: x[2], reverse=True)
center_sorted_granny = sorted(centers_granny, key=lambda x: x[2], reverse=True)
z = np.array([row[2] for row in centers])
z_pop = np.array([row[2] for row in centers_pop])
z_granny = np.array([row[2] for row in centers_granny])
n = 7
if n<k:
    indices = np.zeros(n)
    indices_pop = np.zeros(n)
    indices_granny = np.zeros(n)
    for i in range(0,n):
        indices[i] = np.where(center_sorted[i][2]==z)[0][0]
        indices_pop[i] = np.where(center_sorted_pop[i][2]==z_pop)[0][0]
        indices_granny[i] = np.where(center_sorted_granny[i][2]==z_granny)[0][0]
else: 
    print('n must be smaller than k, the number of clusters')

df_cluster_raw = df_tags.filter(df_tags.prediction.isin(*indices) == True)
df_cluster_raw_pop = df_tags_pop.filter(df_tags_pop.prediction.isin(*indices_pop) == True)
df_cluster_raw_granny = df_tags_granny.filter(df_tags_granny.prediction.isin(*indices_granny) == True)

# Create df's outcomes for the different clustering algorithms
df_cluster = df_cluster_raw             .select(ith("features", lit(0)).alias('lon'),                     ith("features", lit(1)).alias('lat'),                     ith("features", lit(2)).alias('pop'),                     ith("features", lit(3)).alias('granny'))
df_cluster_pop = df_cluster_raw_pop                 .select(ith("features", lit(0)).alias('lon'),                 ith("features", lit(1)).alias('lat'),                 ith("features", lit(2)).alias('pop'))
df_cluster_granny = df_cluster_raw_granny                 .select(ith("features", lit(0)).alias('lon'),                     ith("features", lit(1)).alias('lat'),                     ith("features", lit(2)).alias('granny'))

# Iterating over columns to be scaled
for i in ["pop","granny"]:
    # VectorAssembler Transformation - Converting column to vector type
    assembler = VectorAssembler(inputCols=[i],outputCol=i+"_Vect")

    # MinMaxScaler Transformation
    scaler = MinMaxScaler(inputCol=i+"_Vect", outputCol=i+"_Scaled")

    # Pipeline of VectorAssembler and MinMaxScaler
    pipeline = Pipeline(stages=[assembler, scaler])

    # Fitting pipeline on dataframe
    df_cluster = pipeline.fit(df_cluster).transform(df_cluster).withColumn(i+"_Scaled", unlist(i+"_Scaled")).drop(i+"_Vect")

df_cluster = df_cluster.select(df_cluster.lon, df_cluster.lat, df_cluster.pop_Scaled.alias('pop'), df_cluster.granny_Scaled.alias('granny'))

for row in df_cluster.collect():
    feature = {
            "type": "Feature",
            "properties": {
                "pop": row['pop'],
                "old_females": row['granny']
                },
            "geometry": {
                "type": "Point",
                "coordinates": [row['lon'],row['lat']]
                }
            }
    json_dump = [json.dumps(feature)]
    jsonRDD = sc.parallelize(json_dump)
    df_results = spark.read.json(jsonRDD)
    # write to mongo
    df_results         .write.format("mongo")         .mode("append")         .option("database", "geotest-db")         .option("collection", "results")         .save()

