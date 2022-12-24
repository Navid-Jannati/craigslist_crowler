import json
from abc import ABC, abstractmethod

from mongo import MongoDatabase


class StorageAbstract(ABC):
    @abstractmethod
    def store(self, data, *args):
        pass

    @abstractmethod
    def load(self, *args, **kwargs):
        pass


class MongoStorage(StorageAbstract):

    def __init__(self):
        self.mongo = MongoDatabase()

    def store(self, data, collection, *args):
        collection = getattr(self.mongo.database, collection)
        if isinstance(data, list) and len(data) > 1:
            collection.insert_many(data)
        else:
            collection.insert_one(data)

    def load(self, collection_name, filter_data=None):
        collection = self.mongo.database[collection_name]
        if filter_data is not None:
            data = collection.find(filter_data)
        else:
            data = collection.find()
        return collection.find()

    def update_flag(self, data):
        self.mongo.database.advertisement_links.find_one_and_update(
            {'_id': data['_id']},
            {'$set': {'flag': True}}
        )


class FileStorage(StorageAbstract):

    def store(self, data, filename, *args):
        filename = filename + '-' + data['post_id']
        with open(f'data/adv/{filename}.json', 'w') as file:
            file.write(json.dumps(data))
        print(f'data/adv/{filename}.json')

    def load(self):
        with open('data/adv/advertisement_links.json', 'r') as file:
            links = json.loads(file.read())
            return links

    def update_flag(self):
        pass

