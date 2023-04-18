import datetime


class Logger:
    def __init__(self, log_file):
        self.log_file = open(log_file, 'w')

    def trace(self, message):
        self.log_file.write(f'{datetime.datetime.now()} TRACE {message}')
        self.log_file.write('\n')

    def debug(self, message):
        self.log_file.write(f'{datetime.datetime.now()} DEBUG {message}')
        self.log_file.write('\n')

    def info(self, message):
        self.log_file.write(f'{datetime.datetime.now()} INFO {message}')
        self.log_file.write('\n')

    def warn(self, message):
        self.log_file.write(f'{datetime.datetime.now()} WARN {message}')
        self.log_file.write('\n')

    def error(self, message):
        self.log_file.write(f'{datetime.datetime.now()} ERROR {message}')
        self.log_file.write('\n')

    def fatal(self, message):
        self.log_file.write(f'{datetime.datetime.now()} FATAL {message}')
        self.log_file.write('\n')

    def message(self, handler, profile):
        self.log_file.write(f'{datetime.datetime.now()} MESSAGE')
        self.log_file.write(f'New message by user: {profile[0]["first_name"]} {profile[0]["last_name"]}')
        self.log_file.write(f'Message: {str(handler.text)}')

    def user(self, user_name, user_surname, user_age, user_sex_id, user_city, user_status):
        self.log_file.write(f'{datetime.datetime.now()} USER')
        self.log_file.write(f'New user: {user_name} {user_surname}')
        self.log_file.write(f'Age: {user_age}')
        self.log_file.write(f'Sex id: {user_sex_id}')
        self.log_file.write(f'City: {user_city}')
        self.log_file.write(f'Status: {user_status}')
