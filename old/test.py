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
        self.initial_params = {'sex': self.sex, 'hometown': self.hometown, 'age_from': self.age, 'age_to': self.age, 'has_photo': 1, 'lang': 0}
        self.params = {'access_token': self.token, 'v': self.version}


    def photo_profile(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'user_id': 382668981,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1
        }
        res = requests.get(url, params={**self.params, **params}).json()
        return res



vk = VK('1', 'Москва', 30)
pprint(vk.photo_profile())
