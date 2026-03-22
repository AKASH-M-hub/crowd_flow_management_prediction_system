import glob
import os

import cv2


def build_long_demo(
    input_pattern: str = "data/crowd_videos/demo_training/*.mp4",
    output_path: str = "data/crowd_videos/long_demo.mp4",
    target_seconds: int = 120,
) -> str:
    sources = sorted(glob.glob(input_pattern))
    if not sources:
        raise RuntimeError("No input clips found for long demo generation.")

    first = cv2.VideoCapture(sources[0])
    if not first.isOpened():
        raise RuntimeError(f"Could not open source clip: {sources[0]}")

    fps = first.get(cv2.CAP_PROP_FPS)
    width = int(first.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(first.get(cv2.CAP_PROP_FRAME_HEIGHT))
    first.release()

    if fps <= 0:
        fps = 25.0

    target_frames = int(target_seconds * fps)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    written = 0
    clip_index = 0
    while written < target_frames:
        clip_path = sources[clip_index % len(sources)]
        clip_index += 1

        cap = cv2.VideoCapture(clip_path)
        if not cap.isOpened():
            continue

        while written < target_frames:
            ret, frame = cap.read()
            if not ret:
                break

            if frame.shape[1] != width or frame.shape[0] != height:
                frame = cv2.resize(frame, (width, height))

            writer.write(frame)
            written += 1

        cap.release()

    writer.release()
    return output_path


if __name__ == "__main__":
    output = build_long_demo()
    print(f"Long demo video ready: {output}")
