from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = 'vk1.a.H1O2MeQhqORWS_wXxjnarAEJEnwbbte2M6-dD9up-0tjdAKzGgnESWbgUb-OXm-SufX2uMlqhY9yjG7iIRtIi_J1sA_xJY0dpfMmIKvo3BF2hyg2eKCfDuoA4k5QvFhFtQDXCv5XKustiWYWpKzeFK00fIKJYGWlBRuXQPPe938V3ZVgLodatSCWnJPORofvo3OYGDxKEOcy6kwa7lKohQ'

# token = 'vk1.a.WizWG1P2L55Y71Pw1_Nyee2FPnT6NW-RAPrXfu_8a9sq3G7n1PUepVbE5fhFCo-qjOgivGE8mwbVL2FOoTIDIyNLGvV2aK069lEdAyQvZ7UYxH-TVyYMSVIiyHBJfwgZynXMR_J27nTLDzeWLncwHH9WQELOz-0gG3_JGy9pEzeaDGAShmkRkj9lWwrZ6tjpn38O7nUvwfai6_aYmp4FzQ'

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {
              'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7), })


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")

            elif request == "Как дела?":
                write_msg(event.user_id, f"Отлично{event.user_id}")

            elif request == "Хочу познакомиться":
                write_msg(event.user_id,
                          "Введите ваш пол, возраст и город проживания")
# когда пользователь вводит данные (пол, возраст, город), должна отработать функция vk.json_info() и 

            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
