import math
import sys
from fractions import Fraction
from typing import Set


def fib_greedy_expand(x: int, y: int) -> Set[int]:
    if x == 1:
        return {y}
    else:
        k: int = math.ceil(y/x)
        x_2: int = (-y) % x
        y_2: int = y*k
        return set.union({k}, fib_greedy_expand(x_2, y_2))


def brute_force(x, y):
    return brute_force_helper(Fraction(x, y), 1)

def brute_force_helper(num, term_count):
    if num.numerator == 1:
        return [num]
    else:
        expansion = mustapha(num, term_count)
        if expansion:
            return expansion
        else:
            return brute_force_helper(num, term_count + 1)

def mustapha(num, term_count):
    # if term_count == 4:
    #     exit()
    if num.numerator == 1:
        return [num]
    elif term_count == 1:
        return None

    denominator = 2
    while num - Fraction(1, denominator) <= 0: # ensure minimum denominator is
        denominator += 1
    min_denominator = denominator

    while num - sum([Fraction(1, i) for i in range(denominator, denominator + term_count)]) <= 0:
        denominator += 1
    max_denominator = denominator

    # print(min_denominator, max_denominator)

    for denominator in range(min_denominator, max_denominator+1):
        result = mustapha(num - Fraction(1, denominator), term_count - 1)
        if result:
            concatenated = [Fraction(1, denominator)]
            concatenated.append(result)
            return concatenated

    return None


if __name__ == '__main__':
    # if len(sys.argv[1:]) != 4:
    #     print("Usage: calc.py [start_x] [end_x] [start_y] [end_y]")
    sys.setrecursionlimit(1500)
    print(mustapha(Fraction(4, 17), 3))
    # fib_greedy_expand(4, 17) = {1233, 29, 5, 3039345}