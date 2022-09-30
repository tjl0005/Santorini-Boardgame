import sys
from datetime import datetime


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("./Log/{}.txt".format(datetime.now().strftime("%H%M%S")), "w+")

    def write(self, output):
        self.terminal.write(output)  # Output to console
        self.log.write("{}\n".format(output))  # Save same output to Log file

    def flush(self):
        pass


def startLog(condition):
    if condition:
        sys.stdout = Logger()
