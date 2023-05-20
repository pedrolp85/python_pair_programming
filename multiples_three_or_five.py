from utilities import timeit


@timeit
def sum_of_multiples(number) -> int:
    result = 0

    for i in range(number):
        if (i % 3 == 0) or (i % 5 == 0):
            result += i

    return result


def test_sum_of_multiples():
    assert sum_of_multiples(4) == 3
    assert sum_of_multiples(6) == 8
    assert sum_of_multiples(16) == 60
    assert sum_of_multiples(3) == 0
    assert sum_of_multiples(5) == 3
    assert sum_of_multiples(15) == 45
    assert sum_of_multiples(-5) == 0
