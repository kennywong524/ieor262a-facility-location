"""Check the Part 1(b) shipment bounds in the base and modular models."""

import unittest
from itertools import product

from cfl_data import family
from cfl_model import build_cfl, solve


class Part1bTest(unittest.TestCase):
    tolerance = 1e-5

    def test_report_counterexample(self):
        inst = {
            "I": [0], "J": [0], "d": [20], "q": [100], "q2": [200],
            "f": [10], "f2": [16], "c": {(0, 0): 0},
        }
        for modular in (False, True):
            with self.subTest(modular=modular):
                model = build_cfl(inst, relax=True, modular=modular, strengthened=True)
                model.x[0, 0].set_value(20)
                if modular:
                    model.s[0].set_value(0.2)
                    model.ell[0].set_value(0)
                    self.assertGreaterEqual(model.one_size[0].uslack(), 0)
                else:
                    model.y[0].set_value(0.2)
                self.assertAlmostEqual(model.demand[0].lslack(), 0)
                self.assertAlmostEqual(model.capacity[0].uslack(), 0)
                # Shipping 20 exceeds the limit of 4 by 16 units.
                self.assertAlmostEqual(model.shipment_bound[0, 0].uslack(), -16)
                if modular:
                    model.s[0].set_value(0)
                    model.ell[0].set_value(1)
                    self.assertAlmostEqual(model.shipment_bound[0, 0].uslack(), 0)

    def solve_lp_and_ip(self, inst, modular, *, strengthened):
        costs = []
        for relax in (True, False):
            model = build_cfl(inst, relax=relax, modular=modular, strengthened=strengthened)
            cost, _, _ = solve(model, require_optimal=True, MIPGap=0)
            costs.append(cost)
            if strengthened:
                self.assertEqual(len(model.shipment_bound), len(model.I) * len(model.J))
                for i in model.I:
                    opening = (model.s[i].value + model.ell[i].value
                               if modular else model.y[i].value)
                    for j in model.J:
                        limit = inst["d"][j] * opening
                        self.assertLessEqual(model.x[i, j].value, limit + self.tolerance)
        return costs

    def test_team_instances(self):
        for seed, ratio, modular in product((301, 302, 303), (2, 4, 8), (False, True)):
            with self.subTest(seed=seed, ratio=ratio, modular=modular):
                inst = family("S", ratio=ratio, seed=seed)
                weak_lp, weak_ip = self.solve_lp_and_ip(inst, modular, strengthened=False)
                strong_lp, strong_ip = self.solve_lp_and_ip(inst, modular, strengthened=True)
                self.assertLessEqual(weak_lp, strong_lp + self.tolerance)
                self.assertLessEqual(strong_lp, strong_ip + self.tolerance)
                self.assertAlmostEqual(weak_ip, strong_ip, delta=self.tolerance)


if __name__ == "__main__":
    unittest.main()
