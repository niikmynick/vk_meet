from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from utils import SearchEngine, DataBase, OutputManager

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

outputManager = OutputManager.OutputManager(session)


# check for new messages
def main():
    DataBase.create_database()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_info = vk.users.get(user_id=event.user_id, fields="sex,city,bdate")[0]
            print(user_info)
            age = int(input("Enter the age: "))
            city = int(input("Enter the city: "))
            gender = 2 if input("Enter the gender: ").lower() == "male" else 1
            status = int(input("Enter the status: "))
            count = 100

            matching_users = SearchEngine.search_people(user_vk, age, gender, city, status, count)

            for user in matching_users[:3]:
                print(user)
                for photo in user['top_photos']:
                    print(photo)
                    outputManager.send_image(event.user_id, photo)
                    # user_vk.messages.send(
                    #     peer_id=event.user_id,
                    #     random_id=get_random_id(),
                    #     attachment=photo
                    # )


if __name__ == "__main__":
    main()
