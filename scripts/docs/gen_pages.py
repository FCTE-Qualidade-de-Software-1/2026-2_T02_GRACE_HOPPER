#!/usr/bin/env python3
"""Script para mkdocs-gen-files gerar index.md e contributing.md a partir da raiz."""

import re
from pathlib import Path

LINK_PATTERN = re.compile(
    r"\[(?P<text>(?:\[[^\]]*\]|`[^`]*`|[^\]\[])*)\]\((?P<target>[^\s\)]+)(?P<title>\s+[\"\x27][^\"\x27]*[\"\x27])?\)"
)


def _rewrite_target(target: str) -> str:
    """Reescreve o alvo de um link Markdown relativo ao contexto das páginas geradas."""
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", target) or target.startswith("mailto:"):
        return target

    if "#" in target:
        path, anchor = target.split("#", 1)
        anchor_suffix = "#" + anchor
    else:
        path = target
        anchor_suffix = ""

    if path.startswith("docs/"):
        new_path = path[len("docs/"):]
    elif path == "CONTRIBUTING.md":
        new_path = "contributing.md"
    elif path == "README.md":
        new_path = "index.md"
    else:
        new_path = path

    return new_path + anchor_suffix


def rewrite_links(text: str) -> str:
    """Função pura que reescreve links docs/X.md -> X.md, CONTRIBUTING.md -> contributing.md, README.md -> index.md."""
    def _replace(match: re.Match) -> str:
        text_content = match.group("text")
        target = match.group("target")
        title = match.group("title") or ""
        return f"[{text_content}]({_rewrite_target(target)}{title})"

    return LINK_PATTERN.sub(_replace, text)


def generate_pages() -> None:
    """Lê README.md e CONTRIBUTING.md e grava virtualmente no mkdocs-gen-files."""
    import mkdocs_gen_files

    root_dir = Path(__file__).resolve().parents[2]

    readme_file = root_dir / "README.md"
    if readme_file.exists():
        content = readme_file.read_text(encoding="utf-8")
        with mkdocs_gen_files.open("index.md", "w", encoding="utf-8") as f:
            f.write(rewrite_links(content))

    contributing_file = root_dir / "CONTRIBUTING.md"
    if contributing_file.exists():
        content = contributing_file.read_text(encoding="utf-8")
        with mkdocs_gen_files.open("contributing.md", "w", encoding="utf-8") as f:
            f.write(rewrite_links(content))


if __name__ in ("__main__", "<run_path>"):
    generate_pages()
