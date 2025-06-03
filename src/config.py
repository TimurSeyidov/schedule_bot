import os
from typing import Dict, Optional
from dotenv import dotenv_values

class Config:
    __config: Dict[str, Optional[str]] = None
    __start_path: str = None

    def __init__(self, path_of_config: str, start_path: str = None):
        _path_of_config = path_of_config
        if start_path:
            _path_of_config = os.path.join(start_path, _path_of_config)
        self.__start_path = start_path
        if not os.path.exists(_path_of_config) or not os.path.isfile(_path_of_config):
            raise Exception( f'Файл настроек {_path_of_config} не найден')
        self.__config = dotenv_values(_path_of_config)
        params = ['BOT_API_KEY', 'DB_PATH', 'DB_NAME']
        for param in params:
            if not self.__config.get(param):
                raise Exception(f'Не указан параметр {param}')

    @property
    def bot_api_key(self):
        return self.__config.get('BOT_API_KEY')

    @property
    def database_url(self) -> str:
        db_file = os.path.join(
            self.__start_path,
            self.__config.get('DB_PATH'),
            self.__config.get('DB_NAME')
        )
        if db_file.startswith('/') and not db_file.startswith('//'):
            db_file = '/' + db_file
        os.makedirs(self.__config.get('DB_PATH'), exist_ok=True)
        return f'sqlite://{db_file}'

    @property
    def database_echo(self) -> bool:
        return self.__config.get('DB_ECHO', 'False').lower() == 'true'
