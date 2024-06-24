
from datetime import datetime
import logging.handlers
import requests
import logging
import threading                                              

from module.sql import sqlite, mariadb
from module.mytime import mytime

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class ConsoleHandler(logging.StreamHandler):
    """コンソールにログを表示するためのハンドラー

    logging.StreamHandlerを継承している
    """

    def __init__(self, *args, **kwargs):
        """コンストラクタ"""

        super().__init__(*args, **kwargs)

class FileHandler(logging.FileHandler):
    """ファイルにログを保存するためのハンドラー

    logging.FileHandlerを継承している
    """

    def __init__(self, *args, **kwargs):
        """コンストラクタ

        Args:
            file_path (str): ログファイルのパス
        """

        super().__init__(*args, **kwargs)

class RotatingFileHandler(logging.handlers.RotatingFileHandler):
    """ファイルにログを保存するためのハンドラー

    logging.handlers.RotatingFileHandlerを継承している
    """

    def __init__(self, *args, **kwargs):
        """コンストラクタ

        Args:
            file_path (str): ログファイルのパス
        """

        super().__init__(*args, **kwargs)

class TimeRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """ファイルにログを保存するためのハンドラー

    logging.handlers.TimedRotatingFileHandlerを継承している
    """

    def __init__(self, *args, **kwargs):
        """コンストラクタ

        Args:
            file_path (str): ログファイルのパス
        """

        super().__init__(*args, **kwargs)

class SQLHandler(logging.Handler):
    """SQLにログを保存するためのハンドラー"""

    def __init__(self, db_config):
        """コンストラクタ

        Args:
            db_config (dict): DBの設定情報
        """

        super().__init__()
        self.tablename = db_config['table_name']
        # ログレコードのカラム
        self.db_record_columns = [
            ('id', 'INTEGER', 'PRIMARY KEY', 'AUTOINCREMENT'),
            ('created', 'DATETIME'),
            ('level', 'INTEGER'),
            ('message', 'TEXT'),
            ('filename', 'TEXT'),
            ('funcName', 'TEXT'),
            ('lineno', 'INTEGER'),
        ]
        # ログレコードのうち、AUTOINCREMENT以外のカラム名。
        self.db_record_insert_columns = [column[0] for column in self.db_record_columns if 'AUTOINCREMENT' not in column]

    def db_record_val(self, record):
        """ログレコードの値

        Args:
            record (logging.LogRecord): ログレコード

        Returns:
            tuple: ログレコードの値
        """

        return [
            datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S.%f'),
            record.levelno,
            record.getMessage(),
            record.real_filename,
            record.real_funcName,
            record.real_lineno,
        ]

class SQLiteHandler(SQLHandler):
    """SQLite3にログを保存するためのハンドラー"""

    def __init__(self, db_config):
        """コンストラクタ

        Args:
            db_config (dict): DBの設定情報
        """

        super().__init__(db_config)
        self.db = sqlite.Sqlite(db_config)
        self.db.create_table(self.tablename, self.db_record_columns)

    def emit(self, record):
        """ログの書き込み

        Args:
            record (logging.LogRecord): ログレコード
        """

        self.db.insert(self.tablename, self.db_record_insert_columns, self.db_record_val(record))

class MariaDBHandler(SQLHandler):
    """MariaDBにログを保存するためのハンドラー"""

    def __init__(self, db_config):
        super().__init__(db_config)
        self.db = mariadb.MariaDB(db_config)
        self.db.create_table(db_config['table_name'], self.db_record_columns)

    def emit(self, record):
        self.db.insert(self.tablename, self.db_record_insert_columns, self.db_record_val(record))

