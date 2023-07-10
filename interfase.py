import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import comunity_token, access_token
from core import VkTools
from datastore import add_user, check_user, engine

class CupidBot():
    def __init__(self, comunity_token, access_token)
        self.vk = vk_api.Vk.Api(token=comunity_token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk_tools = VkTools(access_token)
        self.params = none
        self.worksheets = []
        self.offset = 0
        self.engine = engine
  
    def message_send(self, user_id, message, attachment=none):
        self.vk.meethod('messages.send',
             {'user_id': user_id,
              'message': message,
              'attachment': attachment,
              'random_id': get_random_id()})

    def event_handler(self):
        for event in self.longpoll.listen():
          if event.type == VkEventType.MESSAGE_NEW and event.to_me:
              if not self.params:
                  '''логика получения необходиых данных'''
                  self.params = self.vk_tools.get_profile_info(event.user_id)
                  
              if event.text.lower() == 'привет':
                self.message_send(event.user_id, f'Ну здравствуй-здравствуй, {self.params["name"]}')
                  
              elif event.text.lower() == 'поиск':
                  '''проверка наличия города'''
                  if self.params.get("city") is none:
                         self.message_send(
                             event.user_id,
                             'укажите город, в котором вы проживаете с помощью команды "название города",'
                             'например "Санкт-Петербург"') 
                         continue
              
                if self.params.get("year") is none:
                        self.message_send(
                            event.user_id,
                            'укажите возраст, с помощью команды "возраст",'
                             'например "возраст 30"')
                         continue
                '''логика поиска анкет'''
                self.message_send(event.user_id, 'ну давай посмотрим, ето у нас есть')
                if not self.worksheets: 
                    self.worksheets = self.vk_tools.search_worksheet(
                            self.params, self.offset)
                'проверка анкеты в бд в соотвествие с event.user_id'

                    worksheet = None
                    new_worksheets = []
                    for worksheet in self.worksheets:
                        if not check_user(self.engine, event.user_id, worksheet['id']):
                            new_worksheets.append(worksheet)
                    self.worksheets = new_worksheets.copy()
                    worksheet = self.worksheets.pop(0)

                    photos = self.vk_tools.get_photos(worksheet['id'])
                    photo_string = ''
                    for photo in photos:
                        photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
                    self.offset += 50

                    self.message_send(
                        event.user_id,
                        f'имя: {worksheet["name"]} ссылка: vk.com/id{worksheet["id"]}',
                        attachment=photo_string
                    )

                    'добавить анкету в бд в соотвествие с event.user_id'
                    add_user(self.engine, event.user_id, worksheet['id'])
                elif event.text.lower().startswith("город"):
                    city_name = ' '.join(event.text.lower().split()[1:])
                    city = self.vk_tools.get_city(city_name)
                    if city is None:
                        self.message_send(
                            event.user_id, 'Такого города нет')
                    else:
                        self.params['city'] = city['title']
                        self.message_send(
                            event.user_id, f'Город указан {city["title"]}')
                elif event.text.lower().startswith("возраст "):
                    age = event.text.lower().split()[1]
                    try:
                        age = int(age)
                    except ValueError:
                        self.message_send(
                            event.user_id, 'А ты совешеннолетнего возраста достиг?')
                        continue
                    if not 18 <= age <= 69:
                        self.message_send(
                            event.user_id, 'Ваш возраст должен быть от 18 до 69 лет')
                        continue
                    self.params['year'] = age
                    self.message_send(
                        event.user_id, 'Возраст учтен')
                elif event.text.lower() == 'пока':
                    self.message_send(
                        event.user_id, 'Ну возвращайся, если не повезет')
                else:
                    self.message_send(
                        event.user_id, 'Простите, что?')

if __name__ == '__main__':
  cupid_bot = CupidBot(comunity_token, access_token)
  cupid_bot.event_handler()
