#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Retrieves items from the dataset with delete resiliency

        Args:
            index (int): The start index from which to retrieve data
            page_size (int): Size of the page

        Returns:
            (dict): Dictionary containing hypermedia
        """
        dataset = self.indexed_dataset()
        idx = index
        assert (idx >= 0
                and idx < len(dataset))
        data: List[List] = []
        return_dict: Dict = {
            "index": index
        }
        while idx < len(dataset) and len(data) < page_size:
            if dataset.get(idx):
                data.append(dataset[idx])
            idx += 1
        return_dict.update({
            "data": data,
            "page_size": len(data),
            "next_index": idx if dataset.get(idx) else None
        })
        return return_dict
