import math
import sys
from typing import Set


def fib_greedy_expand(x: int, y: int) -> Set[int]:
    if x == 1:
        return {y}
    else:
        k: int = math.ceil(y/x)
        x_2: int = (-y) % x
        y_2: int = y*k
        return set.union({k}, fib_greedy_expand(x_2, y_2))


if __name__ == '__main__':
    if len(sys.argv[1:]) != 4:
        print("Usage: calc.py [start_x] [end_x] [start_y] [end_y]")

    # fib_greedy_expand(4, 17) = {1233, 29, 5, 3039345}