from vk_api.keyboard import VkKeyboardColor


def set_main_keyboard(keyboard):
    set_clear_keyboard(keyboard)
    keyboard.add_button("Поиск", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Мои совпадения", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Помощь", color=VkKeyboardColor.NEGATIVE)


def set_gender_keyboard(keyboard):
    set_clear_keyboard(keyboard)
    keyboard.add_button("Мужской", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Женский", color=VkKeyboardColor.PRIMARY)


def set_status_keyboard(keyboard):
    set_clear_keyboard(keyboard)
    keyboard.add_button("Не женат / не замужем", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Встречается", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Помолвлен", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Женат / замужем", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Все сложно", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("В активном поиске", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Влюблен(-a)", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("В гражданском браке", color=VkKeyboardColor.PRIMARY)


def set_change_keyboard(keyboard):
    set_clear_keyboard(keyboard)
    keyboard.add_button("Да, изменить данные", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Нет, начать поиск", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button("Назад", color=VkKeyboardColor.NEGATIVE)


def set_clear_keyboard(keyboard):
    keyboard.keyboard.clear()
