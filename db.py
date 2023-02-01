import psycopg2
import json

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
                id_user serial NOT NULL PRIMARY KEY,
                name varchar NOT NULL,
                age INTEGER NOT NULL,
                sex varchar(7) NOT NULL,
                city varchar(80) NOT NULL);"""
        )
    print("[INFO] Table USERS was created.")


def create_table_matched_users():
    '''создание таблицы с пользователями, подошедшими под критерии поиска'''
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS matched_users(
                id_matched serial NOT NULL PRIMARY KEY,
                name varchar NOT NULL,
                link varchar NOT NULL,
                id_user INTEGER REFERENCES users(id_user));"""
        )
    print("[INFO] Table MATCHED_USERS was created.")


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
                photo_2 varchar NOT NULL,
                photo_3 varchar NOT NULL);"""
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


def insert_matched_users():
    '''запись данных в таблицу с пользователями, подошедшими под критерии поиска'''
    with open('data_test.json') as f:
        data = json.load(f)
        for item in data:
            with connection.cursor() as cursor:
                cursor.execute(f"""INSERT INTO matched_users (name, link)
                    VALUES ('{item['first_name']} {item['last_name']}', '{item['user_link']}');"""
                               )


def insert_users():
    '''запись данных о пользователях, общающихся с ботом'''
    with connection.cursor() as cursor:
        cursor.execute(f"""INSERT INTO users (name, age, sex, city)
            VALUES ('Иван Иванов', '30', 'мужчина', 'Москва');"""
                       )


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


# drop_users()
# drop_matched_users()
# drop_favorite_users()
# drop_photos()
# create_table_user()
# create_table_matched_users()
# create_table_favorite_users()
# create_table_photos()
# insert_users()
# show_users()
show_matched_users()
# insert_matched_users()
