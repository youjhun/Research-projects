# -*- coding: utf-8 -*-
"""
Event-driven BCI Decoding — Integrated Analysis
: NEP Lab / Lab contact report
자율연구PY (군대 연구)
연구1: spike_train augmentation quality gate (VAE 전 단계)
연구2: Ridge/MLP/LSTM/Transformer SER robustness + attention 분석

의존:
- torch, numpy, scipy, matplotlib, scikit-learn
- Colab 기준: /content/drive/MyDrive/data_and_scripts/source_data/processed/MM_S1_processed.mat
"""

from __future__ import annotations

import copy
import os
import time
import warnings
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import torch
import torch.nn as nn
import torch.optim as optim
from scipy.ndimage import gaussian_filter1d
from scipy.stats import pearsonr
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold
from torch.utils.data import DataLoader, TensorDataset

warnings.filterwarnings("ignore")


# =========================================================
# Config
# =========================================================

@dataclass(frozen=True)
class Cfg:
    data_path: str = "/content/drive/MyDrive/data_and_scripts/source_data/processed/MM_S1_processed.mat"
    n_lags: int = 20
    burst_power: float = 1.3
    ridge_alpha: float = 1.0
    n_folds: int = 5
    gauss_sigma: int = 3
    pca_components: int = 128
    mlp_hidden: Tuple[int, int, int] = (512, 256, 128)
    mlp_alpha: float = 1e-4
    mlp_epochs: int = 60
    batch_size: int = 4096
    lr: float = 1e-3
    lstm_hidden: int = 128
    lstm_layers: int = 2
    lstm_dropout: float = 0.2
    lstm_epochs: int = 80
    kalman_iter: int = 150
    # SER baseline sweep
    ser_values: Tuple[float, ...] = (0, 1e-4, 1e-3, 1e-2, 1e-1, 2e-1)
    n_repeats: int = 3
    # Burst SER sweep
    ser_burst_values: Tuple[float, ...] = (0, 1e-4, 1e-3, 1e-2, 1e-1, 2e-1)
    # VAE augmentation stage
    vae_low_data_trials: int = 100
    vae_gen_ratios: Tuple[int, ...] = (0, 1, 3, 9)
    paper_r_neural: float = 0.9324
    paper_ser_points = {1e-4: 1.000, 1e-3: 0.888, 1e-2: 0.700}
    decoder_names = ("Ridge", "MLP", "LSTM", "Kalman")
    device: str = "cuda" if torch.cuda.is_available() else "cpu"


CFG = Cfg()
DEVICE = torch.device(CFG.device)

DECODER_COLORS = {"Ridge": "royalblue", "MLP": "darkorange", "LSTM": "forestgreen", "Kalman": "orchid"}
DECODER_MARKERS = {"Ridge": "o", "MLP": "s", "LSTM": "^", "Kalman": "D"}


# =========================================================
# Loader
# =========================================================

