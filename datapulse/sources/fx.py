# datapulse/sources/fx.py
import time
from datetime import date, timedelta

import pandas as pd
import requests

from .base import DataSource


class FxSource(DataSource):
    """Câmbio via Frankfurter API (estável, sem API key)."""

    def name(self) -> str:
        return "fx"

    def fetch(
        self, base: str = "BRL", quote: str = "USD", days: int = 7, **_
    ) -> pd.DataFrame:
        end = date.today()
        start = end - timedelta(days=days - 1)
        # Ex.: https://api.frankfurter.app/2025-08-30..2025-09-05?from=BRL&to=USD
        url = f"https://api.frankfurter.app/{start.isoformat()}..{end.isoformat()}"
        params = {"from": base, "to": quote}

        last = None
        for attempt in range(3):
            try:
                r = requests.get(url, params=params, timeout=30)
                r.raise_for_status()
                js = r.json()
                if "rates" not in js or not js["rates"]:
                    raise ValueError(f"Unexpected FX payload (no 'rates'): {js}")
                rows = []
                for d, m in sorted(js["rates"].items()):
                    # m é algo como {"USD": 0.19}
                    rows.append({"date": d, "rate": float(m[quote])})
                df = pd.DataFrame(rows)
                df["date"] = pd.to_datetime(df["date"]).dt.date
                return df
            except Exception as e:
                last = e
                time.sleep(2 * (attempt + 1))
        raise last

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out["change_pct"] = out["rate"].pct_change().fillna(0) * 100
        return out
