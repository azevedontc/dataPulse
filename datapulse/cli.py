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
DEFAULT_CITY = os.getenv("CITY", "Medianeira")
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
    source: str = typer.Option(DEFAULT_SOURCE, help="Fonte: 'weather' ou 'fx'."),
    city: str = typer.Option(DEFAULT_CITY, help="Cidade (para 'weather')."),
    base: str = typer.Option(DEFAULT_BASE, help="Moeda base (para 'fx', ex.: BRL)."),
    quote: str = typer.Option(
        DEFAULT_QUOTE, help="Moeda cotada (para 'fx', ex.: USD)."
    ),
    days: int = typer.Option(DEFAULT_DAYS, help="Número de dias (>0)."),
    out_dir: str = typer.Option(DEFAULT_OUT, help="Diretório de saída."),
):
    """DataPulse - daily data insights"""
    logging.info(
        "Run start: source=%s city=%s base=%s quote=%s days=%s",
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
        # import só quando precisa
        from .sources.weather import WeatherSource

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
        )

    elif source == "fx":
        try:
            from .sources.fx import FxSource
        except ModuleNotFoundError:
            typer.secho(
                "Fonte 'fx' não encontrada (datapulse/sources/fx.py).",
                fg=typer.colors.RED,
            )
            raise

        src = FxSource()
        raw = src.fetch(base=base, quote=quote, days=days)
        daily = src.transform(raw)
        md_path = visualize_and_write(
            daily,  # tem colunas: date, rate, change_pct
            title=f"FX • {base}/{quote}",
            out_dir=out_dir,
            y_col="rate",
            y_label=f"Rate {base}/{quote}",
            image_suffix="fx",
        )

    else:
        typer.secho("Unknown source. Use 'weather' or 'fx'.", fg=typer.colors.RED)
        raise typer.Exit(1)

    build_reports_index(out_dir)
    typer.secho(f"Report generated: {md_path}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    typer.run(main)
