# Prediction Output Reference (Red Panel + Files)

This document explains all possible prediction outcomes shown in the red panel and stored in local result files.

## 1) Main Goal of Prediction

The prediction module answers one operational question:
- Will crowd increase in the upcoming instance (near future horizon) or not?

The displayed decision is:
- Upcoming Crowd: YES
- Upcoming Crowd: NO

This decision is generated only from the trained NN path after progress passes 10%.

## 2) Red Panel Fields and Meaning

- Current: current crowd estimate from tracked detections
- Future: predicted near-future crowd from NN
- Delta: Future - Current
- Upcoming Crowd: final YES or NO decision
- Gate: PASS or HOLD
- Confidence: confidence score from model reliability and temporal stability
- Incoming Probability: probability score derived from alert score
- Trend: STRONG_INCREASE / LIKELY_INCREASE / LIKELY_DROP / STABLE
- Mode: NN_ONLY_DEMO or NN_WARMUP_OR_UNAVAILABLE
- State: ACTIVE or WARMUP
- Threshold: minimum delta required to consider incoming crowd
- Streak: consecutive raw-pass count used to suppress false alerts
- Score: normalized confidence-weighted alert score
- Gate Reason: reason for PASS/HOLD decision
- Recommended Action: NORMAL / WATCH / PREPARE / INTERVENE
- Started at X%: video progress marker

## 3) Possible Decision States

### A) Upcoming Crowd: NO, Gate HOLD
Typical reasons:
- before 10% progress
- NN not ready yet
- delta below threshold
- confidence below minimum
- streak not yet sufficient

### B) Upcoming Crowd: YES, Gate PASS
Conditions:
- active prediction phase (>10%)
- NN ready
- delta >= dynamic threshold
- confidence >= configured minimum
- streak >= configured minimum

## 4) False Alert Reduction Logic

The final YES decision uses multiple gates:
1. confidence gate
2. delta threshold gate
3. consecutive streak gate

This avoids one-frame spikes becoming alerts.

## 5) Local Result Files (Simultaneous Storage)

### 5.1 CSV stream
- File: prediction_output_log.csv
- Purpose: tabular frame-level prediction records

### 5.2 JSONL stream
- File: prediction_output_log.jsonl
- Purpose: structured machine-readable logs with all prediction fields

### 5.3 Alert events
- File: prediction_alert_events.txt
- Purpose: event-level records when final incoming signal turns from NO to YES

## 6) Quick Reading Guide

If you need one quick interpretation from panel/log:
- Upcoming Crowd = YES and Recommended Action = PREPARE/INTERVENE means crowd build-up is likely in upcoming horizon.
- Upcoming Crowd = NO or Gate HOLD means no validated incoming signal yet.
