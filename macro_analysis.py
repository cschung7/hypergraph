import yfinance as yf
import pandas as pd

MACRO_TICKERS = {
    'sp500': '^GSPC',
    'nasdaq': '^IXIC',
    'vix': '^VIX',
    'jpy_usd': 'JPY=X',
    'euro_usd': 'EURUSD=X',
    'gold': 'GC=F',
    'wti': 'CL=F',
    'bond10y2y': 'T10Y2Y',
    'bond10y3m': 'T10Y3M',
}


def fetch_macro_data() -> pd.DataFrame:
    data = yf.download(list(MACRO_TICKERS.values()), period='1y', group_by='ticker')
    closes = {name: data[ticker]['Close'] for name, ticker in MACRO_TICKERS.items()}
    return pd.DataFrame(closes)


def main():
    macro = fetch_macro_data()
    print(macro.tail())


if __name__ == "__main__":
    main()
