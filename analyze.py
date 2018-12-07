import argparse
import csv
import json
import sys
from typing import Set, Dict, Tuple


class Result:
    def __init__(self, x: int, y: int, fib: Set[int], brute: Set[int]):
        self.x = x
        self.y = y
        self.fib = fib
        self.brute = brute


def do_pixel_terms(results: Dict[Tuple[int, int], Result]):
    pass


if __name__ == '__main__':
    # if len(sys.argv[1:]) == 0:
    #     print("Usage: analyze.py [results_file] [image|]")

    # result_file = sys.argv[1]
    # actions = sys.argv[2:]


    parser = argparse.ArgumentParser(description='Make some graphs')
    parser.add_argument('result_file')
    parser.add_argument('actions', nargs='+', choices={'pixel_terms', 'pixel_denominators'}, help='actions to perform')
    args = parser.parse_args()

    mapping = dict()

    with open(args.result_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            x_raw, y_raw, greedy_raw, brute_raw = row
            x = int(x_raw)
            y = int(y_raw)
            greedy = json.loads(greedy_raw)
            brute = json.loads(brute_raw)

            mapping[(x, y)] = (greedy, brute)

    for action in args.actions:
        print(f'Running {action} action:')
        method_to_call = globals()[f'do_{action}'](mapping)
        print(f'Finished {action} action!')
        print()


