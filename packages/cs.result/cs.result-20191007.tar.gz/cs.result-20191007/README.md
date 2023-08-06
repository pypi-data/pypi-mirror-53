Result and friends: callable objects which will receive a value at a later point in time.


*Latest release 20191007*:
Simplify ResultState definition.
Result.bg: use cs.threads.bg to dispatch the Thread.

Result and friends.

A Result is the base class for several callable subclasses
which will receive values at a later point in time,
and can also be used standalone without subclassing.

A call to a Result will block until the value is received or the Result is cancelled,
which will raise an exception in the caller.
A Result may be called by multiple users, before or after the value has been delivered;
if the value has been delivered the caller returns with it immediately.
A Result's state may be inspected (pending, running, ready, cancelled).
Callbacks can be registered via a Result's .notify method.

An incomplete Result can be told to call a function to compute its value;
the function return will be stored as the value unless the function raises an exception,
in which case the exception information is recorded instead.
If an exception occurred, it will be reraised for any caller of the Result.

Trite example::

  R = Result(name="my demo")

  Thread 1:
    value = R()
    # blocks...
    print(value)
    # prints 3 once Thread 2 (below) assigns to it

  Thread 2:
    R.result = 3

  Thread 3:
    value = R()
    # returns immediately with 3

You can also collect multiple Results in completion order using the report() function::

  Rs = [ ... list of Results of whatever type ... ]
  ...
  for R in report(Rs):
    x = R()     # collect result, will return immediately because
                # the Result is complete
    print(x)    # print result

## Function `after(Rs, R, func, *a, **kw)`

After the completion of `Rs` call `func(*a,**kw)` and return
its result via `R`; return the `Result` object.

Parameters:
* `Rs`: an iterable of Results.
* `R`: a `Result` to collect to result of calling `func`.
  If `None`, one will be created.
* `func`, `a`, `kw`: a callable and its arguments.

## Class `AsynchState`

MRO: `enum.Enum`  
State tokens for `Result`s.

## Function `bg(func, *a, **kw)`

Dispatch a `Thread` to run `func`, return a `Result` to collect its value.

## Class `CancellationError`

MRO: `builtins.Exception`, `builtins.BaseException`  
Raised when accessing result or exc_info after cancellation.

## Class `OnDemandFunction`

MRO: `Result`  
Wrap a callable, run it when required.

## Class `OnDemandResult`

MRO: `Result`  
Wrap a callable, run it when required.

## Function `report(LFs)`

Generator which yields completed `Result`s.

This is a generator that yields `Result`s as they complete,
useful for waiting for a sequence of `Result`s
that may complete in an arbitrary order.

## Class `Result`

Basic class for asynchronous collection of a result.
This is also used to make OnDemandFunctions, LateFunctions and other
objects with asynchronous termination.

### Method `Result.__init__(self, name=None, lock=None, result=None)`

Base initialiser for `Result` objects and subclasses.

Parameter:
* `name`: optional parameter naming this object.
* `lock`: optional locking object, defaults to a new `threading.Lock`.
* `result`: if not `None`, prefill the `.result` property.

## Class `ResultState`

MRO: `enum.Enum`  
State tokens for `Result`s.



# Release Log

*Release 20191007*:
Simplify ResultState definition.
Result.bg: use cs.threads.bg to dispatch the Thread.

*Release 20190522*:
Result.__call__ now accepts an optional callable and args.
Result.call: set the Result state to "running" before dispatching the function.
Rename OnDemandFunction to OnDemandResult, keep old name around for compatibility.
Result._complete: also permitted if state==cancelled.

*Release 20190309*:
Small bugfix.

*Release 20181231*:
Result.call: report baser exceptions than BaseException.
Drop _PendingFunction abstract class.

*Release 20181109.1*:
DISTINFO update.

*Release 20181109*:
Derive CancellationError from Exception instead of RuntimeError, fix initialiser.
Rename AsynchState to ResultState and make it an Enum.
Make Results hashable and comparable for equality for use as mapping keys: equality is identity.
New Result.collected attribute, set true if .result or .exc_info are accessed, logs an error if Result.__del__ is called when false, may be set true externally if a Result is not required.
Drop `final` parameter; never used and supplanted by Result.notify.
Result.join: return the .result and .exc_info properties in order to mark the Result as collected.
Result: set .collected to True when a notifier has been called successfully.
Bugfix Result.cancel: apply the new cancelled state.

*Release 20171231*:
Bugfix Result.call to catch BaseException instead of Exception.
New convenience function bg(func) to dispatch `func` in a separate Thread and return a Result to collect its value.

*Release 20171030.1*:
Fix module requirements specification.

*Release 20171030*:
New Result.bg(func, *a, **kw) method to dispatch function in separate Thread to compute the Result value.

*Release 20170903*:
rename cs.asynchron to cs.result
