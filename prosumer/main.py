import datetime
from kafka import KafkaProducer
import time

producer = KafkaProducer(bootstrap_servers=['my-kafka:9092'])

if not producer.bootstrap_connected():
  print("not connected to bootstrap server")
  exit()

def err_callback(error):
  print("could not send: " + error)

def success_callback(metdata):
  print("send successful")

for _ in range(100):
  print("sending...")
  producer.send('testing-consumer', bytes(str(datetime.date.today()), 'utf-8')).add_callback(success_callback).add_callback(err_callback)
  time.sleep(1)
