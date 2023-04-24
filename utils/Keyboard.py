from vk_api.keyboard import VkKeyboardColor, VkKeyboard


def main_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Поиск", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Мои совпадения", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Помощь", color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


def gender_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Мужской", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Женский", color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()


def status_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Не женат / не замужем", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Встречается", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Помолвлен(-а)", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Женат / замужем", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Все сложно", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("В активном поиске", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Влюблен(-a)", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("В гражданском браке", color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()


def change_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Да, изменить данные", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Нет, начать поиск", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button("Вернуться в главное меню", color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()


def next_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Далее", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Вернуться в главное меню", color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()


def fill_in_keyboard(scopes):
    keyboard = VkKeyboard(one_time=True)
    for scope in scopes:
        if scope == "возраст":
            keyboard.add_button("Указать возраст", color=VkKeyboardColor.PRIMARY)
        elif scope == "город":
            keyboard.add_button("Указать город", color=VkKeyboardColor.PRIMARY)
        elif scope == "пол":
            keyboard.add_button("Указать пол", color=VkKeyboardColor.PRIMARY)
        elif scope == "статус":
            keyboard.add_button("Указать статус", color=VkKeyboardColor.PRIMARY)

    keyboard.add_button("Вернуться в главное меню", color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()
