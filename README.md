# Programming Learning Coach

> 一个不直接交付答案的编程学习 Skill，用于 Python 练习、调试、复习和小型项目学习。

`programming-learning-coach` 的目标不是立刻替你写完代码，而是帮助学习者建立可重复的学习闭环：读代码、预测、亲自运行、看输出、调试，并解释代码的 Input / Process / Output。

[English README](README.en.md)

## 它解决什么问题

编程助手可以很快修复问题，但这有时会跳过学习过程。学习者拿到了答案，却没有真正掌握如何读代码、定位错误和验证理解。

这个 Skill 会把学习过程固定下来：

1. 正式学习前先创建一份不含答案的 lesson。
2. 运行代码前先要求学习者预测结果。
3. 以学习者自己运行的输出作为学习证据。
4. 调试时先读错误、定位问题、验证假设，不直接给完整修复代码。
5. 学习者能解释过程或完成迁移练习后，才记录完成状态。

## 适合谁

- 正在学习 Python 基础、控制流、函数、数据结构和文件读写的人。
- 想练习自动化、pandas、CSV、报表或小型项目的人。
- 希望把报错当成学习机会，而不是立刻拿到修复补丁的人。
- 需要积累复习题、概念笔记和项目英语复盘的人。

## 核心能力

| 场景 | Skill 会做什么 |
|---|---|
| 开始一节课 | 教学前创建 lesson 文件，并在首条回复报告绝对路径。 |
| 继续学习 | 先更新 lesson 生命周期和 `lesson-index.json`，再继续。 |
| 编程练习 | 从读代码、预测输出逐步推进到小型迁移练习。 |
| 调试报错 | 引导阅读错误类型、定位行、检查变量、最小复现和一次只改一处。 |
| 复习旧知识 | 从薄弱概念或复习队列中选择内容，并要求新的理解证据。 |
| 重复犯错 | 前两次放入复习队列；同类错误第三次出现时才沉淀为错误参考。 |

## 安装

### 在 Codex 中使用

克隆仓库后，把 Skill 文件夹复制到 Codex Skills 目录：

```bash
git clone <仓库地址>
mkdir -p ~/.codex/skills
cp -R programming-learning-coach ~/.codex/skills/programming-learning-coach
cd ~/.codex/skills/programming-learning-coach
cp WORKSPACE.example.md WORKSPACE.md
```

在 `WORKSPACE.md` 中，把 `workspace_root` 改为自己的学习资料目录绝对路径。`WORKSPACE.md` 是个人本地配置，已被 Git 忽略，不要提交到公开仓库。

其他兼容 Agent Skills 的运行环境也可以使用：将本文件夹复制到其 Skills 目录，再依据 `WORKSPACE.example.md` 创建自己的 `WORKSPACE.md`。

## 它如何工作

### 1. 课前生成学习资料

每次正式学习、复习或学习型调试开始前，Skill 都会在 `lessons/` 创建或更新一份不含答案的 lesson。第一条教学回复必须以如下形式开始：

```text
学习资料已生成：/absolute/path/to/lessons/0001-topic.html
```

lesson 可以包含目标、会用到的概念或函数、Input / Process / Output 目标、预测问题和练习步骤；但不能包含最终答案、完整目标代码或精确最终输出。

### 2. 用证据推进学习

每次只推进一个小概念。Skill 会提出问题或给出一个提示，等待学习者预测、尝试、运行、查看输出和解释。

当学习者说“我懂了”时，Skill 会要求一句解释、一次预测或一个小迁移练习，而不是直接进入下一课。

### 3. 保存学习状态

学习工作区可以逐步包含以下内容：

```text
learning-workspace/
├── CURRENT_LEARNING_STATE.md
├── lessons/
├── lesson-index.json
├── learning-records/
├── concept-notes/
├── practice-records/
├── review-queue/
└── reference/
```

不需要一开始就建立所有目录。根据当前学习阶段按需创建即可。

## 示例提示语

```text
开始今天编程学习。我想练习 Python 字典。
```

```text
我运行 pandas 时出现 KeyError。请带我调试，但先不要直接给完整修复代码。
```

```text
今天复习 Python 函数和 return。
```

```text
先给我生成这节课的 lesson，我要练习文件读写。
```

## 文件说明

| 文件或目录 | 用途 |
|---|---|
| `SKILL.md` | 核心教学、课前生成和调试流程。 |
| `WORKSPACE.example.md` | 本地学习目录的配置模板。 |
| `references/` | 编程教学协议、工作区结构和课件/参考资料规则。 |
| `scripts/create_lesson.py` | 创建不含答案的 HTML lesson 与索引记录。 |
| `scripts/update_lesson.py` | 更新 lesson 的学习阶段状态。 |
| `scripts/rebuild_lesson_index.py` | 为已有 lesson 重建索引。 |
| `scripts/run_preflight_regression.py` | 运行隔离的 Agent 回归测试。 |
| `examples/` | 课件和教学对话示例。 |
| `test-prompts.json` | 人工评估时的行为期望。 |

## 边界

- 这是编程学习教练，不是生产代码交付流程。
- Codex 自己运行代码，不等于学习者已经完成学习。
- 正式教学前必须有真实 lesson 文件，不能只在聊天中写一段课件。
- 课前 lesson 不放完整代码、最终答案或精确目标输出。
- 不负责公开内容、营销文案或社交媒体帖子。
- 只有学习者明确要求时，才提供完整代码。

## 校验

校验 Skill 文件结构：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/programming-learning-coach
```

在已认证且支持非交互运行 Codex CLI 的环境中，可以运行三场景回归测试：

```bash
cd ~/.codex/skills/programming-learning-coach
python3 scripts/run_preflight_regression.py
```

测试会分别创建“新课”“学习型调试”和“复习”三个临时学习目录，并检查 lesson 是否生成、索引是否匹配、首条回复是否先给出路径，以及 lesson 中是否泄漏答案。

## 贡献

欢迎提交 Issue 和 Pull Request。修改时请保持以下原则：聚焦学习行为、保留无答案 lesson 规则，并在行为变化时补充或更新测试。

## 许可证

本项目使用 [MIT License](LICENSE)。
