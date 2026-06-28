from pathlib import Path

import yfinance as yf


def download_spy_data() -> None:
    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "spy.csv"

    print("Downloading SPY data...")

    spy = yf.download(
        "SPY",
        start="2000-01-01",
        auto_adjust=False,
        progress=False,
    )

    if spy.empty:
        raise ValueError("No SPY data was downloaded.")

    spy.to_csv(output_path)

    print(f"Saved {len(spy)} rows to {output_path}")
    print(spy.head())


if __name__ == "__main__":
    download_spy_data()