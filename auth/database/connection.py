from sqlalchemy.engine import create_engine
from sqlalchemy import URL
from os import getenv
from sqlalchemy.orm import sessionmaker
from auth.database.models import Base


class DataBase:
    def __init__(self, db_user=getenv("DB_USER", "postgres"), db_password=getenv("DB_PASSWORD", "postgres"),
                 db_host=getenv("DB_HOST", "localhost"), db_port=getenv("DB_PORT", 6543)):
        self._url = URL.create(drivername="postgresql+psycopg2", username=db_user, password=db_password, host=db_host,
                               port=db_port,
                               database="users")
        self._engine = create_engine(self._url)
        self._SessionLocal = sessionmaker(self._engine)

    def _create_schema(self):
        Base.metadata.create_all(self._engine)

    def _get_db(self):
        db = self._SessionLocal()
        try:
            yield db
        finally:
            db.close()
