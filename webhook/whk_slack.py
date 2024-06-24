import requests

class Webhook_Slack():
    def __init__(self, jsonfile=None, webhook_url=None):
        if jsonfile is not None:
            with open(jsonfile, 'r') as f:
                config = self.load_json(f)
                self.webhook_url = config['webhook_url'] if 'webhook_url' in config else None
        if webhook_url: self.webhook_url = webhook_url

    def send_msg(self, message, attatchments=False):
        headers = {'Content-Type': 'application/json'}
        if attatchments:
            content = {
                'attachments': message
            }
        else:
            content = {
                'text': message
            }
        res = requests.post(self.webhook_url, json=content, headers=headers)
        return res