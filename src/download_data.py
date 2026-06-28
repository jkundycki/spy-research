from pathlib import Path

import pandas as pd
import yfinance as yf


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def download_data(ticker: str, start_date: str) -> pd.DataFrame:
    print(f"Downloading {ticker} data...")

    df = yf.download(
        ticker,
        start=start_date,
        auto_adjust=False,
        progress=False,
    )

    if df.empty:
        raise ValueError(f"No data downloaded for {ticker}")

    return df


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    df = df.reset_index()

    return df


def validate_data(df: pd.DataFrame) -> None:
    required_columns = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if df["Date"].isna().any():
        raise ValueError("Date column contains missing values")

    if df["Close"].isna().any():
        raise ValueError("Close column contains missing values")

    if not df["Date"].is_monotonic_increasing:
        raise ValueError("Date column is not sorted ascending")


def save_data(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} rows to {output_path}")


def main() -> None:
    ticker = "SPY"
    start_date = "2000-01-01"

    project_root = get_project_root()
    output_path = project_root / "data" / "raw" / "spy.csv"

    df = download_data(ticker=ticker, start_date=start_date)
    df = clean_columns(df)
    validate_data(df)
    save_data(df, output_path)

    print(df.head())


if __name__ == "__main__":
    main()