from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine(database_url):
    return create_engine(database_url)


def make_session(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
