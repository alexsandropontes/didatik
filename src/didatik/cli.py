"""CLI do Didatik — comandos sync, upgrade, version e validate."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from didatik import __version__
from didatik.sync import registry_path, sync_runtime

app = typer.Typer(
    name="didatik",
    help="🎓 Didatik — Framework Educacional Learn Run Fly",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()

DIDATIK_GIT = "git+ssh://git@github.com/alexsandropontes/didatik.git#subdirectory=src"


@app.command()
def version() -> None:
    """Mostra a versão do Didatik."""
    console.print(f"🎓 Didatik [cyan]v{__version__}[/cyan]")


@app.command()
def sync(
    force: bool = typer.Option(
        False, "--force", "-f", help="Sobrescreve runtime existente (nunca toca cursos/)"
    ),
) -> None:
    """Instala/atualiza o runtime Didatik (.agent, CLAUDE.md, templates, scripts) e a mini plataforma (platform/) no projeto local."""
    console.print(Panel.fit("[bold cyan]🎓 Didatik: Sync do Runtime Educacional[/bold cyan]"))
    target = Path.cwd()

    if (target / ".agent").exists() and not force:
        console.print("[yellow]![/yellow] Runtime já existe. Use [bold]--force[/bold] para atualizar.")
        raise typer.Exit(code=1)

    try:
        stats = sync_runtime(target, force=force)
    except Exception as exc:  # pragma: no cover
        console.print(f"[red]Erro na sincronização: {exc}[/red]")
        raise typer.Exit(code=1) from exc

    table = Table(title="Artefatos sincronizados", show_lines=False)
    table.add_column("Artefato", style="bold")
    table.add_column("Status")
    labels = {
        ".agent": "Runtime educacional (agentes, comandos, skills)",
        "CLAUDE.md": "Root instruction",
        "templates": "Contrato (schemas + templates)",
        "scripts": "Validador Python/UV",
        "platform": "Mini plataforma Vue 3",
        "docs": "Documentação (Guias de Usuário e Dev)",
        "run": "Scripts de execução (run.sh / run.ps1)",
        "migracao": "Migração 1:1 (curso/ → cursos/<slug>/)",
        "cursos": "Pasta de cursos (multi-curso)",
    }
    for key, label in labels.items():
        val = stats.get(key, 0)
        if key in ("cursos", "migracao"):
            if key == "migracao":
                status = "[green]realizada[/green]" if val else "[dim]não aplicável[/dim]"
            else:
                status = "[green]criada (vazia)[/green]" if val else "[blue]preservada[/blue]"
        else:
            status = "[green]atualizado[/green]" if val else "[dim]sem alteração[/dim]"
        table.add_row(label, status)
    console.print(table)

    if stats.get("platform"):
        console.print(
            "\n[yellow]⚠️  Primeira vez? Instale as dependências da plataforma:[/yellow]"
            "\n   [bold]cd platform && npm install[/bold]"
        )
    console.print(
        "\n[green]✅ Runtime sincronizado.[/green] "
        "Crie seu curso com: [bold]*dk course create \"<descrição>\"[/bold]"
    )


@app.command()
def upgrade() -> None:
    """Atualiza o motor (CLI) do Didatik globalmente via GitHub e sincroniza o projeto local."""
    console.print(Panel.fit("[bold magenta]🎓 Didatik: Global Upgrade Protocol[/bold magenta]"))

    console.print(f"Versão instalada: [cyan]v{__version__}[/cyan]")
    console.print(f"Fonte: [dim]{DIDATIK_GIT}[/dim]")

    cmd = ["uv", "tool", "install", "--force", "--upgrade", "--python", "3.13", DIDATIK_GIT]
    if not typer.confirm("Atualizar o motor globalmente via GitHub?", default=True):
        console.print("[yellow]Upgrade cancelado.[/yellow]")
        raise typer.Exit()

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        console.print(f"[red]Erro no upgrade:[/red]\n{result.stdout}\n{result.stderr}")
        raise typer.Exit(code=1)

    console.print("[bold green]Motor atualizado. Sincronizando o projeto local...[/bold green]")
    sync(force=True)


@app.command()
def validate(
    path: Path = typer.Option(
        None, "--path", "-p", help="Caminho da pasta de cursos (default: ./cursos)"
    ),
) -> None:
    """Valida o contrato de estrutura do curso (atalho para o validador)."""
    reg = registry_path()
    validator = reg / "scripts" / "validate_structure.py"
    if not validator.exists():
        console.print("[red]Validador não encontrado no registry.[/red]")
        raise typer.Exit(code=1)

    local_validator = Path.cwd() / "scripts" / "validate_structure.py"
    target = local_validator if local_validator.exists() else validator
    curso = str(path) if path else str(Path.cwd() / "cursos")

    result = subprocess.run([sys.executable, str(target), curso])
    raise typer.Exit(code=result.returncode)


if __name__ == "__main__":
    app()
