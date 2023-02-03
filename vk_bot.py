from main import *
from db import *
from pprint import pprint

token = 'vk1.a.H1O2MeQhqORWS_wXxjnarAEJEnwbbte2M6-dD9up-0tjdAKzGgnESWbgUb-OXm-SufX2uMlqhY9yjG7iIRtIi_J1sA_xJY0dpfMmIKvo3BF2hyg2eKCfDuoA4k5QvFhFtQDXCv5XKustiWYWpKzeFK00fIKJYGWlBRuXQPPe938V3ZVgLodatSCWnJPORofvo3OYGDxKEOcy6kwa7lKohQ'
# token = 'vk1.a.WizWG1P2L55Y71Pw1_Nyee2FPnT6NW-RAPrXfu_8a9sq3G7n1PUepVbE5fhFCo-qjOgivGE8mwbVL2FOoTIDIyNLGvV2aK069lEdAyQvZ7UYxH-TVyYMSVIiyHBJfwgZynXMR_J27nTLDzeWLncwHH9WQELOz-0gG3_JGy9pEzeaDGAShmkRkj9lWwrZ6tjpn38O7nUvwfai6_aYmp4FzQ'


vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)



def write_msg(user_id, message):
    vk.method('messages.send', {
              'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text
            user_id = str(event.user_id)
            user = User()
            name_user = user.user_name(user_id)
            if request == "привет":
                write_msg(event.user_id, f"Хай, {name_user}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")

            elif request == "Как дела?":
                write_msg(event.user_id, f"Отлично, {name_user}")

            elif request == "Хочу познакомиться":
                drop_users()
                drop_matched_users()
                drop_favorite_users()
                drop_photos()
                create_table_user()
                create_table_matched_users()
                create_table_favorite_users()
                create_table_photos()
                insert_users(user_id)
                insert_matched_users(user_id)
                insert_photos(user_id)
                show_users()
                show_matched_users()
                show_photos()
                # write_msg(event.user_id,
                #           "подобрали пользователей")
                # for event in longpoll.listen():

                # write_msg(event.user_id,
                #           "Введите ваш пол, возраст и город проживания")
                # for event in longpoll.listen():
                #     if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                #         age = event.text
                # vk_b = VK_b(user.user_sex(), user.user_city(user_id), user.user_age(user_id))
                # pprint(vk_b.make_list_id_2(user_id))
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")


# создать функции получения имени, пола, возраста, города пользователя, который пишет в чат
# создаем бд с помощью функций create_table_user(), create_table_matched_users(),
# create_table_favorite_users(), create_table_photos()
# информация о пользователе, общающемся с ботом, записывается в бд функцией insert_users()
# когда пользователь вводит данные (пол, возраст, город), должна отработать функция vk.json_info() и
# информация должна выводиться в бот из базы данных
# с помощью команды из бота необходимо добавлять в бд инфу об избранных пользователях и выводить их
# в чат с помощью команды
# Должна быть возможность перейти к следующему человеку с помощью команды или кнопки
