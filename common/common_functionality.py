from sys import version_info

if version_info[0] < 3:
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser
from os import path


def read_config():
    cfg = ConfigParser()
    filename = path.join(path.dirname(path.dirname(path.abspath(__file__))),
                                      'settings.cfg')
    cfg.read(filename)
    return cfg


def set_time(in_datetime, time="wake_up"):
    cfg = read_config()
    return in_datetime.replace(minute=0).replace(second=0).replace(hour=int(cfg.get(
        'variables', time)))


def percent_elapsed(current_datetime):
    # get wake up time
    wake_up_time = set_time(current_datetime, "wake_up")
    bed_time = set_time(current_datetime, "bedtime")
    hours_awake = float((bed_time - wake_up_time).seconds)
    current_awake_time = float((current_datetime - wake_up_time).seconds)
    return 100 * (current_awake_time / hours_awake)
