from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def visualize_and_write(
    daily_df: pd.DataFrame, *, title: str, out_dir="reports"
) -> Path:
    out_dir = Path(out_dir)
    img_dir = out_dir / "img"
    img_dir.mkdir(parents=True, exist_ok=True)

    # gráfico
    fig = plt.figure()
    x = daily_df["date"].astype(str)
    plt.plot(x, daily_df["avg_c"], marker="o")
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Avg temp (°C)")
    img_path = img_dir / f"{date.today()}_weather.png"
    fig.savefig(img_path, bbox_inches="tight")
    plt.close(fig)

    # markdown
    md_path = out_dir / f"{date.today()}.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"![chart](/reports/img/{img_path.name})\n\n")
        f.write(daily_df.to_markdown(index=False))
        f.write("\n")
    return md_path
