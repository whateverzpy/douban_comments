#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能: 从 comments.json 提取所有 comment 内容，合并后中文分词并输出为空格分隔的 txt。
用法:
    python fenci.py
    python fenci.py -i comments.json -o comments_tokens.txt
依赖:
    pip install jieba
"""

import json
import argparse
import re
import sys
from pathlib import Path

try:
    import jieba
except ImportError:
    print("未安装 jieba，请先执行: pip install jieba", file=sys.stderr)
    sys.exit(1)

PUNCT_PATTERN = re.compile(r'^[\s\W_]+$', re.UNICODE)


def parse_args():
    parser = argparse.ArgumentParser(description="提取 comment 并中文分词")
    parser.add_argument("-i", "--input", default="comments.json", help="输入 JSON 文件")
    parser.add_argument("-o", "--output", default="comments_tokens.txt", help="输出 TXT 文件")
    return parser.parse_args()


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def extract_comments(node):
    results = []
    if isinstance(node, dict):
        for k, v in node.items():
            if k.lower() == "comment" and isinstance(v, (str, int, float)):
                results.append(str(v))
            else:
                results.extend(extract_comments(v))
    elif isinstance(node, list):
        for item in node:
            results.extend(extract_comments(item))
    return results


def clean_text(text: str) -> str:
    # 可按需扩展清洗规则
    return text.replace("\u3000", " ").strip()


def segment(text: str):
    for tok in jieba.cut(text, cut_all=False):
        tok = tok.strip()
        if not tok:
            continue
        if PUNCT_PATTERN.match(tok):
            continue
        yield tok


def main():
    args = parse_args()
    in_path = Path(args.input)
    if not in_path.exists():
        print(f"输入文件不存在: {in_path}", file=sys.stderr)
        sys.exit(2)

    try:
        data = load_json(in_path)
    except Exception as e:
        print(f"读取或解析 JSON 失败: {e}", file=sys.stderr)
        sys.exit(3)

    comments = extract_comments(data)
    if not comments:
        print("未找到任何 comment 字段内容。", file=sys.stderr)

    merged = clean_text("\n".join(comments))
    tokens = list(segment(merged))
    out_path = Path(args.output)
    out_path.write_text(" ".join(tokens), encoding="utf-8")

    print(f"完成: 提取 {len(comments)} 条 comment，生成 {len(tokens)} 个词语 -> {out_path}")


if __name__ == "__main__":
    main()
