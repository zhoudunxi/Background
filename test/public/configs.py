#coding=UTF-8

import os, ConfigParser


def getconfig(section, option):
    """
    Get a configure option.
    :param section, string.
    :param option, string.
    """
    # The configure file.
    config_file = '%s%sconfigs%spublic.conf' % (
        os.path.dirname(os.path.realpath(__file__)),
        os.path.sep, os.path.sep)
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    return config.get(section, option)
