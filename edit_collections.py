import firebase_admin
from firebase_admin import firestore, credentials
# from google.cloud.firestore import ArrayUnion


def truncate_collection(database, collection_name):
    docs = database.collection(collection_name).get()  # Get all data
    for doc in docs:
        key = doc.id
        database.collection(collection_name).document(key).delete()


def add_document(database, collection_name, item):
    return database.collection(collection_name).add(item)


def merge_document(database, collection_name, item):
    return database.collection(collection_name).document(str(item['id'])).set(item, merge=True)


def update_array_field(database, collection_name, doc_id, array_name, val):
    return database.collection(collection_name).document(doc_id).update({array_name: firestore.ArrayUnion([val])})


# For tests
if __name__ == '__main__':
    # connect to firebase project (initialize app)
    cred = credentials.Certificate('.' + '/sdk_key/igo-stats-firebase-adminsdk-vwmdk-b32d0db07c.json')
    default_app = firebase_admin.initialize_app(cred)

    db = firestore.client()
    update_array_field(db, 'collection_name', 'document_id', 'words', 'blob')
