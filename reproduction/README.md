# R0 — clean trial-disjoint Ridge reproduction

R0 answers one question before any new model or SER experiment:

> Can the CRCNS pmd-1 Ridge baseline be run from a clean environment without
> trial leakage, and what result does that corrected procedure actually produce?

The repository currently reports `r=0.8701`. That number is a **legacy claim**, not
a pass threshold. The clean result may differ. A discrepancy is a finding to explain,
not a result to hide or tune away.

## What this entry point fixes

- History windows are built independently inside every reach trial.
- Cross-validation splits trial IDs; train and test IDs are asserted disjoint.
- Prediction smoothing is performed inside each test trial.
- No affine rescaling is fitted on test labels.
- The first executable is CPU-only Ridge with an explicit deterministic `lsqr` solver;
  neural architectures and SER are out of scope.
- Each full run saves fold metrics, configuration, package versions, and optionally the
  data file SHA-256.

## Tablet / Colab path

Open `notebooks/R0_ridge_colab.ipynb` in Google Colab and run cells from top to bottom.
The notebook mounts Drive, checks the data path, installs only three dependencies, runs
a 25-trial smoke test, then runs the full five-fold baseline. Outputs are written to
Google Drive rather than the disposable Colab VM.

The first gate is binary:

- `GREEN`: `MM_S1_processed.mat` is reachable and the smoke run produces JSON/CSV.
- `BLOCKED`: the file is absent or has an unexpected schema. Do not spend weeks editing
  models; resolve access or switch datasets under the separately documented decision rule.

## Command line

```bash
python -m pip install -r reproduction/requirements.txt
python -m unittest discover -s reproduction/tests -v

# Fast data/schema check and small run
python -m reproduction.r0_ridge \
  --data /path/to/MM_S1_processed.mat \
  --output results/r0-smoke \
  --max-trials 25 \
  --folds 5

# Full evidence-producing run
python -m reproduction.r0_ridge \
  --data /path/to/MM_S1_processed.mat \
  --output results/r0-full \
  --hash-data
```

`r0_summary.json` is the claim record. `r0_folds.csv` is the compact table for the PI
report. A run is not a completed R0 result unless both files are saved outside the
ephemeral runtime.

## Explicit non-claims

R0 does not establish neural-interface robustness, compare architectures, model a real
wireless channel, or explain human metacognition. It establishes a trustworthy decoding
measurement substrate. Only after R0 is closed should R1 define a matched-error-count
`iid` versus `burst` corruption experiment.
