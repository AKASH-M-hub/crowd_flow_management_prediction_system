import math


def estimate_area_m2(length_m: float, width_m: float, shape: str = "rectangle") -> float:
    if length_m <= 0 or width_m <= 0:
        return 0.0

    shape = shape.lower().strip()
    if shape == "rectangle":
        return length_m * width_m
    if shape == "circle":
        radius = min(length_m, width_m) / 2.0
        return math.pi * radius * radius
    if shape == "ellipse":
        return math.pi * (length_m / 2.0) * (width_m / 2.0)

    raise ValueError("Unsupported shape. Use rectangle, circle, or ellipse.")


def estimate_safe_capacity(area_m2: float, density_ppm2: float = 2.0) -> int:
    if area_m2 <= 0 or density_ppm2 <= 0:
        return 0
    return int(area_m2 * density_ppm2)


def utilization_status(current_count: int, safe_capacity: int) -> str:
    if safe_capacity <= 0:
        return "UNKNOWN"

    ratio = current_count / safe_capacity
    if ratio >= 1.0:
        return "OVER_CAPACITY"
    if ratio >= 0.85:
        return "CRITICAL"
    if ratio >= 0.7:
        return "HIGH"
    if ratio >= 0.5:
        return "MEDIUM"
    return "LOW"
