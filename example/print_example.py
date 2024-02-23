import time

from horizon import *

event1 = Event(action=lambda t: print('Event 1 triggered at {}'.format(t)), duration=5)
event2 = Event(action=lambda t: print('Event 2 triggered at {}'.format(t)), before_delay=10, before=EndOf(event1))

event1.trigger()
event2.trigger()

loop = EventLoop(events=[event1, event2])

loop.run()
