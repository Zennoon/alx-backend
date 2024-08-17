#!/usr/bin/env python3
"""
Contains:
    Functions
    =========
    index_range - A helper function for pagination that receives
    a page number and page size, and returns the start and end index
    for that page
"""
from typing import Tuple


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
