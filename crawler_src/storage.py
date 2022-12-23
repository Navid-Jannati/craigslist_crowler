import json
from abc import ABC, abstractmethod

from mongo import MongoDatabase


class StorageAbstract(ABC):
    @abstractmethod
    def store(self, data, *args):
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


class FileStorage(StorageAbstract):

    def store(self, data, filename, *args):
        with open(f'data/adv/{filename}.json', 'w') as file:
            file.write(json.dumps(data))
        print(f'data/adv/{filename}.json')

