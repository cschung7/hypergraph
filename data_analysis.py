import yfinance as yf
import pandas as pd
import numpy as np
import networkx as nx
from typing import List


def fetch_ticker_data(tickers: List[str]) -> pd.DataFrame:
    """Fetch historical close prices and fundamentals for tickers."""
    data = yf.Tickers(tickers)
    price = data.history(period="1y")['Close']
    info = {t: data.tickers[t].info for t in tickers}
    fundamentals = pd.DataFrame(info).T
    price.columns = price.columns.droplevel(0)  # yfinance returns multiindex
    return price, fundamentals


def categorize_series(s: pd.Series) -> pd.Series:
    """Categorize values into quantiles."""
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    return s.apply(lambda x: -1 if x <= q1 else (1 if x >= q3 else 0))


def build_correlation_graph(price: pd.DataFrame) -> nx.Graph:
    returns = price.pct_change().dropna(how='all')
    corr = returns.corr().fillna(0)
    G = nx.from_pandas_adjacency(corr)
    return G


def fiedler_value(G: nx.Graph) -> float:
    L = nx.normalized_laplacian_matrix(G).todense()
    eigvals = np.linalg.eigvalsh(L)
    eigvals.sort()
    if len(eigvals) < 2:
        return 0
    return float(eigvals[1])


def main():
    # Example: fetch tickers from S&P500 (this is limited)
    tickers = list(yf.Ticker('^GSPC').constituents.keys())[:100]  # limit for demo
    price, fundamentals = fetch_ticker_data(tickers)

    fundamentals['per_category'] = categorize_series(fundamentals['trailingPE'])
    fundamentals['pbr_category'] = categorize_series(fundamentals['priceToBook'])
    fundamentals['eps_category'] = categorize_series(fundamentals['trailingEps'])
    fundamentals['capsize_category'] = categorize_series(fundamentals['marketCap'])

    G = build_correlation_graph(price)
    fval = fiedler_value(G)

    print(f"Fiedler value: {fval}")
    print(fundamentals[['sector', 'industry', 'per_category', 'pbr_category', 'eps_category', 'capsize_category']].head())

if __name__ == "__main__":
    main()
