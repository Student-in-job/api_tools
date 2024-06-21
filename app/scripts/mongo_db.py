import pymongo
import pymongo.database
import pymongo.mongo_client
import pymongo.collection
from typing import List


def open_connection(host: str, database: str, new: bool = False) -> pymongo.database.Database:
    my_client = pymongo.MongoClient(host)
    mydb = my_client[database]
    if new:
        for db in my_client.list_databases():
            if db["name"] == database:
                my_client.drop_database(database)
    return mydb


def connect_to(host: str, dbname: str) -> pymongo.database.Database:
    my_client = pymongo.MongoClient(host)
    mydb = my_client[dbname]
    return mydb


def get_collection(mongo_db: pymongo.database.Database,  name: str, new: bool = False) -> pymongo.collection.Collection:
    if new:
        mongo_db[name].drop()
    return mongo_db[name]


def insert_row(space: pymongo.collection.Collection, row: dict) -> None:
    space.insert_one(row)


def insert_rows(space: pymongo.collection.Collection, bulk_rows: List[dict]) -> None:
    space.insert_many(bulk_rows)
