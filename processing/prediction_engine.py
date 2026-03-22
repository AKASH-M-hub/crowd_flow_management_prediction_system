from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Sequence

import numpy as np


@dataclass
class PredictionSnapshot:
    current_count: int
    future_count: int
    delta: int
    incoming_raw: bool
    incoming: bool
    incoming_threshold: int
    incoming_streak: int
    confidence_percent: float
    incoming_probability_percent: float
    alert_score: float
    gate_reason: str
    action_recommendation: str
    risk_hint: str
    nn_pred: int
    nn_ready: bool
    prediction_mode: str


def load_metrics_txt(metrics_path: str) -> Dict[str, float]:
    out: Dict[str, float] = {}
    try:
        with open(metrics_path, "r", encoding="utf-8") as f:
            for line in f:
                if ":" not in line:
                    continue
                key, value = line.strip().split(":", 1)
                key = key.strip()
                value = value.strip()
                try:
                    out[key] = float(value)
                except ValueError:
                    continue
    except FileNotFoundError:
        return out
    return out


def _stability_score(count_history: Sequence[int]) -> float:
    if len(count_history) < 8:
        return 0.5
    window = np.array(count_history[-12:], dtype=np.float32)
    mean_val = float(np.mean(window))
    if mean_val <= 0:
        return 0.5
    cv = float(np.std(window) / mean_val)
    return float(max(0.0, min(1.0, 1.0 - cv)))


def _metrics_reliability(metrics: Dict[str, float]) -> float:
    if not metrics:
        return 0.55

    mape = float(metrics.get("mape_percent", 30.0))
    mae = float(metrics.get("mae", 5.0))

    mape_score = max(0.0, min(1.0, 1.0 - (mape / 50.0)))
    mae_score = max(0.0, min(1.0, 1.0 - (mae / 10.0)))
    return 0.65 * mape_score + 0.35 * mae_score


def _risk_hint(delta: int, confidence_percent: float) -> str:
    if delta >= 8 and confidence_percent >= 70:
        return "STRONG_INCREASE"
    if delta >= 4 and confidence_percent >= 55:
        return "LIKELY_INCREASE"
    if delta <= -4 and confidence_percent >= 55:
        return "LIKELY_DROP"
    return "STABLE"


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))


def _gate_reason(
    prediction_active: bool,
    nn_ready: bool,
    delta: int,
    incoming_threshold: int,
    confidence_percent: float,
    min_confidence_percent: float,
    incoming_streak: int,
    min_streak: int,
) -> str:
    if not prediction_active:
        return "BEFORE_10_PERCENT"
    if not nn_ready:
        return "NN_NOT_READY"
    if delta < incoming_threshold:
        return "DELTA_BELOW_THRESHOLD"
    if confidence_percent < min_confidence_percent:
        return "CONFIDENCE_TOO_LOW"
    if incoming_streak < min_streak:
        return "STREAK_NOT_MET"
    return "PASS"


def _action_recommendation(incoming: bool, incoming_raw: bool, confidence_percent: float, delta: int) -> str:
    if incoming and confidence_percent >= 75 and delta >= 6:
        return "INTERVENE"
    if incoming:
        return "PREPARE"
    if incoming_raw:
        return "WATCH"
    return "NORMAL"


def build_prediction_snapshot(
    current_count: int,
    nn_pred: int,
    count_history: Sequence[int],
    metrics: Dict[str, float],
    prediction_active: bool,
    nn_ready: bool,
    incoming_streak: int,
    min_confidence_percent: float,
    min_streak: int,
) -> PredictionSnapshot:
    future_count = max(0, int(nn_pred)) if nn_ready and prediction_active else current_count

    delta = int(future_count - current_count)
    incoming_threshold = max(3, int(round(current_count * 0.15)))

    reliability = _metrics_reliability(metrics)
    stability = _stability_score(count_history)
    confidence_percent = float(round((0.62 * reliability + 0.38 * stability) * 100.0, 1))

    incoming_raw = (
        prediction_active
        and nn_ready
        and delta >= incoming_threshold
        and confidence_percent >= min_confidence_percent
    )
    incoming = incoming_raw and incoming_streak >= min_streak

    threshold_safe = max(1, incoming_threshold)
    alert_score = float(round((delta / threshold_safe) * (confidence_percent / 100.0), 3))
    incoming_probability_percent = float(round(_sigmoid(alert_score) * 100.0, 1))
    gate_reason = _gate_reason(
        prediction_active=prediction_active,
        nn_ready=nn_ready,
        delta=delta,
        incoming_threshold=incoming_threshold,
        confidence_percent=confidence_percent,
        min_confidence_percent=min_confidence_percent,
        incoming_streak=incoming_streak,
        min_streak=min_streak,
    )
    action_recommendation = _action_recommendation(
        incoming=incoming,
        incoming_raw=incoming_raw,
        confidence_percent=confidence_percent,
        delta=delta,
    )
    risk_hint = _risk_hint(delta, confidence_percent)

    return PredictionSnapshot(
        current_count=current_count,
        future_count=future_count,
        delta=delta,
        incoming_raw=incoming_raw,
        incoming=incoming,
        incoming_threshold=incoming_threshold,
        incoming_streak=incoming_streak,
        confidence_percent=confidence_percent,
        incoming_probability_percent=incoming_probability_percent,
        alert_score=alert_score,
        gate_reason=gate_reason,
        action_recommendation=action_recommendation,
        risk_hint=risk_hint,
        nn_pred=nn_pred,
        nn_ready=nn_ready,
        prediction_mode="NN_ONLY_DEMO" if nn_ready else "NN_WARMUP_OR_UNAVAILABLE",
    )
