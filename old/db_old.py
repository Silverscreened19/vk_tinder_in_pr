import sqlalchemy
import json
from models import User, Matched, Favorites, create_tables
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker



conn_driver = 'postgresql'
login = 'postgres'
passw = 'postgres'
server_name = 'localhost'
port = '5432'
db_name = 'vkinder'


def insert_data(session): #записываем данные в бд
    with open('user.json') as f:
        data = json.load(f)
        for rec in data:
            model = {
                'users': User,
                # 'matched_users': Matched,
                # 'photos': Photos,
                # 'favorites_users': Favorites
            }[rec.get('model')]
            session.add(model(id=rec.get('pk'), **rec.get('fields')))
        session.commit()



# if __name__ == '__db__':
DSN = f'{conn_driver}://{login}:{passw}:@{server_name}:{port}/{db_name}'
# DSN = 'postgresql://postgres@localhost:5432/vkinder'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()
insert_data(session)
print(session.query(User.id, User.name).all())
session.close()
# with open('user.json') as f:
#         data = json.load(f)
#         for rec in data:
#             print(rec)
