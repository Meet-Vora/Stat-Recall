import sqlite3
import requests


class Database:

    def __init__(self, auto_commit=True):
        self.database_name = "database.db"
        self.conn = sqlite3.connect(database_name)
        self.cursor = conn.cursor()
        self.auto_commit = auto_commit
        base_url = "http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US"

    def __get_http_request(self):
        pass

    ### Create and write to tables in database ###
    def __db_execute(self, command):
        """
        Private helper method for creating tables
        """
        self.cursor.execute(command)

    def create_champion_metadata_table(self):
        schema = """
        CREATE TABLE IF NOT EXISTS champion_metadata
        (
            id INTEGER NOT NULL, 
            key TEXT NOT NULL PRIMARY KEY, 
            name TEXT NOT NULL,
            title TEXT NOT NULL,
            fullName TEXT NOT NULL,
            icon TEXT NOT NULL,
            resource TEXT NOT NULL,
            attackType TEXT NOT NULL,
            adaptiveType TEXT NOT NULL
        )
        """
        self.__db_execute(schema)

    def create_champion_stats_table(self):
        schema = """
        CREATE TABLE IF NOT EXISTS champion_base_stats
        (
            key TEXT NOT NULL,
            statName TEXT NOT NULL,
            flat INTEGER NOT NULL,
            percent INTEGER NOT NULL,
            perLevel INTEGER NOT NULL,
            percentPerLevel INTEGER NOT NULL,
            FOREIGN KEY(key) REFERENCES champion_metadata(key)
        )
        """
        self.__db_execute(schema)

    def write_all_champion_metadata(self):
        for champion_name in champion_names['champion']:
            self.__write_champion_metadata(champion_name)

        self.conn.commit()

    def __write_champion_metadata(self, champion_name):
        url = self.base_url + "/champions/" + champion_name + ".json"
        request = self.__get_http_request(url)
        request_data = request.json()
        insert_command = """ INSERT INTO 
        
        """

    def write_all_champion_stats(self, champion_name):
        pass

    def __write_champion_stats(self, champion_name):
        pass

    ### Read from tables in database ###

    def get_all_champion_metadata(self):
        """
        Return:
        all champion metadata in JSON python object
        """
        pass

    def get_all_champion_stats(self):
        """
        Return:
        all champion stat data in JSON python object
        """
        pass

    def get_champion_metadata(self, champion_name):
        """
        Return:
        champion data in JSON python object
        """
        pass

    def get_champion_stats(self, champion_name):
        """
        Return:
        champion data in JSON python object
        """
        pass

    # create_table() method with passed-in schema
    # read_table() method

    def close(self):
        self.conn.close()
