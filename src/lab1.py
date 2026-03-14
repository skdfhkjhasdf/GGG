#!/usr/bin/env python3
"""Лабораторная работа: базовая статистика по оценкам."""

from __future__ import annotations

import csv
import statistics
import sys
from pathlib import Path


def load_grades(path: Path) -> list[tuple[str, float]]:
    rows: list[tuple[str, float]] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if "name" not in reader.fieldnames or "grade" not in reader.fieldnames:
            raise ValueError("CSV должен содержать столбцы name и grade")
        for row in reader:
            name = (row.get("name") or "").strip()
            grade_raw = (row.get("grade") or "").strip()
            if not name:
                continue
            try:
                grade = float(grade_raw)
            except ValueError as exc:
                raise ValueError(f"Некорректная оценка: {grade_raw}") from exc
            rows.append((name, grade))
    if not rows:
        raise ValueError("Файл не содержит оценок")
    return rows


def summarize(grades: list[tuple[str, float]]) -> dict[str, float]:
    values = [grade for _, grade in grades]
    mean_value = statistics.mean(values)
    median_value = statistics.median(values)
    stdev_value = statistics.pstdev(values)
    return {
        "mean": mean_value,
        "median": median_value,
        "stdev": stdev_value,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("Использование: python3 src/lab1.py data/grades.csv")
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Файл не найден: {path}")
        return 1

    try:
        grades = load_grades(path)
    except ValueError as exc:
        print(f"Ошибка: {exc}")
        return 1

    stats = summarize(grades)
    above_avg = [name for name, grade in grades if grade > stats["mean"]]

    print("Статистика")
    print(f"Среднее: {stats['mean']:.2f}")
    print(f"Медиана: {stats['median']:.2f}")
    print(f"Стандартное отклонение: {stats['stdev']:.2f}")
    print()
    print("Выше среднего:")
    for name in above_avg:
        print(f"- {name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
