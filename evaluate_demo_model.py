import json
import os
from typing import Dict, List

import numpy as np

from processing.crowd_predictor import CrowdPredictor


def _mape(y_true: List[int], y_pred: List[int]) -> float:
    y_t = np.array(y_true, dtype=np.float32)
    y_p = np.array(y_pred, dtype=np.float32)
    return float(np.mean(np.abs((y_t - y_p) / np.maximum(y_t, 1.0))) * 100.0)


def _rmse(y_true: List[int], y_pred: List[int]) -> float:
    y_t = np.array(y_true, dtype=np.float32)
    y_p = np.array(y_pred, dtype=np.float32)
    return float(np.sqrt(np.mean((y_t - y_p) ** 2)))


def evaluate_series(predictor: CrowdPredictor, counts: List[int], densities: List[float], elapsed: List[float]) -> Dict:
    window = predictor.window_size
    horizon = predictor.horizon_steps

    y_true = []
    y_pred = []
    incoming_true = []
    incoming_pred = []

    for i in range(window, len(counts) - horizon):
        if elapsed[i] <= 0.10:
            continue

        hist_counts = counts[:i]
        hist_densities = densities[:i]
        current = counts[i]
        actual_future = counts[i + horizon]

        pred_future = predictor.predict(hist_counts, hist_densities, elapsed[i])

        delta_true = actual_future - current
        delta_pred = pred_future - current

        threshold = max(2, int(round(current * 0.12)))
        incoming_true.append(1 if delta_true >= threshold else 0)
        incoming_pred.append(1 if delta_pred >= threshold else 0)

        y_true.append(actual_future)
        y_pred.append(pred_future)

    if not y_true:
        return {
            "samples": 0,
            "mae": None,
            "rmse": None,
            "mape_percent": None,
            "incoming_accuracy_percent": None,
        }

    mae = float(np.mean(np.abs(np.array(y_true) - np.array(y_pred))))
    rmse = _rmse(y_true, y_pred)
    mape = _mape(y_true, y_pred)

    acc = float(
        np.mean(np.array(incoming_true, dtype=np.int32) == np.array(incoming_pred, dtype=np.int32)) * 100.0
    )

    return {
        "samples": int(len(y_true)),
        "mae": round(mae, 3),
        "rmse": round(rmse, 3),
        "mape_percent": round(mape, 3),
        "incoming_accuracy_percent": round(acc, 3),
    }


def main():
    model_path = "models/crowd_predictor.joblib"
    series_path = "models/demo_training_series.json"

    if not os.path.exists(model_path):
        raise RuntimeError("Missing trained model: models/crowd_predictor.joblib")
    if not os.path.exists(series_path):
        raise RuntimeError("Missing series archive: models/demo_training_series.json. Run training first.")

    predictor = CrowdPredictor(model_path=model_path)
    if not predictor.is_trained():
        raise RuntimeError("Model file exists but failed to load predictor.")

    with open(series_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    series_list = data.get("series", [])
    if not series_list:
        raise RuntimeError("No demo series in archive.")

    per_video = []
    for idx, s in enumerate(series_list, start=1):
        metrics = evaluate_series(
            predictor,
            counts=[int(v) for v in s["counts"]],
            densities=[float(v) for v in s["densities"]],
            elapsed=[float(v) for v in s["elapsed"]],
        )
        metrics["video_index"] = idx
        per_video.append(metrics)

    valid = [m for m in per_video if m["samples"] > 0]

    def avg(key: str):
        vals = [float(m[key]) for m in valid if m[key] is not None]
        return round(float(sum(vals) / len(vals)), 3) if vals else None

    summary = {
        "model_path": model_path,
        "window_size": predictor.window_size,
        "horizon_steps": predictor.horizon_steps,
        "demo_video_count": len(series_list),
        "videos_evaluated": len(valid),
        "avg_mae": avg("mae"),
        "avg_rmse": avg("rmse"),
        "avg_mape_percent": avg("mape_percent"),
        "avg_incoming_accuracy_percent": avg("incoming_accuracy_percent"),
    }

    out_json = "models/demo5_model_evaluation.json"
    out_csv = "models/demo5_model_evaluation.csv"
    out_txt = "models/demo5_model_evaluation.txt"

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "per_video": per_video}, f, indent=2)

    with open(out_csv, "w", encoding="utf-8") as f:
        f.write("video_index,samples,mae,rmse,mape_percent,incoming_accuracy_percent\n")
        for row in per_video:
            f.write(
                f"{row['video_index']},{row['samples']},{row['mae']},{row['rmse']},{row['mape_percent']},{row['incoming_accuracy_percent']}\n"
            )

    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("DEMO-5 MODEL EVALUATION\n")
        f.write("=======================\n")
        for k, v in summary.items():
            f.write(f"{k}: {v}\n")

    print("Evaluation completed.")
    print(f"Summary: {summary}")
    print(f"Saved: {out_json}")
    print(f"Saved: {out_csv}")
    print(f"Saved: {out_txt}")


if __name__ == "__main__":
    main()
