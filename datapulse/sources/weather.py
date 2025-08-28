import json
import time
from datetime import date
from pathlib import Path

import pandas as pd
import requests

from .base import DataSource


class WeatherSource(DataSource):
    def __init__(self):
        self._base = "https://api.open-meteo.com/v1/forecast"
        self._geocode_base = "https://geocoding-api.open-meteo.com/v1/search"

    def name(self) -> str:
        return "weather"

    def _geocode(self, city: str) -> tuple[float, float]:
        """Busca lat/lon da cidade (1º resultado)."""
        r = requests.get(
            self._geocode_base,
            params={"name": city, "count": 1, "language": "pt", "format": "json"},
            timeout=30,
        )
        r.raise_for_status()
        js = r.json()
        if js.get("results"):
            first = js["results"][0]
            return float(first["latitude"]), float(first["longitude"])
        raise ValueError(f"City not found: {city}")

    def fetch(self, city: str = "São Paulo", days: int = 3, **_) -> pd.DataFrame:
        # cache simples por dia
        cache_dir = Path("data/cache")
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_key = cache_dir / f"{date.today()}_{city}_{days}.json"

        if cache_key.exists():
            raw = json.loads(cache_key.read_text(encoding="utf-8"))
        else:
            # tenta geocoding; se falhar, usa fallback mínimo
            try:
                lat, lon = self._geocode(city)
            except Exception:
                fallback = {
                    "São Paulo": (-23.55, -46.64),
                    "Curitiba": (-25.43, -49.27),
                    "Rio de Janeiro": (-22.91, -43.17),
                    "Belo Horizonte": (-19.92, -43.94),
                }
                lat, lon = fallback.get(city, fallback["São Paulo"])

            params = {
                "latitude": lat,
                "longitude": lon,
                "hourly": "temperature_2m",
                "forecast_days": days,
                "timezone": "auto",
            }

            last = None
            for attempt in range(3):
                try:
                    r = requests.get(self._base, params=params, timeout=30)
                    r.raise_for_status()
                    raw = r.json()
                    cache_key.write_text(json.dumps(raw), encoding="utf-8")
                    break
                except requests.RequestException as e:
                    last = e
                    time.sleep(2 * (attempt + 1))
            else:
                raise last

        data = raw["hourly"]
        df = pd.DataFrame({"time": data["time"], "temp": data["temperature_2m"]})
        df["time"] = pd.to_datetime(df["time"])
        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out["date"] = out["time"].dt.date
        daily = out.groupby("date")["temp"].agg(["min", "max", "mean"]).reset_index()
        daily.rename(
            columns={"min": "min_c", "max": "max_c", "mean": "avg_c"}, inplace=True
        )
        return daily
