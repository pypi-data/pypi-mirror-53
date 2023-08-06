Queue functions for execution later in priority and time order.


*Latest release 20191007*:
Drop pipeline functionality, moved to new cs.pipeline module.

Queue functions for execution later in priority and time order.

I use `Later` objects for convenient queuing of functions whose
execution occurs later in a priority order with capacity constraints.

Why not futures?
I already had this before futures came out,
I prefer its naming scheme and interface,
and futures did not then support prioritised execution.

Use is simple enough: create a `Later` instance and typically queue
functions with the `.defer()` method::

    L = Later(4)      # a Later with a parallelism of 4
    ...
    LF = L.defer(func, *args, **kwargs)
    ...
    x = LF()          # collect result

The `.defer` method and its siblings return a `LateFunction`,
which is a subclass of `cs.result.Result`.
As such it is a callable,
so to collect the result you just call the `LateFunction`.

## Function `defer(func, *a, **kw)`

Queue a function using the current default Later.
Return the LateFunction.

## Class `LateFunction`

MRO: `cs.result.Result`  
State information about a pending function,
a subclass of `cs.result.Result`.

A `LateFunction` is callable,
so a synchronous call can be done like this:

    def func():
      return 3
    L = Later(4)
    LF = L.defer(func)
    x = LF()
    print(x)        # prints 3

Used this way, if the called function raises an exception it is visible:

    LF = L.defer()
    try:
      x = LF()
    except SomeException as e:
      # handle the exception ...

To avoid handling exceptions with try/except the .wait()
method should be used:

    LF = L.defer()
    x, exc_info = LF.wait()
    if exc_info:
      # handle exception
      exc_type, exc_value, exc_traceback = exc_info
      ...
    else:
      # use `x`, the function result

TODO: .cancel(), timeout for wait().

### Method `LateFunction.__init__(self, func, name=None, retry_delay=None)`

Initialise a LateFunction.

Parameters:
* `func` is the callable for later execution.
* `name`, if supplied, specifies an identifying name for the LateFunction.
* `retry_local`: time delay before retry of this function on RetryError.
  Default from `later.retry_delay`.

## Class `LatePool`

A context manager after the style of subprocess.Pool
but with deferred completion.

Example usage:

    L = Later(4)    # a 4 thread Later
    with LatePool(L) as LP:
      # several calls to LatePool.defer, perhaps looped
      LP.defer(func, *args, **kwargs)
      LP.defer(func, *args, **kwargs)
    # now we can LP.join() to block for all LateFunctions
    #
    # or iterate over LP to collect LateFunctions as they complete
    for LF in LP:
      result = LF()
      print(result)

### Method `LatePool.__init__(self, L=None, priority=None, delay=None, when=None, pfx=None, block=False)`

Initialise the LatePool.

Parameters:
* `L`: Later instance, default from default.current.
* `priority`, `delay`, `when`, `name`, `pfx`:
  default values passed to Later.submit.
* `block`: if true, wait for LateFunction completion
  before leaving __exit__.

## Class `Later`

A management class to queue function calls for later execution.

Methods are provided for submitting functions to run ASAP or
after a delay or after other pending functions. These methods
return LateFunctions, a subclass of cs.result.Result.

A Later instance' close method closes the Later for further
submission.
Shutdown does not imply that all submitted functions have
completed or even been dispatched.
Callers may wait for completion and optionally cancel functions.

TODO: __enter__ returns a SubLater, __exit__ closes the SubLater.

TODO: drop global default Later.

### Method `Later.__init__(self, capacity, name=None, inboundCapacity=0, retry_delay=None)`

Initialise the Later instance.

Parameters:
* `capacity`: resource contraint on this Later; if an int, it is used
  to size a Semaphore to constrain the number of dispatched functions
  which may be in play at a time; if not an int it is presumed to be a
  suitable Semaphore-like object, perhaps shared with other subsystems.
* `name`: optional identifying name for this instance.
* `inboundCapacity`: if >0, used as a limit on the number of
  undispatched functions that may be queued up; the default is 0 (no
  limit).  Calls to submit functions when the inbound limit is reached
  block until some functions are dispatched.
* `retry_delay`: time delay for requeued functions.
  Default: `DEFAULT_RETRY_DELAY`.

## Function `retry(retry_interval, func, *a, **kw)`

Call the callable `func` with the supplied arguments.

If it raises `RetryError`,
run `time.sleep(retry_interval)`
and then call again until it does not raise `RetryError`.

## Class `RetryError`

MRO: `builtins.Exception`, `builtins.BaseException`  
Exception raised by functions which should be resubmitted to the queue.

## Class `SubLater`

A class for managing a group of deferred tasks using an existing `Later`.

### Method `SubLater.__init__(self, L)`

Initialise the `SubLater` with its parent `Later`.

TODO: accept discard=False param to suppress the queue and
associated checks.



# Release Log

*Release 20191007*:
Drop pipeline functionality, moved to new cs.pipeline module.

*Release 20181231*:
New SubLater class to provide a grouping for deferred functions and an iteration to collect them as they complete.
Drop WorkerThreadPool (leaks idle Threads, brings little benefit).
Later: drop worker queue thread and semaphore, just try a dispatch on submit or complete.
Later: drop tracking code. Drop capacity context manager, never used.

*Release 20181109*:
Updates for cs.asynchron renamed to cs.result.
Later: no longer subclass MultiOpenMixin, users now call close to end submission, shutdown to terminate activity and wait to await finalisation.
Clean lint, add docstrings, minor bugfixes.

*Release 20160828*:
Use "install_requires" instead of "requires" in DISTINFO.
Add LatePool, a context manager after the flavour of subprocess.Pool.
Python 2 fix.
Rename NestingOpenCloseMixin to MultiOpenMixin - easier to type, say and remember, not to mention being more accurate.
Add RetryError exception for use by Later.retriable.
LateFunction: support RetryError exception from function, causing requeue.
LateFunction: accept retry_delay parameter, used to delay function retry.
Later.defer_iterable: accept `test_ready` callable to support deferring iteration until the callable returns truthiness.
New function retry(retry_interval, func, *a, **kw) to call func until it does not raise RetryError.
Later: wrap several methods in @MultiOpenMixin.is_opened.
Assorted bugfixes and improvements.

*Release 20150115*:
First PyPI release.
