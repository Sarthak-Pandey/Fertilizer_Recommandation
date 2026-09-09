"""
Fertilizer Recommendation System - Model Training Script

Trains the hierarchical gate + specialist architecture and saves
a complete, versioned model bundle.

Usage:
    python training/train.py --version v1 --dataset-version dataset-v1
    python training/train.py --version v2 --dataset-version dataset-v2
"""

import argparse
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, StandardScaler


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATASET = PROJECT_ROOT / "training" / "data" / "fertilizer_recommendation.csv"
MODELS_DIR = PROJECT_ROOT / "ml-service" / "models"

# Features used for training (Core-5 + useful extras from the handoff report)
NUMERICAL_FEATURES = [
    "Soil_pH",
    "Nitrogen_Level",
    "Phosphorus_Level",
    "Potassium_Level",
    "Temperature",
    "Humidity",
    "Rainfall",
    "Soil_Moisture",
]

CATEGORICAL_FEATURES = [
    "Crop_Growth_Stage",
    "Soil_Type",
    "Crop_Type",
]

ALL_FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES
TARGET = "Recommended_Fertilizer"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _git_commit() -> str | None:
    """Return current HEAD commit hash or None."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        pass
    return None


def _build_preprocessor() -> ColumnTransformer:
    """Build a ColumnTransformer matching training expectations."""
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERICAL_FEATURES),
            ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )


def _evaluate_classifier(name: str, y_true, y_pred, labels=None) -> dict:
    """Return a dict of evaluation metrics and print a summary."""
    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
    weighted_f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)

    print(f"\n{'=' * 60}")
    print(f"  {name}")
    print(f"{'=' * 60}")
    print(f"  Accuracy      : {acc:.4f}")
    print(f"  Macro F1      : {macro_f1:.4f}")
    print(f"  Weighted F1   : {weighted_f1:.4f}")
    print(classification_report(y_true, y_pred, zero_division=0))

    metrics = {
        "accuracy": round(float(acc), 4),
        "macro_f1": round(float(macro_f1), 4),
        "weighted_f1": round(float(weighted_f1), 4),
    }

    # Per-class metrics for known classes of interest
    if labels is not None:
        for label in labels:
            mask = y_true == label
            if mask.sum() == 0:
                continue
            pred_mask = y_pred == label
            tp = ((y_pred == label) & (y_true == label)).sum()
            fp = ((y_pred == label) & (y_true != label)).sum()
            fn = ((y_pred != label) & (y_true == label)).sum()
            prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
            metrics[f"{label}_precision"] = round(float(prec), 4)
            metrics[f"{label}_recall"] = round(float(rec), 4)
            metrics[f"{label}_f1"] = round(float(f1), 4)

    return metrics


# ---------------------------------------------------------------------------
# Main training logic
# ---------------------------------------------------------------------------

def train(
    version: str,
    dataset_version: str,
    dataset_path: Path,
    output_dir: Path,
) -> dict:
    """Train the full hierarchical pipeline and save artifacts."""
    print(f"\n{'#' * 60}")
    print(f"  Training model bundle: {version}")
    print(f"  Dataset             : {dataset_path.name} ({dataset_version})")
    print(f"{'#' * 60}\n")

    # ---- Load data --------------------------------------------------------
    df = pd.read_csv(dataset_path)
    assert TARGET in df.columns, f"Target column '{TARGET}' not found"
    for col in ALL_FEATURES:
        assert col in df.columns, f"Feature column '{col}' not found in dataset"

    X = df[ALL_FEATURES].copy()
    y = df[TARGET].copy()

    print(f"Dataset shape     : {X.shape}")
    print(f"Target distribution:\n{y.value_counts()}\n")

    # ---- Train / test split -----------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y,
    )
    print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

    # ---- Fit preprocessing ------------------------------------------------
    preprocessor = _build_preprocessor()
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    print("Preprocessing fitted.")

    # ---- Encode labels ----------------------------------------------------
    label_encoder = LabelEncoder()
    y_train_enc = label_encoder.fit_transform(y_train)
    y_test_enc = label_encoder.transform(y_test)
    class_names = list(label_encoder.classes_)
    print(f"Classes: {class_names}")

    # ---- Train Gate Classifier (7-class) ----------------------------------
    print("\n>>> Training Gate Classifier (7-class RandomForest) ...")
    gate_model = RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    gate_model.fit(X_train_processed, y_train_enc)
    gate_preds = gate_model.predict(X_test_processed)
    gate_preds_labels = label_encoder.inverse_transform(gate_preds)
    gate_metrics = _evaluate_classifier(
        "Gate Classifier (7-class)",
        y_test.values,
        gate_preds_labels,
        labels=["SSP", "NPK"],
    )

    # ---- Prepare binary SSP vs NPK data ----------------------------------
    binary_mask_train = y_train.isin(["SSP", "NPK"])
    binary_mask_test = y_test.isin(["SSP", "NPK"])

    X_train_binary = X_train_processed[binary_mask_train.values]
    y_train_binary = (y_train[binary_mask_train] == "SSP").astype(int).values

    X_test_binary = X_test_processed[binary_mask_test.values]
    y_test_binary = (y_test[binary_mask_test] == "SSP").astype(int).values

    # ---- Train SSP Specialist (binary: 1=SSP, 0=NPK) ---------------------
    print("\n>>> Training SSP Specialist (binary SSP vs NPK) ...")
    ssp_model = RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    ssp_model.fit(X_train_binary, y_train_binary)
    ssp_preds = ssp_model.predict(X_test_binary)
    ssp_labels = np.where(ssp_preds == 1, "SSP", "NPK")
    ssp_true_labels = np.where(y_test_binary == 1, "SSP", "NPK")
    ssp_metrics = _evaluate_classifier(
        "SSP Specialist (binary SSP/NPK)",
        ssp_true_labels,
        ssp_labels,
        labels=["SSP", "NPK"],
    )

    # ---- Train NPK Specialist (same binary model, different perspective) --
    # The NPK specialist is the complement of the SSP specialist.
    # We train a separate model to allow independent tuning in future versions.
    print("\n>>> Training NPK Specialist (binary NPK vs SSP) ...")
    npk_model = RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    # For the NPK specialist, target is 1=NPK, 0=SSP (inverted)
    y_train_npk = (y_train[binary_mask_train] == "NPK").astype(int).values
    y_test_npk = (y_test[binary_mask_test] == "NPK").astype(int).values
    npk_model.fit(X_train_binary, y_train_npk)
    npk_preds = npk_model.predict(X_test_binary)
    npk_labels = np.where(npk_preds == 1, "NPK", "SSP")
    npk_true_labels = np.where(y_test_npk == 1, "NPK", "SSP")
    npk_metrics = _evaluate_classifier(
        "NPK Specialist (binary NPK/SSP)",
        npk_true_labels,
        npk_labels,
        labels=["NPK", "SSP"],
    )

    # ---- Cross-validation on Gate ----------------------------------------
    print("\n>>> 5-Fold CV on Gate Classifier ...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(gate_model, X_train_processed, y_train_enc, cv=cv, scoring="accuracy")
    print(f"  CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    gate_metrics["cv_accuracy_mean"] = round(float(cv_scores.mean()), 4)
    gate_metrics["cv_accuracy_std"] = round(float(cv_scores.std()), 4)

    # ---- Save artifacts ---------------------------------------------------
    version_dir = output_dir / version
    version_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(gate_model, version_dir / "gate_model.pkl")
    joblib.dump(ssp_model, version_dir / "ssp_model.pkl")
    joblib.dump(npk_model, version_dir / "npk_model.pkl")
    joblib.dump(preprocessor, version_dir / "preprocessing.pkl")
    joblib.dump(label_encoder, version_dir / "label_encoder.pkl")

    print(f"\nArtifacts saved to: {version_dir}")

    # ---- Generate metadata ------------------------------------------------
    import sklearn

    metadata = {
        "model_version": version,
        "preprocessing_version": f"preprocessing-{version}",
        "feature_schema_version": f"features-{version}",
        "dataset_version": dataset_version,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": _git_commit(),
        "python_version": platform.python_version(),
        "sklearn_version": sklearn.__version__,
        "features": {
            "numerical": NUMERICAL_FEATURES,
            "categorical": CATEGORICAL_FEATURES,
            "all": ALL_FEATURES,
        },
        "target": TARGET,
        "classes": class_names,
        "models": {
            "gate": "RandomForestClassifier(n_estimators=200, class_weight='balanced')",
            "ssp": "RandomForestClassifier(n_estimators=200, class_weight='balanced') - binary SSP/NPK",
            "npk": "RandomForestClassifier(n_estimators=200, class_weight='balanced') - binary NPK/SSP",
        },
        "metrics": {
            "gate": gate_metrics,
            "ssp_specialist": ssp_metrics,
            "npk_specialist": npk_metrics,
        },
        "dataset_stats": {
            "total_samples": len(df),
            "train_samples": len(X_train),
            "test_samples": len(X_test),
            "class_distribution": y.value_counts().to_dict(),
        },
        "artifacts": [
            "gate_model.pkl",
            "ssp_model.pkl",
            "npk_model.pkl",
            "preprocessing.pkl",
            "label_encoder.pkl",
            "metadata.json",
        ],
        "status": "candidate",
    }

    with open(version_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2, default=str)

    print(f"Metadata saved to: {version_dir / 'metadata.json'}")

    # ---- Summary ----------------------------------------------------------
    print(f"\n{'#' * 60}")
    print(f"  MODEL BUNDLE {version} - TRAINING COMPLETE")
    print(f"{'#' * 60}")
    print(f"  Model version        : {version}")
    print(f"  Preprocessing version: preprocessing-{version}")
    print(f"  Feature schema       : features-{version}")
    print(f"  Dataset version      : {dataset_version}")
    print(f"  Gate accuracy        : {gate_metrics['accuracy']:.4f}")
    print(f"  Gate CV accuracy     : {gate_metrics['cv_accuracy_mean']:.4f}")
    print(f"  SSP F1 (specialist)  : {ssp_metrics.get('SSP_f1', 'N/A')}")
    print(f"  NPK F1 (specialist)  : {npk_metrics.get('NPK_f1', 'N/A')}")
    print(f"  Status               : candidate (NOT production)")
    print(f"\n  To promote to production:")
    print(f"    python training/train.py --promote {version}")
    print(f"{'#' * 60}\n")

    return metadata


def promote(version: str, stage: str = "production") -> None:
    """Promote a model version to a given stage in the registry."""
    registry_path = MODELS_DIR / "registry.json"
    version_dir = MODELS_DIR / version

    if not version_dir.exists():
        print(f"ERROR: Model version '{version}' not found at {version_dir}")
        sys.exit(1)

    metadata_path = version_dir / "metadata.json"
    if not metadata_path.exists():
        print(f"ERROR: metadata.json not found for version '{version}'")
        sys.exit(1)

    # Load or create registry
    registry = {}
    if registry_path.exists():
        with open(registry_path) as f:
            registry = json.load(f)

    old_production = registry.get("production")
    registry[stage] = version

    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)

    # Update metadata status
    with open(metadata_path) as f:
        meta = json.load(f)
    meta["status"] = stage
    meta["promoted_at"] = datetime.now(timezone.utc).isoformat()
    with open(metadata_path, "w") as f:
        json.dump(meta, f, indent=2, default=str)

    print(f"\n{'=' * 60}")
    print(f"  Model {version} promoted to: {stage}")
    if old_production and old_production != version:
        print(f"  Previous production: {old_production} (still available for rollback)")
    print(f"{'=' * 60}\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Train Fertilizer Recommendation Models")
    parser.add_argument("--version", type=str, default="v1", help="Model version identifier (e.g. v1, v2)")
    parser.add_argument("--dataset-version", type=str, default="dataset-v1", help="Dataset version tag")
    parser.add_argument("--dataset", type=str, default=str(DEFAULT_DATASET), help="Path to CSV dataset")
    parser.add_argument("--promote", type=str, default=None, help="Promote a version to production (skip training)")
    parser.add_argument("--stage", type=str, default="production", choices=["production", "staging", "candidate"], help="Target stage for promotion")

    args = parser.parse_args()

    if args.promote:
        promote(args.promote, args.stage)
        return

    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        print(f"ERROR: Dataset not found at {dataset_path}")
        sys.exit(1)

    version_dir = MODELS_DIR / args.version
    if version_dir.exists() and (version_dir / "metadata.json").exists():
        print(f"WARNING: Model version '{args.version}' already exists at {version_dir}")
        print("  Use a different --version or delete the existing bundle.")
        sys.exit(1)

    train(
        version=args.version,
        dataset_version=args.dataset_version,
        dataset_path=dataset_path,
        output_dir=MODELS_DIR,
    )


if __name__ == "__main__":
    main()
