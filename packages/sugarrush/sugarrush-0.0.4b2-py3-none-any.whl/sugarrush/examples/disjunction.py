from sugarrush.utils import power_set
from sugarrush.solver import SugarRush

def power_set_literals(lits):
    """
        For a set of literals, enumerate all true/false assignments
    """
    for subset in power_set(lits):
        yield [lit if lit in subset else -lit for lit in lits]

def sum_test(solver, variables):
    """
        For a set of variables, test all possible boolean assignments,
        and check which of the sums can be found in satisfying assignments. 
    """
    satisfying_assignments = []
    unsatisfying_assignments = []
    for lits in power_set_literals(variables):
        res = solver.solve(assumptions=lits)
        bin_lits = [1 if lit > 0 else 0 for lit in lits]
        if res:
            satisfying_assignments.append(tuple(bin_lits))
        else:
            unsatisfying_assignments.append(tuple(bin_lits))

    print("Satisfying assignments:")
    #[print(lits) for lits in sorted(satisfying_assignments)]
    print(set([sum(lits) for lits in satisfying_assignments]))
    print()
    #print("False positives:")
    #[print(lits) for lits in sorted(satisfying_assignments) if sum(lits[:3]) < 2]
    
    print("Unsatisfying assignments:")
    print(set([sum(lits) for lits in unsatisfying_assignments]))
    #[print(lits) for lits in sorted(unsatisfying_assignments)]

def negate_test():
    n = 3
    solver = SugarRush()
    X = [solver.var() for _ in range(n)]
    bound_X = solver.atmost(X, bound=2)
    bound_X_neg = solver.negate(bound_X)
    solver.add(bound_X_neg)
    sum_test(solver, list(sorted(solver.lits - set([0]))))
    
def run_disjunction():
    """
        CNF that is satisfiable if and only if the sum of the variables is even.
        Created by transforming a set of sum({x})==k - CNF's into an equivalent CNF.
        See: https://garageofcode.blogspot.com/2019/02/sat-parity-board.html
    """
    print(run_disjunction.__doc__)
    n = 9
    solver = SugarRush()
    X = [solver.var() for _ in range(n)]

    bounds_even = [solver.equals(X, k) for k in range(0, n+1, 2)]
    bound = solver.disjunction(bounds_even)

    solver.add(bound)
    sum_test(solver, X)

    ''' successful test
    bound_X_1 = solver.equals(X, bound=0)
    bound_X_2 = solver.equals(X, bound=3)
    bound_X_1or2 = solver.disjunction([bound_X_1, bound_X_2])
    print(bound_X_1)
    print()
    print(bound_X_2)
    print()
    print(bound_X_1or2)
    print()
    solver.add(bound_X_1or2)

    sum_test(solver, X)
    '''

if __name__ == '__main__':
    run_disjunction()