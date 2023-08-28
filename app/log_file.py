import logging
import os


class LogFile:
    def __init__(self, name):
        self.name = name
        self.path = os.path.join(os.path.dirname(__file__), '../log')
        os.makedirs(self.path, exist_ok=True)
        self.log = logging.getLogger(self.name)
        self.log.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.file_handler = logging.FileHandler(os.path.join(self.path, self.name + '.log'))
        self.file_handler.setFormatter(self.formatter)
        self.log.addHandler(self.file_handler)
