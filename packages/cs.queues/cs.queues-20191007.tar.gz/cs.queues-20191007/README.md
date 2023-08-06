some Queue subclasses and ducktypes


*Latest release 20191007*:
PushQueue: improve __str__.
Clean lint, drop cs.obj dependency.

Queue-like items: iterable queues and channels.

## Class `Channel`

A zero-storage data passage.
Unlike a Queue(1), put() blocks waiting for the matching get().

## Function `IterablePriorityQueue(*args, capacity=0, name=None, **kw)`

Factory to create an iterable PriorityQueue.

## Function `IterableQueue(*args, capacity=0, name=None, **kw)`

Factory to create an iterable Queue.

## Class `NullQueue`

MRO: `cs.resources.MultiOpenMixin`  
A queue-like object that discards its inputs.
Calls to .get() raise Queue_Empty.

### Method `NullQueue.__init__(self, blocking=False, name=None)`

Initialise the NullQueue.

Parameters:
* `blocking`: if true, calls to .get() block until .shutdown().
  Default: False.
* `name`: a name for this NullQueue.

## Class `PushQueue`

MRO: `cs.resources.MultiOpenMixin`  
A puttable object which looks like an iterable Queue.

Calling .put(item) calls `func_push` supplied at initialisation
to trigger a function on data arrival, whose processing is mediated
queued via a Later for delivery to the output queue.

### Method `PushQueue.__init__(self, name, functor, outQ)`

Initialise the PushQueue with the Later `L`, the callable `functor`
and the output queue `outQ`.

Parameters:
* `functor` is a one-to-many function which accepts a single
  item of input and returns an iterable of outputs; it may be a
  generator. These outputs are passed to outQ.put individually as
  received.
* `outQ` is a MultiOpenMixin which accepts via its .put() method.

## Class `TimerQueue`

Class to run a lot of "in the future" jobs without using a bazillion
Timer threads.



# Release Log

*Release 20191007*:
PushQueue: improve __str__.
Clean lint, drop cs.obj dependency.

*Release 20190812*:
_QueueIterator: do MultiOpenMixin.__init__ so that __str__ is functional.

*Release 20181022*:
Bugfix Channel, drasticly simplify PushQueue, other minor changes.

*Release 20160828*:
Use "install_requires" instead of "requires" in DISTINFO.
TimerQueue.add: support optional *a and **kw arguments for func.
Many bugfixes and internal changes.

*Release 20150115*:
More PyPI metadata fixups.

*Release 20150111*:
Initial PyPI release.
