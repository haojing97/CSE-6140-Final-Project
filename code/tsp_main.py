import argparse
import os

from ApproxSolver import ApproxSolver
from BnBSolver import BnBSolver
from LS1Solver import LS1Solver
from LS2Solver import LS2Solver


def get_filename(args):
    filename = '{}_{}_{}'.format(os.path.basename(
        args.inst).split()[0], args.alg, args.time)
    if args.seed:
        filename += '_{}'.format(args.seed)
    return filename


def get_solver(alg):
    # get solver by algorithm
    if alg == 'BnB':
        return BnBSolver()
    elif alg == 'Approx':
        return ApproxSolver()
    elif alg == 'LS1':
        return LS1Solver()
    else:
        return LS2Solver()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-alg', help='the method to use, BnB is branch and bound, Approx is approximation algorithm, LS1 is the first local search algorithm, and LS2 is the second local search algorithm.',
                        choices=['BnB', 'Approx', 'LS1', 'LS2'], required=True)
    parser.add_argument(
        '-inst', help='the filepath of a single input instance.', required=True)
    parser.add_argument(
        '-time', help='the cut-off time in seconds.', type=int, required=True)
    parser.add_argument('-seed', help='the random seed.')
    args = parser.parse_args()

    solver = get_solver(args.alg)
    solver.read_data(args.inst)
    solver.init_trace('output/' + get_filename(args) + '.trace')
    solver.solve(args.time, args.seed)
    solver.write_solution('output/' + get_filename(args) + '.sol')
