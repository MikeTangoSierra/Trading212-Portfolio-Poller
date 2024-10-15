from functions.transform_data_functions import bson_to_json
import pymongo
import logging
from datetime import datetime, timedelta


logging.basicConfig(filename='db_functions.log', encoding='utf-8', level=logging.DEBUG)
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
    UPDATED_TIME = dict.get('last_updated')

    if not UPDATED_TIME == "None":
        if DATABASE.COL.count_documents({'last_updated': UPDATED_TIME}, limit=1):
            return True
        else:
            return False


# Get the biggest winning position for a certain time period.
# THIS WON'T WORK UNLESS I WRITE EACH POSITION TO A COLLECTION AT THE END OF A QUARTER AND THEN QUERY THAT COLLECTION AGAINST MY TIME PERIOD.
def get_biggest_winning_position(database, collection, time_period_start, time_period_end):
    DATABASE = CLIENT_CONNECTION_STRING[database]
    COL = DATABASE[collection]

    # Query to find the document with the maximum value within the specified time period.
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
                'ppl': -1,  # Assuming 'ppl' is the field representing profit/loss
                'fxPpl': -1  # Assuming 'fxPpl' is the field representing foreign exchange profit/loss
            }
        },
        {
            '$limit': 1
        }
    ]

    result_json = bson_to_json(list(COL.aggregate(FIND_BIGGEST_WINNING_POSITION_QUERY)))
    return result_json

# Get the biggest losing position for a certain time period
# THIS WON'T WORK UNLESS I WRITE EACH POSITION TO A COLLECTION AT THE END OF A QUARTER AND THEN QUERY THAT COLLECTION AGAINST MY TIME PERIOD.
def get_losing_winning_position(database, collection, time_period_start, time_period_end):
    DATABASE = CLIENT_CONNECTION_STRING[database]
    COL = DATABASE[collection]

    # Query to find the document with the minimum value within the specified time period
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
                'ppl': 1,  # Assuming 'ppl' is the field representing profit/loss
                'fxPpl': 1  # Assuming 'fxPpl' is the field representing foreign exchange profit/loss
            }
        },
        {
            '$limit': 1
        }
    ]

    result_json = bson_to_json(list(COL.aggregate(FIND_BIGGEST_LOSING_POSITION_QUERY)))
    return result_json


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
        if not database == "admin" or not database == "config" or not database == "local":
            for collection in list_existing_collections(database):
                delete_document_from_mongodb(database, collection, time_limit_days)
