import argparse
import glob
import json
import os
from typing import List, Tuple

import cv2

from models.yolo_model import load_model
from processing.crowd_predictor import CrowdPredictor
from processing.detection import detect_people
from processing.video_processing import load_video, read_frame
from prepare_demo_videos import ensure_demo_clips


def extract_series(
    video_path: str,
    model,
    sample_every: int,
    resize_w: int,
    resize_h: int,
) -> Tuple[List[int], List[float], List[float]]:
    cap = load_video(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    counts = []
    densities = []
    elapsed_values = []
    frame_idx = 0
    detection_step = 0

    while True:
        ret, frame = read_frame(cap)
        if not ret:
            break

        frame_idx += 1
        if frame_idx % sample_every != 0:
            continue

        frame = cv2.resize(frame, (resize_w, resize_h))
        detection_step += 1
        use_zoom = detection_step % 2 == 0
        boxes = detect_people(model, frame, use_zoom=use_zoom)

        frame_area = max(1, frame.shape[0] * frame.shape[1])
        box_area_sum = 0
        for x1, y1, x2, y2 in boxes:
            box_area_sum += max(0, x2 - x1) * max(0, y2 - y1)

        density_ratio = min(1.0, box_area_sum / frame_area)
        elapsed_ratio = frame_idx / total_frames if total_frames > 0 else 0.0

        counts.append(len(boxes))
        densities.append(float(density_ratio))
        elapsed_values.append(float(elapsed_ratio))

    cap.release()
    return counts, densities, elapsed_values


def resolve_video_paths(patterns: List[str]) -> List[str]:
    paths = []
    for pattern in patterns:
        paths.extend(glob.glob(pattern))
    unique_paths = sorted(set(paths))
    if not unique_paths:
        raise RuntimeError("No videos matched. Check --videos pattern.")
    return unique_paths


def main():
    parser = argparse.ArgumentParser(description="Train crowd predictor from multiple videos.")
    parser.add_argument(
        "--videos",
        nargs="+",
        default=["data/crowd_videos/*.mp4"],
        help="One or more glob patterns for training videos.",
    )
    parser.add_argument("--sample-every", type=int, default=5, help="Use every Nth frame for training data.")
    parser.add_argument("--resize-w", type=int, default=1366)
    parser.add_argument("--resize-h", type=int, default=768)
    parser.add_argument("--window-size", type=int, default=24)
    parser.add_argument("--horizon-steps", type=int, default=15)
    parser.add_argument("--model-path", default="models/crowd_predictor.joblib")
    parser.add_argument(
        "--prepare-demo",
        action="store_true",
        help="Generate demo training clips from existing videos before training.",
    )
    parser.add_argument("--demo-clips", type=int, default=5, help="Number of demo clips to generate.")
    args = parser.parse_args()

    if args.prepare_demo:
        generated = ensure_demo_clips(
            source_pattern="data/crowd_videos/*.mp4",
            output_dir="data/crowd_videos/demo_training",
            target_count=args.demo_clips,
        )
        print(f"Generated/available demo clips: {len(generated)}")
        args.videos = ["data/crowd_videos/demo_training/*.mp4"]

    video_paths = resolve_video_paths(args.videos)
    print("Training videos:")
    for p in video_paths:
        print(f"  - {p}")

    model = load_model()
    all_series = []
    per_video_report = []

    for video_path in video_paths:
        counts, densities, elapsed_values = extract_series(
            video_path,
            model,
            sample_every=args.sample_every,
            resize_w=args.resize_w,
            resize_h=args.resize_h,
        )
        if len(counts) < args.window_size + args.horizon_steps:
            print(f"Skipping {video_path} (too short: {len(counts)} samples)")
            continue

        print(f"{video_path}: {len(counts)} samples")
        all_series.append(
            {
                "counts": counts,
                "densities": densities,
                "elapsed": elapsed_values,
            }
        )
        per_video_report.append(
            {
                "video_path": video_path,
                "samples": len(counts),
                "count_min": int(min(counts)),
                "count_max": int(max(counts)),
                "count_mean": round(float(sum(counts) / len(counts)), 3),
                "density_mean": round(float(sum(densities) / len(densities)), 6),
                "elapsed_start": round(float(elapsed_values[0]), 6),
                "elapsed_end": round(float(elapsed_values[-1]), 6),
            }
        )

    if not all_series:
        raise RuntimeError("No usable training series found.")

    predictor = CrowdPredictor(
        model_path=args.model_path,
        window_size=args.window_size,
        horizon_steps=args.horizon_steps,
    )
    metrics = predictor.fit_from_series_list(all_series)
    predictor.save()

    os.makedirs("models", exist_ok=True)
    metrics_path = os.path.join("models", "crowd_predictor_metrics.txt")
    with open(metrics_path, "w", encoding="utf-8") as f:
        for key, value in metrics.items():
            f.write(f"{key}: {value}\n")

    report_json_path = os.path.join("models", "demo_training_report.json")
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "training_config": {
                    "sample_every": args.sample_every,
                    "resize_w": args.resize_w,
                    "resize_h": args.resize_h,
                    "window_size": args.window_size,
                    "horizon_steps": args.horizon_steps,
                    "model_path": args.model_path,
                },
                "metrics": metrics,
                "videos": per_video_report,
            },
            f,
            indent=2,
        )

    series_json_path = os.path.join("models", "demo_training_series.json")
    with open(series_json_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "training_config": {
                    "sample_every": args.sample_every,
                    "resize_w": args.resize_w,
                    "resize_h": args.resize_h,
                    "window_size": args.window_size,
                    "horizon_steps": args.horizon_steps,
                    "model_path": args.model_path,
                },
                "series": all_series,
            },
            f,
            indent=2,
        )

    report_csv_path = os.path.join("models", "demo_training_report.csv")
    with open(report_csv_path, "w", encoding="utf-8") as f:
        f.write("video_path,samples,count_min,count_max,count_mean,density_mean,elapsed_start,elapsed_end\n")
        for row in per_video_report:
            f.write(
                f"{row['video_path']},{row['samples']},{row['count_min']},{row['count_max']},{row['count_mean']},{row['density_mean']},{row['elapsed_start']},{row['elapsed_end']}\n"
            )

    print("Training completed.")
    print(f"Model saved to: {args.model_path}")
    print(f"Metrics saved to: {metrics_path}")
    print(f"Demo report saved to: {report_json_path}")
    print(f"Demo report CSV saved to: {report_csv_path}")
    print(f"Series archive saved to: {series_json_path}")
    print(f"Metrics: {metrics}")


if __name__ == "__main__":
    main()
