import sqlite3 as sl

from data import Data


class Engine:
    """
    Class to represent engine - load data objects from Data class (data.py), 
    store it as cache and compute all necessary operations.
    This should be used to add any method for logical part of the application.
    """
    def __init__(self):
        self.cache = {'data': Data()}
        self.cache['data'].load_data()

    def get_data_for_table(self, team_name):
        team = self.cache['data'].Teams[team_name]    # TODO : sort players by number, name, etc. (feature)
        numbers = [str(player.number) for player in team.players]

        return {'size': len(team.players), 'players': team.players, 'numbers': numbers}

    def prepare_games(self):
        # this method is for future use - to load and show previous games
        pass

    def start():
        pass


if __name__ == "__main__":
    e = Engine()
    
    # print(sorted(e.cache['data'].Teams['LUK Lublin'].players))
