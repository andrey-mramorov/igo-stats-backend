import json
import timeit
import os
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore


class UploadDataToFirestore:
    """
    This class is using for upload data to Firestore.
    It supports only-json like objects:
        1) JSON-string (just python string, which can be formatted as JSON)
        2) List of dicts / dict
        3) JSON-file path
    UploadDataToFirestore supports these methods of upload:
        1) 'set'
        'set' is using to add documents with custom id. By default, this method takes 'id' field in dict.
        2) 'add'
        'add' adds document without id (document name). So firestore will set id automatically.

    To upload something firstly you need to create object, secondary set all required fields, then use upload() method.
    """
    def __init__(self, database, json_data=None, method=None, collection_name=None) -> None:
        # Initialize instance variables
        self.db = database
        self.json_data = json_data
        self.method = method
        self.collection_name = collection_name

    # Firestore upload method getter method
    @property
    def method(self):
        return self._method

    # Firestore upload method setter method
    @method.setter
    def method(self, val):
        if val is None:
            print(f'Please, specify method of upload')
        elif val == 'set' or val == 'add':
            self._method = val
        else:
            print(f'Wrong method {val}, use set or add')

    # Collection name getter method
    @property
    def collection_name(self):
        return self._collection_name

    # Collection name setter method
    @collection_name.setter
    def collection_name(self, val):
        if val is None:
            print(f'Please, specify name of collection to upload to')
        elif type(val) == str:
            self._collection_name = val
        else:
            print(f'Wrong type for firestore collection name')

    # Get JSON-data property
    @property
    def json_data(self):
        return self._json_data

    # Set and process JSON-data or path to JSON
    @json_data.setter
    def json_data(self, val):
        if val is None:
            print(f'Please, specify .json file path or give a list of dicts')
        elif type(val) == str:
            try:
                # Open JSON file
                with open(val, 'r') as f:
                    # Returns JSON object as a dictionary
                    data = json.load(f)

                self._json_data = data
            except Exception as e1:
                try:
                    data = json.loads(val)
                    self._json_data = data
                except Exception as e2:
                    print(f'JSON string is not correct: {str(e2)}' + '\n' + f'or wrong file-path name: {str(e1)}')
        elif type(val) == list:
            if type(val[0]) == dict:
                self._json_data = val
        else:
            print(f'Wrong data type')

    # Main class method to populate firestore with the said data
    def upload(self):
        # Get upload running time
        start = timeit.default_timer()

        if self.json_data and self.method and type(self.json_data) == list:
            # Iterating through the json list
            for idx, item in enumerate(self.json_data):

                if self.method == 'set':
                    self.set(item)
                elif self.method == 'add':
                    self.add(item)
                # Successfully got to end of data;
                # print success message
                if idx == len(self.json_data) - 1:
                    # All the program statements
                    stop = timeit.default_timer()
                    print('**** SUCCESS UPLOAD ****')
                    print("Time taken: " + str(stop - start))

    # Collection -add- method
    # Adds all data under a collection with firebase firestore auto generated IDS
    def add(self, item):
        return self.db.collection(self.collection_name).add(item)

    # Collection document -set- method
    # Adds all data under a collection with custom document IDS
    def set(self, item):
        return self.db.collection(self.collection_name).document(str(item['id'])).set(item, merge=True)


# *** FOR TESTS ***
if __name__ == "__main__":
    # Load sdk-key
    cert = os.path.abspath(os.curdir + '/sdk_key/igo-stats-firebase-adminsdk-vwmdk-b32d0db07c.json')

    # Load local tables
    local_db_folder = os.path.abspath(os.curdir) + '/db-samples'
    tables = os.listdir(local_db_folder)

    print('Current tables to load:\n')
    for tb in tables:
        print(tb, end=' ')
    print('\n')

    # Connect to firebase
    cred = credentials.Certificate(cert)
    default_app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    # Default header for players table
    players_header = ['id', 'last_name', 'first_name', 'birth_date', 'town_id', 'rating', 'last_game', 'last_update']

    # Load 'players' table
    players_table = pd.read_csv(local_db_folder + '/' + tables[0], header=None)
    players_table.columns = players_header

    # Sample data
    players_table_test = players_table[:5]

    # Different way to transform table to firestore-nosql-documents
    # json_string = players_table_test.to_json(orient='records')

    json_dict = players_table_test.to_dict(orient='records')

    upd = UploadDataToFirestore(json_dict, 'add', 'test')
    upd.upload()
