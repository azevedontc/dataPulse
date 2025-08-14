import pandas as pd
import requests

from .base import DataSource


class WeatherSource(DataSource):
    def __init__(self):
        self._base = "https://api.open-meteo.com/v1/forecast"

    def name(self) -> str:
        return "weather"

    def fetch(self, city: str = "São Paulo", days: int = 3, **_) -> pd.DataFrame:
        # coordenadas simples; você pode trocar por geocoding depois
        coords = {
            "São Paulo": (-23.55, -46.64),
            "Rio de Janeiro": (-22.91, -43.17),
            "Belo Horizonte": (-19.92, -43.94),
        }
        lat, lon = coords.get(city, coords["São Paulo"])
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m",
            "forecast_days": days,
            "timezone": "auto",
        }
        r = requests.get(self._base, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()["hourly"]
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
