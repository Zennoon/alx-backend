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
        rows = []
        if start < len(dataset) and end <= len(dataset):
            rows = dataset[start:end]
        return rows

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """
        Returns hypermedia representation
        """
        dataset = self.dataset()
        rows = self.get_page(page, page_size)
        max_page_num = math.ceil(len(dataset) // page_size)
        return {
            "page_size": page_size if page_size <= len(rows) else len(rows),
            "page": page,
            "data": rows,
            "next_page": page + 1 if page + 1 <= max_page_num else None,
            "prev_page": page - 1 if page - 1 else None,
            "total_pages": max_page_num
        }


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    A helper function for pagination that receives
    a page number and page size, and returns the start and end index
    for that page.

    Args:
        page (int): The page number
        page_size (int): The amount of records that can be displayed
        at a time

    Returns:
        (tuple): The start and end index for the records to be displayed
        on the page
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)

