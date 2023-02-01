import requests
import json
from pprint import pprint
import time


class VK:

    def __init__(self, sex, hometown, age, version='5.131'):
        self.depth = 0
        self.list_id = []
        self.token = 'vk1.a.WizWG1P2L55Y71Pw1_Nyee2FPnT6NW-RAPrXfu_8a9sq3G7n1PUepVbE5fhFCo-qjOgivGE8mwbVL2FOoTIDIyNLGvV2aK069lEdAyQvZ7UYxH-TVyYMSVIiyHBJfwgZynXMR_J27nTLDzeWLncwHH9WQELOz-0gG3_JGy9pEzeaDGAShmkRkj9lWwrZ6tjpn38O7nUvwfai6_aYmp4FzQ'
        # self.user_id = '438084031'
        self.age = age
        self.version = version
        self.sex = sex
        self.hometown = hometown
        self.params = {'access_token': self.token, 'v': self.version, 'sex': self.sex,
                       'hometown': self.hometown, 'age_from': self.age, 'age_to': self.age, 'has_photo': 1, 'lang': 0}
        self.params_2 = {'access_token': self.token, 'v': self.version}

    def make_list_id(self):  # функция получения списка нужных ID партнеров
        list_id = []
        url = 'https://api.vk.com/method/users.search'
        params = {'fields': 'sex, city, birth_year, status', 'count': 15}
        res = requests.get(url, params={**self.params, **params}).json()
        time.sleep(2)
        for i in range(len(res['response']['items'])):
            if res['response']['items'][i]['can_access_closed'] == True and 'city' in res['response']['items'][i] and self.hometown in res['response']['items'][i]['city']['title'] and 'status' in res['response']['items'][i]:
                list_id.append(res['response']['items'][i]['id'])
        return list_id

    # функция получения списка фото с максимальным количеством лайков (не более 3)
    def photo_profile(self):
        name_list = []
        photo_list_2 = []
        photo_list_3 = []
        photo_list_all = []
        photo_list = []
        set = self.make_list_id()
        for id_ in set:
            url = 'https://api.vk.com/method/photos.get'
            params = {
                'owner_id': id_,
                'album_id': 'profile',
                'extended': '1',
                'photo_sizes': '1'
            }
            res = requests.get(url, params={**self.params_2, **params}).json()
            time.sleep(2)
            all_photo = res['response']['items']
            height = 0
            width = 0
            photo_list_all = []
            for item in all_photo:
                for size in item['sizes']:
                    if height < size['height'] and width < size['width']:
                        height = size['height']
                        width = size['width']
                        url_max = size['url']
                        likes = item['likes']['count']
                photo_dict = [likes, url_max, id_]
                photo_list_all.append(photo_dict)
                height = 0
                width = 0
                url_max = ''
            photo_list.append(photo_list_all)

        for item2 in photo_list:
            name_list = []
            if len(item2) > 3:
                for i in range(3):
                    max_number = max(item2)
                    name_list.append(max_number)
                    set = item2.index(max_number)
                    del (item2[set])
                photo_list_2.append(name_list)
            elif len(item2) <= 3:
                photo_list_3.append(item2)
        photo_list_3.extend(photo_list_2)
        return photo_list_3

    def json_info(self):
        json_data = {}
        json_data_2 = {}
        json_all_data = []
        json_all_data2 = []
        set = self.make_list_id()
        set2 = self.photo_profile()
        for id_ in set:
            url = 'https://api.vk.com/method/users.get'
            params = {'user_id': id_}
            res = requests.get(url, params={**self.params, **params}).json()
            time.sleep(2)
            first_name = res['response'][0]['first_name']
            last_name = res['response'][0]['last_name']
            json_data = {'first_name': first_name,
                         'last_name': last_name,
                         'user_link': f'https://vk.com/id{id_}'
                         }
            json_all_data.append(json_data)

        for id_ in set:
            # print(id_)
            for item in set2:
                if id_ == item[0][2]:
                    json_data_2 = {}
                    if len(item) == 3:
                        json_data_2 = {
                            'user_link': f'https://vk.com/id{id_}',
                            'photos_link_1': item[0][1],
                            'photos_link_2': item[1][1],
                            'photos_link_3': item[2][1]
                        }
                    elif len(item) == 2:
                        json_data_2 = {
                            'user_link': f'https://vk.com/id{id_}',
                            'photos_link_1': item[0][1],
                            'photos_link_2': item[1][1]
                        }
                    elif len(item) == 1:
                        json_data_2 = {
                            'user_link': f'https://vk.com/id{id_}',
                            'photos_link_1': item[0][1]
                        }
                    json_all_data2.append(json_data_2)

        with open("data_user.json", "w") as f:
            json.dump(json_all_data, f, ensure_ascii=False, indent=2)

        with open("data_photo.json", "w") as f:
            json.dump(json_all_data2, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':

    vk = VK('1', 'Москва', 25)  # вводим исходные данные пользователя
    vk.json_info()
