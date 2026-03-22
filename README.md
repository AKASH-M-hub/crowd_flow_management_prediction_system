# Crowd Flow Management Prediction System

## Current Capabilities
- Person detection and tracking from uploaded video.
- Unique-ID based counting with improved ID consistency.
- Max crowd, average crowd, and risk status output.
- Live overlay with crowd flow and hotspot indicators.

## New Prediction Pipeline (Phase 1)
This project now includes a trainable neural-network crowd predictor.

- Training input: detected crowd count time-series from multiple videos.
- Model: MLP neural network (scikit-learn).
- Output: predicted crowd count after a fixed horizon.
- Runtime behavior: if trained model is unavailable, app falls back to regression.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train Predictor from 4-5 Videos
```bash
python train_crowd_predictor.py --videos data/crowd_videos/*.mp4 --sample-every 5 --window-size 24 --horizon-steps 15
```

If you do not have enough videos, auto-generate 5 demo clips from existing videos:
```bash
python train_crowd_predictor.py --prepare-demo --demo-clips 5 --sample-every 10 --window-size 16 --horizon-steps 8
```

Create a longer demo (for prediction trigger testing on 10% progress):
```bash
python build_long_demo_video.py
```

Artifacts created:
- models/crowd_predictor.joblib
- models/crowd_predictor_metrics.txt

### 3. Run Main App with Prediction
```bash
python main.py
```

If `models/crowd_predictor.joblib` exists, neural prediction is used.
If not, automatic fallback prediction is used.

Runtime prediction starts after an initial analysis warmup (about 10-15 seconds).
Runtime now starts future prediction only after video progress crosses 10% (from the 11th percent onward),
and writes live prediction logs to `prediction_output_log.csv`.

Prediction now uses a hybrid ensemble:
- Neural model prediction
- Trend baseline prediction
- Momentum baseline prediction

The popup displays crowd incoming signal, confidence, and trend hint.

## Documentation
- Training/report field definitions: docs/demo_training_output_fields.md
- Generated report outputs:
	- models/demo_training_report.json
	- models/demo_training_report.csv
	- models/demo5_results_summary.md
	- docs/training_explainability.html

## Capacity Module (Phase 2 Foundation)
Added `processing/location_capacity.py` for location-based capacity estimation:
- Area estimation (rectangle/circle/ellipse)
- Safe capacity estimation based on density rules
- Utilization status (LOW to OVER_CAPACITY)

This module is the base for CCTV + geolocation + capacity-aware forecasting.

## Recommended Next Steps
1. Collect 4-5 representative videos from target location(s).
2. Train and evaluate predictor metrics (MAE, MAPE).
3. Tune `window-size` and `horizon-steps` for 3h/4h operational targets.
4. Add API weather/events features for external influence on crowd build-up.
5. Integrate CCTV stream input and location-wise capacity thresholds.