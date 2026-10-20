# -*- coding: utf-8 -*-
"""Step 6 check: look at every generated clip before editing.

For each shot in episode.json it finds the camera switches Seedance made inside the clip,
and writes a contact strip (one frame every 0.5 s, time stamped) to work/review/NN.jpg.
Results go to work/cuts.json, which beat_edit.py uses to keep every angle.

usage: python scripts/review_clips.py <episode_dir>
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import detect_cuts, duration, has_audio, load_episode, save_json  # noqa: E402


def strip(path, out, step=0.5, w=240):
    dur = duration(path)
    ts = [round(t * step + step / 2, 2) for t in range(int(dur / step))]
    ims = []
    for t in ts:
        r = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(t), "-i", path, "-frames:v", "1",
                            "-vf", f"scale={w}:-2", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
        if r.stdout:
            from io import BytesIO
            im = Image.open(BytesIO(r.stdout)).convert("RGB")
            ImageDraw.Draw(im).rectangle((0, 0, 44, 16), fill=(0, 0, 0))
            ImageDraw.Draw(im).text((3, 2), "%.2f" % t, fill=(255, 220, 0))
            ims.append(im)
    if not ims:
        return
    h = ims[0].height
    o = Image.new("RGB", (w * len(ims), h), "white")
    for i, im in enumerate(ims):
        o.paste(im, (i * w, 0))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    o.save(out, quality=88)


def main():
    ep = sys.argv[1] if len(sys.argv) > 1 else "."
    e = load_episode(ep)
    result = {}
    print("镜头  时长   声音  机位切点 / internal cuts")
    for s in e["shots"]:
        path = os.path.join(ep, s["file"])
        if not os.path.exists(path):
            print(f"{s['id']}  还没有视频 / missing: {s['file']}")
            continue
        dur = duration(path)
        cuts = detect_cuts(path)
        result[s["id"]] = {"file": s["file"], "duration": round(dur, 3), "cuts": cuts}
        strip(path, os.path.join(ep, "work", "review", f"{s['id']}.jpg"))
        want = s.get("duration")
        warn = ""
        if want and dur + 0.2 < want:
            warn = f"  ← 提示词写的是 {want} 秒，生成的只有 {dur:.1f} 秒，动作可能被压缩 / shorter than the prompt"
        n = len(s.get("beats", []))
        if n and len(cuts) + 1 < n:
            warn += f"  ← 提示词写了 {n} 个机位，只检测到 {len(cuts) + 1} 个 / fewer angles than written"
        print(f"{s['id']}   {dur:4.1f}s  {'有' if has_audio(path) else '无'}   {cuts}{warn}")
    save_json(os.path.join(ep, "work", "cuts.json"), result)
    print(f"\n缩略条在 work/review/，切点写入 work/cuts.json / strips in work/review/, cuts in work/cuts.json")


if __name__ == "__main__":
    main()
