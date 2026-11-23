# IEOR 262A: Locating Capacitated Facilities Course Project

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

## Reproduce Part 1(b)

The `--strengthened` option adds a shipment bound for every site $i$ and customer $j$. CFL+ uses $x_{ij}\le d_j y_i$. Track C uses $x_{ij}\le d_j(s_i+\ell_i)$. The option applies to both the LP relaxation and the integer model.

```bash
python part1a.py --strengthened --seed 301 --ratio 4
python -m unittest discover -s tests -v
```

For this instance, the strengthened LP objectives are 48,696.70 for CFL+ and 48,538.06 for CFL-C+. Both integer objectives are 49,932.72.

## Files

| File | Purpose |
| --- | --- |
| `cfl_data.py` | Course instance generator and extension data |
| `cfl_model.py` | Course Pyomo starter, LP export, Gurobi settings, and branching example |
| `part1a.py` | Runs the Part 1(a) or strengthened Part 1(b) models and prints objectives and site choices |
| `tests/test_setup.py` | Reproduces the setup row in the report |
| `tests/test_part1a.py` | Checks the Part 1(a) solutions on Team 3's family S instances |
| `tests/test_part1b.py` | Checks the fractional counterexample, shipment bounds, and integer objectives on all nine Team 3 instances |
| `report/main.tex` | Single-file LaTeX report with Parts 1–3 and writing notes |

Compile from the repository root with `cd report` and `latexmk -pdf main.tex`, or upload `report/main.tex` to Overleaf.

## Submission dates (reminder)

Part 1 is due November 23 (three pages). Part 2 is due December 4 (three pages, including the Part 3 plan). The final report and repository are due December 11 (twelve pages plus appendices).
