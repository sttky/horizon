import re
from threading import Thread, ThreadError
from datetime import timedelta

from .events import EventData
from .enumerators import EventThreadStatus

TIME_UNITS_FACTOR = dict(s=1, m=60, h=3600)

RE_TIMEDELTA = r'^((\d{1,2})h)?((\d{1,2})m)?((\d{1,2})s)?$'

def as_timedelta(*arg, **kwargs):
    """
    Processes various inputs and returns a datetime.timedelta instance.

    >>> as_timedelta(datetime.timedelta(seconds=10)) # -> datetime.timedelta(seconds=10)
    >>> as_timedelta(seconds=10) # -> datetime.timedelta(seconds=10)
    >>> as_timedelta("1h10m20s") # -> datetime.timedelta(seconds=4220)
    >>> as_timedelta("1h10m20s") # -> datetime.timedelta(seconds=4220)
    >>> as_timedelta(1) # -> datetime.timedelta(seconds=60), i.e. 1 minute
    """
    if (len(arg) > 1) | (len(arg)*len(kwargs) != 0) | (len(arg) + len(kwargs) == 0):
        raise ValueError("Expecting 1 argument or multiple keyword arguments.")

    if isinstance(arg[0], timedelta):
        return arg[0]
    
    elif type(arg[0]) == dict:
        return timedelta(**arg[0])
    
    elif type(arg[0]) == str:
        res = re.match(RE_TIMEDELTA, arg[0])

        if not res:
            raise ValueError("Invalid input string format!")
        
        else:
            h = 0 if res.group(2) == None else int(res.group(2))
            m = 0 if res.group(4) == None else int(res.group(2))
            s = 0 if res.group(6) == None else int(res.group(2))

        return timedelta(hours=h, minutes=m, seconds=s)
    
    elif type(arg[0]) in (int, float):
        return timedelta(seconds=arg[0])
    
    else:
        raise ValueError()
    

class EventThread(Thread):
    exception = None
    data = EventData()
    state = EventThreadStatus.New # not started

    def run(self):
        """ Runs the thread in a try:except statement to catch and store exceptions. """
        self.state = EventThreadStatus.Running # running
        self.exception = None
        # catch exceptions while executing thread
        try:
            self.return_value = self._target(*self.args, **self._kwargs)
        except BaseException as e:
            self.exception = e

    def join(self):
        """ Joins the thread and re-throws any exception raised inside the thread. """
        super(EventThread, self).join()
        self.state = EventThreadStatus.Completed # completed

        if self.exception is not None:
            self.state = EventThreadStatus.Exception # exception
            raise self.exception
        
        return self.return_value

    