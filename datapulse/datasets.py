# datapulse/datasets.py
from __future__ import annotations

from pathlib import Path
from typing import Literal

import pandas as pd

Source = Literal["weather", "fx", "aqi"]


def load_reports_csvs(
    reports_dir: str = "reports", source: Source | None = None
) -> pd.DataFrame:
    """
    Lê CSVs de /reports e retorna um DataFrame unificado com colunas:
    ['date', 'value', 'source', 'file'].

    - weather: usa coluna 'avg_c'
    - fx:      usa coluna 'rate'
    - aqi:     usa coluna 'aqi'
    """
    p = Path(reports_dir)
    patterns = [p.glob("*.csv")] if source is None else [p.glob(f"*_{source}.csv")]

    frames: list[pd.DataFrame] = []
    for g in patterns:
        for f in sorted(g):
            sfx = f.stem.split("_")[-1]
            # detecta pela terminação do nome do arquivo
            if sfx not in {"weather", "fx", "aqi"}:
                continue
            if source and sfx != source:
                continue
            df = pd.read_csv(f)
            if "date" not in df.columns:
                continue
            if sfx == "weather" and "avg_c" in df.columns:
                series = df[["date", "avg_c"]].rename(columns={"avg_c": "value"})
            elif sfx == "fx" and "rate" in df.columns:
                series = df[["date", "rate"]].rename(columns={"rate": "value"})
            elif sfx == "aqi" and "aqi" in df.columns:
                series = df[["date", "aqi"]].rename(columns={"aqi": "value"})
            else:
                continue
            series["date"] = pd.to_datetime(series["date"]).dt.date
            series["source"] = sfx
            series["file"] = f.name
            frames.append(series)

    if not frames:
        return pd.DataFrame(columns=["date", "value", "source", "file"])

    out = pd.concat(frames, ignore_index=True)
    out = out.sort_values(["source", "date"]).reset_index(drop=True)
    return out
