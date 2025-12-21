from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")        # default admin
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "asd123")
POSTGRES_DB = os.getenv("POSTGRES_DB", "appdb")

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()