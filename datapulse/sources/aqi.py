# datapulse/sources/aqi.py
import time

import pandas as pd
import requests

from .base import DataSource
from .weather import WeatherSource  # reuso do geocoding


class AQISource(DataSource):
    """Qualidade do ar (US AQI) via Open-Meteo Air Quality API."""

    def name(self) -> str:
        return "aqi"

    def fetch(self, city: str = "São Paulo", days: int = 3, **_) -> pd.DataFrame:
        # Reaproveita o geocoding do WeatherSource
        lat, lon = WeatherSource()._geocode(city)  # noqa: SLF001

        url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "us_aqi",
            "forecast_days": days,
            "timezone": "auto",
        }

        last = None
        for attempt in range(3):
            try:
                r = requests.get(url, params=params, timeout=30)
                r.raise_for_status()
                js = r.json()
                if "hourly" not in js or "us_aqi" not in js["hourly"]:
                    raise ValueError(f"Unexpected AQI payload: {js}")
                df = pd.DataFrame(
                    {"time": js["hourly"]["time"], "aqi": js["hourly"]["us_aqi"]}
                )
                df["time"] = pd.to_datetime(df["time"])
                return df
            except Exception as e:
                last = e
                time.sleep(2 * (attempt + 1))
        raise last

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out["date"] = out["time"].dt.date
        daily = out.groupby("date")["aqi"].mean().round(2).reset_index()
        return daily
