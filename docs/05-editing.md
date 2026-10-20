# 05 · 按节拍剪辑 / Cutting to the beat

[中文](#中文) · [English](#english)

## 中文

### 剪辑原则

1. **每个机位都保留**，只剪掉每个机位头尾拖沓的零点几秒。铺垫是梗的一部分，剪掉就看不懂了
2. **第一下重拍对准最有冲击力的切点**：埃及女王是第 2.6 秒，扶梯仰拍切到满头大汗的工人
3. **后面每条片段都在拍点上衔接**
4. **顺序**：开场慢镜头配前奏 → 快慢交替（水上摩托、卡丁车这种快的，和得来速、投影这种慢的穿插）→ 结尾反转
5. **混音**：音乐为主，现场声压低 10 dB 垫在下面（水声、引擎声、扬沙声还听得到）
6. **结尾**：最后一帧定格 0.6 秒，画面和声音一起淡出

### 用脚本（推荐）

```bash
python scripts/review_clips.py EP          # 1. 找出每条片段内部的机位切点 → work/cuts.json
python scripts/analyze_music.py EP         # 2. 测歌：速度、鼓点进入处、每小节能量，算出歌从第几秒开始用
python scripts/beat_edit.py EP --plan      # 3. 先看剪辑表
python scripts/beat_edit.py EP             # 4. 出 4 个版本：4:3 / 9:16 × 带歌 / 只有现场声
```

`analyze_music.py` 会打印每小节的能量条，最响、最密的一段就是高潮。它自动挑第一个「安静之后鼓点全部进来」的位置，让它落在 `music.drop_at`（默认是开场片段的第一个机位切点）。

`beat_edit.py` 的规则：
- 开场那条不剪开头（重拍要对准它里面的切点），结尾对到拍点上：从重拍之后最长的机位尾部剪
- 中间每条的结尾对到拍点上：多出来的时间从第一个机位开头剪（多是慢慢推进的交代镜头，剪了最安全）；第一个机位不到 1 秒时，改从最长的机位开头剪
- 9:16 竖屏：4:3 画面放中间，上下用同一画面放大模糊垫底

### 埃及女王的剪辑表

歌：《4 Raws》（EsDeeKid），约 144 BPM，一拍 0.418 秒。歌从第 10.81 秒开始用，第 13.41 秒的第一下重拍落在成片第 2.6 秒。

| 成片时间 | 镜头 | 用的片段（秒） |
|---|---|---|
| 0.00–4.69 | 01 扶梯 | 0.00–2.60 · 2.62–3.61 · 3.95–5.05 |
| 4.69–9.28 | 02 水上摩托 | 0.28–1.43 · 1.60–4.12 · 4.13–5.05 |
| 9.28–13.46 | 04 得来速 | 0.47–1.57 · 1.60–3.50 · 3.87–5.05 |
| 13.46–17.21 | 03 卡丁车 | 1.27–2.60 · 2.62–5.05 |
| 17.21–21.39 | 05 投影 | 0.83–2.17 · 2.19–3.97 · 3.99–5.05 |
| 21.39–25.56 | 06 无人机 | 0.85–4.12 · 4.14–5.05 |
| 25.57–29.32 | 07 翼装 | 0.90–1.77 · 2.14–3.80 · 3.82–5.05 |
| 29.32–33.53 | 08 地毯 | 0.80–2.47 · 2.49–3.80 · 3.82–5.05 |

成片 34.1 秒（含 0.6 秒定格）。

### 用剪映手动剪

1. 先听歌，找到第一下重拍（鼓点全部进来的那一下），在时间线上打标记
2. 把这个标记对准开场片段里最有冲击力的切点
3. 选中音乐，用「踩点」功能自动标出节拍点，片段衔接处对到点上
4. 每条片段只剪机位头尾，别剪中间

### 调色（剪映「调节」，起步参数）

想让画面更接近老纪录片，可以从下面这组参数开始，对着参考画面微调。调好一条后点「应用到全部」，再单独检查偏暗的片段。

| 参数 | 起步值 |
|---|---|
| 色温 | +15 ~ +25 |
| 饱和度 | 0 ~ +5 |
| 对比度 | -10 |
| 高光 | -15 |
| 阴影 | +10 |
| 褪色 | +10 ~ +20 |
| 清晰 / 锐化 | -20 / 0 |
| 颗粒 | +20 ~ +35 |
| 暗角 | +5 |

导出 1080p、30 帧、码率「推荐」以上（码率低了颗粒会变成色块）。

> 我们试过写脚本在后期统一加颗粒、褪色，怎么调都像贴了一层滤镜，最后放弃了。质感主要靠生成时的提示词，剪映里只做轻微调色。

### 音乐版权

仓库不提供歌曲。商用歌曲尽量在 IG / YouTube 的音乐库里添加：上传「只有现场声」的版本，在 App 里选同一段，原声音量调到 20%~30%。直接压进视频的商用歌曲可能被静音、限流，或收益归版权方。

---

## English

### Principles

1. **Keep every angle**; trim only the dead fractions of a second at each angle's head and tail. The setup is part of the joke
2. **Put the song's first big downbeat on the strongest cut** — 2.6 s in Cleopatra, escalator → the sweating worker
3. **Every later clip joins on a beat**
4. **Order**: slow opener on the intro → alternate fast and slow → twist at the end
5. **Mix**: song on top, clip sound 10 dB under it
6. **Ending**: hold the last frame 0.6 s, fade picture and sound together

### With the scripts

Run the four commands above. `analyze_music.py` prints an energy bar per bar of music (the loudest, densest stretch is the chorus) and picks where to start the song so its first drop hits `music.drop_at`. `beat_edit.py` keeps the opener's head (it carries the drop) and lands its end on a beat by trimming the tail of its longest post-drop angle; every middle clip lands on a beat by trimming the head of its first angle (or of its longest angle if the first would drop under 1 s). The 9:16 version centres the 4:3 picture over a blurred, enlarged copy.

### The Cleopatra cut list

Song: "4 Raws" (EsDeeKid), about 144 BPM, 0.418 s per beat, started at 10.81 s so its first downbeat (13.41 s) lands at 2.6 s. Final length 34.1 s. See the table above.

### By hand in CapCut / Jianying

Mark the first downbeat, put it on the opener's strongest cut, use the auto beat-marking (踩点) feature to snap the joins, trim only heads and tails.

### Grading (starting values)

Use the table above as a starting point in CapCut's Adjust panel, apply to all, then fix darker clips individually. Export 1080p 30 fps at the recommended bitrate or higher. We tried adding grain and fade in post with a script; it always looked like a filter pasted on top, so the look has to come from the prompt.

### Music rights

No song is included. Prefer adding commercial songs from the Instagram / YouTube music library: upload the clip-sound version, pick the same section in the app, set the original sound to 20–30%.
