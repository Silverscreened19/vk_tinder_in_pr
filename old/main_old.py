import requests
from pprint import pprint
import json


class VK:

    def __init__(self, age, sex, hometown, version='5.131'):
        self.token = access_token
        self.age = age
        self.sex = sex
        self.hometown = hometown
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.initial_params = {
            'sex': self.sex,
            'hometown': self.hometown,
            'age_from': self.age,
            'age_to': self.age,
            'has_photo': 1,
            'lang': 0
            }

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id, 'fields': 'sex, city, bdate'}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def users_search(self):
        with open ('users.txt', 'w') as f:
            id_list = []
            url = 'https://api.vk.com/method/users.search'
            params = {'fields': 'sex, city, birth_year, status', 'count': 30}
            res = requests.get(url, params={**params,**self.params, **self.initial_params}).json()
            for i in range(len(res['response']['items'])):
                if res['response']['items'][i]['can_access_closed'] == True and 'city' in res['response']['items'][i] and self.hometown in res['response']['items'][i]['city']['title'] and 'status' in res['response']['items'][i]:
                    id_list.append(res['response']['items'][i]['id'])
            json.dump(id_list, f, ensure_ascii=False, indent=4)
            return id_list


    def photos_get(self):
        url = 'https://api.vk.com/method/photos.get'
        id_list = self.users_search()
        for owner_id in id_list:
            params = {'owner_id': owner_id, 'extended': '1',
                  'photo_sizes': '1', 'album_id': 'profile'}
            res = requests.get(url, params={**self.params, **params}).json()
            all_pics = res['response']['items']
        return all_pics

if __name__ == '__main__':
    access_token = 'vk1.a.WizWG1P2L55Y71Pw1_Nyee2FPnT6NW-RAPrXfu_8a9sq3G7n1PUepVbE5fhFCo-qjOgivGE8mwbVL2FOoTIDIyNLGvV2aK069lEdAyQvZ7UYxH-TVyYMSVIiyHBJfwgZynXMR_J27nTLDzeWLncwHH9WQELOz-0gG3_JGy9pEzeaDGAShmkRkj9lWwrZ6tjpn38O7nUvwfai6_aYmp4FzQ'
    # user_id = '8079094'
    vk = VK(30, 1, 'Москва')
    with open ('users_photos.txt', 'w') as f:
        info = vk.photos_get()
        json.dump(info, f, ensure_ascii=False, indent=4)

        # for i, item in enumerate(info['response']['items']):
        #     print(i)

        # json.dump(info, f, ensure_ascii=False, indent=4)

    # with open ('users_pics.txt', 'w') as file:
    #     pics_info = vk.photos_get(31425366)
    #     json.dump(pics_info, file, ensure_ascii=False, indent=4)

    # pprint(vk.users_search())
    # pprint(vk.users_info())
