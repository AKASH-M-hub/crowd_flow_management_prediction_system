import csv
import math
import os
from typing import Dict, List, Optional

EARTH_RADIUS_M = 6371008.8


def _to_radians(coords: List[Dict[str, float]]) -> List[Dict[str, float]]:
    out = []
    for point in coords:
        out.append({"lat": math.radians(float(point["lat"])), "lng": math.radians(float(point["lng"]))})
    return out


def haversine_distance_m(lat1_deg: float, lon1_deg: float, lat2_deg: float, lon2_deg: float) -> float:
    lat1 = math.radians(lat1_deg)
    lon1 = math.radians(lon1_deg)
    lat2 = math.radians(lat2_deg)
    lon2 = math.radians(lon2_deg)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2.0) ** 2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return EARTH_RADIUS_M * c


def polygon_perimeter_m(coords: List[Dict[str, float]]) -> float:
    if len(coords) < 3:
        return 0.0

    perimeter = 0.0
    for i in range(len(coords)):
        p1 = coords[i]
        p2 = coords[(i + 1) % len(coords)]
        perimeter += haversine_distance_m(p1["lat"], p1["lng"], p2["lat"], p2["lng"])

    return perimeter


def polygon_area_m2(coords: List[Dict[str, float]]) -> float:
    if len(coords) < 3:
        return 0.0

    rad = _to_radians(coords)
    total = 0.0
    for i in range(len(rad)):
        p1 = rad[i]
        p2 = rad[(i + 1) % len(rad)]

        dlon = p2["lng"] - p1["lng"]
        while dlon > math.pi:
            dlon -= 2.0 * math.pi
        while dlon < -math.pi:
            dlon += 2.0 * math.pi

        total += dlon * (2.0 + math.sin(p1["lat"]) + math.sin(p2["lat"]))

    area = abs(total) * (EARTH_RADIUS_M ** 2) / 2.0
    return area


def polygon_centroid(coords: List[Dict[str, float]]) -> Dict[str, float]:
    if not coords:
        return {"lat": 0.0, "lng": 0.0}

    lat_sum = 0.0
    lng_sum = 0.0
    for point in coords:
        lat_sum += float(point["lat"])
        lng_sum += float(point["lng"])

    n = float(len(coords))
    return {
        "lat": lat_sum / n,
        "lng": lng_sum / n,
    }


def capacity_levels(area_m2: float) -> Dict[str, int]:
    low = int(area_m2 * 1.0)
    medium = int(area_m2 * 2.0)
    high = int(area_m2 * 4.0)
    return {
        "low_density_capacity": low,
        "safe_capacity": medium,
        "maximum_capacity": high,
    }


def effective_capacity_model(area_m2: float, perimeter_m: float) -> Dict[str, float]:
    if area_m2 <= 0.0:
        return {
            "gross_area_m2": 0.0,
            "edge_buffer_loss_m2": 0.0,
            "flow_corridor_loss_m2": 0.0,
            "safety_clearance_loss_m2": 0.0,
            "usable_area_m2": 0.0,
            "usable_ratio": 0.0,
            "comfort_capacity": 0,
            "safe_capacity": 0,
            "dense_capacity": 0,
            "critical_capacity": 0,
            "recommended_max_capacity": 0,
            "density_profile_ppm2": {
                "comfort": 1.2,
                "safe": 2.0,
                "dense": 3.0,
                "critical": 4.0,
            },
        }

    # Edge buffer approximates unusable band near boundaries/walls/fences.
    edge_buffer_width_m = 0.75
    edge_buffer_loss_m2 = min(area_m2 * 0.35, perimeter_m * edge_buffer_width_m)

    # Reserve area for movement corridors and emergency access.
    flow_corridor_loss_m2 = area_m2 * 0.12

    # Reserve operational safety margin.
    safety_clearance_loss_m2 = area_m2 * 0.08

    blocked_area = edge_buffer_loss_m2 + flow_corridor_loss_m2 + safety_clearance_loss_m2
    usable_area_m2 = max(0.0, area_m2 - blocked_area)
    usable_ratio = usable_area_m2 / area_m2 if area_m2 > 0 else 0.0

    density_profile = {
        "comfort": 1.2,
        "safe": 2.0,
        "dense": 3.0,
        "critical": 4.0,
    }

    comfort_capacity = int(usable_area_m2 * density_profile["comfort"])
    safe_capacity = int(usable_area_m2 * density_profile["safe"])
    dense_capacity = int(usable_area_m2 * density_profile["dense"])
    critical_capacity = int(usable_area_m2 * density_profile["critical"])

    return {
        "gross_area_m2": round(area_m2, 2),
        "edge_buffer_loss_m2": round(edge_buffer_loss_m2, 2),
        "flow_corridor_loss_m2": round(flow_corridor_loss_m2, 2),
        "safety_clearance_loss_m2": round(safety_clearance_loss_m2, 2),
        "usable_area_m2": round(usable_area_m2, 2),
        "usable_ratio": round(usable_ratio, 4),
        "comfort_capacity": comfort_capacity,
        "safe_capacity": safe_capacity,
        "dense_capacity": dense_capacity,
        "critical_capacity": critical_capacity,
        "recommended_max_capacity": safe_capacity,
        "density_profile_ppm2": density_profile,
    }


