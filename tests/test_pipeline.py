import pandas as pd

from datapulse.pipeline import visualize_and_write


def test_visualize_and_write(tmp_path):
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2025-01-01", "2025-01-02"]).date,
            "avg_c": [20, 21],
            "min_c": [18, 19],
            "max_c": [25, 26],
        }
    )
    md = visualize_and_write(df, title="Test", out_dir=tmp_path)
    assert md.exists()
