from typing import Dict
import pymongo


class Database(object):
    URI = 'mongodb://127.0.0.1:27017'
    DATABASE_NAME = 'pricecheck'
    DATABASE = pymongo.MongoClient(URI)[DATABASE_NAME]

    @staticmethod
    def insert(collection: str, data: Dict):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def update(collection: str, query: Dict, data: Dict):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].remove(query)

    @staticmethod
    def find(collection: str, query: Dict) -> pymongo.cursor:
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].find_one(query)
