import time
from dataclasses import dataclass, field
from typing import List, Union

from .util import as_timedelta

@dataclass
class EventLoop():
    events: List=field(default_factory=[])

    def __post_init__(self):
        self._start_times = [event.start for event in self.events]
        self._event_order = sorted(range(len(self._start_times)), key=lambda k: self._start_times[k])
        self._results = []

    def run(self):
        t0 = time.time()
        complete = False
        i = 0
        j = self._event_order[0]
        while not complete:
            if as_timedelta(time.time() - t0) >= self._start_times[j]:
                res = self.events[j].trigger(as_timedelta(time.time() - t0))
                i += 1
                if i >= len(self.events):
                    complete = True
                else:
                    j = self._event_order[i]
                self._results.append(res)
        

    