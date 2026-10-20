# -*- coding: utf-8 -*-
"""Step 7a: read the song before cutting to it.

Finds the tempo, the "drops" (the first heavy downbeat after a quiet part, where the drums come in),
and the energy of every bar, then picks where to start the song so that a drop lands exactly on the
strongest cut of the video (episode.json → music.drop_at, by default the first camera switch of the
opening shot).

usage: python scripts/analyze_music.py <episode_dir> [song.mp3]
writes work/music.json and fills music.bpm / music.in in episode.json if they are empty
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_episode, mono, save_json  # noqa: E402

HOP = 0.01


def envelopes(y, sr):
    hop = int(sr * HOP)
    win = 2048
    n = (len(y) - win) // hop
    frames = np.lib.stride_tricks.sliding_window_view(y, win)[::hop][:n]
    spec = np.abs(np.fft.rfft(frames * np.hanning(win), axis=1))
    flux = np.log1p(spec).sum(1)
    onset = np.maximum(np.diff(flux, prepend=flux[0]), 0)
    rms = np.sqrt((y[:n * hop].reshape(n, hop) ** 2).mean(1))
    return onset, rms


def tempo(onset):
    """Autocorrelation + comb: the true beat also repeats at 2x and 4x (half bar, bar), a 3:2 impostor does not."""
    o = onset - onset.mean()
    ac = np.correlate(o, o, "full")[len(o) - 1:]
    ac = ac / ac[0]

    def at(lag):
        i = lag / HOP
        k = int(i)
        return ac[k] + (ac[k + 1] - ac[k]) * (i - k) if k + 1 < len(ac) else 0.0

    best = None
    for bpm in np.arange(70, 180, 0.05):
        p = 60 / bpm
        score = at(p) + 0.8 * at(2 * p) + 0.6 * at(4 * p) + 0.4 * at(8 * p)
        if best is None or score > best[0]:
            best = (score, bpm)
    bpm = best[1]
    while bpm < 80:
        bpm *= 2
    while bpm > 160:
        bpm /= 2
    return float(bpm)


def find_drops(rms, bar):
    """Where a quiet bar is followed by a loud bar: peaks of (next bar loudness / previous bar loudness),
    each refined to the 10 ms frame where loudness jumps most."""
    nb = int(bar / HOP)
    c = np.concatenate([[0], np.cumsum(rms)])
    idx = np.arange(nb, len(rms) - nb)
    before = (c[idx] - c[idx - nb]) / nb
    after = (c[idx + nb] - c[idx]) / nb
    ratio = after / np.maximum(before, 1e-6)
    loud = after > 0.35 * after.max()
    drops = []
    order = np.argsort(-ratio)
    for j in order:
        if ratio[j] < 2.0:
            break
        if not loud[j]:
            continue
        i = idx[j]
        if any(abs(i * HOP - d) < bar * 2 for d, _ in drops):
            continue
        lo, hi = max(1, i - 30), min(len(rms) - 1, i + 30)
        k = lo + int(np.argmax(np.diff(rms[lo:hi])))
        drops.append((round((k + 1) * HOP, 2), round(float(ratio[j]), 1)))
    return sorted(drops)


def bar_table(rms, anchor, bar, total):
    start = anchor - bar * int(anchor / bar)
    out = []
    t = start
    while t + bar <= total:
        i0, i1 = int(t / HOP), int((t + bar) / HOP)
        out.append((round(t, 2), float(rms[i0:i1].mean())))
        t += bar
    mx = max(e for _, e in out) or 1
    return [(t, round(e / mx, 2)) for t, e in out]


def main():
    ep = sys.argv[1] if len(sys.argv) > 1 else "."
    e = load_episode(ep)
    mus = e.setdefault("music", {})
    song = sys.argv[2] if len(sys.argv) > 2 else mus.get("file")
    if not song:
        sys.exit("episode.json 里 music.file 没填，也没给歌曲路径 / no song given")
    path = song if os.path.isabs(song) else os.path.join(ep, song)
    y, sr = mono(path)
    total = len(y) / sr
    onset, rms = envelopes(y, sr)
    bpm = tempo(onset)
    beat = 60 / bpm
    bar = beat * 4
    drops = find_drops(rms, bar)
    if not drops:
        sys.exit("没找到明显的鼓点进入处，请手动填 music.in / no drop found, set music.in by hand")
    bars = bar_table(rms, drops[0][0], bar, total)

    # where the drop should land in the video
    drop_at = mus.get("drop_at")
    if drop_at is None:
        cuts = {}
        cp = os.path.join(ep, "work", "cuts.json")
        if os.path.exists(cp):
            cuts = json.load(open(cp, encoding="utf-8"))
        first = (e.get("order") or [s["id"] for s in e["shots"]])[0]
        c = cuts.get(first, {}).get("cuts")
        drop_at = c[0] if c else 0.0
    # use the first drop that leaves enough song for the whole video
    need_len = sum(s.get("duration", 5) for s in e["shots"]) * 0.9
    pick = next((d for d, _ in drops if d - drop_at >= 0 and total - (d - drop_at) >= need_len), drops[0][0])
    music_in = round(max(0.0, pick - drop_at), 2)

    print(f"歌曲 / song: {os.path.basename(path)}  {total:.1f}s")
    print(f"速度 / tempo: {bpm:.1f} BPM，一拍 {beat:.3f}s，一小节 {bar:.2f}s")
    print("鼓点进入处 / drops (time, energy jump):", drops)
    print("\n每小节能量（1.0 = 最响）/ energy per bar:")
    for t, en in bars:
        print(f"  {t:7.2f}s  {'#' * int(en * 30):30s} {en:.2f}")
    print(f"\n建议：歌曲从 {music_in:.2f}s 开始用，第 {pick:.2f}s 的鼓点正好落在成片第 {drop_at:.2f}s")
    print(f"suggest: start the song at {music_in:.2f}s so the drop at {pick:.2f}s lands on video {drop_at:.2f}s")

    save_json(os.path.join(ep, "work", "music.json"), {
        "song": song, "duration": round(total, 2), "bpm": round(bpm, 2), "beat": round(beat, 4),
        "drops": drops, "bars": bars, "drop_at": drop_at, "pick": pick, "music_in": music_in})
    changed = False
    if not mus.get("bpm"):
        mus["bpm"] = round(bpm, 2); changed = True
    if mus.get("in") is None:
        mus["in"] = music_in; changed = True
    if mus.get("drop_at") is None:
        mus["drop_at"] = drop_at; changed = True
    if changed:
        save_json(os.path.join(ep, "episode.json"), e)
        print("已写入 episode.json 的 music.bpm / music.in / music.drop_at")


if __name__ == "__main__":
    main()
