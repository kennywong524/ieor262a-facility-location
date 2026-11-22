from cfl_data import family
from cfl_model import GUROBI_SETTINGS, build_cfl, solve


def evaluate_w(lam, seed, ratio):
    """
    Evaluate the Lagrangian dual function w(lambda)
    for the Capacitated Facility Location Problem.

    Parameters
    ----------
    lam : dict
        Lagrangian multipliers, indexed by customer j.
    inst : dict
        Problem instance containing I, J, f, c, d and q.

    Returns
    -------
    float
        Value of the Lagrangian dual function.
    """

    inst = family("S", ratio=ratio, seed=seed)
    I = inst['I']
    J = inst['J']

    if lam is None:
        lam = {j: 1.0 for j in J} # this is arbitrary right now, vector of 1's

    # Constant part of the Lagrangian
    w = sum(lam[j] * inst['d'][j] for j in J)

    # Solve one independent problem per facility
    for i in I:
        # Sort customers by increasing reduced cost
        order = sorted(J, key=lambda j: inst['c'][i, j] - lam[j])
        remaining = inst['q'][i] # initialize
        transportation_cost = 0.0 # intitialize

        # Greedy continuous knapsack
        for j in order:
            reduced_cost = inst['c'][i, j] - lam[j]

            # Stop when reduced costs become nonnegative
            if reduced_cost >= 0:
                break

            # Allocate as much as possible
            x = min(inst['d'][j], remaining)
            transportation_cost += reduced_cost * x
            remaining -= x

            if remaining <= 0:
                break
        # Compare opening and closing the facility
        open_cost = inst['f'][i] + transportation_cost
        w += min(0, open_cost)

    return w

if __name__ == "__main__":
    print(evaluate_w(None, seed=301, ratio=4))
