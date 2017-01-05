# The configuration information used by this project
# Author: Liang Tang
# License: BSD
import ConfigParser
import os
from pyvalue import constants

config = None


def init():
    package_dir = os.path.dirname(constants.__file__)
    config_file = package_dir + "/../config.ini"
    global config
    if config is None:
        config = ConfigParser.ConfigParser()
        print "Load config file : "+config_file
        config.read(config_file)


