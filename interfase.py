import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import comunity_token, access_token
from core import vktools

class CupidBot():
    def __init__(self, comunity_token, access_token)
        self.vk = vk_api.Vk.Api(token=comunity_token)
        self.longpoll = VkLongPoll(self.vk)
        self.vktools = VkTools(access_token)
        self.params = none
        self.worksheets = []
        self.offset = 0
  
    def message_send(self, user_id, message, attachment=none):
        self.vk.meethod('messages.send',
             {'user_id': user_id,
              'message': message,
              'attachment': attachment,
              'random_id': get_random_id()})

    def event_handler(self):
        for event in self.longpoll.listen():
          if event.type == VkEventType.MESSAGE_NEW and event.to_me:
              if event.text.lower() == 'привет':
                self.params = self.vktools.get_profile_info(event.user_id)
                self.message_send(event.user_id, f'Howdy, {self.params["name"]}')
              elif event.text.lower() == 'поиск':
                self.message_send(event.user_id, 'ооо, ты ищешь компанию... дай-ка подумать, может есть кто на примете')
                if self.worksheets:
                    worksheet = self.worksheets.pop()
                    photos = self.vktools.get_photos(worksheet['id'])
                    photo_string = ''
                    for photo in photos:
                        photo_string += f'photo{photo["owner_id"]}_photo["id"],'
                else:
                    self.message_send(event.user_id, f'имя: {worksheet["name"]} ссылка: vk.com/{worksheet["id"]}'),
                        self.worksheets = self.vktools.search_worksheet(self.params, self.offset)
                        worksheet = self.worksheets.pop()
                        photos = self.vktools.get_photos(worksheet['id'])
                        photo_string = ''
                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_photo["id"],'
                        self.offset += 50
                    self.message_send(event.user_id, f'имя: {worksheet["name"]} ссылка: vk.com/{worksheet["id"]}'),
                    attachment = photo_string
              elif event.text.lower() == 'пока':
                self.message_send(event.user_id, 'мы еще встретимся, партнёр')

              else:
                self.message_send(event.user_id, 'я тебя не понял, партнёр... ну-ка повтори')


if __name__ == '__main__':
  cupid_bot = CupidBot(comunity_token, access_token)
  cupid_bot.event_handler()
