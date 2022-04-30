import firebase_admin
from firebase_admin import firestore, credentials
# from google.cloud.firestore import ArrayUnion


# Function for deleting all documents from chosen collection
def truncate_collection(database, collection_name):
    cnt = 0
    docs = database.collection(collection_name).get()  # Get all data
    for doc in docs:
        key = doc.id
        database.collection(collection_name).document(key).delete()
        cnt += 1

    print(f'Collection {collection_name} was successfully cleaned.')
    print(f'{cnt} docs was deleted.')


def add_document(database, collection_name, item):
    return database.collection(collection_name).add(item)


def merge_document(database, collection_name, item):
    return database.collection(collection_name).document(str(item['id'])).set(item, merge=True)


# Adds new value into array in some document (in fact it merges source array with [value] array)
def update_array_field(database, collection_name, doc_id, array_name, val):
    return database.collection(collection_name).document(doc_id).update({array_name: firestore.ArrayUnion([val])})


# *** FOR TESTS ***
if __name__ == '__main__':
    # connect to firebase project (initialize app)
    cred = credentials.Certificate('.' + '/sdk_key/igo-stats-firebase-adminsdk-vwmdk-b32d0db07c.json')
    default_app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    update_array_field(db, 'players', 'Andrew', 'tournaments', 'World Championship')
