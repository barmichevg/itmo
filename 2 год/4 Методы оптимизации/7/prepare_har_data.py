"""Prepare UCI HAR data for the Adagrad examples.

The script reads the original nested archive distributed with the laboratory,
standardizes all 561 features using statistics fitted on the training split,
converts labels from 1..6 to 0..5, and writes har_preprocessed.npz to both
Adagrad project directories.

Dependency: numpy
Run from any working directory:
    python prepare_har_data.py
"""

from __future__ import annotations

import argparse
import io
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SOURCE = SCRIPT_DIR / "human+activity+recognition+using+smartphones.zip"
DEFAULT_OUTPUTS = (
    SCRIPT_DIR / "lab" / "3 Adagrad" / "data" / "har_preprocessed.npz",
    SCRIPT_DIR / "lab" / "3 CustomAdagrad" / "data" / "har_preprocessed.npz",
)
INNER_ARCHIVE_NAME = "UCI HAR Dataset.zip"
DATASET_DIR_NAME = "UCI HAR Dataset"


def _safe_extract(archive: zipfile.ZipFile, destination: Path) -> None:
    """Extract a ZIP while rejecting absolute paths and parent traversal."""
    destination = destination.resolve()
    for member in archive.infolist():
        parts = PurePosixPath(member.filename).parts
        if PurePosixPath(member.filename).is_absolute() or ".." in parts:
            raise ValueError(f"Unsafe path in ZIP: {member.filename!r}")
    archive.extractall(destination)


def _read_indexed_names(path: Path) -> list[str]:
    names: list[str] = []
    with path.open("r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                _, name = stripped.split(maxsplit=1)
            except ValueError as error:
                raise ValueError(
                    f"Invalid indexed-name line {line_number} in {path}: {stripped!r}"
                ) from error
            names.append(name)
    return names


def _validate_shapes(
    x_train: np.ndarray,
    x_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
    feature_names: list[str],
    class_names: list[str],
) -> None:
    expected = {
        "X_train": (7352, 561),
        "X_test": (2947, 561),
        "y_train": (7352,),
        "y_test": (2947,),
    }
    actual = {
        "X_train": x_train.shape,
        "X_test": x_test.shape,
        "y_train": y_train.shape,
        "y_test": y_test.shape,
    }
    for name, expected_shape in expected.items():
        if actual[name] != expected_shape:
            raise ValueError(
                f"Unexpected {name} shape: {actual[name]}, expected {expected_shape}"
            )
    if len(feature_names) != 561:
        raise ValueError(f"Expected 561 feature names, got {len(feature_names)}")
    if len(class_names) != 6:
        raise ValueError(f"Expected 6 class names, got {len(class_names)}")
    if y_train.min() != 0 or y_train.max() != 5:
        raise ValueError("Training labels must be in the range 0..5")
    if y_test.min() != 0 or y_test.max() != 5:
        raise ValueError("Test labels must be in the range 0..5")


def prepare(source_archive: Path, outputs: tuple[Path, ...]) -> None:
    if not source_archive.is_file():
        raise FileNotFoundError(f"Source archive not found: {source_archive}")

    with zipfile.ZipFile(source_archive) as outer_zip:
        bad_member = outer_zip.testzip()
        if bad_member is not None:
            raise zipfile.BadZipFile(f"Corrupted file in outer ZIP: {bad_member}")
        try:
            inner_bytes = outer_zip.read(INNER_ARCHIVE_NAME)
        except KeyError as error:
            raise FileNotFoundError(
                f"{INNER_ARCHIVE_NAME!r} not found inside {source_archive}"
            ) from error

    with tempfile.TemporaryDirectory(prefix="uci_har_") as temp_name:
        temp_dir = Path(temp_name)
        with zipfile.ZipFile(io.BytesIO(inner_bytes)) as inner_zip:
            bad_member = inner_zip.testzip()
            if bad_member is not None:
                raise zipfile.BadZipFile(f"Corrupted file in inner ZIP: {bad_member}")
            _safe_extract(inner_zip, temp_dir)

        dataset_dir = temp_dir / DATASET_DIR_NAME
        if not dataset_dir.is_dir():
            raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")

        x_train_raw = np.loadtxt(dataset_dir / "train" / "X_train.txt", dtype=np.float64)
        x_test_raw = np.loadtxt(dataset_dir / "test" / "X_test.txt", dtype=np.float64)
        y_train = np.loadtxt(dataset_dir / "train" / "y_train.txt", dtype=np.int64) - 1
        y_test = np.loadtxt(dataset_dir / "test" / "y_test.txt", dtype=np.int64) - 1

        class_names = _read_indexed_names(dataset_dir / "activity_labels.txt")
        feature_names = _read_indexed_names(dataset_dir / "features.txt")

        # Fit normalization on training data only to prevent test-data leakage.
        mean = x_train_raw.mean(axis=0)
        std = x_train_raw.std(axis=0)
        if np.any(std == 0):
            indices = np.flatnonzero(std == 0).tolist()
            raise ValueError(f"Features with zero standard deviation: {indices}")

        x_train = ((x_train_raw - mean) / std).astype(np.float32)
        x_test = ((x_test_raw - mean) / std).astype(np.float32)

        _validate_shapes(
            x_train,
            x_test,
            y_train,
            y_test,
            feature_names,
            class_names,
        )

        payload = {
            "X_train": x_train,
            "X_test": x_test,
            "y_train": y_train,
            "y_test": y_test,
            "class_names": np.asarray(class_names),
            # Object dtype reproduces the existing laboratory NPZ format.
            "feature_names": np.asarray(feature_names, dtype=object),
        }

        for output in outputs:
            output.parent.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(output, **payload)
            print(f"Created: {output}")

    print(f"X_train: {x_train.shape}, X_test: {x_test.shape}")
    print(f"Classes: {len(class_names)}, features: {len(feature_names)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare standardized UCI HAR data for both Adagrad examples."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help=f"Path to the outer source archive (default: {DEFAULT_SOURCE.name})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        action="append",
        help=(
            "Output NPZ path. May be specified more than once. "
            "Without this option, both laboratory data folders are updated."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outputs = tuple(args.output) if args.output else DEFAULT_OUTPUTS
    prepare(args.source.resolve(), tuple(path.resolve() for path in outputs))


if __name__ == "__main__":
    main()
