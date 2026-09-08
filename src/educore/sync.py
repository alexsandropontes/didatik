"""Sincronização do runtime EduCore para o projeto local."""

from __future__ import annotations

import shutil
from importlib import resources
from pathlib import Path

# Pastas/arquivos do projeto que NUNCA são sobrescritos em hipótese alguma
PROTECTED = {"curso"}

SKIP_DIRS = {"node_modules", "dist", ".venv", "__pycache__", ".git"}

COURSE_PLACEHOLDER = """{
  "title": "Meu Curso EduCore",
  "subtitle": "Curso a ser criado pelos agentes educacionais",
  "author": "EduCore",
  "version": "0.1.0",
  "tags": ["educore"],
  "description": "Este curso ainda não foi planejado. Use *ec course create para criar o curso com os agentes @piaget, @freire e @bloom.",
  "objectives": [],
  "skills": [],
  "audience": "A definir pelo planejamento",
  "total_modules": 0,
  "total_lessons": 0,
  "total_duration": 0
}
"""


def registry_path() -> Path:
    """Retorna o caminho do registry empacotado dentro do pacote."""
    root = resources.files("educore") / "registry"
    return Path(str(root))


def _copy_tree(src: Path, dst: Path, force: bool, skip_dirnames: set[str] | None = None) -> bool:
    """Copia árvore preservando arquivos existentes quando force=False."""
    skip_dirnames = skip_dirnames or set()
    changed = False
    if not src.exists():
        return False
    for item in src.rglob("*"):
        if any(part in skip_dirnames for part in item.relative_to(src).parts):
            continue
        if item.is_dir():
            continue
        rel = item.relative_to(src)
        target = dst / rel
        if target.exists() and not force:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        changed = True
    return changed


def _clean_stale(dst_root: Path, src_root: Path, skip_dirnames: set[str] | None = None) -> int:
    """Remove em dst_root arquivos que não existem mais no src_root (force only)."""
    skip_dirnames = skip_dirnames or set()
    removed = 0
    if not dst_root.exists():
        return 0
    for item in dst_root.rglob("*"):
        if item.is_dir():
            continue
        rel = item.relative_to(dst_root)
        if any(part in skip_dirnames for part in rel.parts):
            continue
        if any(part in PROTECTED for part in rel.parts):
            continue
        if not (src_root / rel).exists():
            item.unlink()
            removed += 1
    # Remove diretórios vazios
    for d in sorted(dst_root.rglob("*"), reverse=True):
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()
    return removed


def sync_runtime(target: Path, force: bool = False) -> dict[str, int]:
    """Exporta o registry (.agent, CLAUDE.md, templates, scripts, platform) para target."""
    reg = registry_path()
    stats: dict[str, int] = {}

    # .agent/ (runtime educacional)
    stats[".agent"] = int(_copy_tree(reg / ".agent", target / ".agent", force))

    # CLAUDE.md
    claude_src = reg / "CLAUDE.md"
    claude_dst = target / "CLAUDE.md"
    copied_claude = False
    if claude_src.exists() and (force or not claude_dst.exists()):
        shutil.copy2(claude_src, claude_dst)
        copied_claude = True
    stats["CLAUDE.md"] = int(copied_claude)

    # templates/
    stats["templates"] = int(_copy_tree(reg / "templates", target / "templates", force))

    # scripts/ (validador)
    stats["scripts"] = int(_copy_tree(reg / "scripts", target / "scripts", force))

    # platform/ (mini plataforma — nunca copia node_modules/dist)
    stats["platform"] = int(
        _copy_tree(reg / "platform", target / "platform", force, SKIP_DIRS)
    )

    if force:
        _clean_stale(target / ".agent", reg / ".agent")
        _clean_stale(target / "templates", reg / "templates")
        _clean_stale(target / "platform", reg / "platform", SKIP_DIRS)

    # curso/ — cria placeholder apenas se NÃO existir (jamais sobrescreve)
    curso = target / "curso"
    if not curso.exists():
        curso.mkdir(parents=True)
        (curso / "course.json").write_text(COURSE_PLACEHOLDER, encoding="utf-8")
        stats["curso"] = 1
    else:
        stats["curso"] = 0

    return stats
