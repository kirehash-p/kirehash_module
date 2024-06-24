import discord
import requests

from module.bot import bot_template

class Bot_Discord(bot_template.Bot_Template):
    def __init__(self, jsonfile=None, token=None):
        if jsonfile is not None:
            config = self.load_json(jsonfile)
            self.token = config['token']
        self.discord_client = discord.Client(intents=discord.Intents.all())
        if token: self.token = token
        @self.discord_client.event
        async def on_start():
            await self.on_start()
        @self.discord_client.event
        async def on_message(message: discord.Message):
            await self.on_message(message)

    async def on_start(self):
        """
        ボットが起動したときに実行される関数
        このクラスを継承したクラスでオーバーライドして使用する
        :return: None
        """
        pass

    async def on_message(self, message: discord.Message):
        """
        メッセージを受信したときに実行される関数
        このクラスを継承したクラスでオーバーライドして使用する
        :param message: 受信したメッセージ
        :return: None
        """
        pass

    async def send_reply_message(self, recieved_msg: discord.Message, message):
        """
        メッセージを送信する関数
        :param recieved_msg: 受信したメッセージ
        :param message: 送信するメッセージ
        :return: None
        """
        return await recieved_msg.reply(message)

    async def send_message_by_id(self, channel, message):
        """
        メッセージを送信する関数
        :param channel: 送信するチャンネル。チャンネルのIDか、チャンネルオブジェクトもしくはそれを格納したリストを指定する
        :param message: 送信するメッセージ
        :return: Discordのメッセージオブジェクト
        """
        if type(channel) == str or type(channel) == int:
            channel = self.discord_client.get_channel(int(channel))
        return await channel.send(message)
    
    async def set_status(self, status):
        """
        ボットのステータスを設定する関数
        :param status: ボットのステータス
        :return: None
        """
        await self.discord_client.change_presence(activity=discord.Game(name=status))

    def create_embed(self, title, description, color=0x00ff00):
        """
        Embedを作成する関数
        :param title: Embedのタイトル
        :param description: Embedの説明
        :param color: Embedの色
        :return: Embedオブジェクト
        """
        return discord.Embed(title=title, description=description, color=color)

    def run(self, log_handler=None):
        """
        ボットを起動する関数
        :return: None
        """
        self.discord_client.run(self.token, log_handler=log_handler)
