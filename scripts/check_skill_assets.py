#!/usr/bin/env python3
"""Check that the skill's required files exist and that internal paths resolve.

Also verifies SKILL.md frontmatter (name, description length), parses every
JSON schema, and checks that each language example folder is complete.

Usage:
    python3 scripts/check_skill_assets.py
    python3 scripts/check_skill_assets.py --root /path/to/language-learning-skill
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "references/learning-workflow.md",
    "references/annotation-schema.md",
    "references/translation-principles.md",
    "references/idioms-and-slang.md",
    "references/proficiency-and-difficulty.md",
    "references/quality-assurance.md",
    "references/output-formats.md",
    "languages/english.md",
    "languages/french.md",
    "languages/spanish.md",
    "languages/german.md",
    "prompts/analyze-text.md",
    "prompts/translate-contextually.md",
    "prompts/annotate-vocabulary.md",
    "prompts/extract-expressions.md",
    "prompts/explain-grammar.md",
    "prompts/generate-exercises.md",
    "prompts/quality-review.md",
    "schemas/learning-document.schema.json",
    "schemas/sentence.schema.json",
    "schemas/vocabulary.schema.json",
    "schemas/expression.schema.json",
    "schemas/exercise.schema.json",
    "scripts/validate_learning_document.py",
    "scripts/check_skill_assets.py",
    "tests/language-detection.md",
    "tests/alignment-tests.md",
    "tests/grammar-tests.md",
    "tests/idiom-tests.md",
    "tests/regression-tests.md",
]

REQUIRED_EXAMPLE_FILES = ["source.txt", "example.md", "example.json"]
LANGUAGES = ["english", "french", "spanish", "german"]

PATH_PATTERN = re.compile(
    r"(?<![\w/])(?:references|prompts|languages|schemas|scripts|tests|examples)"
    r"/[A-Za-z0-9_./-]+"
)
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip("\n")
    data: dict[str, str] = {}
    key = None
    for line in block.splitlines():
        if not line.strip():
            continue
        if line[:1].isspace() and key:
            data[key] += " " + line.strip()
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            data[key] = value.strip()
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
    )
    args = parser.parse_args()
    root = args.root.resolve()

    errors: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []

    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.is_file():
            errors.append(f"缺少必需文件：{relative}")
        elif path.stat().st_size == 0:
            errors.append(f"文件为空：{relative}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        text = skill_path.read_text(encoding="utf-8")
        front = parse_frontmatter(text)
        name = front.get("name", "")
        description = front.get("description", "")
        if not name:
            errors.append("SKILL.md frontmatter 缺少 name。")
        elif not NAME_PATTERN.match(name) or len(name) > 64:
            errors.append(f"SKILL.md name 不符合规范：{name!r}")
        elif name != root.name:
            warnings.append(
                f"SKILL.md name={name!r} 与目录名 {root.name!r} 不一致。"
            )
        if not description:
            errors.append("SKILL.md frontmatter 缺少 description。")
        elif len(description) > 1024:
            errors.append("SKILL.md description 超过 1024 字符。")
        elif len(description) < 40:
            warnings.append("SKILL.md description 偏短，可能缺少触发场景。")

        for match in PATH_PATTERN.finditer(text):
            candidate = match.group(0).rstrip(".,;:)]`'\"")
            if candidate.endswith("/"):
                continue
            if not (root / candidate).exists():
                errors.append(f"SKILL.md 引用了不存在的路径：{candidate}")

    for readme in [root / "README.md"]:
        if not readme.is_file():
            continue
        text = readme.read_text(encoding="utf-8")
        for match in PATH_PATTERN.finditer(text):
            candidate = match.group(0).rstrip(".,;:)]`'\"")
            if candidate.endswith("/"):
                continue
            if "*" in candidate or "<" in candidate:
                continue
            if not (root / candidate).exists():
                warnings.append(f"{readme.name} 引用了不存在的路径：{candidate}")

    for path in sorted((root / "schemas").glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.name} 不是合法 JSON：{exc}")
            continue
        if "$schema" not in data:
            warnings.append(f"{path.name} 缺少 $schema。")
        if not path.name.endswith(".schema.json"):
            warnings.append(f"{path.name} 命名不以 .schema.json 结尾。")

    for language in LANGUAGES:
        folder = root / "examples" / language
        if not folder.is_dir():
            errors.append(f"缺少示例目录：examples/{language}/")
            continue
        for filename in REQUIRED_EXAMPLE_FILES:
            path = folder / filename
            if not path.is_file():
                errors.append(f"缺少示例文件：examples/{language}/{filename}")
            elif path.stat().st_size == 0:
                errors.append(f"示例文件为空：examples/{language}/{filename}")
        example_json = folder / "example.json"
        if example_json.is_file():
            try:
                json.loads(example_json.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"examples/{language}/example.json 不是合法 JSON：{exc}")

    notes.append(f"检查根目录：{root}")
    notes.append(f"必需文件：{len(REQUIRED_FILES)} 项")

    for note in notes:
        print(f"NOTE: {note}")
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(
        f"\n{'FAIL' if errors else 'PASS'}: {len(errors)} error(s), "
        f"{len(warnings)} warning(s)"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
