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


# Get the biggest winning position for a certain time period
# Use MongoDB queries for this and minimal python code
# Try something like this https://www.mongodb.com/community/forums/t/fetch-data-with-max-and-between-condition/3973
def get_biggest_winning_position(database, collection, time_period):
    print("working on it!")


# Get the biggest losing position for a certain time period
# Use MongoDB queries for this and minimal python code
# Try something like this https://www.mongodb.com/community/forums/t/fetch-data-with-max-and-between-condition/3973
def get_losing_winning_position(database, collection, time_period):
    print("working on it!")

# Delete a document from a collection based on it's last_updated value
