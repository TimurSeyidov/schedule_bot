from .config import Config
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from .dao import Base

class DbManager:
    __engine: Engine = None
    __session = None

    def __init__(self, config: Config):
        self.__engine = create_engine(
            config.database_url,
            echo=config.database_echo,
            connect_args={
                "check_same_thread": False
            }
        )
        print(config.database_url)
        self.__session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.__engine
        )


    def create_tables(self):
        Base.metadata.create_all(bind=self.__engine)

    @property
    def session(self) -> Session:
        return self.__session()

    def drop_tables(self):
        Base.metadata.drop_all(bind=self.__engine)