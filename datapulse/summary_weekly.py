from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def build_weekly_summary(reports_dir="reports", metric_prefix="weather"):
    p = Path(reports_dir)
    csvs = sorted(p.glob(f"*_{metric_prefix}.csv"), reverse=True)[:7]
    if not csvs:
        raise SystemExit("No CSVs found to summarize.")

    frames = []
    for c in csvs:
        df = pd.read_csv(c)
        if metric_prefix == "weather" and "avg_c" in df.columns:
            df = df[["date", "avg_c"]].rename(columns={"avg_c": "value"})
        elif metric_prefix == "fx" and "rate" in df.columns:
            df = df[["date", "rate"]].rename(columns={"rate": "value"})
        else:  # aqi
            df = df[["date", "aqi"]].rename(columns={"aqi": "value"})
        frames.append(df)

    agg = pd.concat(frames, ignore_index=True)
    agg["date"] = pd.to_datetime(agg["date"])
    out = agg.groupby(agg["date"].dt.date)["value"].mean().reset_index()

    img = p / f"img/{datetime.today().date()}_{metric_prefix}_weekly.png"
    img.parent.mkdir(exist_ok=True, parents=True)
    plt.figure(figsize=(8, 6))
    plt.plot(out["date"].astype(str), out["value"], marker="o")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.title(f"Weekly summary • {metric_prefix}")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.tight_layout()
    plt.savefig(img, bbox_inches="tight")
    plt.close()

    md = p / f"{datetime.today().date()}_{metric_prefix}_weekly.md"
    with md.open("w", encoding="utf-8") as f:
        f.write(f"# Weekly summary • {metric_prefix}\n\n")
        f.write(f"![chart](/reports/img/{img.name})\n\n")
        f.write(out.to_markdown(index=False))
        f.write("\n")
    return md
