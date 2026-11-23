from cfl_data import family

def evaluate_w(lam, seed, ratio, family_name="S", include_x_bounds=True):
    inst = family(family_name, ratio=ratio, seed=seed)

    I = inst["I"]
    J = inst["J"]

    if lam is None:
        lam = {j: 0.0 for j in J}

    # Constant part of the Lagrangian
    w = sum(lam[j] * inst["d"][j] for j in J)

    # Store optimal allocations and opening decisions
    x_sol = {(i, j): 0.0 for i in I for j in J}
    y_sol = {}

    # Independent problem per facility
    for i in I:
        # Reduced costs
        reduced_costs = {j: inst["c"][i, j] - lam[j] for j in J}

        # Sort customers by increasing reduced cost
        order = sorted(J, key=lambda j: reduced_costs[j])

        remaining = inst["q"][i]
        transportation_cost = 0.0
        allocations = {}

        if include_x_bounds:
            # Continuous knapsack with upper bounds x_ij <= d_j
            for j in order:
                rc = reduced_costs[j]
                if rc >= 0:
                    break
                allocation = min(inst["d"][j], remaining)

                allocations[j] = allocation
                transportation_cost += rc * allocation

                remaining -= allocation

                if remaining <= 1e-9:
                    break

        else:
            # No upper bounds: allocate all capacity
            # to the customer with the smallest reduced cost
            j_best = order[0]

            if reduced_costs[j_best] < 0:
                allocations[j_best] = inst["q"][i]
                transportation_cost = (reduced_costs[j_best] * inst["q"][i])

        # Compare opening versus closing
        open_cost = inst["f"][i] + transportation_cost

        if open_cost < 0:
            y_sol[i] = 1
            w += open_cost
            for j, allocation in allocations.items():
                x_sol[i, j] = allocation
        else:
            y_sol[i] = 0
    return w, x_sol, y_sol


if __name__ == "__main__":
    # 2(a)-(c): with upper bounds
    w, x, y = evaluate_w(lam=None, seed=301, ratio=4, include_x_bounds=True)
    x_nonzero = {k: v for k, v in x.items() if v > 1e-9}
    y_open = {i: val for i, val in y.items() if val == 1}
    print("With x bounds w:", w, "x=", x_nonzero, "y=", y_open)

    # 2(d): without upper bounds
    w, x, y = evaluate_w(lam=None, seed=301, ratio=4, include_x_bounds=False)
    x_nonzero = {k: v for k, v in x.items() if v > 1e-9}
    y_open = {i: val for i, val in y.items() if val == 1}
    print("Without x bounds w:", w, "x=", x_nonzero, "y=", y_open)
