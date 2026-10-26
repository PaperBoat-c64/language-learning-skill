#!/usr/bin/env python3
"""Validate a language-learning document.

Checks performed:
  1. JSON Schema validation (when the `jsonschema` package is installed).
  2. Structural checks that work without any third-party dependency.
  3. ID uniqueness, cross-reference resolution, and substring checks.
  4. Source-text integrity against an optional source file.

Exit code 0 when there are no errors, 1 otherwise. Warnings do not fail the run
unless --strict is passed.

Usage:
    python3 scripts/validate_learning_document.py document.json
    python3 scripts/validate_learning_document.py document.json --source source.txt
    python3 scripts/validate_learning_document.py document.json --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

SENTENCE_ID = re.compile(r"^s\d{2,4}-\d{2,4}$")
VOCAB_ID = re.compile(r"^v\d{3,4}$")
EXPRESSION_ID = re.compile(r"^e\d{3,4}$")
GRAMMAR_ID = re.compile(r"^g\d{3,4}$")
EXERCISE_ID = re.compile(r"^x\d{3,4}$")

TEXT_LANGUAGES = {"en", "fr", "es", "de"}
GENRES = {
    "news", "article", "fiction", "dialogue", "lyrics", "email",
    "social-media", "academic", "other",
}
MODES = {"study", "compact", "cards", "exercise-sheet", "json"}
PRIORITIES = {"high", "medium", "low"}
CONFIDENCES = {"high", "medium", "low"}
QA_STATUSES = {"pass", "fail", "unverified", "not-applicable"}
EXPRESSION_TYPES = {
    "collocation", "phrasal-verb", "idiom", "colloquialism",
    "slang", "valency", "grammatical-expression",
}
EXERCISE_TYPES = {
    "meaning", "cloze", "collocation", "rewrite", "grammar-discrimination",
    "translation", "imitation", "speaking-scenario", "recall-card",
}
POS_VALUES = {
    "noun", "verb", "adjective", "adverb", "pronoun", "determiner",
    "article", "preposition", "conjunction", "interjection", "numeral",
    "particle", "proper-noun", "phrase", "other",
}


def normalize(text: str) -> str:
    """NFC normalize and collapse all whitespace to single spaces."""
    text = unicodedata.normalize("NFC", text)
    return re.sub(r"\s+", " ", text).strip()


def squash(text: str) -> str:
    """Remove all whitespace, for diagnosing whitespace-only differences."""
    return re.sub(r"\s+", "", unicodedata.normalize("NFC", text))


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def check_schema(doc: Any, schema_dir: Path, report: Report) -> None:
    """Validate against the bundled schemas if jsonschema is available."""
    try:
        import jsonschema  # type: ignore
    except ImportError:
        report.note("jsonschema 未安装：已执行内置结构检查，未执行正式 JSON Schema 校验。")
        return

    top_path = schema_dir / "learning-document.schema.json"
    try:
        schema = load_json(top_path)
    except OSError as exc:
        report.warn(f"无法读取顶层 schema：{exc}")
        return

    schemas: list[tuple[Path, Any]] = []
    for path in schema_dir.glob("*.json"):
        try:
            schemas.append((path, load_json(path)))
        except (OSError, json.JSONDecodeError):
            continue

    try:
        try:
            from referencing import Registry, Resource
            from referencing.jsonschema import DRAFT202012

            registry = Registry()
            for path, contents in schemas:
                resource = Resource.from_contents(
                    contents, default_specification=DRAFT202012
                )
                registry = registry.with_resource(path.resolve().as_uri(), resource)
                if isinstance(contents, dict) and "$id" in contents:
                    registry = registry.with_resource(contents["$id"], resource)
            validator = jsonschema.Draft202012Validator(schema, registry=registry)
        except ImportError:  # older jsonschema without referencing
            store = {}
            for path, contents in schemas:
                store[path.resolve().as_uri()] = contents
                if isinstance(contents, dict) and "$id" in contents:
                    store[contents["$id"]] = contents
            resolver = jsonschema.RefResolver(
                base_uri=schema_dir.resolve().as_uri() + "/",
                referrer=schema,
                store=store,
            )
            validator = jsonschema.Draft202012Validator(schema, resolver=resolver)
        errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path))
    except Exception as exc:  # pragma: no cover - defensive
        report.warn(f"JSON Schema 校验未能完成：{exc}")
        return

    if not errors:
        report.note("JSON Schema 校验通过（jsonschema）。")
        return

    for error in errors:
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        report.error(f"schema: {location}: {error.message}")


def check_top_level(doc: Any, report: Report) -> bool:
    if not isinstance(doc, dict):
        report.error("文档根节点必须是 JSON 对象。")
        return False

    required = [
        "schemaVersion", "meta", "source", "sentences", "vocabulary",
        "expressions", "grammar", "exercises", "qa",
    ]
    for key in required:
        if key not in doc:
            report.error(f"缺少顶层字段：{key}")
    if report.errors:
        return False

    meta = doc.get("meta")
    if not isinstance(meta, dict):
        report.error("meta 必须是对象。")
        return False
    if meta.get("textLanguage") not in TEXT_LANGUAGES:
        report.error(f"meta.textLanguage 无效：{meta.get('textLanguage')!r}")
    if meta.get("genre") not in GENRES:
        report.error(f"meta.genre 无效：{meta.get('genre')!r}")
    if meta.get("mode") not in MODES:
        report.error(f"meta.mode 无效：{meta.get('mode')!r}")
    level = meta.get("level")
    if not isinstance(level, dict) or level.get("strategy") not in {
        "default-adaptive", "user-specified",
    }:
        report.error("meta.level.strategy 缺失或无效。")

    source = doc.get("source")
    if not isinstance(source, dict) or not isinstance(source.get("text"), str):
        report.error("source.text 缺失。")
    return True


def collections(doc: dict) -> dict[str, list[dict]]:
    result: dict[str, list[dict]] = {}
    for key in ("sentences", "vocabulary", "expressions", "grammar", "exercises"):
        value = doc.get(key)
        result[key] = value if isinstance(value, list) else []
    return result


def check_ids_and_refs(doc: dict, report: Report) -> None:
    data = collections(doc)
    sentences = data["sentences"]
    vocab = data["vocabulary"]
    expressions = data["expressions"]
    grammar = data["grammar"]
    exercises = data["exercises"]

    sentence_ids: set[str] = set()
    seen_paragraph = 0
    for position, sentence in enumerate(sentences):
        if not isinstance(sentence, dict):
            report.error(f"sentences[{position}] 不是对象。")
            continue
        sid = sentence.get("id")
        if not isinstance(sid, str) or not SENTENCE_ID.match(sid):
            report.error(f"sentences[{position}] 的 id 无效：{sid!r}")
            continue
        if sid in sentence_ids:
            report.error(f"句子 ID 重复：{sid}")
        sentence_ids.add(sid)
        paragraph = sentence.get("paragraph")
        if not isinstance(paragraph, int) or paragraph < 1:
            report.error(f"{sid} 的 paragraph 无效：{paragraph!r}")
        elif paragraph < seen_paragraph:
            report.error(f"{sid} 的段落顺序倒退（{seen_paragraph} → {paragraph}）。")
        else:
            seen_paragraph = paragraph
        if not isinstance(sentence.get("text"), str) or not sentence["text"].strip():
            report.error(f"{sid} 缺少原文。")
        if not isinstance(sentence.get("translation"), str) or not sentence["translation"].strip():
            report.error(f"{sid} 缺少译文。")

    id_sets: dict[str, set[str]] = {
        "vocabulary": set(), "expressions": set(), "grammar": set(), "exercises": set(),
    }
    patterns = {
        "vocabulary": (vocab, VOCAB_ID, "v"),
        "expressions": (expressions, EXPRESSION_ID, "e"),
        "grammar": (grammar, GRAMMAR_ID, "g"),
        "exercises": (exercises, EXERCISE_ID, "x"),
    }
    for name, (items, pattern, prefix) in patterns.items():
        for position, item in enumerate(items):
            if not isinstance(item, dict):
                report.error(f"{name}[{position}] 不是对象。")
                continue
            item_id = item.get("id")
            if not isinstance(item_id, str) or not pattern.match(item_id):
                report.error(f"{name}[{position}] 的 id 无效：{item_id!r}")
                continue
            if item_id in id_sets[name]:
                report.error(f"{name} ID 重复：{item_id}")
            id_sets[name].add(item_id)

    # Reference resolution and verbatim checks.
    sentence_text = {
        s.get("id"): s.get("text", "")
        for s in sentences
        if isinstance(s, dict) and isinstance(s.get("id"), str)
    }

    for item in vocab:
        if not isinstance(item, dict):
            continue
        vid = item.get("id", "?")
        refs = item.get("sentenceRefs") or []
        if not refs:
            report.error(f"{vid} 没有 sentenceRefs。")
        for ref in refs:
            if ref not in sentence_text:
                report.error(f"{vid} 引用了不存在的句子：{ref}")
                continue
            surface = item.get("surface", "")
            if isinstance(surface, str) and surface and surface not in sentence_text[ref]:
                report.warn(f"{vid} 的 surface {surface!r} 未出现在 {ref} 中。")
        if item.get("pos") not in POS_VALUES:
            report.error(f"{vid} 的 pos 无效：{item.get('pos')!r}")
        if item.get("priority") not in PRIORITIES:
            report.error(f"{vid} 的 priority 无效：{item.get('priority')!r}")
        if item.get("confidence") not in CONFIDENCES:
            report.error(f"{vid} 的 confidence 无效：{item.get('confidence')!r}")
        if not isinstance(item.get("needsVerification"), bool):
            report.error(f"{vid} 缺少布尔值 needsVerification。")
        elif item.get("confidence") == "low" and item.get("needsVerification") is False:
            report.warn(f"{vid} 的 confidence 为 low 但 needsVerification 为 false。")

    for item in expressions:
        if not isinstance(item, dict):
            continue
        eid = item.get("id", "?")
        refs = item.get("sentenceRefs") or []
        if not refs:
            report.error(f"{eid} 没有 sentenceRefs。")
        for ref in refs:
            if ref not in sentence_text:
                report.error(f"{eid} 引用了不存在的句子：{ref}")
                continue
            span = item.get("text", "")
            if isinstance(span, str) and span and span not in sentence_text[ref]:
                report.warn(f"{eid} 的 text {span!r} 未出现在 {ref} 中。")
        if item.get("type") not in EXPRESSION_TYPES:
            report.error(f"{eid} 的 type 无效：{item.get('type')!r}")
        if item.get("register") is None:
            report.error(f"{eid} 缺少 register。")
        if item.get("type") in {"idiom", "slang"} and not item.get("literalMeaning"):
            report.warn(f"{eid} 是 {item.get('type')}，但缺少 literalMeaning。")

    for item in grammar:
        if not isinstance(item, dict):
            continue
        gid = item.get("id", "?")
        refs = item.get("sentenceRefs") or []
        if not refs:
            report.error(f"{gid} 没有 sentenceRefs。")
        for ref in refs:
            if ref not in sentence_text:
                report.error(f"{gid} 引用了不存在的句子：{ref}")

    for item in exercises:
        if not isinstance(item, dict):
            continue
        xid = item.get("id", "?")
        if item.get("type") not in EXERCISE_TYPES:
            report.error(f"{xid} 的 type 无效：{item.get('type')!r}")
        answer = item.get("answer")
        if not isinstance(answer, dict) or not any(
            key in answer for key in ("key", "model", "rubric")
        ):
            report.error(f"{xid} 没有可判定的答案（key/model/rubric）。")
        elif "rubric" in answer and len(answer.get("rubric") or []) < 2:
            report.warn(f"{xid} 的 rubric 少于两条标准。")
        for ref in item.get("relatedSentences") or []:
            if ref not in sentence_text:
                report.error(f"{xid} 引用了不存在的句子：{ref}")
        for ref in item.get("relatedVocabulary") or []:
            if ref not in id_sets["vocabulary"]:
                report.error(f"{xid} 引用了不存在的词汇：{ref}")
        for ref in item.get("relatedExpressions") or []:
            if ref not in id_sets["expressions"]:
                report.error(f"{xid} 引用了不存在的表达：{ref}")
        for ref in item.get("relatedGrammar") or []:
            if ref not in id_sets["grammar"]:
                report.error(f"{xid} 引用了不存在的语法条目：{ref}")

    # Priority distribution.
    priorities = [i.get("priority") for i in vocab if isinstance(i, dict)]
    high = sum(1 for p in priorities if p == "high")
    if priorities and high > len(priorities) / 3:
        report.warn(
            f"词汇 high 优先级过多：{high}/{len(priorities)}（建议不超过三分之一）。"
        )


def check_source_text(doc: dict, source_path: Path, report: Report) -> None:
    try:
        raw = source_path.read_text(encoding="utf-8")
    except OSError as exc:
        report.error(f"无法读取原文文件：{exc}")
        return

    declared = doc.get("source", {}) if isinstance(doc.get("source"), dict) else {}
    stored = declared.get("text", "")
    if isinstance(stored, str) and stored:
        if normalize(stored) != normalize(raw):
            report.warn("source.text 与 --source 文件在空白规范化后仍不一致。")
        if declared.get("characterCount") not in {None, len(stored)}:
            report.warn(
                f"source.characterCount={declared.get('characterCount')}，"
                f"实际字符数={len(stored)}。"
            )

    sentences = [s for s in doc.get("sentences", []) if isinstance(s, dict)]
    rebuilt = " ".join(str(s.get("text", "")) for s in sentences)

    if normalize(rebuilt) == normalize(raw):
        report.note("原文完整性通过：句子拼接与源文件一致（空白规范化后）。")
        return

    if squash(rebuilt) == squash(raw):
        report.warn("原文仅在空白层面有差异；语义内容一致。")
        return

    report.error("原文完整性失败：句子拼接与源文件不一致。")
    if declared.get("integrity") == "modified-flag":
        report.warn("source.integrity 已标记 modified-flag；请确认差异是有意披露的。")

    a = normalize(rebuilt)
    b = normalize(raw)
    limit = min(len(a), len(b))
    index = next((i for i in range(limit) if a[i] != b[i]), limit)
    start = max(0, index - 40)
    report.error(f"首个差异附近 —— 文档：…{a[start:index + 40]!r}")
    report.error(f"首个差异附近 —— 原文：…{b[start:index + 40]!r}")
    report.error(f"长度：文档 {len(a)} 字符，原文 {len(b)} 字符。")


def check_counts_and_qa(doc: dict, report: Report) -> None:
    sentences = [s for s in doc.get("sentences", []) if isinstance(s, dict)]
    source = doc.get("source", {}) if isinstance(doc.get("source"), dict) else {}
    declared_count = source.get("sentenceCount")
    if isinstance(declared_count, int) and declared_count != len(sentences):
        report.warn(
            f"source.sentenceCount={declared_count}，实际句子数={len(sentences)}。"
        )

    qa = doc.get("qa")
    if not isinstance(qa, dict):
        report.error("qa 缺失或不是对象。")
        return
    checks = qa.get("checks") or []
    statuses = [c.get("status") for c in checks if isinstance(c, dict)]
    if len(checks) < 11:
        report.warn(f"QA 检查项为 {len(checks)} 条，规范要求 11 条。")
    if "fail" in statuses and qa.get("summary") != "fail":
        report.warn("QA 存在 fail，但 summary 不是 fail。")
    if any(s in {"unverified", "not-applicable"} for s in statuses) and qa.get("summary") == "pass":
        report.warn("QA 存在 unverified/not-applicable，但 summary 为 pass。")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a learning document.")
    parser.add_argument("document", type=Path)
    parser.add_argument("--source", type=Path, help="Source text file for integrity check.")
    parser.add_argument(
        "--schema-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "schemas",
    )
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors.")
    parser.add_argument("--json", action="store_true", help="Emit a JSON report.")
    args = parser.parse_args()

    report = Report()

    if not args.document.exists():
        report.error(f"文档不存在：{args.document}")
    else:
        try:
            doc = load_json(args.document)
        except json.JSONDecodeError as exc:
            report.error(f"JSON 解析失败：{exc}")
            doc = None
        if doc is not None and check_top_level(doc, report):
            check_schema(doc, args.schema_dir, report)
            check_ids_and_refs(doc, report)
            check_counts_and_qa(doc, report)
            if args.source:
                check_source_text(doc, args.source, report)

    failed = bool(report.errors) or (args.strict and bool(report.warnings))

    if args.json:
        payload = {
            "document": str(args.document),
            "source": str(args.source) if args.source else None,
            "errors": report.errors,
            "warnings": report.warnings,
            "notes": report.notes,
            "status": "fail" if failed else ("pass-with-warnings" if report.warnings else "pass"),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for note in report.notes:
            print(f"NOTE: {note}")
        for warning in report.warnings:
            print(f"WARN: {warning}")
        for error in report.errors:
            print(f"ERROR: {error}")
        status = "FAIL" if failed else ("PASS (with warnings)" if report.warnings else "PASS")
        print(
            f"\n{status}: {len(report.errors)} error(s), "
            f"{len(report.warnings)} warning(s) — {args.document}"
        )

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
