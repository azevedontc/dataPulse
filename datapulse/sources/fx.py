import time
from datetime import date, timedelta

import pandas as pd
import requests

from .base import DataSource


class FxSource(DataSource):
    """Câmbio via exchangerate.host (gratuito, sem API key)."""

    def name(self) -> str:
        return "fx"

    def fetch(
        self, base: str = "BRL", quote: str = "USD", days: int = 7, **_
    ) -> pd.DataFrame:
        end = date.today()
        start = end - timedelta(days=days - 1)
        url = "https://api.exchangerate.host/timeseries"
        params = {
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "base": base,
            "symbols": quote,
        }

        last = None
        for attempt in range(3):
            try:
                r = requests.get(url, params=params, timeout=30)
                r.raise_for_status()
                rates = r.json()["rates"]
                rows = [{"date": d, "rate": rates[d][quote]} for d in sorted(rates)]
                df = pd.DataFrame(rows)
                df["date"] = pd.to_datetime(df["date"]).dt.date
                return df
            except requests.RequestException as e:
                last = e
                time.sleep(2 * (attempt + 1))
        raise last

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out["change_pct"] = out["rate"].pct_change().fillna(0) * 100
        return out
