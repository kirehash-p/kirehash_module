class SQLTemplate():
    """各SQLモジュールで実行するクエリの生成を行うクラス"""
    def create_table_query(self, table_name, columns):
        columns_str = ", ".join([f"{col[0]} {col[1]} {col[2]}" if len(col) > 2 else f"{col[0]} {col[1]}" for col in columns])
        return f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"

    def insert_query(self, table_name, columns):
        columns_str = ", ".join(columns)
        values_str = ", ".join(["?" for _ in range(len(columns))])
        return f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})"

    def update_query(self, table_name, columns, where):
        columns_str = ", ".join([f"{col} = ?" for col in columns])
        where_str = " AND ".join([f"{col} = ?" for col in where])
        return f"UPDATE {table_name} SET {columns_str} WHERE {where_str}"