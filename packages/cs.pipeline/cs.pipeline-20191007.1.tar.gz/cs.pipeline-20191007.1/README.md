Function pipelines mediated by queues and a Later.


*Latest release 20191007.1*:
Pipeline functionality extracted from cs.later: asynchronous pipelines mediated with a cs.later.Later.

Function pipelines mediated by queues and a Later.

## Class `Pipeline`

MRO: `cs.resources.MultiOpenMixin`  
A Pipeline encapsulates the chain of PushQueues created by
a call to Later.pipeline.

### Method `Pipeline.__init__(self, name, L, actions, outQ)`

Initialise the Pipeline from `name`, Later instance `L`,
list of filter functions `actions` and output queue `outQ`.

Each action is either a 2-tuple of (sig, functor) or an
object with a .sig attribute and a .functor method returning
a callable.

## Function `pipeline(later, actions, inputs=None, outQ=None, name=None)`

Construct a function pipeline to be mediated by this Later queue.
Return: `input, output`
where `input`` is a closeable queue on which more data items can be put
and `output` is an iterable from which result can be collected.

Parameters:
* `actions`: an iterable of filter functions accepting
  single items from the iterable `inputs`, returning an
  iterable output.
* `inputs`: the initial iterable inputs; this may be None.
  If missing or None, it is expected that the caller will
  be supplying input items via `input.put()`.
* `outQ`: the optional output queue; if None, an IterableQueue() will be
  allocated.
* `name`: name for the PushQueue implementing this pipeline.

If `inputs` is None or `open` is true, the returned `input` requires
a call to `input.close()` when no further inputs are to be supplied.

Example use with presupplied Later `L`:

    input, output = L.pipeline(
            [
              ls,
              filter_ls,
              ( FUNC_MANY_TO_MANY, lambda items: sorted(list(items)) ),
            ],
            ('.', '..', '../..'),
           )
    for item in output:
      print(item)



# Release Log

*Release 20191007.1*:
Pipeline functionality extracted from cs.later: asynchronous pipelines mediated with a cs.later.Later.
