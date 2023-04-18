from vk_api.utils import get_random_id


class OutputManager:

    def __init__(self, session):
        self.session = session

    def send_text(self, user_id, message):
        self.session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': get_random_id()})

    def send_image(self, user_id, image):
        self.session.method('messages.send', {'user_id': user_id, 'attachment': image, 'random_id': get_random_id()})
