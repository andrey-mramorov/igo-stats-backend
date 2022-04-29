import os
import firebase_admin
from firebase_admin import credentials, firestore
from update_firestore import UploadDataToFirestore


if __name__ == "__main__":
    # Load sdk-key
    cert = os.path.abspath(os.curdir + '/sdk_key/igo-stats-firebase-adminsdk-vwmdk-b32d0db07c.json')

    # Connect to firebase
    cred = credentials.Certificate(cert)
    default_app = firebase_admin.initialize_app(cred)

    # Select firestore database
    fs_db = firestore.client()
