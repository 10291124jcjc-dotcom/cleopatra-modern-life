---
name: cleopatra-modern-life
description: 古人的现代日常：把一个古代人物（埃及女王、罗马角斗士、维京首领……）放进现代日常，做成一条 30 多秒、全程一本正经的 AI 短视频。从拆参考视频、写梗（古代场景 + 现代物件 + 古法对照物 + 结果）、出一张人物参考图、写 3 机位的即梦 Seedance 提示词，到检查生成的片段、测歌找高潮、按节拍自动剪辑出 4:3 / 9:16 两个版本。用户说「做一期 XX 的现代日常」「古人过现代生活」「历史人物做现代事」「埃及女王那种视频」，或者要改已有一期的梗、提示词、剪辑时使用。Make an "ancient person, modern life" AI short end to end: gags, one character reference, multi-angle Seedance prompts, clip review, and a beat-synced edit.
---

# 古人的现代日常 · Ancient people, modern life

一个古代人物，8 个梗，每个梗一条 5~8 秒的视频，每条里有 3 个机位；全程一本正经，像 90 年代电视纪录片里的重演片段；按歌的节拍剪成 30 多秒。

## 0. 先说清楚

- **用户要有**：ChatGPT（出一张人物参考图）、即梦会员（Seedance 2.5 网页版）、剪映（可选，调色）、一首歌的音频文件
- **红线**：不用在世真人、不用近现代政治人物，脸不能像任何真实的人或演员；请求涉及这些时礼貌拒绝，建议换成古人
- **不碰别人的作品**：参考视频只拆规律，不搬画面、不搬梗、不去水印
- **音乐**：不帮用户从网上下载商用歌曲；让用户自己提供音频文件，或者发布时在平台音乐库里加
- 跟用户说话用中文；给用户直接复制发布的文案不带表情

## 工作区

每期一个文件夹 `EP`。`S/` = 本 Skill 的 `scripts/`。先跑 `python S/setup_check.py EP`（检查 ffmpeg / numpy / Pillow，建好文件夹，从 `templates/episode.json` 复制设定）。

```
EP/
  episode.json        本期设定：主角、8 个镜头（梗、对照物、结果、机位）、顺序、音乐、剪辑
  refs/protagonist.png   人物参考图（用户在 ChatGPT 出）
  prompts/            make_prompts.py 生成，用户整段复制
  clips/NN_名字.mp4    用户从即梦下载回来
  music/song.mp3      用户提供
  work/  final/
```

完整示例：`examples/cleopatra/episode.json`（埃及女王，含 8 条真实用过的提示词和成片剪辑表）。

## 流程

### 第 1 步：拆参考视频（用户给了参考视频时）

按 `docs/00-study-reference.md`：找硬切点、每个镜头取首中尾三帧（或 8 帧）看，写「机位、运镜、动作、结果」，归纳成运镜和表演规律，给用户看。用户没给参考视频，就直接用文档里我们已经总结好的规律。

### 第 2 步：写梗（Claude 写，用户确认）

按 `docs/01-gags.md`：**古代场景 + 现代物件 + 古法对照物 + 结果**，6 条规则（每个梗不同类、反差大、主角一本正经、不用参考视频的梗、开场最一眼就懂、结尾用历史典故反转）。先给用户一张 8 行的表（梗 / 对照物 / 结果 / 主要运镜），确认后写进 `episode.json` 的 `shots`。工作区里有往期时，先读往期 `episode.json` 查重。

### 第 3 步：人物参考图（用户在 ChatGPT 出）

按 `docs/02-reference-image.md` 写 `protagonist.ref_prompt`：正面 + 四分之三侧面、纯色背景、原创长相、**不加质感词**。同时填 `protagonist.name / pronoun / match`（match 是「脸、发型、头饰、衣服」这类要和参考图一致的部分）。

### 第 4 步：写镜头和提示词（Claude 写）

按 `docs/03-shots-and-prompts.md`：每条 3 个机位（8 秒写 4 个），按「交代 → 高潮 → 结果」；每个机位写清时间段、机位、运镜、动作、结果；用运镜词表。写进每个 shot 的 `beats`，`duration` 等于最后一个机位的结束秒数。主角换装时写 `ref_line`。然后：

```
python S/make_prompts.py EP
```

它按固定模板拼出 `prompts/00_参考图.txt` 和 `prompts/NN_名字.txt`（参考图说明 + 机位 + 表演句 + 质感句 + 无文字无商标），并检查秒数和时长是否一致。把提示词发给用户。

### 第 5 步：即梦生成（用户）

告诉用户 `docs/04-jimeng.md` 的设置：只传人物参考图、**不传首帧图**、4:3、**时长和提示词一致**、先 480p、满意了超清放大同一条。下载存成 `clips/NN_名字.mp4`。

### 第 6 步：检查片段

```
python S/review_clips.py EP
```

看 `work/review/NN.jpg` 缩略条（每 0.5 秒一帧），对照检查：同一个主角？机位都出来了？结果拍到了？乱码文字、真实商标？有人看镜头？时长对不对？脚本会提示「比提示词短」「机位少了」。不合格的让用户重新生成，只改出问题的机位。

### 第 7 步：按节拍剪辑

```
python S/analyze_music.py EP          # 速度、鼓点进入处、每小节能量 → 写入 music.bpm / in / drop_at
python S/beat_edit.py EP --plan       # 剪辑表
python S/beat_edit.py EP              # 4:3 / 9:16 × 带歌 / 只有现场声
```

- 先确认 `analyze_music.py` 挑的段落是高潮（能量条最长最密的一段），速度不对时（比如把 144 测成 96）手动改 `music.bpm`
- `music.drop_at` 默认是开场片段的第一个机位切点；想换成别的切点就手动填
- 规则：每个机位都保留，只剪头尾；开场不剪开头；其余每条在拍点上衔接；音乐为主、现场声 -10 dB；结尾定格 0.6 秒淡出
- 想手动改某条的入出点，在 shot 里写 `pieces`

调色交给用户在剪映里做（`docs/05-editing.md` 有起步参数）；**不要写脚本后期加颗粒**，试过，像贴滤镜。

### 第 8 步：发布

按 `docs/07-publishing.md`：IG / YouTube 发 9:16「只有现场声」版本，在 App 音乐库里加歌；X 发 4:3。文案不带表情，标注 AI 生成。

## 踩坑

动手前读一遍 `docs/06-pitfalls.md`。最重要的一条：**不要先出首帧图再图生视频**，画面会太干净、运镜会被锁死；只传人物参考图，用文字写多机位。
