from sqlalchemy.engine import create_engine
from sqlalchemy import URL, event
import os
from sqlalchemy.orm import sessionmaker
from app.models.users import Base
from sqlalchemy.schema import CreateSchema
import sqlalchemy.schema
from app import config


db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", "192.168.1.70")
db_name = "users"

url = URL.create(drivername="postgresql+psycopg2", username=db_user, password=db_password, host=db_host, port=5432,
                 database=db_name)

engine = create_engine(url)


Base.metadata.create_all(engine)
SessionLocal = sessionmaker(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
