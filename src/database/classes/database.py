import sqlite3
import requests
import json
import os

class Database:
    def __init__(self, patch="latest", auto_commit=True):
        self.patch = patch
        self.auto_commit = auto_commit
        
        # self.database_name = "database.db"
        self.database_name = os.path.join(os.path.dirname(
            __file__), './database.db')
        
        self.conn = sqlite3.connect(self.database_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.base_url = "http://cdn.merakianalytics.com/riot/lol/resources/{}/en-US".format(
            self.patch)
        
    
