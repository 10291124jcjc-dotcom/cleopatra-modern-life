# 04 · 即梦生成 / Generating in Jimeng (Seedance)

[中文](#中文) · [English](#english)

## 中文

我们用的是即梦网页版的 Seedance 2.5 视频生成。

### 设置

| 项 | 怎么选 |
|---|---|
| 模式 | 上传参考图、提示词里能用 `@图片1` 引用的模式 |
| 上传 | **只传人物参考图**（@图片1），**不传首帧图** |
| 比例 | 4:3 |
| 时长 | **和提示词里写的秒数一致**：写到 6 秒选 6 秒，写到 8 秒选 8 秒 |
| 清晰度 | 先 480p 试；满意了用「超清」放大**同一条**，不要重新生成 |
| 声音 | 保留，Seedance 自带的现场声后面会垫在音乐下面 |
| 提示词 | 打开 `prompts/NN_*.txt`，复制「以下整段复制到即梦」那条分隔线**以下的全部内容** |

### 时长一定要选对

我们做埃及女王时 8 条都选了 5 秒，但提示词写的是 6 秒和 8 秒。结果动作被压缩，08 地毯那条写了 4 个机位，最关键的「地毯滚开、女王坐起来」被跳过了，女王直接从画面下方升起来，反转不清楚。

### 生成完逐条检查

`python scripts/review_clips.py <EP>` 会给每条出一张缩略条（每 0.5 秒一帧），并检测 Seedance 在片段里切了几个机位。对着检查：

- [ ] 是不是同一个主角？
- [ ] 写的 3 个机位都出来了吗？（脚本会提示「只检测到 2 个」）
- [ ] 结果拍到了吗？
- [ ] 有没有乱码文字、真实商标？
- [ ] 有没有人正对镜头？
- [ ] 时长对不对？（脚本会提示「比提示词短」）

不合格就用同一条提示词再生成一次；改提示词时只改出问题的那个机位。

### 下载后放哪

存成 `clips/NN_名字.mp4`（每条提示词文件开头写了文件名）。

---

## English

We used Seedance 2.5 video generation on the Jimeng website.

### Settings

| Setting | Choice |
|---|---|
| Mode | the one where you upload reference images and refer to them as `@图片1` in the prompt |
| Upload | **only the character reference** (@图片1) — **no first frame** |
| Aspect | 4:3 |
| Duration | **match the prompt**: if it is written up to 6 s pick 6 s, up to 8 s pick 8 s |
| Quality | test at 480p; when happy, upscale **the same take**, don't regenerate |
| Sound | keep it; Seedance's own ambience goes under the song later |
| Prompt | open `prompts/NN_*.txt` and copy **everything below the divider line** ("以下整段复制到即梦 / copy everything below into Jimeng") |

### Get the duration right

We picked 5 s for all eight Cleopatra clips although the prompts were written for 6 and 8 s. The actions got squeezed, and the 4-angle carpet clip skipped its key beat (the rug rolling open and the queen sitting up).

### Check every clip

`python scripts/review_clips.py <EP>` makes a contact strip per clip (one frame every 0.5 s) and counts the angles Seedance cut to. Check: same lead? all angles there? result on screen? no garbled text or real logos? nobody facing the lens? right length? If not, regenerate with the same prompt; when you edit a prompt, change only the angle that failed.

### Where downloads go

Save each one as `clips/NN_name.mp4` (the file name is at the top of each prompt file).
