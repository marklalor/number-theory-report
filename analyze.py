import argparse
import csv
import json
import sys
from typing import Set, Dict, Tuple, List


def disparity_terms(l1,l2):
    return abs(len(l1) - len(l2))

def disparity_denominator(l1,l2):
    return max(l1) - max(l2)

def do_pixel_terms(results: Dict[Tuple[int, int], Tuple[List[int], List[int]]]):
    pass

def do_constant_disp(results: Dict[Tuple[int, int], Tuple[List[int], List[int]]]):
    sums = {}
    for y in range(2, 501):
        for x in range(1, y):
            result = results[(x, y)]
            if x not in sums:
                sums[x] = 0
            sums[x] += disparity_terms(result[0], result[1])

    for key in sums:
        sums[key] /= 499

    print(sums)
    exit()



if __name__ == '__main__':
    # if len(sys.argv[1:]) == 0:
    #     print("Usage: analyze.py [results_file] [image|]")

    # result_file = sys.argv[1]
    # actions = sys.argv[2:]


    parser = argparse.ArgumentParser(description='Make some graphs')
    parser.add_argument('result_file')
    parser.add_argument('actions', nargs='+', choices={'pixel_terms', 'pixel_denominators', 'constant_disp'}, help='actions to perform')
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


