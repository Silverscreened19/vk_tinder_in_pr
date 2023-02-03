import psycopg2
import json
from main import User
from main import VK_b
from pprint import pprint

user = User()
vk_b = VK_b()
connection = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='postgres',
    database='vkinder'
)

connection.autocommit = True


def create_table_user():
    '''создание таблицы с пользователями, общающимися с ботом'''
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
                name text NOT NULL,
                age text NOT NULL,
                sex INTEGER NOT NULL,
                city text NOT NULL,
                vk_id_u INTEGER PRIMARY KEY);"""
        )
    print("[INFO] Table USERS was created.")
# id_user serial NOT NULL PRIMARY KEY,

def create_table_matched_users():
    '''создание таблицы с пользователями, подошедшими под критерии поиска'''
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS matched_users(
                id_matched INTEGER PRIMARY KEY,
                name varchar NOT NULL,
                link varchar NOT NULL,
                vk_id_u INTEGER REFERENCES users(vk_id_u));"""
        )
    print("[INFO] Table MATCHED_USERS was created.")
# id_matched serial NOT NULL PRIMARY KEY,

def create_table_favorite_users():
    '''создание таблицы с избранными пользователями'''
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS favorite_users(
                id_favorite serial NOT NULL PRIMARY KEY,
                id_matched INTEGER REFERENCES matched_users(id_matched));"""
        )
    print("[INFO] Table FAVORITE_USERS was created.")


def create_table_photos():
    '''создание таблицы с фотографиями matched_users'''
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS photos(
                id_photos serial NOT NULL PRIMARY KEY,
                id_matched INTEGER REFERENCES matched_users(id_matched),
                photo_1 varchar NOT NULL,
                photo_2 varchar NULL,
                photo_3 varchar NULL);"""
        )
    print("[INFO] Table PHOTOS was created.")


def drop_users():
    """УДАЛЕНИЕ ТАБЛИЦЫ USERS КАСКАДОМ"""
    with connection.cursor() as cursor:
        cursor.execute(
            """DROP TABLE IF EXISTS users CASCADE;"""
        )
        print('[INFO] Table USERS was deleted.')


def drop_matched_users():
    """УДАЛЕНИЕ ТАБЛИЦЫ MATCHED USERS КАСКАДОМ"""
    with connection.cursor() as cursor:
        cursor.execute(
            """DROP TABLE IF EXISTS matched_users CASCADE;"""
        )
        print('[INFO] Table MATCHED_USERS was deleted.')


def drop_favorite_users():
    """УДАЛЕНИЕ ТАБЛИЦЫ FAVORITE USERS КАСКАДОМ"""
    with connection.cursor() as cursor:
        cursor.execute(
            """DROP TABLE IF EXISTS favorite_users CASCADE;"""
        )
        print('[INFO] Table FAVORITE_USERS was deleted.')


def drop_photos():
    """УДАЛЕНИЕ ТАБЛИЦЫ PHOTOS КАСКАДОМ"""
    with connection.cursor() as cursor:
        cursor.execute(
            """DROP TABLE IF EXISTS photos CASCADE;"""
        )
        print('[INFO] Table PHOTOS was deleted.')


def insert_matched_users(user_id):
    '''запись данных в таблицу с пользователями, подошедшими под критерии поиска'''
    m_info = vk_b.make_list_id_2(user_id)
    for item in m_info:
        with connection.cursor() as cursor:
            cursor.execute(f"""INSERT INTO matched_users (id_matched, name, link, vk_id_u)
                VALUES ('{item['u_id']}', '{item['info']['name']}', '{item['info']['user_link']}', '{user_id}');"""
                            )
    print('Данные о подобранных пользователях внесены в бд')


def insert_users(user_id):
    '''запись данных о пользователях, общающихся с ботом'''
    u_info = user.user_info(user_id)
    with connection.cursor() as cursor:
        for item in u_info['response']:
            f_name = item['first_name']
            l_name = item['last_name']
            u_name = f'{f_name} {l_name}'
            age = user.user_age(user_id)
            sex = item['sex']
            city = item['city']['title']
            vk_id = item['id']


        cursor.execute(f"""INSERT INTO users (name, age, sex, city, vk_id_u)
            VALUES ('{u_name}', '{age}', '{sex}', '{city}', '{vk_id}');"""
                       )
    print(f'запись о пользователе {u_name} внесена в базу')

def insert_photos(user_id):
    ''''''
    p_info = vk_b.photo_profile(user_id)
    with connection.cursor() as cursor:
        for item in p_info:
            if len(item) == 1:
                cursor.execute(f"""INSERT INTO photos (id_matched, photo_1)
                            VALUES ('{item[0][2]}', '{item[0][1]}');"""
                                    )
            elif len(item) == 2:
                cursor.execute(f"""INSERT INTO photos (id_matched, photo_1, photo_2)
                            VALUES ('{item[0][2]}', '{item[0][1]}', '{item[1][1]}');"""
                                    )
            elif len(item) == 3:
                cursor.execute(f"""INSERT INTO photos (id_matched, photo_1, photo_2, photo_3)
                            VALUES ('{item[0][2]}', '{item[0][1]}', '{item[1][1]}', '{item[2][1]}');"""
                                    )
            else:
                print('неверная длина списка photo_profile()')
    print('Данные о фотографиях внесены')

def show_users():
    '''вывод данных об пользователях, общающихся с ботом'''
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM users;""")
        print(cursor.fetchall())


def show_matched_users():
    '''вывод данных о пользователях, подошедших под критерии поиска'''
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM matched_users;""")
        print(cursor.fetchall())

def show_photos():
    '''вывод данных о фотках пользователей, подошедших под критерии поиска'''
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM photos;""")
        pprint(cursor.fetchall())


# drop_users()
# drop_matched_users()
# drop_favorite_users()
# drop_photos()
# create_table_user()
# create_table_matched_users()
# create_table_favorite_users()
# create_table_photos()
# insert_users(2373876)
# insert_matched_users(2373876)
# insert_photos(2373876)
# show_users()
# show_matched_users()
# show_photos()
