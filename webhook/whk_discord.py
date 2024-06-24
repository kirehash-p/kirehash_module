import requests

class Webhook_Discord():
    def __init__(self, jsonfile=None, webhook_url=None, username=None, avatar_url=None):
        if jsonfile is not None:
            with open(jsonfile, 'r') as f:
                config = self.load_json(f)
                self.webhook_url = config['webhook_url'] if 'webhook_url' in config else None
                self.username = config['username'] if 'username' in config else None
                self.avatar_url = config['avatar_url'] if 'avatar_url' in config else None
        if webhook_url: self.webhook_url = webhook_url
        if username: self.username = username
        if avatar_url: self.avatar_url = avatar_url

    def send_msg(self, message, embed=False):
        """
        メッセージを送信する関数
        :param message: 送信するメッセージ
        :return: None
        """
        headers = {'Content-Type': 'application/json'}
        content = {
            'username': self.username,
            'avatar_url': self.avatar_url
        }
        if embed:
            content['embeds'] = message
        else:
            content['content'] = message
        res = requests.post(self.webhook_url, json=content, headers=headers)
        return res