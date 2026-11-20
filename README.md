# IEOR 262A · Locating Capacitated Facilities

Team 3's Fall 2026 group project on capacitated facility location, Lagrangian bounds, and branch and bound. Our extension is Track C (modular capacity).

## Reproduce Part 1(a)

Activate `ieor262a` and run the following commands from the repository root. The first command reproduces the report example with the full solver log. The second reproduces [the saved Pyomo output for all nine team instances](part1a_results.txt).

```bash
python part1a.py --seed 301 --ratio 4 --solver-log
python part1a.py --seed 301 302 303 --ratio 2 4 8
```

The script solves the LP relaxation and the integer model for each formulation using Pyomo 6.10.1 and Gurobi 13.0.3, with `Presolve=0`, `Cuts=0`, and `Heuristics=0`. These are the Part 1(a) models before the strengthening in 1(b). LP exports are written to `instances/`. Site indices start at 0.

| Family S, ratio 4, seed 301 | LP objective | IP objective | LP gap as a share of IP | Optimal facilities |
| --- | ---: | ---: | ---: | --- |
| CFL | 40,480.69 | 49,932.72 | 18.93% | 5, 7, 9 |
| CFL-C | 34,970.51 | 49,932.72 | 29.96% | Small at 5, 7, 9 |

In the base LP, site 1 ships 258 units at an opening of $258/599\approx 0.4307$. The base IP closes that site. Track C uses fractional large facilities in the LP, but its integer solution on this instance uses only small ones. The reported LP gap is $(z_{\mathrm{IP}}-z_{\mathrm{LP}})/z_{\mathrm{IP}}$.

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

The setup test solves the base LP and IP for family S, capacity ratio 4, seed 1. It checks the reported values and site indices, demand satisfaction, capacity, nonnegative shipments, site domains, and the LP lower bound. The Part 1(a) test checks feasibility, recomputes opening and shipping costs, and checks the ordering of the LP and IP bounds for all nine assigned instances.

| Setup instance | LP objective | IP objective | Open sites (zero-based) |
| --- | ---: | ---: | --- |
| S, ratio 4, seed 1 | 42,533.67 | 49,226.88 | 3, 5, 12 |

For the assigned experiments, team $k$ uses seeds $100k+1$, $100k+2$, and $100k+3$ with ratios 2, 4, and 8. The starter script's main block currently selects family L. Running `python cfl_model.py` therefore starts a large solve. The small test above is independent of that default.

## Files

| File | Purpose |
| --- | --- |
| `cfl_data.py` | Course instance generator and extension data |
| `cfl_model.py` | Course Pyomo starter, LP export, Gurobi settings, and branching example |
| `part1a.py` | Runs both Part 1(a) formulations and prints objectives, site choices, and fractional openings |
| `tests/test_setup.py` | Reproduces the setup row in the report |
| `tests/test_part1a.py` | Checks the Part 1(a) solutions on Team 3's family S instances |
| `report/main.tex` | Single-file LaTeX report with Parts 1–3 and writing notes |

Compile from the repository root with `cd report` and `latexmk -pdf main.tex`, or upload `report/main.tex` to Overleaf.

## Course notation

The reference is Alper Atamtürk, *A Graduate Course in Mathematical Optimization*, November 17, 2026. Definition 5.1.4 uses $x_{ij}$ for the amount shipped from site $i$ to customer $j$, $y_i$ for a binary opening decision, $q_i$ for capacity, and $d_j$ for demand. The report follows this convention.

For Part 2, write the relaxed demand residual as $d_j-\sum_i x_{ij}$. Its multiplier is unrestricted because demand is an equality. See Proposition 4.8.3 for LP duality, Proposition 4.9.1 for the supergradient, and Remark 5.3.3 for the continuous knapsack rule. For Part 3, see Theorem 5.3.1 for pruning and Remark 5.3.5 for branching.

## Submission dates

Part 1 is due November 23 (three pages). Part 2 is due December 4 (three pages, including the Part 3 plan). The final report and repository are due December 11 (twelve pages plus appendices). As the team adds tables and figures, record the command for each here.
