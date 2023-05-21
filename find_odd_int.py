from collections import Counter
from collections import defaultdict
from typing import List

import pytest

from utilities import get_random_list
from utilities import timeit


@timeit
def find_odd_int_default_dict(input_ints: List) -> int:
    d = defaultdict(int)
    for integer in input_ints:
        d[integer] += 1

    for k, v in d.items():
        if v % 2 == 1:
            return k


@timeit
def find_odd_int_counter(input_ints: List) -> int:
    counter = Counter(input_ints)
    for item, count in counter.items():
        if count % 2 == 1:
            return int(item)


@pytest.mark.parametrize(
    "input_list, result",
    [
        (get_random_list(min_value=5, max_value=5) + [7, 7, 7], 7),
        (
            get_random_list(min_value=5, max_value=5)
            + get_random_list(min_value=8, max_value=8)
            + [99],
            99,
        ),
    ],
    ids=["case_1", "case_2"],
)
def test_find_odd_int(input_list, result):
    assert find_odd_int_default_dict(input_list) == result


@pytest.mark.parametrize(
    "input_list, result",
    [
        (get_random_list(min_value=5, max_value=5) + [7, 7, 7], 7),
        (
            get_random_list(min_value=5, max_value=5)
            + get_random_list(min_value=8, max_value=8)
            + [99],
            99,
        ),
    ],
    ids=["case_1", "case_2"],
)
def test_find_odd_counter(input_list, result):
    assert find_odd_int_counter(input_list) == result
