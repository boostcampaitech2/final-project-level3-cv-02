from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

load_dotenv(verbose=True)

# database URL for SQLAlchemy
MYSQL_DB = "mysql+pymysql://cv02:boostcampcv02@cv02.cufn2thqplnf.ap-northeast-2.rds.amazonaws.com:3306/cv02?charset=utf8"

# Create the SQLAlchemy engine
engine = create_engine(MYSQL_DB, encoding="utf-8")

# Create a SessionLocal class(not database session yet, will be)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()