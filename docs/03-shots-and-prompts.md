# 03 · 写镜头和提示词 / Shots and prompts

[中文](#中文) · [English](#english)

## 中文

这是整套流程最关键的一步。**不用首帧图**：每条视频只传一张人物参考图，画面、运镜、质感全部用文字写。

### 一条视频 = 3 个机位（8 秒的写 4 个）

按「交代 → 高潮 → 结果」排：

| 机位 | 作用 | 常用写法 | 例子：02 水上摩托 |
|---|---|---|---|
| 机位 1 交代 | 看懂场景和古法对照物 | 全景、超低机位、贴地 / 贴水、从对照物后面拍 | 镜头贴着水面从芦苇船后面拍，摩托从远处冲过来 |
| 机位 2 高潮 | 现代物件真正用起来 | 高速跟拍、特写、无人机视角、遮挡转场 | 水花打满镜头，切到侧面高速跟拍女王 |
| 机位 3 结果 | 看到结果或反应 | 回到对照物、仰拍、推近脸、人走出画面 | 渔夫浑身湿透，一动不动看着她远去 |

### 每个机位必须写清 5 件事

1. **时间段**，精确到 0.5 秒（`0–2 秒`）；各机位首尾相接，最后一个的结束秒数等于时长
2. **机位在哪**：超低 / 贴水 / 贴地 / 过肩 / 帐篷里 / 无人机
3. **镜头怎么动**：推 / 摇 / 平行跟 / 往后退 / 拔高 / 基本固定（不要只写「固定」，见下面的规则）
4. **谁做什么**：写全身动作，写完整
5. **结果**

### 运镜词表

全部来自参考视频和我们实测有效的写法：

超低机位仰拍 · 贴着水面 / 地面拍 · 平行高速跟拍 · 镜头在前面往后退着拍 · 跟着物体往上摇 · 无人机视角拔高 · 越过肩膀拍 · 前景物虚焦挡住画面一侧 · 水花 / 沙子扑满镜头当转场 · 缓慢推近脸

### 固定模板

每条都按这个结构写，`scripts/make_prompts.py` 会从 `episode.json` 自动拼出来：

```
@图片1 是【主角】，【他/她】的【脸、发型、头饰、衣服】和 @图片1 完全一样。

镜头1（0–2 秒）：【机位】，【运镜】，【谁做什么】，【结果】。
镜头2（2–4.5 秒）：……
镜头3（4.5–6 秒）：……

所有人都把这件事当成再平常不过的日常，表情自然、不夸张、不看镜头。
画面质感：看起来像 1990 年代电视历史纪录片里的重演片段，用 16 毫米胶片拍摄。画面偏暖、焦点很软，亮部过曝发白，暗部发灰，宽容度低，颜色淡淡往外渗，镜头手持、偶尔自动对焦来回找。不要高清锐利的现代数码画面，不要电影级调色。无字幕，无文字，无水印，无品牌标志。
```

### 规则

- **第一句永远是参考图说明**，保证每个镜头是同一个人。主角换了装（比如穿上翼装），就在第一句里写明「外面穿了……」
- **秒数加起来等于即梦里选的时长**
- **表演那句、质感那句每条都带，一字不改**
- 质感句里有「镜头手持」，指的是整体手持拍摄的质感；所以机位里**不写「固定机位」，写「基本固定，轻微手持晃动」**，两句就不冲突
- **质感只写「年代 + 拍摄方式 + 机器的缺陷」**，不要写 film grain、grainy、复古滤镜这类词（模型会给你一张干净高清图再套一层假滤镜）
- **每条都写「无文字、无品牌标志」**，防止出现乱码字和真实商标
- 主角**不在**首帧出场的镜头（比如 08 地毯），也照样传参考图，提示词里写她什么时候出现

### 完整例子：02 水上摩托

```
@图片1 是埃及女王，她的脸、假发、金冠、项链和白色长袍和 @图片1 完全一样。

镜头1（0–2 秒）：尼罗河上，两个渔夫坐在一条芦苇小船上慢慢撒网。镜头贴着水面从小船后面拍，远处一个小点越来越近：女王开着一辆现代水上摩托，从小船旁边高速飙过去，激起一大片水花，水花直接打在镜头上。
镜头2（2–4.5 秒）：快艇上的高速跟拍，镜头在女王侧面和她平行飞驰，女王身体前倾压弯，假发上的金珠被风吹得往后飞，表情平静，像在赶路；两岸的棕榈树和泥砖房子快速往后划过。
镜头3（4.5–6 秒）：回到芦苇小船上，两个渔夫浑身湿透，一动不动地看着她远去的方向，其中一个慢慢把脸上的水抹掉。

所有人都把这件事当成再平常不过的日常，表情自然、不夸张、不看镜头。
画面质感：（同上）
```

- 机位 1：**贴水面低机位** + **古法对照物（芦苇船）** + **水花打镜头**（自带转场）
- 机位 2：**平行高速跟拍**，主角表情平静
- 机位 3：**回到对照物看结果**，渔夫一本正经地抹脸

8 条完整提示词在 [`examples/cleopatra/prompts/`](../examples/cleopatra/prompts/)。

---

## English

This is the step that matters most. **No first frame**: each video gets one character reference image; picture, camera and look are all written in text.

### One clip = 3 angles (4 for an 8-second clip)

Ordered **setup → payoff → result**:

| Angle | Job | Typical wording | Example: 02 jet ski |
|---|---|---|---|
| 1 Setup | Show the place and the old-way contrast | wide, very low, at water / ground level, from behind the contrast | camera skims the water behind a reed boat; a jet ski races in from afar |
| 2 Payoff | The modern thing actually in use | fast tracking, close-up, drone view, wipe transition | spray hits the lens, cut to a side-on tracking shot of the queen |
| 3 Result | See the result or the reaction | back to the contrast, low angle, push in on a face, walk out of frame | the fishermen, soaked, stare after her |

### Each angle states five things

1. **Time span**, to 0.5 s (`0–2 秒`); spans run end to end and the last one ends at the clip duration
2. **Camera position**: very low / water level / ground level / over the shoulder / inside the tent / drone
3. **Camera move**: push / tilt or pan / track alongside / pull back / rise / "mostly still" (not "locked off", see the rules)
4. **Who does what**, as a complete full-body action
5. **The result**

### Camera vocabulary

very low angle looking up · skimming the water / ground · fast parallel tracking · leading in front and pulling back · tilting up with an object · drone rising · over the shoulder · out-of-focus foreground blocking one side · spray / sand filling the lens as a transition · slow push-in on a face

### The fixed template

See the Chinese block above; `scripts/make_prompts.py` builds it from `episode.json`. Line by line it says: who @图片1 (image 1) is and that everything must match it · angle 1/2/3 with time spans · "everyone treats this as completely normal, natural, not exaggerated, nobody looks at the camera" · the look: "a reenactment from a 1990s TV history documentary shot on 16 mm film: warm, very soft focus, blown highlights, grey shadows, low dynamic range, colours bleeding slightly, handheld with occasional autofocus hunting; not crisp modern digital, not a cinematic grade; no subtitles, text, watermark or logos".

### Rules

- **The first line is always the reference line**, so every clip shows the same person. If the lead changes clothes (the wingsuit), say so in that line
- **Time spans add up to the duration you pick in Jimeng**
- **The acting line and the look line go in every prompt, word for word**
- The look line says "handheld", meaning the overall handheld feel; so never write "locked-off camera" in an angle — write "mostly still, slight handheld shake" (基本固定，轻微手持晃动) so the two don't contradict
- **Describe the look as era + capture medium + the machine's flaws**, never "film grain", "grainy" or "vintage filter" (you get a clean HD image with a fake filter on top)
- **Always add "no text, no logos"** to avoid garbled lettering and real trademarks
- If the lead is **not** in the opening of a clip (08 carpet), still attach the reference and say when she appears

All eight prompts: [`examples/cleopatra/prompts/`](../examples/cleopatra/prompts/). The prompts are in Chinese because we used Jimeng's Chinese interface; Seedance also accepts English prompts if you translate them.
