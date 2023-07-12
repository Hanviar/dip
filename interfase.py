import vk_api
from sqlalchemy import create_engine
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id

from config import acces_token, comunity_token, db_url_object
from core import VkTools
from data_store import Base, add_user, check_user

class CupidBot():
    def __init__(self, comunity_token, acces_token, engine):
        self.vk = vk_api.VkApi(token=comunity_token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk_tools = VkTools(acces_token)
        self.engine = engine
        self.params = {}
        self.worksheets = []
        self.offset = 0

    def message_send(self, user_id, message, attachment=None):
        self.vk.method('messages.send',
                       {'user_id': user_id,
                        'message': message,
                        'attachment': attachment,
                        'random_id': get_random_id()}
                       )

    def event_handler(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if not self.params:
                    '''логика получения необходиых данных'''
                    self.params = self.vk_tools.get_profile_info(event.user_id)

                if event.text.lower() == 'привет':
                    self.message_send(
                        event.user_id, f'Ну здравствуй-здравствуй, {self.params["name"]}')
                elif event.text.lower() == 'поиск':
                     # проверка наличия города
                    if self.params.get("city") is None:
                        self.message_send(
                            event.user_id,
                            'Пожалуйста укажите город, используя команду "город <название>",'
                             ' например "город Санкт-Петербург"')
                        continue
                    elif self.params.get("year") is None:
                        self.message_send(
                            event.user_id,
                            'Пожалуйста укажите свой возраст используя команду "возраст <число>",'
                            ' например "возраст 30"')
                        continue

                    '''логика поиска анкет'''
                    self.message_send(
                        event.user_id, 'ну давай посмотрим, ето у нас есть')
                    if not self.worksheets:
                        self.worksheets = self.vk_tools.search_worksheet(
                            self.params, self.offset), self.offset += 50
                    
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

                    # добавить анкету в бд в соотвествие с event.user_id
                    add_user(self.engine, event.user_id, worksheet['id'])
                elif event.text.lower().startswith("город "):
                    city_name = ' '.join(event.text.lower().split()[1:])
                    city = self.vk_tools.get_city(city_name)
                    if city is None:
                        self.message_send(
                            event.user_id, 'такого города нет')
                    else:
                        self.params['city'] = city['title']
                        self.message_send(
                            event.user_id, f'город указан {city["title"]}')
                elif event.text.lower().startswith("возраст "):
                    age = event.text.lower().split()[1]
                    try:
                        age = int(age)
                    except ValueError:
                        self.message_send(
                            event.user_id, 'а ты совешеннолетнего возраста достиг?')
                        continue
                    if not 18 <= age <= 69:
                        self.message_send(
                            event.user_id, 'Ваш возраст должен быть от 18 до 69 лет')
                        continue
                    self.params['year'] = age
                    self.message_send(
                        event.user_id, 'возраст учтён')
                elif event.text.lower() == 'пока':
                    self.message_send(
                        event.user_id, 'ну возвращайся, если не повезет')
                else:
                    self.message_send(
                        event.user_id, 'простите, что?')


if __name__ == '__main__':
    engine = create_engine(db_url_object)
    Base.metadata.create_all(engine)

    cupid_bot = CupidBot(comunity_token, acces_token, engine)
    cupid_bot.event_handler()
