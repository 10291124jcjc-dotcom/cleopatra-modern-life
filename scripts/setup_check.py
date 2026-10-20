# -*- coding: utf-8 -*-
"""Check that ffmpeg / ffprobe / numpy / Pillow are available, and set up an episode folder.

usage: python scripts/setup_check.py [new_episode_dir]
"""
import json
import os
import shutil
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ok = True
for tool in ("ffmpeg", "ffprobe"):
    found = shutil.which(tool)
    print(f"{tool:8s} {'OK  ' + found if found else '缺少 / missing  → https://ffmpeg.org/download.html'}")
    ok &= bool(found)
for mod, pip in (("numpy", "numpy"), ("PIL", "pillow")):
    try:
        __import__(mod)
        print(f"{mod:8s} OK")
    except ImportError:
        print(f"{mod:8s} 缺少 / missing  → pip install {pip}")
        ok = False

if len(sys.argv) > 1:
    ep = sys.argv[1]
    for d in ("refs", "clips", "music", "prompts", "work", "final"):
        os.makedirs(os.path.join(ep, d), exist_ok=True)
    dst = os.path.join(ep, "episode.json")
    if not os.path.exists(dst):
        src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates", "episode.json")
        shutil.copy(src, dst)
        print(f"已建好 {ep}，episode.json 从模板复制 / episode folder created")
    else:
        json.load(open(dst, encoding="utf-8"))
        print(f"{dst} 已存在 / already exists")

sys.exit(0 if ok else 1)
