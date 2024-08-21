#!/usr/bin/env python3
"""
Contains:
    Classes
    =======
    LIFOCache - A caching system that implements the
    LIFO (Last In First Out) cache replacement algorithm
"""
from typing import List

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    A caching system that implements the
    LIFO (Last In First Out) cache replacement algorithm

    The limit for the number of items the cache can hold at
    a time is BaseCaching.MAX_ITEMS, which by default is 4

    When a new item is to be added and 4 items are in the cache
    already, the last one inserted out of the four is removed.
    """
    def __init__(self) -> None:
        super().__init__()
        self.keys_by_insertion_order: List = []

    def put(self, key, item):
        """
        Add a new item to the cache

        Args:
            key: The key to store the value by
            item: The value to store
        """
        if key and item:
            if key in self.cache_data:
                self.cache_data[key] = item
            else:
                if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                    last_key = self.keys_by_insertion_order[-1]
                    print("DISCARD: {}".format(last_key))
                    del self.cache_data[last_key]
                    self.keys_by_insertion_order.pop(-1)
                self.cache_data[key] = item
                self.keys_by_insertion_order.append(key)

    def get(self, key):
        """ Get an item from the cache by key

        Args:
            key: The key by which to fetch the value

        Returns:
            The value stored by the given key if the key exists
            in the cache. Otherwise, if key is None, or the key
            is not in the cache, returns None.
        """
        return key and self.cache_data.get(key)
