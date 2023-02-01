from sqlalchemy.engine import create_engine
import os
from sqlalchemy.orm import declarative_base, sessionmaker


db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = "users_db"

db_link = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"

Base = declarative_base()
engine = create_engine(db_link)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