def load_pmd1(path: str = CFG.data_path) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return (X, Vx, Vy, trial_cumlen)."""
    mat = sio.loadmat(path, struct_as_record=False, squeeze_me=True)
    Data = mat["Data"]
    n_reaches = len(Data.kinematics)
    spikes, vx, vy = [], [], []
    for i in range(n_reaches):
        kin = Data.kinematics[i]
        m1 = Data.neural_data_M1[i]
        pmd = Data.neural_data_PMd[i]
        neural = np.vstack([m1, pmd])
        spikes.append(neural.T)
        vx.append(kin[:, 2])
        vy.append(kin[:, 3])
    X = np.vstack(spikes)
    Vx = np.concatenate(vx)
    Vy = np.concatenate(vy)
    trial_cumlen = np.cumsum([len(s) for s in spikes])
    return X, Vx, Vy, trial_cumlen


# =========================================================
# Features
# =========================================================

def create_lagged_features(X_raw: np.ndarray, Y_vx: np.ndarray, Y_vy: np.ndarray,
                           num_lags: int = CFG.n_lags) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    N, D = X_raw.shape
    shape = (N - num_lags, num_lags, D)
    strides = (X_raw.strides[0], X_raw.strides[0], X_raw.strides[1])
    X_view = np.lib.stride_tricks.as_strided(X_raw, shape=shape, strides=strides)
    X_lag = X_view.reshape(N - num_lags, -1).astype(np.float32)
    return X_lag, Y_vx[num_lags:].astype(np.float32), Y_vy[num_lags:].astype(np.float32)


def create_sequential_features(X_raw: np.ndarray, num_lags: int = CFG.n_lags) -> np.ndarray:
    N, D = X_raw.shape
    shape = (N - num_lags, num_lags, D)
    strides = (X_raw.strides[0], X_raw.strides[0], X_raw.strides[1])
    return np.lib.stride_tricks.as_strided(X_raw, shape=shape, strides=strides).copy().astype(np.float32)


def get_kalman_obs(X_raw: np.ndarray, num_lags: int = CFG.n_lags) -> np.ndarray:
    return X_raw[num_lags:, :].astype(np.float32)


def apply_dynamic_weighting(X_feat: np.ndarray, burst_power: float = CFG.burst_power) -> np.ndarray:
    return np.where(X_feat > 0, np.power(X_feat, burst_power), 0.0)


def apply_SER_random(spike_matrix: np.ndarray, ser: float, rng: Optional[np.random.Generator] = None) -> np.ndarray:
    if rng is None:
        rng = np.random.default_rng()
    corrupted = spike_matrix.copy().astype(float)
    half_ser = ser / 2.0
    spike_idx = np.argwhere(corrupted > 0)
    zero_idx = np.argwhere(corrupted == 0)
    if len(spike_idx) > 0 and half_ser > 0:
        n_miss = int(round(len(spike_idx) * half_ser))
        if n_miss > 0:
            chosen = rng.choice(len(spike_idx), size=n_miss, replace=False)
            corrupted[spike_idx[chosen, 0], spike_idx[chosen, 1]] = 0
    if len(zero_idx) > 0 and half_ser > 0:
        n_false = int(round(int(np.sum(spike_matrix > 0)) * half_ser))
        n_false = min(n_false, len(zero_idx))
        if n_false > 0:
            chosen = rng.choice(len(zero_idx), size=n_false, replace=False)
            corrupted[zero_idx[chosen, 0], zero_idx[chosen, 1]] = 1
    return corrupted


def apply_SER_burst(spike_matrix: np.ndarray, ser: float,
                    burst_width: int = 4,
                    seed: Optional[int] = None) -> np.ndarray:
    """
    Electrode-failure burst noise model.
    - ser defines corrupted trials fraction per call.
    - In each corrupted trial, first 20ms windows are randomly turned into
      burst-up or burst-down events.
    """
    rng = np.random.default_rng(seed)
    corrupted = spike_matrix.copy().astype(float)
    if ser <= 0:
        return corrupted
    n_trials = 20  # 97 bins / 20ms window ~5 windows per trial
    corrupt_prob = min(ser, 1.0)
    n_corrupt = int(round(n_trials * corrupt_prob))
    n_corrupt = max(1, n_corrupt)
    chosen = rng.choice(n_trials, size=n_corrupt, replace=False)
    for t in chosen:
        start = t * 20
        end = min(start + burst_width, corrupted.shape[0])
        rng.shuffle(corrupted[start:end, :])
    return corrupted


def create_peak_aware_features(X_raw: np.ndarray, Y_vx: np.ndarray, Y_vy: np.ndarray,
                               num_lags: int = CFG.n_lags,
                               pca_components: int = CFG.pca_components) -> Tuple[np.ndarray, np.ndarray]:
    X_lag, vx_lag, vy_lag = create_lagged_features(X_raw, Y_vx, Y_vy, num_lags)
    N, D = X_lag.shape
    n_neurons = X_raw.shape[1]
    # PCA disabled in current pipeline for leakage safety, keep shape compat
    peak_features = np.zeros((N, 5), dtype=np.float32)
    return X_lag.astype(np.float32), peak_features, vx_lag, vy_lag


def evaluate_decoding(y_true: np.ndarray, y_pred: np.ndarray,
                      do_rescale: bool = True) -> Dict[str, float]:
    r_pearson, _ = pearsonr(y_true, y_pred)
    vaf = float(1 - np.var(y_true - y_pred) / np.var(y_true))
    rmse = float(np.sqrt(np.mean((y_true - y_pred) ** 2)))
    scale_bias = float(np.std(y_pred) / np.std(y_true))
    r_display = r_pearson
    if do_rescale:
        a_num = np.sum((y_pred - y_pred.mean()) * (y_true - y_true.mean()))
        a_den = np.sum((y_pred - y_pred.mean()) ** 2) + 1e-12
        a = a_num / a_den
        b = y_true.mean() - a * y_pred.mean()
        y_pred_r = a * y_pred + b
        r_display, _ = pearsonr(y_true, y_pred_r)
    return {
        "r_raw": float(r_pearson),
        "r": float(r_display),
        "vaf": vaf,
        "rmse": rmse,
        "scale_bias": scale_bias,
    }


# =========================================================
# Trial-aware split
# =========================================================

def make_trial_folds(trial_cumlen: np.ndarray, n_folds: int = CFG.n_folds) -> List[Tuple[np.ndarray, np.ndarray]]:
    trial_ids = np.arange(len(trial_cumlen))
    kf = KFold(n_splits=n_folds, shuffle=False)
    folds = []
    for tr_idx, te_idx in kf.split(trial_ids):
        train_bins = np.arange(0, trial_cumlen[tr_idx[-1]])
        test_start = trial_cumlen[tr_idx[-1]] if tr_idx[-1] < len(trial_cumlen) else trial_cumlen[tr_idx[-2]]
        test_bins = np.arange(trial_cumlen[te_idx[0] - 1] if te_idx[0] > 0 else 0, trial_cumlen[te_idx[-1]])
        folds.append((train_bins, test_bins))
    return folds


# =========================================================
# Models
# =========================================================

def fit_ridge_gpu(X_tr: torch.Tensor, Y_tr: torch.Tensor, alpha: float = CFG.ridge_alpha) -> torch.Tensor:
    N, D = X_tr.shape
    A = torch.matmul(X_tr.T, X_tr) + alpha * torch.eye(D, device=DEVICE)
    B = torch.matmul(X_tr.T, Y_tr)
    return torch.linalg.solve(A, B)


class PeakAwareLoss(nn.Module):
    def __init__(self, peak_threshold: float = 8.0, alpha: float = 3.0, delta: float = 1.0):
        super().__init__()
        self.peak_thr = peak_threshold
        self.alpha = alpha
        self.huber = nn.HuberLoss(reduction="none", delta=delta)

    def forward(self, pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        base_loss = self.huber(pred, target)
        peak_mask = (target.abs() > self.peak_thr).float()
        weights = 1.0 + (self.alpha - 1.0) * peak_mask
        grad = torch.diff(target, dim=0).abs()
        grad = torch.cat([grad[:1], grad], dim=0)
        grad_w = 1.0 + grad / (grad.mean() + 1e-8)
        return (base_loss * weights * grad_w).mean()


class PeakAwareMLP(nn.Module):
    def __init__(self, raw_dim: int, peak_dim: int = 5, hidden_dims: Tuple[int, ...] = CFG.mlp_hidden):
        super().__init__()
        self.pca_stream = nn.Sequential(
            nn.Linear(raw_dim, hidden_dims[0]),
            nn.ReLU(),
            nn.Linear(hidden_dims[0], hidden_dims[1]),
            nn.ReLU(),
        )
        self.peak_stream = nn.Sequential(
            nn.Linear(peak_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
        )
        self.fusion = nn.Sequential(
            nn.Linear(hidden_dims[1] + 32, hidden_dims[2]),
            nn.ReLU(),
            nn.Linear(hidden_dims[2], 2),
        )

    def forward(self, x_pca: torch.Tensor, x_peak: torch.Tensor) -> torch.Tensor:
        h1 = self.pca_stream(x_pca)
        h2 = self.peak_stream(x_peak)
        return self.fusion(torch.cat([h1, h2], dim=1))


def train_mlp_gpu(X_pca: np.ndarray, X_peak: np.ndarray, Y_tr: np.ndarray,
                  epochs: int = CFG.mlp_epochs) -> PeakAwareMLP:
    model = PeakAwareMLP(raw_dim=X_pca.shape[1], peak_dim=X_peak.shape[1]).to(DEVICE)
    opt = optim.Adam(model.parameters(), lr=CFG.lr, weight_decay=CFG.mlp_alpha)
    crit = PeakAwareLoss(peak_threshold=8.0, alpha=3.0)
    xp = torch.tensor(X_pca, dtype=torch.float32, device=DEVICE)
    xk = torch.tensor(X_peak, dtype=torch.float32, device=DEVICE)
    yt = torch.tensor(Y_tr, dtype=torch.float32, device=DEVICE)
    loader = DataLoader(TensorDataset(xp, xk, yt), batch_size=CFG.batch_size, shuffle=True, num_workers=0)
    scaler = torch.cuda.amp.GradScaler(enabled=(DEVICE.type == "cuda"))
    model.train()
    for _ in range(epochs):
        for bx_pca, bx_peak, by in loader:
            opt.zero_grad(set_to_none=True)
            with torch.cuda.amp.autocast(enabled=(DEVICE.type == "cuda")):
                loss = crit(model(bx_pca, bx_peak), by)
            scaler.scale(loss).backward()
            scaler.step(opt)
            scaler.update()
    model.eval()
    return model


class LSTMDecoder(nn.Module):
    def __init__(self, input_dim: int, output_dim: int = 2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=CFG.lstm_hidden,
            num_layers=CFG.lstm_layers,
            batch_first=True,
            dropout=CFG.lstm_dropout if CFG.lstm_layers > 1 else 0.0,
        )
        self.fc = nn.Linear(CFG.lstm_hidden, output_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])


def train_lstm_gpu(X_tr: np.ndarray, Y_tr: np.ndarray, epochs: int = CFG.lstm_epochs) -> LSTMDecoder:
    model = LSTMDecoder(input_dim=X_tr.shape[2]).to(DEVICE)
    opt = optim.Adam(model.parameters(), lr=CFG.lr, weight_decay=CFG.mlp_alpha)
    crit = nn.MSELoss()
    xt = torch.tensor(X_tr, dtype=torch.float32, device=DEVICE)
    yt = torch.tensor(Y_tr, dtype=torch.float32, device=DEVICE)
    loader = DataLoader(TensorDataset(xt, yt), batch_size=CFG.batch_size, shuffle=True, num_workers=0)
    scaler = torch.cuda.amp.GradScaler(enabled=(DEVICE.type == "cuda"))
    model.train()
    for _ in range(epochs):
        for bx, by in loader:
            opt.zero_grad(set_to_none=True)
            with torch.cuda.amp.autocast(enabled=(DEVICE.type == "cuda")):
                loss = crit(model(bx), by)
            scaler.scale(loss).backward()
            scaler.step(opt)
            scaler.update()
    model.eval()
    return model


class KalmanDecoder:
    def __init__(self, n_riccati_iter: int = CFG.kalman_iter):
        self.n_riccati_iter = n_riccati_iter

    def fit(self, X_train: np.ndarray, Vx_train: np.ndarray, Vy_train: np.ndarray) -> "KalmanDecoder":
        Z = np.column_stack([Vx_train, Vy_train])
        self.A = np.linalg.lstsq(Z[:-1], Z[1:], rcond=None)[0].T
        W_xz = np.linalg.lstsq(X_train, Z, rcond=None)[0]
        alpha_H = 1.0
        HtH = Z.T @ Z + alpha_H * np.eye(2)
        self.H = (np.linalg.solve(HtH, Z.T @ X_train)).T
        res_Q = Z[1:] - (self.A @ Z[:-1].T).T
        self.Q = (res_Q.T @ res_Q) / len(res_Q) + 1e-6 * np.eye(2)
        res_R = X_train - (self.H @ Z.T).T
        raw_var = np.var(res_R, axis=0)
        spike_var_floor = np.var(X_train, axis=0) * 0.1 + 1e-4
        self.R_diag = np.maximum(raw_var, spike_var_floor)
        HtRinv = self.H.T / self.R_diag
        HtRinvH = HtRinv @ self.H
        P = np.diag([np.var(Vx_train), np.var(Vy_train)])
        for _ in range(self.n_riccati_iter):
            K = np.linalg.inv(np.linalg.inv(P) + HtRinvH + 1e-8 * np.eye(2)) @ HtRinv
            P_upd = (np.eye(2) - K @ self.H) @ P
            P = self.A @ P_upd @ self.A.T + self.Q
        self.K_steady = K
        return self

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        preds = []
        z = np.zeros(2)
        for t in range(len(X_test)):
            z_prior = self.A @ z
            z = z_prior + self.K_steady @ (X_test[t] - self.H @ z_prior)
            preds.append(z)
        return np.array(preds)


# =========================================================
# Run decoders with trial-aware split
# =========================================================

@dataclass
class FoldResult:
    rx: float
    ry: float
    r_neural: float
    metrics: Dict[str, Dict[str, float]]


def run_gpu_decoding(model_type: str,
                     X_feat: np.ndarray,
                     Vx_tgt: np.ndarray, Vy_tgt: np.ndarray,
                     trial_cumlen: Optional[np.ndarray] = None,
                     X_peak: Optional[np.ndarray] = None,
                     n_splits: int = CFG.n_folds,
                     sigma: int = CFG.gauss_sigma) -> Tuple[List[FoldResult], Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]:
    if trial_cumlen is not None:
        folds = make_trial_folds(trial_cumlen, n_splits)
    else:
        folds = list(KFold(n_splits=n_splits, shuffle=False).split(X_feat))
    Y_combined = np.stack([Vx_tgt, Vy_tgt], axis=1)
    xmean_global = xstd_global = None
    pfeat_mean_global = pfeat_std_global = None
    if model_type == "MLP":
        X_all_t = torch.tensor(X_feat, dtype=torch.float32, device=DEVICE)
        xmean_global = X_all_t.mean(dim=0, keepdim=True)
        xstd_global = X_all_t.std(dim=0, keepdim=True) + 1e-8
        if X_peak is not None:
            P_all_t = torch.tensor(X_peak, dtype=torch.float32, device=DEVICE)
            pfeat_mean_global = P_all_t.mean(dim=0, keepdim=True)
            pfeat_std_global = P_all_t.std(dim=0, keepdim=True) + 1e-8
            del P_all_t
        del X_all_t
        torch.cuda.empty_cache()
    r_out: List[FoldResult] = []
    last_preds = None
    for tr_bins, te_bins in folds:
        vxte_np = Vx_tgt[te_bins]
        byte_np = Vy_tgt[te_bins]
        if model_type == "Kalman":
            kalman = KalmanDecoder()
            kalman.fit(X_feat[tr_bins], Vx_tgt[tr_bins], Vy_tgt[tr_bins])
            p2d = kalman.predict(X_feat[te_bins])
            vxp_np = gaussian_filter1d(p2d[:, 0], sigma=sigma)
            vyp_np = gaussian_filter1d(p2d[:, 1], sigma=sigma)
        else:
            Xtr = torch.tensor(X_feat[tr_bins], dtype=torch.float32, device=DEVICE)
            Xte = torch.tensor(X_feat[te_bins], dtype=torch.float32, device=DEVICE)
            Ytr = torch.tensor(Y_combined[tr_bins], dtype=torch.float32, device=DEVICE)
            if model_type == "Ridge":
                W = fit_ridge_gpu(Xtr, Ytr)
                out = torch.matmul(Xte, W)
            elif model_type == "MLP":
                Xtr_n = (Xtr - xmean_global) / xstd_global
                Xte_n = (Xte - xmean_global) / xstd_global
                Xtr_peak_raw = torch.tensor(X_peak[tr_bins], dtype=torch.float32, device=DEVICE)
                Xte_peak_raw = torch.tensor(X_peak[te_bins], dtype=torch.float32, device=DEVICE)
                Xtr_peak_n = (Xtr_peak_raw - pfeat_mean_global) / pfeat_std_global
                Xte_peak_n = (Xte_peak_raw - pfeat_mean_global) / pfeat_std_global
                mlp = train_mlp_gpu(Xtr_n.cpu().numpy(), Xtr_peak_n.cpu().numpy(), Ytr.cpu().numpy())
                with torch.no_grad():
                    out = mlp(Xte_n, Xte_peak_n)
            elif model_type == "LSTM":
                xmean = Xtr.mean(dim=(0, 1), keepdim=True)
                xstd = Xtr.std(dim=(0, 1), keepdim=True) + 1e-8
                lstm = train_lstm_gpu(((Xtr - xmean) / xstd).cpu().numpy(), Ytr.cpu().numpy())
                with torch.no_grad():
                    out = lstm((Xte - xmean) / xstd)
            else:
                raise ValueError(model_type)

            vxp_np = gaussian_filter1d(out[:, 0].cpu().numpy(), sigma=sigma)
            vyp_np = gaussian_filter1d(out[:, 1].cpu().numpy(), sigma=sigma)
        rx, _ = pearsonr(vxte_np, vxp_np)
        ry, _ = pearsonr(byte_np, vyp_np)
        r_out.append(FoldResult(
            rx=rx, ry=ry, r_neural=(rx + ry) / 2,
            metrics={
                "x": evaluate_decoding(vxte_np, vxp_np, do_rescale=False),
                "y": evaluate_decoding(byte_np, vyp_np, do_rescale=False),
            },
        ))
        last_preds = (vxte_np, vxp_np, byte_np, vyp_np)
    return r_out, last_preds


# =========================================================
# Diagnostics: fold composition, noise model, rescaling
# =========================================================

def diagnose_folds(trial_cumlen: np.ndarray, n_folds: int = CFG.n_folds) -> None:
    print("\n=== Fold composition (trial-level) ===")
    trial_ids = np.arange(len(trial_cumlen))
    for fi, (tr, te) in enumerate(KFold(n_splits=n_folds, shuffle=False).split(trial_ids), 1):
        print(f" Fold {fi}: train={len(tr)} trials, test={len(te)} trials")


def diagnose_noise_models(X: np.ndarray, ser: float = 1e-2) -> None:
    Xr = apply_SER_random(X, ser, rng=np.random.default_rng(0))
    Xb = apply_SER_burst(X, ser, seed=0)
    miss_r = np.sum((X > 0) & (Xr == 0)) / max(np.sum(X > 0), 1)
    false_r = np.sum((X == 0) & (Xr == 1)) / max(np.sum(X == 0), 1)
    burst_changed = np.mean(X != Xb)
    print(f"\n=== Noise model SER={ser} ===")
    print(f" random: miss={miss_r:.4f}, false_alarm={false_r:.4f}")
    print(f" burst : changed_fraction={burst_changed:.4f}")


def diagnose_rescaling(y_true: np.ndarray, y_pred_raw: np.ndarray) -> None:
    m = evaluate_decoding(y_true, y_pred_raw, do_rescale=False)
    m_r = evaluate_decoding(y_true, y_pred_raw, do_rescale=True)
    print("\n=== Velocity rescaling effect ===")
    print(f" raw_r={m['r_raw']:.4f}, vaf={m['vaf']:.4f}, scale_bias={m['scale_bias']:.3f}")
    print(f" rescaled_r={m_r['r']:.4f}")


# =========================================================
# Main experiment
# =========================================================

def run_baseline(X: np.ndarray, Vx: np.ndarray, Vy: np.ndarray,
                 trial_cumlen: np.ndarray) -> Dict[str, Dict[str, float]]:
    X_lag, vx_lag, vy_lag = create_lagged_features(X, Vx, Vy)
    X_lag_dyn = apply_dynamic_weighting(X_lag)
    _, peak_features, _, _ = create_peak_aware_features(X, Vx, Vy)
    X_seq = create_sequential_features(X)
    X_seq_dyn = apply_dynamic_weighting(X_seq)
    X_obs = get_kalman_obs(X)
    X_obs_dyn = apply_dynamic_weighting(X_obs)
    inputs = {
        "Ridge": X_lag_dyn,
        "MLP": X_lag_dyn,
        "LSTM": X_seq_dyn,
        "Kalman": X_obs_dyn,
    }
    out = {}
    for name in CFG.decoder_names:
        print(f"\n[{name}] trial-aware 5-Fold CV...")
        kw = {"trial_cumlen": trial_cumlen}
        if name == "MLP":
            kw["X_peak"] = peak_features
        folds, last = run_gpu_decoding(name, inputs[name], vx_lag, vy_lag, **kw)
        r_neural = float(np.mean([f.r_neural for f in folds]))
        meta = {
            "r": r_neural,
            "vaf": float(np.mean([f.metrics["x"]["vaf"] for f in folds])),
            "rmse": float(np.mean([f.metrics["x"]["rmse"] for f in folds])),
            "scale_bias": float(np.mean([f.metrics["x"]["scale_bias"] for f in folds])),
            "rx": float(np.mean([f.rx for f in folds])),
            "ry": float(np.mean([f.ry for f in folds])),
            "fold_std": float(np.std([f.r_neural for f in folds])),
            "last_preds": last,
        }
        out[name] = meta
        print(f"  r_neural={r_neural:.4f} fold_std={meta['fold_std']:.4f}")
    return out


def run_ser_experiments(X: np.ndarray, Vx: np.ndarray, Vy: np.ndarray,
                        trial_cumlen: np.ndarray, noise: str = "random") -> Dict[str, Dict[float, float]]:
    X_lag, vx_lag, vy_lag = create_lagged_features(X, Vx, Vy)
    X_lag_dyn = apply_dynamic_weighting(X_lag)
    _, peak_features, _, _ = create_peak_aware_features(X, Vx, Vy)
    out: Dict[str, Dict[float, float]] = {n: {} for n in CFG.decoder_names}
    if noise == "random":
        ser_vals = CFG.ser_values
        corrupter = apply_SER_random
    elif noise == "burst":
        ser_vals = CFG.ser_burst_values
        corrupter = apply_SER_burst
    else:
        raise ValueError
    for ser in ser_vals:
        noisy = corrupter(X, ser) if ser > 0 else X
        X_dyn = apply_dynamic_weighting(create_lagged_features(noisy, Vx, Vy)[0])
        for name in CFG.decoder_names:
            kw: Dict = {"trial_cumlen": trial_cumlen}
            if name == "MLP":
                kw["X_peak"] = peak_features
            folds, _ = run_gpu_decoding(name, X_dyn, vx_lag, vy_lag, **kw)
            out[name][ser] = float(np.mean([f.r_neural for f in folds]))
            print(f"[{name}] SER={ser:.0e}  r={out[name][ser]:.4f}")
    return out


def run_lowdata_augmentation(X: np.ndarray, Vx: np.ndarray, Vy: np.ndarray,
                             trial_cumlen: np.ndarray) -> Dict[int, Dict[str, float]]:
    """
    Simulate low-data regime.
    Cases:
      0 -> true 100 + gen 0
      1 -> true 100 + gen 100
      3 -> true 100 + gen 300
      9 -> true 100 + gen 900
    """
    n_trials = len(trial_cumlen)
    sel_trials = np.linspace(0, n_trials - 1, CFG.vae_low_data_trials, dtype=int)
    train_bins = np.arange(0, trial_cumlen[sel_trials[-1]])
    test_bins = np.arange(trial_cumlen[n_trials // 2], trial_cumlen[n_trials - 1])
    X_lag, vx_lag, vy_lag = create_lagged_features(X, Vx, Vy)
    X_lag_dyn = apply_dynamic_weighting(X_lag)
    _, peak_features, _, _ = create_peak_aware_features(X, Vx, Vy)
    out: Dict[int, Dict[str, float]] = {}
    for ratio in CFG.vae_gen_ratios:
        X_tr = X_lag_dyn[train_bins]
        if ratio > 0:
            idx = np.random.default_rng(0).choice(len(train_bins), size=ratio * len(train_bins), replace=True)
            X_tr = np.concatenate([X_tr, X_tr[idx]], axis=0)
            vx_tr = np.concatenate([vx_lag[train_bins], vx_lag[train_bins][idx]], axis=0)
            vy_tr = np.concatenate([vy_lag[train_bins], vy_lag[train_bins][idx]], axis=0)
        else:
            vx_tr = vx_lag[train_bins]
            vy_tr = vy_lag[train_bins]
        mlp = train_mlp_gpu(X_tr, peak_features[train_bins]
                            if ratio == 0 else
                            np.concatenate([peak_features[train_bins], peak_features[train_bins][idx]], axis=0),
                            np.stack([vx_tr, vy_tr], axis=1))
        with torch.no_grad():
            xt = torch.tensor(X_lag_dyn[test_bins], dtype=torch.float32, device=DEVICE)
            xp = torch.tensor(peak_features[test_bins], dtype=torch.float32, device=DEVICE)
            out_tensor = mlp(xt, xp).cpu().numpy()
        vxp = gaussian_filter1d(out_tensor[:, 0], sigma=CFG.gauss_sigma)
        vyp = gaussian_filter1d(out_tensor[:, 1], sigma=CFG.gauss_sigma)
        metrics_x = evaluate_decoding(vx_lag[test_bins], vxp, do_rescale=False)
        metrics_y = evaluate_decoding(vy_lag[test_bins], vyp, do_rescale=False)
        out[ratio] = {
            "r": float((metrics_x["r"] + metrics_y["r"]) / 2),
            "vaf": float((metrics_x["vaf"] + metrics_y["vaf"]) / 2),
            "scale_bias": float((metrics_x["scale_bias"] + metrics_y["scale_bias"]) / 2),
        }
        print(f"gen_ratio="+"{:.0f}".format(ratio)+"  r={out[ratio]['r']:.4f}")
    return out


# =========================================================
# Visualization
# =========================================================

def plot_baseline(results: Dict[str, Dict[str, float]]) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    names = list(results.keys())
    colors = [DECODER_COLORS[n] for n in names]
    for col, (key, label, ylim) in enumerate([
        ("r", "r_neural", (0.5, 1.05)),
        ("vaf", "VAF", (0.5, 1.05)),
        ("scale_bias", "Scale Bias", (0.0, 1.3)),
    ]):
        ax = axes[col]
        vals = [results[n][key] for n in names]
        bars = ax.bar(names, vals, color=colors, alpha=0.82, width=0.4, edgecolor="black", linewidth=1.1)
        if key == "r":
            ax.axhline(CFG.paper_r_neural, color="crimson", linestyle="--", lw=1.5, label=f"Paper SNN ({CFG.paper_r_neural})")
            ax.legend(fontsize=8)
        elif key == "scale_bias":
            ax.axhline(1.0, color="black", linestyle="--", lw=1.5, alpha=0.5, label="Perfect (1.0)")
            ax.legend(fontsize=8)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.012,
                    f"{val:.3f}", ha="center", fontsize=9.5, fontweight="bold")
        ax.set_ylim(ylim)
        ax.set_title(label, fontsize=11, fontweight="bold")
        ax.grid(True, axis="y", alpha=0.3)
    plt.suptitle("Phase 2: Baseline Performance (SER=0) — 4-Decoder Comparison", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig("fig1_baseline_comparison.png", dpi=150, bbox_inches="tight")
    plt.show()


def plot_ser_curve(ser_results: Dict[str, Dict[float, float]], noise: str) -> None:
    plt.figure(figsize=(10, 6))
    for name, curve in ser_results.items():
        xs = sorted(curve)
        ys = [curve[x] for x in xs]
        plt.plot(xs, ys, marker=DECODER_MARKERS[name], color=DECODER_COLORS[name],
                 linewidth=2, label=name)
    plt.xscale("log")
    plt.xlabel("SER (log scale)")
    plt.ylabel("r_neural")
    plt.title(f"SER Robustness Sweep — {noise} noise model")
    plt.ylim([0.0, 1.05])
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()
    name = "ser_curve_" + noise
    plt.savefig(name + ".png", dpi=150, bbox_inches="tight")
    plt.show()


def plot_lowdata_aug(aug: Dict[int, Dict[str, float]]) -> None:
    ratios = sorted(aug)
    xs = [CFG.vae_gen_ratios[0]] + [r for r in ratios if r > 0]
    ys = [aug[r]["r"] for r in xs]
    plt.figure(figsize=(8, 5))
    plt.plot(xs, ys, marker="o", color="darkorange", linewidth=2)
    plt.axhline(aug[0]["r"], color="gray", linestyle="--", alpha=0.7, label="Low-data only")
    plt.xlabel("Generated / Real ratio")
    plt.ylabel("r_neural")
    plt.title("Low-data Augmentation Effect (Mock VAE generation)")
    plt.ylim([0.5, 1.05])
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("fig_aug_lowdata.png", dpi=150, bbox_inches="tight")
    plt.show()


# =========================================================
# Entry
# =========================================================

def main() -> None:
    print("Device:", DEVICE)
    X, Vx, Vy, trial_cumlen = load_pmd1()
    print(f"X={X.shape}  Vx={Vx.shape}  Vy={Vy.shape}")
    print(f"sparsity={np.mean(X == 0) * 100:.2f}%  mean_FR={X.mean() / 0.01:.2f} Hz")
    diagnose_folds(trial_cumlen)
    diagnose_noise_models(X, ser=1e-2)
    # Baseline SER=0
    baseline = run_baseline(X, Vx, Vy, trial_cumlen)
    plot_baseline(baseline)
    last = baseline["Ridge"]["last_preds"]
    if last is not None:
        print(f"last_Ridge_rx={pearsonr(last[0], last[1])[0]:.4f}")
    # SER sweep random
    ser_random = run_ser_experiments(X, Vx, Vy, trial_cumlen, noise="random")
    plot_ser_curve(ser_random, "random")
    # SER sweep burst
    ser_burst = run_ser_experiments(X, Vx, Vy, trial_cumlen, noise="burst")
    plot_ser_curve(ser_burst, "burst")
    # Low-data augmentation
    aug = run_lowdata_augmentation(X, Vx, Vy, trial_cumlen)
    plot_lowdata_aug(aug)
    # Rescaling diagnostic on last Ridge prediction
    if last is not None:
        diagnose_rescaling(last[0], last[1])
    print("\nDone.")


if __name__ == "__main__":
    main()
