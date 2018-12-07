import argparse
import csv
import json
from typing import Dict, Tuple, List

import numpy as np
import pylab
from scipy.misc import imsave
import matplotlib.pyplot as plt


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


def do_greedy_outliers_denominators(results: Dict[Tuple[int, int], Tuple[List[int], List[int]]]):
    term_disparities = {key: disparity_denominator(*value) for key, value in results.items()}

    top_results = sorted(term_disparities.items(), key=lambda x: -x[1])[:10]

    for point, disparity in top_results:
        print(f'{point}: {disparity}')

def do_greedy_outliers_terms(results: Dict[Tuple[int, int], Tuple[List[int], List[int]]]):
    term_disparities = {key: disparity_terms(*value) for key, value in results.items()}

    top_results = sorted(term_disparities.items(), key=lambda x: -x[1])[:10]

    for point, disparity in top_results:
        print(f'{point}: {disparity}')

def do_percentage_same(results: Dict[Tuple[int, int], Tuple[List[int], List[int]]]):
    same = 0
    total = 0

    for point, results in results.items():
        greedy, brute = results
        if set(greedy) == set(brute):
            same += 1
        total += 1

    print(same/total)


def do_percentage_same_n(results: Dict[Tuple[int, int], Tuple[List[int], List[int]]]):
    n_max = max([t[0] for t in results.keys()])

    n_values = list(range(1, n_max+1))

    def percent_same(n):
        same = 0
        total = 0

        for point, items in results.items():
            if point[0] <= n and point[1] <= n:
                greedy, brute = items
                if set(greedy) == set(brute):
                    same += 1
                total += 1

        return same / total if total != 0 else 1

    percentage_values = [percent_same(n) for n in n_values]
    plt.rc('font', family='serif', size=13)
    plt.plot(np.array(n_values), np.array(percentage_values))
    plt.xlabel('$n$')
    # plt.title('Greedy/optimal equivalent expansions for $x,y \leq n$')
    plt.ylabel('Percentage Same')
    plt.ylim(0.7, 1.0)
    pylab.savefig('n_percent_graph.png')

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


