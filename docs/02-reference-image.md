# 02 · 人物参考图 / The character reference

[中文](#中文) · [English](#english)

## 中文

主角每个镜头都出现，所以只做**一张**参考图，用来告诉 Seedance「这个人长这样」。**它不是首帧图**，不决定画面构图和质感，只用来认人。

### 规则

- 正面 + 四分之三侧面并排，纯色背景
- 写清楚：年龄、肤色、脸型、妆、发型、头饰、衣服、首饰
- 必须写「原创长相，不像任何演员或真人」
- 要干净清楚：**不要加颗粒、柔焦、复古这些质感词**，质感在视频提示词里写
- 用 ChatGPT 出（别的出图工具也行），存成 `refs/protagonist.png`

### 我们用的提示词

```
Character reference sheet of one ancient Egyptian queen, front view and three-quarter view side by side on a plain warm beige background. She is in her early thirties, warm olive-brown skin, high cheekbones, calm confident expression, sharp black kohl winged eyeliner, a straight black shoulder-length bob wig with small gold beads, a gold vulture crown with a cobra at the brow, a white pleated linen gown, a broad gold and turquoise collar necklace, gold arm cuffs on both upper arms. An original face, not resembling any actress or real person. Realistic photo, soft natural light, no text.
```

### 套用到别的主角

把中间那段描述换掉就行，结构不变：

```
Character reference sheet of one 【who】, front view and three-quarter view side by side on a plain warm beige background. 【age, skin, face, makeup, hair, headwear, clothes, jewelry】. An original face, not resembling any actor or real person. Realistic photo, soft natural light, no text.
```

### 不做

- 不用在世真人、不用近现代政治人物、不让脸像某个明星或演员
- 只有一个主角时不用三视图、表情图那一套，一张就够

---

## English

The lead appears in every shot, so you make **one** reference image that tells Seedance who this person is. **It is not a first frame**: it does not set the composition or the look, it only identifies the character.

### Rules

- Front view and three-quarter view side by side, plain background
- Spell out age, skin, face, makeup, hair, headwear, clothes, jewelry
- Always say "an original face, not resembling any actor or real person"
- Keep it clean: **no grain, soft focus or vintage words here** — the look goes in the video prompt
- Generate it in ChatGPT (any image tool works) and save it as `refs/protagonist.png`

### Our prompt

See the block above (English). To reuse it for another lead, replace only the description in the middle; keep the structure.

### Don't

- No living people, no modern political figures, no faces that look like a celebrity or actor
- With a single lead you don't need turnarounds or expression sheets — one image is enough
