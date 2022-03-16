import json 
from os.path import exists

class UserDefaults:
    def __init__(self):
        # Could add lazy loading 
        if exists('user-defaults.json'):
            with open('user-defaults.json') as file:
                self.data = json.load(file)
        else:
            self.data = {}

    def __getitem__(self, key):
        return self.data.get(key)

    def __setitem__(self, key, value):
        self.data[key] = value
        with open('user-defaults.json', 'w') as file:
            json.dump(self.data, file, indent=4 )