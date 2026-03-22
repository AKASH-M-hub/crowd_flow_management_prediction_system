from __future__ import annotations

import os
import json
from typing import Callable, Iterable, List, Sequence, Tuple

import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


class CrowdPredictor:
    def __init__(self, model_path: str, window_size: int = 24, horizon_steps: int = 15):
        self.model_path = model_path
        self.window_size = window_size
        self.horizon_steps = horizon_steps
        self.pipeline: Pipeline | None = None
        self.metrics = {}
        self._load_if_available()

    def _load_if_available(self) -> None:
        meta_path = self._meta_path()
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            self.window_size = int(meta.get("window_size", self.window_size))
            self.horizon_steps = int(meta.get("horizon_steps", self.horizon_steps))

        if os.path.exists(self.model_path):
            self.pipeline = joblib.load(self.model_path)

    def _meta_path(self) -> str:
        model_dir = os.path.dirname(self.model_path)
        return os.path.join(model_dir, "crowd_predictor_meta.json")

    def is_trained(self) -> bool:
        return self.pipeline is not None

    def _build_training_rows(
        self,
        count_series: Sequence[int],
        density_series: Sequence[float],
        elapsed_series: Sequence[float],
    ) -> Tuple[np.ndarray, np.ndarray]:
        min_len = min(len(count_series), len(density_series), len(elapsed_series))
        if min_len < self.window_size + self.horizon_steps:
            return np.empty((0, self.window_size * 2 + 1), dtype=np.float32), np.empty((0,), dtype=np.float32)

        x_rows: List[List[float]] = []
        y_rows: List[float] = []

        max_start = min_len - self.window_size - self.horizon_steps + 1
        for start in range(max_start):
            end = start + self.window_size
            target_idx = end + self.horizon_steps - 1

            count_window = [float(v) for v in count_series[start:end]]
            density_window = [float(v) for v in density_series[start:end]]
            elapsed_value = float(elapsed_series[end - 1])

            features = count_window + density_window + [elapsed_value]
            x_rows.append(features)
            y_rows.append(float(count_series[target_idx]))

        return np.array(x_rows, dtype=np.float32), np.array(y_rows, dtype=np.float32)

    def fit_from_series_list(self, series_list: Iterable[dict]) -> dict:
        x_parts = []
        y_parts = []
        for series in series_list:
            x_chunk, y_chunk = self._build_training_rows(
                series["counts"],
                series["densities"],
                series["elapsed"],
            )
            if len(x_chunk) > 0:
                x_parts.append(x_chunk)
                y_parts.append(y_chunk)

        if not x_parts:
            raise ValueError(
                "Not enough samples to train. Provide longer count series or reduce window/horizon."
            )

        x = np.vstack(x_parts)
        y = np.hstack(y_parts)

        split_idx = int(len(x) * 0.8)
        if split_idx <= 0 or split_idx >= len(x):
            raise ValueError("Need more training samples to create train/validation split.")

        x_train = x[:split_idx]
        y_train = y[:split_idx]
        x_val = x[split_idx:]
        y_val = y[split_idx:]

        self.pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "nn",
                    MLPRegressor(
                        hidden_layer_sizes=(96, 48),
                        activation="relu",
                        solver="adam",
                        max_iter=900,
                        random_state=42,
                        early_stopping=True,
                        validation_fraction=0.15,
                        n_iter_no_change=25,
                    ),
                ),
            ]
        )

        self.pipeline.fit(x_train, y_train)

        val_pred = self.pipeline.predict(x_val)
        val_pred = np.maximum(val_pred, 0)

        mae = float(mean_absolute_error(y_val, val_pred))
        mape = float(np.mean(np.abs((y_val - val_pred) / np.maximum(y_val, 1.0))) * 100.0)

        self.metrics = {
            "samples": int(len(x)),
            "train_samples": int(len(x_train)),
            "val_samples": int(len(x_val)),
            "mae": round(mae, 3),
            "mape_percent": round(mape, 3),
        }
        return self.metrics

    def save(self) -> None:
        if self.pipeline is None:
            raise RuntimeError("Cannot save: model is not trained.")
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.pipeline, self.model_path)
        with open(self._meta_path(), "w", encoding="utf-8") as f:
            json.dump(
                {
                    "window_size": self.window_size,
                    "horizon_steps": self.horizon_steps,
                },
                f,
                indent=2,
            )

    def predict(
        self,
        count_history: Sequence[int],
        density_history: Sequence[float],
        elapsed_ratio: float,
    ) -> int:
        if self.pipeline is None:
            raise RuntimeError("Prediction model is not trained or loaded.")

        if len(count_history) < self.window_size or len(density_history) < self.window_size:
            return int(count_history[-1]) if count_history else 0

        count_window = np.array(count_history[-self.window_size :], dtype=np.float32)
        density_window = np.array(density_history[-self.window_size :], dtype=np.float32)
        features = np.concatenate([count_window, density_window, np.array([float(elapsed_ratio)], dtype=np.float32)])
        latest_window = features.reshape(1, -1)

        pred = float(self.pipeline.predict(latest_window)[0])
        return max(0, int(round(pred)))

    def predict_with_context_fallback(
        self,
        count_history: Sequence[int],
        density_history: Sequence[float],
        elapsed_ratio: float,
        fallback_fn: Callable[[Sequence[int]], int],
        warmup_ready: bool,
    ) -> int:
        if not warmup_ready or self.pipeline is None:
            return int(fallback_fn(count_history))
        return self.predict(count_history, density_history, elapsed_ratio)
