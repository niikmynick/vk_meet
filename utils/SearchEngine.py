from utils import DataBase


def search_people(vk, user_searching_id, age, gender, city, status):
    try:
        search_results = vk.users.search(
            age_from=age,
            age_to=age,
            city=city,
            sex=gender,
            status=status,
            count=100,
            has_photo=1,
        )["items"]

    except Exception as e:
        return "Что-то пошло не так. Попробуйте снова"

    for user in search_results:
        if user["is_closed"]:
            continue

        print(user)

        user_id = user["id"]

        if vk.photos.getAll(owner_id=user_id, count=1, no_service_albums=1, extended=1)["count"] == 0:
            continue

        if not DataBase.user_in_match(user_searching_id, user_id):
            top_photos = get_top_photos(vk, user_id)

            if not top_photos:
                continue

            DataBase.add_user(user_id, age, city, gender, status)

            DataBase.add_match(user_searching_id, user_id, ",".join(top_photos))

    return "Поиск завершен"


def get_top_photos(vk, user_id):
    photos = vk.photos.getAll(owner_id=user_id, count=200, no_service_albums=1, extended=1)

    def weight(photo):
        if 'comments' not in photo:
            photo['comments'] = {'count': 0}
        if 'likes' not in photo:
            photo['likes'] = {'count': 0}
        return photo["likes"]["count"] + photo["comments"]["count"]

    sorted_photos = sorted(photos["items"], key=weight, reverse=True)
    return ['photo{}_{}'.format(photo['owner_id'], photo['id']) for photo in sorted_photos[:3]]
