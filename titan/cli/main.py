"""TITAN command-line interface."""

import shutil
from pathlib import Path
from typing import Annotated

import typer
import yaml
from pydantic import ValidationError
from rich.console import Console

from titan.core.config import load_config

app = typer.Typer(
    name="titan",
    help="Infrastructure Automation & Orchestration Platform",
    no_args_is_help=True,
)

console = Console()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_CONFIG = PROJECT_ROOT / "config" / "titan.example.yaml"


@app.callback()
def main() -> None:
    """TITAN — Automate, secure and operate infrastructure."""


@app.command()
def version() -> None:
    """Display TITAN version."""
    console.print("[bold cyan]TITAN[/bold cyan] version 0.1.0")


@app.command()
def init(
    config_path: Annotated[
        Path,
        typer.Option(
            "--config",
            "-c",
            help="Path of the configuration file to create.",
        ),
    ] = Path("config/titan.yaml"),
) -> None:
    """Initialize a local TITAN configuration."""

    if config_path.exists():
        console.print(f"[red]Configuration already exists:[/red] {config_path}")
        raise typer.Exit(code=1)

    if not EXAMPLE_CONFIG.is_file():
        console.print(f"[red]Example configuration not found:[/red] {EXAMPLE_CONFIG}")
        raise typer.Exit(code=1)

    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(EXAMPLE_CONFIG, config_path)
    except OSError as exc:
        console.print(f"[red]Unable to initialize configuration:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    console.print(f"[green]Configuration created:[/green] {config_path}")
    console.print("Edit the file before deploying your infrastructure.")


@app.command()
def validate(
    config_path: Annotated[
        Path,
        typer.Option(
            "--config",
            "-c",
            help="Path of the configuration file to validate.",
        ),
    ] = Path("config/titan.yaml"),
) -> None:
    """Validate the TITAN configuration."""

    try:
        config = load_config(config_path)
    except FileNotFoundError:
        console.print(f"[red]Configuration file not found:[/red] {config_path}")
        raise typer.Exit(code=1) from None
    except (ValidationError, ValueError, yaml.YAMLError) as exc:
        console.print("[red]Configuration validation failed.[/red]")
        console.print(str(exc))
        raise typer.Exit(code=1) from exc
    except OSError as exc:
        console.print(f"[red]Unable to read configuration:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    console.print("[green]Configuration is valid.[/green]")
    console.print(f"Project: {config.project.name}")
    console.print(f"Environment: {config.project.environment}")
    console.print(f"VLANs configured: {len(config.network.vlans)}")
