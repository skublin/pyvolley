import re
import random
import logging
import requests
import pandas as pd
import sqlite3 as sl

from bs4 import BeautifulSoup
from datetime import datetime

from team import Team
from player import Player


logging.basicConfig(filename='data.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logging.info(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

TEAM_NAMES = ['Aluron CMC Warta Zawiercie', 
              'Asseco Resovia Rzeszów', 
              'Barkom Każany Lwów', 
              'BBTS Bielsko-Biała', 
              'Cerrad Enea Czarni Radom', 
              'Cuprum Lubin',
              'GKS Katowice',
              'Grupa Azoty ZAKSA Kędzierzyn-Koźle',
              'Indykpol AZS Olsztyn',
              'Jastrzębski Węgiel',
              'LUK Lublin', 
              'PGE Skra Bełchatów', 
              'Projekt Warszawa',
              'PSG Stal Nysa',
              'Ślepsk Malow Suwałki', 
              'Trefl Gdańsk']


class Data:
    def __init__(self):
        self.URL = "https://www.plusliga.pl"
        self.PLAYERS_URL = self.URL + "/players.html"
        self.TEAMS_URL = self.URL + "/teams.html"
        self.PLAYER_BASE_LOCATION = "/players/id/"
        self.TEAM_BASE_LOCATION = "/teams/id/"
        self.Teams, self.Players = dict(), dict()
        self.data = {"teams": self.Teams, "players": self.Players}
        self.con = sl.connect("plusliga.db")

    def download_players(self):
        self.page = requests.get(self.PLAYERS_URL)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        self.links = self.soup.findAll("a", href=True)
        
        self.con = sl.connect("plusliga.db")

        try:
            with self.con:
                # first, create new table
                self.con.execute("""
                            CREATE TABLE PLAYER 
                            (
                                id INTEGER NOT NULL PRIMARY KEY,
                                name TEXT,
                                team TEXT,
                                birth DATE,
                                position TEXT,
                                number INTEGER,
                                height INTEGER,
                                weight INTEGER,
                                jump INTEGER,
                                site TEXT
                            );
                            """)
        except Exception as e:
            logging.error(e)
            logging.debug("Couldn't create new table (may already exist).")

        self.players_idx = set()

        insert = "INSERT INTO PLAYER (id, name, team, birth, position, number, height, weight, jump, site) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        i = 0
        for a in self.links:
            link = a["href"]
            if re.match(self.PLAYER_BASE_LOCATION, link):
                player_site = self.URL + link
                player_id = player_site.split("/")[-1].split(".")[0]
                if player_id not in self.players_idx:
                    player = self.get_player_data(player_site, player_id)
                    try:
                        with self.con:
                            self.con.execute(insert, player)
                            self.Players[player[0]] = Player(*player)
                            self.players_idx.add(player_id)
                            i += 1
                            if i % 10 == 0:
                                print(f"{i} done...")
                            logging.info(f"Player {i} - done.")
                    except Exception as e:
                        logging.error(e)
                        logging.debug(f"i = {i}, player = {player[1]}, old id = {player_id}, new id = {player[0]}")
                        logging.debug(f"player site -> {player[-1]}")

    def get_player_data(self, site, old_id):
        page = requests.get(site)

        s = BeautifulSoup(page.content, "html.parser")

        info = s.find("div", class_="col-xs-12 col-md-8 col-lg-9")

        name = info.find("h1", class_="playername").string
        team = info.find("div", class_="playerteamname")
        team_name = re.sub(' +', ' ', team.find('span').string)
        birth = info.find("div", class_="col-sm-4 col-md-4 col-lg-3 col-sm-offset-2 col-lg-offset-3").find('span').string
        if birth[0] == ' ':
            birth = birth[1:]
        position = info.find("div", class_="col-sm-5 col-md-4").find('span').string
        number_div = s.find("div", class_="playernumber")
        number = number_div.find('span').string
        height = info.find("div", class_="col-sm-3 col-md-3 col-lg-3 col-lg-offset-1").find('span').string
        weight = info.find("div", class_="col-sm-3 col-md-3 col-lg-3").find('span').string
        jump = info.find("div", class_="col-sm-6 col-md-6 col-lg-4").find('span').string

        return (self.generate_player_idx(old_id), name, team_name, birth, position, self.change_to_int(number), self.change_to_int(height), self.change_to_int(weight), self.change_to_int(jump), site)

    def download_teams(self):
        # just download basic information about teams
        self.websites = self.get_teams_links()

        self.create_teams_table()

        self.headers = {"Nazwa drużyny": "name", "Pierwszy trener": "coach", "Adres": "address"}

        insert = "INSERT INTO TEAM (id, name, address, coach, site) values(?, ?, ?, ?, ?)"

        i = 0
        for site in self.websites:
            team = self.get_team_data(site)
            try:
                with self.con:
                    self.con.execute(insert, team)
                    self.Teams[team[0]] = Team(*team)
                    i += 1
                    print(f"{i} done...")
                    logging.info(f"Team {i} - done.")
            except Exception as e:
                logging.error(e)
                logging.debug(f"i = {i}, team = {team[1]}, team site -> {team[-1]}")

    def get_team_data(self, site):
        result = dict()

        team_site = self.URL + site
        result["site"] = team_site

        p = requests.get(team_site)
        s = BeautifulSoup(p.content, "html.parser")

        info = s.findAll("div", class_="col-sm-12")
        t = set(re.sub("[\n\t\r]", "*", info[6].text).split("*"))

        for value in t:
            v = value.split(":")
            if v[0] in self.headers:
                result[self.headers[v[0]]] = v[1]

        old_idx = site.split("/")[-1].split(".")[0]
        result["idx"] = self.generate_team_idx(old_idx)

        team_name = re.sub('\s+', ' ', result["name"])
        if team_name[0] == ' ':
            team_name = team_name[1:]

        return (result["idx"], team_name, result["address"], result["coach"], result["site"])

    def get_teams_links(self):
        page = requests.get(self.TEAMS_URL)
        soup = BeautifulSoup(page.content, "html.parser")
        section = soup.find("div", class_="col-sm-12")
        links = section.findAll("a", href=True)
        result = set()
        for link in links:
            current = link["href"]
            if re.match(self.TEAM_BASE_LOCATION, current):
                result.add(current)
        
        return result

    def create_teams_table(self):
        try:
            with self.con:
                self.con.execute("""
                            CREATE TABLE TEAM
                            (
                                id INTEGER NOT NULL PRIMARY KEY,
                                name TEXT,
                                address TEXT,
                                coach TEXT,
                                site TEXT
                            );
                            """)
        except Exception as e:
            logging.error(e)
            logging.debug("Couldn't create new table (may already exist).")

    def generate_player_idx(self, current_id):
            # method to generate player's random, individual index, based on index from website
            random.seed(current_id)
            result = random.randint(10000, 99999)
            while result in self.Players:
                result = random.randint(10000, 99999)
            return result

    def generate_team_idx(self, current_id):
            # method to generate team's random, individual index, based on index from website
            random.seed(current_id)
            result = random.randint(1000, 9999)
            while result in self.Teams:
                result = random.randint(1000, 9999)
            return result

    @staticmethod    
    def change_to_int(value):
        try:
            return int(value)
        except ValueError:
            return 0
    
    def download_data(self):
        # method to download data to database

        def download_teams():
            pass

        def create_players_database():
            pass

        def create_teams_database():
            pass
    
    def load_data(self):
        teams = self.load_teams()
        players = self.load_players()

        self.Teams = dict()
        self.Players = dict()
        
        for index, row in teams.iterrows():
            self.Teams[row['name']] = Team(row['id'], row['name'], row['address'], row['coach'], row['site'])

        for index, row in players.iterrows():
            idx = row['id']
            # create new Player object
            p = Player(idx, row['name'], row['team'], row['birth'], row['position'], row['number'], row['height'], row['weight'], row['jump'], row['site'])
            # save player
            self.Players[idx] = p
            # add player to team
            self.Teams[p.team_name].add_player(p)

    def load_players(self):
        with self.con:
            try:
                players = pd.read_sql('''SELECT * FROM PLAYER''', self.con)
                players.sort_values(by=['team', 'number', 'name'], inplace=True)
            except Exception as e:
                logging.error(e)
                logging.debug("Couldn't load PLAYER table, trying to create new one...")

                self.download_players()

                players = self.load_players()
        
        return players

    def load_teams(self):
        with self.con:
            try: 
                teams = pd.read_sql('''SELECT * FROM TEAM''', self.con)
                teams.sort_values(by='name', inplace=True)
            except Exception as e:
                logging.error(e)
                logging.debug("Couldn't load TEAM table, trying to create new one...")

                self.download_teams()

                teams = self.load_teams()
        
        return teams
