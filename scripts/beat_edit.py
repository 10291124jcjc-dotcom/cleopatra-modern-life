# -*- coding: utf-8 -*-
"""Step 7b: cut the clips to the beat.

Rules (the same ones we used for the Cleopatra episode):
  * every camera angle Seedance made is kept; only the dead head/tail of each angle is trimmed
  * the song's drop lands on music.drop_at (the strongest cut, e.g. 2.6 s: escalator → sweating worker)
  * every later clip ends on a beat counted from that drop (edit.snap = "half" for half beats); the extra time
    comes off the head of the clip's first angle (usually a slow establishing move, the safest place to cut),
    or off the longest angle when the first one would drop under 1 s
  * the opening clip keeps its head (it carries the drop); its end lands on a beat by trimming the tail
    of its longest angle after the drop
  * song on top, the clips' own sound 10 dB under it; last frame held 0.6 s, picture and sound fade out

usage:
  python scripts/beat_edit.py <episode_dir>                 every version: 4:3 / 9:16, with song / clip sound only
  python scripts/beat_edit.py <episode_dir> --nomusic       only the clip-sound versions (add the song inside the app)
  python scripts/beat_edit.py <episode_dir> --plan          print the cut list, render nothing
needs work/cuts.json (review_clips.py) and, for the song, music.file / music.in / music.bpm (analyze_music.py)
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import duration, ff_escape, has_audio, load_episode  # noqa: E402

FPS = 30
HOLD_END = 0.6
NATIVE_DB = -10
SIZES = {"4:3": (1440, 1080), "16:9": (1920, 1080), "1:1": (1080, 1080)}


def auto_pieces(dur, cuts, head_trim):
    edges = [0.0] + list(cuts) + [round(dur, 3)]
    ps = []
    for i in range(len(edges) - 1):
        a, b = edges[i], edges[i + 1]
        if i > 0:
            a += 0.02                       # skip the switch frame
        if i == 0 and (b - a) - head_trim >= 1.2:   # short first angles keep their head
            a += head_trim
        if b - a > 0.2:
            ps.append([round(a, 3), round(b, 3)])
    return ps


def plan_cut(ep, e):
    cuts = json.load(open(os.path.join(ep, "work", "cuts.json"), encoding="utf-8"))
    ed = e.get("edit", {})
    head = ed.get("head_trim", 0.3)
    mus = e.get("music", {})
    bpm = mus.get("bpm") or 120.0
    step = 60 / bpm / (2 if ed.get("snap") == "half" else 1)
    drop_at = mus.get("drop_at") or 0.0
    shots = {s["id"]: s for s in e["shots"]}
    order = e.get("order") or [s["id"] for s in e["shots"]]

    plan, t = [], 0.0
    for i, sid in enumerate(order):
        s = shots[sid]
        c = cuts.get(sid)
        if not c:
            sys.exit(f"{sid} 没有 work/cuts.json 记录，先跑 review_clips.py / run review_clips.py first")
        ps = [list(p) for p in s["pieces"]] if s.get("pieces") else \
            auto_pieces(c["duration"], c["cuts"], 0.0 if i == 0 else head)
        if i == 0 and len(order) > 1:
            # the opening clip carries the drop, so its head stays; land its end on a beat by trimming the
            # tail of the longest angle that plays after the drop
            end = sum(b - a for a, b in ps)
            cut = (end - drop_at) % step
            starts, acc = [], 0.0
            for a, b in ps:
                starts.append(acc); acc += b - a
            after = [q for q in range(len(ps)) if starts[q] >= drop_at - 0.05] or [len(ps) - 1]
            j = max(after, key=lambda q: ps[q][1] - ps[q][0])
            if ps[j][1] - ps[j][0] - cut >= 0.6:
                ps[j] = [ps[j][0], round(ps[j][1] - cut, 3)]
        if 0 < i < len(order) - 1:
            end = t + sum(b - a for a, b in ps)
            k = int((end - drop_at) // step)
            target = drop_at + k * step
            cut = end - target
            # take it off the head of the first angle; if that angle would get shorter than 1 s,
            # take it off the head of the longest angle instead
            j = 0 if ps[0][1] - ps[0][0] - cut >= 1.0 else max(range(len(ps)), key=lambda q: ps[q][1] - ps[q][0])
            a, b = ps[j]
            ps[j] = [round(max(0.0, a + cut), 3), b]
        d = sum(b - a for a, b in ps)
        plan.append({"id": sid, "file": s["file"], "start": round(t, 3), "pieces": ps})
        t += d
    return plan, t


def render(ep, e, plan, total, vertical, with_song):
    aspect = e.get("aspect", "4:3")
    W, H = SIZES.get(aspect, SIZES["4:3"])
    out_total = total + HOLD_END
    inputs, fc, vl, al = [], [], [], []
    for n, p in enumerate(plan):
        path = os.path.join(ep, p["file"])
        inputs += ["-i", path]
        audio = has_audio(path)
        for a, b in p["pieces"]:
            k = len(vl)
            fc.append(f"[{n}:v]trim={a}:{b},setpts=PTS-STARTPTS,fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1[v{k}]")
            if audio:
                fc.append(f"[{n}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
                          f"afade=t=in:d=0.03,afade=t=out:st={b - a - 0.03:.3f}:d=0.03[a{k}]")
            else:
                fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{b - a:.3f}[a{k}]")
            vl.append(f"[v{k}]"); al.append(f"[a{k}]")
    fc.append("".join(vl) + f"concat=n={len(vl)}:v=1:a=0,tpad=stop_mode=clone:stop_duration={HOLD_END},"
              f"fade=t=out:st={out_total - 0.5:.3f}:d=0.5[vm]")
    if vertical:
        fc.append("[vm]split[fg0][bg0];[bg0]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
                  "boxblur=30:2,eq=brightness=-0.18[bg];[fg0]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2,format=yuv420p[v]")
    else:
        fc.append("[vm]format=yuv420p[v]")
    fc.append("".join(al) + f"concat=n={len(al)}:v=0:a=1,apad=pad_dur={HOLD_END}[nat]")
    if with_song:
        mus = e["music"]
        song = mus["file"] if os.path.isabs(mus["file"]) else os.path.join(ep, mus["file"])
        m_in = mus.get("in", 0.0)
        inputs += ["-i", song]
        fc.append(f"[{len(plan)}:a]atrim={m_in}:{m_in + out_total:.3f},asetpts=PTS-STARTPTS,aresample=48000,"
                  f"aformat=channel_layouts=stereo,apad=whole_dur={out_total:.3f}[mus]")
        fc.append(f"[nat]volume={NATIVE_DB}dB[nat2];[mus][nat2]amix=inputs=2:normalize=0,"
                  f"afade=t=out:st={out_total - 1.5:.3f}:d=1.5,loudnorm=I=-14:TP=-1.5[a]")
    else:
        fc.append(f"[nat]afade=t=out:st={out_total - 0.6:.3f}:d=0.6,loudnorm=I=-16:TP=-1.5[a]")
    name = "%s_%s_%s.mp4" % (e.get("slug", "episode"), "9x16" if vertical else aspect.replace(":", "x"),
                            "song" if with_song else "clipsound")
    out = os.path.join(ep, "final", name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc),
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "slow",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    print("  ->", out)


def main():
    ep = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "."
    e = load_episode(ep)
    plan, total = plan_cut(ep, e)
    print(f"成片 {total + HOLD_END:.2f}s（含结尾定格 {HOLD_END}s）/ total")
    for p in plan:
        d = sum(b - a for a, b in p["pieces"])
        print(f"  {p['start']:6.2f}-{p['start'] + d:6.2f}  {p['id']}  " +
              "  ".join(f"{a:.2f}-{b:.2f}" for a, b in p["pieces"]))
    if "--plan" in sys.argv:
        return
    mus = e.get("music", {})
    song_ok = bool(mus.get("file")) and mus.get("in") is not None and "--nomusic" not in sys.argv
    if mus.get("file") and mus.get("in") is None and "--nomusic" not in sys.argv:
        print("music.in 还没填，先跑 analyze_music.py；这次只出现场声版本 / run analyze_music.py first")
    for vertical in (False, True):
        render(ep, e, plan, total, vertical, with_song=False)
        if song_ok:
            render(ep, e, plan, total, vertical, with_song=True)


if __name__ == "__main__":
    main()
