# Geospatial Intelligence Integration Guide

This guide explains the geospatial intelligence layer integrated with the existing AI system.

## What Was Added

- Google Maps web dashboard with location search and drawing tools
- Polygon/rectangle coordinate capture
- Geospatial area and perimeter calculation from latitude/longitude
- Capacity estimation using density standards
- Live integration with current + predicted crowd outputs from AI logs
- Risk assessment output: SAFE, MEDIUM, HIGH, OVERCROWD
- Reverse geocoding of selected zone centroid (Geocoding API)
- Nearby place profiling around selected zone (Places API)
- Route intelligence from origin to crowd zone (Directions API)

## Data Flow

Google Maps -> Area Calculation -> Capacity Estimation -> AI Prediction -> Display

## Files Added

- geospatial_dashboard.py: Flask backend and API routes
- templates/geospatial_dashboard.html: interactive map UI
- processing/geospatial_intelligence.py: geospatial formulas + risk logic

## APIs

### GET /api/maps/health
Returns configured Google services and API key readiness.

### GET /api/ai/latest
Returns latest AI values from prediction_output_log.csv:
- current_count
- future_count
- confidence_percent
- incoming
- prediction_mode
- risk_hint
- elapsed_percent
- status

### POST /api/geospatial/reverse-geocode
Input:
- coordinates: list of {lat, lng}

Output:
- centroid
- formatted_address
- place_id
- types

### POST /api/geospatial/nearby-places
Input:
- coordinates: list of {lat, lng}
- radius_m (optional, default 300)
- place_type (optional, default transit_station)
- keyword (optional)

Output:
- centroid
- count
- places[] with name, vicinity, rating, location

### POST /api/geospatial/directions
Input:
- origin: {lat, lng}
- destination: {lat, lng} (optional if coordinates provided)
- coordinates: polygon points to derive centroid destination
- mode: walking/driving/bicycling/transit

Output:
- distance_text
- duration_text
- start_address
- end_address

### POST /api/geospatial/evaluate
Input:
- coordinates: list of {lat, lng}
- optional current_count, predicted_count

Output:
- area_m2
- perimeter_m
- capacities:
  - low_density_capacity (1 person/m2)
  - safe_capacity (2 persons/m2)
  - maximum_capacity (4 persons/m2)
- current_risk
- predicted_risk
- overall_risk

## Google APIs To Enable

Enable these in Google Cloud Console for this project key:
- Maps JavaScript API
- Places API
- Geocoding API
- Directions API
- Maps SDK for Android (for mobile app extension)

Note:
- The current implementation is web + Flask backend.
- Android SDK is included for your requested future native Android app integration.

## Capacity Rules

- Low density: 1 person/m2
- Medium/safe density: 2 persons/m2
- High/max density: 4 persons/m2

## Risk Logic

For both current and predicted crowd counts:
- SAFE: count <= low_density_capacity
- MEDIUM: low < count <= safe_capacity
- HIGH: safe < count <= maximum_capacity
- OVERCROWD: count > maximum_capacity

Overall risk uses max(current_count, predicted_count).

## Run Steps

1. Ensure prediction logs exist by running main.py at least once.
2. Install dependencies:
   pip install -r requirements.txt
3. Set Google Maps API key environment variable:
   - Windows PowerShell:
     $env:GOOGLE_MAPS_API_KEY="YOUR_KEY"
4. Run dashboard backend:
   python geospatial_dashboard.py
5. Open browser:
   http://127.0.0.1:5050

## Notes

- This module reads real outputs from your trained system log (prediction_output_log.csv).
- If no AI log exists yet, API returns unavailable and asks to run main.py first.
- Geospatial area uses spherical polygon approximation and perimeter uses Haversine distance.
- Nearby places output helps identify evacuation support points (transport, hospitals, police, etc.).
- Directions output helps response teams estimate access time to the selected zone.
