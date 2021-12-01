## The overall structure of our project:
- Definition of classes: 
We use the OOP principles, first define a base class called 
BaseSolver. Here we implements some common functions that will be used by the child classes, such as: read_data(read the input file and construct a distance matrix), init_trace(open a file to record trace), record_trace(write trace to .trace), write_solutin(write solution to .sol). Then we implement four solvers that inherits from the BaseSolver, which corresponds to the four algorithms that we use to solve the TSP problem: ApproxSolver(Prim based approximation), BnBSolver(Branch and Bound), LS1Solver(SA), LS2Solver(Hill Climbing).
- Main Function:
Main function is inside tsp_main.py, we use argparse package to parse the command line arguments. Then we choose the corresponding solver based on 'alg' argument, solve the problem by calling solve() and then get the output file.