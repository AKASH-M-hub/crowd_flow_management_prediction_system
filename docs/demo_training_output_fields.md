# Demo Training Output Fields

This document describes the training outputs created after running the demo-based training command.

## Artifacts
- models/crowd_predictor.joblib: trained neural predictor
- models/crowd_predictor_meta.json: model runtime settings
- models/crowd_predictor_metrics.txt: global validation metrics
- models/demo_training_report.json: detailed training report
- models/demo_training_report.csv: per-video summary for quick review

## Metrics Fields (crowd_predictor_metrics.txt)
- samples: total sliding-window training rows used
- train_samples: rows used for model fitting
- val_samples: rows used for validation
- mae: mean absolute error on validation split
- mape_percent: mean absolute percentage error on validation split

## Per-Video Report Fields (demo_training_report.json / .csv)
- video_path: source video path used in training
- samples: number of sampled frames from that video
- count_min: minimum detected people count among sampled frames
- count_max: maximum detected people count among sampled frames
- count_mean: average detected people count among sampled frames
- density_mean: average frame occupancy ratio from person boxes
- elapsed_start: first elapsed ratio in sampled timeline
- elapsed_end: last elapsed ratio in sampled timeline

## Runtime Prediction Log Fields (prediction_output_log.csv)
- frame: frame index where output was logged
- elapsed_percent: percent of total video completed
- current_count: current crowd estimate
- future_count: NN-only future crowd prediction
- delta: future_count - current_count
- incoming_raw: 1 if raw gate condition passes (before streak filtering)
- incoming: 1 if final incoming signal is active after streak filtering
- incoming_threshold: dynamic delta threshold for incoming detection
- incoming_streak: consecutive raw-pass frames count
- confidence_percent: ensemble confidence heuristic score
- alert_score: confidence-weighted normalized alert strength
- risk_hint: STRONG_INCREASE, LIKELY_INCREASE, LIKELY_DROP, or STABLE
- prediction_mode: NN_ONLY_DEMO or NN_WARMUP_OR_UNAVAILABLE
- nn_pred: neural model prediction
- nn_ready: 1 when NN prediction is active after 10% and warmup window
- density_ratio: current estimated occupancy ratio from detections
- status: system risk status label
