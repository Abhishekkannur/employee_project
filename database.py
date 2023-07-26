from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL='postgresql://postgres:565656@localhost:5432/employee_db'

engine= create_engine(SQLALCHEMY_DATABASE_URL,pool_pre_ping=True)

SessionLocal=sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base= declarative_base()

