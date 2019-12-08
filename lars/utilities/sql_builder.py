from typing import List, Dict


class SqlBuilder:
    def __init__(self, table_name: str, column_names: List[str], primary_key: str):
        self._table_name = table_name
        self._column_names = column_names
        self._primary_key = primary_key

    @property
    def table_name(self) -> str:
        return self._table_name

    @property
    def column_names(self) -> List[str]:
        return self._column_names

    def build_insert_statement(self) -> str:
        column_count = len(self._column_names)
        value_holders = ['?' for i in range(column_count)]
        return f"insert into {self._table_name} ({', '.join(self._column_names)}) values ({', '.join(value_holders)});"

    def build_select_statement(self) -> str:
        return f"select * from {self._table_name} where {self._primary_key}=?"

    @staticmethod
    def build_meta_select_table_statement() -> str:
        return f"select * from sqlite_master where type = 'table' and name=?"

    def build_meta_select_columns_statement(self) -> str:
        return f"pragma table_info('{self._table_name}')"

    def build_create_table_statement(self) -> str:
        primary_key_line = f'{self._primary_key} text primary key'
        column_lines = [f'{column} text' for column in self._column_names if column != self._primary_key]
        column_lines.insert(0, primary_key_line)
        separator = ',\n'

        return f'create table {self._table_name} (' \
               f'{separator.join(column_lines)}' \
               f')'
