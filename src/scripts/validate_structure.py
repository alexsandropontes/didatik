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

MODULE_DIR_RE = re.compile(r"^\d{2}$")
MODULE_DIR_LEGACY_RE = re.compile(r"^\d{2}-[a-z0-9]+(-[a-z0-9]+)*$")
LESSON_FILE_RE = re.compile(r"^\d{2}-[a-z0-9]+(-[a-z0-9]+)*\.md$")
LRF_SECTIONS = ["## 🧠 Learn", "## 🏃 Run", "## 🚀 Fly"]
QUIZ_SECTION = "## 📝 Quiz"
QUIZ_MIN_QUESTIONS = 4
QUIZ_MAX_QUESTIONS = 6
QUIZ_OPTIONS_PER_QUESTION = 5
SLUG_MAX_LENGTH = 50      # slug do curso (proteção MAX_PATH 260, Windows 7/8)
LESSON_FILE_MAX = 40      # nome completo do arquivo de aula (incl. "NN-" e ".md")
MODULE_NAME_MAX = 30      # legado: nome completo da pasta do módulo (incl. "NN-")
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


def validate_quiz(lesson: Path, raw: str) -> int:
    """Valida a seção Quiz: 4-6 perguntas, exatamente uma (x) por pergunta."""
    match = re.search(rf"^{QUIZ_SECTION}\s*$", raw, re.MULTILINE)
    if not match:
        warning(f"{lesson.name}: seção '## 📝 Quiz' ausente (aula não concluirá na plataforma)")
        return 0

    quiz_block = raw[match.end():]
    questions = re.findall(
        r"\*\*\d+\.\s*.+?\*\*\s*\r?\n((?:\s*-\s*\([ xX]\).*\r?\n?)+)",
        quiz_block,
    )
    if not QUIZ_MIN_QUESTIONS <= len(questions) <= QUIZ_MAX_QUESTIONS:
        error(
            f"{lesson.name}: quiz com {len(questions)} perguntas "
            f"(exigido entre {QUIZ_MIN_QUESTIONS} e {QUIZ_MAX_QUESTIONS})"
        )
    for i, block in enumerate(questions, start=1):
        answers = re.findall(r"-\s*\(([ xX])\)", block)
        correct = sum(1 for a in answers if a.lower() == "x")
        if correct != 1:
            error(
                f"{lesson.name}: pergunta {i} do quiz tem {correct} opções '(x)' "
                f"(exigido exatamente 1)"
            )
        if len(answers) != QUIZ_OPTIONS_PER_QUESTION:
            error(
                f"{lesson.name}: pergunta {i} do quiz tem {len(answers)} opções "
                f"(exigido exatamente {QUIZ_OPTIONS_PER_QUESTION})"
            )
    return len(questions)


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

    validate_quiz(lesson, raw)

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


def discover_courses(courses_root: Path) -> list[Path]:
    """Descobre cada curso (subpasta com course.json) dentro de cursos/."""
    if not courses_root.exists():
        return []
    return sorted(
        d for d in courses_root.iterdir() if d.is_dir() and (d / "course.json").exists()
    )


def validate_course(course_root: Path) -> bool:
    """Valida um curso individual. Retorna True se aprovado."""
    global errors, warnings
    saved_errors, saved_warnings = errors, warnings
    errors, warnings = [], []

    validate_course_tree(course_root)

    ok = not errors
    print("-" * 60)
    print(f"📚 Curso: {course_root.name}")
    for msg in warnings:
        print(f"  {msg}")
    for msg in errors:
        print(f"  {msg}")
    print(f"  {'✅ APROVADO' if ok else '❌ REPROVADO'}")
    errors, warnings = saved_errors + errors, saved_warnings + warnings
    return ok


