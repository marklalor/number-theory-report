import csv
import json

import sys
from fractions import Fraction
from typing import Set

from multiprocessing import Pool


def fib_greedy_expand(num: Fraction) -> Set[int]:
    if num.numerator == 1:
        return {num.denominator}
    else:
        k: int = (num.denominator//num.numerator)+1
        num2 = num - Fraction(1, k)
        # x_2: int = (-y) % x
        # y_2: int = y*k
        return set.union({k}, fib_greedy_expand(num2))


def brute_force(num: Fraction):
    return brute_force_helper(num, 1)


def brute_force_helper(num: Fraction, term_count: int):
    if num.numerator == 1:
        return {num.denominator}
    else:
        expansion = None
        while expansion is None:
            expansion = mustapha(num, term_count)
            term_count += 1
        return expansion


def mustapha(num: Fraction, term_count: int):
    if num.numerator == 1:
        return {num.denominator}
    elif term_count == 1:
        return None

    denominator = 2
    while num - Fraction(1, denominator) <= 0:
        denominator += 1
    min_denominator = denominator

    while num - sum([Fraction(1, i) for i in range(denominator, denominator + term_count)]) <= 0:
        denominator += 1
    max_denominator = denominator

    for denominator in range(min_denominator, max_denominator+1):
        solution = mustapha(num - Fraction(1, denominator), term_count - 1)
        if solution:
            return set.union({denominator}, solution)

    return None

def find_solutions(input):
    x, y = input
    fraction = Fraction(x, y)
    fib_solution = fib_greedy_expand(fraction)
    brute_force_solution = brute_force(fraction)

    if sum([Fraction(1, i) for i in fib_solution]) != fraction:
        raise ValueError("Fib solution " + str(fib_solution) + " is not equal to fraction " + str(fraction))
    if sum([Fraction(1, i) for i in brute_force_solution]) != fraction:
        raise ValueError("Brute solution " + str(fib_solution) + " is not equal to fraction " + str(fraction))

    return x, y, fib_solution, brute_force_solution

if __name__ == '__main__':
    if len(sys.argv[1:]) != 5:
        print("Usage: calc.py [start_x] [end_x] [start_y] [end_y] [threads]")
        sys.exit(0)

    start_x, end_x, start_y, end_y, threads = [int(arg) for arg in sys.argv[1:]]

    writer = csv.writer(sys.stdout, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    threadpool = Pool(threads)

    class SetEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, set):
                return list(obj)
            return json.JSONEncoder.default(self, obj)

    todo = []
    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            if x >= y:
                continue
            todo.append((x, y))

    for (x, y, fib_solution, brute_force_solution) in threadpool.imap_unordered(find_solutions, todo):

        writer.writerow([x,
                         y,
                         json.dumps(fib_solution, cls=SetEncoder, separators=(',', ':')),
                         json.dumps(brute_force_solution, cls=SetEncoder, separators=(',', ':'))])


