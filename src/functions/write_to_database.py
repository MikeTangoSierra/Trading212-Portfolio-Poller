import pymongo

def create_mongo_db(database):
    try:
        CLIENT_CONNECTION_STRING = pymongo.MongoClient("mongodb://mongodb:27017/")
        DATABASE = CLIENT_CONNECTION_STRING[database]
        COL = DATABASE["TEST"]
        MYDICT = { "name": "John", "address": "Highway 37" }
        COL.insert_one(MYDICT)
    except:
        print("couldn't create db")


