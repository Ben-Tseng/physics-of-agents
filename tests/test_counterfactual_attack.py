import unittest

import numpy as np

from res_attack.counterfactual_attack import counts_at_budget, fitted_step


class CounterfactualAttackTest(unittest.TestCase):
    def setUp(self):
        self.fit = {
            "field": [1.0] + [0.0] * 15,
            "betas": {
                "beta_pos_T": 0.0,
                "beta_pos_F": 0.0,
                "beta_neg_T": 0.0,
                "beta_neg_F": 0.0,
                "beta_0": 0.0,
            },
        }
        self.phi = np.zeros((1, 2, 16))
        self.phi[:, :, 0] = 1.0
        self.J = np.zeros((1, 2, 2))
        self.s = np.ones((1, 2))
        self.tau = np.ones(1)
        self.draws = np.full((1, 2, 5), 0.5)

    def test_budget_counts_are_nested(self):
        targets = np.array([[[0, 1], [1, 2], [2, 2]]])
        np.testing.assert_array_equal(counts_at_budget(targets, 1, 3), [[1, 1, 0]])
        np.testing.assert_array_equal(counts_at_budget(targets, 2, 3), [[1, 2, 1]])

    def test_zero_weight_attack_has_no_effect(self):
        base = fitted_step(
            self.phi, self.J, self.s, self.tau, self.fit,
            np.zeros((1, 2)), 0.0, self.draws
        )
        dropped = fitted_step(
            self.phi, self.J, self.s, self.tau, self.fit,
            np.full((1, 2), 100.0), 0.0, self.draws
        )
        np.testing.assert_array_equal(base, dropped)

    def test_false_friend_pressure_can_reverse_spin(self):
        base = fitted_step(
            self.phi, self.J, self.s, self.tau, self.fit,
            np.zeros((1, 2)), 5.0, self.draws
        )
        attacked = fitted_step(
            self.phi, self.J, self.s, self.tau, self.fit,
            np.ones((1, 2)), 5.0, self.draws
        )
        np.testing.assert_array_equal(base, [[1, 1]])
        np.testing.assert_array_equal(attacked, [[-1, -1]])


if __name__ == "__main__":
    unittest.main()
