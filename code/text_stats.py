#!/usr/bin/env python3
"""text_stats.py -- 词频统计小程序（实验一：基础工具使用）

统计文本文件中的英文词频，按出现次数降序输出前 N 个单词，
并可将完整词频导出为 JSON，供 plot_wordfreq.py 绘制矢量图。

用法:
    python3 code/text_stats.py sample.txt
    python3 code/text_stats.py sample.txt -n 15
    python3 code/text_stats.py sample.txt --json result/sample_stats.json
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

WORD_RE = re.compile(r"[a-z]+(?:'[a-z]+)?")


def count_words(text: str) -> Counter:
    """把文本小写化后按正则切词，返回词频计数器。"""
    return Counter(WORD_RE.findall(text.lower()))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="统计文本文件中的英文词频")
    parser.add_argument("textfile", type=Path, help="待统计的文本文件")
    parser.add_argument("-n", "--top", type=int, default=10,
                        help="显示前 N 个高频词（默认 10）")
    parser.add_argument("--json", type=Path, dest="json_out",
                        help="把完整词频统计写入指定的 JSON 文件")
    args = parser.parse_args(argv)

    if not args.textfile.is_file():
        parser.error(f"找不到文件: {args.textfile}")

    freq = count_words(args.textfile.read_text(encoding="utf-8"))
    total = sum(freq.values())

    print(f"文件: {args.textfile}")
    print(f"总词数: {total}，不同单词数: {len(freq)}，前 {args.top} 名:")
    print(f"{'排名':<6}{'单词':<16}{'次数':<8}{'占比'}")
    for rank, (word, count) in enumerate(freq.most_common(args.top), start=1):
        print(f"{rank:<6}{word:<16}{count:<8}{count / total:.1%}")

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "file": str(args.textfile),
            "total_words": total,
            "unique_words": len(freq),
            "freq": dict(freq),
        }
        args.json_out.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n完整词频已写入: {args.json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
