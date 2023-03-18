from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine, Column, Integer, String, text, BigInteger
from sqlalchemy import update

from sqlalchemy_folder.test_bd import s

from sqlalchemy.sql.expression import select

engine = create_engine("postgresql+psycopg2://postgres:1111@localhost/voice", echo=True)

Base = declarative_base()


class Profile(Base):
    __tablename__ = 'profile'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    city = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=False)
    description = Column(String(50))
    photo = Column(String(), nullable=False)


Base.metadata.create_all(bind=engine)



def create_user(user_id, data):
    """Создание пользователя"""
    query_check_user = text(f"SELECT 1 FROM profile WHERE id = {user_id}")
    user = s.execute(query_check_user).first()
    if not user:
        s.add(Profile(id=user_id, name=data["name"], age=data["age"], city=data["city"],
                      description=data["description"], gender=data["gender"], photo=data["photo"]))
        s.commit()
    else:
        s.execute(
            update(Profile).where(Profile.id == user_id).values(name=data["name"], age=data["age"], city=data["city"],
                                                                description=data["description"], gender=data["gender"],
                                                                photo=data["photo"]))


def get_user(user_id):
    res = s.execute(select(Profile).where(Profile.id == user_id)).fetchone()
    if res:
        return res._asdict()
