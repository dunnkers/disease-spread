# Spark dependencies
import pyspark
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
import json

# user-defined functions (udf)
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

# setup connection for to mongo database
password = os.getenv('MONGODB_ROOT_PASSWORD')
mongoInputUri = 'mongodb://root:{}@my-mongodb:27017'.format(password)
mongoOutputUri = 'mongodb://root:{}@my-mongodb:27017'.format(password)

# start a sparksession
spark = SparkSession \
    .builder \
    .appName("PySparkFindClusters") \
    .config("spark.mongodb.input.uri", mongoInputUri) \
    .config("spark.mongodb.output.uri", mongoOutputUri) \
    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.4.1') \
    .getOrCreate()
sc = spark.sparkContext

# read data from mongo
df = spark \
    .read \
    .format("com.mongodb.spark.sql.DefaultSource") \
    .option("database", "geotest-db") \
    .option("collection", "2020_pop_geojson") \
    .load()

# Put mongo data in dataframe
data = df.select("geometry.coordinates", "properties.pop", "properties.old_females")

# Transform the dataframe into 4 columns: longitude, lattitude, population value, old females population value
df1 = data.select( \
      take_first_udf('coordinates').alias('lon'), \
      take_second_udf('coordinates').alias('lat'), \
      data.pop.cast(FloatType()).alias('pop'), \
      data.old_females.cast(FloatType()).alias('granny'))

# replace all null or na value with 0
df1 = df1.na.fill(0)

# prepare dataframe for K means clustering
FEATURES_COL = ['lon', 'lat', 'pop', 'granny']
vecAssembler = VectorAssembler(inputCols=FEATURES_COL, outputCol="features")
df_kmeans = vecAssembler.transform(df1).select('features')

# K means clustering
k = 15
kmeans = KMeans().setK(k).setSeed(1).setFeaturesCol("features")
model = kmeans.fit(df_kmeans)
centers = model.clusterCenters()
df_tags = model.transform(df_kmeans)

# find the largest value in the centers array
center_sorted = sorted(centers, key=lambda x: x[2], reverse=True)
z = np.array([row[2] for row in centers])
n = 7 # number of clusters (with larges values) we wish to export 
if n<k:
    indices = np.zeros(n)
    for i in range(0,n):
        indices[i] = np.where(center_sorted[i][2]==z)[0][0]
else: 
    print('n must be smaller than k, the number of clusters')

df_cluster_raw = df_tags.filter(df_tags.prediction.isin(*indices) == True)

# dataframe with the n cluster that have the largest pop and granny values
df_cluster = df_cluster_raw \
            .select(ith("features", lit(0)).alias('lon'), \
                    ith("features", lit(1)).alias('lat'), \
                    ith("features", lit(2)).alias('pop'), \
                    ith("features", lit(3)).alias('granny'))

# normalizing the pop and granny column
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

# create json
features = []
insert_features = lambda X: features.append(
    {
      "type": "Feature",
      "properties": {
          "pop": X['pop'],
          "old_females": X['granny']
      },
      "geometry": {
        "type": "Point",
        "coordinates": [X['lon'],X['lat']]
      }
    })
for row in df_cluster.collect():
    insert_features(row)

collection = {
  "type": "FeatureCollection",
  "features": features
}

# export json
with open('./DangerAreasOldFemales.json', 'w') as outfile:
    json.dump(collection, outfile)
