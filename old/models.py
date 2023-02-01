import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

# таблица с данными исходного пользователя Users (пол, город, возраст, юзер_айди_исх),
# таблица со всеми кто совпал(юзер_айди_исх, фио, ссылка),
# таблица с фотками(юзер_айди_мэтчд, 3 столбца с фотами(2 из них нулл)),
# таблица с избранными (юзер_айди_мэтчд)

Base = declarative_base()


class User(Base): # данные пользователя, который общается с ботом
    __tablename__ = 'users'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, nullable=False) # имя и фамилию пишем в одной строке таблицы
    age = sq.Column(sq.Integer, nullable=False) # ограничение по возрасту, не более 100 лет?)
    sex = sq.Column(sq.String, nullable=False)
    city = sq.Column(sq.String, nullable=False)


class Matched(Base):
    __tablename__ = 'matched_users'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, nullable=False)
    link = sq.Column(sq.String, nullable=False)
    id_user = sq.Column(sq.Integer, sq.ForeignKey(
        'users.id'), nullable=False)

    user = relationship(User, backref='matched_users')


class Photos(Base):
    __tablename__ = 'photos'

    id = sq.Column(sq.Integer, primary_key=True)
    id_matched = sq.Column(sq.Integer, sq.ForeignKey(
        'matched_users.id'), nullable=False)
    photos_link_1 = sq.Column(sq.String, nullable=False)
    photos_link_2 = sq.Column(sq.String, nullable=True)
    photos_link_3 = sq.Column(sq.String, nullable=True)

    matched = relationship(Matched, backref='photos')


class Favorites(Base):
    __tablename__ = 'favorites_users'

    id = sq.Column(sq.Integer, primary_key=True)
    id_matched = sq.Column(sq.Integer, sq.ForeignKey(
        'matched_users.id'), nullable=False)

    matched = relationship(Matched, backref='favorites_users')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
