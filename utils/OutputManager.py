from vk_api.utils import get_random_id


class OutputManager:

    def __init__(self, session):
        self.session = session

    def send_message(self, user_id, message=None, attachment=None, keyboard=None):
        self.session.method('messages.send', {'user_id': user_id, 'message': message, 'attachment': attachment, 'keyboard': keyboard, 'random_id': get_random_id()})
