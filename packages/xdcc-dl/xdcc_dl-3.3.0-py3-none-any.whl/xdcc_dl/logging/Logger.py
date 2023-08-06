"""LICENSE
Copyright 2016 Hermann Krumrey <hermann@krumreyh.com>

This file is part of xdcc-dl.

xdcc-dl is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

xdcc-dl is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with xdcc-dl.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import logging
from typing import Optional
from datetime import datetime
from subprocess import check_output, CalledProcessError
from colorama import Fore, Back, Style


# noinspection PyMethodMayBeStatic
class Logger(object):
    """
    Class that handles log and print calls in the bot
    """

    logging_level = logging.WARNING
    """
    The logging level to display
    """

    last_end = "\n"
    """
    Keeps track of the last character to be printed
    """

    def log(self, message: str, level: Optional[int], back: Back = Back.BLACK,
            fore: Fore = Fore.GREEN, end: str = "\n"):
        """
        Logs a message at the specified logging level
        :param message: The message to log
        :param level: The level at which to log the message.
                      If set as None, will always be printed.
        :param back: The background color to print
        :param fore: The foreground color to print
        :param end: Characters to append to the string (Default newline)
        :return: None
        """
        if self.logging_level == -1:
            return

        if level is None or self.logging_level <= level:

            if self.last_end == "\r" and end != "\r":
                print()

            log_message = datetime.now().strftime("[%Y-%d-%m:%H-%M-%S]")
            log_message += " " + fore + back + message

            try:
                rows, _columns = check_output(['stty', 'size']).split()
                columns = int(_columns)
            except (ValueError, CalledProcessError):
                columns = 80

            log_message = log_message[0:columns]

            print(log_message + Style.RESET_ALL, end=end)

            self.last_end = end

    def info(self, message: str, back: Back = Back.BLACK,
             fore: Fore = Fore.GREEN, end: str = "\n"):
        """
        Logs a message at the INFO level
        :param message: The message to log
        :param back: The background color to print
        :param fore: The foreground color to print
        :param end: Characters to append to the string (Default newline)
        :return: None
        """
        self.log(message, logging.INFO, back, fore, end)

    def debug(self, message: str, back: Back = Back.WHITE,
              fore: Fore = Fore.BLACK, end: str = "\n"):
        """
        Logs a message at the DEBUG level
        :param message: The message to log
        :param back: The background color to print
        :param fore: The foreground color to print
        :param end: Characters to append to the string (Default newline)
        :return: None
        """
        self.log(message, logging.DEBUG, back, fore, end)

    def error(self, message: str, back: Back = Back.RED,
              fore: Fore = Fore.BLUE, end: str = "\n"):
        """
        Logs a message at the ERROR level
        :param message: The message to log
        :param back: The background color to print
        :param fore: The foreground color to print
        :param end: Characters to append to the string (Default newline)
        :return: None
        """
        self.log(message, logging.ERROR, back, fore, end)

    def warning(self, message: str, back: Back = Back.YELLOW,
                fore: Fore = Fore.BLUE, end: str = "\n"):
        """
        Logs a message at the WARNING level
        :param message: The message to log
        :param back: The background color to print
        :param fore: The foreground color to print
        :param end: Characters to append to the string (Default newline)
        :return: None
        """
        self.log(message, logging.WARNING, back, fore, end)

    def print(self, message: str, back: Back = Back.BLACK,
              fore: Fore = Fore.GREEN, end: str = "\n"):
        """
        Prints a message
        :param message: The message to print
        :param back: The background color to print
        :param fore: The foreground color to print
        :param end: Characters to append to the string (Default newline)
        :return: None
        """
        self.log(message, None, back, fore, end)
