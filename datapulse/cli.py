import typer

from .pipeline import visualize_and_write
from .sources.weather import WeatherSource


def main(
    source: str = "weather",
    city: str = "São Paulo",
    days: int = 3,
):
    if source != "weather":
        typer.secho(
            "Only 'weather' source is available in MVP.", fg=typer.colors.YELLOW
        )
        raise typer.Exit(1)

    src = WeatherSource()
    raw = src.fetch(city=city, days=days)
    daily = src.transform(raw)
    md_path = visualize_and_write(daily, title=f"Weather • {city}")
    typer.secho(f"Report generated: {md_path}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    typer.run(main)
