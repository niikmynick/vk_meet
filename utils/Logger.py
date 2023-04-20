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
