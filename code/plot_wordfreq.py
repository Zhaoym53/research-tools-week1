#!/usr/bin/env python3
"""plot_wordfreq.py -- 把 text_stats.py 的 JSON 结果绘成矢量柱状图

读取 result/sample_stats.json，生成 result/wordfreq.pdf。
PDF 为矢量格式，放大不失真，适合直接插入 LaTeX 报告。

用法:
    python3 code/text_stats.py sample.txt --json result/sample_stats.json
    python3 code/plot_wordfreq.py
"""

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

JSON_PATH = Path("result/sample_stats.json")
PDF_PATH = Path("result/wordfreq.pdf")
TOP_N = 10


def main() -> int:
    if not JSON_PATH.is_file():
        print(f"缺少统计结果 {JSON_PATH}，请先运行 "
              f"`python3 code/text_stats.py sample.txt --json {JSON_PATH}`",
              file=sys.stderr)
        return 1

    stats = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    items = sorted(stats["freq"].items(), key=lambda kv: kv[1],
                   reverse=True)[:TOP_N]
    words = [w for w, _ in items][::-1]   # 倒序排列，最高频显示在顶部
    counts = [c for _, c in items][::-1]

    fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
    ax.barh(words, counts, color="#4066a0")
    ax.set_xlabel("count")
    ax.set_title(f"Top {TOP_N} words in {stats['file']} "
                 f"({stats['total_words']} words total)")
    for i, c in enumerate(counts):
        ax.text(c, i, f" {c}", va="center", fontsize=9)

    PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PDF_PATH)
    print(f"矢量图已生成: {PDF_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
