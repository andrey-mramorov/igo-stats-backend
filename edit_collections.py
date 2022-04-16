import firebase_admin
from firebase_admin import firestore


def truncate_collection(database, collection_name):
    docs = database.collection(collection_name).get()  # Get all data
    for doc in docs:
        key = doc.id
        database.collection(collection_name).document(key).delete()


def add_document(database, item, collection_name):
    return database.collection(collection_name).add(item)


def merge_document(database, item, collection_name):
    return database.collection(collection_name).document(str(item['id'])).set(item, merge=True)


def update_array_field(database, doc_id, array_name, val, collection_name):
    return database.collection(collection_name).document(doc_id).update({array_name: firestore.ArrayUnion([val])})
