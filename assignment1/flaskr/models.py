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

    user_store = komrade.read()
    if username in user_store:
        raise NameError("User already exists in database")

    pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_store[username] = pw_hash.decode('utf-8')

    komrade.write(user_store)

def validateUser(username, password):
    komrade = KomradeConfig("user")

    user_store = komrade.read()
    if not username in user_store:
        return False

    stored_pw = user_store[username].encode('utf-8')

    return bcrypt.hashpw(password.encode('utf-8'), stored_pw) == stored_pw 
