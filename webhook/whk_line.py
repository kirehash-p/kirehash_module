import requests

class Webhook_Line():
    def __init__(self, jsonfile=None, token=None):
        # jsonファイルが指定されている場合、引数をjsonファイルから読み込む
        if jsonfile is not None:
            with open(jsonfile, 'r') as f:
                config = self.load_json(f)
                self.token = config['token']
        if token: self.token = token

    def send_msg(self, message):
        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {self.token}'}
        payload = {'message': message}
        res = requests.post(line_notify_api, headers=headers, data=payload)
        return res