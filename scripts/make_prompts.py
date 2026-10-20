# -*- coding: utf-8 -*-
"""Step 3–5: turn episode.json into copy-paste prompts.

Writes prompts/00_参考图.txt (for ChatGPT) and prompts/NN_<name>.txt (for Jimeng Seedance, reference-image
mode), every video prompt built from the same fixed template:

  reference line  → who @图片1 is, everything must match it
  镜头1/2/3(/4)   → time span, camera position, camera move, action, result
  acting line     → everyone treats it as normal, deadpan, nobody looks at the camera
  look line       → 1990s TV documentary reenactment on 16 mm film + the machine's flaws
  no text / no watermark / no logos

usage: python scripts/make_prompts.py <episode_dir>
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_episode  # noqa: E402

ACTING = "所有人都把这件事当成再平常不过的日常，表情自然、不夸张、不看镜头。"
LOOK = ("画面质感：看起来像 1990 年代电视历史纪录片里的重演片段，用 16 毫米胶片拍摄。画面偏暖、焦点很软，亮部过曝发白，"
        "暗部发灰，宽容度低，颜色淡淡往外渗，镜头手持、偶尔自动对焦来回找。不要高清锐利的现代数码画面，不要电影级调色。")
TAIL = "无字幕，无文字，无水印，无品牌标志。"


def video_prompt(e, s):
    p = e["protagonist"]
    ref = s.get("ref_line") or f"@图片1 是{p['name']}，{p['pronoun']}的{p['match']}和 @图片1 完全一样。"
    lines = [ref, ""]
    for i, b in enumerate(s["beats"], 1):
        lines.append(f"镜头{i}（{b['t']} 秒）：{b['text']}")
    lines += ["", ACTING, LOOK + s.get("extra", "") + TAIL]
    return "\n".join(lines)


def main():
    ep = sys.argv[1] if len(sys.argv) > 1 else "."
    e = load_episode(ep)
    out = os.path.join(ep, "prompts")
    os.makedirs(out, exist_ok=True)
    p = e["protagonist"]
    with open(os.path.join(out, "00_参考图.txt"), "w", encoding="utf-8") as f:
        f.write("【用在】ChatGPT 出图，只出一次。出来的图存成 refs/protagonist.png\n\n" + p["ref_prompt"] + "\n")
    for s in e["shots"]:
        head = (f"【镜头】{s['id']} {s['name']}　【梗】{s['gag']}\n"
                f"【即梦设置】参考图生视频，只上传 @图片1 = {p['name']}参考图；比例 {e.get('aspect', '4:3')}；"
                f"时长 {s['duration']} 秒（必须和下面写的秒数一致）；先 480p 试\n"
                f"【下载后存成】{s['file']}\n\n")
        with open(os.path.join(out, f"{s['id']}_{s['name']}.txt"), "w", encoding="utf-8") as f:
            f.write(head + video_prompt(e, s) + "\n")
        n = len(s["beats"])
        spans = [b["t"] for b in s["beats"]]
        last = float(spans[-1].split("–")[1])
        warn = "" if abs(last - s["duration"]) < 0.01 else f"  ← 最后一个镜头写到 {last} 秒，时长却是 {s['duration']} 秒"
        print(f"{s['id']} {s['name']}: {n} 个机位，{s['duration']} 秒{warn}")
    print(f"提示词写到 {out}")


if __name__ == "__main__":
    main()
