# Vibe Coding Skill

让新手也能用 AI 稳定做项目，而不是一上来就让 AI 乱写代码。

这个 skill 面向非程序员、新手、产品想法探索者，以及所有想做 vibe coding 但不想反复返工的人。它会把一句模糊想法整理成一组短文档，让 AI 在编码前知道：你要什么、不要什么、先做什么、怎样算完成。它还会帮新项目先建好基本文件，并要求每个小阶段完成后用 Git 留下可回退的检查点。

## 一句话介绍

**Vibe Coding Skill = 给 AI 编码前用的项目说明书生成器。**

它不会要求用户学习软件工程术语。它会用普通话问你几个关键问题，然后把答案整理成 AI 能读懂、能追踪、能测试的项目计划。

## 它适合做什么

适合：

- 从零开始做一个小工具、网页、App、插件、自动化脚本或 API
- 你只有一个粗略想法，需要 AI 帮你梳理
- 你希望 AI 不要一上来乱写代码
- 你希望项目有清楚的范围、验收标准和开发顺序
- 你希望后续换一个 AI，也能继续读懂项目

不适合：

- 已经有大量代码的老项目反向整理
- 只想让 AI 立刻写一次性脚本
- 不需要任何需求确认、测试计划或后续维护的临时任务

## 给新手的解释

这个 skill 会让 AI 做五件事：

1. **想法说明**：确认你到底想做什么，不做什么。
2. **拆解方案**：把项目拆成尽量互不干扰的部分。
3. **模块说明**：说明每个部分负责什么，输入什么，输出什么。
4. **验收清单**：写清楚怎样判断项目真的做好了。
5. **开发路线**：给 AI 一个安全的实现顺序，避免跳来跳去。
6. **项目初始化**：如果是 Python 项目，默认用 `uv`、`pyproject.toml`、`.gitignore` 和 `tests/`。
7. **Git 检查点**：每完成一个小任务，就测试、提交、开 PR、合并，方便回退和审查。

内部文件名仍然使用 `URD.md`、`ADD.md`、`MDD.md`、`TDD.md`、`RMD.md`。这些名字短、稳定、方便追踪；普通用户只需要理解上面的中文名字。

## 目录结构

```text
SKILL.md                     skill 主文件
templates/                   初始化模板
checklists/                  阶段检查清单
scripts/init_project_docs.py  初始化项目文档
scripts/check_project_docs.py 检查文档追踪、重复、wiki 膨胀等问题
scripts/link_project_docs.py  维护 .vibe/trace.json 和 docs/TRACE.md
scripts/init_python_uv_project.py 初始化 Python uv 项目
BEGINNER_GUIDE.md            给新手看的简短说明
EXPLAINER.md                 给 AI 使用的解释模板
REFERENCES.md                方法来源说明
manifest.txt                 包文件清单
```

项目初始化后会生成：

```text
docs/    正式项目说明
wiki/    给 AI 检索用的短笔记
.vibe/   机器可读的追踪状态
```

## 使用方式

把整个目录放进支持 skill 的环境，主说明文件是：

```text
SKILL.md
```

初始化一个项目的文档：

```bash
python scripts/init_project_docs.py --target /path/to/project --level standard --force
```


初始化 Python 项目文件：

```bash
python scripts/init_python_uv_project.py --target /path/to/project --name my-project --kind app --force
```

推荐的开发节奏：

```text
1. 先确认想法说明和验收清单。
2. 初始化项目文件和 Git 仓库。
3. 每次只做 RMD 里的一个小任务。
4. 测试通过后提交 commit。
5. 推送分支并创建 PR。
6. 检查通过后合并，再开始下一个任务。
```

检查文档是否过度膨胀、追踪关系是否断裂：

```bash
python scripts/check_project_docs.py --root /path/to/project
```

添加一条追踪关系：

```bash
python scripts/link_project_docs.py --root /path/to/project \
  --source URD-REQ-001 \
  --target ADD-FR-001 \
  --relation refines \
  --note "登录需求被拆成认证功能"
```

## 推荐给 AI 的第一句话

```text
请读取这个 repo 里的 Vibe Coding Skill。我的项目想法是：____。请先用新手能理解的话解释你会怎么帮我，然后从想法说明开始问我必要的问题，不要直接写代码。
```

## 设计取向

这个 skill 不是为了写厚文档。它的目标是让 AI 在开始编码前获得足够清楚、足够短、可以追踪的项目说明。

它内部使用 SDD、设计矩阵、解耦分析、测试计划、文档追踪、Git 检查点和 LLM Wiki，但这些机制默认藏在后面。对普通用户来说，它就是一个更稳的 vibe coding 起步方式。

每次生成或更新后，都要执行奥卡姆剃刀检查：删掉重复内容、未来功能、无追踪内容，以及把 `wiki/` 写成 `docs/` 副本的内容。
