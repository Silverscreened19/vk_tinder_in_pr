import requests
import json
from pprint import pprint
import time

class VK:

    def __init__(self, sex, hometown, age, version='5.131'):
        self.list_id = []
        self.token = 'vk1.a.WizWG1P2L55Y71Pw1_Nyee2FPnT6NW-RAPrXfu_8a9sq3G7n1PUepVbE5fhFCo-qjOgivGE8mwbVL2FOoTIDIyNLGvV2aK069lEdAyQvZ7UYxH-TVyYMSVIiyHBJfwgZynXMR_J27nTLDzeWLncwHH9WQELOz-0gG3_JGy9pEzeaDGAShmkRkj9lWwrZ6tjpn38O7nUvwfai6_aYmp4FzQ'
        # self.user_id = '438084031'
        self.age = age
        self.version = version
        self.sex = sex
        self.hometown = hometown
        self.params = {'access_token': self.token, 'v': self.version}
        self.initial_params = {'sex': self.sex, 'hometown': self.hometown, 'age_from': self.age, 'age_to': self.age, 'has_photo': 1, 'lang': 0}



    def make_list_id(self): # —Д—Г–љ–Ї—Ж–Є—П –њ–Њ–ї—Г—З–µ–љ–Є—П —Б–њ–Є—Б–Ї–∞ –љ—Г–ґ–љ—Л—Е ID –њ–∞—А—В–љ–µ—А–Њ–≤
        list_id = []
        url = 'https://api.vk.com/method/users.search'
        params = {'fields': 'sex, city, birth_year, status', 'count': 30}
        res = requests.get(url, params={**self.params, **params, **self.initial_params}).json()
        time.sleep(3)
        for i in range(len(res['response']['items'])):
            if res['response']['items'][i]['can_access_closed'] == True and 'city' in res['response']['items'][i] and self.hometown in res['response']['items'][i]['city']['title'] and 'status' in res['response']['items'][i]:
                list_id.append(res['response']['items'][i]['id'])
        return list_id

    # def make_list_id(self): # —Д—Г–љ–Ї—Ж–Є—П –њ–Њ–ї—Г—З–µ–љ–Є—П —Б–њ–Є—Б–Ї–∞ –љ—Г–ґ–љ—Л—Е ID –њ–∞—А—В–љ–µ—А–Њ–≤
    #     list_id = []
    #     url = 'https://api.vk.com/method/users.search'
    #     params = {'fields': 'sex, city, birth_year, status', 'count': 30}
    #     res = requests.get(url, params={**self.params, **params}).json()
    #     time.sleep(3)
    #     for i in range(len(res['response']['items'])):
    #         if res['response']['items'][i]['can_access_closed'] == True and 'city' in res['response']['items'][i] and self.hometown in res['response']['items'][i]['city']['title'] and 'status' in res['response']['items'][i]:
    #             list_id.append(res['response']['items'][i]['id'])
    #     return list_id

    def photo_profile(self): # —Д—Г–љ–Ї—Ж–Є—П –њ–Њ–ї—Г—З–µ–љ–Є—П —Б–њ–Є—Б–Ї–∞ —Д–Њ—В–Њ —Б –Љ–∞–Ї—Б–Є–Љ–∞–ї—М–љ—Л–Љ –Ї–Њ–ї–Є—З–µ—Б—В–≤–Њ–Љ –ї–∞–є–Ї–Њ–≤ (–љ–µ –±–Њ–ї–µ–µ 3)
        # with open ('photo_profile.txt', 'w') as f:
            photo_list_2 = []
            set = self.make_list_id()
            for id_ in set:
                # print(id_)
                url = 'https://api.vk.com/method/photos.get'
                params = {
                    'user_id': id_,
                    'album_id': 'profile',
                    'extended': 1,
                    'photo_sizes': 1
                }
                res = requests.get(url, params={**self.params, **params}).json()
                time.sleep(3)
                # pprint(res)
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
                            owner_id = item['owner_id']
                    photo_dict = [likes, url_max]
                    # pprint(photo_dict)
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
                        del(photo_list_all[set])
                        photo_list_2.append(photo_list)
                else:
                    photo_list = photo_list_all
                    photo_list_2.append(photo_list)
            # json.dump(photo_list_2, f, ensure_ascii=False, indent=2)
            return photo_list_2

    def json_info(self):
        count = 0
        pk_list = []
        json_data = {}
        json_data_2 = {}
        json_all_data = []
        set = self.make_list_id()
        set2 = self.photo_profile()
        pk = 1
        for id_ in set:
            url = 'https://api.vk.com/method/users.get'
            params = {'user_id': id_}
            res = requests.get(url, params={**self.params, **params}).json()
            time.sleep(3)
            first_name = res['response'][0]['first_name']
            last_name = res['response'][0]['last_name']
            json_data = {
                'model': 'matched_users',
                'pk': pk,
                'fields':
                {'name': f' {first_name} {last_name}',
                'link': f'https://vk.com/id{id_}',
                'id_user': 1
                }
                        }
            pk_list.append(pk)
            pk +=1
            json_all_data.append(json_data)
        count_2 = len(json_all_data)
        # print(count_2)
        pk_p = 1
        for item in set2:
            for pk in pk_list:
                if count < count_2:
                    json_data_2 = {}
                    if len(item) == 3:
                        json_data_2 ={
                                'model_ph': "photos",
                                'pk_p': pk_p,
                                'fields_ph':{
                                        'photos_link_1': item[0][1],
                                        'photos_link_2': item[1][1],
                                        'photos_link_3': item[2][1],
                                        'id_matched': pk
                                        }
                        }
                        pk_p+=1
                    elif len(item) == 2:
                        json_data_2 = {
                                'model_ph': "photos",
                                'pk_p': pk_p,
                                'fields_ph':{
                                        'photos_link_1': item[0][1],
                                        'photos_link_2': item[1][1],
                                        'id_matched': pk
                                        }
                        }
                        pk_p+=1
                    elif len(item) == 1:
                        json_data_2 = {
                                'model_ph': "photos",
                                'pk_p': pk_p,
                                'fields_ph':{
                                        'photos_link_1': item[0][1],
                                        'id_matched': pk
                                        }
                        }
                        pk_p+=1
                    json_all_data[count].update(json_data_2)
                    count += 1
                # print(count)
        print(pk_list)
        # pprint(json_all_data)

        with open("data.json", "w") as f:
	        json.dump(json_all_data, f, ensure_ascii=False, indent=2)



if __name__ == '__main__':
    vk = VK('1', 'Москва', 30) # –≤–≤–Њ–і–Є–Љ –Є—Б—Е–Њ–і–љ—Л–µ –і–∞–љ–љ—Л–µ –њ–Њ–ї—М–Ј–Њ–≤–∞—В–µ–ї—П
    vk.json_info()

    # with open('user.json', 'w') as f:
    #     user_list = [{
    #        'model': 'users',
    #        'pk': 1,
    #        'fields':
    #        {'name': 'Максим Иванов',
    #        'age': 30,
    #        'sex': 'male',
    #        'city': 'Москва'}
    #     }]
    #     json.dump(user_list, f, ensure_ascii=False, indent=2)

    # pprint(vk.make_list_id())
    # vk.photo_profile()
