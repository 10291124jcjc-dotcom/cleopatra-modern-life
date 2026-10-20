# 埃及艳后的现代日常 · Cleopatra's Modern Life

- `episode.json`：主角、8 个镜头（梗 / 古法对照物 / 结果 / 机位 / 提示词原文）、剪辑顺序、音乐、成片实际用的入出点
- `prompts/`：`make_prompts.py` 从 episode.json 生成的提示词，就是我们在即梦里用的原文

`episode.json` holds the lead, the 8 shots (gag / contrast / result / camera / prompt text), the edit order, the music settings and the in/out points of the final cut. `prompts/` is what `make_prompts.py` generates from it — the exact text we pasted into Jimeng.

生成时我们 8 条都选了 5 秒（提示词写的是 6 和 8 秒），08 地毯的「地毯滚开、女王坐起来」因此被跳过；你做的时候时长要选对。
We picked 5 s for all eight clips although the prompts were written for 6 and 8 s, so clip 08 lost its rug-unrolling beat. Pick the right duration.

视频片段和歌曲不在仓库里。成片见 [`../../assets/demo.mp4`](../../assets/demo.mp4)。
Clips and the song are not included. The finished cut is in `assets/demo.mp4`.
