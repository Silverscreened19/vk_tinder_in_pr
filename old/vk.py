import requests
from pprint import pprint


class VK:

    def __init__(self, sex, hometown, age, version='5.131'):
        self.list_id = []
        self.token = 'vk1.a.WizWG1P2L55Y71Pw1_Nyee2FPnT6NW-RAPrXfu_8a9sq3G7n1PUepVbE5fhFCo-qjOgivGE8mwbVL2FOoTIDIyNLGvV2aK069lEdAyQvZ7UYxH-TVyYMSVIiyHBJfwgZynXMR_J27nTLDzeWLncwHH9WQELOz-0gG3_JGy9pEzeaDGAShmkRkj9lWwrZ6tjpn38O7nUvwfai6_aYmp4FzQ'
        # self.user_id = '438084031'
        self.age = age
        self.version = version
        self.sex = sex
        self.hometown = hometown
        self.params = {'access_token': self.token, 'v': self.version, 'sex': self.sex,
                       'hometown': self.hometown, 'age_from': self.age, 'age_to': self.age, 'has_photo': 1, 'lang': 0}

    def make_list_id(self):  # функция получения списка нужных ID партнеров
        url = 'https://api.vk.com/method/users.search'
        params = {'fields': 'sex, city, birth_year, status', 'count': 10}
        res = requests.get(url, params={**self.params, **params}).json()
        for i in range(len(res['response']['items'])):
            if res['response']['items'][i]['can_access_closed'] == True and 'city' in res['response']['items'][i] and self.hometown in res['response']['items'][i]['city']['title'] and 'status' in res['response']['items'][i]:
                self.list_id.append(res['response']['items'][i]['id'])
        return self.list_id

    # функция получения списка фото с максимальным количеством лайков (не более 3)
    def photo_profile(self, id_):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'user_id': id_,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1'
        }
        res = requests.get(url, params={**self.params, **params}).json()

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
            photo_dict = [likes, url_max]
            photo_list_all.append(photo_dict)
            height = 0
            width = 0
            url_max = ''

        if len(photo_list_all) > 3:
            photo_list = []
            for i in range(3):
                max_number = max(photo_list_all)
                photo_list.append(max_number)
                set = photo_list_all.index(max_number)
                del (photo_list_all[set])
        else:
            photo_list = photo_list_all
        return photo_list


if __name__ == '__vk__':

    vk = VK('1', 'Москва', 25)  # вводим исходные данные пользователя
    # pprint(vk.make_list_id())
    set = vk.make_list_id()
    for item in set:
        pprint(vk.photo_profile(item))
        print()

# таблица с данными исходного пользователя(пол, город, возраст, юзер_айди_исх),
# таблица со всеми кто совпал(юзер_айди_исх, фио, ссылка),
# таблица с фотками(юзер_айди, 3 столбца с фотами(2 из них нулл)),
# таблица с избранными (юзер_айди_мэтчд)
