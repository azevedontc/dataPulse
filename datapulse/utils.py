from pathlib import Path


def build_reports_index(out_dir: str = "reports") -> Path:
    """
    Cria/atualiza um índice (README.md) dentro de `out_dir`,
    listando todos os relatórios disponíveis.
    """
    out_path = Path(out_dir)
    out_path.mkdir(exist_ok=True)

    index_path = out_path / "README.md"
    lines = ["# 📊 Relatórios disponíveis\n"]

    for md_file in sorted(out_path.glob("*.md")):
        if md_file.name == "README.md":
            continue
        lines.append(f"- [{md_file.stem}]({md_file.name})")

    index_path.write_text("\n".join(lines), encoding="utf-8")
    return index_path
