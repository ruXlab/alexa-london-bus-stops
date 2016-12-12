import json
import os
import time

data_folder = "users"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

class State:
    def __init__(self, _session): 
        self.userId = _session.user.userId or None

    def load_user_data(self):
        json = {}
        try:
            with open(self.data_file()) as data_file:    
                json = json.load(data_file)
        except IOError as e:
            pass
        if len(json) == 0:
            json = {'createdAt': time.strftime("%c")}
        return json

    def update_busstop(self, naptan_code):
        user_data = self.load_user_data()
        user_data['mystop'] = naptan_code
        with open(self.data_file(), 'w') as outfile:
            json.dump(user_data, outfile)

    def data_file(self):
        return "{}/{}".format(data_folder, self.userId)

