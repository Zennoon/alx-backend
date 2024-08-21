#!/usr/bin/env python3
"""
Contains:
    Classes
    =======
    LFUCache - A caching system that implements the
    LFU (Least Frequently Used) cache replacement algorithm
"""
from typing import Dict, List

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    A caching system that implements the
    LFU (Least Frequently Used) cache replacement algorithm

    The limit for the number of items the cache can hold at
    a time is BaseCaching.MAX_ITEMS, which by default is 4

    When a new item is to be added and 4 items are in the cache
    already, the least recently used out of the four is removed.
    """
    def __init__(self) -> None:
        super().__init__()
        self.keys_by_usage_order: List = []
        self.keys_by_usage_frequency: Dict = {}

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
                self.keys_by_usage_order.remove(key)
                self.keys_by_usage_order.append(key)
                self.keys_by_usage_frequency[key] += 1

            else:
                if len(self.cache_data) == BaseCaching.MAX_ITEMS:

                    lfu_lru_key = self.get_lfu_lru_key()
                    print("DISCARD: {}".format(lfu_lru_key))
                    del self.cache_data[lfu_lru_key]
                    self.keys_by_usage_order.remove(lfu_lru_key)
                    del self.keys_by_usage_frequency[lfu_lru_key]
                self.cache_data[key] = item
                self.keys_by_usage_order.append(key)
                self.keys_by_usage_frequency[key] = 1

    def get(self, key):
        """ Get an item from the cache by key
        And update the access/usage list

        Args:
            key: The key by which to fetch the value

        Returns:
            The value stored by the given key if the key exists
            in the cache. Otherwise, if key is None, or the key
            is not in the cache, returns None.
        """
        if key in self.keys_by_usage_order:
            self.keys_by_usage_order.remove(key)
            self.keys_by_usage_order.append(key)
            self.keys_by_usage_frequency[key] += 1
        return key and self.cache_data.get(key)
    
    def get_lfu_lru_key(self):
        """
        Gets the least frequently used item from the cache

        If more than two or more keys have the least frequency,
        returns the least frequently used one.
        """
        sorted_items = sorted([(val, key) for key, val in self.keys_by_usage_frequency.items()])
        lfu_keys = [sorted_items[0][1]]
        i = 1
        while i < len(sorted_items) and sorted_items[i][1] == lfu_keys[0]:
            lfu_keys.append(sorted_items[i][1])
            i += 1

        lfu_lru_key = lfu_keys[0]
        for key in lfu_keys:
            if self.keys_by_usage_order.index(key) < self.keys_by_usage_order.index(lfu_lru_key):
                lfu_lru_key = key
        return lfu_lru_key
