"""Solve the base and modular-capacity formulations for family S."""

import argparse
from itertools import product

from cfl_data import family
from cfl_model import GUROBI_SETTINGS, build_cfl, solve


def fractional_openings(variable):
    entries = []
    for i in variable:
        opening = variable[i].value
        if 1e-6 < opening < 1 - 1e-6:
            entries.append(f"{i}={opening:.4f}")
    return ", ".join(entries) or "none"


def run_instance(seed, ratio, solver_log=False, *, strengthened=False):
    inst = family("S", ratio=ratio, seed=seed)
    print(f"Family S | ratio {ratio} | seed {seed} | site IDs are zero-based")
    print("Gurobi options:", ", ".join(f"{k}={v}" for k, v in GUROBI_SETTINGS.items()))
    for name, modular in (("CFL", False), ("CFL-C", True)):
        if strengthened:
            name += "+"
        prefix = f"{name}_S_r{ratio}_s{seed}"
        lp = build_cfl(inst, relax=True, modular=modular, strengthened=strengthened)
        ip = build_cfl(inst, modular=modular, strengthened=strengthened)
        lp_value, _, _ = solve(lp, display=solver_log, lp_file=prefix + "_lp.lp", require_optimal=True)
        ip_value, _, _ = solve(ip, display=solver_log, lp_file=prefix + "_ip.lp", require_optimal=True)
        gap = (ip_value - lp_value) / ip_value
        print(f"\n{name}: LP = {lp_value:.2f}, IP = {ip_value:.2f}, LP gap = {gap:.2%}")
        if modular:
            print("IP small sites:", [i for i in ip.I if ip.s[i].value > 0.5])
            print("IP large sites:", [i for i in ip.I if ip.ell[i].value > 0.5])
            print("Fractional LP s:", fractional_openings(lp.s))
            print("Fractional LP ell:", fractional_openings(lp.ell))
        else:
            print("IP open sites:", [i for i in ip.I if ip.y[i].value > 0.5])
            print("Fractional LP y:", fractional_openings(lp.y))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, nargs="+", default=[301])
    parser.add_argument("--ratio", type=int, nargs="+", choices=(2, 4, 8), default=[4])
    parser.add_argument("--solver-log", action="store_true", help="Show Gurobi's full logs.")
    parser.add_argument("--strengthened", action="store_true",
                        help="Add the Part 1(b) shipment bounds to both formulations.")
    args = parser.parse_args()
    for index, (seed, ratio) in enumerate(product(args.seed, args.ratio)):
        if index:
            print()
        run_instance(seed, ratio, args.solver_log, strengthened=args.strengthened)


if __name__ == "__main__":
    main()
