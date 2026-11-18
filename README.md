# IEOR 262A · Locating Capacitated Facilities

Fall 2026 group project on capacitated facility location, Lagrangian bounds, and branch and bound. The repository starts with the course-supplied Pyomo model and instance generator. The team number and extension track are still open.

## Reproduce the setup run

From the repository root, activate the Conda environment you used for the project. The tested setup on Kenny's Mac used Python 3.12, Pyomo 6.10.1, and Gurobi 13.0.3.

```bash
conda activate ieor262a
python -m unittest discover -s tests -v
```

On a new computer, create the environment first and activate the machine's own Gurobi academic license.

```bash
conda create -n ieor262a -c gurobi python=3.12 gurobi=13.0.3
conda activate ieor262a
python -m pip install pyomo==6.10.1
```

The test solves the base LP and IP for family S, capacity ratio 4, seed 1. It checks the reported values and site indices, demand satisfaction, capacity, nonnegative shipments, site domains, and the LP lower bound.

| Setup instance | LP objective | IP objective | Open sites (zero-based) |
| --- | ---: | ---: | --- |
| S, ratio 4, seed 1 | 42,533.67 | 49,226.88 | 3, 5, 12 |

For the assigned experiments, team $k$ uses seeds $100k+1$, $100k+2$, and $100k+3$ with ratios 2, 4, and 8. The starter script's main block currently selects family L. Running `python cfl_model.py` therefore starts a large solve. The small test above is independent of that default.

## Files

| File | Purpose |
| --- | --- |
| `cfl_data.py` | Course instance generator and extension data |
| `cfl_model.py` | Course Pyomo starter, LP export, Gurobi settings, and branching example |
| `tests/test_setup.py` | Reproduces the setup row in the report |
| `report/main.tex` | Single-file LaTeX report with Parts 1–3 and writing notes |

Compile from the repository root with `cd report` and `latexmk -pdf main.tex`, or upload `report/main.tex` to Overleaf.

## Course notation

The reference is Alper Atamtürk, *A Graduate Course in Mathematical Optimization*, November 17, 2026. Definition 5.1.4 uses $x_{ij}$ for the amount shipped from site $i$ to customer $j$, $y_i$ for a binary opening decision, $q_i$ for capacity, and $d_j$ for demand. The report follows this convention.

For Part 2, write the relaxed demand residual as $d_j-\sum_i x_{ij}$. Its multiplier is unrestricted because demand is an equality. See Proposition 4.8.3 for LP duality, Proposition 4.9.1 for the supergradient, and Remark 5.3.3 for the continuous knapsack rule. For Part 3, see Theorem 5.3.1 for pruning and Remark 5.3.5 for branching.

## Submission dates

Part 1 is due November 23 (three pages). Part 2 is due December 4 (three pages, including the Part 3 plan). The final report and repository are due December 11 (twelve pages plus appendices). As the team adds tables and figures, record the command for each here.
