from typing import Union, Optional
from typing import Any, List
import logging
import sys

T = Union[int, float, str]

logger = logging.getLogger(__name__)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
consoleHandler = logging.StreamHandler(sys.stdout)
logger.addHandler(consoleHandler)
logger.setLevel(logging.DEBUG)


def is_iterable(obj: Any) -> bool:
    """
    Return whether an object is iterable or not.

    :param obj: Any object for check
    """
    try:
        iter(obj)
    except TypeError:
        return False
    return True


def group_items_in_batches(items: List[Any], items_per_batch: int = 0, fill: Any = None) -> List[List[Any]]:
    """
    Responsible for grouping items in batch taking into account the quantity of items per batch

    e.g.
    >>> group_items_in_batches(items=[1,2,3,4], items_per_batch=3)
    [[1, 2, 3], [4]]
    >>> group_items_in_batches(items=[1,2,3,4], items_per_batch=3, fill=0)
    [[1, 2, 3], [4, 0, 0]]

    :param items: list of any values
    :param items_per_batch: number of items per batch
    :param fill: fill examples when items is not divisible by items_per_batch, default is None
    :return:
    """
    items_length = len(items)
    if not isinstance(items_per_batch, int):
        raise TypeError(f"Value for items_per_batch is not valid. Please send integer.")
    if items_per_batch < 0 or items_per_batch > len(items):
        raise ValueError(f"Value for items_per_batch is not valid. I need a number integer between 0 and {len(items)}")
    if items_per_batch == 0:
        return items

    if fill is not None:
        missing = items_per_batch - items_length % items_per_batch
        items += missing * [fill]

    batches = []

    for i in range(0, items_length, items_per_batch):
        batch = [group for group in items[i:i + items_per_batch]]
        batches.append(batch)
    return batches


def remove_duplicate_items(items: Optional[list]) -> Any:
    """
    remove duplicate items in an item list or duplicate items list of list

    e.g usage:
    >>> remove_duplicate_items([1,2,1,2,1])
    [1, 2]
    >>> remove_duplicate_items(['hi', 'hi', 'ih'])
    ['hi', 'ih']

    >>> remove_duplicate_items([['hi'], ['hi'], ['ih']])
    [['hi'], ['ih']]
    >>> remove_duplicate_items([[1,2,1,2,1], [1,2,1,2,1], [1,2,1,2,3]])
    [[1, 2, 1, 2, 1], [1, 2, 1, 2, 3]]
    """
    # TODO: improve function
    if not is_iterable(items) or isinstance(items, str):
        raise TypeError("Send iterable except string.")

    try:
        return list(dict.fromkeys(items))
    except TypeError:
        return sorted([list(item) for item in set(tuple(x) for x in items)], key=items.index)


if __name__ == "__main__":
    pass
