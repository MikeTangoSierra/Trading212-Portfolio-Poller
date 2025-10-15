from datetime import datetime, timedelta
import logging
import os
import pymongo
from functions import logging as configurecustomlogging

# Configure logging
configurecustomlogging.configure_logging('database_functions.log')

mongo_host = os.environ.get("MONGO_HOST", "mongodb:27017")
mongo_user = os.environ.get("MONGO_USER")
mongo_pass = os.environ.get("MONGO_PASSWORD")

if mongo_user and mongo_pass:
    # Authenticated connection
    mongo_uri = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}?authSource=admin"
else:
    # No auth (local/dev)
    mongo_uri = f"mongodb://{mongo_host}"

CLIENT_CONNECTION_STRING = pymongo.MongoClient(mongo_uri)

def list_existing_databases():
    try:
        return CLIENT_CONNECTION_STRING.list_database_names()
    except Exception as e:
        logging.error(f"Failed to list existing databases: {e}")
        return []

def list_existing_collections(database):
    try:
        return CLIENT_CONNECTION_STRING[database].list_collection_names()
    except Exception as e:
        logging.error(f"Failed to list collections in DB {database}: {e}")
        return []

def check_if_document_exists_in_database(database, collection, document, do_exclude_last_updated_key=False):
    try:
        col = CLIENT_CONNECTION_STRING[database][collection]
        doc_clone = document.copy()
        doc_clone.pop("_id", None)
        if do_exclude_last_updated_key:
            doc_clone.pop("last_updated", None)

        result = col.find_one(doc_clone)
        return result.get("_id") if result else None
    except Exception as e:
        logging.error(f"Error checking document existence in {database}.{collection}: {e}")
        return None

def insert_or_update_document_in_database(database, collection, document, existing_document_id=None):
    try:
        col = CLIENT_CONNECTION_STRING[database][collection]
        if existing_document_id is None:
            logging.debug(f"Inserting into {database}.{collection}: {document}")
            col.insert_one(document)
        else:
            logging.debug(f"Updating {database}.{collection} (ID: {existing_document_id}): {document}")
            result = col.update_one({"_id": existing_document_id}, {"$set": document}, upsert=False)
            if result.matched_count == 0:
                logging.warning(f"No document found with _id={existing_document_id} to update.")
    except Exception as e:
        logging.error(f"Error in insert/update for {database}.{collection}: {e}")

def delete_document_from_mongodb(database, collection, time_limit_days):
    try:
        col = CLIENT_CONNECTION_STRING[database][collection]
        cutoff = datetime.utcnow() - timedelta(days=time_limit_days)
        for doc in col.find({}):
            last_updated = doc.get("last_updated")
            if last_updated:
                doc_time = last_updated
                # Convert string to datetime if necessary
                if isinstance(last_updated, str):
                    try:
                        doc_time = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S.%f")
                    except ValueError:
                        logging.warning(f"Invalid date format in doc: {doc}")
                        continue
                if doc_time <= cutoff:
                    logging.info(f"Deleting outdated document in {database}.{collection}: {doc.get('_id')}")
                    col.delete_one({"_id": doc["_id"]})
    except Exception as e:
        logging.error(f"Failed to delete old documents in {database}.{collection}: {e}")

def clean_up_mongodb(time_limit_days):
    try:
        for database in list_existing_databases():
            if database not in ["admin", "config", "local"]:
                for collection in list_existing_collections(database):
                    delete_document_from_mongodb(database, collection, time_limit_days)
    except Exception as e:
        logging.error(f"Failed to clean up MongoDB: {e}")