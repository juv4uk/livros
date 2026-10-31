#!/usr/bin/env python3
"""Звірення українського перекладу з португальським джерелом."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1] / "ashtavakra gita"
CHAPTERS = ("prelude", "ch1", "ch2", "ch7", "ch8", "ch9")
MARKER = re.compile(r"(?m)^\[(\d+\.\d+)\]\s*")


def extract(path: Path) -> dict[str, str]:
    data = path.read_text(encoding="utf-8")
    matches = list(MARKER.finditer(data))
    verses = {}
    for n, match in enumerate(matches):
        end = matches[n + 1].start() if n + 1 < len(matches) else len(data)
        number = match.group(1)
        body = data[match.end():end].strip()
        if number in verses:
            raise ValueError(f"{path}: повторено {number}")
        if not body or not re.search(r"[^\W\d_]", body, flags=re.UNICODE):
            raise ValueError(f"{path}: порожній текст {number}")
        verses[number] = body
    if not verses:
        raise ValueError(f"{path}: немає віршів")
    return verses


def main() -> int:
    errors = []
    total = 0
    for chapter in CHAPTERS:
        try:
            source = extract(ROOT / "chs" / f"{chapter}.tex")
            target = extract(ROOT / "uk" / "chs" / f"{chapter}.tex")
            if list(source) != list(target):
                errors.append(f"{chapter}: різна нумерація: {list(source)} != {list(target)}")
            else:
                print(f"OK {chapter}: {len(target)}")
                total += len(target)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(str(exc))
    if errors:
        for error in errors:
            print(f"ПОМИЛКА: {error}", file=sys.stderr)
        return 1
    print(f"Перевірено {total} віршів")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
