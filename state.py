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
        user_data = {}
        try:
            with open(self.data_file()) as data_file:    
                user_data = json.load(data_file)
        except IOError as e:
            pass
        if len(user_data) == 0:
            user_data = {'createdAt': time.strftime("%c")}
        return user_data

    def update_busstop(self, naptan_code):
        user_data = self.load_user_data()
        user_data['mystop'] = naptan_code
        self.save_user_data(user_data)

    def get_busstop(self):
        return self.load_user_data().get('mystop', None)


    def save_user_data(self, user_data):
        with open(self.data_file(), 'w') as outfile:
            json.dump(user_data, outfile)

    def data_file(self):
        return "{}/{}".format(data_folder, self.userId)

    def get_current(self):
        return self.load_user_data().get('current', None)

    def set_current(self, state):
        user_data = self.load_user_data()
        user_data['current'] = state
        self.save_user_data()

    

