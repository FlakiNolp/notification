from sqlalchemy.engine import create_engine
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker
import api.config as config


class DataBase:
    def __init__(self, db_user: str = config.DB_USER,
                 db_password: str = config.DB_PASSWORD,
                 db_host: str = config.DB_HOST,
                 db_port: int = config.DB_PORT,
                 test_mode: bool = False):
        if test_mode:
            self._url = URL.create(drivername="postgresql+psycopg2", username=db_user, password=db_password,
                                   host=db_host,
                                   port=db_port,
                                   database="test")
        else:
            self._url = URL.create(drivername="postgresql+psycopg2", username=db_user, password=db_password,
                                   host=db_host,
                                   port=db_port,
                                   database="users")
        self._engine = create_engine(self._url)
        self._SessionLocal = sessionmaker(self._engine)

    def create_schema(self, schema):
        schema.metadata.create_all(self._engine)

    def get_db(self):
        db = self._SessionLocal()
        try:
            yield db
        finally:
            db.close()
