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
python scripts/cast.py --question "今天是否适合出远门？"
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
