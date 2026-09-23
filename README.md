# Random Coin Hexagram

A small, dependency-free Python tool and Codex skill for simulating a traditional
three-coin, six-line I Ching cast.

It produces six coin throws, the base hexagram, moving lines, and the changed
hexagram. The draw uses Python's `secrets` module, so the question text never
affects the outcome.

```text
one question -> six virtual throws -> base hexagram -> moving lines -> changed hexagram
```

## Quick Start

Requires Python 3.10+ and no third-party packages.

```bash
python3 scripts/cast.py --question "今天是否适合出远门？" --show-coins
```

Example output includes the six throws from the bottom line to the top line:

```text
问题：今天是否适合出远门？
本卦：火天大有（上离下乾）
动爻：初爻、四爻
变卦：山风蛊（上艮下巽）
```

For a reproducible check, provide six known line values. Values are ordered from
the first throw (bottom line) to the sixth throw (top line).

```bash
python3 scripts/cast.py --values 6,7,8,9,6,7
```

## Three-Coin Rules

The script uses this conventional mapping:

| Virtual coin total | Line | Meaning |
| --- | --- | --- |
| 6 | old yin | moving yin, changes to yang |
| 7 | young yang | stable yang |
| 8 | young yin | stable yin |
| 9 | old yang | moving yang, changes to yin |

Each coin is independently drawn as `正 = 3` or `反 = 2`. Six throws create the
base hexagram. Lines valued `6` or `9` are moving lines; changing them produces
the changed hexagram.

## 六爻基础

六爻是由下向上排列的六条阴阳爻线。每次投掷三枚硬币得到一条爻，连续投掷
六次形成一卦：第一次是初爻（最下面），第六次是上爻（最上面）。阳爻通常
画作一条完整的线 `——`，阴爻画作中间断开的线 `— —`。

六条爻可以分成上下两个三爻卦（下卦与上卦），六十四卦就是这两个三爻卦的
组合。一次起卦通常会得到三个要素：

- **本卦**：六次投掷直接形成的当前结构，用来描述问题的现状或背景。
- **动爻**：数值为 6 或 9 的爻，表示正在变化的局部因素；没有动爻时，只有本卦。
- **变卦**：把动爻阴阳反转后得到的卦，可作为趋势或后续方向的反思框架。

这些名称是传统术语的简明说明，不代表对未来或他人内心的确定判断。实际
使用时，先把问题收敛为一个可行动的问题，再结合卦象思考自己的选择。

## Command-Line Options

```text
--question TEXT   Label the cast. It does not influence randomness.
--show-coins      Print the three virtual coin faces for each throw.
--values LIST     Test values, e.g. 6,7,8,9,6,7.
```

Run `python3 scripts/cast.py --help` for the complete usage summary.

## Use as a Codex Skill

This repository is also a standalone Codex skill. Clone it into a skill root as
`random-yao`:

```bash
git clone REPOSITORY_URL \
  ~/.codex/skills/random-yao
```

Then invoke it with a request such as:

```text
Use $random-yao to simulate a single six-line coin divination for the question: 今天是否适合出远门？
```

The skill instructions are in [SKILL.md](SKILL.md). UI metadata for compatible
clients is in [agents/openai.yaml](agents/openai.yaml).

### Skill 简介与联动

`random-yao` 是一个轻量的随机起卦 skill。它会运行本项目脚本，返回六次
投掷、每爻数值、本卦、动爻和变卦，并把结果组织成一次性的反思提示。`--question`
只用于标记问题，不会参与随机数计算；同一个问题不应为了得到喜欢的答案而反复起卦。

它可以和其他玄学类 skill 串联使用，但本项目不会自动调用或安装它们。常见的
联动方式包括：

- **八字或紫微斗数 skill**：先看个人长期状态、流年或出行时机，再用 `random-yao`
  针对“今天是否出远门”这类短期选择起卦。
- **风水或择日 skill**：先比较日期、方位和场所条件，再让 `random-yao` 作为
  当下决策的另一种象征性视角。
- **塔罗或梅花易数 skill**：对同一个问题提供不同体系的反思框架；应避免连续
  重复占问，并把各体系结果当作参考而不是互相证明。

如果环境中安装了这些 skill，可以先后调用并把前一步的摘要交给下一步；它们之间
没有固定的接口或自动同步机制。涉及天气、交通、健康和安全时，仍应以现实数据
和专业建议为准。

## Interpretation Boundary

This is a randomized reflection tool. It does not establish another person's
private thoughts, predict the future, or replace medical, legal, financial, or
safety decisions. For the same question, cast once, reflect, and avoid repeated
draws merely to seek a preferred answer.


## ChatGPT Upload Bundle

A ChatGPT-oriented distribution is available under
[`chatgpt/random-yao/`](chatgpt/random-yao/). Unlike the Codex-oriented root
skill, this variant does not require persistent `history/` archiving and is
packaged for direct skill upload.

Build the ZIP with:

```bash
python3 scripts/build_chatgpt_bundle.py
```

The command writes:

```text
dist/random-yao-chatgpt.zip
```

The archive contains exactly one top-level `random-yao/` folder with one
`SKILL.md` and its bundled casting script.

When skill upload is enabled for your ChatGPT account/workspace, install it from
**Plugins → Skills → Create → Upload from your computer**, then select the
generated ZIP and review/install the skill. ChatGPT skill availability depends
on the current plan, workspace settings, and product rollout.
