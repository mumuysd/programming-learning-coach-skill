<sub>🌐 <b>中文</b> · <a href="README.en.md">English</a></sub>

# Programming Learning Coach

一个面向 Python、自动化、Web 开发与项目练习的编程学习 Skill。它不是“立刻给出完整代码”的助手，而是把学习过程固定为：先生成资料，先讲清新知识，再让学习者预测、亲自运行、检查结果并解释。

它的目标是帮助学习者系统提升编程水平，而不是把一次跑通包装成“已经学会”。

## 它解决什么问题

普通编程助手很擅长直接修复报错或补齐代码，但这会跳过几个真正决定学习效果的步骤：代码到底在处理什么输入？为什么会报错？换一个输入还能不能判断？结果能证明什么、不能证明什么？

`programming-learning-coach` 会把这些步骤变成一节小课：

```text
可信资料或现有代码
→ 生成无答案 lesson
→ 讲清一个具体新知识
→ 预测
→ 学习者亲自运行或检查
→ 解释 Input / Process / Output
→ 记录证据与下一次复习
```

## 它怎样教

| 场景 | 行为 |
| --- | --- |
| 学一个新概念 | 在 lesson 中先给出核心解释、判断规则、对照案例和运行/推理机制，再进入练习。 |
| 学 FastAPI、pandas 等库 | 优先使用 `RESOURCES.md` 中登记的官方文档；没有资料时，先补齐来源再引用事实性内容。 |
| 继续旧课 | 比较 lesson 与已有证据，只推进尚未完成的部分；不因 checkpoint 未结束就重复整课。 |
| 遇到报错 | 训练读错误类型、定位行、检查变量、最小复现、一次只改一处。 |
| 说“我懂了” | 用解释、预测或小迁移练习确认，而不是直接跳到下一节。 |
| 同类错误反复出现 | 前两次放入复习队列；同一根因累计三次才生成可复用参考。 |

新知识课不会把概念定义、函数清单或练习步骤伪装成讲解。它至少要有两段实质解释、一条判断规则、两个对照案例和两步机制说明；教学例子必须与练习输入不同，也不会提前写出完成代码、标准答案或最终输出。

## 安装

### 通过 Skills CLI

```bash
npx skills add mumuysd/programming-learning-coach-skill --skill programming-learning-coach
```

### 本地安装到 Codex

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/mumuysd/programming-learning-coach-skill.git ~/.codex/skills/programming-learning-coach
cd ~/.codex/skills/programming-learning-coach
cp WORKSPACE.example.md WORKSPACE.md
```

把 `WORKSPACE.md` 中的 `workspace_root` 改为你的学习工作区绝对路径。该文件是本地配置，已被 Git 忽略，不应提交。

## 开始使用

```text
使用 $programming-learning-coach 开始今天的 Python 学习。我想理解字典里直接取值和 get 的区别。
```

```text
使用 $programming-learning-coach 带我学习 FastAPI 的路径参数、查询参数和请求体。先生成资料并使用官方文档；不要先给完整代码。
```

```text
我遇到了 pandas KeyError。使用 $programming-learning-coach 带我调试，先不要直接给完整修复代码。
```

正式学习开始前，Skill 会先创建 lesson，并在第一条教学回复中报告真实绝对路径：

```text
学习资料已生成：/absolute/path/to/lessons/0001-topic.html
```

## 工作区

最小工作区只需要一个目录。Skill 会按需创建文件，而不会为了模板制造空文档：

```text
learning-workspace/
├── RESOURCES.md                 # 可信资料与使用范围
├── CURRENT_LEARNING_STATE.md    # 当前上下文（可选）
├── lessons/                     # 每节无答案 lesson
├── lesson-index.json            # 生命周期与证据索引
├── learning-records/            # 基于真实证据的学习记录
├── review-queue/                # 薄弱点与复习任务
└── reference/                   # 稳定概念或三次重复错误的参考
```

## 边界

- 这是学习教练，不是默认的生产代码交付流程。
- Agent 自己运行代码不算学习者完成；需要学习者预测、运行或直接检查真实结果，并做自己的解释。
- 没有新知识增量的内容必须诚实标记为练习、复习或迁移验收。
- 不提供投资、交易或收益建议。
- 不生成公开发布文案。

## 验证

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
python3 scripts/run_lesson_regression.py
```

在已登录的 Codex CLI 环境中，还可以运行隔离的 Agent 回归：

```bash
python3 scripts/run_preflight_regression.py --timeout-seconds 420
```

## 贡献

欢迎提交真实的学习场景、错误案例、课程改进和回归用例。请保持两个原则：资料不能泄露当前练习答案；学习完成必须有学习者自己的运行或检查证据。

## License

[MIT License](LICENSE)
