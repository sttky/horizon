from dataclasses import dataclass, field
from typing import Any, Union

from .util import as_timedelta, PropagatingThread, ThreadError
from .enumerators import EventType


@dataclass
class Event():
    name: str="new event"
    id: int=-1
    type: int=EventType.Fixed
    before: Any=None
    after: Any=None
    before_delay: Any=0
    after_delay: Any=0
    duration: Any=0
    action: Any=None


    def __post_init__(self):
        # update the delays and durations to be datetime.timedelta
        self.before_delay = as_timedelta(self.before_delay)
        self.after_delay = as_timedelta(self.after_delay)
        self.duration = as_timedelta(self.duration)
        # initialize the event thread
        self._threading_status = 0
        self._result_is_stale = True
        self._result = None
        self._attach_new_thread()


    def _attach_new_thread(self):
        """ Attaches a fresh thread to this event to run the action. """
        if self.is_alive:
            raise ThreadError('Attempt to attach a new thread while the current thread is still alive.')
        
        thread_name = '{name} Thread'.format(name=self.name)

        if hasattr(self.action, '__call__'):
            self._thread = PropagatingThread(target=self.action, name=thread_name)

        else:
            self._thread = PropagatingThread(target=lambda t:None, name=thread_name)

        self._threading_status = 1 # fresh thread set up


    @property
    def is_event(self):
        return True
    

    @property
    def is_alive(self):
        if not hasattr(self, '_thread'):
            return False
        else:
            return self._thread.is_alive
    
    @property
    def result(self):
        self._result_is_stale = True
        return self._result
        

    @property
    def start(self):
        if self.before == None:
            return as_timedelta(0)
        else:
            return self.before.end + self.before_delay
        
    @property
    def end(self):
        return self.start + self.duration + self.after_delay
    
    def trigger(self, time=0):
        if hasattr(self.action, '__call__'):
            self._thread.args = (time,)
            self._thread.start()



@dataclass
class Marker():
    name: str="new marker"
    id: int=-1
    time: Any=0

    def __post_init__(self):
        self.time=as_timedelta(self.time)

    @property
    def start(self):
        return self.time
    
    @property
    def end(self):
        return self.time
    
    @property
    def is_event(self):
        return False    


class StartOf(Marker):

    def __init__(self, event_or_marker):
        self.anchor = event_or_marker
        if isinstance(self.anchor, Event):
            time = self.anchor.end
        elif isinstance(self.anchor, Marker):
            time = self.anchor.time

        Marker.__init__(self, name="Start of {name}".format(name=self.anchor.name), id=-1, time=time)


class EndOf(Marker):

    def __init__(self, event_or_marker):
        self.anchor = event_or_marker
        if isinstance(self.anchor, Event):
            time = self.anchor.end
        elif isinstance(self.anchor, Marker):
            time = self.anchor.time

        Marker.__init__(self, name="End of {name}".format(name=self.anchor.name), id=-1, time=time)


