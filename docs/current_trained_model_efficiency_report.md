# Current Trained Model Efficiency Report

## 1. Executive Summary

This report consolidates the latest efficiency status of the currently active crowd prediction model.

- Active model has been promoted to the V4-improved configuration.
- Efficiency has improved versus the previous baseline on all tracked benchmark metrics.
- Incoming-event prediction quality is improved, which directly supports better operational alerting.

## 2. Active Model Snapshot

Active artifacts:

- Model file: models/crowd_predictor.joblib
- Model metadata: models/crowd_predictor_meta.json
- Active training metrics: models/crowd_predictor_metrics.txt
- Current evaluation summary: models/reports/current/demo_model_evaluation_summary.md

## 3. Training Efficiency (Validation-Side)

Source: models/crowd_predictor_metrics.txt

- Samples: 3002
- Train samples: 2401
- Validation samples: 601
- Validation MAE: 0.946
- Validation RMSE: 1.487
- Validation MAPE: 32.874%
- Validation incoming accuracy: 90.682%
- Selection target: composite
- Best configuration selected: agg_slim_highreg (hidden layers 80-40)

Interpretation:

- The model generalizes well on validation slices from the prepared training pool.
- Validation incoming accuracy above 90% indicates strong event-direction learning during candidate selection.

## 4. Evaluation Efficiency (Dataset-Level)

Source: models/reports/current/demo_model_evaluation_summary.md

Evaluation scope:

- Demo videos in archive: 13
- Videos evaluated: 13

Average benchmark metrics:

- Average MAE: 2.770
- Average RMSE: 3.214
- Average MAPE: 39.806%
- Average incoming accuracy: 76.736%

Interpretation:

- End-to-end forecast error has reduced compared with the prior active baseline.
- Event/incoming prediction reliability improved and is now more useful for operational decision support.

## 5. Improvement vs Previous Baseline

Source comparison: models/admin/accuracy_comparison_accboost_v4.md

Baseline to current active delta:

- MAE: 2.835 -> 2.770 (improved by 0.065)
- RMSE: 3.277 -> 3.214 (improved by 0.063)
- MAPE: 39.957% -> 39.806% (improved by 0.151%)
- Incoming accuracy: 75.230% -> 76.736% (improved by 1.506%)

Conclusion:

- The active model is better than the previous baseline across all tracked summary metrics.

## 6. Operational Efficiency Impact

Expected practical impact in operations:

- Slightly fewer forecast misses on crowd level transitions.
- Better quality of incoming-event flags and alert confidence behavior.
- Better average stability in decision support for monitoring and escalation.

## 7. Notes and Guardrails

- This report summarizes the current trained state and benchmarked performance currently available in-repo.
- Runtime speed/latency is expected to remain similar because model class and pipeline shape remain comparable.
- For production confidence, continue periodic checks on newly captured unseen videos.

## 8. Final Status

Current model efficiency status: Improved and suitable as active default under present benchmark evidence.
