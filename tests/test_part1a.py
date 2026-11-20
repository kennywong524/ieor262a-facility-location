"""Check the family S solutions in the Team 3 Part 1(a) results."""

import unittest
from itertools import product

from cfl_data import family
from cfl_model import build_cfl, solve


class Part1aTest(unittest.TestCase):
    tolerance = 1e-5

    def check_solution(self, inst, model, modular, relax, objective):
        shipping_cost = 0.0
        opening_cost = 0.0
        for j in model.J:
            received = sum(model.x[i, j].value for i in model.I)
            self.assertAlmostEqual(received, inst["d"][j], delta=self.tolerance)

        for i in model.I:
            if modular:
                small, large = model.s[i].value, model.ell[i].value
                self.assertLessEqual(small + large, 1 + self.tolerance)
            else:
                small, large = model.y[i].value, 0.0
            for amount in (small, large):
                self.assertGreaterEqual(amount, -self.tolerance)
                self.assertLessEqual(amount, 1 + self.tolerance)
                if not relax:
                    self.assertAlmostEqual(amount, round(amount), delta=self.tolerance)

            load = 0.0
            for j in model.J:
                quantity = model.x[i, j].value
                self.assertGreaterEqual(quantity, -self.tolerance)
                load += quantity
                shipping_cost += inst["c"][i, j] * quantity
            capacity = inst["q"][i] * small + inst["q2"][i] * large
            self.assertLessEqual(load, capacity + self.tolerance)
            opening_cost += inst["f"][i] * small + inst["f2"][i] * large
        self.assertAlmostEqual(opening_cost + shipping_cost, objective, delta=self.tolerance)

    def test_team_instances(self):
        for seed, ratio in product((301, 302, 303), (2, 4, 8)):
            with self.subTest(seed=seed, ratio=ratio):
                inst = family("S", ratio=ratio, seed=seed)
                values = {}
                for name, modular in (("CFL", False), ("CFL-C", True)):
                    for kind, relax in (("LP", True), ("IP", False)):
                        model = build_cfl(inst, relax=relax, modular=modular)
                        cost, _, _ = solve(model, require_optimal=True)
                        self.check_solution(inst, model, modular, relax, cost)
                        values[name, kind] = cost
                    self.assertLessEqual(values[name, "LP"], values[name, "IP"] + self.tolerance)
                for kind in ("LP", "IP"):
                    self.assertLessEqual(values["CFL-C", kind], values["CFL", kind] + self.tolerance)

                if (seed, ratio) == (301, 4):
                    self.assertAlmostEqual(values["CFL", "LP"], 40480.69, delta=0.005)
                    self.assertAlmostEqual(values["CFL-C", "LP"], 34970.51, delta=0.005)
                    for name in ("CFL", "CFL-C"):
                        self.assertAlmostEqual(values[name, "IP"], 49932.72, delta=0.005)


if __name__ == "__main__":
    unittest.main()
