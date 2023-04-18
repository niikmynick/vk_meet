from vk_api.keyboard import VkKeyboardColor


def set_standard_keyboard(keyboard):
    keyboard.add_button("Поиск", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Мои совпадения", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Помощь", color=VkKeyboardColor.NEGATIVE)


def set_gender_keyboard(keyboard):
    keyboard.add_button("Мужской", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Женский", color=VkKeyboardColor.PRIMARY)


def set_status_keyboard(keyboard):
    keyboard.add_button("Не женат", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Встречается", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Помолвлен", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Женат", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Все", color=VkKeyboardColor.PRIMARY)
