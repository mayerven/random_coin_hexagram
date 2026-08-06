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
python3 scripts/cast.py --question "今天应该优先处理哪项任务？" --show-coins
```

Example output includes the six throws from the bottom line to the top line:

```text
问题：今天应该优先处理哪项任务？
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
Use $random-yao to simulate a single six-line coin divination for my question.
```

The skill instructions are in [SKILL.md](SKILL.md). UI metadata for compatible
clients is in [agents/openai.yaml](agents/openai.yaml).

## Interpretation Boundary

This is a randomized reflection tool. It does not establish another person's
private thoughts, predict the future, or replace medical, legal, financial, or
safety decisions. For the same question, cast once, reflect, and avoid repeated
draws merely to seek a preferred answer.
