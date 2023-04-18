from utils import DataBase


def search_people(vk, age, gender, city, status, count):
    search_results = vk.users.search(
        age_from=age,
        age_to=age,
        city=city,
        sex=gender,
        status=status,
        count=count,
    )["items"]

    result = []

    for user in search_results:
        if user["is_closed"]:
            continue

        user_id = user["id"]
        if not DataBase.user_exists(user_id):
            top_photos = get_top_photos(vk, user_id)
            DataBase.insert_user(user_id, age, city, gender, status)

            result.append(
                {
                    "id": user_id,
                    "url": f"https://vk.com/id{user_id}",
                    "top_photos": top_photos,
                }
            )
    return result


def get_top_photos(vk, user_id):
    photos = vk.photos.getAll(owner_id=user_id, count=200, no_service_albums=0, extended=1)

    def weight(photo):
        if 'comments' not in photo:
            photo['comments'] = {'count': 0}
        if 'likes' not in photo:
            photo['likes'] = {'count': 0}
        return photo["likes"]["count"] + photo["comments"]["count"]

    sorted_photos = sorted(photos["items"], key=weight, reverse=True)
    return [photo["sizes"][-1]["url"] for photo in sorted_photos[:3]]
