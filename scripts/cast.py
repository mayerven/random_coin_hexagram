#!/usr/bin/env python3
"""Simulate one three-coin six-line divination with secure randomness."""

from __future__ import annotations

import argparse
import secrets
import sys


TRIGRAMS = {
    (1, 1, 1): "乾",
    (1, 1, 0): "兑",
    (1, 0, 1): "离",
    (1, 0, 0): "震",
    (0, 1, 1): "巽",
    (0, 1, 0): "坎",
    (0, 0, 1): "艮",
    (0, 0, 0): "坤",
}

HEXAGRAMS = {
    ("乾", "乾"): "乾为天", ("乾", "兑"): "天泽履", ("乾", "离"): "天火同人", ("乾", "震"): "天雷无妄",
    ("乾", "巽"): "天风姤", ("乾", "坎"): "天水讼", ("乾", "艮"): "天山遁", ("乾", "坤"): "天地否",
    ("兑", "乾"): "泽天夬", ("兑", "兑"): "泽泽兑", ("兑", "离"): "泽火革", ("兑", "震"): "泽雷随",
    ("兑", "巽"): "泽风大过", ("兑", "坎"): "泽水困", ("兑", "艮"): "泽山咸", ("兑", "坤"): "泽地萃",
    ("离", "乾"): "火天大有", ("离", "兑"): "火泽睽", ("离", "离"): "离为火", ("离", "震"): "火雷噬嗑",
    ("离", "巽"): "火风鼎", ("离", "坎"): "火水未济", ("离", "艮"): "火山旅", ("离", "坤"): "火地晋",
    ("震", "乾"): "雷天大壮", ("震", "兑"): "雷泽归妹", ("震", "离"): "雷火丰", ("震", "震"): "震为雷",
    ("震", "巽"): "雷风恒", ("震", "坎"): "雷水解", ("震", "艮"): "雷山小过", ("震", "坤"): "雷地豫",
    ("巽", "乾"): "风天小畜", ("巽", "兑"): "风泽中孚", ("巽", "离"): "风火家人", ("巽", "震"): "风雷益",
    ("巽", "巽"): "巽为风", ("巽", "坎"): "风水涣", ("巽", "艮"): "风山渐", ("巽", "坤"): "风地观",
    ("坎", "乾"): "水天需", ("坎", "兑"): "水泽节", ("坎", "离"): "水火既济", ("坎", "震"): "水雷屯",
    ("坎", "巽"): "水风井", ("坎", "坎"): "坎为水", ("坎", "艮"): "水山蹇", ("坎", "坤"): "水地比",
    ("艮", "乾"): "山天大畜", ("艮", "兑"): "山泽损", ("艮", "离"): "山火贲", ("艮", "震"): "山雷颐",
    ("艮", "巽"): "山风蛊", ("艮", "坎"): "山水蒙", ("艮", "艮"): "艮为山", ("艮", "坤"): "山地剥",
    ("坤", "乾"): "地天泰", ("坤", "兑"): "地泽临", ("坤", "离"): "地火明夷", ("坤", "震"): "地雷复",
    ("坤", "巽"): "地风升", ("坤", "坎"): "地水师", ("坤", "艮"): "地山谦", ("坤", "坤"): "坤为地",
}

LINE_NAMES = ("初", "二", "三", "四", "五", "上")


def parse_values(raw: str | None) -> list[int] | None:
    if raw is None:
        return None
    try:
        values = [int(value.strip()) for value in raw.split(",")]
    except ValueError as error:
        raise argparse.ArgumentTypeError("--values must contain comma-separated integers") from error
    if len(values) != 6 or any(value not in (6, 7, 8, 9) for value in values):
        raise argparse.ArgumentTypeError("--values must contain exactly six values from 6, 7, 8, 9")
    return values


def cast_line() -> tuple[int, list[str]]:
    coins = [secrets.choice((("正", 3), ("反", 2))) for _ in range(3)]
    return sum(value for _, value in coins), [face for face, _ in coins]


def line_bits(values: list[int], changed: bool = False) -> list[int]:
    bits: list[int] = []
    for value in values:
        bit = 1 if value in (7, 9) else 0
        if changed and value in (6, 9):
            bit = 1 - bit
        bits.append(bit)
    return bits


def hexagram_name(bits: list[int]) -> tuple[str, str, str]:
    lower = TRIGRAMS[tuple(bits[:3])]
    upper = TRIGRAMS[tuple(bits[3:])]
    return upper, lower, HEXAGRAMS[(upper, lower)]


def render_line(value: int, position: int, show_moving: bool = True) -> str:
    line = "━━━━━━" if value in (7, 9) else "━━  ━━"
    if show_moving and value in (6, 9):
        marker = "○" if value == 9 else "×"
        line += f"  {marker} 动"
    return f"{LINE_NAMES[position]}爻  {line}  ({value})"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--question", default="未指定", help="label for this cast")
    parser.add_argument("--show-coins", action="store_true", help="show virtual coin faces")
    parser.add_argument("--values", help="six test values from bottom to top, e.g. 6,7,8,9,6,7")
    args = parser.parse_args()

    try:
        values = parse_values(args.values)
    except argparse.ArgumentTypeError as error:
        parser.error(str(error))

    coin_faces: list[list[str]] = []
    if values is None:
        values = []
        for _ in range(6):
            value, faces = cast_line()
            values.append(value)
            coin_faces.append(faces)

    upper, lower, base_name = hexagram_name(line_bits(values))
    changed_bits = line_bits(values, changed=True)
    changed_upper, changed_lower, changed_name = hexagram_name(changed_bits)
    moving = [f"{LINE_NAMES[index]}爻" for index, value in enumerate(values) if value in (6, 9)]

    print(f"问题：{args.question}")
    print("规则：正=3，反=2；结果按初爻到上爻记录。")
    print("\n六次结果（初爻在下）：")
    for index, value in enumerate(values):
        details = f"  {' '.join(coin_faces[index])}" if args.show_coins and coin_faces else ""
        print(f"  第{index + 1}次：{value}{details}")

    print(f"\n本卦：{base_name}（上{upper}下{lower}）")
    print("六爻图（上爻在上）：")
    for index in range(5, -1, -1):
        print(render_line(values[index], index))

    if moving:
        print(f"\n动爻：{'、'.join(moving)}")
        print(f"变卦：{changed_name}（上{changed_upper}下{changed_lower}）")
    else:
        print("\n动爻：无；此卦以本卦为主。")

    print("\n提示：这是安全随机数生成的反思工具，不证明他人想法或未来结果。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
