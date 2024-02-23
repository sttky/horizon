from enum import Enum

class EventType(Enum):
    Fixed = 0
    Dynamic = 1
    WaitForInput = 2

class EventThreadStatus(Enum):
    New = 0
    Running = 1
    Completed = 2
    Exception = 3
    