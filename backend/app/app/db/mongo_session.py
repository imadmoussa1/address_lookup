import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.core.config import settings


class MongoSession:
  _mongo_client = None
  _address_database = None


  @staticmethod
  def mongo_client():
    if MongoSession._mongo_client is None:
      mongo_uri = open("/run/secrets/mongo_db_uri", "r").readline()
      MongoSession._mongo_client = MongoClient(mongo_uri)
    return MongoSession._mongo_client

  @staticmethod
  def is_database_connected():
    try:
      MongoSession.mongo_client().admin.command('ismaster')
      return True
    except ConnectionFailure:
      return False

  @staticmethod
  def address_database():
    if MongoSession._address_database is None and MongoSession.is_database_connected():
      MongoSession._address_database = MongoSession.mongo_client()[settings.RAW_DATABASE_NAME]
    return MongoSession._address_database

  @staticmethod
  def spain_address_collection():
    return MongoSession.address_database()["spain_address"]

