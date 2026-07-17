<div align="center">

# Programming Learning Coach

**面向 Python 与项目实践的编程学习教练：课前生成学习资料、评估独立完成度、引导预测与实操、训练调试、安排复习，并用真实证据验收学习结果。**

<sub>一个用于 Codex 的 evidence-based programming learning Skill：不只是解释代码，而是要求学习者读、猜、跑、看、讲，把“看懂答案”变成“能自己解决问题”。</sub>

<sub>Keywords: Python learning, programming coach, debugging practice, code review, pandas, automation, active recall, Codex Skill.</sub>

<br>
<br>

![Type](https://img.shields.io/badge/type-Codex%20Skill-111827)
![License](https://img.shields.io/badge/license-MIT-blue)
![Focus](https://img.shields.io/badge/focus-Programming%20Learning-4f46e5)
![Method](https://img.shields.io/badge/method-evidence--based-f59e0b)
![Language](https://img.shields.io/badge/language-ZH%20%2B%20EN-10b981)
![Status](https://img.shields.io/badge/status-MVP-ec4899)
[![GitHub Repo stars](https://img.shields.io/github/stars/mumuysd/programming-learning-coach-skill?style=flat&label=stars)](https://github.com/mumuysd/programming-learning-coach-skill)

[30 秒看懂](#30-秒看懂) · [快速开始](#快速开始) · [前后对比](#一眼看懂它怎么教) · [功能地图](#功能地图) · [验证](#验证) · [English README](README.en.md) · [GitHub](https://github.com/mumuysd/programming-learning-coach-skill)

</div>

---

## 30 秒看懂

| 你给它什么 | 它帮你做什么 |
| --- | --- |
| “我想开始学 Python” | 读取现有学习状态，选一个小目标，先生成不含答案的 lesson。 |
| 一段看不懂的代码 | 让你先读代码、预测输出，再通过小练习验证理解。 |
| 一个报错 | 带你读错误类型、定位行、检查变量、做最小复现，而不是直接丢完整修复代码。 |
| “我懂了” | 让你解释、预测或做一次迁移练习，确认不只是“看起来懂了”。 |
| “我看提示做完了” | 记录当前独立完成度；没有足够证据时不虚报升级。 |
| 想复习旧概念 | 从复习队列和薄弱点中选内容，混入新场景重新练习。 |
| 同一种错误反复出现 | 前两次进入复习队列，第三次才沉淀为可复用的错误参考。 |
| 一次有证据的学习 | 同步更新 lesson、学习记录和当前状态；若配置了学习计划，也同步记录关卡进展。 |

核心流程：

```text
一个小目标
-> 独立完成度基线与当日最低版本
-> 生成无答案 lesson
-> 预测
-> 学习者亲自运行
-> 查看输出或错误
-> Input / Process / Output 解释
-> 小迁移练习或复习
-> 严格验收是否达标
-> 同步 lesson、学习记录与当前状态
-> 如有学习计划，记录进展或推进关卡
```

核心原则：

```text
不把助手运行代码当作学习完成；
不把“我懂了”当作理解证据；
不把完整答案当作默认教学方式。
```

---

## 一眼看懂它怎么教

<table>
  <tr>
    <th width="30%">普通编程助手</th>
    <th width="35%">Programming Learning Coach</th>
    <th width="35%">为什么这样做</th>
  </tr>
  <tr>
    <td>“这是报错，直接把这一行改成这样。”</td>
    <td>“先看错误类型和报错行。你觉得这里的变量现在应该是什么？先打印它，再决定只改哪一处。”</td>
    <td>调试能力来自定位、假设和验证，不是复制一次修复代码。</td>
  </tr>
  <tr>
    <td>“这是字典，用 <code>get</code> 取值。”</td>
    <td>先生成本节会用到的概念与函数清单，再要求预测缺失键、默认值和返回结果。</td>
    <td>课前资料给路线，但不泄漏最终答案；预测暴露真正的理解缺口。</td>
  </tr>
  <tr>
    <td>“懂了就继续下一节。”</td>
    <td>“用自己的话解释 Input / Process / Output，或把同一概念换到一个小场景中再写一次。”</td>
    <td>解释和迁移比点头更能证明理解。</td>
  </tr>
  <tr>
    <td>“这次跑通了，直接加下一个功能。”</td>
    <td>先检查最低版本、代表性正常/异常场景、解释能力和当前独立完成度；不稳定就不加新功能。</td>
    <td>一次跑通不等于功能稳定，更不等于学习者能独立重建。</td>
  </tr>
  <tr>
    <td>每次遇到同类错误都重新解释。</td>
    <td>记录错误模式；同一区域、症状和根因累计三次后，生成长期参考资料。</td>
    <td>把重复犯错转成可复习的个人知识库。</td>
  </tr>
</table>

一句话原则：

```text
提示可以降低门槛；
但学习者必须自己运行、观察和解释，能力才会留下来。
```

---

## 快速开始

### 方式一：直接开始一节课

安装后直接说：

```text
开始今天编程学习。我想练习 Python 字典。
```

或：

```text
我运行 pandas 时出现 KeyError。请带我调试，但先不要直接给完整修复代码。
```

Skill 会先创建学习资料，再开始提问。首条教学回复会包含真实文件路径：

```text
学习资料已生成：/absolute/path/to/lessons/0001-topic.html
```

### 方式二：配置个人学习工作区

克隆仓库后，将 Skill 安装到 Codex：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/mumuysd/programming-learning-coach-skill.git ~/.codex/skills/programming-learning-coach
cd ~/.codex/skills/programming-learning-coach
cp WORKSPACE.example.md WORKSPACE.md
```

在 `WORKSPACE.md` 中，将 `workspace_root` 改成自己的学习资料目录绝对路径。该文件是个人配置，已被 Git 忽略，不应提交到公开仓库。

### 方式三：继续已有学习

在已配置的学习工作区中说：

```text
继续我的编程学习，根据当前学习记录安排下一步。
```

它会读取当前状态、已有 lesson、复习队列和学习记录，选择一个可以在本次完成的小目标。

---

## 功能地图

| Icon | 模块 | 输出 |
| --- | --- | --- |
| 📚 | Lesson Preflight | 无答案 lesson、概念/函数清单、预测题、练习步骤 |
| 🧩 | Small-Step Practice | 读代码、预测输出、填空、改错、小改造、迁移练习 |
| 🐛 | Debugging Coach | 错误类型、定位行、变量检查、最小复现、修复原因 |
| 🔁 | Review Queue | 薄弱点、隔天复习、混入新项目的复习任务 |
| 📏 | Independent Completion | 0-3 级独立完成度、晋级证据、失败后的恢复练习 |
| 🗂 | Lesson Lifecycle | `lesson-index.json`、prepared / in-progress / complete 状态 |
| 📝 | Session Finalization | 同步 lesson、学习记录、当前状态和可选学习计划 |
| 📖 | Reference Builder | 概念笔记和三次重复错误后的长期参考资料 |
| 🌐 | Project English | 完成学习后的一句话、5 个词和 IPO 复盘 |

---

## 它会产生什么

一次正式学习可能逐步形成：

```text
learning-workspace/
├── CURRENT_LEARNING_STATE.md
├── lessons/
│   └── 0001-dictionary-basics.html
├── lesson-index.json
├── learning-records/
├── concept-notes/
├── practice-records/
├── review-queue/
└── reference/
```

不是每次都要生成全部文件。Skill 会根据学习进度按需创建，避免把学习过程变成繁琐的文档工作。

---

## 支持的学习场景

| 方向 | 会重点练什么 |
| --- | --- |
| Python 基础 | 变量、条件、循环、函数、数据结构、模块 |
| 文件与数据 | 文件读写、CSV、JSON、数据清洗、pandas |
| 自动化 | 输入输出、脚本拆分、异常处理、可重复运行 |
| 项目代码 | 读现有代码、拆问题、理解数据流、做小改造 |
| 调试 | traceback、变量状态、最小复现、单点修改、原因解释 |
| 独立完成度 | 从提示完成到需求驱动重建，基于证据晋级 |
| 复习 | 间隔复习、混合练习、薄弱概念和错误模式回看 |
| 项目英语 | 与当天真实代码关联的表达、词汇和 IPO 说明 |

---

## 为什么不只是“编程问答”

普通问答通常是：

```text
提问
-> 给出答案
-> 用户复制运行
-> 结束
```

这个 Skill 多走几步：

```text
这次要练的最小概念是什么？
学习者对它的预测是什么？
真实运行结果说明了什么？
学习者能不能解释，或迁移到新场景？
如果反复卡住，应该复习还是生成长期参考？
当前项目是否稳定到可以增加下一项功能？
学习者现在的独立完成度有没有足够证据升级？
```

因此它不会把：

```text
我运行报错了
```

直接变成：

```text
这是完整修复代码，复制即可。
```

而是倾向于从：

```text
报错是什么类型？
traceback 指向哪一行？
这一行使用的变量现在是什么值？
能不能先用最小输入复现？
```

开始。差异在于：**不只帮你过这一关，也训练你下次自己能过。**

---

## 文件结构

```text
programming-learning-coach/
├── SKILL.md
├── README.md
├── README.en.md
├── WORKSPACE.example.md
├── agents/
├── examples/
├── references/
├── scripts/
└── test-prompts.json
```

详细用途：

| 文件或目录 | 用途 |
|---|---|
| `SKILL.md` | 核心教学、课前生成和调试流程。 |
| `WORKSPACE.example.md` | 本地学习目录配置模板。 |
| `references/` | 教学协议、工作区结构和课件/参考资料规则。 |
| `scripts/create_lesson.py` | 创建无答案 HTML lesson 与索引记录。 |
| `scripts/update_lesson.py` | 更新 lesson 的学习阶段状态。 |
| `scripts/finalize_session.py` | 用一次收尾操作同步学习证据和进度文件。 |
| `scripts/rebuild_lesson_index.py` | 为已有 lesson 重建索引。 |
| `scripts/run_preflight_regression.py` | 运行隔离的 Agent 回归测试。 |
| `scripts/run_session_finalize_regression.py` | 验证阶段性记录、完成推进和证据门槛。 |
| `examples/` | 课件和教学对话示例。 |
| `test-prompts.json` | 人工评估时的行为期望。 |

---

## 验证

校验 Skill 结构：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/programming-learning-coach
```

在已认证且支持非交互运行 Codex CLI 的环境中，运行三场景回归测试：

```bash
cd ~/.codex/skills/programming-learning-coach
python3 scripts/run_preflight_regression.py
python3 scripts/run_session_finalize_regression.py
```

测试会创建“新课”“学习型调试”和“复习”三个临时学习目录，并检查：

- lesson 文件是否实际生成；
- `lesson-index.json` 是否有匹配记录；
- 首条教学回复是否先报告 lesson 路径；
- lesson 中是否泄漏答案式内容。
- lesson 是否包含独立完成度和最低可运行版本。
- 阶段性学习是否同步写入 lesson、学习记录和当前状态；
- 可选学习计划是否只在完整证据后推进；
- 缺少预测或 IPO 时是否拒绝误判完成。

## 贡献

欢迎提交 Issue 和 Pull Request。请保持以下原则：聚焦学习行为；保留无答案 lesson 规则；行为变化时同步补充或更新测试。

## 许可证

本项目使用 [MIT License](LICENSE)。
