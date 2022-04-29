import os
import pandas as pd

# *** DEFAULT HEADERS ***
tournaments_header = ['id', 'title', 'place', 'begin_date', 'end_date', 'komi', 'tours', 'rules']
players_header = ['id', 'last_name', 'first_name', 'birth_date', 'town_id', 'rating', 'last_game', 'last_update']
link_pt_header = ['tournament_id', 'player_id', 'place_in_tournament', 'rating_before', 'rating_after',
                  'MM_before', 'MM_cf', 'BHG_cf', 'BER_cf']


# ******


class GoTables:
    def __init__(self, players_t=None, tournaments_t=None, link_pt=None, towns_t=None):
        self.players_t = players_t  # players table
        self.tournaments_t = tournaments_t  # tournaments table
        self.link_pt = link_pt  # table connecting players & tournaments
        self.towns_t = towns_t  # towns table

        if players_t and tournaments_t:
            self._add_players_list()
            self._add_tournaments_list()

    @property
    def players_t(self):
        return self._players_t

    @players_t.setter
    def players_t(self, val):
        if type(val) is None:
            print(f'Players table is not defined')
        elif type(val) is dict:
            self._tournaments_t = val
        elif type(val) is not str:
            print(f'Wrong type {val}. Please specify file path.')
        elif not os.path.exists(val):
            print(f'File {val} does not exist')
        else:
            # Load 'players' table
            players_table = pd.read_csv(val, header=None)
            players_table.columns = players_header

            # To json
            self._players_t = players_table.to_dict(orient='records')
            # self._players_t = players_table

    @property
    def tournaments_t(self):
        return self._tournaments_t

    @tournaments_t.setter
    def tournaments_t(self, val):
        if type(val) is None:
            print(f'Tournaments table is not defined')
        elif type(val) is dict:
            self._tournaments_t = val
        elif type(val) is not str:
            print(f'Wrong type {val}. Please specify file path.')
        elif not os.path.exists(val):
            print(f'File {val} does not exist')
        else:
            # Load 'players' table
            tournaments_table = pd.read_csv(val, header=None)
            tournaments_table.columns = tournaments_header

            # To json
            self._tournaments_t = tournaments_table.to_dict(orient='records')
            # self._tournaments_t = tournaments_table

    @property
    def link_pt(self):
        return self._link_pt

    @link_pt.setter
    def link_pt(self, val):
        if type(val) is None:
            print(f'Players-tournaments table is not defined')
        elif type(val) is not str:
            print(f'Wrong type {val}. Please specify file path.')
        elif not os.path.exists(val):
            print(f'File {val} does not exist')
        else:
            # Load 'players-tournaments' table
            pt_table = pd.read_csv(val, header=None)
            pt_table.columns = link_pt_header

            # To json
            # self._link_pt = pt_table.to_dict(orient='records')
            self._link_pt = pt_table

    def _add_tournaments_list(self):
        for doc in self.players_t:
            p_id = doc['id']
            tournaments_list = self.link_pt.query(f'player_id == {p_id}')['tournament_id'].tolist()
            doc['tournaments'] = tournaments_list

    def _add_players_list(self):
        for doc in self.tournaments_t:
            t_id = doc['id']
            players_list = self.link_pt.query(f'tournament_id == {t_id}')['player_id'].tolist()
            doc['participants'] = players_list


# Test
if __name__ == '__main__':
    gotables = GoTables('./db-samples/players.csv', './db-samples/tournaments.csv',
                        './db-samples/players-tournaments.csv')

    print(gotables.players_t[:4])
