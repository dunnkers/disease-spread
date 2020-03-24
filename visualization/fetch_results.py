from pymongo import MongoClient
import json
from os import getenv

password = getenv('MONGODB_ROOT_PASSWORD')
client = MongoClient('mongodb://root:{}@my-mongodb:27017'.format(password))
db = client['geotest-db']
results_collection = db['results']

with db['results'].watch() as stream:
    for change in stream:
        # Something changed in the `results` collection! :)
        # -> so, dump collection to json
        res = results_collection.find({}, {'_id': 0})
        collection = {
            'type': 'FeatureCollection',
            'features': list(res)
        }
        with open('./results.json', 'w') as outfile:
            json.dump(collection, outfile)