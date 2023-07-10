import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import comunity_token


class CupidBot():
    def __init__(self, comunity_token)
        self.vk = vk_api.Vk.Api(token=comunity_token)
        self.longpoll = VkLongPoll(self.vk)
  
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
                self.message_send(event.user_id, 'здравствуй, партнёр')
              elif event.text.lower() == 'поиск':
                self.message_send(event.user_id, 'ооо, ты ищешь компанию... дай-ка подумать, может есть кто на примете')
              elif event.text.lower() == 'пока':
                self.message_send(event.user_id, 'мы еще встретимся, партнёр')

              else:
                self.message_send(event.user_id, 'я тебя не понял, партнёр... ну-ка повтори')


if __name__ == '__main__':
  cupid_bot = CupidBot(comunity_token)
  cupid_bot.event_handler()
