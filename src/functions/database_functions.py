import pymongo
import logging
from datetime import datetime, timedelta

logging.basicConfig(filename='db_functions.log', encoding='utf-8', level=logging.DEBUG)
CLIENT_CONNECTION_STRING = pymongo.MongoClient("mongodb://mongodb:27017/")

def list_existing_databases():
    try:
        return CLIENT_CONNECTION_STRING.list_database_names()
    except Exception as e:
        logging.error(f"ERROR: Failed to list existing databases: {e}")
        return []

def list_existing_collections(database):
    try:
        return CLIENT_CONNECTION_STRING[database].list_collection_names()
    except Exception as e:
        logging.error(f"ERROR: Failed to list collections in DB {database}: {e}")
        return []

def check_if_document_exists_in_database(database, collection, document, do_exclude_last_updated_key):
    try:
        COL = CLIENT_CONNECTION_STRING[database][collection]
        document_clone = document.copy()
        document_clone.pop("_id", None)
        if do_exclude_last_updated_key:
            document_clone.pop("last_updated", None)

        result = COL.find_one(document_clone)
        if result:
            return result.get("_id")  # Return actual _id from DB
        else:
            return None
    except Exception as e:
        logging.error(f"ERROR checking document existence in {database}.{collection}: {e}")
        return None

def insert_or_update_document_in_database(database, collection, document, existing_document_id):
    try:
        COL = CLIENT_CONNECTION_STRING[database][collection]

        if existing_document_id is None:
            logging.debug(f"Inserting into {database}.{collection}: {document}")
            COL.insert_one(document)
        else:
            logging.debug(f"Updating {database}.{collection} (ID: {existing_document_id}): {document}")
            result = COL.update_one({"_id": existing_document_id}, {"$set": document}, upsert=False)
            if result.matched_count == 0:
                logging.warning(f"WARNING: No document found with _id={existing_document_id} to update.")
    except Exception as e:
        logging.error(f"ERROR in insert/update for {database}.{collection}: {e}")

def delete_document_from_mongodb(database, collection, time_limit_days):
    try:
        COL = CLIENT_CONNECTION_STRING[database][collection]
        cutoff = datetime.today() - timedelta(days=time_limit_days)
        cutoff_str = cutoff.strftime("%Y-%m-%d %H:%M:%S.%f")

        for doc in COL.find({}):
            last_updated = doc.get("last_updated")
            if last_updated:
                try:
                    doc_time = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S.%f")
                    if doc_time <= cutoff:
                        logging.info(f"Deleting outdated document in {database}.{collection}: {doc.get('_id')}")
                        COL.delete_one({"_id": doc["_id"]})
                except ValueError:
                    logging.warning(f"Invalid date format in doc: {doc}")
    except Exception as e:
        logging.error(f"ERROR: Failed to delete old documents in {database}.{collection}: {e}")

def clean_up_mongodb(time_limit_days):
    try:
        for database in list_existing_databases():
            if database not in ["admin", "config", "local"]:
                for collection in list_existing_collections(database):
                    delete_document_from_mongodb(database, collection, time_limit_days)
    except Exception as e:
        logging.error(f"ERROR: Failed to clean up MongoDB: {e}")