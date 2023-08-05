"""
Queues
======

The SoupStarsQueue behaves just like a normal queue, but it will only ever
store one copy of an item, so that the same item can not be added twice. This
helps prevent multiple requests to the same page in a single crawl.

>>> from soupstars.queues import SoupStarsQueue
>>> queue = SoupStarsQueue()
>>> queue.put('a')
>>> queue.put('a')
RequeuedError: Tried to queue `a` twice

Use the `added` attribute of the queue to test if an item has ever been added.

>>> 'a' in queue.added
True

Since the queue uses a hash to store the list of items that have been queued,
only items that are hashable can be added to the queue.

>>> queue.added
{'a'}
>>> queue.put([])
TypeError: unhashable type 'list'

For convenience, multiple items can be added at once.

>>> queue.put_all(['b', 'c'])
>>> print(queue.added)
{'a', 'b', 'c'}

To suppress requeued errors when adding multiple items, use
`ignore_duplicates=True`

>>> queue.put_all(['d', 'd'], ignore_duplicates=True)
>>> queue.added
{'a', 'b', 'c', 'd'}
"""

from queue import Queue
from queue import Empty as EmptyQueueError


class RequeuedError(Exception):
    """
    Raised if the same item is placed into a queue more than once.
    """

    pass


class MaxResultsExceededError(Exception):
    """
    Raised if too many have ever been placed into a queue
    """

    pass


class ResultsQueue(Queue):
    """
    Used to store results before writing them. Accepts only a certain number
    of items total.
    """

    def __init__(self, max_results=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.max_results = max_results

    def put(self, item, **kwargs):
        """
        Places `item` into the queue if it has not already been entered. Raises
        a `FullQueueError` if the queue has already had `max_results` placed
        """

        if (self.max_results > 0) and (self.counter >= self.max_results):
            raise MaxResultsExceededError(f"Queue has already put the maximum ({self.max_results}) number of items")
        else:
            super().put(item, **kwargs)
            self.counter += 1

    def full(self):
        # TODO: write a test for this...
        return (self.max_results > 0) and (self.counter >= self.max_results)


class LinksQueue(Queue):
    """
    A FIFO queue that prevents the same item from being added twice.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.added = set()

    def put(self, item, **kwargs):
        """
        Places `item` into the queue if it has not already been entered. Raises
        a `RequeuedError` if the item was previously placed in the queue
        """

        if item in self.added:
            raise RequeuedError(f"{item} has already been added to the queue. Can not queue the same item twice")
        else:
            super().put(item, **kwargs)
            self.added.add(item)

    def put_all(self, items, ignore_duplicates=False, **kwargs):
        """
        Places all `items` into the queue, one at a time. If the same item has
        ever been placed into the queue before (including during the call),
        it will raise a `RequeuedError`. To suppress the errors, set
        `ignore_duplicates = True
        """

        for item in items:
            try:
                self.put(item, **kwargs)
            except RequeuedError as err:
                if ignore_duplicates:
                    continue
                else:
                    raise err
