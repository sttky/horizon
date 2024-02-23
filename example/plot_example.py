import time

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

colors = ['C0','C1','C2','C3','C4','C5']

from horizon import *
from horizon.util import as_timedelta

event1 = Event(action=lambda t: print('Event 1 triggered at {}'.format(t)), duration=5, after_delay=0.5)
event2 = Event(action=lambda t: print('Event 2 triggered at {}'.format(t)), before_delay=1, before=EndOf(event1), duration=2)
event3 = Event(action=lambda t: print('Event 3 triggered at {}'.format(t)), before_delay=1, before=EndOf(event2), duration=2)
event4 = Event(action=lambda t: print('Event 4 triggered at {}'.format(t)), before_delay=1, before=StartOf(event2), duration=2)

loop = EventLoop(events=[event1, event3, event2, event4])

height = 0.8
fig = plt.figure()
ax = plt.subplot(1,1,1,aspect=1)
for (i, event) in enumerate(loop.events):
    y = len(loop.events) - i
    dy = height
    x = event.start.total_seconds()
    dx = event.duration.total_seconds()
    color = colors[event.type.value]

    rect = Rectangle((x,y), dx, dy, facecolor=color)
    ax.add_patch(rect)

    if event.before_delay > as_timedelta(0):
        rect = Rectangle((x-event.before_delay.total_seconds(),y), event.before_delay.total_seconds(), dy, facecolor=color, alpha=0.5)
        ax.add_patch(rect)

    if event.after_delay > as_timedelta(0):
        rect = Rectangle((x + dx,y), event.after_delay.total_seconds(), dy, facecolor=color, alpha=0.5)
        ax.add_patch(rect)

    if event.before:
        pass

    if event.after:
        pass


ax.autoscale()
plt.show()


loop.run()


