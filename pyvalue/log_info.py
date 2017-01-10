# The log util
# Author: Liang Tang
# License: BSD
import sys
import datetime


class LogInfo(object):
    def __init__(self):
        self._enable = True
        self._key_values = {}

    def put_raw(self, key, value, level=0):
        """
        Put a key-value based log for the specified level logs
        :param level:
        :type level: int
        :param key:
        :type key: str
        :param value:
        :return:
        """
        if not isinstance(level, int):
            raise ValueError("The parameter level must be an integer")
        if level not in self._key_values:
            self._key_values[level] = {}
        self._key_values[level][key] = value

    def put(self, class_obj, key, value, level=0):
        if not hasattr(class_obj, "__name__"):
            raise ValueError("the class_obj argument must has '__name__' attribute")
        class_name = class_obj.__name__
        cat_key = class_name + "_" + key
        self.put_raw(key=cat_key, value=value, level=level)

    def get_raw(self, key, level=0):
        """
        Get a key-value based log for the specified level logs
        :param key:
        :type key: str
        :param level:
        :type level: int
        :return:
        """
        if not isinstance(level, int):
            raise ValueError("The parameter level must be an integer")
        if level not in self._key_values:
            return None
        if key not in self._key_values[level]:
            return None
        return self._key_values[level][key]

    def get(self, class_obj, key, level=0):
        if not hasattr(class_obj, "__name__"):
            raise ValueError("the class_obj argument must has '__name__' attribute")
        class_name = class_obj.__name__
        return self.get_raw(key=(class_name + "_" + key), level=level)

    def println(self, msg):
        self.put_raw(msg, "")
        print msg

    @staticmethod
    def info(msg, newline=True):
        sys.stdout.write("[" + LogInfo._date_str() + "] "+msg)
        if newline:
            sys.stdout.write("\n")

    @staticmethod
    def error(msg, newline=True):
        sys.stderr.write("[" + LogInfo._date_str() + "] " + msg + "\n")
        if newline:
            sys.stdout.write("\n")

    @staticmethod
    def _date_str():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return str(self._key_values)

    def __repr__(self):
        return self.__str__()

