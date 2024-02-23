# Horizon
An event sequencer for automation. Works with events and markers to define a sequence.

*Events* have
* a start that defines when they occur in the sequence. This can be
  * an absolute time in the sequence, or
  * a time relative to another event or marker
* a duration -- or not. Events without fixed duration may wait for another event to finish, user input, etc.
* an end that marks when the event is completed.
* an *EventThread* that runs the target function for the event.
* a target function that will be executed when the event starts.

*Markers*
* have a time that defines where they are located.
* can easily be defined from the Start or End of an event.

The *EventLoop* runs the sequence of all events, making sure that all dependencies are ensured.

Non-executable events may be implemented at a later date as a way to set up Gantt-chart-like 
sequences. Maybe even run these events with dependencies to actively track progress?
