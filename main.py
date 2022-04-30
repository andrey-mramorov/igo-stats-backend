import json
import os

import pandas as pd
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
# import urllib
from update_firestore import UploadDataToFirestore
from prepare_data import GoTables
from edit_collections import truncate_collection


def delete_everything():
    truncate_collection(db, 'members')
    truncate_collection(db, 'tournaments')
    print('Everything was deleted from database\n')


if __name__ == "__main__":
    # *** Load constants & config
    cert = os.path.abspath(os.curdir + '/sdk_key/igo-stats-firebase-adminsdk-vwmdk-b32d0db07c.json')  # sdk-key
    cred = credentials.Certificate(cert)

    with open('./sdk_key/firebaseConfig.json', 'r') as f:  # web-app config
        firebaseConfig = json.load(f)

    with open('./default_path.json', 'r') as f:  # paths to tables
        paths = json.load(f)
    # ***

    # *** Connect to firestore & to storage
    default_app = firebase_admin.initialize_app(cred)
    db = firestore.client()  # to firestore

    firebase_app = pyrebase.initialize_app(firebaseConfig)
    storage = firebase_app.storage()  # to storage
    # ***

    # *** Get URLs of tables in cloud-storage
    players_url = storage.child(paths['players']).get_url(None)
    tournaments_url = storage.child(paths['tournaments']).get_url(None)
    link_pt_url = storage.child(paths['link_pt']).get_url(None)
    towns_url = storage.child(paths['towns']).get_url(None)
    # Read from url (text)
    # players_url = storage.child(players_path).get_url(None)
    # file = urllib.request.urlopen(players_url).read()
    # But pandas can read directly from url
    # players = pandas.read_csv(players_url)
    # ***

    # *** Firstly delete all data from collections (ONLY FOR TESTS)
    delete_everything()
    # ***

    # *** Let's prepare data to upload to Firestore
    local_db = GoTables(players_url, tournaments_url, link_pt_url)
    players = local_db.players_t  # result is JSON-like docs of players with list of tournaments in every player's doc
    tournaments = local_db.tournaments_t  # same (list of players in every tournament's doc)
    # ***

    # *** Upload data
    upload_players = UploadDataToFirestore(db, players, 'add', 'players')
    upload_tournaments = UploadDataToFirestore(db, tournaments, 'add', 'tournaments')

    upload_players.upload()
    print('Players done.\n')
    upload_tournaments.upload()
    print('Tournaments done.\n')
    # *** FOR TESTS ***
    '''
    # Let's upload towns
    local_db = GoTables(towns_t=towns_url)
    towns = local_db.towns_t

    upload_towns = UploadDataToFirestore(db, towns, 'add', 'towns')
    # Truncate towns
    truncate_collection(db, 'towns')
    # Upload
    upload_towns.upload()
    '''
