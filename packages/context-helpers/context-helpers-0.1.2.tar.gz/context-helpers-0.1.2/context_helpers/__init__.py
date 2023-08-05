from contextlib import contextmanager
from contextlib2 import ExitStack

@contextmanager
def nested_context(context_managers):
    """
    This function is for situations where you have a dynamic number of context
    managers you need to enter, so you can't use multi-with. This saves a bit
    of boilerplate over just using ExitStack.

    :param context_managers: an interable of context managers
    :return: a tuple of values yielded from each of the context managers, in order
    """
    with ExitStack() as stack:
        yield tuple(
            stack.enter_context(context_manager)
            for context_manager in context_managers
        )


def nested(*context_managers):
    """
    This function exactly replicates the interface of contextlib.nested from
    python < 2.7. If you're writing new code you should NOT use this function.
    This exists as a way to replace usages of contextlib.nested in an automated
    way so that the code that uses it can be run in python 3.

    :param context_managers: a list of context managers
    :return: a tuple of values yielded from each of the context managers, in order
    """
    return nested_context(context_managers)
