import sys
from datetime import datetime


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("./log/{}.txt".format(datetime.now().strftime("%H%M%S")), "w+")

    def write(self, output):
        self.terminal.write(output)  # Output to console
        self.log.write("{}\n".format(output))  # Save same output to log file

    # Need to handle flush method
    def flush(self):
        pass
