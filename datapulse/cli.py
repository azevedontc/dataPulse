# datapulse/cli.py
import logging
import os
from pathlib import Path

import typer
from dotenv import load_dotenv

from .pipeline import visualize_and_write
from .utils import build_reports_index

# ----- config/env -----
load_dotenv()
DEFAULT_CITY = os.getenv("CITY", "São Paulo")
DEFAULT_DAYS = int(os.getenv("DAYS", "3"))
DEFAULT_OUT = os.getenv("REPORTS_DIR", "reports")
DEFAULT_SOURCE = os.getenv("DEFAULT_SOURCE", "weather")
DEFAULT_BASE = os.getenv("BASE", "BRL")
DEFAULT_QUOTE = os.getenv("QUOTE", "USD")

# ----- logging -----
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "datapulse.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def main(
    source: str = typer.Option(
        DEFAULT_SOURCE, help="Fonte: 'weather' ou 'fx' ou 'aqi'."
    ),
    city: str = typer.Option(DEFAULT_CITY, help="Cidade (para 'weather'/'aqi')."),
    base: str = typer.Option(DEFAULT_BASE, help="Moeda base (para 'fx')."),
    quote: str = typer.Option(DEFAULT_QUOTE, help="Moeda cotada (para 'fx')."),
    days: int = typer.Option(DEFAULT_DAYS, help="Número de dias (>0)."),
    out_dir: str = typer.Option(DEFAULT_OUT, help="Diretório de saída."),
    no_csv: bool = typer.Option(False, help="Não salvar CSV."),
    no_plot: bool = typer.Option(False, help="Não salvar PNG."),
):
    """DataPulse - daily data insights"""
    logging.info(
        "Run start: src=%s city=%s base=%s quote=%s days=%s",
        source,
        city,
        base,
        quote,
        days,
    )
    if days <= 0:
        typer.secho("'days' must be > 0", fg=typer.colors.RED)
        raise typer.Exit(2)

    if source == "weather":
        from .sources.weather import WeatherSource  # lazy import

        src = WeatherSource()
        raw = src.fetch(city=city, days=days)
        daily = src.transform(raw)
        md_path = visualize_and_write(
            daily,
            title=f"Weather • {city}",
            out_dir=out_dir,
            y_col="avg_c",
            y_label="Avg temp (°C)",
            image_suffix="weather",
            write_csv=not no_csv,
            write_plot=not no_plot,
        )

    elif source == "fx":
        from .sources.fx import FxSource  # lazy import

        src = FxSource()
        raw = src.fetch(base=base, quote=quote, days=days)
        daily = src.transform(raw)
        md_path = visualize_and_write(
            daily,
            title=f"FX • {base}/{quote}",
            out_dir=out_dir,
            y_col="rate",
            y_label=f"Rate {base}/{quote}",
            image_suffix="fx",
            write_csv=not no_csv,
            write_plot=not no_plot,
        )

    elif source == "aqi":
        from .sources.aqi import AQISource  # lazy import

        src = AQISource()
        raw = src.fetch(city=city, days=days)
        daily = src.transform(raw)
        md_path = visualize_and_write(
            daily,
            title=f"AQI • {city}",
            out_dir=out_dir,
            y_col="aqi",
            y_label="Air Quality Index",
            image_suffix="aqi",
            write_csv=not no_csv,
            write_plot=not no_plot,
        )

    else:
        typer.secho(
            "Unknown source. Use 'weather', 'fx' or 'aqi'.", fg=typer.colors.RED
        )
        raise typer.Exit(1)

    build_reports_index(out_dir)
    typer.secho(f"Report generated: {md_path}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    typer.run(main)
