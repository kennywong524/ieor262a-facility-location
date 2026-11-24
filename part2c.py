import numpy as np
from cfl_data import family
from part2a import evaluate_w
import matplotlib.pyplot as plt


def subgradient_method(seed, ratio, family_name="S",
                       max_iter=5000, alpha=10.0, tol=1e-6):

    # Load instance data
    inst = family(family_name, ratio=ratio, seed=seed)

    I = inst["I"]
    J = inst["J"]
    demand = inst["d"]

    # Initialize unrestricted multipliers
    lam = {j: 0.0 for j in J}

    # Best dual bound found
    best_w = -np.inf
    best_lam = None

    history = []

    for t in range(1, max_iter + 1):

        # Evaluate dual function and solve Lagrangian problem
        w, x, y = evaluate_w(
            lam,
            inst=inst,
            include_x_bounds=True
        )

        # Save best dual bound
        if w > best_w:
            best_w = w
            best_lam = lam.copy()

        history.append(w)

        # Calculate supergradient
        g = {
            j: demand[j] - sum(x[i, j] for i in I)
            for j in J
        }

        # Calculate norm
        norm_g = np.sqrt(sum(g[j]**2 for j in J))

        # Check stopping condition
        if all(abs(g[j]) <= tol for j in J):
            print(f"Converged at iteration {t}")
            break

        # Normalized supergradient
        direction = {
            j: g[j] / norm_g
            for j in J
        }

        # Step size
        theta = alpha / (t ** 0.5)

        # Update unrestricted multipliers
        for j in J:
            lam[j] += theta * direction[j]

    return best_w, best_lam, history

if __name__ == "__main__":

    for family_name in ["S", "L"]:

        best_w, best_lam, history = subgradient_method(
            seed=301,
            ratio=4,
            family_name=family_name,
            max_iter=5000,
            alpha=10.0,
            tol=1e-3
        )

        print(f"\nFamily {family_name}")
        print("Best dual bound:", best_w)
        print("Best multipliers:", best_lam)
        print("Final dual value:", history[-1])
        print("Iterations:", len(history))

        # Plot dual values
        plt.figure(figsize=(9, 5))
        plt.plot(history, label="Dual value")
        plt.axhline(
            y=best_w,
            color="red",
            linestyle="--",
            label=f"Best bound = {best_w:.2f}"
        )

        plt.xlabel("Iteration")
        plt.ylabel("w(lambda)")
        plt.title(f"Subgradient Method - Family {family_name}")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()