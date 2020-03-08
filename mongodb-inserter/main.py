from datetime import date
import json
from kafka import KafkaConsumer
import pymongo
import sys
from uuid import uuid1
import os

password = os.getenv('MONGODB_ROOT_PASSWORD')

client = pymongo.MongoClient('mongodb://root:{}@my-mongodb:27017'.format(password))
db = client['test-db']
collection = db['test-collection']

print("connected to mongodb")

consumer = KafkaConsumer(
  'testing',
  bootstrap_servers=['my-kafka:9092'], 
  auto_offset_reset='earliest', 
  enable_auto_commit=False
)

if not consumer.bootstrap_connected():
  print("not connected to bootstrap")
  exit(1)

print("All set up, ready to receive messages")

for message in consumer:
  body = message.value.decode('utf-8')
  print("received a new message: " + body)
  collection.insert({"date_received": date.today().__str__(), "data": body})

print("all done, closing connection to MongoDB")
client.close()