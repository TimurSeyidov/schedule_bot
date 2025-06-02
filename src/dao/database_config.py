import os
from typing import Dict, Optional

class DatabaseConfig:
    def __init__(self, config: Dict[str, Optional[str]]):
        if not config.get('DB_PATH'):
            raise Exception('Не указан путь к БД')
        self.__db_path = config.get('DB_PATH')
        if not config.get('DB_NAME'):
            raise Exception('Не указан файл БД')
        self.__db_name = config.get('DB_NAME')

    @property
    def database_url(self) -> str:
        db_file = os.path.join(
            self.__db_path,
            self.__db_name
        )
        os.makedirs(self.__db_path, exist_ok=True)
        return f'sqlite://{db_file}'
