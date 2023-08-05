import time
import datetime
import os
import json


class Configuration():
    
    def __init__(self):
    
        self.host = 'http://localhost:8000/rest/'
        
        # dict to store API key(s)
        self.api_key = {}
        # dict to store API prefix (e.g. Bearer)
        self.api_key_prefix = {}
        # Username for HTTP basic authentication
        self.username = ""
        # Password for HTTP basic authentication
        self.password = ""
    