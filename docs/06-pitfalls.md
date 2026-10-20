# 06 · 踩过的坑 / Pitfalls

[中文](#中文) · [English](#english)

## 中文

### 最大的坑：先出首帧图，再生成视频

我们一开始是这样做的：每个镜头先用 ChatGPT 出一张首帧图，把梗画在图里，再传进即梦做图生视频。看起来很稳，结果：

- **画面太干净**：ChatGPT 出的图是干净的数码画面，Seedance 照着首帧生成，视频也跟着干净，怎么都不像老纪录片
- **运镜很呆**：首帧把构图锁死了，镜头只能在这张图附近小幅推拉，做不出跟拍、甩镜、拔高这些大运镜
- **大多只有一个机位**：一个梗基本从头到尾一个角度

后来做埃及女王时改成：**不传首帧图，只传一张人物参考图，用文字写 3~4 个机位**。运镜、质感、节奏一下就上来了，一条视频里就有交代、高潮、结果三个机位。

**什么时候才需要首帧图**：构图必须非常准确，或者模型怎么都生成不出某个东西时。同一个人要反复出现时，用参考图就够了，不需要首帧。

### 其他的坑

| 坑 | 一开始 | 结果 | 后来 |
|---|---|---|---|
| 质感靠写 grain | 每条提示词写 heavy film grain | ChatGPT 出的图还是很干净 | 写「年代 + 拍摄方式 + 机器缺陷」，不写 grain |
| 质感靠后期加颗粒 | 写脚本统一加颗粒、褪色、柔光 | 像贴了一层滤镜，不像 | 放弃；质感在生成时写，剪映里只轻微调色 |
| 时长选短了 | 提示词写 6~8 秒，生成选了 5 秒 | 动作被压缩，08 的关键反转被跳过 | 时长和提示词写的秒数一致 |
| 表演写得太夸张 | 第一版提示词写了「对镜头挑眉」「自信微笑」 | 拆完参考视频发现原片的人全都一本正经，这样写风格不对 | 生成前改成一本正经、不看镜头 |
| 剪得太狠 | 为了快节奏把每个镜头剪到 2~3 秒 | 铺垫被剪掉，梗看不懂 | 每个机位都保留，只剪头尾 |
| 测错了歌的速度 | 只分析了一段 30 秒的片段，搜索范围设窄了，测成 96 BPM | 一半切点落在两拍之间 | 用整首歌测，`analyze_music.py` 同时比较拍、半小节、一小节的周期，测出 144 BPM |

---

## English

### The big one: making a first frame, then animating it

Our first attempt made a first frame for every shot in ChatGPT with the gag drawn in, then animated it in Jimeng. It looked safe. It wasn't:

- **Too clean**: ChatGPT images are clean digital pictures, Seedance follows the first frame, so the video stayed clean and never looked like old documentary footage
- **Stiff camera**: the first frame locks the composition; the camera can only drift around it — no tracking shots, wipes or drone rises
- **Mostly one angle per gag**

For Cleopatra we switched to **no first frame — one character reference, and 3–4 angles written in text**. Camera, look and pacing all came alive, with setup, payoff and result inside one clip.

**When a first frame is worth it**: only when the composition must be exact, or the model simply can't produce some object. For a recurring character a reference image is enough.

### Other traps

- **Asking for "grain"**: the images stayed clean. Describe era + capture medium + the machine's flaws instead
- **Adding grain in post**: always looked like a pasted filter; we dropped it
- **Picking a shorter duration than the prompt**: actions get squeezed and beats get skipped
- **Over-acted prompts** ("raises an eyebrow at the camera"): the reference is deadpan, so we rewrote them before generating
- **Cutting too hard**: the setups went and the jokes stopped making sense; keep every angle
- **Wrong tempo**: measured on a 30 s excerpt with too narrow a search, we got 96 BPM and half the cuts fell between beats; measured on the whole song and comparing beat / half-bar / bar periodicity, it is 144 BPM

> 小提示：ChatGPT 里「More like a grainy 1990s camcorder frame… Keep everything else.」这种句子是用来改刚出的那张图的，别加进新的出图提示词里，否则在同一个对话里它可能把上一张图的场景沿用过来。
>
> Tip: a line like "…Keep everything else." is for editing the image you just made; don't append it to fresh prompts, or in the same chat ChatGPT may carry the previous scene over.
