"""
Enables logs of the console to be outputted to a unique log file, these can be found under "Logs"
"""
import sys
from datetime import datetime


class Logger(object):
    """
    A class to be used for generating logs
    """

    def __init__(self):
        """
        Initialise and generate the log name using the current date and time
        """
        self.terminal = sys.stdout
        self.log = open("./Logs/{}.txt".format(datetime.now().strftime("%H%M%S")), "w+")

    def write(self, output):
        """
        Write the output of the console to the log file
        """
        self.terminal.write(output)  # Output to console
        self.log.write("{}\n".format(output))  # Save same output to Logs file

    def flush(self):
        """
        Need to include
        """
        pass


def start_log():
    """
    Call to begin a log
    """
    sys.stdout = Logger()
