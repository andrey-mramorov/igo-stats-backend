import os
import pandas as pd

# *** DEFAULT HEADERS ***
tournaments_header = ['rfg_id', 'title', 'place', 'begin_date', 'end_date', 'komi', 'tours', 'rules']
players_header = ['rfg_id', 'last_name', 'first_name', 'birth_date', 'town_id', 'rating', 'last_game', 'last_update']
link_pt_header = ['tournament_id', 'player_id', 'place_in_tournament', 'rating_before', 'rating_after',
                  'MM_before', 'MM_cf', 'BHG_cf', 'BER_cf']
towns_header = ['id', 'town_name', 'name_lat', 'short', 'short_lat', 'fed_id']

# ******


class GoTables:
    """
    This class is using for upload set of tables from RFG Go-Database (TIGR)
    and to do some queries and add additional info to every document.
    Also, it converts source tables to json-like dicts. It is required for further download to Firestore

    To use this class create object and set required tables.
    """
    def __init__(self, players_t=None, tournaments_t=None, link_pt=None, towns_t=None) -> None:
        self.players_t = players_t  # players table
        self.tournaments_t = tournaments_t  # tournaments table
        self.link_pt = link_pt  # table connecting players & tournaments
        self.towns_t = towns_t  # towns table

        if players_t and tournaments_t:
            self._add_players_list()
            self._add_tournaments_list()

    # Players table getter method
    @property
    def players_t(self):
        return self._players_t

    # Players table setter method
    @players_t.setter
    def players_t(self, val):
        if val is None:
            print(f'Players table is not defined')
        elif type(val) is dict:
            self._players_t_t = val
        elif type(val) is not str:
            print(f'Wrong type {val}. Please specify file path.')
        # elif not os.path.exists(val):
            # print(f'File {val} does not exist')
        else:
            # Load 'players' table
            players_table = pd.read_csv(val, header=None)
            players_table.columns = players_header

            # To dict
            self._players_t = players_table.to_dict(orient='records')
            # self._players_t = players_table

    @property
    def tournaments_t(self):
        return self._tournaments_t

    @tournaments_t.setter
    def tournaments_t(self, val):
        if val is None:
            print(f'Tournaments table is not defined')
        elif type(val) is dict:
            self._tournaments_t = val
        elif type(val) is not str:
            print(f'Wrong type {val}. Please specify file path.')
        # elif not os.path.exists(val):
            # print(f'File {val} does not exist')
        else:
            # Load 'players' table
            tournaments_table = pd.read_csv(val, header=None)
            tournaments_table.columns = tournaments_header

            # To dict
            self._tournaments_t = tournaments_table.to_dict(orient='records')
            # self._tournaments_t = tournaments_table

    @property
    def link_pt(self):
        return self._link_pt

    @link_pt.setter
    def link_pt(self, val):
        if val is None:
            print(f'Players-tournaments table is not defined')
        elif type(val) is not str:
            print(f'Wrong type {val}. Please specify file path.')
        # elif not os.path.exists(val):
            # print(f'File {val} does not exist')
        else:
            # Load 'players-tournaments' table
            pt_table = pd.read_csv(val, header=None)
            pt_table.columns = link_pt_header

            self._link_pt = pt_table

    # Method for adding list of tournaments to every player's document
    def _add_tournaments_list(self):
        for doc in self.players_t:
            p_id = doc['rfg_id']
            if int(p_id) != -1:
                tournaments_list = self.link_pt.query(f'player_id == {p_id}')['tournament_id'].tolist()
                doc['tournaments'] = tournaments_list

    # Method for adding list of players to every tournament's document
    def _add_players_list(self):
        for doc in self.tournaments_t:
            t_id = doc['rfg_id']
            if int(t_id) != -1:
                players_list = self.link_pt.query(f'tournament_id == {t_id}')['player_id'].tolist()
                doc['participants'] = players_list

    @property
    def towns_t(self):
        return self._towns_t

    @towns_t.setter
    def towns_t(self, val):
        if val is None:
            print(f'Towns table is not defined')
        elif type(val) is dict:
            self._towns_t = val
        elif type(val) is not str and type(val) is not None:
            print(f'Wrong type {val}. Please specify file path.')
        # elif not os.path.exists(val):
            # print(f'File {val} does not exist')
        else:
            # Load 'towns' table
            towns_table = pd.read_csv(val, header=None)
            towns_table.columns = towns_header

            # To dict
            self._towns_t = towns_table.to_dict(orient='records')
            # self._towns_t = towns_table


# *** FOR TESTS ***
if __name__ == '__main__':
    gotables = GoTables('./db-samples/players.csv', './db-samples/tournaments.csv',
                        './db-samples/players-tournaments.csv')

    print(gotables.players_t[:5])
