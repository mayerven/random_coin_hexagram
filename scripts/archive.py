#!/usr/bin/env python3
"""Archive one completed random-yao cast and its interpretation as Markdown."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path


LINE_NAMES = ("初", "二", "三", "四", "五", "上")


def safe_slug(text: str) -> str:
    slug = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", text, flags=re.UNICODE).strip("-")
    return (slug or "随机起卦")[:48]


def line_shape(value: int) -> str:
    shape = "━━━━━━" if value in (7, 9) else "━━  ━━"
    if value in (6, 9):
        shape += f"  {'○' if value == 9 else '×'} 动"
    return shape


def render_table(values: list[int]) -> str:
    rows = [
        "| 次序（自下而上） | 点数 | 爻 | 状态 |",
        "| --- | ---: | --- | --- |",
    ]
    for index, value in enumerate(values):
        if value == 6:
            status = "老阴，动，变阳"
        elif value == 7:
            status = "少阳，不动"
        elif value == 8:
            status = "少阴，不动"
        else:
            status = "老阳，动，变阴"
        rows.append(f"| {LINE_NAMES[index]}爻 | {value} | {line_shape(value)} | {status} |")
    return "\n".join(rows)


def render_diagram(values: list[int]) -> str:
    return "\n".join(
        f"{LINE_NAMES[index]}爻  {line_shape(values[index])}  ({values[index]})"
        for index in range(5, -1, -1)
    )


def read_interpretation(args: argparse.Namespace) -> str:
    if args.interpretation_file:
        return Path(args.interpretation_file).read_text(encoding="utf-8").strip()
    return (args.interpretation or "").strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cast-json", required=True, help="JSON file produced by cast.py --format json")
    parser.add_argument("--interpretation-file", help="Markdown/text interpretation file")
    parser.add_argument("--interpretation", help="Short interpretation; prefer --interpretation-file for multiline text")
    parser.add_argument("--notes", default="", help="Optional factual notes or follow-up")
    parser.add_argument("--output-dir", default="history", help="Directory for Markdown wiki pages")
    args = parser.parse_args()

    if not args.interpretation_file and not args.interpretation:
        parser.error("provide --interpretation-file or --interpretation")

    record = json.loads(Path(args.cast_json).read_text(encoding="utf-8"))
    values = record["values"]
    if not isinstance(values, list) or len(values) != 6:
        parser.error("cast JSON must contain six values")

    now = dt.datetime.now().astimezone()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{now:%Y%m%d-%H%M%S}-{safe_slug(str(record.get('question', '随机起卦')))}"
    target = output_dir / f"{stem}.md"
    suffix = 2
    while target.exists():
        target = output_dir / f"{stem}-{suffix}.md"
        suffix += 1

    base = record["base"]
    changed = record["changed"]
    moving = "、".join(record["moving"]) if record["moving"] else "无"
    interpretation = read_interpretation(args)
    lines = [
        "---",
        f"date: {now.isoformat(timespec='seconds')}",
        f"question: {record.get('question', '未指定')}",
        f"base: {base['name']}",
        f"moving: {moving}",
        f"changed: {changed['name'] if record['moving'] else '无'}",
        "source: random-yao secure random three-coin cast",
        "---",
        "",
        f"# {record.get('question', '随机起卦')}",
        "",
        f"**起卦时间**：{now:%Y-%m-%d %H:%M:%S %z}",
        "",
        "> 这是随机投币生成的反思工具，不证明命运、他人想法或未来结果。",
        "",
        "## 结果",
        "",
        f"- 本卦：**{base['name']}**（上{base['upper']}下{base['lower']}）",
        f"- 动爻：**{moving}**",
        f"- 变卦：**{changed['name']}**（上{changed['upper']}下{changed['lower']}）" if record["moving"] else "- 变卦：无，静卦以本卦为主",
        "",
        "## 六爻记录",
        "",
        render_table(values),
        "",
        "本卦（上）",
        "",
        "```text",
        render_diagram(values),
        "```",
        "（下）",
        "",
        "## 解读",
        "",
        interpretation,
    ]
    if args.notes:
        lines.extend(["", "## 备注", "", args.notes.strip()])
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
