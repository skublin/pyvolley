from player import Player


class Team:
    def __init__(self, idx, name, address, coach, site):
        self.idx = idx
        self.name = name
        self.address = address
        self.coach = coach
        self.site = site
        # TODO : players as list or dict better (?)
        self.players = []

    def add_player(self, player):
        if type(player) is Player:
            if not player in self.players:
                self.players.append(player)
                player.team = self

    def remove_player(self, player):
        if type(player) is Player:
            if player in self.players:
                self.players.remove(player)
                player.team = None
