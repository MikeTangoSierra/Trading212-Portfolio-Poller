from datetime import datetime, timedelta
from functions.logging import *
from functions.transform_data_functions import bson_to_json
import pymongo

# Setup logging.
configure_logging('db_functions.log')

# Setup our MongoDB client connection string.
CLIENT_CONNECTION_STRING = pymongo.MongoClient("mongodb://mongodb:27017/")
LIST_EXISTING_DBS = CLIENT_CONNECTION_STRING.list_database_names()


# Return a list of existing databases in our mongoDB instance.
def list_existing_databases():
    return LIST_EXISTING_DBS


# Return a list of existing collections in a database.
def list_existing_collections(database):
    DATABASE = CLIENT_CONNECTION_STRING[database]
    return DATABASE.list_collection_names()


# Insert a document to a mongoDB collection.
def insert_document_in_mongodb(database, collection, dict):
    DATABASE = CLIENT_CONNECTION_STRING[database]
    COL = DATABASE[collection]

    try:
        COL.insert_one(dict)
    except:
        logging.error("ERROR:" + " " + "Failed to insert document into collection" + " " + collection)


# Check if a document exists in our mongoDB collection (based on the date/time the document was written to our
# collection).
def check_if_document_exists_in_mongodb(database, collection, dict):
    DATABASE = CLIENT_CONNECTION_STRING[database]
    COL = DATABASE[collection]

    try:
        if COL.find_one(dict):
            return True
        else:
            return False
    except:
        logging.error("ERROR:" + " " + "Failed to check if document exists in collection" + " " + collection)


def get_biggest_winning_position(databases, collections, time_period_start, time_period_end):

    for db in databases:
        DATABASE = CLIENT_CONNECTION_STRING[db]

        for collection in collections:
            COL = DATABASE[collection]
            FIND_BIGGEST_WINNING_POSITION_QUERY = [
                {
                    '$match': {
                        'last_updated': {
                            '$gte': time_period_start,
                            '$lte': time_period_end
                        }
                    }
                },
                {
                    '$sort': {
                        'ppl': -1,
                        'fxPpl': -1
                    }
                },
                {
                    '$limit': 1
                }
            ]

            result = list(COL.aggregate(FIND_BIGGEST_WINNING_POSITION_QUERY))
            if result:
                return bson_to_json(result)
    return {}


def get_biggest_losing_position(databases, collections, time_period_start, time_period_end):

    for db in databases:
        DATABASE = CLIENT_CONNECTION_STRING[db]

        for collection in collections:
            COL = DATABASE[collection]
            FIND_BIGGEST_LOSING_POSITION_QUERY = [
                {
                    '$match': {
                        'last_updated': {
                            '$gte': time_period_start,
                            '$lte': time_period_end
                        }
                    }
                },
                {
                    '$sort': {
                        'ppl': 1,
                        'fxPpl': 1
                    }
                },
                {
                    '$limit': 1
                }
            ]

            result = list(COL.aggregate(FIND_BIGGEST_LOSING_POSITION_QUERY))
            if result:
                return bson_to_json(result)
    return {}


# Delete a document from a collection in MongoDB based on its updated_time being greater than time_limit_days.
def delete_document_from_mongodb(database, collection, time_limit_days):
    DATABASE = CLIENT_CONNECTION_STRING[database]
    COL = DATABASE[collection]
    DOCUMENTS = list(COL.find({}))
    raw_time_limit_date = datetime.today() - timedelta(days=time_limit_days)
    final_time_limit_date = datetime.strptime(str(raw_time_limit_date), "%Y-%m-%d %H:%M:%S.%f")

    try:
        for document in DOCUMENTS:
            updated_time_date = datetime.strptime(document['last_updated'], "%Y-%m-%d %H:%M:%S.%f")
            if updated_time_date <= final_time_limit_date:
                logging.info("INFO:" + " " + "Deleting document from collection" + " " + collection)
                COL.delete_one(document)
    except:
        logging.error("ERROR:" + " " + "Failed to delete document from collection" + " " + collection)


# Utilising our list_existing_databases function, define a function to loop through the list of existing databases
# that it returns and for each collection within our databases that are NOT the "admin", "config" or "local"
# databases, utilise our delete_document_from_mongodb function to loop through each document within the collection
# and delete those documents that have an updated_time greater than the time_limit_days.
def clean_up_mongodb(time_limit_days):
    for database in list_existing_databases():
        if not database == "admin" or not database == "config" or not database == "local" or not database == "system":
            for collection in list_existing_collections(database):
                delete_document_from_mongodb(database, collection, time_limit_days)
