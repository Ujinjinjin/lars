from typing import List, Dict


class SqlBuilder:
    def __init__(self, column_names: List[str], primary_key: str):
        self.column_names = column_names
        self.primary_key = primary_key

    def build_insert_statement(self, log_dict: Dict[str, str]) -> str:
        pass

    def build_select_statement(self) -> str:
        pass

    def build_create_table_statement(self) -> str:
        pass
