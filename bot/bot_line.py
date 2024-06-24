from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage
import requests

from module.bot import bot_template

class Bot_Line(bot_template.Bot_Template):
    def __init__(self, jsonfile=None, token=None, secret=None, router=None, app_route=None):
        # jsonファイルが指定されている場合、引数をjsonファイルから読み込む
        config = {}
        if jsonfile is not None:
            config = self.load_json(jsonfile)
        if secret: config['secret'] = secret
        if token: config['token'] = token
        if app_route: config['app_route'] = app_route

        self.line_bot_api = LineBotApi(config['token'])

        # secretが指定されている場合はLINEのメッセージを受信するためにWebhookHandlerを設定
        if 'secret' in config:
            self.handler = WebhookHandler(config['secret'])
            self.recieve_message_feature = True
        else:
            self.recieve_message_feature = False

        # routerが指定されている場合、指定されたrouterを使う
        if router:
            self.router = router
            self.run_router = False
        elif self.recieve_message_feature:
            self.router = Flask(__name__)
            self.run_router = True

        # メッセージを受信したときの処理を設定
        if self.recieve_message_feature:
            @self.router.route(config['app_route'], methods=['POST'])
            def callback():
                signature = request.headers['X-Line-Signature']
                body = request.get_data(as_text=True)
                try:
                    self.handler.handle(body, signature)
                except Exception as e:
                    print(e)
                    abort(400)
                return 'OK'
            
            @self.handler.add(MessageEvent, message=TextMessage)
            def handle_message(event):
                self.on_message(event)

        if 'variable' in config:
            self.variable = config['variable']

    def send_reply_message(self, reply_token, message):
        """
        返信用トークンからメッセージを送信する
        :param reply_token: 送信先のトークン
        :param message: 送信するメッセージ
        :return: None
        """
        self.line_bot_api.reply_message(reply_token, TextMessage(text=message))

    def send_message_by_id(self, id, message):
        """
        IDからメッセージを送信する
        :param id: 送信先のID
        :param message: 送信するメッセージ
        :return: None
        """
        self.line_bot_api.push_message(id, TextMessage(text=message))

    def on_start(self):
        """
        ボットが起動したときに実行される関数
        このクラスを継承したクラスでオーバーライドして使う
        :return: None
        """
        pass

    def on_message(self, event: MessageEvent):
        """
        メッセージを受信したときに実行される関数
        このクラスを継承したクラスでオーバーライドして使う
        :param event: 受信したイベント
        :return: None
        """
        pass

    def run(self, port=5000, host='0.0.0.0', logging=False):
        """
        ボットを起動する
        :param port: webhookをlistenするポート番号
        :return: None
        """
        self.on_start()
        # メッセージを受信する機能が有効で、かつrouterを起動する場合
        if self.recieve_message_feature and self.run_router:
            self.router.run(host=host, port=port,debug=False)
