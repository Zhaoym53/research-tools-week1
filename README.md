# research-tools-week1

数据安全与隐私保护课程·实验一（基础工具使用）的练习仓库，用于练习 Git/GitHub 版本管理、Codex 辅助编程与 LaTeX 报告写作。

## 目录结构

```text
README.md     项目说明
sample.txt    词频统计的示例文本
code/         实验代码
result/       运行结果（含矢量结果图）
report/       LaTeX 实验报告
figures/      报告插图
```

## 使用方法

```bash
# 词频统计：显示前 10 个高频词
python3 code/text_stats.py sample.txt

# 显示前 15 个，并把完整词频导出为 JSON
python3 code/text_stats.py sample.txt -n 15 --json result/sample_stats.json

# 根据统计结果绘制矢量柱状图（需要 matplotlib）
python3 code/plot_wordfreq.py
```

## 实验一任务清单

- [√ ] 安装并配置 Git，完成本地提交
- [√ ] 在 GitHub 建立仓库并 push 本地代码
- [√ ] 在 GitHub 网页修改 README 后用 git pull 同步
- [ ] 安装配置 Codex，并完成一次辅助编程任务
- [ ] 安装配置 cc-switch，完成供应商切换
- [ ] 使用 LaTeX 模板撰写实验报告（含矢量结果图）
