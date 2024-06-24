import json

class Bot_Template:
    def load_json(self, f):
        with open(f, 'r') as file:
            return json.load(file)

    def run(self):
        pass
