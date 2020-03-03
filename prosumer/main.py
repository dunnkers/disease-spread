from kafka import KafkaProducer
import time
import datetime

producer = KafkaProducer(bootstrap_servers=['my-kafka:9092'])

for _ in range(100):
  producer.send('testing', bytes(str(datetime.date.today()), 'utf-8'))
  time.sleep(1)