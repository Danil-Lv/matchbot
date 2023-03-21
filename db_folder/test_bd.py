from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

def create_engine_foo():
    return create_engine(f"postgresql+psycopg2://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('DB_HOST')}:{getenv('DB_PORT')}/{getenv('DB_NAME')}", echo=True)

session = sessionmaker(bind=create_engine_foo())
s = session()

