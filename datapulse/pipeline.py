# datapulse/pipeline.py
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def visualize_and_write(
    df: pd.DataFrame,
    *,
    title: str,
    out_dir: str = "reports",
    y_col: str = "avg_c",
    y_label: str = "Value",
    image_suffix: str = "report",
    write_csv: bool = True,
) -> Path:
    """
    Salva gráfico + relatório Markdown (+ CSV opcional) e retorna o caminho do .md.
    df precisa ter uma coluna 'date' e a coluna passada em y_col.
    """
    out_path = Path(out_dir)
    img_dir = out_path / "img"
    img_dir.mkdir(parents=True, exist_ok=True)

    # --- gráfico ---
    x = df["date"].astype(str)
    fig = plt.figure(figsize=(8, 6))
    plt.plot(x, df[y_col], marker="o")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(y_label)
    fig.autofmt_xdate()
    plt.tight_layout()

    img_path = img_dir / f"{date.today()}_{image_suffix}.png"
    fig.savefig(img_path, bbox_inches="tight")
    plt.close(fig)

    # --- csv (opcional) ---
    if write_csv:
        csv_path = out_path / f"{date.today()}_{image_suffix}.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8")

    # --- markdown ---
    md_path = out_path / f"{date.today()}.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"![chart](/reports/img/{img_path.name})\n\n")
        f.write(df.to_markdown(index=False))
        f.write("\n")
    return md_path