class WebhookHandler(logging.Handler):
    """メッセージアプリにログを送信するためのハンドラー"""
    
    def __init__(self, webhook_url):
        """コンストラクタ
        
        Args:
            webhook_url (str): メッセージアプリのWebhook URL
        """
        super().__init__()
        self.webhook = webhook_url

    @threaded
    def post_message(self, content):
        """メッセージの送信

        Args:
            dumped_contents (str): メッセージのJSON文字列
        """

        headers = {'Content-Type': 'application/json'}
        requests.post(self.webhook, json=content, headers=headers)

    def get_message_dict(self, record):
        """メッセージの辞書を取得

        Args:
            record (logging.LogRecord): ログレコード

        Returns:
            dict: メッセージの辞書
        """

        return {
            'created': record.created,
            'level': record.levelname,
            'levelno': record.levelno,
            'message': record.getMessage(),
            'filename': record.real_filename,
            'funcName': record.real_funcName,
            'lineno': record.real_lineno,
        }

def sanitize(strings):
    chars = ['*', '`', '_', '~', '>']
    for char in chars:
        strings = strings.replace(char, f'\\{char}')
    return strings

class DiscordHandler(WebhookHandler):
    """Discordにログを送信するためのハンドラー"""

    def __init__(self, bot_config):
        """コンストラクタ

        Args:
            bot_config (dict): Botの設定情報
        """

        super().__init__(bot_config['webhook_url'])
        self.username = bot_config['username']
        self.avatar_url = bot_config['avatar_url']

    def emit(self, record):
        """ログの送信

        Args:
            record (logging.LogRecord): ログレコード
        """

        message = self.get_message_dict(record)
        content = self.create_content(message)
        self.post_message(content)

    def create_content(self, message):
        """メッセージの作成

        Args:
            message (dict): メッセージの辞書
        """

        def color_by_level(levelno):
            if levelno <= logging.DEBUG:
                color = '10066329'
            elif levelno <= logging.INFO:
                color = '16777215'
            elif levelno <= logging.WARNING:
                color = '16776960'
            elif levelno <= logging.ERROR:
                color = '16711680'
            elif levelno <= logging.CRITICAL:
                color = '10038562'
            else:
                color = '0'
            return int(color)

        embeds = [
            {
                'title': message['level'],
                'description': f'@ {sanitize(message["filename"])} \- {sanitize(message["funcName"])} : {message["lineno"]}\n```\n{message["message"]}```',
                'timestamp': mytime.datetime_to_utc(datetime.fromtimestamp(message['created'])).strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'color': color_by_level(message['levelno']),
            }
        ]

        content = {
            'embeds': embeds,
        }
        if self.username:
            content['username'] = self.username
        if self.avatar_url:
            content['avatar_url'] = self.avatar_url

        return content

class SlackHandler(WebhookHandler):
    """Slackにログを送信するためのハンドラー"""

    def __init__(self, bot_config):
        """コンストラクタ

        Args:
            bot_config (dict): Botの設定情報
        """

        super().__init__(bot_config['webhook_url'])

    def emit(self, record):
        """ログの送信

        Args:
            record (logging.LogRecord): ログレコード
        """

        message = self.get_message_dict(record)
        content = self.create_content(message)
        self.post_message(content)

    def create_content(self, message):
        """メッセージの作成

        Args:
            message (dict): メッセージの辞書
        """

        def color_by_level(levelno):
            if levelno <= logging.DEBUG:
                color = '#999999'
            elif levelno <= logging.INFO:
                color = '#FFFFFF'
            elif levelno <= logging.WARNING:
                color = '#FFFF00'
            elif levelno <= logging.ERROR:
                color = '#FF0000'
            elif levelno <= logging.CRITICAL:
                color = '#992D22'
            else:
                color = '#000000'
            return color

        attachments = [
            {
                'fallback': message['level'],
                'color': color_by_level(message['levelno']),
                'fields': [
                    {
                        'title': message['level'],
                        'value': f'@ {sanitize(message["filename"])} - {sanitize(message["funcName"])} : {message["lineno"]}\n```\n{message["message"]}\n```',
                        'short': False,
                        'mrkdwn': True,
                    }
                ],
                'ts': message['created'],
            }
        ]

        content = {
            'attachments': attachments,
        }

        return content
