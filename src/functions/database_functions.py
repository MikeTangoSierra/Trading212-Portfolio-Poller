import pymongo
import logging

logging.basicConfig(filename='db_functions.log', encoding='utf-8', level=logging.DEBUG)
CLIENT_CONNECTION_STRING = pymongo.MongoClient("mongodb://mongodb:27017/")
LIST_EXISTING_DBS = CLIENT_CONNECTION_STRING.list_database_names()


# Insert a document to a mongoDB collection
def insert_document_in_mongodb(database, collection, dict):
    DATABASE = CLIENT_CONNECTION_STRING[database]
    COL = DATABASE[collection]

    try:
        COL.insert_one(dict)
    except:
        logging.error("ERROR:" + " " + "Failed to insert document into collection" + " " + collection)


# Check if a document exists in our mongoDB collection (based on the date/time the document was written to our
# collection)
def check_if_document_exists_in_mongodb(database, collection, dict):
    DATABASE = CLIENT_CONNECTION_STRING[database]
    COL = DATABASE[collection]
    UPDATED_TIME = dict.get('updated_time')

    if not UPDATED_TIME == "None":
        if DATABASE.COL.count_documents({'updated_time': UPDATED_TIME}, limit=1):
            return True
        else:
            return False


# Get the biggest winning position from our specified collection over our specified time period
def get_biggest_winning_position(database, collection, dict, time_period):
    DATABASE = CLIENT_CONNECTION_STRING[database]
    COL = DATABASE[collection]
    UPDATED_TIME = dict.get('updated_time')

    if not UPDATED_TIME == "None" and UPDATED_TIME > time_period:
        try:
            COL.find_one({"profit_loss_value": {"$gt": 0}})
        except:
            logging.error("ERROR:" + " " + "Failed to get biggest winning position from collection" + " " + collection)


# # Get the biggest winning position from our specified collection over our specified time period
def get_losing_winning_position(database, collection, dict, time_period):
    DATABASE = CLIENT_CONNECTION_STRING[database]
    COL = DATABASE[collection]
    UPDATED_TIME = dict.get('updated_time')

    if not UPDATED_TIME == "None" and UPDATED_TIME > time_period:
        try:
            COL.find_one({"profit_loss_value": {"$lt": 0}})
        except:
            logging.error("ERROR:" + " " + "Failed to get biggest losing position from collection" + " " + collection)


# Delete a document from a collection based on it's last_updated being older than our delete_after_days variable
def delete_document_from_collection(database, collection, dict, delete_after_days):
    DATABASE = CLIENT_CONNECTION_STRING[database]
    COL = DATABASE[collection]
    UPDATED_TIME = dict.get('updated_time')

    if not UPDATED_TIME == "None" and UPDATED_TIME < delete_after_days:
        try:
            COL.delete_one(dict)
        except:
            logging.error("ERROR:" + " " + "Failed to delete document from collection" + " " + collection)
