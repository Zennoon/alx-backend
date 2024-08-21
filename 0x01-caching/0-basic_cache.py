#!/usr/bin/env python3
"""
Contains:
    Classes
    =======
    BasicCache - Class providing minimal caching functionality
    with no limit to the number of items it can contain.
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """Simple no limit cache with no need for replacement algorithm"""
    def put(self, key, item):
        """ Add an item to the cache

        Args:
            key: The key to store the value by
            item: The value to store
        """
        if key and item:
            self.cache_data[key] = item

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