from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


def create_engine_foo():
    engine = create_engine("postgresql+psycopg2://postgres:1111@localhost/voice", echo=True)
    return engine


engine = create_engine("postgresql+psycopg2://postgres:1111@localhost/voice", echo=True)
session = sessionmaker(bind=create_engine_foo())
s = session()


def get_random_profile(sessionmaker):
    query = text("SELECT * FROM profile ORDER BY RANDOM() LIMIT 1")
    return sessionmaker.execute(query)


def check_user(user_id):
    query = text(f"SELECT * FROM profile WHERE id = '{user_id}'")
    return s.execute(query).first()


