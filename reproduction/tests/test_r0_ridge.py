import tempfile
import unittest
from pathlib import Path

import numpy as np

from reproduction.r0_ridge import (
    Config,
    Trial,
    evaluate_ridge,
    make_trial_features,
    make_trial_folds,
)


class R0RidgeTests(unittest.TestCase):
    def test_history_windows_remain_inside_one_trial(self) -> None:
        spikes = np.arange(18, dtype=np.float32).reshape(6, 3)
        velocity = np.arange(12, dtype=np.float32).reshape(6, 2)
        features = make_trial_features(
            Trial(spikes=spikes, velocity=velocity),
            Config(n_lags=2, spike_count_power=1.0),
        )
        np.testing.assert_array_equal(features.x[0], spikes[:2].reshape(-1))
        np.testing.assert_array_equal(features.x[-1], spikes[3:5].reshape(-1))
        np.testing.assert_array_equal(features.y, velocity[2:])

    def test_fold_trial_ids_are_disjoint_and_complete(self) -> None:
        seen_test_ids: list[int] = []
        for train_ids, test_ids in make_trial_folds(n_trials=11, n_splits=5):
            self.assertEqual(np.intersect1d(train_ids, test_ids).size, 0)
            self.assertEqual(len(np.union1d(train_ids, test_ids)), 11)
            seen_test_ids.extend(int(i) for i in test_ids)
        self.assertEqual(sorted(seen_test_ids), list(range(11)))

    def test_small_synthetic_run_returns_finite_metrics(self) -> None:
        rng = np.random.default_rng(7)
        trials = []
        for _ in range(10):
            spikes = rng.poisson(0.2, size=(35, 4)).astype(np.float32)
            velocity = np.column_stack(
                (
                    0.8 * spikes[:, 0] - 0.3 * spikes[:, 1],
                    0.5 * spikes[:, 2] + 0.2 * spikes[:, 3],
                )
            ).astype(np.float32)
            trials.append(Trial(spikes=spikes, velocity=velocity))

        rows = evaluate_ridge(
            trials,
            Config(n_lags=2, spike_count_power=1.0, n_folds=5, gauss_sigma=0),
        )
        self.assertEqual(len(rows), 5)
        for row in rows:
            self.assertTrue(np.isfinite(row["r_mean"]))
            self.assertEqual(
                set(row["train_trial_ids"]).intersection(row["test_trial_ids"]), set()
            )

    def test_missing_data_exits_before_creating_results(self) -> None:
        from reproduction.r0_ridge import main

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "results"
            code = main(
                [
                    "--data",
                    str(Path(directory) / "missing.mat"),
                    "--output",
                    str(output),
                ]
            )
            self.assertEqual(code, 2)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
