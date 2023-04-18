from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from utils import SearchEngine, DataBase, OutputManager, Keyboard

# token to get access
GROUP_TOKEN = ""
USER_TOKEN = ""

# authorization
session = VkApi(token=GROUP_TOKEN)
user_access = VkApi(token=USER_TOKEN)

# get longpoll
longpoll = VkLongPoll(session)
vk = session.get_api()
user_vk = user_access.get_api()

keyboard = VkKeyboard(one_time=True)
Keyboard.set_standard_keyboard(keyboard)

outputManager = OutputManager.OutputManager(session)

age_flag = False
city_flag = False
gender_flag = False
status_flag = False


# check for new messages
def main():
    DataBase.create_database()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            user_id = event.user_id
            user_info = vk.users.get(user_id=user_id, fields="sex, city, bdate")[0]
            print(user_info)

            if event.text == "Поиск":
                outputManager.send_message(user_id, message="Поиск", keyboard=keyboard.get_keyboard())

                age = int(input("Enter the age: "))
                city = int(input("Enter the city: "))
                gender = 2 if input("Enter the gender: ").lower() == "male" else 1
                status = int(input("Enter the status: "))

                matching_users = SearchEngine.search_people(user_vk, user_id, age, gender, city, status)

                for user in matching_users:
                    print(user)
                    DataBase.add_match(user_id, user["id"])
                    for photo in user['top_photos']:
                        print(photo)
                        outputManager.send_message(user_id, message=f"https://vk.com/id{user_id}", attachment=photo)

            elif event.text == "Мои совпадения":
                matches = DataBase.get_matches(user_id)

                if matches:
                    for match in matches:
                        outputManager.send_message(user_id, message="Ваши совпадения:")
                        for user in match:
                            outputManager.send_message(user_id, message=f"{DataBase.get_scope(user, 'user_name')} {DataBase.get_scope(user, 'url')}", keyboard=keyboard.get_keyboard())
                else:
                    outputManager.send_message(user_id, message="У вас нет совпадений", keyboard=keyboard.get_keyboard())

            elif event.text == "Помощь":
                outputManager.send_message(user_id, message="Это чат-бот VK Meet - аналог Tinder. \nНажми 'Поиск' для поиска людей", keyboard=keyboard.get_keyboard())

            else:
                outputManager.send_message(user_id, message="Неизвестная команда", keyboard=keyboard.get_keyboard())


if __name__ == "__main__":
    main()
