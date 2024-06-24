import logging

class DefaultFilter(logging.Filter):
    """logger用のユーザー定義フィルター"""

    def filter(self, record):
        """呼び出し元のファイル名、関数名、行番号が表示されるようにする関数

        Returns:
            True: 常にフィルターをパスする
        """

        record.real_filename = getattr(record, 'real_filename', record.filename)
        record.real_funcName = getattr(record, 'real_funcName', record.funcName)
        record.real_lineno = getattr(record, 'real_lineno', record.lineno)
        return True