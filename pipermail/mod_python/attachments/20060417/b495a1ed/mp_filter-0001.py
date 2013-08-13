import os, threading

class FilterWrapper(object):
    """A thin wrapper around a filter object that adds __iter__."""

    def __init__(self, filter):
        self._inpipe, self._outpipe = os.pipe()
        self._update(filter)

    def _update(self, filter):
        """Update filter methods and properties with a new filter object's."""
        for name in dir(filter):
            if not name.startswith('_'):
                setattr(self, name, getattr(filter, name))

    def __iter__(self):
        """Use a pipe for reading from main thread."""
        while 1:
            buffer = os.read(self._inpipe, 1024)
            if buffer:
                yield buffer
            else:
                break


def filterhandler(filter):
    """A generic filter handler.  This statically calls "my_filter, but could
    easily be extended to call req.get_options and apache.resolve_object."""

    if not hasattr(filter.req, 'this_filter'):
        # first call, set up per req filter info
        this_filter = filter.req.this_filter = FilterWrapper(filter)
        filter.req.filter_thread = threading.Thread(target = my_filter, args = (this_filter,))
        filter.req.filter_thread.start()
    else:
        # recurring call
        this_filter = filter.req.this_filter
        this_filter._update(filter)

    while 1:
        buffer = filter.read(1024)
        if buffer is None:
            os.close(this_filter._outpipe)
            filter.req.filter_thread.join()
        elif len(buffer):
            os.write(this_filter._outpipe, buffer)
        else:
            break


def my_filter(filter):
    """Something simple, like convert to all upper case."""
    for bit in filter:
        filter.write(bit.upper())
    filter.close()
