from datetime import datetime
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

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

    empty_scopes = {}

    DataBase.create_database()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            query = event.text.lower()
            print(query)

            user_id = event.user_id
            user_info = vk.users.get(user_id=user_id, fields="sex, city, bdate, relation")[0]
            print(user_info)

            if query == "поиск":

                if not DataBase.user_exists(user_id):
                    DataBase.add_user(user_id, 0, 0, 0, 0)
                    DataBase.add_need(user_id)
                    empty_scopes[user_id] = []

                    try:
                        if len(user_info["bdate"].split(".")) == 3:
                            bdate = user_info["bdate"].split(".")[-1]
                            DataBase.update_user(user_id, "age", datetime.now().year - int(bdate))
                            DataBase.update_need(user_id, "age",
                                                 datetime.now().year - int(bdate))
                        else:
                            raise KeyError

                    except KeyError:
                        empty_scopes[user_id].append("возраст")
                        age_flag = True

                    try:
                        city = user_info["city"]["id"]
                        DataBase.update_user(user_id, "city_id", city)
                        DataBase.update_need(user_id, "city_id", city)
                    except KeyError:
                        empty_scopes[user_id].append("город")
                        city_flag = True

                    try:
                        gender = user_info["sex"]
                        DataBase.update_user(user_id, "gender_id", gender)
                        DataBase.update_need(user_id, "gender_id", 3 - gender)
                    except KeyError:
                        empty_scopes[user_id].append("пол")
                        gender_flag = True

                    try:
                        status = user_info["relation"]
                        DataBase.update_user(user_id, "status_id", status)
                        DataBase.update_need(user_id, "status_id", status)
                    except KeyError:
                        empty_scopes[user_id].append("статус")
                        status_flag = True

                    if status_flag or gender_flag or age_flag or city_flag:
                        outputManager.send_message(user_id, message="Для начала поиска вам необходимо заполнить следующие поля: " + ", ".join(empty_scopes[user_id]), keyboard=Keyboard.fill_in_keyboard(empty_scopes[user_id]))
                    else:
                        outputManager.send_message(user_id, message="Ваш выбранный возраст: " + str(
                        DataBase.get_need(user_id, "age")))

                        outputManager.send_message(user_id, message="Ваш выбранный город: " + user_access.method('database.getCitiesById', values={"city_ids": DataBase.get_need(user_id, "city_id")})[0]['title'])

                        outputManager.send_message(user_id, message="Ваш выбранный пол: " +
                                                                    ("Мужской" if DataBase.get_need(user_id, "gender_id") == 2 else "Женский"))

                        outputManager.send_message(user_id, message="Ваш выбранный статус: " +
                                                                    int_to_status[DataBase.get_need(user_id, "status_id")])

                        outputManager.send_message(user_id, message="Хотите изменить данные?",
                                                   keyboard=Keyboard.change_keyboard())

                elif DataBase.get_need(user_id, "age") == 0 or DataBase.get_need(user_id, "city_id") == 0 or DataBase.get_need(user_id, "gender_id") == 0 or DataBase.get_need(user_id, "status_id") == 0:
                    empty_scopes[user_id] = []
                    if DataBase.get_scope(user_id, "age") == 0:
                        empty_scopes[user_id].append("возраст")
                        age_flag = True
                    if DataBase.get_scope(user_id, "city_id") == 0:
                        empty_scopes[user_id].append("город")
                        city_flag = True
                    if DataBase.get_scope(user_id, "gender_id") == 0:
                        empty_scopes[user_id].append("пол")
                        gender_flag = True
                    if DataBase.get_scope(user_id, "status_id") == 0:
                        empty_scopes[user_id].append("статус")
                        status_flag = True

                    outputManager.send_message(user_id, message="Для начала поиска вам необходимо заполнить следующие поля: " + ", ".join(empty_scopes[user_id]), keyboard=Keyboard.fill_in_keyboard(empty_scopes[user_id]))

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

            elif query == "мои совпадения":
                matches = DataBase.get_seen_matches(user_id)

                if matches:
                    outputManager.send_message(user_id, message="Ваши совпадения:")
                    for match in matches:
                        uid, photo = match
                        outputManager.send_message(user_id, message=f"https://vk.com/id{uid}",
                                                   attachment=photo,
                                                   keyboard=Keyboard.main_keyboard())
                    outputManager.send_message(user_id, message="Это все ваши совпадения")
                else:
                    outputManager.send_message(user_id, message="У вас нет совпадений",
                                               keyboard=Keyboard.main_keyboard())

            elif query == "помощь":
                outputManager.send_message(user_id,
                                           message="Это чат-бот VK Meet - аналог Tinder. \nНажми 'Поиск' для поиска людей",
                                           keyboard=Keyboard.main_keyboard())

            elif query == "да, изменить данные":
                empty_scopes[user_id] = ["возраст", "город", "пол", "статус"]
                outputManager.send_message(user_id, message="Выберите, что хотите изменить",
                                           keyboard=Keyboard.fill_in_keyboard(empty_scopes[user_id]))

            elif query == "нет, начать поиск":

                outputManager.send_message(user_id, message="Поиск начат")

                if not age_flag and not city_flag and not gender_flag and not status_flag:
                    age = DataBase.get_need(user_id, "age")
                    city = DataBase.get_need(user_id, "city_id")
                    gender = DataBase.get_need(user_id, "gender_id")
                    status = DataBase.get_need(user_id, "status_id")

                    out = SearchEngine.search_people(user_vk, user_id, age, gender, city, status)
                    outputManager.send_message(user_id, message=out, keyboard=Keyboard.main_keyboard())

                    if DataBase.matches_exist(user_id):
                        userid, photos = DataBase.get_match(user_id)

                        print(userid, photos)
                        outputManager.send_message(user_id, message=f"https://vk.com/id{userid}", attachment=photos, keyboard=Keyboard.next_keyboard())
                    else:
                        outputManager.send_message(user_id, message="Пока совпадений нет, попробуйте еще раз", keyboard=Keyboard.main_keyboard())

            elif query == "далее":
                if DataBase.matches_exist(user_id):
                    userid, photos = DataBase.get_match(user_id)

                    print(userid, photos)
                    outputManager.send_message(user_id, message=f"https://vk.com/id{userid}", attachment=photos,
                                               keyboard=Keyboard.next_keyboard())
                else:
                    outputManager.send_message(user_id, message="Пока совпадений нет, попробуйте еще раз",
                                               keyboard=Keyboard.main_keyboard())

            elif query == "вернуться в главное меню":
                outputManager.send_message(user_id, message="Главное меню", keyboard=Keyboard.main_keyboard())

            elif query == "указать возраст":
                outputManager.send_message(user_id, message="Введите искомый возраст")
                age_flag = True

            elif age_flag:
                if not event.text.isdigit():
                    outputManager.send_message(user_id, message="Возраст должен быть числом")
                    continue

                DataBase.update_user(user_id, "age", int(event.text))
                DataBase.update_need(user_id, "age", int(event.text))
                age_flag = False
                empty_scopes[user_id].remove("возраст")

                if empty_scopes[user_id]:
                    outputManager.send_message(user_id, message="Также вам необходимо заполнить поля: " + ", ".join(empty_scopes[user_id]), keyboard=Keyboard.fill_in_keyboard(empty_scopes[user_id]))
                else:
                    outputManager.send_message(user_id, message="Вы заполнили все необходимые поля", keyboard=Keyboard.main_keyboard())

            elif query == "указать город":
                outputManager.send_message(user_id, message="Введите ваш город")

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

                DataBase.update_user(user_id, "city_id", response['items'][0]['id'])
                DataBase.update_need(user_id, "city_id", response['items'][0]['id'])
                city_flag = False

                empty_scopes[user_id].remove("город")
                if empty_scopes[user_id]:
                    outputManager.send_message(user_id, message="Также вам необходимо заполнить поля: " + ", ".join(empty_scopes[user_id]), keyboard=Keyboard.fill_in_keyboard(empty_scopes[user_id]))
                else:
                    outputManager.send_message(user_id, message="Вы заполнили все необходимые поля", keyboard=Keyboard.main_keyboard())

            elif query == "указать пол":
                outputManager.send_message(user_id, message="Введите ваш пол", keyboard=Keyboard.gender_keyboard())

            elif gender_flag:
                if event.text == "Мужской":
                    gender_id = 2
                elif event.text == "Женский":
                    gender_id = 1
                else:
                    outputManager.send_message(user_id, message="Неверный пол")
                    continue

                DataBase.update_user(user_id, "gender_id", gender_id)
                DataBase.update_need(user_id, "gender_id", 3 - gender_id)
                gender_flag = False

                empty_scopes[user_id].remove("пол")

                if empty_scopes[user_id]:
                    outputManager.send_message(user_id, message="Также вам необходимо заполнить поля: " + ", ".join(empty_scopes[user_id]), keyboard=Keyboard.fill_in_keyboard(empty_scopes[user_id]))
                else:
                    outputManager.send_message(user_id, message="Вы заполнили все необходимые поля", keyboard=Keyboard.main_keyboard())

            elif query == "указать статус":
                outputManager.send_message(user_id, message="Введите ваш статус", keyboard=Keyboard.status_keyboard())

            elif status_flag:
                DataBase.update_user(user_id, "status_id", status_to_int[event.text])
                DataBase.update_need(user_id, "status_id", status_to_int[event.text])
                status_flag = False

                empty_scopes[user_id].remove("статус")
                if empty_scopes[user_id]:
                    outputManager.send_message(user_id, message="Также вам необходимо заполнить поля: " + ", ".join(empty_scopes[user_id]), keyboard=Keyboard.fill_in_keyboard(empty_scopes[user_id]))
                else:
                    outputManager.send_message(user_id, message="Вы заполнили все необходимые поля", keyboard=Keyboard.main_keyboard())

            elif query == "привет":
                outputManager.send_message(user_id, message="Привет, я бот VK Meet. Чтобы начать поиск, нажми 'Поиск'")

            else:
                outputManager.send_message(user_id, message="Неизвестная команда", keyboard=Keyboard.main_keyboard())


if __name__ == "__main__":
    main()
