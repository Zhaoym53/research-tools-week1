#!/usr/bin/env python3
"""text_stats.py -- 词频统计小程序（实验一：基础工具使用）

统计文本文件中的英文词频，按出现次数降序输出前 N 个单词，
并可将完整词频导出为 JSON，供 plot_wordfreq.py 绘制矢量图。

用法:
    python3 code/text_stats.py sample.txt
    python3 code/text_stats.py sample.txt -n 15
    python3 code/text_stats.py sample.txt --json result/sample_stats.json
    python3 code/text_stats.py sample.txt --stopwords
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

WORD_RE = re.compile(r"[a-z]+(?:'[a-z]+)?")

# 常见英文虚词/功能词。默认不启用过滤，只有命令行传入 --stopwords 时使用。
ENGLISH_STOPWORDS = frozenset({
    "a", "an", "the", "and", "or", "but", "if", "then", "else", "when",
    "while", "because", "as", "of", "at", "by", "for", "with", "about",
    "into", "through", "during", "before", "after", "to", "from", "in",
    "on", "off", "over", "under", "again", "further", "once", "here",
    "there", "all", "any", "both", "each", "few", "more", "most", "other",
    "some", "such", "no", "nor", "not", "only", "own", "same", "so",
    "than", "too", "very", "can", "will", "just", "should", "now",
    "i", "me", "my", "myself", "we", "our", "ours", "you", "your",
    "he", "him", "his", "she", "her", "it", "its", "they", "them",
    "their", "this", "that", "these", "those", "am", "is", "are", "was",
    "were", "be", "been", "being", "have", "has", "had", "having", "do",
    "does", "did", "doing", "would", "could", "ought",
})


def count_words(text: str, stopwords: frozenset[str] | set[str] | None = None) -> Counter:
    """把文本小写化后按正则切词，可选用停用词集合过滤。"""
    words = WORD_RE.findall(text.lower())
    if stopwords:
        words = (word for word in words if word not in stopwords)
    return Counter(words)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="统计文本文件中的英文词频")
    parser.add_argument("textfile", type=Path, help="待统计的文本文件")
    parser.add_argument("-n", "--top", type=int, default=10,
                        help="显示前 N 个高频词（默认 10）")
    parser.add_argument("--json", type=Path, dest="json_out",
                        help="把完整词频统计写入指定的 JSON 文件")
    parser.add_argument("--stopwords", action="store_true",
                        help="过滤内置英文停用词（默认不过滤，保持原行为）")
    args = parser.parse_args(argv)

    if not args.textfile.is_file():
        parser.error(f"找不到文件: {args.textfile}")

    freq = count_words(
        args.textfile.read_text(encoding="utf-8"),
        stopwords=ENGLISH_STOPWORDS if args.stopwords else None,
    )
    total = sum(freq.values())
    filter_note = "，已过滤内置英文停用词" if args.stopwords else ""

    print(f"文件: {args.textfile}")
    print(f"总词数: {total}，不同单词数: {len(freq)}，前 {args.top} 名{filter_note}:")
    print(f"{'排名':<6}{'单词':<16}{'次数':<8}{'占比'}")
    for rank, (word, count) in enumerate(freq.most_common(args.top), start=1):
        print(f"{rank:<6}{word:<16}{count:<8}{count / total:.1%}")

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "file": str(args.textfile),
            "total_words": total,
            "unique_words": len(freq),
            "stopwords_filtered": args.stopwords,
            "freq": dict(freq),
        }
        args.json_out.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n完整词频已写入: {args.json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
