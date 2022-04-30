# Backend for igo-stats web app
Current version of project allows to get csv-tables from cloud-storage and transform that to no-sql objects.
Then this objects are loaded to firestore database.

## Modules & folders description
### 1.
Folder *./tools* includes notebooks which can help to debug main python code
- one file builds SQL database the tables using SQL-Alchemy

### 2.
*update_firesore.py* is module which contains class for downloading dicts or JSON-files to Firestore

### 3.
*prepare_data.py* is module which contains class for loading tables from .csv to pandas.DataFrame.  
Then it creates dict from these dataframes.  
Then it does queries to dataframe with participants-tournaments data and:  
- adds field with list of players to every tournament
- adds field eith list of tournaments to every playes

### 4.
*edit_collections.py* contains functions to add, update and delete documents from firestore.
