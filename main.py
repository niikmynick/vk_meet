from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from utils import SearchEngine, DataBase

# token to get access
GROUP_TOKEN = "vk1.a._AI8Wb2pyxEY6owpf7BU8AJh9yaRN6MtxuPzIROVcNBZRKqamivKTAOq-vvTv8X864ewFOfGYBriqct5X5d9IA40YyNR8uwktUHHL-FFMSC2zducVFnWDiuyWOC7jAo4snVrKu0xmJezRtCpE2D-OHKcZBA5IozQN4OylSfFA92RoQJj7Fbwm2BUEVjKyutqgmEJQuEuqoAHDSc9ZHQ6Gg"
USER_TOKEN = "vk1.a.HZbC8zcLbCoUZUFVGs6itKW_iiuCr7O8fmxvFi7fXz-HTlTixpU0xQtTc0iVs9ArsAqm3epQMKEmoVEOsUhY97GSE1G94ph0xXGV29lyjhbznpWd5aQaR4bc9a_Ebh7PdePw_rv4y5ktMGIQ7CwsJWD45eChqXFc9dpb_Ch-Rw_JBVvrOVw4SkqBRK11ZgwW_LCyC8TwAnyBCZrPcZC11Q"
# authorization
session = VkApi(token=GROUP_TOKEN)
user_access = VkApi(token=USER_TOKEN)

# get longpoll
longpoll = VkLongPoll(session)
vk = session.get_api()
user_vk = user_access.get_api()

# check for new messages
def main():
    DataBase.create_database()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_info = vk.users.get(user_id=event.user_id, fields="sex,city,bdate")[0]
            print(user_info)
            user_id = user_info["id"]
            age = int(input("Enter the age: "))
            city = int(input("Enter the city: "))
            gender = 2 if input("Enter the gender").lower() == "male" else 1
            status = int(input("Enter the status: "))
            count = 100

            matching_users = SearchEngine.search_people(user_vk, age, gender, city, status, count)

            for user in matching_users:
                vk.messages.send(
                    peer_id=event.user_id,
                    random_id=get_random_id(),
                    message=f"{user['url']}\n{', '.join(user['top_photos'])}",
                )


if __name__ == "__main__":
    main()
