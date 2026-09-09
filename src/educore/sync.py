"""Sincronização do runtime EduCore para o projeto local."""

from __future__ import annotations

import json
import re
import shutil
import unicodedata
from importlib import resources
from pathlib import Path

# Pastas/arquivos do projeto que NUNCA são sobrescritos em hipótese alguma
PROTECTED = {"cursos", "curso"}

# Scripts de execução entregues na raiz do projeto
RUN_FILES = ["run.sh", "run.ps1"]

SKIP_DIRS = {"node_modules", "dist", ".venv", "__pycache__", ".git"}


def slugify_title(title: str) -> str:
    """Gera slug a partir do título: sem acentos, kebab-case."""
    normalized = unicodedata.normalize("NFKD", title)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")
    return slug or "curso"


PLACEHOLDER_TITLE = "Meu Curso EduCore"


def migrate_legacy_curso(target: Path) -> str | None:
    """Migra estrutura 1:1 (curso/) para multi-curso (cursos/<slug>/).

    Retorna mensagem de migração ou None.
    """
    legacy = target / "curso"
    multi = target / "cursos"
    if not legacy.exists() or multi.exists():
        return None

    course_json = legacy / "course.json"
    has_content = any(
        d.is_dir() and not d.name.startswith(".") and d.name != "assets"
        for d in legacy.iterdir()
    ) if legacy.exists() else False

    if not has_content:
        # Legado vazio/placeholder: descarta e cria cursos/ limpo
        shutil.rmtree(legacy, ignore_errors=True)
        multi.mkdir(parents=True, exist_ok=True)
        return "estrutura antiga (curso/) vazia — criada cursos/ (multi-curso)"

    # Migra conteúdo para cursos/<slug>/
    title = PLACEHOLDER_TITLE
    if course_json.exists():
        try:
            title = json.loads(course_json.read_text(encoding="utf-8")).get("title", title)
        except (json.JSONDecodeError, OSError):
            pass
    slug = slugify_title(title)
    dest = multi / slug
    dest.mkdir(parents=True, exist_ok=True)
    for item in legacy.iterdir():
        shutil.move(str(item), str(dest / item.name))
    legacy.rmdir()
    return f"curso/ migrado para cursos/{slug}/ (slug gerado do título)"



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

    # run.sh / run.ps1 — sempre atualizados (executáveis)
    run_copied = 0
    for name in RUN_FILES:
        src = reg / name
        if src.exists():
            dst = target / name
            shutil.copy2(src, dst)
            if name.endswith(".sh"):
                dst.chmod(0o755)
            run_copied += 1
    stats["run"] = run_copied

    # cursos/ — migra legado 1:1 se necessário; cria vazio apenas se não existir
    migration = migrate_legacy_curso(target)
    stats["migracao"] = 1 if migration else 0
    cursos = target / "cursos"
    if not cursos.exists():
        cursos.mkdir(parents=True)
        stats["cursos"] = 1
    else:
        stats["cursos"] = 0

    return stats