def risk_status(value: int, capacities: Dict[str, int]) -> str:
    low = capacities["low_density_capacity"]
    safe = capacities["safe_capacity"]
    maximum = capacities["maximum_capacity"]

    if value <= low:
        return "SAFE"
    if value <= safe:
        return "MEDIUM"
    if value <= maximum:
        return "HIGH"
    return "OVERCROWD"


def risk_status_advanced(value: int, model: Dict[str, float]) -> str:
    comfort = int(model["comfort_capacity"])
    safe = int(model["safe_capacity"])
    dense = int(model["dense_capacity"])
    critical = int(model["critical_capacity"])

    if value <= comfort:
        return "SAFE"
    if value <= safe:
        return "MEDIUM"
    if value <= dense:
        return "HIGH"
    if value <= critical:
        return "VERY_HIGH"
    return "OVERCROWD"


def evaluate_zone(coords: List[Dict[str, float]], current_count: int, predicted_count: int) -> Dict:
    area = polygon_area_m2(coords)
    perimeter = polygon_perimeter_m(coords)
    centroid = polygon_centroid(coords)
    capacities = capacity_levels(area)
    capacity_model = effective_capacity_model(area, perimeter)

    current_risk = risk_status_advanced(current_count, capacity_model)
    predicted_risk = risk_status_advanced(predicted_count, capacity_model)
    combined_value = max(current_count, predicted_count)
    overall_risk = risk_status_advanced(combined_value, capacity_model)

    return {
        "area_m2": round(area, 2),
        "perimeter_m": round(perimeter, 2),
        "capacities": capacities,
        "capacity_model": capacity_model,
        "current_count": int(current_count),
        "predicted_count": int(predicted_count),
        "current_risk": current_risk,
        "predicted_risk": predicted_risk,
        "overall_risk": overall_risk,
        "centroid": {
            "lat": round(centroid["lat"], 7),
            "lng": round(centroid["lng"], 7),
        },
        "coordinates_count": len(coords),
        "data_flow": "Google Maps -> Area Calculation -> Capacity Estimation -> AI Prediction -> Display",
    }


def _safe_int(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def load_latest_ai_prediction(csv_path: str) -> Optional[Dict]:
    if not os.path.exists(csv_path):
        return None

    latest = None
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            latest = row

    if latest is None:
        return None

    return {
        "current_count": _safe_int(latest.get("current_count"), 0),
        "future_count": _safe_int(latest.get("future_count"), 0),
        "confidence_percent": _safe_float(latest.get("confidence_percent"), 0.0),
        "incoming": bool(_safe_int(latest.get("incoming"), 0)),
        "prediction_mode": latest.get("prediction_mode", "UNKNOWN"),
        "risk_hint": latest.get("risk_hint", "UNKNOWN"),
        "elapsed_percent": _safe_float(latest.get("elapsed_percent"), 0.0),
        "status": latest.get("status", "UNKNOWN"),
        "source_file": csv_path,
    }
