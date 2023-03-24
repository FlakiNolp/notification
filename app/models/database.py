from sqlalchemy.engine import create_engine
from sqlalchemy import URL
from os import getenv
from sqlalchemy.orm import sessionmaker
from app.models.users import Base


db_user = getenv("DB_USER", "postgres")
db_password = getenv("DB_PASSWORD")
db_host = getenv("DB_HOST", "localhost")
db_port = getenv("DB_PORT", 6543)

url = URL.create(drivername="postgresql+psycopg2", username=db_user, password=db_password, host=db_host, port=db_port,
                 database="users")

engine = create_engine(url)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()