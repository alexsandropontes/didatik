#!/usr/bin/env python3
"""Validador do Contrato EduCore.

Valida a estrutura da pasta curso/ contra o contrato definido em
templates/STRUCTURE.md e na Constituição (Seção II).

Uso: uv run scripts/validate_structure.py [caminho-do-curso]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MODULE_DIR_RE = re.compile(r"^\d{2}-[a-z0-9]+(-[a-z0-9]+)*$")
LESSON_FILE_RE = re.compile(r"^\d{2}-[a-z0-9]+(-[a-z0-9]+)*\.md$")
LRF_SECTIONS = ["## 🧠 Learn", "## 🏃 Run", "## 🚀 Fly"]
FRONTMATTER_KEYS = ["title", "module", "order", "tags", "duration"]

COURSE_REQUIRED = [
    "title", "subtitle", "author", "version", "tags", "description",
    "objectives", "skills", "audience", "total_modules", "total_lessons",
    "total_duration",
]
MODULE_REQUIRED = [
    "title", "order", "description", "objectives", "lessons", "duration",
]

errors: list[str] = []
warnings: list[str] = []


def error(msg: str) -> None:
    errors.append(f"🔴 {msg}")


def warning(msg: str) -> None:
    warnings.append(f"🟡 {msg}")


def validate_course_json(course_path: Path) -> dict | None:
    if not course_path.exists():
        error(f"{course_path} não encontrado (course.json é obrigatório)")
        return None
    try:
        data = json.loads(course_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        error(f"course.json com JSON inválido: {exc}")
        return None
    for key in COURSE_REQUIRED:
        if key not in data:
            error(f"course.json sem a chave obrigatória: '{key}'")
    return data


def validate_module_json(module_dir: Path) -> dict | None:
    module_json = module_dir / "module.json"
    if not module_json.exists():
        error(f"{module_dir.name}/ sem module.json")
        return None
    try:
        data = json.loads(module_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        error(f"{module_dir.name}/module.json com JSON inválido: {exc}")
        return None
    for key in MODULE_REQUIRED:
        if key not in data:
            error(f"{module_dir.name}/module.json sem a chave obrigatória: '{key}'")
    expected_order = int(module_dir.name[:2])
    if data.get("order") != expected_order:
        error(
            f"{module_dir.name}/module.json: order={data.get('order')} "
            f"deveria ser {expected_order} (prefixo da pasta)"
        )
    return data


def validate_lesson(module_dir: Path, lesson: Path, idx: int) -> int:
    raw = lesson.read_text(encoding="utf-8")

    for section in LRF_SECTIONS:
        if section not in raw:
            error(f"{lesson.name}: seção LRF ausente: '{section}'")

    positions = [raw.find(s) for s in LRF_SECTIONS]
    if -1 in positions:
        pass
    elif positions != sorted(positions):
        error(f"{lesson.name}: seções LRF fora de ordem (Learn → Run → Fly)")

    match = re.match(r"^---\r?\n(.*?)\r?\n---", raw, re.DOTALL)
    if not match:
        error(f"{lesson.name}: frontmatter ausente")
        return 0
    frontmatter = match.group(1)
    for key in FRONTMATTER_KEYS:
        if not re.search(rf"^{key}\s*:", frontmatter, re.MULTILINE):
            error(f"{lesson.name}: frontmatter sem '{key}'")

    expected_order = int(lesson.name[:2])
    order_match = re.search(r"^order:\s*(\d+)", frontmatter, re.MULTILINE)
    if order_match and int(order_match.group(1)) != expected_order:
        error(
            f"{lesson.name}: order={order_match.group(1)} "
            f"deveria ser {expected_order} (prefixo do arquivo)"
        )
    if idx + 1 != expected_order:
        warning(
            f"{lesson.name}: numeração não sequencial "
            f"(esperado {idx + 1:02d}, encontrado {expected_order})"
        )

    for img in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", raw):
        if img.startswith("http"):
            continue
        if not (module_dir / img).exists():
            error(f"{lesson.name}: imagem não encontrada: {img}")

    duration_match = re.search(r"^duration:\s*(\d+)", frontmatter, re.MULTILINE)
    return int(duration_match.group(1)) if duration_match else 0


def main() -> int:
    course_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "curso"
    course_root = course_root.resolve()

    if not course_root.exists():
        print(f"🔴 Pasta do curso não existe: {course_root}")
        return 1

    course = validate_course_json(course_root / "course.json")

    module_dirs = sorted(
        d for d in course_root.iterdir() if d.is_dir() and not d.name.startswith(".")
    )
    if not module_dirs:
        warning("curso/ não tem módulos (curso vazio — normal antes de *ec course create)")

    total_lessons = 0
    total_duration = 0

    for expected_idx, module_dir in enumerate(module_dirs, start=1):
        if not MODULE_DIR_RE.match(module_dir.name):
            error(f"pasta de módulo com nome inválido: '{module_dir.name}' (esperado NN-kebab-case)")
            continue
        if int(module_dir.name[:2]) != expected_idx:
            warning(f"{module_dir.name}: numeração de módulo não sequencial (esperado {expected_idx:02d})")

        module_data = validate_module_json(module_dir) or {}

        lessons = sorted(
            f for f in module_dir.glob("*.md") if LESSON_FILE_RE.match(f.name)
        )
        for f in module_dir.glob("*.md"):
            if not LESSON_FILE_RE.match(f.name):
                error(f"{module_dir.name}/ nome de aula inválido: '{f.name}' (esperado NN-kebab-case.md)")

        module_duration = 0
        for idx, lesson in enumerate(lessons):
            module_duration += validate_lesson(module_dir, lesson, idx)
        total_lessons += len(lessons)
        total_duration += module_duration

        if module_data and module_data.get("lessons") != len(lessons):
            error(
                f"{module_dir.name}/module.json: lessons={module_data.get('lessons')} "
                f"mas existem {len(lessons)} aulas"
            )
        if module_data and module_data.get("duration") != module_duration:
            warning(
                f"{module_dir.name}/module.json: duration={module_data.get('duration')} "
                f"mas a soma das aulas é {module_duration}"
            )

    if course:
        if course.get("total_modules") != len(module_dirs):
            error(
                f"course.json: total_modules={course.get('total_modules')} "
                f"mas existem {len(module_dirs)} módulos"
            )
        if course.get("total_lessons") != total_lessons:
            error(
                f"course.json: total_lessons={course.get('total_lessons')} "
                f"mas existem {total_lessons} aulas"
            )
        if course.get("total_duration") != total_duration:
            warning(
                f"course.json: total_duration={course.get('total_duration')} "
                f"mas a soma dos módulos é {total_duration}"
            )

    print("=" * 60)
    print("🎓 VALIDAÇÃO DO CONTRATO EDUCORE")
    print(f"   Curso: {course_root}")
    print(f"   Módulos: {len(module_dirs)} | Aulas: {total_lessons} | Duração: {total_duration} min")
    print("=" * 60)

    for msg in warnings:
        print(f"  {msg}")
    for msg in errors:
        print(f"  {msg}")

    if errors:
        print(f"\n❌ REPROVADO — {len(errors)} erro(s), {len(warnings)} aviso(s)")
        return 1
    print(f"\n✅ APROVADO — contrato respeitado ({len(warnings)} aviso(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
