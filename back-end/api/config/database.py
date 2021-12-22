from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_SERVER")
port = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DB")

MYSQL_DB = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8"

# Create the SQLAlchemy engine
engine = create_engine(MYSQL_DB, encoding="utf-8", pool_size=20, max_overflow=0)

# Create a SessionLocal class(not database session yet, will be)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()