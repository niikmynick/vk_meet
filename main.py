from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard
from utils import SearchEngine, DataBase, OutputManager, Keyboard

# token to get access
GROUP_TOKEN = "vk1.a._AI8Wb2pyxEY6owpf7BU8AJh9yaRN6MtxuPzIROVcNBZRKqamivKTAOq-vvTv8X864ewFOfGYBriqct5X5d9IA40YyNR8uwktUHHL-FFMSC2zducVFnWDiuyWOC7jAo4snVrKu0xmJezRtCpE2D-OHKcZBA5IozQN4OylSfFA92RoQJj7Fbwm2BUEVjKyutqgmEJQuEuqoAHDSc9ZHQ6Gg"
USER_TOKEN = "vk1.a.jU2ekF7o8dM4632o28Wt5x5sysDmxtsRJGAr67T0gSiLX2mbRv-FNegiq49jdvjJv8z-P3c2GKi3PsXF6s2cn5H4ITtf-tt47nsa04YVKtmHVbXrwvNZTmVufJzx6eNupE6fy9vTnWe58V0yAnhXA8m_2S6YHlaJ2O5nEG0eAGBCe4IZsSE41ZkKpAw7lkpI_VmNzmhmrtzULUua4IYe2A"

# authorization
session = VkApi(token=GROUP_TOKEN)
user_access = VkApi(token=USER_TOKEN)

# get longpoll
longpoll = VkLongPoll(session)
vk = session.get_api()
user_vk = user_access.get_api()

keyboard = VkKeyboard(one_time=True)
Keyboard.set_main_keyboard(keyboard)

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

            user_id = event.user_id
            user_info = vk.users.get(user_id=user_id, fields="sex, city, bdate")[0]

            query = event.text.lower()
            print(user_info)

            if query == "поиск":
                if not DataBase.user_exists(user_id):
                    outputManager.send_message(user_id, message="Вы не зарегистрированы")
                    outputManager.send_message(user_id, message="Введите ваш возраст")
                    age_flag = True
                    continue
                else:
                    outputManager.send_message(user_id, message="Вы уже зарегистрированы")

                    outputManager.send_message(user_id, message="Ваш выбранный возраст: " + str(
                        DataBase.get_scope(user_id, "age")))

                    outputManager.send_message(user_id, message="Ваш выбранный город: " + str(
                        DataBase.get_scope(user_id, "city")))

                    outputManager.send_message(user_id, message="Ваш выбранный пол: " + str(
                        DataBase.get_scope(user_id, "gender")))

                    outputManager.send_message(user_id, message="Ваш выбранный статус: " + str(
                        DataBase.get_scope(user_id, "status")))

                    Keyboard.set_change_keyboard(keyboard)
                    outputManager.send_message(user_id, message="Хотите изменить данные?",
                                               keyboard=keyboard.get_keyboard())
                    continue

            elif query == "мои совпадения":
                matches = DataBase.get_matches(user_id)
                Keyboard.set_main_keyboard(keyboard)

                if matches:
                    for match in matches:
                        outputManager.send_message(user_id, message="Ваши совпадения:")
                        for user in match:
                            outputManager.send_message(user_id, message=f"https://vk.com/id{user}",
                                                       keyboard=keyboard.get_keyboard())
                else:
                    outputManager.send_message(user_id, message="У вас нет совпадений",
                                               keyboard=keyboard.get_keyboard())

            elif query == "помощь":
                Keyboard.set_main_keyboard(keyboard)
                outputManager.send_message(user_id,
                                           message="Это чат-бот VK Meet - аналог Tinder. \nНажми 'Поиск' для поиска людей",
                                           keyboard=keyboard.get_keyboard())

            elif query == "да, изменить данные":
                age_flag = True
                outputManager.send_message(user_id, message="Укажи возраст")

            elif query == "нет, начать поиск":

                if not age_flag and not city_flag and not gender_flag and not status_flag:
                    age = DataBase.get_scope(user_id, "age")
                    city = DataBase.get_scope(user_id, "city")
                    gender = DataBase.get_scope(user_id, "gender")
                    status = DataBase.get_scope(user_id, "status")

                    matching_users = SearchEngine.search_people(user_vk, user_id, age, gender, city, status)

                    for user in matching_users:
                        print(user)
                        DataBase.add_match(user_id, user["id"])
                        for photo in user['top_photos']:
                            print(photo)
                            outputManager.send_message(user_id, message=f"https://vk.com/id{user['id']}",
                                                       attachment=photo)

            elif query == "вернуться в главное меню":
                Keyboard.set_main_keyboard(keyboard)
                outputManager.send_message(user_id, message="Главное меню", keyboard=keyboard.get_keyboard())

            elif age_flag:
                if not event.text.isdigit():
                    outputManager.send_message(user_id, message="Возраст должен быть числом")
                    continue
                DataBase.update_need(user_id, "age", int(event.text))
                age_flag = False
                outputManager.send_message(user_id, message="Укажи город")
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

                DataBase.update_need(user_id, "city", response['items'][0]['id'])
                city_flag = False
                Keyboard.set_gender_keyboard(keyboard)
                outputManager.send_message(user_id, message="Укажи пол", keyboard=keyboard.get_keyboard())
                gender_flag = True

            elif gender_flag:
                if event.text == "Мужской":
                    gender_id = 2
                elif event.text == "Женский":
                    gender_id = 1
                else:
                    outputManager.send_message(user_id, message="Неверный пол")
                    continue

                DataBase.update_need(user_id, "gender", gender_id)
                gender_flag = False
                Keyboard.set_status_keyboard(keyboard)
                outputManager.send_message(user_id, message="Укажи статус", keyboard=keyboard.get_keyboard())
                status_flag = True

            elif status_flag:
                status = {
                    "Не женат / не замужем": 1,
                    "Встречается": 2,
                    "Помолвлен": 3,
                    "Женат / замужем": 4,
                    "Всё сложно": 5,
                    "В активном поиске": 6,
                    "Влюблён(-ф)": 7,
                    "В гражданском браке": 8
                }
                DataBase.update_need(user_id, "status", status[event.text])
                status_flag = False

                Keyboard.set_main_keyboard(keyboard)
                outputManager.send_message(user_id, message="Вы успешно зарегистрированы",
                                           keyboard=keyboard.get_keyboard())

            else:
                Keyboard.set_main_keyboard(keyboard)
                outputManager.send_message(user_id, message="Неизвестная команда", keyboard=keyboard.get_keyboard())


if __name__ == "__main__":
    main()
