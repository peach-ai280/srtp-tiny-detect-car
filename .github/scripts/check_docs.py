#!/usr/bin/env python3
"""文档检查：非空、有 H1、相对链接存在、文件名无空格。

设计意图：只查"能机械判定"的东西。文笔、逻辑、格式细节不在这里管——
那些交给评审的人。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "build"}
BAD_NAME = re.compile(r"[ \u3000]")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)")
FENCE = re.compile(r"```.*?```", re.S)

errors, warnings = [], []


def md_files():
    for p in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        yield p


for f in sorted(md_files()):
    rel = f.relative_to(ROOT).as_posix()

    if BAD_NAME.search(f.name):
        errors.append(f"{rel}: 文件名含空格（用下划线）")

    text = f.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        errors.append(f"{rel}: 空文件")
        continue

    # Issue / PR 模板刻意以二级标题开头（GitHub 会在上方渲染标题），不要求 H1
    if not rel.startswith(".github/"):
        body = FENCE.sub("", text)
        if not re.search(r"^#\s+\S", body, re.M):
            errors.append(f"{rel}: 缺少一级标题（# 标题）")

    for target in LINK.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path = target.split("#", 1)[0]
        if not path:
            continue
        if not (f.parent / path).exists():
            errors.append(f"{rel}: 链接目标不存在 -> {target}")

    if len(text) < 60:
        warnings.append(f"{rel}: 内容过短（{len(text)} 字符）")

print(f"检查 {len(list(md_files()))} 个 Markdown 文件")
for w in warnings:
    print(f"  [warn] {w}")
for e in errors:
    print(f"  [error] {e}")

if errors:
    print(f"\n失败：{len(errors)} 个错误")
    sys.exit(1)
print("\n通过")
