---
name: random-yao
description: >
  Use secure random simulation of three coins to generate a six-line I Ching
  divination, including the base hexagram, moving lines, and changed hexagram.
  Use when a user asks to randomly cast, shake, or simulate a coin-based six-line
  divination, especially phrases such as "随机摇一卦", "帮我摇一卦", or "虚拟投币起卦".
---

# Random Yao

Run `scripts/cast.py` once for one clearly stated question. Use the optional
`--question` text only as a label; it does not affect the random draw.

```bash
python scripts/cast.py --question "我现在是否适合暂停主动联系？"
```

## Workflow

1. Help the user reduce the question to one actionable issue. Prefer questions
   about the user's next action over claims about another person's hidden mind.
2. Run the script once. Do not recast the same question merely because the user
   dislikes the result.
3. Explain that the output is a random reflection prompt, not evidence of fate
   or another person's private thoughts.
4. Read the base hexagram as the present frame, the moving line(s) as the active
   tension, and the changed hexagram as a possible direction if the current
   pattern continues.
5. Archive every completed cast and interpretation in the workspace `history/`
   directory before replying. This is mandatory unless the user explicitly asks
   not to retain the record.

## Archive Hook

Use the following sequence for every cast. Generate the JSON only once; it is
the source of truth for the archive. After writing the interpretation, save it
to a temporary UTF-8 Markdown file and archive it with `archive.py`.

```bash
python scripts/cast.py --question "问题" --show-coins --format json > /tmp/random-yao-cast.json
python scripts/archive.py \
  --cast-json /tmp/random-yao-cast.json \
  --interpretation-file /tmp/random-yao-interpretation.md \
  --output-dir history
```

The archive page must contain the question, timestamp, base hexagram, moving
line(s), changed hexagram when applicable, six coin values, the bottom-to-top
diagram, and the complete interpretation. Do not archive sensitive personal
details that are unnecessary to understand the question. Tell the user the
saved page path in the final answer.

## Presentation

Use a compact, scan-friendly Markdown layout for both a cast and an explanation.
Lead with the result, then show how it was formed. Preserve the bottom-to-top
order throughout: the first throw is the initial line at the bottom.

````markdown
## 起卦结果

问题：……

> 本卦：……
> 动爻：……
> 变卦：……

| 次序（自下而上） | 点数 | 爻 | 状态 |
| --- | ---: | --- | --- |
| 初爻 | 7 | ━━━━━━━ | 少阳，不动 |
| 二爻 | 8 | ━━　━━ | 少阴，不动 |
| 三爻 | 9 | ━━━ ○ ━━━ | 老阳，动，变阴 |

本卦（上）
```text
上爻  ━━━━━━━
五爻  ━━   ━━
四爻  ━━━━━━━
三爻  ━━━ ○ ━━━  动
二爻  ━━   ━━
初爻  ━━━━━━━
```
（下）
````

Then explain in this order:

1. **本卦**：当前事情的结构或气氛。
2. **动爻**：正在变化的张力；引用爻辞时，附一两句白话，不作权威断言。
3. **变卦**：若延续目前模式，可能出现的关系或行动方向。
4. **落点**：给一项低风险、可由用户自己决定的行动建议。

For a teaching request about coin casting, use this structure instead:

1. Explain the 6/7/8/9 mapping in a four-row table.
2. State the six-throw procedure as a numbered list.
3. Give one complete, bottom-to-top worked example in a code block.
4. End with the reading order: base hexagram, moving line, changed hexagram.

Use tables for mappings and fixed-width diagrams for line positions. Do not use
tables merely to pad a short answer. Keep headings short and avoid claiming the
visual structure makes a random draw more authoritative.

## Boundaries

- Do not use the cast to make medical, legal, financial, or safety decisions.
- Do not present a result as proof of someone else's feelings, intent, or future
  behavior.
- If the user is repeatedly casting around anxiety, recommend pausing rather
  than generating more draws.

## Script Options

- `--question TEXT`: Label the cast with the user's question.
- `--show-coins`: Include the three virtual coin faces for every line.
- `--values 6,7,8,9,6,7`: Test a known six-line sequence. Values are written
  from the first throw (bottom line) to the sixth throw (top line).
- `--format json`: Emit a structured cast record for `archive.py`; the default
  is the readable text format.
- `scripts/archive.py`: Write a completed cast plus its interpretation as a
  Markdown wiki page. Use `--cast-json`, `--interpretation-file`, and
  `--output-dir history`.
