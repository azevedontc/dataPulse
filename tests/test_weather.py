from datapulse.sources.weather import WeatherSource


def test_transform_has_columns():
    src = WeatherSource()
    df = src.transform(src.fetch(days=1))
    assert {"date", "min_c", "max_c", "avg_c"}.issubset(df.columns)
