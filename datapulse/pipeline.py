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
    write_plot: bool = True,
) -> Path:
    """
    Salva gráfico (PNG) e/ou CSV e o relatório Markdown.
    df precisa ter 'date' e a coluna informada em y_col.
    """
    out_path = Path(out_dir)
    img_dir = out_path / "img"
    img_dir.mkdir(parents=True, exist_ok=True)

    img_name = f"{date.today()}_{image_suffix}.png"
    csv_name = f"{date.today()}_{image_suffix}.csv"

    # --- gráfico ---
    if write_plot:
        x = df["date"].astype(str)
        fig = plt.figure(figsize=(8, 6))
        plt.plot(x, df[y_col], marker="o")
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel(y_label)
        fig.autofmt_xdate()
        plt.tight_layout()
        fig.savefig(img_dir / img_name, bbox_inches="tight")
        plt.close(fig)

    # --- csv ---
    if write_csv:
        df.to_csv(out_path / csv_name, index=False, encoding="utf-8")

    # --- markdown ---
    md_path = out_path / f"{date.today()}.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        if write_plot:
            f.write(f"![chart](/reports/img/{img_name})\n\n")
        f.write(df.to_markdown(index=False))
        f.write("\n")
    return md_path
