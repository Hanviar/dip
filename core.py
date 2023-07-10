from pprint import pprint
from datetime import datetime

import vk_api
from vk_api.exceptions import ApiError

from config import access_token

class VkTools:
  def __init__(self, access_token):
    self.vkapi = vk_api.VkApi(token=access_token)

  def _bdate_toyear(self, bdate):
      user_year = bdate.split('.') 
      now = datetime.now().year
      return now - int(user_year)
    
  def get_profile_info(self, user_id):
      try:
          info, = self.vkapi.method('users.get',
                           {'user_id': user_id,
                           'fields': 'city, sex, bdate'}
                          )
      except ApiError as e:
          info = {}
          print(f'error = {e}')
      
      result = {'name': (info['first_name'] + ' ' + info['last_name']) if 'first_name' in info and 'last_name' in info else none,
                'sex': info.get('sex'),
                'city': info.get('city')['title'] if info.get('city') is not none else none,
                'bdate': self._bdate_toyear(info.get('bdate'))
               }
      
      return result

    def get_city(self, city_name:
        try:
            cities = self.vkapi.method('database.getCities',
                                       {
                                         'q': city_name,
                                         'count': 1
                                       }
                                       )
            if len(cities['items']) > 0:
                return cities['items'][0]
        except ApiError as e:
            print(f'error = {e}')

    def search_worksheet(self, params, offset):
      try:
          users = self.vkapi.method('users.search',
                           {'count': 50,
                            'offset': offset,
                            'hometown': params['city'],
                            'sex': 1 if params['sex'] == 2 else 2,
                            'has_photo': True,
                            'age_from': params['bdate'] - 5,
                            'age_to': params['bdate] + 5
                           }
                          )
      except ApiError as e:
          users = []
          print(f'error = {e}')

      result = [{'name': item['first_name'] + ' ' + item['last_name'],
                'id': item['id']
                } for item in users['items'] if item['is_closed'] is false
               ]
      
      return result

     def get_photos(self, id):
        photos = self.api.method('photos.get',
                                 {'user_id': id,
                                  'album_id': 'profile',
                                  'extended': 1
                                  }
                                 )
        try:
            photos = photos['items']
        except KeyError:
            return []

        res = []

        for photo in photos:
            res.append({'owner_id': photo['owner_id'],
                        'id': photo['id'],
                        'likes': photo['likes']['count'],
                        'comments': photo['comments']['count'],
                        }
                       )

        res.sort(key=lambda x: x['likes'] + x['comments'] * 10, reverse=True)

        return res
       
if __name__ = '__main__':
  user_id =
  tools = VkTools(access_token)
  params = tools.get_profile_info(user_id)
  worksheets = tools.search_worksheet(params, 5)
  worksheet = worksheets.pop()
  photos = tools.get_photos(worksheet['id'])
  pprint(worksheet)
