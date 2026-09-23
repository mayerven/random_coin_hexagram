---
name: random-yao
description: >
  Securely simulate one traditional three-coin, six-line I Ching cast and
  explain the base hexagram, moving lines, and changed hexagram. Use when the
  user asks to randomly cast, shake, or simulate a coin-based six-line
  divination, including requests such as "随机摇一卦", "帮我摇一卦", or "虚拟投币起卦".
---

# Random Yao for ChatGPT

Use the bundled `scripts/cast.py` as the source of randomness and hexagram
mapping. The user's question is only a label and must never influence the draw.

## Workflow

1. If the user already gave one clear question, do not ask them to restate it.
   If no usable question was given, ask for one concise question.
2. Run exactly one cast:

   ```bash
   python scripts/cast.py --question "用户的问题" --show-coins --format json
   ```

3. Treat the JSON output as the source of truth. Do not alter line values,
   moving lines, trigram order, the base hexagram, or the changed hexagram.
4. Present the result in Chinese unless the user asks for another language.
5. Interpret in this order:
   - **本卦**：当前问题的结构、气氛或处境。
   - **动爻**：正在变化的张力。若引用爻辞，保持简短，并给出白话解释。
   - **变卦**：如果当前模式延续，可作为后续方向的传统象征性参考。
   - **落点**：给出一项低风险、由用户自己决定的现实行动建议。
6. Do not recast the same question just because the user dislikes the result.

## Presentation

Lead with a compact result block:

```text
问题：……
本卦：……
动爻：……
变卦：……
```

Then show the six throws from bottom to top when helpful. Preserve traditional
line order: the first throw is the bottom line (初爻), and the sixth throw is
the top line (上爻).

## Boundaries

This is a traditional-culture and reflection tool, not evidence of fate.

- Do not present a cast as proof of another person's hidden thoughts, feelings,
  intent, or future behavior.
- Do not use the cast as the sole basis for medical, legal, financial, safety,
  or other high-stakes decisions.
- When reality can be checked directly, distinguish the traditional reading
  from verifiable facts and practical evidence.
- If the user repeatedly casts around the same anxiety, prefer reflection on
  the existing result rather than generating repeated draws.
