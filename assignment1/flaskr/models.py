import os
import json
import bcrypt
import uuid

class KomradeConfig:
    def __init__(self, name):
        self.config_file = os.path.join(os.path.dirname(__file__), "../" + name + ".json")

        if not os.path.exists(self.config_file):
            open(self.config_file, "w").write("{}")

    def read(self):
        return json.loads(open(self.config_file, "r").read())

    def write(self, data):
        with open(self.config_file, 'w') as fh:
            fh.write(json.dumps(data))

def registerUser(username, password):
    komrade = KomradeConfig("user")
    
    # Implement me

    return None

def validateUser(username, password):
    komrade = KomradeConfig("user")

    # Implement me

    return None
