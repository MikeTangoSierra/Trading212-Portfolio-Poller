import pymongo
import logging

logging.basicConfig(filename='db_functions.log', encoding='utf-8', level=logging.DEBUG)
CLIENT_CONNECTION_STRING = pymongo.MongoClient("mongodb://mongodb:27017/")
LIST_EXISTING_DBS = CLIENT_CONNECTION_STRING.list_database_names()


def create_initial_mongodb(database, collection):
    DATABASE = CLIENT_CONNECTION_STRING[database]
    if database not in LIST_EXISTING_DBS:
        try:
            COL = DATABASE[collection]
            DEFAULT_DICT = {"key": "default_col"}
            COL.insert_one(DEFAULT_DICT)
        except:
            logging.warn("WARN:" + " " + "Database:" + " " + database + " " + "already exists, skipping create")


def write_dict_to_mongodb(database, collection, dict):
    DICT_NAME = (dict['name'])
    DATABASE = CLIENT_CONNECTION_STRING[database]
    COL = DATABASE[collection]
    DICT_EXISTS_IN_COL = COL.find_one({"name":str(DICT_NAME)})



    if DICT_EXISTS_IN_COL:
        try:
            COL.update_one(dict)
        except:
            logging.error("ERROR:" + " " + "Failed to update collection" + " " + collection)
    else:
        try:
            COL.insert_one(dict)
        except:
            logging.error("ERROR:" + " " + "Failed to insert collection" + " " + collection)
