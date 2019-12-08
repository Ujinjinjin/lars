import sqlite3
from typing import List, Dict

from .sql_builder import SqlBuilder


class DbContext:
    def __init__(self, path: str, db_name: str, column_names: List[str], primary_key: str):
        self.connection = sqlite3.connect(f'{path}/{db_name}')
        self.builder = SqlBuilder(column_names, primary_key)
        self.primary_key = primary_key

        self._initialize_table()

    def _initialize_table(self):
        cursor = self.connection.cursor()
        cursor.execute(self.builder.build_create_table_statement())

    def _log_exists_already(self, pk_value: str) -> bool:
        pass

    # noinspection PyBroadException
    def try_insert_log(self, log_dict: Dict[str, str]) -> bool:
        try:
            if not self._log_exists_already(log_dict[self.primary_key]):
                cursor = self.connection.cursor()
                cursor.execute(self.builder.build_insert_statement(log_dict))
                self.connection.commit()
            return True
        except Exception:
            return False

    def dispose(self):
        self.connection.close()
