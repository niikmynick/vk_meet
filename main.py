from datetime import datetime

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

import properties
from utils import SearchEngine, DataBase, OutputManager, Keyboard
from properties import status_to_int, int_to_status, GROUP_TOKEN, USER_TOKEN

# authorization
session = VkApi(token=GROUP_TOKEN)
user_access = VkApi(token=USER_TOKEN)

# get longpoll
longpoll = VkLongPoll(session)
vk = session.get_api()
user_vk = user_access.get_api()

outputManager = OutputManager.OutputManager(session)

age_flag = False
city_flag = False
gender_flag = False
status_flag = False


# check for new messages
def main():
    global age_flag, gender_flag, status_flag
    global city_flag

    DataBase.create_database()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            print(event.text)
            user_id = event.user_id
            user_info = vk.users.get(user_id=user_id, fields="sex, city, bdate, relation")[0]
            query = event.text.lower()
            print(user_info)
            if query == "поиск":
                if not DataBase.user_exists(user_id):
                    outputManager.send_message(user_id, message="Вы не уточнили параметры поиска")
                    DataBase.add_user(
                        user_id,
                        datetime.now().year - int(user_info["bdate"][-4:]) if user_info["bdate"].split(".") == 3 else 0,
                        user_info["city"]["id"] if "city" in user_info else 0,
                        user_info["sex"],
                        user_info["relation"] if "relation" in user_info and user_info["relation"] != "" else 0
                    )
                    DataBase.add_need(user_id)
                    outputManager.send_message(user_id, message="Введите искомый возраст")
                    age_flag = True
                    continue
                else:
                    outputManager.send_message(user_id, message="Вы уже вводили параметры поиска")

                    outputManager.send_message(user_id, message="Ваш выбранный возраст: " + str(
                        DataBase.get_need(user_id, "age")))

                    outputManager.send_message(user_id, message="Ваш выбранный город: " + user_access.method('database.getCitiesById', values={"city_ids": DataBase.get_need(user_id, "city_id")})[0]['title'])

                    outputManager.send_message(user_id, message="Ваш выбранный пол: " +
                                                                ("Мужской" if DataBase.get_need(user_id, "gender_id") == 2 else "Женский"))

                    outputManager.send_message(user_id, message="Ваш выбранный статус: " +
                                                                int_to_status[DataBase.get_need(user_id, "status_id")])

                    outputManager.send_message(user_id, message="Хотите изменить данные?",
                                               keyboard=Keyboard.change_keyboard())
                    continue

            elif query == "мои совпадения":
                matches = DataBase.get_matches(user_id)

                if matches:
                    for match in matches:
                        outputManager.send_message(user_id, message="Ваши совпадения:")
                        for user in match:
                            outputManager.send_message(user_id, message=f"https://vk.com/id{user}",
                                                       keyboard=Keyboard.main_keyboard())
                else:
                    outputManager.send_message(user_id, message="У вас нет совпадений",
                                               keyboard=Keyboard.main_keyboard())

            elif query == "помощь":
                outputManager.send_message(user_id,
                                           message="Это чат-бот VK Meet - аналог Tinder. \nНажми 'Поиск' для поиска людей",
                                           keyboard=Keyboard.main_keyboard())

            elif query == "да, изменить данные":
                age_flag = True
                outputManager.send_message(user_id, message="Введите искомый возраст")

            elif query == "нет, начать поиск":

                outputManager.send_message(user_id, message="Поиск начат")

                if not age_flag and not city_flag and not gender_flag and not status_flag:
                    age = DataBase.get_need(user_id, "age")
                    city = DataBase.get_need(user_id, "city_id")
                    gender = DataBase.get_need(user_id, "gender_id")
                    status = DataBase.get_need(user_id, "status_id")

                    matching_users = SearchEngine.search_people(user_vk, user_id, age, gender, city, status)

                    for user in matching_users:
                        print(user)
                        outputManager.send_message(user_id, message=f"https://vk.com/id{user['id']}", attachment=",".join(user['top_photos']))

            elif query == "вернуться в главное меню":
                outputManager.send_message(user_id, message="Главное меню", keyboard=Keyboard.main_keyboard())

            elif age_flag:
                if not event.text.isdigit():
                    outputManager.send_message(user_id, message="Возраст должен быть числом")
                    continue
                DataBase.update_need(user_id, "age", int(event.text))
                age_flag = False
                outputManager.send_message(user_id, message="Введите искомый город")
                city_flag = True

            elif city_flag:
                values = {
                    'country_id': 1,
                    'q': event.text[:15],
                    'count': 1
                }
                response = user_access.method('database.getCities', values=values)

                if not response['items']:
                    outputManager.send_message(user_id, message="Город не найден")
                    continue

                DataBase.update_need(user_id, "city_id", response['items'][0]['id'])
                city_flag = False
                outputManager.send_message(user_id, message="Укажите искомый пол", keyboard=Keyboard.gender_keyboard())
                gender_flag = True

            elif gender_flag:
                if event.text == "Мужской":
                    gender_id = 2
                elif event.text == "Женский":
                    gender_id = 1
                else:
                    outputManager.send_message(user_id, message="Неверный пол")
                    continue

                DataBase.update_need(user_id, "gender_id", gender_id)
                gender_flag = False
                outputManager.send_message(user_id, message="Укажите искомый статус", keyboard=Keyboard.status_keyboard())
                status_flag = True

            elif status_flag:

                DataBase.update_need(user_id, "status_id", status_to_int[event.text])
                status_flag = False

                outputManager.send_message(user_id, message="Вы успешно зарегистрированы",
                                           keyboard=Keyboard.main_keyboard())

            elif query == "привет":
                outputManager.send_message(user_id, message="Привет, я бот VK Meet. Чтобы начать поиск, нажми 'Поиск'")

            else:
                outputManager.send_message(user_id, message="Неизвестная команда", keyboard=Keyboard.main_keyboard())


if __name__ == "__main__":
    main()
