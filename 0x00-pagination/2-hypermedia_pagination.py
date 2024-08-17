#!/usr/bin/env python3
"""
Contains:
    Classes
    =======
    Server - Mock server that hosts a dataset and is able to
    service requests for that dataset with pagination and a method
    that offers hypermedia pagination

    Functions
    =========
    index_range - Helper function that receives page number and
    page size and returns the appropriate range if indexes to return
    from the dataset
"""
import csv
import math
from typing import List, Mapping, Tuple

index_range = __import__('0-simple_helper_function').index_range


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Receives a page number and the page size and returns the appropriate
        page from the dataset (correct list of rows)

        Args:
            page (int): The page number to retrieve
            page_size (int): THe number of records / rows of the dataset
            to be returned at a time

        Returns:
            (list): The appropriate rows of the dataset corresponding to given
            pagination parameters
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        dataset = self.dataset()
        start, end = index_range(page, page_size)
        try:
            data = dataset[start:end]
        except IndexError:
            data = []
        return data

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """
        Returns hypermedia representation
        """
        dataset = self.dataset()
        rows = self.get_page(page, page_size)
        max_page_num = len(dataset) // page_size + 1
        return {
            "page_size": page_size if page_size <= len(rows) else len(rows),
            "page": page,
            "data": rows,
            "next_page": page + 1 if page + 1 <= max_page_num else None,
            "prev_page": page - 1 if page - 1 else None,
            "total_pages": max_page_num
        }
