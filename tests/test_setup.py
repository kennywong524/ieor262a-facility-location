"""Reproduce the family S setup row in the report with the course solver settings."""

import unittest

from cfl_data import family
from cfl_model import build_cfl, solve


class SetupInstanceTest(unittest.TestCase):
    def test_reported_solution(self):
        instance = family("S", ratio=4, seed=1)
        objectives = []
        tolerance = 1e-5

        for relaxed in (True, False):
            with self.subTest(relaxed=relaxed):
                model = build_cfl(instance, relax=relaxed)
                objective, _, _ = solve(model)
                objectives.append(objective)
                expected = 42533.67 if relaxed else 49226.88
                self.assertAlmostEqual(objective, expected, delta=0.005)

                for j in model.J:
                    received = sum(model.x[i, j].value for i in model.I)
                    self.assertAlmostEqual(received, instance["d"][j], delta=tolerance)
                for i in model.I:
                    opening = model.y[i].value
                    self.assertGreaterEqual(opening, -tolerance)
                    self.assertLessEqual(opening, 1 + tolerance)
                    if not relaxed:
                        self.assertAlmostEqual(opening, round(opening), delta=tolerance)
                    shipments = [model.x[i, j].value for j in model.J]
                    self.assertGreaterEqual(min(shipments), -tolerance)
                    self.assertLessEqual(sum(shipments), instance["q"][i] * opening + tolerance)

                if not relaxed:
                    open_sites = [i for i in model.I if model.y[i].value > 0.5]
                    self.assertEqual(open_sites, [3, 5, 12])

        if len(objectives) == 2:
            self.assertLessEqual(objectives[0], objectives[1] + tolerance)


if __name__ == "__main__":
    unittest.main()
