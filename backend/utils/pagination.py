"""
Pagination calculation and normalization helpers.
"""

import math
from typing import Tuple


def normalize_pagination_params(page: int = 1, per_page: int = 20) -> Tuple[int, int]:
    """
    Normalizes page and per_page parameters.
    - page: minimum 1
    - per_page: between 1 and 100
    """
    norm_page = max(1, page)
    norm_per_page = max(1, min(100, per_page))
    return norm_page, norm_per_page


def calculate_offset(page: int, per_page: int) -> int:
    """Calculates SQL query offset from 1-indexed page and per_page."""
    norm_page, norm_per_page = normalize_pagination_params(page, per_page)
    return (norm_page - 1) * norm_per_page


def calculate_total_pages(total: int, per_page: int) -> int:
    """Calculates total pages using ceiling division."""
    if total <= 0:
        return 0
    _, norm_per_page = normalize_pagination_params(1, per_page)
    return math.ceil(total / norm_per_page)
