from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base

class DatabaseManager:

    def __init__(self):

        self.__engine = create_engine('sqlite:///database.db')

        self.__session_local = sessionmaker(bind=self.__engine, autoflush=False, autocommit=False)

    def init_db(self):
        Base.metadata.create_all(self.__engine)

    def get_db(self):
        try:
            db = self.__session_local()

            yield db
        finally:
            db.close()
