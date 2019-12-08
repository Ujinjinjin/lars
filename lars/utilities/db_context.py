import sqlite3
from typing import Dict

from .sql_builder import SqlBuilder


class DbContext:
    def __init__(self, path: str, db_name: str, primary_key: str, builder: SqlBuilder):
        self.connection = sqlite3.connect(f'{path}/{db_name}')
        self.builder = builder
        self.primary_key = primary_key

        self._initialize_table()

    def _initialize_table(self):
        if not self._table_exists_already():
            cursor = self.connection.cursor()
            cursor.execute(self.builder.build_create_table_statement())
            cursor.close()

    def _table_exists_already(self) -> bool:
        cursor = self.connection.cursor()
        cursor.execute(self.builder.build_meta_select_table_statement(), (self.builder.table_name,))
        table = cursor.fetchone()

        if table is None:
            cursor.close()
            return False

        cursor.execute(self.builder.build_meta_select_columns_statement())
        existing_column_names = [column_meta[1] for column_meta in cursor.fetchall()]
        cursor.close()

        for column_name in self.builder.column_names:
            if column_name not in existing_column_names:
                raise Exception(f'Table {self.builder.table_name} exists already, but columns does not match!')

        return True

    def _log_exists_already(self, pk_value: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute(self.builder.build_select_statement(), (pk_value,))

        log = cursor.fetchone()
        cursor.close()
        return log is not None

    # noinspection PyBroadException
    def insert_log(self, log_dict: Dict[str, str]):
        cursor = self.connection.cursor()
        if not self._log_exists_already(log_dict[self.primary_key]):
            value_tuple = tuple([log_dict[column_name] for column_name in self.builder.column_names])
            cursor.execute(self.builder.build_insert_statement(), value_tuple)
            self.connection.commit()
        cursor.close()

    def dispose(self):
        self.connection.close()
