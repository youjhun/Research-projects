"""Clean R0 Ridge baseline for CRCNS pmd-1.

This module intentionally does one thing: estimate a Ridge velocity decoder with
trial-disjoint cross-validation.  It does not reuse the legacy concatenated
window/split implementation, because that implementation can place bins from a
held-out trial in the training set and can create history windows across trial
boundaries.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterator, Sequence

import numpy as np
import scipy
import scipy.io as sio
from scipy.ndimage import gaussian_filter1d
import sklearn
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold


LEGACY_CLAIM_R = 0.8701


@dataclass(frozen=True)
class Config:
    n_lags: int = 20
    spike_count_power: float = 1.3
    ridge_alpha: float = 1.0
    ridge_solver: str = "lsqr"
    ridge_tolerance: float = 1e-6
    n_folds: int = 5
    gauss_sigma: float = 3.0


@dataclass(frozen=True)
class Trial:
    spikes: np.ndarray
    velocity: np.ndarray


@dataclass(frozen=True)
class TrialFeatures:
    x: np.ndarray
    y: np.ndarray


def load_pmd1_trials(path: Path) -> list[Trial]:
    """Load M1+PMd spikes and x/y velocity while preserving trial boundaries."""
    mat = sio.loadmat(path, struct_as_record=False, squeeze_me=True)
    if "Data" not in mat:
        raise ValueError("MAT file does not contain the expected 'Data' variable")

    data = mat["Data"]
    required = ("kinematics", "neural_data_M1", "neural_data_PMd")
    missing = [name for name in required if not hasattr(data, name)]
    if missing:
        raise ValueError(f"Data is missing fields: {', '.join(missing)}")

    kinematics = np.atleast_1d(data.kinematics)
    m1_trials = np.atleast_1d(data.neural_data_M1)
    pmd_trials = np.atleast_1d(data.neural_data_PMd)
    if not (len(kinematics) == len(m1_trials) == len(pmd_trials)):
        raise ValueError("Kinematics, M1, and PMd have different trial counts")

    trials: list[Trial] = []
    for trial_id, (kin_raw, m1_raw, pmd_raw) in enumerate(
        zip(kinematics, m1_trials, pmd_trials)
    ):
        kin = np.asarray(kin_raw, dtype=np.float32)
        m1 = np.asarray(m1_raw, dtype=np.float32)
        pmd = np.asarray(pmd_raw, dtype=np.float32)
        if kin.ndim != 2 or kin.shape[1] < 4:
            raise ValueError(f"Trial {trial_id}: kinematics must have at least 4 columns")
        if m1.ndim != 2 or pmd.ndim != 2:
            raise ValueError(f"Trial {trial_id}: neural arrays must be two-dimensional")

        # Source arrays are channels x time; model input is time x channels.
        spikes = np.vstack((m1, pmd)).T
        velocity = kin[:, 2:4]
        if len(spikes) != len(velocity):
            raise ValueError(
                f"Trial {trial_id}: neural ({len(spikes)}) and kinematic "
                f"({len(velocity)}) lengths differ"
            )
        trials.append(Trial(spikes=spikes, velocity=velocity))

    if not trials:
        raise ValueError("Dataset contains no trials")
    return trials


def make_trial_features(trial: Trial, config: Config) -> TrialFeatures:
    """Create history features inside one trial; no window crosses a boundary."""
    spikes = np.asarray(trial.spikes, dtype=np.float32)
    velocity = np.asarray(trial.velocity, dtype=np.float32)
    if spikes.ndim != 2 or velocity.ndim != 2 or velocity.shape[1] != 2:
        raise ValueError("Expected spikes [time, channels] and velocity [time, 2]")
    if len(spikes) != len(velocity):
        raise ValueError("Spike and velocity lengths differ")
    if len(spikes) <= config.n_lags:
        raise ValueError(
            f"Trial length {len(spikes)} must exceed n_lags={config.n_lags}"
        )

    weighted = np.where(spikes > 0, np.power(spikes, config.spike_count_power), 0.0)
    weighted = np.asarray(weighted, dtype=np.float32, order="C")
    n_time, n_channels = weighted.shape
    shape = (n_time - config.n_lags, config.n_lags, n_channels)
    strides = (weighted.strides[0], weighted.strides[0], weighted.strides[1])
    windows = np.lib.stride_tricks.as_strided(
        weighted, shape=shape, strides=strides, writeable=False
    )
    x = windows.reshape(shape[0], -1).copy()
    y = velocity[config.n_lags :].copy()
    return TrialFeatures(x=x, y=y)


def make_trial_folds(n_trials: int, n_splits: int) -> Iterator[tuple[np.ndarray, np.ndarray]]:
    """Yield explicit, disjoint train/test trial identifiers."""
    if n_trials < n_splits:
        raise ValueError(f"Need at least {n_splits} trials, found {n_trials}")
    trial_ids = np.arange(n_trials)
    for train_ids, test_ids in KFold(n_splits=n_splits, shuffle=False).split(trial_ids):
        train_ids = trial_ids[train_ids]
        test_ids = trial_ids[test_ids]
        if np.intersect1d(train_ids, test_ids).size:
            raise RuntimeError("Train and test trial IDs overlap")
        yield train_ids, test_ids


def _stack(features: Sequence[TrialFeatures], ids: Sequence[int]) -> tuple[np.ndarray, np.ndarray]:
    x = np.concatenate([features[int(i)].x for i in ids], axis=0)
    y = np.concatenate([features[int(i)].y for i in ids], axis=0)
    return x, y


def _pearson(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float, float]:
    values: list[float] = []
    for dim in range(2):
        if np.std(y_true[:, dim]) == 0 or np.std(y_pred[:, dim]) == 0:
            values.append(float("nan"))
        else:
            values.append(float(np.corrcoef(y_true[:, dim], y_pred[:, dim])[0, 1]))
    return values[0], values[1], float(np.nanmean(values))


def _vaf(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    scores = []
    for dim in range(2):
        denominator = np.var(y_true[:, dim])
        score = float("nan") if denominator == 0 else 1.0 - np.var(
            y_true[:, dim] - y_pred[:, dim]
        ) / denominator
        scores.append(score)
    return float(np.nanmean(scores))


def evaluate_ridge(trials: Sequence[Trial], config: Config) -> list[dict[str, object]]:
    """Fit and evaluate one Ridge model per trial-disjoint fold."""
    features = [make_trial_features(trial, config) for trial in trials]
    rows: list[dict[str, object]] = []

    for fold, (train_ids, test_ids) in enumerate(
        make_trial_folds(len(features), config.n_folds), start=1
    ):
        x_train, y_train = _stack(features, train_ids)
        model = Ridge(
            alpha=config.ridge_alpha,
            solver=config.ridge_solver,
            tol=config.ridge_tolerance,
        )
        model.fit(x_train, y_train)

        test_true: list[np.ndarray] = []
        test_pred: list[np.ndarray] = []
        for trial_id in test_ids:
            feature = features[int(trial_id)]
            prediction = model.predict(feature.x)
            if config.gauss_sigma > 0:
                # Smooth inside each held-out trial, never across trial boundaries.
                prediction = gaussian_filter1d(
                    prediction, sigma=config.gauss_sigma, axis=0, mode="nearest"
                )
            test_true.append(feature.y)
            test_pred.append(prediction)

        y_true = np.concatenate(test_true, axis=0)
        y_pred = np.concatenate(test_pred, axis=0)
        r_x, r_y, r_mean = _pearson(y_true, y_pred)
        rows.append(
            {
                "fold": fold,
                "train_trials": len(train_ids),
                "test_trials": len(test_ids),
                "train_bins": len(y_train),
                "test_bins": len(y_true),
                "r_x": r_x,
                "r_y": r_y,
                "r_mean": r_mean,
                "vaf_mean": _vaf(y_true, y_pred),
                "train_trial_ids": [int(i) for i in train_ids],
                "test_trial_ids": [int(i) for i in test_ids],
            }
        )
    return rows


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_outputs(
    output_dir: Path,
    data_path: Path,
    trials: Sequence[Trial],
    config: Config,
    rows: Sequence[dict[str, object]],
    duration_seconds: float,
    data_sha256: str | None,
) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    scalar_fields = (
        "fold",
        "train_trials",
        "test_trials",
        "train_bins",
        "test_bins",
        "r_x",
        "r_y",
        "r_mean",
        "vaf_mean",
    )
    with (output_dir / "r0_folds.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=scalar_fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in scalar_fields})

    fold_r = np.asarray([float(row["r_mean"]) for row in rows])
    fold_vaf = np.asarray([float(row["vaf_mean"]) for row in rows])
    summary: dict[str, object] = {
        "schema_version": 1,
        "gate": "GREEN",
        "claim_status": "clean_trial_disjoint_result",
        "legacy_claim": {
            "r_mean": LEGACY_CLAIM_R,
            "status": "unverified; produced by the legacy pipeline",
            "comparison_rule": "Report the delta; do not force agreement.",
        },
        "result": {
            "r_mean": float(np.nanmean(fold_r)),
            "r_std_across_folds": float(np.nanstd(fold_r, ddof=1)),
            "vaf_mean": float(np.nanmean(fold_vaf)),
            "delta_from_legacy_r": float(np.nanmean(fold_r) - LEGACY_CLAIM_R),
        },
        "method": {
            "split_unit": "trial",
            "train_test_trial_overlap": False,
            "history_windows_cross_trials": False,
            "prediction_smoothing_crosses_trials": False,
            "affine_test_rescaling": False,
            "decoder": "sklearn.linear_model.Ridge",
            "config": asdict(config),
        },
        "data": {
            "path": str(data_path),
            "sha256": data_sha256,
            "trials": len(trials),
            "time_bins": int(sum(len(trial.spikes) for trial in trials)),
            "channels": int(trials[0].spikes.shape[1]),
        },
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "scikit_learn": sklearn.__version__,
        },
        "duration_seconds": duration_seconds,
        "folds": list(rows),
    }
    (output_dir / "r0_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True, help="Path to MM_S1_processed.mat")
    parser.add_argument("--output", type=Path, default=Path("results/r0"))
    parser.add_argument("--n-lags", type=int, default=20)
    parser.add_argument("--spike-count-power", type=float, default=1.3)
    parser.add_argument("--ridge-alpha", type=float, default=1.0)
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--gauss-sigma", type=float, default=3.0)
    parser.add_argument(
        "--max-trials",
        type=int,
        default=None,
        help="Use the first N trials for a smoke run; omit for the full result.",
    )
    parser.add_argument(
        "--hash-data",
        action="store_true",
        help="Record a SHA-256 of the input file (slower, but preferred for the final run).",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    data_path = args.data.expanduser().resolve()
    if not data_path.is_file():
        print(f"R0_GATE=BLOCKED data_file_not_found={data_path}", file=sys.stderr)
        print(
            "Upload MM_S1_processed.mat to Google Drive, then update DATA_PATH in the Colab notebook.",
            file=sys.stderr,
        )
        return 2

    config = Config(
        n_lags=args.n_lags,
        spike_count_power=args.spike_count_power,
        ridge_alpha=args.ridge_alpha,
        n_folds=args.folds,
        gauss_sigma=args.gauss_sigma,
    )
    started = time.perf_counter()
    trials = load_pmd1_trials(data_path)
    if args.max_trials is not None:
        if args.max_trials < config.n_folds:
            print("R0_GATE=BLOCKED max_trials must be at least the number of folds", file=sys.stderr)
            return 2
        trials = trials[: args.max_trials]
    rows = evaluate_ridge(trials, config)
    summary = _write_outputs(
        output_dir=args.output,
        data_path=data_path,
        trials=trials,
        config=config,
        rows=rows,
        duration_seconds=time.perf_counter() - started,
        data_sha256=_sha256(data_path) if args.hash_data else None,
    )
    result = summary["result"]
    assert isinstance(result, dict)
    print(
        "R0_GATE=GREEN "
        f"r_mean={result['r_mean']:.4f} "
        f"vaf_mean={result['vaf_mean']:.4f} "
        f"output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
