"""Utilities
"""
import os
import time
import datetime
from decimal import Decimal
from dateutil.tz import gettz


def now_ts():
    """
    ts in ms
    """
    return Decimal(time.time() * 1000)


def now_day(days_back: int = 0):
    """Returns a string with the day of the week in the format:
    Mon, Tue, Wed, Thu, Fri, Sat, Sun
    :param days_back: int (-inf, 0]
    """
    return (datetime.datetime.now(gettz(os.environ['TZ'])) + datetime.timedelta(days=days_back)).strftime('%a')


def hour():
    """
    Returns the current hour
    """
    return datetime.datetime.now(gettz(os.environ['TZ'])).hour


def minute():
    """
    Returns the current minute
    """
    return datetime.datetime.now(gettz(os.environ['TZ'])).minute


def tot_min():
    """
    Minutes from 00:00
    """
    return hour() * 60 + minute()


def midday_ts(days_back: int = 0):
    """
    The 12:00 local time N days back
    :param days_back:
    :return: ts in ms
    """
    today = datetime.datetime.now(gettz(os.environ['TZ']))
    yesterday = datetime.datetime(today.year, today.month, today.day, 12,
                                  tzinfo=gettz(os.environ['TZ'])) - datetime.timedelta(days=days_back)
    return Decimal(yesterday.timestamp() * 1e3)


def midnight_ts(days_back: int = 0):
    """
    The 00:00 local time N days back
    :param days_back:
    :return: ts in ms
    """
    today = datetime.datetime.now(gettz(os.environ['TZ']))
    yesterday = datetime.datetime(today.year, today.month, today.day, 0,
                                  tzinfo=gettz(os.environ['TZ'])) - datetime.timedelta(days=days_back)
    return Decimal(yesterday.timestamp() * 1e3)


def day_hour_ts(days_back: int = 0, hour: int = 0):
    """
    The 'hh' local time N days back
    :param days_back: how many days back (-inf, 0]
    :param hour: the hour of the day [0, 23]
    :return: ts in ms
    """
    today = datetime.datetime.now(gettz(os.environ['TZ']))
    yesterday = datetime.datetime(today.year, today.month, today.day, hour,
                                  tzinfo=gettz(os.environ['TZ'])) + datetime.timedelta(days=days_back)
    return Decimal(yesterday.timestamp() * 1e3)


def benchmark(display_func):
    """
    Used to time functions
    :param display_func: function to display the results, e.g. print
    :return:
    """

    def time_it(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            res = func(*args, **kwargs)
            display_func('{name} executed in {time}s'.format(name=func.__name__,
                                                             time=time.perf_counter() - start))
            return res

        return wrapper

    return time_it

def age(dob):
    """
    This function converts the dob to age for a user.
    :param dob: date of birth should be of the format d-m-y
    :return: age
    """
    dob = datetime.datetime.strptime(dob, '%d-%m-%Y')
    today = datetime.datetime.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