def validate_course_tree(course_root: Path) -> None:
    slug = course_root.name
    if len(slug) > SLUG_MAX_LENGTH:
        error(
            f"slug '{slug}' tem {len(slug)} caracteres (máximo {SLUG_MAX_LENGTH} — "
            f"risco de MAX_PATH 260 no Windows 7/8). Renomeie a pasta."
        )
    course = validate_course_json(course_root / "course.json")

    module_dirs = sorted(
        d for d in course_root.iterdir() if d.is_dir() and not d.name.startswith(".")
    )
    if not module_dirs:
        warning("curso sem módulos (curso vazio — normal antes de *ec course create)")

    total_lessons = 0
    total_duration = 0

    for expected_idx, module_dir in enumerate(module_dirs, start=1):
        if MODULE_DIR_LEGACY_RE.match(module_dir.name) and not MODULE_DIR_RE.match(module_dir.name):
            warning(
                f"pasta de módulo '{module_dir.name}': no formato LEGADO (NN-nome). "
                f"Renomeie para só a numeração '{module_dir.name[:2]}' — o título completo vive no module.json."
            )
        elif not MODULE_DIR_RE.match(module_dir.name):
            error(f"pasta de módulo com nome inválido: '{module_dir.name}' (esperado apenas a numeração: 01, 02, ...)")
            continue
        if MODULE_DIR_LEGACY_RE.match(module_dir.name) and len(module_dir.name) > MODULE_NAME_MAX:
            error(
                f"pasta de módulo '{module_dir.name}' tem {len(module_dir.name)} caracteres "
                f"(máximo {MODULE_NAME_MAX} — risco MAX_PATH). Renomeie para '{module_dir.name[:2]}'."
            )
        if int(module_dir.name[:2]) != expected_idx:
            warning(f"{module_dir.name}: numeração de módulo não sequencial (esperado {expected_idx:02d})")

        module_data = validate_module_json(module_dir) or {}

        lessons = sorted(
            f for f in module_dir.glob("*.md") if LESSON_FILE_RE.match(f.name)
        )
        for f in module_dir.glob("*.md"):
            if not LESSON_FILE_RE.match(f.name):
                error(f"{module_dir.name}/ nome de aula inválido: '{f.name}' (esperado NN-kebab-case.md)")
            elif len(f.name) > LESSON_FILE_MAX:
                error(
                    f"{module_dir.name}/{f.name} tem {len(f.name)} caracteres "
                    f"(máximo {LESSON_FILE_MAX} — risco MAX_PATH). Abrevie: 2-4 palavras-chave; "
                    f"título completo no frontmatter → title."
                )

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


def main() -> int:
    courses_root = (
        Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "cursos"
    )
    courses_root = courses_root.resolve()

    # Compat legado 1:1: se cursos/ não existe mas curso/ sim, valida curso/
    if not courses_root.exists():
        legacy = Path.cwd() / "curso"
        if legacy.exists():
            courses_root = legacy.resolve()
        else:
            print(f"🔴 Pasta de cursos não existe: {courses_root}")
            return 1

    course_dirs = discover_courses(courses_root)
    if not course_dirs:
        if (courses_root / "course.json").exists():
            course_dirs = [courses_root]  # legado 1:1 (raiz é o próprio curso)
        else:
            print(f"🟡 {courses_root} não tem cursos (vazio — normal antes de *ec course create)")
            return 0

    print("=" * 60)
    print("🎓 VALIDAÇÃO DO CONTRATO EDUCORE (multi-curso)")
    print(f"   Raiz: {courses_root} | Cursos: {len(course_dirs)}")
    print("=" * 60)

    results = [validate_course(d) for d in course_dirs]

    total_errors = len(errors)
    total_warnings = len(warnings)
    approved = sum(results)
    print("=" * 60)
    if total_errors:
        print(
            f"❌ REPROVADO — {approved}/{len(results)} aprovado(s), "
            f"{total_errors} erro(s), {total_warnings} aviso(s)"
        )
        return 1
    print(f"✅ APROVADO — {approved}/{len(results)} curso(s) com contrato respeitado")
    return 0


if __name__ == "__main__":
    sys.exit(main())
