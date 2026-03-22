import glob
import os
from typing import List

import cv2


def _read_video_info(path: str):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        return None
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    if fps <= 0 or frame_count <= 0 or width <= 0 or height <= 0:
        return None
    return fps, width, height, frame_count


def _write_clip(source: str, output: str, start_frame: int, clip_frames: int) -> bool:
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        return False

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output, fourcc, fps if fps > 0 else 25.0, (width, height))

    cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, start_frame))

    written = 0
    while written < clip_frames:
        ret, frame = cap.read()
        if not ret:
            break
        writer.write(frame)
        written += 1

    cap.release()
    writer.release()
    return written > 0


def ensure_demo_clips(
    source_pattern: str = "data/crowd_videos/*.mp4",
    output_dir: str = "data/crowd_videos/demo_training",
    target_count: int = 5,
    clip_seconds: int = 20,
) -> List[str]:
    os.makedirs(output_dir, exist_ok=True)

    existing = sorted(glob.glob(os.path.join(output_dir, "demo_clip_*.mp4")))
    if len(existing) >= target_count:
        return existing[:target_count]

    source_videos = sorted(glob.glob(source_pattern))
    source_videos = [p for p in source_videos if output_dir not in p.replace("\\", "/")]
    if not source_videos:
        return existing

    next_idx = len(existing)

    for src in source_videos:
        info = _read_video_info(src)
        if info is None:
            continue

        fps, _, _, frame_count = info
        clip_frames = max(1, int(fps * clip_seconds))
        if frame_count <= clip_frames:
            segments = [0]
        else:
            step = max(1, (frame_count - clip_frames) // 2)
            segments = [0, step, min(frame_count - clip_frames, step * 2)]

        for start_frame in segments:
            if next_idx >= target_count:
                break
            out_path = os.path.join(output_dir, f"demo_clip_{next_idx + 1:02d}.mp4")
            ok = _write_clip(src, out_path, start_frame=start_frame, clip_frames=clip_frames)
            if ok:
                next_idx += 1

        if next_idx >= target_count:
            break

    return sorted(glob.glob(os.path.join(output_dir, "demo_clip_*.mp4")))[:target_count]


if __name__ == "__main__":
    clips = ensure_demo_clips()
    print(f"Demo clips ready: {len(clips)}")
    for c in clips:
        print(c)
