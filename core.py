from pprint import pprint
from datetime import datetime

import vk_api
from vk_api.exceptions import ApiError

from config import access_token

class VkTools:
  def __init__(self, access_token):
    self.vkapi = vk_api.VkApi(token=access_token)

  def _bdate_toyear(self, bdate):
      user_year = bdate.split('.')[2] if 'bdate' else none 
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

    def search_worksheet(self, params):
      try:
          users = self.vkapi.method('users.search',
                           {'count': 50,
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

      return users
      

if __name__ = '__main__':
  user_id =
  tools = VkTools(access_token)
  params = tools.get_profile_info(user_id)
  worksheets = tools.search_worksheet(params)
  pprint(worksheets)
