import json
from abc import ABC, abstractmethod


class StorageAbstract(ABC):
    @abstractmethod
    def store(self, data, *args):
        pass


class MongoStorage(StorageAbstract):
    def store(self, data, *args):
        raise NotImplementedError()


class FileStorage(StorageAbstract):

    def store(self, data, filename, *args):
        with open(f'data/adv/{filename}.json', 'w') as file:
            file.write(json.dumps(data))
        print(f'data/adv/{filename}.json')

