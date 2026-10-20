# -*- coding: utf-8 -*-
"""Shared helpers: episode loading, ffmpeg wrappers, simple audio/video analysis."""
import json
import os
import shutil
import subprocess
import sys

import numpy as np

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def need(tool):
    if not shutil.which(tool):
        sys.exit(f"缺少 {tool}，请先安装 ffmpeg（含 ffprobe）并加入 PATH / {tool} not found, install ffmpeg first")


def load_episode(ep):
    p = os.path.join(ep, "episode.json")
    if not os.path.exists(p):
        sys.exit(f"找不到 {p} / episode.json not found")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


def duration(path):
    need("ffprobe")
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def has_audio(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return bool(r.stdout.strip())


def gray_frames(path, w=64, h=48, fps=30):
    """All frames as tiny grayscale arrays, for cut detection."""
    need("ffmpeg")
    r = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-vf", f"scale={w}:{h},format=gray",
                        "-r", str(fps), "-f", "rawvideo", "-"], capture_output=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(-1, h, w).astype(np.float32)


def detect_cuts(path, fps=30, thresh=14.0):
    """Hard cuts inside a clip (Seedance switches camera angles on its own). Returns times in seconds."""
    a = gray_frames(path, fps=fps)
    d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
    cuts = []
    for i in range(len(d)):
        local = np.median(d[max(0, i - 6):i + 7])
        if d[i] > thresh and d[i] > 3 * local:
            t = (i + 1) / fps
            if not cuts or t - cuts[-1] > 0.25:      # merge flash frames
                cuts.append(round(t, 2))
    return cuts


def mono(path, sr=22050):
    """Decode any audio/video file to mono float32."""
    need("ffmpeg")
    r = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(sr),
                        "-f", "s16le", "-"], capture_output=True)
    return np.frombuffer(r.stdout, np.int16).astype(np.float32) / 32768, sr


def ff_escape(path):
    """Path usable inside an ffmpeg filter argument (Windows drive colon escaped)."""
    return path.replace("\\", "/").replace(":", "\\:")
