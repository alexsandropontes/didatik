"""Build hook do hatch: empacota o registry (runtime + plataforma) no wheel,
excluindo node_modules/dist/.venv/.git/__pycache__."""

from __future__ import annotations

from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

SKIP_DIRS = {"node_modules", "dist", ".venv", "__pycache__", ".git"}

REGISTRY_MAP = {
    ".agent": "educore/registry/.agent",
    "CLAUDE.md": "educore/registry/CLAUDE.md",
    "templates": "educore/registry/templates",
    "scripts": "educore/registry/scripts",
    "platform": "educore/registry/platform",
    "run.sh": "educore/registry/run.sh",
    "run.ps1": "educore/registry/run.ps1",
}


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data) -> None:
        root = Path(self.root)
        force_include = build_data.setdefault("force_include", {})
        for src_rel, dst_rel in REGISTRY_MAP.items():
            src = root / src_rel
            if not src.exists():
                continue
            if src.is_file():
                force_include[str(src)] = dst_rel
                continue
            for f in src.rglob("*"):
                if not f.is_file():
                    continue
                rel = f.relative_to(src)
                if any(part in SKIP_DIRS for part in rel.parts):
                    continue
                force_include[str(f)] = f"{dst_rel}/{rel.as_posix()}"
