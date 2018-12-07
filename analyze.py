import argparse
import csv
import json
from typing import Dict, Tuple, List

import numpy as np
from scipy.misc import imsave


def disparity_terms(l1,l2):
    return abs(len(l1) - len(l2))


def disparity_denominator(l1,l2):
    return abs(len(str(max(l1))) - len(str(max(l2))))


def do_pixel_terms(results: Dict[Tuple[int, int], Tuple[List[int], List[int]]]):
    do_pixel_graph(results, disparity_terms)


def do_pixel_denominator(results: Dict[Tuple[int, int], Tuple[List[int], List[int]]]):
    do_pixel_graph(results, disparity_denominator)


def do_pixel_graph(results: Dict[Tuple[int, int], Tuple[List[int], List[int]]], disparity_function):
    term_disparities = {key: disparity_function(*value) for key, value in results.items()}

    max_disparity = max(term_disparities.values())
    data = np.zeros((500, 500, 3), dtype=np.uint8)
    for i in range(0, 500):
        for j in range(0, 500):
            data[i, j] = 255

    color_step = 255/max_disparity

    greys = {i: 255 - color_step*i for i in range(0, max_disparity+1)}

    for point, disparity in term_disparities.items():
        x, y = point
        data[x-1, y-1] = greys[disparity]


    imsave(f'pixel_{disparity_function.__name__}.png', data)

def do_greedy_outliers(results: Dict[Tuple[int, int], Tuple[List[int], List[int]]]):
    term_disparities = {key: disparity_denominator(*value) for key, value in results.items()}

    max_disparity = max(term_disparities.values())

    top_results = sorted(term_disparities.items(), key=lambda x: -x[1])[:10]

    for point, disparity in top_results:
        print(f'{point}: {disparity}')

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
    parser.add_argument('actions', nargs='+', help='actions to perform')
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


